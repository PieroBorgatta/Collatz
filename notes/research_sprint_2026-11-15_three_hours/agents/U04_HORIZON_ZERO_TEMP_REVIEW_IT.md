# U04 — Audit del selettore, del clock e dei certificati adattivi

16 novembre 2026. Revisione matematica indipendente su snapshot di U15_ZERO_TEMPERATURE_IT.md, U14_COLOURED_HORIZON_IT.md, U14_ADAPTIVE_CERTIFICATE_IT.md e U15_LINEAR_CAP_IT.md; verifica condizionale dell'interfaccia U14_SOURCE147_INTERFACE_IT.md. Hash e copie esatte sono nella ricevuta associata. Nessun esperimento, censimento, build, GPU o modifica dei testi originali.

**Esito: PASS entro gli input e i domini espliciti.** Il modello reale della sezione 5 di U15 è qui specializzato a u=1. Il bound di orizzonte di U14 resta condizionato al prefattore del post16. Nessuno di questi risultati dimostra il lower di A o il clock critico.

## 1. Green_p e selezione degli ottimali

Il budget affine già verificato è G₂(n)≤(3n+1)g(n), con pesi terminali g(u), includendo la parola vuota. Poiché Ω≤F e G₂ è finito, la convergenza dominata con dominante Ω²g(u)/F² dà G_p/F^p→Σ_opt g(u). Un singolo witness ottimale positivo e l'upper G_p≤F^(p−2)G₂ danno G_p^(1/p)→F.

La scrittura degli ottimali come seed, anziché parole, è lecita: il gain ottimale fissa univocamente lunghezza e somma degli esponenti per fattorizzazione in 2 e 3; un seed e una lunghezza fissano il cammino deterministico. Gain uno implica la parola vuota. Il bound più forte FΣ_opt g≤g proviene dall'armonicità o dal salto superiore, e non va attribuito al solo budget Green.

## 2. Gap relativo sulla classe heavy nonreturn

Se Ω≥F/2 e F≥εn, il potenziale Ωu≤n impone u≤2/ε. Un ottimo ha seed v≤1/ε. Ci sono dunque finitissime coppie (u,v). Per un target nonreturn ogni seed lo incontra al più una volta; dopo il primo merger asincrono di due orbite, il rapporto dei gain verso tutti i discendenti comuni nonreturn è costante. I rapporti strettamente minori di uno così ottenuti sono finitissimi. Il loro massimo con 1/2 è r_ε<1.

Il dominio nonreturn è essenziale a questa prova: non vengono ignorati possibili giri di ciclo in parole diverse. Il lemma è esistenziale e non fornisce un algoritmo per decidere tutti i merger o un valore effettivo di r_ε.

Sommando le parole nonottimali si ottiene

`0≤G_p/F^p−Σ_opt g≤r_ε^(p−2)G₂/F²`.

La normalizzazione col salto massimo dà, senza floor né upper di g,

`0≤F^(1−p)G_p/g−Q_n(H=F)≤(4/ε)r_ε^(p−2)`.

Per ogni δ>0, lo stesso argomento con seed u≤1/(δε) rende finito l'insieme dei rapporti Ω/F≥δ. L'unicità degli esponenti primi rende finito anche l'insieme degli offset (k−K,E−E_opt). Non viene limitato K assoluto.

## 3. Heavy, raggiungibilità e forza logica dei target

Le inclusioni H_(1/R)⊆B_R⊆H_(1/(RP₀)) sono corrette su tutti i target unità: la prima usa un ottimo, la seconda una parola di primo arrivo e il prodotto correttivo P≤P₀. La parola vuota e i target periodici non costituiscono eccezioni. Resta necessario l'input di primo arrivo; la costante P₀ non è stata cancellata.

Ne segue che ogni H_ε è finito, F=o(n), e l'assenza di orbite divergenti sono equivalenti qualitativamente. Qui assenza di divergenza ammette eventuali cicli non banali: non coincide, da sola, con la piena congettura di Collatz.

