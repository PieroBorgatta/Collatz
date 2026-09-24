# Exact first-barrier audit — 2026-07-27

## Outcome

The generic residue-versus-barrier test is now Lean-checked, but the audit
also proves a sharp limitation: when evaluated at an exact matched source,
the barrier gap is algebraically identical to the signed orbit displacement.
It is therefore not, by itself, a new ranking function.

This quickly confirms—in a source-independent form—the negative conclusion
already reached for the A0 first-barrier program in v4.

## Correct exact modulus

For a nonempty exponent word `w`, put

```text
S = sum(w)
k = length(w)
C = syracuseWordConst(w).
```

The modulus determining an exact valuation word is

```text
M = 2^(S+1),
```

not merely `2^S`. Divisibility modulo `2^S` makes the affine endpoint
integral. The additional bit records that the quotient is odd, hence that
the last valuation is exact.

For every matched source `n`,

```text
(3^k*n + C) % 2^(S+1) = 2^S.
```

This statement is formalized as
`syracuseWordAffine_mod_exactResidueModulus_of_matches`.

## Exact barrier

For a contracting word, define

```text
D = 2^S - 3^k > 0.
```

If

```text
r = n % 2^(S+1)
```

and

```text
C < D*r,
```

then `r <= n`, hence `C < D*n`, and the matched endpoint is strictly below
`n`. This is Lean-checked as
`evalSyracuseWord_lt_of_exactResidue_above_barrier`.

The contrapositive is
`exactResidue_le_barrier_of_matched_nonDrop`.

## The no-go identity

For every matched word and source,

```text
((2^S - 3^k)*n - C) = 2^S*(n - evalSyracuseWord(w,n))
```

over the integers.

Consequently, on a contracting matched word,

```text
C < (2^S - 3^k)*n
    iff
evalSyracuseWord(w,n) < n.
```

These facts are Lean-checked as

- `syracuseWordBarrierGapInt_eq_scaledDisplacement`;
- `evalSyracuseWord_lt_iff_source_above_barrier`.

Thus a computation of the barrier at the canonical exact residue is just a
re-expression of the corresponding descent computation. It does not provide
an independent induction unless one first derives a lower bound on the
residue from data not equivalent to evaluating the same orbit.

## Small exact tree audit

The script
`scripts/phantom_taxonomy/first_barrier_tree.py` enumerates exponent words,
uses the exact modulus `2^(S+1)`, and handles the unbounded exponent alphabet
analytically:

```text
if D_child > C_child,
then every positive residue in that entire large-exponent tail drops.
```

The retained audit depth is 14. It found:

- 51,033 noncontracting words at depth 14;
- every tested first-contracting cylinder strictly closed;
- one finite equality bucket only: word `[2]`, source `1`;
- no sampled starting-integer range and no floating-point arithmetic.

An exploratory run through depth 18 gave the same classification over
1,900,470 noncontracting frontier words. This is evidence only.

The closest strict closure at retained depth was

```text
word = [1,1,2,3]
D = 47
C = 73
r = 7
D*r - C = 256 = 2^7 * (7 - 5).
```

The final equality displays the no-go identity explicitly: the “barrier
margin” is exactly the scaled drop of the canonical source.

## Decision

Do not promote the observed finite-depth statement

```text
every first-contracting prefix drops, except [2] at source 1
```

to a proof strategy without a genuinely independent residue estimate.
Proving it uniformly would already settle a major part of the classical
pointwise/cycle obstruction.

The useful contribution of this phase is instead:

1. correction of the exact cylinder modulus;
2. a reusable Lean theorem converting independent residue bounds into
   descent;
3. a Lean-checked theorem showing exactly when the method becomes circular;
4. early termination of another finite-prefix escalation.

The next project direction should not be another first-barrier enumeration.
The cleanest remaining formal contribution is to formalize the paper-level
Lagarias-coding/non-transport argument from v4, or else to move explicitly
to the separate Diophantine cycle problem.
