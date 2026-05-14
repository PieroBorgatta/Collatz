# Phase 10 Proof Obligations

Date: 2026-05-13

Status: obligation checklist.  This is not a proof plan for Collatz.  It
lists what would have to be proved before the analytic Phase-10 branch
could invoke Lasota-Yorke, Hennion, or Keller-Liverani.

## 1. Gate 10.B Obligations

### 1.1 Infinite phase space

Required statement:

```text
There is a measurable/topological phase space X and a killed weighted
phase kernel K on X whose finite statistics are approximated by the
generated FULL/full_T matrices.
```

Current status: open.

Type: analytic/definitional.

Failure mode: if no such `X` and `K` can be defined without arbitrary
prefix choices, Branch A should be downgraded.

### 1.2 Projection or approximation scheme

Required statement:

```text
K_{T,a,L} = E_{T,a,L} U_s I_{T,a,L}
```

and the generated row-source finite matrix satisfies:

```text
FULL_{T,a,L,N} = K_{T,a,L} + controlled error
```

or a clearly equivalent Galerkin/Ulam/compression statement.

Current status: not established.

Type: analytic plus engineering.

Failure mode: finite matrices remain finite artifacts with no canonical
operator meaning.

### 1.3 High-bit limit convention

Required statement:

```text
The limit j -> infinity means Haar average, Cesaro block average, or a
declared non-limit finite-rank procedure.
```

Current status: candidates exist, no choice is proved.  The current
script-`88` adjacent-block diagnostics use contiguous ordinary integer
windows in the high-bit coordinate `j`.  Prefixes `0 <= j < 2^m` are
compatible with Haar measure on a finite quotient, but adjacent
ordinary intervals are not yet the same thing as a 2-adic
martingale-cylinder comparison.

The first direct child-cylinder diagnostic,
`collatz_100_T15_d3_tail2_z2_cylinder_oscillation.md`, does not show
decreasing full-label oscillation across high-bit depths.  This is
negative pressure on the naive `Z_2` martingale norm, not a proof of
failure.

The higher-tail repeat
`collatz_100_T15_d2_tail4_z2_cylinder_oscillation.md` gives the same
qualitative warning with better child samples.

Type: definitional.

Failure mode: diagnostics depend essentially on arbitrary prefix
windows.

### 1.4 Source partition compatibility

Required statement:

```text
finite diagnostic source cells refine, or are refined by, the analytic
source partition used in E_n and I_n, up to a controlled error.
```

Current status: small but not zero on tested windows.  Script `88`
groups by `(r,h)` cells.  At `T = 15`, `j = 16,32,64`, with
`odd_bits = 2`, `hit_bits = 2`, `v2_cap = 13`, exactly `8/131072`
groups have two `source_phase` states.

Type: definitional/computational.

Failure mode: the finite row-TV bridge estimates the wrong source
average.

### 1.5 Gate 10.B closure lemmas

The positive closure target for Gate 10.B is now:

```text
FULL_{T,a,L,N} approximates K_{T,a,L} = E_{T,a,L} U_s I_{T,a,L}
```

in a declared weak/mixed norm.  For the current generated `FULL`
matrices, the finite core is phase-only:

```text
||K_{2N}^{phase} - K_N^{phase}||
  _{ell_infty(phase) -> L1(omega_N)} -> 0.
```

The retained-labelled version is a stronger sufficient estimate, not
the default target for the current Lean `TransferMatrix V`.

The first proof obligations are deliberately more elementary than a
Banach theorem:

| Lemma | Required statement | Type | Status |
|---|---|---|---|
| source-measure lemma | `omega_N` is the uniform counting measure on retained complete source cells, and the excluded-cell mass is explicit | definitional/computational | verified for `T15_j64_128_L5` by script `107` |
| row-source identity lemma | script/CSV rows define exactly the prefix kernel `K_{T,a,L,N}` with the stated labels and weights | engineering/definitional | verified for `T15_j64_128_L5` by script `107` |
| component/phase/label lemma | retained row drift contracts under `label -> phase -> component`; phase drift is the current `FULL` metric | finite analytic | verified for `T15_j64_128_L5` by script `107` |
| tail split lemma | the `delta > L` part is exactly a separate weighted tail kernel | definitional/computational | verified for `T15_j64_128_L5` by script `107` |
| source-limit lemma | `omega_N` converges, or is replaced by a declared averaging convention with bounded error | analytic/computational | open |
| phase-prefix Cauchy theorem | the phase `K_N` are Cauchy in the chosen weak norm | analytic/combinatorial | open |
| Banach bridge lemma | finite `ell_infty -> L1(omega_N)` control implies the chosen `B_s -> B_w` control after `E/I` | analytic | collaborator-level |

