# Phase 10 Norm Constants From Diagnostics

Date: 2026-05-14

Status: bookkeeping note.  These constants are finite diagnostics only.
They are not theorem hypotheses until an infinite operator, Banach
spaces, projections, and convergence statements are defined.

## 1. Purpose

The Phase 10 diagnostics now produce several different numerical
quantities.  They should not be conflated.

In particular:

- majority fractions are not operator norms;
- dominant-signature flips are not total-variation convergence;
- global weighted tails are not uniform source-cell tails;
- finite prefix/block comparisons are not limits.

This note records the intended mathematical role of each measured
quantity.

## 2. Candidate Constants

### Phase concentration

Diagnostic source:

```text
scripts/spectral_program/88_cylinder_signature_stability.py
```

Candidate quantity:

```text
PhaseBad_T,a,N(theta)
  = Haar/counting fraction of source cells whose destination-phase
    majority is <= theta.
```

Observed examples:

- `T = 15`, `j_count = 32`: phase exact fraction `0.729584`;
- `T = 16`, `j_count = 8`: phase exact fraction `0.861542`.

Possible role:

- tests whether deeper 2-adic cylinders reduce phase variation.

Not a substitute for:

- local constancy;
- a Lipschitz/depth-loss theorem;
- mixed-norm projection error.

### Weighted delta tail

Diagnostic source:

```text
scripts/spectral_program/93_delta_tail_weight.py
```

Candidate quantities:

```text
DeltaTail_global(L)
  = weighted return mass with delta > L
    / total weighted return mass,
```

and

```text
DeltaTail_local_p95(L)
  = p95 over returning source cells of
    weighted return mass with delta > L
    / source-cell weighted return mass.
```

Observed examples:

| run | L | global tail | local p95 |
|---|---:|---:|---:|
| `T16_j8` | 4 | `0.00412187` | `1` |
| `T16_j8` | 5 | `0.000862882` | `0.047619` |
| `T16_j8` | 8 | `0.00000574087` | `0` |
| `T15_j32` | 4 | `0.0040648` | `0.2` |
| `T15_j32` | 5 | `0.000845196` | `0.0379747` |
| `T15_j32` | 8 | `0.00000635292` | `0` |
| `T15_j64` | 4 | `0.00406131` | `0.120879` |
| `T15_j64` | 5 | `0.000830424` | `0.027027` |
| `T15_j64` | 8 | `0.00000682691` | `0` |

Possible role:

- `DeltaTail_global` may feed weak weighted-mass control;
- `DeltaTail_local_p95` may feed a nonuniform/tightness statement;
- a uniform local tail would be stronger than either observed p95.

Not a substitute for:

- summable variation of the potential;
- uniform branch summability;
- compactness.

### Adjacent-block distributional drift

Diagnostic source:

```text
scripts/spectral_program/94_block_cauchy_summary.py
```

Candidate quantity:

```text
BlockTV_full(B)
  = TV distance between full-signature distributions on adjacent
    high-bit blocks of size B.
```

Observed at `T = 15`, block size `16`, comparing `0..15` with `16..31`:

| level | mean TV | p95 TV | p99 TV | max TV | dominant flip fraction |
|---|---:|---:|---:|---:|---:|
| status | `0.0182055` | `0.125` | `0.1875` | `0.375` | `0.0012207` |
| phase | `0.0294743` | `0.1875` | `0.25` | `0.4375` | `0.000701904` |
| delta | `0.0297394` | `0.125` | `0.1875` | `0.4375` | `0.0109253` |
| full | `0.0381069` | `0.1875` | `0.25` | `0.5` | `0.0124817` |

Block-doubling at fixed `T = 15` gives:

| block size | full mean TV | full p95 TV | full p99 TV | full max TV | full dominant flip fraction |
|---:|---:|---:|---:|---:|---:|
| 8 | `0.0462265` | `0.25` | `0.375` | `0.75` | `0.0177002` |
| 16 | `0.0381069` | `0.1875` | `0.25` | `0.5` | `0.0124817` |
| 32 | `0.0310087` | `0.15625` | `0.21875` | `0.375` | `0.011322` |

This is compatible with a Cauchy-type target, but does not prove one.

