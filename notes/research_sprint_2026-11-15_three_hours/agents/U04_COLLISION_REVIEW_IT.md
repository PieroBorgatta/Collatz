# U04 — Audit di collisione fisica, Bellman e trasporti affini

Terza revisione indipendente della sessione del 15–16 novembre 2026. Ho letto U07 nello snapshot `6330c4f371312b83f169d5573b4be3af33eaf02f08075a6c47358379a34eac46`, U08 e il lemma teorico di U10. Ho anche controllato semanticamente i cinque enunciati pubblici di `SpineDispersion.lean`, senza compilare il modulo. Nessun nuovo esperimento, GPU o cambiamento ai testi letti.

**Esito: PASS entro gli input espliciti.** I criteri di nonconcentrazione sono sufficienti ma i loro lower restano aperti. I consumer di coalescenza usano teoremi esterni scritti: non sono stati ricompilati o ricostruiti integralmente qui. I replay numerici degli altri agenti sono fuori dal presente audit.

## 1. Collisione di endpoint e operatore quadratico

Per un root fisso e una profondità m fissata, due cammini inversi che finiscono nel medesimo intero u coincidono a ogni passo. Basta applicare l'unica m-orbita forward deterministica di u; anche gli esponenti sono determinati. Questo rimane vero se il target è periodico, perché il confronto avviene alla stessa profondità. Non si sta contando una collisione fra codifiche duplicate.

Pertanto, per due copie indipendenti del vero kernel Q,

`T^m1(n)=Σ_u Q_n(Y_m=u)²=K₂^m(g²)(n)/g(n)²`,

dove T(n,y)=Q(n,y)² e K₂ ha i pesi critici elevati al quadrato. La positività e l'armonicità danno `K₂(g²)≤g²`; tutti gli iterati coinvolti sono finiti puntualmente anche se g² non è globalmente integrabile. Il telescopio con `C_g=g²−K₂(g²)` è corretto.

La finitezza di `Σ_m K₂^m1(n)` non controlla da sola il resto `K₂^m(g²)(n)`: il secondo applica l'operatore a una funzione non limitata. Una decomposizione infinita senza resto usa un input sulla nonatomicità della legge sui cammini, non il solo budget quadratico. U07 conserva questa distinzione.

## 2. Vincolo lungo una spine divergente

Ho ricostruito la normalizzazione `R_j=P_jg(n_j)/n_j`. La probabilità del predecessore osservato è esattamente `p_j=R_(j−1)/R_j`. Armonicità dà monotonia; `g(n)≤Cn` sui target senza ritorni e `P_j≤P₀` danno limitatezza, quindi R_j→R∞∈(0,∞).

Si ha allora

`Σ_j−log p_j=log(R∞/R₀)`,

`H₂(n_j)≤−2log p_j`, `D(n_j)≤1−p_j²≤2(1−p_j)`.

Ne seguono `ΣH₂≤2log(R∞/R₀)` e `ΣD<∞`. Il parametro R∞ non è ottenuto dalla sola armonicità; l'upper lineare è essenziale e compare nel dominio della nota.

Lungo la spine, `g(n_j)/n_j≥R₀/P₀>0` e `1+log n_j≤C_u(1+j)`. Il lower postulato `D(n)≥c_ε/(1+log n)` sui grandi root pesanti renderebbe quindi la somma divergente. È corretto anche il criterio con H₂. Non è stato provato alcuno di questi lower.

Il confronto con un sibling del predecessore x usa il rapporto esatto `p_y/p_x=4^(-t)g(y)/g(x)`, t∈{1,2}. Il lower risultante contiene log x; non viene impropriamente sostituito con log n, che può essere molto più piccolo dopo un'esponente grande.

## 3. Orizzonte critico e certificato con due seed

Il conteggio N(j) degli esponenti almeno due tende a infinito su ogni orbita positiva dispari: una coda tutta di esponenti uno imporrebbe divisibilità del suo valore iniziale più uno per ogni potenza di due. Inoltre `n_j+1≤(u+1)(3/2)^(j−N(j))`.

Con un tempo m_j≤log_(3/2)(n_j+2)+C si ha dunque j−m_j→∞. La probabilità di ripercorrere quel segmento è `R_(j−m_j)/R_j→1`; l'endpoint prescritto ha probabilità tendente a uno e la collisione delle due copie tende a uno. Questo contraddice il gap uniforme postulato in U07. Il caso m=0 non crea un'eccezione, poiché la collisione a tempo zero è uno e non soddisfa un gap positivo.

