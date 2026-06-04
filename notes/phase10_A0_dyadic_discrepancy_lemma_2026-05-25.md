# Phase 10 A0 Dyadic Discrepancy Lemma Candidate

Date: 2026-05-25

Status: proof-route note for TODO `10.M`.  This is not a proof.

## Context

The A0 weak branch has split the finite error into:

```text
D_N <= D_N(v2 < R) + 2 * mu_N(v2 >= R).
```

Script `117` closes the second term for the current A0 source model:

```text
mu_N(v2 >= R) <= 2^-R.
```

Scripts `118`-`122` show that the open term is best stated as top
dyadic Haar decay:

```text
for every fixed low-v2 source phase p,
  ||mean_[N,2N) K_p - mean_[0,N) K_p||_1 -> 0.
```

## Candidate Lemma 1: Bounded Congruential Signatures Are Periodic

Fix:

```text
source phase p,
return-depth cutoff S,
intermediate valuation cap A,
finite destination alphabet Y.
```

Let `Phi_{p,S,A}(t)` be the truncated congruential signature vector:

```text
Phi_{p,S,A}(t) in l1(Y),
```

where the orbit is followed for at most `S` accelerated Syracuse steps and
the trace is sent to a special tail symbol as soon as any intermediate
valuation exceeds `A`.

Important restriction: this object is purely 2-adic.  It may include the
finite valuation word and symbolic congruential return labels, but it must
not include:

```text
bit-growth weights 2^-delta,
the archimedean test cur < n0.
```

Those two features require separate boundary estimates.

Candidate statement:

```text
There exists M = M(p,S,A,Y) such that
  Phi_{p,S,A}(t + 2^M) = Phi_{p,S,A}(t)
for all admissible source indices t in phase p.
```

If this holds, then for every dyadic `N` divisible by `2^M`:

```text
mean_[0,N) Phi_{p,S,A} = mean_[N,2N) Phi_{p,S,A},
```

so the top Haar coefficient of the bounded part is exactly zero, not just
small.

This is the first genuinely proof-like mechanism found in the A0 branch.
It says bounded finite-depth congruential structure cancels by exact
2-adic periodicity.

## Archimedean Caveat

The actual kernel used by scripts `77`, `119`, and `121` is not a purely
2-adic object.  It also records:

```text
delta = bit_length(next_t) - bit_length(t),
terminal/drop when cur < n0.
```

These are archimedean comparisons.  They are not periodic modulo `2^M`.
The proof route therefore needs one additional deterministic estimate:

```text
bounded congruential part: exact periodic cancellation;
archimedean delta/drop part: boundary or scale-distortion error;
tails: valuation cap and return-depth terms.
```

This correction matters.  The exact-periodic lemma should not be stated
for the full weighted kernel without extra boundary hypotheses.

## Candidate Lemma 2: Intermediate Valuation Tails

The bounded-period lemma needs a tail estimate for the event:

```text
some intermediate valuation a_i > A during the first S steps.
```

For a fixed affine congruential form with odd coefficient:

```text
u t + v,  u odd,
```

the dyadic density of:

```text
v2(u t + v) >= q
```

is exactly at most:

```text
2^-q.
```

This is the same kind of counting theorem as script `117`, but applied
to intermediate affine forms along a fixed valuation word.  A crude union
bound would give:

```text
tail_intermediate(S,A) <= S * 2^-A.
```

This looks formalizable because it is pure modular arithmetic over powers
of two.

## Candidate Lemma 3: Return-Depth Tail

The remaining hard term is not local periodicity and not high
intermediate valuations.  It is the event:

```text
no terminal/drop and no selected return before S steps.
```

The current scripts only give finite evidence that long-depth bins do not
dominate the sampled low-`v2` drift.  A proof still needs one of:

```text
1. a theorem-level return-depth tail bound,
2. a killed-kernel formulation where this mass is explicitly controlled,
3. a different target operator that avoids needing uniform return-time tails.
```

