# Stratum Weight Drift Probe

Status: finite diagnostic, not a theorem.

## Inputs

- T: `12`
- j_count: `16`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- include t=0: `False`
- odd3 coeffs: `-0.5,0,0.5`
- v2eq2 coeffs: `-0.5,0,0.5`
- v2 coeffs: `-0.1,0,0.1`

The diagnostic ratio is

```text
R_W(r,h) = (1/sample_count) sum_return 2^{-delta} W(dst)/W(src).
```

Terminal samples contribute zero.

## Identity Weight

- mean ratio: `0.0303514`
- p95 ratio: `0.25`
- p99 ratio: `0.421875`
- max ratio: `0.9375`
- fraction >= 1: `0`

## Best Grid Points By p95/p99/max

| odd3 | v2eq2 | v2 coeff | mean | p95 | p99 | max | frac >= 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.5 | 0 | 0.0268863 | 0.160814 | 0.41218 | 1.47665 | 0.000488281 |
| 0.5 | 0.5 | 0.1 | 0.0278428 | 0.165489 | 0.413438 | 1.61407 | 0.000976562 |
| 0.5 | 0.5 | -0.1 | 0.027047 | 0.173524 | 0.390885 | 1.37217 | 0.000732422 |
| 0 | 0.5 | 0.1 | 0.0276832 | 0.197229 | 0.359795 | 1.19701 | 0.000244141 |
| 0.5 | 0 | 0.1 | 0.0296562 | 0.201738 | 0.428582 | 1.3767 | 0.000488281 |
| -0.5 | 0.5 | 0.1 | 0.0310581 | 0.207098 | 0.393745 | 0.979146 | 0 |
| -0.5 | -0.5 | -0.1 | 0.0476906 | 0.209503 | 1.1735 | 1.96117 | 0.0119629 |
| -0.5 | 0 | -0.1 | 0.0369611 | 0.210292 | 0.723692 | 2.03365 | 0.000244141 |
| -0.5 | 0.5 | -0.1 | 0.0312745 | 0.216428 | 0.47004 | 2.15315 | 0.000244141 |
| 0 | 0.5 | -0.1 | 0.0274144 | 0.216885 | 0.324108 | 1.51183 | 0.000732422 |
| 0 | 0.5 | 0 | 0.0269973 | 0.217972 | 0.3125 | 1.09968 | 0.000244141 |
| -0.5 | 0.5 | 0 | 0.0305481 | 0.224472 | 0.40625 | 0.881422 | 0 |

## Best Safe Grid Points

Here safe means `fraction >= 1` is zero on the tested finite window.

| odd3 | v2eq2 | v2 coeff | mean | p95 | p99 | max |
|---:|---:|---:|---:|---:|---:|---:|
| -0.5 | 0.5 | 0.1 | 0.0310581 | 0.207098 | 0.393745 | 0.979146 |
| -0.5 | 0.5 | 0 | 0.0305481 | 0.224472 | 0.40625 | 0.881422 |
| -0.5 | 0 | 0 | 0.0352464 | 0.235395 | 0.644032 | 0.818651 |
| 0 | 0 | 0 | 0.0303514 | 0.25 | 0.421875 | 0.9375 |
| 0 | -0.5 | 0 | 0.0373556 | 0.25 | 0.669793 | 0.9375 |

## Worst Cells For Best Grid Point

| r | h | source phase | return frac | base return weight | drift ratio |
|---:|---:|---|---:|---:|---:|
| 3238 | 0 | `v2=1|odd=3|h=0` | 1 | 0.453125 | 0.979146 |
| 3238 | 1 | `v2=1|odd=3|h=1` | 1 | 0.453125 | 0.979146 |
| 3238 | 2 | `v2=1|odd=3|h=2` | 1 | 0.453125 | 0.979146 |
| 3238 | 3 | `v2=1|odd=3|h=3` | 1 | 0.453125 | 0.979146 |
| 2298 | 0 | `v2=1|odd=1|h=0` | 1 | 0.9375 | 0.944044 |
| 2298 | 1 | `v2=1|odd=1|h=1` | 1 | 0.9375 | 0.944044 |
| 2298 | 2 | `v2=1|odd=1|h=2` | 1 | 0.9375 | 0.944044 |
| 2298 | 3 | `v2=1|odd=1|h=3` | 1 | 0.9375 | 0.944044 |
| 1854 | 0 | `v2=1|odd=3|h=0` | 1 | 0.625 | 0.893488 |
| 1854 | 1 | `v2=1|odd=3|h=1` | 1 | 0.625 | 0.893488 |
| 1854 | 2 | `v2=1|odd=3|h=2` | 1 | 0.625 | 0.893488 |
| 1854 | 3 | `v2=1|odd=3|h=3` | 1 | 0.625 | 0.893488 |

## Interpretation

A useful source-stratum drift weight should reduce high quantiles and
not create new cells with ratio above one.  This finite diagnostic
does not prove a drift inequality; it only rejects or motivates
simple parametric weights before more serious analysis.
