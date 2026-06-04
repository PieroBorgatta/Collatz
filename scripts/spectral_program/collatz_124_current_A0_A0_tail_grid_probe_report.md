# A0 Tail Grid Probe

Status: finite diagnostic for TODO `10.M`; not a proof.

## Scope

- phases: `0|3|0,1|3|0,3|1|0,7|3|0`
- step caps S: `10,25,50,75`
- valuation caps A: `4,6,8,10`
- sample limit per phase: `128`
- target modulus bits: `8`
- rows CSV: `collatz_124_current_A0_A0_tail_grid_probe_rows.csv`

The period exponent used for each `(S,A)` is:

```text
period_m = max(min_period_m, S*A + 1 - target_modulus_bits).
```

## Aggregate Grid

| S | A | m | val tail | symbolic tail | drop | kernel tail | word mismatch max | shadow mismatch | kernel mismatch | arch excess |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 4 | 33 | 0.09375 | 0.87109375 | 0.11328125 | 0.853515625 | 0 | 0 | 0.01953125 | 0.01953125 |
| 10 | 6 | 53 | 0.0234375 | 0.94140625 | 0.169921875 | 0.796875 | 0 | 0 | 0.01953125 | 0.01953125 |
| 10 | 8 | 73 | 0.0078125 | 0.95703125 | 0.185546875 | 0.78125 | 0 | 0 | 0.01953125 | 0.01953125 |
| 10 | 10 | 93 | 0.001953125 | 0.962890625 | 0.189453125 | 0.77734375 | 0 | 0 | 0.01953125 | 0.01953125 |
| 25 | 4 | 93 | 0.630859375 | 0.2734375 | 0.40625 | 0.5234375 | 0 | 0 | 0.037109375 | 0.037109375 |
| 25 | 6 | 143 | 0.2109375 | 0.65625 | 0.705078125 | 0.22265625 | 0 | 0.0078125 | 0.0390625 | 0.03515625 |
| 25 | 8 | 193 | 0.06640625 | 0.783203125 | 0.783203125 | 0.14453125 | 0 | 0.017578125 | 0.0390625 | 0.029296875 |
| 25 | 10 | 243 | 0.009765625 | 0.837890625 | 0.8046875 | 0.123046875 | 0 | 0.01953125 | 0.0390625 | 0.029296875 |
| 50 | 4 | 193 | 0.83984375 | 0.033203125 | 0.4375 | 0.484375 | 0 | 0.00390625 | 0.0390625 | 0.037109375 |
| 50 | 6 | 293 | 0.36328125 | 0.353515625 | 0.791015625 | 0.12890625 | 0 | 0.091796875 | 0.041015625 | 0.013671875 |
| 50 | 8 | 393 | 0.1015625 | 0.53515625 | 0.87890625 | 0.041015625 | 0 | 0.154296875 | 0.041015625 | 0.005859375 |
| 50 | 10 | 493 | 0.021484375 | 0.59765625 | 0.904296875 | 0.015625 | 0 | 0.169921875 | 0.041015625 | 0 |
| 75 | 4 | 293 | 0.85546875 | 0.017578125 | 0.4375 | 0.484375 | 0 | 0.00390625 | 0.0390625 | 0.037109375 |
| 75 | 6 | 443 | 0.390625 | 0.2734375 | 0.796875 | 0.123046875 | 0 | 0.13671875 | 0.041015625 | 0 |
| 75 | 8 | 593 | 0.109375 | 0.44921875 | 0.88671875 | 0.033203125 | 0 | 0.220703125 | 0.041015625 | 0 |
| 75 | 10 | 743 | 0.021484375 | 0.51953125 | 0.912109375 | 0.0078125 | 0 | 0.236328125 | 0.041015625 | 0 |

## Extremes

| metric | S | A | value |
|---|---:|---:|---:|
| smallest return-depth tail mean | 75 | 4 | 0.017578125 |
| smallest kernel unresolved tail mean | 75 | 10 | 0.0078125 |
| smallest kernel-period mismatch mean | 10 | 4 | 0.01953125 |

## Interpretation

A proof of the current A0 branch needs the non-periodic terms to be
controlled.  The symbolic return tail is deliberately pessimistic:
it ignores archimedean drops, while the actual killed kernel maps
drops to the zero row.  The `kernel tail` column is therefore the
more relevant unresolved mass for the killed kernel.  Valuation tails
should be handled by dyadic counting, and the archimedean
boundary from `delta` and `drop` by a separate boundary estimate.
The `word mismatch max` column checks that the pure bounded valuation
word is already killed by the chosen large 2-adic period.
