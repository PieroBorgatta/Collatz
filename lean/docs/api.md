# API

Questa pagina documenta l'API Lean, non una API HTTP. Il progetto non espone
endpoint REST, GraphQL o servizi di rete.

## Namespace

Namespace principale:

```lean
namespace CollatzShadowing
```

## Moduli importati dal target principale

Il file `CollatzShadowing.lean` importa:

```lean
import CollatzShadowing.Basic
import CollatzShadowing.Phantom
import CollatzShadowing.Syracuse2Adic
import CollatzShadowing.Auxiliary
import CollatzShadowing.Shadowing
import CollatzShadowing.NoInfinite
import CollatzShadowing.CollatzBridge
import CollatzShadowing.EpisodeInventory
import CollatzShadowing.EpisodeGraph
import CollatzShadowing.Operator
import CollatzShadowing.WeakBridge
import CollatzShadowing.Bound
import CollatzShadowing.Generated.K16S16KCWSmoke
import CollatzShadowing.Generated.T10CriticalSymbolic
import CollatzShadowing.Generated.T10J32HighBitTail
import CollatzShadowing.Generated.T10J32HighBitTailCW
import CollatzShadowing.Generated.K16S16KExactCWSummary
import CollatzShadowing.Generated.K16S16KDeterministicCW
import CollatzShadowing.Generated.K16S16KLB5DeterministicCW
import CollatzShadowing.Generated.K16S16KLB6DeterministicCW
import CollatzShadowing.Generated.K16S16KSCC
import CollatzShadowing.Generated.K16S16KBridge
import CollatzShadowing.Generated.A0ReturnBranches
```

## Dichiarazioni principali

### Basic

- `nu2Nat`, `ν₂`: valutazione 2-adica su naturali.
- `nu2Int`, `nu2Rat`, `nu2Z2`, `ν₂Z2`: varianti su altri domini.
- `syracuseNumerator`: `3 * n + 1`.
- `syracuseExponent`: esponente rimosso dalla mappa accelerata.
- `S`: mappa Syracuse accelerata su `ℕ`.

### Phantom

- `PhantomWord`: parola finita non vuota di esponenti positivi.
- `PhantomWord.length`, `PhantomWord.A`.
- `Cw`, `Aw`, `qwRat`, `qwZ2`.
- `B`, `aAt`, `B_closed_form`.

### Shadowing e NoInfinite

- `PadicCongruentModPow2`.
- `exact_shadowing`.
- `exact_shadowing_periods`.
- `PhantomWord.Expansive`.
- `no_infinite_period_congruence_expansive`.
- `no_positive_endpoint_eventually_periodic_expansive_congruence`.

### Operatori e certificati

- `EpisodeNode`, `TruncatedEpisodeNode`, `TruncatedEpisodeGraph`.
- `PhaseState`, `TransferMatrix`.
- `OperatorDecomposition`.
- `FiniteCWBasis`, `FiniteCWCertificate`.
- `spectralRadius_le_of_finiteCWCertificate`.

### Bridge condizionali

- `ClassicalCollatzConjecture`.
- `AcceleratedCollatzConjecture`.
- `UniformStrictDescentHypothesis`.
- `classicalCollatz_of_uniformStrictDescent_provedBridge`.
- `GlobalDescentCover`.

## Certificati generati

Esempi di dichiarazioni importanti:

- `t10j32HighBitTailSpectralRadiusBound_97_2000`.
- `k16s16KDeterministicGeneratedSpectralRadiusBound`.
- `k16s16KSpectralRadiusBound`.
- `a0SemanticReplayV2Lt8Cap100_loss_free`.

Consultare `CollatzShadowing/THEOREM_INDEX.md` per la mappa completa
dichiarazione-file.

## API esterne

Nessuna API esterna e chiamata a runtime dal progetto Lean. I generatori Python
nel repository superiore possono produrre file Lean, ma non sono servizi API.
