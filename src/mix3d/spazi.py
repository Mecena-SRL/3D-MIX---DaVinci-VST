"""Spazi 3D: 12 tipologie italiane incluse + spazi privati importati da file.

I file privati (schema "mix3d-spazio/1", *.mix3d-space.json) restano solo sul Mac,
in ~/.mix3d/spazi/: non sono nel pacchetto né nel repository.
"""
from __future__ import annotations

import json
import shutil
from functools import lru_cache
from pathlib import Path

BUILTIN = Path(__file__).parent / "data" / "spazi.json"
LOCAL = Path.home() / ".mix3d" / "spazi"
BANDS = {"125": "125", "250": "250", "500": "500", "1000": "1k", "2000": "2k", "4000": "4k"}


@lru_cache
def builtin() -> list[dict]:
    return json.loads(BUILTIN.read_text(encoding="utf-8"))["spazi"]


def normalize(j: dict) -> dict:
    """Converte un file "mix3d-spazio/1" nello schema interno; lo schema interno passa invariato."""
    if j.get("formato") != "mix3d-spazio/1":
        return j
    ac = j.get("acustica", {})
    mics = j.get("mic_consigliati", [])
    sala = j["sala"]
    vol = sala["w"] * sala["d"] * sala["h"]
    return {
        "id": j["id"], "nome": j["nome"], "tipo": j.get("tipologia", "privato"), "privato": True,
        "descrizione": ", ".join(x for x in [j.get("tipologia"), j.get("citta")] if x),
        "sala": sala, "palco": j.get("palco", {"w": sala["w"] * 0.6, "d": 4, "h": 0.5}),
        "aperto": False, "posti": j.get("capienza"), "volume_m3": int(vol),
        "rt60": {BANDS[k]: v for k, v in (ac.get("rt60_s") or {}).items() if k in BANDS},
        "ascoltatore": j["listener"], "pianta": j.get("pianta"), "mic_consigliati": mics,
        "consigli": [x for x in [ac.get("note")] + [f"{m['nome']}: {m.get('nota', '')}" for m in mics] if x],
        "fonti": j.get("fonti", []), "elementi": [],
    }


def local() -> list[dict]:
    out = []
    for f in sorted(LOCAL.glob("*.json")):
        try:
            out.append({**normalize(json.loads(f.read_text(encoding="utf-8"))), "privato": True, "file": str(f)})
        except (ValueError, KeyError):
            continue  # file non valido: lo si ignora, non blocca l'elenco
    return out


def all_spaces() -> list[dict]:
    return builtin() + local()


def get(sid: str) -> dict:
    return next(s for s in all_spaces() if s["id"] == sid)


def import_file(path: str) -> dict:
    """Valida e copia un file spazio in ~/.mix3d/spazi/. Ritorna lo spazio normalizzato."""
    src = Path(path).expanduser()
    s = normalize(json.loads(src.read_text(encoding="utf-8")))
    for k in ("id", "nome", "sala", "ascoltatore"):
        if k not in s:
            raise ValueError(f"file spazio senza '{k}'")
    LOCAL.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, LOCAL / f"{s['id']}.json")
    return s


def critical_distance(s: dict) -> float | None:
    """Distanza critica (m) con sorgente omni: 0,057 * sqrt(V / RT60 a 500 Hz)."""
    rt = (s.get("rt60") or {}).get("500")
    return round(0.057 * (s["volume_m3"] / rt) ** 0.5, 1) if rt and s.get("volume_m3") else None
