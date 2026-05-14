# Refined Square Kernel Probe

Status: finite smoke diagnostic only.  This report does not
close Gate 10.B and does not define an infinite operator.

## Scope

- T: `12`
- j-counts: `16,32`
- refine bits: `0,5,8,10`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- traced rows: `524284`
- terminal rows: `469560`
- return rows: `54724`

## Prefix Drift

| bits | j_left | j_right | source keys | mean samples/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 16 | 32 | 112 | 2340.53571 | 0.00138619007 | 0.00243425369 | 0.0833333333 | 0.12890625 |
| 5 | 16 | 32 | 200 | 1310.7 | 0.00493992965 | 0.00790023804 | 0.041015625 | 0.59765625 |
| 8 | 16 | 32 | 1072 | 244.533582 | 0.0123695007 | 0.0370330811 | 0.041015625 | 0.59765625 |
| 10 | 16 | 32 | 4128 | 63.502907 | 0.0152083349 | 0.0490722656 | 0.0508422852 | 0.59765625 |

## Interpretation Guardrails

- `bits = 0` is the phase-only square kernel.
- `bits > 0` records low residue bits at both source and destination.
- This is a retraced smoke window, not a generated Lean matrix.
- A useful `A1` branch still needs larger-scale stability and a Banach norm.
