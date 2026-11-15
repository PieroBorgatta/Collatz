# Collegamento fra packing, primo arrivo e altezza

Appunti di ricerca del coordinatore, 15 novembre 2026. Questo documento descrive il contenuto matematico dei nuovi moduli `WordProductEnvelope.lean` e `FirstArrivalBudget.lean`; le ricevute della compilazione integrata determinano la versione effettivamente verificata. La costruzione di una quota di immagini resta un problema distinto.

## Budget senza ipotesi analitiche esterne

T01 ha ricostruito il conteggio delle parità e formalizzato una stima universale per ogni segmento finito positivo iniettivo della mappa shortcut T. La somma dei reciproci dei suoi stati distinti è al più 133547/1655, quindi strettamente minore di 81. Il risultato ammette un singolo giro di un ciclo, contato senza ripetizioni; non ammette ripetizioni con molteplicità.

Il conteggio può essere verificato anche direttamente con le cinque classi j=5r+s: ponendo m_s=(0,0,1,1,2), le ragioni delle due serie sono 3125/3456 e 27/32. Le somme dei cinque coefficienti sono rispettivamente 3271/576 e 51/16. Con il limite conservativo della parte light si ottiene la costante dichiarata. Il coordinatore ha ricontrollato questa algebra con razionali esatti, indipendentemente dal programma T01.

## Ogni primo arrivo accelerato è un primo arrivo shortcut

Il tempo shortcut del punto accelerato S^k(u) è esattamente A_k, somma dei k esponenti effettivi. La funzione k↦A_k è strettamente crescente per sorgenti dispari. Dentro un episodio accelerato tutti gli stati shortcut strettamente intermedi sono pari. Un hit shortcut su un target dispari è quindi necessariamente un punto accelerato, con lo stesso clock esatto.

Da ciò segue che una parola di primo arrivo da u a n espande un segmento shortcut di primo arrivo. Per qualunque mappa deterministica, un segmento fino al primo arrivo è iniettivo: una ripetizione prima dell’endpoint anticiperebbe lo stesso arrivo applicando gli ultimi iterati. Le prove includono il tempo zero e target periodici. Non si assume che l’orbita successiva sia iniettiva.

Gli stati accelerati prima dell’arrivo sono un sottoinsieme degli stati shortcut del segmento espanso. Positività dei reciproci e iniettività dei clock trasferiscono il budget 81 alla somma sui passi accelerati. Questo collegamento è ora scritto in Lean, senza lasciare il budget come un input analitico.

## Prodotto esatto e controllo dell’altezza

Per gli stati x_i=S^i(u), i<k, definiamo

`P(u,k)=Π_(i<k)(1+1/(3x_i))`.

La moltiplicazione delle identità `2^(a_i)x_(i+1)=3x_i+1` dà esattamente

`P(u,k)=2^A n/(3^k u)`.

Dal limite sui reciproci e da 1+t≤exp(t) segue P≤exp(27). Per una parola effettiva di immagine w′ da v a y, la nonnegatività della sua costante affine dà

`v≤(2^A′/3^k′)y`.

Se k′=k e A′=A, otteniamo

`v≤(y/n) exp(27) u`.

Il sibling canonico soddisfa y≤16n+5≤21n per n>0. Ogni immagine esistente dello stesso profilo è quindi entro `21 exp(27) u`. Il limite non produce l’immagine e non garantisce che un numero sufficiente di sorgenti ne possieda una.

## Si possono cambiare anche lunghezza e totale

La stessa prova richiede soltanto

`2^A′ 3^k≤C 2^A 3^k′`, con C≥0,

e dà `v≤21 C exp(27)u` nel dominio del sibling. Questa condizione equivale a un limite sul rapporto dei coefficienti omogenei ρ=2^A/3^k, e permette k′ e A′ diversi. Una regione naturale dei cataloghi è quindi una fascia di A−k log₂3, invece del singolo profilo (k,A).

Questo criterio di costo non crea massa. Se anche la parola di immagine è di primo arrivo, i due prodotti sono fra 1 ed exp(27), e l’identità

`ρ′/ρ=(v/u)(n/y)(P′/P)`

mostra che il controllo del rapporto dei coefficienti e quello dell’altezza sono comparabili a costanti universali. Contare tutte le immagini entro un cutoff senza un nuovo confronto di capacità riproporrebbe dunque il problema iniziale. Il possibile vantaggio della fascia deve venire da una stima dei cataloghi aggregati o da una costruzione che controlli insieme costo, massa e collisioni.

## Confine dei risultati

Il limite 81 e il collegamento ai primi arrivi sono lemmi globali finiti formalizzati. La disuguaglianza d’altezza riguarda immagini già certificate. Le identità esterne fra traccia aritmetica, medie pesate e densità non sono importate. Nessuno di questi lemmi dimostra H, esclude le orbite divergenti o esclude i cicli non banali.
