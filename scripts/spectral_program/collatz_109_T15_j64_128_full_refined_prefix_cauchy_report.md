# Refined Prefix-Cauchy Diagnostic

Status: finite diagnostic only.  This report does not prove
existence or convergence of an infinite operator.

## Scope

- groups CSV: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions CSV: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- prefix counts: `64, 128`
- delta cutoff: `None`
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
| `phase` | 64 | 128 | 112 | 1170.21429 | 0.000200334358 | 0.000376969576 | 0.0129394531 |
| `phase+rlo1` | 64 | 128 | 112 | 1170.21429 | 0.000200334358 | 0.000376969576 | 0.0129394531 |
| `phase+rlo2` | 64 | 128 | 112 | 1170.21429 | 0.000200334358 | 0.000376969576 | 0.0129394531 |
| `phase+rlo3` | 64 | 128 | 120 | 1092.2 | 0.000251009505 | 0.000376969576 | 0.0129394531 |
| `phase+rlo4` | 64 | 128 | 144 | 910.166667 | 0.000288804168 | 0.000422452576 | 0.0122436523 |
| `phase+rlo5` | 64 | 128 | 200 | 655.32 | 0.000366423408 | 0.000675026793 | 0.00830078125 |
| `phase+rhi1` | 64 | 128 | 216 | 606.777778 | 0.000389921747 | 0.00183587521 | 0.01171875 |
| `phase+rhi2` | 64 | 128 | 408 | 321.235294 | 0.00049733372 | 0.00141793489 | 0.0123291016 |
| `phase+rlo6` | 64 | 128 | 320 | 409.575 | 0.000512183415 | 0.000996053219 | 0.00653762817 |
| `phase+rlo5+rhi1` | 64 | 128 | 392 | 334.346939 | 0.000671948442 | 0.00114448369 | 0.0108795166 |
| `phase+rhi3` | 64 | 128 | 760 | 172.452632 | 0.000692089581 | 0.00208091736 | 0.0123291016 |
| `phase+rlo7` | 64 | 128 | 568 | 230.746479 | 0.000694560254 | 0.00149231404 | 0.00402832031 |
| `phase+rlo5+rhi2` | 64 | 128 | 760 | 172.452632 | 0.000885093415 | 0.00179290771 | 0.0113525391 |
| `phase+rlo8` | 64 | 128 | 1072 | 122.261194 | 0.000901214662 | 0.00209651887 | 0.00254106522 |
| `phase+rhi4` | 64 | 128 | 1400 | 93.6171429 | 0.000913095803 | 0.00244736671 | 0.0130615234 |

## Selected Candidate Rows

| candidate | j_left | j_right | keys | mean cells/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `phase` | 64 | 128 | 112 | 1170.21429 | 0.000200334358 | 0.000376969576 | 0.0129394531 | 0.0162353516 |
| `phase+rlo10` | 64 | 128 | 4128 | 31.75 | 0.00158517189 | 0.00430297852 | 0.00436067581 | 0.0162353516 |
| `phase+rlo11` | 64 | 128 | 8216 | 15.9522882 | 0.00210545906 | 0.00585854053 | 0.00587081909 | 0.0162353516 |
| `phase+rlo12` | 64 | 128 | 16400 | 7.99170732 | 0.00260885356 | 0.00811767578 | 0.00814819336 | 0.0162353516 |
| `phase+rlo5` | 64 | 128 | 200 | 655.32 | 0.000366423408 | 0.000675026793 | 0.00830078125 | 0.0162353516 |
| `source_cell` | 64 | 128 | 131064 | 1 | 0.00450725254 | 0.0205078125 | 0.0205078125 | 0.0668945312 |

## Interpretation Guardrails

- Smaller drift is evidence for a finite averaged-kernel story, not a theorem.
- The `source_cell` row is an overfit baseline, not a usable finite quotient.
- A useful analytic alphabet must balance drift against state explosion.
- These rows compare destination `PhaseState` distributions only.
- Any infinite-operator claim still requires a topology, norm, and convergence proof.
