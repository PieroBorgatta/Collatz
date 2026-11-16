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

## 2. Defetto CDF e scarti sublineari

Il criterio di trasporto completo T08 si estende a un difetto quantitativo. Siano U,V cataloghi fisici finiti con chiavi positive r(u),s(v), dilatazione C>0 e carico m≥1. Il numero minimo di sorgenti da scartare è esattamente

`K = max_(t≥0)[# {u:r(u)≤t} −m # {v:s(v)≤Ct}]_+`.        (6)

Le soglie possono essere limitate alle chiavi delle sorgenti; dopo l'ultima chiave si legge anche l'eventuale difetto globale di capacità. Per necessità, le sorgenti sotto t possono usare solo immagini sotto Ct, e ogni immagine riceve al più m sorgenti. Per sufficienza, ordinare U e le m copie di ogni immagine per chiave. Procedere in ordine crescente: se l'immagine disponibile più piccola non è ammissibile per la sorgente corrente, scartare quella sorgente; altrimenti assegnarla a quella immagine. Uno scarto avviene esattamente quando tutte le capacità ammissibili sono già consumate. Il numero accumulato di scarti è quindi il massimo dei difetti di prefisso. La stessa costruzione e lo stesso swap argument provano ottimalità di cardinalità.

In un catalogo infinito localmente finito, la medesima procedura definisce una mappa sulle sorgenti conservate. Se il massimo del difetto fino alla soglia R è `K(R)=o(R)`, gli scarti sono sublineari; **non occorre un errore additivo costante**.

Per parole di primo arrivo effettive verso n, l'identità già verificata dà `u=ρn/P`, con `1≤P≤P₀`. Ogni sorgente u≤X ha quindi `ρ≤P₀X/n`. Se il confronto dei cataloghi di n e y soddisfa il bound precedente, il numero di scarti dispari fino a X è al più `K(P₀X/n)=o(X)` per n fissato. Altezza e carico del trasporto conservato sono quelli del lemma già noto: `v≤(y/n)CP₀u` e load≤m.

### Il costo dei lift degli scarti

Sia E⊂[1,X] un insieme di K sorgenti dispari scartate, `1≤K≤X`. I loro lift ordinari sono distinti, e

`# {2^e u≤X : u∈E,e≥0} ≤ Σ_(e≥0) min(K,floor(X/2^e))`.

Con `L=floor(log₂(X/K))`, i primi L+1 termini costano K(L+1), e la coda costa al più `X2^(-L)≤2K`. Dunque

`#lift(E) ≤K[3+log₂(X/K)]`.                              (7)

Per K=0 il costo è zero. In particolare **K=o(X) implica #lift(E)=o(X)**, senza richiedere il più forte K log X=o(X). Per i cataloghi a cutoff variabile questa è la perdita corretta da pagare.

Questo è un lemma di interfaccia / Hall per un grafo a vicinati annidati, non una nuova minorazione dei veri cataloghi. L'input uniforme `K_n(R)=o(R)` con il costo mC richiesto rimane aperto. La versione quantitativa serve a confrontare errori di rinnovo che non siano costanti, senza promuovere errori assoluti a massa relativa.

## 3. Un solo replay fisico completo

Il [protocollo congelato](../../../research/research_sprint_2026-11-15_three_hours/u03/physical_cdf_protocol.json) fissa quattro target, cinque cutoff fino a `X=2^18`, otto carichi e sei dilatazioni. Non sono stati aumentati cutoff o parametri dopo i risultati. Sono state enumerate tutte le **131.072 sorgenti dispari fino a X**, senza cap di profondità o di valutazioni. Tutte raggiungono 1 nel calcolo esatto; non ci sono timeout o cicli ignoti. Un secondo attraversamento diretto di ogni orbita, senza arresti nella cache, verifica tutti i cataloghi e i profili: **5.420.588 passi**, lunghezza Syracuse massima164, totale massimo278. Il fatto S(1)=1 certifica anche i no-hit sui target>1.

Le due esecuzioni, normale e Python-O, hanno output identico. [Ricevuta](../../../research/research_sprint_2026-11-15_three_hours/u03/physical_cdf_receipt.json). Nessuna GPU o risorsa a pagamento è servita.

| n | y=h(n) | Sorgenti dispari del bacino di n fino a X | Sorgenti dispari del bacino di y fino allo stesso X | Minimo carico puramente numerico per coprire U con V |
|---:|---:|---:|---:|---:|
|5|85|122825|3119|40|
|7|29|25111|30991|1|
|31|125|12256|12055|2|
|593|9493|43194|13|3323|

L'ultima colonna è soltanto `ceil(|U|/|V|)`, prima di imporre l'altezza. Per le prime tre coppie i carichi registrati64,1,2 permettono matching completi per rango: le dilatazioni minime di slope sono rispettivamente4/3,2/3,1/2; le altezze fisiche effettive massime sono25,25/9,55/27. Non si sta confrontando un numero di codici con un numero di interi.

La coppia593→9493 è avversaria anche nel catalogo completo. Nessun carico registrato≤128 copre tutte le sorgenti usando immagini nello **stesso** intervallo [1,X], qualunque sia C. Con m=8,C=4 il matching ottimo di cardinalità conserva104/43194 sorgenti dispari e854/85981 dei loro lift ordinari, con altezza massima240017/3567. Con m=128,C=32 conserva1664 dispari e11029 ordinari. Non sono nuovi limiti asintotici: ammettere immagini fra X e DX cambia la capacità e non è escluso da questa tabella.

Anche il cap6 sottocampiona il catalogo fisico: al cutoff finale rappresenta79930/122825 inizi per n=5,16257/25111 per7,8939/12256 per31 e28860/43194 per593. Il sottoalbero dei soli primi due figli interni è ancora più ristretto e non va identificato con l'intero cap6. Queste percentuali finite non dimostrano la densità zero già provata asintoticamente; mostrano il difetto concreto di quel proxy.

### Che cosa suggerisce e che cosa non discrimina

Il replay conferma che una selezione globale per rango controlla bene l'altezza quando c'è capacità, ma non la crea. Il caso593 sposta l'ostacolo dai codici alla scarsità di immagini fisiche a scala registrata. Il candidato uniforme resta un confronto dei cataloghi con difetto sublineare e costo mC ammesso; il lemma (7) consente di usare tale difetto senza una perdita eccessiva nei lift. I cinque cutoff e quattro target non distinguono se quel confronto sarà vero in generale e non suggeriscono una stima universale verificata.

Non è giustificato comprare GPU per estendere questa griglia: il collo di bottiglia è l'assenza di una prova uniforme, non il numero di sorgenti controllate.
