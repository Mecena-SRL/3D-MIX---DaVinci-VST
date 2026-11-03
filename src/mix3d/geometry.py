"""Posizionamento approssimativo dei microfoni nella scena (metri).

Assi: x = larghezza (destra +), y = altezza, z = profondità verso il pubblico.
Il palco è centrato in (0, 0, 0); l'ascoltatore guarda verso -z.

Automatico = posizione tipica dal profilo, raffinata con i ritardi fra
canali dello stesso registratore (stesso clock). Fra registratori diversi i
ritardi acustici non si separano dall'offset di avvio: lì resta la stima.
"""
from __future__ import annotations

import numpy as np

C = 343.0  # m/s a ~20 °C

# posizione tipica per il campo "posizione" del profilo
TYPICAL = {
    "fondo sala": (0.0, 1.8, 0.85), "vicino palco centro": (0.0, 1.5, 0.15),
    "laterale": (0.45, 1.6, 0.4), "vicino ai musicisti": (0.25, 1.0, -0.05),
    "sotto palco centro": (0.0, 1.2, 0.08), "lati palco": (0.4, 1.8, 0.1),
    "regia": (0.0, 1.2, 0.6), "su strumento": (0.3, 0.8, -0.15),
}


def auto_positions(tracks: list[dict], room: dict) -> dict[str, list[float]]:
    """Posizioni per le tracce in modo 'auto'. Le frazioni x/z di TYPICAL
    scalano con la sala; tracce con la stessa posizione tipica si allargano."""
    w, d = room["w"], room["d"]
    seen: dict[str, int] = {}
    out = {}
    for t in tracks:
        key = t.get("posizione_tipica", "")
        fx, y, fz = TYPICAL.get(key, (0.0, 1.5, 0.3))
        k = seen.get(key, 0)
        seen[key] = k + 1
        sign = 1 if k % 2 == 0 else -1
        x = sign * (fx * w / 2 + (k + 1) // 2 * 1.5)
        z = fz * d + t.get("extra_dist_m", 0.0)
        out[t["id"]] = [round(float(np.clip(x, -w / 2, w / 2)), 2), y,
                        round(float(np.clip(z, -3, d)), 2)]
    return out


def same_clock_distances(tracks: list[dict], seconds: float = 60.0, fs: int = 48000) -> dict[str, float]:
    """Distanze extra (m) rispetto al canale più vicino, per tracce con lo stesso
    clock (stesso registratore e stessa durata): ritardo GCC-PHAT * c."""
    from . import media
    from .sync import gcc_phat

    groups: dict[tuple, list[dict]] = {}
    for t in tracks:
        groups.setdefault((t.get("registratore"), round(t["info"]["duration"], 1)), []).append(t)
    out = {}
    for g in groups.values():
        if len(g) < 2:
            continue
        sig = [media.read(t["wav"], t["channels"], 30.0, seconds, fs).mean(axis=1).astype(float) for t in g]
        delays = [gcc_phat(sig[0], s, fs, max_tau=0.1)[0] for s in sig]
        d0 = min(delays)
        out.update({t["id"]: round((d - d0) * C, 2) for t, d in zip(g, delays)})
    return out


def spatial_params(pos, listener) -> tuple[float, float]:
    """(distanza m, pan -1..1) della sorgente virtuale vista dall'ascoltatore."""
    v = np.asarray(pos, float) - np.asarray(listener, float)
    dist = max(float(np.linalg.norm(v)), 0.5)
    az = np.arctan2(v[0], -v[2])  # 0 = davanti (verso il palco)
    return dist, float(np.clip(np.sin(az), -1, 1))
