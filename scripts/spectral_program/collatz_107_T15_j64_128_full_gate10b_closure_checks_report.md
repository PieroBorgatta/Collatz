# Gate 10.B Closure Checks

Status: finite bookkeeping diagnostic, not an infinite-operator theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- bad rule: `odd3_v2_0_or_2`
- bad convention: `src_odd == 3 and src_v2 in {0, 2}`
- delta cutoff: `none`
- include boundary: `False`
- include mixed source cells: `False`
- retained prefix windows: `262128`

## Source Averaging

| j_count | full cells | retained cells | excluded | excluded fraction | mean error coeff | skipped mixed | skipped boundary |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 64 | 131072 | 131064 | 8 | 6.103515625e-05 | 0.0001220703125 | 8 | 0 |
| 128 | 131072 | 131064 | 8 | 6.103515625e-05 | 0.0001220703125 | 8 | 0 |

For bounded row diagnostics `F`, the finite retained-source mean
differs from the complete-cell mean by at most:

```text
2 * excluded_fraction * ||F||_infty.
```

This is a finite correction only; it is not a Haar-limit theorem.

## Row-Source Identity Checks

| check | value |
|---|---:|
| max full-count residual | 0 |
| windows with count residual | 0 |
| max full-weight residual | 0 |
| windows with weight residual | 0 |
| max terminal-fraction residual | 0 |
| windows with terminal residual | 0 |

A zero residual means the CSV full-signature rows exactly define
the empirical row-source prefix kernel used by later diagnostics.
It does not identify that empirical kernel with `E U_s I`.

## Prefix Pair Checks

| pair | rows | component mean | phase mean | label mean | comp-phase excess | phase-label excess | tail-diff mean | tail-a mean | tail-b mean | violations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `64->128` | 131064 | 0.0027624646 | 0.0045072525 | 0.0057602607 | 0.001744788 | 0.0012530082 | 0 | 0 | 0 | 0/0/0 |

The contraction checks are the finite projection inequalities:

```text
||pi_component p - pi_component q||_1
  <= ||pi_phase p - pi_phase q||_1
  <= ||p - q||_1.

||pi_*p - pi_*q||_1 <= ||p - q||_1.
```

`phase_l1` is the drift most directly aligned with the current
Lean `TransferMatrix V` state space.  The label excess terms are
stronger diagnostics.  If they do not tend to zero, they cannot be
silently absorbed into a labelled infinite operator.

The tail columns are finite source-averaged checks of the split
`K_N = K_N^{<=L} + K_N^{>L}`.  They do not provide uniform
sourcewise tail control.

## Non-Claims

This report does not prove a limiting kernel, Banach boundedness,
Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap, or
Conjecture 6.
