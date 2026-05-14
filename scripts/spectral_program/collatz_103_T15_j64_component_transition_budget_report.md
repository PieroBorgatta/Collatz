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
- j count: `64`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- delta cutoffs: `4,5,8`

## Trace Meta

| T | source groups | j count | t window | samples | good samples | bad samples |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 131072 | 64 | 2097152 | 8388604 | 5767164 | 2621440 |

## Weighted Two-Component Matrix

| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 | 0.012281296 | 0.0054655765 | 0.017746872 | 0.040839452 | 0.018100693 | 0.058940144 | 0.03041195 |

## Source Components

| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |
|---:|---|---:|---:|---:|---:|---:|
| 15 | `good` | 0.68749985 | 0.057945292 | 0.94205471 | 0.017746872 | 0 |
| 15 | `bad` | 0.31250015 | 0.20822754 | 0.79177246 | 0.058940144 | 0 |

## Return Flow

| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |
|---:|---|---|---:|---:|---:|
| 15 | `good` | `good` | 0.040150063 | 0.012281296 | 0.69202593 |
| 15 | `good` | `bad` | 0.017795228 | 0.0054655765 | 0.30797407 |
| 15 | `bad` | `good` | 0.14427948 | 0.040839452 | 0.69289704 |
| 15 | `bad` | `bad` | 0.063948059 | 0.018100693 | 0.30710296 |

## Delta Tail Weight

| T | component | cutoff | tail weight/return weight | tail weight/source |
|---:|---|---:|---:|---:|
| 15 | `good` | 4 | 0.0026245807 | 4.6578099e-05 |
| 15 | `good` | 5 | 0.000505608 | 8.9729606e-06 |
| 15 | `good` | 8 | 4.1076088e-06 | 7.2897208e-08 |
| 15 | `bad` | 4 | 0.0050130195 | 0.00029546809 |
| 15 | `bad` | 5 | 0.0010455887 | 6.1627151e-05 |
| 15 | `bad` | 8 | 8.6282227e-06 | 5.0854869e-07 |

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
