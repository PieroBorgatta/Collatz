# Component Block-Cauchy Diagnostic

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
- block sizes: `16`
- adjacent block pairs: `0->16, 16->32, 32->48`
- block windows used: `524256`
- skipped mixed-source windows: `28`
- skipped boundary windows: `0`

The weighted `L1` metric is the row difference in substochastic
return weights after collapsing destinations to `good/bad`.
Terminal/killed events are measured separately in count TV.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `weighted_l1` | 393192 | 0.01388172 | 0.046875 | 0.078125 | 0.203125 | 0.3984375 |
| `all` | `row_sum_abs_diff` | 393192 | 0.011943875 | 0.03125 | 0.0625 | 0.203125 | 0.3984375 |
| `all` | `count_tv_terminal_good_bad` | 393192 | 0.021803597 | 0.0625 | 0.125 | 0.1875 | 0.4375 |
| `all` | `terminal_abs_diff` | 393192 | 0.018120918 | 0.0625 | 0.125 | 0.1875 | 0.4375 |
| `good` | `weighted_l1` | 270312 | 0.0083318406 | 0.03125 | 0.060546875 | 0.109375 | 0.3984375 |
| `good` | `row_sum_abs_diff` | 270312 | 0.006734188 | 0.02734375 | 0.04296875 | 0.09375 | 0.3984375 |
| `good` | `count_tv_terminal_good_bad` | 270312 | 0.015659682 | 0.0625 | 0.125 | 0.1875 | 0.4375 |
| `good` | `terminal_abs_diff` | 270312 | 0.012998868 | 0.0625 | 0.0625 | 0.1875 | 0.4375 |
| `bad` | `weighted_l1` | 122880 | 0.026090371 | 0.078125 | 0.109375 | 0.21875 | 0.34375 |
| `bad` | `row_sum_abs_diff` | 122880 | 0.02340417 | 0.064453125 | 0.109375 | 0.21875 | 0.34375 |
| `bad` | `count_tv_terminal_good_bad` | 122880 | 0.03531901 | 0.125 | 0.125 | 0.1875 | 0.4375 |
| `bad` | `terminal_abs_diff` | 122880 | 0.029388428 | 0.125 | 0.125 | 0.1875 | 0.4375 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 270312 | 0.0053280101 | 0.03125 | 0.078125 | 0.3125 |
| `K_GB` | `good` | `bad` | 270312 | 0.0030038305 | 0.0234375 | 0.0625 | 0.25 |
| `K_BG` | `bad` | `good` | 122880 | 0.017558094 | 0.09375 | 0.203125 | 0.3125 |
| `K_BB` | `bad` | `bad` | 122880 | 0.0085322772 | 0.04296875 | 0.203125 | 0.21875 |

## By Adjacent Pair

| pair | source | count | mean weighted L1 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|
| `0->16` | `all` | 131064 | 0.009535642 | 0.056640625 | 0.09375 | 0.25 |
| `0->16` | `good` | 90104 | 0.0071783004 | 0.046875 | 0.09375 | 0.203125 |
| `0->16` | `bad` | 40960 | 0.014721333 | 0.0625 | 0.09375 | 0.25 |
| `16->32` | `all` | 131064 | 0.013903232 | 0.09375 | 0.109375 | 0.24902344 |
| `16->32` | `good` | 90104 | 0.0084089414 | 0.0625 | 0.1015625 | 0.21875 |
| `16->32` | `bad` | 40960 | 0.025989598 | 0.109375 | 0.109375 | 0.24902344 |
| `32->48` | `all` | 131064 | 0.018206286 | 0.1015625 | 0.21875 | 0.3984375 |
| `32->48` | `good` | 90104 | 0.00940828 | 0.0625 | 0.125 | 0.3984375 |
| `32->48` | `bad` | 40960 | 0.037560182 | 0.203125 | 0.21875 | 0.34375 |

## Interpretation Guardrail

Small means here would support a weak averaged block-kernel
approximation target.  Large p95/max values block any uniform
operator-norm claim unless an exceptional-source mechanism is
proved.  These diagnostics do not define an infinite operator and
do not imply a spectral gap.
