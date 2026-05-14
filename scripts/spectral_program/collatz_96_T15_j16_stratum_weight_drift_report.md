# Stratum Weight Drift Probe

Status: finite diagnostic, not a theorem.

## Inputs

- T: `15`
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

- mean ratio: `0.0305797`
- p95 ratio: `0.25`
- p99 ratio: `0.421875`
- max ratio: `0.96875`
- fraction >= 1: `0`

## Best Grid Points By p95/p99/max

| odd3 | v2eq2 | v2 coeff | mean | p95 | p99 | max | frac >= 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.5 | 0 | 0.0271007 | 0.171875 | 0.41218 | 2.63334 | 0.000701904 |
| 0.5 | 0.5 | 0.1 | 0.0279849 | 0.17846 | 0.4515 | 2.91029 | 0.000946045 |
| 0.5 | 0.5 | -0.1 | 0.0272779 | 0.18254 | 0.41218 | 2.38274 | 0.00106812 |
| 0 | 0.5 | 0.1 | 0.0278001 | 0.201738 | 0.390625 | 1.76518 | 0.000396729 |
| -0.5 | 0.5 | 0.1 | 0.0311721 | 0.21438 | 0.431707 | 1.70824 | 0.000427246 |
| 0.5 | 0 | 0.1 | 0.0298342 | 0.21438 | 0.448976 | 1.76518 | 0.000732422 |
| 0 | 0.5 | -0.1 | 0.0276129 | 0.226209 | 0.359375 | 2.29331 | 0.000671387 |
| 0 | 0.5 | 0 | 0.0271794 | 0.227449 | 0.375 | 1.5972 | 0.000244141 |
| -0.5 | 0.5 | -0.1 | 0.0314821 | 0.229961 | 0.47711 | 2.96278 | 0.000823975 |
| -0.5 | 0 | -0.1 | 0.0372289 | 0.233098 | 0.723692 | 2.94111 | 0.000640869 |
| -0.5 | 0.5 | 0 | 0.0307353 | 0.234375 | 0.421875 | 1.54568 | 0.000518799 |
| 0.5 | 0 | 0 | 0.0295795 | 0.236926 | 0.421875 | 1.5972 | 0.000610352 |

## Best Safe Grid Points

Here safe means `fraction >= 1` is zero on the tested finite window.

| odd3 | v2eq2 | v2 coeff | mean | p95 | p99 | max |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0.0305797 | 0.25 | 0.421875 | 0.96875 |

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
