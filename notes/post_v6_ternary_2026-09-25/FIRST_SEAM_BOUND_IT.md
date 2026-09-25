# Una stima uniforme per il primo difetto di riporto

**25 settembre 2026.** Si dimostra una stima deterministica per la somma
di bit che descrive il primo confronto dei riporti alla giunzione
ternaria. La prova applica il completamento di Fourier e le somme di
Gauss classiche. **Non è una stima del difetto Collatz completo `E`,
né di `Δ_v`**: i successivi append dipendenti dalla parità non sono
controllati. Non si rivendica originalità e non si tratta di una prova Lean.

## 1. Enunciato e normalizzazioni

Siano `r≥3`, `m=2^(r−2)`, `N=2m=2^(r−1)` e `q=8m=2^(r+1)`.
Per un residuo `x` si intende sempre il suo rappresentante in `[0,q)`.
Definiamo

\[
 F(x)=\begin{cases}1&0\le x<q/2,\\-1&q/2\le x<q,\end{cases}
 \qquad f(k)=F(3^k\bmod q),
 \qquad D_r=\sum_{i=1}^{m}f(i).
\]

Quindi `f(i)=(-1)^(bit_r(3^i mod q))`. Scriviamo

\[
 h_{\rm odd}(M)=\sum_{\substack{1\le a<M\\a\text{ dispari}}}\frac1a.
\]

Per esplicitare il collegamento ai riporti, sia
`Q=(3^m−1)/2^r`, scritto in ternario con esattamente `m` cifre,
aggiungendo zeri iniziali. Il valore del prefisso di `i` cifre è
`floor(Q/3^(m−i))=floor(3^i/2^r)`: la sottrazione del termine
`1/(2^r3^(m−i))` non attraversa un intero, poiché `3^i` è dispari.
Nella divisione elementare di questa parola per due, senza append,
il riporto uscente dopo `i` cifre è dunque `bit_r(3^i)`. Se `C_r`
conta questi riporti uguali a uno, inclusa l'ultima cifra, allora

\[
                              D_r=m-2C_r.
\]

L'osservabile così definito non include gli effetti successivi degli
append sulle parole delle traiettorie.

**Proposizione.** Per ogni `r≥3`,

\[
 |D_r|\le\sqrt{8m}\,h_{\rm odd}(4m)h_{\rm odd}(m)
 \le\frac{\sqrt{8m}}4(r^2-1).                       \tag{1}
\]

In particolare

\[
                      2D_r^2\le m(r^2-1)^2.         \tag{2}
\]

Il limite polinomiale è strettamente migliore del limite banale `m`
da `r=18` (`v=15`, quando `r=v+3`). È una stima di ordine
`sqrt(m)·r²` del primo difetto soltanto.

La trasformata additiva su `Z/qZ` è normalizzata mediante

\[
 \widehat F(a)=\frac1q\sum_{x=0}^{q-1}F(x)e(-ax/q),
 \qquad F(x)=\sum_{a=0}^{q-1}\widehat F(a)e(ax/q),
 \qquad e(t)=\exp(2\pi it).
\]

Sul gruppo degli esponenti `Z/NZ` usiamo invece i coefficienti
**non normalizzati**

\[
 A_j=\sum_{k=0}^{N-1}f(k)e(-jk/N),
 \qquad f(k)=\frac1N\sum_{j=0}^{N-1}A_je(jk/N).
\]

## 2. Il sottogruppo delle potenze di tre

Il lemma LTE, oppure l'induzione per quadrature, dà

\[
 \operatorname{ord}_q(3)=N,\qquad 3^m\equiv1+q/2\pmod q.
\]

Pertanto il sottogruppo `G=⟨3⟩` ha indice due nelle unità modulo `q`.
Le sue classi modulo otto sono `1,3`; in particolare `−1∉G`.
Ogni unità si scrive univocamente come `(-1)^ε3^k`, con
`ε∈{0,1}` e `k mod N`.

Per ogni `x` dispari, moltiplicare per `1+q/2` equivale ad aggiungere
`q/2` modulo `q`. Il bit superiore cambia, quindi

\[
                         f(k+m)=-f(k).              \tag{3}
\]

Ne segue `A_j=0` per `j` pari, incluso `j=0`.

Per `j` dispari scegliamo il carattere delle unità determinato da

\[
                  \chi_j(3)=e(-j/N),\qquad\chi_j(-1)=-1.
\]

Lo estendiamo a zero sui residui pari. Poiché
`χ_j(1+q/2)=χ_j(3^m)=−1`, non può fattorizzarsi modulo `q/2`,
né modulo un divisore proprio di `q`: è primitivo.
Sulle unità vale anche `F(−x)=−F(x)`. I contributi di `x∈G`
e di `−x∈−G` al prodotto `χ_j(x)F(x)` sono uguali. Di conseguenza

\[
             A_j=\frac12\sum_{x\bmod q}\chi_j(x)F(x).       \tag{4}
\]

Il fattore `1/2` è essenziale: si usa una sola estensione, scelta
dispari, del carattere su `G`.

## 3. Somme di Gauss: prova nel caso necessario

Poniamo

\[
             \tau_j(a)=\sum_{x\bmod q}\chi_j(x)e(ax/q).
\]

Per `a` pari, sostituire `x` con `(1+q/2)x` cambia il segno del
carattere e lascia invariato il fattore esponenziale. Quindi `τ_j(a)=0`.
Per `a` dispari, la sostituzione invertibile `y=ax` mostra che
`τ_j(a)=χ_j(a)^(-1)τ_j(1)`; tutti questi coefficienti hanno la
stessa norma. L'ortogonalità additiva dà

