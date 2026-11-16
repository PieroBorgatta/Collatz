# U03 — Scala dei momenti capped e capacità fisiche

Sessione aggiuntiva del 15–16 novembre 2026, base `203cbb8`. Documento di lavoro matematico; nessun nuovo risultato qui è formalizzato in Lean. I risultati analitici esterni sono input dichiarati, non assiomi aggiunti alla libreria. Il problema H resta aperto.

## 1. Corollario analitico: tutti i momenti a cap reale crescente

Nella normalizzazione della fonte [146/v1](https://rstation.ai/problems/collatz/papers/146), siano `A_i=3^i 2^(-D_i)`, `B_i=(1/3)Σ_(j≤i)A_j`, `H=sup_i A_i` e

`σ_B dm₃=P(H≤B,Z∈dz)`, `B≥1`.

Questo è il cap reale del moltiplicatore, non il cap delle valutazioni e_i. Dalla stessa prova del delayed-support si ricava, per ogni **p>2 fissato**,

`c_p B^(p−2) ≤ ||σ_B||_p^p ≤ C_p B^(p−2)` per `B≥2`.       (1)

Al critico vale inoltre

`c log(2B) ≤ ||σ_B||₂² ≤ C log(2B)` per `B≥2`.             (2)

Si tratta di un corollario ricostruito della fonte: il bound cubico è esplicito nel manoscritto; il passaggio a ogni p e la tabella di scala qui sotto non sono presentati come una priorità bibliografica accertata. Il bound a cap fissato in ogni L^p finito era già noto nella [discussione del 21 ottobre](https://rstation.ai/r/collatz/posts/16#comment-U25dwMkOamDR5RVr). La stessa discussione prova che persino σ₁ è essenzialmente illimitata in ogni cilindro unità. Non è lecito sostituire p=∞.

### 1.1 Input a cap fissato

La fonte prova `||f_(n,2)||∞≤C(n+1)²` e, da Tao fine-scale mixing,

`||σ₂−f_(n,2)||₁≤C_M(n+1)^(-M)` per ogni M fissato.

Per Δ_n=f_(n+1,2)−f_(n,2), interpolazione dà

`||Δ_n||_p ≤ ||Δ_n||₁^(1/p) ||Δ_n||∞^(1−1/p) ≤ C_(M,p)(n+1)^[−M/p+2−2/p]`.

Scegliere `M>3p−2` rende sommabile questa serie. Il limite L^p coincide con σ₂ per unicità del limite L¹. Dunque `||σ₂||_p<∞` per ogni p finito. Non si assume convergenza puntuale agli interi.

### 1.2 Spacing a esponente p

Se in un fibre di residuo ci sono m parole, i loro valori positivi `V_j=C_j/3^n` ordinati soddisfano `V_j≥j−1`. Per m≥2,

`Σ_j V_j^(p−1) ≥∫₀^(m−1) x^(p−1)dx=(m−1)^p/p`.

Quindi, includendo m=1,

`m^p≤p·2^p Σ_j(1+V_j^(p−1))`.                           (3)

Il bound è volutamente non ottimizzato.

Sia h_(B,n) la shell di primo attraversamento di B a lunghezza n. Come nella fonte esiste al più un totale d_n per quella lunghezza e il suo moltiplicatore a_n è in `(B,3B/2]`. Su ogni fibre, Minkowski e `σ_(2B/a_n)≤σ₂` danno, per una unione E di cilindri di profondità n,

`∫_E h_(B,n)^p dm₃ ≤ C_p B^(p−2) E_*[(1+V_(τ_B)^(p−1))1_(τ_B=n,B_(τ_B)∈E)]`.       (4)

Il cambio di peso è precisamente `P_*(w)=a_n²3^(-n)`; da qui il fattore `a_n^(p−2)≤(3B/2)^(p−2)`. Non si suppongono disgiunte le immagini delle parole.

### 1.3 Il ritardo paga tutti gli incroci anche per p≠3

Il delayed-support della fonte è

`P_*(τ_B=n+k,V_(τ_B)≤K,B_(τ_B)∈S_n^B)≤C K p_n exp(−ck)`.

Moltiplicando per `1+K^(p−1)` e sommando n, la parte V≤K è al più `C_p(K+K^p)exp(−ck)`. Nella parte V>K ogni parola fermata ha un solo precedente n=τ_B−k. Il momento esponenziale uniforme del record dà quindi `C_p exp(−c'K)`. Con K=k+1 si ottiene

`Σ_n ∫_(S_n^B) h_(B,n+k)^p dm₃ ≤ C_p B^(p−2)exp(−δ_p k)`.  (5)

Partizionare per il primo supporto `E_n=S_n^B\⋃_(j<n)S_j^B`. Su E_n le shell precedenti sono zero. Per `0<ε<δ_p`, Hölder pesato dà

`(Σ_(k≥0)h_(B,n+k))^p ≤[Σ_(k≥0)exp(−εk/(p−1))]^(p−1) Σ_(k≥0)exp(εk)h_(B,n+k)^p`.

Integrare su E_n, allargare a S_n^B e applicare (5). Si paga così l'intera potenza della somma, non solo i diagonali. Prima si usano somme finite nonnegative e poi convergenza monotona. Ne segue

`||σ_(2B)−σ_B||_p^p≤C_p B^(p−2)`.

La somma dyadica delle norme L^p è geometrica, perché `(p−2)/p>0`; Minkowski e σ₁≤σ₂ danno l'upper in (1), anche per B non dyadico per monotonicità.

### 1.4 Lower e soglia p=2

La fonte dà, senza atom floor,

`∫(σ_(2B)−σ_B)dm₃≥1/(6B)`,
`m₃(supp(σ_(2B)−σ_B))≤B^(-2)`.

Hölder implica per ogni p>1

`||σ_(2B)−σ_B||_p^p≥6^(-p) B^(p−2)`.

Per p>2 questa shell, con B sostituito da B/2, è dominata da σ_B e prova il lower di (1).

Per p=2 il lower di ogni shell dyadica è una costante positiva. La positività delle shell dà `(Σ_j h_j)²≥Σ_j h_j²`; sommando fino a B si ottiene `||σ_B||₂²≥c log(2B)`.

Per l'upper usare `σ_B≤ρ`, il weak-L² della fonte e il bound cubico. Per t>0,

`m₃{σ_B>t}≤min(1,Ct^(-2),CBt^(-3))`.

Il layer cake quadratico, diviso negli intervalli `(0,1)`, `(1,B)`, `(B,∞)`, costa rispettivamente O(1), O(log B), O(1). Questo prova (2).

Per 1≤p<2, la monotonia σ_B↑ρ e la regolarità L^p nota danno semplicemente `||σ_B||_p^p↑||ρ||_p^p<∞`.

### 1.5 Limiti e utilità per gli interi

La scala del cap è dunque: momenti limitati sotto 2, crescita logaritmica a 2, crescita B^(p−2) sopra 2. È una stima globale per subdensità, non un confronto di tracce n,h(n), né un lower del rilassamento a root variabile.

Ogni p deve restare fissato. Le costanti dipendono anche dal mixing superpolinomiale con M proporzionale a p. Senza controllare questa dipendenza, prendere p=p(n)→∞ per pagare un deficit arbitrariamente lento nel clock sarebbe un passaggio non giustificato.

Con il cap adattivo di U01 si ottiene un criterio subcritico alla scala

`K< p log n/[log3+(p−2)log(3/2)]`.

Per p→∞ il coefficiente si avvicina al clock critico, ma il bound esatto sul massimo delle densità finite già ottenuto nella fonte (paper9, Theorem9) fornisce un controllo migliore. Quel massimo e il criterio Doob critico non sono risultati nuovi di questa sessione. Qui la tabella di scala serve a classificare e controllare le regolarizzazioni.

## 2. Capacità fisiche: lavoro successivo

L'attacco ai cataloghi cumulativi deve produrre una comparazione relativa o un vero trasporto fra sorgenti positive. I risultati di cap e momento sopra non creano quell'input. La seconda parte verrà completata soltanto con un enunciato esatto e i suoi limiti.
