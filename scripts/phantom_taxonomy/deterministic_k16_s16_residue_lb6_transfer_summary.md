# Deterministic K0=16 SCC Residue-Cell Transfer

This run replaces the sampled orbit-harness transition counts with
deterministic enumeration of all finite residue cells in the declared
scope.

## Scope

- SCC rank: `1`
- raw SCC source nodes: `1240`
- lift bits: `6`
- finite lift classes per source: `64`
- total finite lift classes checked: `79360`
- canonical source classes: `70667`
- shadowed initial classes: `8693`
- no-initial classes: `0`
- budget exits: `0`

The enumeration is finite and explicit: every row of the coverage CSV
sums to `2^lift_bits` classes for its raw SCC source node.

## Transfer Matrices

| mode | states | nonzero internal edge types | source events | internal hits | exits | retention mass | rho diagnostic |
|---|---:|---:|---:|---:|---:|---:|---:|
| K | 37 | 209 | 70667 | 68692 | 1975 | 0.972052 | 0.667193301767 |

The edge CSVs store exact rational probabilities as
`count/source_events`; the decimal probability columns are only
legacy-readable diagnostics.
