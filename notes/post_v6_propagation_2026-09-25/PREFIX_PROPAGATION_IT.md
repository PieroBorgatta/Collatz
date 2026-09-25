# Propagazione esatta di tutte le colonne originarie

**25 settembre 2026.** Per la mappa shortcut, dividere il risultato dopo
`t` passi per `3^j`, dove `j` è il numero di passi dispari, lascia come
quoziente esattamente `floor(n/2^t)`. In rappresentazione ternaria questo
significa che **tutte le colonne originarie evolvono mediante semplici
divisioni per due**: gli append a destra non le modificano.

Ne segue un'identificazione esatta dei riporti alla giunzione originaria
con il modello modulare, senza costo di bordo. È un risultato su carta;
non si rivendicano priorità né una formalizzazione Lean. Il controllo
dei riporti non costituisce una stima del peso delle parità o una nuova
discesa.

## 1. Lemma euclideo per ogni intero iniziale

Usiamo la mappa shortcut, estesa anche a zero,

\[
 T(n)=\begin{cases}n/2&n\text{ pari},\\(3n+1)/2&n\text{ dispari}.
 \end{cases}
\]

Siano `n≥0`, `t≥0`, e `j=J_n(t)` il numero di passi dispari fra i
primi `t` passi. Scriviamo

\[
                  n=2^tq+a,\qquad0\le a<2^t.
\]

**Lemma.** Le orbite di `n` e `a` hanno le stesse prime `t` parità e

\[
 T^t(n)=3^j q+T^t(a),\qquad 0\le T^t(a)<3^j.        \tag{1}
\]

In particolare,

\[
 \boxed{\displaystyle
 \left\lfloor\frac{T^t(n)}{3^{J_n(t)}}\right\rfloor
       =\left\lfloor\frac n{2^t}\right\rfloor.}       \tag{2}
\]

**Dimostrazione.** Poniamo `n_s=T^s(n)`, `a_s=T^s(a)` e
`k_s=J_a(s)`. Per `0≤s≤t` dimostriamo simultaneamente

\[
 n_s-a_s=3^{k_s}2^{t-s}q,
 \qquad 0\le a_s<A_s:=3^{k_s}2^{t-s}.              \tag{3}
\]

A `s=0` sono la divisione euclidea iniziale. Se `s<t`, sia `A_s`
sia `n_s−a_s` sono pari. Quindi `n_s` e `a_s` hanno la stessa parità.
Se sono pari, la differenza si divide per due, `k_s` non cambia e
`a_{s+1}=a_s/2<A_s/2=A_{s+1}`.

Se sono dispari, la differenza si moltiplica per `3/2` e
`k_{s+1}=k_s+1`. Poiché `A_s` è un intero pari, `a_s≤A_s−1`;
pertanto

\[
 a_{s+1}=\frac{3a_s+1}{2}
       \le\frac{3A_s-2}{2}
       =\frac32A_s-1<A_{s+1}.
\]

Questo chiude l'induzione. A `s=t`, le parità comuni danno `k_t=j`,
mentre `A_t=3^j`; le formule (3) sono precisamente (1). La divisione
euclidea di (1) per `3^j` dimostra (2). La prova comprende `n=0` e
`t=0`.

## 2. Significato ternario: testa e coda esatte

Sia ora `0<n<3^M` e si rappresenti `n` con esattamente `M` cifre
ternarie, ammettendo zeri iniziali. Dopo `t` passi, si rappresenti
`X_t=T^t(n)` con esattamente `M+j` cifre. Tale larghezza è sempre
valida: un passo pari diminuisce l'intero e un passo dispari soddisfa
`T(x)<3x` per ogni intero positivo `x`.

Le prime `M` cifre rappresentano il quoziente `floor(X_t/3^j)`;
le ultime `j` rappresentano il resto. Per (1)–(2), dunque,

\[
 \begin{split}
 \text{testa di }M\text{ cifre}&=\left\lfloor n/2^t\right\rfloor,\\
 \text{coda di }j\text{ cifre}&=T^t(n\bmod2^t),
 \qquad0\le\text{coda}<3^j.
 \end{split}                                       \tag{4}
\]

Gli zeri iniziali e quelli della coda si conservano per rispettare
queste larghezze. La testa può diventare interamente nulla; l'identità
resta valida anche allora.

