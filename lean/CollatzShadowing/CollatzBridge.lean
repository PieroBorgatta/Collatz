/-
Conditional proof bridge from finite/descent information to Collatz-type
termination statements.

This file deliberately does not prove the Collatz conjecture.  It records
the exact global descent hypothesis that would be sufficient to turn the
accelerated Syracuse formalization into termination at `1`.

Author: AI-assisted (Codex) + Piero Borgatta. Date: 2026-05-20.
-/

import CollatzShadowing.Basic
import CollatzShadowing.WeakBridge

namespace CollatzShadowing

/-!
## Conditional Collatz bridge

The finite K16 Collatz-Wielandt certificates prove statements about
declared finite matrices.  They do not by themselves prove that every
integer orbit is captured by those matrices.

The bridge below isolates the missing mathematical obligation: every
positive odd integer different from `1` must have a finite accelerated
Syracuse iterate that is again positive odd and strictly smaller than
the starting integer.
-/

/-- The classical one-step Collatz map on natural numbers. -/
def collatzStep (n : ℕ) : ℕ :=
  if Even n then n / 2 else 3 * n + 1

/-- Classical Collatz termination, stated for positive natural numbers. -/
def ClassicalCollatzConjecture : Prop :=
  ∀ n : ℕ, 0 < n → ∃ k : ℕ, collatzStep^[k] n = 1

/-- Accelerated Syracuse termination for one initial value. -/
def acceleratedOrbitHitsOne (n : ℕ) : Prop :=
  ∃ k : ℕ, S^[k] n = 1

/--
Accelerated Collatz/Syracuse termination on positive odd natural
numbers.
-/
def AcceleratedCollatzConjecture : Prop :=
  ∀ n : ℕ, 0 < n → Odd n → acceleratedOrbitHitsOne n

/--
The global strict-descent hypothesis needed by the current finite-layer
program.

For every positive odd `n ≠ 1`, some finite accelerated Syracuse iterate
must be a positive odd integer strictly below `n`.  Proving this from the
phantom-shadowing finite certificates is the substantive missing step.
-/
def UniformStrictDescentHypothesis : Prop :=
  ∀ n : ℕ, 0 < n → Odd n → n ≠ 1 →
    ∃ k : ℕ, 0 < S^[k] n ∧ Odd (S^[k] n) ∧ S^[k] n < n

/-- On even inputs, the classical Collatz map is one halving step. -/
theorem collatzStep_of_even {n : ℕ} (h : Even n) :
    collatzStep n = n / 2 := by
  simp [collatzStep, h]

/-- On odd inputs, the classical Collatz map is the affine step `3n+1`. -/
theorem collatzStep_of_odd {n : ℕ} (h : Odd n) :
    collatzStep n = 3 * n + 1 := by
  simp [collatzStep, Nat.not_even_iff_odd.mpr h]

