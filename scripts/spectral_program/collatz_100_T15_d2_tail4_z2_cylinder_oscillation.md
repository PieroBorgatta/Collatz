# Z2 Cylinder Oscillation Diagnostic

Status: finite diagnostic output, not a theorem.

## Inputs

- T values: `15`
- max depth: `2`
- tail bits: `4`
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
| 15 | 128 | 131072 | 3670016 |

## Aggregates

| depth | level | mean TV | p95 TV | p99 TV | max TV | dominant flip | samples | min child counts |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 0 | `delta` | 0.0366331 | 0.140625 | 0.515625 | 1 | 0.00866699 | 131072 | 63/64 |
| 0 | `full` | 0.0486132 | 0.171875 | 0.953125 | 1 | 0.0126343 | 131072 | 63/64 |
| 0 | `phase` | 0.0399633 | 0.15625 | 0.890625 | 1 | 0.0124817 | 131072 | 63/64 |
| 0 | `status` | 0.0270172 | 0.125 | 0.484375 | 0.9375 | 0.0120544 | 131072 | 63/64 |
| 1 | `delta` | 0.0385127 | 0.15625 | 0.5 | 1 | 0.0228882 | 262144 | 31/32 |
| 1 | `full` | 0.0487704 | 0.1875 | 0.9375 | 1 | 0.026535 | 262144 | 31/32 |
| 1 | `phase` | 0.0388441 | 0.15625 | 0.875 | 1 | 0.0115662 | 262144 | 31/32 |
| 1 | `status` | 0.0259775 | 0.125 | 0.4375 | 0.9375 | 0.0110474 | 262144 | 31/32 |
| 2 | `delta` | 0.0424967 | 0.1875 | 0.5 | 1 | 0.0261154 | 524288 | 15/16 |
| 2 | `full` | 0.0509391 | 0.25 | 0.9375 | 1 | 0.0287399 | 524288 | 15/16 |
| 2 | `phase` | 0.0382137 | 0.1875 | 0.8125 | 1 | 0.0103607 | 524288 | 15/16 |
| 2 | `status` | 0.0260091 | 0.125 | 0.4375 | 0.9375 | 0.00964355 | 524288 | 15/16 |

## Interpretation Guardrail

Small values here would support a 2-adic weak/martingale norm.
Large or nondecreasing values would pressure the analytic branch.
Either way, these are finite sampled oscillations, not proof of
continuity, compactness, Lasota-Yorke, or Keller-Liverani
convergence.
