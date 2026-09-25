# Bilanci esatti delle code ternarie

**25 settembre 2026.** Questa nota separa i bit binari dell'input, le
parità Collatz e i riporti delle sole code aggiunte. Le formule sono
identità e maggiorazioni elementari dimostrate su carta; non si
rivendicano priorità o una formalizzazione Lean. La normalizzazione
avvicina la coda a una frazione determinata dall'input, ma non fornisce
un nuovo limite superiore sulla densità dei passi dispari.

## 1. Stato della coda e convenzioni

Sia `n≥0` e sia `T` la mappa shortcut: `T(x)=x/2` per `x` pari,
`T(x)=(3x+1)/2` per `x` dispari. Poniamo

\[
 n_t=T^t(n),\quad p_t=n_t\bmod2,\quad
 j_t=\sum_{i=0}^{t-1}p_i,
 \quad h_t=\left\lfloor n/2^t\right\rfloor\bmod2.
\]

`h_t` è il bit binario dell'input nella posizione `t`, letto dal meno
significativo al più significativo; `p_t` è la parità prodotta.
Il [lemma euclideo dei prefissi](../post_v6_propagation_2026-09-25/PREFIX_PROPAGATION_IT.md)
dà la decomposizione esatta

\[
 n_t=3^{j_t}\left\lfloor n/2^t\right\rfloor+z_t,
 \qquad z_t=T^t(n\bmod2^t),\qquad0\le z_t<3^{j_t}.       \tag{1}
\]

La coda è la rappresentazione ternaria di `z_t` con esattamente `j_t`
cifre, aggiungendo zeri a sinistra. A `t=0` è la parola vuota e
`j_0=z_0=0`.

Poiché `3^j` è dispari, dalla decomposizione segue

\[
 p_t=(h_t+z_t)\bmod2,\qquad j_{t+1}=j_t+p_t,
\]
\[
 \boxed{\displaystyle
 z_{t+1}=\frac{3^{j_t+p_t}h_t+3^{p_t}z_t+p_t}{2}.}    \tag{2}
\]

La formula descrive il trasduttore delle sole code. Si scansionano
le `j_t` cifre con riporto iniziale `h_t`; se `p_t=1`, si aggiunge
la cifra finale `1`. La divisione per due produce la coda successiva
di lunghezza `j_t+p_t`. Il riporto terminale è zero.

## 2. Normalizzazione e frazione binaria dell'input

Definiamo

\[
 u_t=\frac{z_t}{3^{j_t}},\qquad
 a_t=n\bmod2^t=\sum_{i=0}^{t-1}h_i2^i,
 \qquad s_t=\frac{a_t}{2^t}.
\]

La frazione `s_t` si scrive in binario `0.h_(t−1)…h_1h_0`:
è l'ordine inverso rispetto a quello temporale di lettura dei bit.
Non si intende che si stiano leggendo bit nuovi di un altro intero.

Dividendo (2) per `3^(j_t+p_t)` otteniamo

\[
 \boxed{\displaystyle
 u_{t+1}=\frac{h_t+u_t}{2}
          +\frac{p_t}{2\,3^{j_t+1}},}
 \qquad s_{t+1}=\frac{h_t+s_t}{2}.                   \tag{3}
\]

Nel termine correttivo l'esponente `j_t+1` usa il valore di `j`
**prima** del passo. Per `p_t=0` il termine è zero.

Sia `J=j_T`. Iterando (3),

\[
 \delta_T:=u_T-s_T
 =\sum_{i=0}^{T-1}\frac{p_i}{2^{T-i}3^{j_i+1}}
 =\frac{C_T}{2^T3^J}\ge0,                          \tag{4}
\]

dove `C_T` è la costante affine nella formula
`2^T T^T(n)=3^J n+C_T`. L'uguaglianza mostra anche che (4) è una
forma normalizzata della formula affine, non un'informazione
aritmetica indipendente da essa.

Se le posizioni dispari sono `i_1<⋯<i_J`, numerate da zero, allora
`ℓ−1≤i_ℓ≤T−J+ℓ−1`. Applicando questi estremi ai termini
`1/(2^(T−i_ℓ)3^ℓ)` e sommando progressioni geometriche si ottiene

\[
 \boxed{\displaystyle
 2^{-T}\bigl(1-(2/3)^J\bigr)
 \le u_T-\frac{a_T}{2^T}
 \le2^{-J}-3^{-J}.}                                 \tag{5}
\]

Il limite inferiore è raggiunto dalla parola di parità
`1^J0^(T−J)`; quello superiore da `0^(T−J)1^J`. Entrambe sono
parole realizzabili, come dimostrato nel paragrafo 6. Per `J=0`
entrambi gli estremi sono zero. Per `J≥1` l'estremo superiore è
al più `1/6` e decresce con `J`.

La piccolezza dell'errore reale non determina però il bit di parità
di `z_T`. Moltiplicando il solo intervallo superiore in (5) per
`3^J`, la sua larghezza nella coordinata intera `z_T` è