Nel quadro del lower esterno di densità che dà il budget Σ_j A(n_j)/n_j<∞, il lower critico A≥c_ε n/(1+log n) sulla classe heavy nonreturn implica assenza di divergenza. Il viceversa è vacuo perché le classi heavy diventano finite. La stessa osservazione vale per il target di clock K≤log_(3/2)(n+2)+C_ε: su una spine divergente K=j+costante per stabilizzazione, mentre N(j), il numero di esponenti almeno due, tende a infinito e n_j+1≤(b+1)(3/2)^(j−N(j)). La nota non vende questi target come ipotesi logicamente più deboli della nondivergenza.

## 4. Modello reale: perimetro verificato

Specializzo il parametro ammesso dalla nota a u=1. Per t≥T≥5, la derivata della quantità dentro il floor è fra uno e due; ogni incremento E_t−E_(t−1) è quindi uno o due. Il floor dà F_t comparabile a t², F_t>1 per t>0 e Σ_t1/F_t<∞. I valori V_t sono compresi fra uno e una costante finita.

La ricorrenza reale x_t=(3/2^e_t)(x_(t−1)+1/3) è esatta. Gli stati possono essere considerati anche come altezze reali distinte, non soltanto come vertici etichettati: scrivendo x_t=A_t/2^E_t si ha A₁=4, A₂=14 e A_(t+1)=3A_t+2^E_t. Per t≥2, ν₂(A_t)=1, mentre E_t cresce strettamente; i denominatori ridotti distinguono tutti gli x_t successivi. Inoltre x₀=1 e x₁=2 sono distinti dagli altri. Dunque g(x_s)=F_s è ben definito, x_s≥1 e F_s≤x_s.

Sul grafo lineare dichiarato, il catalogo è esattamente quello dei suffissi: Ω_(s→t)=F_t/F_s. Baseline uno e F_s>1 per s>0 danno F(x_t)=F_t, ottimo unico s=0 e K=t. I momenti sono

`G_p(x_t)=F_t^p Σ_(s=0)^t F_s^(1−p)`.

Il budget affine segue da Σ_(s=0)^t1/F_s=3(V_t−1)+1/F_t≤3V_t+1/F_t. Tutti gli upper Green_p indicati nella nota e la convergenza del selettore sono dunque soddisfatti. Eppure x_t è comparabile a t² e K/log x_t diverge.

Questo è un controesempio all'inferenza del clock dai soli vincoli elencati. Non è un controesempio nel grafo intero: già x₁=2 non è dispari e x₂=7/2 non è intero. Non costruisce il vero kernel Q, tutti i genitori o il sistema armonico canonico completo. La conclusione negativa non si estende a prove che usano queste informazioni mancanti.

## 5. Orizzonte dei certificati con rami distinti

Conservo al più un witness nonvuoto per primo genitore fisico. La funzione R(v)=Σv−max v è monotona per coordinate, quindi R(v)≤A quando F>1 e LF è finito. La formulazione lineare richiede ogni possibile ramo rimosso; per famiglia vuota è necessaria la condizione separata ℓ≤0. Ripetizioni dello stesso ramo non possono essere sommate come coordinate diverse.

Parole di rami diversi sono distinte; se tutte hanno lunghezza Syracuse ≤K, la somma dei loro gain è ≤Σ_(k=1)^Kρ_k(n). Condizionatamente al bound uniforme esterno del post16, ||ρ_k||∞<(5/3)(3/2)^k, la somma geometrica dà R(v)<5[(3/2)^K−1] per K≥1. K=0 contiene soltanto la famiglia vuota.

Ne segue correttamente la necessità

`K>log_(3/2)n−log_(3/2)(1+log n)+log_(3/2)(c_ε/5)`

per un certificato che paghi c_ε n/(1+log n). È una barriera a questo formato di certificato, non a ogni possibile prova aritmetica. Il prefattore del post16 resta un input esterno: non è stato rieseguito qui il relativo certificato e non viene sostituito dal solo tasso esponenziale della fonte9.

## 6. Verificatore adattivo: completezza per soglie strette

K_t=K₀+t e U_t=(n+1)2^t tendono entrambi a infinito; ogni fase esamina un insieme finito di cammini interi esatti. Ogni parola finita, quindi ogni massimo di ramo M_x, compare a una fase finita. I record crescono per coordinate. Da LF<∞ e dalla convergenza monotona segue Σ_xv_x(t)↑LF.

