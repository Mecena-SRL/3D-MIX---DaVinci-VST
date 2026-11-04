#pragma once
// MIX3D in Fairlight. All'apertura della finestra avvia l'app MIX3D (se chiusa) e ne mostra il pannello.
// In play suona il mix di MIX3D alla posizione della timeline (al posto dell'ingresso): va messo
// sul bus master, con le tracce originali dentro. Fermo, o con MIX3D spento, lascia passare l'audio.

#include "IPlug_include_in_plug_hdr.h"

#include <atomic>
#include <thread>
#include <vector>

using namespace iplug;

enum EParams { kListen = 0, kNumParams };
enum EMsgTags { kMsgLaunch = 0, kMsgOpenBrowser = 1 };

class MIX3D final : public Plugin
{
public:
  MIX3D(const InstanceInfo& info);
  ~MIX3D();

#if IPLUG_DSP
  void ProcessBlock(sample** inputs, sample** outputs, int nFrames) override;
#endif
  bool OnMessage(int msgTag, int ctrlTag, int dataSize, const void* pData) override;
#ifdef WEBVIEW_EDITOR_DELEGATE
  bool CanNavigateToURL(const char* url);
#endif

private:
  void Feed(); // thread che chiede al server i blocchi in anticipo

  // anello di campioni indicizzato per posizione assoluta dell'host: [mBase, mEnd) è pronto
  static constexpr int kRing = 1 << 20;
  std::vector<float> mRing[2];
  std::atomic<long long> mBase{0}, mEnd{0}, mPos{-1};
  std::atomic<double> mSR{0};
  std::atomic<bool> mPlay{false}, mReady{false}, mRun{true};
  std::thread mFeed;
};
