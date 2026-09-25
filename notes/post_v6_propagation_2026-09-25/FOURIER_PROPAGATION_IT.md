# Fourier su finestre propagate e prefissi esatti

**25 settembre 2026.** Questa nota estende la stima del primo riporto
a due finestre consecutive di lunghezza fissa, mentre il modulo binario
cresce. La maggiorazione è uniforme nei parametri e nella traslazione
della finestra. Le colonne originali della parola effettiva coincidono
esattamente con il modello a ogni tempo. L'utilità quantitativa della
maggiorazione Fourier termina invece molto prima
dell'orizzonte necessario per `E(m,L)`. È una prova su carta mediante
strumenti classici; non è formalizzata in Lean e non si rivendica
originalità matematica.

## 1. Modello e maggiorazione esplicita

Siano interi `r≥3`, `t≥0` e

\[
 m=2^{r-2},\qquad s=r+t,\qquad
 q=2^{s+1}=8m2^t,\qquad N=2^{s-1}=2^{t+1}m.
\]

Per `x mod q`, sempre rappresentato in `[0,q)`, poniamo
`b_s(x)=floor(x/2^s)∈{0,1}` e

\[
 F_s(x)=1-2b_s(x),\qquad f_s(k)=F_s(3^k\bmod q).
\]

Gli esponenti si leggono modulo `N`. Per qualunque traslazione `a mod N`,
definiamo il difetto fra due finestre consecutive:

\[
 D_{r,t}(a)=\sum_{i=1}^m
 \left[b_s(3^{a+i+m}\bmod q)-b_s(3^{a+i}\bmod q)\right].       \tag{1}
\]

**Proposizione.** Per ogni `r≥3`, `t≥0` e `a mod N`,

\[
 |D_{r,t}(a)|\le B_{r,t}:=
 \frac{\sqrt q}{4}(r-1)(s+1),
 \qquad
 2D_{r,t}(a)^2\le m2^t(r-1)^2(r+t+1)^2.             \tag{2}
\]

La stessa maggiorazione `B_(r,t)` vale per
`|Σ_(i=1..m) f_s(a+i)|`. Si può sempre prendere il minimo con il
limite banale `m`.

Per `t=0`, l'antiperiodicità a distanza `m` dà
`D_(r,0)(0)=Σ_(i=1..m)f_r(i)`, precisamente il difetto della
[prima giunzione](../post_v6_ternary_2026-09-25/FIRST_SEAM_BOUND_IT.md).
La crescita in (2) è `2^(t/2)` moltiplicata per un fattore polinomiale:
non si mantiene una costante uniforme in `t` davanti a `sqrt(m)`.

## 2. Coefficienti della sequenza delle potenze

Usiamo `e(x)=exp(2πix)` e la trasformata non normalizzata

\[
 A_j=\sum_{k=0}^{N-1}f_s(k)e(-jk/N),\qquad
 f_s(k)=\frac1N\sum_{j=0}^{N-1}A_je(jk/N).
\]

Il gruppo `G=⟨3⟩` ha ordine `N` e indice due nelle unità modulo `q`.
Inoltre `3^(N/2)≡1+q/2 mod q`, quindi
`f_s(k+N/2)=−f_s(k)` e `A_j=0` per ogni `j` pari.

Per `j` dispari scegliamo il carattere delle unità con
`χ_j(3)=e(−j/N)` e `χ_j(−1)=−1`, esteso a zero sui residui pari.
È ben definito perché ogni unità è univocamente `±3^k`.
Si ha `χ_j(1+q/2)=−1`; questo è anche il criterio che garantisce la
primitività del carattere rispetto al modulo `q`.

Poiché `F_s(−x)=−F_s(x)` sulle unità, i contributi delle due classi
`G` e `−G` sono uguali:

\[
 A_j=\frac12\sum_{x\bmod q}\chi_j(x)F_s(x).         \tag{3}
\]

Con la trasformata additiva normalizzata
`Fhat_s(h)=q^(−1)Σ_x F_s(x)e(−hx/q)`, le frequenze pari si annullano
e quelle dispari hanno modulo `2/(q sin(πh/q))`. Accoppiando `h` con
`q−h` e usando `sin(πh/q)≥2h/q` per `h<q/2`,

