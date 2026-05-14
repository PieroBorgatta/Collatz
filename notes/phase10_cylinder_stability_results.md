# Phase 10 Cylinder Stability Results

Date: 2026-05-13

Status: diagnostic note.  These results are finite computations for
Gate 10.B only.  They do not prove an infinite operator exists, do not
prove a Lasota-Yorke inequality, do not prove Keller-Liverani
convergence, and do not imply a spectral gap.

Related files:

- `notes/phase10_cylinder_stability_plan.md`
- `notes/phase10_candidate_operator.md`
- `scripts/spectral_program/88_cylinder_signature_stability.py`
- `scripts/spectral_program/89_phase_split_inspector.py`
- `scripts/spectral_program/90_refinement_coordinate_score.py`
- `scripts/spectral_program/91_refined_state_stability_probe.py`
- `scripts/spectral_program/92_delta_obstruction_summary.py`
- `scripts/spectral_program/93_delta_tail_weight.py`
- `scripts/spectral_program/94_block_cauchy_summary.py`
- `scripts/spectral_program/95_bad_cell_stratification.py`
- `scripts/spectral_program/collatz_88_decision_summary.md`
- `scripts/spectral_program/collatz_89_phase_split_summary.md`
- `scripts/spectral_program/collatz_90_refinement_coordinate_report.md`
- `scripts/spectral_program/collatz_91_refined_state_report.md`
- `scripts/spectral_program/collatz_92_delta_obstruction_report.md`
- `scripts/spectral_program/collatz_93_delta_tail_weight_report.md`
- `scripts/spectral_program/collatz_94_T15_j32_block_cauchy_report.md`
- `scripts/spectral_program/collatz_94_T16_j8_block_cauchy_report.md`
- `scripts/spectral_program/collatz_95_T16_j8_bad_cell_stratification_report.md`

## 1. Implemented diagnostic

Implemented script:

```text
scripts/spectral_program/88_cylinder_signature_stability.py
```

The originally planned number `86` was not used because
`86_scc_node_certificates.py` already exists.

The script tests high-bit lift stability for

```text
t = r + j * 2^T
```

at four nested signature levels:

- `status`: terminal vs return;
- `phase`: destination phase only;
- `delta`: bit-length exponent only;
- `full`: existing CORE/TAIL signature `(terminal)` or
  `(return,dst_phase,delta)`.

The script skips `t = 0` by default because that single lift is a
zero-mass artifact for the intended 2-adic cylinder interpretation.

## 2. Smoke and calibration runs

### 2.1 Smoke run

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 4 \
  --j-counts 4,8 \
  --block-size 4 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 8 \
  --max-steps 1000
```

Result:

- script completed;
- output schema validated;
- no spectral-radius computation was performed;
- diagnostic recommendation was `killed-domain trouble`.

This run is only a smoke test and should not be interpreted
mathematically.

### 2.2 Calibration run at `T = 6`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 6 \
  --j-counts 8,16 \
  --block-size 8 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 3000
```

Selected aggregate signals:

- final prefix groups: `256`;
- bulk groups: `252`;
- bulk exact status-majority fraction: approximately `0.571429`;
- bulk exact phase-majority fraction: approximately `0.523810`;
- bulk exact full-majority fraction: approximately `0.523810`;
- full-signature TV p95: approximately `0.375`.

Interpretation:

- instability is visible even away from the boundary layer;
- this is too small a `T` to decide 10.B, but it is a useful calibration
  of the diagnostic.

### 2.3 Calibration run at `T = 8`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 8 \
  --j-counts 8,16 \
  --block-size 8 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 3000
```

Selected aggregate signals:

- final prefix groups: `1024`;
- bulk groups: `1020`;
- bulk exact status-majority fraction: approximately `0.647059`;
- bulk exact phase-majority fraction: approximately `0.611765`;
- bulk exact full-majority fraction: approximately `0.592157`;
- status TV p95: approximately `0.125`;
- phase TV p95: approximately `0.25`;
- full TV p95: approximately `0.25`.

Interpretation:

- stability improves with `T`, but not enough to identify the phase
  quotient as a clean projection;
- there remain bulk cylinders with phase majority as low as `0.25`.

## 3. Main diagnostic runs at `T = 10`

### 3.1 Run with `j <= 32`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 10 \
  --j-counts 16,32 \
  --block-size 16 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000
```

Output files:

- `scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- `scripts/spectral_program/collatz_88_signature_distribution.csv`
- `scripts/spectral_program/collatz_88_block_drift.csv`
- `scripts/spectral_program/collatz_88_decision_summary.md`

Selected aggregate signals from the generated decision summary:

- final prefix `j_count`: `32`;
- final prefix groups: `4096`;
- boundary group share: `0.000976562`;
- bulk exact status-majority fraction: `0.596285`;
- bulk exact phase-majority fraction: `0.577713`;
- bulk exact full-majority fraction: `0.532747`;
- bulk average status-majority fraction: `0.962793`;
- bulk average phase-majority fraction: `0.952102`;
- bulk average delta-majority fraction: `0.942693`;
- bulk average full-majority fraction: `0.935545`;
- stable-status bulk groups with phase majority `<= 0.5`: `60`;
- status dominant flip fraction across adjacent blocks: `0.000976562`;
- phase dominant flip fraction across adjacent blocks: `0`;
- delta dominant flip fraction across adjacent blocks: `0.0126953`;
- full dominant flip fraction across adjacent blocks: `0.015625`;
- status TV p95: `0.125`;
- phase TV p95: `0.1875`;
- delta TV p95: `0.125`;
- full TV p95: `0.1875`;
- preliminary recommendation: `enlarge symbolic state`.

### 3.2 Run with `j <= 64`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 10 \
  --j-counts 32,64 \
  --block-size 32 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000
```

