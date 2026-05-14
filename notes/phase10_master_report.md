# Phase 10 Master Report

Date: 2026-05-14

Status: consolidated working report.  This document is the preferred
entry point for Phase 10.  The more specialized `phase10_*.md` files are
working notes and evidence logs.

## 1. Executive Summary

Gate 10.B is not closed.

The finite matrices `full_T` / `FULL_{T,j}` are not currently known to
be exact projections, Ulam discretizations, Galerkin approximants, or
compressions of an infinite operator.

The strongest exact-projection interpretation is currently unsupported.

The analytic branch remains viable only as a conditional program:

```text
kernel first:       K(src,dst)
primary operator:   U_s on functions
dual mass operator: P_s^*
secondary only:     L_s/Ruelle
```

The naive `Z_2` martingale/BV branch is now under pressure: true
2-adic child-cylinder diagnostics do not show decreasing full-label
oscillation on the tested windows.  This pushes the serious analytic
options toward either an enlarged symbolic/countable state space or a
finite-rank fallback.

The finite-rank branch remains the most reliable theorem-producing
branch.

The best current analytic sub-branch is now narrower: use a
good/bad block-valued prefix-average kernel.  Ordinary adjacent
high-bit block Cauchy is not supported by the multipair test, while
nested prefix/Cesaro averages give the cleanest finite signal.  The
target is a weak mixed-norm convergence statement for `K_N`, not a
spectral theorem.

Gate 10.B will be considered closed positively only if the project
proves a finite-to-infinite approximation theorem.  For the existing
Lean matrices this must be a phase-only weighted bridge, because
`TransferMatrix V` is typed over `PhaseState V`, not over
`(PhaseState V, delta)` labels:

```text
FULL_{T,a,L,N} approximates K_{T,a,L} = E_{T,a,L} U_s I_{T,a,L}
```

in a declared `B_s -> B_w` or finite-to-Banach weak norm.  Retained
`(phase, delta)` labels may be used as proof devices to bound the
phase-only weighted error; they are not automatically part of the
operator approximated by the generated `FULL` matrices.  The first
closure lemmas are now source-measure identification, row-source
identity for the empirical prefix kernel, component/phase/label
projection, tail split, and then phase-prefix Cauchy.  Retained-label
prefix Cauchy is a stronger sufficient route for a deliberately enlarged
labelled branch.  None of these is a spectral gap statement.

The first finite bookkeeping lemmas are now fixed in
`notes/phase10_gate10B_provisional_decision.md`: retained-source
averaging error, component/phase/label projection contraction,
row-source identity for the CSV prefix kernel, and retained-label tail
split.  The first genuinely open mathematical lemma is therefore the
phase-prefix Cauchy theorem for the current `FULL` matrices, or the
stronger retained-label prefix Cauchy theorem if we choose the enlarged
labelled branch.

Script `107_gate10b_closure_checks.py` verifies the finite bookkeeping
lemmas on the latest `T = 15`, `64 -> 128`, `delta <= 5` dataset:

```text
retained cells per prefix = 131064 / 131072,
source mean error coeff   = 0.0001220703125,
row-source residuals      = 0,
component/phase/label violations = 0/0/0,
phase_l1 mean            = 0.0045024297,
label_l1 mean            = 0.005743653,
tail weight mean          ~= 2.54e-05.
```

The same phase-only metric on the prefix sequence gives:

```text
16->32 phase_l1 mean  = 0.0066310638,
32->64 phase_l1 mean  = 0.0055465954,
64->128 phase_l1 mean = 0.0045024297.
```

Without the `delta <= 5` cutoff, the same phase-only means are:

```text
16->32 phase_l1 mean  = 0.0066438334,
32->64 phase_l1 mean  = 0.0055544859,
64->128 phase_l1 mean = 0.0045072525.
```

Thus the present phase-prefix trend is not mainly a large-`delta` tail
artifact on these windows.

This is encouraging finite evidence for the phase-only bridge.  It is
not a Cauchy theorem and not a limiting operator.

This closes only the finite bookkeeping layer.  It does not close the
infinite Gate 10.B.

The current phase-only closure skeleton has seven hypotheses:

