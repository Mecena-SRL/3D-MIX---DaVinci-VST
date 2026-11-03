"""Riga di comando MIX3D (F0)."""
from __future__ import annotations

import argparse
import json
import sys


def _load_mono(path: str):
    import numpy as np
    import soundfile as sf

    data, fs = sf.read(path, dtype="float32", always_2d=True)
    return data.mean(axis=1).astype(np.float64), fs


def cmd_info(args):
    from .resolve_bridge import connect, export_otio, read_audio_clips

    resolve = connect()
    info = read_audio_clips(resolve)
    print(json.dumps(info, indent=2, ensure_ascii=False))
    if args.otio:
        print("OTIO:", "ok" if export_otio(resolve, args.otio) else "fallito", file=sys.stderr)


def cmd_sync(args):
    from .sync import estimate_drift

    x, fs = _load_mono(args.reference)
    for path in args.others:
        y, fs_y = _load_mono(path)
        if fs_y != fs:
            sys.exit(f"{path}: sample rate {fs_y} != {fs} (ricampionamento in M1, non ancora)")
        m = estimate_drift(x, y, fs, win_s=args.window, hop_s=args.window,
                           coarse_delay=args.coarse, search_s=args.search)
        print(json.dumps({"file": path, "offset_s": m.offset, "drift_ppm": m.ppm,
                          "rms_residual_us": m.rms_residual * 1e6,
                          "windows_used": int(m.inliers.sum()),
                          "windows_total": len(m.inliers)}))


def cmd_reimport(args):
    from .resolve_bridge import connect, reimport_wav

    track = reimport_wav(connect(), args.wav, args.frame)
    print(f"traccia audio {track} 'MIX3D' creata")


def main(argv=None):
    p = argparse.ArgumentParser(prog="mix3d")
    sub = p.add_subparsers(required=True)

    s = sub.add_parser("info", help="legge la timeline audio attiva di Resolve")
    s.add_argument("--otio", help="esporta anche la timeline in OTIO")
    s.set_defaults(fn=cmd_info)

    s = sub.add_parser("sync", help="stima offset e drift rispetto a un riferimento")
    s.add_argument("reference")
    s.add_argument("others", nargs="+")
    s.add_argument("--coarse", type=float, default=0.0, help="sync grossolano in secondi")
    s.add_argument("--search", type=float, default=0.05, help="ricerca ± secondi per finestra")
    s.add_argument("--window", type=float, default=10.0, help="durata finestra in secondi")
    s.set_defaults(fn=cmd_sync)

    s = sub.add_parser("reimport", help="importa un WAV su una nuova traccia 'MIX3D'")
    s.add_argument("wav")
    s.add_argument("--frame", type=int, required=True, help="frame di timeline di inizio")
    s.set_defaults(fn=cmd_reimport)

    args = p.parse_args(argv)
    try:
        args.fn(args)
    except RuntimeError as e:
        sys.exit(f"errore: {e}")


if __name__ == "__main__":
    main()
