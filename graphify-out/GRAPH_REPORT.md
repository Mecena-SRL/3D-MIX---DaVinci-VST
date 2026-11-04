# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 52 files · ~81,996 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2862 nodes · 5151 edges · 151 communities (70 shown, 81 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 207 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `79a06b70`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- media.py
- numpy
- metadata.py
- cli.py
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
- bd
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
- .isEmpty
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
- xr
- .copy
- xh
- Fc
- Nc
- pm
- ta
- ld
- lm
- analysis.py
- bl
- nm
- ua
- eq.js
- .constructor
- json
- qd
- Hn
- ml
- numpy
- look.py
- Sc
- test_eq.py
- qs
- od
- rp
- ap
- nl
- .parse
- s
- tu
- em
- package.json
- up
- localize.py
- Zh
- .constructor
- om
- Dh
- eq.py
- $h
- jd
- im
- .setHSL
- iu
- zp
- gh
- es
- wh
- estimate_drift
- t
- MIX3D
- xs
- hh
- Hu
- .parseObject
- Ci
- dp
- Ph
- Gu
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

## Communities (151 total, 81 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.05
Nodes (12): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_posizione_del_plugin_in_fairlight() (+4 more)

### Community 1 - "media.py"
Cohesion: 0.11
Nodes (14): audio_streams(), banner(), blocks(), ffmpeg(), _ffmpeg_read(), _graph(), native(), NoAudio (+6 more)

### Community 2 - "numpy"
Cohesion: 0.19
Nodes (11): locate(), _project(), test_dual_mono_goes_left_right_and_line_ignores_distance(), test_split_and_join(), _delay(), _scene(), test_cluster_sources_separates_delay_patterns(), test_distance_from_drr() (+3 more)

### Community 3 - "metadata.py"
Cohesion: 0.10
Nodes (14): probe(), _bcd_tc(), detect(), qt_strings(), read(), sony_xml(), tags(), _txt() (+6 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (19): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+11 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.09
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.05
Nodes (93): api(), audible(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color() (+85 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.06
Nodes (24): Clock, EMsgTags, kMsgLaunch, kMsgOpenBrowser, EParams, kListen, kNumParams, HttpGet() (+16 more)

### Community 8 - "devices.py"
Cohesion: 0.16
Nodes (11): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+3 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 10 - "server.py"
Cohesion: 0.07
Nodes (17): auto_positions(), same_clock_distances(), apply_profile(), auto_place(), estimate_space(), fuse_scene(), Handler, import_resolve() (+9 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.08
Nodes (3): constructor(), setValue(), Yp

### Community 16 - ".constructor"
Cohesion: 0.10
Nodes (9): W(), jl, Ft(), Jt(), kt(), Qt(), Yt(), zt() (+1 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.13
Nodes (3): Ku, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.18
Nodes (7): app_bundle(), arch(), check(), download(), _fetch_json(), install(), parse()

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 27 - "As"
Cohesion: 0.08
Nodes (6): As, ma, nu, pu, ru, td

### Community 28 - "bd"
Cohesion: 0.06
Nodes (10): ad, bd, ed(), md(), Md, pd(), rd, sd (+2 more)

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 33 - "Oa"
Cohesion: 0.13
Nodes (8): Ai, Fa(), Ha(), Oa, qa(), Ri, Va(), za()

### Community 35 - "e"
Cohesion: 0.14
Nodes (6): e, a(), Vd, c(), xp, zd

### Community 37 - "vu"
Cohesion: 0.17
Nodes (23): Au(), bu(), Cu(), Du(), Eu(), fu(), gu(), Iu() (+15 more)

### Community 40 - "co"
Cohesion: 0.17
Nodes (22): Ao(), bo(), co(), Do(), fo(), go(), ho(), jo() (+14 more)

### Community 41 - "bi"
Cohesion: 0.10
Nodes (11): ai(), bi, ci(), fi(), ia, nc, oi(), ph (+3 more)

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

### Community 50 - "mixer.py"
Cohesion: 0.13
Nodes (10): spatial_params(), active(), envelope_db(), is_line(), print_mix(), render(), span(), browse() (+2 more)

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
Cohesion: 0.11
Nodes (5): cd, dd, Mh, rc, ud

### Community 61 - "xr"
Cohesion: 0.07
Nodes (9): Gl, il, Ka, A(), ol(), A(), C(), R() (+1 more)

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - "Nc"
Cohesion: 0.13
Nodes (6): s(), Mi(), Nc, Nd, wd, yi

### Community 68 - "ld"
Cohesion: 0.11
Nodes (6): _d(), fd(), gd(), hd, Id(), ld

### Community 70 - "analysis.py"
Cohesion: 0.14
Nodes (7): analyze(), db(), k_weighting(), Loudness, rt60_from_decays(), warnings(), one()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - ".constructor"
Cohesion: 0.16
Nodes (4): lu, ou, a(), o()

### Community 76 - "json"
Cohesion: 0.23
Nodes (7): all_spaces(), builtin(), critical_distance(), get(), import_file(), local(), normalize()

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.15
Nodes (14): cl(), dl(), gl(), hl(), j(), K(), q(), ll() (+6 more)

### Community 80 - "numpy"
Cohesion: 0.20
Nodes (15): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+7 more)

### Community 81 - "look.py"
Cohesion: 0.20
Nodes (12): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+4 more)

### Community 84 - "test_eq.py"
Cohesion: 0.29
Nodes (7): _bp(), test_auto_taratura(), test_banda_dinamica_agisce_solo_sopra_soglia(), test_curva_uguale_al_filtro(), test_look_master(), test_master_continuo_e_auto(), _track()

### Community 89 - "ap"
Cohesion: 0.23
Nodes (3): ap, Rp(), sp

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.18
Nodes (5): r(), mp, i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 94 - "tu"
Cohesion: 0.06
Nodes (16): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, F0: verifiche su Resolve reale [V] (+8 more)

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 98 - "localize.py"
Cohesion: 0.15
Nodes (10): clock_key(), cluster_sources(), distance_from_ir(), excerpt(), frame_gcc(), images(), impulse_response(), read_aligned() (+2 more)

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 107 - "jd"
Cohesion: 0.12
Nodes (3): hp, jd, lp

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 112 - "gh"
Cohesion: 0.10
Nodes (5): au, gh, Gm, Li, su

### Community 113 - "es"
Cohesion: 0.22
Nodes (3): es, Mm, Zu

### Community 117 - "estimate_drift"
Cohesion: 0.15
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 118 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 119 - "MIX3D"
Cohesion: 0.14
Nodes (12): App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti, Stato: F0 (fondamenta) (+4 more)

### Community 121 - "hh"
Cohesion: 0.13
Nodes (5): Am, Bm, hh, ym(), zm

### Community 125 - ".parseObject"
Cohesion: 0.14
Nodes (3): $l, op, tc

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 153 - "zl"
Cohesion: 0.06
Nodes (26): v(), Ea(), Fl, li, Ma(), pi, p(), ra (+18 more)

## Knowledge Gaps
- **15 isolated node(s):** `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser`, `kListen`, `kNumParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1210 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **81 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `da()` connect `tu` to `.constructor`, `three.module.min.js`, `xr`?**
  _High betweenness centrality (0.301) - this node is a cross-community bridge._
- **What connects `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05391120507399577 - nodes in this community are weakly interconnected._
- **Why does `Compatibilità` connect `tu` to `devices.py`?**
  _High betweenness centrality (0.300) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10588235294117647 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `tu`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._
- **Should `metadata.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09841269841269841 - nodes in this community are weakly interconnected._