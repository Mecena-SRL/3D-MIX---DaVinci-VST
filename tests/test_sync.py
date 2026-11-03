import numpy as np
from scipy.signal import lfilter, resample

from mix3d.sync import estimate_drift, fit_drift, gcc_phat

FS = 48000


def _music_like(seconds: float, seed: int = 1) -> np.ndarray:
    """Rumore rosa approssimato con inviluppo variabile: più simile alla musica del rumore bianco."""
    rng = np.random.default_rng(seed)
    n = int(seconds * FS)
    x = lfilter([0.049922, -0.095993, 0.050612, -0.004408], [1, -2.494956, 2.017265, -0.522189],
                rng.standard_normal(n))
    env = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 0.7 * np.arange(n) / FS))
    return x * env


def _frac_delay(x: np.ndarray, delay_s: float) -> np.ndarray:
    f = np.fft.rfftfreq(len(x), 1 / FS)
    return np.fft.irfft(np.fft.rfft(x) * np.exp(-2j * np.pi * f * delay_s), len(x))


def test_gcc_phat_subsample():
    x = _music_like(10)
    for d in (0.0, 3.7e-3, -12.34e-3, 0.5 / FS):
        y = _frac_delay(x, d) + 0.05 * np.random.default_rng(2).standard_normal(len(x))
        tau, _ = gcc_phat(x, y, FS, max_tau=0.05)
        assert abs(tau - d) < 20e-6, (d, tau)


def test_drift_one_hour_equivalent():
    # 120 s con 50 ppm e offset 23.4 ms
    secs, ppm, offset = 120, 50.0, 23.4e-3
    x = _music_like(secs + 1)
    n = len(x)
    # y(t) = x(t / (1 + ppm)) ritardato di offset: il ritardo cresce di ppm*t
    y = resample(x, int(round(n * (1 + ppm * 1e-6))))
    y = _frac_delay(np.concatenate([y, np.zeros(4800)]), offset)
    y += 0.05 * np.random.default_rng(3).standard_normal(len(y))
    m = estimate_drift(x[: secs * FS], y, FS, win_s=5, hop_s=5, coarse_delay=0.02)
    assert abs(m.ppm - ppm) < 1.0, m
    assert abs(m.offset - offset) < 20e-6, m
    assert m.rms_residual < 20e-6, m


def test_fit_drift_rejects_outliers():
    t = np.arange(0, 600, 10.0)
    d = 0.01 + 30e-6 * t
    d[[5, 17, 40]] += [0.004, -0.02, 0.1]  # applausi, silenzi
    m = fit_drift(t, d)
    assert abs(m.ppm - 30) < 0.01
    assert m.inliers.sum() == len(t) - 3
