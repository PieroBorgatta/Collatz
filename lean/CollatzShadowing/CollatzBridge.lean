/-
Conditional proof bridge from finite/descent information to Collatz-type
termination statements.

This file deliberately does not prove the Collatz conjecture.  It records
the exact global descent hypothesis that would be sufficient to turn the
accelerated Syracuse formalization into termination at `1`.

Author: AI-assisted (Codex) + Piero Borgatta. Date: 2026-05-20.
-/

import CollatzShadowing.Basic

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

end CollatzShadowing