Truncated-label TV at `T = 15`, block size `32`, gives:

| transform | count mean TV | count p95 TV | count p99 TV | count max TV |
|---|---:|---:|---:|---:|
| status | `0.0128616` | `0.0625` | `0.125` | `0.25` |
| phase | `0.0230853` | `0.125` | `0.15625` | `0.28125` |
| clip `delta > 2` | `0.0289039` | `0.125` | `0.1875` | `0.375` |
| clip `delta > 3` | `0.0299863` | `0.125` | `0.1875` | `0.375` |
| clip `delta > 4` | `0.0305662` | `0.15625` | `0.1875` | `0.375` |
| clip `delta > 5` | `0.0308437` | `0.15625` | `0.21875` | `0.375` |
| full | `0.0310049` | `0.15625` | `0.21875` | `0.375` |

Thus large-`delta` clipping helps little at this block size.  Bounded
return-label variation remains part of `A_block`.

Bounded-label excess over phase TV at `T = 15`, block size `32`:

| transform | excess mean | excess p95 | excess p99 | excess max | positive fraction |
|---|---:|---:|---:|---:|---:|
| clip `delta > 2` | `0.00581854` | `0.03125` | `0.09375` | `0.25` | `0.127384` |
| clip `delta > 5` | `0.00775838` | `0.0625` | `0.09375` | `0.25` | `0.162603` |
| full | `0.00791955` | `0.0625` | `0.09375` | `0.25` | `0.163945` |

This suggests a separate bounded-label term:

```text
A_label_bounded(B,L)
```

in addition to phase movement and large-`delta` tail.

Script `99_error_budget_summary.py` now aggregates these same named
terms from the active script-`88` output.  On the current
`T15_B32_j64` dataset it reports:

| term | value |
|---|---:|
| `DeltaTail_global(5)` | `0.000830424` |
| `DeltaTail_local_p95(5)` | `0.027027` |
| `A_phase_block` p95 | `0.125` |
| full `A_label_bounded` p95 | `0.0625` |
| boundary skipped fraction | `0.0000305176` |

These are finite proxies only.  In particular, `DeltaTail_local_max(5)`
is still `1`, so no uniform tail bound is visible.

After the finite row-TV bridge was added, script `99` also reports:

| proxy | value |
|---|---:|
| `A_phase_block` weak `L1` proxy `2*mean` | `0.0461707` |
| full label-TV weak `L1` proxy `2*mean` | `0.0620098` |
| full `A_label_bounded` weak `L1` proxy `2*mean` | `0.0158391` |
| `A_phase_block` sup proxy `2*max` | `0.5625` |
| full label-TV sup proxy `2*max` | `0.75` |

Interpretation: the current data are compatible with a weak averaged
row-distribution norm, but not with a small uniform row-TV/sup-norm
error.

Repeating the same script-`99` aggregation at fixed `T = 15` over block
sizes `8`, `16`, and `32` gives:

| block size | prefix j | phase weak `L1` | full-label weak `L1` | bounded-label weak `L1` | full-label sup proxy |
|---:|---:|---:|---:|---:|---:|
| 8 | 16 | `0.0731834` | `0.0924482` | `0.0192648` | `1.5` |
| 16 | 32 | `0.0589389` | `0.0762047` | `0.0172658` | `1.0` |
| 32 | 64 | `0.0461707` | `0.0620098` | `0.0158391` | `0.75` |

This is positive evidence for an averaged weak row-distribution target.
It is not evidence for a uniform perturbation bound: the sup proxy is
still too large at all three block sizes.

Source-cell consistency check at the same `T = 15` settings:

| prefix j | mixed `(r,h)` source cells | total `(r,h)` cells | fraction |
|---:|---:|---:|---:|
| 16 | 8 | 131072 | `0.0000610352` |
| 32 | 8 | 131072 | `0.0000610352` |
| 64 | 8 | 131072 | `0.0000610352` |

The mixed cells are `r = 0` and `r = 2^14`, for each hit phase.  This
is a small finite correction, but it means the present weak proxy is not
yet literally an average over source-state partition cells.

First true 2-adic child-cylinder diagnostic,
`collatz_100_T15_d3_tail2_z2_cylinder_oscillation.md`:

| depth | full mean TV | full p95 TV | full max TV | phase mean TV |
|---:|---:|---:|---:|---:|
| 0 | `0.0526182` | `0.1875` | `1` | `0.0425999` |
| 1 | `0.0544645` | `0.25` | `1` | `0.0418446` |
| 2 | `0.0575895` | `0.25` | `1` | `0.0410719` |
| 3 | `0.0606241` | `0.5` | `1` | `0.0408087` |

This does not show 2-adic child-cylinder contraction in full labels.
It pressures the naive martingale-variation model, although the deepest
level has small child sample counts and should be repeated with more
tail bits before being treated as a kill-switch.

The repeat run `collatz_100_T15_d2_tail4_z2_cylinder_oscillation.md`
uses `max_j = 128` and has larger child samples:

| depth | full mean TV | full p95 TV | full max TV | phase mean TV |
|---:|---:|---:|---:|---:|
| 0 | `0.0486132` | `0.171875` | `1` | `0.0399633` |
| 1 | `0.0487704` | `0.1875` | `1` | `0.0388441` |
| 2 | `0.0509391` | `0.25` | `1` | `0.0382137` |

The full-label obstruction persists with better sampling.

The stratified run
`collatz_101_T15_d2_tail3_z2_oscillation_strata_report.md` separates
full-TV from the excess over phase TV.  At depth `2`, the global
full-over-phase excess has mean `0.0165176`, p95 `0.125`, and max `0.5`.
Its largest structural contributors are:

| stratum | mass | mean excess | p95 | contribution |
|---|---:|---:|---:|---:|
| `source_odd = 3` | `0.499969` | `0.0261895` | `0.25` | `0.792725` |
| `source_v2 = 2` | `0.125` | `0.0623322` | `0.25` | `0.471709` |
| `source_v2_odd = 2|3` | `0.0625` | `0.120621` | `0.375` | `0.456409` |

Thus the label-excess part is not featureless noise; it is strongly
stratified by variables already visible in earlier bad-cell diagnostics.

The cross-`T` stratified run `T16_d1_tail2` preserves the same pattern:

| stratum | mass | mean excess | p95 | contribution |
|---|---:|---:|---:|---:|
| `source_odd = 3` | `0.499985` | `0.0315485` | `0.25` | `0.816548` |
| `source_v2 = 2` | `0.125` | `0.0780182` | `0.5` | `0.504838` |
| `source_v2_odd = 2|3` | `0.0625` | `0.152130` | `0.5` | `0.492200` |

The targeted interaction-weight probe on `source_v2_odd = 2|3` gives:

| coeff | mean ratio | p95 | p99 | max | fraction `>= 1` |
|---:|---:|---:|---:|---:|---:|
| `0` | `0.0305797` | `0.25` | `0.421875` | `0.96875` | `0` |
| `0.5` | `0.0264688` | `0.226562` | `0.3125` | `1.5972` | `0.0000305176` |
| `1` | `0.0247295` | `0.155199` | `0.326143` | `2.63334` | `0.000366211` |

So the interaction is useful for typical ratios but not for a uniform
drift bound without exceptional-cell control.

The enriched-state split test gives a more useful formulation than the
scalar weight.  For the component `odd = 3 and v2 in {0,2}`:

| run | selected mass | selected contribution | complement mean | complement p95 |
|---|---:|---:|---:|---:|
| `T15`, depth `2` | `0.3125` | `0.742956` | `0.00617565` | `0` |
| `T16`, depth `1` | `0.3125` | `0.767081` | `0.00654463` | `0` |

This suggests a two-component symbolic model may be more natural than a
single weighted sup norm.

The follow-up component transition-budget diagnostic
`collatz_103_T15_j64_component_transition_budget_report.md` measures
the block flow for the same bad component over `0 < t < 2^21`.  It is
stable against the `0 < t < 2^20` run:

| run | source | destination good | destination bad | row sum |
|---|---|---:|---:|---:|
| `0<t<2^20` | `good` | `0.012278567` | `0.0054906632` | `0.017769231` |
| `0<t<2^20` | `bad` | `0.040819731` | `0.018073894` | `0.058893625` |
| `0<t<2^21` | `good` | `0.012281296` | `0.0054655765` | `0.017746872` |
| `0<t<2^21` | `bad` | `0.040839452` | `0.018100693` | `0.058940144` |

