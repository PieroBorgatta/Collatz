# Analisi 5 Copertura e ritorni alla sezione

13 novembre 2026. Analisi in sola lettura del commit 5428e89. Il progetto ha già una copertura universale della sezione e formule parametriche per segmenti arbitrariamente lunghi; manca il controllo dei successivi ritorni. La proposta più produttiva è un verificatore di domini parametrici con copertura esplicita. Un contatore della sola durata delle escursioni non risolve il reset dopo l'uscita.

## Risultati esistenti e confine globale

`lean/CollatzShadowing/ShortcutCoverage.lean:73` prova la diminuzione di un rango fino all'arrivo a 1 o a `20 mod27`; `:129` dà il limite `13n+4`. `MarkedSection.lean:15` definisce i sei porti di E e `:154` li identifica esattamente con episodi contenenti il residuo. `SectionCoverage.lean:119` trasferisce la copertura alla mappa dispari-dispari S. `SectionReturn.lean:25` dà visite arbitrariamente tarde per chi non arriva a 1.

Sono prove globali di copertura, non di discesa. La famiglia `661+1152t → 31+54t` è formalizzata in `SectionReturn.lean:37`; `:56` mostra un primo ritorno crescente `31→121`. L'esistenza di `RankDescent` (`:96`) è formalmente equivalente alla congettura accelerata (`:131`), quindi proporre semplicemente un rango non riduce da solo la difficoltà.

`CancellationTower.lean:44` comprime esattamente `[1,2]^r`: `8^r u−5 → 9^r u−5`, per u pari almeno 2; `:82` esclude discesa interna. `SectionReturn.lean:79` mostra che nessun orizzonte accelerato fissato basta su E. Il criterio affine di `FirstBarrier.lean:144` è un'equivalenza esatta fra endpoint inferiore e sorgente sopra la barriera. `DescentCertificate.lean:73` permette un certificato sufficiente di visita sotto soglia, ma non stima automaticamente la somma degli esponenti reali.

## Pilota ricontrollato

Per `n=205087+1179648t`, t naturale, le coppie costante/coefficiente delle sette righe sono:

`(205087,1179648), (307631,1769472), (461447,2654208), (692171,3981312), (1038257,5971968), (778693,4478976), (146005,839808)`.

Ho verificato esattamente, sui coefficienti simbolici, `3a_i+1=2^e a_(i+1)` e `3b_i=2^e b_(i+1)` con esponenti `[1,1,1,1,2,4]`; ogni endpoint è dispari per ogni t. Le righe 1–4 sono rispettivamente `47,71,35,17 mod72`, escluse da E. Sorgente e riga 5 appartengono al porto `13 mod18`, riga 6 a `853 mod1152`. Quindi 5 e 6 sono davvero i primi due ritorni. Il primo guadagno è `573606+3299328t`, mentre la discesa finale rispetto alla sorgente è `59082+339840t`.

È la deduzione su carta già registrata in `notes/post_v6_reset_2026-09-26/CRITICAL_MAP_IT.md:72`, ora ricontrollata aritmeticamente; non una nuova dichiarazione Lean. La pendenza totale `729/1024` rende già applicabile la barriera esistente: prima di contare una nuova famiglia va confrontata la copertura pregressa.

## Corollario esplicitato durante questa revisione

Per ogni r≥1 e t≥1, definiamo

`x_j=18t·8^(r−j)9^j−5`, per `0≤j≤r`,

`y_j=216t·8^(r−j−1)9^j−7`, per `0≤j<r`.

Allora `S(x_j)=y_j`, con esponente 1, e `S(y_j)=x_(j+1)`, con esponente 2. Tutti gli x_j sono `13 mod18`. Tutti gli y_j sono `65 mod72`, mentre la sezione E ammette solo residui contenuti in `{5,13,29,31,37,49,53,61,67}` modulo 72. Quindi ciascuno di questi segmenti di due passi è un **primo ritorno** a E. Inoltre

`x_(j+1)−x_j=18t·8^(r−j−1)9^j>0`.

