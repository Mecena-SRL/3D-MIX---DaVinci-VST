# Database dispositivi

File: [`src/mix3d/data/devices.json`](../src/mix3d/data/devices.json). Tre sezioni:

- **microfoni**: capsula, diagramma, banda, sensibilità, rumore, SPL max, curva (se digitalizzata).
- **registratori**: formato, bit, sample rate, codec, clock, timecode, rischi (AGC, codec, drift...).
- **profili**: ciò che si assegna a una traccia = registratore + microfono + ruolo nel mix + posizione tipica + indizi (nome file, canali).

Ogni voce ha `fiducia` per campo (`datasheet`, `misurato`, `ipotizzato`; assente = ipotizzato) e `fonti`.

## Come i dati diventano utili

| Dato | Uso |
|---|---|
| banda, curva | risposta stimata e EQ di correzione (±6 dB, solo in banda) applicata nel mix |
| diagramma | grafico polare; in F3 peso fuori asse |
| rumore, SPL max | gamma utile mostrata nel pannello |
| ruolo | guadagno di partenza (base 0 dB, ambiente -3, spot -6, sync/riferimento muto) |
| posizione tipica | posizionamento automatico iniziale nella scena |
| codec, bit, nome file, canale | suggerimento del profilo per ogni traccia |
| rischi | avvisi nel pannello e scelte del motore (AGC, file divisi, drift wireless) |

## Da completare

- Modello action cam DJI, versione VideoMic GO (I o II), modello del mixer.
- Pattern dei nomi file reali di Tascam X8 e DJI Mic 2.
- Misure proprie (sweep + rumore rosa) per passare da `datasheet` a `misurato`.

Per aggiungere un dispositivo: nuova voce in `microfoni`/`registratori`, poi un profilo. `pytest` controlla la coerenza.
