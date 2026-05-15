# Phase Obstruction Budget

Status: finite diagnostic output only.  This report asks whether
the phase martingale obstruction is localized in small structural
source classes.  It does not prove Lasota-Yorke, Hennion,
Keller-Liverani, a spectral gap, or Collatz.

## Top Phase-TV Structural Contributions

| tag | depth | stratum | value | mass | selected mean | contribution | complement mean | global mean |
|---|---:|---|---|---:|---:|---:|---:|---:|
| `T15_d2_tail3` | 0 | `r_v2` | `0` | 0.5 | 0.0564308 | 0.662336 | 0.0287689 | 0.0425999 |
| `T15_d2_tail3` | 0 | `source_v2` | `0` | 0.5 | 0.0564308 | 0.662336 | 0.0287689 | 0.0425999 |
| `T15_d2_tail3` | 0 | `source_odd` | `3` | 0.499969 | 0.0499546 | 0.586288 | 0.035246 | 0.0425999 |
| `T15_d2_tail3` | 0 | `source_odd` | `1` | 0.500031 | 0.035246 | 0.413712 | 0.0499546 | 0.0425999 |
| `T15_d2_tail3` | 1 | `r_v2` | `0` | 0.5 | 0.0564938 | 0.675043 | 0.0271954 | 0.0418446 |
| `T15_d2_tail3` | 1 | `source_v2` | `0` | 0.5 | 0.0564938 | 0.675043 | 0.0271954 | 0.0418446 |
| `T15_d2_tail3` | 1 | `source_odd` | `3` | 0.499969 | 0.0498745 | 0.595913 | 0.0338156 | 0.0418446 |
| `T15_d2_tail3` | 1 | `source_v2_odd` | `0|3` | 0.25 | 0.0718307 | 0.429152 | 0.0318492 | 0.0418446 |
| `T15_d2_tail3` | 2 | `r_v2` | `0` | 0.5 | 0.0564098 | 0.686721 | 0.0257339 | 0.0410719 |
| `T15_d2_tail3` | 2 | `source_v2` | `0` | 0.5 | 0.0564098 | 0.686721 | 0.0257339 | 0.0410719 |
| `T15_d2_tail3` | 2 | `source_odd` | `3` | 0.499969 | 0.0496856 | 0.604825 | 0.0324592 | 0.0410719 |
| `T15_d2_tail3` | 2 | `source_v2_odd` | `0|3` | 0.25 | 0.0732422 | 0.445817 | 0.0303485 | 0.0410719 |
| `T16_d1_tail2` | 0 | `r_v2` | `0` | 0.5 | 0.0610085 | 0.678216 | 0.0289459 | 0.0449772 |
| `T16_d1_tail2` | 0 | `source_v2` | `0` | 0.5 | 0.0610085 | 0.678216 | 0.0289459 | 0.0449772 |
| `T16_d1_tail2` | 0 | `source_odd` | `3` | 0.499985 | 0.0540826 | 0.601204 | 0.0358723 | 0.0449772 |
| `T16_d1_tail2` | 0 | `source_v2_odd` | `0|3` | 0.25 | 0.0782089 | 0.434714 | 0.0338999 | 0.0449772 |
| `T16_d1_tail2` | 1 | `r_v2` | `0` | 0.5 | 0.0610466 | 0.688173 | 0.0276616 | 0.0443541 |
| `T16_d1_tail2` | 1 | `source_v2` | `0` | 0.5 | 0.0610466 | 0.688173 | 0.0276616 | 0.0443541 |
| `T16_d1_tail2` | 1 | `source_odd` | `3` | 0.499985 | 0.0539567 | 0.608231 | 0.0347521 | 0.0443541 |
| `T16_d1_tail2` | 1 | `source_v2_odd` | `0|3` | 0.25 | 0.0796204 | 0.448777 | 0.0325987 | 0.0443541 |

## Reading

The phase obstruction is not a small exceptional set.  The strongest
single structural contributors usually have mass about `1/2` and
contribution about `0.66--0.69`; after removing them, the complement
mean is still around `0.025--0.028`.  This makes a finite-rank
exceptional correction less plausible for the phase term than for
the label-excess term.

Consequently, the Banach-pair route needs a structural phase theorem
or a different operator/quotient.  Merely isolating a bad labelled
component does not solve the phase martingale obstruction.
