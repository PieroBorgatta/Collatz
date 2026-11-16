# Editor reali: il cambio deve partire presto, il carry deve crescere

16 novembre 2026. Ricerca su carta; nessun esperimento, solver o compilazione. Le formule dei §§2–5 sono state controllate indipendentemente da H23, con la guardia sul possibile termine anticipato della parola alternativa. Non è stato costruito un editor con massa relativa non sommabile.

## 1. Obiettivo e quantificatori

Si ipotizzi una spine divergente `n_j=S^j(b)`, con b positivo dispari non divisibile per3. La parola osservata ha gain Ω_j e prodotto `n_j=bΩ_jP_j`, `1≤P_j≤P₀`. Un witness utile è una parola effettiva `w_j:v_j→n_j` che entra dal genitore finale diverso da quello osservato. Il clock può cambiare. Il suo peso relativo è

`Γ_j=Ω(w_j)/Ω_j=bP_j/(v_jP_alt)`.

Si cercano witness o antichain di witness per cui `ΣΓ=∞`; i budget precedenti lo escluderebbero sotto l'input esterno del floor degli atomi. Una mera congruenza, un compagno affine razionale o una famiglia di parole a ogni profondità non fornisce il witness intero richiesto.

## 2. Vincolo esatto sul prefisso forward preservato

Due semi dispari distinti b e v che condividono un prefisso Syracuse di r valutazioni, totale P, soddisfano

`S^r(v)−S^r(b)=3^r(v−b)/2^P`.

Entrambi gli endpoint sono dispari. Di conseguenza

**`2^(P+1) | (v−b)`**.

È la proprietà classica dei cilindri di valutazioni, già usata nelle note precedenti; non una nuova scoperta. Per un witness con `v≤C_b j log j`, ne segue `P+1≤log₂(b+C_b j log j)`. Il primo cambiamento deve quindi avvenire entro O(log j) bit del prefisso iniziale, oppure la parola alternativa deve essere già terminata entro quella soglia. Il clock finale libero impone questa seconda possibilità e non va ignorato.

C'è una conseguenza direttamente sul costo. I seed laterali associati a tempi diversi sono distinti; quindi v_j>b per tutti tranne finitissimi successi. Per questi tempi,

`v_j≥b+2^(P_j^common+1)`,

`Γ_j≤bP₀ 2^(−P_j^common−1)`.

Se un editor preserva `r_j≥(1+ε)log₂j` valutazioni iniziali per tutti i suoi successi grandi, allora `P_j^common≥r_j` e `ΣΓ_j<∞`. Un edit confinato a una breve finestra presso il target conserva quasi tutto il prefisso e paga un costo esponenziale. La sola finestra reale di Weyl può fornire contesti frequenti, ma non risolve questo obbligo di cambiamento iniziale e pullback globale.

Questa stima non vieta editor globali che cambiano presto e si ricongiungono tardi. Specifica il tipo di editor da cercare.

## 3. Un costo medio necessario, prima dell'analisi

Per un witness per tempo i seed laterali sono distinti. Più in generale lo sono i seed di una famiglia globale prefix-free: due percorsi dello stesso seed sono comparabili nell'albero inverso, perché la dinamica forward è deterministica.

Le unità positive dispari sono le classi1 e5 modulo6. Se `v_(1)<…<v_(N)` sono N seed distinti, `v_(r)≥3r−2`. Posto `C=bP₀`, la relazione `Γ≤C/v` implica

`#{w:Γ_w≥t}≤C/(3t)+O(1)`

e, scrivendo `E_w=−log₂Γ_w`,

`Σ_(w≤N) E_w≥log₂(N!)+Nlog₂(3/C)−O(log N)`.

Il costo medio è dunque almeno `log₂N−O_b(1)`. Il target `E_j≤log₂j+log₂log j+O_b(1)` si colloca vicino alla scala combinatoria minima. Questo counting non lo esclude: una sequenza di seed dell'ordine di j log j resta compatibile con la sola aritmetica dei distinti. Il floor esterno dà invece un budget di primo ordine più forte, e proprio contro quello si vorrebbe costruire una contraddizione.

