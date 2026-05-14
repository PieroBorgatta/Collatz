# Stratum Weight Drift Probe

Status: finite diagnostic, not a theorem.

## Inputs

- T: `15`
- j_count: `16`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- include t=0: `False`
- odd3 coeffs: `0`
- v2eq2 coeffs: `0`
- v2 coeffs: `0`
- v2eq2_odd3 coeffs: `1`

The diagnostic ratio is

```text
R_W(r,h) = (1/sample_count) sum_return 2^{-delta} W(dst)/W(src).
```

Terminal samples contribute zero.

## Identity Weight

- identity weight was not included in the grid.

## Best Grid Points By p95/p99/max

| odd3 | v2eq2 | v2 coeff | v2eq2&odd3 | mean | p95 | p99 | max | frac >= 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | 0.0247295 | 0.155199 | 0.326143 | 2.63334 | 0.000366211 |

## Best Safe Grid Points

Here safe means `fraction >= 1` is zero on the tested finite window.

| odd3 | v2eq2 | v2 coeff | v2eq2&odd3 | mean | p95 | p99 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|

## Worst Cells For Best Grid Point

| r | h | source phase | return frac | base return weight | drift ratio |
|---:|---:|---|---:|---:|---:|
| 6394 | 0 | `v2=1|odd=1|h=0` | 1 | 0.96875 | 2.63334 |
| 6394 | 1 | `v2=1|odd=1|h=1` | 1 | 0.96875 | 2.63334 |
| 6394 | 2 | `v2=1|odd=1|h=2` | 1 | 0.96875 | 2.63334 |
| 6394 | 3 | `v2=1|odd=1|h=3` | 1 | 0.96875 | 2.63334 |
| 11430 | 0 | `v2=1|odd=3|h=0` | 1 | 0.484375 | 1.31667 |
| 11430 | 1 | `v2=1|odd=3|h=1` | 1 | 0.484375 | 1.31667 |
| 11430 | 2 | `v2=1|odd=3|h=2` | 1 | 0.484375 | 1.31667 |
| 11430 | 3 | `v2=1|odd=3|h=3` | 1 | 0.484375 | 1.31667 |
| 10046 | 0 | `v2=1|odd=3|h=0` | 1 | 0.65625 | 1.30061 |
| 10046 | 1 | `v2=1|odd=3|h=1` | 1 | 0.65625 | 1.30061 |
| 10046 | 2 | `v2=1|odd=3|h=2` | 1 | 0.65625 | 1.30061 |
| 10046 | 3 | `v2=1|odd=3|h=3` | 1 | 0.65625 | 1.30061 |
| 27814 | 0 | `v2=1|odd=3|h=0` | 1 | 0.453125 | 1.23172 |
| 27814 | 1 | `v2=1|odd=3|h=1` | 1 | 0.453125 | 1.23172 |
| 27814 | 2 | `v2=1|odd=3|h=2` | 1 | 0.453125 | 1.23172 |
| 27814 | 3 | `v2=1|odd=3|h=3` | 1 | 0.453125 | 1.23172 |
| 15360 | 0 | `v2=10|odd=3|h=0` | 1 | 0.625 | 1.21566 |
| 15360 | 1 | `v2=10|odd=3|h=1` | 1 | 0.625 | 1.21566 |
| 15360 | 2 | `v2=10|odd=3|h=2` | 1 | 0.625 | 1.21566 |
| 15360 | 3 | `v2=10|odd=3|h=3` | 1 | 0.625 | 1.21566 |
| 18017 | 0 | `v2=0|odd=1|h=0` | 1 | 0.625 | 1.21566 |
| 18017 | 1 | `v2=0|odd=1|h=1` | 1 | 0.625 | 1.21566 |
| 18017 | 2 | `v2=0|odd=1|h=2` | 1 | 0.625 | 1.21566 |
| 18017 | 3 | `v2=0|odd=1|h=3` | 1 | 0.625 | 1.21566 |
| 2592 | 0 | `v2=5|odd=1|h=0` | 1 | 0.90625 | 1.12104 |
| 2592 | 1 | `v2=5|odd=1|h=1` | 1 | 0.90625 | 1.12104 |
| 2592 | 2 | `v2=5|odd=1|h=2` | 1 | 0.90625 | 1.12104 |
| 2592 | 3 | `v2=5|odd=1|h=3` | 1 | 0.90625 | 1.12104 |
| 32186 | 0 | `v2=1|odd=1|h=0` | 1 | 0.59375 | 1.07702 |
| 32186 | 1 | `v2=1|odd=1|h=1` | 1 | 0.59375 | 1.07702 |
| 32186 | 2 | `v2=1|odd=1|h=2` | 1 | 0.59375 | 1.07702 |
| 32186 | 3 | `v2=1|odd=1|h=3` | 1 | 0.59375 | 1.07702 |
| 19418 | 0 | `v2=1|odd=1|h=0` | 1 | 0.84375 | 1.05854 |
| 19418 | 1 | `v2=1|odd=1|h=1` | 1 | 0.84375 | 1.05854 |
| 19418 | 2 | `v2=1|odd=1|h=2` | 1 | 0.84375 | 1.05854 |
| 19418 | 3 | `v2=1|odd=1|h=3` | 1 | 0.84375 | 1.05854 |
| 20600 | 0 | `v2=3|odd=3|h=0` | 1 | 0.84375 | 1.05854 |
| 20600 | 1 | `v2=3|odd=3|h=1` | 1 | 0.84375 | 1.05854 |
| 20600 | 2 | `v2=3|odd=3|h=2` | 1 | 0.84375 | 1.05854 |
| 20600 | 3 | `v2=3|odd=3|h=3` | 1 | 0.84375 | 1.05854 |

## Interpretation

A useful source-stratum drift weight should reduce high quantiles and
not create new cells with ratio above one.  This finite diagnostic
does not prove a drift inequality; it only rejects or motivates
simple parametric weights before more serious analysis.
