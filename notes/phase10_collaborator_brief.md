# Phase 10 Collaborator Brief

Date: 2026-05-14

Status: external-facing technical brief.  This is designed for a
functional analyst or dynamicist.  It deliberately avoids claiming a
spectral gap, an infinite transfer operator, or any progress toward a
proof of Collatz beyond the declared finite certificates.

## 1. The Question to Ask

The useful collaborator question is:

```text
Given the killed labelled first-return structure below, is there a
natural Banach space and projection scheme for which the generated
finite matrices are legitimate approximants of an infinite operator?
```

The wrong question is:

```text
Can this prove the Collatz conjecture?
```

That is not the current mathematical state.

## 2. Non-Negotiable Constraints

Any collaborator-facing version must state:

- Conjecture 6 is not proved;
- no infinite spectral gap is proved;
- finite spectral-radius values are not asymptotic theorems;
- `full_T` / `FULL_{T,j}` are not known to be projections of an
  infinite operator;
- Hennion and Keller-Liverani are not applicable until their hypotheses
  are matched explicitly;
- the analytic program may fail.

## 3. Finite Objects Already Available

Production finite certificate:

```text
lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean
```

Certified facts:

- finite state space: `Fin 37`;
- matrix: deterministic residue-cell `(K,b)` compression;
- exact CW bound:

```text
90833233962213 / 129559208330288 < 3/4;
```

- Lean theorem:

```text
k16s16KDeterministicGeneratedSpectralRadiusBound.
```

This is finite-rank only.

## 4. Current Analytic Candidate

The leading candidate is a killed labelled high-bit kernel on a
profinite/symbolic space.  A finite version is:

```text
K_{T,a,L,N}(source cell; destination phase, delta)
  = averaged count over high-lift prefixes,
```

with:

- `T`: base stopping depth;
- `a`: extra 2-adic cylinder depth;
- `L`: retained return-exponent cutoff;
- `N`: high-lift averaging or block size;
- terminal mass killed or recorded separately;
- optional weight `2^{-s delta}`.

The target, if meaningful, would be:

```text
|| U_s - I_{T,a,L,N} FULL_{T,a,L,N} E_{T,a} ||_{B_s -> B_w}
  <= epsilon(T,a,L,N),
```

where `U_s` is now the primary row-source/Koopman-side operator.  The
maps `E` and `I` have candidate definitions as conditional expectation
onto cylinder cells and inclusion of cell-constant observables, but the
Banach spaces and norm estimates are not yet established.

After the latest diagnostics, the most precise candidate is a
two-component prefix-average kernel:

```text
X = X_G disjoint_union X_B,
X_B = {odd = 3 and v2 in {0,2}},
K_N = [[K_N,GG, K_N,GB],
       [K_N,BG, K_N,BB]].
```

The finite weak target is:

```text
||K_{2N} - K_N||_{ell_infty(component) -> L1(omega_N)} -> 0,
```

where `omega_N` is currently only finite counting measure on retained
complete source cells, not a proved Haar limit.

## 5. Empirical Signals, Not Theorems

Finite diagnostics suggest:

- the old `PhaseState` quotient is too coarse for exact local
  constancy;
- five extra 2-adic source bits help but do not create a projection
  identity;
- weighted large-`delta` tails are globally small on tested windows;
- local tail control is not uniform;
- adjacent-block TV decreases in one fixed-`T = 15` block-doubling
  test, but this is not convergence;
- bounded retained-label variation is visible and must be separate from
  the large-`delta` tail.
- source cells in the diagnostics are almost, but not exactly, cells of
  the proposed finite `source_phase` partition;
- true 2-adic child-cylinder tests do not currently show decreasing
  full-label oscillation.
- the label-excess part of that obstruction is nevertheless
  structurally concentrated; e.g. `source_v2_odd = 2|3` has mass
  `0.0625` and contributes about `0.456409` of full-over-phase excess in
  the `T15_d2_tail3` diagnostic.
- a lighter `T=16` diagnostic preserves the same signal, with
  contribution about `0.492200`.
- a direct finite drift weight on that interaction improves typical
  ratios but creates exceptional cells above `1`, so it is not a
  uniform drift solution without additional exceptional-mass control.
- the worst exceptional cells for that weight are incoming-source
  effects rather than the weighted bad stratum itself, which suggests a
  simple weighted-sup norm may be the wrong abstraction.
- an enriched-state split is more promising: the component
  `odd = 3 and v2 in {0,2}` has mass `0.3125`, captures about
  `0.74-0.77` of full-over-phase excess in the tested windows, and
  leaves complement p95 `0`.
