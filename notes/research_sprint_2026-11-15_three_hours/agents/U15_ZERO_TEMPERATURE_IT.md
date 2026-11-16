# U15 — Limite p→∞, gap relativo e limite dei budget affini

Addendum richiesto dal coordinatore dopo il suggerimento Green di U04. Prove su carta, da audit; nessun nuovo esperimento. I pesi terminali di questa nota sono g(u), NON g(u)². Il termine di lunghezza zero è sempre incluso. Non viene ottenuto il bound critico di K o il lower del surplus.

## 1. Green pesato e selettore esatto degli ottimali

Per p≥2, porre

`G_p(n)=Σ_(w verso n, seed unità) Ω(w)^p g(u_w)`,

includendo la parola vuota di peso g(n). Il budget affine di U04 dà

`G_2(n)≤(3n+1)g(n)`.

Poiché ogni Ω≤F(n), si ha

`G_p(n)≤F(n)^(p−2)(3n+1)g(n)`.

La convergenza dominata con dominante Ω²g(u)/F² fornisce

**`G_p(n)/F(n)^p → S_opt(n):=Σ_(u∈Opt(n))g(u)`.**

Inoltre `G_p(n)^(1/p)→F(n)`: l'upper segue dal bound precedente e il lower dal singolo witness ottimale di peso F^p g(u)>0. Per F=1 sopravvive soltanto la parola vuota, dunque S_opt=g(n). Non si interpreta p=0 come assenza di contributi: il riferimento a "temperatura zero" significa p→∞, e il termine di lunghezza zero resta presente per ogni p.

Il selettore non dà un nuovo upper degli ottimali. L'armonicità a profondità K, oppure il salto massimo già provato, dà il bound PIÙ FORTE

`F(n)S_opt(n)≤g(n)`.

Il limite del solo budget affine darebbe S_opt≤(3n+1)g/F², peggiore di almeno un fattore3 perché F≤n. Con floor c₀ e upper g≤Cn, sui root F≥εn il bound esatto dà #Opt≤C/(c₀ε); il semplice bound dei seed u≤1/ε è già della stessa scala e non usa g.

## 2. Un gap relativo uniforme, ma non effettivo

**Lemma.** Per ogni ε>0 esiste r_ε<1 tale che, per ogni target NONRETURN n con F(n)≥εn, ogni parola nonottimale verso n soddisfa Ω(w)/F(n)≤r_ε.

Si può assumere 0<ε≤1; altrimenti non ci sono root heavy. Le parole con Ω<F/2 hanno rapporto≤1/2. Ogni altra parola ha seed u≤2/ε, mentre un seed ottimale v è≤1/ε. Sono finitissimi seed.

Per una coppia fissata (u,v), se esiste un discendente nonreturn comune, le due orbite si fondono a un primo punto e da lì i rapporti dei gain verso i discendenti comuni sono ESATTAMENTE costanti. Per un target nonreturn ciascun seed ha una sola parola verso quel target. Il rapporto Ω(u→n)/Ω(v→n) appartiene quindi a un insieme finito dipendente soltanto dalle coppie di seed≤2/ε che effettivamente si fondono prima di un target nonreturn. Per le parole nonottimali si mantengono solo i rapporti strettamente<1. Il massimo di questi finitissimi rapporti e di1/2 è r_ε<1.

La finitezza non certifica né quali coppie si fondano né il loro tempo di fusione. Il gap non è stato reso computabile, stimato numericamente o limitato da una costante esplicita in ε.

Segue il tasso uniforme

**`0≤G_p(n)/F(n)^p−S_opt(n)≤r_ε^(p−2)G_2(n)/F(n)²`.**

Aggiungendo l'upper g(n)≤Cn,

`errore ≤r_ε^(p−2) C(3+1/n)/ε²`.

La normalizzazione suggerita da U04 è più forte perché non richiede né floor né upper di g:

`0≤F(n)^(1−p)G_p(n)/g(n)−Q_n(H=F(n))≤[(3n+1)/F(n)]r_ε^(p−2)≤(4/ε)r_ε^(p−2)`.

Quindi il limite p→∞ seleziona la massa dell'ultimo salto con convergenza esponenziale uniforme sulla classe heavy nonreturn, a costante di gap non effettiva. L'esponente del rapporto r_ε è anche il profilo differenza: se un rapporto fissato vale 3^a/2^b, le parole corrispondenti hanno k−K=a ed E−E_opt=b. Per ogni δ>0, le parole con Ω≥δF hanno quindi offset di lunghezza rispetto a K in un insieme finito dipendente da ε,δ. Questo NON limita K assoluto.

## 3. Heavy equivale a raggiungibilità da seed limitati, entro P₀

Siano H_ε={n unità:F(n)≥εn} e B_R l'insieme dei target raggiunti da qualche seed unità u≤R. Usando un primo arrivo e il prodotto correttivo P≤P₀, si ha per R≥1

**`H_(1/R) ⊆ B_R ⊆ H_(1/(RP₀))`.**

La prima inclusione usa u≤n/F. La seconda usa una parola di primo arrivo da u≤R: Ω=n/(uP)≥n/(RP₀). Include la parola vuota. Non richiede che il target stesso sia non ricorrente, perché si sceglie il primo arrivo.

Ne segue l'equivalenza qualitativa

