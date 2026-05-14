# Source-Refinement Collapse Diagnostic

Status: finite source-quotient diagnostic, not an operator theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- delta cutoff: `5`
- max bits: `10`
- include boundary: `False`
- include mixed source cells: `False`

## Best Nontrivial Candidates By Prefix

Rows below exclude the overfit `source_cell` key and require at
least `16.0` mean source cells per key.

| j_count | candidate | collapse mean | p95 | p99 | max | keys | mean cells/key | singleton frac | worst key mean |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 64 | `phase+rlo10` | 0.021797427 | 0.06098938 | 0.38839722 | 1.3684082 | 4128 | 31.75 | 0.0019379845 | 1.00354 |
| 64 | `phase+rlo9` | 0.024838916 | 0.074707031 | 0.40075684 | 1.1614227 | 2088 | 62.770115 | 0.0038314176 | 1.00354 |
| 64 | `phase+rlo8` | 0.029473027 | 0.1270256 | 0.44380951 | 1.0922852 | 1072 | 122.26119 | 0.0074626866 | 1.00354 |
| 64 | `phase+rlo7` | 0.036983147 | 0.21842384 | 0.55542755 | 1.0922852 | 568 | 230.74648 | 0.014084507 | 1.00354 |
| 64 | `phase+rlo6` | 0.046583461 | 0.38115501 | 0.60773468 | 1.0922852 | 320 | 409.575 | 0.025 | 1.00354 |
| 64 | `phase+rlo5+rhi5` | 0.050514292 | 0.32626343 | 0.70889282 | 0.94371033 | 5368 | 24.415797 | 0.093889717 | 0.68252563 |
| 64 | `phase+rlo5+rhi4` | 0.050704827 | 0.32878876 | 0.70761108 | 0.95557404 | 2808 | 46.675214 | 0.088319088 | 0.68057442 |
| 64 | `phase+rlo5+rhi3` | 0.050781833 | 0.32923508 | 0.70890808 | 0.96018982 | 1464 | 89.52459 | 0.081967213 | 0.67774129 |
| 64 | `phase+rlo5+rhi2` | 0.050970309 | 0.33029938 | 0.70903397 | 0.96747017 | 760 | 172.45263 | 0.073684211 | 0.67524099 |
| 64 | `phase+rlo5+rhi1` | 0.051056808 | 0.33065605 | 0.7057972 | 0.96976566 | 392 | 334.34694 | 0.06122449 | 0.92578125 |
| 128 | `phase+rlo10` | 0.020415877 | 0.060073853 | 0.39105225 | 1.366539 | 4128 | 31.75 | 0.0019379845 | 1.0051575 |
| 128 | `phase+rlo9` | 0.023445317 | 0.070648193 | 0.39865112 | 1.1585159 | 2088 | 62.770115 | 0.0038314176 | 1.0051575 |
| 128 | `phase+rlo8` | 0.028068213 | 0.12545586 | 0.43983269 | 1.0905151 | 1072 | 122.26119 | 0.0074626866 | 1.0051575 |
| 128 | `phase+rlo7` | 0.03566564 | 0.21943092 | 0.54864311 | 1.0905151 | 568 | 230.74648 | 0.014084507 | 1.0051575 |
| 128 | `phase+rlo6` | 0.045285375 | 0.38502312 | 0.60185242 | 1.0905151 | 320 | 409.575 | 0.025 | 1.0051575 |
| 128 | `phase+rlo5+rhi5` | 0.049528506 | 0.32867432 | 0.70068359 | 0.9394455 | 5368 | 24.415797 | 0.093889717 | 0.67277527 |
| 128 | `phase+rlo5+rhi3` | 0.049588853 | 0.33095741 | 0.69997025 | 0.95623398 | 1464 | 89.52459 | 0.081967213 | 0.6693694 |
| 128 | `phase+rlo5+rhi4` | 0.049594387 | 0.33026886 | 0.69846344 | 0.95127487 | 2808 | 46.675214 | 0.088319088 | 0.67218876 |
| 128 | `phase+rlo5+rhi2` | 0.049719814 | 0.33160782 | 0.70059967 | 0.96334648 | 760 | 172.45263 | 0.073684211 | 0.66656424 |
| 128 | `phase+rlo5+rhi1` | 0.049784413 | 0.33151054 | 0.69918823 | 0.9656291 | 392 | 334.34694 | 0.06122449 | 0.93017578 |

## Baselines

| j_count | phase collapse mean | source-cell collapse mean | source-cell keys |
|---:|---:|---:|---:|
| 64 | 0.052910359 | 0 | 131064 |
| 128 | 0.051512269 | 0 | 131064 |

## Interpretation

A good source refinement should lower collapse error without making
almost every source cell its own key.  A near-zero value for
`source_cell` is only the trivial identity refinement.

This diagnostic does not prove convergence.  It only identifies
finite alphabets worth testing before a Lean import or Banach-space
bridge is attempted.
