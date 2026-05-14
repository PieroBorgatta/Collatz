# Cylinder Signature Stability Decision Summary

Status: diagnostic output, not a theorem.

## Inputs

- T values: `15`
- j-counts: `16,32`
- block size: `16`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- include t=0: `False`

## Aggregate Signals

- final prefix j_count: `32`
- final prefix groups: `131072`
- boundary group share: `0`
- bulk exact status-majority fraction: `0.73941`
- bulk exact phase-majority fraction: `0.729584`
- bulk exact full-majority fraction: `0.662506`
- bulk average status-majority fraction: `0.974776`
- bulk average phase-majority fraction: `0.968593`
- bulk average delta-majority fraction: `0.951774`
- bulk average full-majority fraction: `0.947732`
- stable-status bulk groups with phase majority <= 0.5: `1096`
- status dominant flip fraction across adjacent blocks: `0.0012207`
- phase dominant flip fraction across adjacent blocks: `0.000701904`
- delta dominant flip fraction across adjacent blocks: `0.0109253`
- full dominant flip fraction across adjacent blocks: `0.0124817`
- status TV p95: `0.125`
- phase TV p95: `0.1875`
- delta TV p95: `0.125`
- full TV p95: `0.1875`

## Preliminary Recommendation

`enlarge symbolic state`

This recommendation is a modeling diagnostic only.  It does not imply
Conjecture 6, an infinite-operator bound, a Lasota-Yorke inequality,
Keller-Liverani convergence, or a spectral gap.

## Worst Adjacent-Block Full-Signature Drifts

| T | r | h | block A | block B | TV | dominant A | dominant B | changed |
|---:|---:|---:|---:|---:|---:|---|---|---:|
| 15 | 303 | 0 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 303 | 1 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 303 | 2 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 303 | 3 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 8135 | 0 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 8135 | 1 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 8135 | 2 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 8135 | 3 | 0 | 16 | 0.5 | `terminal` | `terminal` | 0 |
| 15 | 12857 | 0 | 0 | 16 | 0.5 | `return|0|3|1|2` | `return|0|3|1|2` | 0 |
| 15 | 12857 | 1 | 0 | 16 | 0.5 | `return|0|3|2|2` | `return|0|3|2|2` | 0 |

## Worst Bulk Final-Prefix Groups

| T | r | h | source phase | status maj | phase maj | delta maj | full maj | full tail weight fraction |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 15 | 951 | 0 | `v2=0|odd=3|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.913978 |
| 15 | 951 | 1 | `v2=0|odd=3|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.913978 |
| 15 | 951 | 2 | `v2=0|odd=3|h=2` | 1 | 0.25 | 0.5 | 0.125 | 0.913978 |
| 15 | 951 | 3 | `v2=0|odd=3|h=3` | 1 | 0.25 | 0.5 | 0.125 | 0.913978 |
| 15 | 1672 | 0 | `v2=3|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 1 | `v2=3|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 2 | `v2=3|odd=1|h=2` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 3 | `v2=3|odd=1|h=3` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 5477 | 0 | `v2=0|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.831579 |
| 15 | 5477 | 1 | `v2=0|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.831579 |
