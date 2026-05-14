# Delta Obstruction Summary

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- j_count: `32`
- include boundary: `False`

## Aggregate

- groups: `131072`
- mean status majority: `0.974776`
- mean phase majority: `0.968593`
- mean delta majority: `0.951774`
- mean full majority: `0.947732`
- phase exact fraction: `0.729584`
- delta exact fraction: `0.66275`
- full exact fraction: `0.662506`
- phase exact but delta non-exact fraction: `0.0670776`
- phase exact but full non-exact fraction: `0.0670776`
- phase non-exact but delta exact fraction: `0.000244141`
- both phase and delta non-exact fraction: `0.270172`
- status+phase exact but delta non-exact groups: `8792`
- stable-status phase-majority <= 0.5 groups: `1096`

## Distinct Delta Counts

| distinct delta count | groups | fraction |
|---:|---:|---:|
| 1 | 86868 | 0.66275 |
| 2 | 22668 | 0.172943 |
| 3 | 12016 | 0.0916748 |
| 4 | 6392 | 0.0487671 |
| 5 | 2356 | 0.0179749 |
| 6 | 628 | 0.00479126 |
| 7 | 128 | 0.000976562 |
| 8 | 16 | 0.00012207 |

## Distinct Full-Signature Counts

| distinct full count | groups | fraction |
|---:|---:|---:|
| 1 | 86836 | 0.662506 |
| 2 | 18692 | 0.142609 |
| 3 | 8720 | 0.0665283 |
| 4 | 6452 | 0.0492249 |
| 5 | 3944 | 0.0300903 |
| 6 | 2312 | 0.0176392 |
| 7 | 1200 | 0.00915527 |
| 8 | 800 | 0.00610352 |
| 9 | 568 | 0.0043335 |
| 10 | 296 | 0.0022583 |
| 11 | 244 | 0.00186157 |
| 12 | 312 | 0.00238037 |
| 13 | 268 | 0.00204468 |
| 14 | 196 | 0.00149536 |
| 15 | 172 | 0.00131226 |
| 16 | 56 | 0.000427246 |
| 17 | 4 | 3.05176e-05 |

## Dominant Delta Signatures

| signature | groups | fraction |
|---|---:|---:|
| `terminal` | 120508 | 0.919403 |
| `return|2` | 3852 | 0.0293884 |
| `return|1` | 3744 | 0.0285645 |
| `return|3` | 2056 | 0.015686 |
| `return|4` | 580 | 0.00442505 |
| `return|0` | 144 | 0.00109863 |
| `return|5` | 120 | 0.000915527 |
| `return|6` | 52 | 0.000396729 |
| `return|7` | 12 | 9.15527e-05 |
| `return|8` | 4 | 3.05176e-05 |

## Worst Status+Phase Exact but Delta Non-Exact Groups

| T | r | h | phase maj | delta maj | full maj | delta distribution |
|---:|---:|---:|---:|---:|---:|---|
| 15 | 131 | 0 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 131 | 1 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 131 | 2 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 131 | 3 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 259 | 0 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 259 | 1 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 259 | 2 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 259 | 3 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 515 | 0 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 515 | 1 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 515 | 2 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 515 | 3 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 643 | 0 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 643 | 1 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 643 | 2 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |
| 15 | 643 | 3 | 1 | 0.5 | 0.5 | `return|2:0.5, return|3:0.5` |

## Worst Stable-Status Phase-Low Groups

| T | r | h | phase maj | delta maj | full maj | dominant full |
|---:|---:|---:|---:|---:|---:|---|
| 15 | 951 | 0 | 0.25 | 0.5 | 0.125 | `return|0|3|1|3` |
| 15 | 951 | 1 | 0.25 | 0.5 | 0.125 | `return|0|3|2|3` |
| 15 | 951 | 2 | 0.25 | 0.5 | 0.125 | `return|0|3|3|3` |
| 15 | 951 | 3 | 0.25 | 0.5 | 0.125 | `return|0|3|0|3` |
| 15 | 1672 | 0 | 0.25 | 0.5 | 0.125 | `return|1|1|1|4` |
| 15 | 1672 | 1 | 0.25 | 0.5 | 0.125 | `return|1|1|2|4` |
| 15 | 1672 | 2 | 0.25 | 0.5 | 0.125 | `return|1|1|3|4` |
| 15 | 1672 | 3 | 0.25 | 0.5 | 0.125 | `return|1|1|0|4` |
| 15 | 5477 | 0 | 0.25 | 0.5 | 0.125 | `return|0|3|1|2` |
| 15 | 5477 | 1 | 0.25 | 0.5 | 0.125 | `return|0|3|2|2` |
| 15 | 5477 | 2 | 0.25 | 0.5 | 0.125 | `return|0|3|3|2` |
| 15 | 5477 | 3 | 0.25 | 0.5 | 0.125 | `return|0|3|0|2` |
| 15 | 6787 | 0 | 0.25 | 0.53125 | 0.125 | `return|8|3|1|3` |
| 15 | 6787 | 1 | 0.25 | 0.53125 | 0.125 | `return|8|3|2|3` |
| 15 | 6787 | 2 | 0.25 | 0.53125 | 0.125 | `return|8|3|3|3` |
| 15 | 6787 | 3 | 0.25 | 0.53125 | 0.125 | `return|8|3|0|3` |

## Interpretation

If many groups are phase-exact but delta-non-exact, then the
remaining obstruction is primarily the weight/return exponent rather
than the destination phase.  Such evidence supports a labelled-edge
or return-signature model, not a premature phase-only operator.

These diagnostics do not imply Conjecture 6, an infinite operator, a
Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral
gap.
