# S14 Revisione formale e audit delle nuove dichiarazioni

13 novembre 2026. Revisione in sola lettura dei dieci nuovi moduli; nessun sorgente principale modificato da S14. L'audit transitivo è stato eseguito sugli oggetti compilati correnti: tutti i 69 teoremi pubblici passano con i soli assiomi standard ammessi.

## Copertura della revisione

Sono state lette tutte le firme e le prove dei nuovi moduli. Il conteggio è **69 teoremi pubblici**, non 69 risultati matematici indipendenti. I moduli contengono anche definizioni, istanze e aiutanti privati; gli aiutanti effettivamente usati sono raggiunti transitivamente dall'audit delle radici.

| Modulo | Teoremi pubblici | Confine semantico controllato |
|---|---:|---|
| RootPoolBudget | 12 | Budget dissipativo generale; budget reciproco forte solo con nonricorrenza dell'intero pool; etichette con carico per parola |
| ReturnBlocks | 8 | Ogni lunghezza finita possiede una sorgente; non una singola sorgente con infiniti ritorni crescenti |
| JointAtomDictionary | 10 | Target dispari per le valutazioni esatte; catalogo finito con lunghezza fissata per l'iniettività; completezza del catalogo non assunta implicitamente |
| AffinePositivity | 5 | Positività affine da esponenti positivi e endpoint positivo; il dizionario Syracuse aggiunge non-vuotezza e target dispari |
| CapacityAllocation | 7 | Celle fisiche capped; la minorazione p e l'esistenza di un'allocazione fattibile restano input |
| RelativeMassFlow | 6 | Lower mass e carico sono ipotesi esplicite; nessuna densità asintotica o costruzione di trasporto |
| WordSurgery | 4 | Identità di costante e congruenza necessaria per lo shift nonnegativo; non una costruzione completa della surgery firmata |
| SiblingPool | 8 | L'iniettività della spina dà nonricorrenza dell'intero insieme di fratelli e il carico forte; nessuna minorazione di massa |
| CycleRotation | 6 | Identità di rotazione e sieve con coprimalità esplicita; non esclusione dei cicli |
| FiniteOrbitTransfer | 3 | Adapter con errore terminale N; il limite numerico di finestra è una premessa, non un teorema di sparsezza completo |

## Risultati della lettura semantica

Non sono stati individuati errori materiali nelle firme o nelle prove lette. I casi limite sono correttamente trattati: cataloghi vuoti, parole vuote dove ammesse, segmenti di lunghezza zero e soglie N maggiori della lunghezza.

Il budget forte dei pool non permette di sommare i contributi di endpoint successivi della medesima orbita: il requisito vieta anche connessioni positive tra due radici differenti. Le formule del pool ammettono etichette ripetute soltanto con un carico totale per parola esplicito. Nella conversione a un cap uniforme `1/X`, la sorgente fisica deve stare in una fascia inferiore `v≥X`; un cutoff superiore `v≤DX` non basta.

Il dizionario ternario distingue il requisito di endpoint positivo dalla sua disparità. La positività della sorgente segue già dall'equazione affine integrale e dagli esponenti positivi, senza ipotesi di disparità; per ottenere le valutazioni Syracuse esatte il target deve invece essere dispari. L'equivalenza finale conserva correttamente queste ipotesi. La cardinalità di un catalogo non viene trasformata in cardinalità delle sorgenti senza la prova di iniettività a lunghezza fissata.

I lemmi di allocazione consentono punteggi anche firmati e richiedono positività della soglia dove si divide. Il certificato di uguaglianza non afferma che l'allocazione rispetti automaticamente il cap: questa proprietà appartiene all'applicazione. Nei flussi la stima inferiore di massa relativa non è ottenuta dal doppio conteggio; resta un input esplicito.

`FiniteOrbitTransfer` è deliberatamente generico: formalizza la rimozione degli ultimi N punti e l'iniettività di `f^[N]` sul prefisso. La nuova costante B per i reciproci, il prodotto affine uniforme e D0 restano deduzioni su carta controllate da S10/S12. Nessuna di tali conclusioni numeriche è stata introdotta nel codice come assioma o come ipotesi nascosta.

## Fonte e base fidata

Le integrazioni di pool e soglia attribuiscono i meccanismi a Shaik con commit fissato; non importano sorgenti o teoremi analitici esterni. Il dizionario attribuisce la motivazione al manoscritto rStation, con correzione esplicita del dominio dispari. Le prove usano le definizioni e gli strumenti del progetto locale.

La scansione dei nuovi moduli non trova `sorry`, `admit`, `native_decide`, `implemented_by`, assiomi dichiarati o definizioni `unsafe`. Questa scansione è supplementare; il controllo decisivo della base fidata è l'audit transitivo delle radici effettivamente elaborate.

L'audit [AllNewDependencyAudit.lean](../verification/AllNewDependencyAudit.lean) enumera tutti i 69 teoremi pubblici e fallisce per ogni assioma diverso da `propext`, `Classical.choice`, `Quot.sound`. La lista e gli hash sorgente sono registrati in [s14_audit_plan.json](../verification/s14_audit_plan.json). La compilazione riusa Lean 4.29.1 e dipendenze fissate già installate; non è un replay con kernel indipendente né una revisione umana della catena analitica esterna.

## Confronto fra agenti

S12 ha confermato la separazione fra deduzioni su carta e adapter formale, la necessità di un pool interamente nonricorrente e l'ipotesi di target dispari nel dizionario. S13 ha inviato replay indipendenti senza mismatch tra le firme e i dati: preservati il controesempio al carico 1 e la distinzione tra catalogo di parole e immagini fisiche. S15 ha ricevuto conteggi e limiti per la decisione sulla v7.

## Esito dell'audit effettivo

**PASS, exit 0.** L'elaborazione dell'audit è iniziata alle 16:21:39 UTC e si è conclusa alle 16:23:35 UTC, in 115,668 secondi. Tutte le 69 radici attese compaiono esattamente una volta nel log; per ciascuna gli assiomi sono un sottoinsieme di `propext`, `Classical.choice`, `Quot.sound`. Nessun `sorryAx`, assioma nativo o assioma aggiuntivo è stato raggiunto.

Gli hash dei dieci sorgenti coincidono con quelli preparati e sono rimasti invariati durante il controllo. L'audit è stato avviato dopo la conferma del coordinatore che tutti i dieci oggetti erano compilati; alla conclusione anche la compilazione integrata risultava PASS. [Log completo](../verification/s14_all_new_axioms.log), [ricevuta con comando, hash e tempi](../verification/s14_receipt.json).

Gli avvisi della compilazione riguardano ipotesi `DecidableEq` superflue in `RelativeMassFlow`, un suggerimento stilistico in `WordSurgery` e una precedente ipotesi inutilizzata in `SignedTransport`. Non sono errori matematici o assiomi aggiuntivi. Non sono stati modificati sorgenti durante la verifica per eliminarli.

Comando riproducibile dalla directory `lean`:

```sh
lake env lean ../notes/research_sprint_2026-11-13/verification/AllNewDependencyAudit.lean
```

Il risultato consolida la base formale delle integrazioni finite. Non prova la stima numerica di sparsezza, il limite D0, una quota relativa di massa, H o Collatz; tali confini sono parte delle firme e della revisione semantica sopra.
