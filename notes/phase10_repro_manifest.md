# Phase 10 Reproducibility Manifest

Date: 2026-05-14

Status: operational manifest.  This records how to reproduce the current
Phase-10 diagnostic artifacts.  It is not a proof log and does not
upgrade diagnostics into theorems.

## 1. Workspace

Main Lean workspace:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
```

Project root used by scripts and notes:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
```

Python environment for Phase-10 spectral scripts:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/.venv/bin/python
```

The active project virtual environment already contains the scientific
dependencies required transitively by the spectral helper modules:

```text
numpy 2.4.4
scipy 1.17.1
```

Do not use macOS/system `python3` for scripts that import
`75_critical_symbolic_operator.py` or `53_lift_phantom_cycles.py`; that
interpreter may not have `numpy`/`scipy`.  If the venv is unavailable,
use the already documented `uv run --with numpy --with scipy python ...`
form instead of installing packages globally.

## 2. Important Warning About Script 88 Outputs

Script `88_cylinder_signature_stability.py` writes shared files:

```text
scripts/spectral_program/collatz_88_cylinder_group_summary.csv
scripts/spectral_program/collatz_88_signature_distribution.csv
scripts/spectral_program/collatz_88_block_drift.csv
scripts/spectral_program/collatz_88_decision_summary.md
```

These files are overwritten by an untagged script-`88` run.  The script
now supports `--output-tag`, which writes tagged copies without
overwriting the active files.

Current active `88` CSVs correspond to the `T15_B32_j64` diagnostic:

```text
T = 15,
j_counts = 32,64,
block_size = 32.
```

Archived copies of the script-`88` CSVs now exist for:

```text
scripts/spectral_program/collatz_88_T15_B8_j16_*.csv
scripts/spectral_program/collatz_88_T15_B16_j32_*.csv
scripts/spectral_program/collatz_88_T15_B32_j64_*.csv
scripts/spectral_program/collatz_88_T15_B16_j64_multipair_*.csv
scripts/spectral_program/collatz_88_T15_B64_j128_prefix_*.csv
```

## 3. Current Active Error-Budget Run

Command:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/99_error_budget_summary.py \
  --T 15 \
  --prefix-j-count 64 \
  --block-size 32 \
  --cutoffs 2,3,4,5,8 \
  --output-tag T15_B32_j64
```

Outputs:

```text
scripts/spectral_program/collatz_99_T15_B32_j64_error_budget_summary.md
scripts/spectral_program/collatz_99_T15_B32_j64_error_budget_summary.csv
```

Headline finite proxies:

```text
DeltaTail_global(5)      = 0.000830424
DeltaTail_local_p95(5)   = 0.027027
DeltaTail_local_max(5)   = 1
A_phase_block p95        = 0.125
full A_label_bounded p95 = 0.0625
full label-TV weak L1    = 0.0620098
full label-TV sup proxy  = 0.75
```

Interpretation: finite proxies only; no operator-norm bound and no
projection theorem.

Auxiliary source-cell consistency check, run directly from the
definition of `state_of(t,h)`:

```text
T = 15, j = 16,32,64:
mixed source-phase low-bit cells = 8 / 131072.
```

These are finite source-partition diagnostics, not theorem-level
measure-identification statements.

## 4. Diagnostic Script Verification

Lean weak bridge:

```text
cd lean
lake build CollatzShadowing.WeakBridge
lake build CollatzShadowing.Generated.A0ReturnBranches
lake build CollatzShadowing
```

Status: passes.  Latest checked A0 generated-data build:
`lake build CollatzShadowing.Generated.A0ReturnBranches` completed
successfully with `3286` jobs after importing the label-gate,
high-lift-modulus, high-lift-continuation, intermediate-label split, and
multi-probe/refined-continuation/target-visibility-structure summary
fields and the derived split-resolution certificate, now factored through
`WeakBridge.LabelSplit.SummaryCounters`, plus the finite return-sample
partition summary through `WeakBridge.LabelSplit.ReturnPartitionSummary`
(covered return samples `11752/11752`, zero coverage failures), and the
finite outcome decomposition through `WeakBridge.LabelSplit.OutcomeSummary`
(`11752` covered return samples, `101628` drop samples, `844`
valuation-tail samples, and `16` step-tail samples account for `114240`
total prefix samples; latest run `82s`).  Latest checked aggregate build:
`lake build CollatzShadowing` completed successfully with `3350` jobs
(latest run `92s`).  The conditional Collatz bridge
`CollatzShadowing.CollatzBridge` also builds after adding the elementary
accelerated/classical simulation lemmas, `acceleratedToClassicalBridge`,
`BranchDescentModel`, `GlobalDescentCover`,
`uniformStrictDescent_of_branchDescentModel`, and the packaged theorems
`classicalCollatz_of_branchDescentModel` and
`classicalCollatz_of_globalDescentCover`.  It also builds with the
concrete finite-model loss audit taxonomy `FiniteModelLossKind`,
`FiniteModelCoverClass`, `CoverClassStatus`, and
`classicalCollatz_of_finiteModelGlobalCover`, plus the witness constructors
`strictDescentWitnessOfIterate` and `strictDescentWitnessOfOneStep`
and the working interface `FiniteModelCoverSpec` with
`classicalCollatz_of_finiteModelCoverSpec`.  The same bridge now includes
the propositional form `HasStrictDescent` and the equivalence
`hasStrictDescent_iff_nonempty_witness`, plus `DirectDropSound` and
`directDropWitnessOfSound` for packaging direct-drop predicates into the
global-cover witness interface.  Direct drops can now be recorded in the
step-indexed form `DirectDropAt`, with
`hasStrictDescent_of_directDropAt` feeding the existential strict-descent
form (`3291` jobs; latest run `98s`).
Latest aggregate build after these additions: `lake build
CollatzShadowing` completed with `3350` jobs (latest run `78s`).

