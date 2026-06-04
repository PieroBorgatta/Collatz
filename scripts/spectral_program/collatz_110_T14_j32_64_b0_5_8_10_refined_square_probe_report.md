# Refined Square Kernel Probe

Status: finite smoke diagnostic only.  This report does not
close Gate 10.B and does not define an infinite operator.

## Scope

- T: `14`
- j-counts: `32,64`
- refine bits: `0,5,8,10`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `14`
- max steps: `1000`
- traced rows: `4194300`
- terminal rows: `3754160`
- return rows: `440140`

## Prefix Drift

| bits | j_left | j_right | source keys | mean samples/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 32 | 64 | 120 | 17476.2333 | 0.000420440901 | 0.000633001328 | 0.0283203125 | 0.0309139785 |
| 5 | 32 | 64 | 208 | 10082.4423 | 0.00160995368 | 0.00250665098 | 0.0280151367 | 0.05859375 |
| 8 | 32 | 64 | 1080 | 1941.8037 | 0.00848590605 | 0.0235137939 | 0.0241374969 | 0.6171875 |
| 10 | 32 | 64 | 4136 | 507.047389 | 0.0121733793 | 0.0367279053 | 0.0367279053 | 0.618164062 |

## Interpretation Guardrails

- `bits = 0` is the phase-only square kernel.
- `bits > 0` records low residue bits at both source and destination.
- This is a retraced smoke window, not a generated Lean matrix.
- A useful `A1` branch still needs larger-scale stability and a Banach norm.
