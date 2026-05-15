# Phase 10 Reduced Core

Date: 2026-05-14

Status: reduced working core after the Phase-10 snapshot.  This note is
the preferred short entry point.  It deliberately suppresses most
diagnostic detail and keeps only the objects needed to decide whether
Gate 10.B can be made mathematical.

## 1. Non-Claims

Gate 10.B is open.

Nothing below proves:

- Conjecture 6;
- an infinite-dimensional spectral gap;
- a Lasota-Yorke inequality;
- Hennion or Keller-Liverani hypotheses;
- that the existing finite `FULL` matrices are projections of a natural
  infinite operator.

The current achievement is narrower: the finite obstruction has been
reduced to a small number of named approximation errors.

## 2. The Essential Finite Object

The diagnostic source space is a finite set of retained cells

```text
S_N = { retained source cells i = (T,r,h) at prefix length N }.
```

For each source cell `i`, the empirical weighted row is

```text
k_N^{cell}(i,q)
  = average over 0 <= j < N of
      1_return(t_j,h) 2^{-delta(t_j,h)}
      1_{destination phase = q},
```

where terminal/killed mass is lost and large-`delta` tails may be
handled by an explicit truncation error.  This is a finite row kernel

```text
k_N^{cell}: S_N -> PhaseState.
```

This cell-level object is the honest finite source kernel.  The existing
Lean `TransferMatrix V` objects are not indexed by `S_N`; they are
indexed by `PhaseState V`.

## 3. Two Branches

There are only two analytic branches worth keeping active now.

### A0: Existing `FULL` Branch

Source quotient:

```text
rho_0(i) = source PhaseState of cell i.
```

Quotient row:

```text
K_N^0(a,q)
  = average_{rho_0(i)=a} k_N^{cell}(i,q).
```

This is the branch compatible with current Lean `TransferMatrix V`
objects.

Cost: the measured source-collapse error is large at current scales:

```text
C_128^0 ~= 0.051512269, p95 ~= 0.27979821.
```

Benefit: phase-prefix drift is small and decreasing on tested prefixes:

```text
P_16^0  ~= 0.006631064,
P_32^0  ~= 0.005546595,
P_64^0  ~= 0.004502430.
```

Verdict: `A0` is the main branch, but only as an averaged-quotient
program.  The active interpretation is `A0-averaged`: `K_N^0` is an
averaged finite-rank quotient, not an exact projection, unless a future
lemma proves `C_N^0 -> 0`.

### A1: Refined Low-Residue Branch

Source quotient:

```text
rho_10(i) = (source PhaseState of i, r(i) mod 2^10).
```

Benefit: source-collapse error is much smaller:

```text
C_128^{10} ~= 0.020415877.
```

Cost: prefix drift is larger:

```text
P_64^{10} ~= 0.001584947
```

for the rectangular `A_10 -> PhaseState` diagnostic.  The square refined
smoke kernel

```text
(PhaseState, t mod 2^10) -> (PhaseState, next_t mod 2^10)
```

has decreasing but much larger drift:

```text
0.015208335 -> 0.013556191 -> 0.012909874.
```

Verdict: `A1` is a secondary research branch.  It is not the main story
for the existing `FULL` matrices unless a new square refined operator
and norm make the larger drift acceptable.

## 4. The Three Errors

For a source quotient `rho_b:S_N -> A_b`, define:

```text
K_N^b(a,q)
  = average_{rho_b(i)=a} k_N^{cell}(i,q).
```

The finite-to-infinite question reduces to three errors.

Source-collapse error:

```text
C_N^b
  = sum_i omega_N(i)
      || k_N^{cell}(i,.) - K_N^b(rho_b(i),.) ||_1.
```

Prefix drift:

```text
P_N^b
  = sum_a m_N^b(a)
      || K_{2N}^b(a,.) - K_N^b(a,.) ||_1.
```

Tail/killing error:

```text
T_{N,L}^b
  = contribution of terminal mass, excluded source cells,
    and retained returns with delta > L.
```

Gate 10.B is not a spectral question until these errors are placed in a
declared weak operator norm.

## 4.1 Banach-Pair Reduction After Martingale Diagnostics

The serious candidate pair is now:

```text
B_w = L1(mu),
B_s = L_infty + weighted martingale variation on Haar cylinders.
```

Compactness `B_s -> B_w` follows formally from martingale truncation:

```text
||f - E_N f||_1 <= a_{N+1}^{-1} Var_a(f).
```

