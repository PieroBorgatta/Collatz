# Mathlib Infrastructure Inventory

Author: AI-assisted (Codex) + Piero Borgatta. Date: 2026-05-04.

This file records the Mathlib API choices for formalizing the exact
congruential shadowing lemma from Section 3 of
`paper/collatz_spectral_reduction.tex`.

The project is pinned to Lean `4.29.1` and Mathlib `v4.29.1`.

## Tested Commands

Use the local elan installation from this machine:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake env lean CollatzShadowing/Inventory.lean
```

The plain command `lake` may not be on the shell `PATH` in Codex.

## Imports

For Phase 1 API exploration:

```lean
import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.NumberTheory.Padics.PadicNorm
import Mathlib.NumberTheory.Padics.PadicNumbers
import Mathlib.NumberTheory.Padics.PadicIntegers
import Mathlib.RingTheory.Multiplicity
import Mathlib.Tactic
```

For later theorem files, prefer narrower imports once the definitions
settle. `import Mathlib` is useful for scratch exploration but too broad
for stable project modules.

## 1.1 Valuations on Nat, Int, Rat

Core declarations:

```lean
#check padicValNat
-- padicValNat (p n : Nat) : Nat

#check padicValInt
-- padicValInt (p : Nat) (z : Int) : Nat

#check padicValRat
-- padicValRat (p : Nat) (q : Rat) : Int

#check padicNorm
-- padicNorm (p : Nat) (q : Rat) : Rat
```

Useful lemmas:

```lean
#check padicValNat.self
-- {p : Nat} -> 1 < p -> padicValNat p p = 1

#check padicValNat.eq_zero_of_not_dvd
-- not divisible by p implies valuation zero

#check padicValInt.of_nat
-- padicValInt p (n : Int) = padicValNat p n

#check padicValRat.of_nat
-- padicValRat p (n : Rat) = padicValNat p n

#check padicValRat.of_int
-- padicValRat p (z : Rat) = padicValInt p z

#check padicValRat.mul
-- valuation of a nonzero rational product

#check padicValRat.pow
-- valuation of a rational power
```

Divisibility bridges for natural numbers:

```lean
#check padicValNat.prime_pow
-- [Fact p.Prime] -> padicValNat p (p ^ n) = n

#check padicValNat_dvd_iff
-- [Fact p.Prime] -> p ^ a ∣ n iff a <= padicValNat p n
```

The general multiplicity API lives in:

```lean
import Mathlib.RingTheory.Multiplicity
```

Useful declarations:

```lean
#check multiplicity
#check emultiplicity
#check pow_dvd_of_le_multiplicity
#check pow_multiplicity_dvd
#check multiplicity_eq_of_dvd_of_not_dvd
```

For this project, `padicValNat`, `padicValInt`, and `padicValRat` are the
right primary API. Use `multiplicity` only if a proof naturally reduces
to generic prime-power divisibility.

## 1.2 Padic and PadicInt

Core types and notation:

```lean
#check Padic
-- Padic (p : Nat) [Fact p.Prime] : Type

#check PadicInt
-- PadicInt (p : Nat) [Fact p.Prime] : Type

#check (ℚ_[2])
-- Type, notation for Padic 2

#check (ℤ_[2])
-- Type, notation for PadicInt 2
```

Use the real Lean notation with Unicode in files:

```lean
example : ℚ_[2] = Padic 2 := rfl
example : ℤ_[2] = PadicInt 2 := rfl
```

Valuations:

```lean
#check Padic.valuation
-- {p : Nat} [Fact p.Prime] -> Q_[p] -> Int

#check PadicInt.valuation
-- {p : Nat} [Fact p.Prime] -> Z_[p] -> Nat
```

Important valuation lemmas:

```lean
#check Padic.valuation_ratCast
-- ((q : Q_[p]).valuation) = padicValRat p q

#check Padic.valuation_intCast
-- ((z : Q_[p]).valuation) = padicValInt p z

#check Padic.valuation_natCast
-- ((n : Q_[p]).valuation) = padicValNat p n

#check Padic.valuation_mul
-- valuation of a nonzero product in Q_[p]

#check Padic.valuation_inv
-- valuation of inverse in Q_[p]

