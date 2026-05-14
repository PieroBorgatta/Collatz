# Phase 10 Error Decomposition Target

Date: 2026-05-13

Status: conditional bookkeeping note.  This is not a theorem, not a
Lasota-Yorke estimate, and not a Keller-Liverani approximation result.
Its purpose is to make every future diagnostic say which analytic error
it is meant to control.

## 1. Intended Approximation Statement

The current analytic branch uses a killed labelled high-bit kernel.  A
typical finite approximant has the form

```text
K_{T,a,L,N}
```

where:

- `T` is the base stopping-depth parameter;
- `a` is extra 2-adic source-cylinder depth;
- `L` is the retained return-exponent cutoff;
- `N` is the high-lift averaging window or block size;
- terminal mass is killed or recorded as an absorbing state, depending
  on the chosen weak norm.

The target approximation statement, if an infinite operator `U_s`
exists, should now be read in row-source/function-side convention:

```text
|| U_s - I_{T,a,L,N} FULL_{T,a,L,N} E_{T,a} ||_{B_s -> B_w}
  <= epsilon(T,a,L,N),
```

with a specified order of limits.  The current diagnostics do not yet
justify any order of limits.

If the ideal projected kernel can be defined, the cleaner two-step
statement is:

```text
K_{T,a,L} = E_{T,a,L} U_s I_{T,a,L},
```

and

```text
|| U_s - I K_{T,a,L} E ||_{B_s -> B_w}
+ || I (K_{T,a,L} - FULL_{T,a,L,N}) E ||_{B_s -> B_w}
  <= epsilon(T,a,L,N).
```

The first term is the analytic projection/truncation error.  The second
term is the empirical/high-lift approximation error.

## 2. Decomposition Template

A useful error budget should split as

```text
epsilon(T,a,L,N)
  <= C0 A_projection(T,a)
   + C1 A_phase_block(T,a,N)
   + C2 A_label_bounded(T,a,L,N)
   + C3 DeltaTail_global(T,a,L,N)
   + C4 DeltaTail_local(T,a,L,N)
   + C5 BoundaryError(T,a,N)
   + C6 DriftExcess(T,a,W,N)
   + C7 OrientationError(T,a,L,N)
   + C8 SourcePartitionError(T,a,N)
   + C9 BlockCoupling(T,a,N).
```

This formula is only a naming scheme.  The constants `C_i` do not exist
until the phase space, strong norm, weak norm, projections, and
orientation convention are fixed.

After `notes/phase10_operator_choice.md`, `OrientationError` should be
zero for the row-source `FULL` layer if future formulas consistently
use `U_s`.  It remains nonzero as a risk whenever the argument switches
to `P_s^*` or `L_s` without an explicit transpose/duality step.

## 3. Term Definitions and Current Evidence

### 3.1 Projection error

```text
A_projection(T,a)
```

Meaning: failure of the finite phase/refined state to be an actual
factor, projection, Galerkin cell, or Ulam partition for the proposed
infinite operator.

Current evidence:

- exact projection to the original `PhaseState` quotient is not
  supported;
- adding five high bits helps but does not create a projection identity;
- no canonical infinite kernel has been proved.

Current status: open and potentially fatal for Branch A.

### 3.2 Phase block drift

```text
A_phase_block(T,a,N)
```

Meaning: distributional movement of destination phase under adjacent
high-lift blocks, before retained `delta` labels are considered.

Possible diagnostic:

```text
TV(phase distribution on block b,
   phase distribution on block b+1).
```

Current evidence at `T = 15`, block size `32`:

```text
phase mean TV = 0.0230853,
phase p95 TV  = 0.125,
phase p99 TV  = 0.15625,
phase max TV  = 0.28125.
```

Current status: plausible weak-norm term, not an operator-norm bound.

After the `U_s` operator choice, the finite bridge target is:

```text
|(K v)(i) - (K' v)(i)|
  <= 2 TV_i(K,K') ||v||_infty.
```

Thus a uniform row-TV bound controls an `ell_infty -> ell_infty`
finite operator error, while an average row-TV bound controls a weighted
finite `ell_infty -> L1` error.  The current mean/p95 diagnostics should
therefore be interpreted as weak/distributional evidence unless a
separate exceptional-source-mass bound is proved.

