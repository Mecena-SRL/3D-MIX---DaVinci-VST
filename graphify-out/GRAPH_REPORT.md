# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 50 files · ~80,743 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2844 nodes · 5120 edges · 161 communities (77 shown, 84 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 206 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `46019983`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- media.py
- hh
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
- ta
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
- yh
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
- MIX3D
- pm
- wi
- ld
- gh
- analysis.py
- bl
- nm
- ua
- eq.js
- .constructor
- jh
- .updateMatrix
- Hn
- ml
- numpy
- look.py
- Sc
- hp
- qs
- od
- yr
- ap
- nl
- .parse
- s
- tu
- qh
- package.json
- up
- numpy
- Zh
- .constructor
- da
- om
- Dh
- eq.py
- $h
- .parseObject
- im
- .setHSL
- mu
- zp
- gh
- es
- wh
- kh
- estimate_drift
- t
- MIX3D
- xs
- .constructor
- ya
- MIX3D::ProcessBlock
- Hu
- $l
- Spazi 3D
- Ci
- dp
- Ph
- Gu
- ba
- Rh
- Compatibilità
- Yu
- Zc
- Qp
- .bind
- Xu
- build_macos.sh
- build_plugin.sh
- Fh
- Ih
- Lh
- il
- Oh
- Uh
- zl
- rm
- EMsgTags
- za
- qu
- EParams

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

## Communities (161 total, 84 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.05
Nodes (12): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_posizione_del_plugin_in_fairlight() (+4 more)

### Community 1 - "media.py"
Cohesion: 0.11
Nodes (15): audio_streams(), banner(), blocks(), ffmpeg(), _ffmpeg_read(), _graph(), native(), NoAudio (+7 more)

### Community 2 - "hh"
Cohesion: 0.20
Nodes (3): dd, hh, wm

### Community 3 - "metadata.py"
Cohesion: 0.11
Nodes (13): _bcd_tc(), detect(), qt_strings(), read(), sony_xml(), tags(), _txt(), wav() (+5 more)

