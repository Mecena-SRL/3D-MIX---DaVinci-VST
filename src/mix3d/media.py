"""Lettura dei file: formato e decodifica con ffmpeg (cache), lettura a blocchi."""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

CACHE = Path.home() / ".mix3d" / "cache"


def ffmpeg() -> str:
    """ffmpeg di sistema, altrimenti quello incluso (imageio-ffmpeg, anche nell'app)."""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe(path: str) -> dict:
    """Formato del primo stream audio: nome, codec, sr, canali, bit, durata.

    Legge sempre il WAV decodificato (sr, canali, durata esatti); codec e bit
    vengono dall'originale, dal banner di ffmpeg.
    """
    m = re.search(r"Audio: (\w+)", banner(path))
    codec = m.group(1) if m else "sconosciuto"
    i = sf.info(decoded(path))
    bits = 32 if "f32" in codec else int(b.group(1)) if (b := re.match(r"pcm_[su](\d+)", codec)) else None
    return {"name": Path(path).name, "codec": codec, "sr": i.samplerate, "channels": i.channels,
            "bits": bits, "duration": i.duration}


def banner(path: str) -> str:
    """Descrizione degli stream secondo ffmpeg (stderr di `ffmpeg -i`)."""
    return subprocess.run([ffmpeg(), "-hide_banner", "-i", path], capture_output=True, text=True).stderr


def decoded(path: str) -> str:
    """WAV leggibile da soundfile: l'originale se possibile, altrimenti copia in cache.

    Video di camera (MP4, MOV, MXF): si estrae solo l'audio. Se i canali sono in
    stream separati (tipico dell'MXF: un mono per canale) si uniscono in ordine
    in un unico WAV multicanale, così ch1..chN corrispondono a quelli della camera.
    """
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
        n = len(re.findall(r"Stream #\S+.*: Audio:", banner(path)))
        merge = ["-filter_complex", "".join(f"[0:a:{i}]" for i in range(n)) + f"amerge=inputs={n}"] if n > 1 else []
        subprocess.run([ffmpeg(), "-v", "error", "-y", "-i", path, "-vn", *merge, "-c:a", "pcm_f32le",
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
