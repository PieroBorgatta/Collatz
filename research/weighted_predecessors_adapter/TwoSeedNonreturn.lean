/-
SPDX-License-Identifier: Apache-2.0
Derived in part from GeneralTargetResidueCoverage.lean.
Copyright 2026 Lech Mazur; see LICENSE and UPSTREAM_NOTICE.
Modified 2026-09-24 for Piero Borgatta's predecessor development:
a bounded pair of congruent candidates contains a nonreturning seed.
Changes and proofs produced with AI assistance.
-/

import Erdos1135.ND.PositiveDensity.GeneralTargetResidueCoverage

/-!
# A bounded pair of candidates contains a non-returning predecessor

A map is injective on its periodic points. Two distinct preimages of the
same point therefore cannot both be periodic. Applying this observation to
two consecutive representatives in the explicit ternary-residue family
removes the unknown cycle-height bound from the existential seed argument.

The finite pair and its common upper bound are explicit; the proof does not
decide which member has no positive return.
-/

namespace Erdos1135.ND.PositiveDensity

namespace TwoSeedNonreturn

/-- Distinct points with the same image cannot both have positive returns. -/
theorem noReturn_or_noReturn_of_same_image
    {α : Type*} (f : α → α) {x y : α}
    (hne : x ≠ y) (himage : f x = f y) :
    (∀ k : ℕ, 0 < k → (f^[k]) x ≠ x) ∨
      (∀ k : ℕ, 0 < k → (f^[k]) y ≠ y) := by
  classical
  by_cases hx : ∀ k : ℕ, 0 < k → (f^[k]) x ≠ x
  · exact Or.inl hx
  · push_neg at hx
    obtain ⟨p, hp, hpx⟩ := hx
    right
    intro q hq hqy
    have hxp : Function.IsPeriodicPt f p x := hpx
    have hyp : Function.IsPeriodicPt f q y := hqy
    exact hne (hxp.eq_of_apply_eq hyp hp hq himage)

theorem generalTargetRoot_strictMono (r : ℕ) : StrictMono (ndGeneralTargetRoot r) := by
  intro k l hkl
  have hp : 4 ^ k < 4 ^ l := Nat.pow_lt_pow_right (by norm_num) hkl
  have hm := Nat.mul_lt_mul_of_pos_right hp (by omega : 0 < 3 * r + 1)
  have hk := generalTargetRoot_cleared r k
  have hl := generalTargetRoot_cleared r l
  omega

/-- The second candidate is bounded independently of the residue index p. -/
theorem twoCandidate_bounds_and_noReturn
    (r q X : ℕ) (p : Fin (3 ^ q)) :
    let k := (p : ℕ) + (X + 1) * 3 ^ q;
    X < ndGeneralTargetRoot r k ∧
      ndGeneralTargetRoot r k < ndGeneralTargetRoot r (k + 3 ^ q) ∧
      ndGeneralTargetRoot r (k + 3 ^ q) <
        ndGeneralTargetRoot r ((X + 3) * 3 ^ q) ∧
      ((∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) (ndGeneralTargetRoot r k) ≠
          ndGeneralTargetRoot r k) ∨
       (∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) (ndGeneralTargetRoot r (k + 3 ^ q)) ≠
          ndGeneralTargetRoot r (k + 3 ^ q))) := by
  let k := (p : ℕ) + (X + 1) * 3 ^ q
  have hq : 1 ≤ 3 ^ q := by positivity
  have hk : X < k := by
    have h := Nat.mul_le_mul_left (X + 1) hq
    dsimp only [k]
    omega
  have hkstep : k < k + 3 ^ q := by omega
  have hktop : k + 3 ^ q < (X + 3) * 3 ^ q := by
    dsimp only [k]
    nlinarith [p.isLt]
  have hlt := generalTargetRoot_strictMono r hkstep
  have htop := generalTargetRoot_strictMono r hktop
  have himage : Tao.syracuse (ndGeneralTargetRoot r k) =
      Tao.syracuse (ndGeneralTargetRoot r (k + 3 ^ q)) :=
    (generalTargetRoot_syracuse r k).trans
      (generalTargetRoot_syracuse r (k + 3 ^ q)).symm
  exact ⟨hk.trans_le (generalTargetRoot_ge_index r k), hlt, htop,
    noReturn_or_noReturn_of_same_image Tao.syracuse (Nat.ne_of_lt hlt) himage⟩

