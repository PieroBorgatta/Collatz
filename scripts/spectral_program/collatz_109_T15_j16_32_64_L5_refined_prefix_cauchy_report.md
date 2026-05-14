# Refined Prefix-Cauchy Diagnostic

Status: finite diagnostic only.  This report does not prove
existence or convergence of an infinite operator.

## Scope

- groups CSV: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv`
- distributions CSV: `../scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv`
- T filter: `15`
- prefix counts: `16, 32, 64`
- delta cutoff: `5`
- max low/high bits: `12`
- include boundary cells: `False`
- include mixed source cells: `False`

## Retained Source Cells

| j_count | retained cells |
|---:|---:|
| 16 | 131064 |
| 32 | 131064 |
| 64 | 131064 |

## Best Candidate Rows

Candidates are ranked by source-cell-weighted L1 drift among common candidate keys.  The minimum mean-cell filter prevents the table from being dominated by the overfit `source_cell` baseline.

| candidate | j_left | j_right | keys | mean cells/key | weighted L1 mean | weighted L1 p95 | key L1 p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `phase` | 32 | 64 | 112 | 1170.21429 | 0.000283809937 | 0.000562667847 | 0.01171875 |
| `phase+rlo1` | 32 | 64 | 112 | 1170.21429 | 0.000283809937 | 0.000562667847 | 0.01171875 |
| `phase+rlo2` | 32 | 64 | 112 | 1170.21429 | 0.000283809937 | 0.000562667847 | 0.01171875 |
| `phase+rlo3` | 32 | 64 | 120 | 1092.2 | 0.000336861309 | 0.000562667847 | 0.01171875 |
| `phase+rlo4` | 32 | 64 | 144 | 910.166667 | 0.000406334763 | 0.000629663467 | 0.01171875 |
| `phase` | 16 | 32 | 112 | 1170.21429 | 0.000418271322 | 0.000632286072 | 0.015625 |
| `phase+rlo1` | 16 | 32 | 112 | 1170.21429 | 0.000418271322 | 0.000632286072 | 0.015625 |
| `phase+rlo2` | 16 | 32 | 112 | 1170.21429 | 0.000418271322 | 0.000632286072 | 0.015625 |
| `phase+rlo3` | 16 | 32 | 120 | 1092.2 | 0.000477581563 | 0.000632286072 | 0.015625 |
| `phase+rlo5` | 32 | 64 | 200 | 655.32 | 0.000518755985 | 0.000915050507 | 0.01171875 |
| `phase+rhi1` | 32 | 64 | 216 | 606.777778 | 0.000603161313 | 0.00215053558 | 0.0234375 |
| `phase+rlo4` | 16 | 32 | 144 | 910.166667 | 0.000609077435 | 0.000789642334 | 0.015625 |
| `phase+rlo6` | 32 | 64 | 320 | 409.575 | 0.000729352048 | 0.00141239166 | 0.00795898438 |
| `phase+rhi2` | 32 | 64 | 408 | 321.235294 | 0.000752509866 | 0.00196838379 | 0.0222167969 |
| `phase+rlo5` | 16 | 32 | 200 | 655.32 | 0.000778901434 | 0.00118160248 | 0.015625 |

## Selected Candidate Rows

| candidate | j_left | j_right | keys | mean cells/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `phase` | 16 | 32 | 112 | 1170.21429 | 0.000418271322 | 0.000632286072 | 0.015625 | 0.0283203125 |
| `phase+rlo10` | 16 | 32 | 4128 | 31.75 | 0.00302166308 | 0.00839233398 | 0.00860595703 | 0.0283203125 |
| `phase+rlo11` | 16 | 32 | 8216 | 15.9522882 | 0.00386905443 | 0.0114746094 | 0.0115356445 | 0.0283203125 |
| `phase+rlo12` | 16 | 32 | 16400 | 7.99170732 | 0.0047000535 | 0.0166015625 | 0.0164855957 | 0.0367431641 |
| `phase+rlo5` | 16 | 32 | 200 | 655.32 | 0.000778901434 | 0.00118160248 | 0.015625 | 0.0283203125 |
| `source_cell` | 16 | 32 | 131064 | 1 | 0.00663106383 | 0.03515625 | 0.03515625 | 0.1875 |
| `phase` | 32 | 64 | 112 | 1170.21429 | 0.000283809937 | 0.000562667847 | 0.01171875 | 0.021484375 |
| `phase+rlo10` | 32 | 64 | 4128 | 31.75 | 0.00215625513 | 0.00592041016 | 0.00598144531 | 0.021484375 |
| `phase+rlo11` | 32 | 64 | 8216 | 15.9522882 | 0.00285879835 | 0.00817871094 | 0.00827026367 | 0.021484375 |
| `phase+rlo12` | 32 | 64 | 16400 | 7.99170732 | 0.00354465125 | 0.01171875 | 0.01171875 | 0.021484375 |
| `phase+rlo5` | 32 | 64 | 200 | 655.32 | 0.000518755985 | 0.000915050507 | 0.01171875 | 0.021484375 |
| `source_cell` | 32 | 64 | 131064 | 1 | 0.00554659544 | 0.02734375 | 0.02734375 | 0.1015625 |

## Interpretation Guardrails

- Smaller drift is evidence for a finite averaged-kernel story, not a theorem.
- The `source_cell` row is an overfit baseline, not a usable finite quotient.
- A useful analytic alphabet must balance drift against state explosion.
- These rows compare destination `PhaseState` distributions only.
- Any infinite-operator claim still requires a topology, norm, and convergence proof.
