# Continuazione: occupazione pesata e due semi finiti

Data: 24 settembre 2026. Sviluppo successivo alla v6 pubblicata; nessuna modifica
al PDF o all'archivio Zenodo congelati.

## Il risultato matematico alla base della nuova via

Se `f(x)=f(y)` e `x≠y`, almeno uno dei due punti non ritorna a sé stesso in un
numero positivo di passi. Infatti una funzione è iniettiva sui propri punti
periodici. Questo fatto elementare è già disponibile in Mathlib; il contributo
qui cercato è la sua applicazione alla scelta quantitativa dei semi.

Per un inizio dispari positivo `n` della mappa Syracuse, ponendo
`L(n)=4n+1`, si ha esattamente

\[
3L(n)+1=4(3n+1),\qquad S(L(n))=S(n).
\]

Quindi uno fra `n` e `4n+1` non ha ritorni positivi. Più in generale,

\[
3L^k(n)+1=4^k(3n+1)
\]

fornisce due candidati espliciti sopra ogni quota `X`: `L^(X+1)(n)` e
`L^(X+2)(n)`. Entrambi sono dispari, maggiori di `X`, limitati superiormente
dal secondo e hanno successore `S(n)`. Almeno uno non ha ritorni positivi.

**Non ritorno non significa divergenza.** Ad esempio 5 non ritorna a 5 e
raggiunge 1. Non stiamo escludendo cicli del successore, né decidendo quale
candidato soddisfa la proprietà. L'argomento è valido anche se quel successore
appartiene a un ciclo.

Il limite pesato generale non può essere ridotto a `R/x` su target arbitrari:
per `x=R=1` i pesi delle visite sono `(3/4)^k` e la loro somma infinita è 4,
proprio `R(3R+1)/x`. La selezione di un seme senza ritorni fornisce quindi
l'ipotesi aggiuntiva che permette il coefficiente lineare; non è una semplice
ottimizzazione algebrica del limite universale.

## Perché serve per i predecessori

Nel sorgente esterno di Lech Mazur la scelta del seme nonperiodico passa per
un limite esistenziale sull'altezza di un possibile ciclo. Quel limite non è
presente nei dati pubblici del target. È possibile sostituirlo con una coppia
finita nella stessa classe ternaria richiesta dalla stima di massa.

Scriviamo

\[
G(r,k)=\frac{4^k(3r+1)-1}{3},\quad Q=3^q.
\]

Per il rappresentante `p<Q` che realizza il residuo utile, scegliamo
`k₁=p+(X+1)Q` e `k₂=k₁+Q`. I due `G(r,kᵢ)` sono distinti, hanno lo stesso
successore Syracuse e lo stesso residuo modulo `Q`. Entrambi superano `X` e
sono minori di `G(r,(X+3)Q)`. Almeno uno è nonperiodico.

Per un target positivo `a` non divisibile per 3 si può prendere

\[
r=\begin{cases}\lfloor4a/3\rfloor&a\equiv1\pmod3,\\
\lfloor2a/3\rfloor&a\equiv2\pmod3,\end{cases}
\qquad r\le2a.
\]

Il limite uniforme

\[
T(a,q,X)=G(2a,(X+3)3^q)
\]

non dipende dal rappresentante `p` né da quale dei due candidati sia
nonperiodico. Questo permette di proporre costanti del teorema di densità che
non contengono il seme scelto esistenzialmente.

## Collegamento alla libreria principale

`TwoSeed.lean` formalizza la coppia e il limite sopra ogni quota nella mappa
Syracuse del progetto, su Lean 4.29.1. Contiene 13 teoremi e due definizioni.
Il build del modulo e quello integrato sono passati; i sei enunciati
principali usano soltanto i tre assiomi standard.

`NonreturnCounting.lean` collega l'assenza di ritorni all'unicità della parola
esatta da ciascuna sorgente. La formula affine dà il limite individuale
`wordWeight ≤ R/x`; una fibra con al massimo una parola ha lo stesso limite.
Il corollario quantitativo, compilato in Lean, usa dunque `K=R`:

\[
\#\{x<N:x\text{ raggiunge }R\}\ \ge\frac{3N}{256R3^m},
\]

sotto le ipotesi esplicite di massa e budget d'errore. La libreria principale
non importa il mixing esterno: queste ipotesi analitiche restano visibili.
Il registro distingue la compilazione di questo collegamento da quella della
coppia di semi e dall'overlay esterno.

## Le due composizioni esterne

L'overlay separato [`research/weighted_predecessors_adapter`](../../research/weighted_predecessors_adapter/README.md)
contiene due percorsi di prova, su Lean 4.30.0-rc2 e il lock upstream:

1. **Occupazione pesata:** il limite `R(3R+1)/x`, già verificato nella libreria
   principale, sostituisce l'iniettività basata sull'assenza di ritorni. Le
   incidenze terminali sono identificate con parole esatte e poi raggruppate
   per sorgente. Il prezzo è un coefficiente `R(3R+1)` invece di `R`.
2. **Due semi:** si conserva il censimento nonperiodico upstream, ma si
   fornisce un seme sotto il limite uniforme `T`. Si definiscono
   `m=132*T*C+1`, `c=3/(256*T*3^m)` e un cutoff `32*(H+1)`, con `H` il
   limite esplicito di altezza del modello. Le formule complete sono nel
   modulo `TwoSeedDensity.lean`.

