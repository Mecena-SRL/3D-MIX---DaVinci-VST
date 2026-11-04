# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 47 files · ~72,156 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2725 nodes · 4861 edges · 142 communities (64 shown, 78 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 195 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `28b16b5b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- ai
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
- .constructor
- bt
- .isEmpty
- mixer.py
- jr
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
- yi
- bl
- nm
- zl
- eq.js
- Gu
- iu
- qd
- Hn
- ml
- numpy
- look.py
- Sc
- em
- ya
- .constructor
- od
- ap
- nl
- .parse
- s
- lm
- package.json
- up
- Zh
- .constructor
- om
- Dh
- eq.py
- $h
- jd
- im
- .setHSL
- zp
- es
- wh
- estimate_drift
- wi
- xs
- .bind
- Hu
- .parseObject
- Ci
- dp
- Ph
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
- hd

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

## Communities (142 total, 78 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.06
Nodes (10): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+2 more)

### Community 1 - "ai"
Cohesion: 0.40
Nodes (4): ai(), fi(), oi(), vi

### Community 2 - "server.py"
Cohesion: 0.09
Nodes (14): apply_profile(), eq_curve(), Handler, new_project(), public_state(), start_job(), wav_bytes(), all_spaces() (+6 more)

### Community 3 - "media.py"
Cohesion: 0.08
Nodes (18): suggest(), banner(), blocks(), decoded(), ffmpeg(), probe(), _bcd_tc(), detect() (+10 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (20): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+12 more)

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
Cohesion: 0.18
Nodes (10): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+2 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 16 - "jl"
Cohesion: 0.11
Nodes (7): Gl, jl, Ka, A(), C(), R(), Wl

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 19 - "Ii"
Cohesion: 0.06
Nodes (4): Ii, A(), ol(), xr

### Community 20 - "vs"
Cohesion: 0.13
Nodes (3): Ku, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.12
Nodes (11): install(), install_fairlight(), refresh_script(), status(), app_bundle(), arch(), check(), download() (+3 more)

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 27 - "As"
Cohesion: 0.07
Nodes (6): As, nu, pu, qu, ru, td

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
Cohesion: 0.11
Nodes (7): e, mp, Vd, c(), wd, xp, zd

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
Cohesion: 0.12
Nodes (7): bi, ci(), ia, nc, ph, rh, uh

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
Cohesion: 0.08
Nodes (15): analyze(), _coarse(), db(), k_weighting(), Loudness, sync_pair(), warnings(), auto_positions() (+7 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): cd, fl, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.13
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.11
Nodes (5): dd, id, Mh, rc, ud

### Community 61 - "t"
Cohesion: 0.17
Nodes (7): t(), n(), c(), l(), o(), r(), a()

### Community 63 - "xh"
Cohesion: 0.09
Nodes (8): Am, bm, Bm, fm, hh, wm, xh, ym()

### Community 65 - "mixer.py"
Cohesion: 0.19
Nodes (7): spatial_params(), active(), envelope_db(), print_mix(), render(), span(), browse()

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.10
Nodes (6): au, es, gh, Gm, su, zm

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 73 - "zl"
Cohesion: 0.06
Nodes (9): Fl, Ma(), mu, tu, ua, zl(), b(), E() (+1 more)

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.15
Nodes (22): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+14 more)

### Community 81 - "look.py"
Cohesion: 0.22
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 85 - "ya"
Cohesion: 0.10
Nodes (13): v(), ma, qs, p(), xa(), g(), ya(), d() (+5 more)

### Community 89 - "ap"
Cohesion: 0.23
Nodes (3): ap, Rp(), sp

### Community 91 - "nl"
Cohesion: 0.14
Nodes (6): el(), il, Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.25
Nodes (5): s(), r(), i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 100 - ".constructor"
Cohesion: 0.16
Nodes (4): lu, ou, a(), o()

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 107 - "jd"
Cohesion: 0.12
Nodes (3): hp, jd, lp

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 117 - "estimate_drift"
Cohesion: 0.15
Nodes (10): align(), DriftModel, estimate_drift(), fit_drift(), windowed_delays(), _frac_delay(), _music_like(), test_drift_one_hour_equivalent() (+2 more)

### Community 118 - "wi"
Cohesion: 0.13
Nodes (9): Ea(), li, pi, ra, ri, wi, Ys(), S() (+1 more)

### Community 121 - ".bind"
Cohesion: 0.20
Nodes (4): bind(), constructor(), getValue(), setValue()

### Community 125 - ".parseObject"
Cohesion: 0.14
Nodes (3): $l, op, tc

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 159 - "hd"
Cohesion: 0.14
Nodes (6): _d(), da(), r(), hd, Id(), n

## Knowledge Gaps
- **4 isolated node(s):** `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser`, `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1154 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **78 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Compatibilità` connect `MIX3D.cpp` to `devices.py`, `hd`?**
  _High betweenness centrality (0.276) - this node is a cross-community bridge._
- **What connects `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06025641025641026 - nodes in this community are weakly interconnected._
- **Why does `da()` connect `hd` to `jl`, `three.module.min.js`, `.constructor`, `MIX3D.cpp`?**
  _High betweenness centrality (0.275) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08819345661450925 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `MIX3D.cpp`?**
  _High betweenness centrality (0.263) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08181818181818182 - nodes in this community are weakly interconnected._