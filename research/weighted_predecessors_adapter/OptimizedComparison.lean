/-
SPDX-License-Identifier: Apache-2.0
Copyright 2026 Piero Borgatta.
Comparisons of the explicit constants in the two quantitative constructions.
Changes and proofs produced with AI assistance.
-/

import OptimizedDensity

/-!
The comparisons concern the displayed target-based constants themselves.
They require neither a chosen seed nor a mixing hypothesis. The condition
`3 ∤ a` needed by the predecessor theorem is also unnecessary here.
-/

namespace Erdos1135.ND.PositiveDensity
namespace OptimizedComparison

theorem rootBound_pos {a : ℕ} (ha : 0 < a) (C : ℕ) :
    0 < OptimizedDensity.rootBound a C := by
  exact CompactSeedNonreturn.seedBound_pos ha _ _

theorem rootBound_lt {a : ℕ} (ha : 0 < a) (C : ℕ) :
    OptimizedDensity.rootBound a C < TwoSeedDensity.rootBound a C := by
  exact CompactSeedNonreturn.seedBound_lt_old ha
    (ndRootCoreBackwardConductor OptimizedDensity.fixedFloor
      (explicitSeedFloor OptimizedDensity.fixedFloor (OptimizedDensity.seedGeneration C) / 4)
      (OptimizedDensity.seedGeneration C)) OptimizedDensity.fixedFloor

theorem conductor_le {a : ℕ} (ha : 0 < a) (C : ℕ) :
    OptimizedDensity.conductor a C ≤ TwoSeedDensity.conductor a C := by
  calc
    OptimizedDensity.conductor a C ≤
        132 * OptimizedDensity.rootBound a C * C + 1 :=
      OptimizedConductor.conductor_le_linear _ _
    _ ≤ 132 * TwoSeedDensity.rootBound a C * C + 1 :=
      Nat.add_le_add_right
        (Nat.mul_le_mul_right C
          (Nat.mul_le_mul_left 132 (rootBound_lt ha C).le)) 1
    _ = TwoSeedDensity.conductor a C := rfl

/-- When the supplied mixing coefficient is positive, even the conductor
comparison is strict. -/
theorem conductor_lt {a C : ℕ} (ha : 0 < a) (hC : 0 < C) :
    OptimizedDensity.conductor a C < TwoSeedDensity.conductor a C := by
  calc
    OptimizedDensity.conductor a C ≤
        132 * OptimizedDensity.rootBound a C * C + 1 :=
      OptimizedConductor.conductor_le_linear _ _
    _ < 132 * TwoSeedDensity.rootBound a C * C + 1 :=
      Nat.add_lt_add_right
        (Nat.mul_lt_mul_of_pos_right
          (Nat.mul_lt_mul_of_pos_left (rootBound_lt ha C) (by decide)) hC) 1
    _ = TwoSeedDensity.conductor a C := rfl

theorem countStart_le {a : ℕ} (ha : 0 < a) (C : ℕ) :
    OptimizedDensity.countStart a C ≤ TwoSeedDensity.countStart a C := by
  have hm := conductor_le ha C
  change OptimizedDensity.markedStart C + 2 * OptimizedDensity.conductor a C +
      20 * 10 ^ 9 ≤
    OptimizedDensity.markedStart C + 2 * TwoSeedDensity.conductor a C + 20 * 10 ^ 9
  omega

