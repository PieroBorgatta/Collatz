# Continuazione: occupazione pesata e due semi finiti

Data: 24 settembre 2026. Sviluppo successivo alla v6 pubblicata; nessuna modifica
al PDF o all'archivio Zenodo congelati.

**Esito finale: entrambe le vie sono compilate e gli audit delle dipendenze
sono passati.** La [CI 36005012141](https://github.com/PieroBorgatta/Collatz/actions/runs/36005012141)
ha completato il replay dei 395 moduli locali sul commit `171150e`.
Il risultato più utile della continuazione è una stima di densità con
costanti uniformi nel bersaglio, senza un'altezza ignota dei cicli nella
scelta del seme. È una modifica verificata della catena di prova esterna;
non una nuova dimostrazione della congettura di Collatz.

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

La libreria principale è **PASS**: build completo di 3371 job e
[CI 36001432687](https://github.com/PieroBorgatta/Collatz/actions/runs/36001432687).
I due nuovi moduli contengono 23 teoremi; i 16 enunciati principali auditati
usano soltanto `propext`, `Classical.choice` e `Quot.sound`.

Anche il replay esterno è **PASS**, su Lean 4.30.0-rc2 e Mathlib fissata dal
lock upstream. La [CI finale 36005012141](https://github.com/PieroBorgatta/Collatz/actions/runs/36005012141)
ha ricontrollato le ricevute di 394 moduli già compilati e compilato l'ultimo:
**395 moduli locali verificati**, di cui 388 della catena originale e sette
dell'overlay. Non è una ricompilazione da zero in una sola esecuzione; il riuso
richiede corrispondenza di sorgenti, dipendenze, configurazione e hash degli
oggetti. Gli oggetti delle librerie esterne provengono dalla cache fissata.

| Audit finale | Perimetro effettivamente percorso | Esito |
|---|---|---|
| Via pesata | 4.672 dichiarazioni locali, inclusi 339 helper privati; 298.851 archi tipo/corpo | Nuovi lemmi raggiunti; vecchia via vietata assente dalla chiusura locale |
| Due semi | 43.248 dichiarazioni raggiungibili, inclusi 5.035 privati; 1.094.025 archi tipo/corpo, senza filtro di modulo | Coppia limitata raggiunta; vecchi selettori con limite ignoto assenti |

Entrambe le radici riportano solo i tre assiomi standard. Il secondo audit
controlla gli assiomi anche durante la traversata diretta. Questi script non
sono checker indipendenti del kernel e non dimostrano l'indispensabilità
logica di ogni lemma raggiunto. La [revisione degli audit](DEPENDENCY_AUDIT_REVIEW_IT.md)
precisa limiti e API utilizzate.

Le evidenze permanenti comprendono:

- [ricevuta completa dei 395 moduli](external_modular_receipt.json);
- [log della compilazione e del riuso](external_modular_build.log);
- [audit pesato](weighted_dependency_audit.log) e [audit dei due semi](two_seed_dependency_audit.log);
- [archivio completo dell'artefatto CI](external_ci_evidence_36005012141.tar.gz),
  inclusi tutti i log dei moduli, autenticazione dei sorgenti, toolchain e lock;
- [manifest SHA-256](verification_manifest.json), con cronologia degli esiti.

Tutti i 395 hash dei log e i sette hash dei sorgenti overlay sono stati
ricontrollati dopo il download dell'artefatto CI. Il campo `compiled: false`
in `weighted-overlay.json`, conservato nell'archivio, descrive esclusivamente
la fase iniziale di preparazione; l'esito successivo è nella ricevuta completa.

I primi quattro replay CI si erano fermati rispettivamente a 333, 340, 391 e
394 moduli: riscritture dipendenti, istanze singleton implicite, positività
non stretta sui naturali e una tattica che espandeva costanti enormi. Tutti
questi errori sono corretti nella revisione verificata. Gli esperimenti locali
interrotti per risorse, incluso il sorgente aggregato, restano verifiche
incomplete distinte: nessun successo viene loro attribuito.
