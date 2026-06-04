# A0 Top Haar Decay Summary

Status: finite diagnostic for TODO `10.M`; not a proof.

## Scope

- input glob: `collatz_111_*_b0_refined_square_key_drift_phase_strata.csv`
- cases after dedupe: `5`
- latest case: `collatz_111_T14_j64_128_b0_refined_square_key_drift_phase_strata.csv`
- phase fits CSV: `collatz_122_current_A0_A0_top_haar_decay_summary_phase_fits.csv`
- threshold fits CSV: `collatz_122_current_A0_A0_top_haar_decay_summary_threshold_fits.csv`
- case points CSV: `collatz_122_current_A0_A0_top_haar_decay_summary_case_points.csv`

## Identity Used

For the A0 phase rows tested in scripts `119` and `121`:

```text
root_haar_l1(N) = ||mean_[N,2N) - mean_[0,N)||_1
                = 2 * prefix_row_l1(N).
```

So the fitted exponent is unchanged from script `118`, but the
quantity is now exactly the top dyadic block-discrepancy coefficient.

## Threshold Fits

| v2 cutoff | phases latest | points | alpha | R2 | latest root component | share of total root |
|---:|---:|---:|---:|---:|---:|---:|
| < 4 | 32 | 5 | 0.6116426187 | 0.9798942684 | 0.0004701730001 | 0.8226294611 |
| < 6 | 48 | 5 | 0.6188119578 | 0.9850205647 | 0.0004878383379 | 0.8535372915 |
| < 8 | 64 | 5 | 0.5992755856 | 0.9880126202 | 0.0005326722352 | 0.9319800875 |
| < 10 | 80 | 5 | 0.5950912623 | 0.9894737055 | 0.0005525503968 | 0.966759544 |
| < 12 | 96 | 5 | 0.5976826136 | 0.9897947604 | 0.0005636666702 | 0.9862089253 |
| < 14 | 112 | 5 | 0.5952264566 | 0.9897743576 | 0.0005687926729 | 0.9951775407 |

## Dominant Latest Low-v2 Phases

Low-v2 report cutoff: `v2 < 8`.

| rank | phase | alpha | latest root Haar L1 | latest root component | share |
|---:|---|---:|---:|---:|---:|
| 1 | `0|3|0` | 0.5332466934 | 0.0004132239847 | 2.582651546e-05 | 0.04518688332 |
| 2 | `0|3|1` | 0.5332466934 | 0.0004132239847 | 2.582651546e-05 | 0.04518688332 |
| 3 | `0|3|2` | 0.5332466934 | 0.0004132239847 | 2.582651546e-05 | 0.04518688332 |
| 4 | `0|3|3` | 0.5332466934 | 0.0004132239847 | 2.582651546e-05 | 0.04518688332 |
| 5 | `1|3|0` | 0.6054982365 | 0.0006726756692 | 2.102112803e-05 | 0.03677922641 |
| 6 | `1|3|1` | 0.6054982365 | 0.0006726756692 | 2.102112803e-05 | 0.03677922641 |
| 7 | `1|3|2` | 0.6054982365 | 0.0006726756692 | 2.102112803e-05 | 0.03677922641 |
| 8 | `1|3|3` | 0.6054982365 | 0.0006726756692 | 2.102112803e-05 | 0.03677922641 |
| 9 | `0|1|0` | 0.6169149642 | 0.0002870261669 | 1.793914684e-05 | 0.03138689523 |
| 10 | `0|1|1` | 0.6169149642 | 0.0002870261669 | 1.793914684e-05 | 0.03138689523 |
| 11 | `0|1|2` | 0.6169149642 | 0.0002870261669 | 1.793914684e-05 | 0.03138689523 |
| 12 | `0|1|3` | 0.6169149642 | 0.0002870261669 | 1.793914684e-05 | 0.03138689523 |
| 13 | `2|1|0` | 0.6976992227 | 0.0008538141847 | 1.334085512e-05 | 0.02334157949 |
| 14 | `2|1|1` | 0.6976992227 | 0.0008538141847 | 1.334085512e-05 | 0.02334157949 |
| 15 | `2|1|2` | 0.6976992227 | 0.0008538141847 | 1.334085512e-05 | 0.02334157949 |
| 16 | `2|1|3` | 0.6976992227 | 0.0008538141847 | 1.334085512e-05 | 0.02334157949 |

## Slowest Low-v2 Phase Fits

| rank | phase | alpha | local alpha median | latest root component | share |
|---:|---|---:|---:|---:|---:|
| 1 | `7|3|0` | 0.2298668295 | 0.157396403 | 3.845200525e-06 | 0.006727683714 |
| 2 | `7|3|1` | 0.2298668295 | 0.157396403 | 3.845200525e-06 | 0.006727683714 |
| 3 | `7|3|2` | 0.2298668295 | 0.157396403 | 3.845200525e-06 | 0.006727683714 |
| 4 | `7|3|3` | 0.2298668295 | 0.157396403 | 3.845200525e-06 | 0.006727683714 |
| 5 | `7|1|0` | 0.3420981079 | 0.7056815399 | 3.356721524e-06 | 0.005873025498 |
| 6 | `7|1|1` | 0.3420981079 | 0.7056815399 | 3.356721524e-06 | 0.005873025498 |
| 7 | `7|1|2` | 0.3420981079 | 0.7056815399 | 3.356721524e-06 | 0.005873025498 |
| 8 | `7|1|3` | 0.3420981079 | 0.7056815399 | 3.356721524e-06 | 0.005873025498 |
| 9 | `6|1|0` | 0.406412087 | 0.5063855406 | 4.006552263e-06 | 0.007009989788 |
| 10 | `6|1|1` | 0.406412087 | 0.5063855406 | 4.006552263e-06 | 0.007009989788 |
| 11 | `6|1|2` | 0.406412087 | 0.5063855406 | 4.006552263e-06 | 0.007009989788 |
| 12 | `6|1|3` | 0.406412087 | 0.5063855406 | 4.006552263e-06 | 0.007009989788 |
| 13 | `3|1|0` | 0.4142787183 | 0.2735791375 | 1.169057957e-05 | 0.02045420551 |
| 14 | `3|1|1` | 0.4142787183 | 0.2735791375 | 1.169057957e-05 | 0.02045420551 |
| 15 | `3|1|2` | 0.4142787183 | 0.2735791375 | 1.169057957e-05 | 0.02045420551 |
| 16 | `3|1|3` | 0.4142787183 | 0.2735791375 | 1.169057957e-05 | 0.02045420551 |

## Aggregate Low-v2 Signal

| metric | value |
|---|---:|
| low phase count | `64` |
| fit-qualified low phase count | `48` |
| median low phase alpha | `0.6112066004` |
| min low phase alpha | `0.2298668295` |
| max low phase alpha | `0.7372606636` |

## Theorem-Oriented Reading

For fixed `R`, there are finitely many phases with `v2 < R`.
If each such phase has vanishing top Haar coefficient, then the
weighted low-`v2` block discrepancy vanishes:

```text
D_N(v2 < R) -> 0.
```

Together with the exact high-`v2` source-tail count from script `117`,
this is the current A0 weak-bridge proof target.  The present data
support power-law decay near alpha ~= 0.6 for aggregate thresholds,
but a proof still requires a structural dyadic discrepancy lemma.
