"""Fusione: dalle immagini (ritardi, distanze, livelli) di una scena nota torna la geometria."""
import numpy as np

from mix3d.fusion import fuse

C = 343.0
STAGE = {"w": 12.0, "d": 4.0}
S = np.array([[-5.0, -1.0], [5.0, -1.0], [0.0, -3.5]])  # palco largo: trilaterazione ben condizionata
M = {"a": [0.0, 4.0], "b": [-5.0, 8.0], "c": [5.0, 12.0], "d": [-2.0, 15.0]}


def _imgs(clock_ms=None, metodo="tempo di volo"):
    clock_ms = clock_ms or {}
    tr = {}
    for i, m in M.items():
        d = np.linalg.norm(S - m, axis=1)
        tr[i] = {"stesso_clock": i not in clock_ms, "sorgenti": [
            {"k": k, "ritardo_ms": d[k] / C * 1e3 + clock_ms.get(i, 0), "livello_db": -20 * np.log10(d[k]) + 3,
             "fiducia": 0.8} for k in range(len(S))]}
        tr[i].update(distanza_m=float(d.min()), metodo=metodo, fiducia_distanza=0.8)
    srcs = [{"k": k, "presenza": 0.3, "ritardi_ms": {}} for k in range(len(S))]
    return {"linea": True, "riferimento": "linea", "sorgenti": srcs, "tracce": tr}


def _start(err=3.0, seed=0):
    rng = np.random.default_rng(seed)
    return {i: [m[0] + rng.uniform(-err, err), 1.5, m[1] + rng.uniform(-err, err)] for i, m in M.items()}


def test_same_clock_recovers_scene():
    """Senza mic bloccati la scena è giusta a meno di spostamenti rigidi: si confrontano le distanze."""
    out = fuse(_imgs(), _start(), set(), STAGE)
    got = [np.array(out["mic"][i]["pos"])[[0, 2]] for i in M] + [np.array(s["pos"])[[0, 2]] for s in out["sorgenti"]]
    true = [np.array(m) for m in M.values()] + list(S)
    for a in range(len(got)):
        for b in range(a):
            assert abs(np.linalg.norm(got[a] - got[b]) - np.linalg.norm(true[a] - true[b])) < 0.3, (a, b)


def test_unknown_clocks_and_locked_mic():
    """Clock diversi: il ritardo assoluto non dice la distanza, restano livelli, differenze fra
    sorgenti e diretto/riverbero. Stima più vaga, e l'incertezza lo deve dire."""
    imgs = _imgs({"c": 12.0, "d": -7.5}, metodo="diretto/riverbero")
    start = _start()
    start["a"] = [0.0, 1.5, 4.0]
    start["b"] = [-5.0, 1.5, 8.0]
    out = fuse(imgs, start, {"a", "b"}, STAGE)
    for i in "cd":  # l'errore resta dentro l'incertezza dichiarata (2 sigma)
        e = out["mic"][i]
        assert np.hypot(e["pos"][0] - M[i][0], e["pos"][2] - M[i][1]) < 2 * e["incertezza_m"], e
        assert e["incertezza_m"] > 1
    for k, s in enumerate(out["sorgenti"]):  # le sorgenti le fissano i mic bloccati
        assert np.hypot(s["pos"][0] - S[k][0], s["pos"][2] - S[k][1]) < 0.5, s
    assert out["mic"]["a"]["bloccato"] and out["mic"]["a"]["incertezza_m"] < out["mic"]["c"]["incertezza_m"]
