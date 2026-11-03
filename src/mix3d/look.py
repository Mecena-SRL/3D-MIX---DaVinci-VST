"""Pipeline gestita, come ACES per il colore.

  ingresso (IDT): ogni mic raddrizzato a neutro con la sua curva (mixer.correction_fir)
  spazio di lavoro: neutro, dove agiscono EQ di traccia e EQ del master
  uscita (look): carattere sonoro + EQ + compressore, scelti per tipo di progetto

Lo stato è nel progetto: "look" (id del preset), "look_intensita" (0-1) e, se si vuole
un carattere diverso da quello del preset, "look_carattere" ("" = nessuno).
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.signal import firwin2, oaconvolve

from . import devices, eq

DB_PATH = Path(__file__).parent / "data" / "looks.json"
TAPS = 1023
LIMIT_DB = 8.0


@lru_cache
def load() -> dict:
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def get(lid: str) -> dict:
    return next(lk for lk in load()["look"] if lk["id"] == lid)


def characters() -> dict[str, str]:
    """Caratteri disponibili: tipologie + microfoni del database con una curva."""
    out = {f"tipo:{k}": f"{c['nome']} ({c['nota']})" for k, c in load()["caratteri"].items()}
    out |= {f"mic:{k}": f"Suona come {m['nome']}" for k, m in devices.load()["microfoni"].items() if m.get("curva")}
    return out


def character_db(car: str, f) -> np.ndarray:
    """Curva del carattere, 0 dB a 1 kHz, limitata a ±LIMIT_DB."""
    kind, key = car.split(":", 1)
    if kind == "mic":
        mic = devices.load()["microfoni"][key]
        r = devices.response_db(mic, f) - devices.response_db(mic, [1000.0])[0]
    else:
        pts = np.array(load()["caratteri"][key]["curva"], float)
        r = np.interp(np.log10(np.maximum(f, 1)), np.log10(pts[:, 0]), pts[:, 1])
    return np.clip(r, -LIMIT_DB, LIMIT_DB)


@lru_cache(maxsize=32)
def character_fir(car: str, amount: float, sr: int) -> np.ndarray:
    f = np.linspace(0, sr / 2, 256)
    return firwin2(TAPS, f / (sr / 2), 10 ** (amount * character_db(car, f) / 20))


def compress(x: np.ndarray, comp: dict, sr: int, amount: float = 1.0) -> np.ndarray:
    """Compressore stereo collegato (RMS), rapporto e makeup scalati dall'intensità."""
    ratio = 1 + (comp.get("rapporto", 2) - 1) * amount
    lv = eq.level_db(x, sr, comp)
    g = -np.maximum(lv - comp.get("soglia_db", -20), 0) * (1 - 1 / ratio) + comp.get("makeup_db", 0) * amount
    hop = max(1, int(eq.FRAME_S * sr))
    g = np.repeat(g, hop)
    g = np.pad(g, (0, len(x) - len(g)), mode="edge") if len(g) else np.zeros(len(x))
    return x * (10 ** (g / 20))[:, None]


def scaled_eq(lk: dict, amount: float) -> list[dict]:
    return [{**b, "g": b.get("g", 0) * amount} for b in lk.get("eq", [])]


def _car(project: dict, lk: dict) -> str | None:
    return project.get("look_carattere", lk.get("carattere"))


def apply(x: np.ndarray, project: dict, sr: int) -> np.ndarray:
    lk, amt = get(project["look"]), float(project.get("look_intensita", 1.0))
    if amt <= 0:  # intensità 0 = neutro, anche per i filtri di taglio
        return x
    if car := _car(project, lk):
        x = oaconvolve(x, character_fir(car, round(amt, 2), sr)[:, None], axes=0)[TAPS // 2:][: len(x)]
    x = eq.process(x, scaled_eq(lk, amt), sr)
    if lk.get("comp"):
        x = compress(x, lk["comp"], sr, amt)
    return x.astype(np.float32)


def curve(project: dict, f) -> np.ndarray:
    """Risposta statica del look (senza compressore), per il grafico."""
    if not project.get("look") or project.get("look_intensita", 1.0) <= 0:
        return np.zeros(len(f))
    lk, amt = get(project["look"]), float(project.get("look_intensita", 1.0))
    r = eq.response_db(scaled_eq(lk, amt), f, project.get("sr", 48000))
    car = _car(project, lk)
    return r + (amt * character_db(car, np.asarray(f, float)) if car else 0)


def catalog() -> dict:
    return {"look": [{k: lk[k] for k in ("id", "nome", "progetto", "descrizione", "carattere")} for lk in load()["look"]],
            "caratteri": characters()}