The fixed `T = 15`, `64 -> 128` run gives the current source-measure
bookkeeping target:

```text
retained source rows = 131064,
possible source rows = 131072,
excluded fraction    = 8 / 131072.
```

This is not yet a limiting result.  It is the finite lemma that must be
proved before the report means can be treated as weak source averages.

The fixed finite source-measure estimate is:

```text
|omega_full(F) - omega_retained(F)|
  <= 2 (excluded_count / full_count) ||F||_infty.
```

For the `T = 15`, `64 -> 128` report this coefficient is:

```text
2 * 8 / 131072 = 0.0001220703125.
```

Script `107_gate10b_closure_checks.py` verifies this bookkeeping on the
latest `T15_j64_128_L5` dataset:

```text
row-source residuals = 0,
component/phase/label violations = 0/0/0,
phase_l1_mean ~= 0.0045024297,
label_l1_mean ~= 0.005743653,
tail_weight_a_mean ~= 0.000025428943,
tail_weight_b_mean ~= 0.000025392998.
```

The current phase-only prefix trend is:

```text
16->32:  0.0066310638,
32->64:  0.0055465954,
64->128: 0.0045024297.
```

With no `delta` cutoff:

```text
16->32:  0.0066438334,
32->64:  0.0055544859,
64->128: 0.0045072525.
```

This makes the next open obligation precise: prove or falsify that this
finite phase drift tends to zero in the declared weak norm.

The phase-only Gate 10.B theorem should now be organized around the
following seven hypotheses:

| ID | Obligation | Status |
|---|---|---|
| H1 | define an infinite source model `X,A,omega,D,tau,delta,pi_{T,a}` independent of finite prefixes | open |
| H2 | prove retained source cells are complete measurable cells with explicit excluded-cell error | finite check verified; limit open |
| H3 | define `K_N^{phase}` as the source-cell average of `1_D 2^{-s delta} 1_{pi tau=q}` | definitional; needs final convention |
| H4 | match `K_N^{phase}` to CSV/generated `FULL` rows with explicit residual | CSV residual zero; generated Lean matching separate |
| H5 | prove `D_N^{phase}->0` in `ell_infty(phase)->L1(omega_N)` | open; finite trend decreases |
| H6 | prove projection/inclusion constants for `E_N,I_N` from finite weak norm to `B_s->B_w` | open/collaborator-level |
| H7 | control killed/terminal and `delta>L` tail terms in the chosen norm | finite global tail small; local/uniform open |

Only H2-H4 have substantial finite bookkeeping support.  H5 is the next
computational/analytic target.  H6 is where Hennion/Keller-Liverani
expertise becomes genuinely necessary.

H4 must be split into two different matching statements.

| Object | File/source | State space | H4 status |
|---|---|---|---|
| deterministic fallback CW | `CollatzShadowing/Generated/K16S16KDeterministicCW.lean` | `Fin 37` with labels `K:b` | certified finite-rank fallback; not a `PhaseState V` `FULL` matrix |
| critical symbolic Lean import | `CollatzShadowing/Generated/T10CriticalSymbolic.lean` from `collatz_75_critical_symbolic_edges.csv` | `TransferMatrix 10` | Lean phase matrix exists, but it is the older `T=10` critical-symbolic object |
| high-bit tail Lean import | `CollatzShadowing/Generated/T10J32HighBitTail.lean` from `high_bit_tail_edges_T10_j32.csv` | `TransferMatrix 13` | Lean `full=core+tail` object exists for `T=10,j=32` |
| Phase-10 H5 diagnostics | script `107` on script-`88` CSVs | empirical phase rows for `T=15`, prefixes `16,32,64,128` | CSV row-source identity verified; no generated Lean import/matching theorem yet |

