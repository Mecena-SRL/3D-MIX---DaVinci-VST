# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 37 files · ~67,586 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 1, .xml 1, .css 1)

## Summary
- 2625 nodes · 4710 edges · 159 communities (59 shown, 100 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 192 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b31c7027`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- vs
- server.py
- test_ui_engine.py
- cli.py
- test_ui_engine.py
- app.js
- MIX3D
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
- jd
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
- xm
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
- .constructor
- od
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
- om
- hd
- Dh
- eq.py
- $h
- hp
- im
- .setHSL
- ou
- zp
- es
- wh
- lp
- estimate_drift
- wi
- xs
- yi
- iu
- su
- Hu
- .parseObject
- yh
- Ci
- dp
- Ph
- yr
- Rh
- jh
- .constructor
- Zc
- Qp
- mu
- qh
- Xu
- build_macos.sh
- wp
- .isEmpty
- Fh
- Ih
- Lh
- Oh
- Uh
- kh
- am
- n
- ba

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
- `Compatibilità` --references--> `compat()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/devices.py
- `Compatibilità` --references--> `da()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/web/vendor/three.module.min.js
- `test_read_audio_clips()` --calls--> `read_audio_clips()`  [EXTRACTED]
  tests/test_resolve_bridge.py → src/mix3d/resolve_bridge.py
- `test_reimport_adds_new_track_only()` --calls--> `reimport_wav()`  [EXTRACTED]
  tests/test_resolve_bridge.py → src/mix3d/resolve_bridge.py
- `test_gcc_phat_subsample()` --calls--> `gcc_phat()`  [EXTRACTED]
  tests/test_sync.py → src/mix3d/sync.py

## Import Cycles
- None detected.

## Communities (159 total, 100 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "vs"
Cohesion: 0.12
Nodes (5): Bm, pu, td, $u, vs

### Community 2 - "server.py"
Cohesion: 0.10
Nodes (11): apply_profile(), browse(), eq_curve(), Handler, import_resolve(), new_project(), public_state(), start_job() (+3 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.17
Nodes (7): banner(), blocks(), decoded(), ffmpeg(), probe(), install(), status()

### Community 4 - "cli.py"
Cohesion: 0.12
Nodes (18): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+10 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.08
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.07
Nodes (72): api(), barChart(), browse(), CAMERAS, chainRisks(), color(), COLORS, css() (+64 more)

### Community 7 - "MIX3D"
Cohesion: 0.10
Nodes (17): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, F0: verifiche su Resolve reale [V], Preset inclusi (+9 more)

### Community 8 - "devices.py"
Cohesion: 0.10
Nodes (17): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+9 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.08
Nodes (3): constructor(), setValue(), Yp

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.11
Nodes (4): Ku, ma, nu, ru

### Community 21 - "jd"
Cohesion: 0.18
Nodes (3): jd, op, qd

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 28 - "bd"
Cohesion: 0.06
Nodes (10): ad, bd, ed(), md(), Md, pd(), rd, sd (+2 more)

### Community 32 - "steps"
Cohesion: 0.06
Nodes (33): runs-on, steps, strategy, release, jobs, dmg, os, name (+25 more)

### Community 33 - "Oa"
Cohesion: 0.13
Nodes (7): Ai, Ha(), Oa, qa(), Ri, Va(), za()

### Community 35 - "e"
Cohesion: 0.11
Nodes (7): e, a(), Vd, c(), wd, xp, zd

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

### Community 45 - "Nh"
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - ".constructor"
Cohesion: 0.07
Nodes (37): ai(), fi(), hl(), j(), K(), q(), W(), Ft() (+29 more)

### Community 48 - "bt"
Cohesion: 0.11
Nodes (13): Ga(), ii(), ja(), bt(), Rt(), ka(), kl(), pa() (+5 more)

### Community 49 - "analysis.py"
Cohesion: 0.15
Nodes (5): analyze(), db(), k_weighting(), Loudness, warnings()

### Community 50 - "mixer.py"
Cohesion: 0.09
Nodes (16): _coarse(), sync_pair(), auto_positions(), estimate_sources(), locate(), same_clock_distances(), spatial_params(), read() (+8 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, mh, ts, ud

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.13
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): cd, id, Mh, rc

### Community 61 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 63 - "xh"
Cohesion: 0.27
Nodes (3): bm, fm, xh

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 70 - "hh"
Cohesion: 0.13
Nodes (5): Am, dd, hh, wm, ym()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - "xr"
Cohesion: 0.06
Nodes (20): v(), Fl, A(), ol(), p(), xa(), g(), xr (+12 more)

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.14
Nodes (21): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+13 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 91 - "nl"
Cohesion: 0.14
Nodes (6): el(), il, Ko, nl(), $o, Qo

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
Cohesion: 0.19
Nodes (3): Gu, a(), o()

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 113 - "es"
Cohesion: 0.17
Nodes (4): es, Mm, zm, Zu

### Community 117 - "estimate_drift"
Cohesion: 0.15
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 118 - "wi"
Cohesion: 0.13
Nodes (9): Ea(), Fa(), li, pi, ra, ri, wi, Ys() (+1 more)

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
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1104 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **100 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `da()` connect `n` to `three.module.min.js`, `.constructor`, `.constructor`, `MIX3D`?**
  _High betweenness centrality (0.230) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `Compatibilità` connect `MIX3D` to `devices.py`, `n`?**
  _High betweenness centrality (0.230) - this node is a cross-community bridge._
- **Should `vs` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `MIX3D`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1032258064516129 - nodes in this community are weakly interconnected._