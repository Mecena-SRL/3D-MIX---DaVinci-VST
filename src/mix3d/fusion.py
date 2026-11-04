"""Fusione delle immagini sonore: posizioni di mic e sorgenti in un'unica scena.

Un'ottimizzazione ai minimi quadrati robusti (scipy) trova insieme:
- posizione (x, z) di ogni mic e di ogni sorgente (y fissa: altezza tipica),
- lo scarto di clock di ogni registratore diverso da quello del riferimento,
- il guadagno di ogni mic (per usare i livelli relativi fra sorgenti).

Cosa la vincola, ognuno pesato con la propria fiducia:
- ritardi sorgente -> mic (TDOA rispetto al riferimento, schema di Ono et al. per
  registrazioni non sincronizzate: lo scarto di clock è un'incognita),
- distanza dalla sorgente principale (tempo di volo o diretto/riverbero),
- direzione nei mic stereo (asse rivolto al centro del palco),
- livelli: la stessa sorgente più lontana suona più piano,
- posizioni di partenza deboli (profilo, sala) e forti per i mic bloccati a mano.

L'incertezza di ogni posizione viene dalla covarianza (J^T J)^-1: è quella che il
pannello mostra come cerchio attorno a ogni punto.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

C = 343.0
SRC_Y = 1.5


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def fuse(imgs: dict, start: dict[str, list[float]], locked: set[str], stage: dict) -> dict:
    """`imgs` = risultato di localize.images; `start` = posizione iniziale [x, y, z] per id
    (mic in sala, riferimento compreso se è un mic); `locked` = id con posizione data dall'utente."""
    line, ref = imgs["linea"], imgs["riferimento"]
    mics = [i for i in start if i in imgs["tracce"] or (i == ref and not line)]
    srcs = imgs["sorgenti"]
    if not mics or not srcs:
        raise ValueError("nessuna sorgente o nessun mic da posizionare")
    clocks = [i for i in mics if i != ref and not imgs["tracce"][i]["stesso_clock"]]
    M, K = len(mics), len(srcs)
    mi = {i: n for n, i in enumerate(mics)}
    p0 = np.array([[start[i][0], start[i][2]] for i in mics], float)
    s0 = np.array([[(k - (K - 1) / 2) * stage["w"] / (K + 1), -stage["d"] / 2] for k in range(K)])

    def unpack(v):
        m = v[: 2 * M].reshape(M, 2)
        s = v[2 * M: 2 * M + 2 * K].reshape(K, 2)
        o = dict(zip(clocks, v[2 * M + 2 * K: 2 * M + 2 * K + len(clocks)]))
        g = v[2 * M + 2 * K + len(clocks):]
        return m, s, o, g

    def dist(m, s, i, k):
        return float(np.hypot(*(m[mi[i]] - s[k]))) if i in mi else 0.0  # la linea è "alla sorgente"

    def residuals(v):
        m, s, o, g = unpack(v)
        r = []
        for tid, img in imgs["tracce"].items():
            if tid not in mi:
                continue
            for e in img["sorgenti"]:
                k = e["k"]
                if e.get("ritardo_ms") is not None:  # tempo di arrivo rispetto al riferimento
                    pred = (dist(m, s, tid, k) - (dist(m, s, ref, k) if not line else 0)) / C + o.get(tid, 0)
                    r.append((pred * 1e3 - e["ritardo_ms"]) / (0.3 / max(e["fiducia"], 0.05)))
                pred_db = -20 * np.log10(max(dist(m, s, tid, k), 0.3)) + g[mi[tid]]
                r.append((pred_db - e["livello_db"]) / 4.0)
                if "azimut_deg" in e:  # asse del mic stereo verso il centro del palco
                    ax = np.arctan2(-m[mi[tid]][0], -(m[mi[tid]][1] + stage["d"] / 2))
                    d = s[k] - m[mi[tid]]
                    az = _wrap(np.arctan2(d[0], d[1]) - ax)
                    r.append(np.degrees(_wrap(az - np.radians(e["azimut_deg"]))) / (15 / max(e["fiducia_azimut"], 0.1)))
            if img.get("distanza_m") and img["sorgenti"]:
                # la sorgente del picco diretto: quella con il ritardo più vicino al picco della risposta
                k = min(img["sorgenti"], key=lambda e: abs((e["ritardo_ms"] or 0) - img.get("ritardo_ms", 0))
                        if "ritardo_ms" in img else -e["fiducia"])["k"]
                sig = 0.08 if img.get("metodo") == "tempo di volo" else 0.6
                sig /= max(img.get("fiducia_distanza", 0.1), 0.1)
                r.append(np.log(max(dist(m, s, tid, k), 0.3) / img["distanza_m"]) / sig)
        for n, i in enumerate(mics):  # punto di partenza: debole, forte se bloccato a mano
            r.extend((m[n] - p0[n]) / (0.05 if i in locked else 4.0))
        r.extend(((s - s0) / np.array([stage["w"] / 2, stage["d"] / 2])).ravel())  # le sorgenti stanno sul palco
        r.extend(np.array(list(o.values())) / 0.05)
        return np.array(r)

    def guess(src):  # scarti di clock e guadagni iniziali coerenti con il punto di partenza
        m, v = p0, []
        for i in clocks + mics:
            es = imgs["tracce"].get(i, {}).get("sorgenti", [])
            d = [float(np.hypot(*(m[mi[i]] - src[e["k"]]))) for e in es]
            if len(v) < len(clocks):
                v.append(np.mean([e["ritardo_ms"] / 1e3 - x / C for e, x in zip(es, d) if e["ritardo_ms"] is not None] or [0]))
            else:
                v.append(np.mean([e["livello_db"] + 20 * np.log10(max(x, 0.3)) for e, x in zip(es, d)] or [0]))
        return np.concatenate([p0.ravel(), src.ravel(), v])

    # più partenze (le sorgenti possono stare in qualunque ordine sul palco): vince il costo minore
    rng = np.random.default_rng(0)
    starts = [s0] + [s0[rng.permutation(K)] for _ in range(min(5, K * K))]
    sol = min((least_squares(residuals, guess(x), loss="soft_l1", f_scale=2.0) for x in starts), key=lambda r: r.cost)
    m, s, o, _ = unpack(sol.x)
    try:
        cov = np.linalg.pinv(sol.jac.T @ sol.jac)
        sd = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        sd = np.full(len(sol.x), 9.9)
    unc = lambda n: round(float(min(np.hypot(sd[2 * n], sd[2 * n + 1]), 99)), 2)
    return {
        "mic": {i: {"pos": [round(float(m[n][0]), 2), start[i][1], round(float(m[n][1]), 2)],
                    "incertezza_m": unc(n), "bloccato": i in locked} for n, i in enumerate(mics)},
        "sorgenti": [{"k": e["k"], "pos": [round(float(s[k][0]), 2), SRC_Y, round(float(s[k][1]), 2)],
                      "incertezza_m": unc(M + k), "presenza": e["presenza"]} for k, e in enumerate(srcs)],
        "scarti_clock_ms": {i: round(float(x) * 1e3, 2) for i, x in o.items()},
        "residuo": round(float(np.sqrt(np.mean(sol.fun ** 2))), 2),
    }
