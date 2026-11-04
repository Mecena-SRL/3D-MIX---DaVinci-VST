#include "MIX3D.h"
#include "IPlug_include_in_plug_src.h"

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>
#ifndef _WIN32
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#endif

static const char* kPanelURL = "http://127.0.0.1:8730/";
using Clock = std::chrono::steady_clock;
using namespace std::chrono_literals;

// GET sul server locale di MIX3D: corpo della risposta se 200, altrimenti false
static bool HttpGet(const std::string& path, std::string& body)
{
#ifdef _WIN32
  return false;
#else
  const int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd < 0) return false;
  timeval tv{3, 0};
  setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof tv);
  setsockopt(fd, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof tv);
#ifdef SO_NOSIGPIPE
  int one = 1;
  setsockopt(fd, SOL_SOCKET, SO_NOSIGPIPE, &one, sizeof one);
#endif
  sockaddr_in a{};
  a.sin_family = AF_INET;
  a.sin_port = htons(8730);
  a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  std::string r;
  if (connect(fd, (sockaddr*) &a, sizeof a) == 0)
  {
    const std::string req = "GET " + path + " HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n";
    if (send(fd, req.data(), req.size(), 0) == (ssize_t) req.size())
    {
      char buf[1 << 16];
      for (ssize_t k; (k = recv(fd, buf, sizeof buf, 0)) > 0;) r.append(buf, k);
    }
  }
  close(fd);
  const size_t e = r.find("\r\n\r\n");
  if (e == std::string::npos || r.compare(9, 3, "200") != 0) return false;
  body = r.substr(e + 4);
  return true;
#endif
}

// numero dopo "chiave": in un JSON piatto (-1 se manca)
static long long Num(const std::string& json, const char* key)
{
  const size_t i = json.find(key);
  return i == std::string::npos ? -1 : std::atoll(json.c_str() + json.find(':', i) + 1);
}

// WAV PCM 16 bit (risposta di /api/render) -> n campioni per canale, ricampionati in lineare
static bool ParseWav(const std::string& w, int n, std::vector<float>& L, std::vector<float>& R)
{
  int ch = 0;
  for (size_t i = 12; i + 8 <= w.size();)
  {
    uint32_t sz;
    std::memcpy(&sz, w.data() + i + 4, 4);
    if (!w.compare(i, 4, "fmt ")) ch = (uint8_t) w[i + 10];
    if (!w.compare(i, 4, "data") && ch > 0)
    {
      const int16_t* d = (const int16_t*) (w.data() + i + 8);
      const int m = (int) (std::min<size_t>(sz, w.size() - i - 8) / (2 * ch));
      if (m < 2) return false;
      L.resize(n);
      R.resize(n);
      for (int k = 0; k < n; k++)
      {
        const double x = (double) k * (m - 1) / std::max(1, n - 1);
        const int j = std::min((int) x, m - 2);
        const double f = x - j;
        auto at = [&](int s, int c) { return d[s * ch + std::min(c, ch - 1)] / 32768.0; };
        L[k] = (float) (at(j, 0) * (1 - f) + at(j + 1, 0) * f);
        R[k] = (float) (at(j, 1) * (1 - f) + at(j + 1, 1) * f);
      }
      return true;
    }
    i += 8 + sz + (sz & 1);
  }
  return false;
}

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
  GetParam(kListen)->InitBool("Ascolto MIX3D", true);
  mRing[0].assign(kRing, 0.f);
  mRing[1].assign(kRing, 0.f);
  mFeed = std::thread([this] { Feed(); });
}

MIX3D::~MIX3D()
{
  mRun = false;
  mFeed.join();
}

// Prepara il mix in anticipo rispetto al playhead. Fermo: dal punto esatto, così il play parte
// subito. In play, dopo un salto: un po' più avanti, quanto serve al server per stare al passo.
void MIX3D::Feed()
{
  long long mix = -2, prev = -1;
  double lag = 0.3; // secondi per un blocco dal server (misurati)
  auto checked = Clock::now() - 1s;
  std::string b;
  std::vector<float> L, R;
  while (mRun)
  {
    if (Clock::now() - checked > 300ms) // c'è qualcosa da ascoltare? il mix è cambiato?
    {
      checked = Clock::now();
      const bool ok = HttpGet("/api/rev?p=1", b);
      const long long m = ok ? Num(b, "\"mix\"") : -1;
      mReady = ok && Num(b, "\"tracce\"") > 0;
      if (m != mix) mEnd = mBase.load(); // audio vecchio: si butta
      mix = m;
    }
    const double sr = mSR;
    const long long pos = mPos;
    const bool play = mPlay;
    if (!mReady || sr <= 0 || pos < 0)
    {
      std::this_thread::sleep_for(50ms);
      continue;
    }
    long long base = mBase, end = mEnd;
    const bool back = pos < prev;
    prev = pos;
    if (back || pos > end) // salto indietro, salto avanti o il server è rimasto indietro
    {
      base = end = pos + (play ? (long long) (lag * 1.5 * sr) : 0);
      mEnd = mBase.load();
      mBase = base;
      mEnd = end;
    }
    if (end - pos >= (play ? std::max(1.0, lag * 3) : 2.0) * sr)
    {
      std::this_thread::sleep_for(10ms);
      continue;
    }
    const int n = (int) (0.5 * sr);
    char path[160];
    std::snprintf(path, sizeof path, "/api/render?t0=%.6f&dur=%.6f&pos=%.6f&play=%d", end / sr, n / sr, pos / sr, play ? 1 : 0);
    const auto t = Clock::now();
    if (!HttpGet(path, b) || !ParseWav(b, n, L, R))
    {
      mReady = false;
      std::this_thread::sleep_for(500ms);
      continue;
    }
    lag = 0.7 * lag + 0.3 * std::chrono::duration<double>(Clock::now() - t).count();
    if (mBase != base) continue; // il playhead è saltato intanto
    for (int k = 0; k < n; k++)
    {
      mRing[0][(end + k) & (kRing - 1)] = L[k];
      mRing[1][(end + k) & (kRing - 1)] = R[k];
    }
    mEnd = end + n;
  }
}

#if IPLUG_DSP
void MIX3D::ProcessBlock(sample** inputs, sample** outputs, int nFrames)
{
  const int nChans = NOutChansConnected();
  const bool play = GetTransportIsRunning();
  const long long pos = (long long) GetSamplePos();
  mSR = GetSampleRate();
  mPos = pos;
  mPlay = play;
  if (!play || pos < 0 || !mReady || !GetParam(kListen)->Bool())
  {
    for (int c = 0; c < nChans; c++)
      for (int s = 0; s < nFrames; s++)
        outputs[c][s] = inputs[c][s];
    return;
  }
  // in play: il mix di MIX3D al posto dell'ingresso; silenzio finché il blocco non è pronto
  const long long base = mBase, end = mEnd;
  for (int s = 0; s < nFrames; s++)
  {
    const long long p = pos + s;
    const bool ok = p >= base && p < end;
    for (int c = 0; c < nChans; c++)
      outputs[c][s] = ok ? mRing[std::min(c, 1)][p & (kRing - 1)] : 0.;
  }
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
