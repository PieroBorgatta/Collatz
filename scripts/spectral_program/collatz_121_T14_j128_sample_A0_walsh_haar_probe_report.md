# A0 Walsh-Haar Probe

Status: finite Walsh-Haar diagnostic for A0W2 / TODO 10.M.

## Scope

- T: `14`
- j_count: `128`
- phases: `0|3|0,7|3|0`
- filters: `return,medium_return`
- signature levels: `phase,phase_delta`
- output CSV: `collatz_121_T14_j128_sample_A0_walsh_haar_probe_by_scale.csv`

## Root Coefficients

| phase | filter | level | samples | support | root half L1 | prefix L1 | L2 energy share |
|---|---|---|---:|---:|---:|---:|---:|
| `0|3|0` | `medium_return` | `phase` | 524288 | 27 | 0.0004286766052 | 0.0002143383026 | 9.644526453e-07 |
| `0|3|0` | `medium_return` | `phase_delta` | 524288 | 44 | 0.0004897117615 | 0.0002448558807 | 8.438230058e-07 |
| `0|3|0` | `return` | `phase` | 524288 | 30 | 0.0004132239847 | 0.0002066119923 | 4.697326978e-07 |
| `0|3|0` | `return` | `phase_delta` | 524288 | 93 | 0.0005805996479 | 0.000290299824 | 5.63120821e-07 |
| `7|3|0` | `medium_return` | `phase` | 4096 | 14 | 0.007080078125 | 0.003540039062 | 0.0005245318846 |
| `7|3|0` | `medium_return` | `phase_delta` | 4096 | 16 | 0.007080078125 | 0.003540039062 | 0.0002969288217 |
| `7|3|0` | `return` | `phase` | 4096 | 16 | 0.007874965668 | 0.003937482834 | 0.0003515026846 |
| `7|3|0` | `return` | `phase_delta` | 4096 | 34 | 0.008344173431 | 0.004172086716 | 0.0002071084438 |

## Largest L2 Haar Energy Shares

| rank | phase | filter | level | block size | nodes | weighted L1 variation | L2 share |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | `7|3|0` | `return` | `phase` | 2 | 2048 | 0.04906320572 | 0.5029457426 |
| 2 | `7|3|0` | `return` | `phase_delta` | 2 | 2048 | 0.04906320572 | 0.5011534211 |
| 3 | `0|3|0` | `medium_return` | `phase` | 2 | 262144 | 0.01763105392 | 0.5003564349 |
| 4 | `0|3|0` | `return` | `phase_delta` | 2 | 262144 | 0.04218265146 | 0.5000771623 |
| 5 | `0|3|0` | `medium_return` | `phase_delta` | 2 | 262144 | 0.01763486862 | 0.5000406544 |
| 6 | `0|3|0` | `return` | `phase` | 2 | 262144 | 0.0420423086 | 0.4999157361 |
| 7 | `7|3|0` | `medium_return` | `phase` | 2 | 2048 | 0.02587890625 | 0.4989883521 |
| 8 | `7|3|0` | `medium_return` | `phase_delta` | 2 | 2048 | 0.02587890625 | 0.4979400784 |
| 9 | `7|3|0` | `return` | `phase_delta` | 4 | 1024 | 0.04942941666 | 0.254066188 |
| 10 | `7|3|0` | `medium_return` | `phase_delta` | 4 | 1024 | 0.02612304688 | 0.2533188609 |
| 11 | `0|3|0` | `return` | `phase_delta` | 4 | 131072 | 0.04204794497 | 0.2510483669 |
| 12 | `0|3|0` | `return` | `phase` | 4 | 131072 | 0.04157893464 | 0.2503658379 |
| 13 | `0|3|0` | `medium_return` | `phase` | 4 | 131072 | 0.0176024437 | 0.2501782174 |
| 14 | `0|3|0` | `medium_return` | `phase_delta` | 4 | 131072 | 0.01761293411 | 0.2500999098 |
| 15 | `7|3|0` | `return` | `phase` | 4 | 1024 | 0.04906320572 | 0.2497218927 |
| 16 | `7|3|0` | `medium_return` | `phase` | 4 | 1024 | 0.02575683594 | 0.2451361992 |

