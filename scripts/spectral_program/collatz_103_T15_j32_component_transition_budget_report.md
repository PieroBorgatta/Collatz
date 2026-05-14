# Two-Component Transition Budget

Status: finite diagnostic output, not a theorem.

Bad component convention:

- `bad(src) := src_odd = 3 and src_v2 in {0,2}`.
- `good` is the complement in the sampled symbolic state.

The weighted entries below are empirical averages of `2^{-delta}`
over source samples in the declared component.  Terminal/killed
events carry zero transfer weight in this diagnostic.

## Inputs

- T values: `15`
- j count: `32`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- delta cutoffs: `4,5,8`

## Trace Meta

| T | source groups | j count | t window | samples | good samples | bad samples |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 131072 | 32 | 1048576 | 4194300 | 2883580 | 1310720 |

## Weighted Two-Component Matrix

| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 | 0.012278567 | 0.0054906632 | 0.017769231 | 0.040819731 | 0.018073894 | 0.058893625 | 0.030424963 |

## Source Components

| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |
|---:|---|---:|---:|---:|---:|---:|
| 15 | `good` | 0.6874997 | 0.057990415 | 0.94200959 | 0.017769231 | 0 |
| 15 | `bad` | 0.3125003 | 0.20822144 | 0.79177856 | 0.058893625 | 0 |

## Return Flow

| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |
|---:|---|---|---:|---:|---:|
| 15 | `good` | `good` | 0.040147317 | 0.012278567 | 0.69100164 |
| 15 | `good` | `bad` | 0.017843098 | 0.0054906632 | 0.30899836 |
| 15 | `bad` | `good` | 0.14434814 | 0.040819731 | 0.6931095 |
| 15 | `bad` | `bad` | 0.063873291 | 0.018073894 | 0.3068905 |

## Delta Tail Weight

| T | component | cutoff | tail weight/return weight | tail weight/source |
|---:|---|---:|---:|---:|
| 15 | `good` | 4 | 0.0026541902 | 4.7162918e-05 |
| 15 | `good` | 5 | 0.00050982743 | 9.0592412e-06 |
| 15 | `good` | 8 | 4.8409782e-06 | 8.6020459e-08 |
| 15 | `bad` | 4 | 0.0050011268 | 0.00029453449 |
| 15 | `bad` | 5 | 0.0010678065 | 6.2886998e-05 |
| 15 | `bad` | 8 | 7.3565052e-06 | 4.3325126e-07 |

## Interpretation Guardrail

This diagnostic can support a two-component ansatz only if the good
component has a controlled row budget and the bad component can be
handled either by finite-rank methods, an exceptional-mass estimate,
or a separate labelled-state argument.  A small finite 2x2 spectral
radius here is not a spectral theorem for an infinite operator.

This script aggregates over actual lifted sources `t`, not over
source-cylinder pair distributions.  Therefore two runs with the
same product `j_count * 2^T` enumerate the same `t` window and are
not independent stability checks in `T`.
