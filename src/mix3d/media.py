"""Lettura dei file: probe con ffprobe, decodifica in cache, lettura a blocchi."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

CACHE = Path.home() / ".mix3d" / "cache"


def probe(path: str) -> dict:
    """Formato del primo stream audio: nome, codec, sr, canali, bit, durata."""
    name = Path(path).name
    if shutil.which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                            "stream=codec_name,sample_rate,channels,bits_per_raw_sample,bits_per_sample"
                            ":format=duration", "-of", "json", path],
                           capture_output=True, text=True, check=True)
        j = json.loads(r.stdout)
        s = j["streams"][0]
        codec = s["codec_name"]
        bits = int(s.get("bits_per_raw_sample") or s.get("bits_per_sample") or 0) or None
        if codec.startswith("pcm_f32"):
            bits = 32
        return {"name": name, "codec": codec, "sr": int(s["sample_rate"]),
                "channels": int(s["channels"]), "bits": bits,
                "duration": float(j["format"]["duration"])}
    i = sf.info(path)
    bits = {"FLOAT": 32, "PCM_24": 24, "PCM_16": 16, "PCM_32": 32}.get(i.subtype)
    codec = "pcm_f32le" if i.subtype == "FLOAT" else f"pcm_s{bits}le"
    return {"name": name, "codec": codec, "sr": i.samplerate, "channels": i.channels,
            "bits": bits, "duration": i.duration}


def decoded(path: str) -> str:
    """WAV leggibile da soundfile: l'originale se possibile, altrimenti copia in cache."""
    try:
        sf.info(path)
        return path
    except RuntimeError:
        pass
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{Path(path).resolve()}:{Path(path).stat().st_mtime}".encode()).hexdigest()[:16]
    out = CACHE / f"{key}.wav"
    if not out.exists():
        tmp = out.with_suffix(".tmp.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vn", "-c:a", "pcm_f32le",
                        str(tmp)], check=True)
        tmp.rename(out)
    return str(out)


def read(wav: str, channels: list[int], t0: float, dur: float, sr_out: int) -> np.ndarray:
    """Campioni [n, len(channels)] da t0 per dur secondi, a sr_out; zeri fuori file."""
    with sf.SoundFile(wav) as f:
        sr = f.samplerate
        a, n = int(round(t0 * sr)), int(round(dur * sr))
        out = np.zeros((n, len(channels)), np.float32)
        s, e = max(a, 0), min(a + n, f.frames)
        if e > s:
            f.seek(s)
            blk = f.read(e - s, dtype="float32", always_2d=True)
            out[s - a:e - a] = blk[:, [c - 1 for c in channels]]
    if sr != sr_out:
        g = np.gcd(sr, sr_out)
        out = resample_poly(out, sr_out // g, sr // g, axis=0).astype(np.float32)
        n_out = int(round(dur * sr_out))
        out = np.pad(out, ((0, max(0, n_out - len(out))), (0, 0)))[:n_out]
    return out


def blocks(wav: str, channels: list[int], block_s: float = 30.0):
    """Itera (t0, sr, blocco mono float64) su tutto il file, senza caricarlo in memoria."""
    with sf.SoundFile(wav) as f:
        sr, n = f.samplerate, int(block_s * f.samplerate)
        pos = 0
        for blk in f.blocks(blocksize=n, dtype="float32", always_2d=True):
            yield pos / sr, sr, blk[:, [c - 1 for c in channels]].mean(axis=1).astype(np.float64)
            pos += len(blk)
