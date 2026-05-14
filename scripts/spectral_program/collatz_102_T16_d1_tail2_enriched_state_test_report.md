# Enriched State Test

Status: finite diagnostic output, not a theorem.

## Inputs

- T values: `16`
- max depth: `1`
- tail bits: `2`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`

The selected component is the part that an enriched state would
isolate.  The complement columns measure the remaining obstruction
outside that component.

## Trace Meta

| T | max j | source groups | parent-child pairs |
|---:|---:|---:|---:|
| 16 | 16 | 262144 | 786432 |

## Depth 0: Full-Over-Phase Excess

| candidate | selected mass | selected mean | selected contribution | complement mean | complement p95 | complement contribution | global mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `source_odd_3_or_v2_2` | 0.562485 | 0.0234551 | 0.815684 | 0.0068139 | 0 | 0.184316 | 0.0161743 |
| `source_odd_3` | 0.499985 | 0.0259293 | 0.801533 | 0.00641994 | 0 | 0.198467 | 0.0161743 |
| `source_v2_0_or_2_odd_3` | 0.3125 | 0.0391724 | 0.75684 | 0.00572066 | 0 | 0.24316 | 0.0161743 |
| `source_v2_2` | 0.125 | 0.0621948 | 0.48066 | 0.00959996 | 0 | 0.51934 | 0.0161743 |
| `source_v2_2_odd_3` | 0.0625 | 0.120728 | 0.466509 | 0.0092041 | 0 | 0.533491 | 0.0161743 |
| `source_v2_0_odd_3` | 0.25 | 0.0187836 | 0.29033 | 0.0153046 | 0.125 | 0.70967 | 0.0161743 |

## Depth 1: Full-Over-Phase Excess

| candidate | selected mass | selected mean | selected contribution | complement mean | complement p95 | complement contribution | global mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `source_odd_3_or_v2_2` | 0.562485 | 0.0284771 | 0.829186 | 0.00754194 | 0 | 0.170814 | 0.0193176 |
| `source_odd_3` | 0.499985 | 0.0315485 | 0.816548 | 0.00708749 | 0 | 0.183452 | 0.0193176 |
| `source_v2_0_or_2_odd_3` | 0.3125 | 0.0474182 | 0.767081 | 0.00654463 | 0 | 0.232919 | 0.0193176 |
| `source_v2_2` | 0.125 | 0.0780182 | 0.504838 | 0.0109318 | 0 | 0.495162 | 0.0193176 |
| `source_v2_2_odd_3` | 0.0625 | 0.15213 | 0.4922 | 0.0104635 | 0 | 0.5078 | 0.0193176 |
| `source_v2_0_odd_3` | 0.25 | 0.0212402 | 0.274882 | 0.0186768 | 0.25 | 0.725118 | 0.0193176 |

## Interpretation Guardrail

A promising enriched component should have small selected mass, large
selected contribution, and a substantially smaller complement mean
or p95.  This only motivates an enlarged symbolic model; it does not
define an infinite operator or a Banach norm.
