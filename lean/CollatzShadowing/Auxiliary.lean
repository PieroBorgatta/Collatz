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
import Mathlib.Data.List.GetD
import Mathlib.Logic.Function.Iterate
import CollatzShadowing.Phantom
import CollatzShadowing.Syracuse2Adic

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

/-!
## Helpers for Tasks 3.2 and 3.3
-/

namespace PhantomWord

/-- Every phantom word has positive length (it is non-empty). -/
theorem length_pos (w : PhantomWord) : 0 < w.length := by
  rcases hvals : w.vals with _ | ⟨a, t⟩
  · exact absurd hvals w.nonempty
  · simp [PhantomWord.length, hvals]

/-- Each entry of the periodic extension `aAt` is positive. -/
theorem aAt_pos (w : PhantomWord) (j : ℕ) : 0 < w.aAt j := by
  unfold aAt
  have hlt : j % w.length < w.vals.length := Nat.mod_lt j w.length_pos
  rw [List.getD_eq_getElem _ _ hlt]
  exact w.positive _ (List.getElem_mem _)

end PhantomWord

/-- The 2-adic valuation alias `ν₂Z2 = nu2Z2` agrees with the underlying
`PadicInt.valuation`, in particular `ν₂Z2 0 = 0`. -/
private theorem nu2Z2_zero : ν₂Z2 (0 : ℤ_[2]) = 0 := by
  unfold ν₂Z2 nu2Z2
  exact PadicInt.valuation_zero

/-- If the `i`-th step matches the prescribed positive `aAt w i`, then
the relevant `3·x + 1` cannot be zero. -/
private theorem ne_zero_of_matches (w : PhantomWord) (x : ℤ_[2]) (i : ℕ)
    (h : ν₂Z2 ((3 : ℤ_[2]) * Syracuse2adic^[i] x + 1) = w.aAt i) :
    (3 : ℤ_[2]) * Syracuse2adic^[i] x + 1 ≠ 0 := by
  intro hz
  rw [hz, nu2Z2_zero] at h
  -- h : 0 = w.aAt i, but aAt is positive
  have := w.aAt_pos i
  omega

/-!
## Task 3.2 — Affine difference identity (paper line 276)

After the first `j` Syracuse steps of `n` and `q_w` follow the same
prescribed word `(a_0, ..., a_{j-1})`, the difference of the iterates
in `ℚ_[2]` is

```text
S^j(n) - S^j(q_w) = (3^j / 2^{B_j}) · (n - q_w).
```

The identity lives in `ℚ_[2]` because the `2^{B_j}` denominator is not
invertible in `ℤ_[2]`. Proof deferred (induction on `j` using the
unitCoeff representation of one `Syracuse2adic` step).
-/

/-- Hypothesis that the first `j` Syracuse steps of `x` follow the
phantom word `w`. -/
def MatchesPrefix (w : PhantomWord) (x : ℤ_[2]) (j : ℕ) : Prop :=
  ∀ i, i < j → ν₂Z2 ((3 : ℤ_[2]) * Syracuse2adic^[i] x + 1) = w.aAt i

