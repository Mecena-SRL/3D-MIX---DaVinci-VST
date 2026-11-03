# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 34 files · ~56,744 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: .whl 4, (none) 1, .xml 1)

## Summary
- 2572 nodes · 4573 edges · 159 communities (65 shown, 94 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ee55fc2`
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
- eq.js
- xr
- tu
- .updateMatrix
- Hn
- ml
- autotune.py
- ya
- Sc
- qu
- .add
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
- Wa
- Zh
- .constructor
- om
- su
- Dh
- eq.py
- $h
- hp
- im
- .setHSL
- .constructor
- yr
- wh
- ai
- test_eq.py
- wi
- Id
- xs
- am
- hl
- Hu
- yh
- Ci
- dp
- Ph
- tc
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
- iu
- .isEmpty
- Fh
- Ih
- Lh
- Oh
- Uh
- kh
- yi

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

## Communities (159 total, 94 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.09
Nodes (18): _coarse(), sync_pair(), auto_positions(), estimate_sources(), locate(), same_clock_distances(), read(), align() (+10 more)

### Community 2 - "server.py"
Cohesion: 0.12
Nodes (13): apply_profile(), auto_place(), browse(), eq_curve(), Handler, import_resolve(), job_analyze(), job_eq_auto() (+5 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.17
Nodes (7): banner(), blocks(), decoded(), ffmpeg(), probe(), install(), status()

### Community 4 - "cli.py"
Cohesion: 0.10
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
Cohesion: 0.19
Nodes (8): chain_risks(), correction_db(), load(), polar_gain(), profile(), response_db(), suggest(), devices_payload()

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 10 - "analysis.py"
Cohesion: 0.16
Nodes (5): analyze(), db(), k_weighting(), Loudness, warnings()

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.05
Nodes (4): constructor(), setValue(), Yp, zp

### Community 16 - "jl"
Cohesion: 0.08
Nodes (8): em, Gl, jl, Ka, A(), C(), R(), Wl

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.07
Nodes (9): Ku, ma, nu, pu, ru, td, $u, vs (+1 more)

### Community 21 - ".parseObject"
Cohesion: 0.09
Nodes (5): jd, $l, lp, op, qd

### Community 26 - "Nr"
Cohesion: 0.08
Nodes (4): gm, np, Nr, uc

### Community 28 - "bd"
Cohesion: 0.06
Nodes (10): ad, bd, ed(), md(), Md, pd(), rd, sd (+2 more)

### Community 32 - "steps"
Cohesion: 0.06
Nodes (33): runs-on, steps, strategy, release, jobs, dmg, os, name (+25 more)

### Community 33 - "Oa"
Cohesion: 0.09
Nodes (7): Ha(), Oa, qa(), ta, Va(), wp, za()

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
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.12
Nodes (11): ba(), Ga(), ja(), bt(), Rt(), ka(), kl(), pa() (+3 more)

### Community 49 - "zl"
Cohesion: 0.24
Nodes (5): Fl, zl(), b(), E(), T()

### Community 50 - "mixer.py"
Cohesion: 0.23
Nodes (6): spatial_params(), active(), correction_fir(), print_mix(), render(), span()

### Community 53 - "ts"
Cohesion: 0.11
Nodes (5): cd, fl, id, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.13
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.12
Nodes (4): dd, Mh, rc, ud

### Community 61 - "t"
Cohesion: 0.27
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - ".constructor"
Cohesion: 0.19
Nodes (8): W(), Ft(), Jt(), kt(), Qt(), Xt(), Yt(), zt()

### Community 68 - "ld"
Cohesion: 0.16
Nodes (3): fd(), gd(), ld

### Community 70 - "hh"
Cohesion: 0.18
Nodes (4): Am, Bm, hh, ym()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.20
Nodes (26): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+18 more)

### Community 75 - "xr"
Cohesion: 0.11
Nodes (4): il, A(), ol(), xr

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "autotune.py"
Cohesion: 0.23
Nodes (12): balance(), _band(), masking(), resonances(), room(), run(), segments(), _smooth() (+4 more)

### Community 81 - "ya"
Cohesion: 0.20
Nodes (11): v(), p(), xa(), g(), ya(), d(), f(), g() (+3 more)

### Community 86 - "spazi.py"
Cohesion: 0.26
Nodes (7): all_spaces(), builtin(), critical_distance(), get(), import_file(), local(), normalize()

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

### Community 100 - ".constructor"
Cohesion: 0.18
Nodes (3): Gu, a(), o()

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 110 - ".constructor"
Cohesion: 0.11
Nodes (6): es, ju, lu, Mm, ou, Tm

### Community 115 - "ai"
Cohesion: 0.40
Nodes (4): ai(), fi(), oi(), vi

### Community 117 - "test_eq.py"
Cohesion: 0.24
Nodes (5): _bp(), test_auto_taratura(), test_banda_dinamica_agisce_solo_sopra_soglia(), test_curva_uguale_al_filtro(), _track()

### Community 118 - "wi"
Cohesion: 0.12
Nodes (10): Ea(), Fa(), li, pi, ra, ri, wi, Ys() (+2 more)

### Community 122 - "am"
Cohesion: 0.32
Nodes (3): am(), rm, sm()

### Community 123 - "hl"
Cohesion: 0.33
Nodes (5): hl(), j(), K(), q(), Ma()

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 138 - "mu"
Cohesion: 0.18
Nodes (4): da(), r(), mu, n

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1084 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **94 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `player` connect `app.js` to `ap`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `Ui` connect `Ui` to `three.module.min.js`, `ti`, `jl`, `vs`, `Oi`, `kh`, `Nr`, `As`, `.parse`, `.clone`, `Oa`, `.cross`, `Nh`, `cp`, `.constructor`, `rp`, `gh`, `ml`, `ya`, `.normalize`, `.angleTo`, `nl`, `.parse`, `s`, `.constructor`, `.fromArray`, `su`, `.applyQuaternion`, `wh`, `.applyMatrix3`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.09413067552602436 - nodes in this community are weakly interconnected._
- **Why does `ti` connect `ti` to `three.module.min.js`, `jl`, `cs`, `vs`, `As`, `bd`, `eu`, `.parse`, `Oa`, `e`, `bi`, `Nh`, `zl`, `ts`, `kd`, `.setValues`, `.copy`, `.constructor`, `rp`, `ld`, `Hn`, `nl`, `s`, `.constructor`, `om`, `su`, `Dh`, `$h`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11954022988505747 - nodes in this community are weakly interconnected._