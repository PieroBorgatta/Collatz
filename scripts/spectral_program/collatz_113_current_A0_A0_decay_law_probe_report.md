# A0 Decay Law Probe

Status: finite trend fit only.  This does not prove `D_N -> 0`.

## Scope

- input glob: `collatz_110_*_refined_square_probe_by_pair.csv`
- raw A0 points: `10`
- deduped scales: `5`
- output CSV: `collatz_113_current_A0_A0_decay_law_probe_points.csv`

## Fit

Model:

```text
D_N ~= c N^{-alpha}
```

| metric | value |
|---|---:|
| `count` | `5` |
| `alpha` | `0.594000397` |
| `c` | `1.07934526` |
| `log_c` | `0.0763546189` |
| `r2` | `0.989858124` |

Local consecutive exponents:

| N_i -> N_{i+1} | local alpha |
|---:|---:|
| 65536 -> 131072 | 0.337498454 |
| 131072 -> 262144 | 0.761634381 |
| 262144 -> 524288 | 0.622017321 |
| 524288 -> 1048576 | 0.557025976 |

Local alpha summary:

| metric | value |
|---|---:|
| `min` | `0.337498454` |
| `median` | `0.589521649` |
| `max` | `0.761634381` |

Leave-one-out fits:

| omitted N | alpha | R2 |
|---:|---:|---:|
| 65536 | 0.644405036 | 0.994851737 |
| 131072 | 0.571758588 | 0.999468194 |
| 262144 | 0.594000397 | 0.989907624 |
| 524288 | 0.588292076 | 0.988939116 |
| 1048576 | 0.592508485 | 0.979832865 |

Leave-one-out alpha summary:

| metric | value |
|---|---:|
| `min` | `0.571758588` |
| `median` | `0.592508485` |
| `max` | `0.644405036` |

## Points

| N -> 2N | D_N | p95 | p99 | max | replicates | predicted | obs/pred |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 65536 -> 131072 | 0.00138619007 | 0.00243425369 | 0.0104980469 | 0.12890625 | 2 | 0.00148651535 | 0.932509755 |
| 131072 -> 262144 | 0.00109704799 | 0.00252437592 | 0.00359725952 | 0.080078125 | 3 | 0.000984821366 | 1.11395632 |
| 262144 -> 524288 | 0.000647069352 | 0.00109326839 | 0.00365161896 | 0.0556640625 | 2 | 0.000652447431 | 0.991757069 |
| 524288 -> 1048576 | 0.000420440901 | 0.000633001328 | 0.00498771667 | 0.0309139785 | 2 | 0.000432248593 | 0.972683099 |
| 1048576 -> 2097152 | 0.000285774472 | 0.00056168437 | 0.00205135345 | 0.0331541219 | 1 | 0.000286366131 | 0.997933908 |

## Interpretation

- Positive `alpha` is finite evidence for decay of the weak A0 drift.
- High `r2` on few points is not a theorem and can be misleading.
- The max column is tracked separately because the target is weak averaged control.
