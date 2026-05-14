# Phase 10 Conditional Refined Kernel

Date: 2026-05-14

Status: conditional model skeleton.  This note defines the next
candidate object after the failure of exact local constancy on the
current `PhaseState` quotient.  It does not assert that the required
limits exist.

## 1. Inputs

Fix:

```text
T >= 1,
a >= 0,
H = Z / 2^m_hit Z,
q in Z / 2^a Z.
```

Write source lifts as:

```text
t = r + (q + 2^a k) * 2^T,
k = 0,1,2,...
```

Equivalently:

```text
t == r + q * 2^T mod 2^(T+a).
```

The diagnostic value `a = 5` corresponds to the observed `j mod 32`
coordinate.

## 2. Transition Observables

For a traced row starting from `(t,h)`, define:

```text
status(t,h) in {terminal, return},
phase(t,h)  in PhaseState V union {terminal},
delta(t,h)  in Z union {terminal},
full(t,h)   = terminal or (phase(t,h), delta(t,h)).
```

Here `delta` is the archimedean bit-length exponent currently used by
the scripts:

```text
delta = bit_length(t') - bit_length(t).
```

This is the main non-2-adic observable and must be treated as an edge
label unless branch-measurability is proved.

## 3. Empirical Refined Kernel

For finite prefix `N`, define:

```text
K_{T,a,N}(r,q,h; terminal)
  = (1/N) # { 0 <= k < N : status(t,h) = terminal }.
```

For return transitions:

```text
K_{T,a,N}(r,q,h; d, ell)
  = (1/N) # { 0 <= k < N :
        status(t,h) = return,
        phase(t,h) = d,
        delta(t,h) = ell }.
```

A weighted version uses:

```text
W_{T,a,N}(r,q,h; d, ell)
  = (1/N) sum 2^(-s ell)
```

over the same returning lifts.

This is an empirical labelled kernel, not yet an operator on a Banach
space.

## 4. Candidate Limits

The weakest useful limit is pointwise Cesaro convergence:

```text
K_{T,a}(r,q,h; y)
  = lim_{N -> infinity} K_{T,a,N}(r,q,h; y)
```

for each terminal/labelled destination `y`.

The stronger useful limit for operator approximation is a uniform or
weighted-tail version:

```text
sup_{source in bounded test set}
  ||K_{T,a,N}(source,.) - K_{T,a}(source,.)||_variation -> 0,
```

plus a tail estimate outside the bounded test set.

## 5. Refinement in `a`

The diagnostics suggest a hierarchy:

```text
a = 0  : current base cylinder,
a = 5  : first serious phase refinement,
a > 5  : residual phase refinement.
```

A plausible projection program would need:

```text
phase_tail(a) -> 0
```

where `phase_tail(a)` measures the mass of source cells whose
destination phase is not concentrated after depth increment `a`.

For the full weighted operator, one also needs:

```text
delta_tail(a,L) -> 0
```

where `L` bounds the retained delta labels and the tail is weighted by
`2^{-s delta}` or by the chosen Banach-space drift weight.

The current finite diagnostic separates two non-equivalent versions:

```text
delta_tail_global(a,L)
  = weighted mass of {delta > L}
    / total weighted return mass,
```

and

```text
delta_tail_local(a,L)
  = source-cell tail ratio for {delta > L}.
```

For `T = 16`, `j_count = 8`, script
`93_delta_tail_weight.py` found:

- `delta_tail_global(.,4) = 0.00412187`;
- `delta_tail_global(.,5) = 0.000862882`;
- `delta_tail_global(.,8) = 0.00000574087`;
- local p95 at `L = 4` is still `1`, while local p95 at `L = 5` is
  `0.047619`.

For `T = 15`, `j_count = 32`, the corresponding global tails are:

- `delta_tail_global(.,4) = 0.0040648`;
- `delta_tail_global(.,5) = 0.000845196`;
- `delta_tail_global(.,8) = 0.00000635292`;
- local p95 at `L = 4` is `0.2`, while local p95 at `L = 5` is
  `0.0379747`.

