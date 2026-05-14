# Block-Cauchy Drift Summary

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- block drift file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_block_drift.csv`
- T filter: `15`
- active T values: `15`
- final prefix j_count: `32`
- include boundary: `False`
- block sizes: `16`
- adjacent block pairs: `0->16`

## Aggregate By Signature Level

| level | count | mean TV | p90 | p95 | p99 | max | dominant flip frac |
|---|---:|---:|---:|---:|---:|---:|---:|
| `delta` | 131072 | 0.0297394 | 0.125 | 0.125 | 0.1875 | 0.4375 | 0.0109253 |
| `full` | 131072 | 0.0381069 | 0.125 | 0.1875 | 0.25 | 0.5 | 0.0124817 |
| `phase` | 131072 | 0.0294743 | 0.125 | 0.1875 | 0.25 | 0.4375 | 0.000701904 |
| `status` | 131072 | 0.0182055 | 0.0625 | 0.125 | 0.1875 | 0.375 | 0.0012207 |

## Selected Classes

| class | level | count | mean TV | p95 | max | dominant flip frac |
|---|---|---:|---:|---:|---:|---:|
| `all` | `delta` | 131072 | 0.0297394 | 0.125 | 0.4375 | 0.0109253 |
| `all` | `full` | 131072 | 0.0381069 | 0.1875 | 0.5 | 0.0124817 |
| `all` | `phase` | 131072 | 0.0294743 | 0.1875 | 0.4375 | 0.000701904 |
| `all` | `status` | 131072 | 0.0182055 | 0.125 | 0.375 | 0.0012207 |
| `full_low` | `delta` | 2636 | 0.0932284 | 0.1875 | 0.25 | 0.479514 |
| `full_low` | `full` | 2636 | 0.19338 | 0.375 | 0.5 | 0.556904 |
| `full_low` | `phase` | 2636 | 0.0804249 | 0.25 | 0.3125 | 0.0349014 |
| `full_low` | `status` | 2636 | 0.0137519 | 0.125 | 0.1875 | 0.0576631 |
| `high_full_tail_weight` | `delta` | 34820 | 0.0944787 | 0.1875 | 0.4375 | 0.00700747 |
| `high_full_tail_weight` | `full` | 34820 | 0.124907 | 0.25 | 0.5 | 0.00815623 |
| `high_full_tail_weight` | `phase` | 34820 | 0.110188 | 0.25 | 0.4375 | 0.0019529 |
| `high_full_tail_weight` | `status` | 34820 | 0.0685305 | 0.1875 | 0.375 | 0.00459506 |
| `phase_low` | `delta` | 1624 | 0.075431 | 0.1875 | 0.25 | 0.167488 |
| `phase_low` | `full` | 1624 | 0.236453 | 0.4375 | 0.5 | 0.29064 |
| `phase_low` | `phase` | 1624 | 0.129156 | 0.25 | 0.3125 | 0.0541872 |
| `phase_low` | `status` | 1624 | 0.0223214 | 0.125 | 0.1875 | 0.0935961 |
| `status_exact` | `delta` | 96916 | 0.00667073 | 0.0625 | 0.25 | 0.0131248 |
| `status_exact` | `full` | 96916 | 0.00846609 | 0.0625 | 0.5 | 0.0168806 |
| `status_exact` | `phase` | 96916 | 0.00115564 | 0 | 0.1875 | 0.000908003 |
| `status_exact` | `status` | 96916 | 0 | 0 | 0 | 0 |

## Worst `full` Drifts

| T | r | h | TV | changed | dominant A | dominant B | phase maj | full maj | full tail weight |
|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| 15 | 303 | 0 | 0.5 | 0 | `terminal` | `terminal` | 0.6875 | 0.6875 | 1 |
| 15 | 303 | 1 | 0.5 | 0 | `terminal` | `terminal` | 0.6875 | 0.6875 | 1 |
| 15 | 303 | 2 | 0.5 | 0 | `terminal` | `terminal` | 0.6875 | 0.6875 | 1 |
| 15 | 303 | 3 | 0.5 | 0 | `terminal` | `terminal` | 0.6875 | 0.6875 | 1 |
| 15 | 8135 | 0 | 0.5 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 8135 | 1 | 0.5 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 8135 | 2 | 0.5 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 8135 | 3 | 0.5 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 12857 | 0 | 0.5 | 0 | `return|0|3|1|2` | `return|0|3|1|2` | 0.25 | 0.15625 | 0.791667 |
| 15 | 12857 | 1 | 0.5 | 0 | `return|0|3|2|2` | `return|0|3|2|2` | 0.25 | 0.15625 | 0.791667 |
| 15 | 12857 | 2 | 0.5 | 0 | `return|0|3|3|2` | `return|0|3|3|2` | 0.25 | 0.15625 | 0.791667 |
| 15 | 12857 | 3 | 0.5 | 0 | `return|0|3|0|2` | `return|0|3|0|2` | 0.25 | 0.15625 | 0.791667 |
| 15 | 2263 | 0 | 0.4375 | 0 | `return|1|3|1|3` | `return|1|3|1|3` | 0.25 | 0.15625 | 0.795918 |
| 15 | 2263 | 1 | 0.4375 | 0 | `return|1|3|2|3` | `return|1|3|2|3` | 0.25 | 0.15625 | 0.795918 |
| 15 | 2263 | 2 | 0.4375 | 0 | `return|1|3|3|3` | `return|1|3|3|3` | 0.25 | 0.15625 | 0.795918 |
| 15 | 2263 | 3 | 0.4375 | 0 | `return|1|3|0|3` | `return|1|3|0|3` | 0.25 | 0.15625 | 0.795918 |

## Interpretation

Small adjacent-block TV would be evidence for a Cesaro/high-lift
distributional model.  It is not the same as local constancy, and
it does not prove convergence as block size or prefix length tends
to infinity.

Dominant-signature flips are stricter in one sense and weaker in
another: rare flips can coexist with substantial TV drift when the
same dominant signature keeps changing its mass.  Any future
Keller-Liverani target should use a normed distributional error,
not majority stability alone.
