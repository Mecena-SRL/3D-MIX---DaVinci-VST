# Plugin MIX3D (VST3 + AU) per Fairlight: passa l'audio e mostra il pannello MIX3D.
# Build (macOS): cmake -G Xcode -DIPLUG2_DIR=<checkout iPlug2> -S plugin/MIX3D -B build && cmake --build build --config Release
cmake_minimum_required(VERSION 3.14)
project(MIX3D VERSION 0.0.5)

if(NOT DEFINED IPLUG2_DIR)
  message(FATAL_ERROR "Imposta -DIPLUG2_DIR=<percorso di iPlug2>")
endif()

include(${IPLUG2_DIR}/iPlug2.cmake)
find_package(iPlug2 REQUIRED)

iplug_add_plugin(${PROJECT_NAME}
  SOURCES
    MIX3D.cpp
    MIX3D.h
    resources/resource.h
  WEB_RESOURCES
    resources/web/index.html
    resources/web/script.js
  UI WEBVIEW
  FORMATS VST3 AU
)
