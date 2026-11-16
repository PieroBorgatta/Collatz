# U04 — Audit indipendente dei no-go a complessità strutturata

Revisione su carta delle note U05 `U05_MOVING_EDITS_IT.md` e `U05_PERIODIC_DICTIONARY_IT.md`, seguita dal solo lemma CDF del §2 di U03. I testi letti sono congelati nella ricevuta separata. Nessun esperimento, cambiamento Lean, uso di GPU o operazione Git.

**Esito: PASS entro i domini dichiarati.** I due risultati riguardano target n,y positivi dispari distinti e fissati, profili totali uguali e prefisso identico. Non risolvono il problema di pochi edit separati da blocchi generici di complessità crescente. Le stime sono ineffettive per l'input S-unità; nessuna priorità bibliografica globale è accertata.

## 1. Compressione e residuo della nota principale

Ho ricostruito il telescopio, senza usare un programma di U05. Per una coda a con lunghezza L e totale B,

`C(a)=3^L−2^B−F(a)`,

`F(a)=Σ_(i:a_i≥2)[2^(A_(i−1)+1)−2^(A_i)]3^(L−i)`.

I passi con esponente 1 scompaiono realmente. Se ciascuna coda ha al più s non-1, il residuo completo

`3^(r+L)(v−u)=2^P R`, `R=2^B(y−n)+F(β)−F(α)`

ha al più 4s+1 coordinate S-unità, con insieme di primi fissato. R è non nullo: R=0 imporrebbe u=v e due parole effettive della medesima lunghezza dalla stessa sorgente avrebbero lo stesso endpoint, contro n≠y. Questo argomento funziona anche se i target sono ciclici e senza primo arrivo.

Il minimo dei valori assoluti ternari delle coordinate è almeno `3^(-max(L−1,ν₃(y−n)))`; l'altezza reale è al più `C2^B3^L≤C6^B` per una coda non vuota. L'applicazione del Corollario 2 di [Evertse 1984, pagina 228](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf) usa il **minimo**, non il massimo, e ammette sottosomme nulle. Le singole coordinate sono non nulle e la somma completa è non nulla, come richiesto. Le possibili dimensioni appartengono all'insieme finito 1,…,4s+1: si prende il massimo delle rispettive costanti.

Ne segue `ν₃(R)≤L+τA+C_τ` per ogni τ>0, dunque `r≤τA+C_τ`. La coda vuota dà direttamente R=y−n e r≤ν₃(y−n). Non si è dimostrato che tutta la profondità r+L sia sublogaritmica.

## 2. Clock, assorbimento e conteggio fisico

Una corsa di ℓ passi di esponente 1 soddisfa esattamente `x_ℓ+1=(3/2)^ℓ(x+1)` e impone `2^ℓ|(x+1)`. Quindi ℓ≤log₂(x+1), e la sua altezza finale spostata è al più `(x+1)^(log₂3)≤(x+1)²`. Un passo non-1 non aumenta x+1. Iterando per al più s+1 corse si ottiene

`L≤s+(2^(s+1)−1)log₂(z+1)`.

Il punto fisso 1 non è un'eccezione: ogni sua ripetizione è un esponente 2 e spende uno degli s eventi permessi. Dal prefisso `z+1≤(3/2)^r(u+1)` e dal budget effettivo `A≤2(r+L)+log₂X`, si ricavano

`A≤c_s r+d_s log X+O_s(1)`.

Prima si sceglie un τ fisso con τc_s<1, ottenendo A,r,L=O(log X). Poi, con questa maggiorazione ormai fissata, si riusa `r≤τA+C_τ` per ogni τ>0: il bound risultante è uniforme sui codici e dà r=o(log X). L'ordine delle scelte non perde il controllo delle costanti ineffettive.

Per i prefissi di totale al più T=O(log X), il numero a lunghezza r è `binom(T,r)`. La somma per r=o(log X) è exp(o(log X)); non si sostituisce con T^r. Le code con al più s non-1 hanno soltanto O(log X) scelte di lunghezza, O((log X)^s) scelte di posizioni e O((log X)^s) scelte di valori. Il costo delle due code è polilogaritmico. Le parole con i target determinano uniche sorgenti u,v, dunque si contano davvero codici fisici, non rappresentazioni duplicate.

La conclusione `#codici=X^o(1)` è corretta. Per s=0 il residuo impone addirittura profondità limitata da ν₃(y−n); le parole vuote contribuiscono al più un codice. Una massa uscente normalizzata per sorgente è quindi o(X), senza cutoff su v. L'affermazione resta a target e complessità fissati.

## 3. Dizionario periodico: denominatori e primo arrivo