Thus a global tail estimate is plausible on the tested window, but a
uniform cellwise estimate remains a separate and stronger hypothesis.

## 6. Conditional Gate 10.B Proposition

Conditional proposition:

Assume there exist:

1. a depth sequence `a_n -> infinity`;
2. labelled kernels `K_{T,a_n}` obtained as Cesaro or Haar limits;
3. a Banach pair `B_s -> B_w`;
4. truncation/projection maps `E_{T,a_n}`, `I_{T,a_n}`;
5. a limiting killed weighted operator `L`;
6. constants `eps_n -> 0`;

such that

```text
|| E_{T,a_n} L I_{T,a_n} - K_{T,a_n} ||_{B_s -> B_w}
  <= eps_n.
```

Then the refined finite kernels may be treated as controlled
approximants of `L`, and Keller-Liverani/Hennion become legitimate
targets.

This is only a proposition skeleton.  Every item above is currently
open.

## 7. Failure Modes

The refined-kernel program fails if:

- the Cesaro limits do not exist;
- limits exist pointwise but not in any useful uniform/weighted norm;
- deeper phase tails do not decay;
- `delta` has no summable or controlled tail;
- killing boundaries remain too irregular;
- no natural Banach pair gives compact strong-to-weak embedding;
- finite matrices remain dependent on arbitrary prefix choices.

In that case, Phase 10 should stop the analytic branch and use the
finite-rank fallback.

## 8. Next Computations

Useful next diagnostics:

1. compare weighted `delta` tails across existing `T = 15` and
   `T = 16` outputs;
2. compare adjacent-block TV errors against the candidate mixed norm,
   not only against dominant-signature flips;
3. run `T = 15`, `j_count = 64` only if the cost is acceptable and only
   to test a named tail/variation constant;
4. compare Cesaro prefix distributions with dyadic block distributions;
5. test whether bad phase cells are sparse in Haar measure as `a`
   grows.

None of these outputs should be called a spectral gap.

## 9. Update After 2-adic Oscillation Diagnostics

The direct child-cylinder diagnostics show that the refined-kernel
program cannot simply assume martingale continuity of the full label.

At `T = 15`, `max_j = 128`, script
`100_z2_cylinder_oscillation.py` gives full-label mean TV:

```text
depth 0: 0.0486132,
depth 1: 0.0487704,
depth 2: 0.0509391.
```

This pushes the conditional kernel toward a labelled symbolic object:

```text
source cylinder -> destination phase,
with delta and possibly source-stratum class as edge/branch data.
```

The stratified excess diagnostic shows that the additional label
variation is not featureless:

```text
source_v2_odd = 2|3
```

has mass `0.0625` and contributes `0.456409` of the depth-`2`
full-over-phase excess.

However, the first direct interaction-weight drift test creates
exceptional cells above `1`.  Therefore the next conditional kernel
should not be sold as a weighted-sup drift solution.  It should be
phrased as one of:

1. a labelled symbolic/countable kernel with tail summability still
   open;
2. a two-part weak norm with an explicit exceptional-source term;
3. a finite-rank fallback if neither formulation survives.

The first enriched-state split test supports option 2 as a concrete
next formulation.  With

```text
bad = {odd = 3 and v2 in {0,2}},
```

the bad component has mass `0.3125` and captures `0.742956` of
full-over-phase excess at `T15` depth `2`, and `0.767081` at `T16`
depth `1`.  The complement has p95 `0` in both tests.  Therefore the
next conditional kernel should be written as:

```text
K = K_good + K_bad,
```

where `K_good` is the candidate for weak/mixed-norm approximation and
`K_bad` is either a labelled symbolic subsystem with its own tail
analysis or a finite-rank/exceptional component.

The component transition-budget diagnostic refines this wording.  The
split should not be treated as `good + small bad error`; over
`0 < t < 2^21`, script `103_component_transition_budget.py` gives:

```text
K_GG = 0.012281296,
K_GB = 0.0054655765,
K_BG = 0.040839452,
K_BB = 0.018100693.
```

