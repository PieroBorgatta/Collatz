# U04 — Audit del massimo aritmetico e del surplus di rami

Quarta revisione indipendente, relativa a U12 nello snapshot `402142a08423a17fbcc92e2c195b60702f44a4d713bd27ac3452168879231b66`. Ho ricostruito le prove e letto staticamente programma, output e certificato del caso593, senza rieseguirli. Nessun nuovo esperimento, build, GPU o operazione Git.

**Esito: PASS nel dominio dichiarato.** Il criterio diretto del §3 può davvero essere espresso senza g e senza una catena casuale Q, usando il lower uniforme esterno della densità dei predecessori. Il lower del surplus rimane aperto. Questa è una riduzione strutturale, non una soluzione o una prova che il nuovo obiettivo sia logicamente molto più debole di H.

## 1. Il lemma a più testimoni

Per una legge p su un insieme numerabile e lower finiti λ_i su atomi distinti, la somma dei lower è al più1. Ogni atomo ha massa al più `1−Σλ_i+max λ_i`; inoltre `Σp_j²≤sup p_j`. Quindi

`D=1−Σp_j²≥Σλ_i−max λ_i`.

La famiglia vuota ha lower zero. Se i testimoni sono parole effettive che entrano in n da genitori finali distinti, la probabilità del cammino completo non supera quella del relativo primo ramo inverso. Questo giustifica sia il certificato con 1/u_i sia quello con i pesi Ω_i. Due seed nello stesso ramo non si possono sommare come atomi distinti.

## 2. F è un massimo, non soltanto un supremo

La parola vuota fornisce peso1. Il catalogo completo di parole effettive con Ω≥1 è finito per `BoundedSlopeCatalogue.catalogue_finite` con R=1; la restrizione ai seed unità è un suo sottoinsieme. Pertanto F(n) esiste ed è realizzato, anche quando n è periodico. Il potenziale Ωu≤n dà il bound sui seed u≤n e F(n)≤n.

L'esistenza del massimo non offre un clock algoritmico: la finitezza del catalogo non fornisce un tempo entro cui decidere l'assenza di ulteriori hit da un piccolo seed. U12 non afferma tale algoritmo.

Per un genitore unità x, concatenare un cammino che realizza F(x) con x→n dimostra che `M_x=ω_xF(x)` è il massimo peso del ramo. Ogni parola non vuota verso n si decompone in questo modo. Dunque

`F(n)=max(1,sup_x M_x)`.

Se F(n)>1, un cammino massimizzante non vuoto individua un ramo con M_x=F(n). La parola vuota deve rimanere separata; per F(n)=1 non è lecito sostituire automaticamente F con il massimo dei rami.

Iterare l'armonicità e usare il floor sul seed dà `g(x)≥c₀F(x)`. Quindi LF=ΣM_x≤g(n)/c₀ è finito. Applicare il lemma dei testimoni a insiemi crescenti di rami che includono quello massimizzante dà, per F(n)>1,

`D(n)≥(c₀/g(n))[LF(n)−F(n)]`.

Il surplus A=LF−F è allora nonnegativo. Un certificato finito produce un lower di A: la funzione somma delle coordinate meno la loro massima è monotona quando le coordinate aumentano o vengono aggiunte. Questo giustifica anche l'uso di testimoni non massimizzanti.

## 3. Riduzione diretta mediante densità: PASS senza Q

Assumere il lower esterno uniforme `underline d(P(u))≥c/u` per ogni seed unità u. Per il ramo x scegliere un cammino dal seed u che realizza M_x. L'inclusione P(u)⊆P(x) e Ωu≤n danno

`underline d(P(x))≥c/u≥cM_x/n`.

Al root senza ritorni i bacini dei diversi genitori sono disgiunti. La finita additività dei conteggi e la superadditività del limite inferiore, seguite dal supremo sugli insiemi finiti, provano LF(n)≤n/c. Non viene assunta l'esistenza della densità di un'unione infinita.

Sulla spine divergente, anche i bacini dei genitori off-spine appartenenti a indici j diversi sono disgiunti: dopo essere entrata nella spine un'orbita non può entrare in un secondo ramo off-spine; un ingresso in ordine inverso ripeterebbe uno stato della spine. Per ogni allocazione finita di tali rami la somma dei loro lower di densità è al più1.

Quando F(n_j)>1,

`0≤A(n_j)≤Σ_(x≠n_(j−1))M_x(n_j)`.

Il limite crescente delle allocazioni finite dà quindi

`Σ_(j≥J) A(n_j)/n_j≤1/c`.

Il seed unità iniziale b della spine fornisce `F(n_j)≥n_j/(bP₀)`, mentre log(n_j+1)≤C_b+jlog(3/2). Il lower postulato A(n)≥c_ε n/(1+log n) sui grandi root F-heavy renderebbe divergente la serie. Tutta questa implicazione usa soltanto oggetti aritmetici e il lower di densità dichiarato; non usa g o Q.