- a follow-up component transition budget shows this bad component is
  coupled, not negligible: over `0 < t < 2^21`, good row budget is
  `0.017746872`, bad row budget is `0.058940144`, and about `30.8%` of
  good weighted return mass flows into bad.
- ordinary adjacent high-bit block Cauchy is not reliable, but
  prefix/Cesaro block kernels are the best current signal:
  `16->32` mean `0.004767821`, `32->64` mean `0.0037076395`,
  `64->128` mean `0.0027624646`.
- lifting the component kernel back to retained full labels is still a
  real cost: at `64->128`, label-excess mean is `0.0029977961`, p95 is
  `0.015625`, and p99 is `0.03125`; the `delta <= 5` cutoff does not
  remove this term.

Current named error budget:

```text
A_projection
+ A_phase_block
+ A_label_bounded
+ DeltaTail_global
+ DeltaTail_local
+ BoundaryError
+ DriftExcess
+ OrientationError
+ SourcePartitionError
+ BlockCoupling
+ PrefixCoupling
+ ComponentLabelLift.
```

## 6. Questions for the Collaborator

1. Is a Koopman-side killed weighted first-return operator `U_s` on
   `Z_2 x H` a natural object here, or is this already the wrong phase
   space/operator?

2. Can the row-source finite kernels `FULL_{T,a,L,N}` be interpreted as
   any of: projections, Galerkin approximants, Ulam discretizations,
   compressions, or controlled finite-rank approximants to `U_s`?

3. If not, is there a nearby infinite object whose finite quotients are
   mathematically honest?

4. What Banach pair is the least artificial candidate:
   martingale/cylinder BV on `Z_2 x H`, weighted symbolic Holder,
   countable Markov shift space, or a drift-weighted sup/Lipschitz
   space?

5. The first 2-adic child-cylinder diagnostics fail to show decreasing
   full-label oscillation.  Does that kill the naive `Z_2` martingale
   space, or is there a standard weaker/enlarged symbolic space that
   could still work?

6. Would a Hennion-style theorem be realistic, or does the lack of
   compactness/tail control make this a false analogy?

7. Would Keller-Liverani be realistic if the block-TV diagnostics could
   be upgraded to a mixed-norm convergence statement?

8. Is the countable episode/return-signature graph likely to satisfy
   Sarig-type recurrence or BIP-like hypotheses, or is that unlikely
   from the start?

9. Should terminal/killed mass be modelled as a hole, an absorbing
   state, or a substochastic kernel?

10. Is the row-source finite matrix orientation compatible with the
   proposed transfer operator, or does it force a transpose/push-forward
   interpretation?

11. Which early failure criterion would convince them to stop the
    analytic branch and publish only the finite-rank note?

12. If the natural object is a two-component block kernel
    `K_GG,K_GB,K_BG,K_BB`, is there a standard vector-valued or
    block-norm transfer-operator framework that could handle it, or
    should `K_bad` be treated as finite-rank/exceptional from the start?

13. Is a prefix/Cesaro kernel limit a legitimate analytic object in
    this setting, or is it too dependent on the chosen enumeration of
    high-bit lifts?

14. Can a weak source-average norm based on finite counting measures
    `omega_N` be upgraded to Haar/counting `L1`, or should this be
    treated as a purely empirical averaging convention?

15. If component prefix convergence holds but retained full-label lift
    remains comparable to the component drift, should the Banach space
    be labelled from the start rather than component-valued?

## 7. Materials to Send First

Send these notes, in this order:

1. `notes/phase10_operator_gate.md`;
2. `notes/phase10_mixed_norm_candidate.md`;
3. `notes/phase10_error_decomposition.md`;
4. `notes/phase10_gate10B_provisional_decision.md`;
5. `notes/phase10_finite_rank_fallback.md`;
6. `notes/phase10_literature_source_map.md`.

Do not send raw numerical reports first.  The collaborator should see
the operator and norm questions before the data.

## 8. Desired Collaborator Profile

Best fit:

- transfer operators for open systems or countable Markov shifts;
- Hennion/Keller-Liverani style perturbation theory;
- symbolic Banach spaces and tail/drift norms;
- enough comfort with profinite or p-adic spaces to reject false
  analogies quickly.

Secondary fit:

- rigorous numerics for finite-rank transfer-operator approximations;
- certified Ulam/Galerkin spectral approximation;
- Lean-friendly finite certificate formalization.

## 9. Expected Useful Outcomes

The collaborator may return one of four useful answers:

1. a plausible Banach/projection framework to formalize next;
2. a proof that the current finite matrices cannot be viewed as the
   desired approximants;
3. a better infinite model using a different state space;
4. a recommendation to stop Branch A and publish the finite-rank
   fallback.

All four outcomes are mathematically valuable.
