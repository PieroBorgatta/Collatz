# U06 — Finitezza dei cataloghi a slope limitata

Addendum alla formalizzazione quadratica. Il nuovo file è `lean/CollatzShadowing/BoundedSlopeCatalogue.lean`; **PASS:** build isolata (3298 job; 128 secondi per il nuovo modulo) e audit transitivo di tutte le 9 dichiarazioni compilate, incluse 3 private codificate. I cinque enunciati pubblici usano soltanto `propext`, `Classical.choice`, `Quot.sound`. Non viene formalizzato l’intero no-go di U11, né una sua asintotica.

## Oggetto e prova

Per n naturale e R razionale positivo, il catalogo E(n,R) contiene le liste w per cui esiste una sorgente naturale u>0 con parola effettiva, endpoint n e peso `ω(w)≥1/R`. La slope reciproca è `ρ(w)=1/ω(w)`. Non si impongono disparità, primo arrivo, lunghezza fissata o nonritorno.

Per ogni sottoinsieme finito W del catalogo si sceglie classicamente una sorgente testimone per ciascuna parola. La scelta vale0 fuori dal catalogo e non richiede di dimostrare l’unicità della sorgente. Il modulo `QuadraticOccupation` dà già

`Σ_(w∈W)ω(w)²≤2C(n)`, `C(n)=n²(3n+1)²/(6n+1)`.

Dalla soglia `ω(w)R≥1` segue `1≤ω(w)²R²`. La somma dà quindi

**`card W≤2C(n)R²`.**

Se E fosse infinito, conterrebbe un insieme finito di cardinalità `ceil(2C(n)R²)+1`, in contraddizione con questo bound. La finitezza del catalogo vale quindi anche per target periodici. Il suo ncard eredita la stessa maggiorazione. Non viene assunto che le diverse parole abbiano sorgenti distinte: i ritorni sono ammessi e il budget quadratico li paga.

Le immagini finite sotto le funzioni lunghezza e somma sono limitate superiormente. Si ottengono dunque **esistenzialmente** K,A tali che `length(w)≤K` e `sum(w)≤A` su tutto il catalogo. Il bound numerico sulla cardinalità non è un bound numerico sulla lunghezza massima, non fornisce un algoritmo di arresto e non permette di scambiare finitezza con una stima effettiva sui tempi.

L’ultimo enunciato conserva anche il limite esplicito sulle sorgenti: il potenziale reciproco fornisce `ω(w)u≤n`; con `ω(w)≥1/R` segue `u≤Rn`. Anche questo bound non è un cutoff temporale.

## Domini e limiti

Il target n=0 è ammesso formalmente: non può essere raggiunto da una sorgente positiva e il catalogo è vuoto. Le sorgenti pari sono ammesse perché la funzione totale S e il potenziale sono definiti su tutti i naturali; ciò estende il dominio del soprainsieme usato per il no-go dispari. La parola vuota è ammessa esattamente quando il target è positivo e R≥1.

Il budget tilt intero, compresa la finitezza con ritorni, era già pubblico in [paper9/v1, Proposizione11](https://rstation.ai/problems/collatz/papers/9/v1). Questa integrazione rende verificabile un ingrediente set-teoretico di U11; non rivendica una priorità matematica generale. Non importa Evertse, un no-go asintotico o una minorazione di massa relativa. H e Collatz restano aperte.

## Dichiarazioni pubbliche

- `subcatalogue_card_le`: bound per ogni Finset di parole del catalogo.
- `catalogue_finite`: finitezza dell’intero catalogo.
- `catalogue_ncard_le`: bound numerico sulla cardinalità del catalogo completo.
- `catalogue_parameter_bounds`: limiti esistenziali su lunghezze e totali.
- `catalogue_source_bound`: esistenza di una sorgente testimone positiva≤Rn.

La definizione pubblica è `catalogue`. La scelta di sorgente e il suo lemma sono ausiliari privati. Cinque enunciati rappresentano la scomposizione formale dello stesso ingrediente, non cinque scoperte. I log e la ricevuta locale sono conservati in `research/research_sprint_2026-11-15_three_hours/u06_catalogue/`; l’integrazione e la build completa restano al coordinatore. Nessun esperimento, GPU, commit o push.

La build riuscita è priva di warning. Il primo tentativo fallito è conservato: richiedeva una selezione classica esplicita e due correzioni di API/namespace. Non è stata modificata la struttura della prova matematica.

L’audit finale conferma l’assenza di dipendenze da placeholder o decisioni native nelle nuove dichiarazioni. I sorgenti e i pin registrati nello snapshot sono rimasti invariati fino alla fine del controllo. Non è una ricompilazione a freddo delle dipendenze o un replay con kernel indipendente.