Selected aggregate signals from the generated decision summary:

- final prefix `j_count`: `64`;
- final prefix groups: `4096`;
- boundary group share: `0.000976562`;
- bulk exact status-majority fraction: `0.533724`;
- bulk exact phase-majority fraction: `0.515152`;
- bulk exact full-majority fraction: `0.468231`;
- bulk average status-majority fraction: `0.962549`;
- bulk average phase-majority fraction: `0.951918`;
- bulk average delta-majority fraction: `0.942464`;
- bulk average full-majority fraction: `0.935239`;
- stable-status bulk groups with phase majority `<= 0.5`: `60`;
- status dominant flip fraction across adjacent blocks: `0`;
- phase dominant flip fraction across adjacent blocks: `0.00195312`;
- delta dominant flip fraction across adjacent blocks: `0.00878906`;
- full dominant flip fraction across adjacent blocks: `0.0117188`;
- status TV p95: `0.09375`;
- phase TV p95: `0.125`;
- delta TV p95: `0.09375`;
- full TV p95: `0.15625`;
- preliminary recommendation: `enlarge symbolic state`.

Interpretation:

- increasing the tested prefix from `32` to `64` does not remove the
  stable-status/phase-split obstruction;
- adjacent-block dominant-signature flips are rare, which argues against
  purely chaotic high-bit behavior on this window;
- the exact full-signature majority fraction decreases because more
  high-bit lifts expose additional sub-signatures;
- the average majority fractions remain high, so the right next question
  is not a new spectral-radius computation but a refinement-coordinate
  search.

## 4. Phase-split coordinate inspection

Implemented script:

```text
scripts/spectral_program/89_phase_split_inspector.py
```

The first inspection selected the worst `h = 0` stable-status groups
from the latest `j <= 64` run, with destination-phase majority at most
`0.5` and status majority equal to `1`.

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/89_phase_split_inspector.py \
  --j-count 64 \
  --limit-groups 12 \
  --h 0 \
  --max-phase-majority 0.5 \
  --min-status-majority 1.0
```

Selected groups:

```text
r = 556, 783, 643, 525, 1023, 166, 636, 871, 813, 131, 44, 511.
```

For destination phase, several of the `phase_majority = 0.5` examples
are completely explained by very small high-bit coordinates such as
`j mod 2`; examples include `r = 44`, `r = 131`, and `r = 511`.

For full weighted signatures, the best simple coordinates are usually
larger high-bit residues such as `j mod 16`, `j mod 32`, or the
corresponding `next_t mod 2^q`; even there, the split is generally not
perfect.  In the inspected sample:

- `r = 813` has full-signature weighted purity `0.9375` under
  `j mod 32`, but the minimum bucket purity is only `0.5`;
- `r = 166` has full-signature weighted purity `0.921875` under
  `j mod 32` and under `next_t mod 32`, again with minimum bucket purity
  `0.5`;
- several other worst groups remain below perfect full-signature purity
  even at `j mod 32`.

Interpretation:

- some phase splits are compatible with a finite symbolic refinement;
- the full weighted signature is harder than destination phase because
  the exponent `delta` contributes additional variation;
- the current evidence favors "enlarge symbolic state" over "current
  phase quotient is an exact 2-adic projection";
- this remains a finite diagnostic, not an analytic theorem.

## 5. Global refinement-coordinate scoring

Implemented script:

```text
scripts/spectral_program/90_refinement_coordinate_score.py
```

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/90_refinement_coordinate_score.py \
  --j-count 64 \
  --progress
```

The script selected all `60` bulk groups in the `T = 10`, `j <= 64`
summary with status majority `1.0` and phase majority at most `0.5`.
It scores candidate refinement coordinates group-by-group, then
aggregates the resulting purities.

Best global coordinates for destination phase:

| coordinate | groups | mean purity | p10 purity | min purity | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 60 | `0.979167` | `0.96875` | `0.953125` | `1` | `0.333333` |
| `j_mod_16` | 60 | `0.951042` | `0.921875` | `0.90625` | `0.4` | `0.333333` |
| `j_mod_8` | 60 | `0.904167` | `0.84375` | `0.828125` | `0.4` | `0.333333` |

Best global coordinates for full weighted signature:

| coordinate | groups | mean purity | p10 purity | min purity | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 60 | `0.85625` | `0.78125` | `0.765625` | `0.4` | `0` |
| `j_mod_16` | 60 | `0.784375` | `0.65625` | `0.640625` | `0.133333` | `0` |
| `j_mod_8` | 60 | `0.722917` | `0.5625` | `0.5625` | `0.0666667` | `0` |

