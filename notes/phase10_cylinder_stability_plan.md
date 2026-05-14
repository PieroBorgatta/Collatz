# Phase 10 Cylinder Stability Plan

Date: 2026-05-13

Status: experiment design note.  This note specifies the first Gate 10.B
diagnostic that should be run before any new spectral-radius or
Lasota-Yorke claim.  It does not report new numerical evidence.

Related notes:

- `notes/phase10_operator_gate.md`
- `notes/phase10_orientation.md`
- `notes/phase10_candidate_operator.md`
- `notes/phase10_cylinder_stability_results.md`

## 1. Purpose

Gate 10.B asks whether the finite matrices `FULL_T` and `FULL_{T,j}` can
be interpreted as projections or controlled approximants of a natural
infinite killed weighted operator.

The first concrete obstruction is high-bit dependence.  For fixed
`T`, residue `r`, and hit phase `h`, the high-bit lifts are

```text
t = r + j * 2^T.
```

If the first-return signature of these lifts is stable, or at least has
a controlled limiting distribution as `j -> infinity`, then a 2-adic or
symbolic operator remains plausible.

If the first-return signature fluctuates without a stable law, then
`FULL_{T,j}` is likely a finite sampling artifact rather than a
projection of a canonical infinite kernel.

## 2. Existing scripts and what they already do

The new diagnostic should reuse existing code rather than reimplementing
orbit tracing.

Relevant scripts:

- `scripts/spectral_program/75_critical_symbolic_operator.py`
  builds finite `full_T` by enumerating `0 <= t < 2^T`.
- `scripts/spectral_program/77_high_bit_tail_bound.py`
  samples high-bit lifts `t = r + j * 2^T`, assigns a majority signature
  to CORE, and assigns minority signatures to TAIL.
- `scripts/spectral_program/78_tail_row_certificate_probe.py`
  diagnoses row-wise tail mass and identifies worst tail source states.
- `scripts/spectral_program/79_boundary_tail_scaling.py`
  separates bulk states from boundary states with `v2(t) >= T`.
- `scripts/spectral_program/85_truncation_stability.py`
  studies truncation stability of finite matrix actions as `j_count`
  grows.

What is still missing:

- a direct cylinder-level test of return-signature stability for fixed
  `(T,r,h)`;
- separation of terminal/return instability, destination-phase
  instability, and weight-exponent `delta` instability;
- block comparison in `j`, not only prefix comparison;
- explicit go/no-go criteria for the 2-adic candidate.

## 3. Proposed future script

Implemented name:

```text
scripts/spectral_program/88_cylinder_signature_stability.py
```

The original plan used number `86`, but `86_scc_node_certificates.py`
already exists in `scripts/spectral_program`; the cylinder-stability
diagnostic therefore uses the next available spectral-program number.

The script should be diagnostic only.  It should not compute or advertise
new spectral-radius bounds.

Implementation convention:

- the diagnostic skips the single lift `t = 0` by default, because it is
  a zero-mass artifact for the intended 2-adic cylinder interpretation
  and can distort small prefix tests;
- use `--include-t-zero` only when deliberately reproducing the raw
  finite enumeration convention of the older scripts.

It should import and reuse:

```text
77_high_bit_tail_bound.py::setup
77_high_bit_tail_bound.py::trace_row
```

or the equivalent `trace_row` infrastructure from script 78.

## 4. Signature levels

For each lift

```text
t = r + j * 2^T
```

and hit phase `h`, trace one row and record several nested signatures.

### 4.1 Status signature

```text
S_status(j) =
  terminal
  or return.
```

Purpose:

- tests whether the killed domain is cylinder-stable.

Failure mode:

- terminal and return cases alternate indefinitely across high bits.

### 4.2 Phase signature

For nonterminal rows:

```text
S_phase(j) = dst_phase(j)
```

where

```text
dst_phase = (capped nu_2(t'), odd_part(t') mod 4, h+1 mod 4).
```

Purpose:

- tests whether the finite phase quotient has a stable image.

Failure mode:

- destination phase changes persistently in the bulk, not only near the
  valuation boundary.

### 4.3 Delta signature

For nonterminal rows:

