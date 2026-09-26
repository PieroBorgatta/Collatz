# Il riporto futuro come vincolo lineare e l'inversione dei suffissi

26 settembre 2026. Questa nota dimostra le formule usate nel
[protocollo](PROTOCOL_IT.md). Le dimostrazioni sono su carta; non sono
nuovi teoremi Lean. Il vincolo sul riporto viene derivato senza assumere
una maggiorazione del peso delle parità. Le formule valgono anche per
completamenti alternativi e non li identificano con la torre esatta.

## 1. Convoluzione troncata e riporto esatto

Per un intero nonnegativo `P`, siano `b_i=bit_i(P)` e

\[
d_n(P)=\sum_{i+j=n}b_i b_j,\qquad
F_N(P)=\sum_{i+j<N}b_i b_j2^{i+j}.
\]

La ricorrenza scolastica è

\[
C_0=0,\qquad C_{n+1}=\left\lfloor\frac{C_n+d_n}{2}\right\rfloor.
\]

La somma delle prime `N` identità di colonna, moltiplicate per le
rispettive potenze di due, dà

\[
F_N(P)=(P^2\bmod2^N)+2^N C_N(P).
\tag{1}
\]

Infatti `F_N(P)` è congruo a `P²` modulo `2^N`, e le prime `N`
cifre d'uscita rappresentano un numero in `[0,2^N)`. Di conseguenza

\[
C_N(P)=\left\lfloor F_N(P)/2^N\right\rfloor.
\tag{2}
\]

La convoluzione usa soltanto i bit d'ingresso sotto `N`. I bit di
`X` da `K` in su non influenzano quindi `C_(r+K)(1+2^r X)`.
La formula non sostituisce `F_N(P)` con il quadrato dell'intero
prefisso: i prodotti di colonna `i+j>=N` sono esclusi da `F_N`.

Poiché `d_n<=n+1`, si ha anche

\[
0\le C_N(P)\le N-1\qquad(N\ge1).
\tag{3}
\]

Per `N=1`, `C_1=floor(b_0/2)=0`. Se `C_n<=n-1`, la ricorrenza
dà `C_(n+1)<=floor((n-1+n+1)/2)=n`, completando l'induzione.

## 2. Decomposizione del riporto ancorato

Fissiamo `r>=3`, `K>=1`, `N=r+K`, `x_K=X mod2^K` e
`P=1+2^r X`. Il bit zero di `P` è uno; gli altri bit non nulli
provengono da `X`, traslati di `r` posizioni. Separando il prodotto
del bit zero, i due prodotti misti e quelli fra bit traslati, otteniamo

\[
F_N(P)=1+2^{r+1}x_K+2^{2r}F_{K-r}(X),
\tag{4}
\]

quando `K>r`. Se `K<=r`, l'ultimo termine è assente, perché nessuna
coppia di bit traslati ha somma di posizioni minore di `N`.

Ponendo `L=K-r>=1`, le (1), (2), (4) danno

\[
\boxed{C_{r+K}(1+2^rX)=C_L(X)+
\left\lfloor
\frac{2x_K}{2^K}+\frac{X^2\bmod2^L}{2^L}
\right\rfloor.}
\tag{5}
\]

Il termine `2^(-N)` proveniente dal bit zero non cambia il pavimento:
le altre frazioni hanno denominatori che dividono `2^(max(K-1,L))`,
mentre `N>max(K-1,L)`. Il termine aggiuntivo in (5) appartiene a
`{0,1,2}`. In particolare

\[
C_L(X)\le C_{r+K}(1+2^rX)\le C_L(X)+2.
\tag{6}
\]

Per `K<=r`, invece, la (4) senza ultimo termine dà semplicemente
`C_(r+K)(1+2^rX)=floor(2*x_K/2^K)`, in `{0,1}`. La formula
lineare successiva non richiede `K>r` e copre anche questi piccoli casi.

## 3. Una sola lastra lineare sui bit liberi

Siano `1<=H<=K`, `K<=2H`, `u=X mod2^H` e

\[
P_0=1+2^r u,\qquad
X=u+2^H t+2^K h,\qquad 0\le t<2^{K-H}.
\]

Il termine alto `h` è irrilevante per il riporto alla frontiera `N`.
Scriviamo `t=Σ_j t_j2^j`. Le nuove cifre d'ingresso di `P` sono
nelle posizioni `e_j=r+H+j`. Due di queste cifre hanno somma di
posizioni almeno `2r+2H>=r+K=N`, quindi nessun loro prodotto
contribuisce a `F_N(P)`. Restano soltanto i prodotti fra una cifra
nuova e una cifra di `P_0`. Per quella nella posizione `e_j`, le
cifre ammesse di `P_0` sono esattamente quelle sotto
`N-e_j=K-H-j`. I due ordini del prodotto danno

