"""Database dispositivi: profili (registratore + microfono), curve e suggerimenti.

Il file `data/devices.json` è la fonte: qui solo lettura e calcoli derivati.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import numpy as np

DB_PATH = Path(__file__).parent / "data" / "devices.json"

# guadagno di default per ruolo (dB): la base regge il mix, il sync non si sente
ROLE_GAIN_DB = {"base": 0.0, "ambiente": -3.0, "spot": -6.0, "riferimento picchi": None,
                "riferimento bilanciamento": None, "sync": None}

# diagramma polare: a + (1-a) cos(theta)
POLAR_A = {"omni": 1.0, "cardioide": 0.5, "supercardioide": 0.37, "ipercardioide": 0.25,
           "figura8": 0.0, "ms": 0.5, "nessuno": 1.0}


@lru_cache
def load() -> dict:
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def profile(pid: str) -> dict:
    """Profilo completo: con le voci di registratore e microfono incorporate."""
    db = load()
    p = next((p for p in db["profili"] if p["id"] == pid), None)
    if p is None:
        raise KeyError(pid)
    rec = db["registratori"][p["registratore"]]
    return {**p, "rec": rec, "mic": db["microfoni"][p["microfono"]],
            "rischi_testo": chain_risks(p["registratore"], p["microfono"]),
            "gain_db": ROLE_GAIN_DB.get(p["ruolo"], -6.0)}


def chain_risks(rec_id: str, mic_id: str) -> list[str]:
    """Avvisi della catena: rischi del registratore + rischi del microfono."""
    db = load()
    keys = db["registratori"][rec_id].get("rischi", []) + db["microfoni"][mic_id].get("rischi", [])
    return [db["rischi"][k] for k in dict.fromkeys(keys)]


def response_db(mic: dict, freqs: np.ndarray) -> np.ndarray:
    """Risposta in frequenza stimata: curva digitalizzata se c'è, altrimenti
    passa-banda del 2° ordine sui limiti di banda del datasheet."""
    f = np.maximum(np.asarray(freqs, float), 1.0)
    if mic.get("curva"):
        pts = np.array(mic["curva"], float)
        return np.interp(np.log10(f), np.log10(pts[:, 0]), pts[:, 1])
    lo, hi = mic.get("banda", [20, 20000])
    hp = (f / lo) ** 4 / (1 + (f / lo) ** 4)
    lp = 1 / (1 + (f / hi) ** 4)
    return 10 * np.log10(hp * lp)


def correction_db(mic: dict, freqs: np.ndarray, limit: float = 6.0) -> np.ndarray:
    """EQ che porta il microfono verso il neutro, limitata a ±limit dB.
    Fuori banda non si spinge: si corregge solo dove il mic ha segnale."""
    r = response_db(mic, freqs)
    lo, hi = mic.get("banda", [20, 20000])
    inband = (np.asarray(freqs) >= lo) & (np.asarray(freqs) <= hi)
    return np.where(inband, np.clip(-r, -limit, limit), 0.0)


def polar_gain(mic: dict, theta: np.ndarray) -> np.ndarray:
    a = POLAR_A.get(mic.get("diagramma", "omni"), 1.0)
    return np.abs(a + (1 - a) * np.cos(theta))


def suggest(info: dict, top: int = 3) -> list[dict]:
    """Classifica i profili per un file: nome, codec, bit, canali.

    `info`: {name, codec, bits, sr, channels, ch_index (1-based, canale iniziale)}.
    Ritorna [{id, nome, score, motivi}], il migliore per primo.
    """
    db = load()
    out = []
    for p in db["profili"]:
        rec = db["registratori"][p["registratore"]]
        score, why = 0.0, []
        if any(re.search(rx, info.get("name", ""), re.I) for rx in p["file"]):
            score += 2; why.append("nome file")
        if info.get("codec") in rec.get("codec", []):
            score += 2; why.append(f"codec {info['codec']}")
        if info.get("bits") in rec.get("bit", []):
            score += 1; why.append(f"{info['bits']} bit")
        if info.get("bits") == 32 and 32 in rec.get("bit", []):
            score += 2; why.append("32 bit float")
        if info.get("sr") in rec.get("sr", []):
            score += 0.5
        if p["canali"] and info.get("ch_index") in p["canali"]:
            score += 1; why.append(f"canale {info['ch_index']}")
        out.append({"id": p["id"], "nome": p["nome"], "score": score, "motivi": why})
    out.sort(key=lambda s: -s["score"])
    best = max(out[0]["score"], 1e-9)
    for s in out:
        s["confidenza"] = round(s["score"] / best * min(best / 6, 1), 2)
    return out[:top]
