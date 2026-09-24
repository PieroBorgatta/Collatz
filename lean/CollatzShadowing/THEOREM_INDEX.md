# Theorem index — `CollatzShadowing`

Curated declaration → file map for the AI-authored proof modules (including
the later arithmetic and trace developments; generated certificate witnesses
are summarized at the end).
Each headline result notes the paper statement it formalizes. The sources
have no `sorry`, `admit`, or project-declared `axiom`; finite proofs using
`native_decide` trust the native compiler. See [STATUS](../STATUS.md) for
the axioms audit and pinned-toolchain caveat.

---

## Shadowing core

### `Basic.lean`
- `S` — accelerated Syracuse map on `ℕ`; `nu2Nat`, `ν₂`, `ν₂Z2` valuations.

### `Phantom.lean`
- `PhantomWord` — nonempty list of positive exponents; `length`, `A`.
- `affineFoldStep`, `Cw`, `Aw`, `Aw_eq_A` — the `(C_w, A_w)` fold (paper eq. 3.1).
- `qwRat`, `qwZ2` — rational / 2-adic fixed point `q_w = C_w/(2^A − 3^L)`.
- `B`, `aAt`, `B_closed_form` — periodic partial sums.

### `Syracuse2Adic.lean`
- `Syracuse2adic : ℤ₂ → ℤ₂` — total map defined using the unit factor of
  `3x+1`, with value `0` at `−1/3`. It is discontinuous there.
- `Syracuse2adic_natCast` — bridge to the integer-level `S` for positive
  odd naturals.

### `SyracuseSingularity.lean`
- `singularLift_numerator`, `singularLift_step_of_seed` — the lift
  `n ↦ 4n+1` adds two numerator-valuation bits while preserving the
  accelerated output.
- `singular_outputs_separated_at_every_precision` — for every `R`, two
  positive odd natural inputs satisfy `2^R ∣ (3n+1)` while their
  accelerated outputs are `1` and `7`. This is a finite-precision
  arithmetic statement, not a formal topological continuity theorem.

### `Auxiliary.lean`
- `nu2Z2_three_mul` — `ν₂(3·n) = ν₂(n)` on `ℤ₂`.
- `qwOddDen` — every phantom has odd `q_w` denominator.
- `affine_difference` — `Sʲ(n) − Sʲ(q_w) = (3ʲ/2^{Bⱼ})(n − q_w)`.
- `nu2_stable_under_proximity` — ultrametric stability of `ν₂`.
- `B_bound_iff`, `B_mul_period`, `qw_orbit_matches`.

### `Shadowing.lean` — **paper Lemma 3.1**
- `exact_shadowing` — exact congruential shadowing.
- `exact_shadowing_periods` — periodic specialization (bound `b·A`).

### `NoInfinite.lean` — **paper Cor. 3.4 + v4 expanding-cycle result**
- `PhantomWord.Expansive`, `qwRat_neg_of_expansive`, `qwZ2_ne_natCast_of_expansive`.
- `no_infinite_period_congruence_expansive` — **Cor. 3.4** (no infinite periodic shadowing).
- `no_positive_endpoint_eventually_periodic_expansive_congruence` — **new in v4**: no positive integer endpoint stays in an expanding phantom's congruence classes for all periods (post-prefix form; generalizes Cor. 3.4 to the eventually-periodic case).

---

## Finite operator / Collatz–Wielandt layer

### `Operator.lean`
- `PhaseState V := Fin (V+1) × Fin 4 × Fin 4`, `phaseState`.
- `TransferMatrix`, `ProbabilityEntry`, `RowSubstochastic`.
- `OperatorDecomposition` — packages `full = core + tail` + row certificates.

### `Bound.lean` — **generic weighted Collatz–Wielandt bound**
- `FiniteCWCertificate`, `ClearedCWRowBound`, `FiniteMatrixBoundCertificate`.
- `spectralRadius_le_of_finiteCWCertificate` — passes a positive weighted CW certificate to Mathlib's real `spectralRadius`.
- `FiniteCWCertificate.add`, `OperatorDecomposition.spectralRadius_le_full` — the `core + tail` spectral corollary.

### `EpisodeGraph.lean`
- `EpisodeNode`, `TruncatedEpisodeGraph`, `SCC`, `Walk`, `reachable_of_walk`.
- `HubSCCCertificate`, `CriticalSCCCertificate` — finite SCC import format.

---

## Phase-10 finite bridges