## 4. Compagni affini: ricorrenza esatta e obbligo mancante

Se due stati sono legati da `y=a x+c`, e i rispettivi passi reali hanno valutazioni e,f, allora

`x'=(3x+1)/2^e`,

`y'=a' x'+c'`,

`a'=2^(e−f)a`, `c'=(3c+1−a)/2^f`.

Queste identità non garantiscono che y sia intero, positivo, dispari, unità, né che f sia la valutazione effettiva. Queste guardie devono accompagnare ogni transizione; lasciarle implicite trasforma l'automa in un calcolo affine astratto.

Per e=f la slope a resta fissa. Se a≠1, la variabile `z=c/(1−a)` evolve come `z'=(3z+1)/2^e`. Un compagno che persiste con la stessa parola è quindi governato da un'altra orbita razionale, non da un carry arbitrariamente azzerabile.

Per un blocco W, il suo affine `T_W(x)=λx+τ` ha fixed point `r=τ/(1−λ)` quando λ≠1. La trasformazione `H_a(x)=a x+(1−a)r` commuta con `T_W`. Questa identità spiega perché compagni piccoli possano seguire un corridor periodico; la legalità a ogni singolo passo resta da provare. Se due blocchi hanno fixed point distinti, nessuna H_a non identica può commutare con entrambi: passare tra corridor diversi richiede cambi di stato/carry.

