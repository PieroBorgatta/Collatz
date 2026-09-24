/-
SPDX-License-Identifier: Apache-2.0
Derived from GeneralTargetFrozenSeed.lean and GeneralTargetPositiveDensity.lean.
Copyright 2026 Lech Mazur; see LICENSE and UPSTREAM_NOTICE.
Modified 2026-09-24 for Piero Borgatta's predecessor development:
a pair of explicit seeds removes the unknown cycle-height bound and yields
uniform constants that do not depend on choosing the nonreturning candidate.
Changes and proofs produced with AI assistance.
-/

import TwoSeedNonreturn
import Erdos1135.ND.PositiveDensity.GeneralTargetPredecessorCount
import Erdos1135.ND.PositiveDensity.ExplicitNumericalSyracuseMixing

namespace Erdos1135.ND.PositiveDensity
noncomputable section
namespace TwoSeedDensity

/-- A uniform bound for either candidate, independent of the good residue. -/
def frozenSeedBound (a b N : ℕ) : ℕ :=
  TwoSeedNonreturn.seedBound a
    (ndRootCoreBackwardConductor b (explicitSeedFloor b N / 4) N) (16 ^ b)

theorem exists_bounded_full_core_mark
    {a b k : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a)
    (hb : 2 ^ 80 ≤ b) (hk : 1 ≤ k)
    (cap : ℕ → ℕ) (hcap : ∀ n, 16 + n / 100 ≤ cap n) (n : ℕ) :
    ∃ (r : ℕ) (hr : Odd r) (hl : 16 ^ b ≤ r),
      r ≤ TwoSeedNonreturn.seedBound a (ndRootCoreBackwardConductor b k n) (16 ^ b) ∧
      Erdos1135.Reaches r a ∧
      (∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) r ≠ r) ∧
      IsUnit (r : ZMod (3 ^ 1)) ∧
      (255 / 256 : ℝ) ≤
        (ndRootCoreSingletonState b r ((by norm_num : (200 : ℕ) ≤ 2 ^ 80).trans hb) hr hl).forwardCoreMarkedMass
          cap ndRootCoreWidth n k (fun _ => 1) := by
  have hb200 : 200 ≤ b := (by norm_num : (200 : ℕ) ≤ 2 ^ 80).trans hb
  obtain ⟨y, _, hy⟩ := exists_unit_rootCoreBackwardMark_ge_full_product
    (b := b) hk cap ndRootCoreWidth n
  let q := ndRootCoreBackwardConductor b k n
  let residue : Fin (3 ^ q) := ⟨y.val, ZMod.val_lt y⟩
  obtain ⟨r, hl, hbound, hr, htarget, hres, hnonreturn⟩ :=
    TwoSeedNonreturn.exists_bounded_nonreturning_predecessor_in_residue ha hthree q (16 ^ b) residue
  have heq : (r : ZMod (3 ^ q)) = y := by
    calc
      _ = ((r % 3 ^ q : ℕ) : ZMod (3 ^ q)) := by simp
      _ = ((y.val : ℕ) : ZMod (3 ^ q)) := congrArg (fun a : ℕ => (a : ZMod (3 ^ q))) hres
      _ = y := ZMod.natCast_zmod_val y
  have hg : ndRootCoreProbabilityProduct b cap ndRootCoreWidth n ≤
      ndRootCoreBackwardMark b cap ndRootCoreWidth k n (r : ZMod (3 ^ q)) := by rwa [heq]
  let U := ndRootCoreSingletonState b r hb200 hr hl.le
  have hp : (255 / 256 : ℝ) ≤ ndRootCoreProbabilityProduct b cap ndRootCoreWidth n :=
    U.coreProbabilityProduct_ge_255_div_256 hb cap hcap n
  have hu : IsUnit (r : ZMod (3 ^ 1)) := by
    by_contra hn
    have hz := rootCoreBackwardMark_natCast_eq_zero_of_not_unit b cap ndRootCoreWidth hk n r hn
    rw [hz] at hg
    nlinarith
  refine ⟨r, hr, hl.le, hbound, htarget, hnonreturn, hu, ?_⟩
  rw [rootCoreSingletonState_markedMass_eq_backwardMark _ _ _ _ _ _ _ _ _ hk]
  nlinarith