\[
                      (3/2)^J-1,
\]

che cresce con `J`. Per dedurre informazione sui bit finali servono
ulteriori vincoli discreti; non basta un'approssimazione reale accurata.

Un vincolo realmente dipendente soltanto da input, tempo e peso
candidato segue combinando l'estremo inferiore con `z_T≤3^J−1`:

\[
              3^J(2^T-a_T-1)+2^J\ge2^T.            \tag{6}
\]

È un **limite inferiore su `J`**, quindi non ha la direzione richiesta
per la discesa. Se `a_T=2^T−1`, forza `J=T`. Non viene presentato
come un limite superiore sul peso delle parità.

## 3. Bilancio locale della massa ternaria

Sia `S_t` la somma delle cifre della coda di lunghezza `j_t`.
Nel passaggio da `t` a `t+1`, sia `A_t` il numero di riporti in
uscita uguali a uno durante la scansione della sola coda, con
riporto iniziale `h_t`. Si include l'eventuale cifra finale aggiunta;
il suo riporto in uscita è zero, quindi non altera `A_t`.
In particolare `0≤A_t≤j_t`.

Per una cifra in ingresso `d`, una cifra in uscita `q` e riporti
entrante `c` e uscente `c'`, vale `2q=d+3c−c'`. Sommando sulle
cifre scansionate, la somma delle cifre in ingresso è `S_t+p_t`,
il riporto iniziale è `h_t` e quello terminale è zero. Pertanto

\[
 \boxed{2S_{t+1}=S_t+p_t+3h_t+2A_t.}               \tag{7}
\]

Il coefficiente del riporto entrante è **tre**. La formula della
parola completa, che parte con riporto zero, non può essere
trasferita alla coda omettendo questo termine.

Introduciamo anche il deficit di cifre e il complemento dei riporti,

\[
 D_t=2j_t-S_t\ge0,\qquad B_t=j_t-A_t\ge0.
\]

La stessa identità equivale a

\[
             2D_{t+1}=D_t+3(p_t-h_t)+2B_t.          \tag{8}
\]

Le formule comprendono la coda vuota: se `j_t=0`, non ci sono
cifre originarie da scansionare; l'eventuale append produce riporto
terminale zero e `A_t=0`.

## 4. Bilanci telescopici: peso e valore della parola

Per evitare di confondere due quantità diverse, definiamo

\[
 J_T=\sum_{t=0}^{T-1}p_t,\qquad
 H_T=\sum_{t=0}^{T-1}h_t,
 \qquad P_T=\sum_{t=0}^{T-1}2^t p_t.
\]

`J_T` è il peso della parola di parità; `P_T` è il suo valore
intero con il primo bit nella posizione meno significativa.
Analogamente `H_T` è il peso dell'input troncato, mentre
`a_T=Σ2^t h_t` ne è il valore.

Sommando (7) e usando `S_0=0`,

\[
 \boxed{\displaystyle
 J_T=2S_T+\sum_{t=1}^{T-1}S_t-3H_T-2\sum_{t=0}^{T-1}A_t.}   \tag{9}
\]

Moltiplicando invece ogni passo per `2^t` prima di sommare,

\[
 \boxed{\displaystyle
 P_T=2^T S_T-3a_T-2\sum_{t=0}^{T-1}2^t A_t.}        \tag{10}
\]

Le corrispondenti forme in termini di deficit sono

\[
 \boxed{\displaystyle
 3(J_T-H_T)=2D_T+\sum_{t=1}^{T-1}D_t
                     -2\sum_{t=0}^{T-1}B_t,}       \tag{11}
\]

\[
 \boxed{\displaystyle
 3(P_T-a_T)=2^T D_T-2\sum_{t=0}^{T-1}2^t B_t.}      \tag{12}
\]

Le somme sono vuote se `T=0`; tutte le identità restano valide.
Le formule (9) e (11) riguardano il peso non pesato, mentre (10)
e (12) riguardano valori binari. Non è lecito trasformare le
seconde nelle prime dividendo per una singola potenza di due.

Questi bilanci isolano esattamente le quantità mancanti. Per una
nuova stima di `J_T` occorre controllare somme di masse e riporti
delle code mediante informazioni indipendenti sul particolare
input. Riordinare (9) o (11) in una condizione equivalente al
limite desiderato non costituisce una nuova stima.

## 5. Due orbite agli orizzonti effettivi del confronto

Poniamo

\[
 r=v+3,\quad m=2^{v+1},\quad
 Q_v=\frac{3^m-1}{2^r},\quad
 H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil.
\]

La parola `W` di `Q_v` viene completata a `m` cifre. La parola
`WW` rappresenta `(3^(2m)−1)/2^r=2Q_(v+1)`.
Le due orbite di coda partono rispettivamente da `Q_v` e `WW`;
per il confronto originale i tempi sono

\[
                    T_L=H_v,\qquad T_U=2H_v+r.
\]

Indichiamo con apici `L,U` le statistiche definite sopra per i
rispettivi input. Applicando (9) ai due tempi e sottraendo,