Un confronto algebrico ulteriore mostra che, allineando il seme al primo
candidato esplicito sopra descritto e con `X≥2`, si ha `T<R²`. A parità di
`C` e con la ricetta lineare `m(Z)=132*Z*C+1`, il coefficiente costruito con
`T` supera tre volte quello costruito con `P=R(3R+1)`. La dimostrazione
su carta e 113.498 controlli esatti sono nella
[nota di confronto](COEFFICIENT_COMPARISON_IT.md).

Questo confronto non è ancora formalizzato in Lean, non identifica il seme
del chooser pesato attuale con quello esplicito e non confronta i cutoff.
Le costanti finali restano enormi; non ne è stata tentata la valutazione
numerica.

## Dipendenze analitiche e significato del risultato

La stima di mixing esterna riguarda una PMF definita da esponenti geometrici
indipendenti e una distanza L1 **nelle fibre ternarie**. Non afferma
indipendenza delle valutazioni lungo un'orbita deterministica. I lemmi di
esattezza e conteggio sono necessari per passare dalla legge probabilistica
ai predecessori interi.

L'audit semantico ha seguito i wrapper del mixing, il processo renewal finito,
la scelta del residuo e la persistenza della massa. Non ha trovato, nel
perimetro letto, un'ipotesi nascosta di convergenza Collatz. Questo giudizio
circoscritto non sostituisce né una revisione di tutte le dimostrazioni
analitiche né una compilazione completa. Dettagli:

- [mixing e processo renewal](MIXING_AUDIT_IT.md);
- [residuo utile e persistenza della massa](SEED_AUDIT.md);
- [ordine dei parametri della coppia di semi](TWO_SEED_AUDIT.md);
- [definizioni numeriche delle costanti](TWO_SEED_EFFECTIVITY_AUDIT_IT.md).

La lettura degli enunciati pubblici conferma che le sole ipotesi sul bersaglio
sono `a>0` e `3∤a`. `ordinaryPredecessorSet` esclude zero; `natCount` conta
interi distinti strettamente sotto la soglia. Il vincolo sugli intervalli nei
lemmi intermedi viene costruito internamente per ogni soglia sufficientemente
grande: non è lasciato al chiamante e non limita il risultato a una sottosequenza.
Questa lettura dei quantificatori resta distinta dal controllo Lean. La
[revisione degli script di audit](DEPENDENCY_AUDIT_REVIEW_IT.md) precisa inoltre
i diversi perimetri di traversata delle dipendenze.

Il teorema esterno di densità positiva dei predecessori resta attribuito al
suo autore. Il lavoro qui riguarda modifiche della dimostrazione e il
controllo delle costanti. Densità positiva dei predecessori non implica che
tutte le orbite convergano a 1; non è una soluzione della congettura.

## Registro della verifica

Lo stato definitivo, i log e gli hash sono registrati nel manifest di questa
cartella. La compilazione principale Lean 4.29, i controlli isolati Lean 4.30,
la compilazione modulare upstream e l'esperimento di sorgente aggregato sono
verifiche distinte: il successo di una non viene attribuito alle altre.


Stato della libreria principale: **PASS**, build completo di 3371 job e
[CI 36001432687](https://github.com/PieroBorgatta/Collatz/actions/runs/36001432687).
I due moduli contengono complessivamente 23 teoremi. L'audit di 16 enunciati
principali riporta solo `propext`, `Classical.choice` e `Quot.sound`.

Il primo replay esterno CI ha verificato 333 moduli prima di segnalare due
riscritture dipendenti non elaborate in `WeightedPathOccupation`. Le correzioni
sono nel commit `8ce1849`. Il secondo replay
[CI 36001432847](https://github.com/PieroBorgatta/Collatz/actions/runs/36001432847)
ha verificato 340 moduli, incluso `WeightedPathOccupation`, e ha segnalato due
istanze `Subsingleton Unit` mancanti in `WeightedTerminalAdapter`. Le istanze
sono ora esplicite; il controllo dei moduli rimanenti e delle dipendenze finali
è ancora in corso. Questo record non attribuisce ancora al replay esterno un
esito positivo.

Il terzo replay [CI 36003767135](https://github.com/PieroBorgatta/Collatz/actions/runs/36003767135)
ha verificato 391 moduli su 395, inclusi tutti i 388 moduli baseline e
`WeightedPathOccupation`, `WeightedTerminalAdapter`, `WeightedCensus`. Tre
obiettivi naturali `1 ≤ 3^q` richiedevano di passare dalla positività stretta
alla disuguaglianza non stretta; le correzioni sbloccano i due moduli dei semi
e la successiva compilazione dei due teoremi finali.

Il quarto replay [CI 36004436985](https://github.com/PieroBorgatta/Collatz/actions/runs/36004436985)
ha verificato 394 moduli su 395, compreso il teorema finale pesato. In
`TwoSeedDensity` resta una tattica di positività che tenta di espandere
costanti enormi: la correzione usa direttamente le disuguaglianze positive
già dimostrate, senza modificarne i valori o aumentare i limiti di Lean.
