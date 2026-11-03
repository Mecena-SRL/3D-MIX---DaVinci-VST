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

| `devices` + `data/devices.json` | database dispositivi (datasheet, fiducia per campo), suggerimento automatico, curve di risposta/correzione, polari | testato |
| `analysis` | forma d'onda, picco, rumore, dinamica, clipping, spettro 1/3 ott, banda utile, loudness BS.1770, sync grossolano+fine | testato su dati simulati |
| `mixer` | mix stereo a blocchi (ascolto e stampa con lo stesso codice), correzione colore, distanza e pan dall'ascoltatore, normalizzazione LUFS | testato |
| `server` + `web/` | pannello nel browser (`mix3d ui`) | provato in Chromium headless |

## Pannello (`mix3d ui`)

Apre `http://127.0.0.1:8730` (solo locale, funziona offline).

1. **+ File** o **Da Resolve**: ogni file diventa una o più tracce (canali a coppie). Il dispositivo è suggerito da nome, codec, bit e canale: conferma o cambia (bordo giallo = da confermare).
2. **Analizza e sincronizza**: analisi di ogni traccia e sync (GCC-PHAT + drift) sulla traccia di riferimento; posizioni automatiche.
3. **Scena 3D**: trascina microfoni e ascoltatore (shift = altezza). *Tutto automatico* ripristina le stime.
4. **Analisi / Dispositivo**: grafici della traccia selezionata, specifiche con fiducia, EQ di correzione, polare.
5. **Ascolto**: play/spazio, A = mix spaziale, B = somma semplice. Buffer ~3 s; a ogni modifica il buffer si rifà.
6. **Stampa**: WAV 24 bit normalizzato (-14 LUFS, picco -1 dBTP), opzionalmente su una nuova traccia o su una traccia esistente di Resolve.

Limiti: il posizionamento automatico è approssimato (posizione tipica del profilo + ritardi fra canali dello stesso registratore); il drift in ascolto è corretto a blocchi (in F1 ricampionamento continuo). Database: [`docs/database_dispositivi.md`](docs/database_dispositivi.md).

## App per Mac (.dmg)

Scarica il `.dmg` dalle [Release](https://github.com/Mecena-SRL/3D-MIX---DaVinci-VST/releases) (arm64 = Apple Silicon, x86_64 = Intel), trascina **MIX3D** in Applicazioni.
L'app non è firmata: al primo avvio tasto destro su MIX3D > Apri > Apri. Si apre il pannello nel browser; **Esci** la chiude.
ffmpeg e Three.js sono inclusi, nessuna installazione extra. Build locale: `packaging/build_macos.sh`; release: Actions > Release macOS > Run workflow con *release* attivo (usa la versione di `pyproject.toml`), oppure push di un tag `vX.Y.Z`.

## Da DaVinci Resolve

Nel pannello: **In Resolve…** › *Installa pannello e script* (oppure `mix3d install-resolve`), poi riavvia Resolve.
- **Workspace › Workflow Integrations › MIX3D**: il pannello in una finestra di Resolve (Studio).
- **Workspace › Scripts › MIX3D**: apre l'app.

*Adjustment clip audio*: in Edit o Fairlight metti un **marker chiamato MIX3D con durata** sulla regione (o usa In/Out), poi Stampa › *Solo la regione*: il mix di quella regione va sulla traccia MIX3D allo stesso punto e sostituisce la stampa precedente.

## Installazione da sorgente (macOS)

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
mix3d ui                                # pannello nel browser
```

Le verifiche da fare su Resolve sono in [`docs/F0_verifiche.md`](docs/F0_verifiche.md).