#check Padic.valuation_pow
-- valuation of natural powers in Q_[p]

#check Padic.valuation_zpow
-- valuation of integer powers in Q_[p]

#check Padic.le_valuation_add
-- ultrametric lower bound for valuation of a sum
```

For `ℤ_[p]`:

```lean
#check PadicInt.valuation_coe
-- ((x : Q_[p]).valuation) = x.valuation

#check PadicInt.valuation_mul
-- valuation of a nonzero product in Z_[p]

#check PadicInt.valuation_pow
-- valuation of powers in Z_[p]

#check PadicInt.valuation_p
-- (p : Z_[p]).valuation = 1

#check PadicInt.valuation_p_pow_mul
-- ((p : Z_[p]) ^ n * c).valuation = n + c.valuation, if c != 0
```

Warning: `PadicInt.valuation 0 = 0` by convention. Therefore valuation
inequalities do not by themselves express divisibility of zero by every
power. For congruence, use ideal membership as the primary definition.

## 1.3 Coercions

Working coercions into `ℤ_[2]`:

```lean
example (n : Nat) : ℤ_[2] := (n : ℤ_[2])
example (z : Int) : ℤ_[2] := (z : ℤ_[2])
```

Working coercions into `ℚ_[2]`:

```lean
example (n : Nat) : ℚ_[2] := (n : ℚ_[2])
example (z : Int) : ℚ_[2] := (z : ℚ_[2])
example (q : Rat) : ℚ_[2] := (q : ℚ_[2])
```

Canonical embedding of `ℤ_[2]` into `ℚ_[2]`:

```lean
example (x : ℤ_[2]) : ℚ_[2] := (x : ℚ_[2])
```

Coercion lemmas:

```lean
#check PadicInt.coe_natCast
-- ((n : Z_[p]) : Q_[p]) = n

#check PadicInt.coe_intCast
-- ((z : Z_[p]) : Q_[p]) = z

#check Padic.coe_inj
-- rational casts into Q_[p] are injective

#check Padic.coe_add
#check Padic.coe_sub
#check Padic.coe_mul
#check Padic.coe_div
```

### Rational numbers that are 2-adic integers

Not every rational should be coerced directly into `ℤ_[2]`. The rational
is a 2-adic integer precisely when its denominator is not divisible by 2.
For the phantom fixed point

```text
q_w = C_w / (2^A - 3^L)
```

the denominator is odd, because `2^A` is even for positive `A` while
`3^L` is odd. So `q_w` belongs to `ℤ_[2]`.

Type-checked template:

```lean
noncomputable def ratToZ2 (q : Rat) (hden : ¬ (2 : Nat) ∣ q.den) : ℤ_[2] :=
  ⟨(q : ℚ_[2]), Padic.norm_rat_le_one hden⟩
```

Relevant lemma:

```lean
#check Padic.norm_rat_le_one
-- if p does not divide q.den, then norm (q : Q_[p]) <= 1
```

This is the preferred construction for `q_w : ℤ_[2]` in Phase 2.

## 1.4 Congruence n equiv q modulo 2^k

The paper writes:

```text
n equiv q_w (mod 2^(B_m + 1))
```

with `n : Nat` and `q_w : Rat`, interpreted inside `ℤ_2`.

Recommended Lean definition:

```lean
def PadicCongruentModPow2 (x y : ℤ_[2]) (k : Nat) : Prop :=
  x - y ∈ (Ideal.span {((2 : ℤ_[2]) ^ k)} : Ideal ℤ_[2])
```

Then the lemma hypothesis should look like:

```lean
PadicCongruentModPow2 (n : ℤ_[2]) qwZ2 (B m + 1)
```

where `qwZ2 : ℤ_[2]` is constructed from the rational `q_w` using the
odd-denominator proof above.

This formulation is robust because it handles `x = y` automatically.

Equivalent nonzero valuation form:

```lean
example (x y : ℤ_[2]) (k : Nat) (hxy : x - y ≠ 0) :
    (x - y ∈ (Ideal.span {((2 : ℤ_[2]) ^ k)} : Ideal ℤ_[2])) ↔
      k ≤ (x - y).valuation := by
  exact PadicInt.mem_span_pow_iff_le_valuation (x - y) hxy k
