"""Gaussian splatting sonoro: da energie per ottava di una scena nota tornano posizioni, raggi e timbri."""
import numpy as np

from mix3d import splat
from mix3d.localize import BANDS

STAGE = {"w": 12.0, "d": 4.0}
MICS = {"a": [-4.0, 1.5, -1.0], "b": [4.0, 1.5, -1.5], "c": [0.0, 1.5, 3.0], "d": [-6.0, 1.5, 8.0],
        "e": [6.0, 1.5, 10.0], "f": [0.0, 1.5, 15.0]}
TRUE = [  # voce solista stretta e brillante, coro largo e scuro
    {"k": 0, "pos": [-3.0, 1.5, -2.0], "r": 0.3, "e": np.array([-20, -14, -10, -8, -8, -10, -16.0])},
    {"k": 1, "pos": [3.0, 1.5, -2.5], "r": 3.0, "e": np.array([-8, -6, -8, -12, -16, -22, -30.0])},
]
DIF = -18.0


def _obs(noise=0.3, seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for i, m in MICS.items():
        for s in TRUE:
            d2 = np.sum((np.array(s["pos"]) - m) ** 2)
            p = s["e"] + 10 * np.log10(1 / (d2 + s["r"] ** 2) + 10 ** (DIF / 10))
            out.append((i, s["k"], (p + rng.normal(0, noise, len(BANDS))).tolist()))
    return out


def test_fit_recovers_splats():
    seeds = [{"k": s["k"], "pos": [s["pos"][0] + 0.6, 1.5, s["pos"][2] - 0.4], "incertezza_m": 1.5} for s in TRUE]
    out = splat.fit(_obs(), {i: {"pos": m, "a": 1.0} for i, m in MICS.items()}, seeds, STAGE)
    g0, g1 = out["gaussiane"]
    err = lambda g, s: np.hypot(g["pos"][0] - s["pos"][0], g["pos"][2] - s["pos"][2])
    assert err(g0, TRUE[0]) < 0.5, g0       # sorgente piccola: i livelli raffinano la fusione (partenza a 0,7 m)
    assert err(g1, TRUE[1]) < 0.8, g1       # sorgente larga: il centro resta vago, ma non peggiora
    assert g0["raggio_m"] < 1.0 < 2.0 < g1["raggio_m"], (g0, g1)
    assert g0["centroide_hz"] > 2 * g1["centroide_hz"]
    assert abs(np.mean(out["diffuso_db"]) - DIF) < 2 and out["errore_db"] < 1


def test_field_at_listener_near_is_louder():
    f = {"gaussiane": [{"id": "g0", "pos": [0, 1.5, 0], "raggio_m": 0.5, "bande_db": [0.0] * 7}], "diffuso_db": [-20.0] * 7}
    near, far = splat.field_at(f, [0, 1.5, 2])["g0"], splat.field_at(f, [0, 1.5, 12])["g0"]
    assert near["diretto_db"][0] > far["diretto_db"][0] + 10 and near["diffuso_db"] == far["diffuso_db"]
