"""Lettura dei file: formato e decodifica con ffmpeg (cache), lettura a blocchi."""
from __future__ import annotations

import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

from . import metadata



class NoAudio(ValueError):
    """File senza stream audio (es. clip solo video)."""


def ffmpeg() -> str:
    """ffmpeg di sistema, altrimenti quello incluso (imageio-ffmpeg, anche nell'app)."""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


LAYOUT = {"mono": 1, "stereo": 2, "2.1": 3, "quad": 4, "4.0": 4, "5.0": 5, "5.1": 6, "6.1": 7, "7.1": 8}
SR = 48000  # i video si leggono sempre a 48 kHz


@lru_cache(maxsize=512)
def native(path: str) -> bool:
    """True se soundfile legge il file direttamente (WAV, BWF, FLAC, AIFF)."""
    try:
        sf.info(path)
        return True
    except RuntimeError:
        return False


@lru_cache(maxsize=512)
def audio_streams(path: str) -> tuple[int, ...]:
    """Canali di ogni stream audio del file, dal banner di ffmpeg."""
    out = []
    for lay in re.findall(r"Stream #\S+.*: Audio: [^\n]*?, \d+ Hz, ([^,\n]+)", banner(path)):
        n = re.match(r"(\d+) channels", lay.strip())
        out.append(int(n.group(1)) if n else LAYOUT.get(lay.strip().split("(")[0], 2))
    return tuple(out)


def probe(path: str) -> dict:
    """Formato: nome, codec, sr, canali, bit, durata. Non decodifica il file (sessioni da ore)."""
    ban = banner(path)
    m = re.search(r"Audio: (\w+)", ban)
    codec = m.group(1) if m else "sconosciuto"
    if native(path):
        i = sf.info(path)
        sr, ch, dur = i.samplerate, i.channels, i.duration
    else:
        ch = sum(audio_streams(path))
        if not ch:
            raise NoAudio(f"{Path(path).name}: nessun audio nel file")
        d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", ban)
        sr, dur = SR, (int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))) if d else 0.0
    bits = 32 if "f32" in codec else int(b.group(1)) if (b := re.match(r"pcm_[su](\d+)", codec)) else None
    meta = metadata.read(path, ban, sr)
    return {"name": Path(path).name, "codec": codec, "sr": sr, "channels": ch,
            "bits": bits, "duration": dur, "metadati": meta, "rilevato": metadata.detect(meta)}


def banner(path: str) -> str:
    """Descrizione degli stream secondo ffmpeg (stderr di `ffmpeg -i`)."""
    return subprocess.run([ffmpeg(), "-hide_banner", "-i", path], capture_output=True, text=True).stderr


def _graph(path: str, sr: int) -> list[str]:
    """Filtri ffmpeg: tutti gli stream audio a sr, uniti in ordine (MXF: un mono per canale)."""
    n = len(audio_streams(path))
    if not n:
        raise NoAudio(f"{Path(path).name}: nessun audio nel file")
    g = "".join(f"[0:a:{i}]aformat=sample_fmts=flt:sample_rates={sr}[a{i}];" for i in range(n))
    g += "".join(f"[a{i}]" for i in range(n)) + (f"amerge=inputs={n}[out]" if n > 1 else "anull[out]")
    return ["-filter_complex", g, "-map", "[out]", "-f", "f32le", "-"]


def _ffmpeg_read(path: str, t0: float, dur: float, sr: int) -> np.ndarray:
    """Solo il pezzo richiesto, con seek nel contenitore: niente copia decodificata di file da ore."""
    seek = ["-ss", f"{t0:.6f}"] if t0 > 0 else []
    r = subprocess.run([ffmpeg(), "-v", "error", *seek, "-t", f"{dur:.6f}", "-i", path, *_graph(path, sr)],
                       capture_output=True)
    if r.returncode:
        raise RuntimeError(f"{Path(path).name}: ffmpeg non legge l'audio ({r.stderr.decode(errors='replace').strip()[-200:]})")
    return np.frombuffer(r.stdout, np.float32).reshape(-1, sum(audio_streams(path)))


def read(wav: str, channels: list[int], t0: float, dur: float, sr_out: int) -> np.ndarray:
    """Campioni [n, len(channels)] da t0 per dur secondi, a sr_out; zeri fuori file."""
    n_out = int(round(dur * sr_out))
    if not native(wav):
        out = np.zeros((n_out, len(channels)), np.float32)
        a = max(0, int(round(-t0 * sr_out)))  # t0 negativo: silenzio prima dell'inizio del file
        if a < n_out:
            x = _ffmpeg_read(wav, max(t0, 0), (n_out - a) / sr_out, sr_out)[:, [c - 1 for c in channels]]
            out[a:a + len(x)] = x[: n_out - a]
        return out
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
        out = np.pad(out, ((0, max(0, n_out - len(out))), (0, 0)))[:n_out]
    return out


def blocks(wav: str, channels: list[int], block_s: float = 30.0):
    """Itera (t0, sr, blocco mono float64) su tutto il file, senza caricarlo in memoria."""
    pick = [c - 1 for c in channels]
    if not native(wav):  # video: un solo ffmpeg che decodifica in streaming
        n_ch, n = sum(audio_streams(wav)), int(block_s * SR)
        nice = ["nice", "-n", "10"] if shutil.which("nice") else []  # l'analisi lascia la precedenza all'ascolto
        proc = subprocess.Popen([*nice, ffmpeg(), "-v", "error", "-i", wav, *_graph(wav, SR)], stdout=subprocess.PIPE)
        pos = 0
        try:
            while buf := proc.stdout.read(n * n_ch * 4):
                blk = np.frombuffer(buf[: len(buf) // (4 * n_ch) * 4 * n_ch], np.float32).reshape(-1, n_ch)
                yield pos / SR, SR, blk[:, pick].mean(axis=1).astype(np.float64)
                pos += len(blk)
        finally:
            proc.kill(); proc.wait()
        return
    with sf.SoundFile(wav) as f:
        sr, n = f.samplerate, int(block_s * f.samplerate)
        pos = 0
        for blk in f.blocks(blocksize=n, dtype="float32", always_2d=True):
            yield pos / sr, sr, blk[:, pick].mean(axis=1).astype(np.float64)
            pos += len(blk)