On the active `T15_B32_j64` report, script `99` gives:

```text
A_phase_block weak L1 proxy = 0.0461707,
full label-TV weak L1 proxy = 0.0620098,
full A_label_bounded weak L1 proxy = 0.0158391.
```

The corresponding sup proxies are `0.5625`, `0.75`, and `0.5`,
respectively.  This points toward a weak averaged norm, not a uniform
sup-row perturbation theorem.

The source average in that report is over `131068` complete `(r,h)`
cells out of `131072` possible cells at `T = 15`, so the finite boundary
correction is `0.0000305176`.  This supports using the report as a
complete-cell averaged diagnostic, but does not prove a limiting Haar
averaging statement.

Additional source-partition warning: script `88` groups by low-bit
cells `(r,h)`, not directly by `source_phase`.  For `T = 15` and
`j = 16,32,64`, with the current `odd_bits = 2`, `hit_bits = 2`,
`v2_cap = 13`, exactly `8` of `131072` `(r,h)` groups have two source
states: `r = 0` and `r = 2^14`, for each of the four hit phases.  The
mass is small, but a proof-level projection must either split these
cells or include `SourcePartitionError`.

### 3.3 Bounded retained-label drift

```text
A_label_bounded(T,a,L,N)
```

Meaning: additional variation caused by retained return labels after
destination-phase movement has already been charged.

Suggested finite diagnostic:

```text
max(0, TV(label distribution) - TV(phase distribution)).
```

Current evidence at `T = 15`, block size `32`:

| retained labels | excess mean | excess p95 | excess p99 | excess max |
|---|---:|---:|---:|---:|
| `delta <= 2` | `0.00581854` | `0.03125` | `0.09375` | `0.25` |
| `delta <= 5` | `0.00775838` | `0.0625` | `0.09375` | `0.25` |
| full label | `0.00791955` | `0.0625` | `0.09375` | `0.25` |

Current status: smaller than phase drift on the tested window, but not
zero.  It cannot be replaced by a large-`delta` tail estimate.

### 3.4 Global weighted tail

```text
DeltaTail_global(T,a,L,N)
```

Meaning: total discarded return mass with `delta > L` after the
operator's weight, currently motivated by `2^{-delta}`.

Current evidence:

| run | `delta > 4` | `delta > 5` | `delta > 8` |
|---|---:|---:|---:|
| `T16_j8` | `0.00412187` | `0.000862882` | `0.00000574087` |
| `T15_j32` | `0.0040648` | `0.000845196` | `0.00000635292` |

Current status: encouraging for a weak global tail term.  It is not a
summability theorem.

### 3.5 Local weighted tail

```text
DeltaTail_local(T,a,L,N)
```

Meaning: source-cell-level discarded weighted return mass.

Possible versions:

- supremum over cells, if an operator-norm statement is desired;
- p95 plus exceptional-mass bound, if the weak norm is distributional;
- drift-weighted average, if a weight `W` is part of the space.

Current evidence:

| run | L | local p95 |
|---|---:|---:|
| `T16_j8` | 4 | `1` |
| `T16_j8` | 5 | `0.047619` |
| `T16_j8` | 8 | `0` |
| `T15_j32` | 4 | `0.2` |
| `T15_j32` | 5 | `0.0379747` |
| `T15_j32` | 8 | `0` |

Current status: the hard tail term.  Supremum control is not visible
from the current diagnostics.

The first aggregated error-budget report,
`scripts/spectral_program/collatz_99_T15_B32_j64_error_budget_summary.md`,
keeps the same warning.  At cutoff `L = 5` it reports:

```text
DeltaTail_global = 0.000830424,
DeltaTail_local_p95 = 0.027027,
DeltaTail_local_max = 1.
```

Thus the global tail remains small, but the local supremum obstruction
is still present.

### 3.6 Boundary and killing error

```text
BoundaryError(T,a,N)
```

Meaning: artifacts from killed terminal mass, incomplete high-lift
blocks, and cells with zero return weight.

Current evidence:

- script `97` skipped `4` incomplete groups in the `T15_B32_j64`
  comparison;
- weighted return-TV has p95 `1` for all transforms in that diagnostic,
  because terminal rows have zero return weight.

