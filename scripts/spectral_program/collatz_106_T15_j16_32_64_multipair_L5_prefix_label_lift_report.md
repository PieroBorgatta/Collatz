# Prefix Label-Lift Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- delta cutoff: `5`
- include boundary: `False`
- include mixed source cells: `False`
- prefix counts: `16, 32, 64`
- prefix windows used: `393192`
- skipped mixed-source windows: `24`
- skipped boundary windows: `0`

`component_l1` is the substochastic row `L1` prefix drift after
collapsing return destinations to `good/bad`.  `label_l1` is the
same drift on retained full return signatures.  `label_excess` is
the nonnegative difference `label_l1 - component_l1` and is the
finite proxy for `ComponentLabelLift`.

All summary means are uniform over retained source cells/prefix
pairs.  By default this excludes boundary rows and mixed-source
cells, so the implicit source weight is finite counting measure,
not a proved limiting Haar measure.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `component_l1` | 262128 | 0.0042351462 | 0.015625 | 0.0234375 | 0.0390625 | 0.125 |
| `all` | `label_l1` | 262128 | 0.0075392035 | 0.024414062 | 0.038085938 | 0.0703125 | 0.34375 |
| `all` | `label_excess` | 262128 | 0.0033040573 | 0.01171875 | 0.017578125 | 0.046875 | 0.28125 |
| `all` | `retained_row_sum_abs_diff` | 262128 | 0.0032317599 | 0.01171875 | 0.015625 | 0.03125 | 0.09375 |
| `all` | `tail_row_sum_abs_diff` | 262128 | 1.3091738e-05 | 0 | 0 | 0.00048828125 | 0.0014648438 |
| `good` | `component_l1` | 180208 | 0.003184482 | 0.01171875 | 0.01953125 | 0.0390625 | 0.1015625 |
| `good` | `label_l1` | 180208 | 0.0057869869 | 0.0234375 | 0.033203125 | 0.0703125 | 0.34375 |
| `good` | `label_excess` | 180208 | 0.0026025048 | 0.0078125 | 0.015625 | 0.05078125 | 0.28125 |
| `good` | `retained_row_sum_abs_diff` | 180208 | 0.002351482 | 0.0078125 | 0.015625 | 0.03125 | 0.09375 |
| `good` | `tail_row_sum_abs_diff` | 180208 | 6.9597565e-06 | 0 | 0 | 0.00024414062 | 0.0014648438 |
| `bad` | `component_l1` | 81920 | 0.006546402 | 0.017578125 | 0.02734375 | 0.04296875 | 0.125 |
| `bad` | `label_l1` | 81920 | 0.011393738 | 0.03125 | 0.046875 | 0.066035156 | 0.34375 |
| `bad` | `label_excess` | 81920 | 0.0048473358 | 0.015625 | 0.023486328 | 0.046875 | 0.28125 |
| `bad` | `retained_row_sum_abs_diff` | 81920 | 0.0051681995 | 0.015625 | 0.020507812 | 0.034575195 | 0.0859375 |
| `bad` | `tail_row_sum_abs_diff` | 81920 | 2.6580901e-05 | 0 | 0.00024414062 | 0.00048828125 | 0.0014648438 |

## By Prefix Pair

