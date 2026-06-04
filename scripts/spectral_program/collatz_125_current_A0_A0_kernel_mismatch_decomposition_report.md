# A0 Kernel Mismatch Decomposition

Status: finite diagnostic for TODO `10.M`; not a proof.

## Scope

- phases: `0|3|0,1|3|0,3|1|0,7|3|0`
- step caps S: `25,50,75`
- valuation caps A: `6,8,10`
- sample limit per phase: `256`
- target modulus bits: `8`
- rows CSV: `collatz_125_current_A0_A0_kernel_mismatch_decomposition_rows.csv`
- examples CSV: `collatz_125_current_A0_A0_kernel_mismatch_decomposition_examples.csv`

Pointwise vector convention:

```text
drop/tail          -> 0
return(dst,delta)  -> 2^-delta e_dst
```

## Aggregate Decomposition

| S | A | m | point L1 | nonzero rate | dst-change L1 | delta-only L1 | drop->return L1 | return->drop L1 | tail-return L1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | 6 | 143 | 0.008209228516 | 0.0419921875 | 0 | 0.008209228516 | 0 | 0 | 0 |
| 25 | 8 | 193 | 0.008209228516 | 0.0419921875 | 0 | 0.008209228516 | 0 | 0 | 0 |
| 25 | 10 | 243 | 0.008209228516 | 0.0419921875 | 0 | 0.008209228516 | 0 | 0 | 0 |
| 50 | 6 | 293 | 0.009307861328 | 0.044921875 | 0 | 0.009307861328 | 0 | 0 | 0 |
| 50 | 8 | 393 | 0.009307861328 | 0.044921875 | 0 | 0.009307861328 | 0 | 0 | 0 |
| 50 | 10 | 493 | 0.009307861328 | 0.044921875 | 0 | 0.009307861328 | 0 | 0 | 0 |
| 75 | 6 | 443 | 0.009307861328 | 0.044921875 | 0 | 0.009307861328 | 0 | 0 | 0 |
| 75 | 8 | 593 | 0.009307861328 | 0.044921875 | 0 | 0.009307861328 | 0 | 0 | 0 |
| 75 | 10 | 743 | 0.009307861328 | 0.044921875 | 0 | 0.009307861328 | 0 | 0 | 0 |

## Best Grid Point

| metric | S | A | value |
|---|---:|---:|---:|
| smallest total point L1 mean | 25 | 6 | 0.008209228516 |

## Focus S=75, A=10

| phase | point L1 | nonzero | dst-change share | delta-only share | drop-return share | return-drop share |
|---|---:|---:|---:|---:|---:|---:|
| `0|3|0` | 0.01409912109 | 0.06640625 | 0 | 1 | 0 | 0 |
| `1|3|0` | 0.003967285156 | 0.01953125 | 0 | 1 | 0 | 0 |
| `3|1|0` | 0.007629394531 | 0.0390625 | 0 | 1 | 0 | 0 |
| `7|3|0` | 0.01153564453 | 0.0546875 | 0 | 1 | 0 | 0 |

## Interpretation

This diagnostic tests whether the residual boundary is mainly a change
of destination label, a harmless weight/delta perturbation on the same
destination, or a true drop/return boundary.  A proof route is cleaner
if `delta_only` dominates, because that becomes a bit-length boundary
estimate.  Destination changes or drop/return flips require a stronger
archimedean boundary lemma.
