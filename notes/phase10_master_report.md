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

2026-05-25 A0 weak-bridge update: the high-`v2` source-tail mass for the
current A0 source model is now an exact count, formalized in Lean as
`WeakBridge.TailCount.dyadic_tail_count_mul_le`.  The remaining A0
target has been sharpened by scripts `118`-`122` to a dyadic
top-Haar/block-discrepancy statement:

```text
for every fixed low-v2 source phase p,
  ||mean_[N,2N) K_p - mean_[0,N) K_p||_1 -> 0.
```

Script `122` rewrites the current script-`111` A0 data in this form.
The aggregate threshold exponents are near `0.6`; for `v2 < 8`, the
latest root-Haar component is `0.0005326722352`, about `93.2%` of the
total latest root drift.  This is finite evidence only.  The missing
mathematical step is a structural dyadic discrepancy lemma for
bounded/medium-depth Syracuse return signatures.

The first precise candidate is recorded and corrected in
`notes/phase10_A0_dyadic_discrepancy_lemma_2026-05-25.md`: after fixing a
return-depth cutoff `S` and an intermediate valuation cap `A`, the bounded
congruential signature should be exactly periodic modulo some `2^M`.
Script `123` confirms this for the pure valuation word: for `S=25,A=8`,
all tested phases have zero valuation-word mismatches at large `m`
(`m=192,193,200`).  But the actual weighted kernel is not purely 2-adic:
bit-growth weights `2^-delta` and the terminal/drop test are archimedean.
The residual bounded-kernel mismatches (`0/128` to `9/128` in the large-m
sample) identify a separate boundary term.  Intermediate high-valuation
tails should be controlled by modular counting (`<= S * 2^-A`).  The
remaining hard theorem is return-depth tail control plus this
archimedean boundary estimate.

Script `124` improves that picture: the symbolic return-depth tail is
pessimistic because it ignores drops below `n0`, whereas the killed kernel
maps drops to the zero row.  With distributed block sampling on the grid
`S in {10,25,50,75}`, `A in {4,6,8,10}`, the pure valuation-word mismatch
is zero throughout with the chosen large periods.  At `S=75,A=10`, the
symbolic return-tail mean is `0.5`, but the killed-kernel unresolved tail
mean is `0`; two tested phases are full-return phases and two are
full-drop phases in the distributed sample.

Script `125` then decomposes the remaining killed-kernel mismatch.  It is
not caused by destination-label changes, not by drop/return flips, and not
by tail/return boundaries.  For all tested `(S,A)`, all nonzero pointwise
kernel L1 is `delta_only`: the destination label is identical, but the
weight `2^-delta` changes.  At `S=75,A=10`, aggregate point L1 mean is
`0.02276611328`, with nonzero rate `0.1821289062`.  Thus the active
bottleneck has sharpened to a bit-length/`delta` boundary lemma for
returning phases.

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

The larger-prefix update at `T=14`, `j=32->64` keeps the same qualitative
picture:

```text
b=0:  0.000420440901
b=5:  0.00160995368
b=8:  0.00848590605
b=10: 0.0121733793
```

Thus the A1 refined-square drift still decreases when the prefix size is
increased, but `b=10` remains roughly `29` times the phase-only drift on
this window.

Script `111_refined_square_key_drift_inspector.py` then decomposes the
same `T=14`, `j=32->64`, `b=10` drift by refined source key.  It rules out
the simplest exceptional-list explanation:

```text
top 10 source-key contribution  = 0.0822067093
top 25 source-key contribution  = 0.131231692
top 100 source-key contribution = 0.254601736
```

The obstruction is instead broad but structured.  Aggregating phase strata
by `(v2, odd mod 4)`, the four families

```text
0|3, 0|1, 1|3, 1|1
```

explain about `0.759884454` of the total `b=10` drift.  Therefore a
serious A1 theorem should not try to delete a short list of bad residues.
It should introduce a source-family weighted weak norm or a two-level
quotient that controls low-`v2`/odd-residue families explicitly.

Script `112_family_weighted_norm_probe.py` tests that idea directly on
the same finite window.  It separates two quantities:

```text
source_weighted_l1:
  average row L1 after reweighting source mass by V(src)

operator_weighted_l1:
  average of sum_dst |Delta K(src,dst)| V(dst)/V(src)
```

