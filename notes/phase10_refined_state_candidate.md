# Phase 10 Refined-State Candidate

Date: 2026-05-14

Status: modeling note.  This note proposes a diagnostic refinement to
test next.  It is not a proof that a refined finite matrix is a
projection of an infinite operator.

Related files:

- `notes/phase10_cylinder_stability_results.md`
- `scripts/spectral_program/90_refinement_coordinate_score.py`
- `scripts/spectral_program/91_refined_state_stability_probe.py`
- `scripts/spectral_program/93_delta_tail_weight.py`
- `scripts/spectral_program/collatz_91_refined_state_report.md`
- `scripts/spectral_program/collatz_93_delta_tail_weight_report.md`

## 1. Empirical trigger

The existing `PhaseState` quotient is too coarse for an exact 2-adic
projection statement on the tested windows.

At `T = 10` and `T = 11`, with `j_count = 128`, there are many bulk
groups whose terminal/return status is stable but whose destination
phase is split.

The strongest simple coordinate for the destination phase is:

```text
j mod 32.
```

For fixed base residue

```text
t = r + j * 2^T,
```

this coordinate is just the next five 2-adic bits of `t` beyond the
base cylinder modulo `2^T`.

Therefore the least artificial interpretation is:

```text
the current phase quotient is too shallow; try a deeper cylinder
partition before quotienting.
```

## 2. Candidate refined source cell

For a chosen depth increment `a = 5`, define a diagnostic refined source
cell by:

```text
C(T,r,q,h) =
  { t : t == r + q * 2^T mod 2^(T+a) } x {h},
q in Z / 2^a Z.
```

Equivalently:

```text
q = floor(t / 2^T) mod 2^a.
```

With `a = 5`, this is exactly `j mod 32` in the high-bit experiments.

This is preferable to treating `j` as an independent variable: in a
2-adic model, `j mod 32` is simply a deeper cylinder coordinate.

## 3. Diagnostic results

On the latest `T = 11`, `j_count = 128` selected obstruction groups,
script `91_refined_state_stability_probe.py` gives:

Destination phase, minimum cell size `4`:

```text
j_mod_32:
  source mean majority = 0.321429
  refined cell mean majority = 0.97061
  exact cell fraction = 0.949405
```

Full weighted signature, same refinement:

```text
j_mod_32:
  source mean majority = 0.256324
  refined cell mean majority = 0.797619
  exact cell fraction = 0.458333
```

Thus five additional 2-adic bits explain most destination-phase
variation in the selected obstruction groups, but they do not explain
the full weighted signature.

## 4. The role of `delta`

The full signature used by the scripts is essentially:

```text
full_signature = (destination phase, delta),
```

for nonterminal rows.

A diagnostic split by

```text
j_mod_32 + delta
```

raises the full-signature refined cell mean to about `0.97653` on the
same `T = 11`, `j_count = 128` selected groups.

This should not be overinterpreted:

- `delta` is a return outcome, not automatically a pre-transition state
  coordinate;
- using `delta` as a source coordinate would be circular unless one
  proves that it is locally constant or predictably measurable on a
  pre-transition branch partition;
- nevertheless, it indicates that the remaining full-signature
  variation after `j mod 32` is primarily weight/exponent variation, not
  destination-phase variation.

## 5. Refined operator options

Option A: deeper 2-adic phase projection.

```text
state = (t mod 2^(T+5), h)
then quotient destination phase separately.
```

Pros:

- natural in `Z_2`;
- directly matches `j mod 32`;
- avoids introducing a non-intrinsic coordinate.

Cons:

- state count grows by `32`;
- still does not control `delta` enough for the weighted operator.

Option B: transition-labelled finite kernel.

```text
source cell -> destination phase with edge label delta.
```

Pros:

- does not pretend `delta` is a state variable;
- matches the existing full signature.

Cons:

- for analytic work, one must control variation/summability of labels;
- Keller-Liverani still needs an operator on a Banach space, not just
  labelled finite edges.

Option C: countable return-signature graph.

```text
state or edge remembers enough of the return branch to determine
(destination phase, delta) up to tails.
```

Pros:

- mathematically honest if finite refinements keep failing;
- compatible with Sarig/CMS language if summability can be proved.

Cons:

- BIP/positive recurrence/summable variation are major open gates;
- may fail to produce compactness or an LY inequality.

## 6. Next Diagnostic

Do not compute a new spectral radius yet.

The next diagnostic should construct, for `T = 10` and `T = 11`, a
refined empirical kernel using source cells:

```text
(r mod 2^T, q mod 32, h)
```

and report:

- row stability of destination phase;
- row stability of `delta`;
- row stability of full signature;
- state-count growth;
- tail mass after majority splitting;
- whether the same `q mod 32` refinement remains useful outside the
  selected obstruction groups.

Only if that diagnostic gives coherent projections should a refined
finite operator be generated.