Therefore the current H4 conclusion is:

```text
CSV-internal K_N^{phase} identity: verified for script-88/107 data.
Generated-Lean FULL matching for the T=15 phase-prefix kernels: open.
K16 deterministic CW: separate finite-rank fallback, not H4.
```

There is an additional source-quotient obstruction.  The script-`107`
source set is made of retained cells `(T,r,h)`.  A `TransferMatrix V`
uses only source `PhaseState V`.  The finite error incurred by replacing
each source-cell row by the average row of its source phase is:

```text
T=15, delta<=5
j=16:  mean 0.055610515, p95 0.27152777,
j=32:  mean 0.054357070, p95 0.27914786,
j=64:  mean 0.052910359, p95 0.27929920,
j=128: mean 0.051512269, p95 0.27979821.
```

This error is much larger than the prefix drift `D_N^{phase}`.  Hence
H4 is not merely missing a Lean import.  It also needs one of:

- a proof that source-phase collapse error tends to zero under further
  refinement;
- a refined source alphabet, beyond the current `PhaseState V`;
- an explicit decision to treat the `PhaseState` matrix as an averaged
  finite-rank object rather than a projection.

Script `108_source_refinement_collapse.py` gives the current best finite
source-refinement candidates.  On `T=15`, `64->128`, `delta<=5`:

| source key | `j=128` collapse mean | mean cells/key | status |
|---|---:|---:|---|
| `PhaseState` | `0.051512269` | about `1170` | too coarse |
| `PhaseState + r mod 2^10` | `0.020415877` | `31.75` | plausible finite refinement |
| `PhaseState + r mod 2^11` | `0.018202554` | `15.95` | plausible but finer |
| `PhaseState + r mod 2^12` | `0.015742233` | `7.99` | useful diagnostic, close to over-refinement |

The no-cutoff version is essentially unchanged.  This points to low
source-residue refinement, not to a large-`delta` tail artifact.

Script `109_refined_prefix_cauchy.py` adds the missing comparison
between prefix lengths for the same candidate source keys.  On
`T=15`, `64->128`, `delta<=5`, source-cell-weighted destination-phase
drift is:

| source key | weighted prefix drift | status |
|---|---:|---|
| `PhaseState` | `0.000200738344` | most stable, but high collapse error |
| `PhaseState + r mod 2^10` | `0.00158494699` | plausible compromise |
| `PhaseState + r mod 2^11` | `0.00210468651` | finer, more drift |
| `PhaseState + r mod 2^12` | `0.00260800395` | near over-refinement |
| `source_cell` | `0.00450242969` | overfit baseline |

The `16->32->64` run gives decreasing refined drift for the selected
keys, for example `r mod 2^10` goes
`0.00302166308 -> 0.00215625513`.  This supports further testing, but it
does not remove the H4/H5 burden.  A positive theorem must state which
source alphabet is used and prove both source-collapse control and
prefix-Cauchy control for that same alphabet.

### 1.6 Branch freeze: `A0` and `A1`

At this point the analytic branch should be split into two named
sub-branches.  This prevents the project from mixing the best feature of
one quotient with the best feature of another.

Let `S_N` be the retained source-cell set and let

```text
k_N^{cell}(i,q)
```

be the empirical weighted destination-phase row for source cell
`i in S_N` and destination phase `q`.  Let `omega_N` be the uniform
source-cell measure used by the diagnostics.  For a source-key map
`rho_b:S_N -> A_b`, define the averaged quotient row

```text
K_N^b(a,q)
  = (1 / |rho_b^{-1}(a)|)
      sum_{i:rho_b(i)=a} k_N^{cell}(i,q).
```

The two finite errors to keep separate are:

```text
C_N^b
  = sum_i omega_N(i)
      sum_q |k_N^{cell}(i,q)-K_N^b(rho_b(i),q)|,

P_N^b
  = sum_a m_N^b(a)
      sum_q |K_{2N}^b(a,q)-K_N^b(a,q)|.
```

