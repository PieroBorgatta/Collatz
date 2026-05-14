# Refined Square Kernel Probe

Status: finite smoke diagnostic only.  This report does not
close Gate 10.B and does not define an infinite operator.

## Scope

- T: `12`
- j-counts: `32,64,128`
- refine bits: `0,5,8,10`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`
- max steps: `1000`
- traced rows: `2097148`
- terminal rows: `1876956`
- return rows: `220192`

## Prefix Drift

| bits | j_left | j_right | source keys | mean samples/key | weighted L1 mean | weighted L1 p95 | key L1 p95 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 32 | 64 | 112 | 4681.10714 | 0.00109704799 | 0.00252437592 | 0.03515625 | 0.080078125 |
| 5 | 32 | 64 | 200 | 2621.42 | 0.00344425218 | 0.0051407814 | 0.03515625 | 0.142578125 |
| 8 | 32 | 64 | 1072 | 489.070896 | 0.0114045768 | 0.0301589966 | 0.0321044922 | 0.611328125 |
| 10 | 32 | 64 | 4128 | 127.006783 | 0.0135561906 | 0.0405578613 | 0.0416259766 | 0.611328125 |
| 0 | 64 | 128 | 112 | 9362.25 | 0.000647069352 | 0.00109326839 | 0.0237903226 | 0.0556640625 |
| 5 | 64 | 128 | 200 | 5242.86 | 0.00232221302 | 0.00316691399 | 0.0278225806 | 0.0712890625 |
| 8 | 64 | 128 | 1072 | 978.145522 | 0.0101905453 | 0.0273723602 | 0.0278949738 | 0.616210938 |
| 10 | 64 | 128 | 4128 | 254.014535 | 0.0129098735 | 0.0367126465 | 0.0367126465 | 0.618164062 |

## Interpretation Guardrails

- `bits = 0` is the phase-only square kernel.
- `bits > 0` records low residue bits at both source and destination.
- This is a retraced smoke window, not a generated Lean matrix.
- A useful `A1` branch still needs larger-scale stability and a Banach norm.
