# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 50 files · ~80,504 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2839 nodes · 5100 edges · 174 communities (74 shown, 100 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 206 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6997c437`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- media.py
- server.py
- devices.py
- cli.py
- test_ui_engine.py
- app.js
- MIX3D.cpp
- metadata.py
- three.module.min.js
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
- vl
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
- xr
- .copy
- xh
- Fc
- MIX3D
- pm
- wi
- ld
- gh
- hh
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
- spazi.py
- od
- yr
- ap
- nl
- .parse
- s
- tu
- resolve_bridge.py
- package.json
- up
- test_eq.py
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
- _TL
- es
- wh
- .constructor
- analysis.py
- t
- MIX3D
- xs
- jn
- geometry.py
- .constructor
- Hu
- .parseObject
- README.md
- Ci
- dp
- Ph
- lm
- yh
- Rh
- _Item
- _Project
- Zc
- Qp
- _FakeTimeline
- jh
- Xu
- build_macos.sh
- build_plugin.sh
- hl
- rp
- Fh
- Ih
- Lh
- il
- Oh
- Uh
- zl
- rm
- Li
- hp
- EMsgTags
- mp
- qh
- EParams
- hd
- vc
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

## Communities (174 total, 100 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.13
Nodes (8): reimport_wav(), _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_posizione_del_plugin_in_fairlight(), test_read_audio_clips(), test_reimport_adds_new_track_only(), test_sync_a_catena_parte_da_resolve(), test_timeline_from_resolve_script_replaces_previous()

### Community 1 - "media.py"
Cohesion: 0.11
Nodes (14): audio_streams(), banner(), blocks(), ffmpeg(), _ffmpeg_read(), _graph(), native(), NoAudio (+6 more)

### Community 2 - "server.py"
Cohesion: 0.07
Nodes (21): auto_positions(), apply_profile(), auto_place(), browse(), eq_curve(), estimate_space(), Handler, host_time() (+13 more)

### Community 3 - "devices.py"
Cohesion: 0.22
Nodes (7): chain_risks(), compat(), compat_matrix(), load(), _powered(), profile(), suggest()