\[
 \sum_{a=0}^{q-1}|\tau_j(a)|^2
 =q\sum_{x=0}^{q-1}|\chi_j(x)|^2=q\varphi(q)=q^2/2.
\]

Ci sono `q/2` indici dispari. Pertanto

\[
                     |\tau_j(a)|=\sqrt q\quad(a\text{ dispari}).   \tag{5}
\]

Questo è il caso particolare del lemma sulle somme di Gauss primitive
esposto da [Keith Conrad, *Gauss and Jacobi sums*, Lemma 3.10 e
Teorema 3.12, p. 7](https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf).
La dimostrazione precedente rende autosufficiente l'uso del risultato
per il modulo composto `q`, che è una potenza di due.

## 4. Le due somme dei moduli dei coefficienti

La funzione `F` cambia segno traslando di `q/2`. Quindi `Fhat(a)=0`
per `a` pari. Sommando una progressione geometrica, per `a` dispari
si ottiene

\[
 \widehat F(a)=\frac{4}{q(1-e(-a/q))},\qquad
 |\widehat F(a)|=\frac{2}{q\sin(\pi a/q)}.            \tag{6}
\]

Per ogni potenza di due `K≥4`, accoppiando `a` con `K−a` e usando
`sin(πa/K)≥2a/K` quando `0<a<K/2`,

\[
 \sum_{\substack{1\le a<K\\a\text{ dispari}}}
       \frac1{\sin(\pi a/K)}
 \le K\,h_{\rm odd}(K/2).                            \tag{7}
\]

Segue da (6)–(7)

\[
                 \sum_a|\widehat F(a)|\le2h_{\rm odd}(4m).  \tag{8}
\]

Sostituendo lo sviluppo additivo in (4) e usando (5),

\[
             |A_j|\le\frac{\sqrt q}{2}\sum_a|\widehat F(a)|
                    \le\sqrt q\,h_{\rm odd}(4m)
                    \quad(j\text{ dispari}).        \tag{9}
\]

Per la finestra degli indici **da 1 a `m`, estremi inclusi**, definiamo

\[
 H_j=\sum_{i=1}^{m}e(ji/N),\qquad
 D_r=\frac1N\sum_{j\text{ dispari}}A_jH_j.
\]

Per `j` dispari la somma geometrica dà
`|H_j|=1/sin(πj/N)`. La finestra da `0` a `m−1` moltiplicherebbe
`H_j` per una fase unitaria: cambierebbe eventualmente la somma
firmata, ma non questa stima. Applicando (7) con `K=N`,

\[
              \frac1N\sum_{j\text{ dispari}}|H_j|
              \le h_{\rm odd}(m).                   \tag{10}
\]

Le formule (9)–(10) dimostrano la prima disuguaglianza di (1), senza
perdite dovute agli estremi della finestra.

## 5. Costanti esplicite e soglie

Se `M=2^k`, `k≥1`, il termine iniziale di `h_odd(M)` è `1`.
Ciascun intervallo `[2^ℓ,2^(ℓ+1))`, per `1≤ℓ≤k−1`, contiene
`2^(ℓ−1)` interi dispari, ciascuno con reciproco al più `2^(−ℓ)`.
Dunque

\[
                 h_{\rm odd}(2^k)\le1+(k-1)/2=(k+1)/2.
\]

Con `4m=2^r` e `m=2^(r−2)` si ottiene la seconda disuguaglianza
di (1) e quindi (2). Per `r=18`,
`(r²−1)²=104329<2m=131072`; per `r=17` il confronto è
`82944>65536`. Il rapporto `(r²−1)²/2^(r−2)` decresce per
`r≥7`, poiché
`((r+1)²−1)/(r²−1)≤4/3<sqrt(2)` in quell'intervallo.
Questo prova la soglia indicata per il limite polinomiale.

Una variante più precisa segue direttamente dal confronto integrale

\[
 h_{\rm odd}(M)=\sum_{j=0}^{M/2-1}\frac1{2j+1}
 \le1+\frac12\log(M-1)\le1+\frac12\log M.
\]

Quando `r=v+3`, usando `log 2<7/10`, si ricava

\[
 |D_r|\le\sqrt{8m}\,
       \frac{(7v+27)(7v+41)}{400}.                  \tag{11}
\]

Questo limite è già minore di `m` per `v≥13`: alla base,
`(118·132)²=242611776<20000·16384=327680000`.
Il rapporto fra il prodotto dei due fattori a `v+1` e quello a `v`
è al più `(7/6)²`, per `v≥3`; il suo quadrato è minore di due.
Il confronto resta quindi valido per tutti i livelli successivi.
Queste sono soglie delle maggiorazioni dimostrate, non nuove verifiche
di orbite della torre.

## 6. Il limite della conclusione

La somma `D_r` riguarda il primo confronto di riporti sulla parola
ternaria prescritta. Il confronto successivo fra due traiettorie
shortcut include append diversi quando le parità divergono: dividere
la parola superiore concatenata per due e applicare `T` alla parola
inferiore non sono la stessa operazione. Una stima per quel primo
difetto non può essere sommata automaticamente lungo tutta l'orbita.

Per controllare `E(m,L)` o il costo pesato di `Δ_v` occorrerebbe un
ulteriore lemma che conservi una descrizione utilizzabile delle parole
e dei riporti dopo questi append. Tale lemma resta aperto. La presente
prova individua una cancellazione aritmetica uniforme in un singolo
passaggio, senza fornire la propagazione necessaria per la discesa.
