# U15 — Quota a cap lineare sui root heavy

Corollario proposto dal coordinatore, verificato su carta da U15. Si usano la formula capped/Doob, h=g_1>0, il prodotto correttivo di primo arrivo P≤P₀ e l'upper g(n)≤Cn. Non viene dimostrato alcun lower del surplus, η o clock. Le costanti sono esistenziali e non effettive.

## 1. Una quota positiva a ogni scala lineare

Sia n_j=S^j(b) una spine divergente da un seed unità b. Porre Ω_j=Ω(b→n_j), n_j=bΩ_jP_j, 1≤P_j≤P₀. Per ogni c>0 si ha

**`liminf_(j→∞) g_(c n_j)(n_j)/g(n_j)>0`.**

Poiché Ω_r≥n_r/(bP₀)→∞, scegliere s tale che Ω_r≥1/(cb) per TUTTI gli r≥s. Per j≥s, ogni prefisso di backtracking da n_j fino a n_s ha gain

`A=Ω_j/Ω_r=n_j/(bP_jΩ_r)≤c n_j`.

Dopo quel segmento, il cap residuo è

`c n_j Ω_s/Ω_j=c bP_jΩ_s≥1`.

Dunque l'evento "backtracking esatto fino a n_s, poi futuro con H_s≤1" resta interamente sotto il cap c n_j. La sua probabilità è

`[Ω_jg(n_s)/(Ω_sg(n_j))]·[h(n_s)/g(n_s)]`

`=Ω_jh(n_s)/(Ω_sg(n_j))≥h(n_s)/(CbP₀Ω_s)>0`.

La scelta dipende dal tail minimo dei prodotti Ω_r, non soltanto dal singolo valore Ω_s. La sola positività puntuale di h basta perché s è fissato prima di far tendere j all'infinito.

## 2. Uniformità esistenziale sulla classe heavy

Per ogni ε,c>0 esistono N e κ>0 tali che, per ogni unità n≥N con F(n)≥εn,

**`g_(c n)(n)/g(n)≥κ`.**

Infatti ogni root heavy è raggiunto da un seed unità≤1/ε. Sono finitissimi seed. Le loro orbite eventualmente periodiche visitano soltanto finitissimi root; si eliminano scegliendo N. Su ognuna delle rimanenti orbite divergenti si applica la sezione1 e si eliminano i finitissimi indici prima del suo s. Il minimo delle finitissime quote positive dà κ. Se non ci sono orbite divergenti nel pool, la classe heavy è finita e la conclusione è vacua oltre N.

La quota non è stata resa funzione esplicita di ε,c. Il risultato va affiancato al corollario U01: lungo una ipotetica spine divergente B_j=o(n_j) implica g_(B_j)(n_j)/g(n_j)→0. Quindi il passaggio fra cap sublineare e cap lineare è netto nell'ordine di grandezza, senza un tasso o un controllo della dipendenza da c↓0. Non viene dedotta una quota a un cap sublineare.

## 3. Un lower assoluto molto piccolo, con ipotesi più forti

Solo in questo paragrafo aggiungere il floor uniforme g(x)≥c₀>0 sulle unità. L'armonicità dà g(n)≥c₀Σ_xM_x(n): ogni witness ottimale verso x implica g(x)≥c₀F(x). Ogni ramo pericoloso M_x>1 costa quindi più di c₀ e il loro numero è al più floor(g(n)/c₀).

In ogni blocco di sei esponenti ci sono due genitori unità; in particolare i primi N+1 genitori unità hanno esponenti≤6(N+1). Fra i primi floor(g(n)/c₀)+1 ce n'è uno sicuro M_x≤1. Come nella prova di h>0, tutto il suo cilindro sta sotto il cap1. Si ottiene

`h(n)≥3c₀·2^(-6[floor(g(n)/c₀)+1])`.

Con g(n)≤Cn è un lower exp(−O(n)), e h(n)/g(n) è almeno quel valore diviso Cn. È insufficiente per conservare una quota relativa o rendere divergente un budget lungo la spine. Il floor e l'upper non vanno retroattribuiti alla prova più debole della sola positività h>0.
