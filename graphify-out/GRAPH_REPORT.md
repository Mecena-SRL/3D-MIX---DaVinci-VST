# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 56 files · ~86,836 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2930 nodes · 5293 edges · 174 communities (76 shown, 98 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 208 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `05fd536a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- media.py
- cli.py
- metadata.py
- sync.py
- test_ui_engine.py
- app.js
- MIX3D.cpp
- devices.py
- three.module.min.js
- server.py
- mix3d
- ti
- .constructor
- Yp
- ei
- jl
- Ui
- cs
- Ii
- .constructor
- updater.py
- Jp
- cr
- Oi
- Kr
- Nr
- As
- localize.py
- eu
- bd
- Np
- steps
- Ai
- ch
- e
- fp
- vu
- hm
- ic
- co
- bi
- $n
- lr
- la
- Nh
- tr
- .constructor
- bt
- xr
- mixer.py
- jr
- fuse
- ts
- main.js
- cp
- ec
- kd
- jc
- Kn
- .setValues
- MIX3D
- .copy
- xh
- Fc
- createField
- pm
- t
- ld
- Sc
- renderTracks
- bl
- nm
- ua
- eq.js
- ou
- renderMonitor
- eq.py
- Hn
- ml
- renderDevice
- look.py
- $p
- ap
- qs
- .updateMatrix
- od
- rp
- up
- nl
- .parse
- s
- tu
- README.md
- package.json
- mu
- lm
- Zh
- zl
- scene
- om
- Dh
- wi
- $h
- .parseObject
- im
- .setHSL
- xa
- zp
- gh
- es
- wh
- na
- numpy
- MIX3D
- xs
- EMsgTags
- EParams
- Hu
- $l
- Ci
- dp
- Ph
- hh
- test_splat.py
- Rh
- ya
- Yu
- Zc
- Qp
- il
- Xu
- build_macos.sh
- build_plugin.sh
- .isEmpty
- su
- Fh
- Ih
- Lh
- A
- Oh
- Uh
- Oa
- td
- pu
- qu
- vs
- iu

## God Nodes (most connected - your core abstractions)
1. `Ui` - 109 edges
2. `ti` - 91 edges
3. `ei` - 73 edges
4. `Nr` - 67 edges
5. `Kr` - 65 edges
6. `As` - 60 edges
7. `cs` - 54 edges
8. `cr` - 49 edges
9. `Oi` - 40 edges
10. `Ii` - 39 edges

## Surprising Connections (you probably didn't know these)
- `F0: verifiche su Resolve reale [V]` --references--> `MIX3D`  [INFERRED]
  docs/F0_verifiche.md → plugin/MIX3D/MIX3D.h
- `Riconoscimento dai metadati` --references--> `detect()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/metadata.py
- `MIX3D` --references--> `MIX3D`  [INFERRED]
  README.md → plugin/MIX3D/MIX3D.h
- `Compatibilità` --references--> `compat()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/devices.py
- `Stato: F0 (fondamenta)` --references--> `sync()`  [INFERRED]
  README.md → src/mix3d/server.py

## Import Cycles
- None detected.

## Communities (174 total, 98 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.05
Nodes (13): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_posizione_del_plugin_in_fairlight() (+5 more)

### Community 1 - "media.py"
Cohesion: 0.11
Nodes (15): audio_streams(), banner(), blocks(), ffmpeg(), _ffmpeg_read(), _graph(), native(), NoAudio (+7 more)

### Community 2 - "cli.py"
Cohesion: 0.11
Nodes (20): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+12 more)

### Community 3 - "metadata.py"
Cohesion: 0.11
Nodes (13): _bcd_tc(), detect(), qt_strings(), read(), sony_xml(), tags(), _txt(), wav() (+5 more)