Esistono pertanto arbitrariamente molti primi ritorni consecutivi, tutti crescenti. Nessun numero fissato di ritorni alla sezione assicura discesa. Questo dettaglio non è contenuto nella sola formulazione del noDrop a orizzonte fisso: occorre anche la verifica dell'appartenenza dei punti intermedi. È tuttavia un corollario elementare dell'aritmetica delle torri già formalizzata, senza rivendicazione di novità bibliografica.

Stato **C/E**: deduzione simbolica su carta e test esatto di 180 coppie di passi per `r=1..8,t=1..5` (40 coppie di parametri), tutti superati. Non è F: nessuna nuova dichiarazione Lean né compilazione svolta in questa analisi.

## Tre strade operative

### 1 Domini esatti e certificati di ritorni composti

Costruire un formato di certificato composto da dominio aritmetico, parola esatta, tempi dei ritorni, certificati di non appartenenza intermedia, endpoint affine e relazione di rango. Il primo lemma utile è un teorema di composizione: se una cella `a+Mt` arriva in una seconda cella con parametro `t'=p+qt`, le prove di matching e dei ritorni si concatenano preservando il dominio esatto. Un secondo lemma deve identificare il complemento delle celle coperte; non basta elencare esempi favorevoli.

Test iniziale: verificare il pilota e una famiglia già nota, rifiutare deliberatamente una parola con valutazione non esatta e una pretesa di primo ritorno con punto intermedio in E. Misurare l'incremento di copertura come differenza esatta tra unioni di progressioni. Priorità alta per ottenere risultati limitati e riutilizzabili; prospettiva globale incerta. Arresto se le celle nuove duplicano il già coperto o se si aumenta soltanto il modulo.

### 2 Compressione del numero non limitato di ritorni crescenti

Formalizzare prima il corollario x_j/y_j sopra: impone il requisito corretto a ogni futuro sintetizzatore. Per t dispari, la forma canonica ha `ν₂(x_j+5)=3(r−j)+1`, quindi il contatore di blocchi si riduce esattamente mentre il cofattore si moltiplica per 9. Questo dà un clock strutturale autentico all'interno della macro, non una discesa dell'intero.

Il lemma successivo da cercare è un'interfaccia di uscita che porti lo stato finale `18t9^r−5` in una famiglia con parametro o rango realmente inferiore. Dichiarare separatamente tutti i vincoli sui fattori 2 e 3 e la durata della coda. Test avversario: far variare r mantenendo t piccolo e viceversa, includendo uscite con clock riacquistato elevato. Arresto se il reset richiede già un'ipotesi globale di discesa o produce una nuova coda non controllata. È un programma a rischio alto, più fedele alla struttura osservata di un numero fissato di ritorni.

### 3 Rango su stati parametrici con verifica delle transizioni di reset

Una volta ottenute alcune interfacce d'uscita, cercare un rango lessicografico su parametri espliciti, oppure un criterio di terminazione basato sulla diminuzione di almeno un parametro lungo ogni ciclo del grafo delle macro. Il primo lemma deve dimostrare che ogni arco del grafo proviene da una macro valida e che ogni punto del dominio possiede un arco applicabile. I cicli del solo quoziente finito non certificano cicli della dinamica reale.

Test: usare i blocchi crescenti del corollario per escludere subito il rango n e ogni conto alla rovescia limitato di ritorni; usare il pilota per ammettere crescita intermedia. Verificare tutte le transizioni di reset simbolicamente, comprese le classi residue scartate. Arresto se un arco indispensabile ha coefficiente espansivo e nessuna diminuzione parametrica dimostrata, oppure se la copertura universale viene assunta. Rischio alto; un esito locale può comunque essere un certificato indipendente per una nuova sottofamiglia.

Nessuna delle tre proposte costituisce una nuova prova globale. La prima è il prossimo lavoro più concreto; la seconda chiarisce un'ostruzione che le future ricerche devono rispettare; la terza ha senso solo dopo aver dimostrato le interfacce di uscita.