Compile check:

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
  scripts/spectral_program/110_refined_square_probe.py \
  scripts/spectral_program/111_refined_square_key_drift_inspector.py \
  scripts/spectral_program/112_family_weighted_norm_probe.py \
  scripts/spectral_program/113_A0_decay_law_probe.py \
  scripts/spectral_program/114_A0_high_v2_tail_split.py \
  scripts/spectral_program/115_A0_decomposition_decay_probe.py \
  scripts/spectral_program/117_A0_v2_tail_formula.py \
  scripts/spectral_program/118_A0_low_v2_phase_decay_probe.py \
  scripts/spectral_program/119_A0_low_v2_return_depth_probe.py \
  scripts/spectral_program/120_A0_dependency_depth_probe.py \
  scripts/spectral_program/121_A0_walsh_haar_probe.py \
  scripts/spectral_program/122_A0_top_haar_decay_summary.py \
  scripts/spectral_program/123_A0_bounded_periodicity_probe.py \
  scripts/spectral_program/124_A0_tail_grid_probe.py \
  scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py \
  scripts/spectral_program/126_A0_return_branch_affine_probe.py
```

Current status: passes.

## 5. Main Tagged Diagnostic Reports

Delta tail reports:

```text
scripts/spectral_program/collatz_93_T15_j32_delta_tail_weight_report.md
scripts/spectral_program/collatz_93_T16_j8_delta_tail_weight_report.md
```

Block-Cauchy reports:

```text
scripts/spectral_program/collatz_94_T15_B8_j16_block_cauchy_report.md
scripts/spectral_program/collatz_94_T15_j32_block_cauchy_report.md
scripts/spectral_program/collatz_94_T15_B32_j64_block_cauchy_report.md
scripts/spectral_program/collatz_94_T16_j8_block_cauchy_report.md
```

Bad-cell and drift reports:

```text
scripts/spectral_program/collatz_95_T16_j8_bad_cell_stratification_report.md
scripts/spectral_program/collatz_96_T12_j16_stratum_weight_drift_report.md
scripts/spectral_program/collatz_96_T15_j16_stratum_weight_drift_report.md
```

Label and error-budget reports:

```text
scripts/spectral_program/collatz_97_T15_B32_j64_truncated_label_block_tv_report.md
scripts/spectral_program/collatz_98_T15_B32_j64_bounded_label_excess_report.md
scripts/spectral_program/collatz_99_T15_B8_j16_error_budget_summary.md
scripts/spectral_program/collatz_99_T15_B16_j32_error_budget_summary.md
scripts/spectral_program/collatz_99_T15_B32_j64_error_budget_summary.md
scripts/spectral_program/collatz_100_T15_d3_tail2_z2_cylinder_oscillation.md
scripts/spectral_program/collatz_100_T15_d2_tail4_z2_cylinder_oscillation.md
scripts/spectral_program/collatz_101_T15_d2_tail3_z2_oscillation_strata_report.md
scripts/spectral_program/collatz_101_T16_d1_tail2_z2_oscillation_strata_report.md
scripts/spectral_program/collatz_96_T15_j16_interaction_only_stratum_weight_drift_report.md
scripts/spectral_program/collatz_96_T15_j16_interaction_c1_stratum_weight_drift_report.md
scripts/spectral_program/collatz_102_T15_d2_tail3_enriched_state_test_report.md
scripts/spectral_program/collatz_102_T16_d1_tail2_enriched_state_test_report.md
scripts/spectral_program/collatz_103_T15_j32_component_transition_budget_report.md
scripts/spectral_program/collatz_103_T15_j64_component_transition_budget_report.md
scripts/spectral_program/collatz_103_T15_j32_v2_2_odd3_component_transition_budget_report.md
scripts/spectral_program/collatz_103_T15_j32_odd3_or_v2_2_component_transition_budget_report.md
scripts/spectral_program/collatz_104_T15_B8_j16_component_block_cauchy_report.md
scripts/spectral_program/collatz_104_T15_B16_j32_component_block_cauchy_report.md
scripts/spectral_program/collatz_104_T15_B32_j64_component_block_cauchy_report.md
scripts/spectral_program/collatz_104_T15_B16_j64_multipair_component_block_cauchy_report.md
scripts/spectral_program/collatz_104_T15_B64_j128_prefix_component_block_cauchy_report.md
scripts/spectral_program/collatz_105_T15_j16_32_64_multipair_component_prefix_cauchy_report.md
scripts/spectral_program/collatz_105_T15_j64_128_prefix_component_prefix_cauchy_report.md
scripts/spectral_program/collatz_106_T15_j16_32_64_multipair_full_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j16_32_64_multipair_L5_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j16_32_64_v2_2_odd3_full_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j16_32_64_odd3_or_v2_2_full_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j64_128_prefix_full_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j64_128_prefix_L5_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j64_128_v2_2_odd3_full_prefix_label_lift_report.md
scripts/spectral_program/collatz_106_T15_j64_128_odd3_or_v2_2_full_prefix_label_lift_report.md
scripts/spectral_program/collatz_107_T15_j64_128_L5_gate10b_closure_checks_report.md
scripts/spectral_program/collatz_107_T15_j16_32_64_L5_gate10b_closure_checks_report.md
scripts/spectral_program/collatz_107_T15_j64_128_full_gate10b_closure_checks_report.md
scripts/spectral_program/collatz_107_T15_j16_32_64_full_gate10b_closure_checks_report.md
scripts/spectral_program/collatz_108_T15_j16_32_64_L5_source_refinement_collapse_report.md
scripts/spectral_program/collatz_108_T15_j64_128_L5_source_refinement_collapse_report.md
scripts/spectral_program/collatz_108_T15_j64_128_L5_bits12_source_refinement_collapse_report.md
scripts/spectral_program/collatz_108_T15_j64_128_full_bits12_source_refinement_collapse_report.md
scripts/spectral_program/collatz_109_T15_j16_32_64_L5_refined_prefix_cauchy_report.md
scripts/spectral_program/collatz_109_T15_j64_128_L5_refined_prefix_cauchy_report.md
scripts/spectral_program/collatz_109_T15_j64_128_full_refined_prefix_cauchy_report.md
scripts/spectral_program/collatz_110_T12_j16_32_b0_5_8_10_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T12_j16_32_64_b0_5_8_10_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T13_j16_32_b0_5_8_10_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T12_j32_64_128_b0_5_8_10_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T13_j32_64_b0_5_8_10_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T14_j32_64_b0_5_8_10_refined_square_probe_report.md
scripts/spectral_program/collatz_110_T14_j32_64_128_b0_refined_square_probe_report.md
scripts/spectral_program/collatz_111_T14_j32_64_b10_refined_square_key_drift_report.md
scripts/spectral_program/collatz_111_T14_j64_128_b0_refined_square_key_drift_report.md
scripts/spectral_program/collatz_112_T14_j32_64_b10_family_weighted_norm_probe_report.md
scripts/spectral_program/collatz_113_current_A0_A0_decay_law_probe_report.md
scripts/spectral_program/collatz_114_T14_j64_128_b0_A0_high_v2_tail_split_report.md
scripts/spectral_program/collatz_115_current_A0_A0_decomposition_decay_probe_report.md
scripts/spectral_program/collatz_117_current_A0_A0_v2_tail_formula_report.md
scripts/spectral_program/collatz_118_current_A0_A0_low_v2_phase_decay_probe_report.md
scripts/spectral_program/collatz_119_T14_j64_128_sample_A0_low_v2_return_depth_probe_report.md
scripts/spectral_program/collatz_120_T14_j128_sample_A0_dependency_depth_probe_report.md
scripts/spectral_program/collatz_121_T14_j128_sample_A0_walsh_haar_probe_report.md
scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_report.md
scripts/spectral_program/collatz_123_current_A0_A0_bounded_periodicity_probe_report.md
scripts/spectral_program/collatz_123_current_A0_large_m_A0_bounded_periodicity_probe_report.md
scripts/spectral_program/collatz_124_current_A0_A0_tail_grid_probe_report.md
scripts/spectral_program/collatz_124_current_A0_spread_A0_tail_grid_probe_report.md
scripts/spectral_program/collatz_125_current_A0_A0_kernel_mismatch_decomposition_report.md
scripts/spectral_program/collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_report.md
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T12_A0_kernel_mismatch_decomposition_report.md
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T12_A0_kernel_mismatch_decomposition_rows.csv
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T12_A0_kernel_mismatch_decomposition_examples.csv
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T13_A0_kernel_mismatch_decomposition_report.md
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T13_A0_kernel_mismatch_decomposition_rows.csv
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T13_A0_kernel_mismatch_decomposition_examples.csv
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T14_A0_kernel_mismatch_decomposition_report.md
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T14_A0_kernel_mismatch_decomposition_rows.csv
scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T14_A0_kernel_mismatch_decomposition_examples.csv
scripts/spectral_program/collatz_126_current_A0_A0_return_branch_affine_probe_branches.csv
scripts/spectral_program/collatz_126_current_A0_A0_return_branch_affine_probe_branches.json
scripts/spectral_program/collatz_126_current_A0_v2lt8_A0_return_branch_affine_probe_branches.csv
scripts/spectral_program/collatz_126_current_A0_v2lt8_A0_return_branch_affine_probe_branches.json
scripts/spectral_program/collatz_126_current_A0_v2lt8_prefix_A0_return_branch_affine_probe_branches.csv
scripts/spectral_program/collatz_126_current_A0_v2lt8_prefix_A0_return_branch_affine_probe_branches.json
scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T12_A0_return_branch_affine_probe_branches.csv
scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T12_A0_return_branch_affine_probe_branches.json
scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T13_A0_return_branch_affine_probe_branches.csv
scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T13_A0_return_branch_affine_probe_branches.json
scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T14_A0_return_branch_affine_probe_branches.csv
scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T14_A0_return_branch_affine_probe_branches.json
```

A0 top-Haar summary command:

```text
python3 scripts/spectral_program/122_A0_top_haar_decay_summary.py \
  --output-tag current_A0
