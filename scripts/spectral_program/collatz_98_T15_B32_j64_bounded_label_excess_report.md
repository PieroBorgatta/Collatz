# Bounded Label Excess

Status: diagnostic output, not a theorem.

## Inputs

- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T: `15`
- block size: `32`
- block starts: `0, 32`
- cutoffs: `2,3,4,5,8`
- skipped incomplete groups: `4`

## Summary

| transform | phase mean TV | label mean TV | excess mean | excess p95 | excess p99 | excess max | excess positive frac |
|---|---:|---:|---:|---:|---:|---:|---:|
| `clip_2` | 0.0230853 | 0.0289039 | 0.00581854 | 0.03125 | 0.09375 | 0.25 | 0.127384 |
| `clip_3` | 0.0230853 | 0.0299863 | 0.006901 | 0.03125 | 0.09375 | 0.25 | 0.149693 |
| `clip_4` | 0.0230853 | 0.0305662 | 0.00748085 | 0.0625 | 0.09375 | 0.25 | 0.159215 |
| `clip_5` | 0.0230853 | 0.0308437 | 0.00775838 | 0.0625 | 0.09375 | 0.25 | 0.162603 |
| `clip_8` | 0.0230853 | 0.031002 | 0.00791669 | 0.0625 | 0.09375 | 0.25 | 0.163945 |
| `full` | 0.0230853 | 0.0310049 | 0.00791955 | 0.0625 | 0.09375 | 0.25 | 0.163945 |

## Interpretation

This measures the bounded-label penalty left after destination-phase
movement is already accounted for.  A small excess would support a
weak norm that treats bounded delta variation as a lower-order
term.  A persistent excess means the label process itself needs
regularity, not only tail control.
