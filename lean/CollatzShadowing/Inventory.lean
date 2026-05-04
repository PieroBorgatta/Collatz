/-
Phase 1 — Mathlib infrastructure inventory.

This is a scratch buffer for exploring Mathlib's API. It is NOT
imported by the main `CollatzShadowing` library. Open it in your
editor and check the InfoView for the output of each `#check` and
`#print`. Sections correspond to tasks 1.1–1.4 of `lean/TODO.md`.

The first time you open this file, the Lean server will spend 1–2
minutes elaborating Mathlib. Subsequent opens are fast.

For each section: tell me which `#check`s succeed, which fail, and
the exact types shown by the InfoView. We will document the findings
in `INVENTORY.md`.

Author: AI-assisted (Claude / Claude Code) + Piero Borgatta. Date: 2026-05-04.
-/

import Mathlib

namespace CollatzShadowing.Inventory

-- ════════════════════════════════════════════════════════════════════
-- Section 1.1 — padicValNat / padicValInt / padicValRat / multiplicity
-- ════════════════════════════════════════════════════════════════════

-- We need ν₂ (the 2-adic valuation) on ℕ, ℤ, ℚ.

#check @padicValNat
#check @padicValInt
#check @padicValRat

-- Sanity checks (these should typecheck and be `decide`-able)
example : padicValNat 2 12 = 2 := by decide
example : padicValNat 2 8  = 3 := by decide
example : padicValNat 2 1  = 0 := by decide
example : padicValNat 2 0  = 0 := by decide   -- by convention

example : padicValInt 2 (-12 : ℤ) = 2 := by decide
example : padicValRat 2 (12 / 5 : ℚ) = 2 := by decide
example : padicValRat 2 (5 / 12 : ℚ) = -2 := by decide

-- `multiplicity` is the more general gadget; `padicValNat p` should be
-- definable from it for prime p. Let's just locate it.
#check @multiplicity

-- And the p-adic NORM (real-valued; we'll mostly use the valuation)
#check @padicNorm

-- ════════════════════════════════════════════════════════════════════
-- Section 1.2 — Padic, PadicInt, valuation API
-- ════════════════════════════════════════════════════════════════════

-- ℚ_p and ℤ_p as Mathlib types
#check @Padic
#check @PadicInt

-- The standard notations
example : ℚ_[2] = Padic 2 := rfl
example : ℤ_[2] = PadicInt 2 := rfl

-- Valuation on ℤ_p (the "how many factors of p does this have" function)
#check @PadicInt.valuation
#check @Padic.valuation

-- Algebraic structure: ℤ_p is a discrete valuation ring, ℚ_p is its field
-- of fractions. Try to inspect the instance:
example : DiscreteValuationRing (ℤ_[2]) := by infer_instance
example : Field (ℚ_[2]) := by infer_instance

-- ════════════════════════════════════════════════════════════════════
-- Section 1.3 — coercions ℕ / ℤ / ℚ  →  ℤ_p / ℚ_p
-- ════════════════════════════════════════════════════════════════════

-- Natural and integer inclusions into ℤ_2
example (n : ℕ) : ℤ_[2] := (n : ℤ_[2])
example (n : ℤ) : ℤ_[2] := (n : ℤ_[2])

-- Inclusion into ℚ_2
example (n : ℕ) : ℚ_[2] := (n : ℚ_[2])
example (q : ℚ) : ℚ_[2] := (q : ℚ_[2])

-- Embedding ℤ_p ↪ ℚ_p (the canonical one)
example (x : ℤ_[2]) : ℚ_[2] := (x : ℚ_[2])

-- ════════════════════════════════════════════════════════════════════
-- Section 1.4 — congruence  n ≡ q (mod 2^k)  in ℤ_2
-- ════════════════════════════════════════════════════════════════════

-- The paper writes `n ≡ q_w (mod 2^(bA+1))` with n ∈ ℕ and q_w ∈ ℚ.
-- The natural Lean formalization: in ℤ_2, view both as elements and
-- assert that their difference is in the ideal (2^k) · ℤ_2.

-- approach A: use the maximal ideal of ℤ_2
#check @PadicInt.maximalIdeal

-- approach B: ν₂(x - y) ≥ k iff (x - y) is divisible by 2^k in ℤ_2
example (x y : ℤ_[2]) (k : ℕ) : Prop :=
  (2 : ℤ_[2])^k ∣ (x - y)

example (x y : ℤ_[2]) (k : ℕ) : Prop :=
  PadicInt.valuation (x - y) ≥ k

-- approach C: `ZMod`-style — quotient by the ideal
-- (most likely we will NOT use this, but it exists)
#check @ZMod

-- ════════════════════════════════════════════════════════════════════
-- Section 1.5 — quick smoke test: state Lemma 3.1's core inequality
-- ════════════════════════════════════════════════════════════════════
-- Just to see if we have the language to express the kind of statement
-- we will need.  This is NOT yet the lemma; just a typecheck probe.

example
    (n : ℕ) (q : ℤ_[2]) (k : ℕ)
    (hcong : (2 : ℤ_[2])^k ∣ ((n : ℤ_[2]) - q)) :
    True := trivial

end CollatzShadowing.Inventory
