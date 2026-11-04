"""Metadati dei file: chi li ha registrati e quando.

- WAV/BWF: chunk `bext` (Originator, Description, TimeReference = timecode),
  `iXML` (progetto, scena, tracce), `LIST/INFO` (ISFT = software/registratore).
- MP4 Sony: XML accanto al clip (C0001M01.XML, A001C001_...M01.XML) con
  modello, timecode LTC e canali audio.
- Tutti: tag letti da ffmpeg (encoder, handler, make/model).

`detect()` confronta il testo raccolto con le firme `metadati` dei registratori.
"""
from __future__ import annotations

import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

from . import devices


def _wav_chunks(path: str, limit: int = 1 << 20) -> dict[str, bytes]:
    """Chunk di testo di un RIFF/RF64/BW64 (salta i dati audio)."""
    out = {}
    with open(path, "rb") as f:
        if f.read(4) not in (b"RIFF", b"RF64", b"BW64"):
            return out
        f.read(4)
        if f.read(4) != b"WAVE":
            return out
        while (h := f.read(8)) and len(h) == 8:
            cid, size = h[:4].decode("latin-1"), struct.unpack("<I", h[4:])[0]
            if cid in ("bext", "iXML", "LIST", "axml") and size <= limit:
                out[cid] = f.read(size)
            else:
                f.seek(size, 1)
            f.seek(size & 1, 1)
    return out


def _txt(b: bytes) -> str:
    return b.split(b"\0", 1)[0].decode("utf-8", "replace").strip()


def wav(path: str, sr: int | None = None) -> dict:
    c, m = _wav_chunks(path), {}
    if b := c.get("bext"):
        m.update(descrizione=_txt(b[:256]), originator=_txt(b[256:288]), riferimento=_txt(b[288:320]),
                 data=_txt(b[320:330]), ora=_txt(b[330:338]))
        ref = struct.unpack("<Q", b[338:346])[0] if len(b) >= 346 else 0
        if sr and ref:
            m["timecode_s"] = ref / sr
    if x := c.get("iXML"):
        try:
            root = ET.fromstring(_txt(x))
            for tag in ("PROJECT", "SCENE", "TAKE", "TAPE", "NOTE"):
                if (v := root.findtext(f".//{tag}")):
                    m[tag.lower()] = v
            m["tracce"] = [t.findtext("NAME") or "" for t in root.iter("TRACK")]
            if (s := root.findtext(".//TIMESTAMP_SAMPLES_SINCE_MIDNIGHT")) and sr and "timecode_s" not in m:
                m["timecode_s"] = int(s) / sr
        except ET.ParseError:
            pass
    if (li := c.get("LIST")) and li[:4] == b"INFO":
        i, b = 4, li
        while i + 8 <= len(b):
            k, n = b[i:i + 4].decode("latin-1"), struct.unpack("<I", b[i + 4:i + 8])[0]
            m[f"info_{k.lower()}"] = _txt(b[i + 8:i + 8 + n])
            i += 8 + n + (n & 1)
    return m


def _bcd_tc(v: str, fps: float) -> float | None:
    """LTC Sony 'ffssmmhh' -> secondi."""
    if not re.fullmatch(r"\d{8}", v or ""):
        return None
    ff, ss, mm, hh = (int(v[i:i + 2]) for i in range(0, 8, 2))
    return hh * 3600 + mm * 60 + ss + ff / fps


def sony_xml(path: str) -> dict:
    """XML NRT accanto al clip Sony (stesso nome + M01.XML)."""
    p = Path(path)
    xml = next((x for x in p.parent.glob(p.stem + "M0*.XML")), None) or \
        next((x for x in p.parent.glob(p.stem + "M0*.xml")), None)
    if xml is None:
        return {}
    try:
        root = ET.parse(xml).getroot()
    except ET.ParseError:
        return {}
    el = {e.tag.split("}")[-1]: e for e in root.iter()}
    m = {"xml": xml.name}
    if (d := el.get("Device")) is not None:
        m.update(costruttore=d.get("manufacturer", ""), modello=d.get("modelName", ""))
    if (a := el.get("AudioFormat")) is not None:
        m["canali_audio"] = a.get("numOfChannel")
        m["porte_audio"] = [{k: v for k, v in e.attrib.items()} for e in a]
    if (lt := el.get("LtcChangeTable")) is not None:
        fps = float(lt.get("tcFps", 25))
        first = next(iter(lt), None)
        if first is not None and (tc := _bcd_tc(first.get("value"), fps)) is not None:
            m["timecode_s"] = tc
    return m


def tags(banner: str) -> dict:
    """Tag di container/stream dal banner di ffmpeg (encoder, handler_name, model...)."""
    keep = ("encoder", "handler_name", "make", "model", "com.apple.quicktime.model", "comment",
            "originator", "timecode", "software")
    out = {}
    for k, v in re.findall(r"^\s+([\w.\-]+)\s*:\s*(.+)$", banner, re.M):
        if k.lower() in keep and k.lower() not in out:
            out[k.lower()] = v.strip()
    return out


def read(path: str, banner: str = "", sr: int | None = None) -> dict:
    m = tags(banner)
    if path.lower().endswith((".wav", ".bwf")):
        m.update(wav(path, sr))
    else:
        m.update(sony_xml(path))
    return m


def detect(meta: dict) -> dict | None:
    """Registratore riconosciuto dai metadati: {id, nome, indizio} o None."""
    text = " ".join(str(v) for v in meta.values() if isinstance(v, str))
    for rid, r in devices.load()["registratori"].items():
        for rx in r.get("metadati", []):
            if (hit := re.search(rx, text, re.I)):
                return {"id": rid, "nome": r["nome"], "indizio": hit.group(0)}
    return None
