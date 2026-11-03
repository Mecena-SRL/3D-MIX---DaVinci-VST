"""Motore del pannello: database, analisi, sync, mix e stampa su un concerto simulato."""
import json
import shutil
import subprocess
import threading
import urllib.request

import numpy as np
import pytest
import soundfile as sf
from scipy.signal import lfilter

from mix3d import analysis, devices, mixer, server

FS = 48000


def _music(seconds, seed=1):
    rng = np.random.default_rng(seed)
    n = int(seconds * FS)
    x = lfilter([0.049922, -0.095993, 0.050612, -0.004408], [1, -2.494956, 2.017265, -0.522189], rng.standard_normal(n))
    env = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 0.7 * np.arange(n) / FS))
    return 0.3 * x * env / np.abs(x).max()


@pytest.fixture(scope="module")
def concert(tmp_path_factory):
    d = tmp_path_factory.mktemp("concerto")
    src = _music(70)
    noise = lambda n, s: 0.002 * np.random.default_rng(s).standard_normal(n)
    # Tascam: 32 bit float, parte da t=0
    sf.write(d / "tascam_0001.wav", np.stack([src + noise(len(src), 3)] * 2, 1), FS, "FLOAT")
    # DJI Mic: parte 1.25 s dopo (il file inizia più tardi), 24 bit
    late = src[int(1.25 * FS):]
    sf.write(d / "TX01_MIC001.wav", (late + noise(len(late), 4))[:, None], FS, "PCM_24")
    return d


def test_database_coerente():
    db = devices.load()
    for p in db["profili"]:
        assert p["registratore"] in db["registratori"] and p["microfono"] in db["microfoni"], p["id"]
        devices.profile(p["id"])
    f = np.array(analysis.THIRD_OCT)
    for m in db["microfoni"].values():
        c = devices.correction_db(m, f)
        assert np.all(np.abs(c) <= 6.0)


def test_rischi_catena():
    # DJI Mic 2 nella FX6: clock della camera (niente drift wireless) ma limiter del trasmettitore
    r = devices.chain_risks("fx6", "dji_mic2_tx")
    db = devices.load()["rischi"]
    assert db["limiter"] in r and db["agc"] in r and db["wireless_drift"] not in r
    assert db["wireless_drift"] in devices.chain_risks("dji_mic2", "dji_mic2_tx")


def test_vocabolario_e_adattatori():
    db = devices.load()
    conn, alim = db["_info"]["connettori"], db["_info"]["alimentazione"]
    for k, m in db["microfoni"].items():
        assert set(m.get("connettore", [])) <= set(conn) and set(m.get("alimentazione", [])) <= set(alim), k
    for k, r in db["registratori"].items():
        assert all(i["tipo"] in conn for i in r.get("ingressi", [])), k
        assert all(mi in db["microfoni"] for mi in r.get("mic_interno", [])), k
    for a in db["adattatori"]:
        assert a["da"] in conn and a["a"] in conn and all(r in db["registratori"] for r in a.get("solo", []))


def test_compatibilita():
    c = devices.compat
    assert c("fx6", "mkh416")["ok"] and "XLR" in c("fx6", "mkh416")["via"]
    assert c("fx30", "mkh416")["ok"] and "XLR-H1" in c("fx30", "mkh416")["via"]
    assert c("fx6", "ecm_b1m")["ok"] is False                  # slitta FX6 non digitale
    assert c("osmo_action5pro", "mkh416")["ok"] is False       # niente phantom
    assert "diretto" in c("osmo_action5pro", "dji_mic2_tx")["via"]
    assert c("tascam_x8", "fx6_interno")["ok"] is False
    assert c("mixer", "c2")["ok"] is None
    for p in devices.load()["profili"]:
        assert c(p["registratore"], p["microfono"])["ok"] is not False, p["id"]


