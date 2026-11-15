# Phase 10.B Conditional Closure Attempt

Date: 2026-05-15

Status: conditional candidate for Gate 10.B, corrected 2026-11-13. The
historical claim of conditional closure below is superseded where it
identifies point samples of merely measurable observables with Haar
integrals. A genuine sampling/identification hypothesis is still open.
This is not a spectral theorem or an exact projection theorem. See the
[November correction and branch-clock lemma](research_sprint_2026-11-13/agents/S11_KERNEL_IT.md).

## 1. Verdict

Gate 10.B should not be closed as:

```text
FULL_{T,j} is an exact finite projection of an infinite transfer
operator.
```

That statement remains unsupported and is probably the wrong target for
the existing `PhaseState` matrices.

There is, however, a plausible conditional closure:

```text
The A0 phase matrices are finite cylinder conditional expectations of a
killed weighted forward kernel on X = Z_2 x H, where H is the finite
hit/height coordinate used by PhaseState.
```

In this interpretation, `FULL_{T,j}` is not an exact projection.  It is
an empirical or generated finite high-bit approximation to a conditional
expectation kernel.  The natural measure is Haar measure on `Z_2` times
counting measure on `H`.

## 2. Infinite Source Model

Fix:

```text
V       = v2 cap used by PhaseState,
H       = Fin 4, or the finite h-coordinate used in the current matrix,
X       = Z_2 x H,
mu      = Haar_Z2 x uniform_H.
```

Let

```text
D subset X
```

be the nonterminal first-return domain, let

```text
tau : D -> X
```

be the first-return/next-source map, and let

```text
delta : D -> N
```

be the return exponent used in the weight `2^{-s delta}`.

Let the finite phase observation be

```text
pi_V : X -> PhaseState V,
pi_V(x,h) = (min(v2(x),V), odd_part(x) mod 4, h mod 4),
```

with the usual convention that the point `x = 0` is null for Haar
measure.  This convention matters only on a measure-zero set in the
infinite model, but it creates finite boundary/mixed cells in low-bit
approximations.

Important: `odd_part(x)` means division by the true `2`-adic valuation,
not division by the capped valuation.  Hence the capped phase atom
`min(v2,V)=V` still contains infinitely many true valuation levels.
Low-bit cells approximate this atom with a high-valuation boundary
error; they do not make it exactly finite at fixed `T`.

For `s >= 0`, define the killed weighted forward observable operator
against phase observables:

```text
(U_s f)(x,h)
  = 1_D(x,h) 2^{-s delta(x,h)} f(pi_V(tau(x,h))).
```

Here `f` is a bounded function on `PhaseState V`.  This is a
Koopman/forward-kernel orientation, not a Ruelle preimage operator.

## 3. Canonical Conditional Expectation Kernel

For each source phase `a in PhaseState V`, define the phase atom

```text
A_a = { (x,h) in X : pi_V(x,h) = a }.
```

Whenever `mu(A_a) > 0`, define the ideal A0 averaged kernel by

```text
K_s^A0(a,q)
  = mu(A_a)^(-1) integral_{A_a cap D}
      2^{-s delta(x,h)} 1_{pi_V(tau(x,h)) = q} dmu(x,h).
```

This is the canonical version of the existing averaged quotient.  It is
not cellwise deterministic and it does not require that all source cells
inside `A_a` have the same row.

Equivalently:

```text
K_s^A0 = E_mu[ U_s 1_q | sigma(pi_V) ].
```

Thus the correct mathematical object behind `A0-averaged` is a
conditional expectation of a killed weighted forward kernel.

## 4. Finite Cylinder Approximation

For integers `T,m >= 0`, let `N = 2^m`.  For a low-bit residue `r mod
2^T` and `h in H`, define the finite cylinder sample:

```text
C_{T,r,h,m}
  = { (x,h) : x == r + j 2^T mod 2^{T+m}, 0 <= j < 2^m }.
```

Equivalently, the script samples

```text
t = r + j 2^T, 0 <= j < 2^m.
```

For prefix windows with `j_count = 2^m`, these residue labels represent
the equal-mass finite quotient of Haar measure on the cylinder
`x == r mod 2^T`. Evaluating a function at the natural representative
of each residue is its Haar integral only when an appropriate
cylindricity or quadrature statement has been proved. Bounded
measurability alone does not supply that statement.

