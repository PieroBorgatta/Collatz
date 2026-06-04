# Refined Square Kernel Probe

Status: finite smoke diagnostic only.  This report does not
close Gate 10.B and does not define an infinite operator.

## Scope

- T: `14`
- j-counts: `32,64,128`
- refine bits: `0`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `14`
- max steps: `1000`
- traced rows: `8388604`
- terminal rows: `7508568`
- return rows: `880036`

## Prefix Drift

| bits | j_left | j_right | source keys | mean samples/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 32 | 64 | 120 | 17476.2333 | 0.000420440901 | 0.000633001328 | 0.0283203125 | 0.0309139785 |
| 0 | 64 | 128 | 120 | 34952.5 | 0.000285774472 | 0.00056168437 | 0.021484375 | 0.0331541219 |

## Interpretation Guardrails

- `bits = 0` is the phase-only square kernel.
- `bits > 0` records low residue bits at both source and destination.
- This is a retraced smoke window, not a generated Lean matrix.
- A useful `A1` branch still needs larger-scale stability and a Banach norm.