\[
\boxed{F_N(P)=F_N(P_0)+\sum_{j=0}^{K-H-1}t_jW_j,\qquad
W_j=2^{r+H+j+1}(P_0\bmod2^{K-H-j}).}
\tag{7}
\]

Definiamo

\[
c_0=C_N(P_0),\quad R_0=P_0^2\bmod2^N,\quad
\alpha=c_0+R_0/2^N,\quad
w_j=\frac{2(P_0\bmod2^{K-H-j})}{2^{K-H-j}}.
\]

La (1) assicura precisamente `F_N(P_0)=c_0*2^N+R_0`; questa
identità resta valida se il quadrato di `P_0` ha colonne da `N` in
su. Non si presume `P_0²<2^N`. La (7) diventa

\[
C_N(P)=\left\lfloor\alpha+\sum_jt_jw_j\right\rfloor.
\tag{8}
\]

Poiché `P_0` è dispari, `0<w_j<2`. Il vincolo `C_N(P)=c` è
dunque esattamente

\[
\boxed{c\le\alpha+\sum_jt_jw_j<c+1.}
\tag{9}
\]

Equivalentemente si moltiplica (9) per `2^N` e si usa la somma
intera in (7). È un vincolo lineare a una sola fascia sui bit della
sorgente libera. Non è una disuguaglianza già dimostrata sulle parità
shortcut, che sono una diversa funzione di quegli stessi bit.

Gli orizzonti del protocollo soddisfano l'ipotesi: per ogni reale
positivo `a`, `ceil(2a)` è `2ceil(a)` oppure `2ceil(a)-1`. Quindi
`H_(v+1)<=2H_v`. Al livello fissato 16 si hanno
`H=63074`, `K=126147=2H-1`, `r=19` e `N=126166`.

## 4. Riporto certificato dalle ultime B colonne

Siano `1<=B<=N`, `M=N-B` e

\[
S_B=\sum_{j=0}^{B-1}d_{M+j}(P)2^j.
\]

Iterare la divisione euclidea nelle ultime `B` colonne dà esattamente

\[
C_N(P)=\left\lfloor\frac{C_M(P)+S_B}{2^B}\right\rfloor.
\tag{10}
\]

Posto `U=max(M-1,0)`, dalla (3), oppure da `C_0=0`, segue

\[
\boxed{\left\lfloor\frac{S_B}{2^B}\right\rfloor
\le C_N(P)\le
\left\lfloor\frac{S_B+U}{2^B}\right\rfloor.}
\tag{11}
\]

Se i due estremi coincidono, quel solo blocco certifica il riporto
esatto. Se differiscono, non autorizzano a scegliere un estremo:
occorrono ulteriori colonne, il riporto iniziale esatto o un altro
calcolo esatto. L'errore rispetto all'inizializzazione artificiale a
zero soddisfa

\[
0\le C_N-\left\lfloor S_B/2^B\right\rfloor
\le\left\lceil U/2^B\right\rceil.
\tag{12}
\]

In particolare, se `2^B>U`, l'intervallo contiene al massimo due
interi consecutivi. La coincidenza degli estremi, non la sola
piccolezza dell'errore, è il criterio di certificazione.

## 5. Residui shortcut e suffissi con pochi zeri

Per la mappa shortcut `T(n)=n/2` se `n` è pari e
`T(n)=(3n+1)/2` se `n` è dispari, una parola di parità di lunghezza
`H` ha dati affini

\[
T^H(y)=\frac{3^a y+A}{2^H},
\tag{13}
\]

con `a` uguale al numero di uno della parola. Due interi hanno la
stessa parola di lunghezza `H` se e soltanto se hanno lo stesso
residuo modulo `2^H`. Una direzione si prova seguendo la differenza
a ogni passo; nell'altra, la differenza finale nella (13) è intera,
quindi `2^H` divide `3^a(y-y')`, e dunque `y-y'`. Ogni parola ha
un unico residuo: a ciascun passo il nuovo bit del residuo sceglie
una delle due parità possibili. Questa è la biezione classica fra
residui e parole di parità.

Manteniamo una parola iniziale di lunghezza `H`, con dati `(a,A)`,
e completiamola fino a `K` con uno salvo zeri in posizioni assolute
ordinate

\[
H\le t_0<t_1<\cdots<t_{z-1}<K,
\qquad s_j=t_j-H.
\]

Tutte le potenze negative di 3 qui indicano inversi nell'anello
modulo la potenza di due considerata. Il residuo superiore richiesto è

\[
\boxed{y\equiv -(A+2^H)3^{-a}
-\sum_{j=0}^{z-1}2^{t_j}3^{-(a+s_j-j)}\pmod{2^K}.}
\tag{14}
\]

Per provarlo, nel suffisso poniamo `w=n+1`. Un passo dispari
trasforma `w` in `3w/2`; un passo pari lo trasforma in `(w+1)/2`.
Se il suffisso ha lunghezza `F=K-H`, dopo tutti i passi

