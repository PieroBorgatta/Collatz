# U02 — Green quadratico, clock critico e limiti dell'occupazione

Sessione aggiuntiva del 15–16 novembre 2026, base Git `203cbb8`. Risultati su carta ricostruiti indipendentemente; nessun sorgente Lean modificato e nessun calcolo GPU o esterno avviato. Il protocollo è in `research/research_sprint_2026-11-15_three_hours/u02/protocol.json`. Le deduzioni non forniscono il lower uniforme ancora necessario per Collatz.

## 1. Il budget come vero potenziale Green

Per un target positivo dispari n senza ritorni, sia B_n^odd il suo bacino dispari. Ogni u nel bacino ha un unico tempo di arrivo k_n(u), e il prodotto correttivo P(u,n) soddisfa

`ω(u,n)=3^k/2^A=n/[uP(u,n)]`, `1≤P(u,n)≤P₀=exp(27)`.

Il Green quadratico degli atomi è dunque esattamente

`G₂(n):=Σ_(m≥0)ρ*_m(n)=Σ_(u∈B_n^odd)[n/(uP(u,n))]²`.

Ne segue il confronto a due lati

`n²P₀⁻²Σ_Bu⁻²≤G₂(n)≤n²Σ_Bu⁻²≤2n²`.

La parte finita superiore è già verificata da `IntegerAtomTilt`; l'identificazione infinita usa serie positive e il dizionario con la legge tilt. L'argomento Dirichlet è compatibile con quello Green nella fonte Valbuena archiviata, `tao-basin-densities.tex`, §Weighted densities and the Green limit. Non si rivendica una nuova teoria del Green.

Posto y_a=(2^a n−1)/3 e sommando soltanto gli a≥1 per cui y_a è intero positivo dispari,

`G₂(n)=1+Σ_a(3/2^a)²G₂(y_a)`.

La parola vuota dà 1; ogni altra parola si divide nel suo primo passo inverso e nel resto. La positività delle serie rende legittimo il riordinamento. Per un target senza ritorni tutti i figli appartengono allo stesso dominio senza ritorni.

Questo produce un kernel sub-Markov concreto:

`Q₂(n,y_a)=(3/2^a)²G₂(y_a)/G₂(n)`, `P(kill at n)=1/G₂(n)`.

Partendo da n, la probabilità di assorbimento dopo m passi al predecessore u è precisamente ω(u,n)²/G₂(n). La somma su tutti u e m è 1 per la definizione di G₂. La profondità media è invece

`E_n T=G₂(n)⁻¹ Σ_u k_n(u)ω(u,n)²`,

eventualmente infinita. Il solo budget dei reciproci quadrati non limita k_n(u). Qui ricompare esattamente il problema dei piccoli antenati raggiunti tardi; la finitezza del Green non dà una velocità uniforme del clock.

Il collegamento con il kernel Doob critico Q₁ è anch'esso esatto. Posto F=G₂/g, per ogni m,

`E_n^Q₁[A_m F(Y_m)]=[G₂(n)−Σ_(j<m)ρ*_j(n)−ℓ*_m(n)]/g(n)`,

dove ℓ*_m è la massa quadratica delle parole che terminano in una foglia divisibile per3.

Infatti il peso di un cammino Q₁ è A_m g(Y_m)/g(n); moltiplicando per A_mG₂(Y_m)/g(Y_m) resta il peso quadratico sui soli endpoint con g>0. Il termine ℓ*_m è necessario: sulle foglie il Green vale1 ma il Doob Q₁ non le trattiene. È un processo moltiplicativo con perdita positiva, ma senza tasso uniforme della coda. Ai target con g(n)≥εn, la sua taglia iniziale può essere O_ε(n), quindi non offre da sola un minorante dell'osservabile 1/g.

## 2. Estensione nuova del budget ai target periodici

La stessa finitezza quadratica vale anche se n ha ritorni, pagando un fattore in n. Per una sorgente u>0, scrivere x_k=S^k(u), ω_k=3^k/2^A e

`Φ_k=(ω_k/x_k)²`.

La relazione esatta di un passo dà

`Φ_k−Φ_(k+1)=ω_k²(6x_k+1)/[x_k²(3x_k+1)²]`.

Tutti i termini sono positivi e Φ₀=1/u². Limitando la somma ai tempi con x_k=n,

`Σ_(k:x_k=n)ω_k²≤n²(3n+1)²/[(6n+1)u²]`.

A lunghezza fissata la sorgente determina la parola; quindi, sommando sulle sorgenti dispari e usando il budget ≤2,

**`G₂(n)≤2n²(3n+1)²/(6n+1)`**, senza ipotesi di nonritorno.

Sono ammessi il punto fisso1 e ogni ciclo ipotetico. Equivalentemente, se si conosce un periodo con peso β, il Green totale è quello di primo arrivo diviso per1−β²; la dissipazione evita di dover conoscere o assumere il periodo. Questo rafforza la semplice estensione ottenuta da `WeightedVisits` e maxω≤n/u, che avrebbe dato2n²(3n+1).

