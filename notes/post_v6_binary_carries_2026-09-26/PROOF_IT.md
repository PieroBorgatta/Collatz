# Riporti binari: stato esatto, ridondanza e limite della compressione

26 settembre 2026. Questa nota dimostra le identità e la famiglia di
collisioni del [protocollo](PROTOCOL_IT.md). Le prove sono su carta;
non sono nuove dichiarazioni Lean né un bilancio uniforme della torre.

## 1. Generazione esatta dal seme 3

Poniamo `R_0=3`, `R_(a+1)=R_a²` e scriviamo
`R_a=Σ_(n≥0) b_(a,n)2^n`, con bit `b_(a,n)∈{0,1}`. Il prodotto
scolastico ha coefficienti non normalizzati

\[
d_{a,n}=\sum_{i=0}^n b_{a,i}b_{a,n-i}.
\]

Con `C_(a,0)=0`, definiamo in colonne crescenti

\[
b_{a+1,n}=(C_{a,n}+d_{a,n})\bmod2,
\qquad C_{a,n+1}=\left\lfloor\frac{C_{a,n}+d_{a,n}}2\right\rfloor.
\tag{1}
\]

La divisione euclidea dà
`d_(a,n)+C_(a,n)=b_(a+1,n)+2C_(a,n+1)`. Moltiplicando per `2^n`
e sommando le prime `N` colonne, i riporti intermedi si cancellano:

\[
\sum_{n<N}d_{a,n}2^n
=\sum_{n<N}b_{a+1,n}2^n+2^N C_{a,N}.
\tag{2}
\]

Il membro sinistro è congruo a `R_a²` modulo `2^N`. Il primo termine
destro è in `[0,2^N)`, dunque è esattamente `R_a² mod2^N`.
Ogni prefisso prodotto da (1) è quindi quello del quadrato effettivo.
Inducendo sui livelli dal seme binario `1,1,0,…` otteniamo

\[
R_a=3^{2^a},\qquad P_v:=R_{v+1}=3^{2^{v+1}}.
\]

Per `v≥0`, `ν₂(P_v−1)=v+3`: la base è `3²−1=8`; a ogni quadrato
successivo il fattore `P_v+1≡2 mod8` aggiunge una valutazione pari a
uno. Posto `r=v+3`, `Q_v=(P_v−1)/2^r` è quindi un intero positivo
dispari. Sottrarre uno a `P_v`, dispari, cambia soltanto il bit zero.
I bit delle due sorgenti sono pertanto

\[
h^L_t=b_{v+1,r+t},\qquad h^U_s=b_{v+2,r+1+s}.
\tag{3}
\]

La scansione può procedere per colonne crescenti, e all'interno di
ogni colonna per livelli crescenti. Conservando i prefissi delle righe,
tutti i coefficienti in (1) sono disponibili. Non si presume che questa
memoria sia di dimensione uniforme.

Per raccordare (3) alle parità shortcut, per una sorgente `x` poniamo
`j_t=J_x(t)` e

\[
T^t(x)=3^{j_t}\lfloor x/2^t\rfloor+z_t,
\qquad (j_0,z_0)=(0,0).
\]

Dato il bit `h_t=bit_t(x)`, la decomposizione implica

\[
p_t=(h_t+z_t)\bmod2,\quad j_{t+1}=j_t+p_t,\quad
z_{t+1}=\frac{3^{j_t+p_t}h_t+3^{p_t}z_t+p_t}{2}.
\tag{4}
\]

Infatti `floor(x/2^t)=h_t+2floor(x/2^(t+1))`; applicare `T` e
raccogliere il nuovo termine principale dà (4). Per induzione si
ottengono esattamente le parità delle sorgenti generate. Questo
raccordo non aggiunge una maggiorazione del loro conteggio.

## 2. Il riporto esposto è una funzione del prefisso

Per un qualunque input nonnegativo `P`, omettiamo l'indice di livello.
Poniamo

\[
F_N(P)=\sum_{\substack{i,j\ge0\\i+j<N}}b_i b_j2^{i+j}.
\]

Dalla (2) segue la formula chiusa

\[
\boxed{C_N(P)=\left\lfloor\frac{F_N(P)}{2^N}\right\rfloor
=\frac{F_N(P)-(P^2\bmod2^N)}{2^N}.}
\tag{5}
\]

La somma `F_N` usa soltanto i bit di `P` nelle posizioni `<N`.
Conoscere `P mod2^N` determina quindi tutti i riporti `C_0,…,C_N`
e tutte le uscite già esposte. Aggiungere questi riporti al prefisso
completo non esclude alcun suo completamento.

La formula **non** è in generale
`C_N=floor((P mod2^N)²/2^N)`: in `F_N` sono esclusi i coefficienti
di colonna `i+j≥N`, anche quando entrambi i bit sono nel prefisso.

Per una cascata con seme fisso 3, il seme e (1) determinano univocamente
tutte le righe modulo `2^N`. Ciò verifica i prefissi della sorgente
esatta; non dimostra un limite uniforme sul peso della parola Collatz.

## 3. Primo riporto diverso per due sorgenti ancorate

Siano `r≥1`, `X,Q` interi positivi dispari distinti, e

\[
P=1+2^rX,\qquad \widetilde P=1+2^rQ,\qquad
M=\nu_2(X-Q),\quad n=r+M.
\]