### Community 4 - "cli.py"
Cohesion: 0.10
Nodes (20): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+12 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.08
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.05
Nodes (93): api(), audible(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color() (+85 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.13
Nodes (6): Clock, HttpGet(), MIX3D::MIX3D(), Num(), ParseWav(), Run()

### Community 8 - "devices.py"
Cohesion: 0.16
Nodes (11): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+3 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 10 - "server.py"
Cohesion: 0.07
Nodes (23): apply_profile(), browse(), eq_curve(), estimate_space(), Handler, host_time(), job_eq_auto(), join_tracks() (+15 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 16 - "ta"
Cohesion: 0.05
Nodes (10): em, Gl, jl, Ka, A(), C(), R(), ta (+2 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.13
Nodes (3): Ku, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.21
Nodes (6): app_bundle(), arch(), check(), download(), install(), parse()

### Community 25 - "Kr"
Cohesion: 0.08
Nodes (3): fi(), gi(), Kr

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 27 - "As"
Cohesion: 0.06
Nodes (8): Am, As, ma, nu, pu, ru, td, ym()

### Community 28 - "bd"
Cohesion: 0.06
Nodes (10): ad, bd, ed(), md(), Md, pd(), rd, sd (+2 more)

### Community 29 - "eu"
Cohesion: 0.13
Nodes (3): eu, iu, xm

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

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
Cohesion: 0.12
Nodes (9): ai(), bi, ci(), nc, oi(), ph, rh, uh (+1 more)

### Community 42 - "$n"
Cohesion: 0.14
Nodes (3): $n(), rs(), _s

### Community 45 - "Nh"
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - ".constructor"
Cohesion: 0.08
Nodes (32): hl(), j(), K(), q(), W(), Ft(), Jt(), kt() (+24 more)

### Community 48 - "bt"
Cohesion: 0.11
Nodes (13): Ga(), ii(), ja(), bt(), Rt(), ka(), kl(), pa() (+5 more)

### Community 50 - "mixer.py"
Cohesion: 0.08
Nodes (18): Stato: F0 (fondamenta), auto_positions(), estimate_sources(), locate(), same_clock_distances(), spatial_params(), active(), correction_fir() (+10 more)

### Community 53 - "ts"
Cohesion: 0.15
Nodes (3): fl, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 56 - "ec"
Cohesion: 0.12
Nodes (4): ec, Mi(), Xn(), yi

### Community 57 - "kd"
Cohesion: 0.12
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): id, Mh, rc, ud

### Community 62 - ".copy"
Cohesion: 0.16
Nodes (3): cd, vc, xc()

### Community 63 - "xh"
Cohesion: 0.27
Nodes (3): bm, fm, xh

### Community 65 - "MIX3D"
Cohesion: 0.14
Nodes (11): MIX3D, kRing, mBase, mEnd, mFeed, mPlay, mPos, mReady (+3 more)

### Community 67 - "wi"
Cohesion: 0.13
Nodes (8): Ea(), ia, li, pi, ra, ri, wi, S()

### Community 68 - "ld"
Cohesion: 0.16
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.12
Nodes (3): lm, na, zm

### Community 70 - "analysis.py"
Cohesion: 0.15
Nodes (6): analyze(), db(), k_weighting(), Loudness, rt60_from_decays(), warnings()

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

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
Cohesion: 0.21
Nodes (13): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+5 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 85 - "qs"
Cohesion: 0.15
Nodes (7): qs, p(), xa(), g(), d(), Ys(), Zs()

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

### Community 98 - "numpy"
Cohesion: 0.08
Nodes (27): clock_key(), cluster_sources(), distance_from_ir(), excerpt(), frame_gcc(), images(), impulse_response(), read_aligned() (+19 more)

### Community 100 - ".constructor"
Cohesion: 0.22
Nodes (3): ju, lu, ou

### Community 101 - "da"
Cohesion: 0.33
Nodes (5): _d(), da(), r(), Id(), n

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 107 - ".parseObject"
Cohesion: 0.07
Nodes (7): ip, jd, lp, op, qd, rp, tc

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 112 - "gh"
Cohesion: 0.13
Nodes (4): au, gh, Gm, su

### Community 113 - "es"
Cohesion: 0.16
Nodes (4): es, Mm, Tm, Zu

### Community 117 - "estimate_drift"
Cohesion: 0.12
Nodes (13): _coarse(), sync_pair(), align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays() (+5 more)

### Community 118 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 119 - "MIX3D"
Cohesion: 0.17
Nodes (9): F0: verifiche su Resolve reale [V], App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti (+1 more)

### Community 122 - "ya"
Cohesion: 0.27
Nodes (7): v(), ya(), f(), g(), u(), x(), y()

### Community 126 - "Spazi 3D"
Cohesion: 0.50
Nodes (3): Preset inclusi, Spazi 3D, Spazi privati (file)

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 133 - "Compatibilità"
Cohesion: 0.29
Nodes (7): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati

### Community 139 - ".bind"
Cohesion: 0.33
Nodes (3): bind(), getValue(), setValue()

### Community 150 - "il"
Cohesion: 0.25
Nodes (3): il, A(), ol()

### Community 153 - "zl"
Cohesion: 0.18
Nodes (6): Fl, Ma(), zl(), b(), E(), T()

### Community 156 - "rm"
Cohesion: 0.32
Nodes (3): am(), rm, sm()

### Community 161 - "EMsgTags"
Cohesion: 0.67
Nodes (3): EMsgTags, kMsgLaunch, kMsgOpenBrowser

### Community 162 - "za"
Cohesion: 0.22
Nodes (6): Ai, Ha(), qa(), Ri, Va(), za()

### Community 164 - "EParams"
Cohesion: 0.67
Nodes (3): EParams, kListen, kNumParams

## Knowledge Gaps
- **15 isolated node(s):** `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser`, `kListen`, `kNumParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1203 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **84 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Compatibilità` connect `Compatibilità` to `devices.py`, `da`?**
  _High betweenness centrality (0.304) - this node is a cross-community bridge._
- **What connects `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05391120507399577 - nodes in this community are weakly interconnected._
- **Why does `da()` connect `da` to `ta`, `three.module.min.js`, `Compatibilità`, `.constructor`?**
  _High betweenness centrality (0.303) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `Compatibilità`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Should `metadata.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11182795698924732 - nodes in this community are weakly interconnected._