Therefore the honest conditional model is block-valued:

```text
K = [[K_GG, K_GB],
     [K_BG, K_BB]].
```

The bad block has larger row budget than the good block and is strongly
coupled to it.  Any future LY/KL statement must include block coupling,
or else route the bad block to an explicitly finite-rank/exceptional
subsystem.  The finite `2 x 2` spectral radius `0.03041195` from this
diagnostic is not an infinite spectral-radius statement.

Alternative bad rules on the common `T15_j32` window support keeping
this middle split provisionally.  The narrower rule `v2=2 and odd=3`
has small source mass `0.0625001` but very large bad row budget
`0.20995882`.  The broader rule `odd=3 or v2=2` has source mass about
`0.5624996` and `G->B` weighted fraction about `0.559896`, so it is too
large and too mixed to be a clean exceptional block.

## 10. Conditional Block-Norm Target

If Branch A continues, the operator should be written on a split phase
space

```text
X = X_G disjoint_union X_B,
B = B_G direct_sum B_B,
```

where `X_B` is the current bad component.  In row-source convention the
function-side operator has block form:

```text
(U f)_G = U_GG f_G + U_GB f_B,
(U f)_B = U_BG f_G + U_BB f_B.
```

A possible vector norm is:

```text
||f||_{s,eta} = max(||f_G||_{s,G}, eta ||f_B||_{s,B}),
||f||_{w,eta} = max(||f_G||_{w,G}, eta ||f_B||_{w,B}),
```

with `eta > 0` chosen before looking at spectral conclusions.

The conditional Lasota-Yorke target would not be a scalar inequality at
first.  It should be a block inequality:

```text
|U_GG f_G|_G <= a_GG |f_G|_G + C_GG ||f_G||_{w,G},
|U_GB f_B|_G <= a_GB |f_B|_B + C_GB ||f_B||_{w,B},
|U_BG f_G|_B <= a_BG |f_G|_G + C_BG ||f_G||_{w,G},
|U_BB f_B|_B <= a_BB |f_B|_B + C_BB ||f_B||_{w,B}.
```

Only after proving such estimates could one compress the strong
constants into a nonnegative matrix

```text
A_eta =
[[a_GG, eta^{-1} a_GB],
 [eta a_BG, a_BB]]
```

and ask whether `rho(A_eta) < 1`.  The finite component matrix from
script `103` is not this `A_eta`; it only says which block-coupling
terms are likely to matter.

Script `104_component_block_cauchy.py` gives the corresponding finite
weak-convergence diagnostic for the block kernels.  At fixed `T = 15`,
the weighted row `L1` drift between adjacent high-bit blocks decreases:

```text
B = 8:  mean 0.012046521, p95 0.0625,
B = 16: mean 0.0095367816, p95 0.056640625,
B = 32: mean 0.0074155295, p95 0.0390625.
```

This supports formulating a mixed-norm target for block-kernel
convergence.  It still does not prove convergence or compactness.

The `T15_B16_j64_multipair` run adds a warning: at fixed block size
`16`, pair means increase along the prefix:

```text
0->16:  0.009535642,
16->32: 0.013903232,
32->48: 0.018206286.
```

Therefore the conditional kernel cannot currently be based on ordinary
adjacent-block Cauchy convergence without an averaging scheme or a
different limit convention.

The prefix/Cesaro diagnostic is more compatible with a limit:

```text
16->32: mean 0.004767821, p95 0.0283203125,
32->64: mean 0.0037076395, p95 0.01953125.
```

The conditional kernel should therefore be formulated first as a
block-valued prefix-average kernel `K_N`, with the mixed-norm target

```text
||K_{2N} - K_N||_{s -> w} -> 0
```

or its projected `I K_N E` version, before invoking any
Keller-Liverani language.

Failure modes:

- no natural `B_B` exists for the bad component;
- `U_BG` or `U_GB` is unbounded in the chosen norms;
- the best `eta` is a fitted finite-window artifact;
- the bad component must instead be handled by a finite-rank theorem.

## 11. Prefix-Average Block Kernel Target

