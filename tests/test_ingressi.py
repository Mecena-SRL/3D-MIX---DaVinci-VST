"""Ingresso di linea, mono/stereo e due mono uniti in stereo."""
import numpy as np
import soundfile as sf

from mix3d import mixer, server


def _project(tmp_path):
    sr = 48000
    t = np.arange(sr) / sr
    sf.write(tmp_path / "l.wav", 0.5 * np.sin(2 * np.pi * 300 * t), sr)
    sf.write(tmp_path / "r.wav", 0.5 * np.sin(2 * np.pi * 700 * t), sr)
    sf.write(tmp_path / "st.wav", np.stack([0.5 * np.sin(2 * np.pi * 300 * t)] * 2, 1), sr)
    p = server.new_project()
    for f in ("l.wav", "r.wav", "st.wav"):
        p["tracks"] += server.tracks_from_file(str(tmp_path / f))
    for tr in p["tracks"]:
        tr.update(mute=False, gain_db=0.0, microfono="feed_mixer", pan=0.0)
    p["look"] = None
    return p


def test_split_and_join(tmp_path):
    p = _project(tmp_path)
    l, r, st = p["tracks"]
    a, b = server.split_track(p, st["id"])
    assert a["channels"] == [1] and b["channels"] == [2] and len(p["tracks"]) == 4
    server.join_tracks(p, a["id"], b["id"])  # stesso file: torna stereo senza copie
    assert p["tracks"][2]["channels"] == [1, 2] and len(p["tracks"]) == 3
    j = server.join_tracks(p, l["id"], r["id"])  # file diversi: doppio mono
    assert j["destra"]["wav"].endswith("r.wav") and len(p["tracks"]) == 2
    back = server.split_track(p, j["id"])
    assert [t["nome"] for t in back] == ["l.wav", "r.wav"] and back[1]["microfono"] == "feed_mixer"


def test_dual_mono_goes_left_right_and_line_ignores_distance(tmp_path):
    p = _project(tmp_path)
    l, r, st = p["tracks"]
    st["mute"] = True
    server.join_tracks(p, l["id"], r["id"])
    out, _ = mixer.render(p, 0.0, 0.5)
    spec = lambda x: np.abs(np.fft.rfft(x))  # noqa: E731
    L, R = spec(out[:, 0]), spec(out[:, 1])
    f300, f700 = 300 * len(out) // 48000, 700 * len(out) // 48000
    assert L[f300] > 20 * L[f700] and R[f700] > 20 * R[f300]
    far = mixer.render({**p, "tracks": [{**p["tracks"][0], "pos": [0, 1.5, 40]}]}, 0.0, 0.5)[0]
    assert np.allclose(far, out, atol=1e-4)  # linea: la posizione non cambia nulla
