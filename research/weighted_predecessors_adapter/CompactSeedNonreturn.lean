/-
SPDX-License-Identifier: Apache-2.0
Derived in part from GeneralTargetResidueCoverage.lean.
Copyright 2026 Lech Mazur; see LICENSE and UPSTREAM_NOTICE.
Modified 2026-09-24 for Piero Borgatta's predecessor development:
use the first congruent exponent above twice the seed floor parameter.
Changes and proofs produced with AI assistance.
-/

import TwoSeedNonreturn

/-!
# A compact uniform bound for two nonreturning-seed candidates

The residue family grows at least as fast as `4^k` when its starting root
is positive. To exceed `16^b`, it therefore suffices to choose an exponent
strictly above `2*b`. The first exponent in a supplied residue class above
that threshold lies at most one residue period later. Its successor lies
at most two periods later, giving an additive exponent bound.

The same-image argument still chooses the nonreturning member existentially;
the uniform bound does not depend on this choice or the supplied residue.
-/

namespace Erdos1135.ND.PositiveDensity
namespace CompactSeedNonreturn

/-- The number of full periods needed to put residue p strictly above B. -/
def residueShift (B Q p : ℕ) : ℕ :=
  B / Q + if p ≤ B % Q then 1 else 0

def firstExponent (B Q p : ℕ) : ℕ :=
  p + residueShift B Q p * Q

theorem firstExponent_bounds (B Q p : ℕ) (hQ : 0 < Q) (hp : p < Q) :
    B < firstExponent B Q p ∧ firstExponent B Q p ≤ B + Q := by
  have hmod := Nat.mod_lt B hQ
  have hdiv := Nat.mod_add_div B Q
  unfold firstExponent residueShift
  split_ifs with h
  · constructor <;> nlinarith
  · constructor <;> nlinarith [Nat.zero_le (B % Q)]

theorem seedBase_pos {a : ℕ} (_ha : 0 < a) (hthree : ¬ 3 ∣ a) :
    0 < TwoSeedNonreturn.seedBase a := by
  obtain ⟨e, he, hstart⟩ := TwoSeedNonreturn.seedBase_start hthree
  rcases he with rfl | rfl <;> norm_num at hstart <;> omega

theorem generalTargetRoot_ge_pow_four {r : ℕ} (hr : 1 ≤ r) (k : ℕ) :
    4 ^ k ≤ ndGeneralTargetRoot r k := by
  have hpow : 0 < (4 : ℕ) ^ k := by positivity
  have hmul := Nat.mul_le_mul_left (4 ^ k) (by omega : 4 ≤ 3 * r + 1)
  have hclear := generalTargetRoot_cleared r k
  nlinarith only [hpow, hmul, hclear]

/-- Both candidates are bounded without using the good residue or its index. -/
def seedBound (a q b : ℕ) : ℕ :=
  ndGeneralTargetRoot (2 * a) (2 * b + 2 * 3 ^ q)

theorem seedBound_pos {a : ℕ} (ha : 0 < a) (q b : ℕ) :
    0 < seedBound a q b := by
  unfold seedBound ndGeneralTargetRoot
  positivity

private theorem two_mul_lt_pow_sixteen (b : ℕ) : 2 * b < 16 ^ b := by
  induction b with
  | zero => norm_num
  | succ b ih =>
    have hpow : 0 < (16 : ℕ) ^ b := by positivity
    rw [pow_succ]
    nlinarith

theorem seedBound_lt_old {a : ℕ} (_ha : 0 < a) (q b : ℕ) :
    seedBound a q b < TwoSeedNonreturn.seedBound a q (16 ^ b) := by
  unfold seedBound TwoSeedNonreturn.seedBound
  apply TwoSeedNonreturn.generalTargetRoot_strictMono (2 * a)
  have hpow : 1 ≤ 3 ^ q := by
    have hpos : 0 < (3 : ℕ) ^ q := by positivity
    omega
  have hlinear := two_mul_lt_pow_sixteen b
  have hscaled := Nat.mul_le_mul_left (16 ^ b + 1) hpow
  nlinarith only [hlinear, hscaled]

