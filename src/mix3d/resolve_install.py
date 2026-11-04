"""Installa MIX3D dentro DaVinci Resolve (macOS).

- Script: Workspace > Scripts > MIX3D (cartella utente, senza permessi speciali). È in Lua:
  gira anche in Resolve gratuito e senza Python installato, e manda la timeline a MIX3D.
- Pannello: Workspace > Workflow Integrations > MIX3D (cartella di sistema: chiede
  la password di amministratore tramite la finestra standard di macOS).
- Plugin Fairlight: MIX3D.vst3 e MIX3D.component nelle cartelle plug-in dell'utente
  (presenti solo nell'app impacchettata: li compila la CI con iPlug2).
"""
from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).parent / "resolve_plugin"
BASE = "Library/Application Support/Blackmagic Design/DaVinci Resolve"
SCRIPT = Path.home() / BASE / "Fusion/Scripts/Utility/MIX3D.lua"
PANEL = Path("/") / BASE / "Workflow Integration Plugins/MIX3D"
# nell'app: MIX3D.app/Contents/Resources/fairlight (copiati dopo PyInstaller da build_macos.sh)
FAIRLIGHT = Path(sys.executable).resolve().parents[1] / "Resources" / "fairlight"
PLUGINS = {"MIX3D.vst3": Path.home() / "Library/Audio/Plug-Ins/VST3",
           "MIX3D.component": Path.home() / "Library/Audio/Plug-Ins/Components"}


def status() -> dict:
    return {"macos": sys.platform == "darwin", "script": SCRIPT.exists(),
            "pannello": (PANEL / "manifest.xml").exists(),
            "fairlight": all((d / n).exists() for n, d in PLUGINS.items()),
            "fairlight_incluso": FAIRLIGHT.is_dir()}


def install_fairlight() -> bool:
    """Copia i plugin VST3/AU nelle cartelle dell'utente (niente password). False se non inclusi."""
    if not FAIRLIGHT.is_dir():
        return False
    for name, dest in PLUGINS.items():
        dest.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(dest / name, ignore_errors=True)
        shutil.copytree(FAIRLIGHT / name, dest / name, symlinks=True)
        subprocess.run(["xattr", "-dr", "com.apple.quarantine", str(dest / name)], capture_output=True)
    return True


def refresh_script() -> None:
    """Dopo un aggiornamento dell'app: rimette lo script nuovo se quello vecchio è installato."""
    if sys.platform == "darwin" and (SCRIPT.exists() or SCRIPT.with_suffix(".py").exists()):
        shutil.copy(SRC / "MIX3D.lua", SCRIPT)
        SCRIPT.with_suffix(".py").unlink(missing_ok=True)


def install(panel: bool = True) -> dict:
    if sys.platform != "darwin":
        raise RuntimeError("integrazione con Resolve disponibile solo su macOS")
    SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(SRC / "MIX3D.lua", SCRIPT)
    SCRIPT.with_suffix(".py").unlink(missing_ok=True)  # script Python delle versioni ≤ 0.0.5
    install_fairlight()
    if panel:
        src, dst = shlex.quote(str(SRC / "workflow")), shlex.quote(str(PANEL))
        cmd = f"mkdir -p {dst} && cp -R {src}/ {dst}/"
        subprocess.run(["osascript", "-e", f'do shell script "{cmd}" with administrator privileges'],
                       check=True, capture_output=True)
    return status()
