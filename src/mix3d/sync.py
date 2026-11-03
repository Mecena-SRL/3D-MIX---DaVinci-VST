"""M2: sync fine fra sorgenti con GCC-PHAT e modello di drift lineare.

Convenzione: un ritardo positivo significa che `y` arriva DOPO `x`
(y(t) ~ x(t - ritardo)).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def gcc_phat(x: np.ndarray, y: np.ndarray, fs: float, max_tau: float | None = None,
             interp: int = 16) -> tuple[float, float]:
    """Ritardo di `y` rispetto a `x` in secondi, con precisione sub-campione.

    Ritorna (ritardo_s, forza_picco). La forza del picco (0..1 circa) serve
    come peso: finestre con applausi o silenzi danno picchi deboli.
    """
    n = len(x) + len(y)
    nfft = 1 << (n - 1).bit_length()
    X = np.fft.rfft(x, nfft)
    Y = np.fft.rfft(y, nfft)
    cross = Y * np.conj(X)
    cross /= np.abs(cross) + 1e-12
    cc = np.fft.irfft(cross, nfft * interp)
    max_shift = nfft * interp // 2
    if max_tau is not None:
        max_shift = min(int(interp * fs * max_tau), max_shift)
    cc = np.concatenate((cc[-max_shift:], cc[: max_shift + 1]))
    i = int(np.argmax(np.abs(cc)))
    # interpolazione parabolica del picco
    shift = float(i)
    if 0 < i < len(cc) - 1:
        a, b, c = np.abs(cc[i - 1 : i + 2])
        den = a - 2 * b + c
        if den != 0:
            shift += 0.5 * (a - c) / den
    tau = (shift - max_shift) / (interp * fs)
    strength = float(np.abs(cc[i]) * interp)
    return tau, strength


@dataclass
class DriftModel:
    """ritardo(t) = offset + ppm * 1e-6 * t  (t in secondi sulla sorgente di riferimento)."""
    offset: float
    ppm: float
    rms_residual: float
    times: np.ndarray = field(repr=False)
    delays: np.ndarray = field(repr=False)
    inliers: np.ndarray = field(repr=False)

    def delay_at(self, t: np.ndarray | float) -> np.ndarray | float:
        return self.offset + self.ppm * 1e-6 * np.asarray(t)


def windowed_delays(x: np.ndarray, y: np.ndarray, fs: float, win_s: float = 10.0,
                    hop_s: float = 10.0, coarse_delay: float = 0.0,
                    search_s: float = 0.05) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Stima il ritardo in finestre successive, seguendo il drift.

    `coarse_delay` è il sync grossolano (es. da Resolve). Ogni finestra di `y`
    viene letta spostata della stima precedente, così il drift lungo un'ora
    resta dentro la finestra di ricerca `search_s`.
    """
    win, hop = int(win_s * fs), int(hop_s * fs)
    times, delays, weights = [], [], []
    current = coarse_delay
    for start in range(0, len(x) - win + 1, hop):
        shift = int(round(current * fs))
        ys = start + shift
        if ys < 0 or ys + win > len(y):
            continue
        tau, w = gcc_phat(x[start : start + win], y[ys : ys + win], fs, max_tau=search_s)
        d = shift / fs + tau
        times.append((start + win / 2) / fs)
        delays.append(d)
        weights.append(w)
        if w > 0.05:  # segui il drift solo con picchi affidabili
            current = d
    return np.array(times), np.array(delays), np.array(weights)


def fit_drift(times: np.ndarray, delays: np.ndarray, tol_s: float = 50e-6,
              iters: int = 200, seed: int = 0) -> DriftModel:
    """Regressione robusta (RANSAC + minimi quadrati sugli inlier)."""
    if len(times) < 2:
        raise ValueError("servono almeno 2 finestre per stimare il drift")
    rng = np.random.default_rng(seed)
    best = np.ones(len(times), bool)
    best_count = 0
    for _ in range(iters):
        i, j = rng.choice(len(times), 2, replace=False)
        if times[i] == times[j]:
            continue
        b = (delays[j] - delays[i]) / (times[j] - times[i])
        a = delays[i] - b * times[i]
        inl = np.abs(delays - (a + b * times)) < tol_s
        if inl.sum() > best_count:
            best, best_count = inl, int(inl.sum())
    b, a = np.polyfit(times[best], delays[best], 1)
    res = delays[best] - (a + b * times[best])
    return DriftModel(offset=float(a), ppm=float(b * 1e6),
                      rms_residual=float(np.sqrt(np.mean(res**2))),
                      times=times, delays=delays, inliers=best)


def estimate_drift(x: np.ndarray, y: np.ndarray, fs: float, refine: int = 1,
                   **kw) -> DriftModel:
    """Stima offset e drift; `refine` passate di raffinamento.

    Con drift forte il ritardo cambia dentro la finestra e il picco GCC si
    allarga. Ogni raffinamento riallinea `y` col modello corrente e stima solo
    il residuo, che è quasi costante.
    """
    times, delays, _ = windowed_delays(x, y, fs, **kw)
    model = fit_drift(times, delays)
    for _ in range(refine):
        y_al = align(y, fs, model, len(x))
        kw2 = {**kw, "coarse_delay": 0.0, "search_s": 0.002}
        t2, d2, _ = windowed_delays(x, y_al, fs, **kw2)
        r = fit_drift(t2, d2)
        # out(t) = y(t + m(t)), residuo r(t) => ritardo totale ~ m(t) + r(t)
        model = DriftModel(offset=model.offset + r.offset, ppm=model.ppm + r.ppm,
                           rms_residual=r.rms_residual, times=t2,
                           delays=model.delay_at(t2) + d2, inliers=r.inliers)
    return model


def align(y: np.ndarray, fs: float, model: DriftModel, n_out: int) -> np.ndarray:
    """Riporta `y` sulla base tempi di `x`: out(t) = y(t + ritardo(t)).

    Prototipo con interpolazione cubica; in F1 va sostituita da un
    ricampionatore a rapporto variabile di qualità (soxr / sinc polifase).
    """
    from scipy.interpolate import CubicSpline

    t = np.arange(n_out) / fs
    src = (t + model.delay_at(t)) * fs
    spline = CubicSpline(np.arange(len(y)), y, extrapolate=False)
    out = spline(src)
    return np.nan_to_num(out)