This is now the real bottleneck.

## Why Script 120 Did Not Kill This Route

Script `120` tested whether untruncated return signatures are determined
by `t mod 2^m` at moderate `m`.  It found that the majority error falls
mainly when cells become sparse.

That does not contradict Candidate Lemma 1.  The lemma says:

```text
after fixing S and A, there is some finite M(S,A).
```

It does not say `M` is small, and it does not apply to untruncated
signatures.  Script `120` was testing the too-strong version:

```text
small fixed M controls the full signature.
```

The new route is instead a double truncation:

```text
first fix S,A and get exact periodic cancellation,
then prove the S,A tails are small.
```

## Proof Skeleton

For fixed threshold `R`:

```text
D_N(v2 < R)
  <= bounded_periodic_part_N(R,S,A)
   + intermediate_valuation_tail_N(R,S,A)
   + archimedean_boundary_N(R,S,A)
   + return_depth_tail_N(R,S).
```

For dyadic `N` large enough relative to `M(R,S,A)`:

```text
bounded_periodic_part_N(R,S,A) = 0.
```

Then:

```text
limsup_N D_N(v2 < R)
  <= C_R * S * 2^-A
   + limsup_N archimedean_boundary_N(R,S,A)
   + return_depth_tail(R,S).
```

If:

```text
lim_{S -> infinity} return_depth_tail(R,S) = 0
```

and then:

```text
A -> infinity,
```

we get:

```text
D_N(v2 < R) -> 0.
```

Together with script `117`:

```text
lim_{R -> infinity} limsup_N
  [D_N(v2 < R) + 2 * mu_N(v2 >= R)] = 0.
```

## Current Honest Status

What looks close to proof:

```text
bounded finite-depth congruential signatures are eventually periodic;
high intermediate valuations have dyadic tail <= 2^-A.
```

What is still hard:

```text
archimedean delta/drop boundary estimates;
return-depth tail / unresolved killed-kernel mass.
```

So the new plan is not "we proved Collatz."  The new plan is:

```text
reduce A0W2 to one hard tail theorem,
with the bounded congruential discrepancy part killed exactly.
```

## Script 123: Bounded Periodicity Probe

Command:

```text
.venv/bin/python scripts/spectral_program/123_A0_bounded_periodicity_probe.py \
  --output-tag current_A0_large_m \
  --sample-limit 128 \
  --step-cap 25 \
  --a-cap 8 \
  --m-values 24,64,128,192,193,200
```

Outputs:

```text
scripts/spectral_program/collatz_123_current_A0_large_m_A0_bounded_periodicity_probe_report.md
scripts/spectral_program/collatz_123_current_A0_large_m_A0_bounded_periodicity_probe_rows.csv
```

The target modulus has `8` bits.  For `S=25`, `A=8`, a crude valuation-word
period upper bound is:

```text
M <= S*A + 1 - 8 = 193.
```

The finite probe confirms the corrected picture:

```text
valuation_word mismatches at m=192/193/200: 0/128 for all tested phases.
```

So the pure bounded valuation word is eventually periodic, as expected.

For symbolic returns, the large-`m` mismatch rates are small but not always
zero in the sample:

```text
0|3|0: 1/128
1|3|0: 4/128
3|1|0: 4/128
7|3|0: 0/128
```

For the actual bounded kernel, the mismatch rates remain visible:

```text
0|3|0: 6/128
1|3|0: 0/128
3|1|0: 5/128
7|3|0: 9/128
```

This is not bad news; it identifies the next missing lemma precisely.  The
pure 2-adic bounded word is periodic.  The residual bounded-kernel
movement comes from symbolic-return edge cases and archimedean
delta/drop effects.

The large return-depth tail is also visible: in `shadow_return` mode,
step/valuation tail rates are around `0.82`-`0.87` for these settings.
So `S=25` is far too small for a theorem-level return-tail bound.  The
next diagnostic should vary `S` and `A` separately and fit:

```text
valuation_tail(S,A),
return_depth_tail(S),
archimedean_boundary(S,A).
```

## Script 124: Tail Grid Probe

Command:

```text
.venv/bin/python scripts/spectral_program/124_A0_tail_grid_probe.py \
  --output-tag current_A0_spread \
  --sample-mode spread \
  --sample-limit 512 \
  --step-caps 10,25,50,75 \
  --a-caps 4,6,8,10 \
  --min-period-m 32
```

Outputs:

```text
scripts/spectral_program/collatz_124_current_A0_spread_A0_tail_grid_probe_report.md
scripts/spectral_program/collatz_124_current_A0_spread_A0_tail_grid_probe_rows.csv
```

This grid separates the pessimistic symbolic tail from the actual killed
kernel tail.  The difference is important:

```text
symbolic return tail ignores archimedean drops;
actual killed kernel maps drops to the zero row.
```

Aggregate highlights:

```text
S=75, A=10:
  valuation tail mean          = 0
  symbolic return tail mean    = 0.5
  drop mean                    = 0.5
  kernel unresolved tail mean  = 0
  word mismatch max            = 0
  kernel period mismatch mean  = 0.1821289062
```

Per tested phase at `S=75, A=10`:

```text
0|3|0: kernel tail 0, drop 0, kernel return 1, mismatch 0.40234375
1|3|0: kernel tail 0, drop 1, kernel return 0, mismatch 0
3|1|0: kernel tail 0, drop 0, kernel return 1, mismatch 0.326171875
7|3|0: kernel tail 0, drop 1, kernel return 0, mismatch 0
```

In the distributed block sample, `kernel_step_tail = 0` and
`kernel_valuation_tail = 0` for all four phases at `S=75,A=10`.  The
remaining kernel mismatch is not unresolved tail; it is a boundary in the
return weights.

This changes the bottleneck:

```text
The return-depth tail looks large only in the symbolic, non-killed model.
For the killed kernel, most long symbolic nonreturns have already dropped
below n0 and therefore contribute the zero row.
```

The current remaining terms are therefore:

```text
1. proof that killed-kernel tail control is uniform;
2. archimedean delta/weight boundary for returning phases;
3. show that the delta boundary has vanishing block-average contribution.
```

This is substantially better than the pre-124 picture.

## Script 125: Kernel Mismatch Decomposition

Command:

```text
.venv/bin/python scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py \
  --output-tag current_A0_spread \
  --sample-mode spread \
  --sample-limit 512 \
  --step-caps 25,50,75 \
  --a-caps 6,8,10 \
  --focus-step-cap 75 \
  --focus-a-cap 10
```

Outputs:

```text
scripts/spectral_program/collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_report.md
scripts/spectral_program/collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_rows.csv
scripts/spectral_program/collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_examples.csv
```

Pointwise vector convention:

```text
drop/tail          -> 0
return(dst,delta)  -> 2^-delta e_dst
```

Result:

```text
For every tested (S,A), all nonzero pointwise L1 comes from delta_only.
destination_change = 0
drop <-> return    = 0
return <-> tail    = 0
```

At `S=75,A=10`:

```text
aggregate point L1 mean = 0.02276611328
aggregate nonzero rate  = 0.1821289062

0|3|0: point L1 0.05029296875, nonzero 0.40234375, delta-only share 1
1|3|0: point L1 0,           nonzero 0,          drop phase
3|1|0: point L1 0.04077148438, nonzero 0.326171875, delta-only share 1
7|3|0: point L1 0,           nonzero 0,          drop phase
```

This is the sharpest current reduction:

```text
bounded congruential labels are periodic;
killed-kernel tail can be made zero in the tested distributed block;
the residual boundary is purely bit-length/delta weight.
```

The next theorem candidate is therefore a `delta` boundary lemma, not a
destination-mixing lemma.
