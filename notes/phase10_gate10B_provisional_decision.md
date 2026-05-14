# Phase 10 Gate 10.B Provisional Decision

Date: 2026-05-14

Status: provisional decision note after diagnostics `88`-`109`.  This is
not a proof of an infinite operator, a spectral gap, or Conjecture 6.

## 1. Gate Question

Gate 10.B asks whether the finite `FULL_{T,j}` / `full_T` matrices can
be interpreted as exact projections, truncations, compressions,
Galerkin/Ulam approximations, or controlled finite-rank approximants of
a natural infinite operator.

Current answer:

```text
No such interpretation has been established.
```

The strongest exact-projection version is currently not supported by
the diagnostics.

## 2. What Has Been Learned

### 2.1 Exact phase local constancy is not supported

The old `PhaseState` quotient is too coarse.  High-bit lifts with the
same base residue can have stable return status but split destination
phase.

Five extra 2-adic bits, detected as `j mod 32`, improve phase stability
substantially but do not create a projection identity.

### 2.2 `delta` is a real label, not a hidden source coordinate

Even when destination phase is exact, the return exponent `delta` can
split.  Treating `delta` as a pre-transition state coordinate would be
circular unless branch measurability is proved.

Therefore the honest diagnostic model is labelled:

```text
source cylinder -> destination phase with edge label delta.
```

This is not the same as saying that the generated Lean matrices are
labelled matrices.  In `CollatzShadowing/Operator.lean`,
`TransferMatrix V` is a matrix on

```text
PhaseState V = Fin (V+1) x Fin 4 x Fin 4.
```

Thus the current Lean `FULL` object is phase-only.  The `(phase, delta)`
labels used in the prefix diagnostics are presently proof/diagnostic data
attached to phase transitions, unless the project explicitly replaces the
finite object by an enlarged labelled-symbolic operator.

### 2.3 Global weighted `delta` tail is encouraging

The `2^{-delta}` normalization gives small global tails on tested
windows:

| run | `delta > 4` | `delta > 5` | `delta > 8` |
|---|---:|---:|---:|
| `T16_j8` | `0.00412187` | `0.000862882` | `0.00000574087` |
| `T15_j32` | `0.0040648` | `0.000845196` | `0.00000635292` |

This supports a weighted-tail term in a future Banach norm.

It does not prove:

- summability;
- uniform local tail control;
- compactness;
- mixed-norm convergence.

### 2.4 Block-Cauchy evidence is mixed

Adjacent-block full-signature TV is not negligible:

| run | block comparison | full mean TV | full p95 TV | full p99 TV | dominant flip fraction |
|---|---|---:|---:|---:|---:|
| `T15_B8_j16` | `0..7` vs `8..15` | `0.0462265` | `0.25` | `0.375` | `0.0177002` |
| `T15_B16_j32` | `0..15` vs `16..31` | `0.0381069` | `0.1875` | `0.25` | `0.0124817` |
| `T15_B32_j64` | `0..31` vs `32..63` | `0.0310087` | `0.15625` | `0.21875` | `0.011322` |
| `T16_B4_j8` | `0..3` vs `4..7` | `0.0507774` | `0.25` | `0.5` | `0.0238647` |

Dominant labels often remain stable while their masses move.  Therefore
majority stability cannot be used as a Keller-Liverani mixed norm.

The fixed-`T=15` block-doubling trend is encouraging for a
distributional/Cesaro target, but it is not a convergence theorem.

A truncated-label test at `T=15`, block size `32`, shows that clipping
large `delta` labels does not substantially reduce full block-TV:

```text
clip delta > 5: mean TV 0.0308437, p95 0.15625
full label:     mean TV 0.0310049, p95 0.15625.
```

Thus the block-Cauchy obstruction is not only a large-`delta` tail
problem.

The bounded-label excess over destination-phase TV is smaller but not
zero.  At `T=15`, block size `32`, full-label excess has:

```text
mean 0.00791955, p95 0.0625, p99 0.09375.
```

This supports treating bounded label variation as a separate lower-order
error term, not as part of the large-`delta` tail.

### 2.5 Source-stratum drift is weak as currently formulated

