# Enriched State Test

Status: finite diagnostic output, not a theorem.

## Inputs

- T values: `15`
- max depth: `2`
- tail bits: `3`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`

The selected component is the part that an enriched state would
isolate.  The complement columns measure the remaining obstruction
outside that component.

## Trace Meta

| T | max j | source groups | parent-child pairs |
|---:|---:|---:|---:|
| 15 | 64 | 131072 | 917504 |

## Depth 0: Full-Over-Phase Excess

| candidate | selected mass | selected mean | selected contribution | complement mean | complement p95 | complement contribution | global mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `source_odd_3_or_v2_2` | 0.562469 | 0.0136099 | 0.764112 | 0.00540123 | 0.03125 | 0.235888 | 0.0100183 |
| `source_odd_3` | 0.499969 | 0.0146722 | 0.732223 | 0.00536504 | 0.03125 | 0.267777 | 0.0100183 |
| `source_v2_0_or_2_odd_3` | 0.3125 | 0.0217712 | 0.679105 | 0.00467613 | 0.03125 | 0.320895 | 0.0100183 |
| `source_v2_2` | 0.125 | 0.0288696 | 0.360209 | 0.00732531 | 0.0625 | 0.639791 | 0.0100183 |
| `source_v2_0_odd_3` | 0.25 | 0.0140572 | 0.350785 | 0.00867208 | 0.0625 | 0.649215 | 0.0100183 |
| `source_v2_2_odd_3` | 0.0625 | 0.0526276 | 0.32832 | 0.00717773 | 0.0625 | 0.67168 | 0.0100183 |

## Depth 1: Full-Over-Phase Excess

| candidate | selected mass | selected mean | selected contribution | complement mean | complement p95 | complement contribution | global mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `source_odd_3_or_v2_2` | 0.562469 | 0.0172518 | 0.768911 | 0.00666545 | 0.0625 | 0.231089 | 0.01262 |
| `source_odd_3` | 0.499969 | 0.0189221 | 0.749641 | 0.00631866 | 0.0625 | 0.250359 | 0.01262 |
| `source_v2_0_or_2_odd_3` | 0.3125 | 0.0284912 | 0.705509 | 0.00540577 | 0.0625 | 0.294491 | 0.01262 |
| `source_v2_2` | 0.125 | 0.0439606 | 0.435427 | 0.00814274 | 0.0625 | 0.564573 | 0.01262 |
| `source_v2_2_odd_3` | 0.0625 | 0.0840302 | 0.416157 | 0.00785929 | 0.0625 | 0.583843 | 0.01262 |
| `source_v2_0_odd_3` | 0.25 | 0.0146065 | 0.289352 | 0.0119578 | 0.125 | 0.710648 | 0.01262 |

## Depth 2: Full-Over-Phase Excess

| candidate | selected mass | selected mean | selected contribution | complement mean | complement p95 | complement contribution | global mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `source_odd_3_or_v2_2` | 0.562469 | 0.0237287 | 0.808025 | 0.00724742 | 0 | 0.191975 | 0.0165176 |
| `source_odd_3` | 0.499969 | 0.0261895 | 0.792725 | 0.00684696 | 0 | 0.207275 | 0.0165176 |
| `source_v2_0_or_2_odd_3` | 0.3125 | 0.03927 | 0.742956 | 0.00617565 | 0 | 0.257044 | 0.0165176 |
| `source_v2_2` | 0.125 | 0.0623322 | 0.471709 | 0.00997271 | 0 | 0.528291 | 0.0165176 |
| `source_v2_2_odd_3` | 0.0625 | 0.120621 | 0.456409 | 0.00957743 | 0 | 0.543591 | 0.0165176 |
| `source_v2_0_odd_3` | 0.25 | 0.0189323 | 0.286547 | 0.0157127 | 0.125 | 0.713453 | 0.0165176 |

## Interpretation Guardrail

A promising enriched component should have small selected mass, large
selected contribution, and a substantially smaller complement mean
or p95.  This only motivates an enlarged symbolic model; it does not
define an infinite operator or a Banach norm.
