# Phase 10 Source-Stratum Drift Ansatz

Date: 2026-05-14

Status: mathematical ansatz, not a theorem.  This note records one
possible way to turn the source-stratum diagnostics into a drift
condition.  It deliberately separates a principled drift function from a
data-fitted penalty.

## 1. Motivation

The diagnostics show three different nonuniformities:

1. destination phase is mostly stable after deeper 2-adic refinement but
   not locally constant;
2. the global weighted `delta` tail is small, while local cell tails can
   remain large;
3. bad cells are not uniformly spread across source phases.

At `T = 16`, `j_count = 8`, the stratum `v2 = 2, odd = 3` has:

```text
phase exact fraction = 0.898926,
full exact fraction  = 0.383301.
```

Thus the main obstruction there is not primarily destination phase; it
is return-signature/weight variation.  Other small high-`v2` strata have
larger phase-low fractions.

This suggests that a Banach norm may need a source-stratum drift weight
in addition to a `delta` tail weight.

## 2. Candidate Weight Form

Let the source coordinate be locally summarized by:

```text
s(x) = (nu_2(t), odd(t) mod 4, h).
```

A finite diagnostic weight would be:

```text
W_diag(s) >= 1.
```

An infinite candidate must not depend on `T`, `j_count`, or a hand-picked
bad-cell list.  A minimal structured family is:

```text
W(t,h)
  = A(nu_2(t)) * B(odd(t) mod 4) * C(h),
```

with:

```text
A(k) >= 1,  B(o) >= 1,  C(h) >= 1.
```

More flexible but riskier:

```text
W(t,h)
  = A(nu_2(t), odd(t) mod 4) * C(h).
```

The second form is closer to the diagnostics, but also closer to
overfitting.

## 3. Desired Drift Inequality

For a labelled killed kernel

```text
K(x; dy, ell),
```

with return exponent `ell = delta`, the weak drift target is:

```text
sum_{return labels}
  2^{-s ell} W(y) K(x; dy, ell)
  <= alpha W(x) + b 1_F(x),
```

where:

```text
alpha < 1.
```

Here `F` should be a finite or compact exceptional source set.  The
killed/terminal mass does not contribute to the left side.

This is the correct kind of statement for a weighted `ell_infty` or
symbolic drift component.  It is not yet a Lasota-Yorke inequality,
because it controls weak weighted mass but not strong variation.

## 4. Strong-Norm Extension

A strong norm would need at least:

```text
||f||_s
  = sup_x |f(x)| / W(x)
    + Var_or_Holder(f/W).
```

The corresponding LY target would require a depth/variation term:

```text
Var(Lf / W)
  <= alpha_var Var(f / W)
     + C ||f||_w.
```

The source-stratum weight can help only if it is compatible with branch
regularity:

```text
W(y) / W(x)
```

must be controlled on return branches.  A weight that jumps too much
across a single branch can make the operator unbounded.

## 5. Finite Diagnostic Test

Once a candidate `W` is proposed, the finite test should be:

```text
R_W(src)
  = sum_dst,ell K_T(src,dst,ell) 2^{-s ell} W(dst) / W(src).
```

The finite diagnostic passes only if:

```text
quantile_p(R_W) < 1
```

for a declared `p`, and the tail of cells with `R_W >= 1` is explicitly
controlled by an exceptional/tail term.

The stronger finite test is:

```text
sup_src R_W(src) <= alpha < 1
```

outside a declared exceptional set.  This is the only version that
resembles a uniform drift lemma.

## 6. Data-Fitting Warning

The following would be a false analytic shortcut:

```text
assign a large W to every stratum that looks bad in T16_j8.
```

That may reduce a finite diagnostic ratio while destroying:

- branch regularity;
- uniformity in `T`;
- convergence in high-bit lift;
- compactness/tightness;
- interpretability of the infinite state space.

Permissible use of data:

- identify candidate structural variables (`nu_2`, odd residue, `h`);
- formulate a simple parametric `W`;
- test whether the same `W` is stable across `T`, `j_count`, and block
  windows.

Impermissible use:

- declaring the fitted finite `W` a Banach weight without a branch
  theorem.

## 7. Kill Criteria For This Ansatz

Abandon the source-stratum drift branch if any of the following occurs:

1. the fitted/parametric `W` changes qualitatively between `T = 15` and
   `T = 16`;
2. `W(y)/W(x)` is unbounded or erratic on observed return branches;
3. the bad mass remains large after weighting;
4. no finite exceptional set `F` can be defined independently of
   prefix length;
5. the only successful `W` is a lookup table for finite residues.

In that case, the honest options are:

- countable labelled return-signature space;
- finite-rank fallback;
- collaborator input on nonstandard symbolic Banach spaces.

