# Phase 10 A0 Averaged Interpretation

Date: 2026-05-15

Status: active interpretation note for the `A0` branch.  This note does
not prove Gate 10.B.  It records the conservative choice that the
existing `PhaseState`/`FULL` branch should be treated as an averaged
finite-rank approximation program, not as an exact projection program.

## 1. Decision

The active interpretation is:

```text
A0-averaged:
  K_N^0 is the averaged PhaseState quotient of the cell kernel
  k_N^{cell}, and is not assumed to be an exact projection.
```

This is a modelling decision, not a theorem.  It is adopted because the
measured source-collapse error is not currently small enough to justify
speaking as if the old `PhaseState` quotient were exact:

```text
C_128^0 ~= 0.051512269,
p95      ~= 0.27979821.
```

The alternative `A0-decay` branch remains logically possible, but it is
not the main branch until there is a proof or substantially stronger
evidence that

```text
C_N^0 -> 0.
```

## 2. Definition

Let `S_N` be the retained source-cell set and let

```text
k_N^{cell}: S_N -> PhaseState
```

be the finite weighted cell kernel.

Let

```text
rho_0:S_N -> PhaseState
```

be the source-phase map.  The averaged quotient is

```text
K_N^0(a,q)
  = average_{i in S_N : rho_0(i)=a} k_N^{cell}(i,q),
```

with the averaging measure explicitly declared.  In the current
diagnostics it is the uniform measure over retained cells in each fiber.

The defining point of `A0-averaged` is that `K_N^0` is not required to
satisfy

```text
k_N^{cell}(i,q) = K_N^0(rho_0(i),q)
```

cellwise, or even approximately in a uniform norm.

Instead, the source-collapse error

```text
C_N^0
  = sum_i omega_N(i)
      || k_N^{cell}(i,.) - K_N^0(rho_0(i),.) ||_1
```

is an explicit modelling/approximation cost.

## 3. What This Buys

This interpretation keeps the existing `FULL`/Lean story aligned with
the actual type of the finite matrices:

```text
TransferMatrix V = Matrix (PhaseState V) (PhaseState V) NNReal.
```

It avoids pretending that the generated or empirical `PhaseState`
matrices are exact projections of a finer source-cell process.

It also makes the collaborator question sharper:

```text
Can a sequence of averaged finite-rank phase quotients K_N^0 converge
weakly to a natural killed weighted operator U_s, even when the
cellwise collapse error C_N^0 is not known to vanish pointwise?
```

If the answer is yes, the analytic program remains meaningful.  If the
answer is no, Gate 10.B should close negatively for the existing `FULL`
matrices and the project should route Phase 10 to the finite-rank
fallback.

## 4. What This Does Not Buy

`A0-averaged` does not provide:

- an exact projection theorem;
- an Ulam/Galerkin interpretation by itself;
- a bound on `C_N^0`;
- compactness;
- a Lasota-Yorke inequality;
- a spectral statement.

In particular, the small observed prefix drift

```text
P_64^0 ~= 0.004502430
```

does not erase the collapse cost.  It only says that the averaged
quotient rows themselves have some finite prefix stability.

## 5. Conditional Theorem Shape

The honest theorem target becomes:

```text
Assume:

1. A natural killed weighted operator U_s is defined on X.
2. K_N^0 is the declared averaged finite-rank approximation scheme.
3. The averaging scheme is compatible with the weak observation norm.
4. P_N^0 -> 0 in that weak norm.
5. Tail/killing errors T_{N,L}^0 are controlled.
6. Projection/inclusion maps E_N,I_N transfer the finite weak bound to
   B_s -> B_w.

Then K_N^0 approximates U_s weakly as an averaged finite-rank scheme.
```

The theorem should not contain the phrase "exact projection" unless a
separate lemma proves it.

## 6. Required Collaborator Judgment

This branch needs a functional analyst/dynamicist to judge one precise
question:

```text
Is the A0 averaged quotient a legitimate approximation framework for
transfer/Koopman operators on a symbolic or 2-adic source space, or is
it too non-canonical to support Hennion/Keller-Liverani style analysis?
```

The collaborator should not be asked to assess the whole Collatz
program.  The narrow mathematical question is enough.

Useful expertise:

- finite-rank approximation schemes for transfer/Koopman operators;
- open/killed systems;
- symbolic Banach spaces and weak operator norms;
- Keller-Liverani-type mixed norm perturbation theory;
- countable Markov or non-archimedean symbolic systems if the finite
  quotient is not compact.

## 7. Failure Modes

`A0-averaged` fails if:

- no natural infinite source operator `U_s` can be defined;
- the averaging measure is arbitrary or changes the dynamics rather
  than approximating it;
- weak convergence of `K_N^0` depends on enumeration artifacts;
- `P_N^0` stops decreasing in the chosen weak norm;
- tail/killing terms cannot be controlled in the same norm;
- no credible Banach bridge exists from finite averaged rows to
  `B_s -> B_w`;
- a collaborator judges the averaged quotient too artificial for the
  intended analytic framework.

If these failures persist, the correct output is the finite-rank
computational note, not a spectral program.

## 8. Practical Rule

From now on, when discussing the existing `FULL` matrices:

```text
Say: averaged PhaseState finite-rank quotient.
Do not say: exact projection of the source-cell kernel.
```

This rule is the main reduction achieved by the current Phase-10 pass.
