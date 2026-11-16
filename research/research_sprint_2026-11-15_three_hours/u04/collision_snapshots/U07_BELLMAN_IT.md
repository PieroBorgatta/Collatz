# U07 — Bellman e una quantità fisica a due copie

Sessione del 15–16 novembre 2026, base `203cbb8`. Questa nota contiene deduzioni su carta. Non modifica Lean e non dimostra un lower relativo o la congettura di Collatz. Il contributo locale proposto è un criterio di nonconcentrazione del vero kernel inverso; non si rivendica che il principio probabilistico sia nuovo nella letteratura.

## 1. Dominio e input

Si lavora sui positivi dispari non divisibili per tre. La traccia canonica g è positiva e soddisfa

`g(n)=Σ_e ω_e g(I_e(n))`, `I_e(n)=(2^e n−1)/3`, `ω_e=3/2^e`,

sommando soltanto i rami interi con endpoint unità. Il kernel di Doob del progetto è

`Q(n,I_e(n))=ω_e g(I_e(n))/g(n)`.

Nella [fonte primaria12](https://rstation.ai/problems/collatz/papers/12) questo kernel è chiamato **P_h**. Il simbolo Q della fonte indica invece una seconda legge costruita dalle densità naturali; le due notazioni non vanno confuse.

Per i target senza ritorni si usa l'upper esterno `g(n)≤Cn`. Per segmenti di primo arrivo positivi e iniettivi, il progetto verifica il bound del prodotto correttivo `1≤P≤P₀=exp(27)`. Questi input, più l'armonicità, bastano al criterio a due copie. Non servono un rate Haar, una minorazione uniforme del floor o un bound del tempo di rilassamento.

## 2. Due copie: endpoint fisici, non conteggi di parole

Definire il difetto di collisione di un passo

`D(n)=1−Σ_y Q(n,y)²`.

È la probabilità che due scelte indipendenti del genitore reale siano diverse. Porre inoltre

`H₂(n)=−log Σ_y Q(n,y)²`,

così `0≤D(n)≤H₂(n)`. Sono statistiche del vero kernel, non della legge geometrica indipendente degli esponenti.

Il kernel sub-Markov `T(n,y)=Q(n,y)²` segue le due copie finché scelgono lo stesso genitore, e le uccide al primo split. Per ogni m,

`T^m1(n)=P(le due copie coincidono attraverso m passi)=Σ_u Q_n(Y_m=u)²`.

L'ultima uguaglianza è specificamente fisica: se due cammini inversi della stessa lunghezza finiscono nello stesso intero u, la deterministica orbita forward di u ricostruisce tutti gli stati e tutte le valutazioni. I cammini coincidono. Pertanto una collisione fra endpoint allo stesso tempo non può essere una collisione fra etichette differenti.

Introducendo l'operatore quadratico

`K₂F(n)=Σ_e ω_e² F(I_e(n))`,

si ha esattamente

`T^m1(n)=K₂^m(g²)(n)/g(n)²`.

L'armonicità positiva implica `K₂(g²)≤g²`, quindi tutte queste quantità sono finite anche senza integrabilità globale di g². Se

`C_g(n)=g(n)²−K₂(g²)(n)=g(n)²D(n)`,

il telescopio finito dà

`g(n)²=Σ_(j<m)K₂^j C_g(n)+K₂^m(g²)(n)`.

È una decomposizione di potenziale per il primo split. Una serie infinita senza resto richiederebbe l'ulteriore nonatomicità della legge sui cammini; non è necessaria alle conclusioni seguenti. La finitezza del Green quadratico non basta da sola a controllare il resto che contiene g².

## 3. Summabilità forzata lungo una ipotetica spine divergente

Supporre che `n_j=S^j(u)` sia una spine divergente di unità. Scrivere `Ω_j=3^j/2^(e₁+…+e_j)` e `n_j=Ω_j uP_j`, con `1≤P_j≤P₀`. Porre

`R_j=P_j g(n_j)/n_j`.

La probabilità di scegliere il predecessore osservato è

`p_j=Q(n_j,n_(j−1))=R_(j−1)/R_j`.

Per armonicità, R_j è nondecrescente. L'upper lineare della traccia dà `R_j≤CP₀`, mentre `R₀=g(u)/u>0`. Dunque `R_j↑R_∞∈(0,∞)` e

`Σ_(j≥1)(1−p_j)≤Σ_(j≥1)−log p_j=log(R_∞/R₀)<∞`.

Inoltre

`H₂(n_j)≤−2log p_j`, `D(n_j)≤1−p_j²≤2(1−p_j)`.

Si ottiene il vincolo necessario

**`Σ_(j≥1) H₂(n_j)≤2log(R_∞/R₀)<∞`**, e quindi **`Σ_j D(n_j)<∞`**.

La conclusione non deriva dalla sola positività di ogni ramo: le probabilità dei rami alternativi possono essere positive ma sommabili lungo una spine. Usa l'upper lineare per rendere R limitata.

## 4. Due criteri sufficienti precisi

### Un lower locale di diversità

Per ogni ε>0, supporre esistano c_ε>0 e N_ε tali che ogni target unità n≥N_ε senza ritorni con `g(n)≥εn` soddisfi

`D(n)≥c_ε/(1+log n)`.

Allora non esiste una spine divergente nel quadro degli input dichiarati.

Infatti, lungo una tale spine,

`g(n_j)/n_j=R_j/P_j≥R₀/P₀=:ε_u>0`.

Inoltre `n_j+1≤(3/2)^j(u+1)`, perciò `1+log n_j≤C_u(1+j)`. Il lower renderebbe `Σ_jD(n_j)` divergente, in contraddizione con il §3. Vale lo stesso criterio con H₂ al posto di D.

Il criterio misura massa complessiva fuori dal ramo dominante, senza scegliere un sibling particolare. **Il lower di diversità non è stato dimostrato.** Non si afferma che questa ipotesi sia globalmente più debole di H: i quantificatori e le altezze delle radici sono diversi.

Precisamente, se x→n è un passo forward e y è il sibling canonico di x, allora le loro probabilità come genitori di n soddisfano `p_y/p_x=4^(−t)g(y)/g(x)`, con t∈{1,2}. Un confronto di tracce `g(y)≥κg(x)/(1+log x)` implica

`D(n)≥2p_xp_y≥κp_x²/[8(1+log x)]`.

Sulla spine divergente p_x→1, e questo dà la stessa contraddizione per summabilità, con il logaritmo dell'altezza del **figlio** x. Senza un confronto fra x e n non è una prova del lower pointwise nel logaritmo di n. Viceversa un lower di D non identifica il sibling canonico, né costruisce un trasporto con altezza e carico controllati; non implica di per sé H.

### Un gap di collisione entro l'orizzonte critico

Una seconda condizione sufficiente è: per ogni ε>0 esistano η_ε>0, C_ε e N_ε tali che ogni target n nel dominio precedente ammetta un m(n) con

`m(n)≤log_(3/2)(n+2)+C_ε`,
`Σ_u Q_n(Y_(m(n))=u)²≤1−η_ε`.

La prova è diretta. Sulla spine sia N(j) il numero di esponenti almeno due prima di j. Si ha N(j)→∞ e

`n_j+1≤(u+1)(3/2)^(j−N(j))`.

Quindi `j−m(n_j)≥N(j)−O_u(1)→∞`. La probabilità di ripercorrere la spine fino a quell'indice è

`R_(j−m(n_j))/R_j→1`.

L'endpoint prescritto ha pertanto probabilità tendente a uno, e la collisione degli endpoint è almeno il suo quadrato, tendente a uno. Contraddizione.

Questo criterio evita la scelta dell'osservabile 1/g e richiede un vero risultato di nonconcentrazione fisica. Non è fornito da un bound del numero dei codici, da un routing verso una classe modulare o dal solo spettro Haar.

Anche il confronto con il criterio precedente sul reciproco della traccia va limitato al suo uso sulla spine: in generale una legge quasi concentrata su un endpoint a g piccolo può avere grande aspettativa di 1/g, mentre una legge diffusa può essere sostenuta su endpoint tutti a g grande. Non si dichiara un'implicazione globale fra i due lower. Il medesimo backtracking pesante rende entrambi sufficienti a escludere divergenza.

**Forza logica del criterio.** Aggiungendo il tail sui label minimi del §5, si ottiene una tightness uniforme: per ogni ε>0 tutti i root pesanti hanno un antenato fra un numero finito di piccoli interi. Infatti scegliere M tale che il bound di eq(36) sia minore di uno; qualche genitore di probabilità positiva ha allora `m_*≤M`, quindi un intero q≤M raggiunge n. Se tutte le orbite fossero eventualmente periodiche, l'unione delle orbite dei q≤M sarebbe finita. I root pesanti nonperiodici sarebbero dunque finiti e il quantificatore “ogni root pesante sufficientemente grande” diventerebbe vacuo. In quel quadro esterno i criteri sono equivalenti all'esclusione delle spine divergenti, non risultati formalmente più deboli già quasi acquisiti. Questa direzione inversa non viene dedotta dai soli input del §1.

## 5. Bilancio entropico e lower più deboli per Shannon

Ponendo `r(n)=g(n)/n`, su ogni ramo vale

`log[r(I_e(n))/r(n)]=log Q(n,I_e(n))+log(1+1/(3I_e(n)))`.

La correzione è nonnegativa e al più `log(1+1/(2n−1))`. Di conseguenza

`E_n log[r(Y₁)/r(n)]=−H(Q(n,·))+E_n log(1+1/(3Y₁))`.

La formula non separa `E log g(Y₁)` da `E log Y₁`, che potrebbero non essere singolarmente finite. È ben definita anche con entropia infinita come aspettativa estesa; il Corollario12 della fonte citata garantisce l'entropia finita nel quadro canonico. Non è stato assunto un momento della valutazione e₁.

Una variante per Shannon usa un input supplementare della medesima fonte, §12 eq(36). Per un genitore x, sia `m_*(x)=min P(x)` il minimo **predecessore** nel suo bacino: non il minimo futuro della sua orbita. Al root nonperiodico i label m_*(x) dei diversi genitori sono distinti, e

`P_(h,n)(m_*(Y₁)>M)≤C_A/β_n·(log M)^(−A)`, `β_n=g(n)/(κn)`.

Quindi sui root pesanti g(n)≥εn, tutti i momenti di `log m_*(Y₁)` sono limitati uniformemente in n. La giustificazione usa l'unione dei bacini dei genitori in una sola first-landing cell, non una somma di stime separate per singoli atomi. Gli input di first passage e densità della fonte restano espliciti; nessun loro progetto è stato ricompilato qui.

Se un genitore ha probabilità 1−q, codificare gli altri label con `1/(ζ(2)m²)`. Gibbs e Hölder danno, per ogni p>1,

`H(Q(n,·))≤C_(ε,p) q^(1−1/p)`.

Infatti il contributo fuori dal genitore principale è al più

`2E[log m_*;off]+qlogζ(2)+qlog(1/q)`,

e `E[log m_*;off]≤(E(log m_*)^p)^(1/p)q^(1−1/p)`. Il contributo del genitore principale è al più q; anche `qlog(1/q)` è dominato da una costante p-dipendente per `q^(1−1/p)`.

Applicando questa stima a q_j=1−p_j del §3,

**`Σ_j H(Q(n_j,·))^(1+δ)<∞` per ogni δ>0**.

Perciò un lower uniforme `H(Q(n,·))≥c_ε/(1+log n)^a`, con un a fissato minore di uno, sui target pesanti sarebbe sufficiente a escludere divergenza. Scegliere δ>0 con `a(1+δ)≤1`. L'endpoint a=1 non segue da questo solo argomento. Il criterio di collisione del §4 è più economico negli input e raggiunge direttamente il denominatore log n.

## 6. Due classi di Bellman da scartare

Un test V globalmente limitato e positivo su tutti i grandi target unità nonperiodici non può soddisfare `QV≥λV`, λ>1, fuori da un insieme finito F. Per scegliere una root il cui albero inverso evita F, usare `a_k=(4^k−1)/3>1`, con 3∤k. Questi target arrivano a1 in un passo; un'orbita forward può contenerne al più uno. Qualche a_k non appartiene quindi all'unione delle orbite forward di F. Tutti i suoi antenati evitano F e sono nonperiodici. L'iterazione imporrebbe `E[V(Y_m)]≥λ^mV(a_k)`, impossibile per il bound globale.

Questo è un principio di massimo standard sul grafo reale. Esclude anche correzioni con conduttore crescente quando il test risultante rimane limitato; non richiede periodicità modulare del test. Non esclude un drift fuori dall'insieme **infinito** `{g≤B}`, né tempi di prova dipendenti dall'altezza.

Anche un ansatz superarmonico `F(n)=n^θc(n)` con 0≤θ<1 e `0<c≤c(n)≤C` non può soddisfare `LF≤F` su tutti i grandi target unità. Il corridoio inverso da `a_K=2·3^K−1` ha K−1 passi tutti1 e termina in `b_K=3·2^K−1`; tutti i punti del corridoio tendono a infinito con K. La singola parola implica

`F(a_K)≥(3/2)^(K−1)F(b_K)`.

La comparabilità a n^θ renderebbe il rapporto dei due membri almeno una costante per `(3/2)^((1−θ)K)`, contraddizione. Ciò resta vero se c dipende da una precisione ternaria crescente: una correzione uniformemente limitata non basta. Il meccanismo dell'ancora negativa e la sua scala sono già discussi nelle fonti; questa è una barriera per l'ansatz, non una nuova soluzione.

La barriera resta valida se l'ansatz è richiesto soltanto sui target senza ritorni. In quel caso usare la famiglia esplicitamente convergente già pubblica `A_K=(2^(3^K+1)−1)/3`. Si ha S(A_K)=1 e `ν₃(A_K+1)=K`; esistono ancora K−1 passi inversi tutti1 fra unità, e tutti gli antenati di un root senza ritorni sono senza ritorni. Il medesimo rapporto esponenziale diverge indipendentemente dall'enorme altezza iniziale A_K.

Una barriera proposta dal coordinatore vale anche vicino al profilo critico. Se F è globalmente comparabile a `n/[log(n+1)]^s`, gli esponenti con genitore unità sono due classi modulo6. Per n grande,

`ω_eF(I_e(n)) ≍ n/[log n+e log2]^s`.

Per s≤1 la serie LF(n) diverge. Per s>1, confrontandola con l'integrale di quella serie, `LF(n)≍_s n(log n)^(1−s)` e quindi `LF(n)/F(n)≍_s log n→∞`. Già gli esponenti fra `ceil(log n)` e `2ceil(log n)` danno il lower sufficiente. Nel profilo puro `F(n)=n/(log n)^s` il rapporto è asintotico a `log n/[3log2(s−1)]`. Una correzione compresa fra due costanti positive non cambia l'ostacolo.

Questo non confuta la possibile disuguaglianza `g≤F`: una maggiorante di g non deve per forza essere essa stessa superarmonica. Confuta soltanto la ricerca di una super-soluzione globalmente comparabile a quel profilo. Vale anche restringendo l'ansatz ai target senza ritorni, perché ogni loro antenato rimane senza ritorni.

## 7. Un certificato aritmetico con due piccoli seed

Supporre anche il floor g(u)≥c₀ sulle unità. Siano x₁,x₂ due diversi genitori unità di un root n senza ritorni. Se esistono due sorgenti unità u₁,u₂≤L con cammini effettivi che entrano in n passando rispettivamente da quei genitori, allora

`Q(n,x_i)≥c₀/(C P₀u_i)≥a/L`, `a=c₀/(C P₀)`.

Infatti la probabilità di seguire tutto il prefisso inverso fino a u_i è `Ω(u_i→n)g(u_i)/g(n)`, e il prodotto esatto dà `Ω≥n/(P₀u_i)`. Questa probabilità non supera quella del primo genitore. Le parole sono primi arrivi perché n non ha ritorni.

Due probabilità entrambe almeno α=a/L impongono α≤1/2 e impediscono un atomo oltre1−α. Più precisamente, isolando una delle due,

`D(n)≥2p_i(1−p_i)≥2α(1−α)≥α`.

Quindi un certificato di due rami con seed≤C_εlog n sui grandi root pesanti fornirebbe il lower del §4. È una domanda aritmetica finita, senza stima numerica di g: i seed devono davvero entrare da genitori diversi. Un unico piccolo seed non basta, e due source label che si fondono prima del root non sono due rami distinti. **Nessun bound logaritmico per il secondo seed è stato dimostrato.**

## 8. Routing crescente e prossima domanda utile

Il [paper37/v3](https://rstation.ai/problems/collatz/papers/37/v3), 26 ottobre, offre un esempio concreto di blocchi inversi correlati e Haar-preserving con costo di routing subesponenziale nella precisione ternaria. Controlla esistenza e costo di un percorso verso una classe, non il peso del vero kernel canonico su quegli endpoint.

Se una costruzione seleziona soltanto un subkernel R dei pesi critici e lo rende sub-Markov, `R^m1≤1`. Il suo contributo all'aspettativa reciproca è quindi al più `1/g(n)`; da solo non produce un lower uniforme quando g(n) è grande. La nonconcentrazione a due copie deve invece controllare le probabilità fisiche normalizzate dal vero g.

La domanda concreta rimasta è un lower del difetto quadratico normalizzato `C_g/g²`, oppure un gap di collisione fisica entro l'orizzonte critico. Le identità sopra eliminano alcuni proxy e riducono gli input del criterio, ma **non forniscono quel lower**. Un controllo finito può soltanto stressare un candidato; non può promuovere il criterio a prova.

Nessuna GPU è stata necessaria alla deduzione. Non è stata accertata una priorità bibliografica del criterio a due copie: l'operatore quadratico e il primo-split sono strumenti standard, qui ricostruiti nel dominio aritmetico del progetto.

## 9. Un solo diagnostico sulla griglia fisica già fissata

Il coordinatore ha autorizzato una misurazione aggiuntiva sulla medesima griglia U03, senza estenderla. Il protocollo U07 è stato fissato alle22:46:12UTC prima dell'esecuzione. Sono stati percorsi direttamente tutti i131.072 dispari≤2^18 fino a1, conservando k,A e l'ultimo genitore prima del primo arrivo agli otto target già scelti. Le cinque soglie restano2^10,2^12,2^14,2^16,2^18.

Il peso di ogni sorgente è la frazione esatta `w(u,n)=u3^k/(n2^A)=1/P`. Arrivi vuoti e genitori divisibili per3 sono registrati a parte; la legge dei genitori unità viene normalizzata soltanto quando ha massa positiva. I genitori non sono troncati all'altezza della sorgente: il censimento osserva anche genitori maggiori di2^18 quando una sorgente più piccola li raggiunge.

PASS:5.420.588 passi diretti,249.564 controlli del potenziale e249.556 identità dell'ultimo genitore. Le40 righe di count coincidono con il precedente censimento U03. Normale e Python-O producono gli stessi byte, SHA-256 `c8d9a302a9080b46d28381c591faaa5a79a7c37488a81203c9ed251ac0be7dd3`.

Al cutoff massimo, il target593 ha i genitori unità osservati395,6325,25301. Il peso relativo di395 è circa0,9971303164; il difetto di collisione finito è circa0,0057252000 e Shannon circa0,02096284nats. Alle prime due soglie il difetto osservato è addirittura zero, perché gli altri genitori non sono ancora comparsi. Il caso è coerente con una lunga escursione nota dall'orbita di27 e mostra il pericolo di interpretare un cutoff finito come il vero kernel.

Questi sono istogrammi finiti pesati, non valori certificati di D(n). La loro convergenza al kernel canonico richiede le identità esterne delle medie pesate D_n; nessun rate a quel cutoff è dimostrato. I numeri di collisione e i pesi sono razionali esatti; i valori Shannon e H₂ in nats sono diagnostici floating. Nessuna griglia è stata ampliata e nessuna GPU o risorsa esterna è stata avviata.
