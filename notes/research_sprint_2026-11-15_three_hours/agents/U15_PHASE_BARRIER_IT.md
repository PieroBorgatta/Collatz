# U15 — Un tentativo max-plus sublineare e un ostacolo esatto

Nota esplorativa separata: nessun lower del surplus o soluzione. Non modifica i due snapshot U15 già passati a revisione. L'obiettivo era provare F(n)=o(n) costruendo un supersolutore del massimo aritmetico.

## 1. Cosa basterebbe, e perché è forte

Se una funzione positiva U sulle unità dispari soddisfa U≥1 e U(n)≥(3/2^e)U(x) per ogni genitore unità x di n, allora per composizione F(n)≤U(n). Pertanto U(n)=o(n) escluderebbe divergenza, perché su una spine divergente F(n_j)≥n_j/(bP₀).

L'esistenza di un tale supersolutore sublineare non è una riduzione dimostrata più debole del problema. Infatti, se ogni orbita è eventualmente periodica, fissato R le finitissime orbite dei seed u≤R visitano soltanto un insieme finito di target. Fuori da esso, ogni seed ottimale è>R e F(n)/n≤1/R. Quindi F(n)=o(n), e F stesso è un supersolutore. Nel quadro corrente: assenza di divergenza ⇔ F(n)=o(n) ⇔ esistenza di un maggiorante supersolutore sublineare.

## 2. Correggere soltanto le sequenze di esponenti uno non basta

Fissare s>0 e λ=3/2. La prima proposta liscia U(n)=n/[log(n+1)]^s fallisce lungo i rami di esponente uno: il rapporto dei logaritmi produce un difetto maggiore del piccolo guadagno affine.

Si può correggere esattamente la fase dei blocchi di uno. Porre

`r(n)=ν₃(n+1)`, `ell(n)=log(n+1)−r(n)logλ`, `U_s(n)=n/[ell(n)]^s`.

ell è positiva: n+1≥3^r implica ell≥r log2 se r>0; se r=0 vale ell=log(n+1)>0. Lungo un passo forward x→n di esponente uno, x+1=(2/3)(n+1), r(x)=r(n)−1 e quindi ell(x)=ell(n). Ne segue

`(3/2)U_s(x)/U_s(n)=3x/(3x+1)<1`.

La correzione risolve quindi esattamente tutti quei vincoli locali. Ma fallisce sui rami di esponente due per una famiglia aritmetica esplicita.

Per ogni R positivo PARI, porre

`x_R=2·3^R−1`, `n_R=(3^(R+1)−1)/2`.

Entrambi sono unità positive dispari. Poiché R+1 è dispari, ν₂(3x_R+1)=2, quindi il passo x_R→n_R ha esponente esattamente due. Inoltre

`r(x_R)=R`, `r(n_R)=0`,

`ell(x_R)=(R+1)log2`, `ell(n_R)=log[(3^(R+1)+1)/2]`.

Perciò

`(3/4)U_s(x_R)/U_s(n_R) = [3x_R/(3x_R+1)] [ell(n_R)/ell(x_R)]^s → [log3/log2]^s>1`.

Il vincolo di supersoluzione è dunque violato per tutti gli R pari abbastanza grandi. Moltiplicare U_s per una costante non cambia il rapporto. Una sola correzione della fase degli uno non costruisce il maggiorante voluto: il passo di esponente due può rientrare in un corridoio di uno con un difetto di fattore costante.

La famiglia non è dichiarata nonperiodica: il controesempio riguarda una supersoluzione proposta su TUTTE le unità. Non viene usata per confutare una variante definita solo su root ipoteticamente divergenti, per la quale occorrerebbe provare separatamente che appartenga a quel dominio.

## 3. L'insieme F=1 è infinito: chiarimento per il test Bellman

Ogni unità n ha un seed ottimale u con F(u)=1. Esistono infiniti genitori unità x≠1 di 1: x=(2^e−1)/3 con e pari e non divisibile per6. Una singola orbita forward può incontrare al più uno di tali x, perché dopo x raggiunge 1 e vi rimane. I seed ottimali scelti per questi x devono quindi essere tutti distinti. Ne segue che {F=1} è infinito, senza usare il budget dei reciproci.

Questo giustifica la frase nella nota principale: il test Z=F/g ha drift nonnegativo fuori da un insieme infinito, quindi non contraddice il no-go dei test limitati con drift uniforme fuori da un insieme finito.