```

A0 bounded periodicity probe commands:

```text
.venv/bin/python scripts/spectral_program/123_A0_bounded_periodicity_probe.py \
  --output-tag current_A0 \
  --sample-limit 512 \
  --step-cap 25 \
  --a-cap 8 \
  --m-values 4,8,12,16,20,24

.venv/bin/python scripts/spectral_program/123_A0_bounded_periodicity_probe.py \
  --output-tag current_A0_large_m \
  --sample-limit 128 \
  --step-cap 25 \
  --a-cap 8 \
  --m-values 24,64,128,192,193,200

.venv/bin/python scripts/spectral_program/124_A0_tail_grid_probe.py \
  --output-tag current_A0 \
  --sample-limit 128 \
  --step-caps 10,25,50,75 \
  --a-caps 4,6,8,10 \
  --min-period-m 32

.venv/bin/python scripts/spectral_program/124_A0_tail_grid_probe.py \
  --output-tag current_A0_spread \
  --sample-mode spread \
  --sample-limit 512 \
  --step-caps 10,25,50,75 \
  --a-caps 4,6,8,10 \
  --min-period-m 32

.venv/bin/python scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py \
  --output-tag current_A0_spread \
  --sample-mode spread \
  --sample-limit 512 \
  --step-caps 25,50,75 \
  --a-caps 6,8,10 \
  --focus-step-cap 75 \
  --focus-a-cap 10

