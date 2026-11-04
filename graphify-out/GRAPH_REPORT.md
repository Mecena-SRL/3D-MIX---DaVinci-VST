# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 46 files · ~71,328 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2715 nodes · 4844 edges · 159 communities (70 shown, 89 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 195 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2ef1ba0a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- numpy
- server.py
- media.py
- cli.py
- test_ui_engine.py
- app.js
- MIX3D.cpp
- devices.py
- three.module.min.js
- ta
- mix3d
- ti
- .constructor
- Yp
- ei
- jl
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
- analysis.py
- mixer.py
- jr
- qs
- ts
- main.js
- cp
- ec
- kd
- jc
- Kn
- .setValues
- t
- .copy
- xh
- Fc
- mixer.py
- pm
- rp
- ld
- gh
- hh
- bl
- nm
- ua
- eq.js
- xr
- tu
- .updateMatrix
- Hn
- ml
- numpy
- look.py
- Sc
- qu
- em
- ya
- .constructor
- od
- .constructor
- ap
- nl
- .parse
- s
- lm
- package.json
- up
- .constructor
- Zh
- .constructor
- json
- om
- Dh
- eq.py
- $h
- hp
- im
- .setHSL
- resolve_install.py
- zp
- hl
- es
- wh
- zl
- estimate_drift
- wi
- xs
- .bind
- Ai
- su
- Hu
- .parseObject
- yh
- Ci
- dp
- Ph
- Ys
- yr
- Rh
- jh
- Yu
- Zc
- Qp
- mu
- qh
- Xu
- build_macos.sh
- build_plugin.sh
- Fh
- Ih
- Lh
- Oh
- Uh
- kh
- am
- n

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
- `Riconoscimento dai metadati` --references--> `detect()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/metadata.py
- `F0: verifiche su Resolve reale [V]` --references--> `MIX3D`  [INFERRED]
  docs/F0_verifiche.md → plugin/MIX3D/MIX3D.h
- `Compatibilità` --references--> `compat()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/devices.py
- `Compatibilità` --references--> `da()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/web/vendor/three.module.min.js
- `MIX3D` --references--> `MIX3D`  [INFERRED]
  README.md → plugin/MIX3D/MIX3D.h

## Import Cycles
- None detected.

## Communities (159 total, 89 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.23
Nodes (12): _bp(), test_auto_taratura(), test_banda_dinamica_agisce_solo_sopra_soglia(), test_curva_uguale_al_filtro(), test_look_master(), test_master_continuo_e_auto(), _track(), _frac_delay() (+4 more)

### Community 2 - "server.py"
Cohesion: 0.13
Nodes (9): apply_profile(), browse(), Handler, import_resolve(), new_project(), public_state(), start_job(), tracks_from_file() (+1 more)

### Community 3 - "media.py"
Cohesion: 0.09
Nodes (16): banner(), blocks(), decoded(), ffmpeg(), probe(), _bcd_tc(), detect(), read() (+8 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (18): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+10 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.08
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.06
Nodes (74): api(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color(), COLORS (+66 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.05
Nodes (28): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, F0: verifiche su Resolve reale [V] (+20 more)

### Community 8 - "devices.py"
Cohesion: 0.16
Nodes (11): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+3 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.08
Nodes (8): Ku, ma, nu, pu, ru, td, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.17
Nodes (7): app_bundle(), arch(), check(), download(), _fetch_json(), install(), parse()

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 28 - "bd"
Cohesion: 0.06
Nodes (10): ad, bd, ed(), md(), Md, pd(), rd, sd (+2 more)

### Community 29 - "eu"
Cohesion: 0.13
Nodes (3): eu, iu, xm

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 33 - "Oa"
Cohesion: 0.17
Nodes (5): Ha(), Oa, qa(), Va(), za()

### Community 35 - "e"
Cohesion: 0.09
Nodes (8): e, hd, a(), Vd, c(), wd, xp, zd

### Community 36 - "fp"
Cohesion: 0.15
Nodes (5): fp, Mi(), Nc, Nd, yi

### Community 37 - "vu"
Cohesion: 0.17
Nodes (23): Au(), bu(), Cu(), Du(), Eu(), fu(), gu(), Iu() (+15 more)

### Community 40 - "co"
Cohesion: 0.17
Nodes (22): Ao(), bo(), co(), Do(), fo(), go(), ho(), jo() (+14 more)

### Community 41 - "bi"
Cohesion: 0.11
Nodes (11): ai(), bi, ci(), fi(), ka(), nc, oi(), ph (+3 more)

### Community 42 - "$n"
Cohesion: 0.14
Nodes (3): $n(), rs(), _s

### Community 45 - "Nh"
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.11
Nodes (13): ba(), Ga(), ii(), ja(), bt(), Rt(), kl(), pa() (+5 more)

### Community 49 - "analysis.py"
Cohesion: 0.15
Nodes (5): analyze(), db(), k_weighting(), Loudness, warnings()

### Community 50 - "mixer.py"
Cohesion: 0.13
Nodes (9): _coarse(), sync_pair(), auto_positions(), estimate_sources(), locate(), same_clock_distances(), read(), auto_place() (+1 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, id, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.12
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): Fl, Mh, rc, ud

### Community 61 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 62 - ".copy"
Cohesion: 0.16
Nodes (3): cd, vc, xc()

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - "mixer.py"
Cohesion: 0.19
Nodes (7): spatial_params(), active(), correction_fir(), envelope_db(), print_mix(), render(), span()

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.12
Nodes (4): gh, Gm, Li, zm

### Community 70 - "hh"
Cohesion: 0.18
Nodes (4): Am, dd, hh, ym()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - "xr"
Cohesion: 0.11
Nodes (4): il, A(), ol(), xr

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.21
Nodes (14): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+6 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 85 - "ya"
Cohesion: 0.20
Nodes (11): v(), p(), xa(), g(), ya(), d(), f(), g() (+3 more)

### Community 88 - ".constructor"
Cohesion: 0.21
Nodes (6): Ft(), Jt(), kt(), Qt(), Yt(), zt()

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.17
Nodes (6): s(), r(), mp, i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 98 - ".constructor"
Cohesion: 0.22
Nodes (5): Gl, Ka, A(), C(), R()

### Community 100 - ".constructor"
Cohesion: 0.12
Nodes (5): Gu, lu, ou, a(), o()

### Community 101 - "json"
Cohesion: 0.26
Nodes (7): all_spaces(), builtin(), critical_distance(), get(), import_file(), local(), normalize()

### Community 105 - "eq.py"
Cohesion: 0.20
Nodes (9): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut() (+1 more)

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 110 - "resolve_install.py"
Cohesion: 0.42
Nodes (3): install(), install_fairlight(), status()

### Community 112 - "hl"
Cohesion: 0.29
Nodes (6): hl(), j(), K(), q(), W(), Ma()

### Community 113 - "es"
Cohesion: 0.22
Nodes (3): es, Mm, Zu

### Community 115 - "zl"
Cohesion: 0.38
Nodes (4): zl(), b(), E(), T()

### Community 117 - "estimate_drift"
Cohesion: 0.21
Nodes (6): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays()

### Community 118 - "wi"
Cohesion: 0.12
Nodes (9): Ea(), Fa(), ia, li, pi, ra, ri, wi (+1 more)

### Community 121 - ".bind"
Cohesion: 0.33
Nodes (3): bind(), getValue(), setValue()

### Community 125 - ".parseObject"
Cohesion: 0.08
Nodes (6): jd, $l, lp, op, qd, tc

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 156 - "am"
Cohesion: 0.32
Nodes (3): am(), rm, sm()

### Community 159 - "n"
Cohesion: 0.33
Nodes (5): _d(), da(), r(), Id(), n

## Knowledge Gaps
- **4 isolated node(s):** `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser`, `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1147 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **89 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Compatibilità` connect `MIX3D.cpp` to `devices.py`, `n`?**
  _High betweenness centrality (0.282) - this node is a cross-community bridge._
- **What connects `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `da()` connect `n` to `.constructor`, `three.module.min.js`, `.constructor`, `MIX3D.cpp`?**
  _High betweenness centrality (0.278) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12535612535612536 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `MIX3D.cpp`?**
  _High betweenness centrality (0.253) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08826945412311266 - nodes in this community are weakly interconnected._