## Coarse-Scale Tail

| phase | filter | level | block size | nodes | weighted L1 variation | L2 share |
|---|---|---|---:|---:|---:|---:|
| `0|3|0` | `medium_return` | `phase` | 8192 | 64 | 0.003668308258 | 0.0001179042947 |
| `0|3|0` | `medium_return` | `phase` | 16384 | 32 | 0.002651691437 | 6.135096453e-05 |
| `0|3|0` | `medium_return` | `phase` | 32768 | 16 | 0.001849651337 | 2.84432046e-05 |
| `0|3|0` | `medium_return` | `phase` | 65536 | 8 | 0.001904964447 | 3.744393533e-05 |
| `0|3|0` | `medium_return` | `phase` | 131072 | 4 | 0.0020403862 | 4.822944478e-05 |
| `0|3|0` | `medium_return` | `phase` | 262144 | 2 | 0.002029895782 | 5.167240081e-05 |
| `0|3|0` | `medium_return` | `phase` | 524288 | 1 | 0.0004286766052 | 9.644526453e-07 |
| `0|3|0` | `medium_return` | `phase_delta` | 8192 | 64 | 0.004813671112 | 0.0001296706351 |
| `0|3|0` | `medium_return` | `phase_delta` | 16384 | 32 | 0.003451824188 | 5.896117909e-05 |
| `0|3|0` | `medium_return` | `phase_delta` | 32768 | 16 | 0.002384662628 | 2.769430419e-05 |
| `0|3|0` | `medium_return` | `phase_delta` | 65536 | 8 | 0.002273082733 | 2.576786445e-05 |
| `0|3|0` | `medium_return` | `phase_delta` | 131072 | 4 | 0.002279758453 | 3.144745649e-05 |
| `0|3|0` | `medium_return` | `phase_delta` | 262144 | 2 | 0.002190113068 | 3.092562174e-05 |
| `0|3|0` | `medium_return` | `phase_delta` | 524288 | 1 | 0.0004897117615 | 8.438230058e-07 |
| `0|3|0` | `return` | `phase` | 8192 | 64 | 0.004421043326 | 9.849208682e-05 |
| `0|3|0` | `return` | `phase` | 16384 | 32 | 0.003436319414 | 6.820829728e-05 |
| `0|3|0` | `return` | `phase` | 32768 | 16 | 0.002594658989 | 4.49244291e-05 |
| `0|3|0` | `return` | `phase` | 65536 | 8 | 0.003633240121 | 9.699175568e-05 |
| `0|3|0` | `return` | `phase` | 131072 | 4 | 0.004072887008 | 0.000134209861 |
| `0|3|0` | `return` | `phase` | 262144 | 2 | 0.004345226916 | 0.0001759644167 |
| `0|3|0` | `return` | `phase` | 524288 | 1 | 0.0004132239847 | 4.697326978e-07 |
| `0|3|0` | `return` | `phase_delta` | 8192 | 64 | 0.006243923563 | 0.0001054101517 |
| `0|3|0` | `return` | `phase_delta` | 16384 | 32 | 0.004801163566 | 6.162412071e-05 |
| `0|3|0` | `return` | `phase_delta` | 32768 | 16 | 0.003836868447 | 4.152753123e-05 |
| `0|3|0` | `return` | `phase_delta` | 65536 | 8 | 0.004744378966 | 6.951323339e-05 |
| `0|3|0` | `return` | `phase_delta` | 131072 | 4 | 0.005165136536 | 8.928850972e-05 |
| `0|3|0` | `return` | `phase_delta` | 262144 | 2 | 0.00524338719 | 0.0001136825628 |
| `0|3|0` | `return` | `phase_delta` | 524288 | 1 | 0.0005805996479 | 5.63120821e-07 |
| `7|3|0` | `medium_return` | `phase` | 64 | 64 | 0.02197265625 | 0.0174319075 |
| `7|3|0` | `medium_return` | `phase` | 128 | 32 | 0.01928710938 | 0.007229248096 |
| `7|3|0` | `medium_return` | `phase` | 256 | 16 | 0.01794433594 | 0.006724222131 |
| `7|3|0` | `medium_return` | `phase` | 512 | 8 | 0.01379394531 | 0.002692526077 |
| `7|3|0` | `medium_return` | `phase` | 1024 | 4 | 0.00927734375 | 0.0009816796866 |
| `7|3|0` | `medium_return` | `phase` | 2048 | 2 | 0.007202148438 | 0.0005312702928 |
| `7|3|0` | `medium_return` | `phase` | 4096 | 1 | 0.007080078125 | 0.0005245318846 |
| `7|3|0` | `medium_return` | `phase_delta` | 64 | 64 | 0.02209472656 | 0.01503967486 |
| `7|3|0` | `medium_return` | `phase_delta` | 128 | 32 | 0.01940917969 | 0.006851659103 |
| `7|3|0` | `medium_return` | `phase_delta` | 256 | 16 | 0.01892089844 | 0.005849391614 |
| `7|3|0` | `medium_return` | `phase_delta` | 512 | 8 | 0.01428222656 | 0.00257361906 |
| `7|3|0` | `medium_return` | `phase_delta` | 1024 | 4 | 0.01037597656 | 0.0009116670377 |
| `7|3|0` | `medium_return` | `phase_delta` | 2048 | 2 | 0.00732421875 | 0.0004565413349 |
| `7|3|0` | `medium_return` | `phase_delta` | 4096 | 1 | 0.007080078125 | 0.0002969288217 |
| `7|3|0` | `return` | `phase` | 64 | 64 | 0.03797006607 | 0.01694147839 |
| `7|3|0` | `return` | `phase` | 128 | 32 | 0.03185510635 | 0.008034170131 |
| `7|3|0` | `return` | `phase` | 256 | 16 | 0.02404642105 | 0.005244127343 |
| `7|3|0` | `return` | `phase` | 512 | 8 | 0.01904916763 | 0.002385437361 |
| `7|3|0` | `return` | `phase` | 1024 | 4 | 0.01216268539 | 0.0009024313127 |
| `7|3|0` | `return` | `phase` | 2048 | 2 | 0.008691310883 | 0.0003979720648 |
| `7|3|0` | `return` | `phase` | 4096 | 1 | 0.007874965668 | 0.0003515026846 |
| `7|3|0` | `return` | `phase_delta` | 64 | 64 | 0.03948068619 | 0.01571727134 |
| `7|3|0` | `return` | `phase_delta` | 128 | 32 | 0.03363656998 | 0.007622439963 |
| `7|3|0` | `return` | `phase_delta` | 256 | 16 | 0.02640390396 | 0.004543554464 |
| `7|3|0` | `return` | `phase_delta` | 512 | 8 | 0.02098703384 | 0.002044686454 |
| `7|3|0` | `return` | `phase_delta` | 1024 | 4 | 0.01419305801 | 0.0007682820904 |
| `7|3|0` | `return` | `phase_delta` | 2048 | 2 | 0.009924411774 | 0.0003303118118 |
| `7|3|0` | `return` | `phase_delta` | 4096 | 1 | 0.008344173431 | 0.0002071084438 |

## Interpretation

The root row is the adjacent half-block discrepancy; half of it is the
script-111 prefix drift for the same phase/filter/level.  A promising
Walsh-Haar proof route would show that coarse-scale coefficients decay
for fixed low-v2 phases, while high-frequency energy remains harmless
under prefix averaging.