def test_suggerimento_32bit_tascam():
    s = devices.suggest({"name": "tascam_0001.wav", "codec": "pcm_f32le", "bits": 32, "sr": 48000, "ch_index": 1})
    assert s[0]["id"].startswith("x8_")


def test_loudness_sinusoide():
    # sinusoide 1 kHz con RMS -20 dBFS su un canale: BS.1770 dà -20 LUFS
    t = np.arange(20 * FS) / FS
    x = 10 ** (-20 / 20) * np.sqrt(2) * np.sin(2 * np.pi * 1000 * t)
    L = analysis.Loudness(FS, 1)
    L.feed(x[:, None])
    assert abs(L.integrated() + 20) < 0.1


def test_pannello_end_to_end(concert):
    server.STATE["project"] = server.new_project()
    p = server.STATE["project"]
    p["tracks"] = server.tracks_from_file(str(concert / "tascam_0001.wav")) + \
        server.tracks_from_file(str(concert / "TX01_MIC001.wav"))
    p["tracks"][1]["offset_s"] = 1.2  # sync grossolano a mano, 50 ms di errore
    job = {"progress": 0, "msg": ""}
    server.job_analyze(job)
    tas, dji = p["tracks"]
    assert tas["analisi"]["lufs"] < 0 and len(tas["analisi"]["overview"]["max"]) > 100
    assert abs(dji["offset_s"] - 1.25) < 50e-6, dji["sync"]
    blk, lv = mixer.render(p, 10.0, 1.0)
    assert blk.shape == (FS, 2) and lv["master"] > -40
    out = concert / "mix.wav"
    r = mixer.print_mix(p, str(out), target_lufs=-23)
    assert abs(r["lufs"] - (-23)) < 0.5 and r["picco_dbfs"] <= -1.0
    assert sf.info(str(out)).subtype == "PCM_24"


def test_api_http(concert):
    srv = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    post = lambda path, body: json.loads(urllib.request.urlopen(urllib.request.Request(
        base + path, json.dumps(body).encode(), {"Content-Type": "application/json"})).read())
    post("/api/new", {})
    st = post("/api/files", {"paths": [str(concert / "tascam_0001.wav")]})
    assert len(st["tracks"]) == 1 and st["tracks"][0]["suggeriti"]
    tid = st["tracks"][0]["id"]
    st = post("/api/state", {"tracks": [{"id": tid, "profile": "x8_416", "confermato": True}]})
    assert st["tracks"][0]["profile"] == "x8_416" and st["tracks"][0]["microfono"] == "mkh416"
    st = post("/api/state", {"tracks": [{"id": tid, "registratore": "fx6", "microfono": "dji_mic2_tx"}]})
    assert (st["tracks"][0]["registratore"], st["tracks"][0]["microfono"]) == ("fx6", "dji_mic2_tx")
    r = urllib.request.urlopen(base + "/api/render?t0=5&dur=0.5")
    assert r.headers["Content-Type"] == "audio/wav" and "master" in json.loads(r.headers["X-Levels"])
    assert "curve" in json.loads(urllib.request.urlopen(base + "/api/devices").read())
    assert urllib.request.urlopen(base + "/").status == 200
    srv.shutdown()


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg assente")
def test_file_video_aac(concert):
    mp4 = concert / "DJI_0001.MP4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(concert / "TX01_MIC001.wav"), "-c:a", "aac",
                    "-b:a", "128k", str(mp4)], check=True)
    t = server.tracks_from_file(str(mp4))[0]
    assert t["info"]["codec"] == "aac" and t["wav"].endswith(".wav")
    assert t["profile"] == "osmo_action"


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg assente")
def test_mxf_canali_in_stream_separati(concert):
    # MXF da camera: video + 4 stream audio mono -> una traccia per coppia di canali, ordine preservato
    mxf = concert / "camera.mxf"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=160x120:rate=25", "-f", "lavfi",
                    "-i", "sine=f=440", "-f", "lavfi", "-i", "sine=f=880", "-t", "3", "-filter_complex",
                    "[1:a]asplit[a][c];[2:a]asplit[b][d]", "-map", "0:v", "-map", "[a]", "-map", "[b]", "-map", "[c]",
                    "-map", "[d]", "-c:v", "mpeg2video", "-c:a", "pcm_s24le", "-ar", "48000", str(mxf)], check=True)
    ts = server.tracks_from_file(str(mxf))
    assert [t["channels"] for t in ts] == [[1, 2], [3, 4]] and ts[0]["info"]["bits"] == 24
    from mix3d import media
    x = media.read(ts[0]["wav"], [1, 2], 1.0, 1.0, FS)
    f = np.fft.rfftfreq(FS, 1 / FS)
    assert [f[np.argmax(np.abs(np.fft.rfft(x[:, c])))] for c in (0, 1)] == [440, 880]


