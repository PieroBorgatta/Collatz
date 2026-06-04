# Phase 10 A0 Decomposition Decay

Date: 2026-05-25

Status: finite diagnostic for script `115_A0_decomposition_decay_probe.py`.

## Question

The proposed A0 proof split is:

```text
D_N <= D_N(v2 < R) + 2 * mu_N(v2 >= R).
```

Script `115` tests this split across all currently available A0 phase-strata
scales.

## Runs Used

The script consumes script-`111` A0 phase-strata CSVs:

```text
T=12, j=16 -> 32
T=12, j=32 -> 64
T=12, j=64 -> 128
T=14, j=32 -> 64
T=14, j=64 -> 128
```

These correspond to five deduplicated prefix scales:

```text
N=65536, 131072, 262144, 524288, 1048576.
```

Command:

```text
python scripts/spectral_program/115_A0_decomposition_decay_probe.py \
  --output-tag current_A0
```

Outputs:

```text
scripts/spectral_program/collatz_115_current_A0_A0_decomposition_decay_probe_report.md
scripts/spectral_program/collatz_115_current_A0_A0_decomposition_decay_probe_by_threshold_scale.csv
scripts/spectral_program/collatz_115_current_A0_A0_decomposition_decay_probe_fits.csv
```

## Main Result

For every tested threshold, the low-`v2` component decays with exponent near
`0.6`:

```text
R    low alpha    low R2
4    0.611642619  0.979894268
6    0.618811958  0.985020565
8    0.599275586  0.988012620
10   0.595091262  0.989473706
12   0.597682614  0.989794760
14   0.595226457  0.989774358
```

So the decay signal is not an artifact of one threshold.  The finite evidence
supports:

```text
D_N(v2 < R) ~= C_R N^{-0.6}
```

for fixed tested `R`.

## Tail Behavior

At fixed `R`, the high-`v2` source mass does not decay with `N`.  This is
expected: it is a source-distribution tail, not a prefix-fluctuation term.

For example, the fitted tail-mass exponents are near zero:

```text
R=10: tail_mass_alpha = -0.003395558
R=12: tail_mass_alpha = -0.013808421
R=14: tail_mass_alpha = -0.059097924
```

Therefore the proof cannot rely on:

```text
mu_N(v2 >= R) -> 0 as N -> infinity
```

for fixed `R`.

The correct structure is the double limit:

```text
first choose R large so that mu(v2 >= R) is small,
then choose N large so that D_N(v2 < R) is small.
```

Equivalently:

```text
lim_{R -> infinity} limsup_{N -> infinity}
  [D_N(v2 < R) + 2 mu_N(v2 >= R)] = 0.
```

## Latest-Scale Proof Bound

At the latest scale `N=1048576`, the proof-style bound is:

```text
R=14:
  observed total D_N      = 0.000285774472
  low component           = 0.000284396336
  tail mass               = 0.0000603994
  2 * tail mass           = 0.000120798824
  low + 2*tail_mass       = 0.000405195160
  bound / observed total  = 1.41788438
```

So `R=14` gives a reasonably tight proof-style bound at the latest scale.
Lower thresholds are much looser:

```text
R=12: bound/total = 2.69038491
R=10: bound/total = 7.79681214
R=8:  bound/total = 28.2655391
```

## Interpretation

The decomposition survives the test, with one important correction:

```text
low-v2 decay is an N-limit;
high-v2 control is an R-tail limit.
```

This is mathematically cleaner than the previous wording.  The A0 proof
target should now be:

```text
For every fixed R:
  D_N(v2 < R) <= C_R N^{-beta}

and:
  mu_N(v2 >= R) <= eps_R with eps_R -> 0 as R -> infinity.
```

The data suggest `beta` near `0.6`; a conservative theorem could aim for:

```text
beta = 1/2 - epsilon.
```

## Consequence

The A0 weak approximation theorem should replace a single tail hypothesis
with a two-parameter statement:

```text
lim_{R -> infinity} limsup_{N -> infinity}
  ||K_{2N} - K_N||_{ell_infty -> L1(mu_N; v2<R)}
  + 2 mu_N(v2>=R)
  = 0.
```

This is now the sharpest finite-to-analytic route produced by Phase 10.
