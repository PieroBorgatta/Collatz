# Deterministic K0=16 SCC Residue-Cell Transfer

This run replaces the sampled orbit-harness transition counts with
deterministic enumeration of all finite residue cells in the declared
scope.

## Scope

- SCC rank: `1`
- raw SCC source nodes: `5802`
- lift bits: `4`
- finite lift classes per source: `16`
- total finite lift classes checked: `92832`
- canonical source classes: `76038`
- shadowed initial classes: `16794`
- no-initial classes: `0`
- budget exits: `0`

The enumeration is finite and explicit: every row of the coverage CSV
sums to `2^lift_bits` classes for its raw SCC source node.

## Transfer Matrices

| mode | states | nonzero internal edge types | source events | internal hits | exits | retention mass | rho diagnostic |
|---|---:|---:|---:|---:|---:|---:|---:|
| K | 38 | 254 | 76038 | 71231 | 4807 | 0.936782 | 0.666730647491 |

The edge CSVs store exact rational probabilities as
`count/source_events`; the decimal probability columns are only
legacy-readable diagnostics.