theorem exists_bounded_core_sequence_seed
    {a b : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a) (hb : 2 ^ 80 ≤ b) (N : ℕ) :
    ∃ (r : ℕ) (hr : Odd r) (hl : 16 ^ b ≤ r),
      r ≤ frozenSeedBound a b N ∧
      Erdos1135.Reaches r a ∧
      (∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) r ≠ r) ∧
      IsUnit (r : ZMod (3 ^ 1)) ∧
      (255 / 256 : ℝ) ≤
        (ndRootCoreSingletonState b r ((by norm_num : (200 : ℕ) ≤ 2 ^ 80).trans hb) hr hl).coreMarkedSequence
          (fun n => 16 + n / 100) ndRootCoreWidth N := by
  let k := explicitSeedFloor b N / 4
  have hfloor := explicitSeedFloor_bounds b N
  have hk : 1 ≤ k := by dsimp [k]; omega
  obtain ⟨r, hr, hl, hbound, ht, hnonreturn, hunit, hmark⟩ :=
    exists_bounded_full_core_mark ha hthree hb hk
      (fun n => 16 + n / 100) (fun _ => le_rfl) N
  refine ⟨r, hr, hl, hbound, ht, hnonreturn, hunit, ?_⟩
  unfold NDGeom2ShiftedWideSymmetricRootSideUniformFloorState.coreMarkedSequence
  rw [NDGeom2ShiftedWideSymmetricRootSideUniformFloorState.explicit_forward_floor]
  exact hmark

theorem exists_bounded_uniform_twoThirds_seed
    {a b : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a) (hb : 2 ^ 80 ≤ b) (C : ℕ)
    (hmix : Tao.syracFineScaleMixingAt 6 (C : ℝ))
    {N : ℕ} (hN : explicitLogarithmicSeedGeneration b C ≤ N) :
    ∃ (r : ℕ) (hr : Odd r) (hl : 16 ^ b ≤ r),
      r ≤ frozenSeedBound a b N ∧
      Erdos1135.Reaches r a ∧
      (∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) r ≠ r) ∧
      IsUnit (r : ZMod (3 ^ 1)) ∧
      ∀ n ≥ explicitLogarithmicGoodMarkedStart b C N,
        let U := ndRootCoreSingletonState b r
          ((by norm_num : (200 : ℕ) ≤ 2 ^ 80).trans hb) hr hl;
        let V := U.forwardIterate (fun j => 16 + j / 100) n;
        ∀ (X : ℝ) (hX : 0 < X)
          (hi : ∀ i : V.state.Label,
            ndGeom2ShiftedWideSymmetricPhysicalIntervalMin V.floor (V.state.root i) < X ∧
            X ≤ ndGeom2ShiftedWideSymmetricPhysicalIntervalMax V.floor (V.state.root i)),
          (2 / 3 : ℝ) ≤ U.forwardCoreTerminalGoodDepthShiftUnitMass
            (fun j => 16 + j / 100) ndRootCoreWidth n (16 + n / 100) (V.floor / 4) X hX hi := by
  obtain ⟨r, hr, hl, hbound, ht, hnonreturn, hunit, hmark⟩ :=
    exists_bounded_core_sequence_seed ha hthree hb N
  refine ⟨r, hr, hl, hbound, ht, hnonreturn, hunit, ?_⟩
  intro n hn U V X hX hi
  let cap := fun j : ℕ => 16 + j / 100
  have hcap : ∀ j, cap j ≤ 17 * (j + 1) := by
    intro j
    have hj := Nat.div_le_self j 100
    dsimp [cap]
    omega
  have he : U.rootSpan 0 := by intro i j; change r ≤ 2 ^ 0 * r; simp
  have hD : U.denominator = 1 := rootCoreSingletonState_denominator_eq_one _ _ _ _ _
  have hseed : (255 / 256 : ℝ) * U.denominator ≤
      U.coreMarkedSequence cap ndRootCoreWidth N := by
    simpa only [hD, mul_one] using hmark
  have hNn : N ≤ n := by unfold explicitLogarithmicGoodMarkedStart at hn; omega
  have hnBudget : explicitLogarithmicTerminalStart U.floor C 0 ≤ n := by
    change explicitLogarithmicTerminalStart b C 0 ≤ n
    unfold explicitLogarithmicGoodMarkedStart at hn
    omega
  have h := NDGeom2ShiftedWideSymmetricRootSideUniformFloorState.explicit_good_marked_margin_logarithmic_full
    C hmix U ((by norm_num : (32 : ℕ) ^ 5 ≤ 2 ^ 80).trans hb)
    cap 0 he hcap (fun _ => le_rfl) hN hNn hnBudget hseed X hX hi
  rw [hD, mul_one] at h
  exact (by norm_num : (2 / 3 : ℝ) ≤ 175 / 256).trans h


