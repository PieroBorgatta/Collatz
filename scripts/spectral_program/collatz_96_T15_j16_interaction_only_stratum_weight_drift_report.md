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
- v2eq2_odd3 coeffs: `-1,-0.5,0,0.5,1`

The diagnostic ratio is

```text
R_W(r,h) = (1/sample_count) sum_return 2^{-delta} W(dst)/W(src).
```

Terminal samples contribute zero.

## Identity Weight

- mean ratio: `0.0305797`
- p95 ratio: `0.25`
- p99 ratio: `0.421875`
- max ratio: `0.96875`
- fraction >= 1: `0`

## Best Grid Points By p95/p99/max

| odd3 | v2eq2 | v2 coeff | v2eq2&odd3 | mean | p95 | p99 | max | frac >= 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | 0.0247295 | 0.155199 | 0.326143 | 2.63334 | 0.000366211 |
| 0 | 0 | 0 | 0.5 | 0.0264688 | 0.226562 | 0.3125 | 1.5972 | 3.05176e-05 |
| 0 | 0 | 0 | 0 | 0.0305797 | 0.25 | 0.421875 | 0.96875 | 0 |
| 0 | 0 | 0 | -0.5 | 0.0381116 | 0.25 | 0.669793 | 0.96875 | 0 |
| 0 | 0 | 0 | -1 | 0.0509868 | 0.25 | 1.1043 | 1.48596 | 0.0229797 |

## Best Safe Grid Points

Here safe means `fraction >= 1` is zero on the tested finite window.

| odd3 | v2eq2 | v2 coeff | v2eq2&odd3 | mean | p95 | p99 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0.0305797 | 0.25 | 0.421875 | 0.96875 |
| 0 | 0 | 0 | -0.5 | 0.0381116 | 0.25 | 0.669793 | 0.96875 |

## Worst Cells For Best Grid Point

| r | h | source phase | return frac | base return weight | drift ratio |
|---:|---:|---|---:|---:|---:|
| 2298 | 0 | `v2=1|odd=1|h=0` | 1 | 0.96875 | 0.96875 |
| 2298 | 1 | `v2=1|odd=1|h=1` | 1 | 0.96875 | 0.96875 |
| 2298 | 2 | `v2=1|odd=1|h=2` | 1 | 0.96875 | 0.96875 |
| 2298 | 3 | `v2=1|odd=1|h=3` | 1 | 0.96875 | 0.96875 |
| 4346 | 0 | `v2=1|odd=1|h=0` | 1 | 0.96875 | 0.96875 |
| 4346 | 1 | `v2=1|odd=1|h=1` | 1 | 0.96875 | 0.96875 |
| 4346 | 2 | `v2=1|odd=1|h=2` | 1 | 0.96875 | 0.96875 |
| 4346 | 3 | `v2=1|odd=1|h=3` | 1 | 0.96875 | 0.96875 |
| 6394 | 0 | `v2=1|odd=1|h=0` | 1 | 0.96875 | 0.96875 |
| 6394 | 1 | `v2=1|odd=1|h=1` | 1 | 0.96875 | 0.96875 |
| 6394 | 2 | `v2=1|odd=1|h=2` | 1 | 0.96875 | 0.96875 |
| 6394 | 3 | `v2=1|odd=1|h=3` | 1 | 0.96875 | 0.96875 |

## Interpretation

A useful source-stratum drift weight should reduce high quantiles and
not create new cells with ratio above one.  This finite diagnostic
does not prove a drift inequality; it only rejects or motivates
simple parametric weights before more serious analysis.