The finite source-cell row is:

```text
k_{T,m}^{cell}(r,h;q)
  = 2^{-m} sum_{0 <= j < 2^m}
      1_D(t_j,h) 2^{-s delta(t_j,h)}
      1_{pi_V(tau(t_j,h)) = q}.
```

The A0 finite quotient is the conditional average over all retained
cells whose source phase is `a`:

```text
K_{T,m}^{A0}(a,q)
  = average_{(r,h): pi_V is constant a on the retained low-bit cell}
      k_{T,m}^{cell}(r,h;q).
```

Because the retained low-bit cells have equal `mu`-mass, this is the
finite conditional average of the sampled rows. To identify it with
the killed observable's Haar conditional expectation, one must prove
the additional sampling hypothesis in Section 8; finite regrouping
alone does not do so.

## 5. Boundary and Mixed-Cell Residual

The finite low-bit cells are not always source-phase atoms.  The current
diagnostics identify the only mixed source cells at `T = 15`,
`h mod 4`:

```text
r = 0,
r = 2^14,
h = 0,1,2,3.
```

Thus:

```text
full cells     = 131072,
retained cells = 131064,
excluded       = 8,
excluded mass  = 8/131072 = 0.00006103515625.
```

For any bounded row diagnostic `F`,

```text
| mean_complete(F) - mean_retained(F) |
  <= 2 * excluded_mass * ||F||_infty
  = 0.0001220703125 * ||F||_infty.
```

This is a genuine finite bookkeeping lemma.  In the infinite Haar model
the corresponding ambiguous boundary is a shrinking high-valuation
residue set, and its mass is `O(2^{-T})` for fixed phase cap.

More generally, for fixed `V`, low-bit cells with valuation below
`T-1` determine both `v2` and `odd_part mod 4`; the unresolved capped
tail sits in high-valuation cells of total Haar mass `O(2^{-T})`.
This is the analytic reason the mixed-cell correction is not merely a
script artifact.

## 6. What Script 107 Already Closes Finite-Exactly

For the current `T=15` prefix reports, script
`107_gate10b_closure_checks.py` verifies:

```text
max full-count residual       = 0,
windows with count residual   = 0,
max full-weight residual      = 0,
windows with weight residual  = 0,
max terminal residual         = 0.
```

Therefore the CSV full-signature rows exactly define the empirical
finite row-source prefix kernel used by the diagnostics.

For prefix windows, the finite phase drift decreases:

```text
16 -> 32: phase mean = 0.0066438334,
32 -> 64: phase mean = 0.0055544859,
64 ->128: phase mean = 0.0045024297.
```

The `64 -> 128`, `delta <= 5` run gives:

```text
tail-diff mean = 8.9701734e-06,
tail-a mean    = 2.5428943e-05,
tail-b mean    = 2.5392998e-05.
```

These are finite evidence for prefix/Haar stability and small retained
tail effect.  They are not convergence theorems.

## 7. The Remaining Obstruction

The phase collapse error remains large:

```text
j=128:
collapse mean = 0.051512269,
p95           = 0.27979821,
p99           = 0.56114054,
max           = 1.0905151.
```

This does not kill the conditional-expectation interpretation.  In fact
conditional expectation allows variation inside a phase atom.  But it
does kill any interpretation where `PhaseState` is treated as a
sourcewise sufficient statistic or exact projection.

Thus the gate can only close in the following weak sense:

```text
A0 is the conditional expectation of the source-cell kernel onto the
sigma-algebra generated by PhaseState.
```

It cannot close as:

```text
source-cell rows are approximately constant on PhaseState fibers.
```

## 8. Conditional Gate 10.B Theorem

The theorem to aim for is:

```text
Theorem A0_HaarConditionalClosure.

Assume:

H0. The low-bit depth `T` is taken large relative to the phase cap `V`,
    and the unresolved capped high-valuation tail is either retained as
    a named residual or shown to have `O(2^{-T})` measure.

H1. The killed return map tau, domain D, and delta are measurable on
    X = Z_2 x H.

H2. For each phase q, the observable

      g_q(x,h)
        = 1_D(x,h) 2^{-s delta(x,h)}
          1_{pi_V(tau(x,h)) = q}

    is bounded and mu-measurable.

H3. The finite script/generator rows either are genuine integrals of g_q
    on the fine cylinders, or are averages of a cylinder-step observable
    g_{q,T,m} with a proved L1 approximation error
    ||g_{q,T,m}-g_q||_1 <= epsilon_{T,m} -> 0 for fixed T.
    Point values at natural representatives do not establish H3.

H4. The finite high-bit prefix windows are powers of two, N = 2^m.
    This makes the quotient cell weights equal; it does not replace H3.

H5. Boundary/mixed source cells have mu-mass tending to zero in the
    declared order of limits.

Then K_{T,m}^{A0} is the finite conditional expectation of the killed
weighted kernel onto sigma(pi_V), up to the explicit residual, and
K_{T,m}^{A0}(a,q) converges in finite-dimensional weak L1 to
the `T`-level conditional expectation as m -> infinity.  If the
boundary residual tends to zero as T -> infinity, the `T`-level
conditional expectations converge to K_s^A0(a,q) in the declared weak
finite-dimensional sense.
```

This would close only an operator-existence and finite approximation
statement after H3 and the other project-specific hypotheses are proved.
They are not proved here. It does not imply compactness, a
Lasota-Yorke inequality, Hennion, Keller-Liverani, or a spectral gap.

## 8.1 Corrected Conditional Proposition Form

The following is a conditional target. In particular, condition B is a
substantive sampling hypothesis, not a consequence of condition A.

```text
Proposition (A0 Haar conditional closure).

Fix a valuation cap V and a finite hit-coordinate set H.  Let

  X = Z_2 x H

with product measure mu = Haar_Z2 x uniform_H.  Let pi_V:X -> Q_V be
the PhaseState observation

  pi_V(x,h) = (min(v2(x),V), odd_part(x) mod 4, h mod 4),

where the point x=0 is assigned an arbitrary value.  Let D subset X be
a measurable killed return domain, tau:D -> X a measurable return map,
and delta:D -> N a measurable return exponent.  For s >= 0 and
q in Q_V define

  g_q(x,h)
    = 1_D(x,h) 2^{-s delta(x,h)}
      1_{pi_V(tau(x,h)) = q}.

Assume:

  (A) g_q is bounded and measurable for every q.

  (B) For every finite low-bit depth T and high-bit prefix depth m,
      form the cylinder-step observable g_{q,T,m} whose values on the
      fine cylinders are the generated sampled rows at

        t = r + j 2^T, 0 <= j < 2^m,

      outside a declared exceptional set E_T. Prove, independently,

        ||g_{q,T,m}-g_q||_{L1(mu)} <= epsilon_{T,m},
        epsilon_{T,m} -> 0 as m -> infinity for fixed T.

      Alternatively, prove that the generated fine-cell values are the
      genuine conditional integrals of g_q. Mere measurability and
      uniform weights on residue labels imply neither alternative.

  (C) The exceptional cells satisfy mu(E_T) -> 0 as T -> infinity, and
      the finite retained/complete averaging error is bounded by

        2 mu(E_T) ||g_q||_infty.

  (D) The high-bit windows are prefix windows of length 2^m, not
      arbitrary adjacent integer intervals.

Then the finite A0 matrix K_{T,m}^{A0}, obtained by averaging retained
source-cell rows over PhaseState fibers, is the conditional expectation
of the reconstructed finite cylinder kernel, up to the exceptional
error in (C). Conditional expectation is an L1 contraction, so its
sampling error is at most epsilon_{T,m}, in addition to that residual.
After the phase-identification and exceptional-cell errors also tend
to zero in the declared order, the limiting A0 kernel is

  K_s^{A0}(a,q)
    = E_mu[g_q | pi_V = a]

for every positive-measure phase atom a.
```

Proof sketch:

```text
1. Haar/cylinder identity:
   the residue labels have equal quotient masses. The average of a
   fine-cylinder-step function is its Haar average; this says nothing
   about point evaluation of an arbitrary measurable function.

2. Finite conditional expectation:
   grouping equal-mass retained low-bit cells by pi_V is exactly
   conditioning the finite quotient measure on the finite sigma-algebra
   generated by pi_V, after removing E_T.

3. Exceptional correction:
   for bounded rows, replacing the complete cell set by the retained
   cell set changes source averages by at most
   2 mu(E_T) ||g_q||_infty.

4. Sampling convergence:
   use the proved L1 error in B and contraction under conditional
   expectation. For genuine conditional integrals the tower property
   already gives the correct parent-cylinder average at every m.

5. Phase quotient:
   conditioning further on sigma(pi_V) gives K_s^{A0}.  This is an
   averaged quotient, not a statement that source rows are constant on
   PhaseState fibers.
```

Proof obligations not yet discharged:

| ID | obligation | status |
|---|---|---|
| P1 | define `D`, `tau`, and `delta` on `Z_2 x H` independently of finite scripts | open |
| P2 | prove measurability and boundedness of `g_q` | open |
| P3 | identify point-sampled rows with Haar averages | open; Section 8.2 proves only the cylinder-step identity |
| P4 | prove the exceptional mass bound for capped valuation/odd-part boundary cells | proof sketch written in Section 8.2; exact normalization fixed |
| P5 | prove generated rows equal the declared finite samples and identify their reconstruction | finite provenance checks pass for two artifacts; the limiting observable and sampling error remain separate |
| P6 | prove convergence in the declared weak norm | conditional-expectation contraction is available; the required sampling hypothesis B remains open |

This is a candidate with explicit open obligations. It does not establish
the sampling premise, close Gate 10.B, or state a spectral theorem.

## 8.2 P3/P4 Local Proof Details

### P3: Haar/cylinder identity

Let `T,m >= 0` and fix `r mod 2^T`.  The residue classes

```text
r + j 2^T mod 2^{T+m},    0 <= j < 2^m,
```

are exactly the `2^m` residue classes modulo `2^{T+m}` contained in the
2-adic cylinder

```text
C_{T,r} = r + 2^T Z_2.
```

Each subcylinder has Haar measure `2^{-(T+m)}` and the parent cylinder
has Haar measure `2^{-T}`.  Therefore the conditional Haar measure on
`C_{T,r}` assigns mass

```text
2^{-(T+m)} / 2^{-T} = 2^{-m}
```

to each subcylinder.  Consequently, for any function `g` that is
constant on residue classes modulo `2^{T+m}`,

```text
E[g | C_{T,r}]
  = 2^{-m} sum_{0 <= j < 2^m} g(r + j 2^T).
```

This proves the identity for functions constant on the fine cylinders.
It does not prove it for arbitrary bounded measurable observables sampled
at the representatives. The function `g=1_(Z_2\N)` is a counterexample:
the embedded naturals form a countable Haar-null set, so g has Haar
integral 1 while every sample at a natural representative is zero.
The same discrepancy occurs in every positive-measure cylinder.

### P4: capped-valuation boundary mass

For the phase observation

```text
pi_V(x,h) = (min(v2(x),V), odd_part(x) mod 4, h mod 4),
```

low-bit residues modulo `2^T` determine the true pair

```text
(v2(x), odd_part(x) mod 4)
```

whenever `v2(x) <= T-2`.  Indeed, if `x = 2^k u` with `u` odd and
`k <= T-2`, then `x mod 2^T` determines `k` and determines
`u mod 4`.

The unresolved part is contained in

```text
{ x in Z_2 : v2(x) >= T-1 } = 2^{T-1} Z_2,
```

which has Haar measure

```text
2^{-(T-1)}.
```

After crossing with finite `H`, the product measure is unchanged if
`H` is normalized counting measure.  Therefore the total mass of
low-bit cells whose phase may be ambiguous because of capped valuation
or odd-part boundary effects is bounded by

```text
mu(E_T) <= 2^{-(T-1)}.
```

For `T = 15`, this gives the crude bound:

```text
2^{-14} = 0.00006103515625.
```

This matches the observed script-107 excluded mass:

```text
8 / 131072 = 0.00006103515625.
```

Thus the current finite mixed-cell correction is exactly the expected
high-valuation boundary mass for `T=15`.

The retained-vs-complete averaging estimate follows from a general
bounded-function lemma.  If `A` is the retained set, `E` the exceptional
set, `mu(E) = e`, `mu(A) = 1 - e`, and `|F| <= M`, then

```text
| mean_A(F) - mean_{A union E}(F) | <= 2 e M.
```

