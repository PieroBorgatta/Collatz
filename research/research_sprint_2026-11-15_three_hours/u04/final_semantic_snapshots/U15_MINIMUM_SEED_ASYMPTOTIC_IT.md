# U15 — Asintotica quantitativa del minimo antenato unità

Corollario proposto dal coordinatore, verificato usando la coda U09. Nessun nuovo lower del surplus, clock, esperimento o priorità globale. Gli argomenti di primo arrivo valgono anche quando il target è periodico; i passaggi sulla spine richiedono divergenza.

## 1. Da minimo antenato a massimo di gain, con errore tendente a zero

Sia m=m_U(n) il minimo seed unità positivo che raggiunge n, parola vuota inclusa. Porre q=3125/3456 e

`E(m)=82 q^floor(log_(32)m)`, m≥1.

La coda U09 dice che ogni segmento shortcut positivo iniettivo i cui stati sono almeno m ha somma dei reciproci≤E(m); E è non crescente e tende a zero.

Scegliere il PRIMO arrivo da m a n. Ogni suo stato dispari è una unità che raggiunge n, dunque è≥m per minimalità. Gli stati shortcut intermedi pari sono almeno il successivo stato dispari, quindi anch'essi≥m. Il segmento fino al primo arrivo è iniettivo, anche se n appartiene a un ciclo. Quindi

`1≤P(m→n)≤exp(E(m)/3)`.

Il massimo F è almeno il gain di questo cammino, mentre ogni suo seed è≥m. Si ottiene

**`exp(−E(m)/3) n/m ≤ F(n) ≤ n/m`.**

Il caso m=n e parola vuota resta valido. In particolare F(n)m_U(n)/n→1 uniformemente quando m_U(n)→∞. La stima non asserisce che il seed minimo sia sempre quello che realizza F.

## 2. Versione per i rami

Per un genitore unità x di n con esponente e, sia m_x=m_U(x) e M_x=(3/2^e)F(x). Poiché (3/2^e)x=n−2^(−e),

**`[1−1/(2^e n)] exp(−E(m_x)/3)/m_x ≤ M_x(n)/n ≤ 1/m_x`.**

Il limite superiore conserva soltanto il bound1/m_x; non viene cancellato il fattore affine nel limite inferiore. Questa formula è puntuale, senza nonritorno del target. Per sommare i rami si usa la finitezza LF già provata dal floor/armonicità oppure dal lower di densità; non si introduce l'additività della densità per unioni infinite.

## 3. Il surplus lungo una ipotetica spine divergente

Sia n_j=S^j(b) divergente. Per ogni genitore laterale x≠n_(j−1), il minimo m_x tende a infinito UNIFORMEMENTE fra i rami al crescere di j: fissato R, i finitissimi seed unità≤R possono entrare nella spine soltanto a finitissimi indici di primo merger. Dopo il massimo di tali indici, nessuno può raggiungere un genitore laterale.

Porre `M_j=min_(x laterale)m_U(x)`. Allora M_j→∞. Oltre la stabilizzazione dell'ottimo U15, il ramo massimo è il predecessore osservato e A=Σ_laterali M_x. Se

`S_j=Σ_(x laterale)1/m_U(x)`,

le somme sono finite e la stima uniforme della sezione2 dà

`[1−1/(2n_j)] exp(−E(M_j)/3) S_j ≤ A(n_j)/n_j ≤ S_j`.

Pertanto

**`A(n_j)/n_j = (1+o(1)) Σ_(x laterale)1/m_U(x)`.**

La costante asintotica è1. Non è disponibile un rate di M_j in funzione di j o n_j: quel minimo riguarda ancora i tempi di primo merger dei piccoli seed. L'identità quantitativa migliora il confronto a costanti fisse, ma non fornisce il lower S_j≥c/log n_j necessario alla prova.

Anche il minimo seed globale di n_j è eventualmente nel ramo di backtracking: esso è limitato da b e si stabilizza dopo gli ingressi dei finitissimi seed≤b. Questo non identifica automaticamente minimo seed e seed di massimo gain; entrambi, eventualmente, passano dallo stesso ramo fisico.