### `WeakBridge.lean` — A0 weak bridge (finite, elementary)
- `weighted_action_diff_le` — weighted row-`L¹` drift bounds the `ℓ∞ → L¹(μ)` action error.
- `FiniteSplit.weighted_sum_le_low_plus_tail`, `weighted_dyadic_delta_boundary_le`.
- `BitLength.bitLength`, `bitLength_two_mul`; dyadic-boundary crossing counts `affineEndpointCrossingUnion_card_le` (`O(c·log N)`); `biAffineDelta_dyadicWeight_period_boundary_le`.
- `TailCount.dyadic_tail_count_mul_le`, `dyadic_tail_mass_le` — **exact** high-`ν₂` source-tail mass `≤ 2⁻ᴿ`.
- `LabelSplit.{BranchCounters, branchResolved, BranchCover, sourceResolved_of_all_branches_resolved}` — abstract finite label-split schema.

### `CollatzBridge.lean` — descent bridge + first-barrier (conditional)
**Proved (elementary):**
- `collatzStep`, `ClassicalCollatzConjecture`, `AcceleratedCollatzConjecture`, `UniformStrictDescentHypothesis`.
- `syracuse_pos`, `syracuse_odd`, `syracuse_lt_self_of_two_le_exponent`.
- `acceleratedCollatz_of_uniformStrictDescent` — descent hypothesis ⇒ accelerated Collatz.
- `acceleratedToClassicalBridge`, `classicalCollatz_of_uniformStrictDescent_provedBridge` — ⇒ classical Collatz.
- `SyracuseWordMatchesFrom`, `evalSyracuseWord_mul_pow_sum_eq_affine_of_matches` — exact affine word identity.
- `syracuseWordFormalFixedPoint`, `…_neg_of_expanding`; `a0SemanticDropCommonPrefix_matches_source_cylinder` (parametric prefix on `103+256t`).
- `AffineNatDropBranch.targetN_lt_sourceN_of_coeffDrop` (drop certificate); `AffineTBranch.not_nextLocalInteger_lt_sourceLocalInteger_of_coeffNondecreasing` (negative lemma: same-coordinate return branches cannot descend).

**Open hypotheses, isolated as named `Prop`s (NOT proved — by design):**
- `A0FirstBarrierExistsAll`, `A0FirstBarrierThresholdAutomatic`.
- `A0EndpointSuffixExitAll_of_firstBarrier` — *conditional* cylinder descent given the above.
- `GlobalDescentCover`, `classicalCollatz_of_globalDescentCover` — *conditional* global bridge.

---

## Later arithmetic and trace results

### `A0InfiniteSubfamily.lean`
- `hasStrictDescent_a0_t_two_mod_sixteen`,
  `hasStrictDescent_a0_t_ten_mod_thirtytwo` — unconditional strict descent
  for two infinite residue subfamilies of the A0 source cylinder.
- `a0Endpoint_word_one_not_drop` and companion short-word lemmas — local
  negative checks, not a global exclusion.

### `PrecisionTax.lean`
- `syracuseWord_precisionTax_scaled_identity_of_matches` — exact affine
  transport of the numerator attached to an expansive fixed word.
- `syracuseWordPhantomPrecision_after_eval_add_sum` — one matched block
  consumes exactly `w.sum` bits of the associated 2-adic precision.
- `syracuseWordPhantomPrecision_after_iterate_add_mul_sum`,
  `syracuseWord_matched_block_precision_budget` — exact telescoping and
  finite repetition budget.
- `no_infinite_matched_expansive_word` — one expansive word with positive
  sum cannot match forever from a natural starting state.

### `PrecisionTemplates.lean`
- `syracuseWordPhantomPrecision_one_after_eval_add_one` and the
  `…one_two…` / `…two_one…` companions — concrete numerators `n+1`,
  `n+5`, `n+7` and exact loss for `[1]`, `[1,2]`, `[2,1]`.
- `no_infinite_matched_syracuseWord_one` and companion lemmas — local
  no-infinite-repetition instances.

### `SwitchingPrecision.lean`
- `switchingPhantom_scaled_identity`,
  `switchingPhantomPrecision_after_step_add_exponent` — precision transport
  across compatible label changes and odd rescaling.
- `arbitrary_phantom_shift_can_set_precision` — unconstrained relabeling
  can reset the counter to any prescribed height.

### `AffineTraceGraph.lean`
- `switchingFormalPoint_transport` — compatible affine labels transport
  their rational formal point along the prescribed branch.