Candidate quantities:

```text
ComponentBudget_G = K_GG + K_GB,
ComponentBudget_B = K_BG + K_BB,
Leak_G_to_B       = K_GB / (K_GG + K_GB).
```

Observed:

```text
ComponentBudget_G = 0.017746872,
ComponentBudget_B = 0.058940144,
Leak_G_to_B       = 0.30797407.
```

Possible role:

- tests whether the enlarged-state split can be represented by a block
  kernel;
- gives finite constants for a future block-norm bookkeeping model;
- warns that the bad block is coupled, not a tiny independent tail.

Not a substitute for:

- an infinite block operator;
- a small-norm perturbation theorem;
- a proof that component budgets converge as the prefix window grows.

Alternative bad-rule budgets on the common `T15_j32` window:

| bad rule | bad mass | good row sum | bad row sum | G->B weighted frac | B->B weighted frac |
|---|---:|---:|---:|---:|---:|
| `v2=2 and odd=3` | `0.0625001` | `0.018664724` | `0.20995882` | `0.0631777` | `0.0626915` |
| `odd=3 and v2 in {0,2}` | `0.3125003` | `0.017769231` | `0.058893625` | `0.308998` | `0.306891` |
| `odd=3 or v2=2` | `0.5624996` | `0.020555724` | `0.038448879` | `0.559896` | `0.558768` |

### Component block-Cauchy drift

Diagnostic source:

```text
scripts/spectral_program/104_component_block_cauchy.py
```

Candidate quantity:

```text
BlockCouplingDrift_B
  = average source-row L1 drift of the substochastic good/bad block
    kernel between adjacent high-bit blocks of size B.
```

Observed at fixed `T = 15`:

| block size | all mean | all p95 | all max | good mean | bad mean |
|---:|---:|---:|---:|---:|---:|
| `8` | `0.012046521` | `0.0625` | `0.40625` | `0.0093235814` | `0.018036723` |
| `16` | `0.0095367816` | `0.056640625` | `0.25` | `0.0071800626` | `0.014721333` |
| `32` | `0.0074155295` | `0.0390625` | `0.140625` | `0.0055656365` | `0.011485113` |
| `64` | `0.0055249292` | `0.026367188` | `0.091308594` | `0.0041154957` | `0.0086254075` |

This is compatible with weak averaged block convergence.  It is not a
uniform bound; the bad-source p95 at block size `32` is still
`0.04296875`.

The `B=64` row is from the later `T15_B64_j128_prefix` run.

Multipair check at block size `16`:

| pair | all mean | all p95 | good mean | bad mean | bad p95 |
|---|---:|---:|---:|---:|---:|
| `0->16` | `0.009535642` | `0.056640625` | `0.0071783004` | `0.014721333` | `0.0625` |
| `16->32` | `0.013903232` | `0.09375` | `0.0084089414` | `0.025989598` | `0.109375` |
| `32->48` | `0.018206286` | `0.1015625` | `0.00940828` | `0.037560182` | `0.203125` |

This shows ordinary adjacent-block drift can worsen later in the
prefix.  The constant is therefore an averaged diagnostic, not a
monotone Cauchy modulus.

### Component prefix/Cesaro drift

Diagnostic source:

```text
scripts/spectral_program/105_component_prefix_cauchy.py
```

Candidate quantity:

```text
PrefixCouplingDrift_N
  = average source-row L1 drift between block-valued prefix kernels
    at prefix sizes N and 2N.
```

Observed at fixed `T = 15`:

| prefix pair | all mean | all p95 | all max | good mean | bad mean |
|---|---:|---:|---:|---:|---:|
| `16->32` | `0.004767821` | `0.0283203125` | `0.125` | `0.0035891502` | `0.0073606666` |
| `32->64` | `0.0037076395` | `0.01953125` | `0.0703125` | `0.002782595` | `0.0057425566` |
| `64->128` | `0.0027624646` | `0.013183594` | `0.045654297` | `0.0020577478` | `0.0043127038` |