```text
H1 source model:        X,A,omega,D,tau,delta,pi_{T,a}
H2 source cells:        retained complete cells plus excluded-cell error
H3 empirical kernel:    K_N^{phase} as weighted source-cell average
H4 FULL matching:       K_N^{phase} equals/approximates generated rows
H5 phase Cauchy:        D_N^{phase} -> 0
H6 Banach bridge:       E_N,I_N transfer finite weak norm to B_s -> B_w
H7 tail/killing:        terminal and delta-tail terms controlled
```

The finite work supports H2-H4 at the script/CSV layer.  H5 is the next
real test.  H6 is the point where outside functional-analytic expertise
may be needed.

H4 has an important limitation.  The CSV row-source identity is verified
for the script-`88`/`107` `T=15` prefix data, but no generated Lean
`TransferMatrix` has yet been imported for those `T=15` phase-prefix
kernels.  Existing Lean objects split as follows:

```text
K16S16KDeterministicCW: Fin 37 K:b fallback certificate, not PhaseState.
T10CriticalSymbolic:    TransferMatrix 10, older critical-symbolic import.
T10J32HighBitTail:      TransferMatrix 13, T=10,j=32 full=core+tail import.
script-107 T15 kernels: CSV-verified only; Lean import/match open.
```

There is a stronger obstruction: script `107` now measures the error
from collapsing retained source cells `(T,r,h)` to source `PhaseState`
rows.  For `T=15`, `delta<=5`, the source-phase collapse means are:

```text
j=16:  0.055610515,
j=32:  0.054357070,
j=64:  0.052910359,
j=128: 0.051512269.
```

The p95 values stay near `0.28`.  This is far larger than the
prefix-to-prefix phase drift.  Therefore the current source-cell kernel
is not an exact `PhaseState -> PhaseState` projection at these scales.
Closing H4 requires either a refined source state, a theorem that this
collapse error tends to zero, or an explicit finite-rank interpretation
that accepts the averaging.

Script `108_source_refinement_collapse.py` tests such refinements.  On
the `T=15`, `64->128`, `delta<=5` data, low residue bits of `r` are the
only clearly effective simple refinement:

```text
j=128 source key        collapse mean   mean cells/key
PhaseState             0.051512269     about 1170
PhaseState + r mod 2^10 0.020415877     31.75
PhaseState + r mod 2^11 0.018202554     15.95
PhaseState + r mod 2^12 0.015742233     7.99
```

The no-cutoff repeat is essentially identical.  This is useful but not
decisive: `r mod 2^12` is already close to a fine finite partition, and
the worst rows remain large.  The current best honest next candidate is
therefore a refined finite source alphabet `PhaseState + r mod 2^10`
or `PhaseState + r mod 2^11`, not the bare `PhaseState`.

Script `109_refined_prefix_cauchy.py` checks the other half of the
tradeoff: after choosing a source key, does its averaged destination
`PhaseState` row stabilize with the prefix length?  On the same
`T=15`, `64->128`, `delta<=5` data, source-cell-weighted prefix drift is
smallest for the bare averaged `PhaseState` quotient:

```text
source key                 weighted prefix drift 64->128
PhaseState                 0.000200738344
PhaseState + r mod 2^10    0.00158494699
PhaseState + r mod 2^11    0.00210468651
PhaseState + r mod 2^12    0.00260800395
source_cell baseline       0.00450242969
```

For `16->32->64`, the selected refined drifts decrease with the prefix
scale; for example `PhaseState + r mod 2^10` gives
`0.00302166308 -> 0.00215625513`, while the `source_cell` baseline gives
`0.00663106383 -> 0.00554659544`.  This is useful finite evidence, but
it sharpens the dilemma rather than closing Gate 10.B: bare `PhaseState`
has better prefix stability but poor source collapse, while adding low
residue bits improves source collapse but moves toward the less stable
cell-level kernel.

The analytic branch is therefore frozen into two named sub-branches:

```text
A0: rho_0(source cell)  = source PhaseState.
A1: rho_10(source cell) = (source PhaseState, r mod 2^10).
```

For a source quotient `rho_b:S_N -> A_b`, write

```text
K_N^b(a,q)
  = average of the cell rows k_N^{cell}(i,q)
    over all retained cells i with rho_b(i)=a.
```

Then the two necessary finite errors are:

```text
C_N^b = source-collapse error from k_N^{cell} to K_N^b rho_b,
P_N^b = prefix drift from K_N^b to K_{2N}^b.
```

`A0` is the only branch currently compatible with the existing
`TransferMatrix V` objects, because those are square matrices on
`PhaseState V`.  But `A0` must carry the large source-collapse term
unless a theorem proves it decays or justifies it as the intended
averaging.

`A1` is the best current compromise at finite scale, but it is not yet a
spectral operator: the present CSVs record destination phase, not a
destination `r mod 2^10` coordinate.  Thus `A1` is currently a
rectangular diagnostic kernel from refined source keys to destination
phases.  A true `A1` operator branch would require destination-refined
data or a separate theorem explaining why the rectangular bridge is
sufficient.

Script `110_refined_square_probe.py` performs the first small retraced
test of such destination-refined data.  It builds square finite kernels

```text
(PhaseState, t mod 2^b) -> (PhaseState, next_t mod 2^b)
```

for `b = 0,5,8,10`.  On the smoke windows `T=12`,
`j=16,32,64,128`, the weighted prefix drifts are:

```text
b=0:  0.00138619007 -> 0.00109704799 -> 0.000647069352
b=5:  0.00493992965 -> 0.00344425218 -> 0.00232221302
b=8:  0.0123695007  -> 0.0114045768  -> 0.0101905453
b=10: 0.0152083349  -> 0.0135561906  -> 0.0129098735
```

The downward trend is not negative, but the refined square kernels are
much noisier than the phase-only kernel at this scale.  At the last
comparison, `b=10` is still about twenty times the phase-only drift.
This supports keeping `A1` as a research branch, not as the main
Phase-10 bridge for the existing `FULL` matrices.

The finite-to-Banach bridge is now reduced to one conditional estimate.
For phase-prefix drift:

```text
D_N = sum_i omega_N(i) sum_y |K_{2N}(i,y)-K_N(i,y)|.
```

If the chosen projections satisfy:

```text
||E_N f||_infty <= C_E ||f||_s,
||I_N g||_w <= C_I ||g||_{L1(omega_N)},
```

then:

```text
||I_N (K_{2N}-K_N) E_N||_{B_s -> B_w}
  <= C_E C_I D_N.
```

So the next genuinely analytic task is no longer vague: choose
`B_s,B_w` and prove or reject these two projection/inclusion bounds.

One modelling choice is now fixed for the existing `FULL` certificates:
start with the phase-only weighted bridge.  The labelled-symbolic bridge
is a fallback/new-object route, useful if phase-only control fails or if
one deliberately writes a companion theory on an enlarged symbolic edge
space.  The finite diagnostics support keeping labels in the error
analysis, but they do not by themselves replace the phase-state Lean
matrices with labelled matrices.

## 2. What Is Certified

Production finite certificate:

```text
lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean
```

Certified finite result:

```text
90833233962213 / 129559208330288 < 3/4.
```

Lean theorem:

```text
k16s16KDeterministicGeneratedSpectralRadiusBound.
```

This certifies only the declared 37-state deterministic residue-cell
`(K,b)` finite matrix.  It does not certify an infinite spectral gap or
Conjecture 6.

## 3. Operator Choice

The primary object is the killed weighted phase kernel:

```text
K(src,dst) >= 0.
```

Here `src` and `dst` are finite phase states.  Return labels such as
`delta` enter through the weight and through the error analysis; they are
not additional coordinates of the current Lean `TransferMatrix V`.

The primary analytic operator is:

```text
(U_s f)(src) = sum_dst K_s(src,dst) f(dst).
```

This is the most honest choice because the phase/high-bit matrices are
row-source:

```text
M_row[src,dst] = K(src,dst).
```

The push-forward is retained as the dual mass operator:

```text
(P_s^* mu)(dst) = sum_src K_s(src,dst) mu(src).
```

The Ruelle/preimage operator is secondary:

```text
(L_s f)(dst) = sum_src K_s(src,dst) f(src).
```

It should not be used as the main Phase-10 object until inverse
branches, summability, and projection compatibility are proved.

## 4. Finite Approximation Target

Let `P_n` be a finite cylinder/phase partition and `F_n` the functions
constant on `P_n`.

Projection:

```text
(E_n f)(C) = average of f over C.
```

Inclusion:

```text
(I_n v)(x) = v(C_n(x)).
```

Ideal finite kernel:

```text
K_n = E_n U_s I_n.
```

Generated empirical/high-bit matrix:

```text
FULL_N.
```

The Gate 10.B question is now:

```text
Is FULL_N close to K_n = E_n U_s I_n?
```

The desired mixed-norm target is:

```text
|| U_s - I_N FULL_N E_N ||_{B_s -> B_w} <= epsilon_N.
```

No such theorem has been proved.

## 5. Weak Norm Direction

Current default:

```text
B_w = L^1(m)
```

on the source phase space, with `m` intended as Haar on the 2-adic
coordinate times counting measure on the finite hit/phase coordinate.

The strong norm must at least control:

```text
||f||_infty.
```

Candidate strong seminorm:

```text
2-adic cylinder oscillation / martingale variation.
```

## 6. Finite Row-TV Bridge

For two finite row-source kernels `K` and `K'`, define:

```text
TV_i(K,K') = (1/2) sum_j |K(i,j) - K'(i,j)|.
```

Then:

```text
|(K v)(i) - (K' v)(i)|
  <= 2 TV_i(K,K') ||v||_infty.
```

Thus:

```text
uniform row-TV -> ell_infty to ell_infty control,
average row-TV -> ell_infty to L1 control.
```

This is why the script-`99` TV diagnostics are relevant to the `U_s`
program.

But p95 is not an operator norm.  To use p95, one needs an
exceptional-source-mass estimate.

## 7. Current Diagnostic State

Active error-budget run:

```text
T = 15,
prefix j_count = 64,
block size = 32.
```

Main finite proxies:

```text
DeltaTail_global(5)      = 0.000830424
DeltaTail_local_p95(5)   = 0.027027
DeltaTail_local_max(5)   = 1
A_phase_block p95        = 0.125
full A_label_bounded p95 = 0.0625
```

Weak averaged row-TV proxies:

```text
A_phase_block weak L1 proxy        = 0.0461707
full label-TV weak L1 proxy        = 0.0620098
full A_label_bounded weak L1 proxy = 0.0158391
```

Fixed-`T = 15` block-size check using the same script-`99` row-TV
bridge:

| block size | prefix j | phase weak `L1` | full-label weak `L1` | bounded-label weak `L1` | full-label sup proxy |
|---:|---:|---:|---:|---:|---:|
| 8 | 16 | `0.0731834` | `0.0924482` | `0.0192648` | `1.5` |
| 16 | 32 | `0.0589389` | `0.0762047` | `0.0172658` | `1.0` |
| 32 | 64 | `0.0461707` | `0.0620098` | `0.0158391` | `0.75` |

Sup proxies are still large:

```text
A_phase_block sup proxy = 0.5625
full label-TV sup proxy = 0.75
```

Interpretation:

- global `delta` tail is encouraging;
- local uniform tail is not controlled;
- weak averaged TV looks plausible;
- the fixed-`T` weak proxy decreases across `B = 8,16,32`, which keeps
  the mixed-norm branch alive;
- uniform row-TV/sup perturbation does not look plausible yet.

Source-measure caveat:

- script `88` averages over low-bit cells `(r,h)`;
- at `T = 15`, `j = 16,32,64`, exactly `8/131072` such cells have two
  `source_phase` states;
- the finite mass is small, but a proof must split these cells or add a
  source-partition error;
- adjacent high-bit blocks in ordinary `j` order are not yet a canonical
  2-adic martingale-cylinder comparison.

First true 2-adic child-cylinder diagnostic:

```text
script: 100_z2_cylinder_oscillation.py
run A:  T15_d3_tail2, max_j = 64
run B:  T15_d2_tail4, max_j = 128
```

Full-label child TV by high-bit depth, first run:

| depth | mean TV | p95 TV | max TV |
|---:|---:|---:|---:|
| 0 | `0.0526182` | `0.1875` | `1` |
| 1 | `0.0544645` | `0.25` | `1` |
| 2 | `0.0575895` | `0.25` | `1` |
| 3 | `0.0606241` | `0.5` | `1` |

With more tail samples and depth restricted to `0..2`:

| depth | mean TV | p95 TV | max TV |
|---:|---:|---:|---:|
| 0 | `0.0486132` | `0.171875` | `1` |
| 1 | `0.0487704` | `0.1875` | `1` |
| 2 | `0.0509391` | `0.25` | `1` |

Interpretation: this does not support a naive 2-adic
martingale-continuity claim.  The higher-tail run reduces sampling
noise but still does not show decreasing full-label oscillation.  This
is negative pressure on the simplest `Z_2` Banach-space branch, not yet
a proof of failure.

Stratified 2-adic diagnostic:

```text
script: 101_z2_oscillation_strata.py
run:    T15_d2_tail3, max_j = 64
```

At depth `2`, the full-TV obstruction is broad, but the label excess
over phase is concentrated:

| stratum | mass | mean excess | p95 | contribution |
|---|---:|---:|---:|---:|
| `source_odd = 3` | `0.499969` | `0.0261895` | `0.25` | `0.792725` |
| `source_v2 = 2` | `0.125` | `0.0623322` | `0.25` | `0.471709` |
| `source_v2_odd = 2|3` | `0.0625` | `0.120621` | `0.375` | `0.456409` |

Interpretation: the naive `Z_2` martingale space is weak, but the
obstruction is not completely featureless.  A labelled symbolic or
drift-weighted state space remains a plausible next analytic object.

Cross-`T` check:

```text
run: T16_d1_tail2
```

At `T = 16`, depth `1`, the same stratum persists:

```text
source_v2_odd = 2|3:
mass = 0.0625,
mean full-over-phase excess = 0.152130,
contribution = 0.492200.
```

This makes the stratum signal more credible as structure, not just a
single-window accident.

Interaction drift probe:

```text
script: 96_stratum_weight_drift_probe.py
run:    T15_j16_interaction_only
```

Adding a weight coefficient only on `source_v2_odd = 2|3` gives:

| coeff | p95 | p99 | max | fraction `>= 1` |
|---:|---:|---:|---:|---:|
| `0` | `0.25` | `0.421875` | `0.96875` | `0` |
| `0.5` | `0.226562` | `0.3125` | `1.5972` | `0.0000305176` |
| `1` | `0.155199` | `0.326143` | `2.63334` | `0.000366211` |

Interpretation: the interaction coefficient improves typical ratios
but creates exceptional cells above `1`.  It is not a safe uniform drift
weight; it remains possible only with an explicit exceptional-mass
argument.

The coefficient-`1` worst cells are not primarily sourced from
`source_v2_odd = 2|3`; the largest observed ratio is at source
`v2=1|odd=1`, with drift ratio `2.63334`.  This means the weight moves
the problem into incoming transitions rather than isolating a clean bad
source stratum.

Enriched-state test:

```text
script: 102_enriched_state_test.py
runs:   T15_d2_tail3, T16_d1_tail2
```

The most promising finite split is not the single stratum `2|3`, but a
broader source component:

```text
bad component = { odd = 3 and v2 in {0,2} }.
```

For full-over-phase excess:

| run | selected mass | selected contribution | complement mean | complement p95 |
|---|---:|---:|---:|---:|
| `T15`, depth `2` | `0.3125` | `0.742956` | `0.00617565` | `0` |
| `T16`, depth `1` | `0.3125` | `0.767081` | `0.00654463` | `0` |

Interpretation: an enlarged symbolic state with a distinguished bad
component is now more credible than a scalar drift weight.  The bad
component itself is not solved; it needs internal labelled dynamics or
must be routed to the finite-rank fallback.

Two-component transition-budget diagnostic:

```text
script: 103_component_transition_budget.py
run:    T15_j32 and T15_j64 prefix-growth check
bad:    odd = 3 and v2 in {0,2}
```

Weighted return matrix between source components, with terminal/killed
events assigned zero transfer weight:

| run | source | destination good | destination bad | row sum |
|---|---|---:|---:|---:|
| `0<t<2^20` | `good` | `0.012278567` | `0.0054906632` | `0.017769231` |
| `0<t<2^20` | `bad` | `0.040819731` | `0.018073894` | `0.058893625` |
| `0<t<2^21` | `good` | `0.012281296` | `0.0054655765` | `0.017746872` |
| `0<t<2^21` | `bad` | `0.040839452` | `0.018100693` | `0.058940144` |

