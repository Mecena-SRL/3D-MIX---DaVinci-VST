"""Installa MIX3D dentro DaVinci Resolve (macOS).

- Script: Workspace > Scripts > MIX3D (cartella utente, senza permessi speciali).
- Pannello: Workspace > Workflow Integrations > MIX3D (cartella di sistema: chiede
  la password di amministratore tramite la finestra standard di macOS).
"""
from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).parent / "resolve_plugin"
BASE = "Library/Application Support/Blackmagic Design/DaVinci Resolve"
SCRIPT = Path.home() / BASE / "Fusion/Scripts/Utility/MIX3D.py"
PANEL = Path("/") / BASE / "Workflow Integration Plugins/MIX3D"


def status() -> dict:
    return {"macos": sys.platform == "darwin", "script": SCRIPT.exists(),
            "pannello": (PANEL / "manifest.xml").exists()}


def install(panel: bool = True) -> dict:
    if sys.platform != "darwin":
        raise RuntimeError("integrazione con Resolve disponibile solo su macOS")
    SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(SRC / "MIX3D_script.txt", SCRIPT)
    if panel:
        src, dst = shlex.quote(str(SRC / "workflow")), shlex.quote(str(PANEL))
        cmd = f"mkdir -p {dst} && cp -R {src}/ {dst}/"
        subprocess.run(["osascript", "-e", f'do shell script "{cmd}" with administrator privileges'],
                       check=True, capture_output=True)
    return status()
