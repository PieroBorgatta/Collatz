# Phase 10 Working Index

Date: 2026-05-14

Status: operational index.  This file summarizes the Phase 10 artifacts
created so far and the current decision state.

## 1. Current Verdict

Gate 10.B is not closed.

Current finite diagnostics say:

```text
exact local constancy on the old PhaseState quotient is not supported.
```

The best current analytic branch is:

```text
hierarchical 2-adic cylinder refinement
+ labelled delta/return-signature kernel
+ distributional/Cesaro convergence target
+ explicit tail norm.
```

The current operator convention is:

```text
kernel first:       K(src,dst)
primary operator:   U_s on functions
dual mass operator: P_s^*
secondary only:     L_s/Ruelle
```

The fallback branch remains valid:

```text
finite-rank deterministic residue-cell certificates.
```

No spectral gap for an infinite operator has been proved.

## 2. Main Notes

| File | Purpose |
|---|---|
| `notes/phase10_reduced_core.md` | Short reduced core: A0/A1, errors `C_N/P_N/T_N`, minimal theorem skeleton, kill criteria |
| `notes/phase10_A0_theorem_skeleton.md` | Formal A0 conditional proposition and missing lemmas |
| `notes/phase10_operator_gate.md` | Main Phase 10 dossier and decision framework |
| `notes/phase10_master_report.md` | Consolidated Phase 10 entry point |
| `notes/phase10_gate10B_provisional_decision.md` | Gate 10.B provisional decision after diagnostics `88`-`98` |
| `notes/phase10_mixed_norm_candidate.md` | Candidate Banach pair and exact mixed-norm target |
| `notes/phase10_error_decomposition.md` | Named approximation-error budget for future diagnostics |
| `notes/phase10_collaborator_brief.md` | External-facing questions for a functional analyst/dynamicist |
| `notes/phase10_proof_obligations.md` | Missing hypotheses before LY/Hennion/Keller-Liverani |
| `notes/phase10_decision_tree.md` | Operational go/no-go and publication routing criteria |
| `notes/phase10_orientation.md` | Matrix orientation: row-source vs incoming/Ruelle |
| `notes/phase10_operator_choice.md` | Provisional choice: kernel first, `U_s` primary, `P_s^*` dual |
| `notes/phase10_candidate_operator.md` | Raw integer kernel and conditional `Z_2 x H` candidate |
| `notes/phase10_cylinder_stability_plan.md` | Design of the first high-bit stability diagnostic |
| `notes/phase10_cylinder_stability_results.md` | Results from scripts `88`-`98` |
| `notes/phase10_refined_state_candidate.md` | Five-bit refinement and residual `delta` obstruction |
| `notes/phase10_highbit_limit_conventions.md` | Possible meanings of `j -> infinity` |
| `notes/phase10_conditional_refined_kernel.md` | Conditional labelled kernel `K_{T,a,N}` |
| `notes/phase10_banach_implications_after_diagnostics.md` | Updated Banach-space ranking |
| `notes/phase10_norm_constants_from_diagnostics.md` | Ledger mapping diagnostics to possible norm constants |
| `notes/phase10_source_stratum_drift_ansatz.md` | Candidate source-stratum drift weight and kill criteria |
| `notes/phase10_literature_source_map.md` | Local/online source audit |
| `notes/phase10_finite_rank_fallback.md` | K16 fallback theorem candidate and K20 smoke preflight |
| `notes/phase10_finite_rank_note_outline.md` | Standalone finite-rank computational-note outline |
| `notes/phase10_repro_manifest.md` | Reproducibility commands and artifact map |

## 3. New Diagnostic Scripts