Bad cells are structured by source strata.  For example, at `T16_j8`,
`v2=2, odd=3` has:

```text
phase exact fraction = 0.898926,
full exact fraction  = 0.383301.
```

However, the first finite drift probe for the simple family

```text
W = exp(a 1_{odd=3} + b 1_{v2=2} + c min(v2,v2_cap))
```

is negative on the harder `T15_j16` window: nontrivial weights improve
p95 only by introducing cells with drift ratio at least `1`.  The only
safe coarse-grid point there is the identity weight.

Thus source-stratum drift remains a side diagnostic, not a foundation.

### 2.6 True 2-adic child-cylinder tests pressure the naive `Z_2` branch

The ordinary adjacent-block trend at fixed `T = 15` is not the same as a
2-adic martingale-cylinder estimate.  A direct child-cylinder diagnostic
was added:

```text
scripts/spectral_program/100_z2_cylinder_oscillation.py
```

With `T = 15`, `max_j = 128`, and depths `0..2`, full-label mean TV is:

```text
0.0486132 -> 0.0487704 -> 0.0509391.
```

This does not support naive full-label continuity on `Z_2 x H`.

However, the label-excess part is structured.  The stratified diagnostic

```text
scripts/spectral_program/101_z2_oscillation_strata.py
```

finds at depth `2`:

```text
source_v2_odd = 2|3:
mass = 0.0625,
mean full-over-phase excess = 0.120621,
contribution = 0.456409.
```

A lighter `T = 16` run preserves the signal:

```text
source_v2_odd = 2|3:
mass = 0.0625,
mean full-over-phase excess = 0.152130,
contribution = 0.492200.
```

A direct interaction drift weight on that stratum improves typical
ratios but creates exceptional cells above `1`; the coefficient-`1`
test gives p95 `0.155199`, max `2.63334`, and fraction `>= 1` equal to
`0.000366211`.  The worst exceptional cells are not sourced from
`2|3`, so this is not a clean uniform drift solution.

The enriched-state split test is more promising than the scalar drift
weight.  The component

```text
odd = 3 and v2 in {0,2}
```

has mass `0.3125`, captures `0.742956` of full-over-phase excess at
`T15` depth `2` and `0.767081` at `T16` depth `1`, and leaves complement
p95 `0` in both runs.

The follow-up component transition budget over `0 < t < 2^21` shows
that this is not a negligible isolated error component:

```text
K_GG = 0.012281296,
K_GB = 0.0054655765,
K_BG = 0.040839452,
K_BB = 0.018100693.
```

The bad row budget is about `0.058940144`, compared with `0.017746872`
for the good row budget, and about `30.8%` of good weighted return mass
flows into bad.  This supports a block-kernel formulation but weakens
any branch that wants to discard `K_bad` as a small perturbation.

Alternative bad-rule tests do not improve the situation enough to
change the provisional split.  The narrow `v2=2 and odd=3` rule isolates
a hot core with bad row budget `0.20995882`; the broad `odd=3 or v2=2`
rule marks about `0.5625` of sources as bad and has `G->B` weighted
fraction about `0.559896`.

The component block-Cauchy test is the best current positive signal for
Branch A: at fixed `T = 15`, weighted good/bad row drift decreases from
mean `0.012046521` at block size `8` to `0.0074155295` at block size
`32`.  This is a weak averaged signal only, not a projection theorem.

The multipair run weakens the naive Cauchy reading: for `B=16`, pair
means are `0.009535642`, `0.013903232`, and `0.018206286` over
`0->16`, `16->32`, and `32->48`.  Any Branch-A limit must therefore be
formulated as an averaged/mixed-norm limit, not as uniform adjacent-block
Cauchy convergence.

The prefix/Cesaro check is currently the best high-bit convention:
`16->32` mean `0.004767821`, `32->64` mean `0.0037076395`,
`64->128` mean `0.0027624646`.  This keeps Gate 10.B open in a
conditional prefix-average form.