## 10. New 2-adic Stratification Signal

Script:

```text
scripts/spectral_program/101_z2_oscillation_strata.py
```

Run:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/101_z2_oscillation_strata.py \
  --T 15 \
  --max-depth 2 \
  --tail-bits 3 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 1000 \
  --min-samples 1024 \
  --output-tag T15_d2_tail3
```

At 2-adic child depth `2`, the global full-over-phase excess is:

```text
mean = 0.0165176,
p95  = 0.125,
max  = 0.5.
```

The main structural contributors are:

| stratum | mass | mean excess | p95 | contribution |
|---|---:|---:|---:|---:|
| `source_odd = 3` | `0.499969` | `0.0261895` | `0.25` | `0.792725` |
| `source_v2 = 2` | `0.125` | `0.0623322` | `0.25` | `0.471709` |
| `source_v2_odd = 2|3` | `0.0625` | `0.120621` | `0.375` | `0.456409` |

This strengthens the case for a structured source-stratum variable in
any next drift or enlarged symbolic model.  It does not validate the
earlier exponential weight family; that still needs a cross-`T` test.

The cross-`T` stratified run `T16_d1_tail2` preserves the same signal:

| stratum | mass | mean excess | p95 | contribution |
|---|---:|---:|---:|---:|
| `source_odd = 3` | `0.499985` | `0.0315485` | `0.25` | `0.816548` |
| `source_v2 = 2` | `0.125` | `0.0780182` | `0.5` | `0.504838` |
| `source_v2_odd = 2|3` | `0.0625` | `0.152130` | `0.5` | `0.492200` |

Thus the structural signal survives at least one change of `T`.

## 11. Interaction-Weight Probe

Script `96_stratum_weight_drift_probe.py` now includes an interaction
coefficient for the stratum:

```text
v2(t) = 2 and odd(t) mod 4 = 3.
```

Targeted hard-window command:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/96_stratum_weight_drift_probe.py \
  --T 15 \
  --j-count 16 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --odd3-coeffs 0 \
  --v2eq2-coeffs 0 \
  --v2-coeffs 0 \
  --v2eq2-odd3-coeffs -1,-0.5,0,0.5,1 \
  --limit 12 \
  --output-tag T15_j16_interaction_only
```

Results:

| interaction coeff | mean ratio | p95 | p99 | max | fraction `>= 1` |
|---:|---:|---:|---:|---:|---:|
| `-1` | `0.0509868` | `0.25` | `1.1043` | `1.48596` | `0.0229797` |
| `-0.5` | `0.0381116` | `0.25` | `0.669793` | `0.96875` | `0` |
| `0` | `0.0305797` | `0.25` | `0.421875` | `0.96875` | `0` |
| `0.5` | `0.0264688` | `0.226562` | `0.3125` | `1.5972` | `0.0000305176` |
| `1` | `0.0247295` | `0.155199` | `0.326143` | `2.63334` | `0.000366211` |

Interpretation:

- positive interaction weights reduce mean and p95;
- they create exceptional cells with ratio `>= 1` and large maxima;
- the only safe points in this one-parameter test are still the
  identity and the negative half-weight, neither of which improves p95;
- therefore this interaction is not yet a uniform drift weight.

It remains potentially useful only in an exceptional-mass framework:
one would need to prove that the new bad cells have controlled weak
mass and do not destroy branch regularity.

The coefficient-`1` exceptional-cell localization is worse than a clean
exceptional-set story.  The largest ratios are not sourced from
`v2=2, odd=3`; they appear in other source phases, for example:

| r | source phase | drift ratio |
|---:|---|---:|
| `6394` | `v2=1|odd=1` | `2.63334` |
| `11430` | `v2=1|odd=3` | `1.31667` |
| `10046` | `v2=1|odd=3` | `1.30061` |
| `15360` | `v2=10|odd=3` | `1.21566` |
| `18017` | `v2=0|odd=1` | `1.21566` |

Thus the interaction weight partly moves mass into the bad weighted
destination stratum, creating new source-side violations.  This is a
strong warning against a simple weighted-sup drift norm.

## 12. Enriched-State Split Is More Promising Than A Scalar Weight

Script:

```text
scripts/spectral_program/102_enriched_state_test.py
```

The candidate component

```text
odd = 3 and v2 in {0,2}
```

has:

| run | selected mass | selected contribution | complement mean | complement p95 |
|---|---:|---:|---:|---:|
| `T15`, depth `2` | `0.3125` | `0.742956` | `0.00617565` | `0` |
| `T16`, depth `1` | `0.3125` | `0.767081` | `0.00654463` | `0` |

This suggests the next candidate should be an enriched symbolic
decomposition:

