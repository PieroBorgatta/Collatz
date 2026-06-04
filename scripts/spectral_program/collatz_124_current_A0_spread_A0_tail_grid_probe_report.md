# A0 Tail Grid Probe

Status: finite diagnostic for TODO `10.M`; not a proof.

## Scope

- phases: `0|3|0,1|3|0,3|1|0,7|3|0`
- step caps S: `10,25,50,75`
- valuation caps A: `4,6,8,10`
- sample limit per phase: `512`
- sample mode: `spread`
- target modulus bits: `8`
- rows CSV: `collatz_124_current_A0_spread_A0_tail_grid_probe_rows.csv`

The period exponent used for each `(S,A)` is:

```text
period_m = max(min_period_m, S*A + 1 - target_modulus_bits).
```

## Aggregate Grid

| S | A | m | val tail | symbolic tail | drop | kernel tail | word mismatch max | shadow mismatch | kernel mismatch | arch excess |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 4 | 33 | 0 | 0.5 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 10 | 6 | 53 | 0 | 0.5 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 10 | 8 | 73 | 0 | 0.5 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 10 | 10 | 93 | 0 | 0.5 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 25 | 4 | 93 | 0.5 | 0 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 25 | 6 | 143 | 0.25 | 0.25 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 25 | 8 | 193 | 0 | 0.5 | 0.25 | 0.25 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 25 | 10 | 243 | 0 | 0.5 | 0.25 | 0.25 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 50 | 4 | 193 | 0.5 | 0 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 50 | 6 | 293 | 0.5 | 0 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 50 | 8 | 393 | 0 | 0.5 | 0.5 | 0 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 50 | 10 | 493 | 0 | 0.5 | 0.5 | 0 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 75 | 4 | 293 | 0.5 | 0 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 75 | 6 | 443 | 0.5 | 0 | 0 | 0.5 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 75 | 8 | 593 | 0 | 0.5 | 0.5 | 0 | 0 | 0 | 0.1821289062 | 0.1821289062 |
| 75 | 10 | 743 | 0 | 0.5 | 0.5 | 0 | 0 | 0 | 0.1821289062 | 0.1821289062 |

## Extremes

| metric | S | A | value |
|---|---:|---:|---:|
| smallest return-depth tail mean | 25 | 4 | 0 |
| smallest kernel unresolved tail mean | 50 | 8 | 0 |
| smallest kernel-period mismatch mean | 10 | 4 | 0.1821289062 |

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