| Script | Role |
|---|---|
| `scripts/spectral_program/77_high_bit_tail_bound.py` | Shared high-bit trace helper; now exposes `next_t` for destination-refined probes |
| `scripts/spectral_program/88_cylinder_signature_stability.py` | High-bit cylinder stability for status/phase/delta/full signatures |
| `scripts/spectral_program/89_phase_split_inspector.py` | Inspect worst phase-unstable groups and simple coordinates |
| `scripts/spectral_program/90_refinement_coordinate_score.py` | Global coordinate scoring over selected obstruction groups |
| `scripts/spectral_program/91_refined_state_stability_probe.py` | Probe refined cells and compound coordinates |
| `scripts/spectral_program/92_delta_obstruction_summary.py` | Separate phase obstruction from `delta` obstruction |
| `scripts/spectral_program/93_delta_tail_weight.py` | Estimate weighted `delta` tails from script `88` distributions |
| `scripts/spectral_program/94_block_cauchy_summary.py` | Summarize adjacent-block TV drift for Cesaro/high-lift diagnostics |
| `scripts/spectral_program/95_bad_cell_stratification.py` | Stratify bad cells by source `v2`, odd residue, and hit phase |
| `scripts/spectral_program/96_stratum_weight_drift_probe.py` | Probe finite drift ratios for simple source-stratum weights |
| `scripts/spectral_program/97_truncated_label_block_tv.py` | Test block TV after clipping large `delta` labels |
| `scripts/spectral_program/98_bounded_label_excess.py` | Measure full-label TV excess over phase TV |
| `scripts/spectral_program/99_error_budget_summary.py` | Aggregate named error-budget constants from script `88` output |
| `scripts/spectral_program/100_z2_cylinder_oscillation.py` | Direct 2-adic child-cylinder oscillation diagnostic |
| `scripts/spectral_program/101_z2_oscillation_strata.py` | Stratify child-cylinder obstruction by source variables |
| `scripts/spectral_program/102_enriched_state_test.py` | Test whether isolating structural source components cleans the complement |
| `scripts/spectral_program/103_component_transition_budget.py` | Measure good/bad/terminal transition budgets for the two-component kernel |
| `scripts/spectral_program/104_component_block_cauchy.py` | Measure adjacent-block drift of the collapsed good/bad block kernel |
| `scripts/spectral_program/105_component_prefix_cauchy.py` | Measure prefix/Cesaro drift of the collapsed good/bad block kernel |
| `scripts/spectral_program/106_prefix_label_lift.py` | Measure the finite cost of lifting prefix component drift to retained full labels |
| `scripts/spectral_program/107_gate10b_closure_checks.py` | Verify finite Gate-10.B bookkeeping lemmas on script-`88` CSVs |
| `scripts/spectral_program/108_source_refinement_collapse.py` | Score source-state refinements by source-cell-to-key collapse error |
| `scripts/spectral_program/109_refined_prefix_cauchy.py` | Measure prefix drift after source-state refinement |
| `scripts/spectral_program/110_refined_square_probe.py` | Smoke-test square refined kernels with destination low residue bits |

## 4. Key Diagnostic Results

Base/refinement tests:

- `T = 10`, `j <= 128`: phase exact fraction `0.496579`;
- `T = 11`, `j <= 128`: phase exact fraction `0.517831`;
- strict coordinate scoring at both levels identifies `j mod 32` as the
  best simple destination-phase coordinate;
- `T = 15`, `j <= 32`: phase exact fraction `0.729584`, full exact
  fraction `0.662506`;
- `T = 16`, `j <= 8`: phase exact fraction `0.861542`, full exact
  fraction `0.804413`;
- `T = 16`, `j <= 8`: keeping `delta <= 4` leaves global weighted
  delta tail `0.00412187`; keeping `delta <= 5` leaves `0.000862882`;
  keeping `delta <= 8` leaves `0.00000574087`.
- `T = 15`, `j <= 32`: the corresponding global weighted delta tails
  are `0.0040648`, `0.000845196`, and `0.00000635292`.
- `T = 15`, block `0..15` vs `16..31`: full-signature adjacent-block
  TV has mean `0.0381069`, p95 `0.1875`, p99 `0.25`, and dominant-flip
  fraction `0.0124817`.
- `T = 15` block-doubling: full-signature TV decreases from block size
  `8` to `16` to `32`: mean `0.0462265 -> 0.0381069 -> 0.0310087`,
  p95 `0.25 -> 0.1875 -> 0.15625`.
- `T = 15`, block size `32`: clipping `delta > 5` leaves count-TV
  essentially unchanged relative to full labels: mean
  `0.0308437` vs `0.0310049`, p95 `0.15625` vs `0.15625`.
- `T = 15`, block size `32`: full-label excess over phase TV has mean
  `0.00791955`, p95 `0.0625`, p99 `0.09375`.
- `T = 16`, block `0..3` vs `4..7`: full-signature adjacent-block TV
  has mean `0.0507774`, p95 `0.25`, p99 `0.5`, and dominant-flip
  fraction `0.0238647`.
- `T = 16`, `j <= 8`: bad cells are structured by source strata;
  for example `v2=2, odd=3` has phase exact fraction `0.898926` but
  full exact fraction only `0.383301`.
