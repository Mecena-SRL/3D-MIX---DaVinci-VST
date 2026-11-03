# Spazi 3D

Assi in metri: x = larghezza (destra +), y = altezza, z = verso il pubblico. z = 0 è il bordo del palco, il palco sta a z < 0.

## Preset inclusi

`src/mix3d/data/spazi.json`: 12 tipologie generiche italiane, senza luoghi reali. Campi: `id, nome, tipo, descrizione, sala{w,d,h}, palco{w,d,h}, aperto, rt60{125..4k} (s), posti, volume_m3, ascoltatore[x,y,z], consigli[], elementi[]`.

Elementi disegnati nella scena: `box{pos,size,colore}`, `palchi{ordini,altezza,profondita}`, `colonne{x[],da,a,passo,diametro,altezza}`, `gradinate{file,da,a,alzata,arco°}`, `abside{raggio}`, `portico{profondita,altezza}`.

Distanza critica (sorgente omni): `0,057 · √(V / RT60₅₀₀)`. È l'anello tratteggiato attorno al palco.

## Spazi privati (file)

Pulsante **Importa da file…** al passo 3. Il file viene copiato in `~/.mix3d/spazi/` e resta solo su quel Mac. **Non va mai nel repository.**

Schema `mix3d-spazio/1` (`*.mix3d-space.json`):

```json
{
  "formato": "mix3d-spazio/1", "id": "mia-sala", "nome": "…", "tipologia": "…", "citta": "…", "capienza": 300,
  "sala": {"w": 14, "d": 14, "h": 9}, "palco": {"w": 12, "d": 7, "h": 0.8}, "listener": [0, 1.2, 6.5],
  "acustica": {"rt60_s": {"125": 1.1, "500": 0.9, "1000": 0.85}, "note": "…"},
  "pianta": {"poligono": [[x, z], …], "elementi": [
    {"tipo": "palco|platea|galleria|boccascena|cappella|coro|organo", "poligono": [[x, z], …], "altezza": 0.8, "quota": 3.5, "nota": "…"},
    {"tipo": "porta", "punto": [x, z]}]},
  "mic_consigliati": [{"nome": "…", "nota": "…"}], "fonti": ["…"]
}
```

`altezza` estrude dal pavimento; con `quota` l'elemento è una lastra a quella altezza (gallerie, cori).