La [fonte148, §5](https://rstation.ai/problems/collatz/papers/148) offre un esempio effettivo: il corridor `(1,2)^M(d)`, d≥5, ammette il compagno `(n−5)/2` e una parola concorrente esplicita. È un risultato del manoscritto, non un editor costruito qui. Applicato solo a una finestra mobile, il nuovo seed resta dell'ordine dello stato all'inizio della finestra; non diventa O(j log j) senza pullback attraverso il prefisso.

## 5. Un automa finito di slope non compra un clock illimitato

Per una transizione che consuma s passi osservati, totale A, e r passi concorrenti, totale B, la slope cambia di

`a_out/a_in=3^(r−s)2^(A−B)`.

Su un ciclo che torna alla stessa slope, l'indipendenza moltiplicativa di2 e3 impone `r−s=0` e `A−B=0` per i totali del ciclo. Con slope iniziale fissata e un insieme finito di slope razionali, la differenza cumulativa dei clock resta limitata: è determinata dalle valutazioni prime del rapporto finale/iniziale.

Quindi la libertà di clock illimitata richiede slope/carry che crescono, oppure una rinormalizzazione con un costo esplicito. Una notazione compatta per quei grandi stati non paga il debito fisico. Questo non vieta editor con clock difference limitata né automi con famiglie crescenti di stati.

## 6. Un filtro finito per compagni di corridor commutanti

Questa è una classe propria di tentativi, non il problema generale: il blocco osservato W è espansivo, ha fixed point `r=−p/q`, con p,q positivi coprimi, e il medesimo compagno `H_a(x)=a x+(1−a)r` deve commutare con W. La slope è un monomio positivo `a=2^u3^v`, con u,v **interi**, come accade quando H è il rapporto affine fra due dizionari terminali Collatz, anche con clock diversi.

Definire `R₆(m)=m/[2^ν₂(m)3^ν₃(m)]` per m intero positivo. Se `H_a(b)=v₀` è un intero positivo distinto da b, allora

`a=(qv₀+p)/(qb+p)`

e quindi l'essere monomio è equivalente alla condizione finita

**`R₆(qv₀+p)=R₆(qb+p)`**.

In particolare,

**`R₆(qb+p) | (v₀−b)`**.

Infatti `gcd(qb+p,q)=1`, perciò `gcd(qb+p,qv₀+p)=gcd(qb+p,v₀−b)`. Il denominatore ridotto di a contiene solo2 e3; tutta la parte R₆ del denominatore non ridotto deve dunque cancellarsi nel gcd.

Per qualunque bound V≥1, la condizione

`R₆(qb+p)>max(b−1,V−b)`

esclude **ogni** compagno positivo distinto≤V di questa classe. La versione `R₆(qb+p)≥b` esclude tutti i compagni più piccoli di b. Quest'ultima da sola non attacca l'editor della spine: per b fisso i seed laterali saranno quasi tutti>b. Il bound con V, per esempio `V=C_bj log j`, è il filtro pertinente al programma minimo. La congruenza necessaria non sostituisce le ulteriori guardie di legalità della parola.

La parte R₆ è un'invariante esatta del corridor, perché

`q T_W(x)+p=(3^|W|/2^||W||)(qx+p)`.

Quando entrambi gli stati sono interi, moltiplicare per questo monomio non cambia R₆. Perciò il solo prolungamento dello stesso corridor non produce nuove classi di compagni disponibili.

Un secondo limite elimina una falsa scappatoia: se due parole positive W,V hanno lo stesso fixed point razionale, esse sono potenze dello stesso periodo primitivo della dinamica2-adica. Il numeratore affine C(W) e `3^|W|−2^||W||` sono dispari, quindi il fixed point è dispari2-adico. Ricostruendo all'indietro con `I_e(y)=(2^e y−1)/3`, ogni intermedio resta dispari; W eV sono dunque itinerari esatti del medesimo punto. Il determinismo li rende returnword della stessa orbita periodica. Il valore−1/3 non dà un'eccezione: manderebbe a0 e non potrebbe tornare in un periodo dispari.

Ne segue che un unico H non identico che commuta con un menu di blocchi non consente una vera concatenazione di corridor differenti: se condividono il fixed point, sono tagli dello stesso periodo; se hanno fixed point diversi, H non può commutare con entrambi. Un processo con H che cambiano può ancora funzionare, ma deve pagare e controllare proprio quelle transizioni.

Questi lemmi finiti sono stati controllati da H23. Non sono un'esclusione generale degli editor e non si rivendica priorità: forniscono un test preciso per scartare l'ansatz del compagno commutante prima di investire in costruzioni più lunghe.

## 7. Non promuovere una visita obbligata a frequenza positiva

[Monks et al., arXiv:1204.3904v2, Theorem6.4](https://arxiv.org/html/1204.3904v2#S6) prova che ogni orbita divergente contiene un valore20 modulo27. Applicando il risultato alle code si ottengono visite illimitate. Serve prudenza se si vuole una frequenza positiva per pagare il peso1/(j log j).

Il grafo modulo27 contiene il self-loop rosso26→26. Un positivo non può seguirlo per sempre, ma può seguirlo per un numero finito arbitrariamente grande: scegliendo un positivo congruo a−1 modulo un'alta potenza di2 e modulo27, il tratto iniziale di soli passi dispari ha la lunghezza desiderata e resta26 modulo27. La potatura usata in un argomento qualitativo non fornisce quindi un bound uniforme sulle lunghezze di quei tratti. Nessuna frequenza positiva delle visite a20 viene dedotta qui. Inoltre il clock di Monks è quello shortcut T, non direttamente l'indice Syracuse j del programma minimo.

## 8. Un menu effettivo: cambiare presto e seguire una parola mista

La barriera del §6 riguarda un compagno che COMMUTA con i blocchi osservati. Si può uscire da quell'ansatz facendo seguire al compagno blocchi diversi. È il meccanismo classico delle paired words, non una nuova idea mai tentata: [Elia–Tucker2015, §§3–5](https://arxiv.org/html/1511.09141v1) è un riferimento pertinente e segnala anche il rischio di classificazioni finite incomplete. Qui ne viene adattata una piccola istanza alle guardie di unità, colore e costo del progetto.

Per parole W,V della stessa lunghezza k e totale A, e traslazione pari c, vale

`T_V(x+c)=T_W(x)+c` se e solo se `C(V)−C(W)=c(2^A−3^k)`.

Se x e x+c sono positivi dispari e W è la parola effettiva di x, l'identità rende il terminale di V intero dispari; il criterio esatto dei cilindri implica che V è la parola effettiva di x+c. Non è solo una relazione fra gain.

Prendere c=−2 e le due regole

`W₁=(1,2) → V₁=(2,1)`,

`W₂=(2,1,2) → V₂=(1,1,3)`.

Per W₁,V₁, le costanti sono5 e7, con denominatore8 e numeratore lineare9. Per W₂,V₂ sono29 e19, con denominatore32 e numeratore lineare27. In entrambi i casi la condizione precedente vale. Le guardie sono esplicite: `Cyl(W₁)=11 mod16` passa a `9 mod16=Cyl(V₁)` sottraendo2; `Cyl(W₂)=57 mod64` passa a `55 mod64=Cyl(V₂)`. Il secondo blocco ha gain27/32<1; il linguaggio generale `{W₁,W₂}*` non va chiamato interamente espansivo.

Per qualunque concatenazione finita p di W₁,W₂, indicare con σ(p) la sostituzione dei blocchi. Ogni x che realizza p ha il compagno x−2 che realizza σ(p), con differenza2 a ogni confine di blocco. I due blocchi non sono potenze di uno stesso periodo e hanno fixed point rispettivamente−5 e29/5. È quindi una vera concatenazione di contesti differenti, attraverso CONIUGAZIONE e non commutazione.

### Un gate terminale preso dalla fonte152

La [fonte152/v1, §4, Eq4.4 e Theorem3](https://rstation.ai/problems/collatz/papers/152) fornisce

`w₂₂=(1,1,2,1,2,1,2,1,2,1,2,1,2,2,2,2,1,2,1,2,2,1)`

e il rivale `g₂₂=(2,1^15,2,2,1,4,3,3)`, con seed `(x−3)/4` e rapporto di gain4. È la word binaria NON bilanciata della fonte152, diversa dall'omonimo w₂₂ Sturmiano della fonte149. I certificati esterni non sono stati rieseguiti.

Poiché `S(4u+1)=S(u)`, sostituire il primo esponente2 di g₂₂ con4 produce g'₂₂, seed `4[(x−3)/4]+1=x−2` e rapporto di gain1. Pertanto

**`p·w₂₂` e `σ(p)·g'₂₂` si fondono con seed iniziali b e b−2.**

Lunghezze e totali coincidono; Γ=1. L'ultimo esponente osservato è1, quello concorrente3, quindi l'ultimo genitore è diverso. Per p non vuoto, il primo esponente cambia immediatamente: W₁ inizia con1 e V₁ con2, W₂ con2 e V₂ con1. Si è quindi ottenuto un esempio parametrico di cambiamento iniziale, inseguimento legale lungo una parola mista e fusione finale. Non è dimostrata la copertura di un futuro dato.

Per b unità, se `b≡1 mod3`, il seed b−2 è già unità. Se `b≡2 mod3`, esso è una foglia: rimuoverne il primo arco dà un seed unità e un clock più corto di1. Il peso relativo diventa `2^e/3`, dove e è il primo esponente concorrente. È4/3 se p inizia con W₁, 2/3 se inizia con W₂, 16/3 se p è vuoto. L'ultimo genitore alternativo resta tale: prima della rimozione la lunghezza è≥22, dopo è≥21 e quindi≥2. Nel caso W₂ il seed unità `(3b−5)/2` può superare b: non va presentato come una discesa fra unità.

### Una sottoclasse libera con tutti i prefissi sopra b

Scegliere i due macroblocchi

`A=(1,2)^4`, lunghezza8 e totale12;

`B=(1,2)^3(2,1,2)`, lunghezza9 e totale14.

Sono prefix-free: le prime sei lettere coincidono, alla settima A ha1 e B ha2. Ogni prefisso di A ha gain>1. Nel tratto finale di B il minimo intermedio è `(9/8)^3·(3/4)=2187/2048>1`, mentre il gain totale è19683/16384>1. Anche w₂₂ appartiene al linguaggio dei prefissi strettamente espansivi: i suoi totali parziali sono

`(1,2,4,5,7,8,10,11,13,14,16,17,19,21,23,25,26,28,29,31,33,34)`,

ciascuno con `2^A_i<3^i`. Di conseguenza ogni parola di `{A,B}*·w₂₂`, incluso il caso di menu vuoto, mantiene tutti i suoi prefissi di gain>1: la discesa forward sotto b non interviene su questo tratto.

Il compagno unità è invece più piccolo di b. Per b1 modulo3 è b−2. Per b2 modulo3, ogni macroblocco non vuoto inizia con W₁, quindi si può usare `(3b−5)/4<b`, Γ=4/3; se il menu è vuoto il seed è `(3b−5)/16<b`. Le guardie del cilindro assicurano integrità e disparità, e la rimozione della foglia assicura l'unità. Questa è una classe propria con concatenazioni nonperiodiche ammesse, non una classificazione completa degli input.

Per applicare il budget P₀/antichain del progetto serve inoltre che i segmenti usati siano primi arrivi semplici. L'identità di fusione e il colore dell'ultimo genitore non richiedono questa ipotesi; il budget la richiede esplicitamente. Su una spine divergente gli arrivi effettivi sono primi arrivi.

### Un obbligo di uscita, senza input analitici

Sia b>2 il minimo seed divergente fra TUTTI i positivi dispari, inclusi i multipli di3. Se la sua parola rimanesse per sempre in `{W₁,W₂}^ω`, il positivo b−2 seguirebbe per sempre i blocchi concorrenti e differirebbe di2 ai confini. Per minimalità b−2 non diverge; in una dinamica deterministica sugli interi ciò lo rende eventualmente periodico e limitato. Anche b sarebbe limitato ai confini, e i blocchi di lunghezza≤3 renderebbero limitata tutta l'orbita: contraddizione.

Vale anche la versione direttamente sulle unità: il minimo seed unità divergente b ha primo gap1, perché un primo gap≥2 manderebbe all'unità `S(b)≤(3b+1)/4<b`. Se la parola resta in questo linguaggio deve quindi iniziare con W₁. Il compagno b−2 divergerebbe; se è foglia, il primo passo concorrente ha gap2 e produce `(3b−5)/4<b`, una unità divergente. Anche questa minimalità è contraddetta. Non è stato usato il floor degli atomi né un criterio di fusione.

Quindi il minimo seed divergente deve USCIRE da questo linguaggio in tempo finito. Se l'uscita ha il gate w₂₂, esiste la fusione esplicita; non sono coperte tutte le altre uscite. Questo è un programma più concreto di classificazione dei gate d'uscita, ma non un'esclusione della divergenza. Per b fissato le parole finite lunghe restano soggette ai vincoli dei cilindri; l'esistenza di un cilindro per ogni concatenazione non dà una realizzazione positiva di un'itinerario infinito.

Le due regole, la loro composizione con il gate e le riparazioni di unità sono state controllate indipendentemente da H23. Sono deduzioni su carta basate sul gate del primario152, non nuove prove Lean né certificati numerici rieseguiti.

La copertura quantitativa va moderata: i due blocchi W₁,W₂ sono un codice prefisso con pesi cilindrici1/8 e1/32. Il gate w₂₂ inizia con11, mentre i blocchi iniziano con12 o212; perciò i cilindri delle parole `{W₁,W₂}*·w₂₂` sono disgiunti. La loro misura2-adica relativa ai dispari è `2^-34/(1−5/32)=2^-29/27`. La positività dell'entropia del linguaggio non equivale a copertura del futuro di un intero fissato; neppure la misura Haar dell'insieme infinito esclude da sola un intero positivo.

## 9. Prime uscite: un piccolo elenco esatto e un carry non limitato

Il codice `{12,212}` è prefisso. Da un confine con coppia `(x,x−2)`, le prime uscite possibili sono: una prima valutazione≥3; una parola `(1,r)` con r≠2; una parola `(2,r)` con r≠1; oppure `(2,1,r)` con r≠2. L'alfabeto non è limitato, ma i casi iniziali si possono scrivere senza scansioni.

Chiamare x' lo stato osservato dopo il passo considerato. Al confine:

- Per valutazione osservata e≥2, il compagno ha SEMPRE valutazione1 e diventa `2^(e−1)x'−3`.
- Per e=1, il compagno ha valutazione `f=1+ν₂(x'−3)≥2` e diventa `(x'−3)/2^(f−1)`.

Per l'uscita `(2,r)`, r≥2, i due gap concorrenti sono1,1; lo stato finale è `2^r x'−5`. Dopo il prefisso21, la relazione è `y=2x−5`; un gap finale r=1 manda a `y'=x'−4`, r=3 manda a `oddpart(x'−1)`, r≥4 manda a `2^(r−3)x'−1`. Anche l'uscita `(1,3)` manda il compagno a `oddpart(x'−1)`, e `(1,r)` con r≥4 manda a `2^(r−3)x'−1`. Qui oddpart è definita su x'−1>0: x'=1 sarebbe incompatibile con un predecessore intero di gap3. Per l'uscita11 resta invece il parametro non limitato `1+ν₂(x'−3)≥3` già nel primo arco concorrente.

Queste identità classificano un primo stato dopo l'uscita. Non forniscono una ricorrenza chiusa in un insieme limitato di stati, né un lower sul numero di rientri nel linguaggio.

### Una famiglia finita che blocca il proseguimento ingenuo del medesimo compagno

L'uscita13 può far convergere il compagno a1 mentre il target osservato è arbitrariamente grande, anche mantenendo tutti i prefissi osservati di gain>1. Questo non è un controesempio a una congettura di co-divergenza: non viene provata la divergenza dell'orbita osservata.

Scegliere K≥5, t=6m≥6, con

`3^(2K+3) | (2^(t+1)+7)`.

Una tale scelta esiste per ogni K: `64^m` percorre il sottogruppo `1+9ℤ₃` ai livelli finiti, perché `ν₃(64−1)=2`, mentre `−7/2∈1+9ℤ₃`. Si può scegliere m arbitrariamente grande nella classe soluzione. Porre

`x=(2^(t+4)+11)/9`,

`b=8^(K+1)(2^(t+1)+7)/9^(K+1)−5`.

Sono interi positivi dispari per m grande; la cifra ternaria aggiuntiva dà `b≡1 mod3`, quindi sia b sia b−2 sono unità. Le parole effettive sono

`b →_(12)^K x →_(1,3) 2^t+1`,

`b−2 →_(21)^K x−2 →_(2,t+2) 1`.

La legalità del primo tratto segue dal criterio dei cilindri e dall'identità `x+5=(9/8)^K(b+5)`. Sul tratto13, gli stati intermedi sono `(2^(t+3)+7)/3` e `(2^(t+2)−1)/3`; per il secondo, `3y+1=2^(t+2)`, perciò il gap concorrente è esattamente t+2. La congruenza t=0 modulo6 paga entrambe le divisioni per3.

Tutti i prefissi osservati hanno gain>1: sul tratto finale il gain minimo è `(9/8)^K·9/16`, e a K=5 è `531441/524288>1`. Tuttavia dopo l'uscita il rapporto affine diventa `y=2^-t(x'−1)`: la slope può collassare arbitrariamente anche con K fissato e con valutazioni osservate≤3.

Le identità della coppia, a parole fissate e su tutto il relativo cilindro, hanno slope nonzero ereditata dai percorsi e relazione finale `H_t(z)=2^-t(z−1)`. Poiché t è arbitrario, un menu finito di IDENTITÀ ESATTE DI COPPIA SUI CILINDRI, indipendente da t e con tali slope nonzero, non copre tutte queste uscite. I soli punti costruiti `(2^t+1,1)` non basterebbero a questa conclusione: tutti soddisfano anche la relazione costante y=1, che non è l'identità affine ereditata dai due percorsi. Non si refutano editor che scelgono un altro seed, non si dimostra che b sia divergente e non si esclude un potenziale più ricco. Le formule e l'esistenza della congruenza sono state controllate da H23; nessuna ricerca numerica è stata eseguita.

### Il grande carry paga una contrazione successiva: una guardia ammortizzata

L'esempio precedente NON è un no-go a un bilancio ammortizzato. Se `z=2^t u+1`, con u positivo dispari e t≥1, i successivi

`r=floor((t−1)/2)`

passi osservati hanno tutti gap2 e soddisfano

**`S^r(z)=(3/4)^r(z−1)+1`**.

Infatti da `2^s u+1` con s≥3 si ottiene `3x+1=4(3·2^(s−2)u+1)`, con fattore tra parentesi dispari: il gap è esattamente2. Iterare fino a s=1 o2 dà la formula.

Se b>1 è il minimo seed unità divergente, nessuno stato futuro può essere<b, perché sarebbe ancora una unità divergente. Pertanto l'uscita13, o213, che porta a z deve pagare

`r log(4/3) ≤ log((z−1)/(b−1))`,

**`t ≤ 2 + 2 log((z−1)/(b−1))/log(4/3)`**.

Questo è un bound in funzione del BUFFER DI CRESCITA reale, non O(log j). Nella famiglia costruita sopra, per K fissato il rapporto `(z−1)/(b−1)` resta limitato mentre t può crescere: dopo i gap2 forzati l'orbita osservata scende quindi sotto b. La famiglia non può essere un minimo seed divergente quando m è abbastanza grande. Il compagno che collassa a1 rivela dunque una possibilità positiva: grande costo locale oppure discesa successiva, con una carica quantitativa sul buffer. Non dimostra che tutte le altre uscite ammettano lo stesso bilancio né che il buffer complessivo sia limitato.

La formula è un corollario elementare, controllato da root e H23, non una rivendicazione di priorità. È il primo target concreto per un potenziale del controller: addebitare il costo delle uscite ai segmenti successivi di contrazione, invece di cercare un impossibile bound locale assoluto.

Lo stesso meccanismo tratta il grande gap nascosto dell'uscita11. Se il primo gap concorrente è f≥7 e `u=S(x−2)`, i primi stati osservati sono

`x₁=3+2^(f−1)u`, `x₂=5+3·2^(f−2)u`.

Segue `3x₂+1=16(1+9·2^(f−6)u)`, con fattore dispari tra parentesi: il terzo gap osservato è esattamente4 e

`z=x₃=1+9·2^(f−6)u`, `ν₂(z−1)=f−6`.

Applicare il medesimo lemma dei gap2 forzati dà, per un minimo seed divergente b,

**`f ≤ 8 + 2 log((z−1)/(b−1))/log(4/3)`**.

I valori f=3,4,5,6 restano quattro classi PARAMETRICHE, con u illimitato, non quattro stati numerici finiti. Questa estensione è stata controllata da H23. I bilanci delle singole uscite non costituiscono ancora un ammortamento globale lungo una traiettoria arbitraria.

## 10. Decisione operativa

La pista locale più promettente, se la si mantiene, deve diventare un processo di coppie di percorsi con prefisso comune di lunghezza O(log j), legalità esatta per tutta la parola e carry crescente ma pagato. Il lemma utile dovrebbe dimostrare che il processo raggiunge un altro colore con seed O(j log j), oppure produrre una massa prefix-free equivalente, su un insieme di tempi con bilancio divergente.

Non è stato ottenuto un tale lemma generale. Il filtro finito di §6 restringe una costruzione precisa; §8 mostra però che una coniugazione fra blocchi diversi sfugge a quella restrizione e produce una famiglia legale. La decisione concreta è studiare i GATE D'USCITA di questo o di un altro linguaggio di coppie, conservando unità, ultimo colore e debito, oppure cercando una condizione di co-divergenza che non richieda fusione né floor analitico. §9 fornisce già un bilancio esatto per le uscite13/213 e per il grande gap nascosto di11: carry controllato dal buffer oppure discesa sotto il minimo seed. Il nuovo obbligo è estenderlo alle altre uscite e controllare l'ammortamento globale. H22 ha individuato nella [fonte81/v2](https://rstation.ai/problems/collatz/papers/81) il reset lineare scelto, inclusi i guadagni di potenza per famiglie costruite; quello non è più un obbligo nuovo. La copertura delle uscite o una massa a piccolo debito lungo il futuro dato resta da dimostrare.