### Community 4 - "cli.py"
Cohesion: 0.21
Nodes (9): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), connect() (+1 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.10
Nodes (4): concert(), _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati()

### Community 6 - "app.js"
Cohesion: 0.05
Nodes (95): api(), audible(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color() (+87 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.12
Nodes (7): Clock, HttpGet(), MIX3D::MIX3D(), MIX3D::ProcessBlock(), Num(), ParseWav(), Run()

### Community 8 - "metadata.py"
Cohesion: 0.08
Nodes (20): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, _bcd_tc() (+12 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (163): _a, aa, ac, ah, ao, ar, bh, Bi (+155 more)

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 14 - "Yp"
Cohesion: 0.08
Nodes (3): constructor(), setValue(), Yp

### Community 18 - "cs"
Cohesion: 0.07
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.07
Nodes (9): Ku, ma, nu, pu, ru, td, $u, vs (+1 more)

### Community 21 - "updater.py"
Cohesion: 0.21
Nodes (6): app_bundle(), arch(), check(), download(), install(), parse()

### Community 26 - "Nr"
Cohesion: 0.08
Nodes (4): gm, np, Nr, uc

### Community 28 - "bd"
Cohesion: 0.08
Nodes (8): bd, ed(), md(), Md, pd(), rd, xd, yd

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 33 - "Oa"
Cohesion: 0.13
Nodes (7): Ai, Ha(), Oa, qa(), Ri, Va(), za()

### Community 35 - "e"
Cohesion: 0.12
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
Cohesion: 0.11
Nodes (11): ai(), bi, ci(), fi(), ia, nc, oi(), ph (+3 more)

### Community 42 - "$n"
Cohesion: 0.13
Nodes (3): $n(), rs(), _s

### Community 45 - "Nh"
Cohesion: 0.17
Nodes (4): dh, _h, Nh, zh

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.10
Nodes (14): ba(), Ga(), ii(), ja(), bt(), Rt(), ka(), kl() (+6 more)

### Community 50 - "mixer.py"
Cohesion: 0.09
Nodes (16): asciuga(), compress(), impulse(), Reverb, reverb(), ruolo(), settings(), spatial_params() (+8 more)

### Community 53 - "ts"
Cohesion: 0.15
Nodes (3): fl, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.14
Nodes (3): Gd, o(), kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): dd, id, Mh, rc

### Community 63 - "xh"
Cohesion: 0.18
Nodes (4): bm, fm, wm, xh

### Community 65 - "MIX3D"
Cohesion: 0.14
Nodes (11): MIX3D, kRing, mBase, mEnd, mFeed, mPlay, mPos, mReady (+3 more)

### Community 67 - "wi"
Cohesion: 0.13
Nodes (9): Ea(), Fa(), li, pi, ra, ri, wi, Ys() (+1 more)

### Community 68 - "ld"
Cohesion: 0.21
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.12
Nodes (4): au, gh, Gm, su

### Community 70 - "hh"
Cohesion: 0.13
Nodes (5): Am, Bm, hh, ym(), zm

### Community 72 - "nm"
Cohesion: 0.24
Nodes (4): Dm(), nm, a(), o()

### Community 74 - "eq.js"
Cohesion: 0.17
Nodes (30): api(), auto(), bands, css(), cut(), dbl(), down(), draw() (+22 more)

### Community 75 - ".constructor"
Cohesion: 0.11
Nodes (5): Gu, lu, ou, a(), o()

### Community 78 - "Hn"
Cohesion: 0.18
Nodes (5): as, Hn, nr, _p, ql

### Community 79 - "ml"
Cohesion: 0.20
Nodes (10): cl(), dl(), gl(), ll(), ml(), rl(), ul(), yl() (+2 more)

### Community 80 - "numpy"
Cohesion: 0.11
Nodes (24): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+16 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 85 - "qs"
Cohesion: 0.12
Nodes (12): v(), qs, p(), xa(), g(), ya(), d(), f() (+4 more)

### Community 86 - "spazi.py"
Cohesion: 0.23
Nodes (8): all_spaces(), builtin(), critical_distance(), get(), import_file(), local(), normalize(), _fetch_json()

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.25
Nodes (5): s(), r(), i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 95 - "resolve_bridge.py"
Cohesion: 0.20
Nodes (6): AudioClip, clear_range(), current_timeline(), _fusionscript(), mix3d_track(), read_audio_clips()

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 98 - "test_eq.py"
Cohesion: 0.33
Nodes (7): _bp(), test_auto_taratura(), test_banda_dinamica_agisce_solo_sopra_soglia(), test_curva_uguale_al_filtro(), test_look_master(), test_master_continuo_e_auto(), _track()

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 107 - ".parseObject"
Cohesion: 0.12
Nodes (4): jd, lp, op, qd

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 110 - "mu"
Cohesion: 0.18
Nodes (4): da(), r(), mu, n

### Community 113 - "es"
Cohesion: 0.22
Nodes (3): es, Mm, Zu

### Community 115 - ".constructor"
Cohesion: 0.16
Nodes (6): Ft(), Jt(), kt(), Qt(), Yt(), zt()

### Community 117 - "analysis.py"
Cohesion: 0.07
Nodes (21): Stato: F0 (fondamenta), analyze(), _coarse(), db(), k_weighting(), Loudness, rt60_from_decays(), sync_pair() (+13 more)

### Community 118 - "t"
Cohesion: 0.27
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 119 - "MIX3D"
Cohesion: 0.25
Nodes (8): App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti, Uso

### Community 122 - "geometry.py"
Cohesion: 0.25
Nodes (3): estimate_sources(), locate(), same_clock_distances()

### Community 123 - ".constructor"
Cohesion: 0.22
Nodes (5): Gl, Ka, A(), C(), R()

### Community 126 - "README.md"
Cohesion: 0.25
Nodes (4): F0: verifiche su Resolve reale [V], Preset inclusi, Spazi 3D, Spazi privati (file)

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 138 - "_FakeTimeline"
Cohesion: 0.25
Nodes (3): region(), _FakeTimeline, test_regione_da_marker_o_inout()

### Community 143 - "hl"
Cohesion: 0.29
Nodes (6): hl(), j(), K(), q(), W(), Ma()

### Community 150 - "il"
Cohesion: 0.25
Nodes (3): il, A(), ol()

### Community 153 - "zl"
Cohesion: 0.22
Nodes (6): Fl, zl(), b(), E(), S(), T()

### Community 156 - "rm"
Cohesion: 0.32
Nodes (3): am(), rm, sm()

### Community 161 - "EMsgTags"
Cohesion: 0.67
Nodes (3): EMsgTags, kMsgLaunch, kMsgOpenBrowser

### Community 164 - "EParams"
Cohesion: 0.67
Nodes (3): EParams, kListen, kNumParams

## Knowledge Gaps
- **15 isolated node(s):** `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser`, `kListen`, `kNumParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1203 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **100 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Compatibilità` connect `metadata.py` to `devices.py`, `mu`?**
  _High betweenness centrality (0.292) - this node is a cross-community bridge._
- **What connects `mix3d`, `kMsgLaunch`, `kMsgOpenBrowser` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._
- **Why does `da()` connect `mu` to `metadata.py`, `three.module.min.js`, `.constructor`, `.constructor`?**
  _High betweenness centrality (0.292) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10960960960960961 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `metadata.py`?**
  _High betweenness centrality (0.233) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0666049953746531 - nodes in this community are weakly interconnected._