\[
 \boxed{\begin{split}
 E_v={}&2S^U_{T_U}-4S^L_{T_L}\\
      &+\sum_{t=1}^{T_U-1}S^U_t
                -2\sum_{t=1}^{T_L-1}S^L_t\\
      &-3\left(\sum_{t=0}^{T_U-1}h^U_t
                -2\sum_{t=0}^{T_L-1}h^L_t\right)\\
      &-2\left(\sum_{t=0}^{T_U-1}A^U_t
                -2\sum_{t=0}^{T_L-1}A^L_t\right),
 \end{split}}                                      \tag{13}
\]

dove `E_v=J_(WW)(T_U)−2J_(Q_v)(T_L)`.
Questo è precisamente il difetto definito sulle parole iniziali
`R_m=3^m−1` al tempo `L=H_v+r` e `R_(2m)` al tempo `2L`:
i primi `r` passi di entrambe sono divisioni pari; restano quindi
`H_v` passi per `Q_v` e `2H_v+r` passi per `WW`.

Per raccordare `E_v` al difetto fra livelli, definiamo

\[
 \Delta_v=J_{Q_{v+1}}(H_{v+1})-2J_{Q_v}(H_v),
 \qquad\varepsilon_v=2H_v-H_{v+1}\in\{0,1\}.
\]

Il primo passo di `WW=2Q_(v+1)` è pari. Dopo averlo tolto, il tempo
superiore è `T_U−1`, che supera `H_(v+1)` di

\[
          T_U-1-H_{v+1}=r-1+\varepsilon_v
                       =v+2+\varepsilon_v.
\]

Se `K_v` è il numero di passi dispari in questo tratto aggiuntivo,

\[
 \boxed{E_v=\Delta_v+K_v,\qquad
        0\le K_v\le v+2+\varepsilon_v.}             \tag{14}
\]

Non si identifica quindi `E_v` con `Δ_v` senza la correzione.

Come controllo finito, i [risultati del probe](tail_results.json)
riportano per `v=12`, `T_L=3943` e `T_U=7901` i quattro termini
di (13), nell'ordine in cui sono scritti:

\[
                  128+8231992-354-8231656=110.
\]

Qui `Δ_12=99` e il tratto aggiuntivo contiene `K_12=11` passi
dispari, coerentemente con (14). La forte cancellazione fra le
somme interne e i riporti è una **verifica dell'identità**, non
una maggiorazione dimostrata per livelli ulteriori. Per ottenere
un limite utile occorre controllare tale differenza congiuntamente;
maggiorare separatamente i grandi termini assoluti perde la
cancellazione osservata.

## 6. Biezione dei cilindri e limite delle conclusioni universali

La ricorrenza delle code mostra direttamente perché le identità
precedenti non impongono una densità universale minore di uno.

Fissiamo una qualunque parola desiderata `p_0,…,p_(T−1)`. Partendo
da `j_0=z_0=0`, a ogni passo scegliamo univocamente

\[
                     h_t=p_t\mathbin{\mathrm{xor}}(z_t\bmod2),
\]

e aggiorniamo `j,z` mediante (2). L'integralità e il vincolo sul
resto si conservano: posto `K=3^j`, il numero `N=hK+z` è in
`[0,2K)` e ha parità `p`. Se `p=0`, il nuovo resto è `N/2<K`;
se `p=1`, è `(3N+1)/2≤3K−1<3K`.

I bit scelti definiscono un unico residuo
`a_T=Σ2^t h_t mod2^T`. Per (1)–(2), ogni intero nonnegativo
con quel residuo ha precisamente la parola di parità desiderata
nei primi `T` passi. Viceversa la scelta di `h_t` è unica a ogni
passo. Si ottiene così la biezione fra i `2^T` residui binari e
le `2^T` parole di parità.

Ad esempio, per `n≡2^T−1 mod2^T`, tutti i primi `T` passi sono
dispari. Lungo questo prefisso,

\[
 h_t=p_t=1,\quad j_t=t,\quad z_t=3^t-1,
 \quad S_t=2t,\quad A_t=t,
\]

e tutte le formule sopra sono soddisfatte, incluso l'estremo superiore
in (5). Pertanto non può seguire da queste sole identità un limite
`J_T≤ρT+o(T)` con `ρ<1` **uniforme su tutti gli input**. Qui l'input
del controesempio può dipendere da `T`; non si sta affermando che
un singolo intero positivo abbia infiniti passi consecutivi dispari.

Questo limite non esclude una stima specifica per la torre `Q_v`.
Per ottenerla serve utilizzare una proprietà selettiva dei suoi bit
`h_t` o delle sue code, oltre a relazioni valide per ogni input.
Il problema residuo è ora formulato sulle code, ma non è stato
risolto dalle identità telescopiche. La
[nota sulla memoria](MEMORY_OBSTRUCTION_IT.md) precisa quali stati
sono raggiungibili e quanta precisione è necessaria per prevedere
esattamente un numero fissato di uscite future.