PHASES=$(python3 - <<'PY'
print(','.join(f'{v}|{odd}|{h}' for v in range(8) for odd in (1,3) for h in range(4)))
PY
)
.venv/bin/python scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_complete_T12 \
  --sample-mode dyadic-prefix \
  --prefix-bits 12 \
  --step-caps 75 \
  --a-caps 10 \
  --focus-step-cap 75 \
  --focus-a-cap 10

.venv/bin/python scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_complete_T13 \
  --sample-mode dyadic-prefix \
  --prefix-bits 13 \
  --step-caps 75 \
  --a-caps 10 \
  --focus-step-cap 75 \
  --focus-a-cap 10

.venv/bin/python scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_complete_T14 \
  --sample-mode dyadic-prefix \
  --prefix-bits 14 \
  --step-caps 75 \
  --a-caps 10 \
  --focus-step-cap 75 \
  --focus-a-cap 10

.venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py \
  --output-tag current_A0 \
  --sample-mode spread \
  --sample-limit 256

.venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8 \
  --sample-mode spread \
  --sample-limit 64

.venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_prefix \
  --sample-mode prefix \
  --sample-limit 128

.venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_complete_T12 \
  --sample-mode dyadic-prefix \
  --prefix-bits 12

.venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_complete_T13 \
  --sample-mode dyadic-prefix \
  --prefix-bits 13

.venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py \
  --phases "$PHASES" \
  --output-tag current_A0_v2lt8_complete_T14 \
  --sample-mode dyadic-prefix \
  --prefix-bits 14
```

Current script-126 arithmetic-certificate output:

```text
current_A0_v2lt8 spread:
  total_samples=4096
  return_samples=1024
  branch_rows=16
  exact_failures=0
  noninteger_branches=0
  word_congruence_failures=0
  drop_affine_failures=0
  no_drop_certificate_rows=16
  branch_word_certificate_failures=0
  arithmetic_certificate_rows=16
  refined_formula_failures=0
  refined_state_failures=0
  label_intermediate_visible_failures=0
  label_intermediate_visible_split=target:0,competing:0
  label_intermediate_visible_prefix_split=target:0,competing:0
  label_final_target_low_failures=0
  label_final_target_high_lift_failures=16
  label_final_target_high_lift_mod_bits_range=7..7
  label_final_competing_failures=0
  label_status_target_high_lift_boundary=16
  label_status_blocked_label_congruence=0
  high_lift_continuation_supported_rows=16
  high_lift_continuation_step_delta_range=6..6
  high_lift_continuation_failures=integrality:0,no_drop:0