Here `C_N^b` is the source-collapse error, and `P_N^b` is the
prefix-Cauchy drift for the chosen source alphabet.  The finite
diagnostics use the common source keys and source-cell-count weights;
any theorem must state the exact limiting convention.

Branch `A0` is the existing `PhaseState` branch:

```text
rho_0(i) = source_phase(i).
```

Its advantage is compatibility with the current Lean `TransferMatrix V`
state space.  Its measured prefix drift is very small.  Its defect is
that `C_N^0` is about `0.05` at current scales and is not yet shown to
decay.  Therefore `A0` can close Gate 10.B only if one proves either:

```text
C_N^0 -> 0
```

in the declared weak source norm, or a theorem saying that the
`PhaseState` matrices are intentionally averaged finite-rank objects and
that this averaging is the right approximation to the infinite operator.

Branch `A1` is the first refined-source branch:

```text
rho_10(i) = (source_phase(i), r(i) mod 2^10).
```

Its advantage is a much smaller source-collapse error.  Its defect is
that it is not currently a square finite transfer matrix: the script-`88`
CSV records destination `PhaseState`, not the destination low residue
coordinate.  Thus `A1` is presently a rectangular diagnostic kernel

```text
A_10 -> PhaseState,
```

not a spectral object comparable to `TransferMatrix V`.  To turn `A1`
into an operator branch, the data generator must record a compatible
destination refinement, for example a destination low-residue key after
the first return, or the theory must prove that a rectangular
finite-to-Banach bridge is sufficient for the intended weak approximation.

Current recommendation:

```text
A0 remains the branch for the existing FULL/Lean objects.
A1 is the first serious diagnostic refinement and possible next operator
branch, but it needs new destination-refined data before any spectral
claim can be attached to it.
```

The first destination-refined smoke test is now available as
`110_refined_square_probe.py`.  It retraces rows and builds square
kernels on `(PhaseState,t mod 2^b)`.  On `T=12`, `j=16,32,64,128`, the
weighted prefix drifts are:

| bits | `16->32` | `32->64` | `64->128` | interpretation |
|---:|---:|---:|---:|---|
| `0` | `0.00138619007` | `0.00109704799` | `0.000647069352` | phase-only baseline |
| `5` | `0.00493992965` | `0.00344425218` | `0.00232221302` | refined but noisier |
| `8` | `0.0123695007` | `0.0114045768` | `0.0101905453` | high drift |
| `10` | `0.0152083349` | `0.0135561906` | `0.0129098735` | high drift, decreasing slowly |

This smoke test does not kill `A1`, because the drift decreases with
prefix size.  It does mean that an `A1` spectral program would have to
pay a much larger finite drift constant than `A0`, at least at this
scale.  The `T=13`, `16->32` repeat matches the `T=12`, `32->64`
numbers and should be treated as a window-consistency check, not as
independent asymptotic evidence.

The component/phase/label finite lemma is also fixed.  If projections
collapse retained labels first to phase and then to `{G,B}`, then:

```text
||pi_*p - pi_*q||_1 <= ||p - q||_1,
LabelExcess(p,q) = ||p-q||_1 - ||pi_*p-pi_*q||_1.
```

Thus good/bad component prefix convergence is insufficient by itself.
For the existing `FULL` matrices the project must prove phase-prefix
convergence, or prove that the component-to-phase excess tends to zero.
The retained-label excess is a stronger diagnostic/error term for the
optional labelled-symbolic branch.

The row-source identity is also fixed at the script layer:

```text
K_N(source, signature)
  = (1/N) sum_{0 <= j < N}
      1_{full(t_j,h)=signature} weight(t_j,h).
```

Scripts `105`, `106`, and `107` read `weight_sum / sample_count`, so
they are exactly measuring this empirical row-source kernel after
component collapse, phase collapse, or retained-label lift.  The
remaining open point is not the CSV identity; it is the equality or
approximation:

```text
K_N ?= E U_s I.
```

The retained-tail split is:

```text
K_N = K_N^{<=L} + K_N^{>L},
|(K_N - K_N^{<=L})f(source)|
  <= K_N^{>L}(source, all labels) ||f||_infty.
```

