# Two-Component Transition Budget

Status: finite diagnostic output, not a theorem.

Bad component convention:

- bad rule: `odd3_or_v2_2`.
- `bad(src) := src_odd == 3 or src_v2 == 2`.
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
- bad rule: `odd3_or_v2_2`
- delta cutoffs: `4,5,8`

## Trace Meta

| T | source groups | j count | t window | samples | good samples | bad samples |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 131072 | 32 | 1048576 | 4194300 | 1835008 | 2359292 |

## Weighted Two-Component Matrix

| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 | 0.009046653 | 0.011509071 | 0.020555724 | 0.016964883 | 0.021483996 | 0.038448879 | 0.03055983 |

## Source Components

| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |
|---:|---|---:|---:|---:|---:|---:|
| 15 | `good` | 0.43750042 | 0.07006618 | 0.92993382 | 0.020555724 | 0 |
| 15 | `bad` | 0.56249958 | 0.13205996 | 0.86794004 | 0.038448879 | 0 |

## Return Flow

| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |
|---:|---|---|---:|---:|---:|
| 15 | `good` | `good` | 0.030835833 | 0.009046653 | 0.44010384 |
| 15 | `good` | `bad` | 0.039230347 | 0.011509071 | 0.55989616 |
| 15 | `bad` | `good` | 0.058373444 | 0.016964883 | 0.4412322 |
| 15 | `bad` | `bad` | 0.073686513 | 0.021483996 | 0.5587678 |

## Delta Tail Weight

| T | component | cutoff | tail weight/return weight | tail weight/source |
|---:|---|---:|---:|---:|
| 15 | `good` | 4 | 0.0024766217 | 5.0908753e-05 |
| 15 | `good` | 5 | 0.00044188773 | 9.0833221e-06 |
| 15 | `good` | 8 | 4.4530518e-06 | 9.1535704e-08 |
| 15 | `bad` | 4 | 0.0047251929 | 0.00018167837 |
| 15 | `bad` | 5 | 0.0010129001 | 3.8944872e-05 |
| 15 | `bad` | 8 | 7.1429169e-06 | 2.7463714e-07 |

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
