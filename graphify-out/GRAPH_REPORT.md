# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 19 files · ~17,704 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .css 1)

## Summary
- 248 nodes · 513 edges · 11 communities (9 shown, 2 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5fccab88`
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
- analysis.py
- mix3d

## God Nodes (most connected - your core abstractions)
1. `estimate_drift()` - 12 edges
2. `render()` - 11 edges
3. `Loudness` - 10 edges
4. `gcc_phat()` - 10 edges
5. `_TL` - 10 edges
6. `read()` - 9 edges
7. `print_mix()` - 9 edges
8. `connect()` - 9 edges
9. `read_audio_clips()` - 9 edges
10. `renderAnalysis()` - 9 edges

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

## Communities (11 total, 2 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.12
Nodes (17): analyze(), _coarse(), db(), sync_pair(), warnings(), job_analyze(), align(), DriftModel (+9 more)

### Community 2 - "server.py"
Cohesion: 0.13
Nodes (10): apply_profile(), browse(), Handler, import_resolve(), new_project(), public_state(), start_job(), tracks_from_file() (+2 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.12
Nodes (9): blocks(), decoded(), probe(), concert(), _music(), test_database_coerente(), test_file_video_aac(), test_loudness_sinusoide() (+1 more)

### Community 4 - "cli.py"
Cohesion: 0.15
Nodes (14): cmd_info(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip, connect() (+6 more)

### Community 5 - "mixer.py"
Cohesion: 0.11
Nodes (10): auto_positions(), same_clock_distances(), spatial_params(), read(), active(), correction_fir(), print_mix(), render() (+2 more)

### Community 6 - "app.js"
Cohesion: 0.18
Nodes (27): api(), browse(), color(), COLORS, css(), drawMiniWave(), drawPolar(), fit() (+19 more)

### Community 7 - "MIX3D"
Cohesion: 0.17
Nodes (9): Come i dati diventano utili, Da completare, Database dispositivi, F0: verifiche su Resolve reale [V], Installazione (macOS), MIX3D, Pannello (`mix3d ui`), Stato: F0 (fondamenta) (+1 more)

### Community 8 - "devices.py"
Cohesion: 0.18
Nodes (7): correction_db(), load(), polar_gain(), profile(), response_db(), suggest(), devices_payload()

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 88 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `read_audio_clips()` connect `cli.py` to `test_resolve_bridge.py`, `server.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `reimport_wav()` connect `cli.py` to `test_resolve_bridge.py`, `server.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.12222222222222222 - nodes in this community are weakly interconnected._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13105413105413105 - nodes in this community are weakly interconnected._
- **Should `test_ui_engine.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._