# Phase 10 Collaborator Brief

Date: 2026-05-15

Status: archived optional external-facing brief after the Phase-10
reduction.  Under the current no-collaborator route this is not an
active dependency.  It is retained only in case later review by a
functional analyst or dynamicist becomes useful.  It asks one narrow
question about the current `A0` branch.  It does not ask for a Collatz
proof.

## 1. The Question

The collaborator question is:

```text
Can the A0 averaged PhaseState finite-rank quotients K_N^0 be interpreted
as a legitimate weak approximation scheme for a natural killed weighted
transfer/Koopman operator U_s?
```

Equivalently:

```text
Is A0-averaged mathematically defensible, or is it too non-canonical to
support a Banach/operator-theoretic program?
```

This is now the main Gate-10.B question for the existing `FULL` matrices.

## 2. Non-Claims

We are not claiming:

- a proof of Conjecture 6;
- an infinite-dimensional spectral gap;
- a Lasota-Yorke inequality;
- Hennion/Keller-Liverani applicability;
- that finite matrices are exact projections of an infinite operator.

The finite data are diagnostic.  The rigorous existing theorem is the
separate finite-rank K16 certificate.

## 3. Finite Object

The honest source-level finite object is a cell kernel

```text
k_N^{cell}: S_N -> PhaseState,
```

where `S_N` is the retained finite source-cell set, with cells
`i = (T,r,h)`.

The existing Lean matrix type is phase-only:

```text
TransferMatrix V = Matrix (PhaseState V) (PhaseState V) NNReal.
```

Therefore the active `A0` quotient is:

```text
rho_0:S_N -> PhaseState,

K_N^0(a,q)
  = average_{rho_0(i)=a} k_N^{cell}(i,q).
```

The averaging measure is currently uniform over retained cells in each
fiber, unless a better convention is supplied.

## 4. Why It Is Averaged, Not Exact

The source-collapse error is not small enough to pretend that
`PhaseState` is an exact projection:

```text
C_128^0 ~= 0.051512269,
p95      ~= 0.27979821.
```

Thus the active interpretation is:

```text
A0-averaged:
  K_N^0 is an averaged PhaseState finite-rank quotient.
```

The phrase to avoid is:

```text
exact projection of the source-cell kernel.
```

The stronger route `C_N^0 -> 0` is logically possible, but it is not the
baseline.

## 5. The Candidate Infinite Operator

The candidate infinite object is a killed weighted forward/Koopman-side
operator:

```text
(U_s f)(x)
  = 1_D(x) 2^{-s delta(x)} f(pi(tau x)).
```

Here `D` is the nonterminal return domain, `tau` is a first-return map,
`delta` is the return exponent, and terminal points lose mass.

This formula is still conditional.  A collaborator may reject the
underlying phase space or suggest a better one.

## 6. Desired Theorem Shape

The hoped-for theorem is weak and conditional:

```text
If:
  1. U_s is a natural killed weighted operator;
  2. K_N^0 is accepted as the averaged finite-rank approximation scheme;
  3. P_N^0 -> 0 in a declared weak norm;
  4. tail/killing errors T_{N,L}^0 are controlled;
  5. finite weak estimates transfer through E_N,I_N to B_s -> B_w;

then K_N^0 approximates U_s weakly as an averaged finite-rank scheme.
```

This would not imply a spectral gap.  It would only make the finite
approximation layer honest enough to discuss later analytic hypotheses.

## 7. Evidence to Know

Finite prefix drift of the averaged phase quotient decreases on tested
prefixes:

```text
P_16^0  ~= 0.006631064,
P_32^0  ~= 0.005546595,
P_64^0  ~= 0.004502430.
```

This is evidence only.  It is not a convergence theorem.

The main obstruction is still source collapse:

```text
C_N^0 is currently much larger than P_N^0.
```

So the collaborator should judge the approximation framework, not the
numerical trend alone.

## 8. Specific Questions

1. Is an averaged quotient like `K_N^0` a legitimate finite-rank
   approximation scheme in any standard or defensible transfer-operator
   framework?

2. If yes, what weak norm or Banach pair could make this meaningful?

3. If no, is the failure due to the averaging convention, the lack of a
   canonical source measure, the killed dynamics, or the phase space?

4. Does this resemble any known setting: open systems, Ulam-type
   schemes, Galerkin approximations, conditional expectations,
   countable Markov shifts, or non-archimedean symbolic systems?

5. What early criterion would decisively stop the analytic branch and
   route Phase 10 to the finite-rank note?

## 9. Materials to Send

Send only the reduced materials first:

1. `notes/phase10_reduced_core.md`;
2. `notes/phase10_A0_averaged_interpretation.md`;
3. `notes/phase10_A0_theorem_skeleton.md`;
4. `notes/phase10_finite_rank_fallback.md`.

Do not send raw numerical reports first.  The collaborator should see
the mathematical reduction before the data.

## 10. Best-Fit Collaborator

Useful expertise:

- transfer/Koopman operators for open or killed systems;
- finite-rank approximation schemes;
- weak operator norms and Keller-Liverani-type perturbation theory;
- symbolic or non-archimedean dynamics;
- countable Markov shifts if the compact model fails.

The needed output is not a proof.  It is a go/no-go judgment on whether
`A0-averaged` is a serious approximation framework.