```

The zero case should remain on the ideal-membership side, because
`(0 : ℤ_[2]).valuation = 0`.

For comparison with finite residues and the Python scripts, Mathlib also
has:

```lean
#check Nat.ModEq
#check Int.ModEq
#check ZMod
```

But these are not the preferred primary representation for Lemma 3.1,
because the theorem naturally lives in `ℤ_[2]` and compares an integer
with a rational 2-adic integer.

## 1.5 Modeling Recommendations for Phase 2

Use the following Lean-side architecture:

1. In `Basic.lean`, define:

```lean
def nu2Nat (n : Nat) : Nat := padicValNat 2 n
def nu2Int (z : Int) : Nat := padicValInt 2 z
def nu2Rat (q : Rat) : Int := padicValRat 2 q
```

The accelerated Syracuse map on naturals can be:

```lean
def syracuseOddStep (n : Nat) : Nat :=
  (3 * n + 1) / 2 ^ padicValNat 2 (3 * n + 1)
```

Later proofs should assume `Odd n` or `n % 2 = 1` as needed.

2. In `Phantom.lean`, represent phantom words as a structure rather than
a bare subtype scattered through proofs:

```lean
structure PhantomWord where
  vals : List Nat
  nonempty : vals ≠ []
  positive : ∀ a ∈ vals, 0 < a
```

3. Define `A_w` as `w.vals.sum`, and define `C_w` by folding the pair
`(C_j, A_j)`:

```lean
def affineFoldStep (state : Nat × Nat) (a : Nat) : Nat × Nat :=
  (3 * state.1 + 2 ^ state.2, state.2 + a)
```

4. Define the rational fixed point first:

```lean
qRat = (C_w : Rat) / ((2 : Rat) ^ A_w - (3 : Rat) ^ L)
```

Then define the 2-adic integer representative via `ratToZ2`, with a proof
that the denominator is odd. For the paper's expansive phantoms, this is
the object used in the congruence hypothesis.

5. Define the shadowing congruence by ideal membership, not by valuation:

```lean
def PadicCongruentModPow2 (x y : ℤ_[2]) (k : Nat) : Prop :=
  x - y ∈ (Ideal.span {((2 : ℤ_[2]) ^ k)} : Ideal ℤ_[2])
```

6. Only introduce `PadicInt.valuation` lemmas after unfolding a nonzero
difference, or after splitting the zero case.

## Open Gaps

- A clean proof that the rational `q_w` has odd denominator in Mathlib's
normalized `Rat.den` form still needs to be written. Mathematically it
comes from `2^A - 3^L` being odd and nonzero, but Lean may require a few
integer/rational normalization lemmas.
- The exact statement of Lemma 3.1 may be easier if the phantom word is
modeled together with its periodic extension function
`aAt : Nat -> Nat`, instead of repeatedly using `List.get` with modular
indices.
- Division by `2^a` inside `ℤ_[2]` is not available as division by a unit,
because `2` is not a unit in `ℤ_[2]`. The affine Syracuse maps involving
division by powers of 2 should probably be stated in `ℚ_[2]`, while the
residue/congruence hypotheses live in `ℤ_[2]`.
- For Phase 3, the central proof step will likely use `Padic.valuation`
on `ℚ_[2]` for affine differences, then return to `ℤ_[2]` congruences via
ideal membership where needed.

## Verified Snippet

The following snippet typechecks under the current project pin:

```lean
import Mathlib.NumberTheory.Padics.PadicIntegers
import Mathlib.NumberTheory.Padics.PadicNumbers

noncomputable def ratToZ2 (q : Rat) (hden : ¬ (2 : Nat) ∣ q.den) : ℤ_[2] :=
  ⟨(q : ℚ_[2]), Padic.norm_rat_le_one hden⟩

def PadicCongruentModPow2 (x y : ℤ_[2]) (k : Nat) : Prop :=
  x - y ∈ (Ideal.span {((2 : ℤ_[2]) ^ k)} : Ideal ℤ_[2])

example (x y : ℤ_[2]) (k : Nat) (hxy : x - y ≠ 0) :
    PadicCongruentModPow2 x y k ↔ k ≤ (x - y).valuation := by
  exact PadicInt.mem_span_pow_iff_le_valuation (x - y) hxy k
```
