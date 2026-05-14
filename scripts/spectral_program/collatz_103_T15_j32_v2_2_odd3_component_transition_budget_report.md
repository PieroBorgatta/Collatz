# Two-Component Transition Budget

Status: finite diagnostic output, not a theorem.

Bad component convention:

- bad rule: `v2_2_odd3`.
- `bad(src) := src_v2 == 2 and src_odd == 3`.
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
- bad rule: `v2_2_odd3`
- delta cutoffs: `4,5,8`

## Trace Meta

| T | source groups | j count | t window | samples | good samples | bad samples |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 131072 | 32 | 1048576 | 4194300 | 3932156 | 262144 |

## Weighted Two-Component Matrix

| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 | 0.017485529 | 0.0011791947 | 0.018664724 | 0.19679618 | 0.013162643 | 0.20995882 | 0.030710211 |

## Source Components

| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |
|---:|---|---:|---:|---:|---:|---:|
| 15 | `good` | 0.93749994 | 0.074991938 | 0.92500806 | 0.018664724 | 0 |
| 15 | `bad` | 0.06250006 | 0.55412292 | 0.44587708 | 0.20995882 | 0 |

## Return Flow

| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |
|---:|---|---|---:|---:|---:|
| 15 | `good` | `good` | 0.070283071 | 0.017485529 | 0.93682228 |
| 15 | `good` | `bad` | 0.0047088671 | 0.0011791947 | 0.063177719 |
| 15 | `bad` | `good` | 0.51933289 | 0.19679618 | 0.93730846 |
| 15 | `bad` | `bad` | 0.034790039 | 0.013162643 | 0.062691544 |

## Delta Tail Weight

| T | component | cutoff | tail weight/return weight | tail weight/source |
|---:|---|---:|---:|---:|
| 15 | `good` | 4 | 0.0069605784 | 0.00012991727 |
| 15 | `good` | 5 | 0.0014525303 | 2.7111076e-05 |
| 15 | `good` | 8 | 1.1010721e-05 | 2.0551206e-07 |
| 15 | `bad` | 4 | 0.00020340526 | 4.2706728e-05 |
| 15 | `bad` | 5 | 3.534397e-05 | 7.4207783e-06 |
| 15 | `bad` | 8 | 1.4194365e-07 | 2.9802322e-08 |

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
