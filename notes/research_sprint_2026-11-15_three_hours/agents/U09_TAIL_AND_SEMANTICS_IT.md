# U09 — Revisione semantica e coda uniforme dei reciproci

Revisione indipendente su sorgenti congelati del 15–16 novembre 2026. Le due nuove formalizzazioni sono state lette, senza avviare un'altra compilazione. La stima di coda seguente è una prova su carta ricostruita dai lemmi finiti già verificati in `OrbitReciprocal`; non è ancora un nuovo teorema Lean. [Ricevuta e hash](../../../research/research_sprint_2026-11-15_three_hours/u09/review_receipt.json).

## 1. Domini dei due nuovi moduli: PASS

### FiniteHorizonBudget

Gli otto enunciati pubblici mantengono distinte tre proprietà:

1. La crescita deterministica `2^k(S^k(u)+1)≤3^k(u+1)` richiede che u sia dispari. Questa ipotesi implica u>0; non è una dichiarazione sulla funzione totale S agli input pari.
2. Il bound di coda `Σ_(u∈U)u⁻²≤2/R` richiede R>0 e ogni u≥R. Non richiede che U provenga da un'orbita.
3. Il budget `Σω²≤2n²/R` richiede sorgenti fisiche iniettive; il wrapper a profondità fissata le rende automaticamente tali, mentre quello che somma profondità diverse richiede esplicitamente il nonritorno del target.

La localizzazione usa `3^K(R+1)≤2^K(n+1)` e lunghezze≤K. Da queste due ipotesi e dal match effettivo si ottiene source≥R; la positività delle sorgenti è dunque derivata e non omessa. Non si introduce una legge casuale o una quota di massa relativa.

I casi vuoti sono corretti. Per K=0, W può contenere solo la parola vuota e la condizione di scala riduce a R≤n. Il wrapper a profondità fissata permette target ciclici, ma per n piccolo e K grande la condizione di scala con R≥1 può non avere soluzioni: per esempio n=1,K≥1. È il limite esplicito di questo envelope, non un errore o una falsa applicazione al ciclo1.

Non vi è vacuità globale: per la parola `[1]` da3 a5, K=1 e R=3 soddisfano esattamente la condizione di scala. Nel lemma generale di coda il grado di libertà R è indipendente dal clock.

### QuadraticOccupation

Gli otto enunciati pubblici e le due definizioni sono coerenti con il potenziale precedente. In particolare

`Φ_k−Φ_(k+1)=ω_k²(6x_k+1)/[x_k²(3x_k+1)²]`, `Φ_k=(ω_k/x_k)²`.

La positività della sorgente garantisce tutti i denominatori non nulli lungo l'orbita. La somma su un insieme finito arbitrario di tempi permette visite ripetute allo stesso target. Il trasferimento alle parole usa l'unicità di una parola esatta a lunghezza fissata dalla stessa sorgente; non confonde parole diverse con visite allo stesso tempo. Il catalogo finale raggruppa le sorgenti e **non** richiede iniettività della sorgente, primo arrivo o nonritorno.

Gli input pari positivi sono ammessi: la dissipazione impiegata vale per la funzione totale S e non usa l'ipotesi di esponente≥1. Il target n=0 è ammesso soltanto con catalogo vuoto, perché un'orbita da una sorgente positiva rimane positiva. Il bound finale è allora0≤0; non vi è una divisione indebita per zero in un caso nonvuoto. Il punto fisso1 e ipotetici altri cicli sono ammessi.