Interpretation:

- high-bit residue coordinates, especially `j mod 32`, are currently the
  strongest simple refinement candidates for destination phase;
- the `j mod 32` score must be treated cautiously because for
  `j_count = 64` it has average bucket size only `2`;
- full weighted signatures remain substantially less explained than
  destination phase, so `delta` or finer return-signature information is
  still missing;
- no tested coordinate gives a perfect global explanation of the full
  signature.

Next stress test:

```text
T = 10, j_count = 128
```

The goal is to check whether `j mod 32` remains strong with four samples
per bucket, and whether `j mod 64` merely inherits the same near-trivial
two-sample behavior.

## 6. Stress test at `T = 10`, `j <= 128`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 10 \
  --j-counts 64,128 \
  --block-size 64 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000 \
  --progress
```

Selected aggregate signals:

- final prefix `j_count`: `128`;
- final prefix groups: `4096`;
- boundary group share: `0.000976562`;
- bulk exact status-majority fraction: `0.515152`;
- bulk exact phase-majority fraction: `0.496579`;
- bulk exact full-majority fraction: `0.449658`;
- bulk average status-majority fraction: `0.962037`;
- bulk average phase-majority fraction: `0.951414`;
- bulk average delta-majority fraction: `0.941891`;
- bulk average full-majority fraction: `0.934636`;
- stable-status bulk groups with phase majority `<= 0.5`: `56`;
- status dominant flip fraction across adjacent blocks: `0`;
- phase dominant flip fraction across adjacent blocks: `0.00195312`;
- delta dominant flip fraction across adjacent blocks: `0.000976562`;
- full dominant flip fraction across adjacent blocks: `0.00585938`;
- status TV p95: `0.0625`;
- phase TV p95: `0.09375`;
- delta TV p95: `0.078125`;
- full TV p95: `0.125`;
- preliminary recommendation: `enlarge symbolic state`.

Interpretation:

- the number of stable-status/phase-unstable bulk groups decreases from
  `60` to `56`, but the obstruction persists;
- adjacent-block distribution drift improves with the larger block size,
  so the data are compatible with a stable limiting distribution rather
  than arbitrary high-bit noise;
- exact concentration in the existing phase quotient remains absent for
  many bulk groups.

## 7. Strict refinement-coordinate scoring at `j <= 128`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/90_refinement_coordinate_score.py \
  --j-count 128 \
  --min-avg-bucket-size 4
```

The stricter bucket-size threshold excludes coordinates that only have
two samples per bucket on the `j <= 128` prefix, such as `j mod 64`.

Best strict global coordinates for destination phase:

| coordinate | groups | mean purity | p10 purity | min purity | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 56 | `0.972656` | `0.953125` | `0.953125` | `0.357143` | `0.285714` |
| `j_mod_16` | 56 | `0.947545` | `0.914062` | `0.914062` | `0.357143` | `0.285714` |
| `j_mod_8` | 56 | `0.897321` | `0.835938` | `0.835938` | `0.357143` | `0.285714` |

Best strict global coordinates for full weighted signature:

| coordinate | groups | mean purity | p10 purity | min purity | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 56 | `0.794643` | `0.679688` | `0.671875` | `0.142857` | `0` |
| `j_mod_16` | 56 | `0.746652` | `0.601562` | `0.59375` | `0.0714286` | `0` |
| `j_mod_8` | 56 | `0.696987` | `0.53125` | `0.523438` | `0.0714286` | `0` |

Interpretation:

- `j mod 32` remains a serious finite-refinement candidate for
  destination phase on this tested window;
- it is not a full operator coordinate, because it leaves substantial
  full-signature variation;
- the analytic branch should split the question into:
  - phase refinement;
  - weight/return-signature refinement;
  - tail/killing regularity.

## 8. Cross-`T` stress test at `T = 11`, `j <= 128`

Command:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 11 \
  --j-counts 64,128 \
  --block-size 64 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000 \
  --progress
```

Selected aggregate signals:

- final prefix `j_count`: `128`;
- final prefix groups: `8192`;
- boundary group share: `0.000488281`;
- bulk exact status-majority fraction: `0.532487`;
- bulk exact phase-majority fraction: `0.517831`;
- bulk exact full-majority fraction: `0.464094`;
- bulk average status-majority fraction: `0.964086`;
- bulk average phase-majority fraction: `0.955415`;
- bulk average delta-majority fraction: `0.943503`;
- bulk average full-majority fraction: `0.937569`;
- stable-status bulk groups with phase majority `<= 0.5`: `84`;
- status dominant flip fraction across adjacent blocks: `0`;
- phase dominant flip fraction across adjacent blocks: `0.00146484`;
- delta dominant flip fraction across adjacent blocks: `0.000488281`;
- full dominant flip fraction across adjacent blocks: `0.00537109`;
- status TV p95: `0.0625`;
- phase TV p95: `0.09375`;
- delta TV p95: `0.078125`;
- full TV p95: `0.125`;
- preliminary recommendation: `enlarge symbolic state`.

Strict coordinate score:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/90_refinement_coordinate_score.py \
  --j-count 128 \
  --min-avg-bucket-size 4
```

