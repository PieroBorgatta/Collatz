# Somme corte di potenze di tre modulo potenze di due

**Ricerca mirata al 25 settembre 2026.** Il risultato direttamente
utilizzabile è una specializzazione di Mérai–Shparlinski: estende il
controllo delle scansioni prescritte oltre la profondità lineare in `r`.
Il lemma dei prefissi esatti trasferisce ora questo limite alla giunzione
originaria della parola Collatz, senza errore di bordo. Le colonne aggiunte
restano escluse da tale osservabile. Non si rivendica originalità né
completezza bibliografica.

## Osservabili da distinguere

Poniamo `m=2^(r−2)`, `k=r+t+1`, `r≥3`, `t≥0`, e definiamo

\[
 S_{r,t}(a)=\sum_{i=1}^{m}
       (-1)^{\operatorname{bit}_{k-1}(3^{a+i})},\qquad a\ge0.
\]

Il bit può essere calcolato dopo la riduzione modulo `2^k`.
Il confronto fra i due blocchi consecutivi è invece

\[
 D_{r,t}=\sum_{i=1}^{m}
 \bigl(\operatorname{bit}_{k-1}(3^{i+m})-
       \operatorname{bit}_{k-1}(3^i)\bigr)
 =\frac{S_{r,t}(0)-S_{r,t}(m)}2.
\]

Solo a `t=0` l'antiperiodicità dà `D_{r,0}=S_{r,0}(0)`.
La distinzione è necessaria alle profondità successive.

## 1. Mérai–Shparlinski: applicazione diretta nel caso diadico

