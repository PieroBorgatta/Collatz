# Pista successiva: il raddoppio di una frontiera ternaria omogenea

**25 settembre 2026.** La rigidità degli antenati seleziona il punto della
torre, ma lascia aperto il controllo del peso della sua parola di parità.
Una rappresentazione complementare permette di formulare precisamente un
possibile lemma successivo. Questa nota contiene una riscrittura e un
limite del metodo, senza nuove stime, esperimenti o rivendicazioni di
originalità.

Sia `J_x(h)` il numero di passi dispari nei primi `h` passi della mappa
abbreviata `T(x)=x/2` sui pari e `(3x+1)/2` sui dispari. Per `v≥5`,
usiamo `H_v=ceil(589·2^v/612)` e
`Δ_v=J_(Q_(v+1))(H_(v+1))−2J_(Q_v)(H_v)`. Poniamo

\[
 m=2^{v+1},\qquad R_m=3^m-1=2^{v+3}Q_v,
 \qquad L_v=H_v+v+3.
\]

La scrittura ternaria di `R_m` consiste in `m` cifre tutte uguali a `2`.
I primi `v+3` passi di `R_m` sono pari e conducono a `Q_v`; pertanto

\[
 J_{Q_v}(H_v)=J_{R_m}(L_v).
\]

Il passaggio al livello successivo raddoppia la lunghezza di questa
frontiera omogenea. Posto `ε_v=2H_v−H_(v+1)∈{0,1}`, vale

\[
 L_{v+1}=2L_v-(v+2+\varepsilon_v).
\]

Definiamo il difetto di concatenazione

\[
 E(m,L)=J_{R_{2m}}(2L)-2J_{R_m}(L).
\]

Eliminare gli ultimi `v+2+ε_v` passi cambia il conteggio dei dispari di
un intero compreso tra zero e quella lunghezza. Segue l'identità con
errore delimitato

\[
 E(m,L_v)-(v+2+\varepsilon_v)\le\Delta_v\le E(m,L_v).
\]

È una riscrittura esatta: non abbiamo ancora stimato `E`.

Il quadro pertinente è l'automa di
[Stérin–Woods, *The Collatz process embeds a base conversion algorithm*,
v4, 2022](https://arxiv.org/html/2007.06979v4).
Il Teorema 16 collega la lettura ternaria delle colonne alla lettura
binaria delle righe; il Corollario 20 identifica le parità attraverso
il transduttore della divisione per due. Questi risultati forniscono una
rappresentazione esatta, ma nessuna stima del difetto qui definito.

Un ostacolo elementare precisa il lavoro necessario. Nella divisione
in base tre per `2^r`, con `r≥1`, leggere una cifra `a` aggiorna il resto
secondo `c↦(3c+a) mod 2^r`. Per una parola ternaria `W` lunga `ℓ`,
l'induzione sulle cifre dà

\[
 c_{\rm out}=(3^\ell c_{\rm in}+[W]_3)\bmod 2^r.
\]

Poiché `3^ℓ` è invertibile modulo `2^r`, questa trasformazione è una
permutazione dei possibili resti. Due resti iniziali distinti non
diventano uguali dopo aver letto la stessa parola. **Non si può quindi
assumere che l'interazione fra le due metà scompaia dopo un numero
costante di cifre.** Questa è una nostra derivazione elementare sulla
divisione, non una conseguenza del paper sul peso delle parità; non
esclude compensazioni aggregate degli effetti dei riporti.

Il prossimo obiettivo sarebbe un lemma quantitativo sul costo di tale
interazione, sfruttando la frontiera esatta e la storia della torre.
La [ricorrenza del margine](../post_v6_margin_2026-09-25/RESULTS_IT.md)
indica quale costo pesato sarebbe sufficiente. Denotando qui con
`m_n=2^(n−1)−J_(Q_n)(H_n)` il margine al livello `n`, si ha

\[
 \frac{m_n}{2^n}=\frac{m_{16}}{2^{16}}
 -\sum_{v=16}^{n-1}\frac{\Delta_v}{2^{v+1}}.
\]

Occorre dunque una maggiorazione dimostrata della somma dei difetti,
compatibile con il margine disponibile. La rappresentazione ternaria
offre una pista per cercarla; non costituisce una soluzione.
