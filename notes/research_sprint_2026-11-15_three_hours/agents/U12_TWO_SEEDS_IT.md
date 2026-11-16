# U12 — Certificati armonici di ramificazione e massimi aritmetici

Sessione del 15–16 novembre 2026, base `203cbb8`. Queste sono deduzioni su carta, non nuove prove Lean. Il controllo numerico è un solo censimento ristretto, preregistrato e interamente finito. Nessun lower asintotico nuovo è stato dimostrato; nessuna GPU o risorsa esterna è stata utilizzata. Non si rivendica una priorità bibliografica globale per gli strumenti di massimo, ramificazione o collisione.

## 1. Dal certificato di due seed a una massa armonica

Nel dominio U07, n è un positivo dispari unità senza ritorni, g è armonica per il vero kernel inverso, `g(u)≥c₀>0` sulle unità, `g(n)≤Cn` e il prodotto di primo arrivo è al più `P₀=exp(27)`. Sia `p_x=Q(n,x)` la probabilità del genitore fisico x.

Scegliere un numero finito di seed unità u_i che raggiungono n attraverso genitori distinti x_i. Il cammino inverso fino a u_i ha probabilità `Ω_i g(u_i)/g(n)` e appartiene all'evento del primo genitore x_i. Pertanto

`p_(x_i)≥c₀ Ω_i/g(n)≥c₀ Ω_i/(Cn)≥a/u_i`, `a=c₀/(CP₀)`.

Il seguente lemma vale per qualunque legge di probabilità: se su atomi distinti si hanno lower `p_i≥λ_i≥0`, allora

**`1−Σ_jp_j² ≥ Σ_iλ_i−max_iλ_i`.**

Infatti ogni atomo della legge ha massa al più `1−Σ_iλ_i+max_iλ_i`: per un atomo selezionato si sottrae dal lower totale soltanto il suo termine, per uno non selezionato non si sottrae nulla. Inoltre `Σ_jp_j²≤sup_jp_j`. La prova vale per una famiglia finita di lower anche se la legge completa è numerabile. La famiglia vuota dà zero.

Ne segue il certificato

`D(n)≥a[Σ_i1/u_i−max_i1/u_i]`,

oppure, usando direttamente i pesi esatti e senza il costo P₀,

`D(n)≥[c₀/(Cn)][Σ_iΩ_i−max_iΩ_i]`.

Due seed u₁≤u₂ danno il caso precedente `D≥a/u₂`. Una famiglia più grande può pagare il denominatore log n anche se i due seed più piccoli non sono O(log n). Occorrono sempre genitori distinti: contare più seed che si sono già fusi nello stesso ramo non aumenta questo certificato.

## 2. Un oggetto aritmetico senza stima numerica di g

Per un positivo dispari unità n definire

`F(n)=max{Ω(w): w è una parola effettiva da un seed unità u a n}`,

includendo la parola vuota, con peso uno. Il massimo esiste: la parola vuota consente di restringere a Ω≥1, e tale catalogo è finito per il budget ponderato già discusso in U11 e ora formalizzato dal modulo `BoundedSlopeCatalogue`. Tutti questi seed soddisfano u≤n dal potenziale `Ωu≤n`.

Se x è un genitore unità di n, con `S(x)=n` ed esponente e, porre

`M_x(n)=(3/2^e)F(x)`.

È esattamente il massimo peso di un cammino che entra in n da x: ogni parola si divide al suo ultimo passo forward, e un cammino che realizza F(x) può essere seguito da quel passo. Quindi

`F(n)=max(1,sup_xM_x(n))`.

Quando F(n)>1, il massimo è realizzato in un ramo e vale `max_xM_x(n)=F(n)`. La parola vuota deve essere separata: non ha un ultimo genitore.

Per armonicità e floor, `g(x)≥c₀F(x)`. Ne segue

`LF(n):=Σ_x(3/2^e)F(x)=Σ_xM_x(n)≤g(n)/c₀<∞`.

Applicare il lemma del §1 a famiglie crescenti di rami, scegliendo i cammini che realizzano M_x. Per F(n)>1 si ottiene

**`D(n)≥[c₀/g(n)][LF(n)−F(n)]≥[c₀/(Cn)][LF(n)−F(n)]`.**

Il surplus `A(n)=LF(n)−F(n)` rimuove il ramo migliore e conserva tutti gli altri. Ogni famiglia finita di cammini reali fornisce un lower certificato di questo surplus; un count di parole senza seed distinti non lo fornisce.

