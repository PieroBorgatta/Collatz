# Semi compatti e conservazione del decadimento di ordine sei

**Nota matematica post-v6 — 24 settembre 2026.** Sviluppo di Piero Borgatta
con assistenza AI. Il teorema analitico di densità dei predecessori utilizzato
è attribuito a Lech Mazur. Qui si isolano due modifiche quantitative della
nostra precedente costruzione uniforme a due semi. Non si rivendicano una
prova di Collatz, ottimalità globale o priorità bibliografica assoluta.

## Enunciato del miglioramento

Sia a>0, con 3∤a, il target. Fissati i parametri b,q,C della costruzione
analitica, poniamo Q=3^q e

\[
 G(r,k)=\frac{4^k(3r+1)-1}{3},\qquad
 T_0=G(2a,(16^b+3)Q),\qquad T_1=G(2a,2b+2Q).
\]

La vecchia scelta era `m₀=132 T₀ C+1`; la nuova è

\[
 m_1=\min\{m\in\mathbb N:m\ge1,\ 88T_1C\le m^6\}.
\]

Con gli altri parametri analitici invariati, il nuovo coefficiente
`c₁=3/(256 T₁ 3^m₁)` è strettamente maggiore di
`c₀=3/(256 T₀ 3^m₀)`. Anche la soglia finale è strettamente minore.
Specializzando ai parametri del teorema esterno, la nuova via dimostra che
almeno `c₁X` interi positivi distinti sotto X raggiungono a, per ogni X oltre
la nuova soglia. I confronti delle formule richiedono soltanto a>0 e C≥0;
il teorema di densità richiede inoltre 3∤a e l'input analitico, scaricato
nella formalizzazione tramite la biblioteca esterna fissata.

## 1. Un indice additivo per la coppia di semi

Per r≥1 si ha G(r,k)≥4^k. Basta quindi k>2b per superare 16^b.
Dato un residuo p modulo Q, il primo indice k≡p mod Q con k>2b soddisfa

\[
 2b<k\le2b+Q,\qquad k+Q\le2b+2Q.
\]

La famiglia di copertura dei residui fornisce una radice iniziale positiva
r≤2a. I due candidati G(r,k), G(r,k+Q) hanno il residuo richiesto e lo
stesso successore Syracuse, sono distinti e non superano T₁.

Una mappa è iniettiva sui propri punti periodici. Due predecessori distinti
dello stesso punto non possono dunque avere entrambi un ritorno positivo.
Almeno uno è un seme senza ritorni, entro il limite uniforme T₁. La prova
non decide quale dei due sia quello utile e non identifica “senza ritorni”
con “divergente”: un punto transitorio verso 1 può non tornare a sé stesso.

Infine `2b+2Q<(16^b+3)Q`; la crescita stretta di G nel secondo parametro
dà T₁<T₀.

## 2. Il budget conserva la sesta potenza

L'input disponibile controlla l'errore L1 con `(2/3)C/m^6`. Per usare
l'interfaccia del conteggio terminale, che è espressa con `D/m²`, si fissa

\[
 D=\frac{2C}{3m^4}.
\]

Il parametro m è già fissato prima della quantificazione sui livelli
successivi k≥m; D può quindi dipendere da m. Le stime di persistenza e i
parametri iniziali continuano a usare C. Il budget richiesto diventa

\[
 88TD\le\frac23m^2
 \quad\Longleftrightarrow\quad 88TC\le m^6.
\]

La nuova ricerca minima ha un testimone finito `88TC+1`, quindi definisce
un naturale calcolabile. Non è proposta come algoritmo pratico sulle enormi
costanti pubbliche. Per minimalità,

\[
 m_1\le88T_1C+1\le132T_0C+1=m_0.
\]

## 3. Coefficiente e soglia

Poiché T₁<T₀ e m₁≤m₀, il denominatore positivo `T₁3^m₁` è strettamente
minore di `T₀3^m₀`, dunque c₁>c₀. Per la soglia si conservano b e Nmark e
si usano le formule del conteggio

\[
 J_i=N_{\rm mark}+2m_i+20\cdot10^9,\qquad
 H_i=2^{(2J_i+4)b\,2^{J_i}+J_i(17(J_i+1)+1)}T_i.
\]

La monotonia dell'esponente e la crescita stretta nel fattore T danno
`32(H₁+1)<32(H₀+1)`, anche nel caso C=0 in cui i conduttori coincidono.
Questi sono confronti fra le nostre due formule uniformi: non un confronto
con ogni possibile scelta esistenziale del seme nel manoscritto esterno.

## Evidenza e perimetro

Le dimostrazioni sono in
[CompactSeedNonreturn](../research/weighted_predecessors_adapter/CompactSeedNonreturn.lean),
[OptimizedConductor](../research/weighted_predecessors_adapter/OptimizedConductor.lean),
[OptimizedDensity](../research/weighted_predecessors_adapter/OptimizedDensity.lean) e
[OptimizedComparison](../research/weighted_predecessors_adapter/OptimizedComparison.lean).
La [CI 36009718722](https://github.com/PieroBorgatta/Collatz/actions/runs/36009718722)
ha verificato la chiusura locale di 399 moduli mediante compilazione e riuso
di ricevute controllate. Tre audit sono passati; la nuova radice e i confronti
usano solo gli assiomi standard indicati nel
[manifest delle evidenze](post_v6_optimization_2026-09-24/verification_manifest.json).

L'input analitico e il risultato esterno sono descritti da
[Mazur, *Positive Lower Density of Collatz Predecessors*](https://www.proofatlas.ai/formalizations/positive-lower-density-collatz-predecessors/).
Il controllo meccanico non sostituisce una revisione matematica indipendente
della catena analitica. Le costanti rimangono enormi. La documentazione
operativa completa è nel [resoconto verificato](post_v6_optimization_2026-09-24/RESULTS_IT.md).
