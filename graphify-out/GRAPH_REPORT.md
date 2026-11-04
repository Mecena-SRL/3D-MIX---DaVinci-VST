# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 48 files · ~75,373 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2774 nodes · 4985 edges · 159 communities (68 shown, 91 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 204 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e547a205`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- blocks
- .do_POST
- media.py
- cli.py
- test_ui_engine.py
- app.js
- MIX3D.cpp
- devices.py
- three.module.min.js
- cli.py
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
- ta
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
- render
- pm
- vl
- ld
- gh
- server.py
- bl
- nm
- ua
- eq.js
- .constructor
- iu
- .updateMatrix
- Hn
- ml
- numpy
- look.py
- Sc
- na
- qs
- _TL
- od
- ap
- nl
- .parse
- s
- tu
- lm
- package.json
- up
- _Item
- Zh
- .constructor
- em
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
- xs
- .constructor
- Hu
- $l
- vs
- Ci
- dp
- Ph
- Gu
- test_ingressi.py
- Rh
- Yu
- Zc
- Qp
- MIX3D
- Compatibilità
- Xu
- build_macos.sh
- build_plugin.sh
- Fh
- Ih
- Lh
- rp
- Oh
- Uh
- MIX3D.h
- README.md

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
- `F0: verifiche su Resolve reale [V]` --references--> `MIX3D`  [INFERRED]
  docs/F0_verifiche.md → plugin/MIX3D/MIX3D.h
- `Riconoscimento dai metadati` --references--> `detect()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/metadata.py
- `MIX3D` --references--> `MIX3D`  [INFERRED]
  README.md → plugin/MIX3D/MIX3D.h
- `Compatibilità` --references--> `compat()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/devices.py
- `Compatibilità` --references--> `da()`  [INFERRED]
  docs/database_dispositivi.md → src/mix3d/web/vendor/three.module.min.js

## Import Cycles
- None detected.

## Communities (159 total, 91 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.12
Nodes (7): _PM, _Project, _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_read_audio_clips(), test_reimport_adds_new_track_only(), test_timeline_from_resolve_script_replaces_previous()

### Community 1 - "blocks"
Cohesion: 0.15
Nodes (8): blocks(), ffmpeg(), _graph(), NoAudio, install(), install_fairlight(), refresh_script(), status()

### Community 2 - ".do_POST"
Cohesion: 0.11
Nodes (13): Handler, join_tracks(), new_project(), public_state(), split_track(), all_spaces(), builtin(), critical_distance() (+5 more)

### Community 3 - "media.py"
Cohesion: 0.10
Nodes (14): audio_streams(), banner(), probe(), _bcd_tc(), detect(), read(), sony_xml(), tags() (+6 more)

