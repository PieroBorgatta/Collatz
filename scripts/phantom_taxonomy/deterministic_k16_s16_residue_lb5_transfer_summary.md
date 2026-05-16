# Deterministic K0=16 SCC Residue-Cell Transfer

This run replaces the sampled orbit-harness transition counts with
deterministic enumeration of all finite residue cells in the declared
scope.

## Scope

- SCC rank: `1`
- raw SCC source nodes: `1240`
- lift bits: `5`
- finite lift classes per source: `32`
- total finite lift classes checked: `39680`
- canonical source classes: `35331`
- shadowed initial classes: `4349`
- no-initial classes: `0`
- budget exits: `0`

The enumeration is finite and explicit: every row of the coverage CSV
sums to `2^lift_bits` classes for its raw SCC source node.

## Transfer Matrices

| mode | states | nonzero internal edge types | source events | internal hits | exits | retention mass | rho diagnostic |
|---|---:|---:|---:|---:|---:|---:|---:|
| K | 37 | 190 | 35331 | 34341 | 990 | 0.971979 | 0.690671054559 |

The edge CSVs store exact rational probabilities as
`count/source_events`; the decimal probability columns are only
legacy-readable diagnostics.