Indeed, writing `a = integral_A F` and `b = integral_E F`,

```text
mean_A(F) - mean_{A union E}(F)
  = a/(1-e) - (a+b)
  = e a/(1-e) - b,
```

and `|a| <= (1-e)M`, `|b| <= eM`.

P3 is closed only for cylinder-step functions; its application to the
generated limiting observable remains open. P4 has a paper proof sketch
and still needs either a formal Lean lemma or a clean prose lemma with
the exact normalization convention.

## 8.3 P6 Martingale/Weak-Norm Closure

The weak norm naturally attached to the A0 closure is not a Holder or
BV norm.  It is the finite-dimensional source-averaged norm induced by
`mu`:

```text
||R||_{w,T}
  = sum_{a in PhaseState V} mu(A_a)
      sum_{q in PhaseState V} |R(a,q)|.
```

Equivalently, if `R` is represented on retained low-bit cells before
phase averaging:

```text
||R||_{cell,w,T}
  = integral_X sum_q |R(C_T(x),q)| dmu(x),
```

with the exceptional set removed and then reinserted by the `2eM`
bound from P4.

For each destination phase `q`, let

```text
g_q(x,h)
  = 1_D(x,h) 2^{-s delta(x,h)}
    1_{pi_V(tau(x,h)) = q}.
```

Since `0 <= g_q <= 1` for `s >= 0`, `g_q in L1(mu)`.  Let
`F_{T,m}` be the finite sigma-algebra generated by residues modulo
`2^{T+m}` and the coordinate `h`.  Then

```text
E[g_q | F_{T,m}]
```

is a bounded martingale in `m`, and the martingale convergence theorem
gives

```text
E[g_q | F_{T,m}] -> E[g_q | F_{T,infty}]
```

in `L1(mu)`, where `F_{T,infty}` is the sigma-algebra generated by the
full high-bit refinement inside the fixed low-bit cylinders.

The script averages over prefix windows:

```text
t = r + j 2^T, 0 <= j < 2^m.
```

These point evaluations cannot be identified with conditional integrals
using bounded measurability alone. If the fine-cell rows are genuine
conditional integrals, the tower property gives
`E[E[g_q|F_{T,m}]|F_T]=E[g_q|F_T]` already for every m. Otherwise define
the sampled cylinder-step reconstruction g_{q,T,m} and prove the L1
approximation in condition B. Its conditional average then differs from
the true one by at most that L1 error. The martingale theorem for actual
conditional integrals does not prove this sampling error bound.

Under the added sampling hypothesis, grouping by `PhaseState` is an L1
contraction. Hence the A0 averaged phase kernels satisfy the corresponding
conditional convergence bound:

```text
|| K_{T,m}^{A0} - K_{T,infty}^{A0} ||_{w,T} -> 0
```

for fixed `T,V`, modulo the explicit exceptional-cell residual.  If the
P4 residual tends to zero as `T -> infinity`, then the `T`-level kernels
converge to the ideal conditional kernel `K_s^A0` in the declared weak
finite-dimensional sense.

This is the correct Keller-Liverani-adjacent mixed norm target:

```text
strong side: bounded phase observables, ||f||_infty;
weak side: source-averaged L1(mu) error after conditional expectation.
```

It is not a Lasota-Yorke inequality.  It gives only the weak
finite-rank approximation layer needed to make Gate 10.B meaningful.

P6 is therefore conditional on the project-specific sampling and phase
identifications. A martingale citation alone does not close it. A
cylinder approximation with controlled L1 error, a proved quadrature
estimate, or genuine conditional-integral rows would supply the missing
bridge. No such theorem for the full A0 kernel is proved here.

## 8.4 P1/P2 Intrinsic Dynamics Obstruction

The remaining hard point is not the phase averaging.  It is the
definition of the killed return map itself.

The scripts define return/terminal behavior for natural representatives
`n0` by iterating the odd Syracuse map until one of the following
events occurs:

```text
1. the orbit returns to the monitored target phantom state;
2. the orbit hits a different monitored phantom state;
3. the odd Syracuse value drops below n0;
4. the step budget is reached.
```

Events 1 and 2 are essentially 2-adic/cylindrical: they can be described
using congruence tubes around phantom representatives and finite
phantom records.

