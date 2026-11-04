"""Immagine sonora di ogni microfono: quante sorgenti sente, con che ritardo,
quanto forti, da che direzione (se stereo) e a che distanza.

Tutto è misurato rispetto a un riferimento: la linea del mixer se c'è (segnale
asciutto, senza sala), altrimenti la traccia di riferimento del sync.

- Sorgenti: GCC-PHAT fotogramma per fotogramma; i fotogrammi dominati dalla
  stessa sorgente danno lo stesso vettore di ritardi su tutti i mic -> gruppi.
- Direzione: nei mic stereo differenza di livello (XY, M/S) o di tempo (capsule
  distanziate) fra sinistro e destro, nei fotogrammi di ciascuna sorgente.
- Distanza: risposta all'impulso linea -> mic. Rapporto diretto/riverbero e
  distanza critica della sala danno i metri; con lo stesso clock della linea
  il ritardo del picco diretto dà i metri in modo quasi esatto.

Convenzioni come in geometry: x destra +, z verso il pubblico, ritardo > 0 = arriva dopo.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import csd, welch

from . import media

C = 343.0
FS = 48000
FRAME_S = 0.2
MAX_TAU = 0.06          # ±60 ms (~20 m) attorno al sync
SPACING = {"integrato": 0.02, "spaziata": 0.17}  # m fra le capsule, se non coincidenti
Q = {"omni": 1.0, "cardioide": 2.0, "supercardioide": 3.0, "ms": 2.0}  # direttività per la distanza critica


def clock_key(t: dict) -> tuple:
    """Tracce con la stessa chiave condividono il clock: i loro ritardi sono acustici puri."""
    return (t.get("registratore") or t["wav"], round(t["info"]["duration"], 1))


def frame_gcc(ref: np.ndarray, x: np.ndarray, fs: float = FS, frame_s: float = FRAME_S,
              max_tau: float = MAX_TAU) -> tuple[np.ndarray, np.ndarray]:
    """Ritardo (s) e forza del picco GCC-PHAT di `x` rispetto a `ref`, per ogni fotogramma."""
    n = int(frame_s * fs)
    f = min(len(ref), len(x)) // n
    a, b = ref[: f * n].reshape(f, n), x[: f * n].reshape(f, n)
    nfft = 2 * n
    cross = np.fft.rfft(b, nfft) * np.conj(np.fft.rfft(a, nfft))
    cc = np.fft.irfft(cross / (np.abs(cross) + 1e-12), nfft)
    k = min(int(max_tau * fs), n - 1)
    cc = np.abs(np.concatenate([cc[:, -k:], cc[:, : k + 1]], axis=1))
    i = np.clip(cc.argmax(1), 1, 2 * k - 1)
    y0, y1, y2 = (cc[np.arange(f), i + d] for d in (-1, 0, 1))
    den = y0 - 2 * y1 + y2
    frac = np.where(den != 0, 0.5 * (y0 - y2) / np.where(den != 0, den, 1), 0)
    return (i + frac - k) / fs, y1


def cluster_sources(tau: np.ndarray, w: np.ndarray, tol: float = 0.3e-3, min_w: float = 0.08,
                    min_frac: float = 0.04, max_src: int = 6) -> list[np.ndarray]:
    """Raggruppa i fotogrammi [F, M] con lo stesso vettore di ritardi (entro `tol`
    sui mic validi in comune). Ritorna gli indici dei fotogrammi di ogni sorgente,
    dalla più presente."""
    ok = w > min_w
    T = np.where(ok, tau, np.nan)
    left = np.flatnonzero(ok.sum(1) >= max(1, min(2, tau.shape[1])))
    out = []
    while len(left) and len(out) < max_src:
        d = np.abs(T[left, None, :] - T[None, left, :])            # [L, L, M]
        common = np.isfinite(d).sum(-1)
        near = (np.nanmax(np.where(np.isfinite(d), d, 0), -1) < tol) & (common > 0)
        score = (near * w[left].sum(1)[None]).sum(1)
        members = left[near[score.argmax()]]
        if len(members) < min_frac * len(tau):
            break
        out.append(members)
        left = np.setdiff1d(left, members)
    return out


def stereo_direction(lr: np.ndarray, kind: str, fs: float = FS) -> tuple[float, float]:
    """Azimut (gradi, + = destra rispetto all'asse del mic) e fiducia 0..1 da un blocco [n, 2]."""
    l, r = lr[:, 0], lr[:, 1]
    el, er = np.sqrt(np.mean(l ** 2)) + 1e-12, np.sqrt(np.mean(r ** 2)) + 1e-12
    if kind == "coincidente":
        # due cardioidi a ±45°: g = 0.5 + 0.5 cos(θ ∓ 45°); si cerca θ che dà lo stesso ILD
        th = np.radians(np.arange(-90, 91))
        ild = np.log((0.5 + 0.5 * np.cos(th - np.pi / 4)) / (0.5 + 0.5 * np.cos(th + np.pi / 4)))
        target = np.log(er / el)
        az = float(np.degrees(th[np.abs(ild - target).argmin()]))
        conf = float(np.clip(1 - np.abs(target) / 3, 0.2, 0.9))  # oltre ~±26 dB è probabile un mic solo
        return az, conf
    from .sync import gcc_phat
    d = SPACING[kind]
    tau, peak = gcc_phat(l, r, fs, max_tau=d / C * 1.5)
    # a destra il suono arriva prima al canale destro: ritardo di R su L negativo
    return float(np.degrees(np.arcsin(np.clip(-tau * C / d, -1, 1)))), float(np.clip(peak * 2, 0, 0.9))


def stereo_kind(mic: dict | None) -> str | None:
    tipo = (mic or {}).get("tipo", "")
    if "XY" in tipo or "M/S" in tipo:
        return "coincidente"
    return "integrato" if tipo == "integrato" else None


def impulse_response(ref: np.ndarray, x: np.ndarray, fs: float = FS, n: int = 16384) -> np.ndarray:
    """Risposta all'impulso stimata ref -> x (Welch H1), centrata: indice n//2 = ritardo zero."""
    f, pxy = csd(ref, x, fs, nperseg=n)
    _, pxx = welch(ref, fs, nperseg=n)
    h = np.fft.irfft(pxy / (pxx + 1e-3 * pxx.max()), n)
    return np.roll(h, n // 2)


def distance_from_ir(h: np.ndarray, fs: float, room: dict, rt60: float, q: float = 1.0,
                     same_clock: bool = False) -> dict:
    """Distanza (m) dal rapporto diretto/riverbero, o dal ritardo se il clock è lo stesso."""
    c0 = len(h) // 2
    e = h ** 2
    p = int(np.argmax(np.abs(h)))
    w = int(0.0025 * fs)
    direct = e[max(p - w, 0): p + w].sum()
    rev = e[p + w: p + int(0.3 * fs)].sum() + 1e-20
    drr = float(10 * np.log10(direct / rev + 1e-20))
    prom = float(np.abs(h[p]) / (np.median(np.abs(h)) * 50 + 1e-20))  # picco netto = buona misura
    vol = room["w"] * room["d"] * room["h"]
    rc = 0.057 * np.sqrt(q * vol / max(rt60, 0.2))  # distanza critica (Sabine)
    out = {"drr_db": round(drr, 1), "ritardo_ms": round((p - c0) / fs * 1e3, 2),
           "distanza_m": round(float(np.clip(rc * 10 ** (-drr / 20), 0.3, 60)), 1),
           "fiducia_distanza": round(float(np.clip(prom, 0, 1)) * 0.5, 2), "metodo": "diretto/riverbero"}
    if same_clock and p > c0:  # stesso clock: il ritardo del suono diretto è il tempo di volo
        out.update(distanza_m=round((p - c0) / fs * C, 2), metodo="tempo di volo",
                   fiducia_distanza=round(float(np.clip(prom, 0, 1)) * 0.9, 2))
    return out


def read_aligned(t: dict, t0: float, dur: float, offset: float | None = None) -> np.ndarray:
    """[n, canali] della traccia sulla timeline da t0, con offset e drift del sync."""
    off = t["offset_s"] if offset is None else offset
    off -= t.get("drift_ppm", 0) * 1e-6 * (t0 - t.get("sync_t0", 0))
    x = media.read(t["wav"], t["channels"], t0 - off, dur, FS)
    if d := t.get("destra"):
        r = media.read(d["wav"], d["channels"], t0 - off - d.get("delta_s", 0), dur, FS)
        x = np.hstack([x[:, :1], r[:, :1]])
    return x.astype(np.float64)


def excerpt(ts: list[dict], max_s: float = 60.0) -> tuple[float, float]:
    """Tratto comune a tutte le tracce (al centro), al massimo `max_s` secondi."""
    a = max(t["offset_s"] for t in ts)
    b = min(t["offset_s"] + t["info"]["duration"] for t in ts)
    if b - a < 5:
        raise ValueError("meno di 5 s in comune fra le tracce")
    dur = min(b - a, max_s)
    return a + (b - a - dur) / 2, dur


def images(tracks: list[dict], ref: dict, room: dict, rt60: float, mics: dict,
           line: bool = False, max_s: float = 60.0) -> dict:
    """Immagine di ogni traccia rispetto a `ref`.

    `mics` = id microfono -> scheda del database. Ritorna {"riferimento", "sorgenti": [...],
    "tracce": {id: immagine}} pronto per la fusione e per il pannello.
    """
    others = [t for t in tracks if t is not ref]
    t0, dur = excerpt([ref] + others, max_s)
    leader = {}  # stesso clock del riferimento: si legge con l'offset del riferimento (ritardi acustici veri)
    rk = clock_key(ref)
    r = read_aligned(ref, t0, dur).mean(1)
    sig, same = {}, {}
    for t in others:
        same[t["id"]] = clock_key(t) == rk
        sig[t["id"]] = read_aligned(t, t0, dur, ref["offset_s"] if same[t["id"]] else None)
    ids = list(sig)
    gcc = [frame_gcc(r, sig[i].mean(1)) for i in ids]
    tau, w = np.stack([g[0] for g in gcc], 1), np.stack([g[1] for g in gcc], 1)
    groups = cluster_sources(tau, w)
    n = int(FRAME_S * FS)
    frame_db = lambda x: 10 * np.log10((x[: len(tau) * n].reshape(len(tau), n, -1) ** 2).mean((1, 2)) + 1e-20)
    ref_db = frame_db(r[:, None])
    sources = []
    for k, fr in enumerate(groups):
        sources.append({"k": k, "presenza": round(len(fr) / len(tau), 2),
                        "ritardi_ms": {i: round(float(np.nanmedian(np.where(w[fr, j] > 0.08, tau[fr, j], np.nan))) * 1e3, 3)
                                       if np.any(w[fr, j] > 0.08) else None for j, i in enumerate(ids)}})
    out = {}
    for j, t in enumerate(others):
        x, db = sig[t["id"]], frame_db(sig[t["id"]])
        img = {"stesso_clock": same[t["id"]], "sorgenti": []}
        kind = stereo_kind(mics.get(t.get("microfono") or "")) if x.shape[1] == 2 and not t.get("destra") else None
        for s, fr in zip(sources, groups):
            heard = w[fr, j] > 0.08
            if heard.mean() < 0.3:
                continue
            e = {"k": s["k"], "ritardo_ms": s["ritardi_ms"][t["id"]],
                 "livello_db": round(float(np.median(db[fr] - ref_db[fr])), 1),
                 "fiducia": round(min(1.0, float(heard.mean() * np.median(w[fr, j]) * 3)), 2)}
            if kind:
                blk = np.concatenate([x[f * n:(f + 1) * n] for f in fr[heard]])
                e["azimut_deg"], e["fiducia_azimut"] = (round(v, 2) for v in stereo_direction(blk, kind))
            img["sorgenti"].append(e)
        img["n_sorgenti"] = len(img["sorgenti"])
        if line:
            q = Q.get((mics.get(t.get("microfono") or "") or {}).get("diagramma"), 1.0)
            img.update(distance_from_ir(impulse_response(r, x.mean(1)), FS, room, rt60, q, same[t["id"]]))
        img["fiducia"] = round(float(np.mean([e["fiducia"] for e in img["sorgenti"]] or [0])), 2)
        out[t["id"]] = img
    return {"riferimento": ref["id"], "linea": line, "tratto_s": [round(t0, 2), round(dur, 2)],
            "sorgenti": sources, "tracce": out}
