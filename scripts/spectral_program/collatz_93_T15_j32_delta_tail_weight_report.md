# Delta Tail Weight Diagnostic

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- j_count: `32`
- include boundary: `False`

## Aggregate

- groups: `131072`
- h values: `0, 1, 2, 3`
- groups with nonzero return weight: `44536`
- nonzero-return group fraction: `0.339783`
- total sample count: `4194300`
- terminal count fraction: `0.895062`
- return count: `440140`
- weighted return mass: `128432.050293`
- max delta observed: `13`

Here `weight_sum` is the weight already emitted by script 88, i.e.
the return contribution normalized by `2^{-delta}`.  Terminal rows
have zero return weight in this diagnostic.

## Delta Weight Distribution

| delta | count fraction | weight fraction | cumulative weight fraction |
|---:|---:|---:|---:|
| 0 | 0.027773 | 0.0951787 | 0.0951787 |
| 1 | 0.268396 | 0.459901 | 0.55508 |
| 2 | 0.412614 | 0.35351 | 0.908589 |
| 3 | 0.167592 | 0.0717928 | 0.980382 |
| 4 | 0.0726133 | 0.015553 | 0.995935 |
| 5 | 0.0300632 | 0.0032196 | 0.999155 |
| 6 | 0.0127414 | 0.000682267 | 0.999837 |
| 7 | 0.00478939 | 0.000128229 | 0.999965 |
| 8 | 0.00211751 | 2.83467e-05 | 0.999994 |
| 9 | 0.000727041 | 4.86639e-06 | 0.999999 |
| 10 | 0.000372609 | 1.24701e-06 | 1 |
| 11 | 9.99682e-05 | 1.67282e-07 | 1 |
| 12 | 7.27041e-05 | 6.08298e-08 | 1 |
| 13 | 2.72641e-05 | 1.14056e-08 | 1 |

## Tail Thresholds

| keep delta <= L | tail count frac | tail weight frac | group tail mean | group tail p95 | group tail max | groups with tail |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.972227 | 0.904821 | 0.89583 | 1 | 1 | 42708 |
| 1 | 0.703831 | 0.44492 | 0.579079 | 1 | 1 | 37324 |
| 2 | 0.291216 | 0.0914106 | 0.280045 | 1 | 1 | 23680 |
| 3 | 0.123624 | 0.0196178 | 0.118269 | 1 | 1 | 15132 |
| 4 | 0.051011 | 0.0040648 | 0.0427772 | 0.2 | 1 | 8592 |
| 5 | 0.0209479 | 0.000845196 | 0.0148622 | 0.0379747 | 1 | 4704 |
| 6 | 0.00820648 | 0.000162929 | 0.00438731 | 0.000589275 | 1 | 2248 |
| 7 | 0.00341709 | 3.46996e-05 | 0.00153788 | 0 | 1 | 1056 |
| 8 | 0.00129959 | 6.35292e-06 | 0.000127367 | 0 | 0.2 | 468 |
| 13 | 0 | 0 | 0 | 0 | 0 | 0 |

## Worst Groups for L = 4

| T | r | h | tail frac | return weight | phase maj | delta maj | full maj | delta weights |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 15 | 101 | 0 | 1 | 0.00390625 | 0.96875 | 0.96875 | 0.96875 | `8:0.00390625` |
| 15 | 101 | 1 | 1 | 0.00390625 | 0.96875 | 0.96875 | 0.96875 | `8:0.00390625` |
| 15 | 101 | 2 | 1 | 0.00390625 | 0.96875 | 0.96875 | 0.96875 | `8:0.00390625` |
| 15 | 101 | 3 | 1 | 0.00390625 | 0.96875 | 0.96875 | 0.96875 | `8:0.00390625` |
| 15 | 255 | 0 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 255 | 1 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 255 | 2 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 255 | 3 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 379 | 0 | 1 | 0.03125 | 0.96875 | 0.96875 | 0.96875 | `5:0.03125` |
| 15 | 379 | 1 | 1 | 0.03125 | 0.96875 | 0.96875 | 0.96875 | `5:0.03125` |
| 15 | 379 | 2 | 1 | 0.03125 | 0.96875 | 0.96875 | 0.96875 | `5:0.03125` |
| 15 | 379 | 3 | 1 | 0.03125 | 0.96875 | 0.96875 | 0.96875 | `5:0.03125` |
| 15 | 381 | 0 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 381 | 1 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 381 | 2 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |
| 15 | 381 | 3 | 1 | 0.015625 | 0.96875 | 0.96875 | 0.96875 | `6:0.015625` |

## Interpretation

A small global weighted delta tail would support a Banach model with
an explicit return-exponent tail weight.  It would not by itself
identify a canonical infinite operator, prove compactness, prove
Lasota-Yorke, or justify the finite matrices as exact projections.

If the group-level tail p95 or max remains large at feasible L, then
a finite labelled quotient is not resolving the obstruction uniformly;
one should treat the labelled countable-state or finite-rank fallback
branches as the safer mathematical alternatives.
