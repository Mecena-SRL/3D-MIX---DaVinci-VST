# Database dispositivi

File: [`src/mix3d/data/devices.json`](../src/mix3d/data/devices.json) (v0.2: 73 microfoni, 47 registratori/camere, 18 adattatori, 26 profili). Sezioni:

- **microfoni**: marca, tipo, capsula, diagramma, banda, sensibilità, rumore, SPL max, curva (se c'è), **connettore**, **alimentazione**.
- **registratori** (camere, registratori, action cam, wireless che registrano): formato, bit, sample rate, codec, clock, timecode, rischi, **ingressi** (tipo, numero, phantom, plug-in power, EIN), **mic_interno**, canali.
- **adattatori**: come un connettore diventa un altro (maniglie XLR Sony, ricevitori wireless, RODE VXLR Pro, cavi).
- **profili**: combinazioni pronte = registratore + microfono + ruolo + posizione + indizi (nome file, canali).
- **rischi**: testi degli avvisi.

Ogni voce ha `fiducia` per campo (`datasheet`, `misurato`, `ipotizzato`; assente = ipotizzato) e `fonti`. `datasheet` solo per i valori verificati sulla fonte citata.

Copertura: Sony (FX6, FX9, FX3, FX30, FX2, a7S III, a7 IV, a6700, ZV-E1, a6300, a6400; ECM-MS2, XM1, VG1, B1M, B10, M1, G1, L1, W3, W2BT, UWP-D), Sennheiser (MKH 416, 8060, 50, MKE 600, 400, ME 66, MKE 2, EW-D, Profile, e 835/935/906/614), RODE (NTG1/2/3/4+/5, VideoMic NTG/Pro+/Micro II/GO/GO II, NT1-A/NT4/NT5, Lavalier II, Wireless GO II/PRO), Tascam (X8, X6, DR-40X, DR-05X/07X, DR-10L Pro, FR-AV2, DR-701D, DR-60D MkII, TM-80/2X/10L), Zoom (F8n Pro, F6, F3, F2, H8, H6, H6essential, H5, H5studio, H4n Pro, H4essential, H1n, H1essential, M3, M4, capsule XYH-6/MSH-6/SGH-6, ZDM-1), DJI (Osmo Action 4/5 Pro/6, Pocket 3, Mic, Mic 2, Mic 3, Mic Mini/Mini 2), Behringer (C-2, ECM8000).

## Compatibilità

`devices.compat(registratore, microfono)` → `{ok, via, note}`:

1. il mic è tra i `mic_interno` del registratore → ok;
2. connettore del mic = tipo di un ingresso → ok diretto;
3. altrimenti un adattatore `da` → `a` (con `solo` per i modelli ammessi) → ok via adattatore;
4. in ogni caso il mic deve avere l'alimentazione disponibile: `phantom` (ingresso o adattatore con phantom), `plug_in_power`, oppure batteria/slitta/USB/nessuna.

`ok: False` = non si collega (connettore o alimentazione), `None` = non verificabile (es. mixer). Nel pannello: i microfoni non collegabili al registratore scelto sono marcati ✕ e la catena mostra "Collegamento: …" o l'avviso. `/api/devices` include `compat` (matrice registratore × microfono).

### Il kit di Ivan

| | Sony FX6 | Sony FX30 | Sony a6300 | Osmo Action 5 Pro | Tascam X8 |
|---|---|---|---|---|---|
| ECM-MS2 | XLR maniglia | XLR-H1 | XLR-K2M | ✕ no phantom | XLR 3-6 |
| MKH 416 | XLR maniglia | XLR-H1 | XLR-K2M | ✕ no phantom | XLR 3-6 |
| C-2 | XLR maniglia | XLR-H1 | XLR-K2M | ✕ no phantom | XLR 3-6 |
| VideoMic GO / GO II | solo con RODE VXLR Pro | 3.5 mm | 3.5 mm | 3.5 mm via adattatore USB-C | 3.5 mm (ingressi 1-2, al posto dei mic interni) |
| DJI Mic 2 / Mini | ricevitore + cavo 3.5 mm-XLR | ricevitore 3.5 mm | ricevitore 3.5 mm | diretto (OsmoAudio) | ricevitore 3.5 mm |

### Cose emerse dalla ricerca

- **FX6**: nessun ingresso 3.5 mm per microfono; slitta MI della maniglia analogica (niente ECM-B1M/B10/M1 in digitale).
- **ECM-MS2**: due XLR con phantom 48 V (non plug-in power).
- **VideoMic GO (prima versione)**: 100 Hz-16 kHz, 34 dB(A): utile come spot/sync, non come base.
- **RODE Wireless GO II**: SPL max 100 dB: in concerto satura vicino alle sorgenti.
- **Osmo Action 4/5 Pro/6, Pocket 3**: audio AAC 16 bit; collegamento diretto con DJI Mic 2 (Action 6 anche Mic 3 e Mic Mini).
- **DJI Mic Mini**: nessuna registrazione interna. **DJI Mic 3**: 32 bit float e timecode (±0.5 ppm).
- **Zoom F6/F3/H6essential, Tascam X6/X8**: 32 bit float; EIN -120…-127 dBu.

## Come i dati diventano utili

| Dato | Uso |
|---|---|
| banda, curva | risposta stimata e EQ di correzione (±6 dB, solo in banda) applicata nel mix |
| diagramma | grafico polare; in F3 peso fuori asse |
| rumore, SPL max | gamma utile mostrata nel pannello; avviso `spl_basso` |
| connettore, alimentazione, ingressi, adattatori | compatibilità della catena |
| ruolo | guadagno di partenza (base 0 dB, ambiente -3, spot -6, sync/riferimento muto) |
| posizione tipica | posizionamento automatico iniziale nella scena |
| codec, bit, nome file, canale | suggerimento del profilo per ogni traccia |
| rischi | avvisi nel pannello e scelte del motore (AGC, file divisi, drift wireless, 16 bit, DSP) |

## Da completare

- Modello action cam DJI (oggi `osmo_action` generico), versione VideoMic GO (I o II), modello del mixer.
- Pattern dei nomi file reali di Tascam X8, Zoom e DJI Mic 2/3.
- Valori `ipotizzato`: confermare sul datasheet (sensibilità/rumore di molti shotgun, ingressi delle mirrorless).
- Plug-in power dell'adattatore USB-C DJI da verificare.
- Misure proprie (sweep + rumore rosa con ECM8000) per passare a `misurato`.

Per aggiungere un dispositivo: nuova voce in `microfoni`/`registratori` con `connettore`/`alimentazione` o `ingressi`, poi un profilo. `pytest` controlla vocabolario, adattatori e che ogni profilo sia collegabile.