Best strict global coordinates for destination phase:

| coordinate | groups | mean purity | p10 purity | min purity | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 84 | `0.97061` | `0.953125` | `0.953125` | `0.285714` | `0.285714` |
| `j_mod_16` | 84 | `0.942708` | `0.914062` | `0.914062` | `0.285714` | `0.285714` |
| `j_mod_8` | 84 | `0.886905` | `0.835938` | `0.835938` | `0.285714` | `0.285714` |

Best strict global coordinates for full weighted signature:

| coordinate | groups | mean purity | p10 purity | min purity | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 84 | `0.797619` | `0.679688` | `0.671875` | `0.142857` | `0` |
| `j_mod_16` | 84 | `0.75` | `0.625` | `0.609375` | `0.047619` | `0` |
| `j_mod_8` | 84 | `0.699777` | `0.585938` | `0.523438` | `0.047619` | `0` |

Interpretation:

- the destination-phase role of `j mod 32` persists from `T = 10` to
  `T = 11`;
- the full weighted signature remains insufficiently explained;
- the next mathematical object should therefore not be "the old
  `PhaseState` with a proof", but a refined state separating phase,
  `delta`, and return-signature data.

## 9. Refined-state probe on the `T = 11` obstruction groups

Implemented script:

```text
scripts/spectral_program/91_refined_state_stability_probe.py
```

First probe:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/91_refined_state_stability_probe.py \
  --coordinates j_mod_8,j_mod_16,j_mod_32 \
  --min-cell-size 4
```

For `j_mod_32` on the latest `T = 11`, `j_count = 128` selected
obstruction groups:

| target | source mean majority | refined cell mean majority | exact cell fraction | mean cell size |
|---|---:|---:|---:|---:|
| destination phase | `0.321429` | `0.97061` | `0.949405` | `4` |
| full weighted signature | `0.256324` | `0.797619` | `0.458333` | `4` |

Second probe with a compound diagnostic coordinate:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python \
  scripts/spectral_program/91_refined_state_stability_probe.py \
  --coordinates j_mod_32,j_mod_32+delta,j_mod_32+next_t_mod_32 \
  --min-cell-size 2
```

For `j_mod_32 + delta`:

| target | source mean majority | refined cell mean majority | exact cell fraction | mean cell size |
|---|---:|---:|---:|---:|
| destination phase | `0.321429` | `0.97653` | `0.955335` | `3.05459` |
| full weighted signature | `0.256324` | `0.97653` | `0.955335` | `3.05459` |

Interpretation:

- `j_mod_32` should be understood as five additional 2-adic bits beyond
  the base `T`-cylinder, not as a mysterious new variable;
- those bits almost stabilize destination phase on the selected
  obstruction groups;
- full-signature variation is mostly the remaining `delta` variation;
- adding `delta` to the coordinate is diagnostic, not a legitimate
  operator definition unless `delta` can be made locally constant or
  branch-measurable before the transition.

## 10. Deep-cylinder test: treating `j mod 32` as five extra bits

The coordinate `j mod 32` was then tested as a real deeper cylinder
coordinate by running script `88` at `T = 15`.

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

Selected final-prefix signals at `j_count = 16`:

- final prefix groups: `131072`;
- boundary group share: `0`;
- bulk exact status-majority fraction: `0.794312`;
- bulk exact phase-majority fraction: `0.785004`;
- bulk exact delta-majority fraction: `0.724670`;
- bulk exact full-majority fraction: `0.723785`;
- bulk average status-majority fraction: `0.974754`;
- bulk average phase-majority fraction: `0.968542`;
- bulk average delta-majority fraction: `0.952701`;
- bulk average full-majority fraction: `0.948709`;
- stable-status bulk groups with phase majority `<= 0.5`: `1096`;
- stable-status bulk groups with full-signature majority `<= 0.5`:
  `2048`;
- status dominant flip fraction across adjacent blocks: `0.00244141`;
- phase dominant flip fraction across adjacent blocks: `0.000793457`;
- delta dominant flip fraction across adjacent blocks: `0.0167542`;
- full dominant flip fraction across adjacent blocks: `0.0177002`;
- status TV p95: `0.125`;
- phase TV p95: `0.25`;
- delta TV p95: `0.25`;
- full TV p95: `0.25`.

Interpretation:

- the deeper cylinder partition is substantially better than the
  original `T = 10` phase quotient;
- it still does not produce exact local constancy, even for destination
  phase;
- full-signature instability remains materially worse than phase
  instability;
- therefore the refined-state branch is plausible but not yet past Gate
  10.B.

## 11. Delta and residual phase obstruction

Script `92_delta_obstruction_summary.py` was run on the `T = 15`,
`j_count = 16` output.

Selected aggregate signals:

- phase exact fraction: `0.785004`;
- delta exact fraction: `0.72467`;
- full exact fraction: `0.723785`;
- phase exact but delta non-exact fraction: `0.0612183`;
- phase exact but full non-exact fraction: `0.0612183`;
- phase non-exact but delta exact fraction: `0.00088501`;
- both phase and delta non-exact fraction: `0.214111`;
- status+phase exact but delta non-exact groups: `8024`;
- stable-status phase-majority `<= 0.5` groups: `1096`.

