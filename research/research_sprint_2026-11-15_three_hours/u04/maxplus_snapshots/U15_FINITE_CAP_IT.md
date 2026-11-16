# U15 — Primi attraversamenti finiti, cap a gradini e salto massimo

Sessione aggiuntiva del 15–16 novembre 2026. Addendum separato alla nota U01, senza modificarla. La semplificazione dei primi attraversamenti è proposta dal coordinatore; il profilo canonico e il salto massimo sono sviluppati da U15 e controllati preliminarmente da U04. Prove su carta, da revisione indipendente. Nessuna nuova conclusione su Collatz, priorità globale, risorsa GPU o modifica Lean.

## 1. Input effettivamente utilizzati

Il target n è positivo dispari e unità modulo 3. Si mantengono le definizioni di U01: legge originale P con P(e=j)=2^(-j); prodotti A_i=3^i/2^(e_1+...+e_i), A_0=1; cap H=sup_i A_i; densità di cilindro ρ_m; densità s_(m,B) con cap infinito e f_(m,B) con solo i primi m prefissi limitati da B. La traccia è definita con medie Cesàro.

Gli input sono:

1. Il dizionario tra parole ammissibili al target intero e veri antenati positivi dispari, con composizione dei gain. I multipli di 3 sono foglie: non ammettono un ulteriore passo inverso intero.
2. Per ogni positivo dispari y fissato, Cesàro ρ_m(y)→g(y). Sulle unità g>0; sulle foglie g=0. La traccia è armonica e definisce il kernel Q, con probabilità di un prefisso w uguale a Ω(w)g(u_w)/g(n).
3. Il catalogo di TUTTE le parole intere con target n, sorgente positiva e Ω≥1 è finito. Le sorgenti qui possono anche essere foglie. È il risultato `BoundedSlopeCatalogue`; vale anche con target periodici.
4. Il budget quadratico non pesato è sommabile: G₂(n)=Σ_mρ*_m(n)<∞, con ρ*_m=Σ_(|w|=m)Ω(w)². Per questo input si usa il risultato preesistente anche con cicli.

Non occorrono, per l'identità del cap, una dominazione uniforme ρ_r(y)≤C_Dg(y), un floor assoluto di g o un upper lineare di g. La positività sulle unità serve a definire Q; non è un floor uniforme. Il quarto input serve per trasferire il cap dal prefisso all'intera sequenza originale e non può essere omesso solo perché il catalogo dei crossing è finito.

## 2. La partizione FINITA secondo il primo attraversamento

Fissare B≥1. Sia T_B(n) l'insieme di tutte le parole intere w ammissibili al target n per le quali

`Ω(w)>B`, mentre ogni prefisso stretto v di w ha `Ω(v)≤B`.

Il target e tutti gli stati intermedi sono quelli effettivi del dizionario intero. La sorgente finale è un positivo dispari qualsiasi, unità oppure foglia. Poiché Ω(w)>B≥1, T_B è contenuto nel catalogo finito dell'input 3. È dunque FINITO, senza ipotesi di nonritorno, bound sui tempi di piccoli seed o stima uniforme delle code. Le sue parole sono prefix-free.

Sia L il massimo delle loro lunghezze, con L=0 se T_B è vuoto. Per ogni m>L, partizionando esattamente le parole di lunghezza m che hanno già attraversato il cap, si ottiene

`ρ_m(n)−f_(m,B)(n)=Σ_(w∈T_B(n)) Ω(w) ρ_(m−|w|)(u_w)`.

Il seguito residuo ha almeno un passo. Una parola di T_B che termina su una foglia contribuisce quindi zero a entrambi i membri della partizione: ρ_r(u_w)=0 per r≥1. Non viene confusa la quantità ρ_0=1 con g(u_w)=0.

La somma è FINITA. Le medie Cesàro di ciascuna sequenza traslata ρ_(m−|w|)(u_w) convergono a g(u_w), e i finitissimi indici m≤L non cambiano il limite. Pertanto

`Cesàro_m f_(m,B)(n) → g(n)−Σ_(w∈T_B(n)) Ω(w)g(u_w)`.

## 3. Pagamento del futuro e identificazione Doob

Sotto la legge originale P, i prodotti A_i formano una martingala nonnegativa. Dato un prefisso che non ha ancora attraversato B, la disuguaglianza massimale sul futuro dà probabilità di attraversamento ≤Ω(w)/B. Come in U01,

`0≤f_(m,B)(n)−s_(m,B)(n)≤ρ*_m(n)/B`.

Il budget dell'input 4 rende la differenza sommabile in m e quindi con media Cesàro nulla. Si conclude l'esistenza della traccia capped e la formula finita

`g_B(n):=Cesàro_m s_(m,B)(n)=g(n)−Σ_(w∈T_B(n)) Ω(w)g(u_w)`.