\[
 \sum_h|\widehat F_s(h)|
 \le2\sum_{\substack{1\le h<q/2\\h\ {m dispari}}}\frac1h
 \le s+1.                                         \tag{4}
\]

L'ultimo passaggio somma blocchi diadici:
`Σ_(1≤h<2^k,h dispari)1/h≤(k+1)/2`.

Le somme di Gauss `τ_j(h)=Σ_xχ_j(x)e(hx/q)` sono nulle per `h` pari
e hanno norma `sqrt(q)` per `h` dispari. Per completezza, il primo fatto
segue dalla sostituzione `x→(1+q/2)x`; il secondo dalla sostituzione
invertibile `x→hx` e da Parseval
`Σ_h|τ_j(h)|²=qφ(q)`. Non si sta applicando una formula per moduli
primi a un modulo composto. La prova e la fonte classica sono esplicitate
nella [nota precedente](../post_v6_ternary_2026-09-25/FIRST_SEAM_BOUND_IT.md).

Inserendo la trasformata additiva in (3), otteniamo

\[
                 |A_j|\le\frac{\sqrt q}{2}(s+1)
                 \quad(j\ {m dispari}).          \tag{5}
\]

## 3. La norma della finestra dipende dalla sua lunghezza

Poniamo

\[
 H_j=\sum_{i=1}^m e(ji/N).
\]

La definizione (1) equivale a

\[
 D_{r,t}(a)=\sum_{j\ {m dispari}} A_j e(ja/N)g_j,
 \qquad
 g_j=\frac{(1-e(jm/N))H_j}{2N}.                    \tag{6}
\]

La traslazione cambia soltanto una fase di modulo uno. Per gli indici
dispari la formula geometrica dà

\[
 |g_j|=\frac{\sin^2(\pi jm/N)}{N\sin(\pi j/N)}
 \le\min\left(\frac mN,\frac1{N\sin(\pi j/N)}\right).       \tag{7}
\]

Per la prima disuguaglianza nel minimo basta
`|1−e(jm/N)|≤2` e `|H_j|≤m`; la seconda segue dalla formula esatta.
Accoppiando `j` con `N−j`,

\[
 \sum_{j\ {m dispari}}|g_j|
 \le\sum_{\substack{1\le j<N/2\\j\ {m dispari}}}
           \min\left(2^{-t},\frac1j\right)
 \le\frac{r-1}{2}.                                \tag{8}
\]

La costante finale è indipendente da `t`. Per `t=0`, la somma è
`h_odd(m)≤(r−1)/2`. Per `t≥1`, gli indici dispari `j<2^t` danno al
più `1/2`; i successivi `r−2` intervalli diadici
`[2^(t+k),2^(t+k+1))`, `0≤k≤r−3`, danno ciascuno al più `1/2`.
Questo prova (8), compreso il caso minimo `r=3`.

Moltiplicando (5) e (8) si ottiene (2). Per una sola finestra, il
moltiplicatore è `H_j/N`; soddisfa lo stesso minimo in (7) e quindi
lo stesso argomento dimostra l'ultima affermazione della proposizione.

Usare soltanto `|g_j|≤1/(N sin(πj/N))` darebbe il limite più debole
con `(s²−1)` al posto di `(r−1)(s+1)`. Il miglioramento conserva
l'informazione che la lunghezza della finestra resta `m`, mentre il
periodo `N` cresce.

## 4. Per quanto tempo il limite resta non banale

Il limite esplicito `B_(r,t)` è strettamente minore di `m` esattamente
quando

\[
             2^t(r-1)^2(r+t+1)^2<2^{r-1}.          \tag{9}
\]

Il membro sinistro cresce strettamente con `t`. La tabella seguente
valuta soltanto questa disuguaglianza fra parametri interi: **non
calcola nuove orbite della torre**.

| `r` | Massimo `t` che soddisfa (9) |
|---:|---:|
| 17 | nessuno |
| 18 | 0 |
| 19 | 0 |
| 20 | 1 |
| 22 | 2 |
| 25 | 4 |
| 32 | 10 |
| 40 | 16 |
| 50 | 25 |
| 64 | 37 |
| 100 | 70 |
| 128 | 97 |

