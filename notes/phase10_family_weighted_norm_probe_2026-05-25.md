# Phase 10 Family Weighted Norm Probe

Date: 2026-05-25

Status: finite diagnostic update for script
`112_family_weighted_norm_probe.py`.

## Question

Script `111_refined_square_key_drift_inspector.py` showed that the A1
refined-square `b=10` drift is broad but structured by source family.  The
main contributing families were:

```text
(v2, odd mod 4) = 0|3, 0|1, 1|3, 1|1.
```

The next test was whether a source-family weighted weak norm could reduce the
effective drift without simply hiding mass.

## Run

```text
python scripts/spectral_program/112_family_weighted_norm_probe.py \
  --T 14 \
  --j-counts 32,64 \
  --bits 10 \
  --v2-cap 14 \
  --max-steps 1000 \
  --progress \
  --output-tag T14_j32_64_b10
```

Outputs:

```text
scripts/spectral_program/collatz_112_T14_j32_64_b10_family_weighted_norm_probe_report.md
scripts/spectral_program/collatz_112_T14_j32_64_b10_family_weighted_norm_probe_grid.csv
scripts/spectral_program/collatz_112_T14_j32_64_b10_family_weighted_norm_probe_worst_rows.csv
```

## Metrics

The script separates two finite quantities:

```text
source_weighted_l1:
  row L1 averaged after reweighting the source measure by V(src).
  This can hide bad source mass.

operator_weighted_l1:
  average of sum_dst |Delta K(src,dst)| V(dst)/V(src).
  This is the more relevant proxy for a weighted strong norm.
```

Identity baseline:

```text
identity_l1_mean = 0.0121733793
identity_p95     = 0.0367279053
identity_max     = 0.618164062
```

## Result

The source-family idea is not supported by this finite test.

Weighting the dominant source families or all `v2 <= 1` families does not
improve the operator-weighted proxy.  It makes it slightly or substantially
worse, depending on the factor:

```text
dominant4_x1.25 operator mean = 0.0122560449
dominant4_x1.50 operator mean = 0.0124930228
dominant4_x2.00 operator mean = 0.0131984470

low_v2_le1 gives the same values on this window.
```

Downweighting the same families can lower the source-measure average, but
this is the wrong success criterion: it hides part of the difficult source
mass and worsens the operator proxy for stronger downweights.

The best operator-weighted candidate is not a source family at all.  It is a
low-residue band:

```text
rlo_mod32_6_26_x1.5:
  operator mean       = 0.0118894199
  relative improvement = 0.0233262632
  operator p95        = 0.0373992920
  operator max        = 0.638671875
  rows worse          = 0.441005803
```

This is only a `2.3%` mean improvement, with a slightly worse p95/max and
about `44%` of source rows made worse.

## Interpretation

This is a useful negative result.

The broad A1 drift is structured by source family, but simple
source-family weights do not produce a convincing weighted-norm contraction
proxy.  The only small operator improvement found here comes from a
data-visible residue band (`rlo mod 32 in {6,26}`), which is too narrow and
too fitted to serve as the main theorem path.

Therefore:

```text
A1 remains useful as diagnostic evidence,
but it should not replace A0 as the main Gate-10.B route.
```

The main branch should return to the phase-only A0 bridge:

```text
prove/measure phase-prefix Cauchy in a weak averaged norm,
then connect the finite CSV kernels to an explicit finite-to-Banach theorem.
```

The A1 branch can remain as a side appendix explaining why low-residue
refinement improves source collapse but does not yet yield a cleaner
operator limit.
