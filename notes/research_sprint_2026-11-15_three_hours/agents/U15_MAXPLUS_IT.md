# U15 — Profilo canonico e cammini calibrati del massimo aritmetico

Sessione aggiuntiva del 15–16 novembre 2026, base `203cbb8`. Prove su carta, da revisione indipendente; nessuna modifica Lean, risorsa esterna, GPU o nuovo esperimento. Il massimo F e il surplus sono quelli di U12. Non viene dimostrato il lower necessario a escludere divergenza e non si rivendica priorità bibliografica globale per la teoria max-plus.

## 1. Definizione e ingredienti

Si lavora sui positivi dispari unità, cioè non divisibili per 3. Una parola effettiva w da u a n ha gain `Ω(w)=3^k/2^A`, k=lunghezza, A=totale. Il progetto verifica `uΩ≤n`. Porre

`F(n)=max{Ω(w): u è unità positiva, w:u→n effettiva}`.

La parola vuota dà F≥1. Il massimo esiste perché i word con Ω≥1 formano un catalogo finito, anche per target periodici: è l'ingrediente di `BoundedSlopeCatalogue`. Inoltre F(n)≤n e ogni seed ottimale soddisfa u≤n/F(n). Una finitezza esistenziale non rende computabile il massimo: per escludere piccoli seed non basta un timeout.

Per un genitore unità x di n, con esponente e, porre `M_x(n)=(3/2^e)F(x)`. Si ha `F(n)=max(1,sup_x M_x(n))`. Se F(n)>1 il massimo è realizzato in almeno un ramo. La somma `LF=Σ_xM_x` è finita usando il floor e l'armonicità della vera traccia g; alternativamente basta il lower uniforme della densità dei predecessori usato da U12. Il surplus è A=LF−F, nonnegativo quando F>1.

## 2. Un profilo canonico, non un massimo delle lunghezze

**Lemma.** Tutte le parole che realizzano F(n) hanno esattamente la stessa lunghezza K(n) e lo stesso totale E(n).

Infatti, `3^k/2^A=3^r/2^B` implica `3^k2^B=3^r2^A`, quindi k=r e A=B per le valutazioni ai primi 3 e 2. La frazione è ridotta, e K(n) è la valutazione ternaria del numeratore di F(n); E(n) è quella binaria del denominatore.

Per F(n)=1 l'unico profilo è (0,0), dunque l'unica parola ottimale è quella vuota. Non esiste un ritorno nonvuoto di gain uno.

**Lemma.** Ogni seed u che realizza F(n) soddisfa F(u)=1. Ogni prefisso u→z di quella parola è calibrato: `F(z)=Ω(u→z)`.

Se F(u)>1, comporre un witness migliore verso u con il cammino u→n migliorerebbe F(n). Lo stesso argomento a uno stato intermedio z dimostra la calibrazione. Tutti gli stati sono unità, come richiesto al seed del witness composto.

Ogni genitore ottimale x di n soddisfa pertanto

`K(n)=K(x)+1`, `E(n)=E(x)+e`.

La policy inversa che sceglie un genitore ottimale e si arresta quando F=1 termina dopo ESATTAMENTE K(n) passi, anche in presenza di target periodici. Tutti i cammini ottimali hanno questo clock; non occorre prendere il massimo delle loro lunghezze. Nessun bound effettivo di K in funzione dell'altezza è stato ottenuto.

Un cammino ottimale non contiene cicli: rimuovere un ciclo ne aumenta il gain, perché il prodotto di gain lungo un ciclo positivo è strettamente minore di uno. Equivalentemente, la calibrazione attorno a un ciclo imporrebbe F=βF con β<1. Quindi gli ottimali sono di primo arrivo e ammettono il prodotto correttivo uniforme P₀=exp(27).

## 3. Stabilizzazione su una ipotetica spine divergente

Sia `n_j=S^j(b)` una spine divergente con b unità e sia `Ω_j=Ω(b→n_j)`. Il prodotto esatto dà `n_j=bΩ_jP_j`, con `1≤P_j≤P₀`. Poiché F(n_j)≥Ω_j, ogni seed ottimale di n_j è al più bP₀.

I candidati sono quindi un insieme FINITO U. Per ogni u∈U che interseca la spine esistono un primo indice r(u) e una parola u→n_r. Per j≥r(u), la parola da u a n_j è unica: un secondo tempo di arrivo a un root nonperiodico darebbe un ritorno. La composizione dà

`Ω(u→n_j)/Ω_j=Ω(u→n_r)/Ω_r=:c_u`,

esattamente costante. I candidati che non intersecano mai la spine non partecipano. Superato il massimo dei finitissimi r(u), e superati gli n_j≤bP₀ che possono fornire l'ottimo vuoto, si ha

**`F(n_j)=C_*Ω_j`**, `C_*=max_(u∈U)c_u`.

L'insieme dei seed ottimali si stabilizza. Con tie-break sul minimo seed, anche il seed scelto si stabilizza. Se k_u è il tempo di arrivo di u al punto n_r, le lunghezze sono j+k_u−r. L'unicità del profilo mostra che tutti i seed ottimali hanno lo stesso offset; dunque

