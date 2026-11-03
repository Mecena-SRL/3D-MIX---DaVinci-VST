"""Auto-taratura dell'EQ: propone bande spiegate, che restano modificabili.

Per ogni traccia, sullo spettro medio (dopo la correzione del microfono):
  1. passa-alto secondo tipo di sorgente e banda del microfono;
  2. risonanze persistenti -> campane strette dinamiche (agiscono solo quando suonano);
  3. bilanciamento tonale verso un target per tipo di sorgente;
  4. sala: se i bassi riverberano più dei medi (RT60 dello spazio) -> taglio dinamico a 200 Hz.
Poi fra tracce: dove due tracce si mascherano, scava sulla meno importante.
Le bande manuali ("auto": False) non vengono mai toccate.
"""
from __future__ import annotations

import uuid

import numpy as np
from scipy.signal import find_peaks, welch

from . import devices, eq, media
from .mixer import correction_fir

GRID = 20 * 2 ** (np.arange(0, 10 * 24) / 24)  # 20 Hz-20 kHz, 1/24 di ottava
SEG_S, N_SEG = 8.0, 8

# tipo di sorgente: pendenza del target (dB/ottava), passa-alto (Hz), priorità
TIPI = {"voce": (-3.5, 90, 3), "strumento": (-4.5, 40, 2), "generico": (-4.5, 30, 1), "ambiente": (-5.0, 30, 0)}
DA_RUOLO = {"spot": "strumento", "ambiente": "ambiente", "base": "generico"}


def tipo(t: dict) -> str:
    return t.get("sorgente") if t.get("sorgente") in TIPI else DA_RUOLO.get(t.get("ruolo"), "generico")


def _band(perche: str, **kw) -> dict:
    return {"id": uuid.uuid4().hex[:6], "on": True, "auto": True, "dyn": None, "perche": perche, **kw}


def _smooth(y: np.ndarray, octaves: float) -> np.ndarray:
    w = max(1, int(octaves * 24))
    return np.convolve(np.pad(y, w, mode="edge"), np.ones(2 * w + 1) / (2 * w + 1), "same")[w:-w]


def segments(t: dict, sr: int, project: dict) -> list[np.ndarray]:
    """Fino a N_SEG estratti mono distribuiti sulla traccia, già con la correzione mic."""
    dur = t["info"]["duration"]
    starts = np.linspace(0, max(dur - SEG_S, 0), N_SEG if dur > SEG_S * 2 else 1)
    mic = t.get("microfono")
    fir = correction_fir(mic, sr) if mic and project.get("correzione", True) else None
    out = []
    for s in starts:
        x = media.read(t["wav"], t["channels"], float(s), min(SEG_S, dur), sr).mean(axis=1)
        if fir is not None:
            x = np.convolve(x, fir, "same")
        if np.sqrt(np.mean(x ** 2)) > 1e-4:  # salta il silenzio
            out.append(x)
    return out


def spectrum(segs: list[np.ndarray], sr: int) -> tuple[np.ndarray, np.ndarray]:
    """Spettro medio e per estratto (dB) sulla griglia GRID, a 1/24 di ottava."""
    per = []
    for x in segs:
        f, p = welch(x, sr, nperseg=min(8192, len(x)))
        edges = GRID[:, None] * 2 ** (np.array([-1, 1]) / 48)
        per.append([p[(f >= lo) & (f < hi)].mean() if np.any((f >= lo) & (f < hi)) else np.interp(c, f, p)
                    for c, (lo, hi) in zip(GRID, edges)])
    per = np.array(per) + 1e-20
    return 10 * np.log10(per.mean(axis=0)), 10 * np.log10(per)


def resonances(segs, fine, per, sr, lo_hz, top=3) -> list[dict]:
    excess = fine - _smooth(fine, 1 / 3)
    rng = (GRID > max(lo_hz, 80)) & (GRID < 8000)
    peaks, props = find_peaks(np.where(rng, excess, 0), height=5, distance=8)
    persist = ((per - np.array([_smooth(p, 1 / 3) for p in per]))[:, peaks] > 3).mean(axis=0)
    out = []
    for i in sorted(peaks[persist >= 0.6], key=lambda i: -excess[i])[:top]:
        b = _band(f"risonanza fissa a {GRID[i]:.0f} Hz (+{excess[i]:.1f} dB sullo spettro, presente "
                  f"nel {persist[list(peaks).index(i)] * 100:.0f}% degli estratti): taglia solo quando suona",
                  tipo="campana", f=round(float(GRID[i])), q=8.0, g=-round(float(min(excess[i], 8)), 1))
        b["dyn"] = {"soglia_db": _threshold(segs, b, sr, 60), "rapporto": 3.0, "attacco_ms": 5, "rilascio_ms": 120}
        out.append(b)
    return out


def _threshold(segs, b, sr, pct) -> float:
    lv = np.concatenate([eq.level_db(eq.component(b, x, sr)[:, None], sr, {"attacco_ms": 5, "rilascio_ms": 80})
                         for x in segs])
    return round(float(np.percentile(lv[lv > -100], pct)), 1) if np.any(lv > -100) else -40.0


