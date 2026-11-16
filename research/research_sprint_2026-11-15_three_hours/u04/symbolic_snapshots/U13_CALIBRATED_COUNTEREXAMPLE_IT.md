# U13 — Prefissi F-calibrati senza ottimalità grezza dei fattori

Sessione del 15–16 novembre 2026, base `203cbb8`. Addendum indipendente alla nota U13, su richiesta del coordinatore dopo la definizione max-plus di U12/U15. Nessun file precedente è stato modificato. Le verifiche sono finite, esatte e preregistrate; nessuna GPU o nuova griglia.

## 1. Definizione e risultato

Per ogni positivo dispari unità n, porre

`F(n)=max{Ω(w): w effettiva da un seed unità positivo a n}`, `Ω(w)=3^|w|/2^Σw`.

La parola vuota è inclusa. La finitezza del catalogo Ω≥1, già stabilita nel progetto, giustifica in generale il massimo; per gli stati usati qui ne dimostriamo direttamente il valore esatto contro TUTTI i seed e tutti i tempi.

Esiste un prefisso effettivo, con sorgente unità31 e target911, tale che ogni suo endpoint n_i soddisfa

**`F(n_i)=Ω(31→n_i)F(31)=Ω(31→n_i)`, `F(31)=1`.**

Ogni suo prefisso è quindi calibrato per F; ogni suo arco soddisfa l'uguaglianza della ricorrenza max-plus. Eppure il fattore finale `[3]:2429→911` non è ottimale nel peso grezzo: il rivale unità `[1]:607→911` ha peso3/2, quattro volte3/8.

Questo è un controesempio effettivo alla deduzione LOCALE “prefissi F-calibrati ⇒ fattori grezzamente ottimali”. Non è un controesempio alla calibrazione pesata dei sotto-cammini, che resta valida per il principio di programmazione dinamica. Non stabilisce alcuna affermazione sulla parola infinita di un minimo controesempio.

## 2. Esclusione dei seed unità minori di31

Tutte le unità dispari positive minori di31 sono contenute nell'insieme chiuso in avanti

`V_U={1,5,7,11,13,17,19,23,25,29,35,53}`.

La chiusura è certificata dalle frecce

`1→1,5→1,7→11,11→17,13→5,17→13,19→29,23→35,25→19,29→11,35→53,53→5`.

911 non appartiene a V_U. Quindi nessun seed unità minore di31 raggiunge911, né un qualunque endpoint precedente del cammino31→911: da quell'endpoint raggiungerebbe911 per transitività.

La sorgente33 è esclusa perché è multipla di3;32 e34 sono pari. Tutti i seed unità maggiori di31 sono pertanto almeno35.

## 3. Il certificato quantitativo alla soglia35

La parola effettiva da31 a911 ha

`k=27`, `A=38`, `Ω_end=3^27/2^38=7625597484987/274877906944`.

Gli stati sono

`31,47,71,107,161,121,91,137,103,155,233,175,263,395,593,445,167,251,377,283,425,319,479,719,1079,1619,2429,911`.

Per ogni prefisso scrivere Ω_i=3^i/2^A_i. Il potenziale normalizzato cresce esattamente:

`n_(i+1)/Ω_(i+1)=n_i/Ω_i+1/(3Ω_i)`.

Il suo valore finale è

`911/Ω_end=250413773225984/7625597484987≈32.83857739921227<35`.

Il margine esatto è

`35−911/Ω_end=16482138748561/7625597484987>0`.

La soglia35 era fissata prima dell'esecuzione e non è stata adattata. Di conseguenza `n_i/Ω_i<35` per OGNI prefisso.

Considerare ora una qualunque parola effettiva u→n_i con seed unità u≥35. Il potenziale reciproco già verificato nel progetto dà

`Ω(u→n_i)≤n_i/u≤n_i/35<Ω_i`.

I seed minori di31 sono impossibili per il §2. Il solo candidato rimasto è31. La sua intera orbita fino a1 è stata verificata, senza ripetizioni prima di1; poi S(1)=1. Ogni endpoint n_i>1 è dunque privo di ritorni e la parola da31 a n_i è unica. Essa realizza il massimo F(n_i), anzi è l'unica sorgente unità che lo realizza. Il caso iniziale i=0 dà F(31)=1 attraverso la parola vuota.

La prova usa quindi un bound valido per tutti gli eventuali seed, non un censimento troncato a35 e non una stima numerica di F.

## 4. Il fattore grezzo perde, quello pesato resta calibrato

Le due relazioni sono esatte:

`S(2429)=911`, `v₂(3·2429+1)=3`,
`S(607)=911`, `v₂(3·607+1)=1`.

Entrambi i genitori sono unità. Il fattore originale ha peso3/8, il rivale3/2. Quindi l’originale non è division-minimal e non massimizza il peso inverso grezzo alla propria profondità.

Però il confronto corretto della ricorrenza max-plus moltiplica ciascun peso per F del suo stato iniziale. Nessun seed unità≤31 raggiunge607: gli inizi minori sono nel set chiuso del §2, e la traiettoria completa di31 non passa per607. Ne segue dal potenziale

`F(607)≤607/35`.

Pertanto

`(3/2)F(607)≤1821/70≈26.0142857<F(911)=3^27/2^38≈27.7418`.

L'arco originale soddisfa invece

`(3/8)F(2429)=F(911)`.

Non c'è una violazione della programmazione dinamica. Il rivale ha coefficiente grezzo maggiore ma un potenziale di ingresso inferiore. Per ricavare una lingua puramente sintattica di fattori ottimali serve un controllo supplementare di quel potenziale; la calibrazione dei prefissi non lo elimina.

## 5. Verifica e ambito

Il protocollo è in [u13calibrated/protocol.json](../../../research/research_sprint_2026-11-15_three_hours/u13calibrated/protocol.json). Il [programma esatto](../../../research/research_sprint_2026-11-15_three_hours/u13calibrated/check_calibrated_prefix.py) controlla la chiusura del set dei seed piccoli, tutte le valutazioni della traiettoria31→911→1, la monotonia del potenziale, ogni confronto con35 e i due rivali. Il percorso non viene scelto o ingrandito dopo il risultato.

Le esecuzioni normale e Python-O producono gli stessi byte. Non sono un nuovo teorema Lean né un censimento di grandi orbite. La prova generale che la disuguaglianza del potenziale esclude tutti i seed≥35 è separata dal solo controllo dei dati finiti. Non si rivendica una priorità bibliografica globale per il principio max-plus o per la distinzione fra ottimalità pesata e grezza.