The current high-bit evidence should be formalized by prefix averages,
not by ordinary adjacent intervals.  Fix `T`, the finite hit coordinate
`h`, and a low-bit source cell `c`.  Let:

```text
sigma(c) in {G,B}
```

be the source component determined by the provisional rule

```text
B = {odd = 3 and v2 in {0,2}}.
```

For a prefix length `N`, define the component-collapsed weighted kernel:

```text
K_N^{sigma,tau}(c)
  = (1/N) sum_{0 <= k < N}
      1_{source(t_k,h) in sigma}
      1_{return(t_k,h)}
      1_{dest(t_k,h) in tau}
      2^{-delta(t_k,h)},

t_k = r(c) + k * 2^T.
```

If `c` is not entirely contained in component `sigma`, the row must
either be split or charged to `SourcePartitionError`.  In the current
script-`88` data this ambiguity is small but nonzero; it is not allowed
to disappear silently in a proof-level statement.

Terminal/killed mass is kept separate:

```text
K_N^{sigma,terminal}(c)
  = (1/N) # {0 <= k < N :
        source(t_k,h) in sigma and status(t_k,h) = terminal }.
```

Script `105_component_prefix_cauchy.py` estimates the finite weak
component drift:

```text
D_N
  = sum_c omega_N(c)
      sum_{tau in {G,B}}
        |K_{2N}^{sigma(c),tau}(c) - K_N^{sigma(c),tau}(c)|.
```

Here `omega_N` is the empirical complete-source-cell averaging weight
used by the diagnostic.  In the default script-`105` run, `omega_N` is
the uniform counting measure on retained source cells/prefix pairs
after excluding mixed-source cells and boundary rows.  It is not yet a
proved Haar limit.  This is a finite `ell_infty -> L1(omega_N)`
proxy for the component-collapsed row-source kernels, because for
bounded component test functions:

```text
|(K_{2N}f)(c) - (K_N f)(c)|
  <= sum_tau |K_{2N}(c,tau) - K_N(c,tau)| ||f||_infty.
```

The target statement is therefore not a uniform Cauchy claim.  The
minimal analytic target is:

```text
||K_{2N} - K_N||_{ell_infty(component) -> L1(omega)}
  -> 0
```

or the corresponding statement after replacing the finite `ell_infty`
and `L1(omega)` spaces by the chosen Banach pair `B_s -> B_w`.

The current finite evidence is:

```text
N = 16 -> 32: mean 0.004767821, p95 0.0283203125,
N = 32 -> 64: mean 0.0037076395, p95 0.01953125,
N = 64 -> 128: mean 0.0027624646, p95 0.013183594.
```

Lifting the same prefix comparison from `{G,B}` destinations back to
full retained return labels has an additional finite cost.  Script
`106_prefix_label_lift.py` reports on the same `T = 15` data:

```text
component_l1 mean = 0.0042377302,
label_l1 mean     = 0.0075584849,
label_excess mean = 0.0033207547,
label_excess p95  = 0.017578125.
```

With `delta <= 5`, the label-excess mean is still `0.0033040573`.
Thus the label-lift obstruction is not mainly a large-`delta` tail on
this window.  Any limiting kernel must either prove convergence of the
retained full-label distributions or keep a separate
`ComponentLabelLift` error term.

The later `64->128` run improves the prefix numbers but does not remove
the label-lift term:

```text
component_l1 mean = 0.0027624646,
label_l1 mean     = 0.0057602607,
label_excess mean = 0.0029977961,
label_excess p95  = 0.015625.
```

This is only evidence for a weak prefix/Cesaro formulation.  It does
not establish:

- existence of a limiting kernel `K_infty`;
- convergence in a strong norm;
- convergence uniformly over source cells;
- compatibility with the original generated `FULL` matrices;
- any spectral consequence.

The next mathematical definition to stabilize is therefore:

```text
K_infty = weak/Cesaro limit of the block-valued kernels K_N,
```

if such a limit exists.  Keller-Liverani language should not be used
before this limit convention and its approximation norm have been
fixed.