- `T = 12`, `j <= 16`: identity weight has finite drift-ratio p95
  `0.25` and max `0.9375`; the best safe coarse source-stratum weight
  tested has p95 `0.207098` and max `0.979146`.
- `T = 15`, `j <= 16`: identity weight has finite drift-ratio p95
  `0.25` and max `0.96875`; nontrivial coarse weights improve p95 only
  by creating a small exceptional set with ratio `>= 1`.

Interpretation:

- five extra 2-adic bits help substantially;
- exact local constancy still degrades as prefixes grow;
- average majorities remain high;
- dominant adjacent-block flips remain relatively rare;
- `delta` remains a real obstruction for the weighted operator;
- the weighted `delta` tail is globally small on the tested window, but
  uniform source-cell tail control is not automatic;
- majority stability and distributional TV drift must be tracked
  separately; dominant labels can stay fixed while their masses move.
- fixed-`T=15` block-doubling is compatible with, but does not prove, a
  Cesaro/mixed-norm approximation program.
- large-`delta` tail is not the only block-Cauchy obstruction; bounded
  return-label variation remains visible.
- bounded return-label variation is smaller than phase movement on the
  tested window, but still needs its own error term.
- `T = 15`, `j <= 64`, block size `32`: the aggregated error-budget
  report gives `DeltaTail_global(5) = 0.000830424`,
  `DeltaTail_local_p95(5) = 0.027027`, `A_phase_block` p95 `0.125`,
  and full `A_label_bounded` p95 `0.0625`.
- The finite row-TV bridge gives weak averaged proxies on the same
  dataset: `A_phase_block` `2*mean = 0.0461707`, full label-TV
  `2*mean = 0.0620098`, and full `A_label_bounded`
  `2*mean = 0.0158391`.  The corresponding sup proxies are still large.
- Re-running the script-`99` row-TV bridge at fixed `T = 15` gives a
  decreasing weak-proxy chain for block sizes `8 -> 16 -> 32`: full
  label-TV `2*mean = 0.0924482 -> 0.0762047 -> 0.0620098`; the sup
  proxy remains large, `1.5 -> 1.0 -> 0.75`.
- Source averaging is not yet clean: script `88` averages over `(r,h)`
  low-bit cells, and at `T = 15`, `j = 16,32,64`, exactly `8/131072`
  such cells have two `source_phase` states.  Also, adjacent high-bit
  blocks in ordinary `j` order are not automatically 2-adic martingale
  cylinders.
- A first actual 2-adic child-cylinder diagnostic
  (`collatz_100_T15_d3_tail2_z2_cylinder_oscillation.md`) is negative
  for the naive martingale story: full-label mean TV is
  `0.0526182 -> 0.0544645 -> 0.0575895 -> 0.0606241` over depths
  `0 -> 3`, with p95 reaching `0.5` at depth `3`.
- A higher-tail repeat
  (`collatz_100_T15_d2_tail4_z2_cylinder_oscillation.md`) still does
  not show full-label contraction: `0.0486132 -> 0.0487704 ->
  0.0509391` over depths `0 -> 2`.
- Stratifying the depth-`2` 2-adic obstruction
  (`collatz_101_T15_d2_tail3_z2_oscillation_strata_report.md`) shows
  that full-over-phase excess is concentrated: `source_v2_odd = 2|3`
  has mass `0.0625`, mean excess `0.120621`, and contribution
  `0.456409`.
- A lighter `T=16` stratification preserves the same signal:
  `source_v2_odd = 2|3` has mass `0.0625`, mean excess `0.152130`, and
  contribution `0.492200`.
- The direct interaction-weight drift probe on that stratum is not a
  safe uniform drift improvement: coefficient `1` lowers p95 to
  `0.155199` but creates max `2.63334` and fraction `>= 1` equal to
  `0.000366211`.
- The worst coefficient-`1` exceptional cells are not sourced from
  `2|3`; the largest comes from `v2=1|odd=1`, suggesting the weight
  shifts the problem to incoming transitions.
- The enriched-state split test is more promising: the component
  `odd = 3 and v2 in {0,2}` has mass `0.3125`, captures `0.742956`
  of full-over-phase excess at `T15` depth `2` and `0.767081` at `T16`
  depth `1`, and leaves complement p95 `0` in both tests.
- The two-component transition-budget test over `0 < t < 2^21` shows
  that the same split is strongly coupled, not a tiny discarded error:
  good row budget `0.017746872`, bad row budget `0.058940144`, and
  `G -> B` weighted fraction among good returns `0.30797407`.
