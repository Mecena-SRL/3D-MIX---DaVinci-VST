# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 27 files · ~47,120 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 1, .xml 1, .css 1)

## Summary
- 2451 nodes · 4247 edges · 150 communities (63 shown, 87 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 186 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e1e9949b`
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
- analysis.py
- mix3d
- ti
- .constructor
- Yp
- ei
- ta
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
- kd
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
- na
- yr
- tu
- .updateMatrix
- Hn
- ml
- ya
- Sc
- .setIndex
- es
- ou
- od
- ap
- nl
- .parse
- s
- Li
- lm
- package.json
- up
- Wa
- Zh
- am
- om
- su
- Dh
- em
- $h
- hp
- im
- .setHSL
- .constructor
- wh
- ai
- getValue
- wi
- Id
- xs
- hl
- Hu
- Ci
- dp
- Ph
- $l
- Rh
- .constructor
- Zc
- Qp
- Xu
- build_macos.sh
- ba
- Fh
- Ih
- Lh
- Oh
- Uh

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

## Communities (150 total, 87 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.18
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 2 - "server.py"
Cohesion: 0.13
Nodes (9): apply_profile(), browse(), Handler, import_resolve(), new_project(), public_state(), start_job(), tracks_from_file() (+1 more)

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
Cohesion: 0.12
Nodes (36): api(), browse(), chainRisks(), color(), COLORS, css(), drawMiniWave(), drawPolar() (+28 more)

### Community 7 - "MIX3D"
Cohesion: 0.14
Nodes (11): Come i dati diventano utili, Da completare, Database dispositivi, F0: verifiche su Resolve reale [V], App per Mac (.dmg), Da DaVinci Resolve, Installazione da sorgente (macOS), MIX3D (+3 more)

### Community 8 - "devices.py"
Cohesion: 0.19
Nodes (8): chain_risks(), correction_db(), load(), polar_gain(), profile(), response_db(), suggest(), devices_payload()

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 10 - "analysis.py"
Cohesion: 0.10
Nodes (9): analyze(), _coarse(), db(), k_weighting(), Loudness, sync_pair(), warnings(), read() (+1 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.05
Nodes (4): constructor(), setValue(), Yp, zp

### Community 16 - "ta"
Cohesion: 0.06
Nodes (9): Gl, jl, Ka, A(), C(), R(), ta, Wl (+1 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 19 - "Ii"
Cohesion: 0.05
Nodes (5): Ii, il, A(), ol(), xr

### Community 20 - "vs"
Cohesion: 0.09
Nodes (8): Gu, Ku, a(), o(), pu, td, $u, vs

### Community 21 - "jd"
Cohesion: 0.09
Nodes (5): jd, lp, op, qd, tc

### Community 26 - "Nr"
Cohesion: 0.08
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
Cohesion: 0.13
Nodes (7): Ai, Ha(), Oa, qa(), Ri, Va(), za()

### Community 35 - "e"
Cohesion: 0.10
Nodes (8): e, hd, a(), Vd, c(), wd, xp, zd

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
Cohesion: 0.06
Nodes (10): dh, _h, jh, kh, Nh, qh, Wh(), Xh() (+2 more)

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.14
Nodes (10): Ga(), ja(), bt(), Rt(), ka(), kl(), pa(), Pl() (+2 more)

### Community 49 - "zl"
Cohesion: 0.38
Nodes (4): zl(), b(), E(), T()

### Community 50 - "mixer.py"
Cohesion: 0.14
Nodes (9): auto_positions(), same_clock_distances(), spatial_params(), active(), correction_fir(), print_mix(), render(), span() (+1 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, id, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 56 - "ec"
Cohesion: 0.12
Nodes (4): ec, Mi(), Xn(), yi

### Community 57 - "kd"
Cohesion: 0.13
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.12
Nodes (4): dd, Fl, Mh, rc

### Community 61 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

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
Cohesion: 0.16
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.13
Nodes (4): es, gh, Gm, zm

### Community 70 - "hh"
Cohesion: 0.17
Nodes (4): Am, Bm, hh, ym()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 76 - "tu"
Cohesion: 0.11
Nodes (5): da(), r(), mu, n, tu

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 81 - "ya"
Cohesion: 0.20
Nodes (11): v(), p(), xa(), g(), ya(), d(), f(), g() (+3 more)

### Community 83 - ".setIndex"
Cohesion: 0.11
Nodes (4): ma, nu, qu, ru

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

### Community 98 - "Wa"
Cohesion: 0.50
Nodes (3): ii(), Wa(), o()

### Community 100 - "am"
Cohesion: 0.32
Nodes (3): am(), rm, sm()

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 115 - "ai"
Cohesion: 0.40
Nodes (4): ai(), fi(), oi(), vi

### Community 118 - "wi"
Cohesion: 0.12
Nodes (10): Ea(), Fa(), li, pi, ra, ri, wi, Ys() (+2 more)

### Community 123 - "hl"
Cohesion: 0.33
Nodes (5): hl(), j(), K(), q(), Ma()

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1053 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **87 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ui` connect `Ui` to `.setFromSpherical`, `three.module.min.js`, `ti`, `ta`, `vs`, `Oi`, `Nr`, `As`, `.parse`, `Oa`, `Nh`, `cp`, `.constructor`, `rp`, `gh`, `ml`, `ya`, `.setIndex`, `es`, `.normalize`, `.angleTo`, `nl`, `.parse`, `s`, `.fromArray`, `su`, `.applyQuaternion`, `.applyMatrix4`, `wh`, `.applyMatrix3`, `.copy`, `.distanceTo`, `.setFromCylindrical`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `ei` connect `ei` to `Nr`, `.parse`, `three.module.min.js`, `bi`, `ti`, `ba`, `.getNormalMatrix`, `.divideScalar`, `.premultiply`, `As`, `.copy`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12535612535612536 - nodes in this community are weakly interconnected._
- **Why does `Kr` connect `Kr` to `$l`, `three.module.min.js`, `ta`, `jd`, `bd`, `.parse`, `e`, `ts`, `.setValues`, `.copy`, `xh`, `.constructor`, `ld`, `gh`, `hh`, `nm`, `.updateMatrix`, `ml`, `ya`, `om`, `.setHSL`, `.setStyle`, `hl`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11260504201680673 - nodes in this community are weakly interconnected._