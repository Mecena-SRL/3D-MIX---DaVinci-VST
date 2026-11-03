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

Interfaccia guidata in 6 passi, con riepilogo (tracce, dispositivi, spazio, sync, picchi) sempre in alto.

1. **Sorgenti**: da Resolve o da file (WAV, MP4, MOV, MXF…). Ogni coppia di canali è una traccia.
2. **Dispositivi**: per ogni traccia registratore + microfono (anche combinazioni miste, es. DJI Mic 2 nella FX6). Specifiche con fiducia, rischi della catena, EQ di correzione, polare.
3. **Spazio**: 12 tipologie italiane incluse (teatro all'italiana, lirico, black box, chiesa, basilica, chiostro, auditorium shoebox e a vigna, cavea, piazza, salone storico, club) o **Importa da file** uno spazio privato. RT60 per banda, distanza critica, consigli. Scena 3D con icone dei dispositivi, **lobi polari 3D** (attivabili), **sorgenti sonore** (+ Sorgente…) e tabella del guadagno polare mic → sorgente. Alt-trascina ruota un microfono.
4. **Analisi**: tabella di salute di tutte le tracce, grafici della selezionata, sync GCC-PHAT + drift, stima della posizione delle sorgenti (TDOA) con ≥3 mic sullo stesso clock.
5. **Ascolto e mix**: play/spazio, A = mix spaziale, B = somma. Buffer ~3 s, rifatto a ogni modifica.
   **EQ dinamico** per traccia: bande illimitate (campana, shelf, passa-alto/basso), ognuna statica o dinamica.
   *Auto-tara* propone le bande da spettro, curva del microfono, risonanze persistenti (tagli dinamici),
   target per sorgente (`voce`, `strumento`, `ambiente`, `generico`), RT60 dello spazio e mascheramento fra tracce.
   Ogni banda dice perché c'è; se la tocchi diventa manuale e l'auto-taratura non la cambia più.
   Nel menu c'è anche **Master**: EQ sul mix intero (auto: bilanciamento a metà + passa-alto 25 Hz). *Tutte* tara prima le tracce, poi il master.
   **Pipeline gestita (come ACES)**: ogni mic entra raddrizzato a neutro con la sua curva (correzione mic), si mixa in neutro,
   e il master esce con un **look** per tipo di progetto (`data/looks.json`): carattere (tipologia di mic o un mic del database con curva),
   EQ e compressore "colla", con intensità 0-100%. Si sceglie nel pannello EQ alla voce Master.
6. **Stampa**: WAV 24 bit normalizzato (picco -1 dBTP) su file, traccia MIX3D, nuova traccia o regione (marker MIX3D / In-Out).

Spazi privati: schema in [`docs/spazi.md`](docs/spazi.md). Restano in `~/.mix3d/spazi/` sul Mac e non vanno nel repository.

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
