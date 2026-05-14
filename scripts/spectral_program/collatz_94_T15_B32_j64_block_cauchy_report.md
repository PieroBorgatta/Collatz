# Block-Cauchy Drift Summary

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- block drift file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_block_drift.csv`
- T filter: `15`
- active T values: `15`
- final prefix j_count: `64`
- include boundary: `False`
- block sizes: `32`
- adjacent block pairs: `0->32`

## Aggregate By Signature Level

| level | count | mean TV | p90 | p95 | p99 | max | dominant flip frac |
|---|---:|---:|---:|---:|---:|---:|---:|
| `delta` | 131072 | 0.0224647 | 0.09375 | 0.09375 | 0.15625 | 0.28125 | 0.00863647 |
| `full` | 131072 | 0.0310087 | 0.125 | 0.15625 | 0.21875 | 0.375 | 0.011322 |
| `phase` | 131072 | 0.0230875 | 0.09375 | 0.125 | 0.15625 | 0.28125 | 0.00128174 |
| `status` | 131072 | 0.0128621 | 0.0625 | 0.0625 | 0.125 | 0.25 | 0 |

## Selected Classes

| class | level | count | mean TV | p95 | max | dominant flip frac |
|---|---|---:|---:|---:|---:|---:|
| `all` | `delta` | 131072 | 0.0224647 | 0.09375 | 0.28125 | 0.00863647 |
| `all` | `full` | 131072 | 0.0310087 | 0.15625 | 0.375 | 0.011322 |
| `all` | `phase` | 131072 | 0.0230875 | 0.125 | 0.28125 | 0.00128174 |
| `all` | `status` | 131072 | 0.0128621 | 0.0625 | 0.25 | 0 |
| `full_low` | `delta` | 1660 | 0.0490211 | 0.09375 | 0.28125 | 0.0963855 |
| `full_low` | `full` | 1660 | 0.153765 | 0.28125 | 0.375 | 0.308434 |
| `full_low` | `phase` | 1660 | 0.0716867 | 0.15625 | 0.21875 | 0.101205 |
| `full_low` | `status` | 1660 | 0.00956325 | 0.0625 | 0.15625 | 0 |
| `high_full_tail_weight` | `delta` | 39944 | 0.0647405 | 0.125 | 0.28125 | 0.00330463 |
| `high_full_tail_weight` | `full` | 39944 | 0.0923042 | 0.1875 | 0.375 | 0.00981374 |
| `high_full_tail_weight` | `phase` | 39944 | 0.0753429 | 0.15625 | 0.28125 | 0.00260365 |
| `high_full_tail_weight` | `status` | 39944 | 0.0422056 | 0.09375 | 0.25 | 0 |
| `phase_low` | `delta` | 1576 | 0.0491751 | 0.09375 | 0.28125 | 0.0862944 |
| `phase_low` | `full` | 1576 | 0.158074 | 0.28125 | 0.375 | 0.307107 |
| `phase_low` | `phase` | 1576 | 0.073842 | 0.15625 | 0.21875 | 0.0939086 |
| `phase_low` | `status` | 1576 | 0.010073 | 0.0625 | 0.15625 | 0 |
| `status_exact` | `delta` | 91824 | 0.00420506 | 0.03125 | 0.125 | 0.0113696 |
| `status_exact` | `full` | 91824 | 0.00544248 | 0.03125 | 0.3125 | 0.0161614 |
| `status_exact` | `phase` | 91824 | 0.000676566 | 0 | 0.09375 | 0.00182959 |
| `status_exact` | `status` | 91824 | 0 | 0 | 0 | 0 |

## Worst `full` Drifts

| T | r | h | TV | changed | dominant A | dominant B | phase maj | full maj | full tail weight |
|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| 15 | 6101 | 0 | 0.375 | 0 | `terminal` | `terminal` | 0.390625 | 0.390625 | 1 |
| 15 | 6101 | 1 | 0.375 | 0 | `terminal` | `terminal` | 0.390625 | 0.390625 | 1 |
| 15 | 6101 | 2 | 0.375 | 0 | `terminal` | `terminal` | 0.390625 | 0.390625 | 1 |
| 15 | 6101 | 3 | 0.375 | 0 | `terminal` | `terminal` | 0.390625 | 0.390625 | 1 |
| 15 | 16423 | 0 | 0.34375 | 0 | `terminal` | `terminal` | 0.609375 | 0.609375 | 1 |
| 15 | 16423 | 1 | 0.34375 | 0 | `terminal` | `terminal` | 0.609375 | 0.609375 | 1 |
| 15 | 16423 | 2 | 0.34375 | 0 | `terminal` | `terminal` | 0.609375 | 0.609375 | 1 |
| 15 | 16423 | 3 | 0.34375 | 0 | `terminal` | `terminal` | 0.609375 | 0.609375 | 1 |
| 15 | 16751 | 0 | 0.34375 | 0 | `terminal` | `terminal` | 0.734375 | 0.734375 | 1 |
| 15 | 16751 | 1 | 0.34375 | 0 | `terminal` | `terminal` | 0.734375 | 0.734375 | 1 |
| 15 | 16751 | 2 | 0.34375 | 0 | `terminal` | `terminal` | 0.734375 | 0.734375 | 1 |
| 15 | 16751 | 3 | 0.34375 | 0 | `terminal` | `terminal` | 0.734375 | 0.734375 | 1 |
| 15 | 22831 | 0 | 0.34375 | 0 | `terminal` | `terminal` | 0.328125 | 0.328125 | 1 |
| 15 | 22831 | 1 | 0.34375 | 0 | `terminal` | `terminal` | 0.328125 | 0.328125 | 1 |
| 15 | 22831 | 2 | 0.34375 | 0 | `terminal` | `terminal` | 0.328125 | 0.328125 | 1 |
| 15 | 22831 | 3 | 0.34375 | 0 | `terminal` | `terminal` | 0.328125 | 0.328125 | 1 |

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
