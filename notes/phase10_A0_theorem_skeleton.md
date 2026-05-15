# Phase 10 A0 Theorem Skeleton

Date: 2026-05-15

Status: formal skeleton only.  This note does not prove Gate 10.B,
Conjecture 6, a spectral gap, or a Lasota-Yorke inequality.  Its purpose
is to state the minimal theorem that would make the existing
`PhaseState` / `FULL` branch mathematically legitimate.

## 1. Scope

Branch `A0` is the branch tied to the existing finite matrix type:

```text
TransferMatrix V = Matrix (PhaseState V) (PhaseState V) NNReal.
```

Therefore `A0` is phase-only.  Return labels such as `delta` may be used
as proof data and error-control data, but they are not part of the
finite state space unless a new labelled operator is explicitly built.

The central question is not whether the finite diagnostics look good.
The central question is whether the averaged `PhaseState` quotient can
be interpreted as a controlled finite-rank approximation of a natural
killed weighted operator.

## 2. Finite Definitions

Fix a prefix length `N`, a phase level `(T,a)` or equivalent finite
phase convention, and a retained finite source-cell set

```text
S_N = { i = (T,r,h) : i is retained }.
```

Let

```text
Q = PhaseState.
```

Let `omega_N` be the finite source-cell probability measure.  In the
current diagnostics it is the normalized counting measure over retained
cells, unless a later convention states otherwise.

For each source cell `i in S_N`, define the empirical cell row

```text
k_N^{cell}(i,q)
  = (1 / sample_N(i))
      sum_{j in prefix window for i}
        1_return(i,j)
        2^{-delta(i,j)}
        1_{pi(tau(i,j)) = q}.
```

Terminal/killed observations contribute no return row mass.  Excluded
cells and large-`delta` truncations are not hidden in this definition;
they belong to explicit error terms below.

Define the source phase quotient

```text
rho_0:S_N -> Q.
```

Define the averaged phase quotient kernel

```text
K_N^0(a,q)
  = average_{i in S_N : rho_0(i)=a} k_N^{cell}(i,q),
```

with the averaging measure stated explicitly.  Under the current
diagnostics this is uniform over retained source cells in the fiber.

This is the finite object that can be compared to a `PhaseState`
transfer matrix.  It is not automatically an exact projection of
`k_N^{cell}`.

## 3. Error Terms

The `A0` theorem must carry three finite errors.

Source-collapse error:

```text
C_N^0
  = sum_{i in S_N} omega_N(i)
      sum_{q in Q}
        | k_N^{cell}(i,q) - K_N^0(rho_0(i),q) |.
```

Prefix drift:

```text
P_N^0
  = sum_{a in Q} m_N(a)
      sum_{q in Q}
        | K_{2N}^0(a,q) - K_N^0(a,q) |,
```

where `m_N = (rho_0)_* omega_N`, or another explicitly declared
source-phase measure.

Tail/killing error:

```text
T_{N,L}^0
  = excluded-cell error
    + terminal/killed loss handled outside the substochastic row
    + retained weighted mass with delta > L.
```

These errors must not be combined informally.  In particular, small
`P_N^0` does not compensate for uncontrolled `C_N^0` unless the chosen
weak norm explicitly permits that compensation.

## 4. Candidate Infinite Operator

The desired infinite-side object is a killed weighted forward operator
on observables:

```text
(U_s f)(x)
  = 1_D(x) 2^{-s delta(x)} f(pi(tau x)).
```

Here:

- `X` is the source phase space;
- `D subset X` is the nonterminal first-return domain;
- `tau:D -> X` is the first-return map;
- `delta:D -> N` is the return weight exponent;
- `pi:X -> Q` or `pi_{T,a}:X -> Q` is the finite phase observation;
- killed/terminal points contribute lost mass.

This formula is only a candidate until `X,D,tau,delta,pi` are defined
without finite-prefix artifacts.

## 5. A0 Conditional Proposition

### Proposition A0

Assume the following data and hypotheses.

H1. Infinite model.  There exist a measurable/topological source space
`X`, a reference measure or averaging scheme `omega`, a killed return
domain `D`, a first-return map `tau`, a weight exponent `delta`, and
finite phase observations `pi_N:X -> Q`.

H2. Finite cells.  The retained finite sets `S_N` are measurable
source-cell models for the chosen finite observations, with explicit
excluded-cell error `e_N`.

H3. Cell-kernel identification.  The empirical rows `k_N^{cell}` are
finite averages of

