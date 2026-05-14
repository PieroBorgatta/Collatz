# Cylinder Signature Stability Decision Summary

Status: diagnostic output, not a theorem.

## Inputs

- T values: `15`
- j-counts: `32,64`
- block size: `32`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `5000`
- include t=0: `False`

## Aggregate Signals

- final prefix j_count: `64`
- final prefix groups: `131072`
- boundary group share: `0`
- bulk exact status-majority fraction: `0.700562`
- bulk exact phase-majority fraction: `0.690704`
- bulk exact full-majority fraction: `0.621368`
- bulk average status-majority fraction: `0.974787`
- bulk average phase-majority fraction: `0.968628`
- bulk average delta-majority fraction: `0.951778`
- bulk average full-majority fraction: `0.947678`
- stable-status bulk groups with phase majority <= 0.5: `1048`
- status dominant flip fraction across adjacent blocks: `0`
- phase dominant flip fraction across adjacent blocks: `0.00128174`
- delta dominant flip fraction across adjacent blocks: `0.00863647`
- full dominant flip fraction across adjacent blocks: `0.011322`
- status TV p95: `0.0625`
- phase TV p95: `0.125`
- delta TV p95: `0.09375`
- full TV p95: `0.15625`

## Preliminary Recommendation

`enlarge symbolic state`

This recommendation is a modeling diagnostic only.  It does not imply
Conjecture 6, an infinite-operator bound, a Lasota-Yorke inequality,
Keller-Liverani convergence, or a spectral gap.

## Worst Adjacent-Block Full-Signature Drifts

| T | r | h | block A | block B | TV | dominant A | dominant B | changed |
|---:|---:|---:|---:|---:|---:|---|---|---:|
| 15 | 6101 | 0 | 0 | 32 | 0.375 | `terminal` | `terminal` | 0 |
| 15 | 6101 | 1 | 0 | 32 | 0.375 | `terminal` | `terminal` | 0 |
| 15 | 6101 | 2 | 0 | 32 | 0.375 | `terminal` | `terminal` | 0 |
| 15 | 6101 | 3 | 0 | 32 | 0.375 | `terminal` | `terminal` | 0 |
| 15 | 16423 | 0 | 0 | 32 | 0.34375 | `terminal` | `terminal` | 0 |
| 15 | 16423 | 1 | 0 | 32 | 0.34375 | `terminal` | `terminal` | 0 |
| 15 | 16423 | 2 | 0 | 32 | 0.34375 | `terminal` | `terminal` | 0 |
| 15 | 16423 | 3 | 0 | 32 | 0.34375 | `terminal` | `terminal` | 0 |
| 15 | 16751 | 0 | 0 | 32 | 0.34375 | `terminal` | `terminal` | 0 |
| 15 | 16751 | 1 | 0 | 32 | 0.34375 | `terminal` | `terminal` | 0 |

## Worst Bulk Final-Prefix Groups

| T | r | h | source phase | status maj | phase maj | delta maj | full maj | full tail weight fraction |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 15 | 951 | 0 | `v2=0|odd=3|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.915344 |
| 15 | 951 | 1 | `v2=0|odd=3|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.915344 |
| 15 | 951 | 2 | `v2=0|odd=3|h=2` | 1 | 0.25 | 0.5 | 0.125 | 0.915344 |
| 15 | 951 | 3 | `v2=0|odd=3|h=3` | 1 | 0.25 | 0.5 | 0.125 | 0.915344 |
| 15 | 1672 | 0 | `v2=3|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 1 | `v2=3|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 2 | `v2=3|odd=1|h=2` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 1672 | 3 | `v2=3|odd=1|h=3` | 1 | 0.25 | 0.5 | 0.125 | 0.916667 |
| 15 | 5477 | 0 | `v2=0|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.832461 |
| 15 | 5477 | 1 | `v2=0|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.832461 |