/-- One of two explicit congruent candidates works, with the second as an
upper bound and a larger bound independent of the chosen residue. -/
theorem exists_bounded_nonreturning_predecessor_of_start
    {a r e : ℕ} (hstart : 3 * r + 1 = 2 ^ e * a)
    (q X : ℕ) (y : Fin (3 ^ q)) :
    ∃ p : Fin (3 ^ q),
      let k := (p : ℕ) + (X + 1) * 3 ^ q;
      ∃ R : ℕ,
        (R = ndGeneralTargetRoot r k ∨ R = ndGeneralTargetRoot r (k + 3 ^ q)) ∧
        X < R ∧ R ≤ ndGeneralTargetRoot r (k + 3 ^ q) ∧
        R < ndGeneralTargetRoot r ((X + 3) * 3 ^ q) ∧
        Odd R ∧ Erdos1135.Reaches R a ∧ R % 3 ^ q = y ∧
        ∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) R ≠ R := by
  obtain ⟨p, hp⟩ := generalTargetRoot_residue_surjective r q y
  let k := (p : ℕ) + (X + 1) * 3 ^ q
  have hpair := twoCandidate_bounds_and_noReturn r q X p
  change X < ndGeneralTargetRoot r k ∧ _ at hpair
  obtain ⟨hlo, hlt, htop, hchoice⟩ := hpair
  have hq : 1 ≤ 3 ^ q := by positivity
  have hk : 0 < k := by
    have h := Nat.mul_le_mul_left (X + 1) hq
    dsimp only [k]
    omega
  have hk2 : 0 < k + 3 ^ q := by omega
  have hmod1 : ndGeneralTargetRoot r k % 3 ^ q = y := by
    have hper := generalTargetRoot_modEq_of_period r q p (X + 1)
    change ndGeneralTargetRoot r p % 3 ^ q = ndGeneralTargetRoot r k % 3 ^ q at hper
    exact hper.symm.trans (congrArg Fin.val hp)
  have hmod2 : ndGeneralTargetRoot r (k + 3 ^ q) % 3 ^ q = y := by
    have hper := generalTargetRoot_modEq_of_period r q k 1
    change ndGeneralTargetRoot r k % 3 ^ q =
      ndGeneralTargetRoot r (k + 1 * 3 ^ q) % 3 ^ q at hper
    simpa only [one_mul] using hper.symm.trans hmod1
  refine ⟨p, ?_⟩
  rcases hchoice with hfirst | hsecond
  · exact ⟨ndGeneralTargetRoot r k, Or.inl rfl, hlo, hlt.le, hlt.trans htop,
      generalTargetRoot_odd r k hk, generalTargetRoot_reaches hstart hk, hmod1, hfirst⟩
  · exact ⟨ndGeneralTargetRoot r (k + 3 ^ q), Or.inr rfl, hlo.trans hlt, le_rfl, htop,
      generalTargetRoot_odd r (k + 3 ^ q) hk2,
      generalTargetRoot_reaches hstart hk2, hmod2, hsecond⟩

/-- Explicit starting parameter; its computation requires only a mod 3. -/
def seedBase (a : ℕ) : ℕ :=
  if a % 3 = 1 then (4 * a) / 3 else (2 * a) / 3

theorem seedBase_start {a : ℕ} (hthree : ¬ 3 ∣ a) :
    ∃ e : ℕ, (e = 1 ∨ e = 2) ∧ 3 * seedBase a + 1 = 2 ^ e * a := by
  by_cases hmod : a % 3 = 1
  · refine ⟨2, Or.inr rfl, ?_⟩
    have hm : (4 * a) % 3 = 1 := by simp [Nat.mul_mod, hmod]
    simp only [seedBase, if_pos hmod]
    norm_num
    omega
  · have hne : a % 3 ≠ 0 := by simpa only [Nat.dvd_iff_mod_eq_zero] using hthree
    have hlt : a % 3 < 3 := Nat.mod_lt _ (by norm_num)
    have htwo : a % 3 = 2 := by omega
    refine ⟨1, Or.inl rfl, ?_⟩
    have hm : (2 * a) % 3 = 1 := by simp [Nat.mul_mod, htwo]
    simp only [seedBase, if_neg hmod]
    norm_num
    omega

theorem seedBase_le_two_mul (a : ℕ) : seedBase a ≤ 2 * a := by
  unfold seedBase
  split_ifs <;> omega

theorem generalTargetRoot_mono_base {r s : ℕ} (hrs : r ≤ s) (k : ℕ) :
    ndGeneralTargetRoot r k ≤ ndGeneralTargetRoot s k := by
  unfold ndGeneralTargetRoot
  exact Nat.add_le_add
    (Nat.mul_le_mul_right _ (by omega : 3 * r + 1 ≤ 3 * s + 1)) hrs

/-- Uniform over every residue; no unknown bound on a possible cycle occurs. -/
def seedBound (a q X : ℕ) : ℕ :=
  ndGeneralTargetRoot (2 * a) ((X + 3) * 3 ^ q)

theorem exists_nonreturning_predecessor_below_explicit_bound
    {a : ℕ} (_ha : 0 < a) (hthree : ¬ 3 ∣ a)
    (q X : ℕ) (y : Fin (3 ^ q)) :
    ∃ R : ℕ, X < R ∧ R < seedBound a q X ∧
      Odd R ∧ Erdos1135.Reaches R a ∧ R % 3 ^ q = y ∧
      ∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) R ≠ R := by
  obtain ⟨e, _, hstart⟩ := seedBase_start hthree
  obtain ⟨p, R, _hpair, hlo, _hsecond, htop, hodd, hreach, hresidue, hno⟩ :=
    exists_bounded_nonreturning_predecessor_of_start hstart q X y
  have hbound := generalTargetRoot_mono_base (seedBase_le_two_mul a) ((X + 3) * 3 ^ q)
  exact ⟨R, hlo, htop.trans_le hbound, hodd, hreach, hresidue, hno⟩

/-- Non-strict upper-bound API for the uniform density construction. -/
theorem exists_bounded_nonreturning_predecessor_in_residue
    {a : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a)
    (q X : ℕ) (y : Fin (3 ^ q)) :
    ∃ R : ℕ, X < R ∧ R ≤ seedBound a q X ∧
      Odd R ∧ Erdos1135.Reaches R a ∧ R % 3 ^ q = y ∧
      ∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) R ≠ R := by
  obtain ⟨R, hlo, htop, hodd, hreach, hresidue, hno⟩ :=
    exists_nonreturning_predecessor_below_explicit_bound ha hthree q X y
  exact ⟨R, hlo, htop.le, hodd, hreach, hresidue, hno⟩

end TwoSeedNonreturn

end Erdos1135.ND.PositiveDensity
