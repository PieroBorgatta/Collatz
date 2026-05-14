# Component Block-Cauchy Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B16_j32_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B16_j32_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- include boundary: `False`
- include mixed source cells: `False`
- block sizes: `16`
- adjacent block pairs: `0->16`
- block windows used: `262140`
- skipped mixed-source windows: `0`
- skipped boundary windows: `0`

The weighted `L1` metric is the row difference in substochastic
return weights after collapsing destinations to `good/bad`.
Terminal/killed events are measured separately in count TV.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `weighted_l1` | 131068 | 0.0095367816 | 0.03125 | 0.056640625 | 0.09375 | 0.25 |
| `all` | `row_sum_abs_diff` | 131068 | 0.0074835065 | 0.03125 | 0.041015625 | 0.074707031 | 0.1875 |
| `all` | `count_tv_terminal_good_bad` | 131068 | 0.021858882 | 0.0625 | 0.125 | 0.1875 | 0.4375 |
| `all` | `terminal_abs_diff` | 131068 | 0.018202383 | 0.0625 | 0.125 | 0.1875 | 0.375 |
| `good` | `weighted_l1` | 90108 | 0.0071800626 | 0.03125 | 0.046875 | 0.09375 | 0.203125 |
| `good` | `row_sum_abs_diff` | 90108 | 0.0054332953 | 0.01953125 | 0.03125 | 0.0703125 | 0.1875 |
| `good` | `count_tv_terminal_good_bad` | 90108 | 0.015689506 | 0.0625 | 0.125 | 0.1875 | 0.4375 |
| `good` | `terminal_abs_diff` | 90108 | 0.012992742 | 0.0625 | 0.0625 | 0.1875 | 0.3125 |
| `bad` | `weighted_l1` | 40960 | 0.014721333 | 0.044482422 | 0.0625 | 0.09375 | 0.25 |
| `bad` | `row_sum_abs_diff` | 40960 | 0.011993771 | 0.03125 | 0.0546875 | 0.078125 | 0.171875 |
| `bad` | `count_tv_terminal_good_bad` | 40960 | 0.035430908 | 0.125 | 0.125 | 0.1875 | 0.375 |
| `bad` | `terminal_abs_diff` | 40960 | 0.029663086 | 0.125 | 0.125 | 0.1875 | 0.375 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 90108 | 0.0044481311 | 0.03125 | 0.0625 | 0.171875 |
| `K_GB` | `good` | `bad` | 90108 | 0.0027319315 | 0.015625 | 0.0625 | 0.125 |
| `K_BG` | `bad` | `good` | 40960 | 0.0096972845 | 0.046875 | 0.076171875 | 0.15625 |
| `K_BB` | `bad` | `bad` | 40960 | 0.0050240487 | 0.03125 | 0.0625 | 0.125 |

## Interpretation Guardrail

Small means here would support a weak averaged block-kernel
approximation target.  Large p95/max values block any uniform
operator-norm claim unless an exceptional-source mechanism is
proved.  These diagnostics do not define an infinite operator and
do not imply a spectral gap.