```text
1_D(x) 2^{-s delta(x)} 1_{pi_N(tau x)=q}
```

over the cells in `S_N`, up to an explicitly bounded finite sampling or
enumeration residual.

H4. Averaged quotient convention.  Either:

```text
C_N^0 -> 0
```

in the declared weak source norm, or the averaged quotient `K_N^0` is
proved to be the intended finite-rank approximation scheme rather than
an exact projection.

H5. Prefix convergence.  The averaged phase kernels satisfy

```text
P_N^0 -> 0
```

in the declared finite weak norm.

H6. Tail/killing control.  For every tolerance `eta > 0`, one can choose
`L` and then `N` so that `T_{N,L}^0 <= eta` in the same weak norm.

H7. Banach bridge.  There exist Banach spaces `B_s,B_w` and maps

```text
E_N:B_s -> functions on Q,
I_N:functions on Q -> B_w
```

or equivalent projection/inclusion maps, with constants independent of
`N`, such that finite weak `L1(m_N)` bounds imply `B_s -> B_w` operator
bounds.

Then the phase kernels `K_N^0` are legitimate weak finite-rank
approximants of the killed weighted operator `U_s`:

```text
|| I_N K_N^0 E_N - U_s ||_{B_s -> B_w}
  <= controlled expression involving C_N^0 + P_N^0 + T_{N,L}^0 + e_N,
```

with the right-hand side tending to zero in the declared order of
limits.

### What This Proposition Would Not Give

Even if Proposition A0 were proved, it would not by itself give:

- a spectral gap;
- quasi-compactness;
- an essential spectral-radius bound;
- Keller-Liverani stability;
- a Collatz theorem.

Those require separate Lasota-Yorke/Hennion/Keller-Liverani hypotheses.

## 6. Minimal Proof Skeleton

Step 1. Prove the finite row identity for `k_N^{cell}` from the trace
definition.  This is mostly bookkeeping and is already CSV-verified in
the current diagnostics, but not yet a generated Lean statement for the
new `T=15` prefix kernels.

Step 2. Decompose the finite error:

```text
k_N^{cell} - K_N^0 rho_0        source-collapse error C_N^0,
K_N^0 - K_{2N}^0                prefix error P_N^0,
full kernel - truncated kernel  tail/killing error T_{N,L}^0.
```

Step 3. Prove that each finite error is controlled in the same weak
norm.  No cross-norm substitution is allowed without a lemma.

Step 4. Use `E_N,I_N` to transfer the finite weak estimate to
`B_s -> B_w`.

Step 5. Stop.  Do not infer spectral consequences until a separate
compactness/quasi-compactness argument is supplied.

## 7. Current Evidence and Obstruction

Finite evidence for `P_N^0` is favorable:

```text
16->32:  0.006631064,
32->64:  0.005546595,
64->128: 0.004502430.
```

But the source-collapse obstruction is currently larger:

```text
C_128^0 ~= 0.051512269,
p95      ~= 0.27979821.
```

Therefore the next proof decision is:

```text
Either prove/argue C_N^0 -> 0,
or explicitly formulate A0 as an averaged finite-rank approximation.
```

The second option may be the more honest one unless new structure is
found.

## 8. Missing Lemmas

M1. Infinite model lemma: define `X,D,tau,delta,pi_N` without finite
prefix artifacts.

M2. Cell identification lemma: show that retained cells are measurable
finite observations of the infinite model.

M3. Source averaging lemma: identify `omega_N` and its possible limit or
justify it as a finite-rank averaging convention.

M4. Collapse lemma: prove `C_N^0 -> 0`, or replace it with an averaged
quotient axiom.

M5. Prefix-Cauchy lemma: prove `P_N^0 -> 0` in the chosen weak norm.

M6. Tail lemma: control terminal/excluded/large-`delta` contributions.

M7. Banach bridge lemma: prove bounded projection/inclusion constants
for the chosen `B_s,B_w`.

M8. Optional spectral lemmas: only after M1-M7, formulate
Lasota-Yorke, Hennion, or Keller-Liverani hypotheses.

## 9. Recommended Next Move

Do not add a new diagnostic yet.  Choose between two precise `A0`
interpretations:

```text
A0-decay:
  try to prove C_N^0 -> 0.

A0-averaged:
  declare K_N^0 to be an averaged finite-rank approximation and ask
  whether such approximations can converge weakly to U_s.
```

This is the question to send to a collaborator.