This is more compatible with a Cesaro/prefix-average limit than the
ordinary adjacent-block diagnostic.

### Prefix label-lift drift

Diagnostic source:

```text
scripts/spectral_program/106_prefix_label_lift.py
```

Candidate quantity:

```text
ComponentLabelLift_N
  = average source-row excess between retained full-label prefix drift
    and good/bad component prefix drift.
```

Observed at fixed `T = 15`, no delta cutoff:

| metric | all mean | all p95 | all p99 | all max |
|---|---:|---:|---:|---:|
| component `L1` | `0.0042377302` | `0.0234375` | `0.0390625` | `0.125` |
| full-label `L1` | `0.0075584849` | `0.038085938` | `0.0703125` | `0.34375` |
| label excess | `0.0033207547` | `0.017578125` | `0.046875` | `0.28125` |

With `delta <= 5`:

| metric | all mean | all p95 | all p99 | all max |
|---|---:|---:|---:|---:|
| component `L1` | `0.0042351462` | `0.0234375` | `0.0390625` | `0.125` |
| full-label `L1` | `0.0075392035` | `0.038085938` | `0.0703125` | `0.34375` |
| label excess | `0.0033040573` | `0.017578125` | `0.046875` | `0.28125` |

Observed at `64->128`, no delta cutoff:

| metric | all mean | all p95 | all p99 | all max |
|---|---:|---:|---:|---:|
| component `L1` | `0.0027624646` | `0.013183594` | `0.01953125` | `0.045654297` |
| full-label `L1` | `0.0057602607` | `0.02444458` | `0.041381836` | `0.13671875` |
| label excess | `0.0029977961` | `0.015625` | `0.03125` | `0.109375` |

With `delta <= 5` at `64->128`, label excess is again essentially the
same:

```text
mean 0.0029815467,
p95  0.015625,
p99  0.03125.
```

Alternative bad rules on the same data:

| bad rule | component `L1` mean | label-excess mean | bad row count |
|---|---:|---:|---:|
| `v2=2 and odd=3` | `0.0035912445` | `0.0039672405` | `16384` |
| `odd=3 and v2 in {0,2}` | `0.0042377302` | `0.0033207547` | `81920` |
| `odd=3 or v2=2` | `0.0044146893` | `0.0031437956` | `147448` |

At `64->128`, the same comparison gives:

| bad rule | component `L1` mean | label-excess mean | bad row count |
|---|---:|---:|---:|
| `v2=2 and odd=3` | `0.0023125054` | `0.0034477554` | `8192` |
| `odd=3 and v2 in {0,2}` | `0.0027624646` | `0.0029977961` | `40960` |
| `odd=3 or v2=2` | `0.002861205` | `0.0028990557` | `73724` |

Possible role:

- measures the finite cost of lifting the block component kernel back
  to retained phase/delta labels;
- tests whether prefix convergence survives the labels actually used by
  the project;
- supplies the `ComponentLabelLift` term in the error decomposition.

Not a substitute for:

- convergence of the full labelled kernel;
- uniform row control;
- a tail theorem, since the `delta <= 5` cutoff barely changes the
  excess on this window.

Observed at `T = 16`, block size `4`, comparing `0..3` with `4..7`:

| level | mean TV | p95 TV | p99 TV | max TV | dominant flip fraction |
|---|---:|---:|---:|---:|---:|
| status | `0.0301514` | `0.25` | `0.5` | `0.75` | `0.0105591` |
| phase | `0.0400963` | `0.25` | `0.5` | `1` | `0.00665283` |
| delta | `0.0440102` | `0.25` | `0.5` | `0.75` | `0.0227661` |
| full | `0.0507774` | `0.25` | `0.5` | `1` | `0.0238647` |

Possible role:

- if repeated over increasing block sizes, could test a Cesaro/high-lift
  Cauchy hypothesis;
- may become a mixed-norm finite approximation error after `L` and
  projections are defined.

Not a substitute for:

- Cauchy convergence as block size tends to infinity;
- Keller-Liverani mixed-norm convergence;
- resolvent control.

### Source-stratum bad-cell concentration

Diagnostic source:

```text
scripts/spectral_program/95_bad_cell_stratification.py
```

Candidate quantities:

```text
BadPhase(stratum)
  = fraction of source cells in the stratum with phase majority <= theta,
```

and

```text
BadFull(stratum)
  = fraction of source cells in the stratum with full-signature majority
    <= theta or large full-tail weight.
```

Observed at `T = 16`, `j_count = 8`:

| stratum | value | count | phase exact | full exact | phase low | full low | high tail |
|---|---|---:|---:|---:|---:|---:|---:|
| `source_v2_odd` | `10|3` | `64` | `0.8125` | `0` | `0.125` | `0.125` | `0.0625` |
| `source_v2` | `10` | `128` | `0.71875` | `0.3125` | `0.09375` | `0.09375` | `0.1875` |
| `source_v2_odd` | `7|3` | `512` | `0.632812` | `0.632812` | `0.046875` | `0.046875` | `0.335938` |
| `source_v2_odd` | `2|3` | `16384` | `0.898926` | `0.383301` | `0.00976562` | `0.167969` | `0.0969238` |
| `source_v2_odd` | `0|3` | `65536` | `0.749695` | `0.692017` | `0.0187988` | `0.0320435` | `0.24469` |

Possible role:

- suggests a drift/tail norm may need source-stratum weights, not just a
  global `delta` cutoff;
- helps decide which bad classes require branch-level analysis.

Not a substitute for:

- an explicit Lyapunov/drift function;
- a proof that bad strata have summable weight;
- a finite-to-infinite projection theorem.

### Finite source-stratum drift ratio

Diagnostic source:

```text
scripts/spectral_program/96_stratum_weight_drift_probe.py
```

Candidate quantity:

```text
R_W(r,h)
  = (1 / sample_count) sum_return 2^{-delta} W(dst)/W(src).
```

Observed:

| run | weight | mean | p95 | p99 | max | fraction >= 1 |
|---|---|---:|---:|---:|---:|---:|
| `T12_j16` | identity | `0.0303514` | `0.25` | `0.421875` | `0.9375` | `0` |
| `T12_j16` | best safe coarse grid | `0.0310581` | `0.207098` | `0.393745` | `0.979146` | `0` |
| `T15_j16` | identity | `0.0305797` | `0.25` | `0.421875` | `0.96875` | `0` |
| `T15_j16` | best p95 coarse grid | `0.0271007` | `0.171875` | `0.41218` | `2.63334` | `0.000701904` |

The best safe coarse grid point at `T12_j16` was:

```text
odd3_coeff = -0.5,
v2eq2_coeff = 0.5,
v2_coeff = 0.1.
```

At `T15_j16`, the only safe point in the same coarse grid was the
identity weight.

Possible role:

- preliminary test for a drift component in a weighted symbolic or
  episode-space norm.
- current evidence is negative for this naive three-parameter family on
  the harder `T15_j16` window.

Not a substitute for:

- a uniform drift theorem;
- verification on harder `T = 15`/`T = 16` windows;
- source-stratum regularity of `W(y)/W(x)`.

## 3. Provisional Lasota-Yorke Bookkeeping

A future conditional LY target should have constants named before they
are estimated:

```text
||L f||_s <= alpha ||f||_s + C ||f||_w,
```

with a bookkeeping decomposition such as:

```text
alpha <= alpha_depth(a)
       + C1 * DeltaTail_global(L)
       + C2 * DeltaTail_local(L)
       + C3 * BlockTV_full(B)
       + C4 * SourceStratumBad(W)
       + C5 * DriftExcess(W)
       + C6 * A_label_bounded(B,L)
       + BoundaryError(T,a,L,B,W).
```

This formula is not a theorem.  Its value is negative discipline: it
forces every empirical number to say which analytic error it is meant
to bound.

## 4. Immediate Use

Use these constants only to decide which mathematical branch is worth
formalizing:

- continue analytic branch if the constants can be attached to a
  genuine operator and norm;
- downgrade to finite-rank fallback if they remain finite-window
  diagnostics with no projection meaning;
- ask a collaborator if the missing step is compactness, weighted
  symbolic summability, or a martingale/profinite BV theorem.
