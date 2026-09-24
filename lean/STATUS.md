# Current mathematical status

Updated 2026-09-24. The published v1–v6 Zenodo PDFs are frozen snapshots.
Published [v6](https://doi.org/10.5281/zenodo.22936057) includes the erratum
to v4; subsequent working-tree developments are separate from its frozen
supplementary archive. This working tree targets pinned Lean v4.29.1 and Mathlib
v4.29.1; portability to later toolchains has not been checked.

## Proved in Lean

- Exact congruential shadowing and exclusion of positive integer orbits
  that remain forever on one expanding periodic phantom word.
- Finite Collatz–Wielandt bounds for explicitly generated matrices,
  including `ρ ≤ 3/4` for the deterministic `(K,b)` certificate. These are
  finite matrix statements and do not establish an infinite-operator gap.
- Exact loss of `w.sum` bits of 2-adic precision each time one fixed
  expansive word `w` matches a positive integer orbit; hence a finite
  budget for consecutive repetitions of that word.
- The full library build on 24 September 2026 checks
  `syracuseWordMatches_iff_exactResidue`: a nonempty positive-exponent
  word matches iff its affine numerator equals `2^A` modulo
  `2^(A+1)`. `repeatPhantomWord_matches_iff_exactResidue` gives modulus
  `2^(kA+1)` for `k > 0` repetitions. The unique odd residue class and
  natural density are paper-level deductions, not formalized here.
- Necessary equation, contractivity, and prefix constraints for a
  hypothetical positive cycle. These do not exclude every nontrivial cycle.
- Two explicit infinite residue subfamilies of the A0 source cylinder
  have strict descent. A finite-word threshold test and a trace-switching
  identity are also proved, together with counterexamples to several
  proposed global rankings.
- For every `R`, two positive odd inputs have `2^R ∣ (3n+1)` but distinct
  accelerated outputs `1` and `7`
  (`singular_outputs_separated_at_every_precision`). This is the exact
  finite-precision arithmetic witness near `−1/3`; topology itself is
  not formalized in that theorem.
- A uniform strict-descent hypothesis implies accelerated and classical
  Collatz by strong induction. The hypothesis is not proved here.
- Post-v6 shortcut coverage: an explicit residue/valuation rank proves
  that every positive shortcut orbit reaches 1 or `20 mod 27` within
  `13*n+4` steps. The sufficient residue is classical; the rank is a
  concrete certificate integrated here.
- An exact six-progression characterization of marked Syracuse episodes,
  unconditional arrival at 1 or this section, and arbitrarily late section
  visits on any orbit that never reaches 1.
- Universal cancellation-tower formulas, all three terminal phases, and
  absence of descent through the complete macro for every even `k≥30`.
  The subfamily `k=18*t+10` belongs to the first section port. In particular,
  marked sources defeat every fixed finite accelerated descent horizon.
- Exact descending marked returns `661+1152*t → 31+54*t` for every t,
  and an increasing first marked return `31 → 121`.
- A telescoping identity for affine orbit weights and the bound
  `sum_{k in H} 3^k/2^(A_k) ≤ R*(3*R+1)/x` for every finite set H of
  visits from x>0 to R>0 (`WeightedVisits.sum_weight_visits_le`).
  No assumption about periodicity or convergence is used. The formal
  theorem is indexed by distinct times. `WeightedWords` now proves the
  corresponding bound for distinct exact exponent words.
- Finite weighted counting without source injectivity: grouping words
  with the same source gives `sum selectedWeight ≤ K/X * card sources`
  for sources at least X>0 and K=R*(3*R+1). Exact odd-source paths also
  give ordinary Collatz predecessors. The final finite theorem yields
  `card predecessors below N ≥ 3*N/(256*K*3^m)` from an explicitly
  assumed analytic mass estimate and error budget; it does not prove
  those assumptions or a positive-density theorem.

- A bounded pair of Syracuse seeds: `L(n)=4*n+1` preserves the next state,
  and one of n and L(n) has no positive return. Above each height X, one of
  `L^[X+1](n)` and `L^[X+2](n)` works, with an explicit common upper bound.
  This uses the standard injectivity of a map on its periodic points;
  it does not decide which candidate works or exclude cycles of the successor.
- At a target R with no positive return, visiting time and exact word are
  unique for each source. The word fiber bound sharpens to R/x, giving a
  conditional predecessor count at least 3*N/(256*R*3^m). The analytic
  mass inequality and error budget remain explicit assumptions.

## Still open in this development

The main missing statement is `UniformStrictDescentHypothesis`: every
positive odd integer other than `1` must have an accelerated iterate below
itself. The named `A0FirstBarrierExistsAll` and
`A0FirstBarrierThresholdAutomatic` hypotheses are also open; both are
needed for the current A0 exit theorem, which covers only that family.
A global descent cover has not been constructed.

The post-v6 section has **unconditional coverage**, but no global return
rank. `SectionReturn.RankDescent R` requires a hit of 1 or an actual later
marked state with smaller R. Its existence is formally equivalent to
accelerated Collatz (`exists_rankDescent_iff_acceleratedCollatz`). This is
an exact interface for the open obligation, not a weakening of it.

The weighted counting direction has a formal local bridge from exact words
to distinct ordinary predecessors. A separate hash-pinned Lean 4.30.0-rc2
[overlay](../research/weighted_predecessors_adapter/README.md) now contains
both the external path adapter and a two-seed route to uniform constants.
The full external build and the final theorem dependency audits are tracked
separately; this snapshot does not yet claim they passed. A local partial
replay checked 37 of 393 modules before it was interrupted under resource
pressure; the complete modular job runs in CI. Targeted semantic audits of
the seed and mixing wrappers do not replace full analytical review.

The integrated main-library build with `TwoSeed` and `NonreturnCounting`
passed (3371 jobs), as did CI run 36001432687. Sixteen headline declarations
were audited and use only `propext`, `Classical.choice`, and `Quot.sound`. The new proof and comparison report is
[here](../notes/post_v6_adapter_2026-09-24/RESULTS_IT.md). It distinguishes
these results from the paper-level comparison of coefficients and from the
external analytical chain. For aligned explicit candidates, the comparison
proves T<R² and a coefficient improvement by more than a factor of three;
this comparison has not been formalized in Lean and does not compare cutoffs.

The earlier conditional counting boundary is recorded in
[the counting report](../notes/post_v6_counting_2026-09-24/RESULTS_IT.md).
Post-tower parameter formulas and resonance distributions are paper-level
deductions with exact finite checks, not Lean theorems; see
[the further research note](../notes/post_v6_parameter_2026-09-24/IDEAS_IT.md).

The integrated build including all three new counting modules passed
(3369 jobs). Fourteen headline declarations were audited and use only
`propext`, `Classical.choice`, and `Quot.sound`; none of those modules
uses `native_decide`. Build output and source hashes are recorded in the
counting report's verification manifest.

The general v6 defect/cancellation ledger remains a paper-level proposal.
Its concrete cancellation-tower family is now treated in
`CancellationTower.lean`; arbitrary switches remain uncontrolled. Equal-valuation
cancellation can raise destination precision even when the affine defect
has no 2-adic root; a proposed finite-cylinder checker must treat those
critical cases explicitly.

The post-v6 development, finite synthesis prototype, and verification
record are in [the continuation report](../notes/post_v6_section_2026-09-24/RESULTS_IT.md).
The integrated library build passed (3365 jobs); thirteen new headline
theorems were audited and depend only on `propext`, `Classical.choice`,
and `Quot.sound`. None of the five new modules uses `native_decide`.

The total `Syracuse2adic` function agrees with the natural-number map on
positive odd inputs but is discontinuous at `−1/3`. Published v6
uses infinite positive-exponent coding only on orbits avoiding that
singular point. Its coding observation says that excluding **all**
non-eventually-periodic words from positive integers is equivalent to the
no-unbounded-orbit problem; it does not prohibit more specific pointwise
arguments.

See [the declaration index](CollatzShadowing/THEOREM_INDEX.md) for exact
Lean statements and [project statistics](../notes/PROJECT_STATISTICS.md)
for historical and current file counts.

The `CollatzShadowing` Lean sources have no `sorry`, `admit`, or
project-declared `axiom`. A `#print axioms` audit of selected structural
headline theorems found only standard Lean axioms. Several finite proofs
use `native_decide`; their generated axiom dependencies place the native
compiler in the trusted base, so the source scan is not a kernel-only
guarantee.

The pinned Lean 4.29.1 predates a documented
[kernel soundness fix in 4.32.2](https://lean-lang.org/doc/reference/latest/releases/v4.32.2/)
and further [soundness fixes and defensive checks in
4.34.0](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/).
Nothing here shows that this project uses those defects. For a new
publication-grade verification, recheck the development with Lean 4.34.0
and a matching Mathlib revision, then repeat the axioms audit. That
portability recheck has not yet been done.