## 7. Deep-cylinder diagnostic actually run

The coordinate `j mod 32` was tested as a genuine deeper 2-adic
cylinder by increasing `T` by five bits.

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 15 \
  --j-counts 8,16 \
  --block-size 8 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000 \
  --progress
```

This probes cells modulo `2^15`, i.e. five bits deeper than the
`T = 10` base cells where `j mod 32` was first detected.

Selected output at final prefix `j_count = 16`:

| quantity | exact group fraction | average majority | minimum majority |
|---|---:|---:|---:|
| status | `0.794312` | `0.974754` | `0.5` |
| destination phase | `0.785004` | `0.968542` | `0.25` |
| delta | `0.724670` | `0.952701` | `0.3125` |
| full signature | `0.723785` | `0.948709` | `0.125` |

Additional signals:

- stable-status groups with phase majority at most `0.5`: `1096`;
- stable-status groups with full-signature majority at most `0.5`:
  `2048`;
- status dominant-flip fraction across adjacent blocks: `0.00244141`;
- phase dominant-flip fraction: `0.000793457`;
- delta dominant-flip fraction: `0.0167542`;
- full dominant-flip fraction: `0.0177002`.

Interpretation:

- deepening the cylinder by five bits is genuinely helpful;
- however, it does not establish local constancy of destination phase or
  full signature;
- full-signature instability remains more severe than phase instability;
- the dominant remaining obstruction is still the return/weight data,
  especially `delta`.

Verdict:

```text
The five-bit refinement is a useful modeling direction, but it is not
yet a projection theorem and not enough to define a certified infinite
operator.
```

## 8. Delta obstruction summary

Script:

```text
scripts/spectral_program/92_delta_obstruction_summary.py
```

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/92_delta_obstruction_summary.py \
  --j-count 16 \
  --limit 16
```

Selected aggregate output on the `T = 15`, `j_count = 16` data:

- phase exact fraction: `0.785004`;
- delta exact fraction: `0.72467`;
- full exact fraction: `0.723785`;
- phase exact but delta non-exact fraction: `0.0612183`;
- phase exact but full non-exact fraction: `0.0612183`;
- phase non-exact but delta exact fraction: `0.00088501`;
- both phase and delta non-exact fraction: `0.214111`;
- status+phase exact but delta non-exact groups: `8024`.

Interpretation:

- once phase is stabilized, full-signature failure is often exactly
  `delta` failure;
- however, a larger set has both phase and `delta` non-exact, so the
  problem is not purely a weight-label issue;
- a phase-only refinement is therefore insufficient for a weighted
  transfer operator.

Worst phase-exact/delta-non-exact examples have simple two-point
splits such as:

```text
return|2 : 0.5, return|3 : 0.5
```

This is compatible with a labelled-edge model, but it is not yet a
Banach-space operator.

## 9. Residual phase obstruction after deepening

Running `89_phase_split_inspector.py` on the worst `T = 15`,
`j_count = 16`, `h = 0` groups shows:

- the worst groups still have destination-phase majority `0.25`;
- `j_mod_8` is the best simple next coordinate in the inspected sample;
- for destination phase, `j_mod_8` gives weighted purity `0.875` with
  average bucket size `2`;
- for full signature, `j_mod_8` is materially weaker, typically
  `0.625` to `0.75` on the inspected groups.

Interpretation:

```text
The phase refinement appears hierarchical: five extra bits help, but
do not close the problem.  Additional bits help some residual phase
splits, while full signature still needs return/weight data.
```

This points toward a controlled tail/refinement program or a countable
return-signature graph, not toward a single finite quotient that can be
declared canonical today.

## 10. Prefix-doubling update at `j_count = 32`

The deeper-cylinder test was doubled once more:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 15 \
  --j-counts 16,32 \
  --block-size 16 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000 \
  --progress
```

Selected output at final prefix `j_count = 32`:

| quantity | exact group fraction | average majority | minimum majority |
|---|---:|---:|---:|
| status | `0.739410` | `0.974776` | `0.53125` |
| destination phase | `0.729584` | `0.968593` | `0.25` |
| delta | `0.662750` | `0.951774` | `0.375` |
| full signature | `0.662506` | `0.947732` | `0.125` |

Block drift:

- status dominant-flip fraction: `0.0012207`;
- phase dominant-flip fraction: `0.000701904`;
- delta dominant-flip fraction: `0.0109253`;
- full dominant-flip fraction: `0.0124817`;
- phase TV p95: `0.1875`;
- full TV p95: `0.1875`.

Interpretation:

- exact local constancy degrades as the prefix grows;
- average majorities remain high;
- dominant block flips are rare;
- this is evidence for a possible distributional/Cesaro model, not for
  exact cylinder constancy.

The `j_count = 32` delta obstruction summary gives:

- phase exact fraction: `0.729584`;
- delta exact fraction: `0.66275`;
- full exact fraction: `0.662506`;
- phase exact but delta non-exact fraction: `0.0670776`;
- both phase and delta non-exact fraction: `0.270172`;
- status+phase exact but delta non-exact groups: `8792`.

This reinforces the same conclusion:

```text
phase refinement helps, but the weighted operator needs a separate
delta/return-signature mechanism and probably a tail norm.
```

## 11. Cross-level deep-cylinder check at `T = 16`

To test whether the `T = 15` result was an accident, the same five-bit
deep-cylinder idea was run one level higher:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 16 \
  --j-counts 4,8 \
  --block-size 4 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000 \
  --progress
```

