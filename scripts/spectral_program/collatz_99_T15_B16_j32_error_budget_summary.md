# Phase 10 Error-Budget Summary

Status: finite diagnostic output, not a theorem.

## Inputs

- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T: `15`
- prefix j_count for tails: `32`
- block size for TV: `16`
- cutoffs: `2,3,4,5,8`
- block starts: `0, 16`
- adjacent pairs: `0->16`

## DeltaTail Terms

| L | global tail | local mean | local p95 | local p99 | local max | groups with tail | groups |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.0914106 | 0.280045 | 1 | 1 | 1 | 23680 | 44536 |
| 3 | 0.0196178 | 0.118269 | 1 | 1 | 1 | 15132 | 44536 |
| 4 | 0.0040648 | 0.0427772 | 0.2 | 1 | 1 | 8592 | 44536 |
| 5 | 0.000845196 | 0.0148622 | 0.0379747 | 0.428571 | 1 | 4704 | 44536 |
| 8 | 6.35292e-06 | 0.000127367 | 0 | 0.000589275 | 0.2 | 468 | 44536 |

## Block Terms

| term | parameter | mean | p95 | p99 | max | weak L1 proxy | sup proxy | extra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `A_phase_block` | `block=16` | 0.0294694 | 0.1875 | 0.25 | 0.4375 | 0.0589389 | 0.875 | 131068 samples |
| `A_label_tv` | `clip_2` | 0.0362655 | 0.1875 | 0.25 | 0.5 | 0.0725311 | 1 | 131068 samples |
| `A_label_tv` | `clip_3` | 0.0373623 | 0.1875 | 0.25 | 0.5 | 0.0747246 | 1 | 131068 samples |
| `A_label_tv` | `clip_4` | 0.0378315 | 0.1875 | 0.25 | 0.5 | 0.075663 | 1 | 131068 samples |
| `A_label_tv` | `clip_5` | 0.0379841 | 0.1875 | 0.25 | 0.5 | 0.0759682 | 1 | 131068 samples |
| `A_label_tv` | `clip_8` | 0.0380985 | 0.1875 | 0.25 | 0.5 | 0.0761971 | 1 | 131068 samples |
| `A_label_tv` | `full` | 0.0381024 | 0.1875 | 0.25 | 0.5 | 0.0762047 | 1 | 131068 samples |
| `A_label_bounded` | `clip_2` | 0.00679609 | 0.0625 | 0.125 | 0.375 | 0.0135922 | 0.75 | positive 0.0809351 |
| `A_label_bounded` | `clip_3` | 0.00789285 | 0.0625 | 0.125 | 0.375 | 0.0157857 | 0.75 | positive 0.0946074 |
| `A_label_bounded` | `clip_4` | 0.00836207 | 0.0625 | 0.125 | 0.375 | 0.0167241 | 0.75 | positive 0.099765 |
| `A_label_bounded` | `clip_5` | 0.00851466 | 0.0625 | 0.125 | 0.375 | 0.0170293 | 0.75 | positive 0.101627 |
| `A_label_bounded` | `clip_8` | 0.00862911 | 0.0625 | 0.125 | 0.375 | 0.0172582 | 0.75 | positive 0.102786 |
| `A_label_bounded` | `full` | 0.00863292 | 0.0625 | 0.125 | 0.375 | 0.0172658 | 0.75 | positive 0.102786 |

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
