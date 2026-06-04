# Phase 10 A0 High-v2 Tail Split

Date: 2026-05-25

Status: finite tail diagnostic for script `114_A0_high_v2_tail_split.py`.

## Question

The A0 weak theorem needs to separate:

```text
mean drift: low-phase structural rows
max drift: sparse high-v2 exceptional rows
```

Script `114` quantifies the second part from the existing script-`111`
phase-strata CSV for the latest A0 comparison:

```text
T = 14, b = 0, j = 64 -> 128.
```

It does not retrace Collatz rows.

## Run

```text
python scripts/spectral_program/114_A0_high_v2_tail_split.py \
  --output-tag T14_j64_128_b0
```

Outputs:

```text
scripts/spectral_program/collatz_114_T14_j64_128_b0_A0_high_v2_tail_split_report.md
scripts/spectral_program/collatz_114_T14_j64_128_b0_A0_high_v2_tail_split_thresholds.csv
scripts/spectral_program/collatz_114_T14_j64_128_b0_A0_high_v2_tail_split_families.csv
```

## Threshold Tail

For threshold sets `{v2 >= R}`:

```text
R    tail mass       tail contribution   tail mean L1     tail max L1
4    0.0624994040    0.177370539         0.000811015      0.0331541219
6    0.0156243742    0.146462709         0.002678847      0.0331541219
8    0.0039056167    0.0680199125        0.004977026      0.0331541219
10   0.0009759273    0.0332404560        0.009733587      0.0331541219
12   0.0002435050    0.0137910747        0.016185036      0.0331541219
14   0.0000603994    0.0048224593        0.022817039      0.0331541219
```

So the high-`v2` tail has increasing row drift but rapidly vanishing source
mass.

The particular family carrying the maximum row drift is:

```text
family 14|3
mass share          = 0.0000298818
contribution share  = 0.0034667383
mean/max row L1     = 0.0331541219
```

## Low-Phase Contribution

The main average contribution is low phase:

```text
family   mass share     contribution share   mean L1
0|3      0.250000159    0.180747533          0.000206612
1|3      0.125000079    0.147116906          0.000336338
0|1      0.250000159    0.125547581          0.000143513
2|1      0.062500040    0.093366318          0.000426907
3|1      0.031250020    0.081816822          0.000748197
```

Thus the obstruction really splits:

```text
average drift: low-v2 mass families
max drift: high-v2 sparse rows
```

## Interpretation

This supports the A0 weak-bridge strategy:

```text
D_N <= D_N(v2 < R) + 2 * mu_N(v2 >= R).
```

The crude substochastic `2 * mass` bound is already small for high thresholds:

```text
v2 >= 10: 2 * mass ~= 0.00195185
v2 >= 12: 2 * mass ~= 0.00048701
v2 >= 14: 2 * mass ~= 0.00012080
```

The proof problem is therefore becoming precise:

1. prove decay of the low-`v2` part, plausibly around `N^{-1/2}`;
2. prove a uniform high-`v2` source-mass tail estimate.

This is not a Collatz proof, but it is now a mathematically clean route for
the A0 weak approximation theorem.