/-- One Syracuse2adic step transforms the difference of two inputs by
the factor `3 / 2^a`, where `a` is the common 2-adic valuation of
`3·x + 1` and `3·y + 1`. -/
private theorem syracuse_one_step_diff (x y : ℤ_[2])
    (hx : (3 : ℤ_[2]) * x + 1 ≠ 0)
    (hy : (3 : ℤ_[2]) * y + 1 ≠ 0)
    (hval_eq : ((3 : ℤ_[2]) * x + 1).valuation = ((3 : ℤ_[2]) * y + 1).valuation) :
    (Syracuse2adic x : ℚ_[2]) - (Syracuse2adic y : ℚ_[2])
      = (3 : ℚ_[2]) / (2 : ℚ_[2]) ^ ((3 : ℤ_[2]) * x + 1).valuation
        * ((x : ℚ_[2]) - (y : ℚ_[2])) := by
  -- Cast spec to ℚ_[2] for both x and y.
  have sxQ : (3 : ℚ_[2]) * (x : ℚ_[2]) + 1
           = (Syracuse2adic x : ℚ_[2])
              * (2 : ℚ_[2]) ^ ((3 : ℤ_[2]) * x + 1).valuation := by
    have h := congrArg (fun z : ℤ_[2] => (z : ℚ_[2])) (Syracuse2adic_spec x hx)
    push_cast at h
    convert h using 2
  have syQ : (3 : ℚ_[2]) * (y : ℚ_[2]) + 1
           = (Syracuse2adic y : ℚ_[2])
              * (2 : ℚ_[2]) ^ ((3 : ℤ_[2]) * y + 1).valuation := by
    have h := congrArg (fun z : ℤ_[2] => (z : ℚ_[2])) (Syracuse2adic_spec y hy)
    push_cast at h
    convert h using 2
  -- Combine: same exponent on both via hval_eq.
  rw [hval_eq] at sxQ
  -- 3·(x-y) = (S2 x - S2 y) · 2^v   (subtracting syQ from sxQ in ℚ_[2]).
  have hQ : (3 : ℚ_[2]) * ((x : ℚ_[2]) - (y : ℚ_[2]))
          = ((Syracuse2adic x : ℚ_[2]) - (Syracuse2adic y : ℚ_[2]))
              * (2 : ℚ_[2]) ^ ((3 : ℤ_[2]) * y + 1).valuation := by
    linear_combination sxQ - syQ
  -- Divide both sides by `2^v` (a unit in ℚ_[2]).
  have h2_ne : (2 : ℚ_[2]) ≠ 0 := two_ne_zero
  have hpow_ne : ((2 : ℚ_[2]) ^ ((3 : ℤ_[2]) * y + 1).valuation) ≠ 0 :=
    pow_ne_zero _ h2_ne
  rw [hval_eq]
  field_simp
  linear_combination -hQ

/--
**Task 3.2.** If `n` and `q_w` follow the same prescribed word for the
first `j` Syracuse steps, then their `j`-th iterates differ by the
affine factor `3^j / 2^{B_j}` times the original difference, in
`ℚ_[2]`. (Paper line 276.)