The retained full-label lift remains a separate diagnostic cost.  On
`64->128`, script `106_prefix_label_lift.py` gives label-excess mean
`0.0029977961`, p95 `0.015625`, and p99 `0.03125`.  This is improved
relative to the smaller prefixes, but it is not zero and is not removed
by the `delta <= 5` cutoff.  For the current `FULL` matrices, however,
the first target is phase-prefix convergence.  Retained-label convergence
is sufficient but stronger than necessary unless the labelled-symbolic
extension is chosen explicitly.

## 3. Provisional Branch Decision

### Branch A: analytic operator program

Still alive, but only in a conditional phase-weighted/distributional
form:

```text
hierarchical 2-adic cylinders
+ weighted return exponent delta
+ global/local tail controls
+ phase-prefix Cesaro convergence target.
```

The naive `Z_2` martingale/BV variant is now downgraded unless an
enlarged symbolic state or exceptional-mass mechanism explains the
child-cylinder obstruction.

Current preferred Branch-A formulation for the existing `FULL`
certificates:

```text
phase-only weighted kernel on PhaseState V,
with component and label projections used as diagnostics.
```

This branch should not claim:

- exact finite projection;
- spectral gap;
- asymptotic subcriticality;
- Conjecture 6.

### Branch B: fallback finite-rank program

Still the safer theorem-producing branch:

```text
finite deterministic residue-cell matrices
+ exact Collatz-Wielandt certificates
+ Lean verification.
```

K16 is already formalized.  K20 currently has only a smoke preflight and
must not be advertised as a production theorem.

## 4. Current Best Candidate Operator

For the existing generated `FULL` matrices, the best candidate is a
killed weighted phase first-return kernel:

```text
K_{T,a,N}(r,q,h; terminal)
  = (1/N) # terminal lifts,
```

and

```text
K_{T,a,N}^{phase}(r,q,h; d)
  = (1/N) sum over lifts returning to destination phase d
            of the chosen return weight.
```

For example, the return exponent `delta` may enter through:

```text
2^{-s ell}.
```

The labelled diagnostic kernel

```text
K_{T,a,N}^{label}(r,q,h; d, ell)
```

is still useful, because it decomposes the phase weight by return label
and controls label-sensitive error terms.  It is not, by itself, the
finite state space of the current Lean matrices.

The open issue is whether the limit as `N -> infinity`, and then the
refinement as `a -> infinity`, exists in any useful weak/strong norm.

## 5. Gate 10.B Closure Criterion

Gate 10.B closes positively only after a finite-to-infinite statement is
proved.  The current best target is not an exact-projection statement
for the old `PhaseState` quotient.  For the already generated Lean
`FULL` matrices, the primary target is a phase-only weighted
prefix/Cesaro block-kernel statement.  Retained labels are used to
control the weighted phase kernel, not automatically as extra state
coordinates.

### 5.1 Positive closure theorem target

A positive closure of Gate 10.B would be a theorem with the following
form.

There exist:

1. a measurable phase space

   ```text
   X = Z_2 x H
   ```

   or a declared labelled/symbolic extension of it;
2. a killed weighted row-source kernel `K_s` or operator `U_s`;
3. finite source partitions `P_{T,a}`;
4. finite observation spaces, with optional diagnostic labels,

   ```text
   Y_L = {terminal} union {destination phase}
         union optional {(destination phase, delta) : delta <= L}
         union optional {tail_L};
   ```

5. source weights `omega_{T,a,N}` converging to a declared source
   measure `omega_{T,a}` or `omega`;
6. empirical prefix kernels `K_{T,a,L,N}`;
7. generated row-source matrices `FULL_{T,a,L,N}`;
8. projection/inclusion maps `E_{T,a,L}`, `I_{T,a,L}`;
9. a Banach pair `B_s -> B_w`;

such that:

```text
K_{T,a,L} = E_{T,a,L} U_s I_{T,a,L}
```

is well-defined and

```text
|| I_{T,a,L}(K_{T,a,L} - FULL_{T,a,L,N})E_{T,a,L} ||
  _{B_s -> B_w}
  -> 0
```

in an explicitly declared order of limits.

For the current prefix branch, a finite weak version of the hard
approximation term can be written first in the phase-only form:

```text
||K_{2N}^{phase} - K_N^{phase}||
  _{ell_infty(phase) -> L1(omega_N)} -> 0.
```

The retained-label version is stronger:

```text
||K_{2N} - K_N||_{ell_infty(labelled) -> L1(omega_N)} -> 0.
```

Equivalently, one may first prove the component version

```text
||K_{2N}^{G/B} - K_N^{G/B}||
  _{ell_infty(component) -> L1(omega_N)} -> 0
```

but then one must also prove that the retained-label lift is controlled:

```text
ComponentLabelLift_N -> 0
```

or include it explicitly in the weak error budget.

There is one more choice that must be explicit.  The operator `U_s`
acts on destination-phase observables:

```text
(U_s f)(x) = 1_D(x) 2^{-s delta(x)} f(tau x).
```

The full diagnostic kernel uses retained labels `(destination phase,
delta)`.  The active decision for the existing `FULL` matrices is:

```text
phase-only weighted bridge:
  labels are proof devices used to control the weighted phase kernel;
```

This is the branch compatible with the current Lean type
`TransferMatrix V = Matrix (PhaseState V) (PhaseState V) NNReal`.

The alternative is a separate new object:

```text
labelled-symbolic bridge:
  labels are part of an enlarged symbolic state/edge space.
```

Both are possible mathematical targets.  They are not the same target.
Switching between them without an explicit projection is a failure mode.
For Phase 10.B, the labelled-symbolic bridge is now fallback/enlargement,
not the primary closure route for the existing finite certificates.

Conclusion allowed after this theorem:

```text
The finite row-source kernels are legitimate approximants of U_s.
```

Conclusions still not allowed at this stage:

- spectral gap;
- Lasota-Yorke inequality;
- Hennion essential spectral radius bound;
- Keller-Liverani spectral stability;
- Conjecture 6.

### 5.1.1 Phase-only closure theorem skeleton

For the current Lean `FULL` matrices, the closure theorem should be
written without labelled state coordinates.  A precise conditional
skeleton is:

```text
Theorem PhaseOnlyGate10BClosure(T,a,s).

Let Q_{T,a} be the declared finite phase alphabet, compatible with
PhaseState V.  Let X be the infinite source space with sigma-algebra A,
source measure omega, killed return domain D, return map tau:D -> X,
phase observation pi_{T,a}:X -> Q_{T,a}, and return exponent
delta:D -> N.

Define the weighted phase operator

  (U_s f)(x) = 1_D(x) 2^{-s delta(x)} f(pi_{T,a}(tau x)).

Assume H1-H7 below.  Then the generated/empirical finite row-source
phase matrices FULL_{T,a,N} are legitimate weak finite-rank
approximants of U_s:

  || I_{T,a,N}(K_{T,a} - FULL_{T,a,N})E_{T,a,N} ||
       _{B_s -> B_w}
    -> 0

in the declared order of limits.
```

The hypotheses are:

| Hypothesis | Content | Current status |
|---|---|---|
| H1 source model | `X`, `A`, `omega`, `D`, `tau`, `delta`, and `pi_{T,a}` are defined without using finite-prefix artifacts | open |
| H2 finite partitions | retained source cells `S_N` form measurable complete cells, with explicit excluded-cell error `e_N` | finite version verified by script `107`; limit open |
| H3 empirical phase kernel | `K_{T,a,N}^{phase}(i,q)` is the source-cell average of `1_D 2^{-s delta} 1_{pi tau=q}` | definitional; needs exact match to scripts/generated data |
| H4 row-source identity | the CSV/generated rows equal `K_{T,a,N}^{phase}` up to an explicit finite residual | CSV residual verified as zero by script `107`; Lean generated match still separate |
| H5 phase-prefix Cauchy | `D_N^{phase} = sum_i omega_N(i) sum_q |K_{2N}^{phase}(i,q)-K_N^{phase}(i,q)| -> 0` | open; current finite trend decreases |
| H6 Banach bridge | finite `ell_infty(Q)->L1(omega_N)` control transfers to `B_s -> B_w` through `E_N,I_N` with bounded constants | open/collaborator-level |
| H7 tail/killing control | terminal/killed mass and `delta>L` tails are represented as substochastic loss or bounded error in the chosen norm | finite global tail small; uniform/local control open |

The finite quantity now aligned with `FULL` is:

```text
D_N^{phase}
  = sum_{i in S_N} omega_N(i)
      sum_{q in Q_{T,a}}
        |K_{2N}^{phase}(i,q)-K_N^{phase}(i,q)|.
```

The currently measured values for `T=15`, `delta<=5` are:

```text
16->32:  D_N^{phase} = 0.0066310638,
32->64:  D_N^{phase} = 0.0055465954,
64->128: D_N^{phase} = 0.0045024297.
```

With no `delta` cutoff, the same diagnostic gives:

```text
16->32:  D_N^{phase} = 0.0066438334,
32->64:  D_N^{phase} = 0.0055544859,
64->128: D_N^{phase} = 0.0045072525.
```

The cutoff sensitivity is small at this scale.  This supports, but does
not prove, the idea that the phase-prefix drift is not being artificially
improved by discarding large `delta` returns.

These numbers only address H5 at finite scale.  H1, H6, and the
generated-Lean matching part of H4 remain the main mathematical gates.

The generated-Lean part of H4 is currently not closed for these `T=15`
prefix kernels.  Existing Lean objects have different roles:

```text
K16S16KDeterministicCW:
  Fin 37 deterministic K:b fallback certificate; not a PhaseState FULL.

T10CriticalSymbolic:
  TransferMatrix 10 imported from the older critical-symbolic CSV.

T10J32HighBitTail:
  TransferMatrix 13 for T=10,j=32 with full = core + tail.

script-107 T15 phase-prefix kernels:
  row-source identity verified at CSV level; no matching Lean import yet.
```

Moreover, the `T=15` script-`107` kernels are naturally indexed by
retained source cells `(T,r,h)`, not only by source `PhaseState`.
Collapsing source cells to phase rows has the following finite weak
errors for `delta<=5`:

```text
j=16:  collapse mean = 0.055610515, p95 = 0.27152777,
j=32:  collapse mean = 0.054357070, p95 = 0.27914786,
j=64:  collapse mean = 0.052910359, p95 = 0.27929920,
j=128: collapse mean = 0.051512269, p95 = 0.27979821.
```

This is not a small bookkeeping term relative to the prefix drift.  It
means the current `PhaseState` quotient is an averaged finite quotient,
not an exact projection of the source-cell kernel.  A positive H4 must
therefore prove decay of this collapse error, refine the source state, or
state explicitly that the finite-rank branch is working with an averaged
quotient.

Script `108_source_refinement_collapse.py` gives the first refinement
test.  On the `T=15`, `64->128`, `delta<=5` data:

```text
j=128:
PhaseState               collapse mean = 0.051512269,
PhaseState + r mod 2^10 collapse mean = 0.020415877,
PhaseState + r mod 2^11 collapse mean = 0.018202554,
PhaseState + r mod 2^12 collapse mean = 0.015742233.
```

The no-cutoff run changes these only in the fourth or fifth decimal
place.  The improvement is real, but it is not yet a theorem and not yet
a canonical infinite quotient.  It suggests a finite source refinement
by low residue bits of `r`; high-bit refinements were weaker or had many
near-singleton classes.

Script `109_refined_prefix_cauchy.py` tests whether those refined
source keys also stabilize as the prefix length grows.  The result is a
tradeoff, not a positive closure.  For `T=15`, `64->128`, `delta<=5`,
source-cell-weighted prefix drift is:

```text
PhaseState                 0.000200738344,
PhaseState + r mod 2^10    0.00158494699,
PhaseState + r mod 2^11    0.00210468651,
PhaseState + r mod 2^12    0.00260800395,
source_cell baseline       0.00450242969.
```

Thus low residue bits reduce source-collapse error but increase prefix
drift relative to the bare averaged phase quotient.  The multipair
`16->32->64` run still gives decreasing drift for each selected key
(`r mod 2^10`: `0.00302166308 -> 0.00215625513`), so the refined
branch is not killed.  But the data now force an explicit choice:
either justify bare `PhaseState` as an averaged quotient with a separate
collapse-error term, or choose a refined source alphabet and prove a
prefix-Cauchy theorem for that alphabet.

We freeze this choice into two named branches:

```text
A0 = existing FULL branch:
     source key = source PhaseState.

A1 = refined-source branch:
     source key = (source PhaseState, r mod 2^10).
```

For either branch, let `rho_b:S_N -> A_b` be the source-key map and let
`k_N^{cell}` be the empirical source-cell row.  The quotient row is

```text
K_N^b(a,q)
  = average_{rho_b(i)=a} k_N^{cell}(i,q).
```

The two obligations are:

```text
C_N^b = ||k_N^{cell} - K_N^b rho_b||_{source L1 -> phase L1},
P_N^b = ||K_{2N}^b - K_N^b||_{source-key L1 -> phase L1}.
```

`A0` is compatible with the existing Lean `TransferMatrix V` type, but
has large measured `C_N^0`.  `A1` improves `C_N^b`, but the current data
only define a rectangular kernel `A_10 -> PhaseState`; they do not yet
define a square refined transfer matrix.  A positive `A1` closure would
therefore require destination-refined data, or a proof that the
rectangular finite-rank bridge is the intended approximation object.

The first destination-refined smoke test has been run.  Script
`110_refined_square_probe.py` constructs square kernels on
`(PhaseState,t mod 2^b)` by retracing and recording `next_t mod 2^b`.
For `T=12`, `j=16,32,64,128`, the weighted drift is:

```text
b=0:  0.00138619007 -> 0.00109704799 -> 0.000647069352,
b=5:  0.00493992965 -> 0.00344425218 -> 0.00232221302,
b=8:  0.0123695007  -> 0.0114045768  -> 0.0101905453,
b=10: 0.0152083349  -> 0.0135561906  -> 0.0129098735.
```

The trend is mildly decreasing, but the refined square kernels are
substantially noisier than the phase-only kernel.  This is not a
negative theorem; it is a warning that `A1` should remain secondary
until larger-scale refined-square diagnostics justify the extra state
space.  The `T=13`, `16->32` run reproduces the `T=12`, `32->64`
numbers because it represents the same effective prefix window under a
different grouping, so it is a consistency check rather than independent
evidence.

This skeleton closes Gate 10.B only conditionally.  It does not even
state a spectral-radius conclusion.

### 5.2 Negative closure criterion

Gate 10.B closes negatively if one of the following is shown to be
structural rather than a finite-window artifact:

- no canonical or defensible infinite phase space `X` supports the
  observed first-return statistics;
- `delta` cannot be made measurable/regular in the chosen source
  sigma-algebra, even when it is used only as a weight;
- prefix limits depend essentially on arbitrary enumeration choices;
- source weights `omega_N` cannot be identified with any meaningful
  limiting measure or controlled averaging convention;
- the generated `FULL` matrices cannot be matched to the empirical
  `K_{T,a,L,N}` kernels or to `E U_s I`;
- good/bad component convergence holds but phase-prefix convergence
  fails in every useful weak norm;
- no Banach pair makes the finite weak metric relevant to `B_s -> B_w`.

Conclusion allowed after negative closure:

```text
The analytic Branch A is not justified by the present finite matrices.
Phase 10 should proceed as a finite-rank/computational certificate
program unless a different infinite model is supplied.
```

### 5.3 First lemmas to attack

The first non-numerical closure work should be these lemmas, in order.

| Lemma | Statement | Type | Current status |
|---|---|---|---|
| source-measure lemma | finite `omega_N` is uniform counting on retained complete source cells and differs from full Haar/counting by an explicit excluded-cell mass | definitional/computational | approachable now |
| row-source identity lemma | the CSV/script empirical kernel is exactly the stated prefix kernel `K_{T,a,L,N}` for the selected labels and weights | engineering/definitional | approachable now |
| component/phase/label lemma | retained row drift contracts under the projections `label -> phase -> component`; phase drift is the metric aligned with current `FULL` | finite analytic | finite check verified by script `107` |
| tail split lemma | the `delta > L` discarded part is exactly a separate weighted tail operator | definitional/computational | approachable now |
| Banach bridge lemma | finite `ell_infty -> L1(omega_N)` estimates imply the proposed `B_s -> B_w` estimates after `E/I` | analytic | collaborator-level |
| prefix Cauchy theorem | `K_N` is Cauchy in the chosen weak labelled norm | analytic/combinatorial | open |

