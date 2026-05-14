# Z2 Cylinder Oscillation Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- T values: `15`
- max depth: `3`
- tail bits: `2`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- include t=0: `False`

For each depth `d`, this compares the two children inside a fixed
high-bit parent class `j mod 2^d`.  This is closer to a 2-adic
martingale oscillation test than adjacent ordinary `j` intervals.

## Trace Meta

| T | max j | source groups | pair rows |
|---:|---:|---:|---:|
| 15 | 64 | 131072 | 7864320 |

## Aggregates

| depth | level | mean TV | p95 TV | p99 TV | max TV | dominant flip | samples | min child counts |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 0 | `delta` | 0.041382 | 0.15625 | 0.5 | 1 | 0.0231323 | 131072 | 31/32 |
| 0 | `full` | 0.0526182 | 0.1875 | 0.96875 | 1 | 0.0273743 | 131072 | 31/32 |
| 0 | `phase` | 0.0425999 | 0.15625 | 0.90625 | 1 | 0.0124817 | 131072 | 31/32 |
| 0 | `status` | 0.028598 | 0.125 | 0.46875 | 0.9375 | 0.0120544 | 131072 | 31/32 |
| 1 | `delta` | 0.0452396 | 0.1875 | 0.5 | 1 | 0.0267944 | 262144 | 15/16 |
| 1 | `full` | 0.0544645 | 0.25 | 0.9375 | 1 | 0.02948 | 262144 | 15/16 |
| 1 | `phase` | 0.0418446 | 0.1875 | 0.875 | 1 | 0.0116119 | 262144 | 15/16 |
| 1 | `status` | 0.0285217 | 0.125 | 0.4375 | 0.9375 | 0.0102234 | 262144 | 15/16 |
| 2 | `delta` | 0.0502739 | 0.25 | 0.5 | 1 | 0.0223236 | 524288 | 7/8 |
| 2 | `full` | 0.0575895 | 0.25 | 0.875 | 1 | 0.0242691 | 524288 | 7/8 |
| 2 | `phase` | 0.0410719 | 0.25 | 0.75 | 1 | 0.0106049 | 524288 | 7/8 |
| 2 | `status` | 0.0292443 | 0.125 | 0.5 | 1 | 0.0096283 | 524288 | 7/8 |
| 3 | `delta` | 0.0549879 | 0.25 | 0.5 | 1 | 0.0278397 | 1048576 | 3/4 |
| 3 | `full` | 0.0606241 | 0.5 | 0.75 | 1 | 0.0293694 | 1048576 | 3/4 |
| 3 | `phase` | 0.0408087 | 0.25 | 0.75 | 1 | 0.0128937 | 1048576 | 3/4 |
| 3 | `status` | 0.031312 | 0.25 | 0.5 | 1 | 0.0145264 | 1048576 | 3/4 |

## Interpretation Guardrail

Small values here would support a 2-adic weak/martingale norm.
Large or nondecreasing values would pressure the analytic branch.
Either way, these are finite sampled oscillations, not proof of
continuity, compactness, Lasota-Yorke, or Keller-Liverani
convergence.