The issue is not compactness.  The issue is whether the retained
operator satisfies a Lasota-Yorke inequality:

```text
Var_a(U_ret,s f) <= alpha Var_a(f) + C ||f||_1,
alpha < 1.
```

The first child-cylinder martingale proxy is cautionary.  The observed
phase increments are large and nearly flat, while full/delta increments
increase on the available depths.  Therefore the only reduced analytic
target worth keeping is:

```text
phase martingale variation
+ structured label-excess correction
+ weak substochastic loss/status control.
```

This is stricter than the earlier `C_N/P_N/T_N` bookkeeping.  It says
that `P_N` must be decomposed by mechanism, not just made numerically
small in aggregate.  If the phase martingale increment does not decay at
larger genuine 2-adic depths, the Banach-pair route should remain
paused even though the finite-rank branch remains valid.

The latest phase-obstruction check strengthens this warning.  The phase
term is not currently concentrated in a small exceptional set: the best
single structural contributors have mass about `1/2`, contribution
about `0.67--0.69`, and leave complement means around `0.026--0.028`.
Thus a small finite-rank bad-component correction may help label-excess,
but it does not solve the phase martingale obstruction.

The current possible repair is different: split off a finite low
destination mode.  The `dst_v2` projection captures about `0.88--0.93`
of the phase child-TV on the tested `T15` windows, and the residual mean
drops from about `0.00499` to `0.00254` over depths `0..4`.  The reduced
candidate is therefore:

```text
U = U Pi_v2 + U Q_v2              (observable/Koopman side),
U Pi_v2 = finite/low-mode part,
U Q_v2  = residual to test with martingale LY.
```

This is only a diagnostic repair route.  It is not a theorem until
`Pi_v2` is defined canonically for the operator and the residual is
bounded in the chosen mixed norm.

The first explicit-lift test is negative for the simplest canonical
versions.  The pair-dependent pooled lift gives a small residual, but a
single global lift is essentially as large as the original phase
variation, and a finite `source PhaseState`-conditioned lift remains
around `0.016--0.020` on `T15_d2_tail3`.  Thus the low-mode repair is
not yet a valid LY framework; it needs a richer source-refined lift or a
new quotient.

## 5. Minimal Conditional Theorem

A mathematically honest positive `A0` statement would have the form:

```text
Assume there exist Banach spaces B_s,B_w, maps E_N,I_N,
and a weighted killed operator U_s such that:

1. K_N^0 is the finite quotient of U_s up to source-collapse error C_N^0;
2. C_N^0 -> 0, or the averaged quotient is proved to be the intended
   finite-rank approximation;
3. P_N^0 -> 0 in the finite weak norm;
4. T_{N,L}^0 can be made small in the same norm;
5. E_N and I_N transfer finite weak bounds to B_s -> B_w bounds.

Then K_N^0 is a legitimate weak finite-rank approximation to U_s.
```

This conclusion is still not a spectral gap.  Hennion/Keller-Liverani
would require additional compactness, boundedness, and resolvent
hypotheses.

## 6. Kill Criteria

Stop the analytic branch and write the finite-rank note if any of these
becomes structural:

- no natural infinite `U_s` can be defined;
- `C_N^0` does not decay and cannot be justified as intended averaging;
- `P_N^0` stops decreasing in the declared weak norm;
- tail/killing error cannot be controlled except by ad hoc exclusions;
- `A1` remains too noisy and no norm explains the larger drift;
- no collaborator validation is being pursued and no internal proof
  supplies a credible Banach-space bridge.

This is not project failure.  It means the rigorous deliverable is the
finite-rank theorem/certificate branch.

## 7. Immediate Next Actions

1. Do not add new diagnostics unless they feed `C_N`, `P_N`, or `T_N`.
2. Use `phase10_A0_theorem_skeleton.md` as the formal `A0`
   proposition skeleton.
3. Use `phase10_A0_averaged_interpretation.md` as the active
   interpretation of existing `FULL` matrices.
4. Move `A1` to appendix/secondary status until a refined square norm is
   justified.
5. Under the no-collaborator route, keep the finite-rank note as the
   active rigorous deliverable, but test the narrow
   `A0_HaarConditionalClosure` bridge in
   `phase10_gate10B_conditional_closure.md`.

The archived collaborator question remains:

```text
Can the A0 averaged quotient be realized as a weak finite-rank
approximation of a natural killed transfer/Koopman operator?
```

Everything else is secondary.
