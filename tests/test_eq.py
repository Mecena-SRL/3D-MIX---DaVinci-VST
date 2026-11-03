"""EQ dinamico e auto-taratura su tracce sintetiche."""
import numpy as np
import soundfile as sf
from scipy.signal import lfilter

from mix3d import autotune, eq, mixer, server

FS = 48000


def test_curva_uguale_al_filtro():
    bands = [{"tipo": "passa_alto", "f": 80, "pendenza": 24}, {"tipo": "campana", "f": 1000, "g": -6, "q": 4},
             {"tipo": "shelf_basso", "f": 200, "g": 3}, {"tipo": "shelf_alto", "f": 8000, "g": -4}]
    x = np.zeros((8192, 1)); x[0] = 1
    h = 20 * np.log10(np.abs(np.fft.rfft(eq.process(x, bands, FS)[:, 0])) + 1e-12)
    f = np.fft.rfftfreq(8192, 1 / FS)
    assert np.allclose(h[5:4000], eq.response_db(bands, f[5:4000], FS), atol=0.05)


def test_banda_dinamica_agisce_solo_sopra_soglia():
    t = np.arange(FS) / FS
    x = np.sin(2 * np.pi * 1000 * t)[:, None]
    x[: FS // 2] *= 0.01  # prima metà piano, seconda forte
    b = [{"tipo": "campana", "f": 1000, "g": -9, "q": 4, "dyn": {"soglia_db": -30, "rapporto": 4}}]
    y = eq.process(x, b, FS)
    piano = 20 * np.log10(np.abs(y[FS // 4: FS // 2]).max() / 0.01)
    forte = 20 * np.log10(np.abs(y[-FS // 4:]).max())
    assert abs(piano) < 0.2 and abs(forte + 9) < 0.3


def _track(path, x, ruolo, nome, sorgente=None):
    sf.write(path, x, FS, "FLOAT")
    t = {"id": nome, "nome": nome, "wav": str(path), "channels": [1], "info": {"duration": len(x) / FS},
         "ruolo": ruolo, "microfono": None, "gain_db": 0.0, "offset_s": 0.0, "pos": [0, 1.5, 3], "eq": None}
    if sorgente:
        t["sorgente"] = sorgente
    return t


def test_auto_taratura(tmp_path):
    rng = np.random.default_rng(0)
    n = 40 * FS
    pink = lfilter([0.049922, -0.095993, 0.050612, -0.004408], [1, -2.494956, 2.017265, -0.522189],
                   rng.standard_normal(n))
    pink = 0.2 * pink / np.abs(pink).max()
    ring = 0.05 * np.sin(2 * np.pi * 900 * np.arange(n) / FS)  # risonanza fissa a 900 Hz
    voce = lfilter(*_bp(300, 3000), rng.standard_normal(n)) * 0.1
    p = server.new_project()
    p["tracks"] = [_track(tmp_path / "amb.wav", pink + ring, "ambiente", "amb"),
                   _track(tmp_path / "voce.wav", voce, "spot", "voce", "voce")]
    p["tracks"][0]["eq"] = [{"tipo": "campana", "f": 3000, "g": 1, "q": 1, "auto": False}]  # manuale: resta
    autotune.run(p, rt60={"125": 1.8, "250": 1.6, "500": 1.2, "1k": 1.0})
    amb, vc = p["tracks"]
    assert amb["eq"][0]["auto"] is False
    assert any(b["tipo"] == "passa_alto" for b in amb["eq"])
    ris = [b for b in amb["eq"] if b.get("dyn") and b["q"] == 8.0]
    assert ris and abs(ris[0]["f"] - 900) < 30, amb["eq"]
    assert any("sala" in b.get("perche", "") for b in amb["eq"])
    assert any("voce" in b.get("perche", "") for b in amb["eq"])  # scava per la voce
    assert all(b["perche"] for b in vc["eq"])
    blk, _ = mixer.render(p, 5.0, 1.0)  # il mix suona con l'EQ
    assert blk.shape == (FS, 2) and np.isfinite(blk).all()
    server.STATE["project"] = p
    c = server.eq_curve("amb")
    assert len(c["f"]) == len(c["statica"]) == len(c["prima"])
    assert min(c["dinamica"]) <= min(c["statica"])


def _bp(lo, hi):
    from scipy.signal import butter
    return butter(2, [lo, hi], "bandpass", fs=FS)
