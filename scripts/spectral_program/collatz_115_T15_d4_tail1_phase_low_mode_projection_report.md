# Phase Low-Mode Projection Test

Status: finite diagnostic output only.  This report tests whether
phase martingale variation is mostly captured by low-dimensional
destination coordinates.  It does not prove Lasota-Yorke, Hennion,
Keller-Liverani, a spectral gap, or Collatz.

## Inputs

- T values: `15`
- max depth: `4`
- tail bits: `1`
- odd bits: `2`
- hit bits: `2`
- v2 cap: `13`

## Trace Meta

| T | max j | source groups | child-pair samples |
|---:|---:|---:|---:|
| 15 | 64 | 131072 | 4063232 |

## Low-Mode Capture

| depth | mode | mode mean TV | phase mean TV | residual mean | residual p95 | capture |
|---:|---|---:|---:|---:|---:|---:|
| 0 | `dst_v2_odd` | 0.0425999 | 0.0425999 | 0 | 0 | 1 |
| 0 | `phase` | 0.0425999 | 0.0425999 | 0 | 0 | 1 |
| 0 | `dst_v2` | 0.0376102 | 0.0425999 | 0.00498962 | 0.03125 | 0.882872 |
| 0 | `dst_v2_h` | 0.0376102 | 0.0425999 | 0.00498962 | 0.03125 | 0.882872 |
| 0 | `dst_odd` | 0.0335419 | 0.0425999 | 0.009058 | 0.03125 | 0.78737 |
| 0 | `dst_odd_h` | 0.0335419 | 0.0425999 | 0.009058 | 0.03125 | 0.78737 |
| 0 | `status` | 0.028598 | 0.0425999 | 0.0140018 | 0.0625 | 0.671317 |
| 0 | `dst_h` | 0.028598 | 0.0425999 | 0.0140018 | 0.0625 | 0.671317 |
| 1 | `dst_v2_odd` | 0.0418446 | 0.0418446 | 0 | 0 | 1 |
| 1 | `phase` | 0.0418446 | 0.0418446 | 0 | 0 | 1 |
| 1 | `dst_v2` | 0.0373451 | 0.0418446 | 0.0044995 | 0 | 0.892471 |
| 1 | `dst_v2_h` | 0.0373451 | 0.0418446 | 0.0044995 | 0 | 0.892471 |
| 1 | `dst_odd` | 0.0337278 | 0.0418446 | 0.00811679 | 0.0625 | 0.806025 |
| 1 | `dst_odd_h` | 0.0337278 | 0.0418446 | 0.00811679 | 0.0625 | 0.806025 |
| 1 | `status` | 0.0285217 | 0.0418446 | 0.0133228 | 0.0625 | 0.681611 |
| 1 | `dst_h` | 0.0285217 | 0.0418446 | 0.0133228 | 0.0625 | 0.681611 |
| 2 | `dst_v2_odd` | 0.0410719 | 0.0410719 | 0 | 0 | 1 |
| 2 | `phase` | 0.0410719 | 0.0410719 | 0 | 0 | 1 |
| 2 | `dst_v2` | 0.0372753 | 0.0410719 | 0.00379658 | 0 | 0.907563 |
| 2 | `dst_v2_h` | 0.0372753 | 0.0410719 | 0.00379658 | 0 | 0.907563 |
| 2 | `dst_odd` | 0.0343704 | 0.0410719 | 0.00670147 | 0 | 0.836836 |
| 2 | `dst_odd_h` | 0.0343704 | 0.0410719 | 0.00670147 | 0 | 0.836836 |
| 2 | `status` | 0.0292443 | 0.0410719 | 0.0118276 | 0 | 0.712027 |
| 2 | `dst_h` | 0.0292443 | 0.0410719 | 0.0118276 | 0 | 0.712027 |
| 3 | `dst_v2_odd` | 0.0408087 | 0.0408087 | 0 | 0 | 1 |
| 3 | `phase` | 0.0408087 | 0.0408087 | 0 | 0 | 1 |
| 3 | `dst_v2` | 0.0377636 | 0.0408087 | 0.00304508 | 0 | 0.925382 |
| 3 | `dst_v2_h` | 0.0377636 | 0.0408087 | 0.00304508 | 0 | 0.925382 |
| 3 | `dst_odd` | 0.035758 | 0.0408087 | 0.00505066 | 0 | 0.876236 |
| 3 | `dst_odd_h` | 0.035758 | 0.0408087 | 0.00505066 | 0 | 0.876236 |
| 3 | `status` | 0.031312 | 0.0408087 | 0.00949669 | 0 | 0.767288 |
| 3 | `dst_h` | 0.031312 | 0.0408087 | 0.00949669 | 0 | 0.767288 |
| 4 | `dst_v2_odd` | 0.0389357 | 0.0389357 | 0 | 0 | 1 |
| 4 | `phase` | 0.0389357 | 0.0389357 | 0 | 0 | 1 |
| 4 | `dst_v2` | 0.0363913 | 0.0389357 | 0.0025444 | 0 | 0.934651 |
| 4 | `dst_v2_h` | 0.0363913 | 0.0389357 | 0.0025444 | 0 | 0.934651 |
| 4 | `dst_odd` | 0.0351028 | 0.0389357 | 0.00383282 | 0 | 0.90156 |
| 4 | `dst_odd_h` | 0.0351028 | 0.0389357 | 0.00383282 | 0 | 0.90156 |
| 4 | `status` | 0.0308466 | 0.0389357 | 0.00808907 | 0 | 0.792245 |
| 4 | `dst_h` | 0.0308466 | 0.0389357 | 0.00808907 | 0 | 0.792245 |

## Best Proper Low Mode

The table excludes `phase` and `dst_v2_odd`, since `dst_v2_odd`
coincides with the full phase variation on the tested windows.

| depth | best mode | capture | residual mean | residual p95 |
|---:|---|---:|---:|---:|
| 0 | `dst_v2` | 0.882872 | 0.00498962 | 0.03125 |
| 1 | `dst_v2` | 0.892471 | 0.0044995 | 0 |
| 2 | `dst_v2` | 0.907563 | 0.00379658 | 0 |
| 3 | `dst_v2` | 0.925382 | 0.00304508 | 0 |
| 4 | `dst_v2` | 0.934651 | 0.0025444 | 0 |

## Reading

A successful finite/low-mode repair would require some low mode to
capture most phase variation and leave a small residual.  If the
best low modes still leave residuals comparable to the original
phase TV, then a finite-rank projection does not repair LY for the
current phase quotient.

On the current tested windows, the best proper mode is usually
`dst_v2` or the equivalent `dst_v2_h`.  This is a plausible repair
signal only if the residual after removing the `dst_v2` marginal
continues to decay under deeper 2-adic refinement.  The diagnostic
is not a projection theorem: a proof would still need a canonical
projection/lift and an operator-norm estimate for the residual.