def balance(broad: np.ndarray, kind: str, hp_hz: float, n=3) -> list[dict]:
    slope = TIPI[kind][0]
    tgt = slope * np.log2(GRID / 1000)
    mid = (GRID > 200) & (GRID < 5000)
    dev = _smooth(broad - tgt - np.median((broad - tgt)[mid]), 0.5)
    rng = (GRID > max(hp_hz * 2, 80)) & (GRID < 14000)
    out = []
    for _ in range(n):
        i = int(np.argmax(np.where(rng, np.abs(dev), 0)))
        rng &= np.abs(np.log2(GRID / GRID[i])) > 1  # una sola correzione per ottava
        if abs(dev[i]) < 2.5:
            break
        fc = float(GRID[i])
        ty = "shelf_basso" if fc < 150 else "shelf_alto" if fc > 7000 else "campana"
        # si alza poco e mai sotto 250 Hz: si alzerebbero anche rumore e rimbombo della sala
        g = round(float(np.clip(-0.7 * dev[i], -6, 3 if fc > 250 else 0)), 1)
        if not g:
            continue
        b = _band(f"{'troppo' if dev[i] > 0 else 'poco'} {_zona(fc)} rispetto al target '{kind}' "
                  f"({dev[i]:+.1f} dB intorno a {fc:.0f} Hz)", tipo=ty, f=round(fc), q=1.0, g=g)
        dev = dev + eq.response_db([b], GRID)
        out.append(b)
    return out


def _zona(f: float) -> str:
    return next(n for lim, n in [(120, "sub/bassi"), (400, "medio-bassi (fango)"), (2000, "medi"),
                                 (6000, "presenza"), (1e9, "aria/sibilanti")] if f < lim)


def room(segs, rt60: dict | None, kind: str, sr: int) -> list[dict]:
    rt = {k: float(v) for k, v in (rt60 or {}).items()}
    lo = np.mean([rt[k] for k in ("125", "250") if k in rt] or [0])
    mid = rt.get("1k") or rt.get("1000") or rt.get("500")
    if kind not in ("ambiente", "generico") or not mid or lo < 1.15 * mid:
        return []
    b = _band(f"la sala rimbomba sui bassi (RT60 {lo:.1f} s a 125-250 Hz contro {mid:.1f} s a 1 kHz): "
              "taglio dinamico sui passaggi forti", tipo="campana", f=200, q=0.8,
              g=-round(float(np.clip(6 * (lo / mid - 1), 1.5, 4)), 1))
    b["dyn"] = {"soglia_db": _threshold(segs, b, sr, 50), "rapporto": 2.0, "attacco_ms": 20, "rilascio_ms": 200}
    return [b]


def masking(project: dict, spectra: dict) -> dict[str, list[dict]]:
    """Per ogni coppia: dove entrambe sono forti e a livello simile, scava sulla meno importante."""
    ts = [t for t in project["tracks"] if t["id"] in spectra and not t.get("mute")]
    rng = (GRID > 150) & (GRID < 5000)
    out: dict[str, list[dict]] = {}
    for i, a in enumerate(ts):
        for b in ts[i + 1:]:
            pa, pb = TIPI[tipo(a)][2], TIPI[tipo(b)][2]
            if pa == pb:
                continue
            hi, lo = (a, b) if pa > pb else (b, a)
            sh, sl = (spectra[hi["id"]] + hi.get("gain_db", 0), spectra[lo["id"]] + lo.get("gain_db", 0))
            strong = (sh > sh[rng].max() - 6) & (sl > sl[rng].max() - 6) & (np.abs(sh - sl) < 6) & rng
            if not strong.any():
                continue
            k = int(np.argmax(np.where(strong, np.minimum(sh, sl), -np.inf)))
            out.setdefault(lo["id"], []).append(_band(
                f"lascia spazio a '{hi['nome']}' intorno a {GRID[k]:.0f} Hz (si mascherano)",
                tipo="campana", f=round(float(GRID[k])), q=1.4, g=-2.5))
    return out


def run(project: dict, rt60: dict | None = None, ids: list[str] | None = None, progress=lambda f: None) -> dict:
    """Propone e applica le bande auto. Ritorna {id traccia: n bande}."""
    sr = project.get("sr", 48000)
    ts = [t for t in project["tracks"] if ids is None or t["id"] in ids]
    spectra, props = {}, {}
    for n, t in enumerate(ts):
        segs = segments(t, sr, project)
        if not segs:
            continue
        fine, per = spectrum(segs, sr)
        kind = tipo(t)
        mic = devices.load()["microfoni"].get(t.get("microfono"), {})
        hp_hz = max(TIPI[kind][1], 0.8 * mic.get("banda", [20])[0])
        bands = [_band(f"passa-alto per '{kind}': sotto {hp_hz:.0f} Hz c'è solo rimbombo e rumore",
                       tipo="passa_alto", f=round(hp_hz), pendenza=12 if kind == "ambiente" else 24)]
        bands += resonances(segs, fine, per, sr, hp_hz) + balance(_smooth(fine, 1 / 3), kind, hp_hz)
        bands += room(segs, rt60, kind, sr)
        spectra[t["id"]], props[t["id"]] = _smooth(fine, 1 / 3), bands
        t["eq_analisi"] = {"f": np.round(GRID, 1).tolist(), "db": np.round(fine, 1).tolist(), "sorgente": kind}
        progress((n + 1) / len(ts))
    for tid, extra in masking(project, spectra).items():
        props.setdefault(tid, []).extend(extra)
    for t in ts:
        if t["id"] in props:
            t["eq"] = [b for b in t.get("eq") or [] if not b.get("auto")] + props[t["id"]]
    return {tid: len(b) for tid, b in props.items()}
