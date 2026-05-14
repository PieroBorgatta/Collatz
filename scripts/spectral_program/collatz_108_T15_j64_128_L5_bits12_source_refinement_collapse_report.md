# Source-Refinement Collapse Diagnostic

Status: finite source-quotient diagnostic, not an operator theorem.

## Inputs

- groups file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv`
- distributions file: `../scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv`
- T filter: `15`
- delta cutoff: `5`
- max bits: `12`
- include boundary: `False`
- include mixed source cells: `False`

## Best Nontrivial Candidates By Prefix

Rows below exclude the overfit `source_cell` key and require at
least `4.0` mean source cells per key.

| j_count | candidate | collapse mean | p95 | p99 | max | keys | mean cells/key | singleton frac | worst key mean |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 64 | `phase+rlo12` | 0.016936304 | 0.047729492 | 0.26745605 | 1.6455078 | 16400 | 7.9917073 | 0.00048780488 | 1.5214844 |
| 64 | `phase+rlo11` | 0.019511369 | 0.051330566 | 0.29309082 | 1.7584229 | 8216 | 15.952288 | 0.00097370983 | 1.5417328 |
| 64 | `phase+rlo10` | 0.021797427 | 0.06098938 | 0.38839722 | 1.3684082 | 4128 | 31.75 | 0.0019379845 | 1.00354 |
| 64 | `phase+rlo9` | 0.024838916 | 0.074707031 | 0.40075684 | 1.1614227 | 2088 | 62.770115 | 0.0038314176 | 1.00354 |
| 64 | `phase+rlo8` | 0.029473027 | 0.1270256 | 0.44380951 | 1.0922852 | 1072 | 122.26119 | 0.0074626866 | 1.00354 |
| 64 | `phase+rlo7` | 0.036983147 | 0.21842384 | 0.55542755 | 1.0922852 | 568 | 230.74648 | 0.014084507 | 1.00354 |
| 64 | `phase+rhi9` | 0.046125038 | 0.25033569 | 0.41137695 | 0.82714844 | 24568 | 5.3347444 | 0.33311625 | 0.44567871 |
| 64 | `phase+rlo6` | 0.046583461 | 0.38115501 | 0.60773468 | 1.0922852 | 320 | 409.575 | 0.025 | 1.00354 |
| 64 | `phase+rlo5+rhi6` | 0.049867427 | 0.32455444 | 0.70996094 | 0.89746094 | 10232 | 12.809226 | 0.099296325 | 0.67932129 |
| 64 | `phase+rhi8` | 0.050364539 | 0.265625 | 0.51367188 | 0.88623047 | 14328 | 9.1474037 | 0.28531547 | 0.42379761 |
| 128 | `phase+rlo12` | 0.015742233 | 0.045013428 | 0.26739502 | 1.6425781 | 16400 | 7.9917073 | 0.00048780488 | 1.5216064 |
| 128 | `phase+rlo11` | 0.018202554 | 0.048156738 | 0.29260254 | 1.7544556 | 8216 | 15.952288 | 0.00097370983 | 1.5408936 |
| 128 | `phase+rlo10` | 0.020415877 | 0.060073853 | 0.39105225 | 1.366539 | 4128 | 31.75 | 0.0019379845 | 1.0051575 |
| 128 | `phase+rlo9` | 0.023445317 | 0.070648193 | 0.39865112 | 1.1585159 | 2088 | 62.770115 | 0.0038314176 | 1.0051575 |
| 128 | `phase+rlo8` | 0.028068213 | 0.12545586 | 0.43983269 | 1.0905151 | 1072 | 122.26119 | 0.0074626866 | 1.0051575 |
| 128 | `phase+rlo7` | 0.03566564 | 0.21943092 | 0.54864311 | 1.0905151 | 568 | 230.74648 | 0.014084507 | 1.0051575 |
| 128 | `phase+rlo6` | 0.045285375 | 0.38502312 | 0.60185242 | 1.0905151 | 320 | 409.575 | 0.025 | 1.0051575 |
| 128 | `phase+rhi9` | 0.045464197 | 0.25061035 | 0.40716553 | 0.82373047 | 24568 | 5.3347444 | 0.33311625 | 0.43572998 |
| 128 | `phase+rlo5+rhi6` | 0.04904184 | 0.32678223 | 0.70068359 | 0.89868164 | 10232 | 12.809226 | 0.099296325 | 0.6696167 |
| 128 | `phase+rlo5+rhi5` | 0.049528506 | 0.32867432 | 0.70068359 | 0.9394455 | 5368 | 24.415797 | 0.093889717 | 0.67277527 |

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