Le valutazioni delle differenze si intendono quelle del valore assoluto.
I due input coincidono esattamente nelle posizioni `<n` e differiscono
al bit `n`. Per (5), i riporti `C_0,…,C_n` coincidono. Nella colonna
`n`, soltanto i termini con indici `(0,n)` e `(n,0)` cambiano; il bit
zero comune è uno. Quindi

\[
d_n(P)-d_n(\widetilde P)
=2\bigl(b_n(P)-b_n(\widetilde P)\bigr)\in\{-2,2\}.
\]

La (1) mostra che le uscite correnti coincidono e che

\[
\boxed{|C_{n+1}(P)-C_{n+1}(\widetilde P)|=1.}
\tag{6}
\]

Inoltre `P+P̃=2+2^r(X+Q)≡2 mod4`, perché `X+Q` è pari.
La fattorizzazione dei quadrati dà dunque

\[
\nu_2(P^2-\widetilde P^2)
=\nu_2(P-\widetilde P)+\nu_2(P+\widetilde P)=n+1.
\tag{7}
\]

La prima uscita diversa del quadrato è esattamente la colonna `n+1`.
Dividendo `(P²−1)` per `2^(r+1)`, la sorgente superiore è
`X+2^(r−1)X²`; la prima differenza rispetto alla sorgente costruita
da `Q` torna quindi alla posizione `M`. Il ritardo di una colonna del
quadrato viene consumato dallo shift aggiuntivo: non rinnova la
precisione della coppia di sorgenti.

## 4. Collisione di riporto e finestre su input ancorati

Fissiamo `r≥3`, `w≥1` e poniamo

\[
a=\max(2r+1,r+w+2),\qquad n=2a,
\]
\[
P=1+2^r+2^{n+1},\qquad \widetilde P=P+2^a.
\tag{8}
\]

Entrambi appartengono al dominio `1+2^rX` con `X` positivo dispari.
Hanno lo stesso ancoraggio modulo `2^(r+1)`, la stessa binade
`[2^(n+1),2^(n+2))`, gli stessi bit nelle posizioni `≥n`, e bit
corrente `b_n=0`.

Nelle colonne `<n`, i termini del quadrato di `P` sono

\[
1+2^{r+1}+2^{2r};
\]

quelli del quadrato di `P̃` sono

\[
1+2^{r+1}+2^{2r}+2^{a+1}+2^{a+r+1}.
\tag{9}
\]

Il bit comune in posizione `n+1` dell'input produce termini soltanto
da `n+2` in su e non interviene. Gli esponenti in (9) sono distinti,
perché `r≥3` e `a≥2r+1`. Il maggiore è
`a+r+1≤n−w−1`, grazie ad `a≥r+w+2`. Le somme in (9) sono quindi
minori di `2^(n−w)`, e in particolare di `2^n`. Per (5), entrambi i
riporti correnti sono zero. Tutte le ultime `w` cifre del quadrato,
nelle posizioni `n−w,…,n−1`, sono zero. Anche le ultime `w` cifre
dell'input sono zero, poiché `a<n−w`.

Nella colonna `n`, `P` ha coefficiente zero mentre `P̃` ha il solo
termine diagonale `b_a²=1`. Pertanto

\[
b_n(P^2)=0,\qquad b_n(\widetilde P^2)=1,
\qquad C_{n+1}(P)=C_{n+1}(\widetilde P)=0.
\tag{10}
\]

Livello, posizione, riporto corrente, ancoraggio basso, bit corrente e
le due finestre del protocollo coincidono, ma l'uscita successiva è
diversa. Quello stato proiettato non è quindi una macchina
deterministica chiusa sul dominio generale ancorato.

L'origine del problema si vede anche nella congruenza

\[
d_n\equiv
\begin{cases}0&n\text{ dispari},\\b_{n/2}&n\text{ pari}\end{cases}
\pmod2:
\tag{11}
\]

i termini non diagonali si accoppiano a due a due. A una colonna pari
l'uscita dipende da un bit letto molto prima, che il solo riporto e
quelle finestre non ricostruiscono.

Gli input (8) **non** sono identificati con le potenze della cascata
dal seme 3. La collisione non dimostra un'impossibilità per la sola
torre esatta, né per astrazioni con più uscite o costi d'errore.

## 5. Informazione futura e obbligo quantitativo rimasto

Un riporto `C_L` con `L>N` può dipendere da bit oltre il prefisso di
lunghezza `N`. Condizionare su quel riporto può quindi selezionare
alcuni completamenti; la (5) non nega tale selettività. Si tratta però
di informazione ulteriore, che non si ottiene gratuitamente dal solo
prefisso esposto. Un conteggio finito dei completamenti sopravvissuti
non dimostra un bilancio uniforme sulla torre.

Con gli orizzonti e i conteggi del protocollo, poniamo
`j_v=J_(Q_v)(H_v)`, `m_v=2^(v−1)−j_v` e
`Δ_v=j_(v+1)−2j_v`. La relazione `m_(v+1)=2m_v−Δ_v`, iterata dalla
base congelata `m_16=1155`, dà

\[
m_{16+N}=2^N\left(1155-
\sum_{i=0}^{N-1}\frac{\Delta_{16+i}}{2^{i+1}}\right).
\tag{12}
\]

Quindi maggiorare tutte quelle somme parziali firmate con `1155` è
esattamente equivalente a mantenere tutti i margini successivi
nonnegativi. La (12) rende esplicito l'obbligo, ma non lo risolve:
serve un limite dei costi ricavato dall'aritmetica della sorgente,
indipendentemente dal conteggio di parità da maggiorare.
