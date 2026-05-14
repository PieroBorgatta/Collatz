# Block-Cauchy Drift Summary

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- block drift file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_block_drift.csv`
- T filter: `16`
- active T values: `16`
- final prefix j_count: `8`
- include boundary: `False`
- block sizes: `4`
- adjacent block pairs: `0->4`

## Aggregate By Signature Level

| level | count | mean TV | p90 | p95 | p99 | max | dominant flip frac |
|---|---:|---:|---:|---:|---:|---:|---:|
| `delta` | 262144 | 0.0440102 | 0.25 | 0.25 | 0.5 | 0.75 | 0.0227661 |
| `full` | 262144 | 0.0507774 | 0.25 | 0.25 | 0.5 | 1 | 0.0238647 |
| `phase` | 262144 | 0.0400963 | 0.25 | 0.25 | 0.5 | 1 | 0.00665283 |
| `status` | 262144 | 0.0301514 | 0.25 | 0.25 | 0.5 | 0.75 | 0.0105591 |

## Selected Classes

| class | level | count | mean TV | p95 | max | dominant flip frac |
|---|---|---:|---:|---:|---:|---:|
| `all` | `delta` | 262144 | 0.0440102 | 0.25 | 0.75 | 0.0227661 |
| `all` | `full` | 262144 | 0.0507774 | 0.25 | 1 | 0.0238647 |
| `all` | `phase` | 262144 | 0.0400963 | 0.25 | 1 | 0.00665283 |
| `all` | `status` | 262144 | 0.0301514 | 0.25 | 0.75 | 0.0105591 |
| `full_low` | `delta` | 7008 | 0.0920377 | 0.5 | 0.75 | 0.356735 |
| `full_low` | `full` | 7008 | 0.263128 | 0.75 | 1 | 0.456621 |
| `full_low` | `phase` | 7008 | 0.199486 | 0.75 | 1 | 0.178082 |
| `full_low` | `status` | 7008 | 0.0258276 | 0.25 | 0.75 | 0.0565068 |
| `high_full_tail_weight` | `delta` | 35060 | 0.260211 | 0.5 | 0.75 | 0.0382202 |
| `high_full_tail_weight` | `full` | 35060 | 0.303736 | 0.5 | 1 | 0.0387906 |
| `high_full_tail_weight` | `phase` | 35060 | 0.292128 | 0.5 | 1 | 0.0420993 |
| `high_full_tail_weight` | `status` | 35060 | 0.225442 | 0.5 | 0.75 | 0.0789504 |
| `phase_low` | `delta` | 3280 | 0.16189 | 0.5 | 0.75 | 0.297561 |
| `phase_low` | `full` | 3280 | 0.52378 | 0.7625 | 1 | 0.508537 |
| `phase_low` | `phase` | 3280 | 0.420122 | 0.75 | 1 | 0.376829 |
| `phase_low` | `status` | 3280 | 0.0551829 | 0.25 | 0.75 | 0.120732 |
| `status_exact` | `delta` | 227956 | 0.0108925 | 0 | 0.75 | 0.0211795 |
| `status_exact` | `full` | 227956 | 0.0140553 | 0 | 1 | 0.0246714 |
| `status_exact` | `phase` | 227956 | 0.00298742 | 0 | 0.75 | 0.0031936 |
| `status_exact` | `status` | 227956 | 0 | 0 | 0 | 0 |

## Worst `full` Drifts

| T | r | h | TV | changed | dominant A | dominant B | phase maj | full maj | full tail weight |
|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| 16 | 393 | 0 | 1 | 1 | `return|0|3|1|2` | `return|0|3|1|1` | 0.25 | 0.125 | 0.916667 |
| 16 | 393 | 1 | 1 | 1 | `return|0|3|2|2` | `return|0|3|2|1` | 0.25 | 0.125 | 0.916667 |
| 16 | 393 | 2 | 1 | 1 | `return|0|3|3|2` | `return|0|3|3|1` | 0.25 | 0.125 | 0.916667 |
| 16 | 393 | 3 | 1 | 1 | `return|0|3|0|2` | `return|0|3|0|1` | 0.25 | 0.125 | 0.916667 |
| 16 | 1647 | 0 | 1 | 1 | `return|1|1|1|6` | `return|1|1|1|5` | 0.25 | 0.125 | 0.916667 |
| 16 | 1647 | 1 | 1 | 1 | `return|1|1|2|6` | `return|1|1|2|5` | 0.25 | 0.125 | 0.916667 |
| 16 | 1647 | 2 | 1 | 1 | `return|1|1|3|6` | `return|1|1|3|5` | 0.25 | 0.125 | 0.916667 |
| 16 | 1647 | 3 | 1 | 1 | `return|1|1|0|6` | `return|1|1|0|5` | 0.25 | 0.125 | 0.916667 |
| 16 | 2689 | 0 | 1 | 1 | `return|1|3|1|1` | `return|1|3|1|0` | 0.25 | 0.125 | 0.909091 |
| 16 | 2689 | 1 | 1 | 1 | `return|1|3|2|1` | `return|1|3|2|0` | 0.25 | 0.125 | 0.909091 |
| 16 | 2689 | 2 | 1 | 1 | `return|1|3|3|1` | `return|1|3|3|0` | 0.25 | 0.125 | 0.909091 |
| 16 | 2689 | 3 | 1 | 1 | `return|1|3|0|1` | `return|1|3|0|0` | 0.25 | 0.125 | 0.909091 |
| 16 | 3411 | 0 | 1 | 1 | `return|1|1|1|3` | `return|1|1|1|2` | 0.25 | 0.125 | 0.916667 |
| 16 | 3411 | 1 | 1 | 1 | `return|1|1|2|3` | `return|1|1|2|2` | 0.25 | 0.125 | 0.916667 |
| 16 | 3411 | 2 | 1 | 1 | `return|1|1|3|3` | `return|1|1|3|2` | 0.25 | 0.125 | 0.916667 |
| 16 | 3411 | 3 | 1 | 1 | `return|1|1|0|3` | `return|1|1|0|2` | 0.25 | 0.125 | 0.916667 |

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