current_A0_v2lt8_complete_T12:
  total_samples=16320
  return_samples=1652
  branch_rows=860
  branch_sample_count_total=1652
  branch_sample_count_coverage_failures=0
  exact_failures=0
  noninteger_branches=0
  word_congruence_failures=0
  drop_affine_failures=0
  no_drop_certificate_rows=860
  branch_word_certificate_failures=0
  arithmetic_certificate_rows=860
  refined_formula_failures=0
  refined_state_failures=0
  label_intermediate_visible_failures=216
  label_intermediate_visible_split=target:12,competing:204
  label_intermediate_visible_prefix_split=target:12,competing:204
  label_intermediate_visible_by_record=k10c1:0,k11c1:156,k12c1:48,k12c2:12,k20c1:0
  label_intermediate_probe_selected=candidate:216,target:12,competing:204,none:0
  label_intermediate_probe_outcome=same_step:216,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_multiprobe_outcome=total:1728,same_step:1728,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_target_multiprobe_outcome=total:96,same_step:96,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_multiprobe_no_return_by_record=k10c1:0,k11c1:0,k12c1:0,k12c2:0,k20c1:0
  label_intermediate_multiprobe_no_return_extended=later_target:0,terminal:0,unresolved:0,later_delta_range:0..0
  label_intermediate_multiprobe_no_return_continuation=supported:0,failures:integrality:0,no_drop:0
  label_intermediate_multiprobe_no_return_actual_continuation=prefix_match:0,suffix_target_word:0,supported:0,failures:integrality:0,no_drop:0
  label_intermediate_multiprobe_no_return_actual_refined_continuation=supported:0,failures:0,extra_bits_range:0..0
  label_intermediate_competing_later_target_intersections=none:204,some:0
  label_intermediate_target_persistence=persistent:0,missing_prior:12,no_prior_competing:12,prior_competing:0
  label_intermediate_target_lift_cover=high_lift_covered:12,low_only:0
  label_final_target_low_failures=0
  label_final_target_high_lift_failures=860
  label_final_target_high_lift_mod_bits_range=7..7
  label_final_competing_failures=0
  label_split_resolution_certificate_rows=860
  label_status_target_high_lift_boundary=656
  label_status_blocked_label_congruence=204
  high_lift_continuation_supported_rows=860
  high_lift_continuation_step_delta_range=6..6
  high_lift_continuation_failures=integrality:0,no_drop:0

current_A0_v2lt8_complete_T13:
  total_samples=32640
  return_samples=3352
  branch_rows=1564
  branch_sample_count_total=3352
  branch_sample_count_coverage_failures=0
  exact_failures=0
  noninteger_branches=0
  word_congruence_failures=0
  drop_affine_failures=0
  no_drop_certificate_rows=1564
  branch_word_certificate_failures=0
  arithmetic_certificate_rows=1564
  refined_formula_failures=0
  refined_state_failures=0
  label_intermediate_visible_failures=376
  label_intermediate_visible_split=target:16,competing:360
  label_intermediate_visible_prefix_split=target:16,competing:360
  label_intermediate_visible_by_record=k10c1:0,k11c1:268,k12c1:92,k12c2:16,k20c1:0
  label_intermediate_probe_selected=candidate:376,target:16,competing:360,none:0
  label_intermediate_probe_outcome=same_step:376,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_multiprobe_outcome=total:3008,same_step:3008,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_target_multiprobe_outcome=total:128,same_step:128,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_multiprobe_no_return_by_record=k10c1:0,k11c1:0,k12c1:0,k12c2:0,k20c1:0
  label_intermediate_multiprobe_no_return_extended=later_target:0,terminal:0,unresolved:0,later_delta_range:0..0
  label_intermediate_multiprobe_no_return_continuation=supported:0,failures:integrality:0,no_drop:0
  label_intermediate_multiprobe_no_return_actual_continuation=prefix_match:0,suffix_target_word:0,supported:0,failures:integrality:0,no_drop:0
  label_intermediate_multiprobe_no_return_actual_refined_continuation=supported:0,failures:0,extra_bits_range:0..0
  label_intermediate_competing_later_target_intersections=none:360,some:0
  label_intermediate_target_persistence=persistent:0,missing_prior:16,no_prior_competing:16,prior_competing:0
  label_intermediate_target_lift_cover=high_lift_covered:16,low_only:0
  label_final_target_low_failures=0
  label_final_target_high_lift_failures=1564
  label_final_target_high_lift_mod_bits_range=7..7
  label_final_competing_failures=0
  label_split_resolution_certificate_rows=1564
  label_status_target_high_lift_boundary=1212
  label_status_blocked_label_congruence=352
  high_lift_continuation_supported_rows=1564
  high_lift_continuation_step_delta_range=6..6
  high_lift_continuation_failures=integrality:0,no_drop:0

current_A0_v2lt8_complete_T14:
  total_samples=65280
  return_samples=6748
  branch_rows=2868
  branch_sample_count_total=6748
  branch_sample_count_coverage_failures=0
  exact_failures=0
  noninteger_branches=0
  word_congruence_failures=0
  drop_affine_failures=0
  no_drop_certificate_rows=2868
  branch_word_certificate_failures=0
  arithmetic_certificate_rows=2868
  refined_formula_failures=0
  refined_state_failures=0
  label_intermediate_visible_failures=744
  label_intermediate_visible_split=target:64,competing:680
  label_intermediate_visible_prefix_split=target:64,competing:680
  label_intermediate_visible_by_record=k10c1:8,k11c1:472,k12c1:200,k12c2:64,k20c1:0
  label_intermediate_probe_selected=candidate:744,target:64,competing:680,none:0
  label_intermediate_probe_outcome=same_step:744,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_multiprobe_outcome=total:5952,same_step:5944,early_target:0,no_return_by_final:8,terminal_by_final:0
  label_intermediate_target_multiprobe_outcome=total:512,same_step:512,early_target:0,no_return_by_final:0,terminal_by_final:0
  label_intermediate_multiprobe_no_return_by_record=k10c1:0,k11c1:0,k12c1:8,k12c2:0,k20c1:0
  label_intermediate_multiprobe_no_return_extended=later_target:8,terminal:0,unresolved:0,later_delta_range:6..6
  label_intermediate_multiprobe_no_return_continuation=supported:0,failures:integrality:8,no_drop:0
  label_intermediate_multiprobe_no_return_actual_continuation=prefix_match:8,suffix_target_word:8,supported:0,failures:integrality:8,no_drop:0
  label_intermediate_multiprobe_no_return_actual_refined_continuation=supported:8,failures:0,extra_bits_range:4..4
  label_intermediate_competing_later_target_intersections=none:680,some:0
  label_intermediate_target_persistence=persistent:0,missing_prior:64,no_prior_competing:64,prior_competing:0
  label_intermediate_target_lift_cover=high_lift_covered:64,low_only:0
  label_final_target_low_failures=0
  label_final_target_high_lift_failures=2868
  label_final_target_high_lift_mod_bits_range=7..7
  label_final_competing_failures=0
  label_split_resolution_certificate_rows=2868
  label_status_target_high_lift_boundary=2176
  label_status_blocked_label_congruence=692
  high_lift_continuation_supported_rows=2868
  high_lift_continuation_step_delta_range=6..6
  high_lift_continuation_failures=integrality:0,no_drop:0
