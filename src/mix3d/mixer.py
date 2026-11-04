"""Mix stereo a blocchi: stesso codice per l'ascolto in tempo reale e per la stampa.

Per ogni traccia: lettura allineata (offset + drift), correzione del colore
del microfono (FIR dal database), EQ della traccia (eq.py), guadagno, distanza e pan rispetto
all'ascoltatore virtuale. In modalità B (bypass) solo somma con i guadagni.
"""
from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

import numpy as np
import soundfile as sf
from scipy.signal import firwin2, oaconvolve

from . import ambiente, devices, eq, look, media
from .analysis import Loudness
from .geometry import spatial_params

POOL = ThreadPoolExecutor(8)
FIR_TAPS = 1023
PAD_S = 0.25  # pre-roll: assesta FIR, filtri IIR e inviluppi dell'EQ fra un blocco e l'altro


@lru_cache(maxsize=64)
def correction_fir(mic_id: str, sr: int) -> np.ndarray:
    mic = devices.load()["microfoni"][mic_id]
    f = np.linspace(0, sr / 2, 256)
    g = 10 ** (devices.correction_db(mic, f) / 20)
    return firwin2(FIR_TAPS, f / (sr / 2), g)


@lru_cache(maxsize=256)
def band_fir(bands_db: tuple, sr: int) -> np.ndarray:
    """FIR a fase lineare dai guadagni per ottava (125 Hz .. 8 kHz), interpolati in log-frequenza."""
    from .localize import BANDS
    f = np.linspace(0, sr / 2, 512)
    g = 10 ** (np.interp(np.log2(np.maximum(f, 20)), np.log2(BANDS), bands_db) / 20)
    return firwin2(FIR_TAPS, f / (sr / 2), g)


def active(tracks: list[dict]) -> list[dict]:
    solo = any(t.get("solo") for t in tracks)
    return [t for t in tracks if not t.get("mute") and (t.get("solo") or not solo)]


