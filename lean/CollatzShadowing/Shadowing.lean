/-
Shadowing congruence and the statement of Paper Section 3, Lemma 3.1.

This file closes Phase 2 of `TODO.md` (task 2.9). The main theorem
`exact_shadowing` is stated paper-faithfully in terms of the 2-adic
Syracuse map `Syracuse2adic` (see `Syracuse2Adic.lean`); the proof is
the content of Phase 4.

Author: AI-assisted (Claude) + Piero Borgatta. Date: 2026-05-04.
-/

import Mathlib.RingTheory.Ideal.Basic
import Mathlib.Logic.Function.Iterate
import CollatzShadowing.Phantom
import CollatzShadowing.Auxiliary
import CollatzShadowing.Syracuse2Adic

namespace CollatzShadowing

/-!
## Shadowing congruence in `ℤ_[2]`

Per `INVENTORY.md` §1.4, congruences `x ≡ y (mod 2^k)` inside `ℤ_[2]`
are encoded as ideal membership. This is robust to the edge case
`x = y`, which would interact badly with the
`PadicInt.valuation 0 = 0` convention.
-/

/-- The shadowing congruence `x ≡ y (mod 2^k)` in `ℤ_[2]`, expressed
as `x - y ∈ ⟨2^k⟩`. -/
def PadicCongruentModPow2 (x y : ℤ_[2]) (k : ℕ) : Prop :=
  x - y ∈ (Ideal.span {((2 : ℤ_[2]) ^ k)} : Ideal ℤ_[2])

/-!
## Lemma 3.1 (exact congruential shadowing) — paper-faithful form

Paper Section 3:

> Let `w` be an expansive phantom with `2`-adic representative `q_w`,
> and let `n` be a positive odd integer. If
>   `n ≡ q_w (mod 2^{B_m + 1})`
> then the first `m` Syracuse steps of `n` produce exactly the
> word `(a_0, a_1, ..., a_{m-1})`.

In Lean: the conclusion is stated 1:1 with the paper, using the 2-adic
extension `Syracuse2adic : ℤ_[2] → ℤ_[2]` (see `Syracuse2Adic.lean`).
The `QwOddDen w` hypothesis is now discharged automatically by
`PhantomWord.qwOddDen` (Task 3.1.5), so users supply only the natural
inputs.

The proof itself (induction on `j`, paper proof body of Lemma 3.1
using auxiliary lemmas 3.1–3.4) is the content of Phase 4.
-/

/--
**Paper Section 3, Lemma 3.1 (Exact congruential shadowing).**

If a positive odd natural `n` is `2`-adically congruent to the phantom
representative `q_w` modulo `2^{B_m + 1}`, then the first `m` Syracuse
steps of `n` (computed inside `ℤ_[2]` via `Syracuse2adic`) produce
exactly the periodic word `(a_0, a_1, ..., a_{m-1})` of `w`.

Equivalent integer-level statement (via `Syracuse2adic_natCast`):
`syracuseExponent (S^[j] n) = w.aAt j` for all `j < m`.
-/
theorem exact_shadowing
    (w : PhantomWord) (n : ℕ) (_h_pos : 0 < n) (_h_odd : Odd n) (m : ℕ)
    (_h_cong :
      PadicCongruentModPow2 (n : ℤ_[2])
        (qwZ2 w (PhantomWord.qwOddDen w)) (w.B m + 1)) :
    ∀ j, j < m →
      ν₂Z2 ((3 : ℤ_[2]) * Syracuse2adic^[j] ((n : ℕ) : ℤ_[2]) + 1) = w.aAt j := by
  sorry

/--
**Paper Section 3, Lemma 3.1 (period form).**

Specialisation of `exact_shadowing` to `m = b · L`: if `n` matches
`q_w` modulo `2^{b·A + 1}`, then `n` shadows `w^∞` for the first `b`
full periods.
-/
theorem exact_shadowing_periods
    (w : PhantomWord) (n : ℕ) (h_pos : 0 < n) (h_odd : Odd n) (b : ℕ)
    (h_cong :
      PadicCongruentModPow2 (n : ℤ_[2])
        (qwZ2 w (PhantomWord.qwOddDen w)) (b * w.A + 1)) :
    ∀ j, j < b * w.length →
      ν₂Z2 ((3 : ℤ_[2]) * Syracuse2adic^[j] ((n : ℕ) : ℤ_[2]) + 1) = w.aAt j := by
  -- B_{b·L} = b · A by full-period accumulation; then reduce to
  -- `exact_shadowing`. Both the helper identity and the reduction are
  -- left to Phase 3/4.
  sorry

end CollatzShadowing
