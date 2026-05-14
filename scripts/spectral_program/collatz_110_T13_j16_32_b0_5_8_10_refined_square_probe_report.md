# Refined Square Kernel Probe

Status: finite smoke diagnostic only.  This report does not
close Gate 10.B and does not define an infinite operator.

## Scope

- T: `13`
- j-counts: `16,32`
- refine bits: `0,5,8,10`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- traced rows: `1048572`
- terminal rows: `938588`
- return rows: `109984`

## Prefix Drift

| bits | j_left | j_right | source keys | mean samples/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 16 | 32 | 112 | 4681.10714 | 0.00109704799 | 0.00252437592 | 0.03515625 | 0.080078125 |
| 5 | 16 | 32 | 200 | 2621.42 | 0.00344425218 | 0.0051407814 | 0.03515625 | 0.142578125 |
| 8 | 16 | 32 | 1072 | 489.070896 | 0.0114045768 | 0.0301589966 | 0.0321044922 | 0.611328125 |
| 10 | 16 | 32 | 4128 | 127.006783 | 0.0135561906 | 0.0405578613 | 0.0416259766 | 0.611328125 |

## Interpretation Guardrails

- `bits = 0` is the phase-only square kernel.
- `bits > 0` records low residue bits at both source and destination.
- This is a retraced smoke window, not a generated Lean matrix.
- A useful `A1` branch still needs larger-scale stability and a Banach norm.
