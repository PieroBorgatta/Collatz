# Block-Cauchy Drift Summary

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- block drift file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_block_drift.csv`
- T filter: `15`
- active T values: `15`
- final prefix j_count: `16`
- include boundary: `False`
- block sizes: `8`
- adjacent block pairs: `0->8`

## Aggregate By Signature Level

| level | count | mean TV | p90 | p95 | p99 | max | dominant flip frac |
|---|---:|---:|---:|---:|---:|---:|---:|
| `delta` | 131072 | 0.0385513 | 0.125 | 0.25 | 0.25 | 0.75 | 0.0167542 |
| `full` | 131072 | 0.0462265 | 0.125 | 0.25 | 0.375 | 0.75 | 0.0177002 |
| `phase` | 131072 | 0.0365944 | 0.125 | 0.25 | 0.375 | 0.75 | 0.000793457 |
| `status` | 131072 | 0.0253372 | 0.125 | 0.125 | 0.25 | 0.75 | 0.00244141 |

## Selected Classes

| class | level | count | mean TV | p95 | max | dominant flip frac |
|---|---|---:|---:|---:|---:|---:|
| `all` | `delta` | 131072 | 0.0385513 | 0.25 | 0.75 | 0.0167542 |
| `all` | `full` | 131072 | 0.0462265 | 0.25 | 0.75 | 0.0177002 |
| `all` | `phase` | 131072 | 0.0365944 | 0.25 | 0.75 | 0.000793457 |
| `all` | `status` | 131072 | 0.0253372 | 0.125 | 0.75 | 0.00244141 |
| `full_low` | `delta` | 2580 | 0.0893411 | 0.25 | 0.5 | 0.274419 |
| `full_low` | `full` | 2580 | 0.239147 | 0.625 | 0.75 | 0.327132 |
| `full_low` | `phase` | 2580 | 0.145349 | 0.375 | 0.625 | 0.0387597 |
| `full_low` | `status` | 2580 | 0.020155 | 0.125 | 0.375 | 0.0728682 |
| `high_full_tail_weight` | `delta` | 27640 | 0.150886 | 0.25 | 0.75 | 0.0138929 |
| `high_full_tail_weight` | `full` | 27640 | 0.185872 | 0.375 | 0.75 | 0.0144718 |
| `high_full_tail_weight` | `phase` | 27640 | 0.171997 | 0.375 | 0.75 | 0.00318379 |
| `high_full_tail_weight` | `status` | 27640 | 0.120152 | 0.25 | 0.75 | 0.0115774 |
| `phase_low` | `delta` | 1628 | 0.110872 | 0.25 | 0.5 | 0.235872 |
| `phase_low` | `full` | 1628 | 0.347052 | 0.625 | 0.75 | 0.316953 |
| `phase_low` | `phase` | 1628 | 0.226351 | 0.375 | 0.625 | 0.0589681 |
| `phase_low` | `status` | 1628 | 0.031941 | 0.125 | 0.375 | 0.115479 |
| `status_exact` | `delta` | 104112 | 0.00903834 | 0.125 | 0.375 | 0.0189027 |
| `status_exact` | `full` | 104112 | 0.0114108 | 0.125 | 0.75 | 0.0221684 |
| `status_exact` | `phase` | 104112 | 0.00196423 | 0 | 0.375 | 0.000499462 |
| `status_exact` | `status` | 104112 | 0 | 0 | 0 | 0 |

## Worst `full` Drifts

| T | r | h | TV | changed | dominant A | dominant B | phase maj | full maj | full tail weight |
|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| 15 | 23209 | 0 | 0.75 | 0 | `terminal` | `terminal` | 0.625 | 0.625 | 1 |
| 15 | 23209 | 1 | 0.75 | 0 | `terminal` | `terminal` | 0.625 | 0.625 | 1 |
| 15 | 23209 | 2 | 0.75 | 0 | `terminal` | `terminal` | 0.625 | 0.625 | 1 |
| 15 | 23209 | 3 | 0.75 | 0 | `terminal` | `terminal` | 0.625 | 0.625 | 1 |
| 15 | 3411 | 0 | 0.75 | 1 | `return|0|1|1|2` | `return|1|1|1|2` | 0.25 | 0.1875 | 0.75 |
| 15 | 3411 | 1 | 0.75 | 1 | `return|0|1|2|2` | `return|1|1|2|2` | 0.25 | 0.1875 | 0.75 |
| 15 | 3411 | 2 | 0.75 | 1 | `return|0|1|3|2` | `return|1|1|3|2` | 0.25 | 0.1875 | 0.75 |
| 15 | 3411 | 3 | 0.75 | 1 | `return|0|1|0|2` | `return|1|1|0|2` | 0.25 | 0.1875 | 0.75 |
| 15 | 393 | 0 | 0.625 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 393 | 1 | 0.625 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 393 | 2 | 0.625 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 393 | 3 | 0.625 | 0 | `terminal` | `terminal` | 0.375 | 0.375 | 1 |
| 15 | 2689 | 0 | 0.625 | 0 | `return|0|1|1|1` | `return|0|1|1|1` | 0.25 | 0.25 | 0.79085 |
| 15 | 2689 | 1 | 0.625 | 0 | `return|0|1|2|1` | `return|0|1|2|1` | 0.25 | 0.25 | 0.79085 |
| 15 | 2689 | 2 | 0.625 | 0 | `return|0|1|3|1` | `return|0|1|3|1` | 0.25 | 0.25 | 0.79085 |
| 15 | 2689 | 3 | 0.625 | 0 | `return|0|1|0|1` | `return|0|1|0|1` | 0.25 | 0.25 | 0.79085 |

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