```text
good component + labelled bad component,
```

not a single scalar drift weight.  The selected bad component remains
unsolved; it requires internal labelled dynamics, an exceptional-mass
argument, or finite-rank treatment.

## 8. Next Computational Step

Do not compute a spectral radius.

The next finite diagnostic, if pursued, should construct transition
rows with enough destination-stratum information to evaluate:

```text
R_W(src)
```

for simple weights such as:

```text
W_{a,b,c}(t,h)
  = exp(a * 1_{odd(t) = 3}
        + b * 1_{nu_2(t) = 2}
        + c * min(nu_2(t), v2_cap)).
```

A successful diagnostic would not prove the drift inequality, but a
failed diagnostic would be strong evidence to stop this branch.

## 9. First Finite Probes

Implemented script:

```text
scripts/spectral_program/96_stratum_weight_drift_probe.py
```

Small-window command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/96_stratum_weight_drift_probe.py \
  --T 12 \
  --j-count 16 \
  --odd3-coeffs=-0.5,0,0.5 \
  --v2eq2-coeffs=-0.5,0,0.5 \
  --v2-coeffs=-0.1,0,0.1 \
  --output-tag T12_j16 \
  --progress
```

This finite test estimates:

```text
R_W(r,h)
  = (1 / sample_count) sum_return 2^{-delta} W(dst)/W(src).
```

Identity weight on the `T = 12`, `j_count = 16` window:

- mean ratio: `0.0303514`;
- p95 ratio: `0.25`;
- p99 ratio: `0.421875`;
- max ratio: `0.9375`;
- fraction `>= 1`: `0`.

Best p95 grid points reduce p95 to about `0.160814`, but introduce a
small number of cells with ratio `>= 1`.  The best safe grid point in
this coarse grid is:

```text
odd3_coeff = -0.5,
v2eq2_coeff = 0.5,
v2_coeff = 0.1.
```

with:

- mean ratio: `0.0310581`;
- p95 ratio: `0.207098`;
- p99 ratio: `0.393745`;
- max ratio: `0.979146`;
- fraction `>= 1`: `0`.

Interpretation:

- the source-stratum weight idea is not immediately falsified on this
  small finite window;
- it is also not impressive enough to be trusted: the identity weight
  already has max below `1`, and p95 improvements are modest unless one
  permits exceptional cells above `1`;
- the next test must use a harder window before this ansatz gets any
  mathematical weight.

Harder-window command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/96_stratum_weight_drift_probe.py \
  --T 15 \
  --j-count 16 \
  --odd3-coeffs=-0.5,0,0.5 \
  --v2eq2-coeffs=-0.5,0,0.5 \
  --v2-coeffs=-0.1,0,0.1 \
  --output-tag T15_j16 \
  --progress
```

Identity weight at `T = 15`, `j_count = 16`:

- mean ratio: `0.0305797`;
- p95 ratio: `0.25`;
- p99 ratio: `0.421875`;
- max ratio: `0.96875`;
- fraction `>= 1`: `0`.

The best p95 grid points again reduce p95, down to `0.171875`, but they
introduce cells with ratio `>= 1`.  In the coarse grid tested, the only
safe point was the identity weight:

```text
odd3_coeff = 0,
v2eq2_coeff = 0,
v2_coeff = 0.
```

Interpretation:

- this is a negative signal for the naive three-parameter stratum
  weight;
- on the harder window, the simple nontrivial weights trade a better
  p95 for exceptional cells above `1`;
- the identity weight remaining safe is not enough for the analytic
  branch, because it says little about strong variation, convergence, or
  larger prefixes.

Provisional verdict:

```text
Do not build Phase 10 around this simple source-stratum weight family.
Keep it only as a diagnostic side channel unless a more principled W is
derived from branch geometry.
```

## Update: Component Split Beats Scalar Weight

The later enriched-state and transition-budget diagnostics strengthen
the negative verdict for this scalar drift ansatz.

The currently preferred structural split is:

```text
bad = { odd = 3 and v2 in {0,2} }.
```

Script `103_component_transition_budget.py`, over `0 < t < 2^21`,
gives the component-aggregated weighted return matrix:

| source | destination good | destination bad | row sum |
|---|---:|---:|---:|
| `good` | `0.012281296` | `0.0054655765` | `0.017746872` |
| `bad` | `0.040839452` | `0.018100693` | `0.058940144` |

This does not make `bad` a small removable perturbation.  It says the
right next object, if Branch A continues, is a block kernel with
explicit coupling terms `K_GG`, `K_GB`, `K_BG`, `K_BB`.  A scalar
source-stratum weight can still be used as a diagnostic, but it is not
the main analytic candidate.
