# Phase 10 A0 Finite Weak Bridge

Date: 2026-05-25

Status: operational bridge note.  This does not prove Gate 10.B or Collatz.
It isolates the finite theorem that the current A0 data can actually feed.

## Decision

After the A1 source-family weighted-norm probe, the main analytic branch is:

```text
A0 phase-only averaged prefix kernels
target norm: weak averaged row-L1 / ell_infty -> L1
not target: uniform row-TV / sup-row control
```

The reason is now concrete.  The A0 phase-only drift decreases at the next
prefix scale:

```text
T=14, b=0:
  32 -> 64:   D_N = 0.000420440901
  64 -> 128:  D_N = 0.000285774472
```

The p95 and p99 decrease too.  The max row drift does not decrease, but the
max is carried by sparse high-`v2` phases with tiny sample mass.

## Finite Kernel Setup

Let `Q_N` be the finite phase alphabet.  In the current A0 run:

```text
Q_N = PhaseState
```

Let `K_N, K_{2N}: Q_N -> Q_N -> R` be the two row-source finite kernels.
For an observable `f:Q_N -> R`, define:

```text
(K_N f)(i) = sum_j K_N(i,j) f(j).
```

Let `mu_N` be the finite source weight on rows.  The measured finite drift is:

```text
D_N = sum_i mu_N(i) sum_j |K_{2N}(i,j) - K_N(i,j)|.
```

This is exactly the `weighted_l1_mean` reported by the script-`110` A0 run.

## Formal Finite Lemma

The elementary bridge is now formalized in Lean:

```text
lean/CollatzShadowing/WeakBridge.lean
```

Main theorem:

```text
weighted_action_diff_le
```

Mathematically, if `mu_N(i) >= 0` and `|f(j)| <= C`, then:

```text
sum_i mu_N(i) |(K_{2N}f)(i) - (K_N f)(i)|
  <= C * D_N.
```

So the finite diagnostic `D_N` is not just a descriptive statistic.  It is
the correct finite operator error for:

```text
ell_infty(Q_N) -> L1(mu_N).
```

This proves the finite part of the bridge.  It does not prove that `K_N`
has an infinite limit.

## Exceptional Tail Split

For substochastic rows, a row difference satisfies:

```text
sum_j |K_{2N}(i,j) - K_N(i,j)| <= 2.
```

Therefore for any exceptional row set `E_N`:

```text
D_N <= D_N(good rows) + 2 * mu_N(E_N).
```

The latest A0 tail inspection shows exactly this shape:

```text
max row source: 14|3|h
row L1:         0.0331541219
sample weight:  47 per h
```

Across the four `h` values:

```text
exceptional sample weight = 188
total sample weight       = 6291452
exceptional mass          ~= 2.98818e-5
```

So the max-row obstruction is not a mass obstruction.  It belongs in an
exceptional-source tail lemma, not in a uniform norm.

## What Remains Open

The remaining proof obligations are now sharper:

### A0-H5 Prefix Cauchy

Prove:

```text
D_N -> 0
```

for the phase-only averaged prefix kernels, in the finite weak norm above.
Current data support this, but do not prove it.

### A0-H6 Banach Bridge

Choose Banach spaces `B_s, B_w` and maps:

```text
E_N : B_s -> ell_infty(Q_N)
I_N : L1(mu_N) -> B_w
```

with constants independent of `N`:

```text
||E_N f||_infty <= C_E ||f||_{B_s}
||I_N g||_{B_w} <= C_I ||g||_{L1(mu_N)}
```

Then the Lean finite lemma gives:

```text
|| I_N (K_{2N}-K_N) E_N ||_{B_s -> B_w}
  <= C_E C_I D_N.
```

This is the exact finite-to-Banach bridge we need.

### A0-H7 Tail Control

Prove an exceptional-source estimate of the form:

```text
lim_{R -> infinity} limsup_N mu_N({v2 >= R}) = 0
```

or a weighted equivalent strong enough to absorb the rare high-`v2` rows.

This source-mass part is now proved for the current script-`111` A0 source
model by exact counting:

```text
mu_N(v2 >= R)
  = (floor((L - 1)/2^R) + floor((R' - 1)/2^R)) / (L + R' - 2)
  <= 2^-R
```

with `t=0` excluded.  The integer core is formalized in Lean as
`CollatzShadowing.WeakBridge.TailCount.dyadic_tail_count_mul_le`.

The current finite split suggests the precise form:

```text
lim_{R -> infinity} limsup_{N -> infinity}
  [D_N(v2 < R) + 2 mu_N(v2 >= R)] = 0.
```

## Consequence

The current A0 program is no longer:

```text
find a better Collatz feature
```

It is:

```text
prove D_N -> 0 in weak averaged row-L1
prove the high-v2 exceptional mass tail in the R-limit
construct E_N/I_N with uniform constants
```

Only after those three items can the finite matrices be honestly called weak
finite-rank approximants of an infinite killed weighted operator.

## Next Action

The next useful artifact is a theorem skeleton with named assumptions:

```text
A0WeakApproximationTheorem
```

whose proof is mostly the Lean lemma plus assumptions `D_N -> 0`, tail
control, and projection/inclusion bounds.  This theorem will still be
conditional, but it will tell us exactly what remains to prove and exactly
where the computations enter.
