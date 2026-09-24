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