```

Interpretation: `arithmetic_certificate_rows = branch_rows` certifies the
valuation-word cylinder, integral bi-affine return formula, dyadic delta,
affine no-drop prefix property, and destination-state refinement for the
extracted finite rows.  It does not certify the global first-return/tail
label on an infinite residue class.  The label-gate diagnostic reduces
the remaining obstruction to explicit 2-adic congruence boundaries:
target high-lift residues and, in the complete-prefix runs, some
intermediate visible-label residues.  There are no final competing
phantom labels in these runs.  The target high-lift boundary is uniformly
one congruence class modulo `2^7` in the branch parameter `u`, and it is
extendable in every imported finite-prefix branch by appending one target
period: the extension has step delta `+6` and zero integrality/no-drop
failures.  The active unresolved family is therefore the intermediate
visible-label congruence family, which still needs an automaton-aware
split before it can be counted as a controlled boundary or rejected as a
genuine obstruction.  The first exact split shows that this family is
dominated by competing/non-target visibility: totals across `T12/T13/T14`
are target `92`, competing `1244`, with zero split-accounting failures in
the Lean import.  A finer per-record split gives `k10c1=8`,
`k11c1=896`, `k12c1=340`, `k12c2=92`, and `k20c1=0`; the dominant
families are therefore the `(11,1)` and `(12,1)` competitors.  A
representative automaton probe then checks one representative for each
intermediate visible congruence class: all `1336` representatives select
the visible candidate and still return to the target at the original final
step; there are zero early target returns, zero no-return-by-final cases,
and zero terminal-by-final cases.  This is diagnostic finite evidence, not
a uniform proof over every residue in those congruence classes.
A stronger exact congruence-intersection check shows that all `1244`
intermediate competitor classes have no intersection with any later
intermediate target-visible class before the final step.  This is a
finite-prefix certificate for the imported summaries; it does not yet
prove the infinite residue-class branch certificate.
The target-intermediate classes also have a finite imported structure:
there are zero persistent-target classes, all `92` target classes are
missing some prior target visibility, all `92` have no prior competing
intersection, and zero have prior competing intersection.  All `92`
target-intermediate classes are covered by target high-lift visibility
(`b >= 2`), with zero low-only target `b=1` classes.
The derived finite split-resolution diagnostic combines these exact
congruence facts with zero final competing labels and the high-lift
continuation arithmetic.  It covers all `5292` imported complete-prefix
branch rows.  This should be read only as a finite branch-split
certificate for the declared summaries, not as an infinite proof.  The
abstract Lean schema is `WeakBridge.LabelSplit.branchResolved` at row
level and `WeakBridge.LabelSplit.summaryResolved` at finite-summary level;
the generated A0 import proves
`a0CompletePrefixSummariesV2Lt8_label_split_summary_resolved`.  The same
namespace now contains the conditional cover bridge
`WeakBridge.LabelSplit.BranchCover` / `BranchPartition`: if a declared
cover assigns source points to resolved branches, then every covered source
point is resolved in the finite label-split sense.  This is only a
conditional bridge; the Collatz/A0 infinite cover is still an open gate.
The finite return-sample partition summary is also imported: across
`T12/T13/T14`, branch-row sample counts cover exactly all `11752` finite
return samples, with zero coverage failures, theorem
`a0CompletePrefixSummariesV2Lt8_return_partition_summary_resolved`.
The complete finite-prefix outcome accounting is also imported through
`WeakBridge.LabelSplit.OutcomeSummary`: theorem
`a0CompletePrefixSummariesV2Lt8_outcome_decomposition_resolved` checks
that the same summaries have `114240` total source samples, decomposed as
`11752` covered return samples, `101628` drop samples, `844`
valuation-tail samples, and `16` step-tail samples, with zero
return-coverage failures.  This is an exact finite balance sheet, not a
claim that the tails vanish in any limiting regime.
The eight-shift multi-probe tests `10688` shifted representatives across
the intermediate visible classes.  It finds zero early target returns.
The target-intermediate subprobe is completely same-step (`736/736`).
There are `8` no-return-by-final shifted representatives, all in `T14`
competitor rows.  The refined split shows all eight are `(12,1)` cases and
all return to target later within the step cap, with step delta exactly
`+6`; there are zero terminal and zero unresolved extended outcomes.  This
is a finite continuation-boundary diagnostic, not yet an infinite theorem.
The naive unrefined continuation over the eight-shift class fails
integrality in all eight cases.  Tracing the actual late-return word gives
prefix agreement with the original word and suffix agreement with the
target word in all eight cases.  After a further four-bit finite split, the
actual continuation is supported in all eight cases with zero refined
failures.

Component transition-budget command:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/103_component_transition_budget.py \
  --T 15 \
  --j-count 64 \
  --odd-bits 2 \
  --hit-bits 2 \
  --v2-cap 13 \
  --max-steps 1000 \
  --output-tag T15_j64
```

