"""Gaussian splatting sonoro: il campo della sala come insieme di gaussiane 3D.

Ogni gaussiana è una sorgente estesa: posizione, raggio (voce solista piccola,
coro o sezione larga) ed energia per ottava. La sala aggiunge un campo diffuso
per banda (la "gaussiana infinita": il riverbero è uguale ovunque).

Come nel 3D Gaussian Splatting, ma i mic fanno da fotocamere: si "renderizza"
quanto ogni mic dovrebbe sentire di ogni sorgente, banda per banda,

    P = g_mic * E_banda * (D(θ) / (d² + r²) + diffuso_banda)

(d = distanza dal centro, r = raggio, D = direttività del mic, g = sensibilità del
mic) e si ottimizzano le gaussiane finché coincide con le energie misurate
(localize.band_db sui fotogrammi di ogni sorgente). Minimi quadrati in dB, scipy.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from .localize import BANDS

PATTERN = {"omni": 1.0, "cardioide": 0.5, "supercardioide": 0.37, "ms": 0.5, "nessuno": 1.0}


def directivity(a: float, mic: np.ndarray, axis: np.ndarray, p: np.ndarray) -> float:
    """Guadagno in energia del mic (pattern a + (1-a)cosθ) verso il punto p."""
    v = p - mic
    c = float(v @ axis / (np.linalg.norm(v) * np.linalg.norm(axis) + 1e-9))
    return max(a + (1 - a) * c, 0.05) ** 2


def stage_axis(mic: np.ndarray, stage: dict) -> np.ndarray:
    """I mic guardano il centro del palco (come in fusion)."""
    return np.array([0.0, mic[1], -stage["d"] / 2]) - mic


def fit(obs: list[tuple[str, int, list[float]]], mics: dict[str, dict], seeds: list[dict],
        stage: dict) -> dict:
    """`obs` = (id mic, sorgente k, energie per ottava dB); `mics` = id -> {"pos", "a"};
    `seeds` = sorgenti della fusione ({"k", "pos", "incertezza_m"}): punto di partenza."""
    B, K = len(BANDS), len(seeds)
    ids = sorted({o[0] for o in obs})
    mi = {i: n for n, i in enumerate(ids)}
    kk = {s["k"]: n for n, s in enumerate(seeds)}
    obs = [o for o in obs if o[1] in kk]
    if not obs:
        raise ValueError("nessuna energia per banda da spiegare")
    M = {i: np.asarray(mics[i]["pos"], float) for i in ids}
    ax = {i: stage_axis(M[i], stage) for i in ids}
    p0 = np.array([s["pos"] for s in seeds], float)
    # i ritardi (fusione) dicono dove sta il centro meglio dei livelli: qui si raffina entro ~1 m
    prior = np.ones(K)
    O = np.array([o[2] for o in obs], float)
    e0 = [np.max([o[2] for o in obs if o[1] == s["k"]] or [[-40.0] * B], axis=0) + 20 for s in seeds]

    def unpack(v):
        xz = v[: 2 * K].reshape(K, 2)
        r = np.exp(v[2 * K: 3 * K])
        e = v[3 * K: 3 * K + K * B].reshape(K, B)
        dif = v[3 * K + K * B: 3 * K + K * B + B]
        g = v[3 * K + K * B + B:]
        pos = np.column_stack([xz[:, 0], p0[:, 1], xz[:, 1]])
        return pos, r, e, dif, g

    I = np.array([mi[o[0]] for o in obs]); Kx = np.array([kk[o[1]] for o in obs])
    Mx = np.array([M[i] for i in ids]); AX = np.array([ax[i] for i in ids])
    A = np.array([mics[i].get("a", 1.0) for i in ids])

    def render(pos, r, e, dif, g):
        """Energia per banda prevista a ogni osservazione [N, B] (dB)."""
        v = pos[Kx] - Mx[I]
        d2 = (v ** 2).sum(1)
        cos = (v * AX[I]).sum(1) / (np.sqrt(d2) * np.linalg.norm(AX[I], axis=1) + 1e-9)
        dirg = np.maximum(A[I] + (1 - A[I]) * cos, 0.05) ** 2
        direct = dirg / (d2 + r[Kx] ** 2)
        return g[I][:, None] + e[Kx] + 10 * np.log10(direct[:, None] + 10 ** (dif[None] / 10))

    def residuals(v):
        pos, r, e, dif, g = unpack(v)
        res = [((render(pos, r, e, dif, g) - O) / 2.0).ravel()]  # 2 dB di tolleranza sulle misure
        res.append(((pos[:, [0, 2]] - p0[:, [0, 2]]) / prior[:, None]).ravel())
        res.append(np.log(r) / 3.0)                              # raggio attorno a 1 m, senza forzare
        res.append([g.mean() / 0.1])                             # scala: sensibilità media 0 dB
        res.append((dif + 15) / 15)                              # diffuso tipico, prior debole
        return np.concatenate([np.atleast_1d(x) for x in res])

    v0 = np.concatenate([p0[:, [0, 2]].ravel(), np.zeros(K), np.ravel(e0), np.full(B, -15.0), np.zeros(len(ids))])
    sol = least_squares(residuals, v0, loss="soft_l1", f_scale=2.0)
    pos, r, e, dif, _ = unpack(sol.x)
    try:
        sd = np.sqrt(np.clip(np.diag(np.linalg.pinv(sol.jac.T @ sol.jac)), 0, None))
    except np.linalg.LinAlgError:
        sd = np.full(len(sol.x), 9.9)
    err = render(*unpack(sol.x)) - O
    out = []
    for n, s in enumerate(seeds):
        lin = 10 ** (e[n] / 10)
        out.append({"id": f"g{s['k']}", "k": s["k"], "pos": [round(float(c), 2) for c in pos[n]],
                    "raggio_m": round(float(r[n]), 2), "bande_db": np.round(e[n], 1).tolist(),
                    "livello_db": round(float(10 * np.log10(lin.sum())), 1),
                    "centroide_hz": int(np.exp((lin * np.log(BANDS)).sum() / lin.sum())),
                    "incertezza_m": round(float(min(np.hypot(sd[2 * n], sd[2 * n + 1]), 99)), 2)})
    return {"bande_hz": BANDS.astype(int).tolist(), "gaussiane": out,
            "diffuso_db": np.round(dif, 1).tolist(), "errore_db": round(float(np.sqrt(np.mean(err ** 2))), 1)}


def field_at(field: dict, p, a: float = 1.0, axis=None) -> dict:
    """Cosa sente un punto (es. l'ascoltatore) per ogni gaussiana: energia diretta e diffusa per banda (dB)."""
    p = np.asarray(p, float)
    dif = np.asarray(field["diffuso_db"])
    out = {}
    for s in field["gaussiane"]:
        c = np.asarray(s["pos"], float)
        dirg = directivity(a, p, np.asarray(axis, float), c) if axis is not None else 1.0
        direct = np.asarray(s["bande_db"]) + 10 * np.log10(dirg / (np.sum((c - p) ** 2) + s["raggio_m"] ** 2))
        out[s["id"]] = {"diretto_db": np.round(direct, 1).tolist(), "diffuso_db": np.round(np.asarray(s["bande_db"]) + dif, 1).tolist()}
    return out
