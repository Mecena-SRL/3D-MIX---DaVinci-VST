#pragma once
// MIX3D in Fairlight: plugin "porta d'ingresso". Lascia passare l'audio invariato e,
// all'apertura della finestra, avvia l'app MIX3D (se chiusa) e ne mostra il pannello.

#include "IPlug_include_in_plug_hdr.h"

using namespace iplug;

enum EParams { kNumParams = 0 };
enum EMsgTags { kMsgLaunch = 0, kMsgOpenBrowser = 1 };

class MIX3D final : public Plugin
{
public:
  MIX3D(const InstanceInfo& info);

#if IPLUG_DSP
  void ProcessBlock(sample** inputs, sample** outputs, int nFrames) override;
#endif
  bool OnMessage(int msgTag, int ctrlTag, int dataSize, const void* pData) override;
#ifdef WEBVIEW_EDITOR_DELEGATE
  bool CanNavigateToURL(const char* url);
#endif
};
