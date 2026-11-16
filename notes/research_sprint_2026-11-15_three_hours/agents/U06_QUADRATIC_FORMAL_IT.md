# U06 — Dissipazione quadratica e cataloghi con ritorni

Formalizzazione locale del nucleo U02, senza input probabilistici. **PASS:** compilazione isolata del modulo (3297 job; 105 secondi per il nuovo modulo) e audit transitivo di tutte le 24 dichiarazioni compilate, comprese le ausiliarie generate. Gli otto enunciati pubblici usano soltanto gli assiomi standard `propext`, `Classical.choice`, `Quot.sound`. Questo controllo locale è distinto dall’integrazione dell’intera libreria.

## Ambito esatto

Per una sorgente naturale positiva x, con x_k=S^k(x), peso ω_k e potenziale Φ_k=(ω_k/x_k)², il nuovo modulo `QuadraticOccupation.lean` dimostra l’identità

`Φ_k−Φ_(k+1)=ω_k²(6x_k+1)/(x_k²(3x_k+1)²)`.

Il membro destro è positivo. La somma su qualsiasi insieme finito di tempi è quindi al più1/x². Per i soli tempi con x_k=n, la normalizzazione

`C(n)=n²(3n+1)²/(6n+1)`

converte la perdita in peso quadratico e dà `Σ_(k∈H)ω_k²≤C(n)/x²`. Sono ammessi tempo zero e visite ripetute al medesimo target.

Le parole esatte di una sorgente sono determinate dalla loro lunghezza. Il bound sui tempi passa perciò a ogni fibra finita di parole da una sorgente. Raggruppando un catalogo per le sue sorgenti fisiche distinte e usando `Σ_u u⁻²≤2`, già verificato da `IntegerAtomTilt`, si ottiene

`Σ_(w∈W)ω(w)²≤2C(n)`.

Non si richiedono source-injectivity, lunghezza fissata, primo arrivo o nonritorno. Sono sufficienti sorgenti positive, parole effettive ed endpoint comune. Non è necessaria neppure una premessa n>0: un catalogo nonvuoto la forza già. Il caso n=0 rimane coerente e obbliga il catalogo a essere vuoto. L’oddness delle sorgenti non è un input: l’identità del potenziale vale per la funzione totale S anche sui naturali positivi pari.

## Attribuzione e limiti

Il budget Green intero, compresa la finitezza per target periodici, era già pubblico in [paper9/v1, Proposizione11](https://rstation.ai/problems/collatz/papers/9/v1). La costante locale esplicita è migliore del bound grossolano ottenuto dal potenziale lineare; si può anche riconoscere nel fattore geometrico dei ritorni della prova già pubblicata. Non si rivendica una nuova priorità sulla finitezza o un metodo analitico nuovo.

Il modulo dimostra solo enunciati finiti. Nessuna legge casuale, convergenza di serie infinite, stima di densità, relazione con Doob o minorazione relativa viene assunta o formalizzata qui. Passare dai cataloghi finiti alle leggi infinite richiede il dizionario e i limiti dichiarati negli appunti U01/U02. H e Collatz restano aperte.

## Verifica

Il controllo riguarda esclusivamente il nuovo modulo nel toolchain già fissato. L’integrazione dell’intera libreria e il relativo audit sono responsabilità del coordinatore. Nessun esperimento finito ulteriore, GPU, servizio esterno, commit o push è stato eseguito dall’agente.

## Dichiarazioni pubbliche

| Enunciato | Contenuto |
|---|---|
| `visitConstant_nonneg` | Nonnegatività della normalizzazione C(n) |
| `squareLoss_pos` | Positività della perdita quadratica |
| `potential_sq_sub_succ` | Identità esatta di dissipazione |
| `sum_squareLoss_range` | Telescopio da tempo zero |
| `sum_squareLoss_finset_le` | Budget su qualsiasi insieme finito di tempi |
| `sum_weight_sq_visits_le` | Pesi quadratici per visite ripetute |
| `sum_wordWeight_sq_fiber_le` | Trasferimento dai tempi alle parole effettive |
| `tilted_catalogue_le` | Budget globale del catalogo con sorgenti ripetute |

Le due definizioni di supporto sono `squareLoss` e `visitConstant`. Gli otto enunciati non rappresentano otto nuove scoperte: sono la scomposizione formale di un solo argomento di dissipazione e conteggio.

La ricevuta locale e i log sono in `research/research_sprint_2026-11-15_three_hours/u06/`. Il primo tentativo fallito è conservato: richiedeva soltanto una normalizzazione `one_mul`, poi corretta prima della build riuscita. I sorgenti controllati non sono cambiati fra lo snapshot e la fine dell’audit. Non si tratta di un replay con kernel indipendente o di una ricompilazione a freddo delle dipendenze.