Il consumo del cutoff futuro si estende così a tutti i target con errore Cesàro al più

`2n²(3n+1)²/[(6n+1)BK]`, per B>n.

Nel dominio senza ritorni resta preferibile il bound2n²/(BK). Il nuovo bound è una prova su carta proposta al coordinatore, non un teorema già aggiunto a Lean.

## 3. Controllo indipendente dell'endpoint critico

La [discussione primaria del20 ottobre](https://rstation.ai/r/collatz/posts/16), passaggio “endpoint refinement”, contiene già il miglioramento all'orizzonte critico. Il seguente adattamento all'osservabile del progetto non rivendica priorità.

Sia n_j=S^j(u) una spine divergente e N(j) il numero di esponenti almeno2 prima di j. Un passo con esponente1 soddisfa `S(x)+1=(3/2)(x+1)`; un passo con esponente almeno2 soddisfa `S(x)+1≤x+1`. Perciò

`n_j+1≤(u+1)(3/2)^(j−N(j))`.

Si ha N(j)→∞: un'eventuale coda tutta di esponenti1 obbligherebbe il suo intero iniziale più1 a essere divisibile per ogni potenza di2.

Assumere ora il floor esterno g≥c₀>0 sulle unità e un θ>0 tale che ogni target grande, dispari, non periodico e non divisibile per3 ammetta m(n) con

`m(n)≤log_(3/2)(n+2)+C`, `E_n^Q₁[1/g(Y_m)]≥θ`.

Sulla spine, `j−m(n_j)≥N(j)−O_u(1)→∞`. L'endpoint del backtracking esatto ha quindi g→∞ e reciproco→0. Il floor forza una probabilità di uscita uniforme da ogni blocco; concatenando i blocchi si contraddice la probabilità positiva uniforme di tornare lungo la spine fino a un antenato fissato, già calcolata in T09. La prova funziona al coefficiente critico senza imporre separatamente un deficit h(n)→∞. Il lower rimane un'ipotesi aperta.

Un rafforzamento elementare quantitativo è disponibile. Sia t_k il tempo dopo il k-esimo esponente non1, λ=log₂3, C_u=log₂(u+1)+1. La corsa di1 successiva a x dura al più log₂(x+1) passi prima dell'uscita. Dal bound globale x+1≤(u+1)(3/2)^t segue

`t_(k+1)≤λt_k+C_u`, dunque `t_k≤C_u(λ^k−1)/(λ−1)`.

Se N(j)=k, j<t_(k+1), perciò

`N(j)≥log_λ[1+(λ−1)j/C_u]−1`.

Usando inoltre il prodotto P≤exp27 sulla spine iniettiva,

`log_(3/2)n_j−j≤O_u(1)−[log2/log(3/2)]N(j)`.

Questo consente lo stesso criterio Doob con un surplus positivo A loglog(n+3) per ogni

`A<log2/[log(3/2)log(log₂3)]`.

La [discussione primaria sui conteggi non1](https://rstation.ai/r/collatz/posts/23) contiene già stime S-unit più forti, fra cui N(j)/log j→∞ e una versione effettiva superlogaritmica. Non sono state ricostruite integralmente qui; se assunte dopo audit, il medesimo argomento ammetterebbe ogni A fisso. L'interesse del bound elementare è l'assenza di quell'input profondo, non una rivendicazione globale di novità.

## 4. Perché la nuova legge microscopica non paga la coda

La [fonte primaria18](https://rstation.ai/problems/collatz/papers/18) distingue correttamente il limite della legge dei conteggi dai momenti interi non troncati. Fornisce inoltre, sotto input esterni nominati, un criterio equivalente alla mancanza di componente divergente attraverso la probabilità di non visitare una banda. Non ottiene il necessario lower. Il conteggio è distinto e il limite della sorgente precede quello della banda.

Il packing del progetto migliora il massimo deterministico in una banda [A,2A) da O(A) a O(A^β) per qualche β<1. Ciò non basta: un errore TV O_p((logA)^−p), anche per ogni p fisso, moltiplicato per A^β non tende necessariamente a zero. Il budget reciproco quadratico riguarda invece pesi fisici e non converte quel count in una variabile uniformemente integrabile. Un attacco utile dovrebbe controllare direttamente code o momenti fattoriali aritmetici delle molte visite; la sostituzione del massimo non risolve il problema.

## Esito e prosecuzione

I contributi propri più concreti di questo incarico sono l'esplicito Green ucciso, la localizzazione precisa del momento del clock e la dissipazione quadratica che estende il budget ai target periodici. Il miglioramento critico del clock è invece già pubblico. Nessun lower relativo tra sibling, velocità uniforme o stima della coda uncapped è stato ottenuto. Non sono stati eseguiti esperimenti: i passaggi qui sono identità e disuguaglianze matematiche con dominio dichiarato, da eventuale formalizzazione separata.