- `no_common_rational_fixed_point_of_distinct_words` — distinct formal
  fixed points cannot be cycles of one scalar rational control state.

### `ThreeTraceObstruction.lean`
- `concrete_shortTrace_lasso` — exact natural-number segment with a repeated
  triple of short-template precision values.
- `threeTraceLassoSeed_invariant`, `threeTraceLassoSeed_shortTraceTriple`
  — unbounded family of natural approximants to the formal point `−19/11`.
- `hiddenTrace_lasso_tax` — the omitted compatible precision decreases by
  four bits per lasso.

### `CycleConstraints.lean`
- `syracuseWordCycleEquationInt`, `syracuseWordCycleEquationNat` —
  necessary cycle equation for a matched periodic word.
- `syracuseWordCycleContracting` — every nonempty positive cycle word is
  contracting.
- `syracuseWordCycleModularSieve` — divisors of the denominator divide the
  word constant.
- `three_mul_le_at_first_contracting_prefix` — finite prefix bound at a
  hypothetical cycle minimum.

### `FirstBarrier.lean`
- `syracuseWordAffine_mod_exactResidueModulus_of_matches` — exact
  extra-bit residue condition for an odd endpoint.
- `evalSyracuseWord_lt_of_exactResidue_above_barrier` — sufficient finite
  residue test for a strict drop.
- `evalSyracuseWord_lt_iff_source_above_barrier` — at the actual source,
  the threshold is equivalent to descent, so it supplies no independent
  global ranking argument.

### `ExactCylinders.lean` — v6 exact-word theorem (full build passed)
- `syracuseWordMatches_iff_exactResidue` — for every nonempty list `w`
  of positive exponents and every natural start `n`, the exact word
  matches iff `(3^w.length * n + C_w) % 2^(w.sum + 1) = 2^w.sum`.
- `repeatPhantomWord_matches_iff_exactResidue` — for a `PhantomWord w`
  and `k > 0`, all `k` blocks match iff the analogous residue equality
  holds modulo `2^(k * w.A + 1)`.
- These equivalences are Lean declarations. Invertibility of `3^L`
  gives one odd residue class; its natural density is `2^-(A+1)`
  (relative odd density `2^-A`). Those class and density corollaries
  are paper-level at present.

---

## Post-v6 marked section and cancellation towers

These working-tree modules follow the frozen Zenodo v6 snapshot. They do
not supply a global Collatz termination rank.

### `ShortcutCoverage.lean`
- `ShortcutCoverage.rank_decrease` — explicit coefficient/valuation rank
  decreases outside the stopping set `{1} ∪ {n : n % 27 = 20}`.
- `ShortcutCoverage.exists_iterate_target_linear_bound` — every positive
  shortcut orbit hits that set in at most `13*n+4` steps. Sufficiency of
  the residue is classical; this is a local arithmetic certificate.

### `MarkedSection.lean`
- `MarkedSection.section_iff_episodeHits20` — exact six-progression
  characterization of a marked odd-to-odd episode; its source is excluded
  and its endpoint included. The theorem assumes `¬ 3 ∣ n`, with no cap
  on the actual 2-adic exponent.

### `SectionCoverage.lean`
- `SectionCoverage.shortcut_episode`, `shortcut_episode_endpoint` — exact
  correspondence between the shortcut and accelerated maps.
- `SectionCoverage.exists_accelerated_hit` — unconditional arrival at 1
  or the marked section on every positive odd Syracuse orbit.

### `CancellationTower.lean`
- `cancellationTower_run`, `cancellationTower_iterate` — arbitrary-length
  `[1,2]` repetition from `8^r*u-5` to `9^r*u-5` for even `u≥2`.
- `cancellationTower_exit_one`, `_two`, `_three`, `_ternary` — the three
  exact terminal phases and retained ternary identities.
- `cancellationTower_noDrop_of_even_ge_thirty` — the complete macro from
  `(2^(k+1)-11)/3` has no strict descent for every even `k≥30`.
- `cancellationTowerSource_mod_eighteen` — the infinite subfamily
  `k=18*t+10` belongs to the first marked residue class.

### `SectionReturn.lean`
- `SectionReturn.recurrent_section_of_never_hits_one` — every orbit
  avoiding 1 visits the marked section at arbitrarily late times.
- `SectionReturn.descending_return_family` — exact one-step returns
  `661+1152*t → 31+54*t` with exponent 6 and strict descent.
