#!/bin/bash
# Compila il plugin MIX3D (VST3 + AU, universale arm64/x86_64) con iPlug2. Uso (su macOS): plugin/build_plugin.sh
# Risultato: dist/plugin/MIX3D.vst3 e dist/plugin/MIX3D.component, firmati ad hoc.
set -euo pipefail
cd "$(dirname "$0")/.."
IPLUG2_REF=d82b2e99b17c8f723d3f6e2a88ffd8b656f28e5d   # iPlug2 fissato: build riproducibile
DEPS=build/iPlug2
if [ ! -d "$DEPS/.git" ]; then
  git init -q "$DEPS" && git -C "$DEPS" remote add origin https://github.com/iPlug2/iPlug2.git
fi
git -C "$DEPS" fetch -q --depth 1 origin "$IPLUG2_REF" && git -C "$DEPS" checkout -q FETCH_HEAD
(cd "$DEPS/Dependencies/IPlug" && [ -d VST3_SDK/pluginterfaces ] || ./download-vst3-sdk.sh)
cmake -G Xcode -S plugin/MIX3D -B build/plugin -DIPLUG2_DIR="$PWD/$DEPS" \
  -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" -DCMAKE_OSX_DEPLOYMENT_TARGET=11.0 \
  -DIPLUG_DEPLOY_PLUGINS=OFF -DIPLUG2_DISABLE_DEPRECATION_WARNINGS=ON
cmake --build build/plugin --config Release
rm -rf dist/plugin && mkdir -p dist/plugin
for b in MIX3D.vst3 MIX3D.component; do
  src=$(find build/plugin -path "*Release*" -name "$b" -maxdepth 6 | head -1)
  [ -n "$src" ] || src=$(find build/plugin -name "$b" -type d | head -1)
  cp -R "$src" dist/plugin/
  codesign --force --deep -s - "dist/plugin/$b"
done
ls -la dist/plugin
