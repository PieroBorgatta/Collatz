# Two-Component Transition Budget

Status: finite diagnostic output, not a theorem.

Bad component convention:

- `bad(src) := src_odd = 3 and src_v2 in {0,2}`.
- `good` is the complement in the sampled symbolic state.

The weighted entries below are empirical averages of `2^{-delta}`
over source samples in the declared component.  Terminal/killed
events carry zero transfer weight in this diagnostic.

## Inputs

- T values: `12`
- j count: `16`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- delta cutoffs: `4,5,8`

## Trace Meta

| T | source groups | j count | samples | good samples | bad samples |
|---:|---:|---:|---:|---:|---:|
| 12 | 16384 | 16 | 262140 | 180220 | 81920 |

## Weighted Two-Component Matrix

| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 12 | 0.012155066 | 0.0054441273 | 0.017599193 | 0.040500844 | 0.017905426 | 0.05840627 | 0.030155007 |

## Source Components

| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |
|---:|---|---:|---:|---:|---:|---:|
| 12 | `good` | 0.68749523 | 0.057574076 | 0.94242592 | 0.017599193 | 0 |
| 12 | `bad` | 0.31250477 | 0.20566406 | 0.79433594 | 0.05840627 | 0 |

## Return Flow

| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |
|---:|---|---|---:|---:|---:|
| 12 | `good` | `good` | 0.039751415 | 0.012155066 | 0.6906604 |
| 12 | `good` | `bad` | 0.017822661 | 0.0054441273 | 0.3093396 |
| 12 | `bad` | `good` | 0.14228516 | 0.040500844 | 0.69343315 |
| 12 | `bad` | `bad` | 0.063378906 | 0.017905426 | 0.30656685 |

## Delta Tail Weight

| T | component | cutoff | tail weight/return weight | tail weight/source |
|---:|---|---:|---:|---:|
| 12 | `good` | 4 | 0.0029090031 | 5.1196108e-05 |
| 12 | `good` | 5 | 0.00062318187 | 1.0967498e-05 |
| 12 | `good` | 8 | 2.4631695e-06 | 4.3349795e-08 |
| 12 | `bad` | 4 | 0.0050456447 | 0.00029469728 |
| 12 | `bad` | 5 | 0.0010484801 | 6.1237812e-05 |
| 12 | `bad` | 8 | 6.7354183e-06 | 3.9339066e-07 |

## Interpretation Guardrail

This diagnostic can support a two-component ansatz only if the good
component has a controlled row budget and the bad component can be
handled either by finite-rank methods, an exceptional-mass estimate,
or a separate labelled-state argument.  A small finite 2x2 spectral
radius here is not a spectral theorem for an infinite operator.