- Alternative bad-rule checks support the current middle split: the
  narrow `v2=2 and odd=3` rule is a hot core with bad row budget
  `0.20995882`, while the broad `odd=3 or v2=2` rule marks about
  `0.5625` of sources as bad.
- Component block-Cauchy drift decreases at fixed `T=15` over block
  sizes `8 -> 16 -> 32`: weighted row `L1` mean
  `0.012046521 -> 0.0095367816 -> 0.0074155295`.
- But the `B=16`, `j=64` multipair check worsens over adjacent pairs:
  `0.009535642 -> 0.013903232 -> 0.018206286`.  This blocks a naive
  ordinary-block Cauchy claim.
- The prefix/Cesaro component test is more favorable:
  `16->32` mean `0.004767821`, `32->64` mean `0.0037076395`,
  `64->128` mean `0.0027624646`.
- The prefix label-lift test shows a real retained-label cost above the
  good/bad component kernel: full-label `L1` mean `0.0075584849` versus
  component `L1` mean `0.0042377302`, with label-excess mean
  `0.0033207547` and p95 `0.017578125`.  The `delta <= 5` cutoff gives
  essentially the same excess, so this is not mainly a large-delta
  tail.
- On the larger `64->128` prefix comparison, label-excess improves to
  mean `0.0029977961`, p95 `0.015625`, and p99 `0.03125`, but remains a
  separate retained-label error term.
- The finite Gate-10.B closure check on `T15_j64_128_L5` verifies:
  retained source cells `131064/131072`, source mean error coefficient
  `0.0001220703125`, zero row-source identity residuals, zero
  component/phase/label projection violations, phase `L1` mean
  `0.0045024297`, label `L1` mean `0.005743653`, and tail-weight means
  about `2.54e-05`.
- The current phase-only prefix trend is decreasing on tested data:
  `16->32 = 0.0066310638`, `32->64 = 0.0055465954`,
  `64->128 = 0.0045024297`.  This is finite evidence, not a Cauchy
  theorem.
- The no-cutoff repeat gives nearly the same phase trend:
  `16->32 = 0.0066438334`, `32->64 = 0.0055544859`,
  `64->128 = 0.0045072525`, so the current trend is not mainly a
  `delta > 5` truncation artifact.
- H4 is only CSV-closed for the new `T=15` phase-prefix diagnostics:
  `K16S16KDeterministicCW` is a separate `Fin 37` fallback certificate,
  while the existing `PhaseState` Lean imports are `T=10` objects
  (`T10CriticalSymbolic`, `T10J32HighBitTail`).  A generated Lean import
  for the `T=15` script-`107` kernels is still missing.
- More seriously, source-cell to source-`PhaseState` collapse is not
  small at tested scales: means are `0.055610515`, `0.054357070`,
  `0.052910359`, `0.051512269` for `j=16,32,64,128`, with p95 near
  `0.28`.  Thus `PhaseState` is currently an averaged quotient, not an
  exact projection of the source-cell kernel.
- Script `108` shows that low source-residue refinement helps:
  at `j=128`, `PhaseState + r mod 2^10` has collapse mean
  `0.020415877`, `r mod 2^11` has `0.018202554`, and `r mod 2^12`
  has `0.015742233`.  This is promising finite evidence, but the finest
  case has only about `8` cells/key and large worst rows, so it is not a
  proof of a natural infinite quotient.
- Script `109` shows the opposite side of the same tradeoff.  For
  `64->128`, `delta<=5`, source-cell-weighted prefix drift is smallest
  for bare `PhaseState` (`0.000200738`), while refined keys drift more:
  `r mod 2^10` gives `0.001584947`, `r mod 2^11` gives
  `0.002104687`, and `r mod 2^12` gives `0.002608004`.  The overfit
  `source_cell` baseline is `0.004502430`.  Thus refinement improves
  source collapse but moves the kernel toward the less stable
  cell-level baseline.
- Across `16->32->64`, the same refined-prefix drift decreases for each
  selected key: `r mod 2^10` goes `0.003021663 -> 0.002156255`, while
  `source_cell` goes `0.006631064 -> 0.005546595`.  This is finite
  trend evidence only, not a Cauchy theorem.
- The analytic branch is now split into `A0` and `A1`.  `A0` keeps the
  existing `PhaseState`/`TransferMatrix V` object and must carry or prove
  away the source-collapse error.  `A1` uses
  `PhaseState + r mod 2^10`; it is the best current diagnostic
  refinement, but it is not yet a square spectral operator because the
  CSVs do not record a destination low-residue coordinate.
