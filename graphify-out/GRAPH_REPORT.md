# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 24 files · ~45,911 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .css 1)

## Summary
- 2406 nodes · 4182 edges · 142 communities (55 shown, 87 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 183 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `96725c49`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- numpy
- server.py
- test_ui_engine.py
- cli.py
- .constructor
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
- xr
- Nc
- jr
- qs
- ts
- mp
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
- hd
- ua
- .constructor
- yr
- tu
- .updateMatrix
- Hn
- ml
- n
- ya
- Sc
- nu
- es
- xp
- Ku
- od
- ap
- nl
- .parse
- s
- lm
- mu
- up
- yh
- Zh
- am
- jh
- om
- .constructor
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
- wi
- xs
- Gu
- hl
- Hu
- kh
- Ci
- dp
- Ph
- .parseObject
- Rh
- Yu
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

## Communities (142 total, 87 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.12
Nodes (15): auto_positions(), same_clock_distances(), spatial_params(), auto_place(), align(), DriftModel, estimate_drift(), fit_drift() (+7 more)

### Community 2 - "server.py"
Cohesion: 0.10
Nodes (12): profile(), print_mix(), apply_profile(), browse(), Handler, import_resolve(), job_print(), new_project() (+4 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.10
Nodes (12): banner(), blocks(), decoded(), ffmpeg(), probe(), concert(), _music(), test_database_coerente() (+4 more)

### Community 4 - "cli.py"
Cohesion: 0.15
Nodes (13): cmd_info(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip, connect() (+5 more)

### Community 5 - ".constructor"
Cohesion: 0.16
Nodes (6): Gl, Ka, ql, A(), C(), R()

### Community 6 - "app.js"
Cohesion: 0.12
Nodes (34): api(), browse(), chainRisks(), color(), COLORS, css(), drawMiniWave(), drawPolar() (+26 more)

### Community 7 - "MIX3D"
Cohesion: 0.15
Nodes (10): Come i dati diventano utili, Da completare, Database dispositivi, F0: verifiche su Resolve reale [V], App per Mac (.dmg), Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`) (+2 more)

### Community 8 - "devices.py"
Cohesion: 0.12
Nodes (12): chain_risks(), correction_db(), load(), polar_gain(), response_db(), suggest(), active(), correction_fir() (+4 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (163): _a, aa, ac, ah, ao, ar, bh, Bi (+155 more)

### Community 10 - "analysis.py"
Cohesion: 0.10
Nodes (9): analyze(), _coarse(), db(), k_weighting(), Loudness, sync_pair(), warnings(), read() (+1 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.05
Nodes (4): constructor(), setValue(), Yp, zp

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 21 - "jd"
Cohesion: 0.12
Nodes (4): jd, lp, op, qd

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 27 - "As"
Cohesion: 0.09
Nodes (4): As, pu, qu, ru

### Community 28 - "bd"
Cohesion: 0.06
Nodes (11): ad, bd, ed(), md(), Md, pd(), rd, sd (+3 more)

### Community 32 - "steps"
Cohesion: 0.07
Nodes (26): runs-on, steps, strategy, jobs, dmg, os, name, on (+18 more)

### Community 33 - "Oa"
Cohesion: 0.08
Nodes (9): Ai, Ha(), Oa, qa(), Ri, ta, Va(), wp (+1 more)

### Community 35 - "e"
Cohesion: 0.17
Nodes (5): e, Vd, c(), wd, zd

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
Cohesion: 0.11
Nodes (13): Ga(), ii(), ja(), bt(), Rt(), ka(), kl(), pa() (+5 more)

### Community 49 - "xr"
Cohesion: 0.08
Nodes (10): Fl, il, A(), ol(), xr, zl(), b(), E() (+2 more)

### Community 50 - "Nc"
Cohesion: 0.20
Nodes (4): Mi(), Nc, Nd, yi

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): cd, fl, mh, ts

### Community 56 - "ec"
Cohesion: 0.10
Nodes (6): Dm(), ec, nm, a(), o(), Xn()

### Community 57 - "kd"
Cohesion: 0.12
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): id, Mh, rc, ud

### Community 61 - "t"
Cohesion: 0.19
Nodes (7): t(), n(), c(), l(), o(), r(), ym()

### Community 63 - "xh"
Cohesion: 0.27
Nodes (3): bm, fm, xh

### Community 65 - ".constructor"
Cohesion: 0.19
Nodes (8): W(), Ft(), Jt(), kt(), Qt(), Xt(), Yt(), zt()

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 70 - "hh"
Cohesion: 0.12
Nodes (5): Am, Bm, dd, hh, wm

### Community 78 - "Hn"
Cohesion: 0.25
Nodes (4): as, Hn, nr, _p

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "n"
Cohesion: 0.33
Nodes (3): da(), r(), n

### Community 81 - "ya"
Cohesion: 0.15
Nodes (12): v(), ma, p(), xa(), g(), ya(), d(), f() (+4 more)

### Community 84 - "es"
Cohesion: 0.22
Nodes (3): es, Mm, Zu

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.25
Nodes (5): s(), r(), i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 100 - "am"
Cohesion: 0.32
Nodes (3): am(), rm, sm()

### Community 103 - ".constructor"
Cohesion: 0.15
Nodes (4): au, Gm, Li, su

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 110 - ".constructor"
Cohesion: 0.17
Nodes (4): ju, lu, ou, Tm

### Community 115 - "ai"
Cohesion: 0.40
Nodes (4): ai(), fi(), oi(), vi

### Community 118 - "wi"
Cohesion: 0.13
Nodes (9): Ea(), Fa(), li, pi, ra, ri, wi, Ys() (+1 more)

### Community 123 - "hl"
Cohesion: 0.67
Nodes (4): hl(), j(), K(), q()

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1026 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **87 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ti` connect `ti` to `.constructor`, `three.module.min.js`, `cs`, `vs`, `As`, `bd`, `eu`, `.parse`, `Oa`, `bi`, `Nh`, `xr`, `ts`, `kd`, `.setValues`, `.copy`, `.constructor`, `rp`, `ld`, `hd`, `.constructor`, `Hn`, `nl`, `s`, `om`, `Dh`, `$h`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `ei` connect `ei` to `Nr`, `.parse`, `three.module.min.js`, `bi`, `ti`, `ba`, `.getNormalMatrix`, `.divideScalar`, `.premultiply`, `As`, `.copy`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.12121212121212122 - nodes in this community are weakly interconnected._
- **Why does `player` connect `app.js` to `ap`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09848484848484848 - nodes in this community are weakly interconnected._