This gives weak source-averaged tail control from the global weighted
tail, but not a uniform sourcewise tail bound.

The finite-to-Banach bridge has now been reduced to projection constants.
For a labelled row-drift diagnostic define:

```text
D_N = sum_i omega_N(i) sum_y |K_{2N}(i,y)-K_N(i,y)|.
```

If:

```text
||E_N f||_infty <= C_E ||f||_s,
||I_N g||_w <= C_I ||g||_{L1(omega_N)},
```

then:

```text
||I_N (K_{2N}-K_N) E_N||_{B_s -> B_w}
  <= C_E C_I D_N.
```

The finite report supplies `D_N`; the analytic missing piece is proving
usable `C_E,C_I` and the convergence of the source measures/norms.

Before proving those constants, the project must choose the label
interpretation:

```text
phase-only bridge:
  test functions ignore delta after the weight has been applied;

labelled-symbolic bridge:
  retained return labels are part of the symbolic state/edge space.
```

The two choices require different infinite objects.  A proof for one
does not automatically close Gate 10.B for the other.

For the current generated `FULL` matrices, the phase-only bridge is the
primary obligation.  This follows from the Lean type:

```text
TransferMatrix V = Matrix (PhaseState V) (PhaseState V) NNReal.
```

Thus retained `(phase, delta)` labels are proof diagnostics/error-control
data unless the project explicitly constructs a new labelled-symbolic
operator.  The labelled Cauchy theorem remains useful as a sufficient
stronger estimate, but Gate 10.B for the existing `FULL` certificates
should first be attempted in the phase-only weighted norm.

## 2. Operator Obligations

### 2.1 Kernel measurability

Required statement:

```text
src -> K(src, A)
```

is measurable for each target set `A`, including terminal/killed
events.

Current status: open.

Type: analytic/combinatorial.

### 2.2 Label measurability

Required statement:

```text
delta(src)
```

or the labelled transition law is measurable on the chosen cylinder or
symbolic sigma-algebra.

Current status: open.  Diagnostics show that `delta` is not safely a
hidden finite source coordinate.

Type: combinatorial/analytic.

### 2.3 Orientation convention

Required statement:

```text
The analytic operator is U_K, and every row-source finite matrix is
matched to U_K through K(src,dst).
```

Current status: provisionally fixed in `notes/phase10_operator_choice.md`.
`P_K^*` is retained as the dual mass operator.  `L_K` is secondary.

Type: definitional.

Failure mode: proving a theorem for the transpose of the intended
operator.

## 3. Banach-Space Obligations

### 3.1 Strong norm

Required statement:

```text
B_s is a Banach space and U_s is bounded on B_s.
```

Candidate: martingale/cylinder BV or weighted symbolic Holder on
`Z_2 x H` / labelled symbolic space.

Current status: not proved.

Type: analytic.

### 3.2 Weak norm

Required statement:

```text
B_s embeds continuously into B_w, and the finite diagnostics estimate
the B_s -> B_w error rather than an unrelated statistic.
```

Current status: finite row-TV has a candidate bridge for bounded
observables:

```text
|(K v)(i) - (K' v)(i)| <= 2 TV_i(K,K') ||v||_infty.
```

This supports an `ell_infty -> L1` or bounded-test weak norm if the
source-cell averaging weights are specified.  It does not give a
supremum/operator-norm estimate from p95 diagnostics alone.

Type: analytic.

### 3.3 Compactness or tightness

Required statement:

```text
unit ball of B_s is relatively compact in B_w
```

or a Hennion-compatible substitute.

Current status: open.

Type: analytic/collaborator-required.

Failure mode: Hennion cannot be invoked.

### 3.4 Tail/drift weight

Required statement:

```text
large-delta and bad-source strata are controlled by a summable or
drift-compatible weight W.
```

Current evidence:

- `DeltaTail_global(5)` is small on tested windows;
- `DeltaTail_local_max(5)` can still be `1`;
- the naive source-stratum drift family is weak on `T15_j16`.

Current status: open, with negative pressure on naive weights.

