# Delta Tail Weight Diagnostic

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T filter: `16`
- active T values: `16`
- j_count: `8`
- include boundary: `False`

## Aggregate

- groups: `262144`
- h values: `0, 1, 2, 3`
- groups with nonzero return weight: `55476`
- nonzero-return group fraction: `0.211624`
- total sample count: `2097148`
- terminal count fraction: `0.895004`
- return count: `220192`
- weighted return mass: `64130.3369141`
- max delta observed: `12`

Here `weight_sum` is the weight already emitted by script 88, i.e.
the return contribution normalized by `2^{-delta}`.  Terminal rows
have zero return weight in this diagnostic.

## Delta Weight Distribution

| delta | count fraction | weight fraction | cumulative weight fraction |
|---:|---:|---:|---:|
| 0 | 0.0274306 | 0.0941832 | 0.0941832 |
| 1 | 0.267566 | 0.459346 | 0.553529 |
| 2 | 0.413675 | 0.355089 | 0.908618 |
| 3 | 0.167 | 0.0716743 | 0.980293 |
| 4 | 0.0726275 | 0.0155854 | 0.995878 |
| 5 | 0.0303735 | 0.00325899 | 0.999137 |
| 6 | 0.0129523 | 0.000694874 | 0.999832 |
| 7 | 0.00492298 | 0.000132055 | 0.999964 |
| 8 | 0.00225258 | 3.02119e-05 | 0.999994 |
| 9 | 0.000635809 | 4.26378e-06 | 0.999999 |
| 10 | 0.000381485 | 1.27913e-06 | 1 |
| 11 | 5.44979e-05 | 9.13667e-08 | 1 |
| 12 | 0.000127162 | 1.06594e-07 | 1 |

## Tail Thresholds

| keep delta <= L | tail count frac | tail weight frac | group tail mean | group tail p95 | group tail max | groups with tail |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.972569 | 0.905817 | 0.938844 | 1 | 1 | 53284 |
| 1 | 0.705003 | 0.446471 | 0.66213 | 1 | 1 | 45980 |
| 2 | 0.291328 | 0.0913817 | 0.342024 | 1 | 1 | 24228 |
| 3 | 0.124328 | 0.0197073 | 0.16919 | 1 | 1 | 13344 |
| 4 | 0.0517003 | 0.00412187 | 0.0773761 | 1 | 1 | 6824 |
| 5 | 0.0213268 | 0.000862882 | 0.0349716 | 0.047619 | 1 | 3360 |
| 6 | 0.00837451 | 0.000168008 | 0.0131177 | 0 | 1 | 1452 |
| 7 | 0.00345153 | 3.59528e-05 | 0.00500707 | 0 | 1 | 644 |
| 8 | 0.00119895 | 5.74087e-06 | 0.00157198 | 0 | 1 | 240 |
| 12 | 0 | 0 | 0 | 0 | 0 | 0 |

## Worst Groups for L = 4

| T | r | h | tail frac | return weight | phase maj | delta maj | full maj | delta weights |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 16 | 127 | 0 | 1 | 0.0234375 | 0.75 | 0.75 | 0.75 | `6:0.015625, 7:0.0078125` |
| 16 | 127 | 1 | 1 | 0.0234375 | 0.75 | 0.75 | 0.75 | `6:0.015625, 7:0.0078125` |
| 16 | 127 | 2 | 1 | 0.0234375 | 0.75 | 0.75 | 0.75 | `6:0.015625, 7:0.0078125` |
| 16 | 127 | 3 | 1 | 0.0234375 | 0.75 | 0.75 | 0.75 | `6:0.015625, 7:0.0078125` |
| 16 | 255 | 0 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 255 | 1 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 255 | 2 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 255 | 3 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 327 | 0 | 1 | 0.0546875 | 0.625 | 0.625 | 0.625 | `5:0.03125, 6:0.015625, 7:0.0078125` |
| 16 | 327 | 1 | 1 | 0.0546875 | 0.625 | 0.625 | 0.625 | `5:0.03125, 6:0.015625, 7:0.0078125` |
| 16 | 327 | 2 | 1 | 0.0546875 | 0.625 | 0.625 | 0.625 | `5:0.03125, 6:0.015625, 7:0.0078125` |
| 16 | 327 | 3 | 1 | 0.0546875 | 0.625 | 0.625 | 0.625 | `5:0.03125, 6:0.015625, 7:0.0078125` |
| 16 | 367 | 0 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 367 | 1 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 367 | 2 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |
| 16 | 367 | 3 | 1 | 0.015625 | 0.875 | 0.875 | 0.875 | `6:0.015625` |

## Interpretation

A small global weighted delta tail would support a Banach model with
an explicit return-exponent tail weight.  It would not by itself
identify a canonical infinite operator, prove compactness, prove
Lasota-Yorke, or justify the finite matrices as exact projections.

If the group-level tail p95 or max remains large at feasible L, then
a finite labelled quotient is not resolving the obstruction uniformly;
one should treat the labelled countable-state or finite-rank fallback
branches as the safer mathematical alternatives.
