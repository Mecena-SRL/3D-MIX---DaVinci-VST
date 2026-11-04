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


def _fusionscript(lib: str, modules: str):
    """Carica fusionscript direttamente dalla libreria di Resolve.

    DaVinciResolveScript.py usa il modulo `imp` (assente nell'app impacchettata e da
    Python 3.12): qui si carica l'estensione con importlib e si usa quello solo come riserva.
    """
    from importlib.machinery import ExtensionFileLoader
    from importlib.util import module_from_spec, spec_from_loader

    for path in (lib, *_EXTRA_LIBS.get(_plat(), ())):
        if path and os.path.isfile(path):
            loader = ExtensionFileLoader("fusionscript", path)
            mod = module_from_spec(spec_from_loader("fusionscript", loader))
            loader.exec_module(mod)
            return mod
    if modules not in sys.path:
        sys.path.append(modules)
    try:
        return importlib.import_module("DaVinciResolveScript")
    except ImportError as e:
        raise RuntimeError(f"libreria di scripting di Resolve non trovata ({lib})") from e


_EXTRA_LIBS = {"darwin": ("/Applications/DaVinci Resolve Studio/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",)}
_plat = lambda: "linux" if sys.platform.startswith("linux") else sys.platform  # noqa: E731

HINT = ("In Resolve usa Workspace > Scripts > MIX3D: manda la timeline a MIX3D e funziona sempre, "
        "anche con Resolve gratuito. Per leggerla da qui serve Resolve Studio con "
        "Preferenze > Sistema > Generale > Scripting esterno: Locale.")


def connect():
    """Ritorna l'oggetto `resolve`, o solleva RuntimeError con il motivo."""
    modules, lib = _DEFAULT_PATHS.get(_plat(), ("", ""))
    os.environ.setdefault("RESOLVE_SCRIPT_API", os.path.dirname(modules))
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", lib)
    modules = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
    try:
        mod = _fusionscript(os.environ["RESOLVE_SCRIPT_LIB"], modules)
        resolve = mod.scriptapp("Resolve")
    except Exception as e:
        raise RuntimeError(f"Resolve non raggiungibile ({e}). {HINT}") from e
    if resolve is None:
        raise RuntimeError(f"Resolve non risponde. {HINT}")
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


def region(resolve) -> tuple[int, int, str] | None:
    """Regione da elaborare, in frame relativi all'inizio della timeline.

    Prima un marker chiamato "MIX3D" con durata (la "adjustment clip"), poi
    In/Out della timeline. None se non c'è nessuno dei due. [V] GetMarkInOut
    esiste da Resolve 19.
    """
    _, tl = current_timeline(resolve)
    for frame, m in sorted((tl.GetMarkers() or {}).items()):
        if m.get("name", "").strip().upper() == "MIX3D" and m.get("duration", 0) > 1:
            return int(frame), int(frame + m["duration"]), "marker MIX3D"
    io = getattr(tl, "GetMarkInOut", lambda: {})() or {}
    io = io.get("audio") or io.get("video") or {}
    if "in" in io and "out" in io:
        start = tl.GetStartFrame()
        return int(io["in"]) - start, int(io["out"]) - start, "In/Out"
    return None


def mix3d_track(resolve) -> int | None:
    """Indice della traccia audio chiamata MIX3D, se esiste."""
    _, tl = current_timeline(resolve)
    for i in range(1, tl.GetTrackCount("audio") + 1):
        if tl.GetTrackName("audio", i) == "MIX3D":
            return i
    return None


def clear_range(resolve, track: int, start: int, end: int) -> int:
    """Toglie dalla traccia MIX3D le stampe precedenti che si sovrappongono alla
    regione (solo clip il cui nome inizia con MIX3D). Ritorna quante. [V] DeleteClips."""
    _, tl = current_timeline(resolve)
    old = [it for it in tl.GetItemListInTrack("audio", track) or []
           if it.GetName().upper().startswith("MIX3D") and it.GetStart() < end and it.GetEnd() > start]
    if old:
        tl.DeleteClips(old, False)
    return len(old)
