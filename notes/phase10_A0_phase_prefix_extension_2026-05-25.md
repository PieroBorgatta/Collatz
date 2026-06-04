# Phase 10 A0 Phase-Prefix Extension

Date: 2026-05-25

Status: finite diagnostic update for the phase-only A0 branch.

## Question

After script `112_family_weighted_norm_probe.py` gave a negative result for
simple A1 source-family weighted norms, the main branch returns to A0:

```text
source alphabet = PhaseState
destination alphabet = PhaseState
```

The next finite question is whether the phase-only prefix drift continues to
decrease at the next prefix scale.

## Run

```text
python scripts/spectral_program/110_refined_square_probe.py \
  --T 14 \
  --j-counts 32,64,128 \
  --refine-bits 0 \
  --v2-cap 14 \
  --max-steps 1000 \
  --progress \
  --output-tag T14_j32_64_128_b0
```

Outputs:

```text
scripts/spectral_program/collatz_110_T14_j32_64_128_b0_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T14_j32_64_128_b0_refined_square_probe_by_pair.csv
```

The run traced `8,388,604` rows:

```text
terminal rows = 7,508,568
return rows   =   880,036
```

## Result

Phase-only weighted `L1` prefix drift:

```text
T=14, b=0:

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

The main weak averaged proxy decreases:

```text
0.000420440901 -> 0.000285774472
```

This is a relative decrease of about `32.03%`.

The p95 and p99 also decrease.  The max increases slightly, so the result is
supportive for a weak averaged norm but not for a uniform/sup norm.

## Interpretation

This is the cleanest current finite signal for the main Gate-10.B branch:

```text
A0 phase-only prefix drift continues downward at the next scale.
```

It does not prove a Cauchy theorem.  It does, however, strengthen the case
that the proof attempt should focus on:

```text
weak averaged row-TV / L1 control
not uniform row-TV
not A1 residue refinement as the main branch
```

The next mathematical obligation is therefore not another empirical feature,
but the finite-to-Banach bridge:

```text
show that the finite A0 prefix kernels approximate a declared operator
in a weak norm, with the observed D_N feeding the operator bound.
```

The remaining finite risk is the rare-row tail: the maximum row drift does
not currently decay monotonically, so any theorem must either avoid uniform
control or isolate the exceptional-source mass explicitly.

## Tail Inspection

The follow-up key-drift inspection:

```text
python scripts/spectral_program/111_refined_square_key_drift_inspector.py \
  --T 14 \
  --j-counts 64,128 \
  --bits 0 \
  --v2-cap 14 \
  --max-steps 1000 \
  --progress \
  --output-tag T14_j64_128_b0
```

confirms that the increased maximum is a rare-source phenomenon.

Global drift:

```text
weighted_l1_mean = 0.000285774472
top 10 contribution share  = 0.390638229
top 25 contribution share  = 0.712042880
```

The largest row `L1` value comes from the four phases `14|3|h`:

```text
source phase 14|3|h
row L1       = 0.0331541219
sample weight = 47
contribution per h ~= 0.000866 of total sample mass
```

So the max obstruction is not a high-mass obstruction.  It is a sparse
high-`v2` tail, exactly the kind of object that a weak averaged theorem can
discard or control by an exceptional-source estimate.

The main contribution to the average drift is instead carried by low
source phases:

```text
0|3|h contribution per h = 0.0451868833
1|3|h contribution per h = 0.0367792264
0|1|h contribution per h = 0.0313868952
```

This reinforces the split:

```text
mean drift: low-phase structural families
max drift: sparse high-v2 exceptional tail
```

That is favorable for a weak averaged A0 bridge and unfavorable for a
uniform row-TV/sup-norm bridge.