def test_stampa_regione(concert):
    server.STATE["project"] = server.new_project()
    p = server.STATE["project"]
    p["tracks"] = server.tracks_from_file(str(concert / "tascam_0001.wav"))
    r = mixer.print_mix(p, str(concert / "reg.wav"), target_lufs=None, rng=(10.0, 15.0))
    assert r["inizio_s"] == 10.0 and abs(sf.info(str(concert / "reg.wav")).duration - 5.0) < 0.01


class _FakeTimeline:
    def __init__(self, markers, inout=None):
        self.markers, self.inout = markers, inout

    def GetMarkers(self):
        return self.markers

    def GetMarkInOut(self):
        return self.inout

    def GetStartFrame(self):
        return 86400


def test_regione_da_marker_o_inout(monkeypatch):
    from mix3d import resolve_bridge as rb
    tl = _FakeTimeline({100: {"name": "altro", "duration": 50}, 500: {"name": "MIX3D", "duration": 250}})
    monkeypatch.setattr(rb, "current_timeline", lambda r: (None, tl))
    assert rb.region(None) == (500, 750, "marker MIX3D")
    tl.markers, tl.inout = {}, {"audio": {"in": 86500, "out": 86600}}
    assert rb.region(None) == (100, 200, "In/Out")
    tl.inout = {}
    assert rb.region(None) is None


def test_spazi_preset_e_import(tmp_path, monkeypatch):
    from mix3d import spazi
    ss = spazi.builtin()
    assert len(ss) >= 10 and len({s["id"] for s in ss}) == len(ss)
    for s in ss:
        assert {"sala", "palco", "ascoltatore", "rt60"} <= s.keys() and spazi.critical_distance(s) > 0, s["id"]
    # file privato nello schema mix3d-spazio/1: copiato solo nella cartella locale
    monkeypatch.setattr(spazi, "LOCAL", tmp_path / "spazi")
    f = tmp_path / "sala.mix3d-space.json"
    f.write_text(json.dumps({"formato": "mix3d-spazio/1", "id": "sala_x", "nome": "Sala X", "capienza": 99,
                             "sala": {"w": 10, "d": 12, "h": 6}, "listener": [0, 1.2, 5],
                             "acustica": {"rt60_s": {"500": 0.8, "1000": 0.7}, "note": "asciutta"}}))
    s = spazi.import_file(str(f))
    assert s["rt60"] == {"500": 0.8, "1k": 0.7} and s["ascoltatore"] == [0, 1.2, 5]
    assert spazi.get("sala_x")["privato"] and (tmp_path / "spazi" / "sala_x.json").exists()


def test_localizzazione_tdoa():
    from mix3d import geometry
    mics = np.array([[-4, 1.5, 3], [4, 1.5, 3], [0, 1.5, 8], [-2, 1.5, -1]], float)
    src = np.array([1.3, 1.5, -2.1])
    d = np.linalg.norm(mics - src, axis=1)
    pos, err = geometry.locate(mics, (d - d[0]) / geometry.C, (-6, 6, -4, 2))
    assert np.allclose(pos, src, atol=0.11) and err < 0.1
