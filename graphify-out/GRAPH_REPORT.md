# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 54 files · ~84,220 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2891 nodes · 5212 edges · 153 communities (72 shown, 81 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 208 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4709084d`
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
- .constructor
- Ui
- cs
- Ii
- vs
- updater.py
- Jp
- cr
- Oi
- Kr
- Nr
- As
- xd
- eu
- $p
- Np
- steps
- Oa
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
- vl
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
- splat.py
- pm
- t
- ld
- em
- analysis.py
- bl
- nm
- ua
- eq.js
- .constructor
- ta
- jn
- Hn
- ml
- numpy
- look.py
- Sc
- ap
- qs
- qd
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
- .constructor
- mp
- om
- Dh
- vc
- $h
- jd
- im
- .setHSL
- ai
- zp
- gh
- es
- wh
- yi
- numpy
- MIX3D
- xs
- EMsgTags
- EParams
- Hu
- .parseObject
- Ci
- dp
- Ph
- Gu
- iu
- Rh
- Yu
- Zc
- Qp
- Xu
- build_macos.sh
- build_plugin.sh
- Fh
- Ih
- Lh
- Oh
- Uh
- zl
- qu

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

## Communities (153 total, 81 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.05
Nodes (12): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_posizione_del_plugin_in_fairlight() (+4 more)

### Community 1 - "media.py"
Cohesion: 0.11
Nodes (15): audio_streams(), banner(), blocks(), ffmpeg(), _ffmpeg_read(), _graph(), native(), NoAudio (+7 more)

### Community 2 - "cli.py"
Cohesion: 0.09
Nodes (20): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+12 more)

### Community 3 - "metadata.py"
Cohesion: 0.11
Nodes (13): _bcd_tc(), detect(), qt_strings(), read(), sony_xml(), tags(), _txt(), wav() (+5 more)