The finite `2 x 2` spectral radius of this component-aggregated matrix
is `0.03041195` on the larger `0 < t < 2^21` window.  This number is
only a finite diagnostic.  It is not an infinite spectral-radius
estimate.

Interpretation: the split is useful, but the bad component is not an
isolated small perturbation.  It has source mass about `0.3125`, carries
about `3.31` times the weighted return row budget of the good component,
and roughly `30.8%` of the good weighted return mass flows into bad.
Thus a serious analytic model should use a block kernel

```text
K = [[K_GG, K_GB],
     [K_BG, K_BB]]
```

or an explicit finite-rank/exceptional treatment for the bad block.  A
scalar drift weight alone is not the right next object.

Guardrail: this script aggregates over actual lifted sources `t`.
Runs with the same product `j_count * 2^T` enumerate the same `t`
window and are not independent stability checks in `T`.

Alternative bad-rule comparison on the common `T15_j32` window:

| bad rule | bad mass | good row sum | bad row sum | G->B weighted frac | B->B weighted frac |
|---|---:|---:|---:|---:|---:|
| `v2=2 and odd=3` | `0.0625001` | `0.018664724` | `0.20995882` | `0.0631777` | `0.0626915` |
| `odd=3 and v2 in {0,2}` | `0.3125003` | `0.017769231` | `0.058893625` | `0.308998` | `0.306891` |
| `odd=3 or v2=2` | `0.5624996` | `0.020555724` | `0.038448879` | `0.559896` | `0.558768` |

The narrow rule isolates a very active core but makes `bad` too
singular.  The broad rule absorbs more than half the source space and
mixes too strongly to be a clean exceptional component.  The current
middle rule remains the best provisional compromise.

Consequent analytic target: any future LY estimate should be formulated
first as a block inequality on `B_G direct_sum B_B`, with constants
`a_GG,a_GB,a_BG,a_BB`.  Only after those constants are proved would it
make sense to ask whether the weighted block matrix has radius `< 1`.
The empirical component matrix above is not that theorem-level matrix.

Component block-Cauchy diagnostic:

```text
script: 104_component_block_cauchy.py
runs:   T15_B8_j16, T15_B16_j32, T15_B32_j64
```

This reads the existing script-`88` block distributions and compares
adjacent high-lift blocks after collapsing destinations to `good/bad`.
The main metric is weighted substochastic row `L1` drift.

| block size | all mean | all p95 | all max | good mean | bad mean |
|---:|---:|---:|---:|---:|---:|
| `8` | `0.012046521` | `0.0625` | `0.40625` | `0.0093235814` | `0.018036723` |
| `16` | `0.0095367816` | `0.056640625` | `0.25` | `0.0071800626` | `0.014721333` |
| `32` | `0.0074155295` | `0.0390625` | `0.140625` | `0.0055656365` | `0.011485113` |
| `64` | `0.0055249292` | `0.026367188` | `0.091308594` | `0.0041154957` | `0.0086254075` |

The `B=64` row comes from the later `T15_B64_j128_prefix` run and
compares the adjacent blocks `0..63` and `64..127`.

Block-entry mean absolute drifts at block size `32`:

```text
K_GG: 0.0034798091
K_GB: 0.0020858274
K_BG: 0.0073552837
K_BB: 0.0041298296
```

Interpretation: this is positive evidence for a weak averaged
block-kernel approximation target.  It is still not a uniform
operator-norm estimate: p95 and max values remain visible, especially
on bad-source rows.

Multipair caution:

```text
script: 88_cylinder_signature_stability.py
run:    T15_B16_j64_multipair
script: 104_component_block_cauchy.py
```

For block size `16`, comparing three adjacent pairs in the same prefix:

| pair | all mean | all p95 | good mean | bad mean | bad p95 |
|---|---:|---:|---:|---:|---:|
| `0->16` | `0.009535642` | `0.056640625` | `0.0071783004` | `0.014721333` | `0.0625` |
| `16->32` | `0.013903232` | `0.09375` | `0.0084089414` | `0.025989598` | `0.109375` |
| `32->48` | `0.018206286` | `0.1015625` | `0.00940828` | `0.037560182` | `0.203125` |