- Script `110` adds a retraced smoke square kernel
  `(PhaseState,t mod 2^b) -> (PhaseState,next_t mod 2^b)`.  At `T=12`,
  `16->32->64->128`, the weighted drift for `b=10` decreases
  `0.015208335 -> 0.013556191 -> 0.012909874`, but remains much larger
  than phase-only drift
  `0.001386190 -> 0.001097048 -> 0.000647069`.  This keeps `A1` alive
  as a research branch but argues against switching the main `FULL`
  story to it prematurely.
- source-stratum structure may matter for a future drift/tail norm.
- the first source-stratum drift probe is not falsified, but remains a
  weak side channel; the harder `T15_j16` probe is negative for the
  naive three-parameter weight family.

## 5. Fallback Status

Production K16:

- Lean file: `lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean`;
- exact max ratio:

```text
90833233962213 / 129559208330288 < 3/4.
```

- `lake build CollatzShadowing.Generated.K16S16KDeterministicCW`
  succeeds.

K20 smoke preflight:

- sampled smoke SCC largest component: `5802` nodes;
- deterministic smoke `(K,b)` matrix: `38` states;
- exact smoke CW ratio:

```text
42001755821431 / 62996587868160 < 3/4.
```

This is not a production K20 theorem.

## 6. Verified Commands

Python compile:

```text
python3 -m py_compile \
  scripts/spectral_program/77_high_bit_tail_bound.py \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  scripts/spectral_program/89_phase_split_inspector.py \
  scripts/spectral_program/90_refinement_coordinate_score.py \
  scripts/spectral_program/91_refined_state_stability_probe.py \
  scripts/spectral_program/92_delta_obstruction_summary.py \
  scripts/spectral_program/93_delta_tail_weight.py \
  scripts/spectral_program/94_block_cauchy_summary.py \
  scripts/spectral_program/95_bad_cell_stratification.py \
  scripts/spectral_program/96_stratum_weight_drift_probe.py \
  scripts/spectral_program/97_truncated_label_block_tv.py \
  scripts/spectral_program/98_bounded_label_excess.py \
  scripts/spectral_program/99_error_budget_summary.py \
  scripts/spectral_program/100_z2_cylinder_oscillation.py \
  scripts/spectral_program/101_z2_oscillation_strata.py \
  scripts/spectral_program/102_enriched_state_test.py \
  scripts/spectral_program/103_component_transition_budget.py \
  scripts/spectral_program/104_component_block_cauchy.py \
  scripts/spectral_program/105_component_prefix_cauchy.py \
  scripts/spectral_program/106_prefix_label_lift.py \
  scripts/spectral_program/107_gate10b_closure_checks.py \
  scripts/spectral_program/108_source_refinement_collapse.py \
  scripts/spectral_program/109_refined_prefix_cauchy.py \
  scripts/spectral_program/110_refined_square_probe.py
```

Lean:

```text
lake build CollatzShadowing.Generated.K16S16KDeterministicCW
```

K20 smoke CW:

```text
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k20_smoke_residue_K_cw_certificate.json
```

Phantom-taxonomy script compile:

```text
python3 -m py_compile \
  scripts/phantom_taxonomy/deterministic_residue_transfer.py \
  scripts/phantom_taxonomy/scc_cw_certificate.py \
  scripts/phantom_taxonomy/scc_report.py \
  scripts/phantom_taxonomy/orbit_harness.py
```

## 7. Next Actions

1. Keep `A0` as the branch for existing `FULL`/Lean objects; do not
   claim it is an exact projection.
2. Prepare the data-generator change needed for `A1`: record a
   destination refinement compatible with `r mod 2^10`, then test whether
   it yields a square refined kernel.
3. Define the finite weak norm for `A0` and, separately, for `A1`;
   state the exact source averaging measure in both cases.
4. Keep source-collapse error, refined-prefix drift, global weighted
   `delta` tail, weighted-local source-cell tail,
   adjacent-block distributional TV, and block coupling as separate
   constants.
5. Test one more prefix scale only after the chosen norm says which
   alphabet and which error constant it feeds.
6. For fallback, run a production K20 sampled SCC only after declaring
   the sample scope and comparison criterion.
7. Do not compute or advertise new spectral radii until the operator
   and projection meaning are fixed.