On the present `T = 15`, `64 -> 128` dataset, the source-measure
exception is small and explicit:

```text
retained source rows = 131064,
possible source rows = 131072,
excluded fraction    = 8 / 131072 = 0.00006103515625.
```

This finite fact does not prove a limiting source-measure theorem, but
it is the right first lemma shape.

The current finite checks are reproduced by:

```text
python3 scripts/spectral_program/107_gate10b_closure_checks.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_L5
```

The report verifies zero row-source identity residuals and no
component-to-phase, phase-to-label, or component-to-label contraction
violations on the retained rows.  The key finite drift means are:

```text
component_l1 mean = 0.0027621063,
phase_l1 mean     = 0.0045024297,
label_l1 mean     = 0.005743653.
```

The phase-only prefix trend currently available is:

```text
16->32:  0.0066310638,
32->64:  0.0055465954,
64->128: 0.0045024297.
```

This is a useful finite signal for the phase-only bridge, not a proof of
prefix Cauchy convergence.

### 5.4 First finite lemmas

The following finite lemmas are now the first closure lemmas.  They are
bookkeeping lemmas, not spectral statements.

#### Lemma 1: retained-source averaging error

Let `S` be the complete finite source-cell set and `A subset S` the
retained source-cell set used by a diagnostic after excluding mixed or
boundary rows.  Let:

```text
|S| = n,
|S \ A| = e.
```

Let `omega_S` and `omega_A` be the uniform probability measures on `S`
and `A`.  For any bounded diagnostic row function `F`:

```text
| integral F d omega_S - integral F d omega_A |
  <= 2 (e/n) ||F||_infty.
```

Proof: write `omega_S = ((n-e)/n) omega_A + (e/n) omega_E`, where
`omega_E` is uniform on the excluded cells.  Then:

```text
omega_S(F) - omega_A(F)
  = (e/n) (omega_E(F) - omega_A(F)).
```

This is the exact finite meaning of the source-measure correction.
For the current `T = 15`, `64 -> 128` prefix diagnostic:

```text
n = 131072,
e = 8,
2e/n = 0.0001220703125.
```

Thus the retained-source report mean differs from the complete
low-bit-cell mean by at most:

```text
0.0001220703125 * ||F||_infty.
```

This does not identify the complete low-bit-cell mean with an infinite
Haar limit.  It only removes one finite bookkeeping ambiguity.

#### Lemma 2: component/phase/label projection

Let `Y_label` be the retained labelled destination set, let `Y_phase`
be its destination-phase projection, and let:

```text
pi_phase : Y_label -> Y_phase,
pi_component : Y_phase -> {G,B}
```

be the finite projections.  For two substochastic labelled rows `p,q`,
define their phase and component push-forwards:

```text
p_phase = (pi_phase)_* p,
q_phase = (pi_phase)_* q,
p_component = (pi_component)_* p_phase,
q_component = (pi_component)_* q_phase.
```

Then:

```text
||p_component - q_component||_1
  <= ||p_phase - q_phase||_1
  <= ||p - q||_1.
```

Define the finite excess terms:

```text
ComponentPhaseExcess(p,q)
  = ||p_phase - q_phase||_1
    - ||p_component - q_component||_1 >= 0,

PhaseLabelExcess(p,q)
  = ||p - q||_1 - ||p_phase - q_phase||_1 >= 0.
```

Therefore:

```text
||p - q||_1
  = ||p_component - q_component||_1
    + ComponentPhaseExcess(p,q)
    + PhaseLabelExcess(p,q).
```

Thus:

```text
||K_{2N}^{component} - K_N^{component}||_1
  <= ||K_{2N}^{phase} - K_N^{phase}||_1
  <= ||K_{2N}^{label} - K_N^{label}||_1.
```

For the existing `FULL` matrices, the middle term is the aligned
finite metric.  Component convergence alone is too weak unless the
component-to-phase excess is controlled.  Labelled convergence is
sufficient but stronger than necessary unless the project chooses a new
labelled-symbolic operator.