### Community 4 - "sync.py"
Cohesion: 0.14
Nodes (12): same_clock_distances(), align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay() (+4 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.08
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.05
Nodes (98): api(), audible(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color() (+90 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.12
Nodes (7): Clock, HttpGet(), MIX3D::MIX3D(), MIX3D::ProcessBlock(), Num(), ParseWav(), Run()

### Community 8 - "devices.py"
Cohesion: 0.16
Nodes (11): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+3 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 10 - "server.py"
Cohesion: 0.06
Nodes (28): auto_positions(), apply_profile(), auto_place(), browse(), estimate_space(), fuse_scene(), Handler, host_time() (+20 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.08
Nodes (3): constructor(), setValue(), Yp

### Community 16 - ".constructor"
Cohesion: 0.08
Nodes (9): jl, Ft(), Jt(), kt(), Qt(), Yt(), zt(), Li (+1 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.13
Nodes (3): Ku, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.18
Nodes (7): app_bundle(), arch(), check(), download(), _fetch_json(), install(), parse()

### Community 25 - "Kr"
Cohesion: 0.07
Nodes (3): fi(), gi(), Kr

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 27 - "As"
Cohesion: 0.08
Nodes (6): As, ma, nu, pu, ru, td

### Community 28 - "xd"
Cohesion: 0.17
Nodes (4): md(), sd, xd, yd

### Community 30 - "$p"
Cohesion: 0.07
Nodes (6): bd, ed(), Md, $p, pd(), rd

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 33 - "Oa"
Cohesion: 0.13
Nodes (7): Ai, Ha(), Oa, qa(), Ri, Va(), za()

### Community 35 - "e"
Cohesion: 0.09
Nodes (10): _d(), e, hd, Id(), a(), Vd, c(), wd (+2 more)

### Community 36 - "fp"
Cohesion: 0.22
Nodes (3): fp, Nc, Nd

### Community 37 - "vu"
Cohesion: 0.17
Nodes (23): Au(), bu(), Cu(), Du(), Eu(), fu(), gu(), Iu() (+15 more)

### Community 40 - "co"
Cohesion: 0.17
Nodes (22): Ao(), bo(), co(), Do(), fo(), go(), ho(), jo() (+14 more)

### Community 41 - "bi"
Cohesion: 0.13
Nodes (7): bi, ci(), ia, nc, ph, rh, uh

### Community 42 - "$n"
Cohesion: 0.14
Nodes (3): $n(), rs(), _s

### Community 43 - "lr"
Cohesion: 0.07
Nodes (5): am(), lr, rm, sm(), yr

### Community 45 - "Nh"
Cohesion: 0.06
Nodes (10): dh, _h, jh, kh, Nh, qh, Wh(), Xh() (+2 more)

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.09
Nodes (15): ba(), Ga(), ii(), ja(), bt(), Rt(), ka(), kl() (+7 more)

### Community 49 - "xr"
Cohesion: 0.07
Nodes (9): Gl, il, Ka, A(), ol(), A(), C(), R() (+1 more)

### Community 50 - "mixer.py"
Cohesion: 0.13
Nodes (9): locate(), spatial_params(), active(), correction_fir(), envelope_db(), is_line(), print_mix(), render() (+1 more)

### Community 52 - "fuse"
Cohesion: 0.17
Nodes (9): fuse(), dist(), residuals(), unpack(), _wrap(), _imgs(), _start(), test_same_clock_recovers_scene() (+1 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, id, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.13
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.12
Nodes (4): dd, Fl, Mh, rc

### Community 61 - "MIX3D"
Cohesion: 0.14
Nodes (11): MIX3D, kRing, mBase, mEnd, mFeed, mPlay, mPos, mReady (+3 more)

### Community 63 - "xh"
Cohesion: 0.09
Nodes (8): Am, bm, Bm, fm, hh, wm, xh, ym()

### Community 65 - "splat.py"
Cohesion: 0.20
Nodes (7): directivity(), field_at(), fit(), render(), residuals(), unpack(), stage_axis()

### Community 67 - "t"
Cohesion: 0.27
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 70 - "analysis.py"
Cohesion: 0.12
Nodes (8): analyze(), _coarse(), db(), k_weighting(), Loudness, rt60_from_decays(), sync_pair(), warnings()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - ".constructor"
Cohesion: 0.16
Nodes (4): lu, ou, a(), o()

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.21
Nodes (13): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+5 more)

### Community 81 - "look.py"
Cohesion: 0.11
Nodes (20): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut() (+12 more)

### Community 84 - "ap"
Cohesion: 0.23
Nodes (3): ap, Rp(), sp

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.25
Nodes (5): s(), r(), i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 95 - "README.md"
Cohesion: 0.17
Nodes (8): Come i dati diventano utili, Da completare, Database dispositivi, Riconoscimento dai metadati, F0: verifiche su Resolve reale [V], Preset inclusi, Spazi 3D, Spazi privati (file)

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 97 - "mu"
Cohesion: 0.15
Nodes (7): Compatibilità, Cose emerse dalla ricerca, Il kit di Ivan, da(), r(), mu, n

### Community 107 - "jd"
Cohesion: 0.12
Nodes (3): hp, jd, lp

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 110 - "ai"
Cohesion: 0.50
Nodes (3): ai(), oi(), vi

### Community 112 - "gh"
Cohesion: 0.10
Nodes (6): au, es, gh, Gm, su, zm

### Community 117 - "numpy"
Cohesion: 0.07
Nodes (30): band_db(), clock_key(), cluster_sources(), distance_from_ir(), excerpt(), frame_gcc(), images(), impulse_response() (+22 more)

### Community 119 - "MIX3D"
Cohesion: 0.20
Nodes (10): App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti, Stato: F0 (fondamenta) (+2 more)

### Community 121 - "EMsgTags"
Cohesion: 0.67
Nodes (3): EMsgTags, kMsgLaunch, kMsgOpenBrowser

### Community 123 - "EParams"
Cohesion: 0.67
Nodes (3): EParams, kListen, kNumParams

### Community 125 - ".parseObject"
Cohesion: 0.14
Nodes (3): $l, op, tc

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 153 - "zl"
Cohesion: 0.06
Nodes (31): v(), Ea(), Fa(), hl(), j(), K(), q(), W() (+23 more)

## Knowledge Gaps
- **15 isolated node(s):** `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser`, `kListen`, `kNumParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1219 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **81 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `da()` connect `mu` to `.constructor`, `three.module.min.js`, `xr`?**
  _High betweenness centrality (0.348) - this node is a cross-community bridge._
- **What connects `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05391120507399577 - nodes in this community are weakly interconnected._
- **Why does `Compatibilità` connect `mu` to `devices.py`, `README.md`?**
  _High betweenness centrality (0.347) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `mu`?**
  _High betweenness centrality (0.314) - this node is a cross-community bridge._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09390243902439024 - nodes in this community are weakly interconnected._