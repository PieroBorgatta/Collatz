# Refinement Coordinate Score Report

Status: diagnostic output, not a theorem.

## Inputs

- groups file: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/scripts/spectral_program/collatz_88_cylinder_group_summary.csv`
- selected groups: `84`
- j_count: `128`
- max phase majority: `0.5`
- min status majority: `1.0`
- h filter: `all`
- include boundary groups: `False`
- include t=0: `False`
- minimum average bucket size: `4.0`
- strong purity threshold: `0.9`
- minimum bucket purity threshold: `0.5`

## Best Global Coordinates for Destination Phase

| coordinate | groups | mean purity | p10 purity | min purity | mean min-bucket | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 84 | 0.97061 | 0.953125 | 0.953125 | 0.464286 | 0.285714 | 0.285714 |
| `j_mod_16` | 84 | 0.942708 | 0.914062 | 0.914062 | 0.464286 | 0.285714 | 0.285714 |
| `j_mod_8` | 84 | 0.886905 | 0.835938 | 0.835938 | 0.464286 | 0.285714 | 0.285714 |
| `next_t_mod_64` | 60 | 0.825521 | 0.375 | 0.25 | 0.516667 | 0.333333 | 0.333333 |
| `next_t_mod_32` | 84 | 0.799107 | 0.375 | 0.25 | 0.416667 | 0.190476 | 0.190476 |
| `j_mod_4` | 84 | 0.775298 | 0.679688 | 0.679688 | 0.464286 | 0.285714 | 0.285714 |
| `next_t_mod_16` | 84 | 0.717262 | 0.25 | 0.25 | 0.392857 | 0.142857 | 0.142857 |
| `next_t_mod_8` | 84 | 0.613095 | 0.25 | 0.25 | 0.369048 | 0.0952381 | 0.0952381 |
| `j_mod_2` | 84 | 0.553571 | 0.375 | 0.375 | 0.464286 | 0.285714 | 0.285714 |
| `j_shift_1_mod_2` | 84 | 0.498512 | 0.492188 | 0.492188 | 0.497024 | 0 | 0 |
| `next_t_mod_4` | 84 | 0.464286 | 0.25 | 0.25 | 0.322511 | 0 | 0 |
| `next_t_mod_2` | 84 | 0.358259 | 0.25 | 0.25 | 0.322894 | 0 | 0 |

## Best Global Coordinates for Full Signature

| coordinate | groups | mean purity | p10 purity | min purity | mean min-bucket | strong groups | perfect groups |
|---|---:|---:|---:|---:|---:|---:|---:|
| `j_mod_32` | 84 | 0.797619 | 0.679688 | 0.671875 | 0.321429 | 0.142857 | 0 |
| `j_mod_16` | 84 | 0.75 | 0.625 | 0.609375 | 0.321429 | 0.047619 | 0 |
| `j_mod_8` | 84 | 0.699777 | 0.585938 | 0.523438 | 0.366071 | 0.047619 | 0 |
| `next_t_mod_64` | 60 | 0.6625 | 0.296875 | 0.15625 | 0.383333 | 0.0666667 | 0 |
| `next_t_mod_32` | 84 | 0.639137 | 0.25 | 0.15625 | 0.337426 | 0 | 0 |
| `j_mod_4` | 84 | 0.609747 | 0.476562 | 0.40625 | 0.363095 | 0.047619 | 0 |
| `next_t_mod_16` | 84 | 0.574777 | 0.25 | 0.148438 | 0.335193 | 0 | 0 |
| `next_t_mod_8` | 84 | 0.487723 | 0.21875 | 0.148438 | 0.310268 | 0 | 0 |
| `j_mod_2` | 84 | 0.438616 | 0.265625 | 0.226562 | 0.364583 | 0.047619 | 0 |
| `j_shift_1_mod_2` | 84 | 0.388021 | 0.296875 | 0.273438 | 0.372024 | 0 | 0 |
| `next_t_mod_4` | 84 | 0.369048 | 0.195312 | 0.148438 | 0.261589 | 0 | 0 |
| `delta` | 84 | 0.339286 | 0.257812 | 0.257812 | 0.32717 | 0 | 0 |

## Interpretation

The ranking aggregates coordinate quality group-by-group.  It does
not use a coordinate that has one bucket per lift as evidence, because
coordinates with average bucket size below the configured threshold
are excluded.

A high destination-phase score supports trying a finite symbolic
refinement of the phase quotient.  A weaker full-signature score
means the weight exponent or return signature still carries
unmodeled information.

These diagnostics do not imply Conjecture 6, an infinite operator, a
Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral
gap.