This weakens any simple Cauchy narrative in ordinary adjacent `j`
blocks.  The averaged block-size trend remains useful, but later
block-pairs show larger drift.  A serious limit statement must specify
the averaging scheme, subsequence/order of limits, or an
exceptional-source/tail mechanism.

Component prefix/Cesaro diagnostic:

```text
script: 105_component_prefix_cauchy.py
runs:   T15_j16_32_64_multipair, T15_j64_128_prefix
```

This compares nested prefix averages rather than ordinary adjacent
blocks:

| prefix pair | all mean | all p95 | good mean | bad mean | bad p95 |
|---|---:|---:|---:|---:|---:|
| `16->32` | `0.004767821` | `0.0283203125` | `0.0035891502` | `0.0073606666` | `0.03125` |
| `32->64` | `0.0037076395` | `0.01953125` | `0.002782595` | `0.0057425566` | `0.021484375` |
| `64->128` | `0.0027624646` | `0.013183594` | `0.0020577478` | `0.0043127038` | `0.015077209` |

Interpretation: the prefix/Cesaro version is currently much more
promising than ordinary adjacent-block Cauchy.  The new `64->128`
test strengthens this finite trend.  It is still finite evidence only,
but it gives the cleanest current Gate-10.B branch: define a
block-valued prefix-average kernel and seek mixed-norm convergence of
those averages.

The formal finite target is:

```text
PrefixCoupling_N
  = sum_c omega_N(c)
      sum_{tau in {G,B}}
        |K_{2N}(c,tau) - K_N(c,tau)|
  -> 0.
```

Equivalently, on bounded component observables:

```text
|| (K_{2N} - K_N) f ||_{L1(omega_N)}
  <= PrefixCoupling_N ||f||_infty.
```

This is the exact status of script `105`: it estimates a finite
`ell_infty(component) -> L1(source)` proxy.  It does not yet lift to
retained phase/delta labels, does not prove a limiting kernel, and does
not identify the generated `FULL` matrices as projections of an
infinite operator.

The source measure in this proxy is currently only the script-level
finite counting measure on retained complete source cells/prefix pairs.
The default run excludes mixed-source cells and boundary rows.  A
proof-level branch still has to show whether these measures converge to
the intended Haar/counting source measure, or charge the difference as
an explicit source-measure error.

Prefix label-lift diagnostic:

```text
script: 106_prefix_label_lift.py
runs:   T15_j16_32_64_multipair_full,
        T15_j16_32_64_multipair_L5,
        T15_j64_128_prefix_full,
        T15_j64_128_prefix_L5
```

This compares the component-collapsed prefix drift with the retained
full-label prefix drift.  With no delta cutoff:

| metric | mean | p95 | p99 | max |
|---|---:|---:|---:|---:|
| component `L1` | `0.0042377302` | `0.0234375` | `0.0390625` | `0.125` |
| full-label `L1` | `0.0075584849` | `0.038085938` | `0.0703125` | `0.34375` |
| label excess | `0.0033207547` | `0.017578125` | `0.046875` | `0.28125` |

With cutoff `delta <= 5`, the label excess is essentially unchanged:

```text
mean 0.0033040573, p95 0.017578125, p99 0.046875.
```

On the larger prefix comparison `64->128`, the same quantities improve
but do not vanish:

| metric | mean | p95 | p99 | max |
|---|---:|---:|---:|---:|
| component `L1` | `0.0027624646` | `0.013183594` | `0.01953125` | `0.045654297` |
| full-label `L1` | `0.0057602607` | `0.02444458` | `0.041381836` | `0.13671875` |
| label excess | `0.0029977961` | `0.015625` | `0.03125` | `0.109375` |

Interpretation: the component kernel is not hiding only rare
large-`delta` tails.  Retained full labels still add a real
`ComponentLabelLift` term.  The term decreases across the tested
prefixes, but the p99/max rows remain too large for a uniform claim.

Alternative bad-rule label-lift checks do not overturn the current
middle split:

| bad rule | component `L1` mean | label-excess mean | bad row count |
|---|---:|---:|---:|
| `v2=2 and odd=3` | `0.0035912445` | `0.0039672405` | `16384` |
| `odd=3 and v2 in {0,2}` | `0.0042377302` | `0.0033207547` | `81920` |
| `odd=3 or v2=2` | `0.0044146893` | `0.0031437956` | `147448` |