### Community 4 - "sync.py"
Cohesion: 0.07
Nodes (19): analyze(), _coarse(), db(), k_weighting(), Loudness, rt60_from_decays(), sync_pair(), warnings() (+11 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.08
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.13
Nodes (26): api(), browse(), CAMERAS, checkUpdate(), COLORS, FX, grouped(), installIt() (+18 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.12
Nodes (7): Clock, HttpGet(), MIX3D::MIX3D(), MIX3D::ProcessBlock(), Num(), ParseWav(), Run()

### Community 8 - "devices.py"
Cohesion: 0.11
Nodes (13): chain_risks(), compat(), compat_matrix(), load(), _powered(), profile(), suggest(), is_line() (+5 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 10 - "server.py"
Cohesion: 0.06
Nodes (25): auto_positions(), apply_profile(), auto_place(), eq_curve(), estimate_space(), Handler, host_time(), job_analyze() (+17 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.08
Nodes (3): constructor(), setValue(), Yp

### Community 16 - "jl"
Cohesion: 0.06
Nodes (18): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, da() (+10 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - ".constructor"
Cohesion: 0.18
Nodes (3): Gu, a(), o()

### Community 21 - "updater.py"
Cohesion: 0.18
Nodes (7): app_bundle(), arch(), check(), download(), _fetch_json(), install(), parse()

### Community 26 - "Nr"
Cohesion: 0.08
Nodes (4): gm, np, Nr, uc

### Community 28 - "localize.py"
Cohesion: 0.14
Nodes (11): band_db(), clock_key(), cluster_sources(), distance_from_ir(), excerpt(), frame_gcc(), images(), impulse_response() (+3 more)

### Community 30 - "bd"
Cohesion: 0.06
Nodes (9): ad, bd, md(), Md, pd(), rd, sd, xd (+1 more)

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 35 - "e"
Cohesion: 0.10
Nodes (8): e, hd, a(), Vd, c(), wd, xp, zd

### Community 36 - "fp"
Cohesion: 0.16
Nodes (5): fp, Mi(), Nc, Nd, yi

### Community 37 - "vu"
Cohesion: 0.17
Nodes (23): Au(), bu(), Cu(), Du(), Eu(), fu(), gu(), Iu() (+15 more)

### Community 40 - "co"
Cohesion: 0.17
Nodes (22): Ao(), bo(), co(), Do(), fo(), go(), ho(), jo() (+14 more)

### Community 41 - "bi"
Cohesion: 0.11
Nodes (10): ai(), bi, ci(), fi(), nc, oi(), ph, rh (+2 more)

### Community 42 - "$n"
Cohesion: 0.14
Nodes (3): $n(), rs(), _s

### Community 43 - "lr"
Cohesion: 0.06
Nodes (6): am(), lr, rm, sm(), Tl(), yr

### Community 45 - "Nh"
Cohesion: 0.06
Nodes (10): dh, _h, jh, kh, Nh, qh, Wh(), Xh() (+2 more)

### Community 47 - ".constructor"
Cohesion: 0.08
Nodes (32): hl(), j(), K(), q(), W(), Ft(), Jt(), kt() (+24 more)

### Community 48 - "bt"
Cohesion: 0.10
Nodes (14): ba(), Ga(), ii(), ja(), bt(), Rt(), ka(), kl() (+6 more)

### Community 50 - "mixer.py"
Cohesion: 0.07
Nodes (18): asciuga(), compress(), impulse(), Reverb, reverb(), ruolo(), settings(), locate() (+10 more)

### Community 52 - "fuse"
Cohesion: 0.09
Nodes (17): fuse(), dist(), residuals(), unpack(), _wrap(), directivity(), field_at(), fit() (+9 more)

### Community 53 - "ts"
Cohesion: 0.15
Nodes (3): fl, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.17
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.12
Nodes (4): dd, id, Mh, rc

### Community 61 - "MIX3D"
Cohesion: 0.14
Nodes (11): MIX3D, kRing, mBase, mEnd, mFeed, mPlay, mPos, mReady (+3 more)

### Community 62 - ".copy"
Cohesion: 0.12
Nodes (4): cd, ud, vc, xc()

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - "createField"
Cohesion: 0.13
Nodes (15): createField(), drAt(), drawMap(), weights(), drColor(), drLabel(), forward(), frontGeometry() (+7 more)

### Community 67 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 68 - "ld"
Cohesion: 0.15
Nodes (5): _d(), fd(), gd(), Id(), ld

### Community 70 - "renderTracks"
Cohesion: 0.18
Nodes (17): fmt(), go(), health(), pct(), pushTrack(), quality(), refresh(), renderHealth() (+9 more)

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - "ou"
Cohesion: 0.22
Nodes (3): ju, lu, ou

### Community 76 - "renderMonitor"
Cohesion: 0.20
Nodes (15): audible(), color(), lane(), laneName(), lanes(), members(), push(), pushFx() (+7 more)

### Community 77 - "eq.py"
Cohesion: 0.27
Nodes (7): _ap1(), _ap2(), component(), dyn_gain_db(), process(), response_db(), _sos_cut()

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "renderDevice"
Cohesion: 0.24
Nodes (15): barChart(), chainRisks(), css(), drawMiniWave(), drawPolar(), fit(), fmtTc(), kHz() (+7 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.17
Nodes (6): s(), r(), mp, i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 95 - "README.md"
Cohesion: 0.25
Nodes (4): F0: verifiche su Resolve reale [V], Preset inclusi, Spazi 3D, Spazi privati (file)

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 100 - "zl"
Cohesion: 0.18
Nodes (6): Fl, Ma(), zl(), b(), E(), T()

### Community 101 - "scene"
Cohesion: 0.26
Nodes (12): isLine(), mic(), micDir(), polarGainDb(), polarMatrix(), polarR(), renderField(), renderIO() (+4 more)

### Community 105 - "wi"
Cohesion: 0.13
Nodes (8): Ea(), Fa(), ia, li, pi, ra, ri, wi

### Community 107 - ".parseObject"
Cohesion: 0.07
Nodes (6): hp, jd, lp, op, qd, tc

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 110 - "xa"
Cohesion: 0.28
Nodes (7): v(), xa(), g(), d(), u(), Ys(), Zs()

### Community 112 - "gh"
Cohesion: 0.11
Nodes (5): es, gh, Gm, Tm, zm

### Community 117 - "numpy"
Cohesion: 0.07
Nodes (38): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+30 more)

### Community 119 - "MIX3D"
Cohesion: 0.20
Nodes (10): App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti, Stato: F0 (fondamenta) (+2 more)

### Community 121 - "EMsgTags"
Cohesion: 0.67
Nodes (3): EMsgTags, kMsgLaunch, kMsgOpenBrowser

### Community 123 - "EParams"
Cohesion: 0.67
Nodes (3): EParams, kListen, kNumParams

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 130 - "hh"
Cohesion: 0.17
Nodes (4): Am, Bm, hh, ym()

### Community 131 - "test_splat.py"
Cohesion: 0.29
Nodes (3): _obs(), test_fit_recovers_splats(), test_listener_mix_reproduces_direct_and_reverb()

### Community 133 - "ya"
Cohesion: 0.32
Nodes (5): ya(), f(), g(), x(), y()

### Community 150 - "A"
Cohesion: 0.40
Nodes (3): A(), ol(), S()

### Community 153 - "Oa"
Cohesion: 0.09
Nodes (7): Ha(), Oa, qa(), ta, Va(), wp, za()

### Community 163 - "vs"
Cohesion: 0.10
Nodes (6): Ku, ma, nu, ru, $u, vs

## Knowledge Gaps
- **15 isolated node(s):** `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser`, `kListen`, `kNumParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1237 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **98 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Compatibilità` connect `jl` to `devices.py`?**
  _High betweenness centrality (0.306) - this node is a cross-community bridge._
- **What connects `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.051207729468599035 - nodes in this community are weakly interconnected._
- **Why does `da()` connect `jl` to `three.module.min.js`, `.constructor`?**
  _High betweenness centrality (0.305) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `jl`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._