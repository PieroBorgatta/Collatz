# Two-Component Transition Budget

Status: finite diagnostic output, not a theorem.

Bad component convention:

- `bad(src) := src_odd = 3 and src_v2 in {0,2}`.
- `good` is the complement in the sampled symbolic state.

The weighted entries below are empirical averages of `2^{-delta}`
over source samples in the declared component.  Terminal/killed
events carry zero transfer weight in this diagnostic.

## Inputs

- T values: `16`
- j count: `8`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- delta cutoffs: `4,5,8`

## Trace Meta

| T | source groups | j count | samples | good samples | bad samples |
|---:|---:|---:|---:|---:|---:|
| 16 | 262144 | 8 | 2097148 | 1441788 | 655360 |

## Weighted Two-Component Matrix

| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 16 | 0.012300449 | 0.0054556147 | 0.017756064 | 0.040779662 | 0.018012235 | 0.058791897 | 0.030342989 |

## Source Components

| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |
|---:|---|---:|---:|---:|---:|---:|
| 16 | `good` | 0.6874994 | 0.058094533 | 0.94190547 | 0.017756064 | 0 |
| 16 | `bad` | 0.3125006 | 0.20817871 | 0.79182129 | 0.058791897 | 0 |

## Return Flow

| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |
|---:|---|---|---:|---:|---:|
| 16 | `good` | `good` | 0.040319381 | 0.012300449 | 0.69274639 |
| 16 | `good` | `bad` | 0.017775151 | 0.0054556147 | 0.30725361 |
| 16 | `bad` | `good` | 0.14435425 | 0.040779662 | 0.69362726 |
| 16 | `bad` | `bad` | 0.063824463 | 0.018012235 | 0.30637274 |

## Delta Tail Weight

| T | component | cutoff | tail weight/return weight | tail weight/source |
|---:|---|---:|---:|---:|
| 16 | `good` | 4 | 0.0026553992 | 4.7149437e-05 |
| 16 | `good` | 5 | 0.0005265328 | 9.3491499e-06 |
| 16 | `good` | 8 | 4.0816496e-06 | 7.2474031e-08 |
| 16 | `bad` | 4 | 0.0050962406 | 0.00029961765 |
| 16 | `bad` | 5 | 0.0010863633 | 6.3869357e-05 |
| 16 | `bad` | 8 | 6.843313e-06 | 4.0233135e-07 |

## Interpretation Guardrail

This diagnostic can support a two-component ansatz only if the good
component has a controlled row budget and the bad component can be
handled either by finite-rank methods, an exceptional-mass estimate,
or a separate labelled-state argument.  A small finite 2x2 spectral
radius here is not a spectral theorem for an infinite operator.
