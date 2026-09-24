/-
Universal weighted occupation for the external SyracusePath API.
This module does not assume termination or exclude cycles.
-/
import Erdos1135.ND.PositiveDensity.Geom2ShiftedWideSymmetricRootUniformGroupedCapacity
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

namespace Erdos1135.ND.PositiveDensity.WeightedPathOccupation

open scoped BigOperators

noncomputable section

/-- The exponent removed in the first `k` accelerated steps. -/
def exponentSum (x : ℕ) : ℕ → ℕ
  | 0 => 0
  | k + 1 => exponentSum x k + Tao.syracuseExponent (Tao.syracuse^[k] x)

/-- The multiplicative part of the affine `k`-step Syracuse iterate. -/
def weight (x k : ℕ) : ℝ := 3 ^ k / 2 ^ exponentSum x k

/-- The remaining reciprocal potential along the actual orbit. -/
def potential (x k : ℕ) : ℝ := weight x k / (Tao.syracuse^[k] x : ℝ)

/-- The exact potential lost at time `k`. -/
def loss (x k : ℕ) : ℝ :=
  weight x k / ((Tao.syracuse^[k] x : ℝ) * (3 * (Tao.syracuse^[k] x : ℝ) + 1))

theorem orbit_pos {x : ℕ} (hx : 0 < x) (k : ℕ) : 0 < Tao.syracuse^[k] x := by
  cases k with
  | zero => simpa using hx
  | succ k =>
      simpa only [Function.iterate_succ_apply'] using Tao.syracuse_pos (Tao.syracuse^[k] x)

theorem weight_pos (x k : ℕ) : 0 < weight x k := by
  unfold weight
  positivity

theorem weight_zero (x : ℕ) : weight x 0 = 1 := by
  simp [weight, exponentSum]

theorem weight_succ (x k : ℕ) :
    weight x (k + 1) =
      3 * weight x k / (2 : ℝ) ^ Tao.syracuseExponent (Tao.syracuse^[k] x) := by
  unfold weight
  rw [exponentSum, pow_add, pow_succ]
  ring

theorem orbit_step (x k : ℕ) :
    (2 : ℝ) ^ Tao.syracuseExponent (Tao.syracuse^[k] x) * (Tao.syracuse^[k + 1] x : ℝ) =
      3 * (Tao.syracuse^[k] x : ℝ) + 1 := by
  have h := Tao.two_pow_syracuseExponent_mul_syracuse (Tao.syracuse^[k] x)
  have hnat : 2 ^ Tao.syracuseExponent (Tao.syracuse^[k] x) * Tao.syracuse^[k + 1] x =
      3 * Tao.syracuse^[k] x + 1 := by
    simpa only [Function.iterate_succ_apply'] using h
  exact_mod_cast hnat

/-- The factor `2^a` cancels exactly between weight and orbit state. -/
theorem potential_succ {x : ℕ} (hx : 0 < x) (k : ℕ) :
    potential x (k + 1) = 3 * weight x k / (3 * (Tao.syracuse^[k] x : ℝ) + 1) := by
  have hn : (0 : ℝ) < (Tao.syracuse^[k] x : ℝ) := by exact_mod_cast orbit_pos hx k
  have hm : (0 : ℝ) < (Tao.syracuse^[k + 1] x : ℝ) := by
    exact_mod_cast orbit_pos hx (k + 1)
  have hd : (0 : ℝ) < 2 ^ Tao.syracuseExponent (Tao.syracuse^[k] x) := by positivity
  have hstep := orbit_step x k
  unfold potential
  rw [weight_succ, ← hstep]
  field_simp

/-- Exact dissipation, including time zero and visits to the fixed point `1`. -/
theorem potential_sub_succ {x : ℕ} (hx : 0 < x) (k : ℕ) :
    potential x k - potential x (k + 1) = loss x k := by
  have hn : (0 : ℝ) < (Tao.syracuse^[k] x : ℝ) := by exact_mod_cast orbit_pos hx k
  have ha : (0 : ℝ) < 3 * (Tao.syracuse^[k] x : ℝ) + 1 := by positivity
  rw [potential_succ hx]
  unfold potential loss
  field_simp
  ring

theorem potential_pos {x : ℕ} (hx : 0 < x) (k : ℕ) :
    0 < potential x k := by
  have hn : (0 : ℝ) < (Tao.syracuse^[k] x : ℝ) := by exact_mod_cast orbit_pos hx k
  exact div_pos (weight_pos x k) hn

theorem loss_pos {x : ℕ} (hx : 0 < x) (k : ℕ) : 0 < loss x k := by
  have hn : (0 : ℝ) < (Tao.syracuse^[k] x : ℝ) := by exact_mod_cast orbit_pos hx k
  unfold loss
  exact div_pos (weight_pos x k) (by positivity)

/-- Telescoping of the exact loss along any finite initial orbit segment. -/
theorem sum_loss_range {x : ℕ} (hx : 0 < x) (N : ℕ) :
    ∑ k ∈ Finset.range N, loss x k = 1 / (x : ℝ) - potential x N := by
  induction N with
  | zero => simp [potential, weight_zero]
  | succ N ih =>
      rw [Finset.sum_range_succ, ih, ← potential_sub_succ hx N]
      ring

theorem sum_loss_range_le {x : ℕ} (hx : 0 < x) (N : ℕ) :
    ∑ k ∈ Finset.range N, loss x k ≤ 1 / (x : ℝ) := by
  rw [sum_loss_range hx]
  exact sub_le_self _ (le_of_lt (potential_pos hx N))

/-- Every finite set of distinct times consumes at most the initial potential. -/
theorem sum_loss_finset_le {x : ℕ} (hx : 0 < x) (H : Finset ℕ) :
    ∑ k ∈ H, loss x k ≤ 1 / (x : ℝ) := by
  calc
    ∑ k ∈ H, loss x k ≤ ∑ k ∈ Finset.range (H.sup id + 1), loss x k :=
      Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_range_sup_succ H)
        (fun k _ _ => le_of_lt (loss_pos hx k))
    _ ≤ 1 / (x : ℝ) := sum_loss_range_le hx _

/-- Universal weighted visit bound. No nonperiodicity or termination assumption
is needed, and `H` may contain time zero. -/
theorem sum_weight_visits_le {x R : ℕ} (hx : 0 < x) (H : Finset ℕ)
    (hvisits : ∀ k ∈ H, Tao.syracuse^[k] x = R) :
    ∑ k ∈ H, weight x k ≤ (R : ℝ) * (3 * (R : ℝ) + 1) / (x : ℝ) := by
  have hfactor : (0 : ℝ) ≤ (R : ℝ) * (3 * (R : ℝ) + 1) := by positivity
  have hsum : (∑ k ∈ H, weight x k) =
      ((R : ℝ) * (3 * (R : ℝ) + 1)) * ∑ k ∈ H, loss x k := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro k hk
    have hn : (0 : ℝ) < (Tao.syracuse^[k] x : ℝ) := by exact_mod_cast orbit_pos hx k
    have hr : (0 : ℝ) < (R : ℝ) := by simpa [hvisits k hk] using hn
    unfold loss
    rw [hvisits k hk]
    field_simp
  rw [hsum]
  simpa [div_eq_mul_inv, mul_assoc] using
    mul_le_mul_of_nonneg_left (sum_loss_finset_le hx H) hfactor

/-- Splitting the sum at the first accelerated step. -/
theorem exponentSum_succ_first (x k : ℕ) :
    exponentSum x (k + 1) = Tao.syracuseExponent x + exponentSum (Tao.syracuse x) k := by
  induction k with
  | zero => simp [exponentSum]
  | succ k ih =>
      rw [exponentSum, ih, exponentSum]
      simp [Function.iterate_succ_apply, Nat.add_assoc]

/-- The external positive valuation word records exactly this exponent sum. -/
theorem valuation_tupleWeight_eq (n x : ℕ) (hodd : Odd x) :
    Tao.taoTupleWeight (Tao.syracuseValuationPNatList n x hodd) =
      exponentSum x n := by
  induction n generalizing x with
  | zero => rfl
  | succ n ih =>
      change Tao.syracuseExponent x +
          Tao.taoTupleWeight (Tao.syracuseValuationPNatList n (Tao.syracuse x)
            (Tao.syracuse_odd x)) = exponentSum x (n + 1)
      rw [ih, exponentSum_succ_first]

/-- The exact external atom of a path is its orbit occupation weight. -/
theorem path_atom_eq_weight {x R : ℕ} (p : NDGeom2RootSideSyracusePath x R) :
    ndRootUniformWordAtom p.word = weight x p.depth := by
  unfold ndRootUniformWordAtom weight
  rw [p.word_length, ← p.valuation_eq, valuation_tupleWeight_eq]

/-- Distinct words at one source have distinct depths, including cyclic paths. -/
theorem sum_path_wordWeight_le {ι : Type*} {x R : ℕ} (hx : 0 < x)
    (F : Finset ι) (p : ι → NDGeom2RootSideSyracusePath x R)
    (hword : Set.InjOn (fun i => (p i).word) F) :
    (∑ i ∈ F, ndRootUniformWordAtom (p i).word) ≤
      (R : ℝ) * (3 * (R : ℝ) + 1) / (x : ℝ) := by
  classical
  have hinj : Set.InjOn (fun i => (p i).depth) F := by
    intro i hi j hj hd
    apply hword hi hj
    exact NDGeom2RootSideSyracusePath.word_eq_of_source_depth_eq (p i) (p j) rfl hd
  have hsum : (∑ i ∈ F, ndRootUniformWordAtom (p i).word) =
      ∑ k ∈ F.image (fun i => (p i).depth), weight x k := by
    rw [Finset.sum_image hinj]
    apply Finset.sum_congr rfl
    intro i _
    exact path_atom_eq_weight (p i)
  rw [hsum]
  apply sum_weight_visits_le hx
  intro k hk
  rcases Finset.mem_image.mp hk with ⟨i, hi, rfl⟩
  exact (p i).terminal_eq

/-- A fiber can contain many paths; injectivity of source and depth is enough. -/
theorem path_fiber_bound {ι : Type*} (F : Finset ι) (source : ι → ℕ)
    {R : ℕ} (p : ∀ i, NDGeom2RootSideSyracusePath (source i) R)
    (hinj : Set.InjOn (fun i => (source i, (p i).depth)) F)
    (x : ℕ) (hx : 0 < x) :
    (∑ i ∈ F with source i = x, ndRootUniformWordAtom (p i).word) ≤
      (R : ℝ) * (3 * (R : ℝ) + 1) / (x : ℝ) := by
  classical
  let G := F.filter (fun i => source i = x)
  have hdepth : Set.InjOn (fun i => (p i).depth) G := by
    intro i hi j hj hd
    rcases Finset.mem_filter.mp hi with ⟨hi, hsi⟩
    rcases Finset.mem_filter.mp hj with ⟨hj, hsj⟩
    apply hinj hi hj
    exact Prod.ext (hsi.trans hsj.symm) hd
  have hsum : (∑ i ∈ G, ndRootUniformWordAtom (p i).word) =
      ∑ k ∈ G.image (fun i => (p i).depth), weight x k := by
    rw [Finset.sum_image hdepth]
    apply Finset.sum_congr rfl
    intro i hi
    rw [path_atom_eq_weight, (Finset.mem_filter.mp hi).2]
  change (∑ i ∈ G, ndRootUniformWordAtom (p i).word) ≤ _
  rw [hsum]
  apply sum_weight_visits_le hx
  intro k hk
  rcases Finset.mem_image.mp hk with ⟨i, hi, rfl⟩
  simpa only [(Finset.mem_filter.mp hi).2] using (p i).terminal_eq

/-- Weighted counting with bounded occupation multiplicity, on any finite family. -/
theorem finite_weighted_source_bound {ι : Type*}
    (F : Finset ι) (source : ι → ℕ) {R : ℕ}
    (p : ∀ i, NDGeom2RootSideSyracusePath (source i) R)
    (hinj : Set.InjOn (fun i => (source i, (p i).depth)) F)
    {X : ℝ} (hX : 0 < X) (hsource : ∀ i ∈ F, X ≤ (source i : ℝ))
    (ψ : ℕ → ℝ) (hψ : ∀ x ∈ F.image source, 0 ≤ ψ x) :
    (∑ i ∈ F, ndRootUniformWordAtom (p i).word * ψ (source i)) ≤
      ((R : ℝ) * (3 * (R : ℝ) + 1) / X) * ∑ x ∈ F.image source, ψ x := by
  classical
  have hgroup : (∑ i ∈ F, ndRootUniformWordAtom (p i).word * ψ (source i)) =
      ∑ x ∈ F.image source,
        (∑ i ∈ F with source i = x, ndRootUniformWordAtom (p i).word) * ψ x := by
    rw [← Finset.sum_fiberwise_of_maps_to
      (fun i hi => Finset.mem_image_of_mem source hi)
      (fun i => ndRootUniformWordAtom (p i).word * ψ (source i))]
    apply Finset.sum_congr rfl
    intro x _
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro i hi
    rw [(Finset.mem_filter.mp hi).2]
  rw [hgroup, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro x hx
  rcases Finset.mem_image.mp hx with ⟨i, hi, rfl⟩
  have hxpos : 0 < source i := by exact_mod_cast lt_of_lt_of_le hX (hsource i hi)
  apply mul_le_mul_of_nonneg_right _ (hψ _ (Finset.mem_image_of_mem source hi))
  exact (path_fiber_bound F source p hinj (source i) hxpos).trans
    (div_le_div_of_nonneg_left (by positivity) hX (hsource i hi))

/-- Version for an arbitrary finite index type, matching terminal-incidence APIs. -/
theorem weighted_source_bound {ι : Type*} [Fintype ι]
    (source : ι → ℕ) {R : ℕ}
    (p : ∀ i, NDGeom2RootSideSyracusePath (source i) R)
    (hinj : Function.Injective (fun i => (source i, (p i).depth)))
    {X : ℝ} (hX : 0 < X) (hsource : ∀ i, X ≤ (source i : ℝ))
    (ψ : ℕ → ℝ) (hψ : ∀ x, 0 ≤ ψ x) :
    (∑ i, ndRootUniformWordAtom (p i).word * ψ (source i)) ≤
      ((R : ℝ) * (3 * (R : ℝ) + 1) / X) *
        ∑ x ∈ Finset.univ.image source, ψ x := by
  classical
  exact finite_weighted_source_bound Finset.univ source p hinj.injOn hX
    (fun i _ => hsource i) ψ (fun x _ => hψ x)

end
end Erdos1135.ND.PositiveDensity.WeightedPathOccupation
