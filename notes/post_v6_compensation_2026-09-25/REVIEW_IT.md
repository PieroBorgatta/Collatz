# Revisione interna e limiti della verifica

25 settembre 2026. Revisione mediante agenti e replay aritmetico indipendente;
non referee umano esterno.

Il produttore, l'analisi matematica e il verificatore C/GMP sono stati
sviluppati separatamente. Prima dei nuovi calcoli è stato pubblicato il
protocollo con hash dei sorgenti e della calibrazione. Tutti i file congelati
sono rimasti invariati durante e dopo la verifica dei livelli 22–24.

La revisione ha controllato:

- equivalenza esatta tra credito saturo e massima caduta;
- arrotondamento di H, soglia v=15 e conclusione di visita Syracuse entro J;
- distinzione fra candidata uniforme e verifiche finite;
- sufficienza dei bit e loro consumo nella composizione affine;
- uguaglianza degli hash delle parole complete nei due replay;
- conteggi, estremi, pareggi e testimoni della massima caduta;
- mancata modifica delle costanti dopo i livelli tenuti separati;
- quantificatori del limite sull'astrazione di residuo e altezza;
- distinzione tra interi compatibili generici e punti della torre Q_v.

Il controllo avversariale ha rilevato che una prima versione del wrapper
di replay non rifiutava tutti i riepiloghi alterati. Il wrapper, non incluso
fra i sorgenti congelati, è stato corretto prima del commit dei risultati:
ora impone le decisioni della candidata per ogni livello, il coefficiente,
l'hash del protocollo e la coerenza di `all_passed` e `failed_levels`.
Due test aggiuntivi verificano il rifiuto di queste manomissioni. I dati,
il protocollo, il motore Python e il verificatore C non sono cambiati.

La concordanza fra programmi non è una prova formale del software. La
dimostrazione sull'astrazione è su carta, con revisione interna. La candidata
non ha ancora una prova uniforme, e nessuna nuova dichiarazione Lean viene
presentata come tale. L'originalità matematica non è stabilita.