Il certificato aritmetico con due seed è corretto con tutte le sue condizioni. I seed devono essere unità positive, devono entrare nel root senza ritorni e devono arrivare attraverso due **ultimi genitori distinti**. Il cammino intero di ciascun seed ha probabilità almeno `c₀/(C P₀u_i)`; la probabilità del primo genitore inverso è almeno quella del cammino completo. Se u_i≤L, i due rami hanno massa almeno α=c₀/(C P₀L).

Poiché α≤1/2, un atomo p compreso fra α e 1−α dà `D≥2p(1−p)≥α`. Il lower con secondo seed O_ε(log n) sarebbe quindi sufficiente, ma non è stato ottenuto. Due seed che si fondono prima del root non certificano due genitori differenti.

## 4. Shannon: label corretti e uniformità dei momenti

Ho letto il §12, equazione (36) e Corollario 12 della [fonte primaria 12/v1](https://rstation.ai/problems/collatz/papers/12). La legge chiamata Q in U07 è P_h nella fonte; il Q della fonte è un'altra legge. Il label `m_*(x)=min P(x)` è il minimo **predecessore** del genitore x, non il minimo futuro della sua orbita.

Al root senza ritorni, i bacini dei diversi genitori sono disgiunti e questi label sono distinti. Il bound della fonte riguarda l'intera unione in una cella di landing, non una somma illegittima di bound per singoli atomi. Sui root pesanti β_n≥ε/κ, la sua coda logaritmica di ogni ordine implica momenti uniformi di ogni potenza fissata di log m_*.

Condizionando fuori da un genitore di probabilità 1−q, Gibbs con il codice `1/(ζ(2)m²)` dà l'upper entropico riportato. Hölder controlla il termine `E[log m_*;off]` con q^(1−1/p); il costo binario e q log(1/q) hanno lo stesso upper. Quindi `H≤C_(ε,p)q^(1−1/p)` è corretto. Scegliendo p=(1+δ)/δ si ottiene `Σ_j H(n_j)^(1+δ)<∞`.

Il criterio Shannon con denominatore `(1+log n)^a`, a<1, segue scegliendo δ con a(1+δ)≤1. L'endpoint a=1 non segue. Il bilancio per log(g(n)/n) conserva la correzione bounded e non separa due aspettative potenzialmente infinite. La finitezza di Shannon citata nel quadro canonico è distinta dall'esistenza di un momento dell'esponente o dell'altezza del genitore, che non viene affermata.

Anche la qualificazione sulla forza logica dei criteri passa: il tail dei label rende tight la famiglia dei root pesanti attraverso finitissimi piccoli antenati. Se ogni orbita fosse eventualmente periodica, i root pesanti senza ritorni sarebbero finiti e i lower oltre una soglia sarebbero vacui. Questa direzione usa quel tail esterno supplementare.

## 5. Barriere Bellman e ansatz quasi critici

Per il drift QV≥λV con λ>1 e V globalmente limitato, la famiglia `(4^k−1)/3`, 3∤k e k≥2, fornisce root unità senza ritorni che vanno a1 in un passo Syracuse. Una singola orbita forward può contenerne al più uno. Fuori dall'unione delle orbite di un insieme finito F si può quindi scegliere un root il cui intero albero inverso evita F. Iterare il drift su questo albero contraddice la limitatezza di V. L'argomento non si estende automaticamente a un insieme eccezionale infinito.

Il corridoio inverso di esponenti uno da `2·3^K−1` a `3·2^K−1` prova la barriera contro super-soluzioni globalmente comparabili a n^θ per θ<1. La famiglia esplicitamente convergente `A_K=(2^(3^K+1)−1)/3` riproduce K−1 passi inversi uno fra unità: S(A_K)=1 e ν₃(A_K+1)=K. Questo mantiene la barriera anche sul solo dominio senza ritorni.

Per `F(n)=n/(log n)^s`, a root grande, i genitori unità corrispondono a due classi di esponenti modulo6. Su ciascun ramo `ω_e I_e(n)=n−2^(−e)` e `log I_e(n)=log n+e log2−log3+O(1/n)`. Pertanto, per s>1,

`LF(n)/F(n) ∼ log n/[3log2(s−1)]`.

Il coefficiente 1/3 è la densità delle due classi legali fra sei; il denominatore log2 viene dal passo della progressione. Per s≤1 la serie diverge. Una correzione compresa fra due costanti positive conserva il lower divergente del rapporto, benché non l'esatto equivalente. Tutti i genitori di un root senza ritorni restano senza ritorni, perciò la restrizione non elimina l'ostacolo.

Questa è una barriera contro una **super-soluzione** di quella forma. Non confuta l'eventuale esistenza di una maggiorante F di g che non sia essa stessa superarmonica.

## 6. U08: consumer di coalescenza e clock fisici

Ho letto le interfacce `pair:cylinders`, `pair:dictionary`, `pop:discrepancy`, `thm:pair` e `lem:clock` nelle due sorgenti TeX archiviate da U08. L'evento di assorbimento usa modulo2^t e il successo a t passi shortcut produce un merger ordinario bilanciato entro2t. Ho confrontato anche Teorema1 ed equazione (18) della [fonte 124/v1](https://rstation.ai/problems/collatz/papers/124), che fornisce il costo uniforme `(1+log D)^4/sqrt(t+1)` e un solo errore2^t per un intero blocco.

La disuguaglianza deterministica `C^j(u)≥u/2^j` paga correttamente gli attraversamenti dei target prima del merger. La sola coalescenza eventuale non sarebbe sufficiente; U08 scarta invece il bordo esplicito R2^N. La concatenazione di coppie adiacenti funziona perché il merger bilanciato è a un tempo comune, estendibile al medesimo deadline.

Per il fattore3, la decomposizione u=2^v m usa coppie adiacenti 3m,3m+1, poi la singola m→3m+1. Troncare v≤t dà orologi individuali al più3t+1; il conteggio include `(t+1)2^t` e X/2^t oltre al costo Xq_t. I valori di t scelti rendono tutti i bordi sublineari. I fattori2, i menu finiti e i denominatori smooth sono trattati mediante mappe iniettive fissate, senza assumere indipendenza dei bacini.

Per le finestre crescenti, il vettore dei target a≤R si conserva simultaneamente: nessun prefisso entra sotto R. Non serve moltiplicare l'errore per R. Con R=X^r e t=floor((1−r)log₂X/4), il bordo è X^((1+r)/2); la condizione `log(G_X+2)=o((log X)^(1/8))` paga il termine di famiglia. L'errore è assoluto o(X), non relativo a un bacino raro.

PASS condizionale agli input di coalescenza citati. Non ho ricostruito tutte le loro prove infinite o ricompilato archivi esterni. La conseguenza sui trasporti richiede davvero bacini disgiunti.

## 7. U10: coefficiente non smooth e tempi asincroni

Il lemma teorico passa anche quando r e s differiscono. Per la mappa ordinaria, un prefisso con o passi dispari ed e dimezzamenti ha offset `0≤R≤2^e(3^o−1)/2`. L'uguaglianza degli endpoint incrocia i coefficienti in un intero non nullo, perché la sua cancellazione imporrebbe P/Q∈2^ℤ3^ℤ.

Usando o+e≤N e o'+e'≤N, ciascun termine d'offset è al più Q6^N/2; il termine con B è al più |B|6^N. Ne segue `u≤(|B|+Q)6^N`. Per la shortcut, l'offset R_t≤3^t−2^t dà `u≤(|B|+2Q)6^N`. Sono ammessi i prefissi vuoti e N=0. Non è esclusa una coalescenza a tempi successivi, né dimostrato un trasferimento positivo fra bacini.

Il lemma separa l'interfaccia a tempo fissato dei coefficienti non smooth dal meccanismo smooth di U08. Non prova una diversa legge asintotica dei loro label. I numeri dei replay U10 non sono stati rieseguiti nel presente audit.

## 8. Nucleo Lean finito: controllo semantico

I cinque enunciati pubblici di `SpineDispersion.lean` riguardano cataloghi finiti e un rapporto monotono R_i/R_(i+1). Il selected branch limita il difetto dall'alto senza richiedere una legge di probabilità; la nonnegatività viene dimostrata separatamente sotto ipotesi di subprobabilità. Il budget finale è `2/a·(R_N−R_0)`, più grossolano del bound logaritmico su carta ma sufficiente e correttamente delimitato.

Un catalogo troncato che contiene il ramo selezionato dà un upper del difetto della legge completa. Nessun lower, limite infinito, processo casuale o teorema analitico esterno è nascosto negli enunciati. Questo è un controllo del significato; la compilazione e l'audit degli assiomi spettano all'integrazione del coordinatore.

## Conclusione dell'audit

Non ho trovato correzioni matematiche necessarie nei testi congelati. Restano aperti il lower normalizzato di collisione, il gap fisico entro il clock critico e il bound logaritmico del secondo seed. La nonconcentrazione fisica è un obiettivo ben definito; il suo enunciato sufficiente non equivale a un risultato quasi completato. Nessuna delle note dimostra H o Collatz.