**`K(n_j)=j+C_*'`** eventualmente.

Per j abbastanza grande l'unico genitore ottimale è il predecessore osservato n_(j−1): tutti i seed ottimali erano già entrati prima nella spine. Quindi

`F(n_j)=ω_jF(n_(j−1))`, `A(n_j)=Σ_(x≠n_(j−1))M_x(n_j)`.

Anche il secondo ramo diventa piccolo in senso relativo. Fissare δ>0. Un ramo con M_x≥δF(n_j) avrebbe un seed u≤bP₀/δ. I finitissimi possibili u entrano nella spine a finitissimi indici; oltre quegli ingressi nessuno può entrare da un ramo laterale. Pertanto

`max_(x≠n_(j−1)) M_x(n_j)/F(n_j)→0`.

Non si è ricavato un tasso: il massimo dei tempi di ingresso dei piccoli seed è proprio l'obbligo non uniforme già incontrato nelle prove del clock. La stabilizzazione non risolve quel problema.

## 4. Calibrazione infinita e due tipi diversi di rango

Dalla sezione precedente ogni eventuale divergenza produce una spine infinita interamente calibrata a partire da un seed F=1: scegliere un seed ottimale stabilizzato; ogni suo prefisso si può completare a un punto ottimale sufficientemente lontano.

Viceversa una traiettoria infinita calibrata non può entrare in un ciclo, per il prodotto β<1. Sui positivi, l'assenza di ripetizioni implica divergenza. Pertanto l'esclusione di tutte le spine calibrate infinite equivale all'esclusione della divergenza; non è stata promossa a un problema formalmente più debole.

La funzione K è un rango INTERO inverso: scende di uno seguendo un genitore ottimale. In avanti, su una spine calibrata, sale di uno. Non è un rango di terminazione forward.

Un secondo potenziale è `V(n)=n/F(n)`. Su un passo calibrato x→Sx,

`V(Sx)=V(x)+1/[3F(x)]`.

Su un cammino calibrato da u con F(u)=1, V=uP e quindi `u≤V≤uP₀`. Gli incrementi positivi sono sommabili. Anche questo non è un rango discreto: una crescita razionale stretta ma limitata non implica terminazione.

Il bound aperto `K(n)≤log_(3/2)(n+2)+C_ε` sui root grandi F(n)≥εn escluderebbe divergenza: sulla spine K=j+C_*', mentre il numero N(j) di esponenti almeno due tende a infinito e impone `log_(3/2)(n_j+2)≤j−N(j)+O_b(1)`. La finitezza del catalogo non fornisce questo bound.

## 5. Un budget puramente aritmetico per i singoli rami laterali

Per ogni occorrenza di un genitore laterale x di n_j scegliere un seed unità u che realizza M_x(n_j). I seed scelti sono distinti fra tutte le occorrenze: i bacini laterali di una spine iniettiva sono disgiunti.

Dato `M_x(n_j)/n_j≤1/u`, per ogni p>1 e ogni famiglia finita di occorrenze,

`Σ_(j,x laterale)[M_x(n_j)/n_j]^p≤Σ_(u≥1)u^(−p)≤ζ(p)`.

A p=2 basta il budget elementare ≤2 già formalizzato nel progetto. Questo corollario della carica reciproca non usa la densità dei predecessori né g/Q. È però più debole del budget ℓ¹ per la SOMMA dei rami che U12 ricava con il lower di densità: non controlla da solo `Σ_j A(n_j)/n_j`.

## 6. Un test Bellman naturale, con limite esplicito

Se si usa anche g, porre Z=F/g. Il floor armonico dà `0<Z≤1/c₀`. L'identità esatta è

`QZ(n)−Z(n)=[LF(n)−F(n)]/g(n)=A(n)/g(n)`.

Su F>1 il drift è nonnegativo; sull'insieme infinito F=1 può essere negativo. Questo aggira soltanto la barriera dei test limitati con drift moltiplicativo uniforme fuori da un insieme FINITO. Non dimostra un drift quantitativo: il lower A richiesto rimane esattamente aperto. La finitezza di tutte le policy ottimali non prova che una catena Q che sceglie anche rami non ottimali raggiunga F=1 a tempo uniforme.

## 7. Perché non compare automaticamente una lingua Sturmian

Le parole ottimali da un seed F=1 massimizzano il gain a ogni prefisso. Ma per un FATTORE x→z la calibrazione confronta rivali usando anche F della loro sorgente:

`Ω(v→z)F(v)≤F(z)=Ω(x→z)F(x)`.

Non segue la stessa disuguaglianza sui gain nudi. Il certificato U13 su31→911 mostra esattamente questo limite: il prefisso è calibrato, mentre il fattore2429→911 di gain3/8 perde contro607→911 di gain3/2. Il confronto PESATO da F resta valido. Perciò la chiusura per fattori delle lingue pubblicate non si può importare senza una nuova ipotesi.

## Stato

Sono stati isolati un profilo ottimale canonico, una policy inversa propria e la stabilizzazione esatta; il clock uniforme e il surplus logaritmico restano aperti. Questi risultati sono proposti come raccordo strutturale, non come prova di Collatz o priorità globale. Nessun esperimento è stato aggiunto.