The second quantity is the relevant finite proxy for a weighted strong
norm.  The result is negative for simple source-family weights.  Weighting
the dominant four families, or equivalently all `v2 <= 1` families on this
window, worsens the operator proxy:

```text
identity operator mean     = 0.0121733793
dominant4_x1.25 mean       = 0.0122560449
dominant4_x1.50 mean       = 0.0124930228
dominant4_x2.00 mean       = 0.0131984470
```

The best tested operator-weighted candidate is not a source-family weight
but the fitted residue band `rlo mod 32 in {6,26}`:

```text
rlo_mod32_6_26_x1.5 mean  = 0.0118894199
relative improvement      = 0.0233262632
operator p95              = 0.0373992920
operator max              = 0.638671875
rows worsened             = 0.441005803
```

This is too small and too fitted to be the main theorem path.  Therefore
`A1` remains a diagnostic/refinement branch, while the main Gate-10.B
program returns to the phase-only `A0` weak averaged bridge.

The first larger A0 follow-up is positive.  Re-running the same square
probe with `b=0` only at `T=14`, `j=32,64,128` gives:

```text
j=32 -> 64:
  weighted_l1_mean = 0.000420440901
  weighted_l1_p95  = 0.000633001328
  weighted_l1_p99  = 0.00498771667
  weighted_l1_max  = 0.0309139785

j=64 -> 128:
  weighted_l1_mean = 0.000285774472
  weighted_l1_p95  = 0.000561684370
  weighted_l1_p99  = 0.00205135345
  weighted_l1_max  = 0.0331541219
```

This is the cleanest current finite signal for A0: the weak averaged
phase-only prefix drift decreases at the next scale.  The rare-row maximum
does not decrease monotonically, so the correct target remains weak
averaged control with an exceptional-source tail, not uniform row-TV.

The matching key-drift inspection of the `64->128`, `b=0` comparison shows
that this rare-row maximum is indeed sparse.  The largest row drift comes
from the four high-`v2` phases `14|3|h`:

```text
row L1        = 0.0331541219
sample weight = 47
```

while the high-contribution average drift is carried by low phases such as
`0|3|h`, `1|3|h`, and `0|1|h`.  This splits the A0 obstruction into the
right shape for a weak theorem:

```text
mean drift: low-phase structural families
max drift: sparse high-v2 exceptional tail
```

The finite row-source bridge itself is now formalized in Lean:

```text
lean/CollatzShadowing/WeakBridge.lean
```

Main theorem:

```text
CollatzShadowing.WeakBridge.weighted_action_diff_le
```

It proves the exact finite estimate used by the A0 program.  For finite
row-source kernels `K,L`, nonnegative source weights `mu`, and any
observable satisfying `|f| <= C`:

```text
sum_i mu(i) |(Kf)(i) - (Lf)(i)|
  <= C * sum_i mu(i) sum_j |K(i,j) - L(i,j)|.
```

Therefore the script-`110` value `D_N = weighted_l1_mean` is already the
finite `ell_infty -> L1(mu_N)` operator error.  The unresolved part is not
this finite inequality; it is proving `D_N -> 0`, controlling the sparse
high-`v2` exceptional rows, and constructing Banach projection/inclusion
maps with constants independent of `N`.

The resulting conditional theorem target is now recorded as
`notes/phase10_A0_weak_approximation_theorem_2026-05-25.md`.  Its named
assumptions are:

```text
A0W1 finite kernel identification,
A0W2 D_N -> 0,
A0W3 exceptional-source tail,
A0W4 tail/killing control,
A0W5 projection bound,
A0W6 inclusion bound,
A0W7 limit operator convention.
```

Under these assumptions the theorem gives:

```text
|| I_N (K_{2N} - K_N) E_N ||_{B_s -> B_w}
  <= C_E C_I (D_N + r_N + tau_{N,L} + exceptional_tail_N).
```

This is now the precise Gate-10.B target.  It is still conditional, but
the computational term entering the theorem is no longer ambiguous.

Script `113_A0_decay_law_probe.py` estimates the current finite decay of
that computational term from the available script-`110` A0 by-pair CSVs.
After deduplicating equivalent prefix scales by `N = j_left * 2^T`, five
scales fit:

```text
D_N ~= c N^{-alpha}
alpha = 0.594000397
c     = 1.07934526
R^2   = 0.989858124
```

Robustness checks are compatible with the same scale:

```text
local-alpha median      = 0.589521649
leave-one-out alpha min = 0.571758588
leave-one-out alpha max = 0.644405036
```

This is finite evidence for A0W2, not a theorem.  The conservative analytic
target suggested by the data is:

```text
D_N <= C N^{-1/2+epsilon}
```

plus an exceptional high-`v2` tail estimate.  The rate being close to
`1/2` is useful but also a warning: it may reflect Cesaro/averaging
fluctuation rather than a spectral gap.

Script `114_A0_high_v2_tail_split.py` then quantifies the exceptional-tail
side on the latest A0 `T=14`, `64->128`, `b=0` key-drift data.  For
thresholds `{v2 >= R}`:

```text
R=10: tail mass 0.0009759273, contribution 0.0332404560
R=12: tail mass 0.0002435050, contribution 0.0137910747
R=14: tail mass 0.0000603994, contribution 0.0048224593
```

The family carrying the maximum row drift, `14|3`, has mass
`0.0000298818` and contribution `0.0034667383`, with row `L1`
`0.0331541219`.  Meanwhile the largest average contributions are low
phases (`0|3`, `1|3`, `0|1`).  This supports the proof decomposition:

```text
D_N <= D_N(v2 < R) + 2 * mu_N(v2 >= R).
```

The analytic task is now sharply split: prove low-phase decay and prove a
uniform high-`v2` source-mass tail.

Script `115_A0_decomposition_decay_probe.py` tests this split across all
available A0 phase-strata scales:

```text
N = 65536, 131072, 262144, 524288, 1048576.
```

For every tested threshold `R`, the low component decays with exponent near
`0.6`:

```text
R=4:  low alpha 0.611642619
R=6:  low alpha 0.618811958
R=8:  low alpha 0.599275586
R=10: low alpha 0.595091262
R=12: low alpha 0.597682614
R=14: low alpha 0.595226457
```

But the fixed-threshold tail mass does not decay with `N`; its fitted
exponent is near zero.  This corrects the theorem shape.  The A0 target is
not a single limit in `N` for a fixed tail threshold, but a double-limit
statement:

```text
lim_{R -> infinity} limsup_{N -> infinity}
  [D_N(v2 < R) + 2 * mu_N(v2 >= R)] = 0.
```

At the latest scale, `R=14` is already a reasonably tight proof-style split:

```text
observed D_N       = 0.000285774472
D_N(v2 < 14)       = 0.000284396336
2 * mu_N(v2 >= 14) = 0.000120798824
bound / observed   = 1.41788438
```

Script `117_A0_v2_tail_formula.py` closes the second half for the current
finite source model.  The high-`v2` mass is not a fitted law; it is exact
counting.  For a script-`111` comparison with

```text
L = j_left * 2^T,
R = j_right * 2^T,
t=0 excluded,
```

the source tail is exactly:

```text
mu(v2 >= q)
  = (floor((L - 1)/2^q) + floor((R - 1)/2^q)) / (L + R - 2)
  <= 2^-q.
```

The verification against all current A0 phase-strata CSVs has max
observed-formula error `0`.  The integer core is formalized in Lean as:

```text
CollatzShadowing.WeakBridge.TailCount.dyadic_tail_count_mul_le
```

So the sharpest current A0 route is now: prove low-`v2` decay for every
fixed threshold, then use the exact dyadic tail and take the double limit.

Scripts `118_A0_low_v2_phase_decay_probe.py` and
`119_A0_low_v2_return_depth_probe.py` begin that remaining low-`v2`
attack.  Script `118` fits the phase-by-phase decay from the existing
script-`111` phase strata.  For `v2 < 8`, the median per-phase alpha is:

```text
0.6112066004
```

The dominant latest low phases are the mass families `0|3|h`, `1|3|h`,
`0|1|h`, and `2|1|h`.  The slowest fitted low phases are currently:

```text
7|3|h: alpha 0.2298668295
7|1|h: alpha 0.3420981079
6|1|h: alpha 0.4064120870
3|1|h: alpha 0.4142787183
```

These slow phases are not the dominant mass contributors at the latest
scale, but they are the first candidates to isolate if low-`v2` decay
fails.

Script `119` retraces four representative phases:

```text
0|3|0, 1|3|0, 3|1|0, 7|3|0.
```

For all four, it finds:

```text
prefix_l1 / half_l1 = 0.5.
```

Thus the measured A0 prefix drift is exactly ordinary dyadic block
discrepancy:

```text
K_[0,2N) - K_[0,N)
  = (1/2) * (K_[N,2N) - K_[0,N)).
```

The top drift bins are not long-return tails.  They are mostly medium
returns:

```text
step 11-25,
delta 0 or delta 1-3.
```

So the next proof mechanism is probably not another tail estimate.  It is
a bounded-depth residue-period or dependency-depth discrepancy lemma:

```text
bounded-depth return signatures have vanishing dyadic block discrepancy
inside each fixed source phase.
```

Script `120_A0_dependency_depth_probe.py` tests the naive version of that
idea directly by grouping selected phases by `t mod 2^m`.  The result is
not clean local constancy.  For the dominant phase `0|3|0`, return-phase
majority error behaves as:

```text
m=8:   error 0.712411342, singleton 0
m=12:  error 0.410966196, singleton 0
m=16:  error 0.247757128, singleton 0.202980411
m=20:  error 0.046751945, singleton 0.389220953
```

For the medium-return subset, error remains large until the cells are
already highly sparse:

```text
m=18: error 0.256938037, singleton 0.765021584.
```

Thus the simple claim "bounded-depth signatures depend on few low 2-adic
bits" is probably false or too weak.  The more plausible low-`v2` proof
route is now:

```text
2-adic discrepancy / Walsh-Haar cancellation
```

for bounded-depth signature functions over dyadic blocks.

Script `121_A0_walsh_haar_probe.py` computes that spectrum directly for
the same two phases.  It confirms that the root Haar coefficient is exactly
the half-block discrepancy from script `119`:

```text
0|3|0 return/phase:
  root half L1 = 0.000413223985
  prefix L1    = 0.000206611992

7|3|0 return/phase:
  root half L1 = 0.007874965668
  prefix L1    = 0.003937482834
```

But the full signal is not smooth in the naive spectral sense.  For
`0|3|0`, the finest two Haar levels carry about `0.4999` and `0.2504` of
the `L2` Haar energy; the root share is only about `4.7e-7`.  For `7|3|0`,
the same phenomenon appears, with root share about `3.5e-4`.

This means the proof target should not be "the signal has little
high-frequency content."  It should be the sharper dyadic-block statement:

```text
for each fixed low-v2 phase,
|| average over [0,N) - average over [N,2N) ||_1 -> 0.
```

In other words, A0W2 is a top-Haar-coefficient decay problem.

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

Decision update 2026-06-04: Branch A should continue only as a conditional
operator/Banach-space or finite-rank publication track.  It should not be
presented as a path to the pointwise Collatz statement unless a separate
distributional-to-pointwise theorem is discovered.

For the Collatz proof attempt, the current branch is the pointwise A0
first-barrier program.  The hard gate is not more finite `T` data; it is the
aperiodic obstruction.  Periodic phantom shadowing is excluded by the fixed
point equation `(2^A - 3^L) q = C`, but an infinite aperiodic valuation word
has only a 2-adic limit `xi_W` and no known algebraic rigidity excluding
positive integer realizations.  The next mathematical test is whether
first-barrier minimality plus the A0 congruence/threshold package yields a
constraint on aperiodic `xi_W` beyond the classical parity-vector residue
description.  If not, the pointwise branch should be reported as an exact
isolation of the classical aperiodic obstruction, not as a proof route.
The periodic boundary is now Lean-checked in post-prefix form:
`NoInfinite.lean:no_positive_endpoint_eventually_periodic_expansive_congruence`
excludes any positive endpoint from remaining in all congruence classes of an
expansive phantom period.  This theorem marks the useful boundary of the
current phantom sign argument: eventually periodic expansive behavior is
excluded; aperiodic infinite concatenation is not.

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
