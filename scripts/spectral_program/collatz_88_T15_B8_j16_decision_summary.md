# Cylinder Signature Stability Decision Summary

Status: diagnostic output, not a theorem.

## Inputs

- T values: `15`
- j-counts: `8,16`
- block size: `8`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- include t=0: `False`

## Aggregate Signals

- final prefix j_count: `16`
- final prefix groups: `131072`
- boundary group share: `0`
- bulk exact status-majority fraction: `0.794312`
- bulk exact phase-majority fraction: `0.785004`
- bulk exact full-majority fraction: `0.723785`
- bulk average status-majority fraction: `0.974754`
- bulk average phase-majority fraction: `0.968542`
- bulk average delta-majority fraction: `0.952701`
- bulk average full-majority fraction: `0.948709`
- stable-status bulk groups with phase majority <= 0.5: `1096`
- status dominant flip fraction across adjacent blocks: `0.00244141`
- phase dominant flip fraction across adjacent blocks: `0.000793457`
- delta dominant flip fraction across adjacent blocks: `0.0167542`
- full dominant flip fraction across adjacent blocks: `0.0177002`
- status TV p95: `0.125`
- phase TV p95: `0.25`
- delta TV p95: `0.25`
- full TV p95: `0.25`

## Preliminary Recommendation

`enlarge symbolic state`

This recommendation is a modeling diagnostic only.  It does not imply
Conjecture 6, an infinite-operator bound, a Lasota-Yorke inequality,
Keller-Liverani convergence, or a spectral gap.

## Worst Adjacent-Block Full-Signature Drifts

| T | r | h | block A | block B | TV | dominant A | dominant B | changed |
|---:|---:|---:|---:|---:|---:|---|---|---:|
| 15 | 3411 | 0 | 0 | 8 | 0.75 | `return|0|1|1|2` | `return|1|1|1|2` | 1 |
| 15 | 3411 | 1 | 0 | 8 | 0.75 | `return|0|1|2|2` | `return|1|1|2|2` | 1 |
| 15 | 3411 | 2 | 0 | 8 | 0.75 | `return|0|1|3|2` | `return|1|1|3|2` | 1 |
| 15 | 3411 | 3 | 0 | 8 | 0.75 | `return|0|1|0|2` | `return|1|1|0|2` | 1 |
| 15 | 23209 | 0 | 0 | 8 | 0.75 | `terminal` | `terminal` | 0 |
| 15 | 23209 | 1 | 0 | 8 | 0.75 | `terminal` | `terminal` | 0 |
| 15 | 23209 | 2 | 0 | 8 | 0.75 | `terminal` | `terminal` | 0 |
| 15 | 23209 | 3 | 0 | 8 | 0.75 | `terminal` | `terminal` | 0 |
| 15 | 393 | 0 | 0 | 8 | 0.625 | `terminal` | `terminal` | 0 |
| 15 | 393 | 1 | 0 | 8 | 0.625 | `terminal` | `terminal` | 0 |

## Worst Bulk Final-Prefix Groups

| T | r | h | source phase | status maj | phase maj | delta maj | full maj | full tail weight fraction |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 15 | 951 | 0 | `v2=0|odd=3|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.911111 |
| 15 | 951 | 1 | `v2=0|odd=3|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.911111 |
| 15 | 951 | 2 | `v2=0|odd=3|h=2` | 1 | 0.25 | 0.5 | 0.125 | 0.911111 |
| 15 | 951 | 3 | `v2=0|odd=3|h=3` | 1 | 0.25 | 0.5 | 0.125 | 0.911111 |
| 15 | 1672 | 0 | `v2=3|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 1 | `v2=3|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 2 | `v2=3|odd=1|h=2` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 3 | `v2=3|odd=1|h=3` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 5477 | 0 | `v2=0|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.829787 |
| 15 | 5477 | 1 | `v2=0|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.829787 |
