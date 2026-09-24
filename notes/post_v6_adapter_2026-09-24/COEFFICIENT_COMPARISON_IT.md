# Confronto algebrico dei coefficienti: due semi e occupazione pesata

24 settembre 2026. Dimostrazione a livello matematico e controlli Python
esatti; nessun compilatore Lean eseguito e nessuna modifica ai moduli.
La nuova comparazione `T<R²` e quella fra coefficienti non sono state
formalizzate o verificate in Lean; questo stato è distinto da quello dei
lemmi già esistenti sui due semi e sul loro maggiorante uniforme.

**Risultato:** sotto le ipotesi indicate, il maggiorante uniforme dei due
semi soddisfa `T < R² < P`, dove `P=R(3R+1)` e `R` è già il primo candidato.
Con lo stesso parametro naturale di mixing `C` e la stessa ricetta
`m(Z)=132*Z*C+1`, il coefficiente costruito con `T` è strettamente maggiore
di tre volte quello costruito con `P`. Questo è un confronto fra formule
allineate sul medesimo seme, non fra i chooser dei due teoremi attuali.

## Ipotesi e identità

Siano `a>0`, `3∤a`, `Q=3^q≥1`, `X≥2`, `0≤p<Q` e

\[
r=\begin{cases}\lfloor4a/3\rfloor&a\equiv1\pmod3,\\
\lfloor2a/3\rfloor&a\equiv2\pmod3,
\end{cases}\quad
k=p+(X+1)Q,\quad n=(X+3)Q.
\]

Con `G(s,j)=(4^j(3s+1)-1)/3`, poniamo
`R=G(r,k)`, `T=G(2a,n)`, `b₀=3r+1` e `B=3R+1`.
Queste identità coincidono con `ndGeneralTargetRoot` sui naturali.

Si hanno:

- `b₀=4a` nel primo caso e `b₀=2a` nel secondo;
- `b₀≥4` e `6a+1≤4b₀`;
- `B=4^k b₀`, `3T+1=4^n(6a+1)`;
- `2k−n=2p+(X−1)Q≥1`;
- `k≥3`, dunque `B≥256` e `R≥85`.

## Dimostrazione del maggiorante

Poiché `n+1≤2k`,

\[
3T+1
=4^n(6a+1)
\le 4^{n+1}b_0
\le 4^{2k}b_0
=\frac{B^2}{b_0}
\le\frac{B^2}{4}.
\]

Pertanto

\[
T\le\frac{(3R+1)^2-4}{12}
=\frac{3R^2+2R-1}{4}
=R^2-\frac{(R-1)^2}{4}
<R^2.
\]

L'ultimo confronto non richiede `R≥3`: per la versione non stretta basta
il quadrato `(R−1)²≥0`; per quella stretta qui basta `R>1`.
In particolare `T<P=R(3R+1)`.

Per questo maggiorante sono sufficienti `Q≥1` e `p≥0`: la forma `Q=3^q`
e il limite superiore su `p` non entrano nella dimostrazione. Con
`p<Q`, inoltre `n>k+Q`; dato `r≤2a`, entrambi i candidati
`R₁=G(r,k)` e `R₂=G(r,k+Q)` sono inferiori a `T`.
Poiché `R₁<R₂`, anche `T<R₂²`: il confronto vale per qualunque dei due
semi venga scelto nel successivo argomento di nonperiodicità.

## Coefficienti, con la medesima scelta lineare di m

Per `C∈ℕ` fissato e `Z>0`, definiamo

\[
m_Z=132ZC+1,\qquad
c_Z=\frac{3}{256Z\,3^{m_Z}}.
\]

La funzione `Z↦c_Z` è strettamente decrescente anche quando `C=0`.
Per `P=R(3R+1)` vale l'identità esatta

\[
\frac{c_T}{c_P}
=\frac PT\,3^{132C(P-T)}.
\]

Poiché `T<R²`,

\[
\frac PT>3+\frac1R>3,
\qquad c_T>3c_P>c_P.
\]

Se `C>0`, anche `m_T<m_P`; se `C=0`, entrambi i valori di `m` sono `1`
e il miglioramento viene interamente dal prefattore. Lo stesso ragionamento
si applica a `P₂=R₂(3R₂+1)` quando viene scelto il secondo candidato.

Questo non confronta la ricetta lineare con conduttori scelti in modo
ottimale: cambiando la scelta di `m`, bisogna rifare il confronto.
Non stabilisce un cutoff migliore: nella soglia compare anche l'altezza
dell'intervallo, con basi `T` e `R` diverse. Non stabilisce la dominanza
del coefficiente del codice two-seed su quello del codice weighted attuale,
il cui seme esistenziale non è stato identificato con uno di questi candidati.
Nessuna rivendicazione di priorità o novità bibliografica segue dall'algebra.

## Controlli esatti di coerenza

Python ha verificato tutte le disuguaglianze intermedie su **113.498** tuple:
`1≤a≤200`, `3∤a`, `0≤q≤4`, `2≤X≤8`, tutti `0≤p<3^q`.
Solo aritmetica intera e `fractions.Fraction`, senza floating point.
Il test finito non sostituisce la dimostrazione precedente.

Esempio consentito: `a=2,q=0,X=2,p=0` produce
`r=1,R=85,T=4437,P=21760`, quindi `T/R²=261/425<1` e
`P/T=1280/261>3`.

L'ipotesi `X≥2` non si può eliminare da `T<R²` senza altre modifiche:
`a=2,q=0,X=1,p=0` produce `R=21,T=1109>441=R²`.

Lo script riproducibile è `coefficient_comparison.py`, con risultati in
`coefficient_comparison.json`, accanto alla copia di questa nota nel
repository. Eseguire `python3 coefficient_comparison.py` riscrive il JSON.
Il rapporto macchina distingue espressamente i controlli finiti dalla prova
generale, dalla formalizzazione Lean e dall'allineamento dei chooser.
