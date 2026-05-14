# Component Prefix-Cauchy Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- include boundary: `False`
- include mixed source cells: `False`
- prefix counts: `16, 32, 64`
- prefix windows used: `393192`
- skipped mixed-source windows: `24`
- skipped boundary windows: `0`

The weighted `L1` metric is the row difference in substochastic
return weights after collapsing destinations to `good/bad`.
Terminal/killed events are measured separately in count TV.
All summary means are uniform over retained source cells/prefix
pairs.  By default this excludes boundary rows and mixed-source
cells, so the implicit source weight is a finite counting measure
on the retained complete cells, not a proved limiting Haar
measure.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `weighted_l1` | 262128 | 0.0042377302 | 0.015625 | 0.0234375 | 0.0390625 | 0.125 |
| `all` | `row_sum_abs_diff` | 262128 | 0.0032317275 | 0.01171875 | 0.015625 | 0.03125 | 0.09375 |
| `all` | `count_tv_terminal_good_bad` | 262128 | 0.0094488666 | 0.03125 | 0.0625 | 0.09375 | 0.21875 |
| `all` | `terminal_abs_diff` | 262128 | 0.007766244 | 0.03125 | 0.046875 | 0.078125 | 0.1875 |
| `good` | `weighted_l1` | 180208 | 0.0031858726 | 0.01184082 | 0.01953125 | 0.0390625 | 0.1015625 |
| `good` | `row_sum_abs_diff` | 180208 | 0.0023517431 | 0.0078125 | 0.015625 | 0.03125 | 0.09375 |
| `good` | `count_tv_terminal_good_bad` | 180208 | 0.0067949259 | 0.03125 | 0.046875 | 0.0625 | 0.21875 |
| `good` | `terminal_abs_diff` | 180208 | 0.0055755016 | 0.03125 | 0.03125 | 0.0625 | 0.15625 |
| `bad` | `weighted_l1` | 81920 | 0.0065516116 | 0.017584229 | 0.026855469 | 0.04296875 | 0.125 |
| `bad` | `row_sum_abs_diff` | 81920 | 0.0051675214 | 0.015625 | 0.020507812 | 0.034667969 | 0.0859375 |
| `bad` | `count_tv_terminal_good_bad` | 81920 | 0.015287018 | 0.046875 | 0.0625 | 0.09375 | 0.1875 |
| `bad` | `terminal_abs_diff` | 81920 | 0.012585449 | 0.03125 | 0.0625 | 0.09375 | 0.1875 |

## By Prefix Pair

| pair | source | count | mean weighted L1 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|
| `16->32` | `all` | 131064 | 0.004767821 | 0.028320312 | 0.046875 | 0.125 |
| `16->32` | `good` | 90104 | 0.0035891502 | 0.0234375 | 0.046875 | 0.1015625 |
| `16->32` | `bad` | 40960 | 0.0073606666 | 0.03125 | 0.046875 | 0.125 |
| `32->64` | `all` | 131064 | 0.0037076395 | 0.01953125 | 0.03125 | 0.0703125 |
| `32->64` | `good` | 90104 | 0.002782595 | 0.017089844 | 0.03125 | 0.0703125 |
| `32->64` | `bad` | 40960 | 0.0057425566 | 0.021484375 | 0.033203125 | 0.064208984 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 180208 | 0.0019816395 | 0.015625 | 0.03125 | 0.0859375 |
| `K_GB` | `good` | `bad` | 180208 | 0.0012042331 | 0.0078125 | 0.021484375 | 0.0625 |
| `K_BG` | `bad` | `good` | 81920 | 0.0042631421 | 0.017578125 | 0.03125 | 0.078125 |
| `K_BB` | `bad` | `bad` | 81920 | 0.0022884696 | 0.015625 | 0.030718384 | 0.0625 |

## Interpretation Guardrail

Small means here support a Cesaro/prefix-average mixed-norm
target.  Large p95/max values still block uniform operator-norm
claims unless an exceptional-source mechanism is proved.
These diagnostics do not define an infinite operator and do not
imply a spectral gap.
