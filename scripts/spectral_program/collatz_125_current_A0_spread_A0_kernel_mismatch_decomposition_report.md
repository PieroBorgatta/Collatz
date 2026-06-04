# A0 Kernel Mismatch Decomposition

Status: finite diagnostic for TODO `10.M`; not a proof.

## Scope

- phases: `0|3|0,1|3|0,3|1|0,7|3|0`
- step caps S: `25,50,75`
- valuation caps A: `6,8,10`
- sample limit per phase: `512`
- sample mode: `spread`
- target modulus bits: `8`
- rows CSV: `collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_rows.csv`
- examples CSV: `collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_examples.csv`

Pointwise vector convention:

```text
drop/tail          -> 0
return(dst,delta)  -> 2^-delta e_dst
```

## Aggregate Decomposition

| S | A | m | point L1 | nonzero rate | dst-change L1 | delta-only L1 | drop->return L1 | return->drop L1 | tail-return L1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | 6 | 143 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 25 | 8 | 193 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 25 | 10 | 243 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 50 | 6 | 293 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 50 | 8 | 393 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 50 | 10 | 493 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 75 | 6 | 443 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 75 | 8 | 593 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |
| 75 | 10 | 743 | 0.02276611328 | 0.1821289062 | 0 | 0.02276611328 | 0 | 0 | 0 |

## Best Grid Point

| metric | S | A | value |
|---|---:|---:|---:|
| smallest total point L1 mean | 25 | 6 | 0.02276611328 |

## Focus S=75, A=10

| phase | point L1 | nonzero | dst-change share | delta-only share | drop-return share | return-drop share |
|---|---:|---:|---:|---:|---:|---:|
| `0|3|0` | 0.05029296875 | 0.40234375 | 0 | 1 | 0 | 0 |
| `1|3|0` | 0 | 0 | 0 | 0 | 0 | 0 |
| `3|1|0` | 0.04077148438 | 0.326171875 | 0 | 1 | 0 | 0 |
| `7|3|0` | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation

This diagnostic tests whether the residual boundary is mainly a change
of destination label, a harmless weight/delta perturbation on the same
destination, or a true drop/return boundary.  A proof route is cleaner
if `delta_only` dominates, because that becomes a bit-length boundary
estimate.  Destination changes or drop/return flips require a stronger
archimedean boundary lemma.