```text
S_delta(j) = delta(j)
```

where

```text
delta(j) = bit_length(t') - bit_length(t).
```

Purpose:

- isolates instability of the weight from instability of the destination
  phase.

Failure mode:

- phase is stable but `delta` fluctuates without a limiting law.  This
  would weaken the weighted operator program but may leave an unweighted
  or differently weighted operator possible.

### 4.4 Full weighted signature

The current high-bit scripts use:

```text
S_full(j) =
  terminal
  or (return, dst_phase(j), delta(j)).
```

This is the signature used by CORE/TAIL majority splitting.

Purpose:

- matches the existing finite `FULL_{T,j}` construction.

Failure mode:

- majority signatures drift as `j_count` grows or differ between
  adjacent high-bit blocks.

## 5. Metrics to compute

For each cylinder group `(T,r,h)` and each block or prefix of `j`, compute
the following.

### 5.1 Distinct-count metrics

For each signature level:

```text
distinct_status_count
distinct_phase_count
distinct_delta_count
distinct_full_count
```

These are coarse instability flags.

### 5.2 Majority metrics

For each signature level:

```text
majority_signature
majority_count
majority_fraction = majority_count / block_size
```

Interpretation:

- `majority_fraction = 1` means exact stability on the tested block;
- high but non-unit majority may support a tail/perturbation model;
- drifting majority signatures are a serious warning.

### 5.3 Distribution metrics

For two blocks `A` and `B` in the high-bit lift coordinate:

```text
TV_A_B = 1/2 * sum_sig |p_A(sig) - p_B(sig)|.
```

Use this for:

- status distributions;
- phase distributions;
- delta distributions;
- full signature distributions.

Purpose:

- tests Cauchy behavior in `j`, not just prefix stabilization.

### 5.4 Tail-weight metrics

Using the current majority rule for a block:

```text
tail_count = block_size - majority_count
tail_weight = sum_{j not majority, nonterminal} 2^{-delta(j)}
tail_weight_fraction = tail_weight / full_weight
```

These feed a possible CORE/TAIL perturbation framework, but only after a
candidate operator is fixed.

### 5.5 Boundary metrics

Record whether the source is in the valuation boundary layer:

```text
boundary = (nu_2(t) >= T)
```

and aggregate separately:

- bulk: `nu_2(t) < T`;
- boundary: `nu_2(t) >= T`.

Interpretation:

- instability confined to the boundary may be addressable by a
  valuation-counting tail lemma;
- bulk instability is much more damaging for the 2-adic projection
  model.

## 6. Proposed run modes

### 6.1 Prefix-doubling mode

For fixed `T`, compare:

```text
j_count = 8, 16, 32, 64, 128, ...
```

Outputs:

- dominant signature at each `j_count`;
- majority fraction at each `j_count`;
- TV distance from previous prefix;
- number of groups whose dominant signature changed.

This extends script 85 but at the raw signature level.

### 6.2 Adjacent-block mode

For block size `B`, compare:

```text
j in [0,B)
j in [B,2B)
j in [2B,3B)
...
```

Outputs:

- pairwise TV distances between adjacent blocks;
- dominant signature changes across blocks;
- maximum and quantiles of block drift over `(r,h)`.

This is the most important anti-artifact test.  Prefix averages can look
stable while block distributions still drift.

### 6.3 T-refinement mode

Compare `T` and `T+1` by splitting a cylinder:

```text
r mod 2^T
```

into:

```text
r mod 2^{T+1},
r + 2^T mod 2^{T+1}.
```

Outputs:

- whether child cylinders inherit parent dominant signatures;
- whether apparent stability at depth `T` disappears at `T+1`.

Purpose:

- tests whether `FULL_T` is a coherent projective family.

### 6.4 Phase-vs-weight mode

Compare instability at three levels:

```text
status only,
phase only,
phase + delta.
```

Possible outcomes:

- status stable, phase stable, delta unstable:
  weighting is the main obstacle;
- status stable, phase unstable:
  quotient/projection is the obstacle;
- status unstable:
  killed domain regularity is the obstacle.

## 7. Output files

Recommended outputs for the future script:

```text
scripts/spectral_program/collatz_86_cylinder_group_summary.csv
scripts/spectral_program/collatz_86_signature_distribution.csv
scripts/spectral_program/collatz_86_block_drift.csv
scripts/spectral_program/collatz_86_decision_summary.md
```

### 7.1 Group summary CSV

One row per `(T,r,h,j_mode)`:

```text
T
r
h
mode
j_start
j_count
source_phase
boundary_flag
distinct_status_count
distinct_phase_count
distinct_delta_count
distinct_full_count
status_majority_fraction
phase_majority_fraction
delta_majority_fraction
full_majority_fraction
terminal_fraction
return_fraction
full_weight
tail_weight
tail_weight_fraction
dominant_status_signature
dominant_phase_signature
dominant_delta_signature
dominant_full_signature
```

### 7.2 Signature distribution CSV

One row per observed signature:

```text
T
r
h
mode
j_start
j_count
signature_level
signature
count
fraction
weight_sum
```

### 7.3 Block drift CSV

One row per adjacent block comparison:

```text
T
r
h
signature_level
block_a_start
block_b_start
block_size
tv_distance
dominant_a
dominant_b
dominant_changed
```

### 7.4 Decision summary Markdown

The summary should report:

- worst groups by full-signature TV distance;
- worst bulk groups;
- worst boundary groups;
- fraction of groups with exact status stability;
- fraction of groups with exact phase stability;
- fraction of groups with exact full-signature stability;
- number of dominant-signature flips under prefix doubling;
- qualitative branch recommendation.

## 8. Interpretation rules

These rules are intentionally qualitative until the first diagnostic run
is inspected.

### 8.1 Positive signal for the 2-adic operator branch

Evidence supports continuing the `Z_2 x H` branch if:

- status is stable on almost all bulk cylinders;
- destination phase is stable or has small block-TV drift;
- full-signature instability is mostly boundary-layer;
- prefix and adjacent-block distributions are Cauchy-like;
- T-refinement does not destroy dominant signatures.

This would not prove a Lasota-Yorke inequality.  It would only justify
continuing Gate 10.B.

### 8.2 Signal for weighted-operator trouble

If status and phase are stable but `delta` is not, then:

- the unweighted or differently normalized operator may still be
  meaningful;
- the current weight `2^{-delta}` is analytically suspect;
- Lasota-Yorke constants involving `delta` should not be formulated yet.

### 8.3 Signal for quotient/projection trouble

If destination phase is unstable in the bulk, then:

- `PhaseState V` is probably too coarse for an exact projection;
- one may need a larger symbolic state or countable episode state;
- `FULL_T` should not be treated as `E_T L I_T`.

### 8.4 Signal for killed-domain trouble

If terminal/return status is unstable in the bulk, then:

- the killed domain is unlikely to be clopen at useful cylinder depth;
- 2-adic Lipschitz/BV frameworks become fragile;
- an open-system CMS model may be more appropriate than a compact
  `Z_2 x H` map.

### 8.5 Signal for fallback

Switch toward finite-rank fallback if:

- adjacent-block TV distances do not decay with block size;
- dominant signatures keep flipping as `j_count` doubles;
- instability is not confined to valuation boundary layers;
- T-refinement repeatedly destroys apparent parent-cylinder stability.

## 9. What not to conclude

The diagnostic must not be used to claim:

- Conjecture 6;
- a spectral gap;
- an infinite-operator bound;
- Keller-Liverani convergence;
- Lasota-Yorke constants.

It can only support or reject the next modeling step.

## 10. Minimal next implementation

The first implementation should be narrow:

```text
python scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 10 \
  --j-counts 16,32,64 \
  --block-size 16 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 5000
```

Minimum outputs:

- group summary;
- signature distribution;
- block drift;
- markdown decision summary.

Acceptance for the first run:

- it must separate status, phase, delta, and full signatures;
- it must compare adjacent high-bit blocks, not only prefixes;
- it must report bulk and boundary separately;
- it must end with one of:

  ```text
  continue Z_2 branch;
  enlarge symbolic state;
  switch to countable episode graph;
  switch to finite-rank fallback;
  inconclusive.
  ```