/-- The common floor is fixed before choosing any good residue or seed. -/
def fixedFloor : ℕ := 2 ^ 80

def seedGeneration (C : ℕ) : ℕ :=
  explicitLogarithmicSeedGeneration fixedFloor C

/-- Explicit in the target and the supplied mixing constant; independent of
which good residue and which nonreturning candidate the existence proof picks. -/
def rootBound (a C : ℕ) : ℕ :=
  frozenSeedBound a fixedFloor (seedGeneration C)

def conductor (a C : ℕ) : ℕ := 132 * rootBound a C * C + 1

def markedStart (C : ℕ) : ℕ :=
  explicitLogarithmicGoodMarkedStart fixedFloor C (seedGeneration C)

def countStart (a C : ℕ) : ℕ :=
  markedStart C + 2 * conductor a C + 20 * 10 ^ 9

def intervalHeight (a C : ℕ) : ℕ :=
  ndExplicitRootIntervalHeight fixedFloor 17 (rootBound a C) (countStart a C)

def cutoff (a C : ℕ) : ℕ := 32 * (intervalHeight a C + 1)

/-- The original nonreturning census coefficient, with the unknown seed
replaced by its explicit uniform upper bound. -/
def coefficient (a C : ℕ) : ℝ :=
  3 / (256 * (rootBound a C : ℝ) * (3 : ℝ) ^ conductor a C)

