/-
SPDX-License-Identifier: Apache-2.0
Derived from GeneralTargetPositiveDensity.lean, Copyright 2026 Lech Mazur.
See LICENSE and UPSTREAM_NOTICE. Modified 2026-09-24 for Piero Borgatta:
replace the non-returning seed by a finite residue lift and weighted occupation.
Changes and proofs produced with AI assistance.
-/

import WeightedTerminalAdapter
import WeightedCensus
import WeightedFrozenSeed
import Erdos1135.ND.PositiveDensity.ExplicitNumericalSyracuseMixing

namespace Erdos1135.ND.PositiveDensity
noncomputable section

theorem weighted_predecessors_positive_lower_density
    {a : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a) :
    ∃ c : ℝ, 0 < c ∧ ∃ X0 : ℕ, ∀ X : ℕ, X0 ≤ X →
      c * (X : ℝ) ≤ (Terras.natCount (ordinaryPredecessorSet a) X : ℝ) := by
  let b : ℕ := 2 ^ 80
  let C : ℕ := explicitSyracuseMixingCoefficient
  let N := explicitLogarithmicSeedGeneration b C
  let Nmark := explicitLogarithmicGoodMarkedStart b C N
  have hmix : Tao.syracFineScaleMixingAt 6 (C : ℝ) := explicitSyracuseMixing_six
  obtain ⟨r, hr, hl, ht, _hunit, hgood⟩ :=
    weighted_exists_generalTarget_uniform_twoThirds_seed ha hthree (b := b) le_rfl C hmix
      (N := N) le_rfl
  have hb200 : 200 ≤ b := by dsimp [b]; norm_num
  let U := ndRootCoreSingletonState b r hb200 hr hl
  let cap := fun j : ℕ => 16 + j / 100
  have he : U.rootSpan 0 := by intro i j; change r ≤ 2 ^ 0 * r; simp
  have hcap : ∀ j, cap j ≤ 17 * (j + 1) := by
    intro j
    have hj := Nat.div_le_self j 100
    dsimp [cap]
    omega
  have hreach : ∀ i, Erdos1135.Reaches (U.state.root i) a := fun _ => ht
  let P : ℝ := (r : ℝ) * (3 * (r : ℝ) + 1)
  have hPpos : 0 < P := by
    have hrpos : (0 : ℝ) < r := by exact_mod_cast hr.pos
    dsimp [P]
    positivity
  have hcharge : U.WeightedSourceCharge P := by
    intro cap n shift K X hX hsource psi hp
    exact WeightedTerminalAdapter.singletonTerminal_weighted_source_bound
      b r hb200 hr hl cap n shift K X hX hsource psi hp
  let m : ℕ := 132 * (r * (3 * r + 1)) * C + 1
  have hm : 1 ≤ m := by dsimp [m]; omega
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hmdef : (m : ℝ) = 132 * P * (C : ℝ) + 1 := by
    dsimp [m, P]
    push_cast
    ring
  have hsquare : 88 * P * (C : ℝ) ≤ (2 / 3 : ℝ) * (m : ℝ) ^ 2 := by
    nlinarith [sq_nonneg ((m : ℝ) - 1)]
  have hquadratic : ndExplicitQuadraticMixingAt (C : ℝ) m :=
    explicitMixing_quadratic (Nat.cast_nonneg C) hmix hm
  let J := Nmark + 2 * m + 20 * 10 ^ 9
  let H := ndExplicitRootIntervalHeight b 17 r J
  let eta : ℝ := 9 * (2 / 3 : ℝ) / (16 * ((3 ^ m : ℕ) : ℝ))
  have heta : 0 < eta := by dsimp [eta]; positivity
  refine ⟨eta / (32 * P), by positivity, 32 * (H + 1), ?_⟩
  apply U.generalTarget_publicCount_from_mass_of_weightedCharge P hPpos hcharge a hreach cap he hcap J H
    (by dsimp [J]; omega)
    (fun i => U.iterate_physicalIntervalMax_le_explicit cap 17 r hcap (fun _ => le_rfl) J i)
  intro n hn V X hX hi
  have hroom := U.explicitConductor_quarter_room cap m n (by dsimp [J] at hn; omega)
  exact U.fullGoodCoreTerminalMass_ge_of_square_budget_and_height_of_weightedCharge
    P hPpos.le hcharge cap ndRootCoreWidth n (cap n) m ((U.forwardIterate cap n).floor / 4)
    hm hroom.1 hroom.2 (Nat.cast_nonneg C) hquadratic (by norm_num)
    hsquare (3 ^ m) (by positivity) (unitReferenceDensity_finite_upper m)
    X hX hi (hgood n (by dsimp [J] at hn; omega) X hX hi)

end
end Erdos1135.ND.PositiveDensity