`nessuna divergenza ⇔ ogni H_ε è finito ⇔ F(n)=o(n)`.

Infatti, se tutte le orbite sono eventualmente periodiche, le finitissime orbite da seed≤R visitano un insieme finito. Viceversa, una divergenza da u dà infiniti target in H_(1/(uP₀)). A ε fissato non si afferma un'uguaglianza tra H_ε e B_(1/ε): le costanti sono diverse e il fattore correttivo non viene cancellato.

Il gap della sezione2 organizza i confronti fra finitissimi seed. Non paga l'escursione prima del merger: è questa che può rendere grande K e ignota la costante r_ε.

## 4. I due target sufficienti sono equivalenti qualitativamente alla nondivergenza

Supporre qui anche il lower esterno d(P(u))≥c/u che dà il budget U12 Σ_j A(n_j)/n_j≤1/c sulle spine divergenti. Considerare la proprietà:

per ogni ε>0 esistono c_ε>0 e N_ε tali che, per n≥N_ε nonreturn con F≥εn, `A(n)≥c_ε n/(1+log n)`.

Questa proprietà esclude divergenza: sulla spine da b vale F≥n/(bP₀), mentre n_j+1≤(b+1)(3/2)^j. Il lower darebbe una serie armonica divergente per ΣA/n, in contrasto col budget. Viceversa, in assenza di divergenza H_ε è finito, e la proprietà è vacua superato il suo massimo. È quindi QUALITATIVAMENTE equivalente a no-divergenza nel quadro degli input; non è stata dimostrata una riduzione logicamente più debole.

Lo stesso vale per il bound critico del profilo ottimale `K(n)≤log_(3/2)(n+2)+C_ε` su root heavy nonreturn sufficientemente grandi. In assenza di divergenza è vacuo. Se vi fosse divergenza, la stabilizzazione darebbe K(n_j)=j+costante, mentre il numero N(j) di esponenti almeno due tende a infinito e impone log_(3/2)(n_j+2)≤j−N(j)+O(1). Le due affermazioni sarebbero incompatibili.

Questa equivalenza non rende inutili i target aritmetici: specifica soltanto che dimostrarli richiede la parte sostanziale ancora mancante, senza sostituirla con una finitezza di catalogo.

## 5. Un ostacolo rigoroso a estrarre K dai soli momenti affini

Il seguente modello NON è una traiettoria intera di Collatz. Serve a isolare l'informazione insufficiente: prodotti dei gain ammessi, calibrazione lungo un cammino, identità affine positiva e tutti i budget Green_p non determinano da soli il clock critico. Non si omette l'integralità per poi dichiarare una confutazione sul grafo effettivo.

Fissare T≥5. Per t≤T scegliere e_t=1, E_t=t e F_t=(3/2)^t. Per t≥T porre

`E_t=T+floor[(t−T)log₂3−2log₂((t+1)/(T+1))]`, `F_t=3^t/2^E_t`.

Gli incrementi della quantità dentro floor sono tra1 e2: la sua derivata è log₂3−2/[(t+1)log2]∈(1,2) per t≥T. Dunque ogni e_t=E_t−E_(t−1) è1 oppure2. Inoltre

`(3/2)^T[(t+1)/(T+1)]² ≤F_t<2(3/2)^T[(t+1)/(T+1)]²`.

Tutti i F_t sono≥1 e Σ_t1/F_t<∞. Per un u>0 reale fissato, definire

`V_t=u+(1/3)Σ_(s=0)^(t−1)1/F_s`, `x_t=F_tV_t`.

Si ha esattamente x_t=(3/2^e_t)(x_(t−1)+1/3), con x_t>0, V_t limitato e F_t/x_t≥1/V_∞>0. Il cammino è calibrato per il massimo sul suo grafo lineare con baseline1: ogni suffisso da x_s a x_t ha gain F_t/F_s≤F_t, e il massimo viene dal seed iniziale con F_0=1. Il profilo ottimale è K=t, mentre x_t è dell'ordine t², quindi K/log x_t→∞.

Assegnare i pesi terminali g(x_s)=F_s. Per il catalogo lineare verso x_t,

`G_p(x_t)=F_t^p Σ_(s=0)^t F_s^(1−p)`.

Per p≥2 il fattore normalizzato è uniformemente limitato; per p→∞ tende a1, perché F_0=1 e F_s>1 per s>0. Il budget affine è soddisfatto:

`G_2(x_t)/F_t²=Σ_(s=0)^t1/F_s ≤3V_t+1/F_t = (3x_t+1)g(x_t)/F_t²`.

Eppure K cresce come t. I momenti non pesano esplicitamente la lunghezza e non possono distinguere questo modello dall'obbligo di clock desiderato. Il modello non soddisfa l'intero sistema di genitori interi, né viene presentato come una costruzione del vero kernel Q. Il risultato negativo riguarda l'inferenza dai SOLI vincoli elencati: per ottenere il clock serve una proprietà aritmetica aggiuntiva dei cammini interi.

## Stato

Il limite zero-temperature seleziona esattamente gli ottimali e ammette un gap uniforme esistenziale sulla classe heavy nonreturn. I momenti affini non hanno fornito un clock; la barriera reale sopra identifica precisamente l'uso mancante dell'integralità. Lower A e clock critico restano aperti.
