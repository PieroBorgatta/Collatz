# Prefix Label-Lift Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_or_v2_2`
- bad convention: `src_odd == 3 or src_v2 == 2`
- delta cutoff: `none`
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
| `all` | `component_l1` | 262128 | 0.0044146893 | 0.015625 | 0.0234375 | 0.04296875 | 0.140625 |
| `all` | `label_l1` | 262128 | 0.0075584849 | 0.024414062 | 0.038085938 | 0.0703125 | 0.34375 |
| `all` | `label_excess` | 262128 | 0.0031437956 | 0.009765625 | 0.015625 | 0.046875 | 0.3125 |
| `all` | `retained_row_sum_abs_diff` | 262128 | 0.0032317275 | 0.01171875 | 0.015625 | 0.03125 | 0.09375 |
| `all` | `tail_row_sum_abs_diff` | 262128 | 0 | 0 | 0 | 0 | 0 |
| `good` | `component_l1` | 114680 | 0.0034139018 | 0.013671875 | 0.021484375 | 0.0390625 | 0.140625 |
| `good` | `label_l1` | 114680 | 0.0059003646 | 0.0234375 | 0.03515625 | 0.0703125 | 0.3125 |
| `good` | `label_excess` | 114680 | 0.0024864628 | 0.0078125 | 0.015625 | 0.046875 | 0.25 |
| `good` | `retained_row_sum_abs_diff` | 114680 | 0.0024283432 | 0.0078125 | 0.015625 | 0.03125 | 0.09375 |
| `good` | `tail_row_sum_abs_diff` | 114680 | 0 | 0 | 0 | 0 | 0 |
| `bad` | `component_l1` | 147448 | 0.0051930675 | 0.015625 | 0.0234375 | 0.043212891 | 0.12890625 |
| `bad` | `label_l1` | 147448 | 0.0088481141 | 0.027587891 | 0.0390625 | 0.067382812 | 0.34375 |
| `bad` | `label_excess` | 147448 | 0.0036550466 | 0.015625 | 0.01953125 | 0.046875 | 0.3125 |
| `bad` | `retained_row_sum_abs_diff` | 147448 | 0.0038565723 | 0.014648438 | 0.017578125 | 0.03125 | 0.0859375 |
| `bad` | `tail_row_sum_abs_diff` | 147448 | 0 | 0 | 0 | 0 | 0 |

## By Prefix Pair

| pair | source | metric | count | mean | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `16->32` | `all` | `component_l1` | 131064 | 0.0049826083 | 0.03125 | 0.046875 | 0.140625 |
| `16->32` | `all` | `label_l1` | 131064 | 0.0082151939 | 0.046875 | 0.078125 | 0.34375 |
| `16->32` | `all` | `label_excess` | 131064 | 0.0032325856 | 0.016113281 | 0.0625 | 0.3125 |
| `16->32` | `good` | `component_l1` | 57340 | 0.00391218 | 0.025390625 | 0.046875 | 0.140625 |
| `16->32` | `good` | `label_l1` | 57340 | 0.0064413847 | 0.0390625 | 0.078125 | 0.3125 |
| `16->32` | `good` | `label_excess` | 57340 | 0.0025292047 | 0.015625 | 0.05859375 | 0.25 |
| `16->32` | `bad` | `component_l1` | 73724 | 0.0058151507 | 0.03125 | 0.046875 | 0.12890625 |
| `16->32` | `bad` | `label_l1` | 73724 | 0.0095948019 | 0.046875 | 0.07421875 | 0.34375 |
| `16->32` | `bad` | `label_excess` | 73724 | 0.0037796511 | 0.025390625 | 0.0625 | 0.3125 |
| `32->64` | `all` | `component_l1` | 131064 | 0.0038467703 | 0.01953125 | 0.03125 | 0.077148438 |
| `32->64` | `all` | `label_l1` | 131064 | 0.006901776 | 0.032226562 | 0.0625 | 0.1953125 |
| `32->64` | `all` | `label_excess` | 131064 | 0.0030550056 | 0.015625 | 0.037109375 | 0.1875 |
| `32->64` | `good` | `component_l1` | 57340 | 0.0029156237 | 0.017578125 | 0.03125 | 0.0703125 |
| `32->64` | `good` | `label_l1` | 57340 | 0.0053593446 | 0.03125 | 0.0625 | 0.1796875 |
| `32->64` | `good` | `label_excess` | 57340 | 0.0024437209 | 0.015625 | 0.0390625 | 0.15625 |
| `32->64` | `bad` | `component_l1` | 73724 | 0.0045709843 | 0.020507812 | 0.031616211 | 0.077148438 |
| `32->64` | `bad` | `label_l1` | 73724 | 0.0081014262 | 0.033691406 | 0.0625 | 0.1953125 |
| `32->64` | `bad` | `label_excess` | 73724 | 0.003530442 | 0.017578125 | 0.035644531 | 0.1875 |