Proof by induction on `j`. Stated in `ℚ_[2]` because `2^{B_j}` is not
a unit in `ℤ_[2]`.
-/
theorem affine_difference
    (w : PhantomWord) (n : ℤ_[2]) (j : ℕ)
    (h_n : MatchesPrefix w n j)
    (h_qw : MatchesPrefix w (qwZ2 w (PhantomWord.qwOddDen w)) j) :
    (Syracuse2adic^[j] n : ℚ_[2])
        - (Syracuse2adic^[j] (qwZ2 w (PhantomWord.qwOddDen w)) : ℚ_[2])
      = ((3 : ℚ_[2]) ^ j) / ((2 : ℚ_[2]) ^ w.B j)
          * ((n : ℚ_[2]) - (qwZ2 w (PhantomWord.qwOddDen w) : ℚ_[2])) := by
  induction j with
  | zero =>
    simp [Function.iterate_zero, PhantomWord.B_zero]
  | succ k ih =>
    -- IH applies once we drop the (k+1)-th matching constraint.
    have h_n_k : MatchesPrefix w n k := fun i hi => h_n i (Nat.lt_succ_of_lt hi)
    have h_qw_k : MatchesPrefix w (qwZ2 w (PhantomWord.qwOddDen w)) k :=
      fun i hi => h_qw i (Nat.lt_succ_of_lt hi)
    have ih' := ih h_n_k h_qw_k
    -- Set abbreviations for readability.
    set q : ℤ_[2] := qwZ2 w (PhantomWord.qwOddDen w) with hq
    set xn : ℤ_[2] := Syracuse2adic^[k] n with hxn
    set xq : ℤ_[2] := Syracuse2adic^[k] q with hxq
    -- Use the matching hypothesis at step k for both n and q.
    -- Note: `ν₂Z2 = .valuation` by def, so these proofs serve both forms.
    have h_match_n_ν : ν₂Z2 ((3 : ℤ_[2]) * xn + 1) = w.aAt k := h_n k (Nat.lt_succ_self k)
    have h_match_q_ν : ν₂Z2 ((3 : ℤ_[2]) * xq + 1) = w.aAt k := h_qw k (Nat.lt_succ_self k)
    have h_match_n : ((3 : ℤ_[2]) * xn + 1).valuation = w.aAt k := h_match_n_ν
    have h_match_q : ((3 : ℤ_[2]) * xq + 1).valuation = w.aAt k := h_match_q_ν
    have h_xn_ne : (3 : ℤ_[2]) * xn + 1 ≠ 0 := by
      have := ne_zero_of_matches w n k h_match_n_ν
      simpa [hxn] using this
    have h_xq_ne : (3 : ℤ_[2]) * xq + 1 ≠ 0 := by
      have := ne_zero_of_matches w q k h_match_q_ν
      simpa [hxq] using this
    have h_val_eq : ((3 : ℤ_[2]) * xn + 1).valuation = ((3 : ℤ_[2]) * xq + 1).valuation := by
      rw [h_match_n, h_match_q]
    -- One-step difference formula at k.
    have step := syracuse_one_step_diff xn xq h_xn_ne h_xq_ne h_val_eq
    -- Iterates at k+1.
    have h_iter : Syracuse2adic^[k+1] n = Syracuse2adic xn := by
      rw [Function.iterate_succ', Function.comp_apply]
    have h_iter_q : Syracuse2adic^[k+1] q = Syracuse2adic xq := by
      rw [Function.iterate_succ', Function.comp_apply]
    rw [h_iter, h_iter_q, step, h_match_n, w.B_succ k]
    rw [ih']
    -- Algebraic simplification in ℚ_[2].
    have h2_ne : (2 : ℚ_[2]) ≠ 0 := two_ne_zero
    have hpow_Bk : ((2 : ℚ_[2]) ^ w.B k) ≠ 0 := pow_ne_zero _ h2_ne
    have hpow_aAt : ((2 : ℚ_[2]) ^ w.aAt k) ≠ 0 := pow_ne_zero _ h2_ne
    field_simp
    ring

/-!
## Phase-4 helpers: monotonicity of `B` and ℤ_[2]-valued affine difference
-/

namespace PhantomWord

/-- The periodic partial sum `B` is monotonically non-decreasing. -/
theorem B_mono (w : PhantomWord) {j k : ℕ} (h : j ≤ k) : w.B j ≤ w.B k := by
  induction k, h using Nat.le_induction with
  | base => exact le_refl _
  | succ k _ ih =>
    rw [B_succ]
    have := w.aAt_pos k
    omega

end PhantomWord

/-- **`ℤ_[2]`-valued affine difference identity.** Multiplied form
of `affine_difference`, valid in `ℤ_[2]` (no division).

Proved by direct induction on `j`, mirroring `affine_difference` but
staying in `ℤ_[2]` throughout (the `2^{B_j}` factor sits on the LHS,
so no division is needed). -/
theorem affine_difference_z2
    (w : PhantomWord) (n : ℤ_[2]) (j : ℕ)
    (h_n : MatchesPrefix w n j)
    (h_qw : MatchesPrefix w (qwZ2 w (PhantomWord.qwOddDen w)) j) :
    (Syracuse2adic^[j] n - Syracuse2adic^[j] (qwZ2 w (PhantomWord.qwOddDen w)))
        * (2 : ℤ_[2]) ^ w.B j
      = (3 : ℤ_[2]) ^ j * (n - qwZ2 w (PhantomWord.qwOddDen w)) := by
  induction j with
  | zero =>
    simp [Function.iterate_zero, PhantomWord.B_zero]
  | succ k ih =>
    have h_n_k : MatchesPrefix w n k := fun i hi => h_n i (Nat.lt_succ_of_lt hi)
    have h_qw_k : MatchesPrefix w (qwZ2 w (PhantomWord.qwOddDen w)) k :=
      fun i hi => h_qw i (Nat.lt_succ_of_lt hi)
    have ih' := ih h_n_k h_qw_k
    set q : ℤ_[2] := qwZ2 w (PhantomWord.qwOddDen w) with hq
    set xn : ℤ_[2] := Syracuse2adic^[k] n with hxn
    set xq : ℤ_[2] := Syracuse2adic^[k] q with hxq
    have h_match_n_ν : ν₂Z2 ((3 : ℤ_[2]) * xn + 1) = w.aAt k := h_n k (Nat.lt_succ_self k)
    have h_match_q_ν : ν₂Z2 ((3 : ℤ_[2]) * xq + 1) = w.aAt k := h_qw k (Nat.lt_succ_self k)
    have h_match_n : ((3 : ℤ_[2]) * xn + 1).valuation = w.aAt k := h_match_n_ν
    have h_match_q : ((3 : ℤ_[2]) * xq + 1).valuation = w.aAt k := h_match_q_ν
    have h_xn_ne : (3 : ℤ_[2]) * xn + 1 ≠ 0 := by
      have := ne_zero_of_matches w n k h_match_n_ν
      simpa [hxn] using this
    have h_xq_ne : (3 : ℤ_[2]) * xq + 1 ≠ 0 := by
      have := ne_zero_of_matches w q k h_match_q_ν
      simpa [hxq] using this
    have sx := Syracuse2adic_spec xn h_xn_ne
    have sq := Syracuse2adic_spec xq h_xq_ne
    rw [h_match_n] at sx
    rw [h_match_q] at sq
    -- One step difference identity in ℤ_[2].
    have h_step_z2 : (3 : ℤ_[2]) * (xn - xq)
                   = (Syracuse2adic xn - Syracuse2adic xq) * (2 : ℤ_[2]) ^ w.aAt k := by
      linear_combination sx - sq
    have h_iter : Syracuse2adic^[k+1] n = Syracuse2adic xn := by
      rw [Function.iterate_succ', Function.comp_apply]
    have h_iter_q : Syracuse2adic^[k+1] q = Syracuse2adic xq := by
      rw [Function.iterate_succ', Function.comp_apply]
    rw [h_iter, h_iter_q, w.B_succ k]
    -- Goal now: (S2 xn - S2 xq) * 2^{B k + aAt k} = 3^{k+1} * (n - q)
    calc (Syracuse2adic xn - Syracuse2adic xq) * (2 : ℤ_[2]) ^ (w.B k + w.aAt k)
        = ((Syracuse2adic xn - Syracuse2adic xq) * (2 : ℤ_[2]) ^ w.aAt k)
              * (2 : ℤ_[2]) ^ w.B k := by rw [pow_add]; ring
      _ = ((3 : ℤ_[2]) * (xn - xq)) * (2 : ℤ_[2]) ^ w.B k := by rw [← h_step_z2]
      _ = (3 : ℤ_[2]) * ((xn - xq) * (2 : ℤ_[2]) ^ w.B k) := by ring
      _ = (3 : ℤ_[2]) * ((3 : ℤ_[2]) ^ k * (n - q)) := by rw [ih']
      _ = (3 : ℤ_[2]) ^ (k + 1) * (n - q) := by ring

/-!
## Task 3.3 — Stable `ν₂` under 2-adic proximity

Under the prefix-matching hypothesis (and hence with the affine
difference of Task 3.2 controlled), `ν₂(3·x + 1)` and `ν₂(3·y + 1)`
agree and equal the prescribed `a_j` whenever the 2-adic distance
between `x` and `y` is at least `a_j + 1`.
-/

/-- Negation preserves the 2-adic valuation in `ℤ_[2]`. -/
private theorem valuation_z2_neg (x : ℤ_[2]) (hx : x ≠ 0) :
    (-x).valuation = x.valuation := by
  have h_neg_ne : -x ≠ 0 := neg_ne_zero.mpr hx
  have hnorm_eq : ‖-x‖ = ‖x‖ := norm_neg x
  rw [PadicInt.norm_eq_zpow_neg_valuation hx,
      PadicInt.norm_eq_zpow_neg_valuation h_neg_ne] at hnorm_eq
  have h2_pos : (0 : ℝ) < 2 := by norm_num
  have h2_ne_one : (2 : ℝ) ≠ 1 := by norm_num
  -- (2:ℝ)^(-v(-x)) = (2:ℝ)^(-v(x)) ⟹ -v(-x) = -v(x) ⟹ v(-x) = v(x)
  have h_eq_zpow : (-((-x).valuation : ℤ)) = (-(x.valuation : ℤ)) :=
    zpow_right_injective₀ h2_pos h2_ne_one hnorm_eq
  omega

/-- **Strict ultrametric on `ℤ_[2]`.** When the 2-adic valuations of two
non-zero `ℤ_[2]`-elements differ strictly, the valuation of the sum
equals the smaller of the two. -/
private theorem valuation_add_eq_left_of_lt
    (a b : ℤ_[2]) (ha : a ≠ 0) (hb : b ≠ 0) (hab : a + b ≠ 0)
    (hlt : a.valuation < b.valuation) :
    (a + b).valuation = a.valuation := by
  -- ≥ direction.
  have hge : a.valuation ≤ (a + b).valuation := by
    have h := PadicInt.le_valuation_add hab
    have hmin : min a.valuation b.valuation = a.valuation := min_eq_left (le_of_lt hlt)
    omega
  -- ≤ direction by contradiction: a = (a + b) + (-b).
  have hle : (a + b).valuation ≤ a.valuation := by
    by_contra hgt
    push Not at hgt
    have h_a_eq : a = (a + b) + (-b) := by ring
    have h_neg_b_ne : -b ≠ 0 := neg_ne_zero.mpr hb
    have h_sum_ne : (a + b) + (-b) ≠ 0 := by rw [← h_a_eq]; exact ha
    have h_min_lt : a.valuation < min (a + b).valuation (-b).valuation := by
      rw [valuation_z2_neg b hb]
      exact lt_min hgt hlt
    have h_le := PadicInt.le_valuation_add h_sum_ne
    rw [← h_a_eq] at h_le
    omega
  omega

/--
**Task 3.3.** If the 2-adic difference between two `ℤ_[2]`-elements
has valuation at least `a_j + 1`, then both produce the same `ν₂` of
`3·· + 1`, equal to `a_j`. (Used to feed the inductive step of
Lemma 3.1.)
-/
theorem nu2_stable_under_proximity
    (w : PhantomWord) (x y : ℤ_[2]) (j : ℕ)
    (h_match_y : ν₂Z2 ((3 : ℤ_[2]) * y + 1) = w.aAt j)
    (h_close : ((w.aAt j) + 1 : ℕ) ≤ ν₂Z2 (x - y)) :
    ν₂Z2 ((3 : ℤ_[2]) * x + 1) = w.aAt j ∧
      ν₂Z2 ((3 : ℤ_[2]) * y + 1) = w.aAt j := by
  refine ⟨?_, h_match_y⟩
  -- Set a := 3y+1, b := 3(x-y), so a + b = 3x+1.
  set a : ℤ_[2] := (3 : ℤ_[2]) * y + 1 with ha_def
  set b : ℤ_[2] := (3 : ℤ_[2]) * (x - y) with hb_def
  have hab_eq : a + b = (3 : ℤ_[2]) * x + 1 := by
    change (3 : ℤ_[2]) * y + 1 + 3 * (x - y) = 3 * x + 1
    ring
  -- ν(a) = aAt w j (from hypothesis, ν₂Z2 = .valuation).
  have hva : a.valuation = w.aAt j := h_match_y
  -- ν(b) ≥ aAt w j + 1 (since ν(3·z) = ν(z) on ℤ_[2], Task 3.1).
  have hvb_ge : w.aAt j + 1 ≤ b.valuation := by
    have h := h_close
    change w.aAt j + 1 ≤ ((3 : ℤ_[2]) * (x - y)).valuation
    have hmul : ν₂Z2 ((3 : ℤ_[2]) * (x - y)) = ν₂Z2 (x - y) := nu2Z2_three_mul (x - y)
    -- ν₂Z2 = .valuation by def
    have hval : ν₂Z2 ((3 : ℤ_[2]) * (x - y)) = ((3 : ℤ_[2]) * (x - y)).valuation := rfl
    omega
  -- Strict comparison: v(a) < v(b).
  have hlt : a.valuation < b.valuation := by rw [hva]; omega
  -- Non-zero conditions.
  have ha_ne : a ≠ 0 := by
    intro h
    have : a.valuation = 0 := by rw [h]; exact PadicInt.valuation_zero
    rw [hva] at this
    have := w.aAt_pos j
    omega
  have hb_ne : b ≠ 0 := by
    intro h
    have : b.valuation = 0 := by rw [h]; exact PadicInt.valuation_zero
    have := w.aAt_pos j
    omega
  have hab_ne : a + b ≠ 0 := by
    intro h
    have : a.valuation = b.valuation := by
      have ha_eq : a = -b := by
        have : a + b = 0 := h
        linear_combination this
      rw [ha_eq, valuation_z2_neg b hb_ne]
    omega
  -- Apply the strict ultrametric.
  have h_sum := valuation_add_eq_left_of_lt a b ha_ne hb_ne hab_ne hlt
  rw [hab_eq] at h_sum
  -- ν₂Z2 = .valuation by def; combine with hva.
  change ((3 : ℤ_[2]) * x + 1).valuation = w.aAt j
  omega

end CollatzShadowing
