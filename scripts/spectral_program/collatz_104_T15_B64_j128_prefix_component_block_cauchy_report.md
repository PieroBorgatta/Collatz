# Component Block-Cauchy Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- active T values: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- include boundary: `False`
- include mixed source cells: `False`
- block sizes: `64`
- adjacent block pairs: `0->64`
- block windows used: `262128`
- skipped mixed-source windows: `12`
- skipped boundary windows: `0`

The weighted `L1` metric is the row difference in substochastic
return weights after collapsing destinations to `good/bad`.
Terminal/killed events are measured separately in count TV.

## By Source Component

| source | metric | count | mean | p90 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| `all` | `weighted_l1` | 131064 | 0.0055249292 | 0.01953125 | 0.026367188 | 0.0390625 | 0.091308594 |
| `all` | `row_sum_abs_diff` | 131064 | 0.0040508148 | 0.014648438 | 0.020507812 | 0.03125 | 0.063476562 |
| `all` | `count_tv_terminal_good_bad` | 131064 | 0.011261197 | 0.046875 | 0.0625 | 0.078125 | 0.171875 |
| `all` | `terminal_abs_diff` | 131064 | 0.0089746231 | 0.03125 | 0.046875 | 0.078125 | 0.171875 |
| `good` | `weighted_l1` | 90104 | 0.0041154957 | 0.016601562 | 0.0234375 | 0.038085938 | 0.086914062 |
| `good` | `row_sum_abs_diff` | 90104 | 0.0029436693 | 0.01171875 | 0.018554688 | 0.03125 | 0.051269531 |
| `good` | `count_tv_terminal_good_bad` | 90104 | 0.008113541 | 0.03125 | 0.046875 | 0.078125 | 0.140625 |
| `good` | `terminal_abs_diff` | 90104 | 0.0064370061 | 0.03125 | 0.046875 | 0.0625 | 0.140625 |
| `bad` | `weighted_l1` | 40960 | 0.0086254075 | 0.0234375 | 0.030154419 | 0.043212891 | 0.091308594 |
| `bad` | `row_sum_abs_diff` | 40960 | 0.0064863186 | 0.017578125 | 0.0234375 | 0.034667969 | 0.063476562 |
| `bad` | `count_tv_terminal_good_bad` | 40960 | 0.018185425 | 0.046875 | 0.0625 | 0.09375 | 0.171875 |
| `bad` | `terminal_abs_diff` | 40960 | 0.014556885 | 0.046875 | 0.0625 | 0.09375 | 0.171875 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 90104 | 0.0024876592 | 0.015625 | 0.026733398 | 0.056640625 |
| `K_GB` | `good` | `bad` | 90104 | 0.0016278365 | 0.01171875 | 0.02331543 | 0.0546875 |
| `K_BG` | `bad` | `good` | 40960 | 0.0053706095 | 0.020385742 | 0.03125 | 0.056152344 |
| `K_BB` | `bad` | `bad` | 40960 | 0.003254798 | 0.015625 | 0.0234375 | 0.047363281 |

## By Adjacent Pair

| pair | source | count | mean weighted L1 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|
| `0->64` | `all` | 131064 | 0.0055249292 | 0.026367188 | 0.0390625 | 0.091308594 |
| `0->64` | `good` | 90104 | 0.0041154957 | 0.0234375 | 0.038085938 | 0.086914062 |
| `0->64` | `bad` | 40960 | 0.0086254075 | 0.030154419 | 0.043212891 | 0.091308594 |

## Interpretation Guardrail

Small means here would support a weak averaged block-kernel
approximation target.  Large p95/max values block any uniform
operator-norm claim unless an exceptional-source mechanism is
proved.  These diagnostics do not define an infinite operator and
do not imply a spectral gap.
