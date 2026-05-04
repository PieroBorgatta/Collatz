/-
Auxiliary lemmas for the proof of Lemma 3.1 (Phase 3 of `TODO.md`).

These lemmas correspond, one-to-one, to Phase 3 tasks 3.1, 3.1.5, 3.3,
and 3.4. Task 3.2 (the affine-difference identity) requires extending
the Syracuse map to `ℤ_[2]`, so it lives in a separate Phase 3
follow-up.

Author: AI-assisted (Claude) + Piero Borgatta. Date: 2026-05-04.
-/

import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.NumberTheory.Padics.PadicIntegers
import Mathlib.Algebra.BigOperators.Group.List.Basic
import CollatzShadowing.Phantom

namespace CollatzShadowing

/-!
## Task 3.4 — `B_m + 1 - B_j ≥ a_j + 1 ↔ B_m ≥ B_{j+1}`

This is purely arithmetical: by the recursion of `B`, the partial sum
satisfies `B (j+1) = B j + a_j`, so the equivalence reduces to
`B_m ≥ B_j + a_j ↔ B_m + 1 ≥ B_j + a_j + 1`, which is `omega`.
-/

namespace PhantomWord

/-- Recursive characterisation of `B` along the periodic word. With
`B` defined as the sum-form `((range m).map aAt).sum`, this is just
`List.range_succ` plus the singleton-sum simplification. -/
theorem B_succ (w : PhantomWord) (j : ℕ) :
    w.B (j + 1) = w.B j + w.aAt j := by
  change ((List.range (j + 1)).map w.aAt).sum = ((List.range j).map w.aAt).sum + w.aAt j
  rw [List.range_succ, List.map_append, List.sum_append, List.map_singleton,
      List.sum_singleton]

/-- **Task 3.4.** The bound `B_m + 1 - B_j ≥ a_j + 1` is equivalent to
`B_m ≥ B (j+1)`. -/
theorem B_bound_iff (w : PhantomWord) (j m : ℕ) :
    (w.aAt j + 1 ≤ w.B m + 1 - w.B j) ↔ (w.B (j + 1) ≤ w.B m) := by
  rw [B_succ]
  omega

end PhantomWord

/-!
## Task 3.1 — `ν₂(3 · n) = ν₂(n)` in `ℤ_[2]`

Since `3` is a unit in `ℤ_[2]` (its `2`-adic norm is `1`), multiplication
by `3` preserves the valuation. Mathlib gives this through
`PadicInt.valuation_mul` once we know `(3 : ℤ_[2]).valuation = 0`.
-/

/-- `(3 : ℤ_[2])` is non-zero. The `decide` tactic does not work on
`ℤ_[2]` (it lacks decidable equality), so we route through a `Nat`
cast injectivity argument. -/
theorem three_ne_zero_z2 : (3 : ℤ_[2]) ≠ 0 := by
  exact_mod_cast (by decide : (3 : ℕ) ≠ 0)

/-- `(3 : ℤ_[2])` has trivial `2`-adic valuation: `3` is not divisible
by `2`. There is no `PadicInt.valuation_natCast` in Mathlib v4.29.1, so
we route through `ℚ_[2]` via the `valuation_coe` simp lemma and the
existing `Padic.valuation_natCast`. -/
theorem valuation_three_z2 : (3 : ℤ_[2]).valuation = 0 := by
  have h1 : ((3 : ℤ_[2]) : ℚ_[2]).valuation = 0 := by
    have hcast : ((3 : ℤ_[2]) : ℚ_[2]) = ((3 : ℕ) : ℚ_[2]) := by push_cast; rfl
    rw [hcast, Padic.valuation_natCast]
    have h3 : padicValNat 2 3 = 0 :=
      padicValNat.eq_zero_of_not_dvd (by decide : ¬ (2 : ℕ) ∣ 3)
    exact_mod_cast h3
  -- `PadicInt.valuation_coe` gives `(x : ℚ_[p]).valuation = (x.valuation : ℤ)`.
  rw [PadicInt.valuation_coe] at h1
  exact_mod_cast h1

/-- **Task 3.1.** Multiplication by `3` is `ν₂`-invariant on `ℤ_[2]`. -/
theorem nu2Z2_three_mul (n : ℤ_[2]) : nu2Z2 (3 * n) = nu2Z2 n := by
  by_cases hn : n = 0
  · simp [hn, nu2Z2]
  · unfold nu2Z2
    rw [PadicInt.valuation_mul three_ne_zero_z2 hn, valuation_three_z2, zero_add]

