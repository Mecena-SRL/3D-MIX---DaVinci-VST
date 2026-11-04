# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 48 files · ~73,260 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2741 nodes · 4896 edges · 161 communities (63 shown, 98 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 195 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6a6a1a92`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- media.py
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
- Wa
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
- .toJSON
- .copy
- xh
- Fc
- mixer.py
- pm
- vl
- ld
- gh
- analysis.py
- bl
- nm
- ua
- eq.js
- Gu
- iu
- .updateMatrix
- Hn
- ml
- numpy
- look.py
- Sc
- na
- qs
- hh
- od
- ap
- nl
- .parse
- s
- tu
- lm
- package.json
- up
- yh
- Zh
- .constructor
- jh
- om
- Dh
- eq.py
- $h
- .parseObject
- im
- .setHSL
- mu
- zp
- su
- es
- wh
- hp
- estimate_drift
- wi
- qh
- xs
- .bind
- hd
- Hu
- $l
- Ci
- dp
- Ph
- kh
- qu
- Rh
- tc
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
- da

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

## Communities (161 total, 98 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.06
Nodes (10): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+2 more)

### Community 1 - "media.py"
Cohesion: 0.10
Nodes (15): suggest(), banner(), blocks(), decoded(), ffmpeg(), probe(), detect(), install() (+7 more)

### Community 2 - "server.py"
Cohesion: 0.10
Nodes (11): browse(), eq_curve(), Handler, job_eq_auto(), join_tracks(), new_project(), public_state(), split_track() (+3 more)

### Community 3 - "media.py"
Cohesion: 0.14
Nodes (10): _bcd_tc(), read(), sony_xml(), tags(), _txt(), wav(), _wav_chunks(), bwf() (+2 more)

### Community 4 - "cli.py"
Cohesion: 0.10
Nodes (20): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+12 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.08
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.06
Nodes (78): api(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color(), COLORS (+70 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.05
Nodes (29): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, F0: verifiche su Resolve reale [V] (+21 more)

### Community 8 - "devices.py"
Cohesion: 0.11
Nodes (13): chain_risks(), compat(), compat_matrix(), load(), _powered(), profile(), apply_profile(), all_spaces() (+5 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (159): _a, aa, ac, ah, ao, ar, bh, Bi (+151 more)

### Community 10 - "ta"
Cohesion: 0.06
Nodes (11): Gl, il, Ka, A(), ol(), A(), C(), R() (+3 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 16 - "jl"
Cohesion: 0.13
Nodes (3): em, jl, Wl

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.08
Nodes (8): Ku, ma, nu, pu, ru, td, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.20
Nodes (7): app_bundle(), arch(), check(), download(), _fetch_json(), install(), parse()

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 28 - "bd"
Cohesion: 0.06
Nodes (10): ad, bd, ed(), md(), Md, pd(), rd, sd (+2 more)

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 33 - "Oa"
Cohesion: 0.06
Nodes (22): Ai, v(), Fa(), Fl, Ha(), Oa, qa(), p() (+14 more)

### Community 35 - "e"
Cohesion: 0.10
Nodes (12): t(), e, n(), c(), l(), o(), a(), Vd (+4 more)

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
Cohesion: 0.09
Nodes (12): ai(), bi, ci(), fi(), ia, ka(), nc, oi() (+4 more)

### Community 42 - "$n"
Cohesion: 0.14
Nodes (3): $n(), rs(), _s

### Community 43 - "lr"
Cohesion: 0.07
Nodes (5): am(), lr, rm, sm(), yr

### Community 45 - "Nh"
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - ".constructor"
Cohesion: 0.06
Nodes (26): ba(), Ga(), hl(), j(), K(), q(), W(), ja() (+18 more)

### Community 48 - "Wa"
Cohesion: 0.50
Nodes (3): ii(), Wa(), o()

### Community 50 - "mixer.py"
Cohesion: 0.13
Nodes (9): _coarse(), sync_pair(), auto_positions(), estimate_sources(), locate(), same_clock_distances(), read(), auto_place() (+1 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, mh, rc, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 56 - "ec"
Cohesion: 0.10
Nodes (4): ec, Mi(), Xn(), yi

### Community 57 - "kd"
Cohesion: 0.17
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.11
Nodes (5): cd, dd, id, Mh, ud

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - "mixer.py"
Cohesion: 0.18
Nodes (7): spatial_params(), active(), envelope_db(), is_line(), print_mix(), render(), span()

### Community 67 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.14
Nodes (3): gh, Gm, zm

### Community 70 - "analysis.py"
Cohesion: 0.15
Nodes (5): analyze(), db(), k_weighting(), Loudness, warnings()

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
Cohesion: 0.12
Nodes (25): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+17 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 86 - "hh"
Cohesion: 0.17
Nodes (4): Am, Bm, hh, ym()

### Community 91 - "nl"
Cohesion: 0.20
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

### Community 100 - ".constructor"
Cohesion: 0.12
Nodes (6): ju, lu, ou, a(), o(), Tm

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 107 - ".parseObject"
Cohesion: 0.08
Nodes (6): ip, jd, lp, op, qd, rp

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 113 - "es"
Cohesion: 0.22
Nodes (3): es, Mm, Zu

### Community 117 - "estimate_drift"
Cohesion: 0.16
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 118 - "wi"
Cohesion: 0.13
Nodes (9): Ea(), li, pi, ra, ri, wi, Ys(), S() (+1 more)

### Community 121 - ".bind"
Cohesion: 0.33
Nodes (3): bind(), getValue(), setValue()

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 159 - "da"
Cohesion: 0.33
Nodes (5): _d(), da(), r(), Id(), n

## Knowledge Gaps
- **4 isolated node(s):** `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser`, `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1159 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **98 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `da()` connect `da` to `three.module.min.js`, `ta`, `.constructor`, `MIX3D.cpp`?**
  _High betweenness centrality (0.280) - this node is a cross-community bridge._
- **What connects `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06025641025641026 - nodes in this community are weakly interconnected._
- **Why does `Compatibilità` connect `MIX3D.cpp` to `devices.py`, `da`?**
  _High betweenness centrality (0.280) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0953058321479374 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `MIX3D.cpp`?**
  _High betweenness centrality (0.267) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0989247311827957 - nodes in this community are weakly interconnected._