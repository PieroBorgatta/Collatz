# U14 — Un verificatore adattivo completo per lower stretti del surplus

16 novembre 2026. Programma su carta, senza esecuzione di nuovi scan, Lean, GPU o modifica dei programmi esistenti. Questa nota dà una scelta adattiva precisa e la sua completezza a target fissato; non dimostra il lower globale e non rivendica novità algoritmica. È un dovetail di cammini effettivi con un contratto verificabile.

## 1. Input e stato

Input: un intero positivo dispari unità n e una soglia razionale `ℓ>0`. Si usano i risultati U12: F è un massimo, ogni massimo di ramo `M_x=ω_xF(x)` è raggiunto da una parola finita, e LF è finito. Non si assume che esista un seed sotto `O(log n)`, né un cutoff dei suoi tempi di arrivo.

Per la fase t≥0 porre

`K₀(n)=min{K≥0:3^K≥(n+1)2^K}`,

`K_t=K₀(n)+t`, `U_t=(n+1)2^t`.

K₀ è computabile con confronti interi. È almeno `log_(3/2)(n+1)`, quindi l'orizzonte scelto supera già la barriera necessaria del precedente addendum. Entrambi i budget crescono senza limite; la crescita del cutoff dei seed è parte dell'algoritmo, non un'ipotesi sui seed che dovrebbero bastare.

Per ogni primo genitore dispari x di n conservare un record `v_x`, inizialmente zero: il massimo gain trovato in quel ramo, con seed e parola che lo attestano. Si conserva anche l'esatto totale dei v_x, la coordinata massima e quindi `R_t=Σv_x−maxv_x`. I rami senza record hanno valore zero.

## 2. Una fase finita, completamente specificata

1. Per ciascun seed positivo dispari unità `u≤U_t`, eseguire al più K_t iterazioni Syracuse esatte. Le esecuzioni precedenti possono essere riusate.
2. Per ogni visita a n a tempo `1≤k≤K_t`, registrare l'ultimo stato x prima di n, il totale A degli esponenti e `Ω=3^k/2^A`. Aggiornare `v_x←max(v_x,Ω)`; se il massimo non aumenta, il witness nuovo non aggiunge massa.
3. Confrontare R_t con ℓ. Arrestare con successo se esiste un witness di gain>1 e `R_t>ℓ`. Restituire un witness per ciascun ramo presente e tutti i confronti razionali `Σ_(x≠b)v_x>ℓ`.
4. Altrimenti aumentare t. Un mancato hit, un timeout o una fase senza miglioramenti non è un certificato negativo.

La visita a tempo zero è la parola vuota e non viene registrata in alcun ramo. Le visite ripetute, anche su cicli, sono ammesse nei K_t passi e raggruppate per il medesimo primo ramo; non occorre fermare o classificare un ciclo. Tutte le parole prodotte sono effettive per costruzione. Non vengono sommati due witness del medesimo ramo.

## 3. Correttezza e completezza a root fissato

Ogni record è un lower del vero M_x. Il test di gain>1 attesta `F(n)>1`, senza dover conoscere F esattamente. La monotonia di `R(v)=Σv−maxv` implica quindi `A(n)≥R_t>ℓ`: ogni successo è un certificato esatto finito, verificabile ripetendo soltanto i cammini restituiti.

Ogni parola effettiva finita ha seed e lunghezza finiti. Entrerà dunque in una fase, poiché U_t e K_t tendono entrambi a infinito. In particolare ogni massimo M_x viene prima o poi raggiunto dal record del suo ramo. I record crescono coordinata per coordinata. La convergenza monotona, con `ΣM_x=LF<∞`, dà

`Σ_xv_x(t)↑LF(n)`.

Se F>1, una parola che realizza F è non vuota ed entra in una fase finita. Da allora la coordinata massima è esattamente F, anche se il verificatore non sa che non esistono miglioramenti futuri. Ne segue

`R_t↑LF(n)−F(n)=A(n)`.

Pertanto **se F(n)>1 e A(n)>ℓ, la procedura termina con successo**. Non serve un piccolo seed postulato: la completezza usa soltanto l'esistenza dei massimi finiti e la sommabilità dei rami. Il caso A≤ℓ può non terminare, e non viene trasformato in una decisione negativa. La stessa conclusione vale raggruppando per primo esponente, che al target n determina univocamente il genitore x.

## 4. Scale e costo: ciò che questo evita, ciò che lascia aperto

Una fase usa al più `U_tK_t` passi forward, prima del riuso; non è una stima del tempo pratico. L'ineguaglianza `S(y)+1≤(3/2)(y+1)` limita la grandezza degli interi visitati a `(3/2)^(K_t)(U_t+1)`. I loro bit sono `O(log(n+1)+t)`. Anche il gain può essere mantenuto esattamente mediante (k,A): dal telescopio `2^A≤4^k u/y_k` segue `A≤2K_t+log₂U_t` per gli stati positivi. Non serve aritmetica approssimata per validare un witness.

Una soglia analitica `c n/(1+log n)` si può sostituire da una maggiorazione razionale certificata; il margine stretto consente di raffinare tale maggiorazione. Non basta arrotondare informalmente un confronto vicino alla soglia.

Il contratto supera il difetto di un orizzonte fisso e produce **vera crescita sia della profondità sia della scala delle sorgenti**. Non fornisce però una funzione nota che maggiori la fase di successo in termini di n e ℓ. Per passare a un teorema uniforme occorre dimostrare che il lower desiderato è vero, oppure controllare il tasso di convergenza dei record al surplus: nessuno dei due segue da questa completezza.

L'obiettivo di ricerca più preciso è quindi una stima quantitativa per questo processo colorato, eventualmente su blocchi di una vera spine, non un nuovo scan indistinto di più antenati. Il punto da misurare o provare è l'aumento del **totale dopo rimozione del ramo migliore**, con costo di profondità e scala conservato. Il numero di parole, di hit o di seed che migliorano soltanto il ramo dominante non è progresso per quel contratto.

## Stato dell'audit

**U04: PASS** su correttezza, completezza per soglie strette con F>1 e LF finito, finitezza delle fasi e bound dei bit. Nessun rate uniforme o certificato negativo segue. Non è stato eseguito alcun nuovo censimento né ottenuto un lower uniforme.
