# Phase 10 Banach-Space Implications After Diagnostics

Date: 2026-05-14

Status: ranking update.  This note updates the Banach-space
recommendation after the cylinder/refinement diagnostics.  It does not
prove any Lasota-Yorke inequality.

## 1. Diagnostic Summary Relevant to Banach Spaces

Observed:

- exact local constancy on the original `PhaseState` quotient fails;
- adding five 2-adic source bits improves phase stability substantially;
- increasing high-lift prefixes decreases exact local constancy;
- average majority and adjacent-block drift remain reasonably controlled;
- the remaining full-signature obstruction is partly `delta` variation;
- some residual phase variation persists even after five extra bits.
- at `T = 16`, `j_count = 8`, the weighted `delta` tail after the
  existing `2^{-delta}` normalization is globally small: keeping
  `delta <= 4` leaves weighted tail `0.00412187`, keeping `delta <= 5`
  leaves `0.000862882`, and keeping `delta <= 8` leaves
  `0.00000574087`;
- at `T = 15`, `j_count = 32`, the corresponding values are
  `0.0040648`, `0.000845196`, and `0.00000635292`;
- the same tail is not uniformly small cellwise at low thresholds:
  at `T = 16`, `delta <= 4` has group-level tail p95 `1`, while
  `delta <= 5` drops to `0.047619`; at `T = 15`, the corresponding p95
  values are `0.2` and `0.0379747`.
- adjacent-block drift at `T = 15`, `j_count = 32` has full-signature
  TV p95 `0.1875` even though the dominant full-signature flip fraction
  is only `0.0124817`.
- at `T = 15`, block size `32`, clipping large `delta` labels does not
  materially reduce full count-TV: `clip delta > 5` has mean `0.0308437`
  and p95 `0.15625`, while the full label has mean `0.0310049` and p95
  `0.15625`.
- the bounded-label excess over phase TV on the same window is smaller
  than phase movement but visible: full-label excess has mean
  `0.00791955`, p95 `0.0625`, p99 `0.09375`, and max `0.25`.
- at `T = 16`, `j_count = 8`, bad cells are visibly stratified by source
  coordinates; for example, `v2=2, odd=3` has phase exact fraction
  `0.898926` but full exact fraction only `0.383301`.
- a first source-stratum drift probe is negative for a naive
  three-parameter weight family on `T = 15`, `j_count = 16`: nontrivial
  weights improve p95 only by creating a small exceptional set with
  ratio `>= 1`.
- the first genuine 2-adic child-cylinder diagnostics do not show
  decreasing full-label oscillation.  With `T = 15`, `max_j = 128`,
  full-label mean TV is `0.0486132 -> 0.0487704 -> 0.0509391` over
  depths `0 -> 2`.
- stratifying the `T = 15`, depth-`2` child-cylinder obstruction shows
  that full-over-phase excess is concentrated: `source_v2_odd = 2|3`
  has mass `0.0625`, mean excess `0.120621`, and contributes
  `0.456409` of the global excess.
- a lighter `T = 16` stratification preserves the same signal:
  `source_v2_odd = 2|3` has mass `0.0625`, mean excess `0.152130`, and
  contributes `0.492200` of the global excess.
- a direct interaction-weight drift test on `source_v2_odd = 2|3`
  improves p95 only by creating exceptional cells above `1`; coefficient
  `1` gives p95 `0.155199` but max `2.63334` and fraction `>= 1`
  equal to `0.000366211`.
- an enriched-state split with bad component `odd = 3 and v2 in {0,2}`
  captures `0.742956` of full-over-phase excess at `T15` depth `2` and
  `0.767081` at `T16` depth `1`, while the complement has p95 `0` in
  both tests.
- the follow-up component transition budget over `0 < t < 2^21` shows
  that this split is coupled: good row budget `0.017746872`, bad row
  budget `0.058940144`, and `G -> B` weighted fraction among good
  returns `0.30797407`.
- alternative bad rules are worse in different ways: `v2=2 and odd=3`
  has bad row budget `0.20995882`, while `odd=3 or v2=2` marks about
  `0.5625` of sources as bad and mixes with `G -> B` fraction
  `0.559896`.
