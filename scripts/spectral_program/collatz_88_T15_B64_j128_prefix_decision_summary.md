# Cylinder Signature Stability Decision Summary

Status: diagnostic output, not a theorem.

## Inputs

- T values: `15`
- j-counts: `64,128`
- block size: `64`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- include t=0: `False`

## Aggregate Signals

- final prefix j_count: `128`
- final prefix groups: `131072`
- boundary group share: `0`
- bulk exact status-majority fraction: `0.67569`
- bulk exact phase-majority fraction: `0.665833`
- bulk exact full-majority fraction: `0.596497`
- bulk average status-majority fraction: `0.974753`
- bulk average phase-majority fraction: `0.968595`
- bulk average delta-majority fraction: `0.951734`
- bulk average full-majority fraction: `0.947595`
- stable-status bulk groups with phase majority <= 0.5: `1008`
- status dominant flip fraction across adjacent blocks: `0`
- phase dominant flip fraction across adjacent blocks: `0.0017395`
- delta dominant flip fraction across adjacent blocks: `0.000854492`
- full dominant flip fraction across adjacent blocks: `0.00265503`
- status TV p95: `0.046875`
- phase TV p95: `0.078125`
- delta TV p95: `0.078125`
- full TV p95: `0.109375`

## Preliminary Recommendation

`enlarge symbolic state`

This recommendation is a modeling diagnostic only.  It does not imply
Conjecture 6, an infinite-operator bound, a Lasota-Yorke inequality,
Keller-Liverani convergence, or a spectral gap.

## Worst Adjacent-Block Full-Signature Drifts

| T | r | h | block A | block B | TV | dominant A | dominant B | changed |
|---:|---:|---:|---:|---:|---:|---|---|---:|
| 15 | 10167 | 0 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 10167 | 1 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 10167 | 2 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 10167 | 3 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 16751 | 0 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 16751 | 1 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 16751 | 2 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 16751 | 3 | 0 | 64 | 0.265625 | `terminal` | `terminal` | 0 |
| 15 | 8495 | 0 | 0 | 64 | 0.25 | `terminal` | `terminal` | 0 |
| 15 | 8495 | 1 | 0 | 64 | 0.25 | `terminal` | `terminal` | 0 |

## Worst Bulk Final-Prefix Groups

| T | r | h | source phase | status maj | phase maj | delta maj | full maj | full tail weight fraction |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 15 | 951 | 0 | `v2=0|odd=3|h=0` | 1 | 0.25 | 0.507812 | 0.125 | 0.915567 |
| 15 | 951 | 1 | `v2=0|odd=3|h=1` | 1 | 0.25 | 0.507812 | 0.125 | 0.915567 |
| 15 | 951 | 2 | `v2=0|odd=3|h=2` | 1 | 0.25 | 0.507812 | 0.125 | 0.915567 |
| 15 | 951 | 3 | `v2=0|odd=3|h=3` | 1 | 0.25 | 0.507812 | 0.125 | 0.915567 |
| 15 | 1672 | 0 | `v2=3|odd=1|h=0` | 1 | 0.25 | 0.507812 | 0.125 | 0.91623 |
| 15 | 1672 | 1 | `v2=3|odd=1|h=1` | 1 | 0.25 | 0.507812 | 0.125 | 0.91623 |
| 15 | 1672 | 2 | `v2=3|odd=1|h=2` | 1 | 0.25 | 0.507812 | 0.125 | 0.91623 |
| 15 | 1672 | 3 | `v2=3|odd=1|h=3` | 1 | 0.25 | 0.507812 | 0.125 | 0.91623 |
| 15 | 5477 | 0 | `v2=0|odd=1|h=0` | 1 | 0.25 | 0.5 | 0.125 | 0.832021 |
| 15 | 5477 | 1 | `v2=0|odd=1|h=1` | 1 | 0.25 | 0.5 | 0.125 | 0.832021 |