Per una parola q non vuota di esponenti positivi, porre ℓ=|q|, a=Σq e d=2^a−3^ℓ. Si ha d≠0 e gcd(d,6)=1. La formula

`C(q^t)=C(q)[2^(at)−3^(ℓt)]/d`

segue dalla composizione affine. Un solo Δ, minimo comune multiplo dei |d| del dizionario finito, elimina tutti i denominatori: la costante di una concatenazione è lineare nelle costanti dei pezzi, quindi non serve Δ elevato al numero di pezzi. Per le lettere libere C([e])=1 e i loro esponenti variabili non creano nuovi coefficienti.

Il residuo moltiplicato per Δ è così una somma di al più 4s+1 S-unità con coefficienti in un insieme finito. Inoltre ν₃(ΔR)=ν₃(R), poiché Δ è coprimo con 3. L'upper del minimo ternario e dell'altezza sostiene esattamente lo stesso bound `r≤τA+C_τ`.

Per un pezzo effettivo q^t, l'identità

`2^(at)[d x_t−C(q)]=3^(ℓt)[d x−C(q)]`

è corretta. Se d x−C(q)=0, la prima copia effettiva di q torna a x e ripete uno stato. L'iniettività della parola originale di primo arrivo, incluso l'endpoint, esclude questo caso. Non si assume l'assenza di altri cicli positivi.

La coprimalità con 3 dà quindi `2^(at)|(d x−C(q))`, con intero a destra non nullo. Ne segue `at≤log₂(x+1)+O_q(1)` e una lunghezza O_q(1+log(x+1)). Le altezze intermedie hanno crescita polinomiale; componendo al più s pezzi si ottiene il clock necessario per l'assorbimento precedente.

La sola parola originale deve essere di primo arrivo. La coda immagine può contenere ritorni: avendo lo stesso L e B dell'originale, i suoi parametri t ed e sono già O(log X), e il suo conteggio è polilogaritmico. Questo è sufficiente per il risultato proposto.

I casi q=[1] e q=[2] chiariscono il dominio: nel primo il punto fisso affine è negativo e il fattore non si annulla su x>0; nel secondo è x=1 e l'esclusione deriva proprio dal primo arrivo originale. Parole periodiche non primitive non creano problemi. Una potenza con t=0 viene omessa dalla decomposizione; se la si usa solo nella formula affine, dà C(vuota)=0 e non richiede l'argomento del ritorno. Dizionario vuoto, s=0 e coda vuota sono coperti separatamente.

**Anche questo no-go passa.** Il numero di pezzi e il dizionario devono restare fissati. Non è ottenuto un controllo per dizionari o complessità crescenti con X.

## 4. Lemma CDF parziale e costo dei lift: PASS

Ho controllato il §2 di U03 separatamente dai suoi nuovi dati numerici. Per cataloghi finiti a vicinati annidati e capacità incoming m, lo scarto minimo è

`K=max_t[U(t)−mV(Ct)]_+`.

La necessità è Hall sui prefissi. Ordinando sorgenti e copie delle immagini, il greedy crescente assegna la più piccola immagine disponibile se ammissibile; altrimenti scarta la sorgente corrente. Dopo ogni prefisso il numero degli scarti è il massimo deficit visto. Le parità di chiave non alterano il ragionamento.

Per cataloghi infiniti occorrono **sottolivelli finiti** per ogni soglia R. È automatico nel caso fisico, poiché u≤nρ. La sola espressione topologica “localmente finito su (0,∞)” potrebbe consentire accumulo a zero; ho suggerito questa precisazione a U03. Con sottolivelli finiti, un difetto o(R) produce o(X) scarti fisici a target fissato e mantiene altezza e carico già dichiarati.

Se E contiene K sorgenti dispari distinte fino a X, il numero dei loro lift è al più `Σ_e min(K,floor(X/2^e))`. Separando a `floor(log₂(X/K))` si ottiene

`#lift(E)≤K[3+log₂(X/K)]`.

Questo dimostra che K=o(X) basta anche dopo i lift. Il caso K=0 si tratta con valore zero; non occorre imporre K log X=o(X). È un lemma d'interfaccia corretto, non una dimostrazione del difetto o(R) per i veri cataloghi.

## Limiti della verifica

Nessuna delle tre conclusioni fornisce il lower relativo richiesto da H. I due no-go U05 delimitano costruzioni che non possono sostenere una quota positiva; il lemma U03 dice come usare un difetto sublineare qualora venga dimostrato. La parte asintotica rimane su carta e usa Evertse come teorema esterno. Non sono stati verificati nuovamente i replay finiti di U03 o introdotti assiomi Lean.