- `SectionReturn.first_return_can_increase` — first return `31 → 121`.
- `SectionReturn.marked_sources_noDrop_for_any_horizon` — explicit
  marked sources defeat every fixed finite accelerated descent horizon.
- `SectionReturn.classicalCollatz_of_rankDescent` — a fixed natural rank
  with eventual descending marked returns (or a hit of 1) implies Collatz.
  **`RankDescent` is an open hypothesis**, not an established property.
- `SectionReturn.exists_rankDescent_iff_acceleratedCollatz` — existence
  of such a rank is equivalent to accelerated Collatz, making the
  boundary of the reduction explicit in the formal statement.

### `WeightedVisits.lean`
- `WeightedVisits.potential_sub_succ` — exact one-step loss of
  `weight/iterate` along the positive Syracuse orbit.
- `WeightedVisits.sum_loss_range` — telescoping identity over every
  finite initial segment.
- `WeightedVisits.sum_loss_finset_le` — the loss over any finite set
  of distinct times is at most `1/x`.
- `WeightedVisits.sum_weight_visits_le` — the sum of affine weights
  of visits from x>0 to R>0 is at most `R*(3*R+1)/x`, even if R is
  periodic. This is a weighted occupation bound, not orbit descent.

### `WeightedWords.lean`
- `WeightedVisits.matches_eq_of_length_eq` — exact words of the same
  length from the same source coincide.
- `WeightedVisits.word_sum_eq_exponentSum`, `wordWeight_eq_weight_of_matches`
  — word exponents and weights agree with the actual orbit data.
- `WeightedVisits.sum_wordWeight_fiber_le` — total affine weight of a
  finite set of distinct exact words from x to R is at most R*(3*R+1)/x.

### `WeightedCounting.lean`
- `WeightedCounting.sum_grouped_by_source` — group a finite weighted sum
  by distinct sources, allowing multiple representations.
- `WeightedCounting.weighted_sum_le_image_sum` — a fiber bound K/x gives
  the bound K/X times the sum over distinct sources x≥X>0.
- `WeightedCounting.card_image_lower_bound`, `card_image_selected_lower_bound`
  — mass at least η forces at least η*X/K distinct sources.
- `WeightedCounting.mazur_main_term_lower_bound` — the stated error
  budget and main-term inequality imply mass at least 3/(8*3^m).
  Both inequalities are hypotheses, not external analytic imports.

### `WeightedPredecessors.lean`
- `WeightedPredecessors.word_fiber_bound`, `selected_weighted_source_bound`
  — apply the grouped bounds to exact words with common endpoint R.
- `WeightedPredecessors.classical_hits_of_accelerated_hits` — expand a
  finite odd-input Syracuse path to the ordinary map with arbitrary target.
- `WeightedPredecessors.ordinary_predecessor_count_of_mass` — a path
  mass lower bound counts distinct ordinary predecessors below N.
- `WeightedPredecessors.conditional_predecessor_count` — a finite count
  at least 3*N/(256*R*(3*R+1)*3^m), assuming the exact paths, their source
  interval, and an analytic mass/error estimate. No no-return assumption
  is used; no unconditional positive-density conclusion is claimed.

## `Generated/` — machine-generated finite certificates

Verified by Lean; emitted by `../../scripts/phantom_taxonomy/` generators.

- `K16S16KDeterministicCW` — `k16s16KDeterministicGeneratedSpectralRadiusBound` (deterministic `(K,b)` bound `ρ ≤ 3/4`, `K₀=16`).
- `K16S16KLB5DeterministicCW`, `K16S16KLB6DeterministicCW` — finite
  variants with the same explicit `ρ ≤ 3/4` certificate form.
- `T10J32HighBitTailCW` — `t10j32HighBitTailSpectralRadiusBound_97_2000` (single-node `ρ ≤ 97/2000`); plus `…CWData`, `…CWRows00–13`.
- `K16S16KExactCWSummary`, `K16S16KSCC`, `K16S16KBridge` — 37-state empirical `(K,b)` CW + SCC + bridge.
- `T10CriticalSymbolic`, `T10J32HighBitTail` — exact `T=10` transfer-matrix imports.
- `A0ReturnBranches` — generated A0 return-branch data.

These contribute the bulk of the line/declaration count but are **generated**,
not hand-authored. See [`../../notes/PROJECT_STATISTICS.md`](../../notes/PROJECT_STATISTICS.md)
for the hand-written vs generated split.
