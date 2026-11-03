# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 34 files · ~57,153 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 1, .xml 1, .css 1)

## Summary
- 2576 nodes · 4587 edges · 158 communities (67 shown, 91 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1fe99267`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- numpy
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
- .parseObject
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
- zl
- mixer.py
- jr
- qs
- ts
- main.js
- cp
- ec
- ia
- jc
- Kn
- .setValues
- t
- .copy
- xh
- Fc
- .constructor
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
- ya
- Sc
- qu
- em
- spazi.py
- od
- ap
- nl
- .parse
- s
- Li
- lm
- package.json
- up
- .constructor
- Zh
- .constructor
- om
- il
- Dh
- eq.py
- $h
- hp
- im
- .setHSL
- .constructor
- Zu
- wh
- ai
- scipy_signal
- wi
- hd
- xs
- hl
- Hu
- $l
- yh
- Ci
- dp
- Ph
- xp
- Ai
- Rh
- jh
- Yu
- Zc
- Qp
- mu
- qh
- Xu
- build_macos.sh
- .isEmpty
- Fh
- Ih
- Lh
- ba
- Oh
- Uh
- kh
- getValue

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
- `test_read_audio_clips()` --calls--> `read_audio_clips()`  [EXTRACTED]
  tests/test_resolve_bridge.py → src/mix3d/resolve_bridge.py
- `test_reimport_adds_new_track_only()` --calls--> `reimport_wav()`  [EXTRACTED]
  tests/test_resolve_bridge.py → src/mix3d/resolve_bridge.py
- `test_gcc_phat_subsample()` --calls--> `gcc_phat()`  [EXTRACTED]
  tests/test_sync.py → src/mix3d/sync.py
- `test_fit_drift_rejects_outliers()` --calls--> `fit_drift()`  [EXTRACTED]
  tests/test_sync.py → src/mix3d/sync.py
- `test_drift_one_hour_equivalent()` --calls--> `estimate_drift()`  [EXTRACTED]
  tests/test_sync.py → src/mix3d/sync.py

## Import Cycles
- None detected.

## Communities (158 total, 91 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.08
Nodes (18): analyze(), _coarse(), db(), sync_pair(), warnings(), auto_positions(), estimate_sources(), locate() (+10 more)

### Community 2 - "server.py"
Cohesion: 0.12
Nodes (9): apply_profile(), eq_curve(), Handler, import_resolve(), new_project(), public_state(), start_job(), tracks_from_file() (+1 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.17
Nodes (7): banner(), blocks(), decoded(), ffmpeg(), probe(), install(), status()

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (18): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+10 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.09
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.08
Nodes (62): api(), barChart(), browse(), CAMERAS, chainRisks(), color(), COLORS, css() (+54 more)

### Community 7 - "MIX3D"
Cohesion: 0.11
Nodes (14): Come i dati diventano utili, Da completare, Database dispositivi, F0: verifiche su Resolve reale [V], Preset inclusi, Spazi 3D, Spazi privati (file), App per Mac (.dmg) (+6 more)

### Community 8 - "devices.py"
Cohesion: 0.21
Nodes (8): chain_risks(), correction_db(), load(), polar_gain(), profile(), response_db(), suggest(), devices_payload()

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.05
Nodes (4): constructor(), setValue(), Yp, zp

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.07
Nodes (10): au, Ku, ma, nu, pu, ru, su, td (+2 more)

### Community 21 - ".parseObject"
Cohesion: 0.09
Nodes (5): jd, lp, op, qd, tc

### Community 25 - "Kr"
Cohesion: 0.08
Nodes (3): fi(), gi(), Kr

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
Nodes (33): runs-on, steps, strategy, release, jobs, dmg, os, name (+25 more)

### Community 33 - "Oa"
Cohesion: 0.17
Nodes (5): Ha(), Oa, qa(), Va(), za()

### Community 35 - "e"
Cohesion: 0.13
Nodes (6): e, mp, Vd, c(), wd, zd

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
Cohesion: 0.14
Nodes (7): bi, ci(), ka(), nc, ph, rh, uh

### Community 42 - "$n"
Cohesion: 0.14
Nodes (3): $n(), rs(), _s

### Community 43 - "lr"
Cohesion: 0.06
Nodes (6): am(), lr, rm, sm(), Tl(), yr

### Community 45 - "Nh"
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.12
Nodes (12): Ga(), ii(), ja(), bt(), Rt(), kl(), pa(), Pl() (+4 more)

### Community 49 - "zl"
Cohesion: 0.38
Nodes (4): zl(), b(), E(), T()

### Community 50 - "mixer.py"
Cohesion: 0.11
Nodes (9): k_weighting(), Loudness, spatial_params(), active(), correction_fir(), print_mix(), render(), span() (+1 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, mh, rc, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 56 - "ec"
Cohesion: 0.12
Nodes (4): ec, Mi(), Xn(), yi

### Community 57 - "ia"
Cohesion: 0.25
Nodes (3): Gd, o(), ia

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): dd, Fl, id, Mh

### Community 61 - "t"
Cohesion: 0.18
Nodes (4): t(), n(), r(), a()

### Community 62 - ".copy"
Cohesion: 0.12
Nodes (4): cd, ud, vc, xc()

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - ".constructor"
Cohesion: 0.19
Nodes (8): W(), Ft(), Jt(), kt(), Qt(), Xt(), Yt(), zt()

### Community 68 - "ld"
Cohesion: 0.21
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.12
Nodes (4): es, gh, Gm, zm

### Community 70 - "hh"
Cohesion: 0.17
Nodes (4): Am, Bm, hh, ym()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.19
Nodes (27): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+19 more)

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.15
Nodes (20): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+12 more)

### Community 81 - "ya"
Cohesion: 0.20
Nodes (11): v(), p(), xa(), g(), ya(), d(), f(), g() (+3 more)

### Community 86 - "spazi.py"
Cohesion: 0.20
Nodes (7): all_spaces(), builtin(), critical_distance(), get(), import_file(), local(), normalize()

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.25
Nodes (5): s(), r(), i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 98 - ".constructor"
Cohesion: 0.18
Nodes (7): da(), r(), Gl, Ka, A(), C(), R()

### Community 100 - ".constructor"
Cohesion: 0.12
Nodes (5): Gu, lu, ou, a(), o()

### Community 103 - "il"
Cohesion: 0.25
Nodes (3): il, A(), ol()

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 115 - "ai"
Cohesion: 0.31
Nodes (6): ai(), c(), l(), o(), oi(), vi

### Community 117 - "scipy_signal"
Cohesion: 0.36
Nodes (5): _frac_delay(), _music_like(), test_drift_one_hour_equivalent(), test_fit_drift_rejects_outliers(), test_gcc_phat_subsample()

### Community 118 - "wi"
Cohesion: 0.12
Nodes (10): Ea(), Fa(), li, pi, ra, ri, wi, Ys() (+2 more)

### Community 119 - "hd"
Cohesion: 0.22
Nodes (3): _d(), hd, Id()

### Community 123 - "hl"
Cohesion: 0.33
Nodes (5): hl(), j(), K(), q(), Ma()

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1086 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **91 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `player` connect `app.js` to `ap`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `Ui` connect `Ui` to `three.module.min.js`, `ti`, `jl`, `vs`, `Oi`, `kh`, `As`, `.parse`, `.clone`, `Oa`, `.cross`, `Nh`, `cp`, `.constructor`, `rp`, `gh`, `xr`, `ml`, `ya`, `.normalize`, `.angleTo`, `nl`, `.parse`, `s`, `.constructor`, `.constructor`, `.fromArray`, `.applyQuaternion`, `Zu`, `wh`, `.applyMatrix3`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.08246225319396051 - nodes in this community are weakly interconnected._
- **Why does `Nr` connect `Nr` to `up`, `gh`, `three.module.min.js`, `xr`, `.updateMatrix`, `.constructor`, `bt`, `Sc`, `Ii`, `em`, `.parseObject`, `qs`, `wh`, `.copy`, `xs`, `t`, `lm`, `xh`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._