The worst phase-exact but delta-non-exact examples are simple two-point
splits, for example:

```text
return|2 : 0.5, return|3 : 0.5.
```

Script `89_phase_split_inspector.py` was also run on the worst
`T = 15`, `j_count = 16`, `h = 0` phase-low groups.  In that sample:

- the best simple destination-phase coordinate is typically `j_mod_8`;
- destination-phase weighted purity reaches `0.875` with average bucket
  size `2`;
- full-signature weighted purity remains only about `0.625` to `0.75`
  on the worst inspected groups.

Interpretation:

- the residual obstruction is mixed;
- some rows are phase-stable and only `delta`-unstable;
- many others still need deeper phase information;
- a credible infinite model must therefore separate phase depth,
  `delta`/weight labels, and tail control.

### 11.1 Prefix-doubling update: `T = 15`, `j_count = 32`

The deeper-cylinder test was doubled from `j_count = 16` to
`j_count = 32`.

Selected final-prefix signals:

- bulk exact status-majority fraction: `0.739410`;
- bulk exact phase-majority fraction: `0.729584`;
- bulk exact delta-majority fraction: `0.662750`;
- bulk exact full-majority fraction: `0.662506`;
- bulk average status-majority fraction: `0.974776`;
- bulk average phase-majority fraction: `0.968593`;
- bulk average delta-majority fraction: `0.951774`;
- bulk average full-majority fraction: `0.947732`;
- stable-status phase-majority `<= 0.5` groups: `1096`;
- stable-status full-majority `<= 0.5` groups: `2108`;
- phase dominant flip fraction across adjacent blocks: `0.000701904`;
- delta dominant flip fraction across adjacent blocks: `0.0109253`;
- full dominant flip fraction across adjacent blocks: `0.0124817`;
- phase TV p95: `0.1875`;
- full TV p95: `0.1875`.

The exact fractions decrease with the longer prefix, while the average
majorities remain high and adjacent-block dominant flips remain rare.
This is evidence against exact local constancy, but still compatible
with a distributional/Cesaro approximation program.

Script `92_delta_obstruction_summary.py` at `j_count = 32` gives:

- phase exact fraction: `0.729584`;
- delta exact fraction: `0.66275`;
- full exact fraction: `0.662506`;
- phase exact but delta non-exact fraction: `0.0670776`;
- both phase and delta non-exact fraction: `0.270172`;
- status+phase exact but delta non-exact groups: `8792`.

### 11.2 Cross-level check: `T = 16`, `j_count = 8`

The five-bit refinement pattern was checked one level higher by running
script `88` at `T = 16`, `j_counts = 4,8`.

Selected final-prefix signals:

- bulk exact status-majority fraction: `0.869583`;
- bulk exact phase-majority fraction: `0.861542`;
- bulk exact delta-majority fraction: `0.806473`;
- bulk exact full-majority fraction: `0.804413`;
- bulk average status-majority fraction: `0.976719`;
- bulk average phase-majority fraction: `0.971191`;
- bulk average delta-majority fraction: `0.955656`;
- bulk average full-majority fraction: `0.952102`;
- stable-status phase-majority `<= 0.5` groups: `1952`;
- stable-status full-majority `<= 0.5` groups: `5680`;
- phase dominant flip fraction across adjacent blocks: `0.00665283`;
- delta dominant flip fraction across adjacent blocks: `0.0227661`;
- full dominant flip fraction across adjacent blocks: `0.0238647`.

Interpretation:

- `T = 16` repeats the same qualitative pattern as `T = 15` on the
  comparable short prefix;
- deeper cylinders help substantially;
- worst cells and full-signature variation remain.

The `T = 16`, `j_count = 8` delta-obstruction summary gives:

- phase exact fraction: `0.861542`;
- delta exact fraction: `0.806473`;
- full exact fraction: `0.804413`;
- phase exact but delta non-exact fraction: `0.0571289`;
- both phase and delta non-exact fraction: `0.136398`;
- status+phase exact but delta non-exact groups: `14976`.

### 11.3 Weighted delta-tail checks

Implemented script:

```text
scripts/spectral_program/93_delta_tail_weight.py
```

This script reads the `88` outputs and measures only the weighted
`delta` tail, using the `2^{-delta}` weights already emitted by script
`88`.  It does not trace orbits and does not compute a spectral radius.
The optional `--output-tag` keeps multiple reports side by side.

Commands:

```text
python3 scripts/spectral_program/93_delta_tail_weight.py \
  --T 16 \
  --j-count 8 \
  --max-threshold 8 \
  --worst-threshold 4 \
  --output-tag T16_j8

python3 scripts/spectral_program/93_delta_tail_weight.py \
  --T 15 \
  --j-count 32 \
  --max-threshold 8 \
  --worst-threshold 4 \
  --output-tag T15_j32
```

Selected output from
`scripts/spectral_program/collatz_93_T16_j8_delta_tail_weight_report.md`:

- groups: `262144`;
- groups with nonzero return weight: `55476`;
- terminal count fraction: `0.895004`;
- return count: `220192`;
- weighted return mass: `64130.3369141`;
- max delta observed: `12`.

