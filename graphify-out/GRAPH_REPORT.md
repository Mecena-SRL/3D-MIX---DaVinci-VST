# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 24 files · ~45,664 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .css 1)

## Summary
- 2401 nodes · 4171 edges · 159 communities (61 shown, 98 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 183 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b271df64`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- numpy
- server.py
- test_ui_engine.py
- cli.py
- mixer.py
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
- xr
- Vp
- jr
- qs
- ts
- xd
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
- geometry.py
- ld
- gh
- hh
- bl
- hd
- ua
- .constructor
- yr
- tu
- .updateMatrix
- Hn
- ml
- nm
- ya
- Sc
- na
- es
- zl
- od
- jn
- ap
- nl
- .parse
- s
- il
- lm
- mu
- up
- yh
- Zh
- am
- jh
- om
- su
- Dh
- em
- $h
- hp
- im
- .setHSL
- .constructor
- qh
- wh
- ai
- .isEmpty
- wi
- xs
- Li
- Gu
- hl
- Hu
- kh
- Ai
- Ci
- dp
- Ph
- pu
- $l
- Rh
- Yu
- Zc
- Qp
- Xu
- build_macos.sh
- ba
- getValue
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

## Communities (159 total, 98 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.18
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 2 - "server.py"
Cohesion: 0.11
Nodes (13): connect(), apply_profile(), auto_place(), browse(), Handler, import_resolve(), job_analyze(), job_print() (+5 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.10
Nodes (11): blocks(), decoded(), ffmpeg(), probe(), concert(), _music(), test_api_http(), test_database_coerente() (+3 more)

### Community 4 - "cli.py"
Cohesion: 0.16
Nodes (12): cmd_info(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip, current_timeline() (+4 more)

### Community 5 - "mixer.py"
Cohesion: 0.23
Nodes (6): spatial_params(), active(), correction_fir(), print_mix(), render(), span()

### Community 6 - "app.js"
Cohesion: 0.12
Nodes (34): api(), browse(), chainRisks(), color(), COLORS, css(), drawMiniWave(), drawPolar() (+26 more)

### Community 7 - "MIX3D"
Cohesion: 0.15
Nodes (10): Come i dati diventano utili, Da completare, Database dispositivi, F0: verifiche su Resolve reale [V], App per Mac (.dmg), Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`) (+2 more)

### Community 8 - "devices.py"
Cohesion: 0.18
Nodes (8): chain_risks(), correction_db(), load(), polar_gain(), profile(), response_db(), suggest(), devices_payload()

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 10 - "analysis.py"
Cohesion: 0.13
Nodes (5): analyze(), db(), k_weighting(), Loudness, warnings()

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.05
Nodes (4): constructor(), setValue(), Yp, zp

### Community 16 - "ta"
Cohesion: 0.06
Nodes (11): da(), r(), Gl, jl, Ka, A(), C(), R() (+3 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.09
Nodes (7): Ku, ma, nu, ru, $u, vs, Zu

### Community 21 - ".parseObject"
Cohesion: 0.07
Nodes (7): ip, jd, lp, op, qd, rp, tc

### Community 26 - "Nr"
Cohesion: 0.08
Nodes (4): gm, np, Nr, uc

### Community 28 - "bd"
Cohesion: 0.11
Nodes (6): bd, ed(), Md, pd(), rd, td

### Community 29 - "eu"
Cohesion: 0.13
Nodes (3): eu, iu, xm

### Community 32 - "steps"
Cohesion: 0.08
Nodes (24): runs-on, steps, strategy, jobs, dmg, os, name, on (+16 more)

### Community 33 - "Oa"
Cohesion: 0.16
Nodes (6): Fa(), Ha(), Oa, qa(), Va(), za()

### Community 35 - "e"
Cohesion: 0.10
Nodes (8): e, n(), mp, Vd, c(), wd, xp, zd

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
Nodes (8): bi, ci(), ia, ka(), nc, ph, rh, uh

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
Nodes (13): Ea(), Ga(), ii(), ja(), bt(), Rt(), kl(), pa() (+5 more)

### Community 52 - "qs"
Cohesion: 0.14
Nodes (8): qs, p(), ra, xa(), g(), d(), Ys(), Zs()

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, id, mh, ts

### Community 54 - "xd"
Cohesion: 0.15
Nodes (4): md(), sd, xd, yd

### Community 57 - "kd"
Cohesion: 0.13
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): dd, Mh, rc, ud

### Community 61 - "t"
Cohesion: 0.19
Nodes (6): t(), c(), l(), o(), r(), a()

### Community 62 - ".copy"
Cohesion: 0.16
Nodes (3): cd, vc, xc()

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - ".constructor"
Cohesion: 0.21
Nodes (7): Ft(), Jt(), kt(), Qt(), Xt(), Yt(), zt()

### Community 67 - "geometry.py"
Cohesion: 0.17
Nodes (5): _coarse(), sync_pair(), auto_positions(), same_clock_distances(), read()

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 70 - "hh"
Cohesion: 0.17
Nodes (4): Am, Bm, hh, ym()

### Community 72 - "hd"
Cohesion: 0.17
Nodes (4): _d(), hd, Id(), n

### Community 74 - ".constructor"
Cohesion: 0.18
Nodes (4): lu, ou, a(), o()

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 81 - "ya"
Cohesion: 0.27
Nodes (7): v(), ya(), f(), g(), u(), x(), y()

### Community 84 - "es"
Cohesion: 0.22
Nodes (3): es, Mm, zm

### Community 85 - "zl"
Cohesion: 0.24
Nodes (5): Fl, zl(), b(), E(), T()

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.25
Nodes (5): s(), r(), i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 94 - "il"
Cohesion: 0.25
Nodes (3): il, A(), ol()

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
Cohesion: 0.33
Nodes (5): li, pi, ri, wi, S()

### Community 123 - "hl"
Cohesion: 0.50
Nodes (5): hl(), j(), K(), q(), W()

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1025 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **98 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ei` connect `ei` to `Nr`, `.parse`, `three.module.min.js`, `bi`, `ti`, `ba`, `.getNormalMatrix`, `.divideScalar`, `.premultiply`, `As`, `.copy`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `player` connect `app.js` to `ap`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11397849462365592 - nodes in this community are weakly interconnected._
- **Why does `ti` connect `ti` to `three.module.min.js`, `ta`, `cs`, `vs`, `.parseObject`, `As`, `eu`, `.parse`, `Oa`, `bi`, `Nh`, `xd`, `kd`, `.setValues`, `.copy`, `.constructor`, `ld`, `hd`, `.constructor`, `Hn`, `zl`, `jn`, `nl`, `s`, `su`, `Dh`, `$h`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Should `test_ui_engine.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1032258064516129 - nodes in this community are weakly interconnected._