The narrow rule leaves too much retained-label drift.  The broad rule
slightly lowers label excess but marks about `56.25%` of retained source
rows as bad, so it is less useful as an exceptional/block component.
The `64->128` alternative-rule repeat gives the same qualitative
conclusion: label-excess means are `0.0034477554` for the narrow rule,
`0.0029977961` for the middle rule, and `0.0028990557` for the broad
rule.

## 8. Main Risks

The analytic program may fail because:

- no canonical infinite kernel may exist;
- `FULL_N` may be a finite artifact rather than an approximant to
  `E_N U_s I_N`;
- local `delta` tails may remain uncontrolled;
- `U_s` is Koopman/composition-like and may not regularize;
- compactness `B_s -> B_w` may fail;
- row-TV diagnostics may not upgrade to mixed-norm convergence.
- current high-bit block diagnostics may be measuring ordinary interval
  stability rather than the 2-adic continuity needed for the Banach
  norm.
- the first actual 2-adic child-cylinder diagnostic does not show
  decreasing full-label oscillation.
- the label-excess obstruction may require a nontrivial symbolic/drift
  state, not just a smoothness norm on `Z_2 x H`.

## 9. Hennion/Keller-Liverani Status

Do not invoke Hennion yet.

Missing:

- Banach pair;
- boundedness of `U_s`;
- compactness/tightness;
- Lasota-Yorke inequality.

Do not invoke Keller-Liverani yet.

Missing:

- proof that `FULL_N` approximates `E_N U_s I_N`;
- mixed-norm convergence;
- uniform LY estimates;
- spectral isolation/resolvent control.

## 10. Fallback Branch

If Gate 10.B fails, the finite-rank branch remains publishable as a
rigorous finite theorem.

K16 is production:

```text
37 states,
exact CW certificate,
Lean verification,
max ratio < 3/4.
```

K20 is smoke only:

```text
42001755821431 / 62996587868160 < 3/4,
status OK,
not a production theorem.
```

## 11. Current Recommendation

Continue Branch A only as a conditional operator/Banach-space program.

Next analytic work:

1. define the prefix-average block kernel `K_N` as the provisional
   Gate-10.B object and keep ordinary adjacent blocks only as a
   diagnostic side channel;
2. decide whether the finite source averaging weight is exactly the
   projected Haar/counting measure or needs boundary/source-partition
   correction;
3. lift the component-collapsed `good/bad` convergence target to the
   retained phase/delta label kernel, or explicitly charge the gap to a
   new `ComponentLabelLift` error term;
4. extend the prefix weak-proxy trend beyond fixed `T = 15`, and check
   whether it survives changes in `T`, `j`, and source weighting;
5. explain or bypass the negative 2-adic child-cylinder signal before
   committing to a martingale-variation Banach space;
6. turn the `source_v2_odd = 2|3` concentration into an explicit
   enlarged-state candidate; the best current finite split is
   `odd = 3 and v2 in {0,2}`, whose complement has p95 `0` in the
   latest enriched-state tests;
7. ask a transfer-operator/open-systems/countable-symbolic expert
   whether `U_s` on a 2-adic martingale-variation space is viable.

Parallel work:

1. prepare the finite-rank computational note around K16;
2. keep K20 smoke separate until promoted to production;
3. avoid all claims of spectral gap or asymptotic subcriticality.

## 12. Main Working Notes

Core:

```text
notes/phase10_operator_choice.md
notes/phase10_mixed_norm_candidate.md
notes/phase10_error_decomposition.md
notes/phase10_proof_obligations.md
notes/phase10_decision_tree.md
```

Diagnostics:

```text
notes/phase10_cylinder_stability_results.md
notes/phase10_norm_constants_from_diagnostics.md
scripts/spectral_program/collatz_99_T15_B32_j64_error_budget_summary.md
scripts/spectral_program/collatz_100_T15_d2_tail4_z2_cylinder_oscillation.md
```

Fallback:

```text
notes/phase10_finite_rank_fallback.md
notes/phase10_finite_rank_note_outline.md
```

External discussion:

```text
notes/phase10_collaborator_brief.md
notes/phase10_literature_source_map.md
```