Important caveat: this script aggregates over actual lifted sources
`t`.  Runs with the same product `j_count * 2^T` enumerate the same
prefix window and are not independent stability checks in `T`.

Alternative bad-rule comparison commands:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/103_component_transition_budget.py \
  --T 15 \
  --j-count 32 \
  --bad-rule v2_2_odd3 \
  --output-tag T15_j32_v2_2_odd3

uv run --with numpy --with scipy python \
  scripts/spectral_program/103_component_transition_budget.py \
  --T 15 \
  --j-count 32 \
  --bad-rule odd3_or_v2_2 \
  --output-tag T15_j32_odd3_or_v2_2
```

Component block-Cauchy commands:

Multipair source data:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 15 \
  --j-counts 16,32,64 \
  --block-size 16 \
  --max-steps 1000 \
  --output-tag T15_B16_j64_multipair
```

Large prefix source data:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/88_cylinder_signature_stability.py \
  --T 15 \
  --j-counts 64,128 \
  --block-size 64 \
  --max-steps 1000 \
  --progress \
  --output-tag T15_B64_j128_prefix
```

```text
python3 scripts/spectral_program/104_component_block_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B8_j16_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B8_j16_signature_distribution.csv \
  --output-tag T15_B8_j16

python3 scripts/spectral_program/104_component_block_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j32_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j32_signature_distribution.csv \
  --output-tag T15_B16_j32

python3 scripts/spectral_program/104_component_block_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B32_j64_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B32_j64_signature_distribution.csv \
  --output-tag T15_B32_j64

python3 scripts/spectral_program/104_component_block_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_B16_j64_multipair

python3 scripts/spectral_program/104_component_block_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_B64_j128_prefix
```

Component prefix/Cesaro command:

```text
python3 scripts/spectral_program/105_component_prefix_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_multipair

python3 scripts/spectral_program/105_component_prefix_cauchy.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_prefix
```

Prefix label-lift commands:

```text
python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_multipair_full

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_multipair_L5

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --bad-rule v2_2_odd3 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_v2_2_odd3_full

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --bad-rule odd3_or_v2_2 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_odd3_or_v2_2_full

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_prefix_full

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_prefix_L5

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --bad-rule v2_2_odd3 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_v2_2_odd3_full

python3 scripts/spectral_program/106_prefix_label_lift.py \
  --T 15 \
  --bad-rule odd3_or_v2_2 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_odd3_or_v2_2_full
```

Gate 10.B finite closure-check command:

```text
python3 scripts/spectral_program/107_gate10b_closure_checks.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_L5
```

The regenerated `107` report includes component, phase, and full-label
row-drift means.  The phase mean is the one aligned with the current
Lean `TransferMatrix V` state space.

Additional phase-prefix trend command:

```text
python3 scripts/spectral_program/107_gate10b_closure_checks.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_L5
```

No-cutoff sensitivity commands:

```text
python3 scripts/spectral_program/107_gate10b_closure_checks.py \
  --T 15 \
  --no-delta-cutoff \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_full

python3 scripts/spectral_program/107_gate10b_closure_checks.py \
  --T 15 \
  --no-delta-cutoff \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_full
```

H4 matching note:

```text
The script-107 reports verify the CSV row-source identity for the T=15
phase-prefix kernels.  They do not generate a matching Lean
TransferMatrix.  The existing generated PhaseState Lean imports are the
older T10CriticalSymbolic and T10J32HighBitTail objects.
```

The same reports now include `Source-Phase Collapse Checks`, measuring
the cost of replacing source-cell rows by source-PhaseState averaged
rows.  This is the finite diagnostic for whether a `TransferMatrix V`
is an exact projection or an averaged quotient.

Source-refinement collapse commands:

```text
python3 scripts/spectral_program/108_source_refinement_collapse.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_L5

python3 scripts/spectral_program/108_source_refinement_collapse.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_L5

python3 scripts/spectral_program/108_source_refinement_collapse.py \
  --T 15 \
  --delta-cutoff 5 \
  --max-bits 12 \
  --min-mean-cells 4 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_L5_bits12

python3 scripts/spectral_program/108_source_refinement_collapse.py \
  --T 15 \
  --no-delta-cutoff \
  --max-bits 12 \
  --min-mean-cells 4 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_full_bits12
```

The source-refinement reports are finite obstruction diagnostics.  They
do not define a natural infinite quotient, but they identify
`source_phase + low residue bits` as the first serious candidate for a
refined source alphabet.

Refined prefix-Cauchy commands:

```text
python3 scripts/spectral_program/109_refined_prefix_cauchy.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B16_j64_multipair_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B16_j64_multipair_signature_distribution.csv \
  --output-tag T15_j16_32_64_L5

