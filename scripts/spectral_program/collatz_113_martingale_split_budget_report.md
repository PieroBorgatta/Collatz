# Martingale Split Budget

Status: finite diagnostic output only.  This report separates the
available child-cylinder martingale proxies into phase variation,
full-over-phase label excess, and status/loss variation.  It does
not prove Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap,
or Collatz.

Structural candidate used for label-excess isolation: `source_odd_3_or_v2_2`.

## Global Split

| tag | depth | phase mean | label-excess mean | status/loss mean | full mean | split/full |
|---|---:|---:|---:|---:|---:|---:|
| `T15_d2_tail3` | 0 | 0.0425999 | 0.0100183 | 0.028598 | 0.0526182 | 1.5435 |
| `T15_d2_tail3` | 1 | 0.0418446 | 0.01262 | 0.0285217 | 0.0544645 | 1.52368 |
| `T15_d2_tail3` | 2 | 0.0410719 | 0.0165176 | 0.0292443 | 0.0575895 | 1.50781 |
| `T16_d1_tail2` | 0 | 0.0449772 | 0.0161743 | 0.0320451 | 0.0611515 | 1.52403 |
| `T16_d1_tail2` | 1 | 0.0443541 | 0.0193176 | 0.0337435 | 0.0636717 | 1.52996 |

The split is intentionally conservative: phase, label-excess, and
status/loss are not independent norms, and their sum is not claimed
to be sharp.  It is a bookkeeping device for deciding what a serious
strong norm would have to control.

## Structural Label-Excess Isolation

| tag | depth | selected mass | selected contribution | complement mean | complement p95 | complement contribution |
|---|---:|---:|---:|---:|---:|---:|
| `T15_d2_tail3` | 0 | 0.562469 | 0.764112 | 0.00540123 | 0.03125 | 0.235888 |
| `T15_d2_tail3` | 1 | 0.562469 | 0.768911 | 0.00666545 | 0.0625 | 0.231089 |
| `T15_d2_tail3` | 2 | 0.562469 | 0.808025 | 0.00724742 | 0 | 0.191975 |
| `T16_d1_tail2` | 0 | 0.562485 | 0.815684 | 0.0068139 | 0 | 0.184316 |
| `T16_d1_tail2` | 1 | 0.562485 | 0.829186 | 0.00754194 | 0 | 0.170814 |

## Reading

The phase component is large and nearly flat on the current depths,
so exponential martingale weights are not justified by the present
data.  The label-excess component is more promising: a single
structural candidate captures about 80 percent of full-over-phase
excess in both available T15/T16 reports, with complement p95 equal
to zero in the strongest rows.  This supports an enriched or
decomposed strong norm, not a plain full-label martingale BV norm.

Next falsification target: rerun the child-cylinder diagnostic at
larger depth/tail windows and require the phase component or the
post-enrichment complement to show real decay.  If both remain
flat, the Hennion/Keller-Liverani route should remain paused.