- component block-Cauchy drift decreases under block doubling at fixed
  `T = 15`: weighted good/bad row `L1` mean
  `0.012046521 -> 0.0095367816 -> 0.0074155295` for block sizes
  `8 -> 16 -> 32`.
- the `B=16`, `j=64` multipair check worsens along ordinary adjacent
  pairs: `0.009535642 -> 0.013903232 -> 0.018206286`.
- the prefix/Cesaro check improves from `16->32` to `32->64`:
  `0.004767821 -> 0.0037076395`.

Implication:

```text
The next analytic model should be distributional and labelled, not a
simple locally constant map on the old finite quotient.
```

## 2. Updated Candidate Ranking

### Rank 1: labelled countable symbolic / return-signature space

State:

```text
symbolic source cylinder + return label data,
with delta as an edge label.
```

Norm shape:

```text
||f||_s = sup |f|/W + Holder_or_variation(f/W),
||f||_w = weighted local L1 or weighted sup on cylinders.
```

Why it moved up:

- it can represent persistent `delta` variation without pretending
  `delta` is a pre-existing phase coordinate;
- compatible with Sarig/TMS-with-holes language if summability and
  recurrence can be proved;
- allows a tail program for large return labels.
- the finite `T = 16` diagnostic suggests the globally weighted
  large-`delta` tail is small after `2^{-delta}` weighting.
- source-stratum diagnostics suggest full-signature instability is
  structured enough to ask for a drift function, rather than completely
  homogeneous noise.
- bounded return-label variation can be represented honestly as an edge
  regularity term instead of being folded into the large-`delta` tail.
- the newest 2-adic stratification shows that label excess is strongly
  structured by source `v2` and odd residue, which is more naturally
  symbolic/drift data than smooth `Z_2` variation.
- the enriched-state split leaves a clean complement across two tested
  `T` values.
- the component transition budget points toward a vector-valued/block
  symbolic kernel rather than a scalar function space with a tiny error
  term.
- the component block-Cauchy diagnostic is compatible with a weak
  averaged block-kernel approximation target.
- the multipair check suggests ordinary adjacent-block Cauchy
  convergence is too strong or wrongly ordered.
- the prefix-average convention is currently the best weak-limit
  candidate.

Main risks:

- BIP/finitely irreducible structure may fail;
- positive recurrence may fail;
- summable variation of the potential is currently unproved;
- state space may be countable with no compactness.
- global weighted tail control may be too weak if Hennion/KL require a
  uniform source-cell estimate.
- a bounded-label regularity estimate is still missing; clipping large
  labels does not remove the block-TV obstruction.
- the bad component is not small in row budget and is coupled back to
  good; a block-norm or exceptional subsystem is mandatory.
- p95/max component drifts remain nonzero, so a uniform norm still looks
  implausible without exceptional-source control.

### Rank 2, under pressure: martingale/BV space on 2-adic cylinder partitions

State:

```text
functions on Z_2 x H with cylinder variation across depth.
```

Norm shape:

```text
||f||_s = ||f||_infty + sum_a beta_a Var_a(f),
||f||_w = L1(Haar) or cylinder L1.
```

Why it remains plausible:

- the observed `j mod 32` signal is naturally deeper 2-adic cylinder
  structure;
- exact local constancy is not required if variation tails decay;
- compactness may be approached through martingale/cylinder truncation.
- phase-only child-cylinder means are fairly flat and slightly
  decreasing in the higher-tail run.

Main risks:

- `delta` and killing use archimedean information;
- no variation-tail inequality is known;
- the first-return map may not be measurable with controlled depth loss.
- full-label child-cylinder oscillation does not decrease in the first
  direct 2-adic tests; this branch now needs either an enlarged state,
  a weaker norm, or a collaborator-supplied mechanism.
- the stratified label-excess signal may only justify a symbolic/drift
  extension, not a true martingale compactness theorem.
- the simplest interaction drift weight is not safe uniformly; it would
  need an exceptional-mass framework.
- the selected bad component still needs its own internal symbolic
  dynamics or a finite-rank treatment.

### Rank 3: weighted `ell_infty` / drift space on episode graph

State:

```text
episode or return-signature nodes.
```

Norm shape:

```text
||f|| = sup |f(u)| / W(u).
```

Why useful:

- natural fallback bridge to finite-rank certificates;
- handles labelled transitions and drift cleanly.

Main risks:

- little smoothing;
- no automatic compact strong-to-weak embedding;
- Hennion may be unavailable without an additional compactness device.
- a naive source-stratum weight on `(v2, odd mod 4, h)` is not strong
  enough on the first harder finite probe.

### Rank 4: Lipschitz on `Z_2 x H`

State:

```text
continuous or Lipschitz functions on the profinite product.
```

Why downgraded:

- exact local constancy fails on the tested quotient;
- `bit_length` and order-based killing are not 2-adic continuous;
- a Lipschitz first-return map is not yet visible.

It remains useful as a language for source cylinders, but not as the
leading Banach candidate.

### Rank 5: classical interval BV / countable interval branches

Still mostly a false analogy unless a concrete interval model is built.

## 3. Updated Lasota-Yorke Target

The target should be formulated with an explicit tail label:

```text
||L f||_s <= alpha ||f||_s + C ||f||_w,
alpha < 1,
```

where the contraction part must include both:

```text
phase_refinement_tail(a)
```

and

```text
delta_weight_tail(L) = sum_{|delta| > L} 2^{-s delta} * tail_weight.
```

A phase-only `alpha` is not enough.

The newest finite diagnostic suggests two different constants should be
kept separate:

```text
DeltaTail_global(L)
  = total weighted return mass with delta > L
    / total weighted return mass,
```

and

```text
DeltaTail_local_p95(L)
  = p95 over source cells of
    weighted return mass with delta > L
    / source-cell weighted return mass.
```

At `T = 16`, `j_count = 8`, the observed values include:

| run | L | `DeltaTail_global(L)` | `DeltaTail_local_p95(L)` |
|---|---:|---:|---:|
| `T16_j8` | 4 | `0.00412187` | `1` |
| `T16_j8` | 5 | `0.000862882` | `0.047619` |
| `T16_j8` | 8 | `0.00000574087` | `0` |
| `T15_j32` | 4 | `0.0040648` | `0.2` |
| `T15_j32` | 5 | `0.000845196` | `0.0379747` |
| `T15_j32` | 8 | `0.00000635292` | `0` |

This is encouraging for a weighted-tail norm, but it is not a proof of
summability or uniform approximation.

For any Keller-Liverani target, majority stability should not be used as
the mixed norm.  The block diagnostic suggests using a distributional
error such as:

```text
BlockTV_full(N)
  = sup_or_weighted_p95 over source cells of
    TV(full-signature distribution on block N,
       full-signature distribution on next block N).
```

At `T = 15`, comparing blocks `0..15` and `16..31`, the full-signature
TV p95 is `0.1875`, and the high full-tail-weight class has p95 `0.25`.

A fourth bookkeeping term may be needed for source-stratum drift:

```text
SourceStratumBad(W)
  = weighted mass of source strata where phase/full instability is high.
```

No function `W` has been defined yet.  The diagnostic only says that
such a function is worth looking for.  The first coarse parametric test
suggests that if such a `W` exists, it is not just a simple
three-parameter penalty on `odd=3`, `v2=2`, and capped `v2`.

A separate bounded-label term is also needed:

```text
A_label_bounded(B,L)
  = weighted_or_p95 excess of retained-label TV over destination-phase
    TV at block size B and cutoff L.
```

This term is not a substitute for `DeltaTail_global(L)`: the former
measures variation inside the retained labelled alphabet, while the
latter measures discarded large-`delta` mass.

## 4. Immediate Mathematical Gate

Before invoking Hennion or Keller-Liverani, define:

1. the labelled kernel;
2. the tail weight `W`;
3. the strong variation/Holder seminorm;
4. the weak norm;
5. the compactness mechanism;
6. the mixed-norm approximation statement.

No current diagnostic proves these items.

## 5. Collaborator Profile Update

The most useful collaborator is now likely someone with experience in:

- countable Markov shifts with holes;
- Sarig-style thermodynamic formalism;
- weighted symbolic Banach spaces;
- or martingale/BV spaces on profinite partitions.

The question to ask:

```text
Given a killed labelled kernel with good empirical block stability but
no local constancy, is there a natural Banach space in which finite
cylinder averages can be controlled?
```
