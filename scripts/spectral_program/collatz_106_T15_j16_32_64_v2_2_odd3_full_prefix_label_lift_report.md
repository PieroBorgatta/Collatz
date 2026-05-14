# Prefix Label-Lift Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `v2_2_odd3`
- bad convention: `src_v2 == 2 and src_odd == 3`
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
| `all` | `component_l1` | 262128 | 0.0035912445 | 0.013671875 | 0.01953125 | 0.033935547 | 0.109375 |
| `all` | `label_l1` | 262128 | 0.0075584849 | 0.024414062 | 0.038085938 | 0.0703125 | 0.34375 |
| `all` | `label_excess` | 262128 | 0.0039672405 | 0.015625 | 0.0234375 | 0.0625 | 0.28125 |
| `all` | `retained_row_sum_abs_diff` | 262128 | 0.0032317275 | 0.01171875 | 0.015625 | 0.03125 | 0.09375 |
| `all` | `tail_row_sum_abs_diff` | 262128 | 0 | 0 | 0 | 0 | 0 |
| `good` | `component_l1` | 245744 | 0.003428975 | 0.013183594 | 0.01953125 | 0.034179688 | 0.109375 |
| `good` | `label_l1` | 245744 | 0.0070186511 | 0.0234375 | 0.03515625 | 0.0703125 | 0.34375 |
| `good` | `label_excess` | 245744 | 0.0035896761 | 0.01171875 | 0.01953125 | 0.0625 | 0.28125 |
| `good` | `retained_row_sum_abs_diff` | 245744 | 0.0030657983 | 0.01171875 | 0.015625 | 0.03125 | 0.09375 |
| `good` | `tail_row_sum_abs_diff` | 245744 | 0 | 0 | 0 | 0 | 0 |
| `bad` | `component_l1` | 16384 | 0.0060251281 | 0.015625 | 0.015625 | 0.03125 | 0.078125 |
| `bad` | `label_l1` | 16384 | 0.015655465 | 0.046875 | 0.046875 | 0.0625 | 0.22070312 |
| `bad` | `label_excess` | 16384 | 0.0096303374 | 0.03125 | 0.03125 | 0.046875 | 0.21875 |
| `bad` | `retained_row_sum_abs_diff` | 16384 | 0.0057205036 | 0.015625 | 0.015625 | 0.03125 | 0.071289062 |
| `bad` | `tail_row_sum_abs_diff` | 16384 | 0 | 0 | 0 | 0 | 0 |

## By Prefix Pair

| pair | source | metric | count | mean | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `16->32` | `all` | `component_l1` | 131064 | 0.0041106006 | 0.0234375 | 0.0390625 | 0.109375 |
| `16->32` | `all` | `label_l1` | 131064 | 0.0082151939 | 0.046875 | 0.078125 | 0.34375 |
| `16->32` | `all` | `label_excess` | 131064 | 0.0041045933 | 0.03125 | 0.0625 | 0.28125 |
| `16->32` | `good` | `component_l1` | 122872 | 0.0038912171 | 0.0234375 | 0.0390625 | 0.109375 |
| `16->32` | `good` | `label_l1` | 122872 | 0.0075091412 | 0.0390625 | 0.078125 | 0.34375 |
| `16->32` | `good` | `label_excess` | 122872 | 0.0036179241 | 0.0234375 | 0.0625 | 0.28125 |
| `16->32` | `bad` | `component_l1` | 8192 | 0.0074011385 | 0.01953125 | 0.039916992 | 0.078125 |
| `16->32` | `bad` | `label_l1` | 8192 | 0.018805295 | 0.046875 | 0.06640625 | 0.22070312 |
| `16->32` | `bad` | `label_excess` | 8192 | 0.011404157 | 0.03125 | 0.0625 | 0.21875 |
| `32->64` | `all` | `component_l1` | 131064 | 0.0030718884 | 0.015625 | 0.025512695 | 0.0546875 |
| `32->64` | `all` | `label_l1` | 131064 | 0.006901776 | 0.032226562 | 0.0625 | 0.1953125 |
| `32->64` | `all` | `label_excess` | 131064 | 0.0038298876 | 0.021484375 | 0.048828125 | 0.171875 |
| `32->64` | `good` | `component_l1` | 122872 | 0.0029667329 | 0.015625 | 0.02545166 | 0.0546875 |
| `32->64` | `good` | `label_l1` | 122872 | 0.006528161 | 0.03125 | 0.0625 | 0.1953125 |
| `32->64` | `good` | `label_excess` | 122872 | 0.0035614281 | 0.01953125 | 0.05078125 | 0.171875 |
| `32->64` | `bad` | `component_l1` | 8192 | 0.0046491176 | 0.015625 | 0.026184082 | 0.0390625 |
| `32->64` | `bad` | `label_l1` | 8192 | 0.012505636 | 0.03515625 | 0.05859375 | 0.1328125 |
| `32->64` | `bad` | `label_excess` | 8192 | 0.007856518 | 0.0234375 | 0.0390625 | 0.125 |

## Worst Label-Excess Rows

| T | r | h | source | pair | component L1 | label L1 | label excess | retained row diff | tail row diff |
|---:|---:|---:|---|---|---:|---:|---:|---:|---:|
| 15 | 28571 | 0 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 28571 | 1 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 28571 | 2 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
| 15 | 28571 | 3 | `good` | `16->32` | 0.0625 | 0.34375 | 0.28125 | 0.03125 | 0 |
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
