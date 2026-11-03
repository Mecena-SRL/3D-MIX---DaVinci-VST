#!/bin/bash
# Crea MIX3D.app e il .dmg. Uso (su macOS): packaging/build_macos.sh
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION=$(python3 -c "import tomllib;print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
ARCH=$(uname -m)
python3 -m pip install -q . pyinstaller
python3 -m PyInstaller --noconfirm --clean --windowed --name MIX3D \
  --osx-bundle-identifier it.mecena.mix3d \
  --collect-data mix3d --collect-all imageio_ffmpeg --collect-all soundfile \
  --hidden-import scipy.signal --hidden-import scipy.interpolate \
  packaging/launcher.py
rm -rf dist/dmg && mkdir -p dist/dmg
cp -R dist/MIX3D.app dist/dmg/
ln -s /Applications dist/dmg/Applications
hdiutil create -volname "MIX3D $VERSION" -srcfolder dist/dmg -ov -format UDZO "dist/MIX3D-$VERSION-macos-$ARCH.dmg"
echo "dist/MIX3D-$VERSION-macos-$ARCH.dmg"
