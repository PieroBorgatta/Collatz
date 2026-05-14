# Prefix Label-Lift Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `v2_2_odd3`
- bad convention: `src_v2 == 2 and src_odd == 3`
- delta cutoff: `none`
- include boundary: `False`
- include mixed source cells: `False`
- prefix counts: `64, 128`
- prefix windows used: `262128`
- skipped mixed-source windows: `16`
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
| `all` | `component_l1` | 131064 | 0.0023125054 | 0.0080566406 | 0.01171875 | 0.017578125 | 0.037109375 |
| `all` | `label_l1` | 131064 | 0.0057602607 | 0.018249512 | 0.02444458 | 0.041381836 | 0.13671875 |
| `all` | `label_excess` | 131064 | 0.0034477554 | 0.01171875 | 0.016845703 | 0.033203125 | 0.109375 |
| `all` | `retained_row_sum_abs_diff` | 131064 | 0.0020254074 | 0.0073242188 | 0.010253906 | 0.015625 | 0.031738281 |
| `all` | `tail_row_sum_abs_diff` | 131064 | 0 | 0 | 0 | 0 | 0 |
| `good` | `component_l1` | 122872 | 0.0022346629 | 0.0082008362 | 0.01171875 | 0.017578125 | 0.037109375 |
| `good` | `label_l1` | 122872 | 0.0054969189 | 0.018310547 | 0.024597168 | 0.041503906 | 0.13671875 |
| `good` | `label_excess` | 122872 | 0.0032622561 | 0.01171875 | 0.017089844 | 0.033691406 | 0.109375 |
| `good` | `retained_row_sum_abs_diff` | 122872 | 0.0019440998 | 0.0075683594 | 0.010253906 | 0.015625 | 0.031738281 |
| `good` | `tail_row_sum_abs_diff` | 122872 | 0 | 0 | 0 | 0 | 0 |
| `bad` | `component_l1` | 8192 | 0.003480067 | 0.0068634033 | 0.009765625 | 0.017089844 | 0.030029297 |
| `bad` | `label_l1` | 8192 | 0.0097101307 | 0.017578125 | 0.0234375 | 0.038085938 | 0.10351562 |
| `bad` | `label_excess` | 8192 | 0.0062300637 | 0.01171875 | 0.015625 | 0.029296875 | 0.09375 |
| `bad` | `retained_row_sum_abs_diff` | 8192 | 0.0032449416 | 0.005859375 | 0.0084228516 | 0.015625 | 0.020141602 |
| `bad` | `tail_row_sum_abs_diff` | 8192 | 0 | 0 | 0 | 0 | 0 |

## By Prefix Pair

| pair | source | metric | count | mean | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `64->128` | `all` | `component_l1` | 131064 | 0.0023125054 | 0.01171875 | 0.017578125 | 0.037109375 |
| `64->128` | `all` | `label_l1` | 131064 | 0.0057602607 | 0.02444458 | 0.041381836 | 0.13671875 |
| `64->128` | `all` | `label_excess` | 131064 | 0.0034477554 | 0.016845703 | 0.033203125 | 0.109375 |
| `64->128` | `good` | `component_l1` | 122872 | 0.0022346629 | 0.01171875 | 0.017578125 | 0.037109375 |
| `64->128` | `good` | `label_l1` | 122872 | 0.0054969189 | 0.024597168 | 0.041503906 | 0.13671875 |
| `64->128` | `good` | `label_excess` | 122872 | 0.0032622561 | 0.017089844 | 0.033691406 | 0.109375 |
| `64->128` | `bad` | `component_l1` | 8192 | 0.003480067 | 0.009765625 | 0.017089844 | 0.030029297 |
| `64->128` | `bad` | `label_l1` | 8192 | 0.0097101307 | 0.0234375 | 0.038085938 | 0.10351562 |
| `64->128` | `bad` | `label_excess` | 8192 | 0.0062300637 | 0.015625 | 0.029296875 | 0.09375 |

## Worst Label-Excess Rows

| T | r | h | source | pair | component L1 | label L1 | label excess | retained row diff | tail row diff |
|---:|---:|---:|---|---|---:|---:|---:|---:|---:|
| 15 | 5249 | 0 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 5249 | 1 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 5249 | 2 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 5249 | 3 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 23257 | 0 | `good` | `64->128` | 0.015625 | 0.125 | 0.109375 | 0.0078125 | 0 |
| 15 | 23257 | 1 | `good` | `64->128` | 0.015625 | 0.125 | 0.109375 | 0.0078125 | 0 |
| 15 | 23257 | 2 | `good` | `64->128` | 0.015625 | 0.125 | 0.109375 | 0.0078125 | 0 |
| 15 | 23257 | 3 | `good` | `64->128` | 0.015625 | 0.125 | 0.109375 | 0.0078125 | 0 |
| 15 | 28571 | 0 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 28571 | 1 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 28571 | 2 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 28571 | 3 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 0 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 1 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 2 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 3 | `good` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 20600 | 0 | `good` | `64->128` | 0.00390625 | 0.10546875 | 0.1015625 | 0.00390625 | 0 |
| 15 | 20600 | 1 | `good` | `64->128` | 0.00390625 | 0.10546875 | 0.1015625 | 0.00390625 | 0 |
| 15 | 20600 | 2 | `good` | `64->128` | 0.00390625 | 0.10546875 | 0.1015625 | 0.00390625 | 0 |
| 15 | 20600 | 3 | `good` | `64->128` | 0.00390625 | 0.10546875 | 0.1015625 | 0.00390625 | 0 |
| 15 | 13220 | 0 | `good` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 13220 | 1 | `good` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 13220 | 2 | `good` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 13220 | 3 | `good` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 2592 | 0 | `good` | `64->128` | 0.01171875 | 0.10546875 | 0.09375 | 0.01171875 | 0 |

## Interpretation Guardrail

Small `component_l1` with large `label_excess` means the good/bad
kernel is hiding retained-label drift.  Small `label_excess` would
support, but not prove, lifting the component kernel to retained
labels in a weak averaged norm.  This diagnostic does not define
an infinite operator and does not imply a spectral gap.
