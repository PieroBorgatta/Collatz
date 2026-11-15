# S02 Budget condivisi per pool di radici

13 novembre 2026. Nuovo modulo locale: `lean/CollatzShadowing/RootPoolBudget.lean`. Nessuna dipendenza esterna aggiunta, nessuna modifica all'entrypoint o ai moduli preesistenti.

## Risultato matematico e integrazione web

Il modulo distingue due strumenti.

Per qualunque insieme finito W di parole distinte esatte dalla sorgente x>0, con endpoint R_w, vale il budget dissipativo

`Σ_(w∈W) ω(w)/[R_w(3R_w+1)] ≤ 1/x`.

È una deduzione dell'infrastruttura locale `WeightedVisits` e `WeightedWords`, ora tradotta in Lean. Si ammettono target differenti, visite ripetute, target periodici e parola vuota. Non serve un'ipotesi di terminazione o iniettività della mappa sorgente.

Il confronto diretto con S01 ha identificato un secondo meccanismo della fonte [Shaik, PoolCharge](https://github.com/shaikidris/CollatzConvergencePositiveDensity/blob/f0fda887ee60dc8ac4ef0d864935148b03734726/WordCertDensity/Roots/PoolCharge.lean). Se l'intero pool P non ammette collegamenti orbitali positivi fra i suoi membri, inclusi i ritorni allo stesso membro, allora da una sorgente può esistere al più una parola esatta che termini in P. Si ottiene il budget più forte

`Σ_(w∈W) ω(w)/R_w ≤ 1/x`.

L'idea del pool è attribuita alla fonte nel commento del modulo. Definizione e prove locali sono indipendenti, espresse con la mappa e le parole già presenti nel progetto; nessun teorema analitico o modulo della libreria esterna è importato.

## Interfacce implementate

- `normalizedWeight_eq_loss`: identifica la normalizzazione con la dissipazione al tempo reale della parola.
- `sum_normalizedWeight_le` e `sum_selected_le`: budget generale e sottoselezioni.
- `sum_labeled_normalizedWeight_le`: etichette duplicate sono consentite solo con un carico complessivo per parola al più M; il budget diventa M/x.
- `normalized_source_fiber_bound`: passa al raggruppamento reale per sorgente, consentendo target diversi.
- `distinct_sources_of_normalized_mass`: una minorazione **assunta** η della massa normalizzata selezionata implica `ηX≤card(sorgenti)` quando le sorgenti sono almeno X.
- `NonrecurrentPool`, `pool_visit_time_unique` e `word_eq_of_pool`: dichiarano e utilizzano l'assenza di collegamenti positivi nell'intero pool.
- `reciprocalWeight_le_initial`, `sum_reciprocalWeight_pool_le` e `sum_labeled_reciprocalWeight_pool_le`: budget forte, anche con metadati e carico esplicito per parola.

Le stime superiori sulle etichette non richiedono coefficienti nonnegativi: la loro somma per parola è limitata da M≥0 e il peso fisico è nonnegativo. Le usuali allocazioni probabilistiche ne sono un caso particolare.

## Confronto tra agenti e limiti

S01 ha controllato l'equivalenza dell'interfaccia `NonrecurrentPool` con quella della fonte e non ha identificato ipotesi mancanti. S03 ha fornito il test concettuale essenziale: endpoint successivi dei blocchi crescenti `[1,2]` appartengono alla stessa orbita e quindi non formano questo pool. Per loro rimane applicabile il budget dissipativo generale, non quello forte. S04 sta costruendo un dizionario di cataloghi fisici a profondità e somma degli esponenti fissate; il raggruppamento per sorgenti permette poi di trattare cataloghi a più profondità senza assumere iniettività globale.

Controtest elementare: da x=1 le parole vuota e `[2]` arrivano entrambe a 1. La somma dei carichi `ω/R` è `1+3/4=7/4>1`; il singleton `{1}` non è un pool nonricorrente. Un'etichetta duplicata della stessa parola richiede a sua volta il vincolo di carico: due etichette di coefficiente 1 non possono essere trattate come un'unica incidenza di coefficiente 1.

La minorazione della massa analitica resta aperta. Cambiare normalizzazione non conserva gratuitamente una stima analitica che usava pesi diversi. I risultati non confrontano densità vere di due bacini, non provano H e non escludono cicli o divergenza.

## Verifica

La prima parte, comprendente budget dissipativo, etichette, fibra reale e conteggio condizionale, ha superato l'elaborazione locale. La **build finale del singolo modulo è riuscita, exit 0**, con 3.295 job e 138 secondi per il nuovo modulo. Comando dalla directory lean:

`DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build CollatzShadowing.RootPoolBudget`

Log: `notes/research_sprint_2026-11-13/verification/s02_budget.log`. Le uniche segnalazioni sono due linter su ipotesi `[DecidableEq ι]` superflue nel tipo dei teoremi etichettati; non sono errori di compilazione o ipotesi matematiche nuove. Un audit stretto delle dodici radici è predisposto in `verification/s02_budget_axioms.lean`, ma non è stato eseguito da S02: il coordinatore lo affida a un reviewer successivo.

Il toolchain è quello locale fissato, Lean 4.29.1 con Mathlib corrispondente. La verifica riutilizza dipendenze compilate e non è un replay con kernel indipendente.