Current status: must be separated before any weak norm is chosen.

### 3.7 Drift excess

```text
DriftExcess(T,a,W,N)
```

Meaning: failure of a source-stratum weight `W` to make the killed
weighted kernel contractive or tight.

Finite proxy:

```text
R_W(src)
  = average_return_weighted W(dst) / W(src).
```

Current evidence:

- on `T12_j16`, a coarse nontrivial weight can reduce p95 without
  creating ratios `>= 1`;
- on the harder `T15_j16` window, the same naive family improves p95
  only by creating a small exceptional set with ratio `>= 1`;
- identity is the only safe coarse-grid point in that run.

Current status: weak side channel, not a foundation.

### 3.8 Source partition error

```text
SourcePartitionError(T,a,N)
```

Meaning: mismatch between the finite diagnostic source cells and the
cells of the proposed analytic phase partition.

Current evidence:

- script `88` uses `(r,h)` cells with `t = r + j 2^T`;
- the proposed finite phase state uses `(v2(t), odd(t) mod 4, h mod 4)`;
- at `T = 15`, `j = 16,32,64`, exactly `8/131072` low-bit cells are
  mixed in source phase;
- contiguous high-bit blocks in `j` are not automatically 2-adic
  martingale cylinders.

Current status: small as a finite mass correction on the tested window,
but conceptually important for Gate 10.B.

### 3.9 Orientation error

```text
OrientationError(T,a,L,N)
```

Meaning: mismatch between the row-source finite matrices used for
Collatz-Wielandt certificates and a preimage/Ruelle convention.

Current status: conceptual, not numerical.  Any formula for `U_s` must
state whether it is push-forward/Markov, incoming/Ruelle, or the
transpose of a generated matrix.

After `notes/phase10_operator_choice.md`, the default row-source
`FULL` interpretation sets this term to zero for `U_s`.  It reappears
only if an argument switches to `P_s^*` or `L_s` without an explicit
duality/transpose step.

### 3.10 Block coupling

```text
BlockCoupling(T,a,N)
```

Meaning: failure of the proposed good/bad split to be either a small
perturbation or a bounded block operator on the chosen Banach pair.

Current evidence:

- the candidate split `bad = {odd = 3 and v2 in {0,2}}` captures most
  of the full-over-phase excess;
- script `103_component_transition_budget.py` over `0 < t < 2^21`
  gives the component-aggregated weighted matrix:

```text
K_GG = 0.012281296,
K_GB = 0.0054655765,
K_BG = 0.040839452,
K_BB = 0.018100693.
```

Current status: useful structural signal, but it shows `K_bad` is not
a tiny isolated error.  A future proof must use a block norm or route
the bad component to a finite-rank/exceptional subsystem.

Script `104_component_block_cauchy.py` gives a first finite
block-drift proxy for this term.  At fixed `T = 15`, weighted
good/bad row `L1` drift decreases under block doubling:

| block size | all mean | all p95 | all max |
|---:|---:|---:|---:|
| `8` | `0.012046521` | `0.0625` | `0.40625` |
| `16` | `0.0095367816` | `0.056640625` | `0.25` |
| `32` | `0.0074155295` | `0.0390625` | `0.140625` |

Current status: positive for weak averaged convergence, still
insufficient for uniform operator-norm convergence.

The `T15_B16_j64_multipair` check shows this term is not monotone in
ordinary adjacent block position:

```text
0->16  mean 0.009535642,
16->32 mean 0.013903232,
32->48 mean 0.018206286.
```

Thus `BlockCoupling` must be formulated as an averaged/mixed-norm term
or replaced by a more natural high-bit limiting scheme.

The prefix-average version is more favorable.  Script
`105_component_prefix_cauchy.py` reports:

```text
16->32 mean 0.004767821, p95 0.0283203125,
32->64 mean 0.0037076395, p95 0.01953125.
```

Therefore the current best interpretation of `BlockCoupling` is not
ordinary block Cauchy but prefix/Cesaro mixed-norm convergence.

More explicitly, after collapsing destinations to `{G,B}`, the finite
prefix diagnostic estimates:

```text
PrefixCoupling_N
  = sum_c omega_N(c)
      sum_{tau in {G,B}}
        |K_{2N}(c,tau) - K_N(c,tau)|.
```