/--
If `2^k` divides `m`, then `k` classical Collatz steps from `m` are just
`k` halvings.
-/
theorem collatzStep_iterate_div_pow_two_of_pow_dvd
    (m k : ℕ) (h : 2 ^ k ∣ m) :
    collatzStep^[k] m = m / 2 ^ k := by
  induction k generalizing m with
  | zero =>
      simp
  | succ k ih =>
      have htwo_pow : 2 ∣ 2 ^ (k + 1) := by
        rw [pow_succ']
        exact dvd_mul_right 2 (2 ^ k)
      have htwo_m : 2 ∣ m := htwo_pow.trans h
      have heven_m : Even m := even_iff_two_dvd.mpr htwo_m
      have htail : 2 ^ k ∣ m / 2 := by
        rw [Nat.dvd_div_iff_mul_dvd htwo_m]
        simpa [pow_succ'] using h
      rw [Function.iterate_succ, Function.comp_apply,
        collatzStep_of_even heven_m, ih (m / 2) htail,
        Nat.div_div_eq_div_mul, pow_succ']

/-- The odd part of a positive natural number. -/
def natOddPart (n : ℕ) : ℕ :=
  n / 2 ^ nu2Nat n

theorem natOddPart_pos {n : ℕ} (hn : 0 < n) : 0 < natOddPart n := by
  have hdiv : 2 ^ nu2Nat n ∣ n := by
    simpa [nu2Nat] using (pow_padicValNat_dvd (p := 2) (n := n))
  have hpow_pos : 0 < 2 ^ nu2Nat n := pow_pos (by norm_num : 0 < (2 : ℕ)) _
  exact Nat.div_pos (Nat.le_of_dvd hn hdiv) hpow_pos

theorem natOddPart_odd {n : ℕ} (hn : 0 < n) : Odd (natOddPart n) := by
  have hn_ne : n ≠ 0 := Nat.ne_of_gt hn
  have hdiv : 2 ^ nu2Nat n ∣ n := by
    simpa [nu2Nat] using (pow_padicValNat_dvd (p := 2) (n := n))
  have hnot : ¬ 2 ∣ natOddPart n := by
    intro htwo
    have hpow_succ : 2 ^ (nu2Nat n + 1) ∣ n := by
      have hmul : 2 ^ nu2Nat n * 2 ∣ n :=
        (Nat.dvd_div_iff_mul_dvd hdiv).mp (by simpa [natOddPart] using htwo)
      simpa [pow_succ, mul_comm, mul_left_comm, mul_assoc, nu2Nat] using hmul
    exact pow_succ_padicValNat_not_dvd (p := 2) (n := n) hn_ne hpow_succ
  exact Nat.not_even_iff_odd.mp (by
    intro heven
    exact hnot (even_iff_two_dvd.mp heven))

theorem collatzStep_iterate_natOddPart (n : ℕ) :
    collatzStep^[nu2Nat n] n = natOddPart n := by
  have hdiv : 2 ^ nu2Nat n ∣ n := by
    simpa [nu2Nat] using (pow_padicValNat_dvd (p := 2) (n := n))
  simpa [natOddPart] using
    collatzStep_iterate_div_pow_two_of_pow_dvd n (nu2Nat n) hdiv

theorem syracuse_pos (n : ℕ) : 0 < S n := by
  have hm_pos : 0 < syracuseNumerator n := by
    simp [syracuseNumerator]
  have hdiv : 2 ^ syracuseExponent n ∣ syracuseNumerator n := by
    simpa [syracuseExponent, syracuseNumerator, nu2Nat] using
      (pow_padicValNat_dvd (p := 2) (n := 3 * n + 1))
  have hpow_pos : 0 < 2 ^ syracuseExponent n :=
    pow_pos (by norm_num : 0 < (2 : ℕ)) _
  exact Nat.div_pos (Nat.le_of_dvd hm_pos hdiv) hpow_pos

theorem syracuse_odd (n : ℕ) : Odd (S n) := by
  have hm_pos : 0 < syracuseNumerator n := by
    simp [syracuseNumerator]
  have hm_ne : syracuseNumerator n ≠ 0 := Nat.ne_of_gt hm_pos
  have hdiv : 2 ^ syracuseExponent n ∣ syracuseNumerator n := by
    simpa [syracuseExponent, syracuseNumerator, nu2Nat] using
      (pow_padicValNat_dvd (p := 2) (n := 3 * n + 1))
  have hnot : ¬ 2 ∣ S n := by
    intro htwo
    have hpow_succ :
        2 ^ (syracuseExponent n + 1) ∣ syracuseNumerator n := by
      have hmul : 2 ^ syracuseExponent n * 2 ∣ syracuseNumerator n :=
        (Nat.dvd_div_iff_mul_dvd hdiv).mp (by simpa [S] using htwo)
      simpa [pow_succ, mul_comm, mul_left_comm, mul_assoc,
        syracuseExponent, syracuseNumerator, nu2Nat] using hmul
    exact pow_succ_padicValNat_not_dvd
      (p := 2) (n := syracuseNumerator n) hm_ne hpow_succ
  exact Nat.not_even_iff_odd.mp (by
    intro heven
    exact hnot (even_iff_two_dvd.mp heven))

theorem collatzStep_iterate_syracuse {n : ℕ} (hodd : Odd n) :
    collatzStep^[syracuseExponent n + 1] n = S n := by
  have hdiv : 2 ^ syracuseExponent n ∣ 3 * n + 1 := by
    simpa [syracuseExponent, syracuseNumerator, nu2Nat] using
      (pow_padicValNat_dvd (p := 2) (n := 3 * n + 1))
  rw [Function.iterate_succ, Function.comp_apply, collatzStep_of_odd hodd]
  simpa [S, syracuseNumerator] using
    collatzStep_iterate_div_pow_two_of_pow_dvd
      (3 * n + 1) (syracuseExponent n) hdiv

/--
Every finite accelerated Syracuse orbit segment from a positive odd input
can be expanded into a finite classical Collatz orbit segment.
-/
theorem classical_hits_one_of_accelerated_hits_one
    {n k : ℕ} (hn : 0 < n) (hodd : Odd n) (h : S^[k] n = 1) :
    ∃ m : ℕ, collatzStep^[m] n = 1 := by
  induction k generalizing n with
  | zero =>
      exact ⟨0, by simpa using h⟩
  | succ k ih =>
      have htail : S^[k] (S n) = 1 := by
        simpa [Function.iterate_succ, Function.comp_apply] using h
      have hSpos : 0 < S n := syracuse_pos n
      have hSodd : Odd (S n) := syracuse_odd n
      obtain ⟨m, hm⟩ := ih hSpos hSodd htail
      exact ⟨m + (syracuseExponent n + 1), by
        rw [Function.iterate_add, Function.comp_apply,
          collatzStep_iterate_syracuse hodd, hm]⟩

/-- A concrete strict-descent witness for one accelerated odd orbit. -/
structure StrictDescentWitness (n : ℕ) where
  k : ℕ
  positive : 0 < S^[k] n
  odd : Odd (S^[k] n)
  descends : S^[k] n < n

/-- Propositional form of existence of an accelerated strict descent. -/
def HasStrictDescent (n : ℕ) : Prop :=
  ∃ k : ℕ, 0 < S^[k] n ∧ Odd (S^[k] n) ∧ S^[k] n < n

/-- Step-indexed direct drop for the accelerated Syracuse map. -/
def DirectDropAt (k n : ℕ) : Prop :=
  0 < S^[k] n ∧ Odd (S^[k] n) ∧ S^[k] n < n

/-- A step-indexed direct drop gives the existential strict-descent form. -/
theorem hasStrictDescent_of_directDropAt {k n : ℕ}
    (h : DirectDropAt k n) : HasStrictDescent n :=
  ⟨k, h.1, h.2.1, h.2.2⟩

/-- Any concrete strict-descent witness gives a step-indexed direct drop. -/
theorem directDropAt_of_witness {n : ℕ}
    (w : StrictDescentWitness n) : DirectDropAt w.k n :=
  ⟨w.positive, w.odd, w.descends⟩

/-- A concrete witness gives the propositional strict-descent statement. -/
theorem hasStrictDescent_of_witness {n : ℕ}
    (w : StrictDescentWitness n) : HasStrictDescent n :=
  ⟨w.k, w.positive, w.odd, w.descends⟩

/--
Convert the propositional strict-descent statement into a concrete
witness.  This uses classical choice and is meant only as a packaging
device; constructive proofs should provide `StrictDescentWitness` directly.
-/
noncomputable def strictDescentWitnessOfHasStrictDescent
    {n : ℕ} (h : HasStrictDescent n) : StrictDescentWitness n := by
  classical
  unfold HasStrictDescent at h
  exact
    ⟨Classical.choose h,
      (Classical.choose_spec h).1,
      (Classical.choose_spec h).2.1,
      (Classical.choose_spec h).2.2⟩

theorem hasStrictDescent_iff_nonempty_witness {n : ℕ} :
    HasStrictDescent n ↔ Nonempty (StrictDescentWitness n) := by
  constructor
  · intro h
    exact ⟨strictDescentWitnessOfHasStrictDescent h⟩
  · intro h
    rcases h with ⟨w⟩
    exact hasStrictDescent_of_witness w

/-- Package an explicitly found accelerated strict descent as a witness. -/
def strictDescentWitnessOfIterate
    {n k : ℕ}
    (hpos : 0 < S^[k] n)
    (hodd : Odd (S^[k] n))
    (hdrop : S^[k] n < n) :
    StrictDescentWitness n :=
  ⟨k, hpos, hodd, hdrop⟩

/-- One-step strict descent packaged as a witness. -/
def strictDescentWitnessOfOneStep
    {n : ℕ}
    (hpos : 0 < S n)
    (hodd : Odd (S n))
    (hdrop : S n < n) :
    StrictDescentWitness n :=
  strictDescentWitnessOfIterate
    (k := 1)
    (by simpa using hpos)
    (by simpa using hodd)
    (by simpa using hdrop)

/--
Abstract branch-cover route from the finite phantom-shadowing layer to
strict descent.

The source space `σ` may be infinite, while the branch label space `β` is
finite.  The structure packages exactly the extra theorem still missing
from the current finite diagnostics: every positive odd `n ≠ 1` must map
to a covered source, and every resolved covering branch must provide an
actual strict-descent witness for the accelerated Syracuse orbit of `n`.

This is intentionally conditional.  The existing finite prefix
certificates instantiate only finite summaries; they do not construct
this global branch-cover model.
-/
structure BranchDescentModel (σ β : Type*) [Fintype β] where
  sourceOf : ℕ → σ
  cover : WeakBridge.LabelSplit.BranchCover σ β
  counters : β → WeakBridge.LabelSplit.BranchCounters
  witness :
    ∀ ⦃n : ℕ⦄ ⦃b : β⦄,
      cover.Covers b (sourceOf n) →
      WeakBridge.LabelSplit.branchResolved (counters b) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n

/--
A resolved global branch-cover model is sufficient for the exact
`UniformStrictDescentHypothesis`.

This theorem is not a proof that such a model exists.  It isolates the
remaining bridge: construct the cover and prove that resolved branches
really give strict Syracuse descent for every positive odd source.
-/
theorem uniformStrictDescent_of_branchDescentModel
    {σ β : Type*} [Fintype β]
    (M : BranchDescentModel σ β)
    (hresolved : WeakBridge.LabelSplit.coverResolved M.cover M.counters) :
    UniformStrictDescentHypothesis := by
  intro n hn hodd hn1
  rcases M.cover.covers (M.sourceOf n) with ⟨b, hb⟩
  have hbResolved : WeakBridge.LabelSplit.branchResolved (M.counters b) :=
    hresolved hb
  let w := M.witness hb hbResolved hn hodd hn1
  exact ⟨w.k, w.positive, w.odd, w.descends⟩

/--
Global descent cover with explicitly declared loss classes.

This is a more audit-friendly version of `BranchDescentModel`.  For each
positive odd `n ≠ 1`, the cover must produce one of three outcomes:

* a direct strict-descent witness;
* a finite branch label whose counters are resolved and whose branch
  semantics give a strict-descent witness;
* a declared loss label whose semantics also give a strict-descent
  witness.

Thus an outside/budget/tail class can appear in this structure only after
it has been converted into an actual strict-descent witness.  Merely
listing a loss class is not enough.
-/
structure GlobalDescentCover (σ β loss : Type*) [Fintype β] [Fintype loss] where
  sourceOf : ℕ → σ
  BranchCovers : β → σ → Prop
  LossCovers : loss → σ → Prop
  branchCounters : β → WeakBridge.LabelSplit.BranchCounters
  branchWitness :
    ∀ ⦃n : ℕ⦄ ⦃b : β⦄,
      BranchCovers b (sourceOf n) →
      WeakBridge.LabelSplit.branchResolved (branchCounters b) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n
  lossWitness :
    ∀ ⦃n : ℕ⦄ ⦃ell : loss⦄,
      LossCovers ell (sourceOf n) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n
  cover :
    ∀ n : ℕ, 0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n ⊕
        ({ b : β // BranchCovers b (sourceOf n) } ⊕
          { ell : loss // LossCovers ell (sourceOf n) })

/-- All branch labels of a declared global cover have resolved counters. -/
def GlobalDescentCover.branchesResolved
    {σ β loss : Type*} [Fintype β] [Fintype loss]
    (C : GlobalDescentCover σ β loss) : Prop :=
  ∀ b : β, WeakBridge.LabelSplit.branchResolved (C.branchCounters b)

/--
A resolved global descent cover with declared loss witnesses implies the
uniform strict-descent hypothesis.

This theorem is conditional: it does not construct the cover and it does
not prove that the current finite A0 certificates supply one.
-/
theorem uniformStrictDescent_of_globalDescentCover
    {σ β loss : Type*} [Fintype β] [Fintype loss]
    (C : GlobalDescentCover σ β loss)
    (hresolved : C.branchesResolved) :
    UniformStrictDescentHypothesis := by
  intro n hn hodd hn1
  rcases C.cover n hn hodd hn1 with w | branchOrLoss
  · exact ⟨w.k, w.positive, w.odd, w.descends⟩
  · rcases branchOrLoss with branch | loss
    · rcases branch with ⟨b, hb⟩
      have w := C.branchWitness hb (hresolved b) hn hodd hn1
      exact ⟨w.k, w.positive, w.odd, w.descends⟩
    · rcases loss with ⟨ell, hell⟩
      have w := C.lossWitness hell hn hodd hn1
      exact ⟨w.k, w.positive, w.odd, w.descends⟩

/--
If every positive odd integer different from `1` eventually drops to a
smaller positive odd accelerated iterate, then accelerated Collatz
termination follows by strong induction.

This theorem is fully formalized and contains no computational or
spectral claim.  The open problem is the hypothesis
`UniformStrictDescentHypothesis`.
-/
theorem acceleratedCollatz_of_uniformStrictDescent
    (hdesc : UniformStrictDescentHypothesis) :
    AcceleratedCollatzConjecture := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
      intro hn hodd
      by_cases h1 : n = 1
      · exact ⟨0, by simp [h1]⟩
      · obtain ⟨k, hpos, hodd', hlt⟩ := hdesc n hn hodd h1
        obtain ⟨l, hl⟩ := ih (S^[k] n) hlt hpos hodd'
        exact ⟨l + k, by
          rw [Function.iterate_add, Function.comp_apply]
          exact hl⟩

/--
Bridge proposition from accelerated termination on positive odd numbers
to classical Collatz termination on all positive natural numbers.

This is separated from the finite-layer problem because it is a standard
arithmetical bridge between the full Collatz map and the accelerated
odd-only Syracuse map, not a spectral or phantom-shadowing claim.
-/
def AcceleratedToClassicalBridge : Prop :=
  AcceleratedCollatzConjecture → ClassicalCollatzConjecture

/--
Elementary bridge from accelerated odd termination to classical Collatz
termination.

The proof expands the initial even tail into repeated halvings, then
expands each accelerated Syracuse step into one odd `3n+1` step followed
by the exact number of halving steps.
-/
theorem acceleratedToClassicalBridge : AcceleratedToClassicalBridge := by
  intro hacc n hn
  let m := natOddPart n
  have hmpos : 0 < m := by
    simpa [m] using natOddPart_pos hn
  have hmodd : Odd m := by
    simpa [m] using natOddPart_odd hn
  obtain ⟨ka, hka⟩ := hacc m hmpos hmodd
  obtain ⟨kc, hkc⟩ :=
    classical_hits_one_of_accelerated_hits_one hmpos hmodd hka
  have hprefix : collatzStep^[nu2Nat n] n = m := by
    simpa [m] using collatzStep_iterate_natOddPart n
  exact ⟨kc + nu2Nat n, by
    rw [Function.iterate_add, Function.comp_apply, hprefix, hkc]⟩

/--
Classical Collatz follows from two explicit hypotheses:

1. the standard bridge from accelerated odd termination to full Collatz
   termination;
2. the global strict-descent hypothesis for accelerated odd orbits.

The first hypothesis should be a later elementary Lean target.  The
second is the real mathematical gap for the finite phantom-shadowing
program.
-/
theorem classicalCollatz_of_uniformStrictDescent
    (hbridge : AcceleratedToClassicalBridge)
    (hdesc : UniformStrictDescentHypothesis) :
    ClassicalCollatzConjecture :=
  hbridge (acceleratedCollatz_of_uniformStrictDescent hdesc)

/--
Classical Collatz follows from the strict-descent hypothesis alone,
because the accelerated-to-classical bridge is now proved.
-/
theorem classicalCollatz_of_uniformStrictDescent_provedBridge
    (hdesc : UniformStrictDescentHypothesis) :
    ClassicalCollatzConjecture :=
  acceleratedToClassicalBridge (acceleratedCollatz_of_uniformStrictDescent hdesc)

/--
A resolved global branch-descent model would imply classical Collatz.

This is still conditional on constructing the global branch-cover model;
it just removes the previously separate elementary accelerated/classical
bookkeeping obligation.
-/
theorem classicalCollatz_of_branchDescentModel
    {σ β : Type*} [Fintype β]
    (M : BranchDescentModel σ β)
    (hresolved : WeakBridge.LabelSplit.coverResolved M.cover M.counters) :
    ClassicalCollatzConjecture :=
  classicalCollatz_of_uniformStrictDescent_provedBridge
    (uniformStrictDescent_of_branchDescentModel M hresolved)

/--
A resolved global descent cover with declared loss witnesses would imply
classical Collatz.

This is the current Lean-level target for the finite/phantom-shadowing
program: construct such a cover, or show exactly which declared loss
class cannot be converted into a strict-descent witness.
-/
theorem classicalCollatz_of_globalDescentCover
    {σ β loss : Type*} [Fintype β] [Fintype loss]
    (C : GlobalDescentCover σ β loss)
    (hresolved : C.branchesResolved) :
    ClassicalCollatzConjecture :=
  classicalCollatz_of_uniformStrictDescent_provedBridge
    (uniformStrictDescent_of_globalDescentCover C hresolved)

/--
Declared unresolved finite-model loss classes for the current global
proof audit.

`drop below start` is not listed here: it is a direct strict-descent
witness, not a loss.  Resolved branch transitions are also not losses;
they are handled by the branch side of `GlobalDescentCover`.
-/
inductive FiniteModelLossKind where
  | outsideSCC
  | budgetExit
  | valuationTail
  | stepTail
  deriving Repr, DecidableEq, Fintype

/--
Coarse classes used when auditing a proposed finite/phantom-shadowing
global cover.
-/
inductive FiniteModelCoverClass where
  | directDrop
  | resolvedBranch
  | outsideSCC
  | budgetExit
  | valuationTail
  | stepTail
  deriving Repr, DecidableEq, Fintype

def FiniteModelLossKind.toCoverClass :
    FiniteModelLossKind → FiniteModelCoverClass
  | .outsideSCC => .outsideSCC
  | .budgetExit => .budgetExit
  | .valuationTail => .valuationTail
  | .stepTail => .stepTail

/--
Current proof status of a cover class.

This is an audit label, not a theorem about the Collatz dynamics:

* `witness`: the class is already a strict-descent witness by definition;
* `branch`: the class is acceptable only after branch semantics and
  resolved counters produce a strict-descent witness;
* `openLoss`: the class is not acceptable in a proof until converted into
  a strict-descent witness or proved absent.
-/
inductive CoverClassStatus where
  | witness
  | branch
  | openLoss
  deriving Repr, DecidableEq, Fintype

def FiniteModelCoverClass.currentStatus :
    FiniteModelCoverClass → CoverClassStatus
  | .directDrop => .witness
  | .resolvedBranch => .branch
  | .outsideSCC => .openLoss
  | .budgetExit => .openLoss
  | .valuationTail => .openLoss
  | .stepTail => .openLoss

theorem finiteModelCoverClass_currentStatus :
    FiniteModelCoverClass.currentStatus .directDrop = .witness
      ∧ FiniteModelCoverClass.currentStatus .resolvedBranch = .branch
      ∧ FiniteModelCoverClass.currentStatus .outsideSCC = .openLoss
      ∧ FiniteModelCoverClass.currentStatus .budgetExit = .openLoss
      ∧ FiniteModelCoverClass.currentStatus .valuationTail = .openLoss
      ∧ FiniteModelCoverClass.currentStatus .stepTail = .openLoss := by
  simp [FiniteModelCoverClass.currentStatus]

/--
The current concrete global-cover target for the finite model: branch
labels are abstract, while loss labels are exactly the declared audit
classes `FiniteModelLossKind`.
-/
abbrev FiniteModelGlobalCover (σ β : Type*) [Fintype β] :=
  GlobalDescentCover σ β FiniteModelLossKind

theorem classicalCollatz_of_finiteModelGlobalCover
    {σ β : Type*} [Fintype β]
    (C : FiniteModelGlobalCover σ β)
    (hresolved : C.branchesResolved) :
    ClassicalCollatzConjecture :=
  classicalCollatz_of_globalDescentCover C hresolved

/--
A small Type-level wrapper around a proposition.

It is used in cover specifications whose cases must be pattern-matched to
construct data, such as `StrictDescentWitness`.
-/
abbrev ProofToken (P : Prop) : Type :=
  { _u : Unit // P }

def proofTokenOf {P : Prop} (h : P) : ProofToken P :=
  ⟨(), h⟩

/--
Soundness condition for a direct-drop predicate on a source space.

This is the proposition one should prove for an actual finite/A0 source
model: whenever the source attached to `n` is marked as a direct drop, the
accelerated orbit of `n` has a strict-descent event.
-/
def DirectDropSound {σ : Type*}
    (sourceOf : ℕ → σ) (DirectDropCovers : σ → Prop) : Prop :=
  ∀ ⦃n : ℕ⦄,
    DirectDropCovers (sourceOf n) →
    0 < n → Odd n → n ≠ 1 →
    HasStrictDescent n

/--
Turn propositional direct-drop soundness into the concrete witness
function required by `FiniteModelCoverSpec`.
-/
noncomputable def directDropWitnessOfSound
    {σ : Type*} {sourceOf : ℕ → σ} {DirectDropCovers : σ → Prop}
    (hsound : DirectDropSound sourceOf DirectDropCovers) :
    ∀ ⦃n : ℕ⦄,
      DirectDropCovers (sourceOf n) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n := by
  intro n hdrop hn hodd hn1
  exact strictDescentWitnessOfHasStrictDescent
    (hsound hdrop hn hodd hn1)

/--
Audit-friendly specification for the current finite-model global cover.

Compared with `FiniteModelGlobalCover`, this separates the direct-drop
predicate from the direct-drop witness.  This is the form in which the
next proof obligations should be attacked:

* prove that `DirectDropCovers` really gives `StrictDescentWitness`;
* prove branch semantics for resolved branches;
* prove every declared loss class has a witness, or prove it cannot occur.
-/
structure FiniteModelCoverSpec (σ β : Type*) [Fintype β] where
  sourceOf : ℕ → σ
  DirectDropCovers : σ → Prop
  BranchCovers : β → σ → Prop
  LossCovers : FiniteModelLossKind → σ → Prop
  branchCounters : β → WeakBridge.LabelSplit.BranchCounters
  directDropWitness :
    ∀ ⦃n : ℕ⦄,
      DirectDropCovers (sourceOf n) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n
  branchWitness :
    ∀ ⦃n : ℕ⦄ ⦃b : β⦄,
      BranchCovers b (sourceOf n) →
      WeakBridge.LabelSplit.branchResolved (branchCounters b) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n
  lossWitness :
    ∀ ⦃n : ℕ⦄ ⦃ell : FiniteModelLossKind⦄,
      LossCovers ell (sourceOf n) →
      0 < n → Odd n → n ≠ 1 →
      StrictDescentWitness n
  cover :
    ∀ n : ℕ, 0 < n → Odd n → n ≠ 1 →
      ProofToken (DirectDropCovers (sourceOf n)) ⊕
        ({ b : β // BranchCovers b (sourceOf n) } ⊕
          { ell : FiniteModelLossKind // LossCovers ell (sourceOf n) })

def FiniteModelCoverSpec.toGlobalDescentCover
    {σ β : Type*} [Fintype β]
    (S : FiniteModelCoverSpec σ β) :
    FiniteModelGlobalCover σ β :=
  { sourceOf := S.sourceOf,
    BranchCovers := S.BranchCovers,
    LossCovers := S.LossCovers,
    branchCounters := S.branchCounters,
    branchWitness := S.branchWitness,
    lossWitness := S.lossWitness,
    cover := by
      intro n hn hodd hn1
      rcases S.cover n hn hodd hn1 with direct | branchOrLoss
      · exact Sum.inl (S.directDropWitness direct.property hn hodd hn1)
      · exact Sum.inr branchOrLoss }

theorem classicalCollatz_of_finiteModelCoverSpec
    {σ β : Type*} [Fintype β]
    (S : FiniteModelCoverSpec σ β)
    (hresolved : S.toGlobalDescentCover.branchesResolved) :
    ClassicalCollatzConjecture :=
  classicalCollatz_of_finiteModelGlobalCover
    S.toGlobalDescentCover hresolved

end CollatzShadowing