Quando F>1, un witness nonvuoto che realizza F viene trovato a una fase finita. Da quel momento max_xv_x(t)=F. Anche prima la funzione R è monotona; pertanto R_t↑LF−F=A. Il controllo gain>1 certifica il dominio corretto senza conoscere F. Se A>ℓ>0 la procedura termina; se A≤ℓ può proseguire indefinitamente e non produce un esito negativo. I cicli sono inclusi nei cammini finiti e raggruppati correttamente.

Anche le stime aritmetiche sono corrette: S(y)+1≤(3/2)(y+1) limita i bit delle altezze a O(log(n+1)+t). Dal telescopio 2^A=(u/y_k)Π_(i=0)^(k−1)(3+1/y_i)≤4^k u/y_k segue A≤2K_t+log₂U_t. Il numero U_tK_t conta passi forward, non costo totale in bit. Una soglia irrazionale va sostituita da una maggiorazione razionale certificata e raffinata sfruttando il margine stretto.

La completezza a target fissato non fornisce un tasso uniforme di arresto, un cutoff negativo o il lower ancora aperto. Questi tre testi precisano il contratto del problema senza risolverlo.

## 7. Quota positiva a cap lineare

Su una spine divergente da b, gli stati interi sono distinti e quindi n_r→∞. Dal prodotto di primo arrivo segue Ω_r=n_r/(bP_r)→∞. Per c>0 si può fissare s con Ω_r≥1/(cb) per tutti r≥s. Ogni prefisso del backtracking n_j→n_s ha gain Ω_j/Ω_r≤c n_j. Il cap residuo al tempo s è c bP_jΩ_s≥1.

Il cilindro di quel backtracking seguito dall'evento H_s≤1 è dunque safe; la sua massa è

`Ω_j h(n_s)/(Ω_s g(n_j))≥h(n_s)/(C bP₀Ω_s)>0`

usando l'upper g(n)≤Cn e la positività puntuale h(n_s)>0. Questo prova la quota liminf positiva, senza floor. Il tail bound su tutti gli r≥s è indispensabile; non basterebbe controllare soltanto Ω_s.

Ogni root ε-heavy è raggiunto da un seed unità≤1/ε. Il pool è finito: le orbite eventualmente periodiche contribuiscono finitissimi target, e sulle altre il minimo delle quote positive dà uniformità esistenziale oltre una soglia. Le costanti restano non effettive e non sono uniformi in c↓0. L'affiancamento al cap sublineare di U01 è lecito con gli input di quest'ultimo; non autorizza un passaggio a un cap o(n).

Il lower assoluto separato della sezione 3 richiede il floor c₀. Da g(n)≥c₀ΣM_x si hanno al più floor(g(n)/c₀) rami M_x>1; un ramo safe esiste fra i primi floor(g(n)/c₀)+1 genitori unità, con esponente al più sei volte quel numero. Il suo cilindro paga almeno 3c₀·2^(−6[floor(g(n)/c₀)+1]). La stima è corretta e soltanto exp(−O(n)) con l'upper lineare; non paga il lower critico di A.

## 8. Interfaccia condizionale della durata esterna

Assumendo l'equazione (7) esterna riportata da U14, log R≤C_W(k+1)/log(k+2). Essa implica prima k+1≥c log R e poi, reinserendo quel lower nel denominatore, k+1≥c' log R·loglog R per R sufficientemente grande. È un'inversione valida dell'input, non un nuovo audit della sua prova effettiva o delle sue dipendenze.

La variante K_t=(K₀+t)² mantiene l'enumerazione completa di ogni parola finita e ha bit O((log(n+1)+t)²). A n fissato, eventuali witness della frontiera K_t/2≤|w|≤K_t hanno R almeno dell'ordine di t. Se n è nonreturn, una parola verso n non può avere già visitato uno o un ciclo positivo; la guardia importata è automatica. Segue il lower condizionale di costo c_W log t·loglog t, per ogni dizionario finito fissato prima di t. Non segue l'esistenza di tali witness o il loro contributo a rami distinti.