\[
2^F w_F=3^{F-z}w_0+
\sum_{j=0}^{z-1}2^{s_j}3^{F-z-s_j+j}.
\]

L'integralità impone quindi

\[
n_0=w_0-1\equiv-1-
\sum_{j=0}^{z-1}2^{s_j}3^{j-s_j}\pmod{2^F}.
\]

Sostituendo `n_0=T^H(y)` nella (13) si ottiene (14). Il residuo
è quello della parola richiesta per l'unicità appena dimostrata.

Per zero, uno e due zeri le specializzazioni sono rispettivamente

\[
y_*=-(A+2^H)3^{-a},
\]
\[
y_{t_0}=y_*-2^{t_0}3^{-(a+t_0-H)},
\]
\[
y_{t_0,t_1}=y_*
-2^{t_0}3^{-(a+t_0-H)}
-2^{t_1}3^{-(a+t_1-H-1)},
\tag{15}
\]

sempre modulo `2^K`. L'esponente del secondo zero tiene conto del
primo passo pari: usare lo stesso esponente della formula a un solo
zero per entrambi i termini non sarebbe corretto.

Il peso della parola completata è esattamente `a+(K-H)-z`.
Questa identità riguarda la parola costruita, non una stima del peso
della sorgente effettiva al livello superiore.

## 6. Inversione quadratica con Newton e inverso simultaneo

Per `r>=3` poniamo

\[
f(x)=x+2^{r-1}x^2,\qquad D(x)=1+2^r x.
\]

La fattorizzazione

\[
f(x)-f(x')=(x-x')\bigl(1+2^{r-1}(x+x')\bigr)
\tag{16}
\]

ha secondo fattore dispari. Pertanto
`nu2(f(x)-f(x'))=nu2(x-x')` per interi distinti. In particolare `f`
è iniettiva, e quindi biiettiva, sui residui modulo ogni `2^K`.

Il seguente aggiornamento ricava insieme l'inverso quadratico e quello
della derivata. Supponiamo di avere, a precisione `p>=1`,

\[
f(x)\equiv y\pmod{2^p},\qquad uD(x)\equiv1\pmod{2^p}.
\]

Per `p<q<=2p`, definiamo

\[
e=f(x)-y,\qquad
x'=(x-eu)\bmod2^q,
\]
\[
u'=u\bigl(2-D(x')u\bigr)\bmod2^q.
\tag{17}
\]

Prima della riduzione modulo `2^q`, la variazione `delta=-eu` è
divisibile per `2^p`. L'identità quadratica esatta dà

\[
f(x+\delta)-y=e(1-uD(x))+2^{r-1}\delta^2,
\]

divisibile per `2^(2p)`, dunque per `2^q`. La riduzione di `x'`
non cambia la congruenza. Inoltre `D(x')-D(x)` è divisibile per
`2^p`, quindi `uD(x')≡1 mod2^p`. Infine

\[
u'D(x')\equiv1-(1-uD(x'))^2\equiv1\pmod{2^q}.
\]

Entrambi gli invarianti sono così conservati alla nuova precisione.
La base è `p=1`, `x=y mod2`, `u=1`, poiché `f(x)≡x mod2` e
`D(x)` è dispari. Raddoppiando fino a `K` si ottiene l'unico
residuo `x` con `f(x)≡y mod2^K`.

## 7. Completamenti compatibili e portata del test

Il residuo `y` della (14) conserva la parola superiore effettiva di
lunghezza `H`. Dunque `y≡f(Q_v) mod2^H`. Dalla (16), il suo inverso
`x mod2^K` conserva `Q_v mod2^H`. Ripristinare i bit della sorgente
da `K` in su produce

\[
X=2^K\left\lfloor Q_v/2^K\right\rfloor+x.
\]

Le parole inferiore di lunghezza `H` e superiore costruita di lunghezza
`K` sono quelle richieste per la biezione dei residui. Se i bit alti
contengono il bit principale di `Q_v`, preservano anche la binade.
Questo è il caso del livello 16 fissato nel protocollo.

Con `j_L=J_(Q_v)(H)`, il difetto del completamento è quindi

\[
\Delta_v(X)=a+(K-H)-z-2j_L.
\tag{18}
\]

Le (7), (9), (14), (17), (18) forniscono vincoli e costruzioni esatti
da sottoporre al test finito fissato. Non dimostrano che il vincolo del
riporto escluda ogni parola di peso elevato, né che i completamenti
siano sorgenti della cascata dal seme 3. Una loro eventuale violazione
della candidata `Delta<=g` riguarda la classe selezionata nel protocollo;
non dimostra una violazione sulla torre esatta. Questa nota non contiene
una maggiorazione uniforme di `Delta_v(Q_v)`.