Sotto Q, le parole di T_B con sorgente unità sono esattamente i prefissi di primo attraversamento. I loro cilindri sono disgiunti; quelli che terminano su foglie hanno probabilità zero. La probabilità totale di attraversare è dunque la somma FINITA Σ_T Ωg(u)/g(n). Ne segue

**`g_B(n)=g(n) Q_n(H≤B)`**.

Per B<1, entrambi i membri sono zero perché A_0=1. La prova vale anche se n è periodico. La finitezza del primo crossing non rende nullo l'errore f_m−s_m per m>L: il futuro della legge originale può non essere ammissibile al target alla precisione più fine. È il budget quadratico a controllare quell'errore.

Questa prova sostituisce le due approssimazioni temporali della nota U01 con una sola somma finita e rimuove l'input C_D dalla sola identificazione. Non viene attribuita all'identità una massa relativa positiva a cap sublineare.

## 4. Il cap reale è una variabile a supporto finito sotto Q

Definire F(n) come in U12/U15 usando solo seed unità, parola vuota inclusa. Ogni prefisso di un cammino Q è una parola effettiva da una sorgente unità al target n, dunque `A_i≤F(n)`.

I valori di A_i almeno uno appartengono al catalogo finito. Siccome A_0=1, il sup H è un MASSIMO appartenente a un insieme finito di monomi compreso in [1,F(n)]. Ne segue che, a n fissato,

**`B↦g_B(n)` è una funzione a gradini con finitissimi salti.**

La soglia che conserva tutta la traccia è precisamente

**`g_B(n)=g(n) ⇔ B≥F(n)`**.

L'implicazione verso destra usa la positività di g sul seed di una parola ottimale: se B<F(n), il cilindro di quel prefisso ha probabilità strettamente positiva e oltrepassa B. Include il caso F(n)=1, in cui ogni cap B<1 perde tutta la traccia. Il vecchio sufficiente B≥n è migliorato al bound esatto B≥F(n), con F(n)≤n.

## 5. Formula esatta dell'ultimo salto

Per unicità della fattorizzazione 3^k/2^E, tutte le parole che realizzano F(n) hanno la stessa lunghezza K(n) e totale E(n). Sia Opt(n) l'insieme finito dei loro seed unità. Ciascun seed dà una sola parola alla lunghezza K, per determinismo dell'orbita forward.

Su ogni cammino Q si ha pertanto

`{H=F(n)}={A_(K(n))=F(n)}`.

Infatti il massimo H è raggiunto; ogni parola di gain F ha necessariamente lunghezza K. Viceversa nessun prefisso supera F. I cilindri ottimali a profondità K sono disgiunti e hanno probabilità F(n)g(u)/g(n). Quindi

`Q_n(H=F(n)) = [F(n)/g(n)] Σ_(u∈Opt(n)) g(u)`

e il salto superiore è

**`g(n)−g_(F(n)^-)(n)=F(n)Σ_(u∈Opt(n))g(u)>0`.**

Qui il valore da sinistra è ben definito dalla funzione a gradini finita. Se F=1, K=0 e Opt={n}, la formula restituisce il salto totale g(n) a B=1. Ogni seed ottimale soddisfa anche F(u)=1: altrimenti concatenare un witness migliore verso u produrrebbe un gain maggiore di F(n).

Aggiungendo SOLO per questo corollario un floor assoluto g(u)≥c₀ sulle unità e un upper g(n)≤Cn, sui target F(n)≥εn il salto superiore ha massa relativa almeno c₀ε/C. Non è quindi disponibile un principio generale di perdita piccola avvicinando il cap a F dal basso. Questo fatto non fornisce un lower del surplus A=LF−F e non esclude divergenza.

## 6. Un budget affine distinto, suggerito da U04

Per ogni cammino inverso effettivo di m passi vale l'identità

`n=Ω_m u_m+(1/3)Σ_(i=1)^m Ω_i`.

Dalla positività della sorgente segue Σ_(i≥1)A_i≤3n su ogni cammino infinito Q, anche se il grafo intero contiene cicli. Scrivendo `K₂h(n)=Σ_x ω(n,x)²h(x)`, si ha quindi

`Σ_(m≥0)K₂^m g(n)≤(3n+1)g(n)`.

Equivalentemente, la ricorrenza affine e l'armonicità danno esattamente

`K₂[((x+1/3)g(x))](n)=n g(n)`.

È un Green quadratico con terminale g, distinto dal budget non pesato G₂ dell'input 4. Non si usa per sostituire automaticamente quell'input: senza un floor uniforme non paga le foglie e il futuro della legge originale. Non produce da solo un lower del surplus.

## Stato

L'identità capped/Doob ha ora una prova finitaria nei crossing, con ipotesi più deboli della nota U01. Il catalogo dà inoltre supporto finito del cap, soglia esatta e salto massimo esplicito. Nessuno di questi risultati paga il clock uniforme dei piccoli antenati né il lower logaritmico del surplus ancora aperti.
