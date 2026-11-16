# Ultima riduzione: basta il floor degli atomi, non la traccia canonica

16 novembre 2026. Due raccordi su carta, controllati indipendentemente da H01, H02 e H03 negli ultimi minuti dell'ora. Nessuna compilazione o ricerca numerica. Il primo raccordo è già un corollario del primario12; il secondo è una costruzione di potenziale opzionale. Non si rivendica priorità bibliografica.

## Il budget globale ha una via più corta

La [fonte12, §2, lower logaritmico da InputD](https://rstation.ai/problems/collatz/papers/12) ricava dal floor degli atomi, prima dell'input di esistenza della densità naturale, il lower

`liminf_(X→∞) [2/log X] Σ_(odd u≤X, u→v) 1/u ≥ α/(4v)`

per un target unità nonperiodico v. Qui α è il floor uniforme esterno del manoscritto El Jaouhari. Il lower riguarda medie armoniche; non assume densità naturale o CLT.

Per una famiglia FINITA di seed laterali che formano un'antichain rispetto alla spine, i bacini sono disgiunti. La somma delle medie armoniche odd normalizzate è al più quella di tutti i dispari positivi, che tende a1. Additività finita e limite inferiore danno

`Σ_v 1/v ≤4/α`.

Nel programma minimo, `Γ_w=Ω_w/Ω_j≤bP₀/v_w`. Ne segue direttamente

**`Σ_(j,w) Γ_w≤4bP₀/α`**

per ogni famiglia finita di witness off-spine, prefix-free dal target alla sorgente. Tutti i seed interessati sono nonperiodici perché raggiungono una spine nonperiodica. Non serve trasferire il lower ai cicli. Non si sommano parole annidate.

Il nucleo analitico può quindi limitarsi al floor esterno degli atomi; il prodotto P₀ e la legalità delle parole sono gli ingredienti aritmetici del progetto. Non occorrono Leen, esistenza di densità naturale, traccia canonica di Valbuena, Q, collisioni o F per questo budget globale. Il fatto che il primario12 contenga già la via logaritmica va riconosciuto: il progresso del progetto è aver eliminato dipendenze superflue dalla propria deduzione.

## Un'alternativa per chi vuole il telescopio punto per punto

Il telescopio non richiede l'uguaglianza armonica: basta `h≥Lh`. Si può costruire una tale h senza identificarla con la traccia canonica.

Lavorare sul dominio D delle unità positive dispari nonperiodiche. È numerabile e chiuso per predecessori unità. Porre `f_k=L_D^k1`. Le densità atomiche complete soddisfano lo shift esatto

`ρ_(k+1)=L_D^kρ₁≤2f_k`,

perché ρ₁ vale1 o2 sulle unità. Il floor completo implica dunque `f_k≥α/2`. Lo shift k+1 è indispensabile: il terminale troncato completo può essere una foglia, mentre L_D mantiene terminali unità.

Sia `S_K(n)=Σ_(k<K)f_k(n)`. Per n∈D una sorgente può comparire in una sola parola fra tutte queste profondità. Inoltre `Ωu≤n`. Tagliare le sorgenti a `X=n exp(4K)` dà

`Σ_low Ω≤nH_floor(X)≤4nK+n(1+log n)`.

Sulla coda Ω<exp(−4K), perciò Ω≤exp(−2K)√Ω. Sommando sopra TUTTE le parole di esponenti positivi, non solo quelle ammissibili,

`Σ_(|w|=k)√Ω(w)=R^k`, `R=√3/(√2−1)<5<exp(2)`.

La coda sommata per k<K è quindi limitata uniformemente in K. Ne segue `S_K(n)≤4nK+D_n`, con D_n finito. Si tratta di una stima simbolica, senza scansioni o valutazioni numeriche.

Per 0<r<1 porre

`h_r=(1−r)Σ_(k≥0)r^k f_k=(1−r)²Σ_(K≥1)r^(K−1)S_K`.

Allora `α/2≤h_r(n)≤4n+(1−r)D_n`. Una sottosuccessione comune r_i→1 converge puntualmente su D a una funzione h con `α/2≤h(n)≤4n`. Per positività,

`L_Dh_r=[h_r−(1−r)1]/r`.

Fatou dà `L_Dh≤h`. Non si dichiara h canonica, computabile o uguale a g. Questa superarmonicità basta a tutte le disuguaglianze finite del telescopio e delle antichain. Restringersi a D evita del tutto i fattori di ciclo; un'estensione a tutti i root è possibile con upper quadratico, ma non serve alla via di nondivergenza.

## Decisione di ricerca

Per il solo budget globale, usare la prima via, più breve e già attribuita. Conservare la costruzione Abel come spiegazione della sufficienza di una superfunzione, non come un nuovo apparato obbligatorio. Nessuna delle due costruzioni fornisce i witness con massa relativa non sommabile. L'obbligo aritmetico sul carry e sul colore resta interamente aperto; il problema dei cicli resta distinto.