private theorem intervalExponent_mono (b L : ℕ) {N N' : ℕ} (hN : N ≤ N') :
    (2 * N + 4) * b * 2 ^ N + N * (L * (N + 1) + 1) ≤
      (2 * N' + 4) * b * 2 ^ N' + N' * (L * (N' + 1) + 1) := by
  have hpow : (2 : ℕ) ^ N ≤ 2 ^ N' := Nat.pow_le_pow_right (by decide) hN
  exact Nat.add_le_add
    (Nat.mul_le_mul
      (Nat.mul_le_mul_right b (by omega : 2 * N + 4 ≤ 2 * N' + 4)) hpow)
    (Nat.mul_le_mul hN
      (Nat.add_le_add_right
        (Nat.mul_le_mul_left L (Nat.add_le_add_right hN 1)) 1))

/-- The explicit interval height is monotone in the root bound and the
generation, without any positivity assumptions on those parameters. -/
theorem explicitRootIntervalHeight_mono (b L : ℕ) {M M' N N' : ℕ}
    (hM : M ≤ M') (hN : N ≤ N') :
    ndExplicitRootIntervalHeight b L M N ≤ ndExplicitRootIntervalHeight b L M' N' := by
  unfold ndExplicitRootIntervalHeight
  exact Nat.mul_le_mul
    (Nat.pow_le_pow_right (by decide) (intervalExponent_mono b L hN)) hM

/-- A strict improvement in the root bound gives a strict height improvement,
even when the new and old generation indices coincide. -/
theorem explicitRootIntervalHeight_lt (b L : ℕ) {M M' N N' : ℕ}
    (hM : M < M') (hN : N ≤ N') :
    ndExplicitRootIntervalHeight b L M N < ndExplicitRootIntervalHeight b L M' N' := by
  unfold ndExplicitRootIntervalHeight
  calc
    2 ^ ((2 * N + 4) * b * 2 ^ N + N * (L * (N + 1) + 1)) * M <
        2 ^ ((2 * N + 4) * b * 2 ^ N + N * (L * (N + 1) + 1)) * M' :=
      Nat.mul_lt_mul_of_pos_left hM (by positivity)
    _ ≤ 2 ^ ((2 * N' + 4) * b * 2 ^ N' + N' * (L * (N' + 1) + 1)) * M' :=
      Nat.mul_le_mul_right M'
        (Nat.pow_le_pow_right (by decide) (intervalExponent_mono b L hN))

theorem intervalHeight_lt {a : ℕ} (ha : 0 < a) (C : ℕ) :
    OptimizedDensity.intervalHeight a C < TwoSeedDensity.intervalHeight a C := by
  exact explicitRootIntervalHeight_lt OptimizedDensity.fixedFloor 17
    (rootBound_lt ha C) (countStart_le ha C)

theorem cutoff_lt {a : ℕ} (ha : 0 < a) (C : ℕ) :
    OptimizedDensity.cutoff a C < TwoSeedDensity.cutoff a C := by
  unfold OptimizedDensity.cutoff TwoSeedDensity.cutoff
  exact Nat.mul_lt_mul_of_pos_left
    (Nat.add_lt_add_right (intervalHeight_lt ha C) 1) (by decide)

theorem coefficient_pos {a : ℕ} (ha : 0 < a) (C : ℕ) :
    0 < OptimizedDensity.coefficient a C := by
  have hroot : (0 : ℝ) < OptimizedDensity.rootBound a C := by
    exact_mod_cast rootBound_pos ha C
  unfold OptimizedDensity.coefficient
  positivity

theorem old_coefficient_pos {a : ℕ} (ha : 0 < a) (C : ℕ) :
    0 < TwoSeedDensity.coefficient a C := by
  have hroot : (0 : ℝ) < TwoSeedDensity.rootBound a C := by
    exact_mod_cast (rootBound_pos ha C).trans (rootBound_lt ha C)
  unfold TwoSeedDensity.coefficient
  positivity

/-- The gain from the smaller root bound is strict even if rounding leaves
the conductor unchanged. -/
theorem old_coefficient_lt {a : ℕ} (ha : 0 < a) (C : ℕ) :
    TwoSeedDensity.coefficient a C < OptimizedDensity.coefficient a C := by
  have hrootpos : (0 : ℝ) < OptimizedDensity.rootBound a C := by
    exact_mod_cast rootBound_pos ha C
  have hrootlt : (OptimizedDensity.rootBound a C : ℝ) < TwoSeedDensity.rootBound a C := by
    exact_mod_cast rootBound_lt ha C
  have hpow : (3 : ℝ) ^ OptimizedDensity.conductor a C ≤
      (3 : ℝ) ^ TwoSeedDensity.conductor a C :=
    pow_le_pow_right₀ (by norm_num) (conductor_le ha C)
  have hpowpos : (0 : ℝ) < (3 : ℝ) ^ OptimizedDensity.conductor a C :=
    pow_pos (by norm_num) _
  have hdenom :
      256 * (OptimizedDensity.rootBound a C : ℝ) *
          (3 : ℝ) ^ OptimizedDensity.conductor a C <
        256 * (TwoSeedDensity.rootBound a C : ℝ) *
          (3 : ℝ) ^ TwoSeedDensity.conductor a C := by
    calc
      _ < 256 * (TwoSeedDensity.rootBound a C : ℝ) *
          (3 : ℝ) ^ OptimizedDensity.conductor a C :=
        mul_lt_mul_of_pos_right
          (mul_lt_mul_of_pos_left hrootlt (by norm_num)) hpowpos
      _ ≤ _ := mul_le_mul_of_nonneg_left hpow
        (mul_nonneg (by norm_num : (0 : ℝ) ≤ 256) (Nat.cast_nonneg _))
  exact div_lt_div_of_pos_left (by norm_num)
    (mul_pos (mul_pos (by norm_num) hrootpos) hpowpos) hdenom

theorem publicCoefficient_lt {a : ℕ} (ha : 0 < a) :
    TwoSeedDensity.publicCoefficient a < OptimizedDensity.publicCoefficient a :=
  old_coefficient_lt ha explicitSyracuseMixingCoefficient

theorem publicCutoff_lt {a : ℕ} (ha : 0 < a) :
    OptimizedDensity.publicCutoff a < TwoSeedDensity.publicCutoff a :=
  cutoff_lt ha explicitSyracuseMixingCoefficient

/-- A simultaneous strict comparison of the published formulas. The density
theorems themselves additionally require that the target is not divisible by 3. -/
theorem public_constants_strictly_improve {a : ℕ} (ha : 0 < a) :
    0 < TwoSeedDensity.publicCoefficient a ∧
      TwoSeedDensity.publicCoefficient a < OptimizedDensity.publicCoefficient a ∧
      OptimizedDensity.publicCutoff a < TwoSeedDensity.publicCutoff a :=
  ⟨old_coefficient_pos ha explicitSyracuseMixingCoefficient,
    publicCoefficient_lt ha, publicCutoff_lt ha⟩

end OptimizedComparison
end Erdos1135.ND.PositiveDensity
