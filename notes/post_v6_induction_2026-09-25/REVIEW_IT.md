# Revisione interna della fase di trasferimento

25 settembre 2026. Revisione tramite agenti, non referee umano indipendente.

Sono stati separati tre compiti: formalizzazione del criterio generale,
analisi e formalizzazione del trasferimento, critica dei controesempi e
degli esperimenti. Il coordinatore ha scritto il probe e integrato i risultati.

La revisione ha verificato:

- Il termine additivo è incluso attraverso la dissipazione del potenziale.
- Il criterio conclude una visita entro l'orizzonte, non necessariamente
  un endpoint sotto soglia. Il test 9→7→11 copre questa distinzione.
- Il trasferimento richiede un endpoint inferiore sotto soglia, oppure
  direttamente il limite sulla parte omogenea allo stesso tempo scelto.
- La condizione relativa sui pesi è sufficiente; non è provata per tutti
  i livelli e non segue dalla sola ricorrenza quadratica.
- Il controesempio al cono usa esponenti Syracuse effettivi, anche con
  coefficiente lineare negativo. Non è dimostrata la sua raggiungibilità
  dalla famiglia Q_v.
- Le regole del probe dipendono da v e dal certificato inferiore; la
  baseline superiore serve al controllo del replay. I dati erano già
  disponibili, quindi l'esplorazione è descritta come retrospettiva.
- I 52 tentativi includono tutti i fallimenti. La tabella e gli esempi
  coincidono con il JSON. Un test fallito non implica mancata discesa.
- Cercare un tempo che soddisfi il criterio è legittimo per certificati
  finiti; il problema uniforme è dimostrare la terminazione della ricerca.
- La quarta regola temporale non supera i precedenti certificati diretti;
  il suo successo osservato non viene presentato come legge generale.

Non è stabilita originalità nella letteratura. Il numero di dichiarazioni
Lean misura l'organizzazione della formalizzazione, non il numero di
scoperte matematiche. Il manifest finale distingue controlli locali,
replay CI e dipendenze formali. La catena di verifica resta quella del
toolchain Lean/Mathlib fissato nel progetto; questo lavoro non effettua
il porting a un toolchain successivo.