Event 3 is not 2-adic.  The comparison

```text
S^k(n0) < n0
```

uses the ordinary order on positive integers.  There is no continuous or
canonical analogue of this inequality on `Z_2`.  Therefore a killed
operator on `Z_2 x H` cannot literally reproduce the script's terminal
rule unless we add extra structure.

There are three possible resolutions.

### P1-A: return-only 2-adic kernel

Define `D` as the set of points whose first hit among the monitored
2-adic phantom tubes is the target return tube, before any other
monitored tube.  Define `tau` by that first return and define `delta`
from the returned local coordinate.

This is the cleanest `Z_2` operator.  But it no longer includes the
archimedean "drop below start" killing rule.  The difference between the
script kernel and this 2-adic kernel must be carried as a terminal/error
term.

Verdict: mathematically clean, but it changes the finite model unless
the drop-below mass is separately controlled.

### P1-B: arithmetic lift space

Enlarge the source space to remember the natural representative scale:

```text
X_lift = { (r, h, b_or_scale, n0 representative data) }.
```

or use an inverse-limit/profinite coordinate together with a height
coordinate sufficient to interpret the inequality `S^k(n0) < n0`.

This can reproduce the script's terminal rule more faithfully, but it is
no longer a pure `Z_2 x H` transfer operator.  The measure is also less
canonical unless the height/scale distribution is declared.

Verdict: faithful to computation, but analytically less elegant and
more likely to be finite-rank rather than a natural infinite operator.

### P1-C: killed term as external substochastic loss

Keep `X = Z_2 x H` and define the return part 2-adically.  Treat
drop-below and budget events as substochastic loss measured at the
finite-cylinder level:

```text
K_finite = K_return + K_loss,
```

where `K_loss` is not represented by a destination phase. This separates
the terminal tail/killing residual, but does not prove the retained
kernel's sampling and limiting identification. Corrected H3 and the
other open obligations still have to be established.

Verdict: best current compromise.  It matches the existing
substochastic matrix interpretation and avoids pretending that ordinary
integer order is 2-adic.

## 8.5 Updated P1/P2 Status

The conditional A0 closure should therefore be narrowed:

```text
The retained return kernel is a candidate for a Haar/cylinder
conditional-expectation model, conditional on corrected H3 and the
other open identifications. Gate 10.B remains open for the generated
kernels. Terminal/drop-below killing is not intrinsically 2-adic and
must be handled as substochastic loss or by an arithmetic lift space.
```

Updated proof obligations:

| ID | obligation | updated status |
|---|---|---|
| P1a | define monitored phantom tubes in `Z_2` | plausible from existing shadowing formalization |
| P1b | define first return among monitored tubes | plausible as a hitting-time map, measurable under cylinder hypotheses |
| P1c | define drop-below killing on `Z_2` | not canonical; must be external loss or enlarged state |
| P2a | measurability of tube-hitting return map | plausible but not written |
| P2b | boundedness of `g_q` for `s >= 0` | immediate once `delta:N` and `D` are defined, since `0 <= 2^{-s delta} <= 1` |

The corrected current status is:

```text
candidate for retained 2-adic return kernels, sampling still open;
open/structurally non-2-adic for drop-below killing;
terminal mass requires a declared substochastic loss or an arithmetic lift.
```

## 8.6 Final 10.B Verdict for Paper Use

Recommended wording:

```text
Gate 10.B remains open for the retained return part of the phase
operator. A candidate infinite object is a killed weighted
forward kernel on X = Z_2 x H, observed through PhaseState and averaged
by conditional expectation with respect to Haar x counting measure.
Prefix high-bit samples with j_count = 2^m have equal quotient weights.
Their identification with Haar-cylinder conditional expectations of
this kernel still requires a sampling theorem, in addition to the
explicit high-valuation boundary residual.

The gate is not positive for the stronger claim that the finite FULL
matrices are exact projections, nor for the claim that PhaseState is a
sourcewise sufficient statistic.  Moreover, the script-level
drop-below-start killing rule is archimedean and is not intrinsic to
Z_2.  It must be treated as external substochastic loss, or else the
state space must be enlarged with arithmetic lift data.
```

Operational decision:

```text
Use P1-C.

Retained returns:
  model by the A0 Haar conditional-expectation kernel.

Terminal/drop-below/budget events:
  model as substochastic loss measured at the finite-cylinder level.
```

Consequences:

- Gate 10.B cannot be reported as resolved for the generated retained
  return kernel until the sampling/identification obligations are proved.
- The finite-rank K16 note remains the only theorem-producing output.
- 10.C-10.F may only resume as conditional analysis of the retained
  kernel plus substochastic loss.
- No spectral gap or asymptotic Collatz claim follows.

## 9. Compatibility with Existing FULL Matrices

The candidate closure can apply to those row-source constructions only
after the sampling hypothesis has been proved. A finite provenance check
identifies the samples or finite quotient rows; it does not identify
their limit with a measurable Haar observable.

Initial provenance audit:

Reproducible checker:

```text
scripts/spectral_program/111_gate10b_provenance_check.py
```

Current report:

```text
scripts/spectral_program/collatz_111_gate10b_provenance_report.md
```

Result:

```text
T10CriticalSymbolic compatible = True,
T10J32HighBitTail.full compatible = True.
```

### T10CriticalSymbolic

Lean file:

```text
lean/CollatzShadowing/Generated/T10CriticalSymbolic.lean
```

Generated from:

```text
../collatz_75_critical_symbolic_edges.csv
scripts/phantom_taxonomy/lean_phase_transfer.py
scripts/spectral_program/75_critical_symbolic_operator.py
```

The builder loops over:

```text
0 <= t < 2^T,
h in Fin 4,
src = state_of(t,h,...),
dst = state_of(next_t,h+1,...),
weight = 2^{-s delta}.
```

and normalizes by `source_counts[src]`.  Therefore the generated matrix
is a finite Haar/counting conditional expectation over the quotient
`Z/2^T Z x H`, grouped by source `PhaseState`.  It is compatible with
the A0 conditional-expectation interpretation as a finite-resolution
global cylinder approximant.

It is not a high-bit prefix stability object: it corresponds to one
finite quotient depth `T`, not to the script-88/script-107 prefix family
`t = r + j 2^T`.

### T10J32HighBitTail

Lean file:

```text
lean/CollatzShadowing/Generated/T10J32HighBitTail.lean
```

Generated from:

```text
scripts/phantom_taxonomy/high_bit_tail_edges_T10_j32.csv
scripts/phantom_taxonomy/export_high_bit_tail_edges.py
scripts/phantom_taxonomy/lean_high_bit_tail.py
scripts/spectral_program/77_high_bit_tail_bound.py
```

The exporter loops over:

```text
0 <= r < 2^T,
h in Fin 4,
0 <= j < j_count,
t = r + j 2^T.
```

For the generated artifact:

```text
T = 10,
j_count = 32 = 2^5,
odd_bits = 2,
hit_bits = 2,
v2_cap = 13.
```

Thus the `full` matrix is a finite Haar/counting conditional
expectation over the quotient `Z/2^{T+5} Z x H`, grouped by source
`PhaseState`.  This is directly compatible with the conditional 10.B
interpretation.

The `core` and `tail` matrices are extra majority-signature
decompositions of this same finite quotient.  They are finite
bookkeeping objects; the conditional-expectation interpretation applies
first to `full = core + tail`, not automatically to the majority split
as an infinite operator decomposition.

### Remaining generated matrices

For other generated Lean matrices:

```text
other historical FULL matrices,
```

one still needs a provenance check:

```text
Do their rows equal the same high-bit Haar-prefix conditional
expectation rows, with the same source measure and boundary convention?
```

If yes, they inherit the conditional 10.B interpretation.  If no, they
remain finite artifacts/certificates only.

## 10. Updated Recommendation

The no-collaborator route can safely reopen 10.B in the following
narrow form:

```text
Formalize A0_HaarConditionalClosure as a conditional theorem/proposition
in prose, and add a provenance checker for each generated FULL matrix.
```

Do not reopen:

```text
- spectral gap claims;
- Hennion/Keller-Liverani;
- exact projection language;
- sourcewise PhaseState sufficiency.
```

The finite-rank note remains the rigorous deliverable.  This closure
attempt adds a plausible mathematical bridge for future work, but it is
not yet strong enough to replace the finite-rank result.
