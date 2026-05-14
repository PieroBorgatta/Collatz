# Refined State Stability Probe

Status: diagnostic output, not a theorem.

## Inputs

- details file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_90_refinement_coordinate_details.csv`
- coordinates: `j_mod_32,j_mod_32+delta,j_mod_32+next_t_mod_32`
- minimum cell size: `2`
- strong threshold: `0.9`

## Destination Phase

| coordinate | source groups | cells | source mean | cell mean | p10 cell | min cell | exact cells | strong cells | cell size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `j_mod_32+delta` | 84 | 3224 | 0.321429 | 0.97653 | 1 | 0.25 | 0.955335 | 0.955335 | 3.05459 |
| `j_mod_32+next_t_mod_32` | 84 | 2688 | 0.321429 | 0.972098 | 1 | 0.25 | 0.955357 | 0.955357 | 3.99107 |
| `j_mod_32` | 84 | 2688 | 0.321429 | 0.97061 | 1 | 0.25 | 0.949405 | 0.949405 | 4 |

## Full Weighted Signature

| coordinate | source groups | cells | source mean | cell mean | p10 cell | min cell | exact cells | strong cells | cell size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `j_mod_32+delta` | 84 | 3224 | 0.256324 | 0.97653 | 1 | 0.25 | 0.955335 | 0.955335 | 3.05459 |
| `j_mod_32+next_t_mod_32` | 84 | 2688 | 0.256324 | 0.799231 | 0.5 | 0.25 | 0.459821 | 0.459821 | 3.99107 |
| `j_mod_32` | 84 | 2688 | 0.256324 | 0.797619 | 0.5 | 0.25 | 0.458333 | 0.458333 | 4 |

## Interpretation

A good phase-refinement coordinate should raise the cell-majority
statistics for `phase_signature`.  It is not enough for defining a
weighted transfer operator unless the same or an augmented coordinate
also controls `full_signature`.

These diagnostics do not imply Conjecture 6, an infinite operator, a
Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral
gap.