This is a weak row-source proxy.  It controls bounded component test
functions only in an averaged source norm:

```text
|| (K_{2N} - K_N) f ||_{L1(omega_N)}
  <= PrefixCoupling_N ||f||_infty.
```

In the default script-`105` convention, `omega_N` is uniform counting
measure on retained complete source cells/prefix pairs, with mixed
source cells and boundary rows excluded.  This is the finite measure
used by the report means; it is not yet identified with a limiting Haar
or invariant source measure.

It does not control a supremum over source cells.  It also does not
control the retained full phase/delta labels unless those labels are
added back as separate terms in the error budget.

For the next version of the error decomposition, `BlockCoupling` should
therefore be split as:

```text
BlockCoupling(T,a,N)
  = PrefixCoupling(T,a,N)
  + ComponentLabelLift(T,a,L,N)
  + SourcePartitionError(T,a,N).
```

`PrefixCoupling` is what script `105` currently measures.
`ComponentLabelLift` is the cost of replacing the component-collapsed
kernel by the labelled destination kernel.  `SourcePartitionError` is
already listed separately, but it appears again here because a mixed
source cell can create an artificial good/bad row.

Script `106_prefix_label_lift.py` gives the first finite measurement of
`ComponentLabelLift` on the `T15_j16_32_64_multipair` data.  With full
labels retained:

```text
component_l1 mean = 0.0042377302,
label_l1 mean     = 0.0075584849,
label_excess mean = 0.0033207547,
label_excess p95  = 0.017578125,
label_excess p99  = 0.046875.
```

Repeating with `delta <= 5` gives essentially the same label excess:

```text
label_excess mean = 0.0033040573,
label_excess p95  = 0.017578125,
label_excess p99  = 0.046875.
```

The larger prefix comparison `64->128` improves both component drift
and label drift:

```text
component_l1 mean = 0.0027624646,
label_l1 mean     = 0.0057602607,
label_excess mean = 0.0029977961,
label_excess p95  = 0.015625,
label_excess p99  = 0.03125.
```

Thus `ComponentLabelLift` is not mainly a large-`delta` tail effect on
this window.  It is bounded-retained-label movement and must remain a
separate term in the approximation budget.

## 4. What Would Be Needed for a Real Bound

For a weak finite approximation theorem, one could aim for:

```text
A_phase_block(T,a,N) -> 0,
A_label_bounded(T,a,L,N) -> 0,
DeltaTail_global(T,a,L,N) -> 0,
BoundaryError(T,a,N) -> 0,
SourcePartitionError(T,a,N) -> 0,
BlockCoupling(T,a,N) controlled,
```

in a specified distributional norm, with explicit treatment of
exceptional cells.

For a classical operator-norm or Lasota-Yorke theorem, this is not
enough.  One would also need:

- a genuine infinite phase space `X`;
- boundedness of `U_s` on `B_s` and `B_w`;
- compactness or tightness from `B_s` to `B_w`;
- uniform or drift-weighted local tail bounds;
- summable variation or distortion for the retained labels;
- a projection/inclusion scheme compatible with the generated finite
  matrices.

## 5. Early Falsifiers

The analytic Branch A should be downgraded if any of the following
persists after the norm is fixed:

- `A_phase_block` does not decrease under larger blocks;
- `A_label_bounded` stays bounded away from zero for fixed retained
  cutoff `L`;
- `DeltaTail_local` is large on cells with non-negligible weak mass;
- terminal/killed boundary effects dominate the weak norm;
- all plausible source-stratum weights either overfit or create
  `R_W >= 1` on significant cells;
- the good/bad split remains strongly coupled and no block-norm or
  exceptional-subsystem formulation is available;
- no exact or approximate projection relation can be stated between
  `K_{T,a,L,N}` and an infinite `U_s`.

## 6. Immediate Use

Future experiments should report which terms they estimate.  A table of
numbers without mapping to this decomposition should not be used as
evidence for Hennion, Keller-Liverani, or a spectral-gap statement.

Script `99_error_budget_summary.py` is the current preferred wrapper for
this rule: it aggregates only named finite proxies and writes them under
the error-budget labels above.
