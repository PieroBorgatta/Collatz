/-
SPDX-License-Identifier: Apache-2.0
The mixing conversion adapts PredecessorAnalyticSupport.lean.
Copyright 2026 Lech Mazur; see LICENSE and UPSTREAM_NOTICE.
Modified 2026-09-24 for Piero Borgatta's predecessor development:
retain the sixth-power decay and the exact two-thirds L1 factor, and choose
the least positive conductor satisfying the resulting finite budget.
Changes and proofs produced with AI assistance.
-/

import Erdos1135.ND.PositiveDensity.PredecessorAnalyticSupport
import Mathlib.Data.Nat.Find
import Mathlib.Data.Nat.Sqrt

namespace Erdos1135.ND.PositiveDensity
namespace OptimizedConductor

/-- A finite witness for the decidable conductor search. -/
theorem exists_conductor (T C : ℕ) :
    ∃ m : ℕ, 1 ≤ m ∧ 88 * T * C ≤ m ^ 6 := by
  let B := 88 * T * C
  have hm : 1 ≤ B + 1 := Nat.succ_le_succ (Nat.zero_le B)
  have hpow : B + 1 ≤ (B + 1) ^ 6 := by
    simpa only [pow_one] using
      (pow_le_pow_right₀ hm (by decide : (1 : ℕ) ≤ 6))
  exact ⟨B + 1, hm, (Nat.le_succ B).trans hpow⟩

/-- The least positive conductor with sufficient sixth-power error budget.
The predicate is decidable and this natural-valued definition is computable;
no classical choice is used to select the conductor. -/
def conductor (T C : ℕ) : ℕ := Nat.find (exists_conductor T C)

theorem conductor_one_le (T C : ℕ) : 1 ≤ conductor T C :=
  (Nat.find_spec (exists_conductor T C)).1

theorem conductor_pos (T C : ℕ) : 0 < conductor T C :=
  lt_of_lt_of_le (by decide : (0 : ℕ) < 1) (conductor_one_le T C)

theorem conductor_budget (T C : ℕ) : 88 * T * C ≤ conductor T C ^ 6 :=
  (Nat.find_spec (exists_conductor T C)).2

theorem conductor_budget_real (T C : ℕ) :
    88 * (T : ℝ) * (C : ℝ) ≤ (conductor T C : ℝ) ^ 6 := by
  exact_mod_cast conductor_budget T C

theorem conductor_minimal {T C m : ℕ} (hm : 1 ≤ m)
    (hbudget : 88 * T * C ≤ m ^ 6) : conductor T C ≤ m :=
  Nat.find_min' (exists_conductor T C) ⟨hm, hbudget⟩

/-- A square-root conductor is already sufficient; the least sixth-root
conductor can only be smaller. The proof never evaluates the square root. -/
theorem conductor_le_sqrt (T C : ℕ) :
    conductor T C ≤ Nat.sqrt (88 * T * C) + 1 := by
  have hm : 1 ≤ Nat.sqrt (88 * T * C) + 1 :=
    Nat.succ_le_succ (Nat.zero_le _)
  apply conductor_minimal hm
  exact ((Nat.le_succ _).trans (Nat.succ_le_succ_sqrt' (88 * T * C))).trans
    (pow_le_pow_right₀ hm (by decide : (2 : ℕ) ≤ 6))

theorem conductor_le_budget_succ (T C : ℕ) :
    conductor T C ≤ 88 * T * C + 1 :=
  (conductor_le_sqrt T C).trans
    (Nat.add_le_add_right (Nat.sqrt_le_self (88 * T * C)) 1)

/-- Comparison with the original linear conductor in TwoSeedDensity. -/
theorem conductor_le_linear (T C : ℕ) :
    conductor T C ≤ 132 * T * C + 1 :=
  (conductor_le_budget_succ T C).trans
    (Nat.add_le_add_right
      (Nat.mul_le_mul_right C (Nat.mul_le_mul_right T (by decide : 88 ≤ 132))) 1)

theorem conductor_mono {T T' C C' : ℕ} (hT : T ≤ T') (hC : C ≤ C') :
    conductor T C ≤ conductor T' C' := by
  apply conductor_minimal (conductor_one_le T' C')
  exact (Nat.mul_le_mul (Nat.mul_le_mul_left 88 hT) hC).trans
    (conductor_budget T' C')

/-- Rescale the existing quadratic-census API without discarding the
sixth-power mixing decay or its exact L1 prefactor. -/
noncomputable def scaledConstant (C : ℝ) (m : ℕ) : ℝ :=
  (2 / 3 : ℝ) * C / (m : ℝ) ^ 4

theorem scaledConstant_nonneg {C : ℝ} (hC : 0 ≤ C) (m : ℕ) :
    0 ≤ scaledConstant C m :=
  div_nonneg (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2 / 3) hC)
    (pow_nonneg (Nat.cast_nonneg m) 4)

/-- The scale is fixed at the chosen conductor. Its dependence on m is
allowed by ndExplicitQuadraticMixingAt, which quantifies only over k ≥ m. -/
theorem scaled_quadratic_mixing {C : ℝ} (_hC : 0 ≤ C)
    (hmix : Tao.syracFineScaleMixingAt 6 C) {m : ℕ} (hm : 1 ≤ m) :
    ndExplicitQuadraticMixingAt (scaledConstant C m) m := by
  intro k hmk
  rw [unitReferenceDensity_fullL1_eq_twoThirds_oscillation hmk]
  calc
    _ ≤ (2 / 3 : ℝ) * (C / (m : ℝ) ^ 6) :=
      mul_le_mul_of_nonneg_left (hmix k m hm hmk) (by norm_num)
    _ = scaledConstant C m / (m : ℝ) ^ 2 := by
      unfold scaledConstant
      rw [div_div, ← pow_add]
      ring

/-- The sixth-power budget gives exactly the square budget required by the
existing terminal census. No sign assumption on T or C is needed for this
algebraic implication; positivity of m supplies the denominator. -/
theorem square_budget {T C : ℝ} {m : ℕ} (hm : 1 ≤ m)
    (hbudget : 88 * T * C ≤ (m : ℝ) ^ 6) :
    88 * T * scaledConstant C m ≤ (2 / 3 : ℝ) * (m : ℝ) ^ 2 := by
  have hmpos : (0 : ℝ) < m := by
    exact_mod_cast lt_of_lt_of_le (by decide : (0 : ℕ) < 1) hm
  have hm4 : (0 : ℝ) < (m : ℝ) ^ 4 := pow_pos hmpos 4
  unfold scaledConstant
  rw [← mul_div_assoc]
  apply (div_le_iff₀ hm4).mpr
  convert mul_le_mul_of_nonneg_left hbudget (by norm_num : (0 : ℝ) ≤ 2 / 3) using 1 <;>
    ring

theorem conductor_square_budget (T C : ℕ) :
    88 * (T : ℝ) * scaledConstant (C : ℝ) (conductor T C) ≤
      (2 / 3 : ℝ) * (conductor T C : ℝ) ^ 2 :=
  square_budget (conductor_one_le T C) (conductor_budget_real T C)

end OptimizedConductor
end Erdos1135.ND.PositiveDensity
