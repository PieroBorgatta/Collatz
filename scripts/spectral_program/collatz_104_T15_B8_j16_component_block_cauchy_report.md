# Component Block-Cauchy Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B8_j16_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B8_j16_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- include boundary: `False`
- include mixed source cells: `False`
- block sizes: `8`
- adjacent block pairs: `0->8`
- block windows used: `262140`
- skipped mixed-source windows: `0`
- skipped boundary windows: `0`

The weighted `L1` metric is the row difference in substochastic
return weights after collapsing destinations to `good/bad`.
Terminal/killed events are measured separately in count TV.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `weighted_l1` | 131068 | 0.012046521 | 0.046875 | 0.0625 | 0.12695312 | 0.40625 |
| `all` | `row_sum_abs_diff` | 131068 | 0.010124155 | 0.03125 | 0.0625 | 0.125 | 0.25 |
| `all` | `count_tv_terminal_good_bad` | 131068 | 0.029622028 | 0.125 | 0.125 | 0.25 | 0.75 |
| `all` | `terminal_abs_diff` | 131068 | 0.025334178 | 0.125 | 0.125 | 0.25 | 0.75 |
| `good` | `weighted_l1` | 90108 | 0.0093235814 | 0.03125 | 0.0625 | 0.125 | 0.40625 |
| `good` | `row_sum_abs_diff` | 90108 | 0.0076302683 | 0.03125 | 0.0625 | 0.125 | 0.25 |
| `good` | `count_tv_terminal_good_bad` | 90108 | 0.021535269 | 0.125 | 0.125 | 0.25 | 0.75 |
| `good` | `terminal_abs_diff` | 90108 | 0.0183613 | 0.125 | 0.125 | 0.25 | 0.75 |
| `bad` | `weighted_l1` | 40960 | 0.018036723 | 0.0625 | 0.078125 | 0.140625 | 0.40625 |
| `bad` | `row_sum_abs_diff` | 40960 | 0.015610462 | 0.0625 | 0.0625 | 0.125 | 0.25 |
| `bad` | `count_tv_terminal_good_bad` | 40960 | 0.047412109 | 0.125 | 0.25 | 0.25 | 0.5 |
| `bad` | `terminal_abs_diff` | 40960 | 0.040673828 | 0.125 | 0.25 | 0.25 | 0.5 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 90108 | 0.0060317688 | 0.046875 | 0.125 | 0.28125 |
| `K_GB` | `good` | `bad` | 90108 | 0.0032918126 | 0.0234375 | 0.0625 | 0.1875 |
| `K_BG` | `bad` | `good` | 40960 | 0.011941701 | 0.0625 | 0.125 | 0.25 |
| `K_BB` | `bad` | `bad` | 40960 | 0.006095022 | 0.03125 | 0.09375 | 0.25 |

## Interpretation Guardrail

Small means here would support a weak averaged block-kernel
approximation target.  Large p95/max values block any uniform
operator-norm claim unless an exceptional-source mechanism is
proved.  These diagnostics do not define an infinite operator and
do not imply a spectral gap.