L. Mérai, I. E. Shparlinski, *Distribution of short subsequences of
inversive congruential pseudorandom numbers modulo 2^t*,
**Mathematics of Computation 89 (322), 911–922 (2020)**,
[DOI](https://doi.org/10.1090/mcom/3467).
Testo verificato: [arXiv:1812.08837v2, 12 giugno 2019](https://arxiv.org/pdf/1812.08837v2),
**Teorema 1.2**, formula (1.5), Lemma 2.1.

Il teorema riguarda `u_n=A/(g^n−b)+c mod 2^k`, con `A,g` dispari,
`b` pari, `β=ν₂(g²−1)`, `2^(32β)<N≤ord_(2^k)(g)`.
La discrepanza è al più `c₀ exp(−η₀(log N)³/k²)`.
Sono ammesse `b=c=0`: scegliendo `g=3`, `A=3^(a+m) mod 2^k`,
`N=m`, i residui sono la finestra desiderata in ordine inverso.
Qui `β=3`; le ipotesi valgono per `r≥99`. L'intervallo `[0,1/2)` dà

\[
 |S_{r,t}(a)|\le B_{r,t},\quad |D_{r,t}|\le B_{r,t},\qquad
 B_{r,t}=2c_0m\exp\!\left[-\eta_0\frac{(\log m)^3}{(r+t+1)^2}\right].
\]

Le costanti sono uniformi in `a`; non ne sono forniti valori numerici
nell'enunciato. **`r≥99` è una soglia di applicabilità, non di risparmio
numericamente certificato.**

La sostituzione mostra `B/m→0` se `k=o(r^(3/2))`: per esempio,
`t≤r^(3/2−ε)`, con `ε>0` fissato. Per `t≈m`, l'esponente tende invece
a zero. Il risultato usa direttamente la discrepanza, senza aggiungere
un fattore logaritmico tramite Fourier.

## 2. Vandehey: differenziazione e cautela sull'ipotesi del primo

J. Vandehey, *Differencing methods for Korobov-type exponential sums*,
**Journal d'Analyse Mathématique 138, 405–439 (2019)**,
[articolo dell'editore](https://doi.org/10.1007/s11854-019-0038-2),
[testo primario arXiv:1606.07911](https://arxiv.org/pdf/1606.07911).

I **Corollari 1.2–1.3 e il Teorema 1.4** trattano
`Σ_{n≤N} e(hb^n/q)` quando i fattori primi di `q` appartengono a un
insieme finito fissato `P`, con `gcd(hb,q)=1`. Sono quindi ammessi
`P={2}`, `b=3`. Il Corollario 1.2 dà risparmio per `N≥q^ε`.
Il Teorema 1.4 scende, per `q` sufficientemente grande, alla soglia

\[
 N\ge\exp\!\left(
 \frac{\log q}{\log_2\log q-3\log_2\log\log q}\right).
\]

Per `q=2^k`, `N=m`, questa soglia ha scala `k/log k=O(r)`,
meno estesa della precedente nel regime asintotico rilevante.
Le differenze finite costituiscono comunque un riferimento tecnico
pertinente per fasi ottenute dai prefissi.

Il **Teorema 2.4**, che riporta il Teorema 4 di Korobov (1972),
richiede esplicitamente un **primo dispari**. Non va applicato
direttamente a `2^k`. Il collegamento diadico sopra usa invece
Mérai–Shparlinski. Nessuno di questi enunciati ammette automaticamente
pesi arbitrari determinati dalla parità dell'orbita.

## 3. Kerr–Mérai–Shparlinski: cifre interne e somme bilineari

B. Kerr, L. Mérai, I. E. Shparlinski, *On digits of Mersenne numbers*,
**Revista Matemática Iberoamericana 38 (6), 1901–1925 (2022)**,
[DOI](https://doi.org/10.4171/RMI/1316),
[testo pubblicato](https://ems.press/content/serial-article-files/39096).

Il **Teorema 1.1** stima somme `Σ_{n≤X} Λ(n)e(ag^n/q^γ)`,
con `q≥3` primo, `q∤ag`, `g≥2`, `2≤X≤q^(Aγ)` e `A>0` fissato.
Il **Teorema 1.3** riguarda blocchi fissati di cifre dei numeri
`2^p−1`, al variare dei primi `p≤X`, nelle posizioni
`ε log X≤j≤(log X)^(3/2−ε)`.

La scala `3/2` e le somme bilineari della Sezione 2 sono pertinenti
al problema dei moduli potenti. Gli autori indicano che l'esclusione
di `q=2` è rimovibile con adattamenti, ma qui non si assumono tali
adattamenti già verificati. I pesi separati delle somme bilineari
non rappresentano automaticamente append adattivi. Il risultato
non fornisce il ponte fra queste scansioni e `E` o `Δ_v`.

## 4. Confronto con lavori più recenti

Mérai–Shparlinski, *Distribution of recursive matrix pseudorandom number
generator modulo prime powers*, **Math. Comp. 93 (2024), 1355–1370**,
[DOI](https://doi.org/10.1090/mcom/3895),
[testo primario](https://arxiv.org/pdf/2302.03964), §§1.2–1.3,
extende il metodo a ricorrenze matriciali. Il dominio resta della forma
`N≥exp(c(log q)^(2/3))`; gli autori descrivono risultati di forza simile
al caso inversivo e discutono separatamente la dimensione uno. Non
ricaviamo da questo lavoro un ampliamento della scala temporale utile
per le nostre due finestre. La specializzazione esplicita del §1 resta
il riferimento operativo.

Bhakta–Shparlinski, *Exponential Sums with Sparse Polynomials and
Distribution of the Power Generator*,
[arXiv:2412.07989v2](https://arxiv.org/html/2412.07989v2), studia somme
complete di polinomi sparsi, anche su moduli composti, e il generatore
`u_n=u_(n−1)^e mod p`. Quest'ultimo non è la successione `3^n mod 2^k`.
Le stime complete del lavoro non sono già una stima delle nostre finestre
corte; non ne assumiamo un trasferimento senza dimostrarlo.

## Una limitazione elementare dell'obiettivo alle profondità grandi

Questa osservazione riguarda **`S_{r,t}(0)` soltanto**, non costituisce
una conseguenza negativa per `D_{r,t}`. Non richiede letteratura:
le prime potenze sono troppo piccole per avere il bit considerato
uguale a uno. Infatti, con

\[
 J=\min\!\left(m,\left\lfloor\frac{k-1}{\log_2 3}\right\rfloor\right),
\]

si ha `3^i<2^(k−1)` per `1≤i≤J`; non esiste uguaglianza fra una
potenza positiva di tre e una di due. I primi `J` addendi valgono `+1`,
i restanti almeno `−1`. Pertanto

\[
                         S_{r,t}(0)\ge2J-m.
\]

Per `t=m` ne segue

\[
 \liminf_{r\to\infty}\frac{S_{r,m}(0)}m
       \ge\frac2{\log_2 3}-1>0.26.
\]

Non è quindi possibile richiedere `S_{r,t}(0)=o(m)` uniformemente
fino a `t=m`. La differenza dei due blocchi potrebbe comportarsi
diversamente: questa osservazione non la decide.

## Implicazione per il progetto

Il [lemma dei prefissi esatti](PREFIX_PROPAGATION_IT.md) identifica
`D_actual(r,t)=D_(r,t)` a ogni tempo: il trasferimento dal modello alle
colonne originarie è quindi dimostrato in questa fase. Combinandolo con
il §1 si ottiene `D_actual/m→0` quando `r+t+1=o(r^(3/2))`, anche se le
parità e il numero delle colonne aggiunte sono scelti dalla dinamica.
Si tratta dell'applicazione di un teorema esistente, con costanti non
esplicitate e senza una nuova soglia numerica certificata.

Rimangono le colonne aggiunte, che la definizione di `D_actual` esclude,
e il raccordo al peso delle parità su tempi dell'ordine di `m`.
Le fonti qui verificate non forniscono quel raccordo. L'ostruzione per
la singola finestra iniziale vieta inoltre una richiesta indiscriminata
di bilanciamento fino a `t=m`; non decide il difetto fra le due finestre.
Questo giudizio riguarda gli enunciati controllati, non afferma
l'assenza di altri risultati pertinenti in letteratura.