Selected output from
`scripts/spectral_program/collatz_93_T15_j32_delta_tail_weight_report.md`:

- groups: `131072`;
- groups with nonzero return weight: `44536`;
- terminal count fraction: `0.895062`;
- return count: `440140`;
- weighted return mass: `128432.050293`;
- max delta observed: `13`.

Weighted delta distribution at `T = 16`, `j_count = 8`:

| delta | count fraction | weight fraction | cumulative weight fraction |
|---:|---:|---:|---:|
| 0 | `0.0274306` | `0.0941832` | `0.0941832` |
| 1 | `0.267566` | `0.459346` | `0.553529` |
| 2 | `0.413675` | `0.355089` | `0.908618` |
| 3 | `0.167` | `0.0716743` | `0.980293` |
| 4 | `0.0726275` | `0.0155854` | `0.995878` |
| 5 | `0.0303735` | `0.00325899` | `0.999137` |
| 6 | `0.0129523` | `0.000694874` | `0.999832` |
| 7 | `0.00492298` | `0.000132055` | `0.999964` |
| 8 | `0.00225258` | `0.0000302119` | `0.999994` |

Tail threshold comparison:

| run | keep `delta <= L` | global weighted tail | group tail p95 | group tail max |
|---|---:|---:|---:|---:|
| `T16_j8` | 4 | `0.00412187` | `1` | `1` |
| `T16_j8` | 5 | `0.000862882` | `0.047619` | `1` |
| `T16_j8` | 8 | `0.00000574087` | `0` | `1` |
| `T15_j32` | 4 | `0.0040648` | `0.2` | `1` |
| `T15_j32` | 5 | `0.000845196` | `0.0379747` | `1` |
| `T15_j32` | 8 | `0.00000635292` | `0` | `0.2` |

Interpretation:

- globally, the `2^{-delta}` normalization makes the large-delta tail
  very small and remarkably stable across the two tested finite
  windows;
- locally, a few low-return-weight groups can have all their return
  mass at large delta, so uniform cellwise tail control is not automatic;
- this supports a weighted-tail Banach target but not a finite
  projection theorem;
- a useful Lasota-Yorke target should separate global weighted tail
  estimates from uniform or weighted-local tail estimates.

### 11.4 Adjacent-block Cauchy diagnostics

Implemented script:

```text
scripts/spectral_program/94_block_cauchy_summary.py
```

Command:

```text
python3 scripts/spectral_program/94_block_cauchy_summary.py \
  --T 15 \
  --j-count 16 \
  --worst-level full \
  --output-tag T15_B8_j16

python3 scripts/spectral_program/94_block_cauchy_summary.py \
  --T 15 \
  --j-count 32 \
  --worst-level full \
  --output-tag T15_j32

python3 scripts/spectral_program/94_block_cauchy_summary.py \
  --T 15 \
  --j-count 64 \
  --worst-level full \
  --output-tag T15_B32_j64

python3 scripts/spectral_program/94_block_cauchy_summary.py \
  --T 16 \
  --j-count 8 \
  --worst-level full \
  --output-tag T16_j8
```

Selected output from
`scripts/spectral_program/collatz_94_T15_j32_block_cauchy_report.md`:

| level | mean TV | p95 TV | p99 TV | max TV | dominant flip fraction |
|---|---:|---:|---:|---:|---:|
| status | `0.0182055` | `0.125` | `0.1875` | `0.375` | `0.0012207` |
| phase | `0.0294743` | `0.1875` | `0.25` | `0.4375` | `0.000701904` |
| delta | `0.0297394` | `0.125` | `0.1875` | `0.4375` | `0.0109253` |
| full | `0.0381069` | `0.1875` | `0.25` | `0.5` | `0.0124817` |

Selected class-level signals:

- `status_exact` cells have full-signature mean TV `0.00846609` and
  p95 `0.0625`;
- `phase_low` cells have full-signature mean TV `0.236453` and p95
  `0.4375`;
- `full_low` cells have full-signature mean TV `0.19338` and p95
  `0.375`;
- high full-tail-weight cells have full-signature mean TV `0.124907`
  and p95 `0.25`.

Fixed-`T=15` block-doubling gives:

| block size | compared blocks | full mean TV | full p95 TV | full p99 TV | full max TV | dominant flip fraction |
|---:|---|---:|---:|---:|---:|---:|
| 8 | `0..7` vs `8..15` | `0.0462265` | `0.25` | `0.375` | `0.75` | `0.0177002` |
| 16 | `0..15` vs `16..31` | `0.0381069` | `0.1875` | `0.25` | `0.5` | `0.0124817` |
| 32 | `0..31` vs `32..63` | `0.0310087` | `0.15625` | `0.21875` | `0.375` | `0.011322` |

This is compatible with a Cauchy-type block target, but it is not a
limit theorem and should not be used as Keller-Liverani convergence.

For `T = 16`, `j_count = 8`, using adjacent blocks of size `4`, the
aggregate full-signature TV is larger:

| level | mean TV | p95 TV | p99 TV | max TV | dominant flip fraction |
|---|---:|---:|---:|---:|---:|
| status | `0.0301514` | `0.25` | `0.5` | `0.75` | `0.0105591` |
| phase | `0.0400963` | `0.25` | `0.5` | `1` | `0.00665283` |
| delta | `0.0440102` | `0.25` | `0.5` | `0.75` | `0.0227661` |
| full | `0.0507774` | `0.25` | `0.5` | `1` | `0.0238647` |

The shorter block size makes this comparison less stable than the
`T15_j32` block `16+16` diagnostic, but it reinforces that the worst
phase/full cells carry large distributional drift.

Interpretation:

- rare dominant-signature flips are not enough: full-signature TV drift
  can remain substantial even when the dominant label does not change;
- status-exact cells are much calmer, which supports a killed-domain
  decomposition;
- the bad phase/full cells are exactly where a normed distributional
  error would have to pay a tail or refinement cost;
- this is compatible with a Cesaro/block target, but still far from a
  convergence theorem.

### 11.5 Truncated-label and bounded-label block diagnostics

Implemented scripts:

```text
scripts/spectral_program/97_truncated_label_block_tv.py
scripts/spectral_program/98_bounded_label_excess.py
```

Commands:

```text
python3 scripts/spectral_program/97_truncated_label_block_tv.py \
  --T 15 \
  --block-size 32 \
  --cutoffs 2,3,4,5,8 \
  --output-tag T15_B32_j64

python3 scripts/spectral_program/98_bounded_label_excess.py \
  --T 15 \
  --block-size 32 \
  --cutoffs 2,3,4,5,8 \
  --output-tag T15_B32_j64
```

Selected output from
`scripts/spectral_program/collatz_97_T15_B32_j64_truncated_label_block_tv_report.md`:

| transform | count mean TV | count p95 | count p99 | count max |
|---|---:|---:|---:|---:|
| `status` | `0.0128616` | `0.0625` | `0.125` | `0.25` |
| `phase` | `0.0230853` | `0.125` | `0.15625` | `0.28125` |
| `clip_2` | `0.0289039` | `0.125` | `0.1875` | `0.375` |
| `clip_3` | `0.0299863` | `0.125` | `0.1875` | `0.375` |
| `clip_4` | `0.0305662` | `0.15625` | `0.1875` | `0.375` |
| `clip_5` | `0.0308437` | `0.15625` | `0.21875` | `0.375` |
| `clip_8` | `0.031002` | `0.15625` | `0.21875` | `0.375` |
| `full` | `0.0310049` | `0.15625` | `0.21875` | `0.375` |

The run compared `131068` complete groups and skipped `4` incomplete
groups.  The skipped groups are a boundary artifact of the sampled
block partition, not evidence of a theorem or counterexample.

Selected output from
`scripts/spectral_program/collatz_98_T15_B32_j64_bounded_label_excess_report.md`:

| transform | phase mean TV | label mean TV | excess mean | excess p95 | excess p99 | excess max |
|---|---:|---:|---:|---:|---:|---:|
| `clip_2` | `0.0230853` | `0.0289039` | `0.00581854` | `0.03125` | `0.09375` | `0.25` |
| `clip_3` | `0.0230853` | `0.0299863` | `0.006901` | `0.03125` | `0.09375` | `0.25` |
| `clip_4` | `0.0230853` | `0.0305662` | `0.00748085` | `0.0625` | `0.09375` | `0.25` |
| `clip_5` | `0.0230853` | `0.0308437` | `0.00775838` | `0.0625` | `0.09375` | `0.25` |
| `clip_8` | `0.0230853` | `0.031002` | `0.00791669` | `0.0625` | `0.09375` | `0.25` |
| `full` | `0.0230853` | `0.0310049` | `0.00791955` | `0.0625` | `0.09375` | `0.25` |

Interpretation:

- clipping large `delta` labels barely reduces count-TV once
  `delta <= 4` or `delta <= 5` is retained;
- therefore the block-Cauchy obstruction is not only a large-`delta`
  tail obstruction;
- bounded retained-label variation is smaller than destination-phase
  movement but remains visible;
- the mixed-norm program should contain a separate
  `A_label_bounded(B,L)` term in addition to `A_phase_block(B)` and
  `DeltaTail(L)`;
- the weighted-TV columns in script `97` should be treated only as
  return-weight diagnostics, because terminal rows have zero return
  weight in the source distribution file.

### 11.6 Bad-cell stratification: `T = 16`, `j_count = 8`

Implemented script:

```text
scripts/spectral_program/95_bad_cell_stratification.py
```

Command:

```text
python3 scripts/spectral_program/95_bad_cell_stratification.py \
  --T 16 \
  --j-count 8 \
  --output-tag T16_j8 \
  --min-count 64 \
  --limit 12
```

Selected output from
`scripts/spectral_program/collatz_95_T16_j8_bad_cell_stratification_report.md`:

Global:

- groups: `262144`;
- phase exact fraction: `0.861542`;
- full exact fraction: `0.804413`;
- phase-low fraction: `0.0125122`;
- full-low fraction: `0.0267334`;
- high full-tail-weight fraction: `0.133743`;
- mean full majority: `0.952102`;
- mean full-tail-weight fraction: `0.154547`.

