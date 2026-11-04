import numpy as np

from mix3d import ambiente


def test_asciuga_riduce_la_coda():
    sr, rng = 48000, np.random.default_rng(0)
    dry = np.zeros(sr * 3)
    dry[::sr // 2] = 1.0  # colpi ogni 0,5 s
    t = np.arange(int(1.5 * sr)) / sr
    wet = np.convolve(dry, rng.standard_normal(len(t)) * np.exp(-6.9 * t / 1.5) * 0.05)[: len(dry)]
    x = np.stack([dry + wet] * 2, axis=1)
    y = ambiente.asciuga(x, sr, 1.5, 1.0)
    tail = lambda z: np.sum(z[int(0.2 * sr): int(0.45 * sr), 0] ** 2)  # fra un colpo e l'altro
    assert tail(y) < tail(x) * 0.3
    hit = lambda z: np.abs(z[sr // 2 - 50: sr // 2 + 50, 0]).max()
    assert hit(y) > 0.5 * hit(x)  # l'attacco resta


def test_riverbero_a_blocchi_uguale_al_continuo():
    sr, rng = 48000, np.random.default_rng(1)
    x = rng.standard_normal((sr * 2, 2)).astype(np.float32) * 0.1
    rv = ambiente.Reverb()
    whole = rv(x, sr, 0.0, "teatro")
    rv = ambiente.Reverb()
    parts = np.vstack([rv(x[i: i + sr // 2], sr, i / sr, "teatro") for i in range(0, sr * 2, sr // 2)])
    assert np.abs(parts - whole).max() < 1e-4


def test_ruolo_dal_microfono():
    assert ambiente.ruolo({"microfono": "feed_mixer"}) == "diretto"
    assert ambiente.ruolo({"microfono": "osmo_action_interni"}) == "ambiente"
    assert ambiente.ruolo({"microfono": "osmo_action_interni", "ruolo": "diretto"}) == "diretto"
