# Projected Residual Lift Test

Status: finite diagnostic output only.  This report measures signed
residuals after removing the destination-v2 low mode with explicit
fiber lifts.  It does not prove Lasota-Yorke, Hennion,
Keller-Liverani, a spectral gap, or Collatz.

## Inputs

- T values: `15`
- max depth: `2`
- tail bits: `3`
- global lift: `False`
- source lift: `False`
- source refine bits: `0,2,4,6,8`

## Trace Meta

| T | max j | source groups | child-pair samples | global lift | source lift | source refine bits |
|---:|---:|---:|---:|---|---|---|
| 15 | 64 | 131072 | 917504 | `False` | `False` | `0,2,4,6,8` |

## Residual Summary

| depth | metric | mean | p95 | max | relative mean |
|---:|---|---:|---:|---:|---:|
| 0 | `phase_tv` | 0.0425999 | 0.15625 | 1 | 1 |
| 0 | `dst_v2_tv` | 0.0376102 | 0.15625 | 1 | 0.882872 |
| 0 | `proxy_residual` | 0.00498962 | 0.03125 | 1 | 0.117128 |
| 0 | `pair_pooled_residual` | 0.00730881 | 0.0322581 | 1 | 0.171569 |
| 0 | `uniform_residual` | 0.0424853 | 0.15625 | 1.50781 | 0.99731 |
| 0 | `source_refined_b0_residual` | 0.0163037 | 0.0648543 | 1 | 0.382716 |
| 0 | `source_refined_b2_residual` | 0.0163037 | 0.0648543 | 1 | 0.382716 |
| 0 | `source_refined_b4_residual` | 0.0163303 | 0.0656114 | 1.00017 | 0.383342 |
| 0 | `source_refined_b6_residual` | 0.0163606 | 0.0694846 | 1.00135 | 0.384053 |
| 0 | `source_refined_b8_residual` | 0.0162752 | 0.0702851 | 1.00301 | 0.382048 |
| 1 | `phase_tv` | 0.0418446 | 0.1875 | 1 | 1 |
| 1 | `dst_v2_tv` | 0.0373451 | 0.1875 | 1 | 0.892471 |
| 1 | `proxy_residual` | 0.0044995 | 0 | 1 | 0.107529 |
| 1 | `pair_pooled_residual` | 0.00581871 | 0.03125 | 1 | 0.139055 |
| 1 | `uniform_residual` | 0.0423781 | 0.203125 | 1.52344 | 1.01275 |
| 1 | `source_refined_b0_residual` | 0.0182418 | 0.0941164 | 1.00114 | 0.435941 |
| 1 | `source_refined_b2_residual` | 0.0182418 | 0.0941164 | 1.00114 | 0.435941 |
| 1 | `source_refined_b4_residual` | 0.0182612 | 0.0941663 | 1.00059 | 0.436405 |
| 1 | `source_refined_b6_residual` | 0.0182636 | 0.0941317 | 1.00212 | 0.436463 |
| 1 | `source_refined_b8_residual` | 0.0181501 | 0.094112 | 1.00201 | 0.433751 |
| 2 | `phase_tv` | 0.0410719 | 0.25 | 1 | 1 |
| 2 | `dst_v2_tv` | 0.0372753 | 0.25 | 1 | 0.907563 |
| 2 | `proxy_residual` | 0.00379658 | 0 | 1 | 0.0924374 |
| 2 | `pair_pooled_residual` | 0.00440467 | 0 | 1 | 0.107243 |
| 2 | `uniform_residual` | 0.041697 | 0.21875 | 1.53125 | 1.01522 |
| 2 | `source_refined_b0_residual` | 0.0197842 | 0.125648 | 1.0031 | 0.481697 |
| 2 | `source_refined_b2_residual` | 0.0197842 | 0.125648 | 1.0031 | 0.481697 |
| 2 | `source_refined_b4_residual` | 0.0197924 | 0.125501 | 1.00342 | 0.481896 |
| 2 | `source_refined_b6_residual` | 0.0197697 | 0.12528 | 1.00454 | 0.481343 |
| 2 | `source_refined_b8_residual` | 0.0196251 | 0.125 | 1.01513 | 0.477823 |

## Reading

`proxy_residual` is the script-115 quantity `TV_phase - TV_dst_v2`.
`pair_pooled_residual` is an optimistic signed residual using a
pair-dependent lift inside each dst_v2 fiber.  `global_pooled`
uses one lift per depth.  `source_pooled` uses one lift per depth
and finite source PhaseState.  `uniform_residual` uses a fixed
uniform lift and is a pessimistic sanity check.  If only the
pair-pooled residual is small, the repair is not yet canonical.
If the source-pooled residual is small, a finite source-conditioned
low-mode operator becomes a plausible next target.  The
`source_refined_b{k}` rows test the same idea after adding
`r mod 2^k` to the finite source key.

