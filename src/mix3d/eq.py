"""EQ parametrico e dinamico per traccia.

Una banda è un dict:
    {"tipo": "campana"|"shelf_basso"|"shelf_alto"|"passa_alto"|"passa_basso",
     "f": Hz, "g": dB, "q": Q, "pendenza": dB/ott (solo passa_*), "on": bool,
     "dyn": None | {"soglia_db", "rapporto", "attacco_ms", "rilascio_ms"},
     "perche": testo, "auto": bool}

Campana e shelf usano la forma Regalia-Mitra: y = x + (K - 1) * s(x), dove s è la
componente di banda (da un passa-tutto). Così il guadagno K può cambiare a ogni
campione e la stessa banda diventa dinamica senza un secondo filtro: la soglia
guarda il livello di s, e la banda va da 0 dB (sotto soglia) fino a g dB.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, lfilter, sosfilt, sosfreqz

FRAME_S = 0.002  # risoluzione dell'inviluppo dinamico


def _ap1(f: float, sr: int) -> tuple[list, list]:
    t = np.tan(np.pi * min(f, 0.49 * sr) / sr)
    c = (t - 1) / (t + 1)
    return [c, 1.0], [1.0, c]


def _ap2(f: float, q: float, sr: int) -> tuple[list, list]:
    f = min(f, 0.49 * sr)
    t = np.tan(np.pi * min(f / q, 0.49 * sr) / sr)
    c, d = (t - 1) / (t + 1), -np.cos(2 * np.pi * f / sr)
    return [-c, d * (1 - c), 1.0], [1.0, d * (1 - c), -c]


def component(band: dict, x: np.ndarray, sr: int) -> np.ndarray:
    """La parte di segnale su cui agisce una campana o uno shelf."""
    if band["tipo"] == "campana":
        return (x - lfilter(*_ap2(band["f"], band.get("q", 1.0), sr), x, axis=0)) / 2
    ap = lfilter(*_ap1(band["f"], sr), x, axis=0)
    return (x + ap) / 2 if band["tipo"] == "shelf_basso" else (x - ap) / 2


def _sos_cut(band: dict, sr: int) -> np.ndarray:
    order = max(1, int(band.get("pendenza", 12)) // 6)
    btype = "highpass" if band["tipo"] == "passa_alto" else "lowpass"
    return butter(order, min(band["f"], 0.49 * sr), btype, fs=sr, output="sos")


def level_db(s: np.ndarray, sr: int, dyn: dict) -> np.ndarray:
    """Inviluppo in dB per frame di FRAME_S, con attacco e rilascio."""
    hop = max(1, int(FRAME_S * sr))
    m = len(s) // hop
    p = (s[: m * hop].reshape(m, hop, -1) ** 2).mean(axis=(1, 2)) if m else np.zeros(0)
    a = np.exp(-FRAME_S / max(dyn.get("attacco_ms", 5) / 1000, 1e-4))
    r = np.exp(-FRAME_S / max(dyn.get("rilascio_ms", 80) / 1000, 1e-4))
    env, e = np.empty(m), 0.0
    for i, v in enumerate(p):
        k = a if v > e else r
        e = k * e + (1 - k) * v
        env[i] = e
    return 10 * np.log10(env + 1e-12)


def dyn_gain_db(band: dict, s: np.ndarray, sr: int) -> np.ndarray:
    """Guadagno per campione: 0 sotto soglia, fino a g sopra (secondo il rapporto)."""
    dyn, g = band["dyn"], band.get("g", 0.0)
    over = np.maximum(level_db(s, sr, dyn) - dyn.get("soglia_db", -30), 0)
    amt = np.clip(over * (1 - 1 / max(dyn.get("rapporto", 2.0), 1.0)), 0, abs(g)) * np.sign(g)
    hop = max(1, int(FRAME_S * sr))
    out = np.repeat(amt, hop)
    return np.pad(out, (0, len(s) - len(out)), mode="edge") if len(out) else np.zeros(len(s))


def process(x: np.ndarray, bands: list[dict], sr: int) -> np.ndarray:
    """Applica le bande in serie a x [n, canali]."""
    for b in bands:
        if not b.get("on", True):
            continue
        if b["tipo"] in ("passa_alto", "passa_basso"):
            x = sosfilt(_sos_cut(b, sr), x, axis=0)
            continue
        s = component(b, x, sr)
        if b.get("dyn"):
            k = 10 ** (dyn_gain_db(b, s, sr) / 20)[:, None]
        elif b.get("g", 0.0):
            k = 10 ** (b["g"] / 20)
        else:
            continue
        x = x + (k - 1) * s
    return x.astype(np.float32)


def response_db(bands: list[dict], freqs, sr: int = 48000, dynamic: bool = False) -> np.ndarray:
    """Curva statica (bande dinamiche a riposo, 0 dB) o con le dinamiche al massimo."""
    f = np.asarray(freqs, float)
    w = 2 * np.pi * f / sr
    z = np.exp(-1j * w)
    h = np.ones_like(z)
    for b in bands:
        if not b.get("on", True):
            continue
        if b["tipo"] in ("passa_alto", "passa_basso"):
            h *= sosfreqz(_sos_cut(b, sr), worN=f, fs=sr)[1]
            continue
        g = b.get("g", 0.0) if (dynamic or not b.get("dyn")) else 0.0
        num, den = _ap2(b["f"], b.get("q", 1.0), sr) if b["tipo"] == "campana" else _ap1(b["f"], sr)
        ap = np.polyval(num[::-1], z) / np.polyval(den[::-1], z)
        s = (1 - ap) / 2 if b["tipo"] in ("campana", "shelf_alto") else (1 + ap) / 2
        h *= 1 + (10 ** (g / 20) - 1) * s
    return 20 * np.log10(np.abs(h) + 1e-12)