/-!
## Task 3.1.5 — `QwOddDen` for every phantom

Strategy: lift the rational `qwRat w = Cw / (2^A_w − 3^L)` to its
integer-valued form `Rat.divInt (Cw : ℤ) qwIntDen`, where
`qwIntDen w := (2 : ℤ)^A_w − (3 : ℤ)^L` is non-zero and has odd
absolute value. Then:

* `Rat.den_dvd` gives `((divInt …).den : ℤ) ∣ qwIntDen`.
* `Int.natCast_dvd` converts to `(divInt …).den ∣ qwIntDen.natAbs`.
* `Odd.of_dvd_nat` then gives `Odd (divInt …).den`.
* Odd implies `¬ 2 ∣ den`.
-/

namespace PhantomWord

/-- A phantom word's exponent sum is at least its length: each entry is
≥ 1, hence the sum is ≥ length · 1. -/
theorem length_le_A (w : PhantomWord) : w.length ≤ w.A := by
  exact List.length_le_sum_of_one_le w.vals (fun a ha => w.positive a ha)

/-- `A_w ≥ 1` for any phantom word. -/
theorem one_le_Aw (w : PhantomWord) : 1 ≤ w.Aw := by
  rw [Aw_eq_A]
  have hL : 1 ≤ w.length := by
    rcases hvals : w.vals with _ | ⟨a, t⟩
    · exact absurd hvals w.nonempty
    · simp [PhantomWord.length, hvals]
  exact le_trans hL w.length_le_A

/-- The integer denominator `2^A_w − 3^L`. -/
def qwIntDen (w : PhantomWord) : ℤ :=
  (2 : ℤ) ^ w.Aw - (3 : ℤ) ^ w.length

/-- The integer denominator is odd: `2^A_w` is even (since `A_w ≥ 1`)
and `3^L` is odd, so their difference is odd. -/
theorem qwIntDen_odd (w : PhantomWord) : Odd (qwIntDen w) := by
  unfold qwIntDen
  apply Even.sub_odd
  · -- Even ((2 : ℤ)^Aw): since Aw ≥ 1, 2 ∣ 2^Aw
    rw [even_iff_two_dvd]
    exact dvd_pow_self _ (Nat.one_le_iff_ne_zero.mp w.one_le_Aw)
  · -- Odd ((3 : ℤ)^L): 3 is odd, hence 3^L is odd
    exact Odd.pow ⟨1, by ring⟩

/-- `qwRat w` written as a `Rat.divInt` of two integers. -/
theorem qwRat_eq_divInt (w : PhantomWord) :
    qwRat w = Rat.divInt (Cw w : ℤ) (qwIntDen w) := by
  unfold qwRat qwIntDen
  rw [Rat.divInt_eq_div]
  push_cast
  ring

/-- **Task 3.1.5.** The rational fixed point `q_w` of any phantom word
has odd denominator. Consequently `qwZ2 w` can be applied unconditionally
once we discharge the hypothesis with this theorem. -/
theorem qwOddDen (w : PhantomWord) : QwOddDen w := by
  unfold QwOddDen
  rw [qwRat_eq_divInt]
  -- Step 1: (den : ℤ) ∣ qwIntDen.
  have hdvdInt : ((Rat.divInt (Cw w : ℤ) (qwIntDen w)).den : ℤ) ∣ (qwIntDen w) :=
    Rat.den_dvd _ _
  -- Step 2: convert to ℕ-divisibility on natAbs.
  rw [Int.natCast_dvd] at hdvdInt
  -- hdvdInt : (Rat.divInt _ _).den ∣ (qwIntDen w).natAbs.
  -- Step 3: qwIntDen.natAbs is odd.
  have hodd_nat : Odd (qwIntDen w).natAbs := Odd.natAbs (qwIntDen_odd w)
  -- Step 4: divisor of odd is odd.
  have hden_odd : Odd (Rat.divInt (Cw w : ℤ) (qwIntDen w)).den :=
    Odd.of_dvd_nat hodd_nat hdvdInt
  -- Step 5: odd ⟹ ¬ 2 ∣.
  intro h2dvd
  have hmod0 : (Rat.divInt (Cw w : ℤ) (qwIntDen w)).den % 2 = 0 :=
    Nat.dvd_iff_mod_eq_zero.mp h2dvd
  have hmod1 : (Rat.divInt (Cw w : ℤ) (qwIntDen w)).den % 2 = 1 :=
    Nat.odd_iff.mp hden_odd
  omega

end PhantomWord

end CollatzShadowing
