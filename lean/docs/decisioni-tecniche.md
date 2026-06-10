# Decisioni tecniche

## Lean 4 + Mathlib

Decisione: usare Lean 4 con Mathlib tramite Lake.

Motivo: il progetto e una formalizzazione matematica; Lean fornisce controllo
di tipo, verifica dei teoremi e integrazione con Mathlib.

Versioni:

- Lean `4.29.1`
- Mathlib `v4.29.1`

## Progetto Lake autonomo

Decisione: mantenere `lean/` come progetto Lake autonomo.

Effetto: si puo eseguire `lake build` direttamente da
`/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean`.

## Relazioni dirette per episode graph

Decisione: modellare il grafo episodi come relazione diretta locale, non con
una API Mathlib di grafo non diretto.

File:

- `CollatzShadowing/EpisodeGraph.lean`
- `CollatzShadowing/EPISODE_INVENTORY.md`

## Matrici finite su `NNReal`

Decisione: usare `Matrix ... NNReal` per operatori e certificati finiti.

Motivo: la non-negativita e codificata nel tipo, riducendo ipotesi separate.

## Certificati generati come moduli Lean

Decisione: importare certificati finiti in `CollatzShadowing/Generated/*.lean`.

Motivo: Lean verifica gli artefatti generati come parte del build. I generatori
vivono nella root superiore, soprattutto in:

- `../scripts/phantom_taxonomy/`
- `../scripts/spectral_program/`

La procedura precisa di rigenerazione per ogni file e Da verificare.

## Bridge condizionali dichiarati esplicitamente

Decisione: isolare obblighi matematici non ancora provati come `Prop` nominati.

Motivo: evita di confondere una condizione sufficiente con una prova completa.

Esempi:

- `UniformStrictDescentHypothesis`
- `A0FirstBarrierExistsAll`
- `GlobalDescentCover`

## Nessun Docker

Decisione osservata: nessun Docker nella directory `lean/`.

Motivo: il progetto e compilato da Lake/Lean e non richiede servizi runtime.