This is why script `107` now reports `component_l1`, `phase_l1`, and
`label_l1` separately.  The script-`106` label-excess term remains useful
as a stronger diagnostic, but `phase_l1` is the metric aligned with the
current Lean `FULL`.

#### Lemma 3: row-source identity for the current CSV layer

For a fixed retained source cell `(T,r,h)` and prefix length `N`, script
`88_cylinder_signature_stability.py` records:

```text
sample_count = N,
weight_sum(signature)
  = sum_{0 <= j < N, full(t_j,h)=signature} weight(t_j,h),
t_j = r + j 2^T.
```

Scripts `105` and `106` then use:

```text
weight_sum(signature) / sample_count.
```

Therefore the reported row entries are exactly the row-source empirical
prefix kernel:

```text
K_N(source, signature)
  = (1/N) sum_{0 <= j < N}
      1_{full(t_j,h)=signature} weight(t_j,h).
```

After component collapse, the reported component row is exactly:

```text
K_N(source, tau)
  = sum_{signature : component(signature)=tau}
      K_N(source, signature).
```

This proves identity with the empirical prefix kernel defined by the
scripts.  It does not prove identity with an ideal projected operator
`E U_s I`.

#### Lemma 4: retained-label tail split

Fix a cutoff `L`.  Split the labelled row into:

```text
K_N = K_N^{<=L} + K_N^{>L},
```

where `K_N^{<=L}` retains signatures with `delta <= L` and `K_N^{>L}`
contains all returning signatures with `delta > L`.

For bounded test functions `||f||_infty <= 1`:

```text
|(K_N - K_N^{<=L})f(source)|
  <= K_N^{>L}(source, all labels).
```

Thus the weak source-averaged tail error is bounded by:

```text
sum_source omega_N(source) K_N^{>L}(source, all labels).
```

This is the finite operator meaning of the global weighted tail
diagnostic.  It is not a uniform tail bound unless the sourcewise tail
is controlled in supremum or by an exceptional-source estimate.

## 6. Required Before Hennion/Keller-Liverani

Do not invoke Hennion or Keller-Liverani until all of the following are
specified:

1. infinite phase space `X`;
2. killed weighted phase operator `U_s` or its dual push-forward;
3. strong Banach norm `||.||_s`;
4. weak norm `||.||_w`;
5. compactness or tightness mechanism;
6. finite maps `E_N`, `I_N`, or equivalent projections;
7. mixed-norm approximation statement;
8. tail constants and their role in the inequality;
9. orientation convention relative to the generated finite matrices.

## 7. Go / No-Go Criteria

Continue Branch A only if the next step produces a named norm and a
testable approximation statement such as:

```text
||E_N L I_N - K_N||_{s -> w} <= epsilon_N,
epsilon_N -> 0.
```

Switch emphasis to Branch B if:

- block-TV does not decrease under larger block tests;
- block-TV decreases too slowly or only on selected windows;
- local `delta` tails remain uncontrolled;
- no non-overfitted drift/tail weight survives `T15/T16`;
- finite kernels depend essentially on arbitrary prefix choices;
- no collaborator can identify a plausible Banach pair.

## 8. Immediate Next Action

The next analytic action should be definitional, not numerical:

```text
prove or falsify the first Gate-10.B closure lemmas:
source-measure, row-source identity, component/phase/label projection,
phase-prefix Cauchy, and tail split.
```

Recommended candidate for the existing `FULL` certificates:

```text
weighted phase kernel on a martingale-cylinder or symbolic source space
```

Read the labelled diagnostics as:

```text
labels control the phase-kernel error;
labelled symbolic space only if the phase-only bridge fails.
```

with constants:

- `DeltaTail_global(L)`;
- `DeltaTail_local(L)`;
- `BlockTV_full(B)`;
- boundary/killing regularity term;
- optional source-stratum drift only if derived from branch geometry.

If that statement cannot be written cleanly, stop the analytic branch
and develop the finite-rank fallback as the main Phase 10 product.

Follow-up:

```text
notes/phase10_mixed_norm_candidate.md
```

now writes this target explicitly.  Its most fragile error term is the
adjacent-block distributional error `A_block(N)`, not the majority
signature flip rate.