/-- A predecessor above `16^b` in the supplied residue class, with an additive
exponent bound independent of which member of the pair is nonreturning. -/
theorem exists_bounded_nonreturning_predecessor_in_residue
    {a : ℕ} (ha : 0 < a) (hthree : ¬ 3 ∣ a)
    (q b : ℕ) (y : Fin (3 ^ q)) :
    ∃ R : ℕ, 16 ^ b < R ∧ R ≤ seedBound a q b ∧
      Odd R ∧ Erdos1135.Reaches R a ∧ R % 3 ^ q = y ∧
      ∀ t : ℕ, 0 < t → (Tao.syracuse^[t]) R ≠ R := by
  let r := TwoSeedNonreturn.seedBase a
  obtain ⟨e, _he, hstart⟩ := TwoSeedNonreturn.seedBase_start hthree
  have hr : 1 ≤ r := by
    have hpos := seedBase_pos ha hthree
    dsimp only [r]
    omega
  obtain ⟨p, hp⟩ := generalTargetRoot_residue_surjective r q y
  let l := residueShift (2 * b) (3 ^ q) p
  let k := firstExponent (2 * b) (3 ^ q) p
  have hbounds : 2 * b < k ∧ k ≤ 2 * b + 3 ^ q :=
    firstExponent_bounds (2 * b) (3 ^ q) p (by positivity) p.isLt
  have hk : 0 < k := by omega
  have hk2 : 0 < k + 3 ^ q := by omega
  have hkupper : k + 3 ^ q ≤ 2 * b + 2 * 3 ^ q := by omega
  have hpower : 16 ^ b < 4 ^ k := by
    calc
      16 ^ b = (4 : ℕ) ^ (2 * b) := by rw [pow_mul]; norm_num
      _ < 4 ^ k := Nat.pow_lt_pow_right (by norm_num) hbounds.1
  have hlo : 16 ^ b < ndGeneralTargetRoot r k :=
    hpower.trans_le (generalTargetRoot_ge_pow_four hr k)
  have hkstep : k < k + 3 ^ q := by
    have hpos : 0 < (3 : ℕ) ^ q := by positivity
    omega
  have hlt := TwoSeedNonreturn.generalTargetRoot_strictMono r hkstep
  have hupper : ndGeneralTargetRoot r (k + 3 ^ q) ≤ seedBound a q b := by
    calc
      _ ≤ ndGeneralTargetRoot r (2 * b + 2 * 3 ^ q) :=
        (TwoSeedNonreturn.generalTargetRoot_strictMono r).monotone hkupper
      _ ≤ ndGeneralTargetRoot (2 * a) (2 * b + 2 * 3 ^ q) :=
        TwoSeedNonreturn.generalTargetRoot_mono_base
          (TwoSeedNonreturn.seedBase_le_two_mul a) _
      _ = seedBound a q b := rfl
  have himage : Tao.syracuse (ndGeneralTargetRoot r k) =
      Tao.syracuse (ndGeneralTargetRoot r (k + 3 ^ q)) :=
    (generalTargetRoot_syracuse r k).trans
      (generalTargetRoot_syracuse r (k + 3 ^ q)).symm
  have hmod1 : ndGeneralTargetRoot r k % 3 ^ q = y := by
    have hper := generalTargetRoot_modEq_of_period r q p l
    change ndGeneralTargetRoot r p % 3 ^ q = ndGeneralTargetRoot r k % 3 ^ q at hper
    exact hper.symm.trans (congrArg Fin.val hp)
  have hmod2 : ndGeneralTargetRoot r (k + 3 ^ q) % 3 ^ q = y := by
    have hper := generalTargetRoot_modEq_of_period r q k 1
    change ndGeneralTargetRoot r k % 3 ^ q =
      ndGeneralTargetRoot r (k + 1 * 3 ^ q) % 3 ^ q at hper
    simpa only [one_mul] using hper.symm.trans hmod1
  rcases TwoSeedNonreturn.noReturn_or_noReturn_of_same_image Tao.syracuse
      (Nat.ne_of_lt hlt) himage with hfirst | hsecond
  · exact ⟨ndGeneralTargetRoot r k, hlo, hlt.le.trans hupper,
      generalTargetRoot_odd r k hk, generalTargetRoot_reaches hstart hk,
      hmod1, hfirst⟩
  · exact ⟨ndGeneralTargetRoot r (k + 3 ^ q), hlo.trans hlt, hupper,
      generalTargetRoot_odd r (k + 3 ^ q) hk2,
      generalTargetRoot_reaches hstart hk2, hmod2, hsecond⟩

end CompactSeedNonreturn
end Erdos1135.ND.PositiveDensity
