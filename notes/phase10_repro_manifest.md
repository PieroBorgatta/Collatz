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
`hasStrictDescent_iff_nonempty_witness`, plus `DirectDropSound`,
`BranchSound`, and `LossSound` for packaging direct-drop, resolved-branch,
and declared-loss predicates into the global-cover witness interface.
`FiniteModelSoundSpec` packages these three propositional soundness
obligations and proves `classicalCollatz_of_finiteModelSoundSpec` through
`FiniteModelCoverSpec`.  Direct drops can now be recorded in the
step-indexed form `DirectDropAt`, with
`hasStrictDescent_of_directDropAt` feeding the existential strict-descent
form; the reducers `DirectDropAtSound`, `BranchDropAtSound`,
`LossDropAtSound`, and `LossAbsent` convert explicit descent-time or
absence proofs into the three soundness obligations (`3291` jobs; latest
run `107s`).  The bridge also contains a minimal natural-number semantics
for finite Syracuse exponent words: `syracuseStepWithExponent`,
`evalSyracuseWord`, `SyracuseWordMatchesFrom`,
`evalSyracuseWord_eq_iterate_of_matches`, and
`directDropAt_of_word_matches_eval_lt`.  Thus a matched nonempty exponent
word whose evaluated endpoint is below its start yields `DirectDropAt`
(`3291` jobs; latest run `35s`).  The current branch-facing wrapper is
`BranchWordDropSound`: for each resolved branch it asks for such a word
match plus endpoint descent, and the theorems
`branchDropAtSound_of_branchWordDropSound` and
`branchSound_of_branchWordDropSound` convert it into the soundness
obligation used by `FiniteModelSoundSpec` (`3291` jobs; latest run `82s`).
A read-only coefficient audit of the existing complete-prefix script-126 CSV
outputs for `T12/T13/T14` found no immediate affine direct-drop return rows:
`0/860`, `0/1564`, and `0/2868` rows satisfy coefficientwise
`next_t < source_t` on their declared progressions.  This is an empirical
finite-artifact audit, not a Lean theorem; it indicates that the current A0
return rows require a transition/descent mechanism rather than a one-word
direct-drop instantiation of `BranchWordDropSound`.
The bridge now contains the transition-chain version of this mechanism:
`evalSyracuseWordChain`, `syracuseWordChainLength`,
`SyracuseWordChainMatchesFrom`,
`evalSyracuseWordChain_eq_iterate_of_matches`, and
`directDropAt_of_word_chain_matches_eval_lt`.  The branch-facing condition
`BranchTransitionChainDropSound` allows intermediate growing return words,
but still requires the final endpoint to be below the original source
integer.  Theorems
`branchDropAtSound_of_branchTransitionChainDropSound` and
`branchSound_of_branchTransitionChainDropSound` connect this condition to
`BranchSound` (`3291` jobs; latest run `91s`).
The bridge also contains the elementary affine-coordinate exclusion
`AffineTBranch.not_nextLocalInteger_lt_sourceLocalInteger_of_coeffNondecreasing`:
for a row `source_t = q*u+r`, `next_t = a*u+b`, coefficientwise
non-decrease `a >= q`, `b >= r` rules out a strict drop after embedding
both coordinates into the same residue class `residue + modulus*t`.
A read-only JSON audit of the complete-prefix script-126 artifacts confirms
that all current A0 return rows are in this monotone class, both before and
after destination refinement: `T12/T13/T14` have zero base non-decrease
failures (`0/860`, `0/1564`, `0/2868`) and zero refined failures, with
minimum slope ratio `531441/524288 > 1`.  This is a negative reduction:
same-coordinate chains made only from these return rows cannot supply the
endpoint descent required by `BranchTransitionChainDropSound`.
The complementary direct-drop certificate shape is now formalized as
`AffineNatDropBranch.targetN_lt_sourceN_of_coeffDrop`, and
`directDropAt_of_word_matches_affineNatDrop` connects that affine
certificate to `DirectDropAt` when the matched Syracuse word and the
source/endpoint affine equalities are supplied.  A read-only
reconstruction of the script-126 direct-drop traces found that all finite
drop groups in the complete prefixes have integer affine endpoint formulae
and satisfy the coefficientwise global drop condition on their observed
congruence progressions: `T12/T13/T14` have `9032/16692/30900` certified
drop groups, covering exactly `14548/29040/58040` finite drop samples, with
zero bad groups and zero noninteger groups.  This supports the local
`DirectDropAtSound` route but does not prove an infinite source partition or
remove the declared tails.
The declared valuation-tail samples are now understood more sharply.  A
read-only replay of the same traces shows that every finite valuation-tail
sample in `T12/T13/T14` is already below the original source after the
high-valuation step (`120/120`, `240/240`, `484/484`); script `126`
classified them as tails because it checks `a_val > a_cap` before
`cur < n0`.  Lean proves the supporting general lemma
`syracuse_lt_self_of_two_le_exponent`: for `1 < n`, an accelerated exponent
at least `2` implies `S n < n`; the wrapper
`directDropAt_one_of_two_le_syracuseExponent` packages this as
`DirectDropAt 1 n`.  The finite `step_tail` samples remain different at the
original cap: the replay finds `0/8` and `0/8` final drops
at cap `75`.  Extending just those eight representatives to cap `100`
turns them into direct drops: four `t=4853`, `phase=0|1|h` representatives
drop at step `91`, and four `t=7110`, `phase=1|3|h` representatives drop at
step `76`.  This is finite evidence that the current `step_tail` counts are
budget artifacts, not a global no-budget-exit theorem.
A full read-only semantic replay with priority `drop` before
`valuation_tail` and cap `100` has no residual finite losses on the complete
prefixes: `T12 = 14668` drops plus `1652` returns, `T13 = 29288` drops plus
`3352` returns, and `T14 = 58532` drops plus `6748` returns.  This has not
yet replaced the generated cap-75 Lean import; it is the next candidate
generation policy.
However, a raw drop-row import is not the right next artifact.  A read-only
compression audit with the complete `v2 < 8` phase list gives, at `T14`,
`31324` phase-word drop groups and `28852` singleton groups.  All semantic
drop words in `T12/T13/T14` share the common prefix `[1,1,2,1,1,1]`, so the
proof-facing reduction should factor this prefix and prove a suffix/contractive
word criterion rather than exporting thousands of one-off rows.  Lean now has
the supporting word-factorization lemmas `evalSyracuseWord_append`,
`SyracuseWordMatchesFrom_append`, and
`directDropAt_of_suffix_after_prefix_matches_eval_lt`, plus the exact
matched-word affine formula
`evalSyracuseWord_mul_pow_sum_eq_affine_of_matches`.  The observed common
prefix is named `a0SemanticDropCommonPrefix = [1,1,2,1,1,1]`, and Lean proves
`a0SemanticDropCommonPrefix_affine_of_matches`:
`128 * endpoint = 729*n + 817`.  The corresponding proof-facing suffix target
is `directDropAt_of_a0CommonPrefix_suffix_scaled_contracting`, which requires
the scaled inequality
`3^len(s)*(729*n+817)+128*C_s < 128*2^A_s*n`.
Lean also proves the threshold form
`directDropAt_of_a0CommonPrefix_suffix_threshold_contracting`, reducing this
to `729*3^len(s) <= 128*2^A_s` plus an explicit lower-bound inequality for
`n`.  The finite theorem `smallOddHasDirectDropWithin100Bool` verifies by
`native_decide` that every positive odd `n < 455`, `n != 1`, has a direct
accelerated drop within `100` steps; `hasStrictDescent_of_odd_lt_455` packages
that finite exception range as `HasStrictDescent`.  The combined theorem
`hasStrictDescent_of_a0CommonPrefix_suffix_threshold_at_455` then says that a
future generated suffix certificate only needs the common-prefix match,
nonempty suffix, slope-gap inequality, and threshold inequality at `455` to
produce `HasStrictDescent`.  The Lean row type
`A0SemanticSuffixCertificate` and predicate
`A0SemanticSuffixCertificate.ValidAt455` now package that exact obligation;
`A0SemanticSuffixCertificate.hasStrictDescent_of_validAt455` is the local
bridge from one valid suffix row plus a matched common-prefix word to
`HasStrictDescent`.  The coarser row type
`A0SemanticSuffixPairCertificate` gives the formal meaning of the pair
compression: a valid pair row certifies a concrete suffix once its
`length`, `sum`, and `syracuseWordConst` bound are supplied.  The computable
checker `A0SemanticSuffixPairCertificate.allValidAt455Bool` and membership
lemma `validAt455_of_mem_of_allValidAt455Bool` prepare the path for a generated
T14 pair list.
Script `126` exposes this audit through the opt-in
`--semantic-replay-word-audit` flag.  With the complete `T14` phase list and
`--semantic-replay-step-cap 100`, the no-write check prints
`semantic_replay_drop_word_audit=distinct_words:7831,phase_word_groups:31324,phase_word_singletons:28852,distinct_suffixes:7831,suffix_slope_failures:0,suffix_threshold_max:455,common_prefix_failures:0,common_prefix_samples:58532`.
The separate opt-in flag `--semantic-replay-suffix-certificate` writes one
exact row per observed suffix after the common prefix into the existing JSON
stats payload, and creates no additional artifact by default.  The no-write
checks report `semantic_replay_suffix_certificate=rows:2287,failures:0,
threshold_max:320` at `T12` and
`semantic_replay_suffix_certificate=rows:7831,failures:0,threshold_max:455`
at `T14`.
Lean imports the three-prefix compact audit as
`a0SemanticDropWordAuditSummariesV2Lt8Cap100`; theorem
`a0SemanticDropWordAuditV2Lt8Cap100_summary` verifies total semantic drop
samples `102488`, common-prefix failures `0`, suffix slope-failure words `0`,
maximum suffix threshold `455`, phase-word groups `57392`, and singleton
phase-word groups `52696`.  It also records the opt-in suffix-certificate
aggregate: `14348` suffix rows across `T12/T13/T14`, equal to the distinct
suffix count, with `0` suffix-certificate failures and certificate threshold
max `455`.  The opt-in export also records the coarser pair compression by
`(suffix_len, suffix_sum)`: `241/290/351` pair rows at `T12/T13/T14`, `882`
total pair rows across the three summaries, zero pair-certificate failures,
and pair threshold max `455`.  The pair-failure counter checks the exact
row-level `ValidAt455` inequality used by the Lean pair-certificate bridge.
A read-only inclusion audit shows that the T14 pair table contains the T12 and
T13 pair tables; on common pairs, T14 has `suffixConstMax` and threshold
maxima at least as large as the earlier prefixes.  Thus the current minimal
pair-table candidate is the single T14 table with `351` rows.
The script-side current-run pair coverage audit at T14 prints
`semantic_replay_suffix_pair_coverage=suffix_rows:7831,covered_suffix_rows:7831,uncovered_suffix_rows:0,covered_drop_samples:58532,covered_phase_word_groups:31324,failures:missing_pair:0,const_bound:0,threshold_bound:0,loss_free:1`.
The source-level line is
`semantic_replay_source_pair_coverage=drop_samples:58532,covered_samples:58532,uncovered_samples:0,common_prefix_failures:0,failure_total:0,loss_free:1`.
A read-only stability check beyond T14 is negative.  The fixed T14 pair table
does not cover T15: T15 has `117016` semantic-drop samples, `14201` distinct
suffixes, and `404` current-run pair rows; relative to the T14 table there are
`53` missing pair keys, `69` missing suffix rows, `224` const-bound failures,
and `37` threshold-bound failures.  Likewise T15 does not cover T16: T16 has
`233992` semantic-drop samples, `26112` distinct suffixes, `473` current-run
pair rows, and threshold max `463`; relative to the T15 table there are `69`
missing pair keys, `85` missing suffix rows, `263` const-bound failures, and
`56` threshold-bound failures.  T16 also fails to cover T17: T17 has `467696`
semantic-drop samples, `47843` distinct suffixes, `560` current-run pair rows,
and threshold max `463`; relative to the T16 table there are `87` missing pair
keys, `115` missing suffix rows, `321` const-bound failures, and `51`
threshold-bound failures.  Therefore the current finite pair tables are
finite certificates, not stable-cover candidates.
Lean now has the cutoff-parametric bridge
`hasStrictDescent_of_a0CommonPrefix_suffix_threshold_at_cutoff` plus the
finite cutoff-464 and cutoff-648 wrappers
`hasStrictDescent_of_a0CommonPrefix_suffix_threshold_at_464` and
`hasStrictDescent_of_a0CommonPrefix_suffix_threshold_at_648`.
The certificate API is also parametrized via
`A0SemanticSuffixCertificate.ValidAtCutoff` and
`A0SemanticSuffixPairCertificate.ValidAtCutoff`, with computable
`validAtCutoffBool` / `allValidAtCutoffBool` for future generated tables.
Script `126` now accepts `--semantic-replay-certificate-cutoff`.  With T18 and
cutoff `648`, the current-run audit reports `85753` suffix rows, `652` pair
rows, threshold max `647`, zero certificate failures, and source-level
coverage `934832/934832` with `failure_total:0`.
At T19, the original operational caps are no longer enough: with `a_cap=10`
and semantic step cap `100`, the replay has `44` loss samples (`8`
valuation-tail, `36` step-tail).  Enlarging to `a_cap=20` and semantic step
cap `200` makes T19 loss-free: `drop=1869500`, `return=219460`, max
drop/return steps `138/105`, `156188` distinct suffixes, `749` pair rows,
threshold max `647`, and full source-pair coverage.  Generated Lean records
this compactly, after a follow-up cutoff-`648` no-write check, as
`a0SemanticReplayT19A20Cap200Cutoff648`.
With the same enlarged caps, T20 is also loss-free:
`drop=3739212`, `return=438708`, no valuation/step tails, max drop/return
steps still `138/105`, `284363` distinct suffixes, `842` pair rows, threshold
max still `647`, and full source-pair coverage `3739212/3739212`.
Generated Lean records this compactly as
`a0SemanticReplayT20A20Cap200Cutoff648`, and records the finite T19/T20
stability of threshold and step maxima as
`a0SemanticReplayT19T20A20Cap200Cutoff648_stable_bounds`.
The proof-facing cover interface is no longer tied to the T14 table:
`A0SemanticSuffixPairCover` and `A0SemanticDropSourcePairCover` accept an
arbitrary finite pair-certificate table, and the use theorems
`hasStrictDescent_of_a0SemanticSuffixPairCoverAtCutoff` and
`hasStrictDescent_of_a0SemanticDropSourcePairCoverAtCutoff` require only
validity at a cutoff plus a small-exception theorem below that cutoff.  The
existing T14 table is connected to this generic route by
`a0SemanticSuffixPairCertificatesT14_allValidAtCutoff455` and
`A0SemanticSuffixT14PairCover.toGeneric`.
The table-level wrapper `A0SemanticDropTableSpec` now packages a finite pair
table, cutoff, row-validity proof, and small-exception theorem; its theorem
`A0SemanticDropTableSpec.hasStrictDescent_of_sourceCover` reduces a local A0
semantic-drop proof to providing source-cover data into that table.  The T14
table instantiates the wrapper as `a0SemanticDropTableSpecT14`.
At the finite-branch interface, `A0SemanticDropBranchCoverSound` and
`branchSound_of_a0SemanticDropBranchCoverSound` state the current local
obligation in the language of `BranchSound`: for a resolved branch, provide
`T.SourceCover n` into a fixed semantic-drop table.
The common prefix in this obligation has now been made parametric.  Script
`126` has A0 source cylinder `n = 103 + 256*t`; Lean proves
`a0SemanticDropCommonPrefix_matches_source_cylinder` for all `t`, and the
endpoint formula `eval_a0SemanticDropCommonPrefix_source_cylinder`:
after `[1,1,2,1,1,1]` the endpoint is `593 + 1458*t`.  The append lemma
`SyracuseWordMatchesFrom_append_of_matches` and constructor
`AffineTBranch.a0SemanticDropSourcePairCover_of_localInteger_suffixCover`
show that the remaining local source-cover data is exactly a suffix match
from this endpoint plus assignment to a valid pair-certificate row.
That residual datum is now named `A0EndpointSuffixPairCover`, with the
table-level theorem
`A0SemanticDropTableSpec.hasStrictDescent_of_endpointSuffixCover`; for the
current generated T14 table the corresponding wrapper is
`hasStrictDescent_of_a0SemanticDropTableSpecT14_endpointSuffixCover`.
The first suffix split is also formalized.  From the endpoint
`593 + 1458*t`, odd `t` forces next exponent `1`, while `t=2*u` gives
`2 + ν₂(445 + 2187*u)`.  This records where the problem stops being a fixed
prefix calculation and becomes a recursive affine-valuation problem.
A quick no-write suffix-closure probe checked all `t < 2^20`: every sampled
suffix drops below the original source within cap `300`, with observed max
suffix length `205`.  This remains finite evidence.  It does not currently
look like a small finite suffix-word closure: distinct suffix words grow from
`206920` at `D=19` to `383215` at `D=20`, and pair rows grow from `982` to
`1123`.  High first suffix exponents (`>=5`) drop coefficientwise in one
step; the low-exponent branches `1..4` recursively generate the hard affine
valuation process.
A follow-up exact no-write probe tracked the repeated first-bad `e=1` branch.
For every tested depth `m <= 30`, there is a residue class
`t == r_m (mod 2^m)` forcing the first `m` suffix exponents after the common
prefix to be `1`, with the affine endpoint still coefficientwise above the
original source after those `m` steps.  At `m=30`, the class is
`t == 79536431 (mod 2^30)` and the slope ratio is approximately `1.09e6`.
This is an exact finite obstruction to any proof strategy that requires a
uniformly bounded suffix length.  It is not a theorem about all infinite
low-exponent paths.  The Lean-side local API now includes
`AffineNatDropBranch.CoeffNondecreasing`, `AffineNatDropBranch.eOneChild`, and
`AffineNatDropBranch.eOneChild_not_coeffDrop_of_slope_growth`.
The same probe identifies the exact 2-adic boundary: the repeated `e=1`
residue bits are periodic with period `18`, representing `t = -11/27`.
Lean records the rational endpoint identities
`a0Endpoint_phantomParameter_eq_negOne`,
`593 + 1458*(-11/27) = -1`, and
`a0Source_phantomParameter_eq_negThirtyFiveOverTwentySeven`,
`103 + 256*(-11/27) = -35/27`.  Hence this infinite obstruction is the usual
`-1` phantom endpoint in the A0 post-prefix coordinate, not evidence for a
finite suffix-table closure.
Lean now generalizes this periodic-boundary mechanism through
`syracuseWordAffineEndpointQ`, `syracuseWordFormalFixedPoint`,
`syracuseWordFormalFixedPoint_fixed`, and
`syracuseWordFormalFixedPoint_neg_of_expanding`: any nonempty periodic
exponent word with `2^sum(word) < 3^length(word)` has a negative formal
rational fixed point.  The first examples `[1]`, `[1,2]`, and `[2,1]` are
formalized as endpoints `-1`, `-5`, and `-7`.  A no-write enumeration of
primitive binary words on `{1,2}` through length `12` found `6050`
low-average periodic words, all explained by this negative phantom mechanism.
The identity `syracuseWordAffineEndpointQ_sub_formalFixedPoint` records the
deviation law `x - x_* -> (3^length/2^sum) * (x - x_*)`; the factor is proved
larger than `1` in the expanding case by
`syracuseWordExpansionFactor_gt_one_of_expanding`.
Exact no-write residue lifting for repeated patterns `[1]`, `[1,2]`,
`[2,1]`, `[1,1,2]`, `[1,2,1]`, and `[2,1,1]` shows unique compatible residue
classes and coefficientwise non-drop through repetitions `1,2,4,8,12`.  The
finite bad prefixes are therefore neighborhoods of many negative periodic
phantom endpoints, not just neighborhoods of `-1`.
A no-write exit check on the same patterns through repetitions
`1,2,4,8,12,16,20`, using suffix cap `5000`, found no drop misses after the
forced prefix.  This is only finite evidence for a possible exit/renewal
lemma.
The table-free endpoint target is formalized as `A0EndpointSuffixExit t`;
theorem `hasStrictDescent_of_a0EndpointSuffixExit` proves that any such
matched suffix descent from `593 + 1458*t` below `103 + 256*t` implies
`HasStrictDescent (103 + 256*t)`.  This is the proof-facing exit/renewal
contract independent of finite pair-table certificates.  The all-parameter
conditional wrapper is `A0EndpointSuffixExitAll`, with theorem
`hasStrictDescent_a0Cylinder_of_endpointSuffixExitAll`.
The endpoint target also has direct certificate criteria:
`a0EndpointSuffixExit_of_suffix_scaled_contracting`,
`a0EndpointSuffix_scaled_contracting_of_threshold`, and
`a0EndpointSuffixExit_of_suffix_threshold_contracting`.  These use the
endpoint affine inequality, or its threshold form with slope gap
`256*2^sum - 1458*3^length`, without assigning the suffix to a finite pair
table.  The widest no-write phantom-neighborhood probe so far checked
`62037` primitive expanding words on `{1,2,3,4}` through length `12`, repeated
`10` times, with cap `5000`; it found no misses and a smallest surplus margin
over `log2(729/128)` of about `0.001474779`.
A follow-up no-write first-barrier check found that, for all `62037`
phantom-neighborhood cases, the exit occurs exactly at the first prefix
satisfying `1458*3^L <= 256*2^A`; the endpoint threshold inequality is already
true at that first crossing.  The same rule was checked for all
`0 <= t < 2^20` under cap `1000`: all `1048576` cases exited at first
crossing, with maximum suffix length `205`.
A fixed-pattern repetition probe found that the post-periodic extra tail is
not obviously bounded: for several patterns, including `11121211212`,
`121111114121`, and `211111311111`, the extra segment reaches hundreds of
steps by `60` repetitions.  This points away from a bounded-tail automaton and
toward a first-barrier crossing theorem.
The first-barrier target is now named in Lean.  Definitions
`A0EndpointSuffixSlopeBarrier`, `A0EndpointSuffixThreshold`, and
`A0FirstBarrierSuffix` package the slope crossing, threshold inequality, and
minimality of the crossing.  The remaining two open obligations are
`A0FirstBarrierExistsAll` and `A0FirstBarrierThresholdAutomatic`; theorem
`A0EndpointSuffixExitAll_of_firstBarrier` proves that these imply
`A0EndpointSuffixExitAll`.
The length-one threshold base case is now Lean-checked:
`syracuseWordConst_append_singleton` gives the append-singleton formula for the
word numerator constant, while `a0EndpointSuffixThreshold_singleton_of_barrier`
and `a0FirstBarrierThreshold_singleton` prove automatic threshold validity for
singleton first-barrier suffixes.  This does not prove the general
`A0FirstBarrierThresholdAutomatic` obligation and does not address
`A0FirstBarrierExistsAll`.
Lean also proves threshold monotonicity in the endpoint parameter:
`a0EndpointSuffixThreshold_mono_t` and
`a0EndpointSuffixThreshold_of_one_le`.  These lemmas make the remaining
positive route precise: derive a lower bound on `t` from the matching
congruence, then move a threshold check upward by monotonicity.
The matching congruence bridge is now formalized:
`evalSyracuseWord_odd_of_matches` proves oddness of the endpoint for any
nonempty matched word, and
`padicValNat_syracuseWordAffine_of_matches` proves the exact valuation
`ν₂(3^len*n + C_word) = sum(word)`.  The specialized A0 corollary is
`padicValNat_a0EndpointSuffixAffine_of_matches` for
`n = 593 + 1458*t`.
The corresponding divisibility form is also formalized:
`syracuseWordAffine_dvd_of_matches`,
`a0EndpointSuffixAffine_dvd_of_matches`, `A0EndpointSuffixCongruence`, and
`a0EndpointSuffixCongruence_of_matches`.  The A0 congruence is
`2^sum ∣ (593*3^len + C_word) + 2*(729*3^len)*t`; no inverse modulo a power of
two is chosen at this stage.  Lemma
`a0EndpointSuffixCongruence_reducedCoeff_odd` records the oddness of the
reduced coefficient `729*3^len`.  Lemma
`a0EndpointSuffixCongruence_half_of_even_constant` proves the inverse-ready
halving step: if `sum = a+1` and
`593*3^len + C_word = 2*b`, then
`2^a ∣ b + (729*3^len)*t`.
The threshold side is now factored through
`A0EndpointSuffixThresholdWitness`: find `t0 <= t` where the endpoint threshold
already holds, then use `a0EndpointSuffixThreshold_of_thresholdWitness`.
`A0FirstBarrierThresholdWitnessAutomatic` is the corresponding first-barrier
obligation, and `A0FirstBarrierThresholdAutomatic_of_thresholdWitness` connects
it back to the earlier target.
The first-barrier package now carries the congruence explicitly:
`a0FirstBarrierSuffix_congruence`,
`A0FirstBarrierCongruenceThresholdWitnessAutomatic`, and
`A0FirstBarrierThresholdWitnessAutomatic_of_congruence` reduce the
threshold-side task to proving
`first-barrier + A0 linear congruence => threshold witness`.
The slope-only route is also Lean-checked as insufficient:
`a0NaiveSlopeBarrierCounterexampleWord` crosses the slope barrier, while
`a0NaiveSlopeBarrierCounterexample_thresholdZeroFails` proves that the endpoint
threshold inequality fails at `t = 0`.  A no-write lift of the exact matching
constraints for this word gives the unique residue
`t == 237364345562 (mod 2^39)`; the threshold itself needs only `t >= 1`.
Thus the remaining longer-suffix threshold proof must exploit
`SyracuseWordMatchesFrom` congruence information, not slope data alone.
Lean now proves this repair for the concrete word as
`a0NaiveSlopeBarrierCounterexample_threshold_of_match`: matching forces the
first exponent to be `4`, which rules out `t = 0`; the threshold then follows
from the `t = 1` check and monotonicity.
Decision recorded 2026-06-04: do not treat further finite `T` audits or weak
operator estimates as a path to the pointwise Collatz statement.  The
Collatz-relevant continuation is the pointwise first-barrier branch.  Its hard
gate is the aperiodic obstruction: periodic phantom shadowing is excluded by a
fixed-point equation, but an aperiodic infinite valuation word has only a
2-adic limit `ξ_W` and no currently known algebraic rigidity excluding
`ξ_W ∈ ℕ_{>0}`.  The next mathematical test is whether first-barrier minimality
plus the A0 congruence/threshold package gives a constraint on aperiodic
`ξ_W` beyond the classical parity-vector residue description.  If it does not,
the pointwise branch should be presented as an exact isolation of the classical
aperiodic obstruction, not as a claimed proof route.
The periodic side of this boundary is now Lean-checked in post-prefix form:
`NoInfinite.lean:no_positive_endpoint_eventually_periodic_expansive_congruence`
excludes any positive natural endpoint from shadowing an expansive phantom
period congruentially for all period counts.  This is a theorem about
eventually periodic expansive behavior only; it does not touch aperiodic
infinite valuation words.
Generated Lean also includes one feasibility row,
`a0SemanticSuffixPairCertificateT14ThresholdMax`, for the worst observed T14
threshold pair `(suffix_len,suffix_sum)=(35,58)`; theorem
`a0SemanticSuffixPairCertificateT14ThresholdMax_valid` verifies the exact
`ValidAt455` arithmetic.  The one-row list
`a0SemanticSuffixPairCertificatesT14Prototype` passes
`A0SemanticSuffixPairCertificate.allValidAt455Bool` by `native_decide`.
The full T14 pair-compressed table is now imported as
`a0SemanticSuffixPairCertificatesT14`; Lean verifies its row count `351` and
the theorem `a0SemanticSuffixPairCertificatesT14_allValid` by `native_decide`.
Theorem `a0SemanticSuffixPairCertificatesT14_matches_summary` ties the table
row count and threshold maximum back to the compact audit summary.
The use theorem `hasStrictDescent_of_mem_a0SemanticSuffixPairCertificatesT14`
turns membership in this table, concrete suffix length/sum/constant bounds,
and the common-prefix word match into `HasStrictDescent`.
The assignment structure `A0SemanticSuffixT14PairCover` packages one concrete
suffix-to-table-row proof, and theorem
`hasStrictDescent_of_a0SemanticSuffixT14PairCover` is the corresponding local
descent bridge.  The finite coverage summary
`a0SemanticSuffixT14PairCoverageSummariesV2Lt8Cap100` verifies, for
T12/T13/T14, that all `14348` observed distinct suffix rows and all `102488`
drop samples are covered by the T14 pair table, with zero missing-pair,
constant-bound, or threshold-bound failures.  This is still finite-prefix
coverage only.
The source-level target `A0SemanticDropSourceT14PairCover` packages exactly
what remains to prove for a concrete source in the semantic-drop path:
positivity/oddness/non-one, a suffix-to-T14-pair cover, and the common-prefix
word match.  Theorem `hasStrictDescent_of_a0SemanticDropSourceT14PairCover`
then gives `HasStrictDescent`.  The finite source accounting summary
`a0SemanticDropSourceT14CoverageSummariesV2Lt8Cap100` records all `102488`
observed semantic-drop source samples through T12/T13/T14 as covered, with
zero finite source-coverage failures.
Script `126_A0_return_branch_affine_probe.py` now supports this as an
opt-in audit through `--semantic-replay-step-cap`; the flag adds replay
counters to `stats` without altering the return-branch rows or default
behavior.  Verified no-write on the complete `T14` prefix:
`semantic_replay=step_cap:100,drop:58532,return:6748,valuation_tail:0,step_tail:0,loss:0,loss_free:1`
and `semantic_replay_step_max=drop:91,return:75,valuation_tail:0,step_tail:0`.
A direct no-write `analyze(...)` verification of the modified script gives:
`T12` semantic `(drop, return, loss_free, drop_step_max, return_step_max) =
(14668, 1652, 1, 68, 51)`;
`T13 = (29288, 3352, 1, 91, 73)`;
`T14 = (58532, 6748, 1, 91, 75)`.
Lean imports this as `a0SemanticReplaySummariesV2Lt8Cap100` and theorem
`a0SemanticReplayV2Lt8Cap100_loss_free`, proving the finite cap-100 replay
summary: total `114240`, drop `102488`, return `11752`, valuation-tail `0`,
step-tail `0`, max drop/return steps `91/75`, and resolved finite outcome
accounting.  It is explicitly separate from the conservative cap-75 outcome
summary.  The comparison theorem
`a0SemanticReplayV2Lt8Cap100_reclassifies_conservative_tails` proves that
the semantic replay keeps the same finite total and return count, while moving
exactly the conservative `860` tail samples into the drop count.  This remains
a finite replay check, not an infinite cover.
Latest checked bridge build after first-barrier packaging:
`lake build CollatzShadowing.CollatzBridge` completed with `3291` jobs
(latest run `150s` after the conditional halving congruence).  Latest checked
dependent and aggregate builds:
`lake build CollatzShadowing.NoInfinite` completed with `1798` jobs
(latest run `59s` after the post-prefix eventually-periodic boundary theorem),
`lake build CollatzShadowing.Generated.A0ReturnBranches` completed with
`3292` jobs (latest run `142s`), and `lake build CollatzShadowing` completed
with `3350` jobs (latest run `86s`).

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
return-coverage failures.  The generated theorem
`a0CompletePrefixSummariesV2Lt8_declared_tail_counts` extracts the
residual tail counts (`844`, `16`, total `860`), and
`a0CompletePrefixSummariesV2Lt8_declared_tail_positive` records that this
finite prefix summary is not loss-free.  This is an exact finite balance
sheet, not a claim that the tails vanish in any limiting regime.
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
