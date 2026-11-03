"""Ponte con DaVinci Resolve Studio via API di scripting Python (F0).

Richiede Resolve Studio aperto e lo scripting esterno abilitato
(Preferenze > Sistema > Generale > "External scripting using": Local).
Le chiamate marcate [V] vanno verificate sulla tua versione di Resolve.
Regola: non modifica mai media o tracce esistenti; aggiunge solo una traccia.
"""
from __future__ import annotations

import importlib
import os
import sys
from dataclasses import asdict, dataclass

_DEFAULT_PATHS = {
    "darwin": ("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules",
               "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"),
    "win32": (os.path.expandvars(r"%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"),
              r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"),
    "linux": ("/opt/resolve/Developer/Scripting/Modules", "/opt/resolve/libs/Fusion/fusionscript.so"),
}


def connect():
    """Ritorna l'oggetto `resolve`, o solleva RuntimeError con il motivo."""
    plat = "linux" if sys.platform.startswith("linux") else sys.platform
    modules, lib = _DEFAULT_PATHS.get(plat, ("", ""))
    os.environ.setdefault("RESOLVE_SCRIPT_API", os.path.dirname(modules))
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", lib)
    modules = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
    if modules not in sys.path:
        sys.path.append(modules)
    try:
        dvr = importlib.import_module("DaVinciResolveScript")
    except ImportError as e:
        raise RuntimeError(f"modulo DaVinciResolveScript non trovato in {modules}") from e
    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        raise RuntimeError("Resolve non risponde: è aperto? È Studio? Scripting esterno su 'Local'?")
    return resolve


@dataclass
class AudioClip:
    track: int
    name: str
    start_frame: int        # posizione sulla timeline
    end_frame: int
    left_offset: int        # frame tagliati all'inizio del file sorgente
    file_path: str          # [V] deve essere l'originale, non un proxy
    sample_rate: str
    channels: str


def current_timeline(resolve):
    project = resolve.GetProjectManager().GetCurrentProject()
    if project is None:
        raise RuntimeError("nessun progetto aperto")
    tl = project.GetCurrentTimeline()
    if tl is None:
        raise RuntimeError("nessuna timeline attiva")
    return project, tl


def read_audio_clips(resolve) -> dict:
    """Passi 1-2 del piano: tracce audio, posizioni e file originali."""
    project, tl = current_timeline(resolve)
    clips = []
    for track in range(1, tl.GetTrackCount("audio") + 1):
        for item in tl.GetItemListInTrack("audio", track) or []:
            mpi = item.GetMediaPoolItem()
            prop = (lambda k: mpi.GetClipProperty(k)) if mpi else (lambda k: "")
            clips.append(AudioClip(
                track=track, name=item.GetName(), start_frame=item.GetStart(),
                end_frame=item.GetEnd(), left_offset=item.GetLeftOffset(),
                file_path=prop("File Path"), sample_rate=prop("Sample Rate"),
                channels=prop("Audio Ch"),
            ))
    return {
        "project": project.GetName(),
        "timeline": tl.GetName(),
        "fps": tl.GetSetting("timelineFrameRate"),
        "start_frame": tl.GetStartFrame(),
        "clips": [asdict(c) for c in clips],
    }


def export_otio(resolve, path: str) -> bool:
    """Passo 3: backup/struttura in OTIO (API >= 18.5)."""
    _, tl = current_timeline(resolve)
    return bool(tl.Export(path, resolve.EXPORT_OTIO, resolve.EXPORT_NONE))


def reimport_wav(resolve, wav_path: str, record_frame: int, track_type: str = "stereo",
                 track_index: int | None = None) -> int:
    """Passo 6: importa un WAV su una NUOVA traccia audio, o su `track_index` se dato
    (la traccia scelta da te: il clip si aggiunge, gli altri clip restano).

    Ritorna l'indice della traccia usata. [V] `recordFrame`, `trackIndex` e
    `mediaType` in AppendToTimeline vanno verificati sulla tua versione.
    """
    project, tl = current_timeline(resolve)
    pm = resolve.GetProjectManager()
    pm.SaveProject()
    media_pool = project.GetMediaPool()
    items = media_pool.ImportMedia([os.path.abspath(wav_path)])
    if not items:
        raise RuntimeError(f"import fallito: {wav_path}")
    track = track_index
    if track is None:
        if not tl.AddTrack("audio", track_type):
            raise RuntimeError("impossibile creare la traccia audio")
        track = tl.GetTrackCount("audio")
        tl.SetTrackName("audio", track, "MIX3D")
    placed = media_pool.AppendToTimeline([{
        "mediaPoolItem": items[0], "trackIndex": track,
        "recordFrame": int(record_frame), "mediaType": 2,
    }])
    if not placed:
        raise RuntimeError("AppendToTimeline non ha posizionato il clip")
    return track
