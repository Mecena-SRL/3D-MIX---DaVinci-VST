"""Analisi per traccia (a blocchi, file lunghi ok) e loudness BS.1770."""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter, welch

from . import media
from .sync import estimate_drift, gcc_phat

THIRD_OCT = 1000 * 2 ** (np.arange(-17, 14) / 3)  # 20 Hz .. 20 kHz


def k_weighting(fs: float):
    """Due biquad del filtro K (ITU-R BS.1770), validi a qualunque fs (forma libebur128)."""
    K = np.tan(np.pi * 1681.974450955533 / fs)
    Q, Vh = 0.7071752369554196, 10 ** (3.999843853973347 / 20)
    Vb, a0 = Vh ** 0.4996667741545416, 1 + K / Q + K * K
    shelf = (np.array([Vh + Vb * K / Q + K * K, 2 * (K * K - Vh), Vh - Vb * K / Q + K * K]) / a0,
             np.array([1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]))
    K, Q = np.tan(np.pi * 38.13547087602444 / fs), 0.5003270373238773
    a0 = 1 + K / Q + K * K
    highpass = (np.array([1.0, -2.0, 1.0]), np.array([1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]))
    return [shelf, highpass]


class Loudness:
    """Loudness integrata a flusso: si alimenta con blocchi [n, canali]."""

    def __init__(self, fs: float, channels: int):
        self.fs, self.filters = fs, k_weighting(fs)
        self.zi = [[np.zeros(2) for _ in range(channels)] for _ in self.filters]
        self.rest = np.zeros((0, channels))
        self.e100 = []  # energia per 100 ms

    def feed(self, x: np.ndarray):
        x = np.atleast_2d(x.T).T.astype(np.float64)
        for k, (b, a) in enumerate(self.filters):
            cols = []
            for c in range(x.shape[1]):
                y, self.zi[k][c] = lfilter(b, a, x[:, c], zi=self.zi[k][c])
                cols.append(y)
            x = np.stack(cols, axis=1)
        x = np.vstack([self.rest, x])
        n = int(self.fs / 10)
        m = len(x) // n
        if m:
            self.e100.extend((x[: m * n] ** 2).reshape(m, n, -1).mean(axis=1).sum(axis=1))
        self.rest = x[m * n:]

    def blocks400(self) -> np.ndarray:
        e = np.asarray(self.e100)
        if len(e) < 4:
            return np.zeros(0)
        return np.convolve(e, np.ones(4) / 4, "valid")  # 400 ms con 75% di sovrapposizione

    def integrated(self) -> float:
        z = self.blocks400()
        z = z[-0.691 + 10 * np.log10(z + 1e-20) > -70]
        if not len(z):
            return -np.inf
        rel = -0.691 + 10 * np.log10(z.mean()) - 10
        z = z[-0.691 + 10 * np.log10(z) > rel]
        return float(-0.691 + 10 * np.log10(z.mean()))

    def curve(self, step_s: float = 1.0) -> list[float]:
        """Loudness a breve termine (3 s) ogni step_s secondi, per il grafico."""
        e = np.asarray(self.e100)
        k = int(step_s * 10)
        if len(e) < 30:
            return []
        st = np.convolve(e, np.ones(30) / 30, "valid")[::k]
        return np.round(-0.691 + 10 * np.log10(st + 1e-20), 1).tolist()


def db(x):
    return float(20 * np.log10(max(float(x), 1e-10)))


