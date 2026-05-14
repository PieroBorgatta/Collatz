# Phase 10 Error-Budget Summary

Status: finite diagnostic output, not a theorem.

## Inputs

- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T: `15`
- prefix j_count for tails: `16`
- block size for TV: `8`
- cutoffs: `2,3,4,5,8`
- block starts: `0, 8`
- adjacent pairs: `0->8`

## DeltaTail Terms

| L | global tail | local mean | local p95 | local p99 | local max | groups with tail | groups |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.0913817 | 0.321478 | 1 | 1 | 1 | 17988 | 37340 |
| 3 | 0.0197073 | 0.150476 | 1 | 1 | 1 | 10732 | 37340 |
| 4 | 0.00412187 | 0.064389 | 0.800156 | 1 | 1 | 5720 | 37340 |
| 5 | 0.000862882 | 0.026621 | 0.047619 | 1 | 1 | 2944 | 37340 |
| 8 | 5.74087e-06 | 0.000591168 | 0 | 0 | 1 | 228 | 37340 |

## Block Terms

| term | parameter | mean | p95 | p99 | max | weak L1 proxy | sup proxy | extra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `A_phase_block` | `block=8` | 0.0365917 | 0.25 | 0.375 | 0.75 | 0.0731834 | 1.5 | 131068 samples |
| `A_label_tv` | `clip_2` | 0.0443052 | 0.25 | 0.375 | 0.75 | 0.0886105 | 1.5 | 131068 samples |
| `A_label_tv` | `clip_3` | 0.0455184 | 0.25 | 0.375 | 0.75 | 0.0910367 | 1.5 | 131068 samples |
| `A_label_tv` | `clip_4` | 0.0459609 | 0.25 | 0.375 | 0.75 | 0.0919218 | 1.5 | 131068 samples |
| `A_label_tv` | `clip_5` | 0.046144 | 0.25 | 0.375 | 0.75 | 0.092288 | 1.5 | 131068 samples |
| `A_label_tv` | `clip_8` | 0.0462241 | 0.25 | 0.375 | 0.75 | 0.0924482 | 1.5 | 131068 samples |
| `A_label_tv` | `full` | 0.0462241 | 0.25 | 0.375 | 0.75 | 0.0924482 | 1.5 | 131068 samples |
| `A_label_bounded` | `clip_2` | 0.00771355 | 0.125 | 0.125 | 0.5 | 0.0154271 | 1 | positive 0.0512406 |
| `A_label_bounded` | `clip_3` | 0.00892666 | 0.125 | 0.25 | 0.5 | 0.0178533 | 1 | positive 0.0594501 |
| `A_label_bounded` | `clip_4` | 0.00936918 | 0.125 | 0.25 | 0.5 | 0.0187384 | 1 | positive 0.0623798 |
| `A_label_bounded` | `clip_5` | 0.00955229 | 0.125 | 0.25 | 0.5 | 0.0191046 | 1 | positive 0.0634785 |
| `A_label_bounded` | `clip_8` | 0.0096324 | 0.125 | 0.25 | 0.5 | 0.0192648 | 1 | positive 0.0639668 |
| `A_label_bounded` | `full` | 0.0096324 | 0.125 | 0.25 | 0.5 | 0.0192648 | 1 | positive 0.0639668 |

## Boundary Term

- complete groups: `131068`
- skipped incomplete groups: `4`
- total groups seen in block distributions: `131072`

## Interpretation

These numbers are finite proxies for the named error-budget terms.
`weak L1 proxy` is `2 * mean TV`, motivated by the finite row-TV
bridge for bounded observables under uniform source-cell averaging.
`sup proxy` is `2 * max TV`.  These are still not operator-norm
bounds for the infinite problem: p95 values require a separate
exceptional-mass argument, and no projection to an infinite operator
is implied.
