# U15 — Rinnovo locale e ostacolo ai lower medi di h

Ultimo attacco al surplus su richiesta del coordinatore. Il risultato è una barriera specifica: positività o medie residue di h=g_1, anche rafforzate da un floor uniforme, non forzano un secondo ramo ladder nel solo sistema di rinnovo. Il modello negativo è dichiaratamente diverso dal grafo intero di Collatz. Non viene dimostrato il lower A richiesto.

## 1. Il kernel di primo record scende in altezza

Sia C(n) l'insieme delle parole inverse di PRIMO attraversamento stretto di1, con sorgente unità: il gain finale è a>1 e tutti i prefissi propri hanno gain≤1. È finito per il catalogo. L'ultimo passo che attraversa ha gain3/2, dunque 1<a≤3/2. Per ogni w∈C(n), la sorgente u_w<n. Definire

`Tf(n)=Σ_(w∈C(n)) a_w f(u_w)`.

L'identità capped dà esattamente `h=(I−T)g`, h=g_1>0. Le parole che terminano su un nuovo record si decompongono univocamente in successive parole di primo attraversamento relative; pertanto l'operatore dei record è T+T²+... . Sul sottoinsieme degli interi≤n questa somma termina, perché ogni nuovo record scende strettamente di altezza. Si recupera g=(I−T)^(-1)h come somma finita al target n.

Anche il massimo aritmetico ha la ricorrenza

`F(n)=max(1,max_(w∈C(n)) a_w F(u_w))`.

Se una parola ottimale ha gain>1, il suo primo attraversamento relativo di1 è in C e il resto deve essere ottimale al nuovo root. L'implicazione opposta segue per composizione. Il kernel ladder g-trasformato ha probabilità a_wg(u_w)/g(n) e viene ucciso con probabilità h(n)/g(n); scende strettamente e assorbe entro il numero degli stati interi minori di n. Questo è un rango dei RECORD, non un bound sui passi inversi tra due record.

## 2. Il nuovo collegamento high-tail rende il rinnovo locale

Questo paragrafo riguarda target NONRETURN. Per w:u→n di primo attraversamento inverso, di gain a, sia G_i il gain del prefisso FORWARD u→x_i. Per i≥1 il suffisso verso n è un prefisso inverso proprio e ha gain a/G_i≤1. Quindi G_i≥a>1 e tutti gli stati non iniziali x_i sono almeno a u>u.

Il budget high-tail U09 sui cammini iniettivi applicato a questi stati dà P(u→n)=1+O(u^(−δ)) per un δ>0 assoluto del risultato high-tail. Ne segue

`n/u=aP≤3/2+O(u^(−δ))`, quindi `u≥(2/3−O(n^(−δ)))n`.

Per passare da u a n nella stima d'errore si usa prima il bound di primo arrivo u≥n/[(3/2)P₀]. La località è uniforme nella lunghezza del crossing. Non è estesa a parole che ripetono cicli senza pagare il relativo fattore. La correzione locale P→1 non impone ancora un altro colore di primo ramo.

## 3. Un modello triangolare con h uniformemente positivo e F heavy

La costruzione seguente conserva il rinnovo triangolare, la località della sezione2, monomi di gain del tipo3^k/2^E e tutte le sue conseguenze puramente algebriche. Non conserva il vero offset affine di ogni parola Syracuse, l'insieme completo dei genitori interi o i loro colori fisici. Serve precisamente a non attribuire a quei soli input un lower che richiede gli input omessi.

Prendere un intero dispari unità n₀≥100. Definire n_j come la massima unità dispari≤(3/2)n_(j−1)−3. I gap fra unità dispari sono≤4; dunque n_j>(3/2)n_(j−1)−7 e n_j cresce almeno geometricamente, con n_j/n_(j−1)→3/2.

Scegliere per ogni j un monomio a_j=3^k/2^E nell'intervallo aperto

`(n_j−2)/n_(j−1) < a_j < (n_j−1)/n_(j−1)`.

Tale scelta esiste per la densità dei monomi, conseguenza dell'irrazionalità log2/log3. Si possono scegliere k grandi ed E fra k e2k, quindi il monomio è il gain di qualche parola di esponenti1 e2. Inoltre 1<a_j<3/2. La costruzione non afferma che quella parola colleghi proprio i due interi n_(j−1),n_j.

Sul sistema di tutte le unità positive, porre un solo arco T da n_j a n_(j−1), di coefficiente a_j; nessun arco dagli altri stati. Porre

`g(n_j)=n_j/n₀`, `h(n_j)=[n_j−a_jn_(j−1)]/n₀` per j≥1,

`g(n₀)=h(n₀)=1`, e `g(n)=h(n)=1` fuori dalla catena.

Si ha esattamente h=g−Tg, 1/n₀<h≤1 su tutti gli stati, 1≤g(n)≤n. Poiché la catena ha solo O(log X) stati≤X, la media di h tende a1 in OGNI classe residua contenente infinitamente molte unità, con la media presa sulle unità di quella classe. Quindi non manca soltanto la positività puntuale: il modello ha un floor e medie residue massimali.

Il massimo del modello è F(n₀)=1, F(n_j)=a_jF(n_(j−1)), F=1 altrove. Scrivendo d_j=n_j−a_jn_(j−1)∈(1,2),

`F(n_j)/n_j=(1/n₀)∏_(i=1)^j(1−d_i/n_i) →D/n₀>0`,

perché Σ_i d_i/n_i<∞. La catena è quindi uniformemente heavy. Inoltre il fattore di correzione del singolo arco è

`P_j=n_j/[a_jn_(j−1)]=1+O(1/n_j)`,

più forte di una località P=1+O(n^(−δ)) con δ≤1. Eppure sul root heavy il primo ladder ha UN SOLO ramo e il suo surplus somma−massimo è esattamente zero.

## 4. Implicazione per il tentativo sul surplus reale

Il modello dimostra che nessun lower aggregato di h su classi residue, e nemmeno un floor di h su tutti gli interi, obbliga da solo un secondo ramo ladder quando si usa soltanto rinnovo, località per altezza e gain monomiali. Il vero A=LF−F distingue i PRIMI RAMI FISICI: più record nello stesso ramo non si sommano come nuovi M_x. Per trasferire il rinnovo a un lower di A occorre una proprietà aggiuntiva che separi quei colori e conservi l'offset intero della parola, oppure una stima condizionata alla classe heavy che forzi un altro bacino piccolo. Le medie non condizionate di h non la forniscono.

Il modello non è un controesempio Collatz e non confuta un argomento che utilizzi l'offset effettivo o un certificato robusto per colori. Individua esattamente perché il tentativo basato sul solo h positivo e sulla triangolarità si arresta.

## Convenzione sugli upper della traccia

Dove gli altri addenda U15 usano g≤Cn, lo dichiarano come ipotesi oppure lavorano su spine divergenti/root nonreturn. L'upper esterno senza fattore di ritorno non viene qui attribuito ai target periodici; su quelli la fonte porta un fattore ciclico. Le identità capped/Doob e di rinnovo non hanno usato questo upper.
