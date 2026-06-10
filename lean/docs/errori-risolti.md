# Errori risolti

Questa pagina raccoglie problemi tecnici gia documentati nei file del
repository.

## `lake` non nel PATH

Sintomo:

```text
lake: command not found
```

Soluzione osservata:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

Opzionale:

```bash
export PATH="/Volumes/AFUOCO/MAC/Applicazioni/elan/bin:$PATH"
```

## Uso di API Mathlib non adatte a grafi diretti

Problema: le API standard `SimpleGraph`/`Graph` osservate sono orientate a
grafi non diretti o non erano adatte all'episode graph.

Decisione: usare una relazione diretta locale:

```lean
abbrev EpisodeRel (α : Type*) := α → α → Prop
def Reachable (E : EpisodeRel α) (u v : α) : Prop :=
  Relation.ReflTransGen E u v
```

File coinvolti:

- `CollatzShadowing/EPISODE_INVENTORY.md`
- `CollatzShadowing/EpisodeGraph.lean`

## Estensione totale di `Syracuse2adic`

Problema: il punto `x = -1/3` annulla `3*x + 1`, mentre la formula
accelerata richiede una convenzione.

Decisione: definire `Syracuse2adic(-1/3) := 0`, documentando che il punto
degenerato non e usato dagli input di interesse.

File:

- `CollatzShadowing/Syracuse2Adic.lean`

## Direct-return descent non valido

Il log in `TODO.md` registra che la strategia di discesa diretta usando solo
return branch nella stessa coordinata locale e stata esclusa per gli artefatti
osservati. La forma negativa e formalizzata in:

```lean
AffineTBranch.not_nextLocalInteger_lt_sourceLocalInteger_of_coeffNondecreasing
```

Implicazione: non usare quella strategia come prova globale.

## Tails finite cap-75

Il log in `TODO.md` documenta che alcuni tail osservati con cap `75` sono stati
reinterpretati tramite replay semantico cap `100`, con teorema finito:

```lean
a0SemanticReplayV2Lt8Cap100_loss_free
```

Nota: rimane un risultato finito e cap-specific, non un teorema infinito.
