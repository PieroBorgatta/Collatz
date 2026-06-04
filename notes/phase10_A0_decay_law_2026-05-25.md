# Phase 10 A0 Decay Law Probe

Date: 2026-05-25

Status: finite trend diagnostic for script `113_A0_decay_law_probe.py`.

## Question

The A0 weak bridge reduces the finite analytic input to the phase-only
prefix drift:

```text
D_N = sum_i mu_N(i) sum_j |K_{2N}(i,j) - K_N(i,j)|.
```

The next question is whether the available `D_N` values are compatible with
a decay law:

```text
D_N ~= c N^{-alpha}.
```

This does not prove `D_N -> 0`; it only tests whether the finite data have a
stable decay signature.

## Run

```text
python scripts/spectral_program/113_A0_decay_law_probe.py \
  --output-tag current_A0
```

Outputs:

```text
scripts/spectral_program/collatz_113_current_A0_A0_decay_law_probe_report.md
scripts/spectral_program/collatz_113_current_A0_A0_decay_law_probe_points.csv
```

The script consumes existing script-`110` by-pair CSVs and deduplicates
equivalent prefix scales by:

```text
N = j_left * 2^T.
```

## Fit Result

Using five deduplicated A0 scales:

```text
D_N ~= c N^{-alpha}

alpha = 0.594000397
c     = 1.07934526
R^2   = 0.989858124
```

The points are:

```text
N=65536:    D_N = 0.00138619007
N=131072:   D_N = 0.00109704799
N=262144:   D_N = 0.000647069352
N=524288:   D_N = 0.000420440901
N=1048576:  D_N = 0.000285774472
```

## Robustness Checks

Local consecutive exponents:

```text
65536 -> 131072:    alpha = 0.337498454
131072 -> 262144:   alpha = 0.761634381
262144 -> 524288:   alpha = 0.622017321
524288 -> 1048576:  alpha = 0.557025976
```

Local summary:

```text
min    = 0.337498454
median = 0.589521649
max    = 0.761634381
```

Leave-one-out alpha range:

```text
min    = 0.571758588
median = 0.592508485
max    = 0.644405036
```

So the global exponent is not caused by one isolated point.  The earliest
local slope is noisy, but the leave-one-out fits are stable around `0.6`.

## Interpretation

This is currently the best finite evidence for A0W2:

```text
D_N -> 0.
```

The empirically suggested rate is:

```text
D_N = O(N^{-0.59})
```

or conservatively:

```text
D_N = O(N^{-1/2})
```

at the tested scales.

The latter is especially interesting because `N^{-1/2}` is the natural
Monte-Carlo/Cesaro fluctuation scale.  That means the observed decay may be
evidence of averaging stability rather than a deep deterministic contraction.
This is still useful for the weak A0 bridge, but it warns against overselling
the result as a spectral gap.

## Consequence

The proof target should be sharpened from:

```text
prove D_N -> 0
```

to something like:

```text
prove D_N <= C N^{-beta}
```

for some `beta > 0`, probably first with `beta = 1/2 - epsilon` or an
exceptional-tail version.

The finite data now support using `D_N` as the numerical term in the
conditional `A0WeakApproximationTheorem`, but they do not establish the
analytic Cauchy theorem.

## Next Step

The next useful mathematical/computational task is to separate the decay into
two components:

```text
low-phase structural rows: expected smooth N^{-alpha} decay
high-v2 exceptional rows: small source mass, nonuniform max
```

This would turn the current empirical fit into a candidate proof strategy:

```text
D_N <= D_N(low phase) + 2 * mu_N(high-v2 tail).
```
