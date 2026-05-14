# Prefix Label-Lift Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_or_v2_2`
- bad convention: `src_odd == 3 or src_v2 == 2`
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
| `all` | `component_l1` | 131064 | 0.002861205 | 0.0097961426 | 0.01361084 | 0.020507812 | 0.05859375 |
| `all` | `label_l1` | 131064 | 0.0057602607 | 0.018249512 | 0.02444458 | 0.041381836 | 0.13671875 |
| `all` | `label_excess` | 131064 | 0.0028990557 | 0.010253906 | 0.015625 | 0.03125 | 0.109375 |
| `all` | `retained_row_sum_abs_diff` | 131064 | 0.0020254074 | 0.0073242188 | 0.010253906 | 0.015625 | 0.031738281 |
| `all` | `tail_row_sum_abs_diff` | 131064 | 0 | 0 | 0 | 0 | 0 |
| `good` | `component_l1` | 57340 | 0.0021725026 | 0.0087890625 | 0.012695312 | 0.01953125 | 0.058105469 |
| `good` | `label_l1` | 57340 | 0.0043852629 | 0.016601562 | 0.0234375 | 0.042480469 | 0.13671875 |
| `good` | `label_excess` | 57340 | 0.0022127603 | 0.0078125 | 0.013671875 | 0.03125 | 0.109375 |
| `good` | `retained_row_sum_abs_diff` | 57340 | 0.0014994713 | 0.005859375 | 0.0092773438 | 0.015625 | 0.024902344 |
| `good` | `tail_row_sum_abs_diff` | 57340 | 0 | 0 | 0 | 0 | 0 |
| `bad` | `component_l1` | 73724 | 0.0033968542 | 0.010742188 | 0.013671875 | 0.020996094 | 0.05859375 |
| `bad` | `label_l1` | 73724 | 0.0068296869 | 0.01953125 | 0.025390625 | 0.041015625 | 0.12109375 |
| `bad` | `label_excess` | 73724 | 0.0034328327 | 0.01171875 | 0.015625 | 0.030273438 | 0.109375 |
| `bad` | `retained_row_sum_abs_diff` | 73724 | 0.0024344624 | 0.0078125 | 0.010986328 | 0.016235352 | 0.031738281 |
| `bad` | `tail_row_sum_abs_diff` | 73724 | 0 | 0 | 0 | 0 | 0 |

## By Prefix Pair

| pair | source | metric | count | mean | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `64->128` | `all` | `component_l1` | 131064 | 0.002861205 | 0.01361084 | 0.020507812 | 0.05859375 |
| `64->128` | `all` | `label_l1` | 131064 | 0.0057602607 | 0.02444458 | 0.041381836 | 0.13671875 |
| `64->128` | `all` | `label_excess` | 131064 | 0.0028990557 | 0.015625 | 0.03125 | 0.109375 |
| `64->128` | `good` | `component_l1` | 57340 | 0.0021725026 | 0.012695312 | 0.01953125 | 0.058105469 |
| `64->128` | `good` | `label_l1` | 57340 | 0.0043852629 | 0.0234375 | 0.042480469 | 0.13671875 |
| `64->128` | `good` | `label_excess` | 57340 | 0.0022127603 | 0.013671875 | 0.03125 | 0.109375 |
| `64->128` | `bad` | `component_l1` | 73724 | 0.0033968542 | 0.013671875 | 0.020996094 | 0.05859375 |
| `64->128` | `bad` | `label_l1` | 73724 | 0.0068296869 | 0.025390625 | 0.041015625 | 0.12109375 |
| `64->128` | `bad` | `label_excess` | 73724 | 0.0034328327 | 0.015625 | 0.030273438 | 0.109375 |

## Worst Label-Excess Rows

| T | r | h | source | pair | component L1 | label L1 | label excess | retained row diff | tail row diff |
|---:|---:|---:|---|---|---:|---:|---:|---:|---:|
| 15 | 5249 | 0 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 5249 | 1 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 5249 | 2 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 5249 | 3 | `good` | `64->128` | 0.02734375 | 0.13671875 | 0.109375 | 0.01171875 | 0 |
| 15 | 28571 | 0 | `bad` | `64->128` | 0.01171875 | 0.12109375 | 0.109375 | 0.01171875 | 0 |
| 15 | 28571 | 1 | `bad` | `64->128` | 0.01171875 | 0.12109375 | 0.109375 | 0.01171875 | 0 |
| 15 | 28571 | 2 | `bad` | `64->128` | 0.01171875 | 0.12109375 | 0.109375 | 0.01171875 | 0 |
| 15 | 28571 | 3 | `bad` | `64->128` | 0.01171875 | 0.12109375 | 0.109375 | 0.01171875 | 0 |
| 15 | 23257 | 0 | `good` | `64->128` | 0.0234375 | 0.125 | 0.1015625 | 0.0078125 | 0 |
| 15 | 23257 | 1 | `good` | `64->128` | 0.0234375 | 0.125 | 0.1015625 | 0.0078125 | 0 |
| 15 | 23257 | 2 | `good` | `64->128` | 0.0234375 | 0.125 | 0.1015625 | 0.0078125 | 0 |
| 15 | 23257 | 3 | `good` | `64->128` | 0.0234375 | 0.125 | 0.1015625 | 0.0078125 | 0 |
| 15 | 30046 | 0 | `bad` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 1 | `bad` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 2 | `bad` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 30046 | 3 | `bad` | `64->128` | 0.01953125 | 0.12109375 | 0.1015625 | 0.01171875 | 0 |
| 15 | 13220 | 0 | `bad` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 13220 | 1 | `bad` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 13220 | 2 | `bad` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 13220 | 3 | `bad` | `64->128` | 0 | 0.1015625 | 0.1015625 | 0 | 0 |
| 15 | 31128 | 0 | `bad` | `64->128` | 0.0087890625 | 0.10253906 | 0.09375 | 0.0087890625 | 0 |
| 15 | 31128 | 1 | `bad` | `64->128` | 0.0087890625 | 0.10253906 | 0.09375 | 0.0087890625 | 0 |
| 15 | 31128 | 2 | `bad` | `64->128` | 0.0087890625 | 0.10253906 | 0.09375 | 0.0087890625 | 0 |
| 15 | 31128 | 3 | `bad` | `64->128` | 0.0087890625 | 0.10253906 | 0.09375 | 0.0087890625 | 0 |
| 15 | 13908 | 0 | `bad` | `64->128` | 0.00048828125 | 0.094238281 | 0.09375 | 0.00048828125 | 0 |

## Interpretation Guardrail

Small `component_l1` with large `label_excess` means the good/bad
kernel is hiding retained-label drift.  Small `label_excess` would
support, but not prove, lifting the component kernel to retained
labels in a weak averaged norm.  This diagnostic does not define
an infinite operator and does not imply a spectral gap.