| pair | source | metric | count | mean | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `16->32` | `all` | `component_l1` | 131064 | 0.0047644305 | 0.028320312 | 0.046875 | 0.125 |
| `16->32` | `all` | `label_l1` | 131064 | 0.008195066 | 0.046875 | 0.078125 | 0.34375 |
| `16->32` | `all` | `label_excess` | 131064 | 0.0034306355 | 0.0234375 | 0.0625 | 0.28125 |
| `16->32` | `good` | `component_l1` | 90104 | 0.0035874777 | 0.0234375 | 0.046875 | 0.1015625 |
| `16->32` | `good` | `label_l1` | 90104 | 0.0062911244 | 0.0390625 | 0.078125 | 0.34375 |
| `16->32` | `good` | `label_excess` | 90104 | 0.0027036466 | 0.015625 | 0.0625 | 0.28125 |
| `16->32` | `bad` | `component_l1` | 40960 | 0.0073534966 | 0.03125 | 0.046875 | 0.125 |
| `16->32` | `bad` | `label_l1` | 40960 | 0.012383366 | 0.046875 | 0.0703125 | 0.34375 |
| `16->32` | `bad` | `label_excess` | 40960 | 0.0050298691 | 0.03125 | 0.0546875 | 0.28125 |
| `32->64` | `all` | `component_l1` | 131064 | 0.0037058619 | 0.01953125 | 0.03125 | 0.0703125 |
| `32->64` | `all` | `label_l1` | 131064 | 0.006883341 | 0.032226562 | 0.0625 | 0.1953125 |
| `32->64` | `all` | `label_excess` | 131064 | 0.0031774791 | 0.015625 | 0.0390625 | 0.171875 |
| `32->64` | `good` | `component_l1` | 90104 | 0.0027814864 | 0.017089844 | 0.03125 | 0.0703125 |
| `32->64` | `good` | `label_l1` | 90104 | 0.0052828494 | 0.03125 | 0.0625 | 0.1953125 |
| `32->64` | `good` | `label_excess` | 90104 | 0.002501363 | 0.015625 | 0.0390625 | 0.171875 |
| `32->64` | `bad` | `component_l1` | 40960 | 0.0057393074 | 0.021484375 | 0.033203125 | 0.064453125 |
| `32->64` | `bad` | `label_l1` | 40960 | 0.01040411 | 0.03515625 | 0.0625 | 0.15039062 |
| `32->64` | `bad` | `label_excess` | 40960 | 0.0046648026 | 0.01953125 | 0.0390625 | 0.125 |

## Worst Label-Excess Rows

| T | r | h | source | pair | component L1 | label L1 | label excess | retained row diff | tail row diff |
|---:|---:|---:|---|---|---:|---:|---:|---:|---:|
| 15 | 28571 | 0 | `bad` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 28571 | 1 | `bad` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 28571 | 2 | `bad` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 28571 | 3 | `bad` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 30046 | 0 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 30046 | 1 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 30046 | 2 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 30046 | 3 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 2592 | 0 | `good` | `16->32` | 0.03125 | 0.3125 | 0.28125 | 0.03125 | 0 |
| 15 | 2592 | 1 | `good` | `16->32` | 0.03125 | 0.3125 | 0.28125 | 0.03125 | 0 |
| 15 | 2592 | 2 | `good` | `16->32` | 0.03125 | 0.3125 | 0.28125 | 0.03125 | 0 |
| 15 | 2592 | 3 | `good` | `16->32` | 0.03125 | 0.3125 | 0.28125 | 0.03125 | 0 |
| 15 | 23257 | 0 | `good` | `16->32` | 0.046875 | 0.296875 | 0.25 | 0.015625 | 0 |
| 15 | 23257 | 1 | `good` | `16->32` | 0.046875 | 0.296875 | 0.25 | 0.015625 | 0 |
| 15 | 23257 | 2 | `good` | `16->32` | 0.046875 | 0.296875 | 0.25 | 0.015625 | 0 |
| 15 | 23257 | 3 | `good` | `16->32` | 0.046875 | 0.296875 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 0 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 1 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 2 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 3 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 31744 | 0 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 31744 | 1 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 31744 | 2 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 31744 | 3 | `good` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 30970 | 0 | `good` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.046875 | 0 |

## Interpretation Guardrail

Small `component_l1` with large `label_excess` means the good/bad
kernel is hiding retained-label drift.  Small `label_excess` would
support, but not prove, lifting the component kernel to retained
labels in a weak averaged norm.  This diagnostic does not define
an infinite operator and does not imply a spectral gap.
