# H.2 — Chiusura del trasporto mediante il solo ultimo esponente

26 settembre 2026 · Piero Borgatta con assistenza Codex.

**Abbiamo ottenuto un limite più forte del precedente:** per due target
positivi dispari distinti n,y e ogni dilatazione fissa D>0, tutte le
correzioni ammissibili dell'ultimo esponente, positive e negative, producono
soltanto o(X) immagini distinte entro DX da sorgenti dispari entro X.
Si possono scegliere liberamente anche nuovi fattori di due all'immagine.
Usiamo la parola del primo arrivo a n; quando n non ha ritorni positivi,
come nel dominio dell'ipotesi H, questo comprende tutte le parole di arrivo.

La [dimostrazione completa](PROOF_IT.md) separa profondità limitate,
espansioni grandi e compressioni grandi. La congruenza modulo 3^k esclude
correzioni limitate a profondità arbitraria. Una doppia stima geometrica
controlla le altre immagini, senza supporre iniettività e senza scegliere
una correzione ottimale. Il risultato non dipende da un censimento numerico.

## Che cosa è verificato

- `SignedTransport.lean`: sei teoremi aritmetici sulle identità affini,
  le congruenze e le stime di espansione/compressione.
- Il teorema asintotico o(X) è **su carta**, non ancora formalizzato in Lean.
- Il controllo Python usa aritmetica esatta: 690 trasporti firmati,
  cinque rappresentanti di una fibra e 80 casi di conteggio diadico.
  Questi esempi verificano l'implementazione delle identità; non dimostrano
  l'enunciato asintotico.
- Compilazione integrata riuscita: 3.380 passaggi, exit 0. Audit di tutti
  i sei teoremi superato con soli assiomi standard. La compilazione segnala
  una sola ipotesi di disparità inutilizzata, senza errori. Replay Python
  identico byte per byte sia normale sia con `-O`.
- Esiti finali, comandi, limiti della verifica e hash sono nel
  [manifest](verification_manifest.json) e nei log allegati.

## Decisione e prossimo problema

**Non ha senso continuare a ottimizzare soltanto l'ultimo esponente.**
Nemmeno ammettere tutte le sue modifiche recupera una quota positiva di
immagini a dilatazione fissa, se il bacino sorgente ha densità inferiore
positiva. Un controllo migliore delle collisioni non risolve questo limite.

La prossima costruzione deve cambiare altri esponenti, quindi la costante
affine C, oppure la profondità della parola. Il requisito da ottenere è
un confronto di massa relativa con altezza e molteplicità controllate;
una mappa definita su singoli esempi non è sufficiente. Questa costruzione
**non è ancora disponibile**. È il problema rimasto aperto, non un nuovo
teorema annunciato.

**H resta aperta; Collatz non è risolta.** Il risultato esclude un metodo
specifico di confronto, non la densità del bacino superiore. L'eventuale
programma H riguarderebbe comunque le orbite non periodiche e lascerebbe
da trattare separatamente i cicli non banali.

Il quadro bibliografico già consultato resta quello del
[riesame del 26 settembre](../post_v6_reset_2026-09-26/RESULTS_IT.md) e del
[seguito H.1](../post_v6_basin_transport_2026-09-26/SOURCES_IT.md).
Questo seguito sviluppa una deduzione interna: non rivendica novità nella
letteratura né una revisione umana indipendente. I PDF pubblicati restano
snapshot immutati.
