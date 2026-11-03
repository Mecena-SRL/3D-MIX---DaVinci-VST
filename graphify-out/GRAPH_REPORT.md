# Graph Report - 3D-MIX---DaVinci-VST  (2026-11-03)

## Corpus Check
- 19 files · ~18,233 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .css 1)

## Summary
- 252 nodes · 521 edges · 11 communities (10 shown, 1 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4e4a2792`
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
2. `Loudness` - 10 edges
3. `render()` - 10 edges
4. `gcc_phat()` - 10 edges
5. `renderAnalysis()` - 10 edges
6. `_TL` - 10 edges
7. `read()` - 9 edges
8. `print_mix()` - 9 edges
9. `connect()` - 9 edges
10. `read_audio_clips()` - 9 edges

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

## Communities (11 total, 1 thin omitted)

### Community 0 - "test_resolve_bridge.py"
Cohesion: 0.07
Nodes (9): _Item, _MPI, _PM, _Pool, _Project, _Resolve, test_read_audio_clips(), test_reimport_adds_new_track_only() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.18
Nodes (11): align(), DriftModel, estimate_drift(), fit_drift(), gcc_phat(), windowed_delays(), _frac_delay(), _music_like() (+3 more)

### Community 2 - "server.py"
Cohesion: 0.12
Nodes (11): profile(), apply_profile(), browse(), Handler, import_resolve(), new_project(), public_state(), start_job() (+3 more)

### Community 3 - "test_ui_engine.py"
Cohesion: 0.11
Nodes (9): blocks(), decoded(), probe(), concert(), _music(), test_database_coerente(), test_file_video_aac(), test_loudness_sinusoide() (+1 more)

### Community 4 - "cli.py"
Cohesion: 0.15
Nodes (14): cmd_info(), cmd_reimport(), cmd_sync(), cmd_ui(), _load_mono(), main(), AudioClip, connect() (+6 more)

### Community 5 - "mixer.py"
Cohesion: 0.20
Nodes (6): spatial_params(), active(), correction_fir(), print_mix(), render(), span()

### Community 6 - "app.js"
Cohesion: 0.17
Nodes (28): api(), browse(), chainRisks(), color(), COLORS, css(), drawMiniWave(), drawPolar() (+20 more)

### Community 7 - "MIX3D"
Cohesion: 0.17
Nodes (9): Come i dati diventano utili, Da completare, Database dispositivi, F0: verifiche su Resolve reale [V], Installazione (macOS), MIX3D, Pannello (`mix3d ui`), Stato: F0 (fondamenta) (+1 more)

### Community 8 - "devices.py"
Cohesion: 0.20
Nodes (7): chain_risks(), correction_db(), load(), polar_gain(), response_db(), suggest(), devices_payload()

### Community 10 - "analysis.py"
Cohesion: 0.08
Nodes (12): analyze(), _coarse(), db(), k_weighting(), Loudness, sync_pair(), warnings(), auto_positions() (+4 more)

## Knowledge Gaps
- **1 isolated node(s):** `mix3d`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 90 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `read_audio_clips()` connect `cli.py` to `test_resolve_bridge.py`, `server.py`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **What connects `mix3d` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_resolve_bridge.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606606606606606 - nodes in this community are weakly interconnected._
- **Why does `reimport_wav()` connect `cli.py` to `test_resolve_bridge.py`, `server.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12433862433862433 - nodes in this community are weakly interconnected._
- **Should `test_ui_engine.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10846560846560846 - nodes in this community are weakly interconnected._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14814814814814814 - nodes in this community are weakly interconnected._