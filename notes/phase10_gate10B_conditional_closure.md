# Phase 10.B Conditional Closure Attempt

Date: 2026-05-15

Status: conditional positive solution for Gate 10.B in the weak
`A0-averaged` sense.  This is not a spectral theorem and not an exact
projection theorem.  It gives a mathematically natural infinite object
whose finite cylinder conditional expectations match the shape of the
current phase-prefix kernels, up to explicitly named finite residuals.

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

This is not an arbitrary enumeration.  For prefix windows with
`j_count = 2^m`, it is exactly the uniform finite quotient of Haar
measure on the cylinder `x == r mod 2^T`.

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

Because all retained low-bit cells have equal `mu`-mass, this uniform
cell average is exactly the finite conditional expectation over the
retained part of the phase atom.

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

H3. The finite script/generator rows equal the finite high-bit cylinder
    averages of g_q, up to the explicit boundary/mixed-cell residual.

H4. The finite high-bit prefix windows are powers of two,
    N = 2^m, so that the average over j is Haar-uniform on the quotient
    of each low-bit cylinder.

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

This closes Gate 10.B only as an operator-existence and finite
approximation statement.  It does not imply compactness, a
Lasota-Yorke inequality, Hennion, Keller-Liverani, or a spectral gap.

## 9. Compatibility with Existing FULL Matrices

The closure applies directly to prefix/Haar cylinder kernels whose
provenance is the script-88/script-107 row-source construction.

Initial provenance audit:

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
