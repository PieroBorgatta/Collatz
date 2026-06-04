# A0 Decomposition Decay Probe

Status: finite diagnostic only.  This does not prove the A0 theorem.

## Scope

- input glob: `collatz_111_*_b0_refined_square_key_drift_phase_strata.csv`
- deduped cases: `5`
- thresholds: `4,6,8,10,12,14`
- by-scale CSV: `collatz_115_current_A0_A0_decomposition_decay_probe_by_threshold_scale.csv`
- fits CSV: `collatz_115_current_A0_A0_decomposition_decay_probe_fits.csv`

## Cases

| N -> 2N | T | j pair | total D | max row L1 |
|---:|---:|---:|---:|---:|
| 65536 -> 131072 | 12 | 16->32 | 0.00138555428 | 0.12890625 |
| 131072 -> 262144 | 12 | 32->64 | 0.0010970601 | 0.080078125 |
| 262144 -> 524288 | 12 | 64->128 | 0.000647280889 | 0.0556640625 |
| 524288 -> 1048576 | 14 | 32->64 | 0.000420440901 | 0.0309139785 |
| 1048576 -> 2097152 | 14 | 64->128 | 0.000285774472 | 0.0331541219 |

## Threshold Summary

| rank | R | low alpha | low R2 | tail-mass alpha | latest low | latest tail mass | latest 2mass | bound/total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 14 | 0.595226457 | 0.989774358 | -0.0590979239 | 0.000284396336 | 6.03994118e-05 | 0.000120798824 | 1.41788438 |
| 2 | 12 | 0.597682614 | 0.98979476 | -0.0138084207 | 0.000281833335 | 0.000243504997 | 0.000487009994 | 2.69038491 |
| 3 | 10 | 0.595091262 | 0.989473706 | -0.00339555825 | 0.000276275198 | 0.000975927338 | 0.00195185468 | 7.79681214 |
| 4 | 8 | 0.599275586 | 0.98801262 | -0.000843118072 | 0.000266336118 | 0.0039056167 | 0.0078112334 | 28.2655391 |
| 5 | 6 | 0.618811958 | 0.985020565 | -0.000208098303 | 0.000243919169 | 0.0156243742 | 0.0312487483 | 110.201122 |
| 6 | 4 | 0.611642619 | 0.979894268 | -4.9535242e-05 | 0.0002350865 | 0.062499404 | 0.124998808 | 438.226317 |

## Reading Rule

- `low alpha` estimates decay of `D_N(v2 < R)`.
- `tail-mass alpha` estimates decay of the exceptional source mass for fixed R.
- `bound/total` compares the proof-style bound to the observed total at the latest scale.
- A useful threshold has a decaying low part and a not-too-loose tail bound.
