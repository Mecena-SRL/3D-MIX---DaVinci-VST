"""Motore di localizzazione su una sala simulata: 2 sorgenti, linea del mixer, 3 mic."""
import numpy as np
import soundfile as sf

from mix3d import localize as L

FS = L.FS
ROOM = {"w": 16.0, "d": 20.0, "h": 7.0}


def _delay(x, d):
    f = np.fft.rfftfreq(len(x), 1 / FS)
    return np.fft.irfft(np.fft.rfft(x) * np.exp(-2j * np.pi * f * d), len(x))


def _scene(seconds=30, seed=0):
    """Due sorgenti che si alternano ogni 2 s; mic = diretto 1/r + coda di sala."""
    rng = np.random.default_rng(seed)
    n = seconds * FS
    gate = (np.arange(n) // (2 * FS)) % 2
    src = [rng.standard_normal(n) * (gate == k) for k in (0, 1)]
    S = np.array([[-3.0, 0.0], [3.0, 0.0]])                    # (x, z)
    M = np.array([[0.0, 4.0], [-5.0, 8.0], [5.0, 12.0]])
    tail = rng.standard_normal(int(0.4 * FS)) * np.exp(-np.arange(int(0.4 * FS)) / (0.06 * FS)) * 0.02
    mics = []
    for m in M:
        y = sum(_delay(s, np.linalg.norm(p - m) / L.C) / np.linalg.norm(p - m) for s, p in zip(src, S))
        mics.append(y + np.convolve(y, tail)[:n] + 1e-3 * rng.standard_normal(n))
    return sum(src), mics, S, M


def _track(tmp, name, x, rec="x8"):
    p = str(tmp / f"{name}.wav")
    sf.write(p, np.atleast_2d(x.T).T.astype(np.float32), FS, subtype="FLOAT")
    return {"id": name, "wav": p, "channels": [1] if x.ndim == 1 else [1, 2], "offset_s": 0.0,
            "info": {"duration": len(x) / FS}, "registratore": rec}


def test_images_line_same_clock(tmp_path):
    line, mics, S, M = _scene()
    ref = _track(tmp_path, "linea", line)
    ts = [ref] + [_track(tmp_path, f"m{i}", m) for i, m in enumerate(mics)]
    out = L.images(ts, ref, ROOM, rt60=1.0, mics={}, line=True)
    assert len(out["sorgenti"]) == 2
    for s in out["sorgenti"]:
        p = S[np.argmin([abs(np.linalg.norm(S[k] - M[1]) / L.C * 1e3 - s["ritardi_ms"]["m1"]) for k in (0, 1)])]
        for i in range(3):  # ritardo linea -> mic = tempo di volo dalla sorgente
            assert abs(s["ritardi_ms"][f"m{i}"] - np.linalg.norm(p - M[i]) / L.C * 1e3) < 0.1
    for i in range(3):
        img = out["tracce"][f"m{i}"]
        assert img["n_sorgenti"] == 2 and img["stesso_clock"] and img["metodo"] == "tempo di volo"
        assert min(abs(img["distanza_m"] - np.linalg.norm(S - M[i], axis=1))) < 0.2


def test_cluster_sources_separates_delay_patterns():
    rng = np.random.default_rng(1)
    tau = np.vstack([np.tile([1e-3, 2e-3], (60, 1)), np.tile([-1e-3, 4e-3], (40, 1)), rng.uniform(-0.05, 0.05, (10, 2))])
    groups = L.cluster_sources(tau, np.full(tau.shape, 0.5))
    assert [len(g) for g in groups] == [60, 40]


def test_stereo_direction_xy_and_spaced():
    rng = np.random.default_rng(2)
    s = rng.standard_normal(FS)
    th = np.radians(30)  # sorgente a destra
    xy = np.stack([s * (0.5 + 0.5 * np.cos(th + np.pi / 4)), s * (0.5 + 0.5 * np.cos(th - np.pi / 4))], 1)  # L punta a -45°
    az, _ = L.stereo_direction(xy, "coincidente")
    assert abs(az - 30) < 2
    ab = np.stack([s, _delay(s, -0.17 * np.sin(th) / L.C)], 1)  # destra: arriva prima al canale destro
    az, _ = L.stereo_direction(ab, "spaziata")
    assert abs(az - 30) < 4, az


def test_distance_from_drr():
    n = 16384
    h = np.zeros(n)
    h[n // 2 + 100] = 1.0
    tail = np.random.default_rng(3).standard_normal(int(0.3 * FS)) * np.exp(-np.arange(int(0.3 * FS)) / (0.05 * FS))
    near, far = h.copy(), h.copy()
    near[n // 2 + 300: n // 2 + 300 + len(tail)][: n // 2 - 300] += 0.01 * tail[: n // 2 - 300]
    far[n // 2 + 300: n // 2 + 300 + len(tail)][: n // 2 - 300] += 0.1 * tail[: n // 2 - 300]
    dn = L.distance_from_ir(near, FS, ROOM, 1.0)["distanza_m"]
    df = L.distance_from_ir(far, FS, ROOM, 1.0)["distanza_m"]
    assert df > 3 * dn
