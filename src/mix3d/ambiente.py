"""Suono diretto e suono dello spazio: quanto ambiente, quanto asciugarlo, compressione e riverbero.

Le tracce si dividono in due bus:
- diretto: linea del mixer, microfoni vicini (lavalier, dinamici, wireless, strumento);
- ambiente: microfoni di camera e action cam, registratori, shotgun, stereo.
Il bus ambiente si somma a potenza costante (dieci camere non fanno dieci volte il riverbero
della piazza), si può asciugare (riduzione della coda di riverbero) e dosare.
Sul master poi una compressione regolabile e un riverbero di carattere (piazza con impianto,
chiesa, teatro...), che si aggiunge al suono senza sostituirlo.
"""
from __future__ import annotations

import threading
from functools import lru_cache

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt, istft, stft

from . import devices

DIRETTI = {"linea", "lavalier", "dinamico", "strumento", "wireless"}

DEFAULT = {"ambiente": 0.6, "asciuga": 0.0, "compressione": 0.3, "riverbero": 0.0, "carattere": "piazza_pa"}

# riverberi di carattere: rt60 (s, medi), smorzamento degli acuti, pre-delay, echi discreti (s, dB)
CARATTERI = {
    "studio": {"nome": "Asciutto / studio", "rt": 0.35, "acuti": 0.6, "pre": 0.005, "echi": []},
    "club": {"nome": "Club / locale", "rt": 0.8, "acuti": 0.5, "pre": 0.008, "echi": [(0.023, -8)]},
    "piazza_pa": {"nome": "Piazza con impianto", "rt": 1.3, "acuti": 0.45, "pre": 0.02,
                  "echi": [(0.085, -6), (0.17, -10), (0.26, -15)]},  # facciate attorno alla piazza
    "teatro": {"nome": "Teatro all'italiana", "rt": 1.3, "acuti": 0.7, "pre": 0.015, "echi": [(0.018, -9), (0.031, -11)]},
    "sala_concerto": {"nome": "Sala da concerto", "rt": 2.0, "acuti": 0.65, "pre": 0.025, "echi": [(0.021, -8), (0.037, -10)]},
    "chiesa": {"nome": "Chiesa (acustico)", "rt": 3.8, "acuti": 0.4, "pre": 0.035, "echi": [(0.045, -9), (0.07, -11)]},
}


def settings(project: dict) -> dict:
    return {**DEFAULT, **(project.get("ambiente_fx") or {})}


def ruolo(t: dict) -> str:
    """'diretto' o 'ambiente': dalla traccia (scelta a mano) o dal tipo di microfono."""
    if t.get("ruolo") in ("diretto", "ambiente"):
        return t["ruolo"]
    mic = devices.load()["microfoni"].get(t.get("microfono") or "", {})
    return "diretto" if mic.get("tipo") in DIRETTI else "ambiente"


def asciuga(x: np.ndarray, sr: int, rt60: float, amount: float) -> np.ndarray:
    """Riduzione della coda di riverbero (sottrazione spettrale del riverbero tardivo).
    La potenza tardiva si stima dalla potenza di 50 ms prima, smorzata secondo l'RT60."""
    if amount <= 0 or len(x) < 2048:
        return x
    hop, n = 256, 1024
    delay = max(1, int(0.05 * sr / hop))
    decay = np.exp(-13.8 * delay * hop / sr / max(rt60, 0.2))
    floor = 10 ** (-18 * amount / 20)
    out = np.empty_like(x)
    for c in range(x.shape[1]):
        _, _, Z = stft(x[:, c], sr, nperseg=n, noverlap=n - hop)
        P = np.abs(Z) ** 2
        late = np.zeros_like(P)
        late[:, delay:] = decay * P[:, :-delay]
        g = np.maximum(1 - 1.5 * amount * late / (P + 1e-12), floor)
        g[:, 1:] = 0.5 * g[:, 1:] + 0.5 * g[:, :-1]  # niente "musical noise"
        _, y = istft(Z * g, sr, nperseg=n, noverlap=n - hop)
        out[:, c] = y[: len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))
    return out


@lru_cache(maxsize=8)
def impulse(car: str, sr: int) -> np.ndarray:
    """Risposta all'impulso stereo sintetica: echi discreti + coda esponenziale in 3 bande."""
    c = CARATTERI.get(car, CARATTERI["piazza_pa"])
    rt, n = c["rt"], int(min(c["rt"] * 1.5, 6.0) * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(7)
    ir = np.zeros((n, 2))
    bands = [(butter(2, 300, "lowpass", fs=sr, output="sos"), rt * 1.15),
             (butter(2, [300, 4000], "bandpass", fs=sr, output="sos"), rt),
             (butter(2, 4000, "highpass", fs=sr, output="sos"), rt * c["acuti"])]
    for ch in range(2):
        noise = rng.standard_normal(n)
        for sos, r in bands:
            ir[:, ch] += sosfilt(sos, noise) * np.exp(-6.9 * t / r)
    ir *= np.minimum(t / 0.01, 1)[:, None]  # attacco morbido della coda
    for k, (d, g) in enumerate(c["echi"]):
        i = int(d * sr)
        if i < n:
            ir[i, k % 2] += 10 ** (g / 20) * 6
            ir[min(i + int(0.0007 * sr), n - 1), 1 - k % 2] += 10 ** (g / 20) * 5
    ir /= np.sqrt((ir ** 2).sum() / 2)
    return np.vstack([np.zeros((int(c["pre"] * sr), 2)), ir]).astype(np.float32)


class Reverb:
    """Convoluzione a blocchi: la coda di un blocco suona nel successivo se i blocchi sono contigui
    (ascolto, plugin, stampa). Dopo un salto la coda riparte da zero."""

    def __init__(self):
        self.lock, self.end, self.key, self.tail = threading.Lock(), None, None, None

    def __call__(self, x: np.ndarray, sr: int, t0: float, car: str) -> np.ndarray:
        ir = impulse(car, sr)
        y = np.stack([fftconvolve(x[:, c], ir[:, c]) for c in range(2)], axis=1)
        n = len(x)
        with self.lock:
            if self.key == (car, sr) and self.end is not None and abs(self.end - t0) < 1e-3:
                m = min(len(self.tail), len(y))
                y[:m] += self.tail[:m]
            self.end, self.key, self.tail = t0 + n / sr, (car, sr), y[n:].copy()
        return y[:n]


REVERB = Reverb()


def compress(out: np.ndarray, project: dict, sr: int) -> np.ndarray:
    """Compressione del master (sul blocco con il pre-roll, così non ci sono salti fra i blocchi)."""
    from .look import compress as comp
    amt = settings(project)["compressione"]
    if amt <= 0:
        return out
    return comp(out, {"soglia_db": -26, "rapporto": 4, "attacco_ms": 15, "rilascio_ms": 180, "makeup_db": 8}, sr, amt)


def reverb(out: np.ndarray, project: dict, sr: int, t0: float) -> np.ndarray:
    """Riverbero di carattere aggiunto al master (blocco senza pre-roll, che parte da t0)."""
    s = settings(project)
    if s["riverbero"] <= 0:
        return out
    return (out + REVERB(out, sr, t0, s["carattere"]) * (0.5 * s["riverbero"])).astype(np.float32)