def render(project: dict, t0: float, dur: float, bypass: bool = False) -> tuple[np.ndarray, dict]:
    """Blocco stereo [n, 2] dalla posizione t0 (s di timeline) e livelli per traccia (dBFS).
    Si lavora con PAD_S di pre-roll fino all'EQ del master, poi si scarta."""
    sr = project.get("sr", 48000)
    n, m = int(round(dur * sr)), int(round(PAD_S * sr))
    out = np.zeros((n + m, 2), np.float32)
    amb, n_amb = np.zeros((n + m, 2), np.float32), 0  # bus ambiente (camere, action cam, registratori)
    fx = ambiente.settings(project)
    levels, env = {}, {}
    field = (project.get("ascolto_campo") or {}) if project.get("campo_ascolto") else {}

    errors = {}

    def load(t):  # lettura allineata (offset + drift); le letture dei video vanno in parallelo
        try:
            return _load(t)
        except Exception as e:  # una clip illeggibile tace, l'ascolto delle altre continua
            errors[t["id"]] = str(e)[:160]

    def _load(t):
        off = t["offset_s"] - t.get("drift_ppm", 0) * 1e-6 * (t0 - t.get("sync_t0", 0))
        x = media.read(t["wav"], t["channels"], t0 - off - m / sr, (n + m) / sr, sr)[: n + m]
        if d := t.get("destra"):  # due mono uniti in stereo: il secondo canale è il destro
            r = media.read(d["wav"], d["channels"], t0 - off - d.get("delta_s", 0) - m / sr, (n + m) / sr, sr)[: n + m]
            x = np.hstack([x[:, :1], r[:, :1]])
        return x

    # solo le clip che suonano in questo blocco: in una timeline da ore le altre non si leggono
    ts = [t for t in active(project["tracks"])
          if t["offset_s"] - PAD_S < t0 + dur and t0 - PAD_S < t["offset_s"] + t["info"]["duration"]]
    for t, x in zip(ts, POOL.map(load, ts)):
        if x is None:
            continue
        mic = t.get("microfono")
        line = is_line(t)
        if mic and not line and project.get("correzione", True) and not bypass:
            x = oaconvolve(x, correction_fir(mic, sr)[:, None], axes=0)[FIR_TAPS // 2:][: len(x)]
        if t.get("eq") and not bypass:
            x = eq.process(x, t["eq"], sr)
        if (bands := field.get(t["id"])) and not bypass:  # ascolto dal campo: EQ per ottava dalle gaussiane
            x = oaconvolve(x, band_fir(tuple(bands), sr)[:, None], axes=0)[FIR_TAPS // 2:][: len(x)]
        g = 10 ** (t.get("gain_db", 0) / 20)
        env[t["id"]] = envelope_db(x[m:] * g)
        if x.shape[1] == 1:
            x = np.repeat(x, 2, axis=1)
        if line:  # ingresso di linea (mixer): niente distanza né posizione, solo il pan della traccia
            th = (np.clip(t.get("pan", 0), -1, 1) + 1) * np.pi / 4
            if t.get("pan"):
                x = x * np.array([np.cos(th), np.sin(th)]) * np.sqrt(2)
        elif not bypass:
            dist, pan = spatial_params(t["pos"], project["listener"])
            pan = np.clip(pan * project.get("larghezza", 1.0) + t.get("pan", 0), -1, 1)
            if not field:  # col campo la distanza è già nei pesi delle bande
                g *= (project.get("dist_ref_m", 5.0) / dist) ** project.get("attenuazione", 0.5)
            th = (pan + 1) * np.pi / 4  # pan a potenza costante
            x = x * np.array([np.cos(th), np.sin(th)]) * np.sqrt(2)
        x = x * g
        if not bypass and ambiente.ruolo(t) == "ambiente":
            amb[: len(x)] += x
            n_amb += 1
            x = x * fx["ambiente"] / np.sqrt(n_amb)  # solo per il livello mostrato (circa)
        else:
            out[: len(x)] += x
        levels[t["id"]] = round(float(20 * np.log10(np.sqrt(np.mean(x[m:] ** 2)) + 1e-10)), 1)
    if n_amb:  # a potenza costante: più camere non vuol dire più riverbero
        rt = (project.get("spazio_stimato") or {}).get("rt60") or 1.2
        out += ambiente.asciuga(amb, sr, rt, fx["asciuga"]) * (fx["ambiente"] / np.sqrt(n_amb))
    if project.get("eq_master") and not bypass:
        out = eq.process(out, project["eq_master"], sr)
    if project.get("look") and not bypass:  # uscita della pipeline: carattere, EQ, colla
        out = look.apply(out, project, sr)
    if not bypass:
        out = ambiente.reverb(ambiente.compress(out, project, sr)[m:], project, sr, t0)
    else:
        out = out[m:]
    out = out * 10 ** (project.get("master_db", 0) / 20)
    levels["master"] = round(float(20 * np.log10(np.abs(out).max(initial=0) + 1e-10)), 1)
    levels["env"] = env
    if errors:
        levels["errori"] = errors
    return out, levels


def is_line(t: dict) -> bool:
    """Traccia registrata in linea (uscita del mixer), non da un microfono in sala."""
    mic = devices.load()["microfoni"].get(t.get("microfono") or "", {})
    return mic.get("tipo") == "linea"


def envelope_db(x: np.ndarray, frames: int = 10) -> list[float]:
    """RMS in dBFS su `frames` finestre uguali (prima della spazializzazione): anima le onde in ascolto."""
    parts = np.array_split(x.mean(axis=1), frames)
    return [round(float(20 * np.log10(np.sqrt(np.mean(p ** 2)) + 1e-10)), 1) if len(p) else -100.0 for p in parts]


def span(project: dict) -> tuple[float, float]:
    """Inizio e fine della timeline coperta dalle tracce attive."""
    ts = active(project["tracks"]) or project["tracks"]
    return (min(t["offset_s"] for t in ts),
            max(t["offset_s"] + t["info"]["duration"] for t in ts))


def print_mix(project: dict, path: str, target_lufs: float | None = -14.0,
              ceiling_dbtp: float = -1.0, block_s: float = 30.0, rng: tuple[float, float] | None = None,
              progress=lambda f: None) -> dict:
    """Stampa il mix su WAV 48 kHz 24 bit, su tutta la timeline o sulla regione `rng`
    (secondi). Prima passata: misura; seconda: normalizza."""
    start, end = rng or span(project)
    sr = project.get("sr", 48000)
    tmp = path + ".tmp.wav"
    loud, peak = Loudness(sr, 2), 0.0
    with sf.SoundFile(tmp, "w", sr, 2, "FLOAT") as f:
        t = start
        while t < end:
            blk, _ = render(project, t, min(block_s, end - t))
            loud.feed(blk); f.write(blk)
            peak = max(peak, float(np.abs(blk).max(initial=0)))
            t += block_s
            progress(0.8 * (t - start) / (end - start))
    lufs = loud.integrated()
    gain_db = 0.0 if target_lufs is None or not np.isfinite(lufs) else target_lufs - lufs
    peak_db = 20 * np.log10(peak + 1e-10) + 0.5  # +0.5 dB: margine per il true peak fra campioni
    gain_db = min(gain_db, ceiling_dbtp - peak_db)
    g = 10 ** (gain_db / 20)
    with sf.SoundFile(tmp) as src, sf.SoundFile(path, "w", sr, 2, "PCM_24") as dst:
        for blk in src.blocks(blocksize=sr * 30, dtype="float32"):
            dst.write(blk * g)
    os.remove(tmp)
    progress(1.0)
    return {"path": path, "inizio_s": start, "durata_s": end - start, "lufs_prima": round(lufs, 1),
            "lufs": round(lufs + gain_db, 1), "guadagno_db": round(gain_db, 1),
            "picco_dbfs": round(peak_db - 0.5 + gain_db, 1)}
