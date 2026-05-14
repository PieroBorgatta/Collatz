# Component Block-Cauchy Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B32_j64_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B32_j64_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- include boundary: `False`
- include mixed source cells: `False`
- block sizes: `32`
- adjacent block pairs: `0->32`
- block windows used: `262140`
- skipped mixed-source windows: `0`
- skipped boundary windows: `0`

The weighted `L1` metric is the row difference in substochastic
return weights after collapsing destinations to `good/bad`.
Terminal/killed events are measured separately in count TV.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `weighted_l1` | 131068 | 0.0074155295 | 0.02734375 | 0.0390625 | 0.0625 | 0.140625 |
| `all` | `row_sum_abs_diff` | 131068 | 0.0054434859 | 0.01953125 | 0.03125 | 0.046875 | 0.1015625 |
| `all` | `count_tv_terminal_good_bad` | 131068 | 0.015938292 | 0.0625 | 0.09375 | 0.125 | 0.25 |
| `all` | `terminal_abs_diff` | 131068 | 0.012861644 | 0.0625 | 0.0625 | 0.125 | 0.25 |
| `good` | `weighted_l1` | 90108 | 0.0055656365 | 0.0234375 | 0.034179688 | 0.0625 | 0.140625 |
| `good` | `row_sum_abs_diff` | 90108 | 0.0039739532 | 0.015625 | 0.026367188 | 0.046875 | 0.1015625 |
| `good` | `count_tv_terminal_good_bad` | 90108 | 0.011493153 | 0.0625 | 0.0625 | 0.125 | 0.25 |
| `good` | `terminal_abs_diff` | 90108 | 0.0093082745 | 0.03125 | 0.0625 | 0.09375 | 0.25 |
| `bad` | `weighted_l1` | 40960 | 0.011485113 | 0.03125 | 0.04296875 | 0.06640625 | 0.12841797 |
| `bad` | `row_sum_abs_diff` | 40960 | 0.0086763144 | 0.024060059 | 0.032592773 | 0.05078125 | 0.096679688 |
| `bad` | `count_tv_terminal_good_bad` | 40960 | 0.025717163 | 0.0625 | 0.09375 | 0.15625 | 0.25 |
| `bad` | `terminal_abs_diff` | 40960 | 0.020678711 | 0.0625 | 0.09375 | 0.125 | 0.25 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 90108 | 0.0034798091 | 0.0234375 | 0.045898438 | 0.086425781 |
| `K_GB` | `good` | `bad` | 90108 | 0.0020858274 | 0.015625 | 0.03125 | 0.08984375 |
| `K_BG` | `bad` | `good` | 40960 | 0.0073552837 | 0.03125 | 0.046875 | 0.096679688 |
| `K_BB` | `bad` | `bad` | 40960 | 0.0041298296 | 0.021484375 | 0.031738281 | 0.0625 |

## Interpretation Guardrail

Small means here would support a weak averaged block-kernel
approximation target.  Large p95/max values block any uniform
operator-norm claim unless an exceptional-source mechanism is
proved.  These diagnostics do not define an infinite operator and
do not imply a spectral gap.