La direzione logica opposta è qualificata correttamente. F(n)≥εn implica m_U(n)≤1/ε. Se tutte le orbite fossero eventualmente periodiche, i root interessati apparterrebbero all'unione finita delle orbite di quei finitissimi seed. Il lower oltre una soglia sarebbe vacuo. Non si ottiene una prova di H né l'esclusione di tutti i cicli.

## 4. Confronto con il minimo antenato e baseline

Il confronto `n/(P₀m_U(n))≤F(n)≤n/m_U(n)` è corretto. L'upper vale per ogni parola; il lower sceglie il primo arrivo dal minimo seed unità, che è iniettivo anche quando il target è periodico. Il caso della parola vuota è innocuo.

Il minimo ordinario m_* è dispari ma può essere multiplo di3. Se lo è, il suo primo iterato Syracuse è una unità che raggiunge ancora il target ed è al più2m_*. Quindi m_U≤2m_*. Il passaggio dal tail di fonte12 ai root F-heavy richiede quell'input supplementare e non è nascosto nella riduzione diretta.

Fra i primi tre esponenti ammessi e₀,e₀+2,e₀+4, con e₀∈{1,2}, esattamente uno produce una foglia divisibile per3. Restano due genitori unità con e≤6 e M_x≥ω_x≥3/64. Rimuovere il ramo massimo ne lascia almeno uno: per F>1, A(n)≥3/64. La condizione F>1 è essenziale per identificare A con la somma privata del ramo migliore.

## 5. Certificato593: completamento globale corretto

Il dominio preregistrato enumera soltanto seed dispari non divisibili per3. Per questo il minimo unità è31, non27. La correzione della previsione testuale è registrata e non cambia la griglia del programma.

La traiettoria esplicita da31 a593 ha14 passi e totale18, quindi Ω₁=3¹⁴/2¹⁸=4782969/262144. Il secondo ramo proviene dal seed6325 in un passo di esponente5, con Ω₂=3/32. La traiettoria separata da593 a1 ne certifica il nonritorno.

Il censimento risolve ogni seed unità≤6325. Non registra tutti i pesi di tutti i seed, ma in questo caso basta: nessun seed unità<31 raggiunge593; per ogni intero u≥33, `593/u≤593/33<Ω₁`. Il solo candidato31 dunque certifica F globale. Per gli altri rami, il censimento trova soltanto6325, e ogni seed u>6325 è intero almeno6326, con `593/u≤593/6326<3/32` perché 3·6326>32·593. Questo chiude davvero il secondo massimo di ramo, senza estrapolazione del cutoff.

Ne segue A(593)≥3/32. Il bound su D resta condizionale al floor e all'upper della traccia; non è un valore numerico del kernel limite. La lettura statica del programma conserva guardie esplicite anche in modalità ottimizzata e vieta di trasformare un timeout o un ciclo sconosciuto in un no-hit. Non ho rieseguito il censimento e non ne uso i conteggi come prova asintotica.

## 6. Complessità di un dizionario periodico fissato

Per una parola q non vuota, con a=3^ℓ, d=2^A e c=C(q), il denominatore D_q=a−d è non nullo e coprimo con6. La relazione `d^t(D_qx_t+c)=a^t(D_qx+c)` dà d^t|(D_qx+c) quando l'intero a destra non si annulla.

Da questa divisibilità segue Atlog2≤log(K_q(x+1)). La crescita shifted per ogni passo e ℓ≤A danno `x_t+1≤C_q(x+1)^Λ`, Λ=log₂3. Se D_qx+c=0, il blocco ripete invece un punto fisso e il suo endpoint resta x: la stessa maggiorazione dell'endpoint vale senza imporre primo arrivo o negare cicli ipotetici. Le potenze di lunghezza zero si omettono o si trattano come identità.

Componendo al più s pezzi si ottiene il bound di U12 su log(n+1). Se u=O(log n), esso impone

`s≥[loglog n−logloglog n]/log(log₂3)−O(1)`.

Le costanti dipendono dal dizionario fissato. Il medesimo tipo di necessità per il numero dei passi non-1 segue separando le corse di1. Queste barriere riguardano una complessità costruttiva fissata; non confutano il criterio dei seed e non coprono dizionari che crescono con n.

## 7. U15: profilo canonico e stabilizzazione esatta

Ho letto la nota U15 `U15_MAXPLUS_IT.md` nello snapshot `2f7d1ac0b1f349fa12d32fa8074b7cec970478187262380ae414f01caa1f1f04`.

Tutte le parole che realizzano F(n) hanno lo stesso profilo (K,E), per unicità della fattorizzazione del gain 3^K/2^E. Ogni loro seed u soddisfa F(u)=1, altrimenti la concatenazione di un witness migliore lo contraddirebbe. Lo stesso argomento calibra ogni prefisso. Il rango K scende quindi di uno seguendo un genitore ottimale e termina a F=1; non è un rango di terminazione forward. Il caso F=1 corrisponde a K=E=0 e alla sola parola vuota.

