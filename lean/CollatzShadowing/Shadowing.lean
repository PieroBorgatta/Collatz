/-
Shadowing congruence and the statement of Paper Section 3, Lemma 3.1.

This file closes Phase 2 of `TODO.md` (task 2.9). The main theorem
`exact_shadowing` is stated with `sorry` as proof; the proof itself is
the content of Phase 4.

Author: AI-assisted (Claude) + Piero Borgatta. Date: 2026-05-04.
-/

import Mathlib.RingTheory.Ideal.Basic
import Mathlib.Logic.Function.Iterate
import CollatzShadowing.Phantom

namespace CollatzShadowing

/-!
## Shadowing congruence in `ℤ_[2]`

Per `INVENTORY.md` §1.4, congruences of the form `x ≡ y (mod 2^k)`
inside `ℤ_[2]` are encoded as ideal membership. This is robust to the
edge case `x = y`, which would otherwise interact badly with the
`PadicInt.valuation 0 = 0` convention.
-/

/-- The shadowing congruence `x ≡ y (mod 2^k)` in `ℤ_[2]`, expressed
as `x - y ∈ ⟨2^k⟩`. -/
def PadicCongruentModPow2 (x y : ℤ_[2]) (k : ℕ) : Prop :=
  x - y ∈ (Ideal.span {((2 : ℤ_[2]) ^ k)} : Ideal ℤ_[2])

/-!
## Lemma 3.1 (exact congruential shadowing)

Paper Section 3:

> Let `w` be an expansive phantom with `2`-adic representative `q_w`,
> and let `n` be a positive odd integer. If
>   `n ≡ q_w (mod 2^{B_m + 1})`
> then the first `m` Syracuse steps of `n` produce exactly the
> word `(a_0, a_1, ..., a_{m-1})`.

Modeling notes:

* The word agreement is stated as
  `syracuseExponent (S^[j] n) = aAt w j` for every `j < m`. This is
  equivalent to the paper's "the first m steps have ν₂-word `(a_0, ...
  a_{m-1})`" because `syracuseExponent` is precisely `ν₂(3·n + 1)`
  (see `Basic.lean`).
* The hypothesis `h_den : QwOddDen w` makes `qwZ2 w h_den` a valid
  `ℤ_[2]` element. For expansive phantoms this hypothesis holds
  unconditionally; the proof is deferred to Phase 3.
* Positivity of `n` is required by the paper; oddness is required for
  the accelerated Syracuse map to make sense in the intended way.
* The proof itself (induction on `j`, paper proof body of Lemma 3.1)
  is the content of Phase 4.
-/

/--
**Paper Section 3, Lemma 3.1 (Exact congruential shadowing).**

If a positive odd natural `n` is `2`-adically congruent to the phantom
representative `q_w` modulo `2^{B_m + 1}`, then the first `m`
Syracuse steps of `n` produce exactly the periodic word
`(a_0, a_1, ..., a_{m-1})` of `w`.
-/
theorem exact_shadowing
    (w : PhantomWord) (h_den : PhantomWord.QwOddDen w)
    (n : ℕ) (_h_pos : 0 < n) (_h_odd : Odd n) (m : ℕ)
    (_h_cong :
      PadicCongruentModPow2 (n : ℤ_[2]) (qwZ2 w h_den) (w.B m + 1)) :
    ∀ j, j < m → syracuseExponent (S^[j] n) = w.aAt j := by
  sorry

/--
**Paper Section 3, Lemma 3.1 (period form).**

Specialisation of `exact_shadowing` to `m = b · L`: if `n` matches
`q_w` modulo `2^{b·A + 1}`, then `n` shadows `w^∞` for the first `b`
full periods.
-/
theorem exact_shadowing_periods
    (w : PhantomWord) (h_den : PhantomWord.QwOddDen w)
    (n : ℕ) (h_pos : 0 < n) (h_odd : Odd n) (b : ℕ)
    (h_cong :
      PadicCongruentModPow2 (n : ℤ_[2]) (qwZ2 w h_den) (b * w.A + 1)) :
    ∀ j, j < b * w.length → syracuseExponent (S^[j] n) = w.aAt j := by
  -- B_{b·L} = b · A by full-period accumulation; then reduce to
  -- `exact_shadowing`. Both the helper identity and the reduction are
  -- left to Phase 3/4.
  sorry

end CollatzShadowing
