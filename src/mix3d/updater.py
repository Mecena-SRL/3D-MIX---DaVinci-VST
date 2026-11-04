"""Aggiornamento dalle GitHub Releases: controllo versione e installazione dell'app macOS.

Il controllo legge l'ultima release pubblica; l'installazione (solo app impacchettata)
scarica il dmg dell'architettura giusta, poi uno script separato aspetta la chiusura
di MIX3D, sostituisce MIX3D.app e la riapre.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from . import __version__

REPO = "Mecena-SRL/3D-MIX---DaVinci-VST"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
DIR = Path.home() / ".mix3d" / "update"
_cache: dict = {}


def parse(v: str) -> tuple[int, ...]:
    """'v0.0.10' -> (0, 0, 10); parti non numeriche ignorate."""
    return tuple(int(p) for p in v.lstrip("v").split(".") if p.isdigit())


def arch() -> str:
    return "arm64" if platform.machine() in ("arm64", "aarch64") else "x86_64"


def app_bundle() -> Path | None:
    """MIX3D.app in esecuzione, solo se è l'app impacchettata (PyInstaller)."""
    if not getattr(sys, "frozen", False):
        return None
    p = Path(sys.executable).resolve()
    return next((a for a in p.parents if a.suffix == ".app"), None)


def check(force: bool = False, fetch=None) -> dict:
    """Stato aggiornamento. Cache di un'ora; senza rete ritorna l'errore, non solleva."""
    if not force and _cache.get("t", 0) > time.time() - 3600:
        return _cache["r"]
    try:
        rel = (fetch or _fetch_json)(API)
        latest = rel["tag_name"]
        asset = next((a for a in rel.get("assets", []) if a["name"].endswith(f"-{arch()}.dmg")), None)
        r = {"corrente": __version__, "ultima": latest.lstrip("v"), "disponibile": parse(latest) > parse(__version__),
             "url": asset and asset["browser_download_url"], "pagina": rel.get("html_url"),
             "note": (rel.get("body") or "")[:2000], "installabile": app_bundle() is not None and bool(asset)}
    except Exception as e:  # offline o limite API: l'app funziona lo stesso
        r = {"corrente": __version__, "disponibile": False, "errore": str(e)}
    _cache.update(t=time.time(), r=r)
    return r


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "MIX3D-updater"})
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.load(r)


def download(url: str, job: dict) -> Path:
    DIR.mkdir(parents=True, exist_ok=True)
    out = DIR / url.rsplit("/", 1)[1]
    req = urllib.request.Request(url, headers={"User-Agent": "MIX3D-updater"})
    with urllib.request.urlopen(req, timeout=30) as r, open(out, "wb") as f:
        total, done = int(r.headers.get("Content-Length") or 0), 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            done += len(chunk)
            job["progress"] = 0.9 * done / total if total else 0.5
            job["msg"] = f"download {done >> 20} MB"
    return out


SCRIPT = """#!/bin/bash
# Sostituisce MIX3D.app con quella del dmg e la riapre (lanciato da MIX3D prima di uscire).
while kill -0 {pid} 2>/dev/null; do sleep 0.5; done
MNT=$(mktemp -d)
hdiutil attach -nobrowse -quiet -mountpoint "$MNT" "{dmg}" || exit 1
rm -rf "{app}.old" && mv "{app}" "{app}.old" && ditto "$MNT/MIX3D.app" "{app}" && rm -rf "{app}.old" || mv "{app}.old" "{app}"
hdiutil detach -quiet "$MNT"
xattr -dr com.apple.quarantine "{app}" 2>/dev/null
open "{app}"
"""


def install(job: dict) -> dict:
    """Scarica e prepara la sostituzione; il server poi esce e lo script riapre l'app."""
    st = check(force=True)
    app = app_bundle()
    if not st.get("disponibile"):
        return {"messaggio": "Hai già l'ultima versione"}
    if not (app and st.get("url")):
        raise RuntimeError(f"Aggiornamento automatico solo dall'app MIX3D: scarica da {st.get('pagina')}")
    dmg = download(st["url"], job)
    script = DIR / "aggiorna.sh"
    script.write_text(SCRIPT.format(pid=os.getpid(), dmg=dmg, app=app))
    script.chmod(0o755)
    subprocess.Popen(["/bin/bash", str(script)], start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    job["msg"] = "riavvio"
    return {"versione": st["ultima"], "riavvio": True}