python3 scripts/spectral_program/109_refined_prefix_cauchy.py \
  --T 15 \
  --delta-cutoff 5 \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_L5

python3 scripts/spectral_program/109_refined_prefix_cauchy.py \
  --T 15 \
  --no-delta-cutoff \
  --groups scripts/spectral_program/collatz_88_T15_B64_j128_prefix_cylinder_group_summary.csv \
  --distributions scripts/spectral_program/collatz_88_T15_B64_j128_prefix_signature_distribution.csv \
  --output-tag T15_j64_128_full
```

These reports measure prefix drift after choosing a finite source key.
They should be read together with script `108`: source refinement lowers
collapse error but raises prefix drift toward the `source_cell`
baseline.

Refined square-kernel smoke commands:

```text
uv run --with numpy --with scipy python \
  scripts/spectral_program/110_refined_square_probe.py \
  --T 12 \
  --j-counts 16,32 \
  --refine-bits 0,5,8,10 \
  --max-steps 1000 \
  --output-tag T12_j16_32_b0_5_8_10

uv run --with numpy --with scipy python \
  scripts/spectral_program/110_refined_square_probe.py \
  --T 12 \
  --j-counts 16,32,64 \
  --refine-bits 0,5,8,10 \
  --max-steps 1000 \
  --output-tag T12_j16_32_64_b0_5_8_10

uv run --with numpy --with scipy python \
  scripts/spectral_program/110_refined_square_probe.py \
  --T 13 \
  --j-counts 16,32 \
  --refine-bits 0,5,8,10 \
  --max-steps 1000 \
  --output-tag T13_j16_32_b0_5_8_10

uv run --with numpy --with scipy python \
  scripts/spectral_program/110_refined_square_probe.py \
  --T 12 \
  --j-counts 32,64,128 \
  --refine-bits 0,5,8,10 \
  --max-steps 1000 \
  --output-tag T12_j32_64_128_b0_5_8_10
```

These are smoke diagnostics only.  They retrace finite rows and record
destination low-residue data for a possible `A1` square kernel.
The `T13_j16_32` run is a consistency check for the corresponding
effective prefix window, not independent asymptotic evidence.

## 6. Lean K16 Verification

Build command:

```text
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
lake build CollatzShadowing.Generated.K16S16KDeterministicCW
```

Current status:

```text
Build completed successfully (3302 jobs).
```

Lean theorem to cite:

```text
k16s16KDeterministicGeneratedSpectralRadiusBound
```

## 7. Exact CW Certificate Verification

K16 production finite certificate:

```text
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json
```

Current verified output:

```text
alpha=3/4
max_ratio=90833233962213/129559208330288
max_node=K11:b2
status=OK
```

K20 smoke certificate:

```text
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k20_smoke_residue_K_cw_certificate.json
```

Current verified output:

```text
alpha=3/4
max_ratio=42001755821431/62996587868160
max_node=K4:b4
status=OK
```

K20 remains smoke only.

## 8. Phantom-Taxonomy Script Verification

Compile check:

```text
python3 -m py_compile \
  scripts/phantom_taxonomy/deterministic_residue_transfer.py \
  scripts/phantom_taxonomy/scc_cw_certificate.py \
  scripts/phantom_taxonomy/scc_report.py \
  scripts/phantom_taxonomy/orbit_harness.py
```

Current status: passes.

## 9. ASCII Check

Command:

```text
rg -n "[^\\x00-\\x7F]" \
  notes/phase10_*.md \
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
  scripts/spectral_program/110_refined_square_probe.py \
  scripts/spectral_program/111_refined_square_key_drift_inspector.py \
  scripts/spectral_program/112_family_weighted_norm_probe.py \
  scripts/spectral_program/113_A0_decay_law_probe.py \
  scripts/spectral_program/114_A0_high_v2_tail_split.py \
  scripts/spectral_program/115_A0_decomposition_decay_probe.py \
  scripts/spectral_program/117_A0_v2_tail_formula.py \
  scripts/spectral_program/118_A0_low_v2_phase_decay_probe.py \
  scripts/spectral_program/119_A0_low_v2_return_depth_probe.py \
  scripts/spectral_program/120_A0_dependency_depth_probe.py \
  scripts/spectral_program/121_A0_walsh_haar_probe.py \
  scripts/spectral_program/122_A0_top_haar_decay_summary.py \
  scripts/spectral_program/123_A0_bounded_periodicity_probe.py \
  scripts/spectral_program/124_A0_tail_grid_probe.py \
  scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py
```

Current status: no matches.

## 10. What Must Be Archived for External Reproduction

Before any external release or paper supplement, archive:

- active `collatz_88_*` CSVs for each tagged diagnostic run;
- the exact command line used for each script-`88` run;
- all `collatz_93` through `collatz_110` reports and CSVs;
- K16 deterministic residue-cell manifest, edge CSV, source coverage,
  JSON CW certificate, and generated Lean file;
- K20 smoke files only if clearly marked as smoke;
- a git tree hash or file hashes for generated artifacts.

## 11. Current Non-Claims

The reproducibility manifest does not establish:

- existence of an infinite operator;
- convergence of finite matrices;
- a Lasota-Yorke inequality;
- Hennion/Keller-Liverani hypotheses;
- a spectral gap;
- Conjecture 6.
