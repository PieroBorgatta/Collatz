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
  scripts/spectral_program/110_refined_square_probe.py
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
```

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
  scripts/spectral_program/110_refined_square_probe.py
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