La [Proposizione11 del paper9/v1](https://rstation.ai/problems/collatz/papers/9/v1) già identifica il dizionario tilt agli interi, ne dimostra la sommabilità nel dominio nonperiodico e la estende ai cicli mediante una serie geometrica. Il modulo locale verifica una dissipazione esplicita e la relativa costante. Non costituisce una priorità per la finitezza del Green, né per la sua estensione periodica.

## 2. Coda quantitativa: enunciato più forte del minimo globale

Sia A l'insieme degli stati di un qualsiasi segmento finito positivo e iniettivo della shortcut T. Per ogni intero R≥0, porre

`q=3125/3456`, `ℓ=27/32`, `J=5R`.

Allora

`Σ_(x∈A, x≥2^(5R))1/x`

`≤ (10R+2)/32^R +(19626/331)q^R +(102/5)ℓ^R`

`≤ (135202/1655)q^R <82q^R`.                                      (1)

Non serve che tutti gli stati di A siano alti. La somma seleziona soltanto quelli sopra la soglia; gli altri possono essere arbitrariamente piccoli. La versione in cui tutti gli stati sono≥2^(5R) è un corollario immediato. È sempre indispensabile l'iniettività temporale del segmento: ripetere arbitrariamente un ciclo non è ammesso.

### 2.1 Bande finite e bordo temporale

Per j≥0, sia `F_j=2^(-j)#(A∩[2^j,2^(j+1)))`. Il lemma finito esistente dà

`F_j≤j2^(-j)+H_j+L_j`,

`H_j=(5/4)^j(2/3)^floor(3j/5)`, `L_j=3^floor(3j/5)/2^j`.

Il primo termine è proprio il bordo temporale dell'adattamento al segmento finito; non viene eliminato. Prendere un cutoff finito 5Q maggiore di ogni logaritmo dyadico degli stati e con Q≥R. Il conteggio per bande del filtro alto dà

`Σ_(x∈A,x≥2^J)1/x≤Σ_(J≤j<5Q)F_j`.

Tutti i passaggi fino a questo punto sono somme finite. Le bande sotto J sono vuote per il filtro selezionato; non occorre la correzione speciale della banda zero usata nel precedente bound globale<81.

L'identità geometrica esatta

`Σ_(j<N)j/2^j =2−(2N+2)/2^N`

fornisce, sottraendo il valore a J da quello a5Q,

`Σ_(J≤j<5Q)j/2^j≤(2J+2)/2^J=(10R+2)/32^R`.

Il resto scartato è nonnegativo. Il bordo resta quindi uniformemente controllato anche se il segmento è più corto della profondità j usata nella singola banda.

### 2.2 Le due somme geometriche

Per s∈{0,…,4} si ha esattamente

`H_(5r+s)=q^r H_s`, `L_(5r+s)=ℓ^r L_s`.

I coefficienti dei cinque residui sono

`Σ_s H_s=3271/576`, `Σ_s L_s=51/16`.

Quindi, maggiorando le somme geometriche finite con quelle complete,

`Σ_(5R≤j<5Q)H_j≤q^R(3271/576)/(1−q)=(19626/331)q^R`,

`Σ_(5R≤j<5Q)L_j≤ℓ^R(51/16)/(1−ℓ)=(102/5)ℓ^R`.

Questo prova la prima disuguaglianza di (1), senza alcun limite sull'orbita.

### 2.3 Compressione in un solo esponenziale

Scrivere `t_R=(10R+2)/32^R`. Si ha t_0=2 e

`t_(R+1)/t_R=(10R+12)/[32(10R+2)]≤3/16≤q`.

Per induzione t_R≤2q^R; inoltre ℓ≤q. Perciò il coefficiente totale è

`2+19626/331+102/5=135202/1655<82`.

Il risultato vale anche per R=0; in quel caso è più grossolano del precedente<81, perché la banda zero non è stata ottimizzata. Se A è vuoto tutte le somme sono zero.

## 3. Prodotto affine e dipendenza dal minimo

Sia `u→n` una parola Syracuse positiva dispari di primo arrivo, e supporre soltanto che gli stati dei fattori `x_i=S^i(u)`, i<k, siano≥2^(5R). Il clock già verificato la include in un segmento shortcut iniettivo. Gli stati x_i appartengono al filtro alto di quel segmento, anche se il suo endpoint n è sotto la soglia. Da (1) e `log(1+t)≤t` segue

`1≤P(u,n)=Π_(i<k)(1+1/(3x_i))≤exp[(82/3)q^R]`.                  (2)

Più precisamente si può usare `(135202/4965)q^R` nell'esponente. Il limite superiore tende a1 uniformemente nella lunghezza e nel target. Per una soglia reale M≥1, scegliere `R=floor(log₂M/5)` e porre

`α=log(3456/3125)/(5log2)>0`.

Allora `q^R≤q^(-1)M^(−α)`, e (2) dà `log P≤[82/(3q)]M^(−α)`. La potenza è piccola, circa0,029; non si tratta di un rapido rilassamento in funzione del tempo.

Per ogni immagine effettiva di stesso profilo verso y, il teorema di altezza già verificato migliora a

`v≤(y/n)exp[(82/3)q^R]u`.

L'immagine deve ancora esistere. Non si costruisce una parte positiva del bacino.

## 4. Utilità e limite per il problema aperto

Lungo una spine divergente iniettiva, il minimo della coda tende a infinito. La stima (2) rende quantitativo il fatto che il prodotto correttivo della coda tende a1, esprimendo l'errore attraverso quel minimo. Può rendere espliciti alcuni errori di normalizzazione e i costi dei trasporti che restano alti.

Non limita però il primo tempo di arrivo da un piccolo antenato. Non controlla la velocità con cui crescono le densità dei bacini annidati e non dà una probabilità uniforme di escape del processo Doob. Nel rapporto esatto di backtracking rimane il fattore di massa, oltre al prodotto affine. Promuovere la coda di P a un rate del clock cancellerebbe nuovamente l'obbligo centrale.

Su un singolo giro di un ciclo si ottiene analogamente un gap logaritmico piccolo quando il minimo del ciclo è alto. Senza un altro input di teoria delle forme lineari non segue un limite sul periodo; anche combinandolo con un lower esterno si ottiene una restrizione, non l'esclusione generale dei cicli.

La stima qui è una conseguenza quantitativa locale del packing esistente. La revisione non ne certifica una priorità bibliografica globale. Nessuna GPU, esperimento d'orbita, compilazione ridondante o modifica dei moduli è stata eseguita.