Asintoticamente la soglia soddisfa

\[
                  t_{\max}(r)=r-4\log_2 r+O(1).    \tag{10}
\]

Infatti (9) è equivalente a
`t+2log₂(r−1)+2log₂(r+t+1)<r−1`. Ogni indice ammissibile ha `t<r`;
in tale intervallo il prodotto `(r−1)(r+t+1)` è dell'ordine di `r²`,
con costanti assolute. Ne segue (10). In particolare, per ogni `ε>0`
fissato, `0≤t≤(1−ε)r` è coperto per `r` sufficientemente grande.

Questa è una soglia di efficacia della maggiorazione derivata, non una
dimostrazione che il difetto effettivo diventi grande oltre la soglia.
Altre stime delle somme modulari possono avere domini migliori.

## 5. Dal modello alle prime due porzioni della parola effettiva

Consideriamo ora

\[
 U_t=T^t\!\left(\frac{3^{2m}-1}{2^r}\right),\qquad
 j=J_{(3^{2m}-1)/2^r}(t).
\]

Scriviamo `U_t` con esattamente `2m+j` cifre ternarie, aggiungendo zeri
a sinistra. Il difetto `D_actual(r,t)` conta i riporti in uscita della
divisione grezza per due nelle posizioni `m+1..2m`, meno quelli nelle
posizioni `1..m`. **Ignora le ultime `j` posizioni**, introdotte dalla
variazione della larghezza: non è un confronto di interi passi Collatz.

Il [lemma sui prefissi](PREFIX_PROPAGATION_IT.md) dimostra l'identità
generale, valida per ogni intero `n≥0`, ogni `t≥0` e `j=J_n(t)`,

\[
 \left\lfloor\frac{T^t(n)}{3^j}\right\rfloor
 =\left\lfloor\frac n{2^t}\right\rfloor.           \tag{11}
\]

Applicandola a `n=(3^(2m)−1)/2^r` e dividendo ulteriormente per
`3^(2m−i)`, otteniamo, per ogni `1≤i≤2m`,

\[
 \left\lfloor\frac{U_t}{3^{2m+j-i}}\right\rfloor
 =\left\lfloor\frac{3^i}{2^{r+t}}\right\rfloor.     \tag{12}
\]

Il riporto in uscita dalla posizione `i` è la parità di questo prefisso.
**Tutti i primi `2m` riporti**, e dunque entrambi i blocchi originali,
coincidono con `b_s(3^i mod q)`. Non occorre eliminare una fascia finale
né aggiungere un errore di bordo. Per ogni tempo `t≥0`,

\[
 D_{\rm actual}(r,t)=D_{r,t}(0),\qquad
 |D_{\rm actual}(r,t)|\le\min(m,B_{r,t}).            \tag{13}
\]

L'esattezza non assume un limite desiderato su `j` e non deriva da
un'ipotesi di influenza limitata del riporto. Le ultime `j` posizioni,
escluse dalla definizione di `D_actual`, restano necessarie per ricostruire
l'intero valore e la sua parità.

## 6. Portata e limite della propagazione

Le formule (2) e (13) danno una maggiorazione uniforme per un osservabile
ben definito lungo la traiettoria superiore. L'identificazione esatta
dei prefissi vale a ogni tempo e non è una verifica numerica. Il limite
Fourier diventa però banale dopo un numero di passi
dell'ordine di `r`, mentre il confronto richiesto da `E(m,L)` coinvolge
tempi dell'ordine di `m=2^(r−2)`.

Inoltre `D_actual` riguarda riporti nelle due porzioni originali della
parola superiore. Non coincide con `E`, non conta le parità della
traiettoria inferiore e omette le ultime `j` colonne. Una somma dei
limiti (13) non può essere identificata automaticamente con il bilancio
globale delle due orbite. Quel collegamento resta da dimostrare.

Non si ricava quindi una nuova discesa, né una stima uniforme per
`E(m,L)` o `Δ_v`. È stata invece identificata esattamente la parte della
parola governata dalle potenze modulari, insieme all'intervallo breve
in cui questa particolare maggiorazione ne controlla il difetto in modo
non banale.
