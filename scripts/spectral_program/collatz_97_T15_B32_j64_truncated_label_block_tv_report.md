# Truncated Label Block TV

Status: diagnostic output, not a theorem.

## Inputs

- distributions file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_signature_distribution.csv`
- T: `15`
- block size: `32`
- block starts: `0, 32`
- adjacent pairs: `0->32`
- cutoffs: `2,3,4,5,8`
- complete groups compared: `131068`
- groups skipped for incomplete blocks: `4`

## Summary

| transform | count mean TV | count p95 | count p99 | count max | weight mean TV | weight p95 | weight p99 | weight max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `status` | 0.0128616 | 0.0625 | 0.125 | 0.25 | 0.0780969 | 1 | 1 | 1 |
| `phase` | 0.0230853 | 0.125 | 0.15625 | 0.28125 | 0.246644 | 1 | 1 | 1 |
| `clip_2` | 0.0289039 | 0.125 | 0.1875 | 0.375 | 0.276272 | 1 | 1 | 1 |
| `clip_3` | 0.0299863 | 0.125 | 0.1875 | 0.375 | 0.28009 | 1 | 1 | 1 |
| `clip_4` | 0.0305662 | 0.15625 | 0.1875 | 0.375 | 0.281403 | 1 | 1 | 1 |
| `clip_5` | 0.0308437 | 0.15625 | 0.21875 | 0.375 | 0.281778 | 1 | 1 | 1 |
| `clip_8` | 0.031002 | 0.15625 | 0.21875 | 0.375 | 0.281873 | 1 | 1 | 1 |
| `full` | 0.0310049 | 0.15625 | 0.21875 | 0.375 | 0.281873 | 1 | 1 | 1 |

## Interpretation

If clipped labels have much lower TV than full labels, then the
mixed norm can plausibly retain bounded delta labels and charge the
rest to a tail term.  If clipping barely changes TV, then phase
movement rather than delta tails is the dominant block-Cauchy
obstruction.

Weighted TV ignores terminal mass because terminal rows have zero
return weight in the source diagnostic.  It should be interpreted
only as a return-weight diagnostic, not as a complete weak norm.
