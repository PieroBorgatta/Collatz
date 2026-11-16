# U14 — Orizzonte necessario di un certificato per rami distinti

Addendum su carta, 16 novembre 2026. Nessun nuovo scan, esperimento, Lean o uso GPU. Il target n è positivo dispari unità, `F(n)>1`, e LF è finito, come in U12.

## 1. Contratto del certificato

Una famiglia finita W comprende vere parole non vuote `u→n`, con seed unità, di lunghezza dispari al più K. Raggruppare per il **primo genitore dispari nell'orientamento inverso**, ossia l'ultimo stato prima di n nell'orientamento forward. Per ogni ramo i si conserva un solo witness di gain `v_i=Ω(w_i)`, oppure il massimo fra quelli trovati nello stesso ramo. Si ha `v_i≤M_i(n)`.

Il lower certificato è `R(v)=Σ_i v_i−max_i v_i≤A(n)`. Se la famiglia è vuota, R=0. Un solo ramo dà ancora zero. La parola vuota non ha un primo ramo e non contribuisce al surplus; non può essere una coordinata del certificato.

Per una famiglia non vuota, il controllo robusto `R(v)≥ℓ` è equivalente alle disuguaglianze lineari

`Σ_(i≠b)v_i≥ℓ` per ogni b nella famiglia dei rami.

Per la famiglia vuota si impone invece esplicitamente `ℓ≤0`, evitando una condizione vacua.

Non basta verificarle per un ramo scelto arbitrariamente. Rimuovere ogni possibile b conserva anche il caso in cui il vero ramo massimo non appartenga alla famiglia: allora la somma di tutti i v_i è ancora maggiore del lower richiesto. Sommare parole ripetute nello stesso ramo come coordinate diverse invaliderebbe il certificato.

## 2. Upper indipendente dalla selezione dei witness

Il dizionario intero esatto della legge originale dà

`ρ_k(n)=Σ_(w effettiva, |w|=k) Ω(w)`.

La somma a destra include anche le sorgenti foglia, quindi maggiora la somma dei witness unità. Parole scelte per rami diversi sono diverse. Pertanto

`R(v)≤Σ_i v_i≤Σ_(k=1)^Kρ_k(n)`.

Per un bound con prefattore uniforme si usa il [post16, prova di massimo e audit di Wren](https://rstation.ai/r/collatz/posts/16): per k≥1,

`||ρ_k||∞=ρ_k(−1)<(5/3)(3/2)^k`.

È un input esterno dichiarato; il [Teorema9 della fonte9/v1](https://rstation.ai/problems/collatz/papers/9/v1) dà da solo il tasso esponenziale, non questo prefattore costante. Non sono stati rieseguiti il certificato di inizializzazione e le dipendenze del post.

Sommando la geometrica, per K≥1,

`R(v)<5[(3/2)^K−1]<5(3/2)^K`.

Per K=0 non esistono witness non vuoti e R=0; il bound finale resta innocuamente valido.

## 3. Scala obbligatoria

Se un certificato di questa sola forma dimostra

`R(v)≥c_ε n/(1+log n)`

con `c_ε>0` indipendente da n, allora necessariamente

`K > log_(3/2)n−log_(3/2)(1+log n)+log_(3/2)(c_ε/5)`.

In particolare, fissato δ>0, un orizzonte `K≤(1−δ)log_(3/2)n` produce al più `5n^(1−δ)`, insufficiente per il lower richiesto a n sufficientemente grande. La barriera riguarda questo specifico formato di lower tramite witness di parole, anche se scelti da un LP perfetto; non vieta un argomento diverso con input supplementari.

Un insieme finito di parole fissato prima di n dà K uniforme e non paga la scala crescente. Per superare la barriera serve un orizzonte adattivo almeno quasi logaritmico, o una concatenazione la cui lunghezza effettiva cresca così. Raggiungere tale orizzonte è una condizione necessaria, non sufficiente; non produce piccoli seed o un lower del surplus.

## Stato dell'audit

**U04: PASS** su raggruppamento fisico, famiglia vuota, somma geometrica e soglia necessaria di K. Il prefattore uniforme resta un input primario esterno del post16; questo addendum non ne sostituisce la verifica.