Selected strata:

| stratum | value | count | phase exact | full exact | phase low | full low | high tail | mean full majority | mean tail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `source_v2_odd` | `10|3` | `64` | `0.8125` | `0` | `0.125` | `0.125` | `0.0625` | `0.695312` | `0.427778` |
| `source_v2` | `10` | `128` | `0.71875` | `0.3125` | `0.09375` | `0.09375` | `0.1875` | `0.804688` | `0.391774` |
| `source_v2_odd` | `7|3` | `512` | `0.632812` | `0.632812` | `0.046875` | `0.046875` | `0.335938` | `0.916016` | `0.352469` |
| `source_v2_odd` | `2|3` | `16384` | `0.898926` | `0.383301` | `0.00976562` | `0.167969` | `0.0969238` | `0.792633` | `0.267488` |
| `source_v2_odd` | `0|3` | `65536` | `0.749695` | `0.692017` | `0.0187988` | `0.0320435` | `0.24469` | `0.930984` | `0.266609` |

Interpretation:

- the worst phase-low fractions occur in small high-`v2` strata, but
  there are also large strata, such as `v2=2, odd=3`, where destination
  phase is mostly stable while full-signature exactness is poor;
- full instability and high tail are therefore structured, not purely
  random, but the structure is not a proof of a drift function;
- a future Banach norm may need an explicit source-stratum weight in
  addition to `delta` tail and block-TV terms.

### 11.7 Error-budget aggregation: `T = 15`, `j_count = 64`

Implemented script:

```text
scripts/spectral_program/99_error_budget_summary.py
```

Command:

```text
python3 scripts/spectral_program/99_error_budget_summary.py \
  --T 15 \
  --prefix-j-count 64 \
  --block-size 32 \
  --cutoffs 2,3,4,5,8 \
  --output-tag T15_B32_j64
```

Selected output from
`scripts/spectral_program/collatz_99_T15_B32_j64_error_budget_summary.md`:

| proxy | value |
|---|---:|
| `DeltaTail_global(5)` | `0.000830424` |
| `DeltaTail_local_p95(5)` | `0.027027` |
| `DeltaTail_local_max(5)` | `1` |
| `A_phase_block` p95 | `0.125` |
| full `A_label_bounded` p95 | `0.0625` |
| boundary skipped fraction | `0.0000305176` |

Interpretation:

- the global weighted `delta` tail remains small at the larger
  `j_count = 64` prefix window;
- local p95 improves relative to the previous `T15_j32` tail report,
  but the local maximum remains `1`;
- therefore this supports the bookkeeping decomposition but not a
  uniform tail bound, not a compactness claim, and not a projection
  theorem.

## 12. Interpretation for Gate 10.B

The `T = 10` and `T = 11` runs do not support the strongest version of
the compact `Z_2 x H -> PhaseState V` projection model.

Reason:

- average bulk stability is high;
- adjacent-block dominant signature flips are relatively rare;
- however, there are bulk cylinders with status stably returning but
  destination phase strongly split;
- in particular, the diagnostic found `56` such groups at `T = 10`,
  `j <= 128`, and `84` at `T = 11`, `j <= 128`.

The worst stable-status phase examples include residues such as:

```text
r = 556, 783, 525, 643, 1023, ...
```

where the status is `return` throughout the tested prefixes but the
destination phase is not concentrated in a single `PhaseState` cell.

Provisional conclusion:

```text
The current PhaseState quotient is probably too coarse for an exact
2-adic projection statement.
```

This does not kill the analytic branch.  It suggests that the next
candidate should be one of:

1. an enlarged symbolic state that remembers additional high-bit or
   branch data;
2. a countable episode/return-signature graph;
3. a finite-rank fallback if no canonical refinement stabilizes.

The `T = 11` run reinforces this conclusion rather than reversing it.

The `T = 15` deeper-cylinder run shows that the best phase refinement is
useful, but also shows that usefulness is not the same as a projection
identity.

## 13. What these results do not show

These finite diagnostics do not show:

- convergence in `j`;
- convergence in `T`;
- existence of an infinite operator;
- compactness of any Banach embedding;
- a Lasota-Yorke inequality;
- Keller-Liverani stability;
- a spectral gap;
- Conjecture 6.

They only show that the naive phase quotient has visible high-bit
dependence at the return-signature level.

## 14. Recommended next action

The next useful step is still not another spectral-radius computation.
It is to convert the observed phase-depth and delta-tail signals into a
precise candidate norm and approximation statement.

Concrete options:

- finite phase refinement by adding `j mod 32` as a diagnostic
  coordinate;
- full-signature refinement by retaining bounded `delta <= L` and
  treating the complement as a weighted tail, not as zero;
- countable return-signature refinement if no finite `delta` class
  stabilizes.

Then rerun only diagnostics that feed named constants, for example:

```text
python3 scripts/spectral_program/93_delta_tail_weight.py \
  --T 15 \
  --j-count 32 \
  --max-threshold 8
```

Purpose:

- compare the weighted `delta` tail across `T` and prefix length;
- decide whether the tail bound should be global, weighted-local, or
  rejected as too nonuniform.