Questo è un nuovo raccordo locale proposto fra inverse minima, massimi di pesi effettivi e collisione. Non è un lower già dimostrato di A. Il teorema di finitezza usato qui è un ingrediente esistente, non una nuova priorità matematica attribuita alla sessione.

### Confronto con il minimo antenato

Sia m_U(n) il più piccolo seed **unità** che raggiunge n, includendo il seed n stesso. Il potenziale e un cammino di primo arrivo da m_U(n) danno

`n/[P₀m_U(n)]≤F(n)≤n/m_U(n)`.

La prima disuguaglianza usa il prodotto uniforme sul primo arrivo; resta valida anche per un target periodico scegliendo quel primo arrivo, che è iniettivo. Il minimo ordinario m_*(x) della fonte12 può invece essere multiplo di3. Si ha `m_U(x)≤2m_*(x)`: il minimo ordinario è dispari; se è multiplo di3, il suo primo iterato S è una unità, raggiunge ancora x e non supera `(3m_*+1)/2`. Non si può applicare direttamente il floor di g a un seed multiplo di3.

Il tail di [fonte12, §12, eq(36)](https://rstation.ai/problems/collatz/papers/12) implica che g(n)≥εn, al root nonperiodico, forza un seed unità ≤2M_ε in qualche ramo. Quindi forza F(n)≥δ_εn, con δ_ε>0. Viceversa F(n)≥εn implica subito g(n)≥c₀εn. La direzione che usa il tail è un input analitico esterno; non viene presentata come teorema Lean del progetto.

## 3. Un criterio di surplus che evita del tutto il kernel canonico

La stessa riduzione può essere provata usando soltanto il lower esterno di densità dei predecessori

`underline d(P(u))≥c/u` per ogni seed unità u,

e il prodotto P₀, senza usare g o Q. Il lower è uno degli input pubblici della fonte12, con le dipendenze dichiarate lì; qui non ne vengono ricompilate le formalizzazioni.

Per un genitore x di n, scegliere un seed u che realizza M_x. Poiché `Ωu≤n` e `P(u)⊆P(x)`,

`underline d(P(x))≥c/u≥cM_x(n)/n`.

Al root senza ritorni, i bacini dei diversi genitori sono disgiunti. Basta additività finita e il limite inferiore per concludere `LF(n)≤n/c`; non occorre assumere l'esistenza della densità di una unione infinita.

Su una spine divergente `n_j=S^j(b)`, tutti i bacini dei genitori off-spine sono disgiunti anche fra j diversi. Per ogni j sufficientemente grande F(n_j)>1 e

`A(n_j)=Σ_xM_x−max_xM_x≤Σ_(x≠n_(j−1))M_x`.

Pertanto

**`Σ_(j≥J) A(n_j)/n_j≤1/c`.**

Una condizione sufficiente puramente aritmetica è dunque: per ogni ε>0, sui root unità senza ritorni sufficientemente grandi con F(n)≥εn,

`A(n)≥c_ε n/(1+log n)`.

Infatti il seed b della spine dà `F(n_j)≥n_j/(bP₀)`, mentre `log(n_j+1)≤jlog(3/2)+log(b+1)`. Il lower farebbe divergere la serie appena limitata. I cicli non banali restano un obbligo distinto.

La condizione è **aperta**. Se tutte le orbite fossero eventualmente periodiche, i root F(n)≥εn sarebbero finiti: `m_U(n)≤1/ε` li colloca nell'unione delle orbite di finitissimi seed. Il quantificatore sui root grandi sarebbe vacuo. Non viene quindi promossa questa riformulazione a un problema formalmente più debole già quasi risolto.

Un lower elementare dà solo `A(n)≥3/64` quando F(n)>1: fra i primi tre genitori ammessi ci sono due unità, con esponenti al più6, e ciascuno ha M_x≥3/64; dopo aver rimosso il ramo massimo ne rimane almeno uno. Il salto dal lower costante a n/log n è precisamente il contenuto mancante.

## 4. Limite delle costruzioni con pochi corridoi

Sia D un dizionario finito di parole non vuote di esponenti positivi. Una costruzione del seed che usa un numero fissato s di pezzi, ciascuno lettera libera oppure q^t con q∈D, non può raggiungere target arbitrariamente grandi da seed u=O(log n).

Per q di lunghezza ℓ e totale A, scrivere `a=3^ℓ`, `d=2^A`, c=C(q) e D_q=a−d≠0. Su una ripetizione effettiva si ha

`d^t[D_qx_t+c]=a^t[D_qx+c]`.

Se D_qx+c≠0, l'integralità e gcd(a,d)=1 danno

`d^t | D_qx+c`, quindi `Atlog2≤log(K_q(x+1))`,

con K_q fissato. Il bound shifted di ogni passo dà

`x_t+1≤(3/2)^(ℓt)(x+1)≤C_q(x+1)^Λ`, `Λ=log₂3`.

Qui ℓ≤A. Se D_qx+c=0, il blocco ripete un punto fisso e il suo endpoint resta x: la stessa maggiorazione è valida. Per un primo arrivo il caso fisso è comunque vietato. Le lettere libere hanno un bound lineare e rientrano nella stessa maggiorazione.

Scegliere un C_D≥1 uniforme sui pezzi. Componendo s pezzi,

`log(n+1)≤Λ^s[log(u+1)+B_D]`, `B_D=log C_D/(Λ−1)`.

Quindi, se u≤Klog(n+1),

`s≥[loglog n−logloglog n]/log(log₂3)−O_(D,K)(1)`.

Questo esclude soltanto la costruzione con complessità fissata, non il criterio dei seed. Una variante ancora più semplice: se un cammino contiene k esponenti non1, ogni corsa di1 può aumentare shiftedheight al più alla potenza Λ e gli altri passi non lo aumentano. Ne segue `log(n+1)≤Λ^(k+1)log(u+1)`, con la stessa necessità di k crescente. Sono conseguenze elementari dei corridoi; non si rivendica una priorità globale rispetto alla letteratura già esaminata sugli esponenti non1.

## 5. Un certificato fisico esatto per593

Un unico controllo preregistrato considera tutti i seed unità u≤6325, soltanto una piccola parte del precedente cutoff2^18. Ogni orbita è stata seguita esattamente fino a1; il root593 è separatamente certificato senza ritorni. Nessun timeout è stato classificato come assenza di hit.

PASS normale/O identici: **2109 seed**, **61581 passi**, **zero ignoti**. Fra718 arrivi a593, uno è il seed593 vuoto,716 entrano dal genitore395 e uno dal genitore6325.

I minimi unità dei due primi rami sono esattamente

- `31→47→71→107→161→121→91→137→103→155→233→175→263→395→593`, con k=14, A=18, `Ω₁=4782969/262144`;
- `6325→593`, con esponente5 e `Ω₂=3/32`.

Nessun seed unità minore di6325 entra in593 da un ramo diverso da395. In particolare la massa armonica dei rappresentanti, tolto il migliore, è esattamente1/6325 per questi due rami.

Si può certificare anche il massimo peso-ancora: per u≥33, `Ω≤593/u<Ω₁`, e nessun seed unità minore di31 raggiunge593. Dunque **F(593)=Ω₁**. Ogni seed u>6325 ha `Ω≤593/u<3/32`, perciò il secondo massimo di ramo è proprio Ω₂. Ne segue

`A(593)≥3/32`, e `D(593)≥3c₀/(32·593·C)`.

È un lower condizionale alle costanti del floor/upper, non il valore numerico del vero D. Il censimento non prova un bound logaritmico del secondo seed o del surplus al crescere del root.

La previsione testuale iniziale usava erroneamente27 come unità. Il programma e il dominio preregistrato escludevano già tutti i multipli di3 e hanno restituito31. Il protocollo originale è conservato; `prediction_correction.json` registra la correzione senza cambiare dominio o rieseguire il programma. Questa distinzione è rilevante: il minimo ordinario e il minimo unità non coincidono.

Programma, protocollo, output normale/O e ricevuta sono in `research/research_sprint_2026-11-15_three_hours/u12/`. SHA dell'output: `39afd5e0040babde9da7162404ae055474a0c90b23bbb0884580e66a02ed86cd`.

## Esito

Il contributo più utile è il certificato armonico, esteso al surplus aritmetico LF−F, e la sua verifica positiva su un caso avverso. Il lower logaritmico generale resta aperto; le costruzioni con un numero fissato di corridoi non lo forniscono. Nessun uso GPU, modifica Lean, commit o push da questo agente. Il testo è proposto per revisione indipendente prima di qualunque promozione a risultato integrato.