**Seconda dimostrazione di (2), mediante il trasduttore.** Conserviamo
sempre gli zeri iniziali e chiamiamo `p_s` l'intero rappresentato dalle
prime `M` colonne dopo `s` passi. La divisione ternaria per due procede
da sinistra a destra, con riporto iniziale zero. Le cifre del quoziente
su quelle colonne dipendono soltanto dalle stesse colonne in ingresso.
L'eventuale cifra `1` aggiunta a destra non modifica quel calcolo.
Quindi `p_(s+1)=floor(p_s/2)` a ogni passo, qualunque sia la parità
dell'intero completo. Da `p_0=n` segue `p_t=floor(n/2^t)`.
D'altra parte la larghezza completa è `M+j`, per cui
`p_t=floor(T^t(n)/3^j)`: si ritrova (2). La dimostrazione aritmetica
del paragrafo precedente copre direttamente anche il caso `n=0`.

Questa interpretazione si colloca nel contesto di Tristan Stérin e
Damien Woods, [*The Collatz process embeds a base conversion algorithm*,
arXiv:2007.06979v4](https://arxiv.org/html/2007.06979v4): il Teorema 16
descrive la conversione fra base `3′` e base due nel loro CQCA, il
Corollario 20 identifica i bit di parità e l'Appendice B.2 dimostra la
correttezza dei trasduttori. Questi risultati sono un riferimento
strutturale pertinente; non si afferma che la formula (2), nella presente
notazione ordinaria, sia letteralmente l'enunciato del loro Teorema 16.
Le due prove sopra rendono autosufficiente l'identità qui utilizzata.

## 3. Prefissi della famiglia di potenze di tre

Siano `r≥1`, `M≥1` tali che

\[
                  X_0=\frac{3^M-1}{2^r}
\]

sia un intero positivo. Si scriva `X_t=T^t(X_0)` con larghezza
`w=M+j`, dove `j=J_(X_0)(t)`. Il prefisso di lunghezza `i` rappresenta

\[
             P_i(X_t)=\left\lfloor\frac{X_t}{3^{M+j-i}}\right\rfloor.
\]

**Teorema.** Per ogni `t≥0` e ogni `1≤i≤M`, senza restrizioni sulla
lunghezza dell'orbita,

\[
 \boxed{\displaystyle P_i(X_t)=
          \left\lfloor\frac{3^i}{2^{r+t}}\right\rfloor.}      \tag{5}
\]

**Dimostrazione.** Applicando (2) e poi dividendo per `3^(M−i)`,

\[
 \begin{split}
 P_i(X_t)
 &=\left\lfloor
     \frac{\lfloor X_t/3^j\rfloor}{3^{M-i}}
   \right\rfloor\\
 &=\left\lfloor
     \frac{3^M-1}{2^{r+t}3^{M-i}}
   \right\rfloor
  =\left\lfloor
     \frac{3^i-3^{i-M}}{2^{r+t}}
   \right\rfloor.
 \end{split}
\]

Scriviamo `3^i=2^(r+t)q+s`. Il resto è un intero dispari, quindi
`1≤s≤2^(r+t)−1`. Poiché `0<3^(i−M)≤1`, sottrarlo a `s`
lascia un numero in `[0,2^(r+t))`. Il quoziente intero resta `q`,
dimostrando (5), incluso il prefisso completo `i=M`.

Il risultato vale in particolare ai tempi `t=2,4,8`, e a ogni altro
tempo intero nonnegativo. Non richiede una stima del tipo
`4^t<3^M`, né un bound desiderato sul numero di passi dispari.
La formula non specifica le ultime `j` colonne aggiunte.

## 4. Giunzione originaria: il modello dei riporti è esatto

Per il progetto poniamo

\[
 r=v+3,\qquad m=2^{v+1}=2^{r-2},\qquad
 Q_v=\frac{3^m-1}{2^r}.
\]

La parola `W` di `Q_v` è completata a `m` cifre. La concatenazione
`WW` rappresenta

\[
       Q_v(3^m+1)=\frac{3^{2m}-1}{2^r}=2Q_{v+1}.
\]

Consideriamo `U_t=T^t(WW)`, con `j_U=J_(WW)(t)`, scritto con
`2m+j_U` cifre. Dividendo la parola grezza per due con riporto
iniziale zero, il riporto uscente dopo la cifra `i` è la parità
del prefisso, cioè `γ_i=P_i(U_t) mod2`. Per (5),

\[
 \gamma_i=\eta_{r+t}(i)
 :=\left\lfloor\frac{3^i}{2^{r+t}}\right\rfloor\bmod2
 =\operatorname{bit}_{r+t}(3^i\bmod2^{r+t+1}),
 \qquad1\le i\le2m.                                \tag{6}
\]

Definiamo il difetto della giunzione originaria sulle prime `2m`
colonne, escludendo le ultime `j_U`:

\[
 D_{\rm actual}(r,t)=\sum_{i=m+1}^{2m}\gamma_i
                    -\sum_{i=1}^{m}\gamma_i,
\]
\[
 D_{\rm model}(r,t)=\sum_{i=m+1}^{2m}\eta_{r+t}(i)
                   -\sum_{i=1}^{m}\eta_{r+t}(i).
\]

Segue l'identità, senza termine d'errore,

\[
               \boxed{D_{\rm actual}(r,t)=D_{\rm model}(r,t).} \tag{7}
\]

A `t=0`, la relazione `3^m≡1+2^r (mod 2^(r+1))` dà
`η_r(i+m)=1−η_r(i)`, quindi

\[
 D_{\rm model}(r,0)=\sum_{i=1}^{m}(1-2\eta_r(i)),
\]

con la stessa convenzione di segno della
[prima giunzione](../post_v6_ternary_2026-09-25/FIRST_SEAM_BOUND_IT.md).
La [nota Fourier](FOURIER_PROPAGATION_IT.md) fornisce una maggiorazione
uniforme di questo modello e quantifica la finestra nella quale il
limite è migliore di quello banale.

## 5. Identità fra i riporti totali delle due orbite

Alla stessa altezza temporale `t`, poniamo

\[
 L_t=T^t(Q_v),\quad j_L=J_(Q_v)(t),\qquad
 U_t=T^t(WW),\quad j_U=J_(WW)(t).
\]

Le parole hanno rispettivamente larghezze `m+j_L` e `2m+j_U`.
Per (5), **le prime `m` colonne superiori coincidono esattamente
con le prime `m` colonne inferiori**, e così anche tutti i loro
riporti in uscita. Non si assume `j_L=j_U`.

Siano `C_L(t)` e `C_U(t)` i numeri totali di riporti in uscita uguali
a uno nelle due parole complete. Indichiamo con `A_L(t)` e `A_U(t)`
gli stessi conteggi limitati alle code di lunghezze `j_L` e `j_U`.
Essendo conteggi di bit,

\[
          0\le A_L(t)\le j_L,\qquad0\le A_U(t)\le j_U.
\]

Sia `H` il conteggio comune delle prime `m` colonne e sia `K` quello
delle seconde `m` colonne superiori. Allora

\[
 C_L=H+A_L,\qquad C_U=H+K+A_U,
 \qquad K-H=D_{\rm model}.
\]

Pertanto

\[
 \boxed{C_U(t)-2C_L(t)
       =D_{\rm model}(r,t)+A_U(t)-2A_L(t),}           \tag{8}
\]

e, senza ipotesi sulla densità delle parità,

\[
 \left|C_U(t)-2C_L(t)-D_{\rm model}(r,t)\right|
       \le\max(j_U,2j_L)\le2t.                     \tag{9}
\]

Questi conteggi coincidono con il carry totale del passo Collatz
successivo nel ledger. Gli zeri iniziali conservati hanno riporto
zero. Se l'intero è dispari, il riporto uscente dalla parola originale
è uno; la cifra `1` aggiunta a destra chiude quel riporto a zero,
quindi non aggiunge un riporto in uscita uguale a uno. Non occorre
un'ulteriore correzione per tale append.

## 6. Portata e limite

L'identità (7) trasferisce senza perdita al difetto delle colonne
originarie ogni stima del modello modulare. La formula (8) collega
inoltre quel difetto ai riporti totali delle due orbite, isolando
esattamente il contributo delle code aggiunte.

La seconda porzione di `m` colonne superiori non viene identificata
con l'orbita inferiore. Le code conservano informazione sulle parità;
il teorema non ne determina i riporti, il peso o la successione dei
bit finali. Il limite `2t` in (9) è una maggiorazione elementare,
non una cancellazione dimostrata nelle code.

Inoltre il confronto dei riporti in (8) usa lo stesso tempo `t` per
le due orbite. Non è direttamente il confronto a tempi diversi che
definisce `E(m,L)`. La maggiorazione Fourier disponibile perde
efficacia molto prima degli orizzonti richiesti da `E` e `Δ_v`.

Non segue quindi una nuova discesa né una stima uniforme del peso
delle parità. La propagazione esatta dei prefissi individua con
precisione l'informazione ancora da controllare: le code introdotte
dagli append e il loro contributo al bilancio globale.