Type: analytic/computational.

### 3.5 Block-kernel decomposition

Required statement:

```text
K = [[K_GG, K_GB],
     [K_BG, K_BB]]
```

acts boundedly on a chosen vector-valued or block-weighted Banach pair,
or else `K_bad` is replaced by a declared finite-rank/exceptional
subsystem with controlled coupling errors.

Current evidence:

- the candidate bad set `odd = 3 and v2 in {0,2}` explains most of the
  full-over-phase excess;
- over `0 < t < 2^21`, the finite component budgets are
  `K_GG = 0.012281296`, `K_GB = 0.0054655765`,
  `K_BG = 0.040839452`, `K_BB = 0.018100693`;
- `K_bad` is not a small isolated tail.

Current status: open.  This is now a necessary proof obligation for the
two-component Branch-A formulation.

Type: analytic/computational/collaborator-required.

Minimal block-norm target:

```text
||f||_{s,eta} = max(||f_G||_{s,G}, eta ||f_B||_{s,B})
```

with block LY constants forming

```text
A_eta =
[[a_GG, eta^{-1} a_GB],
 [eta a_BG, a_BB]].
```

The required theorem would be `rho(A_eta) < 1` after all `a_ij` are
proved analytic constants.  The empirical component matrix from script
`103` is not `A_eta`; it is only evidence that all four block terms are
non-negligible enough to name.

Finite evidence from script `104`:

```text
weighted block row-L1 mean:
B=8  -> 0.012046521,
B=16 -> 0.0095367816,
B=32 -> 0.0074155295.
```

This supports trying to prove a mixed-norm block approximation.  It does
not supply any analytic `a_ij`.

The `B=16`, `j=64` multipair run has pair means
`0.009535642`, `0.013903232`, `0.018206286`, so a proof obligation must
state the averaging/limit convention explicitly.  A uniform
adjacent-block Cauchy statement is not currently supported.

For the prefix/Cesaro convention, the immediate proof obligation is:

```text
||K_{2N} - K_N||_{B_s -> B_w} -> 0
```

for the block-valued kernel.  Finite evidence is:

```text
16->32 mean 0.004767821,
32->64 mean 0.0037076395.
```

At the present level this should be read first in the weaker finite
form:

```text
sum_c omega_N(c)
  sum_{tau in {G,B}}
    |K_{2N}(c,tau) - K_N(c,tau)|
  -> 0.
```

The analytic upgrade requires four additional obligations:

| Obligation | Type | Current status |
|---|---|---|
| define the limiting source weight `omega` | analytic/definitional | open |
| prove finite `omega_N` converges to `omega` | analytic/computational | open |
| lift `{G,B}` convergence to retained labels | analytic/computational | open |
| embed the finite proxy into `B_s -> B_w` | analytic/collaborator-required | open |

The prefix diagnostic can support a Gate-10.B branch only if these four
items are stated and attacked.  Without them, script `105` remains a
finite consistency check rather than an operator approximation theorem.

Script `106_prefix_label_lift.py` shows that the label-lift obligation
is real on the current `T = 15` data:

```text
label_excess mean = 0.0033207547,
label_excess p95  = 0.017578125,
label_excess p99  = 0.046875.
```

The `delta <= 5` repeat gives essentially the same values, so this
obligation cannot be discharged merely by citing the global large-delta
tail.  It requires a retained-label variation argument or an explicit
weak error term.

The later `64->128` prefix run improves the finite values:

```text
label_excess mean = 0.0029977961,
label_excess p95  = 0.015625,
label_excess p99  = 0.03125.
```

This is positive for the prefix branch, but it is still an obligation,
not a theorem: the source measure, label space, and `B_s -> B_w` bridge
remain undefined at proof level.

## 4. Lasota-Yorke Obligations

Target inequality:

```text
||L f||_s <= alpha ||f||_s + C ||f||_w,
alpha < 1.
```

or the corresponding statement for `U_K`.

The bookkeeping decomposition would have to justify something like:

```text
alpha <= alpha_depth(a)
       + C1 DeltaTail_global(L)
       + C2 DeltaTail_local(L)
       + C3 A_phase_block(B)
       + C4 A_label_bounded(B,L)
       + C5 BoundaryError(T,a,L,B)
       + C6 DriftExcess(W)
       + C7 BlockCoupling(G,B).
```

Current status: no Lasota-Yorke inequality is proved.

Missing lemmas:

| Lemma | Type | Current status |
|---|---|---|
| boundedness of killed operator | analytic | open |
| cylinder-depth contraction or bounded variation control | analytic/combinatorial | open |
| global large-`delta` summability | analytic/computational | only finite evidence |
| local tail/tightness estimate | analytic/computational | hard obstruction remains |
| retained-label variation estimate | analytic/computational | finite proxy exists |
| killed-boundary regularity | analytic | open |
| source-stratum drift inequality | analytic/computational | naive family weak |
| block-kernel coupling bound | analytic/computational | finite budget only |
| exceptional-cell mass control | computational/analytic | open |

## 5. Hennion Skeleton Obligations

Conditional skeleton:

```text
Assume:
1. L is bounded on B_s and B_w;
2. B_s -> B_w is compact or Hennion-compact;
3. ||L^n f||_s <= A alpha^n ||f||_s + C ||f||_w;
4. alpha < 1.

Then:
essential spectral radius of L on B_s is <= alpha.
```

Local missing hypotheses:

- actual infinite `L`;
- Banach pair;
- compactness/tightness;
- iterated LY inequality;
- treatment of killed mass;
- tail/drift summability.
- block coupling or finite-rank/exceptional treatment of `K_bad`.

Failure modes:

- `L` is unbounded on the chosen strong space;
- compact embedding fails because the symbolic alphabet/tail is too
  large;
- local tails destroy uniform estimates;
- killing creates irregular boundaries;
- retained labels have nonsummable variation.

## 6. Keller-Liverani Skeleton Obligations

Conditional skeleton:

```text
Assume:
1. L_N and L act on B_s and B_w;
2. sup_N ||L_N^n||_s satisfies a uniform LY bound;
3. ||L_N - L||_{B_s -> B_w} -> 0;
4. resolvent bounds hold on the spectral contour of interest.

Then:
isolated spectral data of L_N converge/stabilize near those of L.
```

Local missing hypotheses:

- definition of `L`;
- proof that generated matrices are `L_N`;
- mixed-norm convergence;
- uniform LY constants;
- spectral isolation;
- orientation consistency.

Failure modes:

- finite matrices are only prefix artifacts;
- `L_N` converges only weakly along selected subsequences;
- p95 diagnostics cannot be upgraded to operator norm or controlled
  exceptional mass;
- no isolated spectral object exists to stabilize;
- the finite spectral radius is dominated by a killed finite artifact.

## 7. Finite-Rank Fallback Obligations

These are much more concrete.

Already satisfied for production K16:

- deterministic residue-cell enumeration;
- exact JSON CW certificate;
- generated Lean import;
- Lean finite spectral-radius theorem.

Still needed for a standalone note:

- precise prose definition of the finite residue-cell model;
- exact Lean-generation command or artifact policy;
- external artifact hashes/manifest;
- clear distinction between production K16 and K20 smoke;
- optional Lean imports for sensitivity checks.

## 8. Current Branch Recommendation

Analytic Branch A:

```text
continue only as a conditional operator/norm program.
```

Finite-rank Branch B:

```text
prepare as the reliable theorem-producing deliverable.
```

Collaboration:

```text
ask a transfer-operator/countable-symbolic/open-systems analyst whether
the Gate-10.B kernel/projection problem has a natural solution or should
be abandoned.
```

## 9. Immediate Next Proof-Obligation Work

1. Decide whether the weak norm is distributional with exceptional-cell
   mass or a genuine supremum/operator norm.
2. Prove or falsify the bridge from row-TV diagnostics to the chosen
   `B_s -> B_w` norm for `U_s`.
3. Try to prove or falsify local tail control for `DeltaTail_local`.
4. Try a better drift/tail weight only if it has a mathematical form,
   not merely a fitted diagnostic role.
5. If no projection statement emerges, freeze Branch A and write the
   finite-rank note.