## Worst Label-Excess Rows

| T | r | h | source | pair | component L1 | label L1 | label excess | retained row diff | tail row diff |
|---:|---:|---:|---|---|---:|---:|---:|---:|---:|
| 15 | 30046 | 0 | `bad` | `16->32` | 0.03125 | 0.34375 | 0.3125 | 0.03125 | 0 |
| 15 | 30046 | 1 | `bad` | `16->32` | 0.03125 | 0.34375 | 0.3125 | 0.03125 | 0 |
| 15 | 30046 | 2 | `bad` | `16->32` | 0.03125 | 0.34375 | 0.3125 | 0.03125 | 0 |
| 15 | 30046 | 3 | `bad` | `16->32` | 0.03125 | 0.34375 | 0.3125 | 0.03125 | 0 |
| 15 | 2592 | 0 | `good` | `16->32` | 0.0625 | 0.3125 | 0.25 | 0.03125 | 0 |
| 15 | 2592 | 1 | `good` | `16->32` | 0.0625 | 0.3125 | 0.25 | 0.03125 | 0 |
| 15 | 2592 | 2 | `good` | `16->32` | 0.0625 | 0.3125 | 0.25 | 0.03125 | 0 |
| 15 | 2592 | 3 | `good` | `16->32` | 0.0625 | 0.3125 | 0.25 | 0.03125 | 0 |
| 15 | 26430 | 0 | `bad` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 1 | `bad` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 2 | `bad` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 26430 | 3 | `bad` | `16->32` | 0.015625 | 0.265625 | 0.25 | 0.015625 | 0 |
| 15 | 28571 | 0 | `bad` | `16->32` | 0.125 | 0.34375 | 0.21875 | 0.03125 | 0 |
| 15 | 28571 | 1 | `bad` | `16->32` | 0.125 | 0.34375 | 0.21875 | 0.03125 | 0 |
| 15 | 28571 | 2 | `bad` | `16->32` | 0.125 | 0.34375 | 0.21875 | 0.03125 | 0 |
| 15 | 28571 | 3 | `bad` | `16->32` | 0.125 | 0.34375 | 0.21875 | 0.03125 | 0 |
| 15 | 30970 | 0 | `good` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.046875 | 0 |
| 15 | 30970 | 1 | `good` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.046875 | 0 |
| 15 | 30970 | 2 | `good` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.046875 | 0 |
| 15 | 30970 | 3 | `good` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.046875 | 0 |
| 15 | 31744 | 0 | `bad` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.015625 | 0 |
| 15 | 31744 | 1 | `bad` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.015625 | 0 |
| 15 | 31744 | 2 | `bad` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.015625 | 0 |
| 15 | 31744 | 3 | `bad` | `16->32` | 0.046875 | 0.265625 | 0.21875 | 0.015625 | 0 |
| 15 | 5249 | 0 | `good` | `16->32` | 0.03125 | 0.25 | 0.21875 | 0.03125 | 0 |

## Interpretation Guardrail

Small `component_l1` with large `label_excess` means the good/bad
kernel is hiding retained-label drift.  Small `label_excess` would
support, but not prove, lifting the component kernel to retained
labels in a weak averaged norm.  This diagnostic does not define
an infinite operator and does not imply a spectral gap.
