# A0 v2 Tail Formula

Status: exact finite source-count check for script-111 A0 phase strata.

## Scope

- input glob: `collatz_111_*_b0_refined_square_key_drift_phase_strata.csv`
- thresholds: `4,6,8,10,12,14`
- cases used after dedupe: `5`
- output CSV: `collatz_117_current_A0_A0_v2_tail_formula_by_scale.csv`

## Exact Count Lemma

For a script-111 A0 comparison with

```text
L = j_left  * 2^T
R = j_right * 2^T
```

and with `t=0` excluded, the phase source tail is exactly

```text
mu({phase_v2 >= q})
  = (floor((L - 1)/2^q) + floor((R - 1)/2^q)) / (L + R - 2)
  <= 2^-q.
```

The factor from the hit coordinate cancels from numerator and denominator.

## Verification

| metric | value |
|---|---:|
| max absolute observed-formula error | `0` |
| max formula / 2^-q | `0.9999904633` |
| min dyadic slack | `5.960468267e-07` |
| mean h_mod | `4` |

## Latest Scale by Threshold

| q | N_left | observed tail | formula tail | 2^-q | formula/bound |
|---:|---:|---:|---:|---:|---:|
| 4 | 1048576 | 0.06249940395 | 0.06249940395 | 0.0625 | 0.9999904633 |
| 6 | 1048576 | 0.01562437415 | 0.01562437415 | 0.015625 | 0.9999599457 |
| 8 | 1048576 | 0.0039056167 | 0.0039056167 | 0.00390625 | 0.9998378753 |
| 10 | 1048576 | 0.0009759273376 | 0.0009759273376 | 0.0009765625 | 0.9993495937 |
| 12 | 1048576 | 0.0002435049969 | 0.0002435049969 | 0.000244140625 | 0.9973964675 |
| 14 | 1048576 | 6.039941177e-05 | 6.039941177e-05 | 6.103515625e-05 | 0.9895839625 |

## Interpretation

This proves the high-v2 mass part of the A0 weak decomposition for the
current finite source model.  The remaining hard part is the structural
low-v2 decay:

```text
D_N(v2 < q) -> 0
```

The tail no longer needs to be fitted: it is a counting lemma.
