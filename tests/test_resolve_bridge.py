"""Test del ponte con un finto oggetto Resolve (niente Resolve reale in CI)."""
from mix3d.resolve_bridge import read_audio_clips, reimport_wav


class _MPI:
    def GetClipProperty(self, k):
        return {"File Path": "/media/fx6/C0001.MP4", "Sample Rate": "48000", "Audio Ch": "4"}[k]


class _Item:
    def GetMediaPoolItem(self): return _MPI()
    def GetName(self): return "C0001.MP4"
    def GetStart(self): return 86400
    def GetEnd(self): return 90000
    def GetLeftOffset(self): return 12


class _TL:
    def __init__(self): self.tracks, self.names = 1, {}
    def GetTrackCount(self, t): return self.tracks
    def GetItemListInTrack(self, t, i): return [_Item()]
    def GetName(self): return "Concerto"
    def GetSetting(self, k): return "25"
    def GetStartFrame(self): return 86400
    def AddTrack(self, t, kind): self.tracks += 1; return True
    def SetTrackName(self, t, i, n): self.names[i] = n; return True


class _Pool:
    def __init__(self): self.appended = None
    def ImportMedia(self, paths): return ["mpi"]
    def AppendToTimeline(self, infos): self.appended = infos; return ["ti"]


class _Project:
    def __init__(self): self.tl, self.pool = _TL(), _Pool()
    def GetCurrentTimeline(self): return self.tl
    def GetName(self): return "Canto di Virginio"
    def GetMediaPool(self): return self.pool


class _PM:
    def __init__(self): self.p, self.saved = _Project(), False
    def GetCurrentProject(self): return self.p
    def SaveProject(self): self.saved = True; return True


class _Resolve:
    def __init__(self): self.pm = _PM()
    def GetProjectManager(self): return self.pm


def test_read_audio_clips():
    info = read_audio_clips(_Resolve())
    assert info["timeline"] == "Concerto"
    c = info["clips"][0]
    assert c["file_path"].endswith("C0001.MP4") and c["start_frame"] == 86400 and c["left_offset"] == 12


def test_reimport_adds_new_track_only():
    r = _Resolve()
    track = reimport_wav(r, "mix.wav", 86400)
    assert track == 2 and r.pm.saved
    assert r.pm.p.tl.names[2] == "MIX3D"
    assert r.pm.p.pool.appended[0]["trackIndex"] == 2 and r.pm.p.pool.appended[0]["mediaType"] == 2


def test_timeline_from_resolve_script_replaces_previous(tmp_path):
    """La timeline mandata dallo script Lua in Resolve sostituisce quella letta prima."""
    import numpy as np
    import soundfile as sf

    from mix3d import server

    wav = tmp_path / "zoom.wav"
    sf.write(wav, np.zeros(48000), 48000)
    info = {"timeline": "Concerto", "fps": "25", "start_frame": 86400,
            "clips": [{"track": 1, "name": "zoom", "start_frame": 86425, "left_offset": 0, "file_path": str(wav)}]}
    server.STATE["project"] = server.new_project()
    for _ in range(2):
        assert server.import_resolve(info) == 1
    tracks = server.STATE["project"]["tracks"]
    assert len(tracks) == 1 and tracks[0]["da_resolve"]
    assert server.STATE["project"]["resolve"]["fps"] == 25.0


def test_connect_explains_how_to_fix(monkeypatch):
    import pytest

    from mix3d import resolve_bridge as rb

    monkeypatch.setenv("RESOLVE_SCRIPT_LIB", "/manca/fusionscript.so")
    monkeypatch.setenv("RESOLVE_SCRIPT_API", "/manca")
    with pytest.raises(RuntimeError, match="Workspace > Scripts > MIX3D"):
        rb.connect()


def test_clip_raggruppate_per_canale_di_resolve(tmp_path):
    """A sinistra si vedono A1, A2…: ogni traccia sa da quale canale di Resolve viene.
    Una clip video senza audio non è un errore; un file con due stream audio a sr diversi si legge."""
    import subprocess

    import numpy as np
    import soundfile as sf

    from mix3d import media, server

    a, b = tmp_path / "a.wav", tmp_path / "b.wav"
    for f in (a, b):
        sf.write(f, np.zeros((48000, 1), np.float32), 48000)
    cam, muto = tmp_path / "DJI_0001.MP4", tmp_path / "muto.MP4"
    ff = media.ffmpeg()
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "sine=f=440:sample_rate=48000", "-f", "lavfi",
                    "-i", "sine=f=880:sample_rate=44100", "-t", "1", "-map", "0", "-map", "1", "-c:a", "aac", str(cam)], check=True)
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "color=s=64x64", "-t", "1", str(muto)], check=True)
    clip = lambda tr, name, f, start, kind="audio": {"track": tr, "name": name, "start_frame": start, "left_offset": 0,
                                                       "file_path": str(f), "kind": kind}
    info = {"timeline": "T", "fps": 25, "start_frame": 0,
            "clips": [clip(1, "a", a, 0), clip(1, "b", b, 50), clip(2, "cam", cam, 0), clip(1, "muto", muto, 0, "video")]}
    server.STATE["project"] = server.new_project()
    server.import_resolve(info)
    p = server.STATE["project"]
    assert [t["canale"] for t in p["tracks"]] == ["A1", "A1", "A2"]
    assert p["tracks"][2]["info"]["channels"] == 2 and p["resolve"]["non_lette"] == []


def test_posizione_del_plugin_in_fairlight():
    """L'host può contare dal timecode (01:00:00:00) o da zero: entrambi finiscono sui secondi MIX3D."""
    from mix3d import server
    server.STATE["project"]["resolve"] = {"start_frame": 86400, "fps": 24.0, "timeline": "t"}
    server.STATE["host_rel"] = False
    assert server.host_time(3610.0) == 10.0  # timecode assoluto
    assert server.host_time(5.0) == 5.0      # prima del timecode: l'host conta da zero...
    assert server.host_time(3610.0) == 3610.0  # ...e così resta
    server.STATE["project"].pop("resolve")
    server.STATE["host_rel"] = False
