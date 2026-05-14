# Phase 10 Error-Budget Summary

Status: finite diagnostic output, not a theorem.

## Inputs

- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T: `15`
- prefix j_count for tails: `64`
- block size for TV: `32`
- cutoffs: `2,3,4,5,8`
- block starts: `0, 32`
- adjacent pairs: `0->32`

## DeltaTail Terms

| L | global tail | local mean | local p95 | local p99 | local max | groups with tail | groups |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.0912888 | 0.225698 | 1 | 1 | 1 | 29740 | 49628 |
| 3 | 0.0196166 | 0.0833406 | 0.479675 | 1 | 1 | 20348 | 49628 |
| 4 | 0.00406131 | 0.026659 | 0.120879 | 0.636364 | 1 | 12540 | 49628 |
| 5 | 0.000830424 | 0.00814013 | 0.027027 | 0.133333 | 1 | 7440 | 49628 |
| 8 | 6.82691e-06 | 7.49825e-05 | 0 | 0.00175747 | 0.0588235 | 912 | 49628 |

## Block Terms

| term | parameter | mean | p95 | p99 | max | weak L1 proxy | sup proxy | extra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `A_phase_block` | `block=32` | 0.0230853 | 0.125 | 0.15625 | 0.28125 | 0.0461707 | 0.5625 | 131068 samples |
| `A_label_tv` | `clip_2` | 0.0289039 | 0.125 | 0.1875 | 0.375 | 0.0578078 | 0.75 | 131068 samples |
| `A_label_tv` | `clip_3` | 0.0299863 | 0.125 | 0.1875 | 0.375 | 0.0599727 | 0.75 | 131068 samples |
| `A_label_tv` | `clip_4` | 0.0305662 | 0.15625 | 0.1875 | 0.375 | 0.0611324 | 0.75 | 131068 samples |
| `A_label_tv` | `clip_5` | 0.0308437 | 0.15625 | 0.21875 | 0.375 | 0.0616874 | 0.75 | 131068 samples |
| `A_label_tv` | `clip_8` | 0.031002 | 0.15625 | 0.21875 | 0.375 | 0.0620041 | 0.75 | 131068 samples |
| `A_label_tv` | `full` | 0.0310049 | 0.15625 | 0.21875 | 0.375 | 0.0620098 | 0.75 | 131068 samples |
| `A_label_bounded` | `clip_2` | 0.00581854 | 0.03125 | 0.09375 | 0.25 | 0.0116371 | 0.5 | positive 0.127384 |
| `A_label_bounded` | `clip_3` | 0.006901 | 0.03125 | 0.09375 | 0.25 | 0.013802 | 0.5 | positive 0.149693 |
| `A_label_bounded` | `clip_4` | 0.00748085 | 0.0625 | 0.09375 | 0.25 | 0.0149617 | 0.5 | positive 0.159215 |
| `A_label_bounded` | `clip_5` | 0.00775838 | 0.0625 | 0.09375 | 0.25 | 0.0155168 | 0.5 | positive 0.162603 |
| `A_label_bounded` | `clip_8` | 0.00791669 | 0.0625 | 0.09375 | 0.25 | 0.0158334 | 0.5 | positive 0.163945 |
| `A_label_bounded` | `full` | 0.00791955 | 0.0625 | 0.09375 | 0.25 | 0.0158391 | 0.5 | positive 0.163945 |

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
