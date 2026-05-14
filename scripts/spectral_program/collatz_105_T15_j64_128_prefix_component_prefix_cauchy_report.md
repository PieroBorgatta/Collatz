# Component Prefix-Cauchy Diagnostic

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
- prefix counts: `64, 128`
- prefix windows used: `262128`
- skipped mixed-source windows: `16`
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
| `all` | `weighted_l1` | 131064 | 0.0027624646 | 0.009765625 | 0.013183594 | 0.01953125 | 0.045654297 |
| `all` | `row_sum_abs_diff` | 131064 | 0.0020254074 | 0.0073242188 | 0.010253906 | 0.015625 | 0.031738281 |
| `all` | `count_tv_terminal_good_bad` | 131064 | 0.0056305984 | 0.0234375 | 0.03125 | 0.0390625 | 0.0859375 |
| `all` | `terminal_abs_diff` | 131064 | 0.0044873115 | 0.015625 | 0.0234375 | 0.0390625 | 0.0859375 |
| `good` | `weighted_l1` | 90104 | 0.0020577478 | 0.0083007812 | 0.01171875 | 0.019042969 | 0.043457031 |
| `good` | `row_sum_abs_diff` | 90104 | 0.0014718347 | 0.005859375 | 0.0092773438 | 0.015625 | 0.025634766 |
| `good` | `count_tv_terminal_good_bad` | 90104 | 0.0040567705 | 0.015625 | 0.0234375 | 0.0390625 | 0.0703125 |
| `good` | `terminal_abs_diff` | 90104 | 0.0032185031 | 0.015625 | 0.0234375 | 0.03125 | 0.0703125 |
| `bad` | `weighted_l1` | 40960 | 0.0043127038 | 0.01171875 | 0.015077209 | 0.021606445 | 0.045654297 |
| `bad` | `row_sum_abs_diff` | 40960 | 0.0032431593 | 0.0087890625 | 0.01171875 | 0.017333984 | 0.031738281 |
| `bad` | `count_tv_terminal_good_bad` | 40960 | 0.0090927124 | 0.0234375 | 0.03125 | 0.046875 | 0.0859375 |
| `bad` | `terminal_abs_diff` | 40960 | 0.0072784424 | 0.0234375 | 0.03125 | 0.046875 | 0.0859375 |

## By Prefix Pair

| pair | source | count | mean weighted L1 | p95 | p99 | max |
|---|---|---:|---:|---:|---:|---:|
| `64->128` | `all` | 131064 | 0.0027624646 | 0.013183594 | 0.01953125 | 0.045654297 |
| `64->128` | `good` | 90104 | 0.0020577478 | 0.01171875 | 0.019042969 | 0.043457031 |
| `64->128` | `bad` | 40960 | 0.0043127038 | 0.015077209 | 0.021606445 | 0.045654297 |

## By Block Entry

| entry | source | destination | count | mean abs drift | p95 | p99 | max |
|---|---|---|---:|---:|---:|---:|---:|
| `K_GG` | `good` | `good` | 90104 | 0.0012438296 | 0.0078125 | 0.013366699 | 0.028320312 |
| `K_GB` | `good` | `bad` | 90104 | 0.00081391823 | 0.005859375 | 0.011657715 | 0.02734375 |
| `K_BG` | `bad` | `good` | 40960 | 0.0026853048 | 0.010192871 | 0.015625 | 0.028076172 |
| `K_BB` | `bad` | `bad` | 40960 | 0.001627399 | 0.0078125 | 0.01171875 | 0.023681641 |

## Interpretation Guardrail

Small means here support a Cesaro/prefix-average mixed-norm
target.  Large p95/max values still block uniform operator-norm
claims unless an exceptional-source mechanism is proved.
These diagnostics do not define an infinite operator and do not
imply a spectral gap.
