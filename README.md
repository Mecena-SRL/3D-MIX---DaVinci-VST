# MIX3D

Fusione multi-sorgente e mix per concerti, teatro ed eventi, integrato con DaVinci Resolve Studio.
Il piano completo è in [`docs/piano_mix3d_v1.0.pdf`](docs/piano_mix3d_v1.0.pdf).

Non è un VST: un motore Python offline legge la timeline di Resolve, analizza i file originali
e reimporta una traccia `MIX3D`. Non modifica mai i media né le tracce esistenti.

## Stato: F0 (fondamenta)

| Modulo | Cosa fa | Stato |
|---|---|---|
| `resolve_bridge` | legge le tracce audio e i file originali, esporta OTIO, reimporta un WAV su una nuova traccia | scritto, da verificare su Resolve reale |
| `sync` (M2) | GCC-PHAT sub-campione, drift lineare robusto (RANSAC), raffinamento | testato su dati simulati: errore < 20 µs, drift < 1 ppm |

## Installazione (macOS)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

In Resolve Studio: **Preferenze > Sistema > Generale > External scripting using: Local**.

## Uso

```bash
mix3d info --otio backup.otio           # tracce, clip e file originali della timeline attiva
mix3d sync tascam.wav fx6.wav dji.wav   # offset e drift di ogni file rispetto al riferimento
mix3d reimport mix.wav --frame 86400    # nuova traccia 'MIX3D' al frame indicato
```

Le verifiche da fare su Resolve sono in [`docs/F0_verifiche.md`](docs/F0_verifiche.md).