Selected output at final prefix `j_count = 8`:

| quantity | exact group fraction | average majority | minimum majority |
|---|---:|---:|---:|
| status | `0.869583` | `0.976719` | `0.5` |
| destination phase | `0.861542` | `0.971191` | `0.25` |
| delta | `0.806473` | `0.955656` | `0.375` |
| full signature | `0.804413` | `0.952102` | `0.125` |

Additional signals:

- stable-status phase-majority `<= 0.5` groups: `1952`;
- stable-status full-majority `<= 0.5` groups: `5680`;
- phase dominant-flip fraction: `0.00665283`;
- delta dominant-flip fraction: `0.0227661`;
- full dominant-flip fraction: `0.0238647`.

Interpretation:

- the five-bit refinement is again helpful at the next level;
- the worst cells remain bad;
- full-signature variation is again more severe than phase variation;
- this supports a hierarchical/distributional program, not an exact
  finite projection claim.

The `T = 16`, `j_count = 8` delta summary gives:

- phase exact fraction: `0.861542`;
- delta exact fraction: `0.806473`;
- full exact fraction: `0.804413`;
- phase exact but delta non-exact fraction: `0.0571289`;
- both phase and delta non-exact fraction: `0.136398`;
- status+phase exact but delta non-exact groups: `14976`.

The same two-point delta splits appear, for example:

```text
return|2 : 0.5, return|3 : 0.5.
```

This independently confirms that `delta` must be treated as an edge
label/tail issue rather than hidden inside the old phase quotient.

## 12. Weighted delta-tail check

Script:

```text
scripts/spectral_program/93_delta_tail_weight.py
```

Command on the current `T = 16`, `j_count = 8` output:

```text
python3 scripts/spectral_program/93_delta_tail_weight.py \
  --T 16 \
  --j-count 8 \
  --max-threshold 8 \
  --worst-threshold 4 \
  --output-tag T16_j8
```

The same diagnostic was also run after regenerating the `T = 15`,
`j_count = 32` output, with `--output-tag T15_j32`.

Selected output:

| run | retained labels | global weighted tail | local tail p95 |
|---|---|---:|---:|
| `T16_j8` | `delta <= 4` | `0.00412187` | `1` |
| `T16_j8` | `delta <= 5` | `0.000862882` | `0.047619` |
| `T16_j8` | `delta <= 8` | `0.00000574087` | `0` |
| `T15_j32` | `delta <= 4` | `0.0040648` | `0.2` |
| `T15_j32` | `delta <= 5` | `0.000845196` | `0.0379747` |
| `T15_j32` | `delta <= 8` | `0.00000635292` | `0` |

Interpretation:

- the existing `2^{-delta}` normalization makes the large-delta tail
  globally small on both tested finite windows;
- however, uniform cellwise tail control is stronger than global tail
  control and is not automatic at low thresholds;
- bounded-`delta` finite kernels should therefore be phrased as
  truncations with a quantified weighted tail, not as exact finite
  reductions.

## 13. Update After True 2-adic Child Tests

The five-bit refinement remains useful as a finite modelling device,
but it should not be read as evidence for naive full-label continuity
on `Z_2 x H`.

New diagnostic:

```text
scripts/spectral_program/100_z2_cylinder_oscillation.py
```

At `T = 15`, with `max_j = 128`, the full-label child-cylinder mean TV
over depths `0,1,2` is:

```text
0.0486132 -> 0.0487704 -> 0.0509391.
```

Thus deeper 2-adic child comparisons do not currently show contraction
of the full label.

New stratified diagnostic:

```text
scripts/spectral_program/101_z2_oscillation_strata.py
```

At depth `2`, the full-over-phase excess is concentrated in source
strata:

```text
source_v2_odd = 2|3:
mass = 0.0625,
mean excess = 0.120621,
contribution = 0.456409.
```

Interpretation:

- the old finite phase quotient is too coarse;
- adding 2-adic bits helps phase modelling but not full-label
  continuity;
- the remaining obstruction is structured by source-stratum and label
  data;
- the next refined state should therefore be labelled/symbolic, not
  merely a deeper unlabelled `Z_2` cylinder.