def analyze(wav: str, channels: list[int], duration: float, is_float: bool,
            points: int = 1200, progress=lambda f: None) -> dict:
    """Forma d'onda, livelli, clipping, rumore, spettro, banda utile, loudness."""
    bucket = max(duration / points, 1e-3)
    mins, maxs, rms100, psd_acc = [], [], [], None
    peak, clips, loud = 0.0, 0, None
    for t0, sr, x in media.blocks(wav, channels):
        loud = loud or Loudness(sr, 1)
        loud.feed(x[:, None])
        nb = int(bucket * sr)
        m = len(x) // nb
        if m:
            seg = x[: m * nb].reshape(m, nb)
            mins.extend(seg.min(axis=1)); maxs.extend(seg.max(axis=1))
        n100 = int(sr / 10)
        k = len(x) // n100
        if k:
            rms100.extend(np.sqrt((x[: k * n100].reshape(k, n100) ** 2).mean(axis=1)))
        peak = max(peak, float(np.abs(x).max(initial=0)))
        if not is_float:
            clips += int(np.count_nonzero(np.abs(x) >= 0.999))
        if len(x) >= 8192:
            f, p = welch(x, sr, nperseg=8192)
            psd_acc = p if psd_acc is None else psd_acc + p
        progress(min((t0 + len(x) / sr) / max(duration, 1e-9), 1.0))
    r = 20 * np.log10(np.maximum(rms100, 1e-10)) if rms100 else np.array([-120.0])
    out = {"overview": {"min": np.round(mins, 4).tolist(), "max": np.round(maxs, 4).tolist(), "step_s": bucket},
           "peak_dbfs": round(db(peak), 1), "clip_campioni": clips,
           "rms_dbfs": round(float(np.percentile(r, 50)), 1),
           "rumore_dbfs": round(float(np.percentile(r, 5)), 1),
           "dinamica_db": round(float(np.percentile(r, 95) - np.percentile(r, 10)), 1),
           "lufs": round(loud.integrated(), 1) if loud else None,
           "lufs_curva": loud.curve() if loud else []}
    if psd_acc is not None:
        pdb = 10 * np.log10(psd_acc + 1e-30)
        bands = [float(pdb[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].mean()) if np.any((f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))) else None
                 for c in THIRD_OCT]
        ref = np.median(pdb[(f > 1000) & (f < 4000)])
        above = f[(pdb > ref - 45) & (f > 1000)]
        out["spettro"] = {"f": np.round(THIRD_OCT, 1).tolist(), "db": [round(b, 1) if b is not None else None for b in bands]}
        out["banda_utile_hz"] = int(above.max()) if len(above) else None
    out["avvisi"] = warnings(out)
    return out


def warnings(a: dict) -> list[str]:
    w = []
    if a["clip_campioni"]:
        w.append(f"{a['clip_campioni']} campioni saturi")
    if a["dinamica_db"] < 12:
        w.append("dinamica compressa: possibile AGC/limiter")
    if (a.get("banda_utile_hz") or 20000) < 15500:
        w.append(f"banda limitata a ~{a['banda_utile_hz'] / 1000:.1f} kHz (codec?)")
    if a["rumore_dbfs"] > -50:
        w.append("rumore di fondo alto")
    return w


def sync_pair(ref: dict, trk: dict, max_s: float = 900.0, fs: int = 16000) -> dict:
    """Ritardo fine e drift di `trk` rispetto a `ref` sulla parte comune.

    Le tracce hanno `offset_s` (inizio del file sulla timeline). Senza un sync
    grossolano affidabile (da Resolve) prima si cerca su ±160 s a bassa risoluzione.
    """
    if not trk.get("da_resolve"):
        trk = {**trk, "offset_s": trk["offset_s"] - _coarse(ref, trk)}
    t_start = max(ref["offset_s"], trk["offset_s"])
    t_end = min(ref["offset_s"] + ref["info"]["duration"], trk["offset_s"] + trk["info"]["duration"])
    dur = min(t_end - t_start, max_s)
    if dur < 20:
        raise ValueError("meno di 20 s in comune con il riferimento")
    x = media.read(ref["wav"], ref["channels"], t_start - ref["offset_s"], dur, fs).mean(axis=1).astype(np.float64)
    y = media.read(trk["wav"], trk["channels"], t_start - trk["offset_s"], dur, fs).mean(axis=1).astype(np.float64)
    m = estimate_drift(x, y, fs, win_s=10, hop_s=10, search_s=0.25)
    conf = float(m.inliers.mean()) * float(np.exp(-m.rms_residual / 200e-6))
    return {"offset_s": trk["offset_s"] - m.offset, "drift_ppm": round(m.ppm, 2), "sync_t0": t_start,
            "residuo_us": round(m.rms_residual * 1e6, 1), "fiducia": round(conf, 2)}


def _coarse(ref: dict, trk: dict, fs: int = 4000, dur: float = 180.0) -> float:
    """Ritardo grossolano fra gli inizi dei due file (secondi)."""
    x = media.read(ref["wav"], ref["channels"], 0, dur, fs).mean(axis=1).astype(np.float64)
    y = media.read(trk["wav"], trk["channels"], 0, dur, fs).mean(axis=1).astype(np.float64)
    tau, _ = gcc_phat(x, y, fs, max_tau=dur * 0.9, interp=1)
    return tau + trk["offset_s"] - ref["offset_s"]
