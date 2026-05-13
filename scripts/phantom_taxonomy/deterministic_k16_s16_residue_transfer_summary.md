# Deterministic K0=16 SCC Residue-Cell Transfer

This run replaces the sampled orbit-harness transition counts with
deterministic enumeration of all finite residue cells in the declared
scope.

## Scope

- SCC rank: `1`
- raw SCC source nodes: `1240`
- lift bits: `4`
- finite lift classes per source: `16`
- total finite lift classes checked: `19840`
- canonical source classes: `17671`
- shadowed initial classes: `2169`
- no-initial classes: `0`
- budget exits: `0`

The enumeration is finite and explicit: every row of the coverage CSV
sums to `2^lift_bits` classes for its raw SCC source node.

## Transfer Matrices

| mode | states | nonzero internal edge types | source events | internal hits | exits | retention mass | rho diagnostic |
|---|---:|---:|---:|---:|---:|---:|---:|
| node | 1240 | 1631 | 17671 | 17176 | 495 | 0.971988 | 0.614114751961 |
| KL | 76 | 300 | 17671 | 17176 | 495 | 0.971988 | 0.68239680859 |
| K | 37 | 182 | 17671 | 17176 | 495 | 0.971988 | 0.701094388677 |

The edge CSVs store exact rational probabilities as
`count/source_events`; the decimal probability columns are only
legacy-readable diagnostics.