/-- A uniform quantitative predecessor estimate, conditional only on the
supplied fine-scale mixing theorem. No nonreturning seed is supplied as an
assumption, and the constants contain no existentially selected seed. -/
theorem predecessor_count_of_mixing
    {a : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a) (C : ℕ)
    (hmix : Tao.syracFineScaleMixingAt 6 (C : ℝ)) :
    0 < coefficient a C ∧
      ∀ Y : ℕ, cutoff a C ≤ Y →
        coefficient a C * (Y : ℝ) ≤
          (Terras.natCount (ordinaryPredecessorSet a) Y : ℝ) := by
  let b := fixedFloor
  let N := seedGeneration C
  let T := rootBound a C
  obtain ⟨r, hr, hl, hbound, ht, hnonreturn, _hunit, hgood⟩ :=
    exists_bounded_uniform_twoThirds_seed ha hthree (b := b) le_rfl C hmix
      (N := N) le_rfl
  have hTnat : r ≤ T := hbound
  have hTpos : (0 : ℝ) < T := by
    exact_mod_cast hr.pos.trans_le hTnat
  have hrT : (r : ℝ) ≤ T := by exact_mod_cast hTnat
  have hb200 : 200 ≤ b := by dsimp [b, fixedFloor]; norm_num
  let U := ndRootCoreSingletonState b r hb200 hr hl
  let cap := fun j : ℕ => 16 + j / 100
  have he : U.rootSpan 0 := by intro i j; change r ≤ 2 ^ 0 * r; simp
  have hcap : ∀ j, cap j ≤ 17 * (j + 1) := by
    intro j
    have hj := Nat.div_le_self j 100
    dsimp [cap]
    omega
  have hreach : ∀ i, Erdos1135.Reaches (U.state.root i) a := fun _ => ht
  have hseed : ∀ i k, 0 < k → (Tao.syracuse^[k]) (U.state.root i) ≠ U.state.root i :=
    fun _ => hnonreturn
  have hP : U.parentSourcePotential = (r : ℝ) := by
    change ndGeom2PredictableRootSideParentSourcePotential (Finset.univ : Finset Unit)
      (fun _ => (1 : ℝ)) (fun _ => r) = _
    simp [ndGeom2PredictableRootSideParentSourcePotential]
  have hPpos : 0 < U.parentSourcePotential := by rw [hP]; exact_mod_cast hr.pos
  have hPT : U.parentSourcePotential ≤ (T : ℝ) := by rw [hP]; exact hrT
  let m := conductor a C
  have hm : 1 ≤ m := by dsimp [m, conductor]; omega
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hmdef : (m : ℝ) = 132 * (T : ℝ) * (C : ℝ) + 1 := by
    dsimp [m, conductor, T]
    push_cast
    ring
  have hRC := mul_le_mul_of_nonneg_right hrT (Nat.cast_nonneg (α := ℝ) C)
  have hsquare : 88 * U.parentSourcePotential * (C : ℝ) ≤
      (2 / 3 : ℝ) * (m : ℝ) ^ 2 := by
    rw [hP]
    nlinarith only [hRC, hmdef, hmR, sq_nonneg ((m : ℝ) - 1)]
  have hquadratic : ndExplicitQuadraticMixingAt (C : ℝ) m :=
    explicitMixing_quadratic (Nat.cast_nonneg C) hmix hm
  let J := countStart a C
  let H := intervalHeight a C
  let eta : ℝ := 3 / (8 * (3 : ℝ) ^ m)
  have heta : 0 < eta := by dsimp [eta]; positivity
  have heta_eq : eta = 9 * (2 / 3 : ℝ) / (16 * ((3 ^ m : ℕ) : ℝ)) := by
    dsimp [eta]
    push_cast
    field_simp
    ring
  have hmass : ∀ n, J ≤ n →
      let V := U.forwardIterate cap n;
      ∀ (X : ℝ) (hX : 0 < X)
        (hi : ∀ i : V.state.Label,
          ndGeom2ShiftedWideSymmetricPhysicalIntervalMin V.floor (V.state.root i) < X ∧
          X ≤ ndGeom2ShiftedWideSymmetricPhysicalIntervalMax V.floor (V.state.root i)),
        eta ≤ U.fullGoodCoreTerminalMass cap ndRootCoreWidth n
          (V.fullTerminalShift X hX hi) 1 := by
    intro n hn V X hX hi
    have hnm : 2 * m ≤ n := by dsimp [J, countStart, m] at hn ⊢; omega
    have hroom := U.explicitConductor_quarter_room cap m n hnm
    rw [heta_eq]
    exact U.fullGoodCoreTerminalMass_ge_of_square_budget_and_height_of_nonreturningSeed
      cap ndRootCoreWidth n (cap n) m ((U.forwardIterate cap n).floor / 4)
      hm hroom.1 hroom.2 hseed (Nat.cast_nonneg C) hquadratic (by norm_num)
      hsquare (3 ^ m) (by positivity) (unitReferenceDensity_finite_upper m)
      X hX hi (hgood n (by
        change markedStart C ≤ n
        dsimp [J, countStart] at hn
        omega) X hX hi)
  have hcount := U.generalTarget_publicCount_from_mass a hreach hseed cap he hcap
    hPpos J H (by dsimp [J, countStart]; omega)
    (fun i => U.iterate_physicalIntervalMax_le_explicit cap 17 T hcap
      (fun _ => hTnat) J i) hmass
  have hcoef : coefficient a C = eta / (32 * (T : ℝ)) := by
    change 3 / (256 * (T : ℝ) * (3 : ℝ) ^ m) = eta / (32 * (T : ℝ))
    dsimp [eta]
    field_simp
    ring
  have hcoefpos : 0 < coefficient a C := by rw [hcoef]; positivity
  refine ⟨hcoefpos, ?_⟩
  intro Y hY
  have hcoefle : coefficient a C ≤ eta / (32 * U.parentSourcePotential) := by
    rw [hcoef]
    exact div_le_div_of_nonneg_left heta.le (by positivity)
      (mul_le_mul_of_nonneg_left hPT (by norm_num : (0 : ℝ) ≤ 32))
  exact (mul_le_mul_of_nonneg_right hcoefle (Nat.cast_nonneg Y)).trans
    (hcount Y hY)

/-- Constants specialized to the external library's fixed numerical mixing
coefficient. They depend only on the public target a. -/
def publicCoefficient (a : ℕ) : ℝ := coefficient a explicitSyracuseMixingCoefficient

def publicCutoff (a : ℕ) : ℕ := cutoff a explicitSyracuseMixingCoefficient

/-- The explicit numerical public theorem, obtained through a bounded pair of
candidate seeds. The imported analytic library remains part of its proof. -/
theorem generalTarget_predecessors_explicit_lower_bound
    {a : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a) :
    0 < publicCoefficient a ∧
      ∀ Y : ℕ, publicCutoff a ≤ Y →
        publicCoefficient a * (Y : ℝ) ≤
          (Terras.natCount (ordinaryPredecessorSet a) Y : ℝ) :=
  predecessor_count_of_mixing ha hthree explicitSyracuseMixingCoefficient
    explicitSyracuseMixing_six

end TwoSeedDensity
end
end Erdos1135.ND.PositiveDensity