### Community 4 - "cli.py"
Cohesion: 0.13
Nodes (11): AudioClip, clear_range(), connect(), current_timeline(), _fusionscript(), mix3d_track(), read_audio_clips(), region() (+3 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.09
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.05
Nodes (93): api(), audible(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color() (+85 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.20
Nodes (3): MIX3D::MIX3D(), MIX3D::ProcessBlock(), Run()

### Community 8 - "devices.py"
Cohesion: 0.14
Nodes (13): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+5 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 10 - "cli.py"
Cohesion: 0.22
Nodes (9): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), export_otio() (+1 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.08
Nodes (3): constructor(), setValue(), Yp

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 19 - "Ii"
Cohesion: 0.05
Nodes (5): Ii, il, A(), ol(), xr

### Community 20 - "vs"
Cohesion: 0.08
Nodes (6): Ku, ma, nu, qu, ru, $u

### Community 21 - "updater.py"
Cohesion: 0.18
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
Cohesion: 0.13
Nodes (8): Ai, Fa(), Ha(), Oa, qa(), Ri, Va(), za()

### Community 35 - "e"
Cohesion: 0.11
Nodes (7): e, hd, a(), Vd, c(), xp, zd

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
Nodes (13): ai(), bi, ci(), fi(), Gd, o(), ia, nc (+5 more)

### Community 42 - "$n"
Cohesion: 0.13
Nodes (3): $n(), rs(), _s

### Community 43 - "lr"
Cohesion: 0.07
Nodes (5): am(), lr, rm, sm(), yr

### Community 45 - "Nh"
Cohesion: 0.06
Nodes (10): dh, _h, jh, kh, Nh, qh, Wh(), Xh() (+2 more)

### Community 47 - ".constructor"
Cohesion: 0.08
Nodes (18): hl(), j(), K(), q(), W(), Ft(), Jt(), kt() (+10 more)

### Community 48 - "bt"
Cohesion: 0.06
Nodes (21): ba(), Ea(), Ga(), ii(), ja(), bt(), Rt(), ka() (+13 more)

### Community 50 - "mixer.py"
Cohesion: 0.10
Nodes (13): _coarse(), sync_pair(), auto_positions(), estimate_sources(), locate(), same_clock_distances(), _ffmpeg_read(), read() (+5 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, mh, ts, ud

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 56 - "ec"
Cohesion: 0.11
Nodes (4): ec, Mi(), Xn(), yi

### Community 60 - ".setValues"
Cohesion: 0.11
Nodes (5): cd, dd, id, Mh, rc

### Community 61 - "t"
Cohesion: 0.27
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 63 - "xh"
Cohesion: 0.27
Nodes (3): bm, fm, xh

### Community 65 - "render"
Cohesion: 0.29
Nodes (4): envelope_db(), is_line(), render(), load()

### Community 67 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 68 - "ld"
Cohesion: 0.12
Nodes (6): _d(), fd(), gd(), Id(), ld, wd

### Community 70 - "server.py"
Cohesion: 0.06
Nodes (14): analyze(), db(), k_weighting(), Loudness, rt60_from_decays(), warnings(), spatial_params(), native() (+6 more)

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 73 - "ua"
Cohesion: 0.11
Nodes (6): Fl, ua, zl(), b(), E(), T()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - ".constructor"
Cohesion: 0.18
Nodes (4): lu, ou, a(), o()

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.13
Nodes (24): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+16 more)

### Community 81 - "look.py"
Cohesion: 0.27
Nodes (10): apply(), _car(), catalog(), character_db(), character_fir(), characters(), curve(), get() (+2 more)

### Community 85 - "qs"
Cohesion: 0.12
Nodes (10): v(), qs, p(), ya(), d(), f(), g(), u() (+2 more)

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

### Community 105 - "eq.py"
Cohesion: 0.23
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), process(), response_db(), _sos_cut(), eq_curve()

### Community 107 - ".parseObject"
Cohesion: 0.09
Nodes (5): jd, lp, op, qd, tc

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 113 - "es"
Cohesion: 0.20
Nodes (3): es, Mm, Zu

### Community 117 - "estimate_drift"
Cohesion: 0.15
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 123 - ".constructor"
Cohesion: 0.22
Nodes (5): Gl, Ka, A(), C(), R()

### Community 126 - "vs"
Cohesion: 0.09
Nodes (9): Am, Bm, hh, pu, td, vs, wm, ym() (+1 more)

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 131 - "test_ingressi.py"
Cohesion: 0.60
Nodes (3): _project(), test_dual_mono_goes_left_right_and_line_ignores_distance(), test_split_and_join()

### Community 138 - "MIX3D"
Cohesion: 0.22
Nodes (9): App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti, Stato: F0 (fondamenta) (+1 more)

### Community 139 - "Compatibilità"
Cohesion: 0.20
Nodes (10): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, da() (+2 more)

### Community 153 - "MIX3D.h"
Cohesion: 0.22
Nodes (6): EMsgTags, kMsgLaunch, kMsgOpenBrowser, EParams, kNumParams, MIX3D

### Community 156 - "README.md"
Cohesion: 0.25
Nodes (4): F0: verifiche su Resolve reale [V], Preset inclusi, Spazi 3D, Spazi privati (file)

## Knowledge Gaps
- **4 isolated node(s):** `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser`, `kNumParams`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1167 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **91 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Compatibilità` connect `Compatibilità` to `devices.py`?**
  _High betweenness centrality (0.273) - this node is a cross-community bridge._
- **What connects `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12105263157894737 - nodes in this community are weakly interconnected._
- **Why does `da()` connect `Compatibilità` to `three.module.min.js`, `.constructor`, `.constructor`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Should `.do_POST` be split into smaller, more focused modules?**
  _Cohesion score 0.10826210826210826 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `Compatibilità`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10483870967741936 - nodes in this community are weakly interconnected._