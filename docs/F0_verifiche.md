# F0: verifiche su Resolve reale [V]

Da fare sul Mac con Resolve Studio aperto e una timeline di prova (2-3 tracce audio da camere e Tascam).

- [ ] Versione di Resolve Studio: ______
- [ ] `mix3d info` si collega (scripting esterno su "Local")
- [ ] `file_path` punta all'originale e non a un proxy/optimized media
- [ ] `left_offset` e `start_frame` corrispondono a quanto si vede in timeline
- [ ] `mix3d info --otio x.otio` crea un OTIO valido
- [ ] `mix3d reimport` crea la traccia `MIX3D` e posiziona il clip al frame giusto (`recordFrame`)
- [ ] Il clip reimportato è collegato al Media Pool (problema noto sul forum)
- [ ] `mix3d sync` su un concerto vero: drift plausibile (DJI Mic, a6300) e residuo < 20 µs

Annotare qui ogni comportamento diverso dal previsto.
