"""Metadati: BWF (bext/iXML/INFO), XML Sony accanto al clip, riconoscimento del registratore."""
import struct

import numpy as np
import soundfile as sf

from mix3d import devices, media, metadata

FS = 48000


def chunk(cid: bytes, data: bytes) -> bytes:
    return cid + struct.pack("<I", len(data)) + data + (b"\0" if len(data) & 1 else b"")


def bwf(path, originator: str, tc_s: float):
    """WAV vero + chunk bext, iXML e LIST/INFO aggiunti in coda."""
    sf.write(path, (np.random.randn(FS, 2) * 0.01).astype("float32"), FS, "FLOAT")
    raw = bytearray(open(path, "rb").read())
    bext = (b"Concerto".ljust(256, b"\0") + originator.encode().ljust(32, b"\0") + b"REF".ljust(32, b"\0")
            + b"2026-11-03" + b"21:00:00" + struct.pack("<Q", int(tc_s * FS)) + b"\0" * 256)
    ixml = b"<BWFXML><PROJECT>Canto</PROJECT><SCENE>1</SCENE><TRACK_LIST><TRACK><NAME>MKH416</NAME></TRACK></TRACK_LIST></BWFXML>"
    info = b"INFO" + chunk(b"ISFT", b"TASCAM Portacapture X8\0")
    raw += chunk(b"bext", bext) + chunk(b"iXML", ixml) + chunk(b"LIST", info)
    raw[4:8] = struct.pack("<I", len(raw) - 8)
    open(path, "wb").write(bytes(raw))


def test_bwf_tascam(tmp_path):
    p = tmp_path / "260001_0001.wav"
    bwf(p, "TASCAM X8", 3600 + 0.5)
    m = metadata.wav(str(p), FS)
    assert m["originator"] == "TASCAM X8" and m["project"] == "Canto" and m["tracce"] == ["MKH416"]
    assert abs(m["timecode_s"] - 3600.5) < 1e-6 and "Portacapture X8" in m["info_isft"]
    info = media.probe(str(p))
    assert info["rilevato"]["id"] == "tascam_x8"
    s = devices.suggest({**info, "ch_index": 1})
    assert s[0]["id"].startswith("x8_") and any(w.startswith("metadati") for w in s[0]["motivi"])


def test_xml_sony(tmp_path):
    clip = tmp_path / "A001C003_261103AB.MP4"
    clip.write_bytes(b"")
    (tmp_path / "A001C003_261103ABM01.XML").write_text(
        '<?xml version="1.0"?><NonRealTimeMeta xmlns="urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.00">'
        '<LtcChangeTable tcFps="25"><LtcChange frameCount="0" value="12345620" status="increment"/></LtcChangeTable>'
        '<Device manufacturer="Sony" modelName="ILME-FX6V" serialNo="1"/>'
        '<AudioFormat numOfChannel="4"><AudioRecPort port="CH1" audioCodec="LPCM24" trackDst="CH1"/></AudioFormat>'
        '</NonRealTimeMeta>')
    m = metadata.sony_xml(str(clip))
    assert m["modello"] == "ILME-FX6V" and m["canali_audio"] == "4"
    assert abs(m["timecode_s"] - (20 * 3600 + 56 * 60 + 34 + 12 / 25)) < 1e-6  # ffssmmhh
    assert metadata.detect(m)["id"] == "fx6"


def test_firme_distinte():
    # FX3 non deve prendere i file FX30 e viceversa
    assert metadata.detect({"modello": "ILME-FX30"})["id"] == "fx30"
    assert metadata.detect({"modello": "ILME-FX3"})["id"] == "fx3"
    assert metadata.detect({"encoder": "Lavf"}) is None
