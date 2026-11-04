# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-04)

## Corpus Check
- 48 files · ~78,187 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .plist 4, (none) 1, .xib 1)

## Summary
- 2807 nodes · 5031 edges · 167 communities (78 shown, 89 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 206 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `19047283`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_resolve_bridge.py
- media.py
- server.py
- test_metadata.py
- cli.py
- test_ui_engine.py
- app.js
- MIX3D.cpp
- devices.py
- three.module.min.js
- .do_GET
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
- analysis.py
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
- xd
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
- su
- es
- wh
- .constructor
- estimate_drift
- t
- MIX3D
- xs
- jn
- ya
- .constructor
- Hu
- $l
- README.md
- Ci
- dp
- Ph
- Gu
- test_ingressi.py
- Rh
- Compatibilità
- Yu
- Zc
- Qp
- resolve_install.py
- n
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
- EMsgTags
- Ai
- qu
- EParams
- wp

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
- `Stato: F0 (fondamenta)` --references--> `sync()`  [INFERRED]
  README.md → src/mix3d/server.py

## Import Cycles
- None detected.

## Communities (167 total, 89 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.05
Nodes (12): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_clip_raggruppate_per_canale_di_resolve(), test_posizione_del_plugin_in_fairlight() (+4 more)

### Community 1 - "media.py"
Cohesion: 0.13
Nodes (12): _coarse(), sync_pair(), audio_streams(), banner(), blocks(), ffmpeg(), _ffmpeg_read(), _graph() (+4 more)

### Community 2 - "server.py"
Cohesion: 0.14
Nodes (11): apply_profile(), auto_place(), estimate_space(), import_resolve(), job_analyze(), join_tracks(), new_project(), serve() (+3 more)

### Community 3 - "test_metadata.py"
Cohesion: 0.25
Nodes (3): bwf(), chunk(), test_bwf_tascam()

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (18): cmd_info(), cmd_install_resolve(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip (+10 more)

### Community 5 - "test_ui_engine.py"
Cohesion: 0.09
Nodes (6): concert(), _FakeTimeline, _music(), test_file_video_aac(), test_mxf_canali_in_stream_separati(), test_regione_da_marker_o_inout()

### Community 6 - "app.js"
Cohesion: 0.05
Nodes (93): api(), audible(), barChart(), browse(), CAMERAS, chainRisks(), checkUpdate(), color() (+85 more)

### Community 7 - "MIX3D.cpp"
Cohesion: 0.12
Nodes (7): Clock, HttpGet(), MIX3D::MIX3D(), MIX3D::ProcessBlock(), Num(), ParseWav(), Run()

### Community 8 - "devices.py"
Cohesion: 0.09
Nodes (19): chain_risks(), compat(), compat_matrix(), correction_db(), load(), polar_gain(), _powered(), profile() (+11 more)

### Community 9 - "three.module.min.js"
Cohesion: 0.01
Nodes (161): _a, aa, ac, ah, ao, ar, bh, Bi (+153 more)

### Community 10 - ".do_GET"
Cohesion: 0.12
Nodes (7): eq_curve(), Handler, host_time(), public_state(), wav_bytes(), critical_distance(), test_api_http()

### Community 13 - ".constructor"
Cohesion: 0.09
Nodes (39): OrbitControls, addPointer(), dollyIn(), dollyOut(), getSecondPointerPosition(), getZoomScale(), handleKeyDown(), handleMouseDownDolly() (+31 more)

### Community 18 - "cs"
Cohesion: 0.06
Nodes (9): bc, cs, ds, fs, gs, hs, ms, ps (+1 more)

### Community 20 - "vs"
Cohesion: 0.13
Nodes (3): Ku, $u, vs

### Community 21 - "updater.py"
Cohesion: 0.17
Nodes (8): browse(), app_bundle(), arch(), check(), download(), _fetch_json(), install(), parse()

### Community 25 - "Kr"
Cohesion: 0.07
Nodes (3): fi(), gi(), Kr

### Community 26 - "Nr"
Cohesion: 0.07
Nodes (4): gm, np, Nr, uc

### Community 27 - "As"
Cohesion: 0.09
Nodes (5): As, nu, pu, ru, td

### Community 28 - "bd"
Cohesion: 0.12
Nodes (5): bd, ed(), Md, pd(), rd

### Community 32 - "steps"
Cohesion: 0.06
Nodes (37): needs, runs-on, steps, strategy, release, jobs, dmg, plugin (+29 more)

### Community 33 - "Oa"
Cohesion: 0.17
Nodes (6): Fa(), Ha(), Oa, qa(), Va(), za()

### Community 35 - "e"
Cohesion: 0.08
Nodes (10): _d(), e, hd, Id(), a(), Vd, c(), wd (+2 more)

### Community 36 - "fp"
Cohesion: 0.15
Nodes (5): fp, Mi(), Nc, Nd, yi

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
Cohesion: 0.13
Nodes (3): $n(), rs(), _s

### Community 45 - "Nh"
Cohesion: 0.06
Nodes (10): dh, _h, jh, kh, Nh, qh, Wh(), Xh() (+2 more)

### Community 47 - "vl"
Cohesion: 0.23
Nodes (20): vl(), b(), D(), E(), f(), g(), I(), L() (+12 more)

### Community 48 - "bt"
Cohesion: 0.08
Nodes (16): ba(), Ea(), Ga(), ii(), ja(), bt(), Rt(), ka() (+8 more)

### Community 50 - "mixer.py"
Cohesion: 0.10
Nodes (12): auto_positions(), estimate_sources(), locate(), spatial_params(), active(), correction_fir(), envelope_db(), is_line() (+4 more)

### Community 53 - "ts"
Cohesion: 0.12
Nodes (4): fl, id, mh, ts

### Community 54 - "main.js"
Cohesion: 0.27
Nodes (7): { app, BrowserWindow }, createWindow(), { execFile }, http, isUp(), load(), page()

### Community 57 - "kd"
Cohesion: 0.11
Nodes (4): Gd, o(), ia, kd

### Community 60 - ".setValues"
Cohesion: 0.13
Nodes (4): dd, Fl, Mh, rc

### Community 62 - ".copy"
Cohesion: 0.13
Nodes (4): cd, ud, vc, xc()

### Community 63 - "xh"
Cohesion: 0.09
Nodes (8): Am, bm, Bm, fm, hh, wm, xh, ym()

### Community 65 - "MIX3D"
Cohesion: 0.14
Nodes (11): MIX3D, kRing, mBase, mEnd, mFeed, mPlay, mPos, mReady (+3 more)

### Community 67 - "wi"
Cohesion: 0.33
Nodes (5): li, pi, ri, wi, S()

### Community 68 - "ld"
Cohesion: 0.19
Nodes (3): fd(), gd(), ld

### Community 69 - "gh"
Cohesion: 0.10
Nodes (4): gh, Gm, lm, zm

### Community 70 - "analysis.py"
Cohesion: 0.14
Nodes (7): analyze(), db(), k_weighting(), Loudness, rt60_from_decays(), warnings(), one()

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
Cohesion: 0.23
Nodes (14): balance(), _band(), masking(), resonances(), room(), run(), run_master(), segments() (+6 more)

### Community 81 - "look.py"
Cohesion: 0.24
Nodes (11): apply(), _car(), catalog(), character_db(), character_fir(), characters(), compress(), curve() (+3 more)

### Community 85 - "qs"
Cohesion: 0.10
Nodes (10): v(), es, ma, qs, p(), xa(), g(), d() (+2 more)

### Community 86 - "spazi.py"
Cohesion: 0.29
Nodes (6): all_spaces(), builtin(), get(), import_file(), local(), normalize()

### Community 91 - "nl"
Cohesion: 0.22
Nodes (5): el(), Ko, nl(), $o, Qo

### Community 92 - ".parse"
Cohesion: 0.17
Nodes (6): s(), r(), mp, i(), pp, si()

### Community 93 - "s"
Cohesion: 0.36
Nodes (7): s(), B(), H(), O(), P(), V(), z()

### Community 95 - "xd"
Cohesion: 0.17
Nodes (4): md(), sd, xd, yd

### Community 96 - "package.json"
Cohesion: 0.50
Nodes (3): main, name, version

### Community 98 - "test_eq.py"
Cohesion: 0.29
Nodes (7): _bp(), test_auto_taratura(), test_banda_dinamica_agisce_solo_sopra_soglia(), test_curva_uguale_al_filtro(), test_look_master(), test_master_continuo_e_auto(), _track()

### Community 100 - ".constructor"
Cohesion: 0.17
Nodes (4): ju, lu, ou, Tm

### Community 105 - "eq.py"
Cohesion: 0.24
Nodes (8): _ap1(), _ap2(), component(), dyn_gain_db(), level_db(), process(), response_db(), _sos_cut()

### Community 107 - ".parseObject"
Cohesion: 0.07
Nodes (6): hp, jd, lp, op, qd, tc

### Community 109 - ".setHSL"
Cohesion: 0.33
Nodes (3): Jr(), qn(), Yn()

### Community 115 - ".constructor"
Cohesion: 0.21
Nodes (6): Ft(), Jt(), kt(), Qt(), Yt(), zt()

### Community 117 - "estimate_drift"
Cohesion: 0.13
Nodes (12): same_clock_distances(), align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay() (+4 more)

### Community 118 - "t"
Cohesion: 0.24
Nodes (6): t(), n(), c(), l(), o(), r()

### Community 119 - "MIX3D"
Cohesion: 0.20
Nodes (10): App per Mac (.dmg), Da DaVinci Resolve, Ingressi: linea, mono, stereo, Installazione da sorgente (macOS), MIX3D, Pannello (`mix3d ui`), Plugin in Fairlight e aggiornamenti, Stato: F0 (fondamenta) (+2 more)

### Community 122 - "ya"
Cohesion: 0.31
Nodes (6): ya(), f(), g(), u(), x(), y()

### Community 123 - ".constructor"
Cohesion: 0.22
Nodes (5): Gl, Ka, A(), C(), R()

### Community 126 - "README.md"
Cohesion: 0.25
Nodes (4): F0: verifiche su Resolve reale [V], Preset inclusi, Spazi 3D, Spazi privati (file)

### Community 129 - "Ph"
Cohesion: 0.50
Nodes (3): ih, lh(), Ph

### Community 131 - "test_ingressi.py"
Cohesion: 0.38
Nodes (3): _project(), test_dual_mono_goes_left_right_and_line_ignores_distance(), test_split_and_join()

### Community 133 - "Compatibilità"
Cohesion: 0.25
Nodes (8): Come i dati diventano utili, Compatibilità, Cose emerse dalla ricerca, Da completare, Database dispositivi, Il kit di Ivan, Riconoscimento dai metadati, da()

### Community 138 - "resolve_install.py"
Cohesion: 0.33
Nodes (4): install(), install_fairlight(), refresh_script(), status()

### Community 139 - "n"
Cohesion: 0.20
Nodes (4): constructor(), r(), n, setValue()

### Community 143 - "hl"
Cohesion: 0.29
Nodes (6): hl(), j(), K(), q(), W(), Ma()

### Community 150 - "il"
Cohesion: 0.29
Nodes (3): il, A(), ol()

### Community 153 - "zl"
Cohesion: 0.38
Nodes (4): zl(), b(), E(), T()

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
- **15 isolated node(s):** `kListen`, `kNumParams`, `kMsgLaunch`, `kMsgOpenBrowser`, `kRing` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1189 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **89 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `da()` connect `Compatibilità` to `.constructor`, `three.module.min.js`, `n`, `.constructor`?**
  _High betweenness centrality (0.282) - this node is a cross-community bridge._
- **What connects `kListen`, `kNumParams`, `kMsgLaunch` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05391120507399577 - nodes in this community are weakly interconnected._
- **Why does `Compatibilità` connect `Compatibilità` to `devices.py`?**
  _High betweenness centrality (0.278) - this node is a cross-community bridge._
- **Should `media.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12643678160919541 - nodes in this community are weakly interconnected._
- **Why does `compat()` connect `devices.py` to `Compatibilità`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13538461538461538 - nodes in this community are weakly interconnected._