Sulla spine divergente da b, tutti i seed ottimali sono limitati da bP₀. Dopo il massimo dei finitissimi indici d'ingresso di quei seed nella spine, il rapporto fra il loro gain e Ω(b→n_j) è costante. Quindi F(n_j)=C_*Ω_j, l'insieme ottimale si stabilizza e K(n_j)=j+costante. Oltre quegli ingressi ogni cammino ottimale ha come ultimo genitore n_(j−1); il massimo è unico a livello di ramo. Ripetendo l'argomento per i seed≤bP₀/δ si ottiene che il massimo laterale diviso per F(n_j) tende a zero. Il tempo di stabilizzazione resta esistenziale, senza una velocità uniforme.

Sono corrette anche l'equivalenza con l'assenza di spine calibrate infinite e la carica ℓ^p dei singoli rami laterali: i seed scelti per i rami sono distinti, dunque i loro reciproci alla potenza p>1 hanno somma finita. Questo non controlla da solo la somma ℓ¹ dei rami. Il potenziale V=n/F cresce su un passo calibrato di 1/(3F), ma può restare limitato; non è un rango discreto.

L'identità Bellman per Z=F/g è QZ−Z=A/g. Il drift nonnegativo vale solo su F>1; l'insieme F=1 non è finito. Una giustificazione elementare di quest'ultima affermazione: ciascuno degli infiniti genitori unità x≠1 di1 è raggiunto da un seed ottimale con F=1, mentre una singola orbita forward incontra al più uno di tali x, perché dopo x arriva a1. I seed scelti sono pertanto distinti. Questa giustificazione è stata comunicata da U15 separatamente e non cambia lo snapshot.

## 8. U15: primi crossing finiti e cap a gradini

Ho letto `U15_FINITE_CAP_IT.md` nello snapshot `4d4618aca2449eb4662b62d767e857963597b83aa844a6cc9551ec3cd86b050c`.

Qui i prefissi del crossing sono **outermost-first**, come in U01. Per trasferire la finitezza del catalogo Lean di parole forward si usa la reversione: il gain resta uguale, ma un prefisso forward non va confuso con un prefisso inverso.

Il primo crossing di un cap B≥1 ha gain>B≥1, quindi appartiene al catalogo finito di tutte le parole intere, comprese quelle con sorgente foglia. Il relativo insieme T_B è finito e prefix-free. Per m maggiore di tutte le sue lunghezze, la differenza fra densità non capped e cap del prefisso si partiziona in una somma finita dei seguiti ρ_(m−|w|)(u_w). Rimane almeno un passo: i termini che terminano su foglie sono zero, non ρ₀=1.

Si può dunque passare direttamente al Cesàro root per root. La prova non richiede più una dominazione uniforme C_D, un floor assoluto o un upper lineare di g. Rimane indispensabile pagare il futuro della legge originale con l'errore ρ*_m/B e il Green non pesato sommabile. La finitezza del catalogo dei crossing non rende nullo quell'errore: il futuro originale può non restare compatibile con lo stesso intero a precisione crescente.

L'identità `g_B=g·Q(H≤B)` segue dalla somma finita delle probabilità dei primi crossing. Anche i target periodici sono ammessi con gli input dichiarati. Sotto Q ogni prefisso ha gain≤F; i gain almeno1 appartengono a un catalogo finito, e A₀=1. Il sup H è quindi un massimo con supporto finito. Una parola ottimale ha probabilità positiva, perciò il cap minimo che conserva tutta la traccia è esattamente F.

L'unicità del profilo ottimale dà `{H=F}={A_K=F}`. I cilindri ottimali alla stessa profondità sono disgiunti e corrispondono a seed distinti; dunque il salto superiore è `FΣ_opt g(u)`. Il caso F=1 è trattato estendendo g_B=0 per B<1 e restituisce il salto totale g(n) a1. Il lower relativo del salto sui root F-heavy richiede, soltanto per quel corollario, il floor e l'upper lineare dichiarati.

Il budget affine suggerito durante questa revisione è corretto: `n=A_mY_m+(1/3)Σ_(i=1)^mA_i` implica Σ_(i≥1)A_i≤3n lungo ogni cammino inverso positivo. Equivalentemente, posto h(x)=(x+1/3)g(x), l'armonicità dà K₂h(n)=ng(n), quindi h−K₂h=g/3. Il telescopio finito e la positività provano `Σ_(m≥0)K₂^m g(n)≤(3n+1)g(n)`. Si tratta del terminale g, non di g², e non sostituisce automaticamente il Green non pesato necessario per le foglie e il futuro originale.

**PASS anche su queste due note U15.** Il clock uniforme e il lower del surplus non sono stati ottenuti; nessun principio generale consente di perdere poca traccia avvicinando il cap a F dal basso.

## Esito e limiti

Nessuna correzione matematica necessaria allo snapshot U12 assegnato. Il nuovo obiettivo A è ben definito e ammette certificati finiti reali, ma l'ordine n/log n manca interamente: il lower costante non lo approssima alla scala dei root pesanti. La priorità bibliografica globale del raccordo max-plus non è stata stabilita.

Le due note U15 sono incluse nei nuovi snapshot della ricevuta. Non si promuove la stabilizzazione esistenziale del massimo a un cutoff effettivo dei tempi di arrivo.
