# Phase 10 Refined Square Extension

Date: 2026-05-22

Status: finite diagnostic update for script `110_refined_square_probe.py`.

## Question

The A1 branch refines the source alphabet by adding low residue bits:

```text
(PhaseState, t mod 2^b) -> (PhaseState, next_t mod 2^b).
```

Earlier smoke runs showed that this refined square kernel is stable in the
prefix direction, but noisier than the phase-only branch.  The next check was
whether the downward trend persists when the true prefix size is doubled.

## New Runs

New run:

```text
python scripts/spectral_program/110_refined_square_probe.py \
  --T 13 \
  --j-counts 32,64 \
  --refine-bits 0,5,8,10 \
  --v2-cap 13 \
  --max-steps 1000 \
  --output-tag T13_j32_64_b0_5_8_10
```

This exactly reproduces the previous `T=12, j=64->128` values.  This is
expected: for `b <= 10`, the refined square probe depends primarily on the
prefix size

```text
N = j_count * 2^T
```

rather than on `T` and `j_count` separately.

New larger-prefix run:

```text
python scripts/spectral_program/110_refined_square_probe.py \
  --T 14 \
  --j-counts 32,64 \
  --refine-bits 0,5,8,10 \
  --v2-cap 14 \
  --max-steps 1000 \
  --output-tag T14_j32_64_b0_5_8_10
```

This traces `4,194,300` rows.

## Results

Weighted `L1` prefix drift:

```text
T=12, j=64->128:
  b=0:  0.000647069352
  b=5:  0.00232221302
  b=8:  0.0101905453
  b=10: 0.0129098735

T=14, j=32->64:
  b=0:  0.000420440901
  b=5:  0.00160995368
  b=8:  0.00848590605
  b=10: 0.0121733793
```

So the drift decreases at the larger prefix scale for all tested `b`.

## Interpretation

The A1 refined-square branch remains alive:

```text
prefix drift decreases when N doubles.
```

But it is still much noisier than the phase-only branch:

```text
b=10 drift / b=0 drift ~= 29
```

at the latest tested scale.

Conclusion:

```text
A1 is useful finite evidence for a refined-source theory,
but it is not yet competitive with the phase-only bridge as the main
Gate-10.B route.
```

The next useful A1 test would be either:

```text
T=14, j=64->128
```

which is roughly twice the new run, or a cheaper diagnostic that isolates
which refined residue classes contribute most to the remaining `b=10`
drift.
