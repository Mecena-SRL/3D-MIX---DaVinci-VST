#include "MIX3D.h"
#include "IPlug_include_in_plug_src.h"

#include <cstdlib>
#include <string>
#include <thread>

static const char* kPanelURL = "http://127.0.0.1:8730/";

// Avvia l'app senza bloccare l'host: `open` torna subito, l'app parte senza aprire il browser.
static void Run(const std::string& cmd)
{
  std::thread([cmd] { std::system(cmd.c_str()); }).detach();
}

MIX3D::MIX3D(const InstanceInfo& info)
: iplug::Plugin(info, MakeConfig(kNumParams, 0))
{
#ifdef WEBVIEW_EDITOR_DELEGATE
  mEditorInitFunc = [&]()
  {
    LoadIndexHtml(__FILE__, GetBundleID()); // pagina di avvio: aspetta il server e poi carica il pannello
    EnableScroll(true);
  };
#endif
}

#if IPLUG_DSP
void MIX3D::ProcessBlock(sample** inputs, sample** outputs, int nFrames)
{
  const int nChans = NOutChansConnected();
  for (int c = 0; c < nChans; c++)
    for (int s = 0; s < nFrames; s++)
      outputs[c][s] = inputs[c][s];
}
#endif

bool MIX3D::OnMessage(int msgTag, int ctrlTag, int dataSize, const void* pData)
{
  if (msgTag == kMsgLaunch)
  {
    Run("open -g -b it.mecena.mix3d --args --no-browser || open -g -a MIX3D --args --no-browser");
    return true;
  }
  if (msgTag == kMsgOpenBrowser)
  {
    Run(std::string("open ") + kPanelURL);
    return true;
  }
  return false;
}

#ifdef WEBVIEW_EDITOR_DELEGATE
bool MIX3D::CanNavigateToURL(const char* url)
{
  // solo la pagina inclusa e il pannello locale: niente siti esterni dentro Resolve
  const std::string u(url);
  return u.rfind("file:", 0) == 0 || u.rfind(kPanelURL, 0) == 0 || u.rfind("about:", 0) == 0;
}
#endif
