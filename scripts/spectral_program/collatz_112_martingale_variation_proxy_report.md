# Martingale Variation Proxy

Status: finite diagnostic output only.  This report estimates
martingale-increment sizes from existing child-cylinder TV summaries.
It does not prove an infinite operator, a Lasota-Yorke inequality,
Hennion, Keller-Liverani, a spectral gap, or Collatz.

For binary child distributions `p0,p1`, the mean child deviation
from the parent average is `TV(p0,p1)`.  Therefore the `mean_tv`
column from script `100` is the natural finite proxy for
`||d_n K||_1` in the martingale-variation pair.

## Partial Variation Table

| input | level | weight | depths | mean TV by depth | raw mean sum | weighted mean sum | last/first |
|---|---|---|---|---|---:|---:|---:|
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `delta` | `none` | `0,1,2` | `0.0366330979362,0.0385126913747,0.0424966812134` | 0.117642 | 0.117642 | 1.16006 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `delta` | `theta=0.9` | `0,1,2` | `0.0366330979362,0.0385126913747,0.0424966812134` | 0.117642 | 0.13189 | 1.16006 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `delta` | `theta=0.75` | `0,1,2` | `0.0366330979362,0.0385126913747,0.0424966812134` | 0.117642 | 0.163533 | 1.16006 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `delta` | `theta=0.5` | `0,1,2` | `0.0366330979362,0.0385126913747,0.0424966812134` | 0.117642 | 0.283645 | 1.16006 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `full` | `none` | `0,1,2` | `0.0486131546989,0.0487704277039,0.0509390830994` | 0.148323 | 0.148323 | 1.04785 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `full` | `theta=0.9` | `0,1,2` | `0.0486131546989,0.0487704277039,0.0509390830994` | 0.148323 | 0.16569 | 1.04785 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `full` | `theta=0.75` | `0,1,2` | `0.0486131546989,0.0487704277039,0.0509390830994` | 0.148323 | 0.204199 | 1.04785 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `full` | `theta=0.5` | `0,1,2` | `0.0486131546989,0.0487704277039,0.0509390830994` | 0.148323 | 0.34991 | 1.04785 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `phase` | `none` | `0,1,2` | `0.0399633135114,0.0388440778179,0.0382137298584` | 0.117021 | 0.117021 | 0.95622 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `phase` | `theta=0.9` | `0,1,2` | `0.0399633135114,0.0388440778179,0.0382137298584` | 0.117021 | 0.130301 | 0.95622 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `phase` | `theta=0.75` | `0,1,2` | `0.0399633135114,0.0388440778179,0.0382137298584` | 0.117021 | 0.159691 | 0.95622 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `phase` | `theta=0.5` | `0,1,2` | `0.0399633135114,0.0388440778179,0.0382137298584` | 0.117021 | 0.270506 | 0.95622 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `status` | `none` | `0,1,2` | `0.0270171998039,0.0259775346325,0.026009051005` | 0.0790038 | 0.0790038 | 0.962685 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `status` | `theta=0.9` | `0,1,2` | `0.0270171998039,0.0259775346325,0.026009051005` | 0.0790038 | 0.0879911 | 0.962685 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `status` | `theta=0.75` | `0,1,2` | `0.0270171998039,0.0259775346325,0.026009051005` | 0.0790038 | 0.107892 | 0.962685 |
| `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.csv` | `status` | `theta=0.5` | `0,1,2` | `0.0270171998039,0.0259775346325,0.026009051005` | 0.0790038 | 0.183008 | 0.962685 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `delta` | `none` | `0,1,2,3` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097` | 0.191883 | 0.191883 | 1.32879 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `delta` | `theta=0.9` | `0,1,2,3` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097` | 0.191883 | 0.229144 | 1.32879 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `delta` | `theta=0.75` | `0,1,2,3` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097` | 0.191883 | 0.321419 | 1.32879 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `delta` | `theta=0.5` | `0,1,2,3` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097` | 0.191883 | 0.77286 | 1.32879 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `full` | `none` | `0,1,2,3` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196` | 0.225296 | 0.225296 | 1.15215 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `full` | `theta=0.9` | `0,1,2,3` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196` | 0.225296 | 0.267393 | 1.15215 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `full` | `theta=0.75` | `0,1,2,3` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196` | 0.225296 | 0.371321 | 1.15215 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `full` | `theta=0.5` | `0,1,2,3` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196` | 0.225296 | 0.876898 | 1.15215 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `phase` | `none` | `0,1,2,3` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733` | 0.166325 | 0.166325 | 0.957953 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `phase` | `theta=0.9` | `0,1,2,3` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733` | 0.166325 | 0.195779 | 0.957953 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `phase` | `theta=0.75` | `0,1,2,3` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733` | 0.166325 | 0.268141 | 0.957953 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `phase` | `theta=0.5` | `0,1,2,3` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733` | 0.166325 | 0.617046 | 0.957953 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `status` | `none` | `0,1,2,3` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306` | 0.117676 | 0.117676 | 1.0949 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `status` | `theta=0.9` | `0,1,2,3` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306` | 0.117676 | 0.139345 | 1.0949 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `status` | `theta=0.75` | `0,1,2,3` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306` | 0.117676 | 0.192838 | 1.0949 |
| `collatz_100_T15_d3_tail2_z2_cylinder_oscillation.csv` | `status` | `theta=0.5` | `0,1,2,3` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306` | 0.117676 | 0.453115 | 1.0949 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `delta` | `none` | `0,1,2,3,4` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097,0.0600595474243` | 0.251943 | 0.251943 | 1.45134 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `delta` | `theta=0.9` | `0,1,2,3,4` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097,0.0600595474243` | 0.251943 | 0.320684 | 1.45134 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `delta` | `theta=0.75` | `0,1,2,3,4` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097,0.0600595474243` | 0.251943 | 0.511237 | 1.45134 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `delta` | `theta=0.5` | `0,1,2,3,4` | `0.0413820205196,0.0452396392822,0.0502738952637,0.0549879074097,0.0600595474243` | 0.251943 | 1.73381 | 1.45134 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `full` | `none` | `0,1,2,3,4` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196,0.0648212432861` | 0.290118 | 0.290118 | 1.23192 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `full` | `theta=0.9` | `0,1,2,3,4` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196,0.0648212432861` | 0.290118 | 0.366191 | 1.23192 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `full` | `theta=0.75` | `0,1,2,3,4` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196,0.0648212432861` | 0.290118 | 0.576188 | 1.23192 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `full` | `theta=0.5` | `0,1,2,3,4` | `0.0526182113155,0.0544645309448,0.0575895309448,0.0606241226196,0.0648212432861` | 0.290118 | 1.91404 | 1.23192 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `phase` | `none` | `0,1,2,3,4` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733,0.0389356613159` | 0.205261 | 0.205261 | 0.913986 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `phase` | `theta=0.9` | `0,1,2,3,4` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733,0.0389356613159` | 0.205261 | 0.255123 | 0.913986 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `phase` | `theta=0.75` | `0,1,2,3,4` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733,0.0389356613159` | 0.205261 | 0.391197 | 0.913986 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `phase` | `theta=0.5` | `0,1,2,3,4` | `0.0425998626217,0.0418445587158,0.0410718917847,0.0408086776733,0.0389356613159` | 0.205261 | 1.24002 | 0.913986 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `status` | `none` | `0,1,2,3,4` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306,0.0308465957642` | 0.148523 | 0.148523 | 1.07863 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `status` | `theta=0.9` | `0,1,2,3,4` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306,0.0308465957642` | 0.148523 | 0.18636 | 1.07863 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `status` | `theta=0.75` | `0,1,2,3,4` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306,0.0308465957642` | 0.148523 | 0.290328 | 1.07863 |
| `collatz_100_T15_d4_tail1_z2_cylinder_oscillation.csv` | `status` | `theta=0.5` | `0,1,2,3,4` | `0.0285980163082,0.0285217285156,0.0292442866734,0.0313119888306,0.0308465957642` | 0.148523 | 0.94666 | 1.07863 |

## Interpretation

A useful martingale Banach pair needs summable increments after the
chosen weights `a_n` are applied.  On the currently available
finite windows, the full and delta mean increments do not yet show
decay across depth; in several runs they increase.  The phase
increments are only nearly flat/slightly decreasing on the tested
windows, not remotely summable at these depths.  This is negative
pressure on exponential weights `a_n = theta^{-n}` unless a later
stratification, state enrichment, or retained-kernel reformulation
changes the increment profile.

The result is not a disproof: the available depths are shallow, the
sample windows are finite, and the measured signature kernel is not
yet proved to be `E_N U_ret,s I_N`.  It is, however, the right
finite quantity to monitor before invoking Hennion or
Keller-Liverani.
