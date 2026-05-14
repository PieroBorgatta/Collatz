# Refined Prefix-Cauchy Diagnostic

Status: finite diagnostic only.  This report does not prove
existence or convergence of an infinite operator.

## Scope

- groups CSV: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions CSV: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- prefix counts: `64, 128`
- delta cutoff: `5`
- max low/high bits: `12`
- include boundary cells: `False`
- include mixed source cells: `False`

## Retained Source Cells

| j_count | retained cells |
|---:|---:|
| 64 | 131064 |
| 128 | 131064 |

## Best Candidate Rows

Candidates are ranked by source-cell-weighted L1 drift among common candidate keys.  The minimum mean-cell filter prevents the table from being dominated by the overfit `source_cell` baseline.

| candidate | j_left | j_right | keys | mean cells/key | weighted L1 mean | weighted L1 p95 | key L1 p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `phase` | 64 | 128 | 112 | 1170.21429 | 0.000200738344 | 0.000377416611 | 0.0129394531 |
| `phase+rlo1` | 64 | 128 | 112 | 1170.21429 | 0.000200738344 | 0.000377416611 | 0.0129394531 |
| `phase+rlo2` | 64 | 128 | 112 | 1170.21429 | 0.000200738344 | 0.000377416611 | 0.0129394531 |
| `phase+rlo3` | 64 | 128 | 120 | 1092.2 | 0.000250913616 | 0.000377416611 | 0.0129394531 |
| `phase+rlo4` | 64 | 128 | 144 | 910.166667 | 0.000288779778 | 0.000422477722 | 0.0122436523 |
| `phase+rlo5` | 64 | 128 | 200 | 655.32 | 0.000366538783 | 0.000681638718 | 0.00830078125 |
| `phase+rhi1` | 64 | 128 | 216 | 606.777778 | 0.000390158565 | 0.00183653831 | 0.01171875 |
| `phase+rhi2` | 64 | 128 | 408 | 321.235294 | 0.000497885635 | 0.00142002106 | 0.0122070312 |
| `phase+rlo6` | 64 | 128 | 320 | 409.575 | 0.000512370447 | 0.000995159149 | 0.00652313232 |
| `phase+rlo5+rhi1` | 64 | 128 | 392 | 334.346939 | 0.000671748094 | 0.00114297867 | 0.0108520508 |
| `phase+rhi3` | 64 | 128 | 760 | 172.452632 | 0.000692283147 | 0.00208282471 | 0.0122070312 |
| `phase+rlo7` | 64 | 128 | 568 | 230.746479 | 0.000694473752 | 0.00149250031 | 0.00402832031 |
| `phase+rlo5+rhi2` | 64 | 128 | 760 | 172.452632 | 0.000885101041 | 0.00179290771 | 0.0113525391 |
| `phase+rlo8` | 64 | 128 | 1072 | 122.261194 | 0.000901180375 | 0.00209617615 | 0.00254058838 |
| `phase+rhi4` | 64 | 128 | 1400 | 93.6171429 | 0.000913385171 | 0.00245094299 | 0.0130615234 |

## Selected Candidate Rows

| candidate | j_left | j_right | keys | mean cells/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `phase` | 64 | 128 | 112 | 1170.21429 | 0.000200738344 | 0.000377416611 | 0.0129394531 | 0.0162353516 |
| `phase+rlo10` | 64 | 128 | 4128 | 31.75 | 0.00158494699 | 0.00431060791 | 0.00435638428 | 0.0162353516 |
| `phase+rlo11` | 64 | 128 | 8216 | 15.9522882 | 0.00210468651 | 0.005859375 | 0.00587463379 | 0.0162353516 |
| `phase+rlo12` | 64 | 128 | 16400 | 7.99170732 | 0.00260800395 | 0.00811767578 | 0.00814819336 | 0.0162353516 |
| `phase+rlo5` | 64 | 128 | 200 | 655.32 | 0.000366538783 | 0.000681638718 | 0.00830078125 | 0.0162353516 |
| `source_cell` | 64 | 128 | 131064 | 1 | 0.00450242969 | 0.0205078125 | 0.0205078125 | 0.0668945312 |

## Interpretation Guardrails

- Smaller drift is evidence for a finite averaged-kernel story, not a theorem.
- The `source_cell` row is an overfit baseline, not a usable finite quotient.
- A useful analytic alphabet must balance drift against state explosion.
- These rows compare destination `PhaseState` distributions only.
- Any infinite-operator claim still requires a topology, norm, and convergence proof.
