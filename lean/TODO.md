# Lean 4 Formalization Plan — Collatz Spectral Reduction

## Verifiche manuali documentazione Wiki.js — 2026-06-10

Questa sezione e stata aggiunta durante la generazione della struttura
documentale per Wiki.js.

- [x] Eseguire build completo:
  `/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build`.
  Verificato il 2026-06-10: `Build completed successfully (3350 jobs).`
- [ ] Salvare screenshot del build riuscito in
  `docs/assets/screenshots/lake-build-success.png`.
- [x] Eseguire controllo placeholder:
  `rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"`.
  Verificato il 2026-06-10: nessuna occorrenza.
- [ ] Salvare screenshot del controllo placeholder in
  `docs/assets/screenshots/no-placeholders-check.png`.
- [ ] Salvare screenshot della struttura progetto in
  `docs/assets/screenshots/project-structure.png`.
- [ ] Importare o sincronizzare `docs/wiki-source.md` in Wiki.js.
- [ ] Inserire in `docs/wiki-source.md` l'URL/IP reale della istanza Wiki.js.
- [ ] Verificare, script per script, la procedura precisa di rigenerazione dei
  moduli in `CollatzShadowing/Generated/`.

This document is the operational plan for formalizing the mathematical
content of [`paper/collatz_spectral_reduction.tex`](../paper/collatz_spectral_reduction.tex)
in **Lean 4** with **Mathlib**.

The goal of this phase of the research program (see
[`METHODOLOGY.md`](../METHODOLOGY.md)) is to produce a machine-verified
proof of **Lemma 3.1** (the exact congruential shadowing lemma) and,
ideally, also Corollary 3.4 (no infinite shadowing). These two results
together would constitute the formally verified core of the paper.

A revised preprint (`v2`) will incorporate the formalized statements
once complete, and only then will the work be sent to external
reviewers.

---

## How to use this document (instructions for AI assistants)

This file is shared across multiple AI assistants and human sessions.
**Read this section before doing anything else.**

### Reading order for an AI starting fresh

1. Read this entire `TODO.md` once.
2. Read `../METHODOLOGY.md` to understand the broader research program.
3. Read the relevant section of `../paper/collatz_spectral_reduction.tex`
   (Section 3 for the shadowing lemma, Section 5 for the operator,
   Section 6 for the bound).
4. Read the latest entry in the **Session log** at the bottom of this
   file to know what the previous session accomplished.
5. Identify the next pending task (status `[ ]`) whose prerequisites are
   all done (`[x]`).

### Updating the document

When you complete or partially advance a task:

1. Update the task's status marker. Use:
   - `[ ]` — not started
   - `[~]` — in progress (with a note explaining what is partial)
   - `[x]` — done (with a brief description of the artifact produced)
   - `[!]` — blocked (with explanation of the blocker)
2. Add an entry at the top of the **Session log** describing what you
   did, what you learned, and what the next session should focus on.
3. Commit changes to git with a clear message indicating the task ID.

### Contribution conventions

- Every file under `lean/` has a header comment indicating which AI
  wrote or substantially modified it, and the date.
- Each `theorem` or `lemma` declaration that is formalized from the paper
  must have a comment referencing the paper section it formalizes (e.g.
  `-- Paper Section 3, Lemma 3.1`).
- Use `sorry` placeholders generously when stating theorems before
  proving them. A compiling file with `sorry` is more useful than a
  non-compiling file without.
- Prefer Mathlib lemmas over hand-rolled ones. If you find yourself
  re-deriving something, search Mathlib first (e.g. via
  `exact?`, `apply?`, `loogle` or the
  [Moogle](https://www.moogle.ai) search).

### Known limitations of AI assistants on Lean

- Lean 4 syntax has evolved significantly; AIs trained on older corpora
  often produce Lean 3 syntax that will not compile. **Always run
  `lake build` to verify.**
- Mathlib is large and changes frequently. Lemma names may have moved.
  When a name lookup fails, search the current Mathlib repo.
- The `sorry` keyword silently allows proofs to typecheck. The
  successful end state is **`lake build` succeeds with zero `sorry`
  warnings** for a target file.

---

## Current status (most recent first)

> *Last updated: 2026-05-28 — **Phase 5 complete: Lemma 3.1 and Corollary 3.4 formalized**. Project is `sorry`-free. **Phase 6 complete**: paper v2 drafted, Lean note written, Related Work + Chang comparison done, GitHub README updated, METHODOLOGY.md updated, Zenodo v2 published, and `pdflatex` verified online by Piero. **Phase 7 complete for the current branch**: tasks 7.1-7.4, 7.6, and 7.7 are complete; 7.4 closes with the full `K0=16` sampled run and SCC report, outcome (b), so 7.5 is not applicable. **F.1 is closed for the declared finite residue-cell scope and imported in Lean**: `deterministic_residue_transfer.py` enumerates all `2^4` finite residue subclasses for each of the 1240 raw SCC source states, writes exact deterministic transition matrices, and the `(K,b)` matrix has a generated Lean/Python exact CW certificate with max ratio `90833233962213/129559208330288 < 3/4`; sensitivity checks at `lift_bits = 5, 6` also stay below `3/4`. **Phase 8 complete for the current branch**: 8.1-8.9 are complete; 8.3 closes on the generated 37-state compressed `K,b` SCC certificate; 8.5 has the matrix/decomposition API, a generated exact import of the empirical `T = 10` critical-symbolic full transfer matrix, and an exact generated `T = 10, j = 32` majority `core/tail` `OperatorDecomposition`; 8.6 connects finite CW certificates to Mathlib `spectralRadius`; 8.7 exposes the `T = 10, j = 32` numerical spectral-radius bound `97/2000 = 0.0485` through a fully expanded Lean-checked 224-row CW certificate generated from the exact CSV. **Phase 9 complete**: paper v3 redaction and publication were completed externally by Piero; v3 DOI/record `10.5281/zenodo.20160154` / `https://zenodo.org/records/20160154`. **Phase 10 A0 weak branch reopened**: the finite row-L1 bridge is formalized in `CollatzShadowing/WeakBridge.lean`; the high-`v2` source-tail mass is now both an exact count and a real mass estimate with Lean theorems `WeakBridge.TailCount.dyadic_tail_count_mul_le` and `WeakBridge.TailCount.dyadic_tail_mass_le`; the general finite low/tail split is formalized as `WeakBridge.FiniteSplit.weighted_sum_le_low_plus_tail`; the `delta_only` reduction is formalized as `WeakBridge.FiniteSplit.weighted_dyadic_delta_boundary_le`; first bit-length infrastructure is formalized as `WeakBridge.BitLength.bitLength_two_mul`, same-window add/sub lemmas, dyadic-boundary crossing lemmas, endpoint-union bounds, affine endpoint-union bounds, `WeakBridge.BitLength.affineDelta_period_eq_of_not_mem_badSet`, `WeakBridge.BitLength.biAffineDelta_period_eq_of_not_mem_badSet`, `WeakBridge.BitLength.biAffineDelta_dyadicWeight_period_boundary_le`, and `WeakBridge.BitLength.biAffineDelta_refine`; script `126` now records exact valuation-word cylinder arithmetic, an affine no-drop prefix certificate, destination-refined bi-affine return branches, and an exact congruence diagnostic for the `best_shadow` label gate. Through complete prefixes `T12/T13/T14`, formula/delta/word/no-drop/refined failures remain zero, no final competitor phantom is detected, and the target high-lift boundary is converted into an exact continuation branch: all rows have high-lift continuation support, step delta exactly `+6`, and zero integrality/no-drop failures. Lean still imports the open label-gate count `6628`, now attributable to possible intermediate phantom-label congruences plus the high-lift boundary bookkeeping. Script `125` complete-prefix period-shift runs through `T14` remain entirely `delta_only`, with no destination/drop/tail boundary. The next open proof target is splitting/controlling the intermediate visible-label congruence families in an automaton-aware way.*

Latest Phase-10 reduction: the intermediate label obstruction is now split
in Lean.  Across `T12/T13/T14`, target visibility contributes `92`,
competitor visibility contributes `1244`, and the per-record totals are
`k10c1=8`, `k11c1=896`, `k12c1=340`, `k12c2=92`, `k20c1=0`.  Multi-probe
diagnostics test `10688` shifted representatives with zero early target
returns; the target-intermediate subprobe is `736/736` same-step.  The eight
`T14` competitor no-return-by-final multiprobe cases are all `(12,1)` and
all return to target later with step delta `+6`; they are a continuation
boundary, not an early-return obstruction.  The naive unrefined affine
continuation over the eight-shift class fails integrality in all eight
cases; tracing the actual late-return word gives prefix/suffix agreement,
and a further finite four-bit refinement supports all eight continuations
with zero refined failures.  This is imported in Lean as
`a0CompletePrefixSummariesV2Lt8_intermediate_multiprobe_no_return_actual_refined`;
the target-intermediate structure is also imported as
`a0CompletePrefixSummariesV2Lt8_intermediate_target_visibility_structure`
with persistent target visibility `0`, missing-prior target visibility
`92`, no-prior-competitor intersections `92`, and prior-competitor
intersections `0`; all `92` target-intermediate classes are covered by
target high-lift visibility (`b >= 2`) and zero are low-only target
`b = 1` classes.  These are still finite diagnostics, not an infinite
first-return theorem.  Combining the current exact split criteria gives a
finite imported split-resolution certificate for all `5292` branch rows
across the three complete-prefix summaries, theorem
`a0CompletePrefixSummariesV2Lt8_label_split_resolution_certificate`.
This finite certificate is now factored through the abstract Lean schema
`WeakBridge.LabelSplit.BranchCounters` / `SummaryCounters`; the generated
A0 summary proves
`a0CompletePrefixSummariesV2Lt8_label_split_summary_resolved`.  The
conditional cover bridge is also formalized abstractly:
`WeakBridge.LabelSplit.BranchCover`, `BranchPartition`,
`sourceResolved_of_all_branches_resolved`, and
`partition_sourceResolved_of_all_branches_resolved` state that once a
source space is covered by resolved branch labels, every covered source is
resolved in the finite label-split sense.  This still does not construct
the Collatz/A0 infinite cover.  For the complete finite prefixes, Lean now
also imports a return-sample partition summary:
`a0CompletePrefixSummariesV2Lt8_return_partition_summary_resolved` proves
that the branch-row sample counts cover all `11752` finite return samples
with zero coverage failures.  The same finite accounting is now lifted to
the complete prefix outcome decomposition.  `WeakBridge.LabelSplit.OutcomeSummary`
records total samples, covered return samples, drop samples,
	valuation-tail samples, and step-tail samples; the generated theorem
	`a0CompletePrefixSummariesV2Lt8_outcome_decomposition_resolved` proves
	for the imported `T12/T13/T14` summaries that
	`11752 + 101628 + 844 + 16 = 114240`, with covered return samples equal
	to all finite return samples and zero return-coverage failures.  This is
	only a finite prefix balance sheet; the nonzero tails are not eliminated
	by this theorem.  The generated theorem
	`a0CompletePrefixSummariesV2Lt8_declared_tail_counts` extracts the
	declared residual tail counts (`844`, `16`, total `860`), and
	`a0CompletePrefixSummariesV2Lt8_declared_tail_positive` records that this
	finite prefix summary is not loss-free.

The direct-return descent route has now been ruled out for the current
script-126 complete-prefix return rows.  A read-only JSON audit of
`T12/T13/T14` found zero coefficientwise decreasing return branches in
either the base coordinates or the destination-refined coordinates: all
`860/1564/2868` rows satisfy `a >= q` and `b >= r`, and all refined rows
satisfy `refined_a >= refined_q` and `refined_b >= refined_r`.  The minimum
base slope ratio is `531441/524288 > 1`, and every row is strictly
expansive in at least one coefficient.  Lean now contains the generic
negative lemma `AffineTBranch.not_nextLocalInteger_lt_sourceLocalInteger_of_coeffNondecreasing`:
a branch with `source_t = q*u+r`, `next_t = a*u+b`, `a >= q`, `b >= r`
cannot by itself be a strict descent in the same fixed local residue
coordinate.  This does not prove an infinite theorem, but it prevents a
false proof strategy: concatenating only these same-coordinate A0 return
branches cannot supply the endpoint descent required by
`BranchTransitionChainDropSound` unless some later mechanism leaves this
monotone return class or reaches a genuine drop/loss redirection.

The complementary direct-drop audit is positive on the same finite
complete-prefix artifacts.  Reconstructing the script-126 traces in read-only
mode, the finite `drop_samples` group into exact `(phase, word)`
congruence classes with a source affine integer and endpoint affine integer.
For `T12/T13/T14`, all `9032/16692/30900` drop groups have integer endpoint
formulae and satisfy the coefficientwise drop condition on the whole
observed congruence progression, covering exactly `14548/29040/58040`
finite drop samples with zero bad groups and zero noninteger groups.  Lean
now has the generic arithmetic certificate
`AffineNatDropBranch.targetN_lt_sourceN_of_coeffDrop`, which proves
`targetSlope*u + targetIntercept < sourceSlope*u + sourceIntercept` from
`targetSlope <= sourceSlope` and `targetIntercept < sourceIntercept`.  This
is connected to the Syracuse-word bridge by
`directDropAt_of_word_matches_affineNatDrop`: a matched word plus source and
endpoint affine equalities plus this coefficientwise drop certificate gives
`DirectDropAt`.  This is the right local shape for future
`DirectDropAtSound`, but it is still only local arithmetic plus finite
reconstruction: it does not prove that the finite prefix classes form an
infinite A0/Collatz cover, and it does not remove the declared
valuation/step tails.

The declared tail taxonomy has also been sharpened.  A read-only replay of
script-126 traces shows that every finite `valuation_tail` in
`T12/T13/T14` is already below the original start immediately after the
high-valuation step: `120/120`, `240/240`, and `484/484`.  These were
classified as tails because script `126` checks `a_val > a_cap` before
checking `cur < n0`.  Lean now proves the general one-step arithmetic lemma
`syracuse_lt_self_of_two_le_exponent`: if `1 < n` and
`2 <= syracuseExponent n`, then `S n < n`.  This gives a plausible
redirection path for valuation-tail classes, subject to proving the
intermediate value is `> 1` and matching the actual step in the global
source model.  The wrapper
`directDropAt_one_of_two_le_syracuseExponent` packages the same fact as
`DirectDropAt 1 n`, the form required by `DirectDropAtSound`.  The
`step_tail` samples are different: the replay finds
`0/8` and `0/8` final drops at the original cap `75`.  Extending only those
eight representatives to cap `100` shows they are budget artifacts rather
than new observed obstruction classes: the four `t = 4853` cases
(`phase = 0|1|h`, `h=0..3`) drop at step `91`, and the four `t = 7110`
cases (`phase = 1|3|h`, `h=0..3`) drop at step `76`.  This finite replay
suggests cap extension can remove the current prefix `step_tail` counts,
but it is not an infinite no-budget-exit theorem.
With the semantically corrected priority "drop before valuation-tail" and
cap `100`, the same read-only replay has no residual finite losses:
`T12 = 14668` drops plus `1652` returns, `T13 = 29288` drops plus `3352`
returns, and `T14 = 58532` drops plus `6748` returns.  This should guide
the next generated artifact, but it does not by itself replace the existing
Lean import, which still records the conservative cap-75 outcome summary.
Script `126` now has an opt-in `--semantic-replay-step-cap` flag that
records exactly these proof-facing replay counters in `stats` without
changing the return-branch rows or the default output policy.  A no-write
`T14` run with `--semantic-replay-step-cap 100` reports
`semantic_replay=step_cap:100,drop:58532,return:6748,valuation_tail:0,step_tail:0,loss:0,loss_free:1`
and `semantic_replay_step_max=drop:91,return:75,valuation_tail:0,step_tail:0`.
A direct no-write call to `analyze(...)` verifies all three complete
prefixes with the modified script: `T12` has max semantic drop/return steps
`68/51`, `T13` has `91/73`, and `T14` has `91/75`, all with
`semantic_replay_loss_free = 1`.
Lean imports this as the separate semantic-replay summary
`a0SemanticReplaySummariesV2Lt8Cap100` and theorem
`a0SemanticReplayV2Lt8Cap100_loss_free`: total `114240`, drop `102488`,
return `11752`, valuation-tail `0`, step-tail `0`, max drop/return steps
`91/75`, and resolved finite outcome accounting.  This theorem is finite
and cap-specific; it does not assert an infinite loss-free cover.

- **Phase 0 complete.** Lake project initialized with `math` template,
  pinned to **Lean 4 v4.29.1** and **Mathlib v4.29.1**. Mathlib
  precompiled cache downloaded (~7 GB in `lean/.lake/`). `lake build`
  succeeds on the placeholder file `CollatzShadowing/Basic.lean`.
- **Phase 1 complete.** `CollatzShadowing/INVENTORY.md`
  documents the relevant Mathlib API for `padicValNat`, `multiplicity`,
  `padicNorm`, `Padic`, `PadicInt`, coercions, and the chosen
  congruence model in `ℤ_[2]`. `CollatzShadowing/Inventory.lean` is the
  corresponding typechecked Lean scratch buffer.
- **Phase 2 Basic definitions complete.** `CollatzShadowing/Basic.lean`
  now defines the accelerated Syracuse map `S`, aliases for `ν₂` on
  `ℕ`, `ℤ`, `ℚ`, and the Mathlib valuation on `ℤ_[2]`.
- **Task 2.4 complete.** `CollatzShadowing/Phantom.lean` defines
  `structure PhantomWord` (nonempty list of positive naturals), with
  projections `length` and `A` (per-period exponent sum).
- **Tasks 2.5 + 2.6 complete.** Same file now defines
  `affineFoldStep`, the `(C_j, A_j)` fold from eq. (3.1), the named
  coefficients `Cw`, `Aw`, the equality `Aw_eq_A`, and the affine
  Syracuse map `S_w : ℤ_[2] → ℚ_[2]` (the codomain is `ℚ_[2]`, not
  `ℤ_[2]`, since `2` is not a unit in `ℤ_[2]`; this matches the
  recommendation in `INVENTORY.md` Open Gaps).
- **Tasks 2.7 + 2.8 complete.** `Phantom.lean` adds `aAt` (periodic
  extension), `B` (periodic partial sum, closed-form
  `(m/L)·A + sum (take (m%L) vals)`), `qwRat` (rational fixed point),
  the `QwOddDen` hypothesis, and `qwZ2` (the `ℤ_[2]` representative
  parameterised by that hypothesis).
- **Task 2.9 complete.** New file `CollatzShadowing/Shadowing.lean`
  contains `PadicCongruentModPow2` (ideal-membership formulation per
  INVENTORY §1.4) and the statements `exact_shadowing` and
  `exact_shadowing_periods` (Lemma 3.1 and its periodic specialisation),
  both with `:= sorry`. `lake build` succeeds with exactly two
  expected `sorry` warnings.
- **Phase 2 is now complete.**
- **Phase 3 partially advanced (3.1, 3.1.5, 3.4 proved).** New file
  `CollatzShadowing/Auxiliary.lean` contains:
  * `valuation_three_z2` — `(3 : ℤ_[2]).valuation = 0` (helper for 3.1).
  * `nu2Z2_three_mul` — Task 3.1, `ν₂(3·n) = ν₂(n)` for `n ∈ ℤ_[2]`.
  * `length_le_A`, `one_le_Aw` — structural facts on `PhantomWord`.
  * `qwIntDen`, `qwIntDen_odd`, `qwRat_eq_divInt` — bridge to integer
    arithmetic.
  * `qwOddDen` — Task 3.1.5, every phantom has odd `qwRat.den`. The
    `QwOddDen` hypothesis carried in the Lemma 3.1 statement is now
    discharged unconditionally for any `PhantomWord`.
  * `B_succ`, `B_bound_iff` — Task 3.4, the periodic-recursion identity
    and the `B_m + 1 − B_j ≥ a_j + 1 ↔ B_m ≥ B_{j+1}` equivalence.
  * Tasks **3.2, 3.3 remain pending** — both require extending the
    Syracuse map `S` to `ℤ_[2]`, which is non-trivial infrastructure
    work.
- Phase-2 cleanup made during Phase 3: `PhantomWord.B` was refactored
  from the closed form `(m/L)·A + sum (take (m%L) vals)` to the
  literal sum form `((List.range m).map aAt).sum`. This makes `B_succ`
  one rewrite. The closed form has since been restored as the proved
  theorem `PhantomWord.B_closed_form` in `Auxiliary.lean`.
- **Paper-faithful 2-adic infrastructure landed.** New file
  `CollatzShadowing/Syracuse2Adic.lean` defines
  `Syracuse2adic : ℤ_[2] → ℤ_[2]`, the natural extension of the
  accelerated Syracuse map to the 2-adic integers, and proves the
  bridge `Syracuse2adic_natCast` connecting it to the integer-level
  `S : ℕ → ℕ`. The construction uses `PadicInt.unitCoeff` and a
  documented total extension at the degenerate point `x = -1/3`.
- `Shadowing.lean` refactored: `exact_shadowing` and
  `exact_shadowing_periods` now state Lemma 3.1 in the paper-faithful
  form `ν₂Z2 (3 · Syracuse2adic^[j] x + 1) = aAt w j`, and the
  `QwOddDen` hypothesis is now discharged automatically via
  `PhantomWord.qwOddDen`.
- Tasks 3.2 and 3.3 now have paper-faithful statements (with `sorry`)
  in `Auxiliary.lean`, ready for proof.
- **Phase 3 complete.** Tasks 3.2 and 3.3 are proved.
- **Phase 4 complete: Lemma 3.1 (paper Section 3) is fully formalized
  in Lean 4 + Mathlib.** Both `exact_shadowing` (the main theorem) and
  `exact_shadowing_periods` (the periodic specialisation) are proved
  with zero `sorry`s. The project as a whole is `sorry`-free.
- The matching property of `q_w`'s own orbit is now proved as
  `qw_orbit_matches`, and `exact_shadowing` no longer carries
  `h_qw_matches` as a hypothesis.
- **Phase 5 complete.** The periodicity identity
  `B_mul_period : B (b · L) = b · A` is proved, and
  `exact_shadowing_periods` now uses the paper's congruence bound
  `b · A` rather than `B (b · L)`. `NoInfinite.lean` formalizes the
  no-infinite-shadowing corollary for expansive phantoms.

---

## Folder layout (target)

```
lean/
├── lakefile.toml             Lake build configuration
├── lean-toolchain            Lean 4 version pin
├── lake-manifest.json        auto-generated dependency lock
├── README.md                 Lean-side README, build instructions
├── TODO.md                   this file
├── CollatzShadowing.lean     project entry point (re-exports modules)
└── CollatzShadowing/
    ├── Basic.lean            ν₂, accelerated Syracuse map S
    ├── Phantom.lean          phantom words, q_w, S_w
    ├── Shadowing.lean        Lemma 3.1 and proof
    ├── NoInfinite.lean       Corollary 3.4
    └── CollatzBridge.lean    conditional descent-to-Collatz bridge
```

Files under `CollatzShadowing/` may be split further as proofs grow.

---

## Phase 0 — Project setup

Acceptance: a `lake build` from the `lean/` directory succeeds with an
empty placeholder file. This validates that Lean and Mathlib are
correctly installed.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 0.1 | [x] | Install **elan** (Lean toolchain manager) on the development machine. | `elan 4.2.1` installed in `/Volumes/AFUOCO/MAC/Applicazioni/elan`. |
| 0.2 | [x] | Initialize a Lake project in `lean/` named `CollatzShadowing`. | `lakefile.toml`, `lean-toolchain` (v4.29.1), `CollatzShadowing.lean`, `CollatzShadowing/Basic.lean` all created by `lake init CollatzShadowing math`. |
| 0.3 | [x] | Add **Mathlib** as a dependency with the `lake-manifest.json` resolved. | `lakefile.toml` requires mathlib v4.29.1; manifest resolved by `lake update`; Mathlib precompiled cache fetched via `lake exe cache get` (~7 GB in `.lake/`). |
| 0.4 | [x] | Verify the project builds. | `lake build` succeeds on placeholder. |
| 0.5 | [x] | Add a `README.md` in `lean/` with build instructions. | `lean/README.md` was committed before Phase 0 began; build instructions still valid with Lake-generated layout. |
| 0.6 | [x] | Commit Phase 0 to git. | Commit referenced in session log below. |

Notes:
- elan installation: `curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh`
- Lake project init: from `lean/`, run `lake init CollatzShadowing math` (the `math` template adds Mathlib as dependency).
- First `lake build` will download and compile Mathlib (~10–30 min, several GB).

---

## Phase 1 — Mathlib infrastructure inventory

Acceptance: a written inventory of which Mathlib API we will use and
which gaps we must fill ourselves. This phase is mostly research, not
coding.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 1.1 | [x] | Locate Mathlib's API for `padicValNat`, `multiplicity`, and `padicNorm`. | `CollatzShadowing/INVENTORY.md` lists relevant imports and lemma names. |
| 1.2 | [x] | Locate Mathlib's `Padic`, `PadicInt`, `Padic.valuation`. | `Padic`, `PadicInt`, `Padic.valuation`, `PadicInt.valuation`, and valuation lemmas documented. |
| 1.3 | [x] | Find how to coerce `ℚ → ℚ_2` and `ℤ → ℤ_2` in Mathlib. | Working snippets documented, including rational-to-`ℤ_[2]` when the denominator is odd. |
| 1.4 | [x] | Identify how to express congruence `n ≡ q (mod 2^k)` when `q ∈ ℚ` (or, equivalently, in `ℤ_2`). | Use ideal membership `x - y ∈ Ideal.span {((2 : ℤ_[2]) ^ k)}`; type-checked equivalence with valuation in the nonzero case documented. |
| 1.5 | [x] | Document gaps and approaches in `lean/CollatzShadowing/INVENTORY.md`. | `INVENTORY.md` written; `Inventory.lean` rebuilt as the typechecked scratch buffer. |

Note on 1.4: this is the single most subtle modeling question. The paper
states `n ≡ q_w (mod 2^(bA+1))` where `n ∈ ℕ` and `q_w ∈ ℚ`. The most
natural formalization uses `ℤ_2` (the 2-adic integers) and asserts the
congruence as `(n : ℤ_2) - (q_w : ℤ_2) ∈ (2^(bA+1)) * ℤ_2`. This must
be verified to match the paper's intended meaning before Phase 2.

---

## Phase 2 — Basic definitions (no proofs yet)

Acceptance: all definitions referenced in Lemma 3.1 exist in the Lean
codebase, and the lemma statement compiles with `sorry` as proof.

| ID | Status | Task | File | Acceptance criterion |
|----|--------|------|------|----------------------|
| 2.1 | [x] | Define accelerated Syracuse map `S : ℕ → ℕ` for odd inputs. | `Basic.lean` | `#check CollatzShadowing.S` works. |
| 2.2 | [x] | Define `ν₂` (alias for `padicValNat 2`). | `Basic.lean` | `#check CollatzShadowing.ν₂` works. |
| 2.3 | [x] | Extend `ν₂` to `ℤ_2 \ {0}` (Mathlib should already cover this). | `Basic.lean` | `nu2Z2` and `ν₂Z2` wrap `PadicInt.valuation`; `#check CollatzShadowing.nu2Z2` works. |
| 2.4 | [x] | Define `PhantomWord := List ℕ` with a positivity constraint on each entry. | `Phantom.lean` | `structure PhantomWord` with `vals`, `nonempty`, `positive` fields plus `length`/`A` projections; `#check CollatzShadowing.PhantomWord` succeeds. |
| 2.5 | [x] | Define affine map `S_w` for a phantom word `w`. | `Phantom.lean` | `S_w : PhantomWord → ℤ_[2] → ℚ_[2]`. Acceptance check: for `w = [1]`, `S_w x = (3·x + 1)/2` in `ℚ_[2]` (proved by `simp` from the unfolded fold). Note: codomain is `ℚ_[2]`, not `ℤ_[2]`, since `2` is not a unit in `ℤ_[2]`. |
| 2.6 | [x] | Define `C_w` and `A_w` via the recursion of paper eq. (3.1). | `Phantom.lean` | `affineFoldStep`, `affineCoeffs`, `Cw`, `Aw` defined; `Aw_eq_A` proves `Aw w = w.A`. For `w = [1]`: `Cw = 1`, `Aw = 1` by `rfl` (matches paper). |
| 2.7 | [x] | Define `q_w := C_w / (2^A_w - 3^L)` as an element of `ℤ_2` (when defined). | `Phantom.lean` | `qwRat : PhantomWord → ℚ` (smoke-checked: `qwRat phantomOne = -1`), `QwOddDen` hypothesis, `qwZ2 : (w : PhantomWord) → QwOddDen w → ℤ_[2]` via `Padic.norm_rat_le_one`. Proof of `QwOddDen` for expansive phantoms deferred to Phase 3. |
| 2.8 | [x] | Define partial sum `B_m := List.take m (cycle w)).sum`. | `Phantom.lean` | `B w m := (m/L)·A + sum (take (m%L) vals)`; `aAt w j := vals.getD (j%L) 0` (the periodic extension `a_j`). Smoke-checked: `phantomOne.B m = m`, `phantomOne.aAt j = 1`. |
| 2.9 | [x] | State Lemma 3.1 with `:= sorry` proof. | `Shadowing.lean` | New file with `PadicCongruentModPow2`, `exact_shadowing`, `exact_shadowing_periods`. `lake build` succeeds with only the two intentional `sorry`s. |

---

## Phase 3 — Auxiliary lemmas

Acceptance: each auxiliary lemma needed for the inductive proof of
Lemma 3.1 is stated and proved.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 3.1 | [x] | `ν₂(3·n) = ν₂(n)` for `n ∈ ℤ_2`. | `Auxiliary.lean:nu2Z2_three_mul` — proved, no `sorry`. Routed via `valuation_three_z2` (computed by going through `Padic.valuation_natCast` and `padicValNat.eq_zero_of_not_dvd`) and `PadicInt.valuation_mul`. |
| 3.1.5 | [x] | Prove `QwOddDen w` for every phantom word (no expansive hypothesis needed: 2^A_w − 3^L is non-zero and odd whenever L ≥ 1, A_w ≥ 1). | `Auxiliary.lean:qwOddDen` — proved, no `sorry`. Strategy: `qwIntDen w := 2^A_w − 3^L`, parity via `Even.sub_odd`, then bridge to `(qwRat w).den` through `Rat.divInt_eq_div`, `Rat.den_dvd`, `Int.natCast_dvd`, `Odd.of_dvd_nat`. The `QwOddDen` hypothesis in `exact_shadowing` is now dischargeable for any `PhantomWord`. |
| 3.2 | [x] | After matching the prefix `(a_0, ..., a_{j-1})`, the difference `S^j(n) - S^j(q_w)` is `(3^j / 2^{B_j}) · (n - q_w)` in `ℚ_[2]`. | `Auxiliary.lean:affine_difference` — proved by induction on `j`, using `syracuse_one_step_diff` (per-step formula via `Syracuse2adic_spec` + `linear_combination` in `ℚ_[2]`) and `B_succ`. |
| 3.3 | [x] | If `ν₂(x - y) ≥ a_j + 1`, then `ν₂(3·x + 1) = ν₂(3·y + 1)` and equals `a_j` for both. | `Auxiliary.lean:nu2_stable_under_proximity` — proved via custom strict ultrametric `valuation_add_eq_left_of_lt` (built from `le_valuation_add` + contradiction with `valuation_z2_neg`). |
| 3.4 | [x] | The condition `B_m + 1 - B_j ≥ a_j + 1` is equivalent to `B_m ≥ B_{j+1}`. | `Auxiliary.lean:B_bound_iff` — proved, `omega` once `B_succ` (the recursion identity for the sum-form `B`) is in place. `Phantom.lean` was refactored: `B m := ((List.range m).map aAt).sum` makes `B_succ` a one-rewrite. |

---

## Phase 4 — Proof of Lemma 3.1

Acceptance: `lake build CollatzShadowing.Shadowing` succeeds with
zero `sorry`s in `Shadowing.lean`.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 4.1 | [x] | Write the induction skeleton on `j` from `0` to `m-1`. | `Shadowing.lean:exact_shadowing` uses strong induction on `j` (`Nat.strong_induction_on`). |
| 4.2 | [x] | Prove the base case `j = 0`. | Subsumed by the case `((n : ℤ_[2]) = q_w)` (handled by `qw_orbit_matches`) and the generic case using `affine_difference_z2`. The induction works uniformly for all `j < m`. |
| 4.3 | [x] | Prove the inductive step using lemmas 3.1–3.4. | The generic case applies `affine_difference_z2` (Phase-3 helper, derived from Task 3.2), `valuation_two_pow_z2`, `valuation_three_pow_z2`, `B_mono`, `B_succ`, and finally `nu2_stable_under_proximity` (Task 3.3). Closed by `omega`. |
| 4.4 | [x] | Verify the special case `m = bA` (full periods). | `exact_shadowing_periods` is stated and proved as a literal specialisation of `exact_shadowing` to `m = b · L`. The bound is currently `B (b · L)`; replacing with `b · A` is a Phase-5 task. |
| 4.5 | [x] | Final `lake build` clean run. | `Build completed successfully (1799 jobs)` — zero warnings, zero `sorry`s. |

---

## Phase 5 — Remove residual hypotheses and Corollary 3.4 (optional)

Acceptance: the remaining intrinsic phantom-orbit hypothesis is
discharged, the paper's periodic congruence bound is used directly, and
Corollary 3.4 (no positive integer can shadow `w^∞` for all `m`) is
formalized and proved.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 5.1 | [x] | Prove `B_mul_period : B (b · L) = b · A`. | `Auxiliary.lean:PhantomWord.B_mul_period` — proved, no `sorry`; supporting lemmas `aAt_add_length`, `aAt_mul_length_add_of_lt`, and `block_sum_mul_length`. |
| 5.2 | [x] | Restate the periodic specialisation with the paper bound `b · A`. | `Shadowing.lean:exact_shadowing_periods` now assumes congruence modulo `2^(b*A+1)` and converts via `B_mul_period`. |
| 5.3 | [x] | Prove `qw_orbit_matches`, discharging `h_qw_matches`. | `Auxiliary.lean:qw_orbit_matches` proved. `Shadowing.lean:exact_shadowing` and `exact_shadowing_periods` no longer require `h_qw_matches`; they use `qw_orbit_matches` internally. |
| 5.4 | [x] | State Corollary 3.4 in Lean. | New `NoInfinite.lean` states and proves the 2-adic congruential core: congruence modulo all powers forces equality, and period congruence for every `b` is impossible unless `(n : ℤ_[2]) = q_w`. No `sorry`. |
| 5.5 | [x] | Prove the full paper Corollary 3.4 for expansive phantoms. | `NoInfinite.lean:PhantomWord.Expansive`, `qwRat_neg_of_expansive`, `qwZ2_ne_natCast_of_expansive`, and `no_infinite_period_congruence_expansive` proved, no `sorry`. |
| 5.6 | [x] | Record the post-prefix boundary theorem for eventually periodic expansive shadowing. | `NoInfinite.lean:no_positive_endpoint_eventually_periodic_expansive_congruence` proves that any positive post-prefix endpoint cannot remain in the congruence classes of an expansive phantom period for all numbers of periods. This is a boundary theorem: it excludes the eventually periodic expansive obstruction, not aperiodic infinite concatenations. |

---

## Phase 6 — Integration into v2 of the paper

Acceptance: a published `v2` of the preprint on Zenodo that
incorporates the Lean formalization.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 6.1 | [x] | Lean-side README describes the project and build. | `lean/README.md` exists; build works as documented. |
| 6.2 | [x] | Paper Section 3 notes the Lean formalization. | `paper/collatz_spectral_reduction_v2.tex` §3.3 (Formal verification in Lean 4) drafted with explicit references to `exact_shadowing`, `exact_shadowing_periods`, `no_infinite_period_congruence_expansive`. |
| 6.3 | [x] | `METHODOLOGY.md` "Planned next phase" section moved to "Completed". | Section retitled "Formal verification phase: COMPLETED"; literature reconnaissance method appended. |
| 6.4 | [x] | Recompile PDF, replace on Zenodo, publish as new version (v2). | Verified 2026-05-10: Zenodo record `10.5281/zenodo.20098868` is v2 (`version = 2.0.0`) under concept DOI `10.5281/zenodo.20021537`; published PDF and supplementary zip checksums match the local artifacts. |
| 6.5 | [x] | Update GitHub README with v2 reference. | Top-level `README.md` rewritten: dual DOI badges (concept + v2), separate paper rows for v1/v2, Lean section with theorem-to-file mapping, "Planned next steps" section A→B→C, updated citation block to v2 DOI. |
| 6.6 | [x] | Add Related Work to paper covering Chang 2026, Siegel 2023, Rozier 2025, Neklyudov 2022, Lemmens-Nussbaum, Laarhoven-de Weger, Mori 2025, Leventides-Poulios, Bastos-Caprio-Messaoudi. | v2 §1.2 covers all listed works with explicit relationships. |
| 6.7 | [x] | Add Section 9.1 with quantitative comparison vs Chang 2026 bounds (R ≤ 0.0893, ρ(B̃₂_ext) ≤ 5/32). | v2 §9.1 (Comparison with concurrent work) drafted. |
| 6.8 | [x] | Make AI-collaboration as research methodology an explicit secondary goal of v2. | v2 abstract note + §11 (Methodology) expanded; cross-AI verification protocol documented. |
| 6.9 | [x] | Verify v2 .tex compiles without errors. | Verified online by Piero on 2026-05-10: `paper/collatz_spectral_reduction_v2.tex` compiles with `pdflatex`. Local TeX installation remains intentionally absent because `texlive` is too large. |

---

## Phase 7 — Priority A: phantom-set taxonomy vs Chang Theorem 7.15

Acceptance: a finite, scriptable enumeration that either confirms
the empirical phantom set ($k \le 24$, paper Appendix A) is closed
under SCC inclusion at depth $K_0$, or produces explicit new SCCs
to be added to the analysis. Sets the working phantom universe for
Phase 8.

Strictly outside Lean (Python/SciPy work). Listed here for
roadmap continuity. Estimated effort: 1-2 weeks of focused
scripting, with cross-AI checking between the necklace-enumeration
code and an independent direct-search fallback to catch
off-by-one errors.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 7.1 | [x] | Implement primitive cyclic-composition enumerator via Möbius inversion of necklace counts $M(K, \ell)$. | `scripts/phantom_taxonomy/necklace_counts.py` implements `M(K, ell) = (1/ell) * sum_{d | gcd(K, ell)} mu(d) * binom(K/d - 1, ell/d - 1)`, brute-force verifies formula counts through `K <= 10`, and reproduces Chang's displayed `R(K)` values for `K = 3..20`; `necklace_counts_k3_20.csv` records the small table. |
| 7.2 | [x] | For each enumerated composition $(k_1, \ldots, k_\ell)$ with expansive drift $\Delta = \ell \log_2 3 - K > 0$, compute the rational fixed point $q_w$ and its $2$-adic representative. | `scripts/phantom_taxonomy/phantom_representatives.py` emits per-composition rows `(word, C_w, A, L, q_w, q_w mod 2^m)` using exact `Fraction` arithmetic; generated `phantom_representatives_k3_16.csv` and `phantom_representatives_k3_20.csv`. Sanity checks prove `(2^A - 3^L) q_w = C_w`, `S_w(q_w) = q_w`, odd denominator, and per-`K` row counts match `M_expanding` from 7.1. |
| 7.3 | [x] | Build the orbit-simulation harness: for a given residue class of $q_w$ mod $2^{B_m+1}$, sample $N$ integer lifts and trace their first $b$ shadowing periods; record episode-graph transitions. | `scripts/phantom_taxonomy/orbit_harness.py` samples lifts `n = q_w mod 2^(bA+1) + t*2^(bA+1)`, traces odd Syracuse orbits, detects monitored phantom congruence hits, and emits detail/event/edge CSVs. Smoke outputs: `orbit_harness_k10_*` and `orbit_harness_k16_smoke_*`; the latter uses the `K0 = 16` representative table with a small sample budget. |
| 7.4 | [x] | Run the full enumeration at $K_0 = 16$. | Sampled full-composition run completed: `orbit_harness_k16_full_*` traces all 1247 representatives with `K <= 16`, `b = 1..2`, 8 dense lifts/source, max 1000 steps. `notes/phantom_taxonomy_k16_scc_report.md` reports 2401 observed nodes, 5041 edge types, and one nontrivial SCC of size 1222; full node list in `orbit_harness_k16_full_scc_nodes.csv`. Outcome is (b), feeding the completed 7.6 empirical integration and exact rational certificates. |
| 7.5 | [x] | If 7.4 outcome is (a): push $K_0$ to $20$ and re-run. | Not applicable: 7.4 closed with outcome (b), so the conditional branch to $K_0 = 20$ is skipped for this program branch. |
| 7.6 | [x] | If 7.4 or 7.5 outcome is (b): integrate the new SCCs into the cross-node operator and recompute $\spec(M_{\mathrm{cross}})$. | Closed as an **empirical integration result**, strengthened with exact rational certificates for the empirical matrices. `scc_transfer_summary.py` builds substochastic retention matrices from the `K0=16` event stream; `scc_collatz_wielandt.py` computes empirical CW upper expressions; `scc_cw_certificate.py` verifies exact rational inequalities `(P v)_i ≤ 0.89 v_i` for stored positive integer vectors. 16-lift certificates: raw 1240-node max ratio `439764459109/496636575879 ≈ 0.885485444423`; `(K,L,b)` 76-state max ratio `88036787882257/99446226949575 ≈ 0.885270266985`; `(K,b)` 37-state max ratio `136756256754601/154382162832639 ≈ 0.885829387575`. Scope note in `notes/phantom_taxonomy_empirical_scc_integration.md`: this still certifies sampled empirical matrices, not the stronger deterministic/theorem-level transition construction. |
| 7.7 | [x] | Document the enumeration result in a new `notes/phantom_taxonomy.md` and reference it from the v3 paper draft. | `notes/phantom_taxonomy.md` exists and summarizes 7.1-7.6: exact necklace enumeration, rational representatives, orbit harness, `K0=16` SCC run, empirical integration, stability, exact rational certificates for sampled matrices, and the remaining deterministic-transition gap. No v3 draft exists yet, so this note is the document to cite/import when Phase 9 starts. |

---

## Phase 8 — Priority B: Lean formalization of episode graph and FULL_{T,j}

Acceptance: a Lean 4 module `CollatzShadowing.EpisodeGraph` that
defines the episode graph as a local directed relation, formalizes the
truncated transfer operator at the critical node, the
$\full_{T,j} = \core_{T,j} + \tail_{T,j}$ decomposition, and proves
that the weighted Collatz–Wielandt expression is a true upper
bound on $\spec(\full_{T,j})$ for each finite $(T, j)$. No
formalization of the open conjectures of paper §9 is in scope.

Conditional on Phase 7 having fixed the working phantom set.
Estimated effort: 2-4 weeks of LLM-assisted Lean sessions,
comparable in scope to Phases 1-5 of this TODO.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 8.1 | [x] | Mathlib API inventory for `SimpleDigraph`, strongly-connected-component constructions, non-negative matrices, Perron–Frobenius / Collatz–Wielandt characterizations. | `CollatzShadowing/EPISODE_INVENTORY.md` written; `CollatzShadowing/EpisodeInventory.lean` typechecks. Inventory conclusion: use a local directed relation plus `Relation.ReflTransGen` for episode reachability/SCCs, and `Matrix ... NNReal` with finite Collatz-Wielandt-style certificates for the first operator layer. |
| 8.2 | [x] | Define the paper-level episode node `(k, c, b)` and the episode graph as a local directed relation on episode nodes. | `CollatzShadowing/EpisodeGraph.lean` typechecks. It defines `EpisodeNode` with natural coordinates, finite cutoff nodes `TruncatedEpisodeNode K C B`, `EpisodeGraph.edge : EpisodeRel EpisodeNode`, finite `TruncatedEpisodeGraph`, reachability/SCC wrappers, `edgeFinset`, and checked `Fintype` plumbing for cutoff boxes. |
| 8.3 | [x] | Formalize SCC computation/certification for the finite episode graph. | Completed for the paper-facing compressed SCC in `CollatzShadowing/EpisodeGraph.lean` and `CollatzShadowing/Generated/K16S16KSCC.lean`: `TruncatedEpisodeGraph.SCC` packages a finite node set with mutual-reachability proofs; `Walk`, `reachable_of_walk`, and `HubSCCCertificate` define a concrete import format based on finite paths to/from a hub; `CriticalSCCCertificate` packages a critical node plus SCC membership. `scripts/phantom_taxonomy/lean_scc_certificate.py` generates the 37-state compressed `K,b` SCC certificate from the Phase-7 JSON, importing the edge table, hub walks, an SCC object, and a critical-SCC certificate. The full raw 1240-node SCC import is optional audit work, not part of the 8.3 closure criterion. |
| 8.4 | [x] | Define the refined phase state $\sigma(t, h) := (\nu_2(t) \wedge V, \mathrm{odd}(t) \bmod 4, h \bmod 4)$ as a finite type. | `CollatzShadowing/Operator.lean` defines `PhaseState V := Fin (V+1) × Fin 4 × Fin 4`, `cappedNu2`, `oddPart`, `mod4Fin`, and `phaseState`; `instance : Fintype (PhaseState V)` typechecks. |
| 8.5 | [x] | Define $\full_{T,j}$, $\core_{T,j}$, $\tail_{T,j}$ as `Matrix PhaseState PhaseState ℝ≥0`, with the empirical-signature majority defining the partition. | Completed for the concrete paper-facing empirical import in `CollatzShadowing/Operator.lean`, `Generated/T10CriticalSymbolic.lean`, and `Generated/T10J32HighBitTail.lean`: `TransferMatrix V := Matrix (PhaseState V) (PhaseState V) NNReal`, `ProbabilityEntry` records exact imported probabilities as numerator/positive-denominator data, `RowSubstochastic` states row bounds, and `OperatorDecomposition` packages `full = core + tail` plus row certificates. `lean_phase_transfer.py` generates an exact `T = 10` critical-symbolic full matrix and its baseline decomposition. `export_high_bit_tail_edges.py` exports exact rational majority-signature `full/core/tail` edge weights for `T = 10, j = 32`; `lean_high_bit_tail.py` imports the generated `core` and `tail` matrices as `TransferMatrix 13`, defines `t10j32HighBitTailFull := core + tail`, generates support-based row-sum certificates, proves `t10j32HighBitTailCore_rowSubstochastic`, `t10j32HighBitTailTail_rowSubstochastic`, and `t10j32HighBitTailFull_rowSubstochastic`, and packages `t10j32HighBitTailDecomposition : OperatorDecomposition 13`. |
| 8.6 | [x] | Prove the weighted Collatz–Wielandt bound $\spec(\full) \le \max_i (\core v)_i / v_i + \max_i (\tail v)_i / v_i$ for any positive $v$ such that $\full v$ is well-defined. | Completed in `CollatzShadowing/Bound.lean`: `FiniteCWBasis`, `FiniteCWCertificate`, `FiniteMatrixBoundCertificate`, `ClearedCWRowBound`, and `ClearedCWCertificateSummary` package finite pointwise certificates and exact cleared-denominator arithmetic certificates. `ClearedCWRowBound.toNNRealInequality` proves the cleared arithmetic inequality over `NNReal`; `EvaluatedCWRowBound.toCWRow` and `finiteCWCertificateOfEvaluatedRows` bridge evaluated cleared rows into a full `FiniteCWCertificate`. `FiniteCWCertificate.add`, `finiteCWCertificateOfSumEq`, `CWCertificate.add`, and `OperatorDecomposition.cwCertificate_full` prove the finite `core+tail` CW bound for both the generic matrix API and the phase-state operator API. The spectral bridge uses `matrixLinftyOpNNNorm`, `spectralRadius_le_of_matrixLinftyOpNNNorm_le`, `finiteCWWeightedRealConjugate`, `finiteCWWeightedRealConjugate_spectrum_eq`, and `spectralRadius_le_of_finiteCWCertificate` to pass from a positive weighted CW certificate to Mathlib's real `spectralRadius`; `spectralRadius_le_of_finiteCWCertificateOfSumEq` and `OperatorDecomposition.spectralRadius_le_full` give the generic and phase-state `core+tail` spectral corollaries. `lean_cw_smoke.py` generates `Generated/K16S16KCWSmoke.lean` from one Phase-7 JSON edge; `lean_cw_summary.py` generates `Generated/K16S16KExactCWSummary.lean`, which imports the full 37-node `K,b` certificate summary, defines `K16S16KState := Fin 37`, generated labels, vector, positive basis, row-nested `NNReal` matrix, exact row supports, row-evaluation witnesses, the exact max-ratio inequality `136756256754601/154382162832639 < 89/100`, all 37 cleared-denominator per-node inequalities by `norm_num`, `k16s16KClearedCWSummary`, `k16s16KEvaluatedRows`, and the full generated certificate `k16s16KFiniteCWCertificate : FiniteCWCertificate k16s16KMatrix k16s16KCWBasis k16s16KAlphaNNReal`. `Generated/K16S16KBridge.lean` checks that the generated SCC and CW matrix certificates use the same `Fin 37` state ordering and labels, packages the combined result as `k16s16KCertifiedComponentWithCW`, and exposes `k16s16KSpectralRadiusBound` for the realified 37-state matrix. |
| 8.7 | [x] | Tie the bound theorem to the explicit numerical computation of paper §7 via a `decide`-style certificate at $T = 10$, $j = 32$. | `Generated/T10J32HighBitTailCW.lean` exposes `t10j32HighBitTailSpectralRadiusBound_97_2000 : spectralRadius ℝ (nnrealMatrixToReal t10j32HighBitTailMatrix) ≤ (((97 : NNReal) / (2000 : NNReal)) : ℝ≥0∞)`. The generator `scripts/phantom_taxonomy/lean_t10j32_cw.py` builds a positive integer CW vector from `high_bit_tail_edges_T10_j32.csv`, verifies the exact rational inequalities in Python before emission, and now emits `Data` plus 14 row modules whose 224 evaluated row witnesses are checked by Lean directly. `lake build CollatzShadowing.Generated.T10J32HighBitTailCW` succeeds with no `axiom`, `sorry`, or `admit` in the generated CW certificate. |
| 8.8 | [x] | `lean/CollatzShadowing/INVENTORY.md` updated to cover the Phase-8 additions; `lean/README.md` updated. | Verified 2026-05-12: `README.md` now documents the clean build status, main modules, and generated Phase-8 certificate target; `CollatzShadowing/INVENTORY.md` documents the production Phase-8 graph/operator/CW-certificate API; `CollatzShadowing/EPISODE_INVENTORY.md` notes the implemented production modules. |
| 8.9 | [x] | `lake build` clean across the full project. | Verified 2026-05-13: `lake build` succeeds across the full project; `rg -n "sorry|admit" CollatzShadowing *.lean` finds no Lean proof placeholders. |

---

## Open theorem-level follow-ups

These follow-ups track theorem-level or certificate-level hardening
beyond the original empirical Phase-7 / generated-Lean Phase-8 branch.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| F.1 | [x] | Close the deterministic-transition gap in `notes/phantom_taxonomy.md` / Phase 7.6. | Completed for the declared finite residue-cell scope on macro-state space `(K,b)`. `deterministic_residue_transfer.py` enumerates all `2^4` residue subclasses for each of the 1240 raw SCC source states, classifies 19840 cells with zero budget exits, writes exact rational deterministic matrices plus coverage manifest, and reruns the exact CW pipeline on the 37-state `(K,b)` matrix. Certificates: `deterministic_k16_s16_residue_K_cw_certificate.json` and `Generated/K16S16KDeterministicCW.lean`; max ratio `90833233962213/129559208330288 < 3/4`. Sensitivity checks at `lift_bits = 5, 6` also verify `< 3/4`, with max ratios about `0.69067` and `0.66719`. |

---

## Phase 9 — v3 paper redaction

Acceptance: a published `v3` of the preprint on Zenodo, after
Phases 7 and 8 are complete (Phase 9 is therefore conditional on
both). Phase 9 does **not** depend on Phase 10 (Priority C).

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 9.1 | [x] | Decide v3 framing. | Completed in the published v3. Piero confirmed the v3 framing was chosen and executed; this TODO entry was synced after publication. |
| 9.2 | [x] | Update §1.2 (Related Work) with any new arXiv work appearing between v2 and v3. | Completed in the published v3. Literature/reconnaissance details can be mirrored here later if desired. |
| 9.3 | [x] | Update §8 (Cross-node certificate) with the augmented SCC of Phase 7, if any. | Completed in the published v3, including the Phase-7/F.1 taxonomy and deterministic finite residue-cell certificate story. |
| 9.4 | [x] | Update §3.3 (Formal verification) to cover the Phase-8 additions: `EpisodeGraph`, `Operator`, `Bound`. | Completed in the published v3, covering the broader Lean graph/operator/bound/certificate layer. |
| 9.5 | [x] | Update §10 "Planned next steps" to reflect Phases 7 and 8 as completed and to refocus on Priority C (Phase 10). | Completed in the published v3; Phase 10 remains a future analytic/collaboration program, not a proved result. |
| 9.6 | [x] | Update §11 (Methodology) with the v2→v3 Lean session log and any new methodological observations. | Completed in the published v3. |
| 9.7 | [x] | Build the v3 supplementary archive (Zenodo zip) including the updated `lean/`, the Phase-7 enumeration code under `scripts/phantom_taxonomy/`, and the v3 PDF. | Completed externally for the v3 release. Exact local archive path/size not recorded in this TODO sync. |
| 9.8 | [x] | Publish v3 on Zenodo as new version of the existing record; update GitHub README with the new version DOI. | Completed externally by Piero before this TODO sync. v3 Zenodo record: `https://zenodo.org/records/20160154`; DOI: `10.5281/zenodo.20160154`. |

---

## Phase 10 — Priority C: transfer-operator roadmap / finite-rank fallback

Acceptance for `v3`: **planning only**. Phase 10 must not claim a
spectral gap, must not close Conjecture 6, and must not turn speculative
analytic hypotheses into theorems. Its purpose is to make the future
analytic project attackable: identify the candidate infinite operator,
candidate Banach spaces, target inequalities, fallback finite-rank path,
and collaboration package.

The key fork is Task 10.B. If 10.B identifies a natural infinite kernel
whose finite projections recover the paper-facing matrices, continue to
the analytic branch 10.C-10.F. If 10.B does not identify such a kernel,
switch to the finite-rank fallback branch 10.G and treat that branch as
the main Phase-10 output rather than a side result.

Current 2026-05-15 route: no collaborator is being pursued.  Therefore
Hennion and Keller-Liverani are not invoked as active claims, and the
active rigorous deliverable remains the finite-rank computational note
around the K16 deterministic `(K,b)` Collatz-Wielandt certificate.
However, 10.B has a narrower conditional closure attempt:
`A0-averaged` may be interpreted as a Haar/cylinder conditional
expectation of a killed weighted forward kernel on `Z_2 x H`, provided
the provenance and boundary hypotheses in
`notes/phase10_gate10B_conditional_closure.md` are checked.

Recommended sequencing:

```text
10.A -> 10.B -> 10.C -> 10.D -> {10.E, 10.F} -> 10.H -> 10.I -> 10.J
             \-> 10.G fallback, if 10.B is negative
```

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 10.A | [x] | Build a literature/hypothesis matrix for Lasota-Yorke, Hennion, Keller-Liverani, Baladi, Sarig/BIP, Bowen, GDMS/countable shifts, and relevant $p$-adic/non-archimedean dynamics. Include a Chang 2026 compatibility column. | `notes/phase10_literature_matrix.md` records theorem hypotheses and match/gap/unknown status. The matrix remains background for the paused analytic branch. |
| 10.B | [~] | Identify the correct infinite phase space / quotient behind `FULL_{T,j}` and `full_T`. | Conditional closure attempt in `notes/phase10_gate10B_conditional_closure.md`: define `X = Z_2 x H`, Haar/counting source measure, killed forward kernel `U_s`, and interpret `A0-averaged` as conditional expectation onto `sigma(PhaseState)`. This is not an exact projection and does not imply spectral claims. Remaining work: provenance checks for generated `FULL` matrices and proof-quality boundary/martingale statements. |
| 10.C | [~] | Compare candidate Banach spaces. Candidates include $2$-adic Lipschitz/Hölder spaces on a refined quotient, weighted symbolic spaces, and variation-type spaces on residue trees. | `notes/phase10_mixed_norm_candidate.md` now names the serious default pair: strong space `L_infty +` weighted martingale variation over Haar cylinders, weak space `L1(mu)`. Compactness `B_s -> B_w` follows by martingale tail truncation. This is a Banach-pair target, not a spectral proof. |
| 10.D | [~] | Formulate the transfer operator explicitly. | Candidate `U_K`/push-forward/Ruelle orientations were separated. The compatible branch is now the killed forward kernel on `Z_2 x H` used in `A0_HaarConditionalClosure`; Ruelle/preimage language remains inactive. |
| 10.E | [~] | State a target Lasota-Yorke-type inequality. | The active target is now `Var_a(U_ret,s f) <= alpha Var_a(f) + C ||f||_1`, with `alpha < 1`, for the retained-return kernel only. Missing lemmas are boundary variation, depth distortion, loss separation, and finite mixed-norm approximation. No Lasota-Yorke inequality is claimed. |
| 10.F | [~] | Write conditional skeletons for Hennion and Keller-Liverani. | Conditional skeletons exist only as non-claims. Hennion/Keller-Liverani are not active without a proof-quality operator/norm bridge. |
| 10.G | [x] | Finite-rank / truncated-operator fallback branch. | Active no-collaborator deliverable. `notes/phase10_finite_rank_note_outline.md` now states the finite K16 theorem scope, exact CW proof paragraph, stable artifacts, manifest/hash table, verification commands, sensitivity checks, limitations, relation to `A0-averaged`, and a first paper-facing draft block. |
| 10.H | [~] | Run computational experiments supporting analytic constants, only after 10.C and 10.D are closed. | Experiment plans exist, but free-floating numerics are stopped. Further experiments must support either the finite-rank note reproducibility or a later internally justified operator/norm framework. |
| 10.I | [!] | Prepare a collaboration package. | `notes/phase10_collaborator_brief.md` exists but is archived optional. No collaborator route is active. |
| 10.J | [x] | Decide v4 vs companion vs coauthored paper, with branch criteria. | `notes/phase10_decision_tree.md` keeps the finite-rank computational note as the active rigorous deliverable, while reopening A0 only as the conditional Haar/conditional-expectation bridge in `notes/phase10_gate10B_conditional_closure.md`. |
| 10.K | [x] | Formalize the finite A0 weak row-L1 bridge. | `CollatzShadowing/WeakBridge.lean` proves `weighted_action_diff_le`: finite weighted row-L1 drift controls the finite `ell_infty -> L1(mu_N)` action error. `lake build CollatzShadowing.WeakBridge` and `lake build CollatzShadowing` pass. |
| 10.L | [x] | Prove the high-`v2` source-tail mass bound for the current A0 source model. | `scripts/spectral_program/117_A0_v2_tail_formula.py` verifies the exact formula against all current A0 phase-strata CSVs with max observed-formula error `0`. `WeakBridge.TailCount.dyadic_tail_count_mul_le` formalizes the integer core `tail_count * 2^R <= total_count`; `WeakBridge.TailCount.dyadic_tail_mass_le` gives the real mass form `tail_count / total_count <= 1 / 2^R` when the total count is positive. |
| 10.M | [~] | Prove or falsify fixed-threshold low-`v2` decay `D_N(v2 < R) -> 0`. | Current evidence from scripts `115`, `118`, and `122` is positive: threshold low-`v2` / top-Haar exponents are near `0.6`, and the median per-phase alpha for `v2 < 8` is `0.6112066004`. Script `119` shows representative drift is dyadic half-block discrepancy (`prefix_l1/half_l1 = 0.5`) dominated by medium-depth returns (`step 11-25`, `delta 0` or `1-3`), not long-return tails. Script `120` weakens the naive finite-period route: dependency-depth majority error falls mainly as cells become sparse. Script `121` shows large fine-scale Haar energy but tiny root coefficients; script `122` recasts the exact target as top dyadic block-discrepancy decay, with `v2 < 8` latest root component `0.0005326722352` (about `93.2%` of total root drift). Script `123` confirms pure bounded valuation words become exactly periodic at large enough `m` (zero mismatches at `m>=192` in the sample for `S=25,A=8`). Script `124` with distributed block sampling shows killed-kernel unresolved tail can vanish at `S=75,A=10`, while symbolic tails remain pessimistic. Script `125` shows the residual killed-kernel pointwise L1 is entirely `delta_only`: no destination changes, no drop/return flips, no tail/return boundaries; the complete-prefix `v2<8`, `(S,A)=(75,10)` runs through `T14` keep the mismatch entirely `delta_only`, with weighted aggregate point-L1 around `0.012`, but these prefixes are tiny compared with the fixed period `2^743`. Lean now has the generic reduction `WeakBridge.FiniteSplit.weighted_dyadic_delta_boundary_le`: if deltas agree off a boundary, average `|2^-delta_1 - 2^-delta_2|` is bounded by boundary mass. Lean also has `WeakBridge.BitLength.bitLength_two_mul`, same-window add/sub lemmas, crossing lemmas showing that bit-length changes imply a dyadic endpoint is crossed, identity/affine endpoint-union bounds, `affineDeltaBadSet_card_le`, `affineDelta_period_eq_of_not_mem_badSet`, `biAffineDeltaBadSet_card_le`, `biAffineDelta_period_eq_of_not_mem_badSet`, and `biAffineDelta_dyadicWeight_period_boundary_le`: the finite weighted discrepancy of one bi-affine branch's `2^-delta` weights is controlled by the weighted mass of the explicitly counted source/target crossing set. Script `126` now extracts branch data in the reparameterized form `source_t=q*u+r`, `target_t=a*u+b`, records the exact valuation-word cylinder `n == word_residue mod 2^(sum(word)+1)`, checks that the branch source progression implies the induced `t`-congruence, and checks an exact affine no-drop prefix certificate: for every prefix of the fixed word, `n_i(u)-n_0(u)` has nonnegative affine numerator on `u >= 0`. It also computes destination-refined coefficients `refined_q/refined_r/refined_a/refined_b` and runs an exact congruence diagnostic for `best_shadow`: visibility of a phantom record is reduced to solvability of a linear congruence modulo `2^(sum_a+1)`. Complete finite-prefix runs `T12/T13/T14` produce `860/1564/2868` return branch rows, all with zero formula/delta/word/no-drop/refined failures, `no_drop_certificate_rows = branchRows`, and `arithmetic_certificate_rows = branchRows`. The label gate is now sharply localized: `labelFinalTargetLowFailures = 0`, `labelFinalCompetingFailures = 0`, and `labelPrefixIntegralityFailures = 0`. Every row has a target high-lift boundary (`860/1564/2868`), but script `126` now converts that boundary into an exact continuation branch by appending one target period: all rows have high-lift continuation support, step delta exactly `+6`, and zero continuation integrality/no-drop failures. Some rows still have possible intermediate phantom-label congruences (`216/376/744`, affecting `204/352/692` branch rows). Lean imports `a0CompletePrefixSummariesV2Lt8LabelOpenTotal = 6628` and `a0CompletePrefixSummariesV2Lt8HighLiftContinuationFailureTotal = 0`. This is a genuine arithmetic reduction of the observed branch rows, but it is still not a global first-return certificate: the remaining unproved part is to split or bound the intermediate visible-label congruence families in an automaton-aware way. Revised acceptance criterion: prove or certify fixed returning labels as positive bi-affine branches after intermediate-boundary splitting, then use the crossing bounds to prove the dyadic block discrepancy of the `2^-delta` weights, or find a counterexample family. |
| 10.N | [~] | Convert A0 low-`v2` decay plus the exact dyadic tail into a theorem-level double-limit statement. | Generic finite decomposition formalized as `WeakBridge.FiniteSplit.weighted_sum_le_low_plus_tail`: a weighted average is bounded by its exact low contribution plus a uniform tail bound times tail mass. Target remains `lim_{R -> infinity} limsup_N [D_N(v2 < R) + 2 mu_N(v2 >= R)] = 0`, with the `mu_N` term discharged by 10.L and the Collatz-specific low-`v2` term still requiring 10.M. |

Current 10.M refinement (2026-05-27): script `126` now splits the
intermediate visible-label congruences into target and competing/non-target
families.  In the complete-prefix `T12/T13/T14` runs the split is target
`12/16/64` and competing `204/360/680`, with Lean theorem
`a0CompletePrefixSummariesV2Lt8_intermediate_visible_split` certifying
totals target `92`, competing `1244`, and split failures `0`.  Thus the
active unresolved family is dominated by intermediate competitor visibility,
not by target high-lift and not mainly by target early-return visibility.
The next split by phantom record gives Lean-certified totals
`k10c1=8`, `k11c1=896`, `k12c1=340`, `k12c2=92`, `k20c1=0`, with
`a0CompletePrefixSummariesV2Lt8_intermediate_visible_by_record`.  A
representative automaton probe of all `1336` intermediate visible classes
selects the visible candidate and still returns to the target at the same
final step, with zero early target returns, zero no-return-by-final, and
zero terminal-by-final representatives; this is imported as
`a0CompletePrefixSummariesV2Lt8_intermediate_probe_same_step`.  This is
diagnostic finite evidence, not a uniform congruence-class proof.  The
stronger exact congruence split now also proves, on the imported finite
prefix summaries, that the `1244` intermediate competitor classes have no
intersection with any later intermediate target-visible class before the
final step:
`a0CompletePrefixSummariesV2Lt8_intermediate_competing_no_later_target`.
This removes the competitor classes as a plausible early-target mechanism
inside the current finite summaries; it is still not an infinite theorem.
For target-intermediate classes, Lean now imports the finite structure
theorem `a0CompletePrefixSummariesV2Lt8_intermediate_target_visibility_structure`:
across the `92` target-visible classes there are zero persistent-target
classes, all `92` are missing some prior target visibility, all `92` have
no prior competing intersection, and zero have prior competing
intersection.  The same theorem now records that all `92` are covered by
target high-lift visibility and zero are low-only target `b=1` classes,
so target-intermediate visibility is not the observed early-return
mechanism in the imported summaries.  Combining this with zero final
competitor labels, zero competitor-later-target intersections, and the
exact high-lift continuation gives a finite split-resolution certificate
for all `5292` imported branch rows:
`a0CompletePrefixSummariesV2Lt8_label_split_resolution_certificate`.
This is still a finite complete-prefix branch-split certificate, not an
asymptotic theorem.  The row-level predicate is isolated as
`WeakBridge.LabelSplit.branchResolved`, and the imported complete-prefix
summary satisfies `WeakBridge.LabelSplit.summaryResolved` via
`a0CompletePrefixSummariesV2Lt8_label_split_summary_resolved`.  The
cover-to-source bridge is now isolated as
`WeakBridge.LabelSplit.BranchCover` / `BranchPartition`; the missing
mathematical step is a genuine Collatz/A0 cover or partition by such
resolved branch labels, not another finite aggregate counter.  The finite
prefix return samples themselves are accounted for by
`WeakBridge.LabelSplit.ReturnPartitionSummary`, instantiated as
`a0CompletePrefixSummariesV2Lt8_return_partition_summary_resolved`.
The finite prefix outcome decomposition is also recorded as
`WeakBridge.LabelSplit.OutcomeSummary`; the generated theorem
`a0CompletePrefixSummariesV2Lt8_outcome_decomposition_resolved` checks
the exact balance `11752` covered return samples plus `101628` drop
samples plus `844` valuation-tail samples plus `16` step-tail samples =
`114240` total source samples, with zero return-coverage failures.  This
is a finite accounting certificate only; it does not prove that the tail
terms vanish in a limit.
The added eight-shift multi-probe tests `10688` shifted representatives:
there are zero early target returns, `10680` same-step returns, and `8`
no-return-by-final cases, all in `T14` competitor rows.  The target-only
multi-probe has `736/736` same-step and zero failures, imported as
`a0CompletePrefixSummariesV2Lt8_intermediate_target_multiprobe_same_step`.
The eight no-return-by-final shifted representatives are all `(12,1)`;
extended tracing to the step cap shows all eight return to target later
with step delta exactly `+6`, with zero terminal/unresolved outcomes,
imported as
`a0CompletePrefixSummariesV2Lt8_intermediate_multiprobe_no_return_extended`.
The unrefined affine continuation over the eight-shift class fails
integrality in all eight cases.  The traced actual late-return word has
the original word as prefix and the target word as suffix in all eight
cases; after an additional four-bit split, all eight actual continuations
are arithmetically supported with zero refined failures, imported as
`a0CompletePrefixSummariesV2Lt8_intermediate_multiprobe_no_return_actual_refined`.
Thus the honest remaining finite boundary is a finite refinement/label
certificate problem, not target-intermediate early return.

Ambition levels:

- **Minimum:** roadmap, candidate definitions, literature/hypothesis
  matrix, and obstacles clarified. This is enough for `v3`.
- **Intermediate:** a Lasota-Yorke-type inequality is formulated with
  explicit hypotheses and partial finite/computational checks.
- **Strong:** quasi-compactness or a spectral-gap statement is proved for
  a well-defined family of operators, or a certified finite-rank/truncated
  theorem is established with explicit scope.

Editor note for `v3`: the planned-next-steps section should say that the
next analytic task is to identify the correct infinite transfer operator,
the corresponding candidate Banach space, and the target
Lasota-Yorke-type inequalities. The finite Lean-certified matrices provide
evidence for a reproducible finite certificate layer; they are not, by
themselves, evidence of an infinite-dimensional spectral gap.

---

## Phase 11 — Conditional proof bridge toward Collatz

Acceptance: isolate, in Lean, the exact global theorem that would turn
the finite/descent program into a Collatz-type termination statement.
This phase must not claim that the missing global hypothesis is proved.

Current route: reduce the remaining Collatz proof problem to a
well-typed global descent statement for the accelerated Syracuse map.
The first Lean bridge is now formalized in
`CollatzShadowing/CollatzBridge.lean`.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 11.A | [x] | Define the accelerated and classical termination targets. | `CollatzBridge.lean` defines `collatzStep`, `ClassicalCollatzConjecture`, `acceleratedOrbitHitsOne`, and `AcceleratedCollatzConjecture`. |
| 11.B | [x] | Formalize the strict-descent bridge. | `UniformStrictDescentHypothesis` states that every positive odd `n ≠ 1` has a finite accelerated iterate that is positive odd and strictly smaller than `n`; `acceleratedCollatz_of_uniformStrictDescent` proves this hypothesis implies accelerated termination by strong induction. |
| 11.C | [x] | Separate classical-vs-accelerated bookkeeping from the finite phantom-shadowing gap. | `CollatzBridge.lean` now proves the elementary bridge `acceleratedToClassicalBridge`: accelerated termination on positive odd inputs implies classical Collatz termination on all positive naturals. The proof formalizes the initial even-tail halving, expands each accelerated Syracuse step into one odd `3n+1` step plus the exact number of halvings, and removes `AcceleratedToClassicalBridge` as an external hypothesis. |
| 11.D | [~] | Connect the finite phantom-shadowing layer to `UniformStrictDescentHypothesis`. | `CollatzBridge.lean` now defines `StrictDescentWitness`, `BranchDescentModel`, and proves `uniformStrictDescent_of_branchDescentModel`: a resolved finite branch-cover model would imply `UniformStrictDescentHypothesis`. With 11.C closed, it also proves `classicalCollatz_of_branchDescentModel`: such a resolved global branch-descent model would imply `ClassicalCollatzConjecture`. This is only a conditional bridge. The substantive open problem is still to construct such a global branch-cover model from the phantom-shadowing certificates, with no uncontrolled outside/budget/tail class. The K16 finite CW certificate alone does not prove this. |
| 11.E | [~] | Classify all finite-model losses for the global proof. | `CollatzBridge.lean` now defines `GlobalDescentCover`, whose cover cases are exactly: direct strict-descent witness, resolved branch witness, or declared loss label with its own strict-descent witness. It also defines the concrete audit types `FiniteModelLossKind` (`outsideSCC`, `budgetExit`, `valuationTail`, `stepTail`), `FiniteModelCoverClass`, `CoverClassStatus`, and theorem `finiteModelCoverClass_currentStatus`: `directDrop` is already `witness`, `resolvedBranch` is `branch`, and all four loss classes are `openLoss`. The theorem `classicalCollatz_of_finiteModelGlobalCover` proves that a resolved cover with exactly these declared loss labels implies `ClassicalCollatzConjecture`. `FiniteModelCoverSpec` is the witness-level interface, and `FiniteModelSoundSpec` is the propositional interface with exactly three soundness obligations: `DirectDropSound`, `BranchSound`, and `LossSound`. This does not classify the actual A0/K16 losses yet; it makes their required status explicit. Needed next split: `drop below start` is a direct witness; internal certified transitions are branch witnesses; outside-SCC, budget exits, valuation tails, and step tails must be proved impossible, redirected to descent, or assigned a real loss witness. |

Minimal theorem chain now visible:

```text
UniformStrictDescentHypothesis
  -> AcceleratedCollatzConjecture
  -> ClassicalCollatzConjecture   (proved by acceleratedToClassicalBridge)
```

The hard missing arrow is:

```text
finite phantom-shadowing/CW layer
  -> GlobalDescentCover / BranchDescentModel + resolved global branch cover
  -> UniformStrictDescentHypothesis
  -> ClassicalCollatzConjecture
```

---

## Session log

> Append-only. Newest entries on top.
>
> Format per entry:
> ```
> ### YYYY-MM-DD — AI / human name
> - Tasks advanced: 0.X, 0.Y
> - Artifacts produced: paths
> - Notes: any blockers, open questions, things the next session should know
> - Next recommended task: X.Y
> ```

### 2026-05-28 (A0 return branches: monotone-return exclusion) — Codex + Piero Borgatta

- Tasks advanced: 10.M, 11.D.
- Artifacts modified:
  - `CollatzShadowing/CollatzBridge.lean`
  - `CollatzShadowing/Generated/A0ReturnBranches.lean`
  - `CollatzShadowing/INVENTORY.md`
  - `scripts/spectral_program/126_A0_return_branch_affine_probe.py`
  - `notes/phase10_repro_manifest.md`
  - `lean/TODO.md`
- Notes:
  - Added the generic Lean record `AffineTBranch` with local coordinates
    `source_t = q*u+r` and `next_t = a*u+b`.
  - Proved
    `AffineTBranch.not_nextLocalInteger_lt_sourceLocalInteger_of_coeffNondecreasing`:
    if `a >= q` and `b >= r`, the embedded integer
    `residue + modulus*next_t` cannot be strictly smaller than
    `residue + modulus*source_t`.
  - Ran a read-only exact JSON audit of the existing script-126
    complete-prefix artifacts.  For `T12/T13/T14`, all return rows are
    coefficientwise nondecreasing in both base and refined coordinates:
    `0/860`, `0/1564`, `0/2868` base failures and the same zero refined
    failures.  Every row is strictly expansive in at least one coefficient;
    the minimum slope ratio is `531441/524288 > 1`.
  - Consequence: the current A0 same-coordinate return rows cannot provide
    the endpoint descent required by `BranchWordDropSound` or by a
    transition chain made only of these monotone return rows.  Any future
    global proof must use actual drop outcomes, prove/redirect the declared
    tails, or identify a different semantic mechanism; a chain of the
    imported A0 return branches alone is a dead end.
  - Added `AffineNatDropBranch` and theorem
    `AffineNatDropBranch.targetN_lt_sourceN_of_coeffDrop`, the generic
    arithmetic certificate for direct-drop affine branches, plus
    `directDropAt_of_word_matches_affineNatDrop`, which connects such a
    certificate to `DirectDropAt` when the Syracuse word match and affine
    source/endpoint equalities are supplied.
  - Ran a read-only reconstruction of script-126 drop traces.  The complete
    prefixes `T12/T13/T14` have `9032/16692/30900` drop groups covering
    `14548/29040/58040` finite drop samples; every group has an integer
    affine endpoint and satisfies the coefficientwise global drop criterion
    on its observed congruence progression.  This supports the local
    `DirectDropAtSound` route, but only after an actual infinite cover or
    parametric source partition is proved.
  - Replayed the declared tails.  All finite valuation-tail samples already
    satisfy `cur < n0` after the high-valuation step (`120/120`,
    `240/240`, `484/484`), so they are candidate direct drops rather than
    genuine losses.  The `step_tail` samples do not drop at the original cap
    (`0/8`, `0/8`), but extending just those eight representatives to cap
    `100` gives drops at steps `91` (`t=4853`, phases `0|1|h`) and `76`
    (`t=7110`, phases `1|3|h`).  This points to a finite budget-cap
    artifact, not a theorem-level absence of budget exits.
  - Reclassified the complete prefixes in read-only mode with drop checked
    before high-valuation tail and cap `100`.  Under that semantic order,
    `T12/T13/T14` have zero residual finite losses:
    `14668+1652=16320`, `29288+3352=32640`, and `58532+6748=65280`
    as drop/return decompositions.
  - Extended script `126` with opt-in flag `--semantic-replay-step-cap`.
    The default extraction is unchanged; with the flag, the script adds
    proof-facing replay counters to `stats` and stdout.  Verified with
    `../.venv/bin/python -m py_compile` and a no-write `T14` run:
    `loss_free=1`, `drop=58532`, `return=6748`, max drop step `91`.
    A direct no-write `analyze(...)` check verifies all `T12/T13/T14`:
    semantic counts are respectively `(drop,return) = (14668,1652)`,
    `(29288,3352)`, `(58532,6748)`, all with zero semantic loss samples.
  - Added the Lean finite summary
    `a0SemanticReplaySummariesV2Lt8Cap100` and theorem
    `a0SemanticReplayV2Lt8Cap100_loss_free`.  This imports the cap-100
    semantic replay separately from the existing conservative cap-75
    outcome summary.
  - Added
    `a0SemanticReplayV2Lt8Cap100_reclassifies_conservative_tails`: Lean now
    checks that the semantic replay keeps the same finite total and return
    count as the conservative complete-prefix summary, while moving exactly
    the conservative `860` tail samples into the drop count.  This is a
    finite replay comparison only, not a proof of an infinite source
    partition.
  - Proved `syracuse_lt_self_of_two_le_exponent`: if `1 < n` and the
    accelerated Syracuse exponent is at least `2`, then the next accelerated
    iterate is below `n`.  Added
    `directDropAt_one_of_two_le_syracuseExponent`, which packages this as
    `DirectDropAt 1 n`.  This is the theorem-level ingredient for
    redirecting high-valuation tails, but it does not prove that every
    valuation-tail class in the global model is covered.
  - Added word-concatenation infrastructure:
    `evalSyracuseWord_append`, `SyracuseWordMatchesFrom_append`, and
    `directDropAt_of_suffix_after_prefix_matches_eval_lt`.  This supports the
    observed factorization of semantic drop words into a common initial block
    plus a suffix that actually produces descent.
  - Added the exact matched-word affine formula
    `evalSyracuseWord_mul_pow_sum_eq_affine_of_matches`, the contraction
    criterion `directDropAt_of_word_matches_affine_contracting`, and the
    suffix version
    `directDropAt_of_suffix_after_prefix_affine_contracting`.
    Specialized the observed common prefix as
    `a0SemanticDropCommonPrefix = [1,1,2,1,1,1]` and proved
    `a0SemanticDropCommonPrefix_affine_of_matches`:
    `128 * endpoint = 729*n + 817` for a matched prefix.  The `817` is the
    integer-coordinate constant; the earlier `19` belongs to a local `t`
    coordinate after subtracting the target residue.
  - Added
    `directDropAt_of_a0CommonPrefix_suffix_scaled_contracting`: a suffix after
    the common prefix gives a direct drop if the scaled inequality
    `3^len(s)*(729*n+817)+128*C_s < 128*2^A_s*n` is certified.
    Added the threshold form
    `directDropAt_of_a0CommonPrefix_suffix_threshold_contracting`, which
    derives the scaled inequality from a nonnegative slope gap
    `729*3^len(s) <= 128*2^A_s` and an explicit lower-bound inequality for
    `n`.  This is the Lean target corresponding to the audit's
    `suffix_threshold_max`.
  - Added a finite small-case Lean check for the suffix-threshold route:
    `smallOddHasDirectDropWithin100Bool` verifies by `native_decide` that
    every positive odd `n < 455`, `n != 1`, has a direct accelerated drop
    within `100` steps; `hasStrictDescent_of_odd_lt_455` packages this as
    `HasStrictDescent n`.  This closes only the finite exception range for
    the current observed threshold; it is not a global cover theorem.
  - Added
    `hasStrictDescent_of_a0CommonPrefix_suffix_threshold_at_455`, combining
    the finite small-case theorem with the A0 common-prefix suffix threshold:
    if a matched word has the common prefix, a nonempty suffix, slope gap
    `729*3^len(s) <= 128*2^A_s`, and the intercept inequality already holds
    at `455`, then the original `n` has `HasStrictDescent`.  This is now the
    preferred compact target for a future generated suffix certificate.
  - Added the proof-facing Lean row type
    `A0SemanticSuffixCertificate` and predicate
    `A0SemanticSuffixCertificate.ValidAt455`.  The theorem
    `A0SemanticSuffixCertificate.hasStrictDescent_of_validAt455` turns one
    valid suffix row plus a matched common-prefix word into `HasStrictDescent`.
    This is only a local bridge: it does not prove that the generated finite
    suffix list covers all future sources.
  - Added the coarser Lean row type `A0SemanticSuffixPairCertificate`, with
    theorem `A0SemanticSuffixPairCertificate.hasStrictDescent_of_validAt455`:
    one valid pair row certifies any concrete suffix with matching
    `(length,sum)` and `syracuseWordConst` bounded by the row's declared
    maximum.  This is the proof-facing meaning of the `351`-row T14 pair
    compression.  Added the computable checker
    `A0SemanticSuffixPairCertificate.allValidAt455Bool` and membership lemma
    `validAt455_of_mem_of_allValidAt455Bool`, so a future generated list can
    be checked as a whole and then used row-by-row.
  - Ran a read-only compression audit of the semantic drop words with the
    complete `v2 < 8` phase list.  At `T14` the raw semantic drops would give
    `31324` phase-word groups, `28852` of them singleton, so a raw Lean import
    of drop rows is the wrong direction.  All semantic drop words in
    `T12/T13/T14` share the common prefix `[1,1,2,1,1,1]`; the next reduction
    should factor this prefix and prove a suffix/contractive-word criterion,
    not export thousands of one-off rows.
  - Extended script `126` with opt-in flag `--semantic-replay-word-audit`.
    With `--semantic-replay-step-cap 100`, a no-write complete `T14` run now
    prints
    `semantic_replay_drop_word_audit=distinct_words:7831,phase_word_groups:31324,phase_word_singletons:28852,distinct_suffixes:7831,suffix_slope_failures:0,suffix_threshold_max:455,common_prefix_failures:0,common_prefix_samples:58532`.
    Added the separate opt-in flag `--semantic-replay-suffix-certificate`,
    which stores one exact row per observed suffix after the common prefix in
    the JSON stats payload when writing is enabled.  No new artifact is
    produced by default.  Read-only checks give `rows:2287, failures:0,
    threshold_max:320` at `T12` and `rows:7831, failures:0,
    threshold_max:455` at `T14`.
    Verified with `../.venv/bin/python -m py_compile`.
  - Imported the compact audit into Lean as
    `a0SemanticDropWordAuditSummariesV2Lt8Cap100` and theorem
    `a0SemanticDropWordAuditV2Lt8Cap100_summary`: across `T12/T13/T14`,
    common-prefix samples equal all semantic drop samples (`102488`), common
    prefix failures are `0`, suffix slope-failure words are `0`, and the
    maximum observed suffix threshold is `455`.  The same theorem records why
    raw import is unattractive: `57392` phase-word groups, `52696` singleton
    groups.  It now also records the suffix-certificate aggregate:
    `14348` suffix rows across `T12/T13/T14`, equal to the distinct suffix
    count, with `0` suffix-certificate failures and certificate threshold max
    `455`.  The same opt-in export now records a pair compression by
    `(suffix_len, suffix_sum)`: `882` pair rows across `T12/T13/T14`, T14 max
    `351` pair rows, `0` pair-certificate failures, and pair threshold max
    `455`.  The pair-failure counter now checks the same `ValidAt455` formula
    used by the Lean pair-certificate bridge.  A read-only inclusion audit
    shows that the T14 pair set contains all T12/T13 pairs; for common pairs,
    T14 also dominates the earlier `suffixConstMax` and threshold maxima.  If
    a generated table is imported, the minimal current candidate is therefore
    the single T14 table with `351` pair rows.
    The script now also prints the current-run pair coverage audit.  At T14:
    `semantic_replay_suffix_pair_coverage=suffix_rows:7831,covered_suffix_rows:7831,uncovered_suffix_rows:0,covered_drop_samples:58532,covered_phase_word_groups:31324,failures:missing_pair:0,const_bound:0,threshold_bound:0,loss_free:1`.
    It also prints source-level coverage:
    `semantic_replay_source_pair_coverage=drop_samples:58532,covered_samples:58532,uncovered_samples:0,common_prefix_failures:0,failure_total:0,loss_free:1`.
  - Ran read-only stability checks beyond T14.  The fixed T14 pair table does
    not cover T15: T15 has `117016` semantic-drop samples, `14201` distinct
    suffixes, and `404` current-run pair rows; using the T14 table leaves `53`
    missing pair keys, `69` missing suffix rows, `224` const-bound failures,
    and `37` threshold-bound failures.  T15 does not stabilize T16 either:
    T16 has `233992` semantic-drop samples, `26112` distinct suffixes, `473`
    current-run pair rows, and threshold max `463`; using the T15 table leaves
    `69` missing pair keys, `85` missing suffix rows, `263` const-bound
    failures, and `56` threshold-bound failures.  T16 still does not stabilize
    T17: T17 has `467696` semantic-drop samples, `47843` distinct suffixes,
    `560` current-run pair rows, and threshold max `463`; using the T16 table
    leaves `87` missing pair keys, `115` missing suffix rows, `321`
    const-bound failures, and `51` threshold-bound failures.  This falsifies
    the tentative idea that any one of the current finite tables is a stable
    future cover.
  - Generalized the Lean cutoff bridge.  Added
    `smallOddHasDirectDropWithin100Bool464`,
    `hasStrictDescent_of_odd_lt_464`,
    `smallOddHasDirectDropWithin100Bool648`,
    `hasStrictDescent_of_odd_lt_648`,
    `hasStrictDescent_of_a0CommonPrefix_suffix_threshold_at_cutoff`, and
    cutoff wrappers at `464` and `648`.  The point is conceptual: `455` was
    an observed finite cutoff, not a structural constant; T16 already needs
    cutoff support beyond it, and T18 has threshold max `647`.
  - Generalized the suffix/pair certificate API itself.  Added
    `A0SemanticSuffixCertificate.ValidAtCutoff`,
    `A0SemanticSuffixCertificate.ValidAt464`,
    `A0SemanticSuffixPairCertificate.ValidAtCutoff`,
    `A0SemanticSuffixPairCertificate.ValidAt464`,
    `validAtCutoffBool`, `allValidAtCutoffBool`, and the corresponding
    membership/use theorems.  This is required before any T16-style table can
    be represented honestly.
  - Extended script `126` with
    `--semantic-replay-certificate-cutoff`.  Default `455` preserves the T14
    audit; running T18 with cutoff `648` gives
    `semantic_replay_suffix_certificate=rows:85753,cutoff:648,failures:0,threshold_max:647`,
    `semantic_replay_suffix_pair_certificate=rows:652,cutoff:648,failures:0,threshold_max:647`,
    and
    `semantic_replay_source_pair_coverage=drop_samples:934832,covered_samples:934832,uncovered_samples:0,common_prefix_failures:0,failure_total:0,loss_free:1`.
  - Ran T19 read-only.  With the old operational cap (`a_cap=10`, step cap
    `100`) T19 is not loss-free: `drop=1869460`, `return=219456`,
    `valuation_tail=8`, `step_tail=36`, `loss=44`; nevertheless the drop
    suffixes have threshold max `647`, `156178` distinct suffixes, `741` pair
    rows, and zero pair/source coverage failures for the drop part.  With
    enlarged operational caps (`a_cap=20`, semantic step cap `200`) T19 becomes
    loss-free: `drop=1869500`, `return=219460`, `valuation_tail=0`,
    `step_tail=0`, max drop/return steps `138/105`, `156188` distinct
    suffixes, `749` pair rows, threshold max `647`, and full source coverage
    for all drops.  A follow-up no-write run with certificate cutoff `648`
    also has zero suffix/pair certificate failures, so the Lean summary uses
    the smaller cutoff.  Imported this as compact Lean summary
    `a0SemanticReplayT19A20Cap200Cutoff648` with theorem
    `a0SemanticReplayT19A20Cap200Cutoff648_summary`.
  - Ran T20 read-only with the same enlarged caps (`a_cap=20`, semantic step
    cap `200`) and certificate cutoff `648`.  The replay is again loss-free:
    `drop=3739212`, `return=438708`, no valuation/step tails, max drop/return
    steps still `138/105`, `284363` distinct suffixes, `842` pair rows,
    threshold max still `647`, and full source coverage
    `3739212/3739212`.  Imported this as compact Lean summary
    `a0SemanticReplayT20A20Cap200Cutoff648` with theorem
    `a0SemanticReplayT20A20Cap200Cutoff648_summary`; theorem
    `a0SemanticReplayT19T20A20Cap200Cutoff648_stable_bounds` records only
    the finite observed stability of threshold and step maxima, not a global
    bound.
  - Removed a T14-specific proof-interface bottleneck.  `CollatzBridge.lean`
    now has generic `A0SemanticSuffixPairCover` and
    `A0SemanticDropSourcePairCover` objects for any finite pair-certificate
    table valid at an arbitrary cutoff, with use theorems
    `hasStrictDescent_of_a0SemanticSuffixPairCoverAtCutoff` and
    `hasStrictDescent_of_a0SemanticDropSourcePairCoverAtCutoff`.  The
    generated T14 cover is now explicitly viewed as a special case through
    `a0SemanticSuffixPairCertificatesT14_allValidAtCutoff455` and
    `A0SemanticSuffixT14PairCover.toGeneric`.  This is a genuine proof-shape
    reduction: T18/T20-style tables no longer need new descent theorems, only
    valid rows plus source/suffix assignment.
  - Added `A0SemanticDropTableSpec`, packaging a finite pair table, its cutoff,
    `allValidAtCutoffBool`, and the corresponding small-exception theorem.
    Its theorem `A0SemanticDropTableSpec.hasStrictDescent_of_sourceCover`
    states the remaining local obligation cleanly: provide source-cover data
    into the table, and strict descent follows.  The generated T14 table now
    instantiates this as `a0SemanticDropTableSpecT14`, with theorem
    `hasStrictDescent_of_a0SemanticDropTableSpecT14_sourceCover`.
  - Connected the table spec to the existing global bridge shape.  Added
    `A0SemanticDropBranchCoverSound` and
    `branchSound_of_a0SemanticDropBranchCoverSound`: a resolved finite branch
    is sound if it supplies `T.SourceCover n` for a fixed
    `A0SemanticDropTableSpec T`.  This identifies the next nontrivial proof
    obligation without claiming it is solved.
  - Proved the common-prefix part of that source-cover premise
    parametrically on the natural A0 source cylinder.  Script `126` uses
    source integers `n = 103 + 256*t`; Lean now proves
    `a0SemanticDropCommonPrefix_matches_source_cylinder`, namely every such
    source has accelerated exponent prefix `[1,1,2,1,1,1]`, and
    `eval_a0SemanticDropCommonPrefix_source_cylinder`, with endpoint
    `593 + 1458*t`.  The `AffineTBranch.localInteger` wrappers record the
    same fact in the local-coordinate language.  Added the missing append
    direction `SyracuseWordMatchesFrom_append_of_matches` and the constructor
    `AffineTBranch.a0SemanticDropSourcePairCover_of_localInteger_suffixCover`;
    therefore, for A0 sources, the remaining `SourceCover` obligation is now
    just: prove a suffix match from `593 + 1458*t` and assign that suffix to a
    valid pair row.
  - Named that remaining obligation as `A0EndpointSuffixPairCover`.  It
    packages exactly a suffix-pair cover plus
    `SyracuseWordMatchesFrom suffix (593 + 1458*t)`.  The theorem
    `A0EndpointSuffixPairCover.hasStrictDescent_atCutoff` and the table-level
    wrapper `A0SemanticDropTableSpec.hasStrictDescent_of_endpointSuffixCover`
    turn such data into `HasStrictDescent (103 + 256*t)`.  The generated T14
    table exposes this as
    `hasStrictDescent_of_a0SemanticDropTableSpecT14_endpointSuffixCover`.
  - Added the first formal suffix split after the common prefix:
    `syracuseExponent_a0CommonPrefix_endpoint`,
    `syracuseExponent_a0CommonPrefix_endpoint_of_odd_t`, and
    `syracuseExponent_a0CommonPrefix_endpoint_even_t`.  In particular, if
    `t` is odd then the next exponent from `593 + 1458*t` is forced to be
    `1`; if `t = 2*u`, the next exponent is
    `2 + ν₂(445 + 2187*u)`.  This identifies the next real recursive
    obstruction rather than hiding it inside finite suffix words.
  - Ran a quick no-write suffix-closure probe from endpoint `593 + 1458*t`.
    For every `t < 2^20`, the suffix drops below `103 + 256*t` within cap
    `300`; the observed max suffix length is `205`.  However this does not
    look like a small finite word-table closure: distinct suffix words grow
    from `206920` at `D=19` to `383215` at `D=20`, and pair rows
    `(suffixLength,suffixSum)` grow from `982` to `1123`.  The first split is
    benign for high exponents: if the first suffix exponent is `≥ 5`, the
    branch drops in one step coefficientwise.  The only first bad exponents
    are `1..4`, but recursively the low-exponent branches keep regenerating
    new affine states.  Current verdict: strong finite evidence of descent,
    no evidence yet of a small finite suffix automaton; the plausible next
    route is a drift/renewal bound on the recursive affine-valuation process,
    or a finite-rank fallback.
  - Sharpened that verdict with an exact no-write `e=1` branch probe.  For
    each tested depth `m <= 30`, there is a residue class
    `t == r_m (mod 2^m)` for which the first `m` post-prefix suffix exponents
    are all `1`, and the affine endpoint after those `m` suffix steps is still
    coefficientwise above the original source.  Example: at `m=30`,
    `t == 79536431 (mod 2^30)`, and the affine slope ratio has grown to about
    `1.09e6`.  Thus a proof by uniformly bounded suffix length/table closure
    is not the right target.  This is a finite exact obstruction probe, not a
    global theorem about all infinite low-exponent paths.  Lean now records
    the corresponding local obstruction API via
    `AffineNatDropBranch.CoeffNondecreasing`,
    `AffineNatDropBranch.eOneChild`, and
    `AffineNatDropBranch.eOneChild_not_coeffDrop_of_slope_growth`; build
    `lake build CollatzShadowing.CollatzBridge` passes (`3291` jobs; latest
    run `81s` after the phantom-boundary identity).
  - Identified the exact 2-adic boundary behind that repeated `e=1` branch.
    The residue bits are periodic with period `18` in the no-write probe,
    corresponding to the 2-adic value `t = -11/27`; Lean records the rational
    identities
    `a0Endpoint_phantomParameter_eq_negOne`:
    `593 + 1458*(-11/27) = -1`, and
    `a0Source_phantomParameter_eq_negThirtyFiveOverTwentySeven`:
    `103 + 256*(-11/27) = -35/27`.  Thus the all-`1` suffix obstruction is
    the usual `-1` phantom endpoint in the post-prefix coordinate.  This
    explains why no uniform finite suffix table should be expected, while not
    proving that all other low-exponent paths are harmless.
  - Generalized the periodic-boundary diagnosis in Lean.  Added
    `syracuseWordAffineEndpointQ`, `syracuseWordFormalFixedPoint`,
    `syracuseWordFormalFixedPoint_fixed`, and
    `syracuseWordFormalFixedPoint_neg_of_expanding`: for any nonempty
    periodic exponent word with `2^sum(word) < 3^length(word)`, the formal
    rational fixed point is negative.  Concrete checks
    `syracuseWordFormalFixedPoint_one`,
    `syracuseWordFormalFixedPoint_one_two`, and
    `syracuseWordFormalFixedPoint_two_one` give the first phantom endpoints
    `-1`, `-5`, and `-7`.  A no-write enumeration of primitive binary
    periodic words on `{1,2}` through length `12` found `6050` low-average
    periodic words, all falling under this negative phantom mechanism.  This
    is a structural explanation for the failure of finite suffix closure, not
    a global exit theorem for nonperiodic low-exponent paths.
  - Checked representative repeated patterns `[1]`, `[1,2]`, `[2,1]`,
    `[1,1,2]`, `[1,2,1]`, and `[2,1,1]` by exact no-write residue lifting.
    For repetitions `1,2,4,8,12`, each pattern has a unique compatible
    residue class and remains coefficientwise non-dropping through the forced
    prefix; the slope ratio grows as predicted by
    `(3^length)/(2^sum) > 1`.  Thus the obstruction is not just the all-`1`
    path: any proof must handle arbitrarily long neighborhoods of many
    negative periodic phantom endpoints.
  - Added the exact affine-deviation identity
    `syracuseWordAffineEndpointQ_sub_formalFixedPoint`: one application of a
    word sends `x - x_*` to `(3^length/2^sum) * (x - x_*)`, where `x_*` is the
    formal fixed point.  The companion lemma
    `syracuseWordExpansionFactor_gt_one_of_expanding` records that this factor
    is `> 1` in the low-exponent expanding case.  A no-write exit probe on
    the repeated patterns above, for repetitions `1,2,4,8,12,16,20`, found no
    misses under suffix cap `5000`; observed drops occur after the forced
    bad prefix plus a finite extra segment.  This is encouraging for an
    exit/renewal theorem but remains empirical: no uniform bound and no
    nonperiodic-path theorem has been proved.
  - Isolated the table-free endpoint target as `A0EndpointSuffixExit t`.
    It says: from the already-proved A0 endpoint `593 + 1458*t`, there exists
    an actual suffix word whose endpoint is below the original source
    `103 + 256*t`.  The theorem `hasStrictDescent_of_a0EndpointSuffixExit`
    proves that this target alone implies `HasStrictDescent (103 + 256*t)`.
    The wrapper `A0EndpointSuffixExitAll` and theorem
    `hasStrictDescent_a0Cylinder_of_endpointSuffixExitAll` package the
    corresponding cylinder-wide conditional result.  This is now the cleanest
    formulation of the desired exit/renewal theorem, separated from finite
    pair tables and from the CW finite-rank fallback.
  - Added direct proof-facing criteria for that endpoint target:
    `a0EndpointSuffixExit_of_suffix_scaled_contracting`,
    `a0EndpointSuffix_scaled_contracting_of_threshold`, and
    `a0EndpointSuffixExit_of_suffix_threshold_contracting`.  These avoid a
    finite pair-table assignment: a matched suffix from `593 + 1458*t` gives
    `A0EndpointSuffixExit t` as soon as the endpoint affine inequality
    `3^len*s_endpoint + C_s < 2^sum*s_source` holds, or via the equivalent
    threshold form with slope gap
    `256*2^sum - 1458*3^len`.  The wide no-write phantom-neighborhood probe
    suggests this slope/threshold barrier is the right local certificate:
    over `62037` primitive expanding words on `{1,2,3,4}` through length `12`
    and `10` repetitions, no cap-`5000` exit miss was found; the smallest
    observed surplus margin above `log2(729/128)` was about `0.001474779`.
    A follow-up no-write check found a sharper empirical rule: in all `62037`
    phantom-neighborhood cases, the exit occurs exactly at the first prefix
    of the matched suffix satisfying the slope barrier
    `1458*3^L <= 256*2^A`, and the endpoint threshold inequality already
    holds at that first crossing.  The same first-barrier rule also holds for
    every dense natural sample `0 <= t < 2^20` under cap `1000`; all
    `1048576` cases exit at first crossing, with maximum suffix length `205`.
    This is strong finite evidence for a “first barrier crossing” theorem,
    not yet a proof.
    A fixed-pattern repetition probe (`[1]`, `[1,2]`, `[1,1,2]`,
    `11121211212`, `121111114121`, `211111311111`, etc.) shows that the
    post-periodic extra tail is not uniformly bounded in any obvious way:
    for some patterns the extra segment grows to several hundred steps by
    `60` repetitions.  Thus the viable formulation is not “periodic phantom
    plus bounded tail”, but “exit at first A0 slope-barrier crossing”.
  - Formalized that formulation in Lean.  Added
    `A0EndpointSuffixSlopeBarrier`, `A0EndpointSuffixThreshold`,
    `A0FirstBarrierSuffix`, `A0FirstBarrierExistsAll`, and
    `A0FirstBarrierThresholdAutomatic`.  The theorem
    `a0EndpointSuffixExit_of_firstBarrier_threshold` proves the local easy
    implication: first barrier plus threshold gives `A0EndpointSuffixExit t`.
    The theorem `A0EndpointSuffixExitAll_of_firstBarrier` packages the exact
    remaining decomposition:
    `A0FirstBarrierExistsAll + A0FirstBarrierThresholdAutomatic =>
    A0EndpointSuffixExitAll`.  Thus the current A0 endpoint program is now
    split into two explicit open obligations, neither of which is claimed as
    proved.
  - Added the word arithmetic lemma `syracuseWordConst_append_singleton`, and
    proved the singleton first-barrier threshold case in Lean:
    `a0EndpointSuffixThreshold_singleton_of_barrier` and
    `a0FirstBarrierThreshold_singleton`.  This is only the length-one base
    case for the threshold obligation.  It does not prove
    `A0FirstBarrierThresholdAutomatic` for longer suffixes and does not address
    `A0FirstBarrierExistsAll`.
  - Added the monotonicity lemmas `a0EndpointSuffixThreshold_mono_t` and
    `a0EndpointSuffixThreshold_of_one_le`: once the endpoint threshold
    inequality is true at a parameter value, it remains true for larger `t`.
    This is the proof-facing interface for any future congruence-derived lower
    bound on the matched parameter.
  - Added the matching-to-congruence bridge in Lean.  The lemma
    `evalSyracuseWord_odd_of_matches` proves that a nonempty matched word lands
    at an odd endpoint; `padicValNat_syracuseWordAffine_of_matches` then proves
    the exact valuation
    `ν₂(3^len*n + C_word) = sum(word)`.  The A0 endpoint corollary
    `padicValNat_a0EndpointSuffixAffine_of_matches` specializes this to
    `n = 593 + 1458*t`.  This is the right formal handle for deriving residue
    classes/lower bounds on `t` from `SyracuseWordMatchesFrom`.
  - Added the divisibility/congruence form of the same bridge:
    `syracuseWordAffine_dvd_of_matches`,
    `a0EndpointSuffixAffine_dvd_of_matches`,
    `A0EndpointSuffixCongruence`, and
    `a0EndpointSuffixCongruence_of_matches`.  The A0 congruence is written as
    `2^sum ∣ (593*3^len + C_word) + 2*(729*3^len)*t`, deliberately avoiding a
    premature choice of inverse modulo `2^sum`.  Solving this linear
    congruence, together with first-barrier minimality, is now the concrete
    lower-bound/residue task.  Lean also proves
    `a0EndpointSuffixCongruence_reducedCoeff_odd`, recording that the reduced
    coefficient `729*3^len` is odd and therefore the right candidate for
    inversion modulo powers of two.
    The conditional halving lemma
    `a0EndpointSuffixCongruence_half_of_even_constant` proves the next exact
    step: if `sum = a+1` and
    `593*3^len + C_word = 2*b`, then the A0 congruence implies
    `2^a ∣ b + (729*3^len)*t`.  This is the inverse-ready congruence modulo
    `2^(sum-1)`.
  - Recast the longer-suffix threshold target through a witness interface.
    `A0EndpointSuffixThresholdWitness t suff` asks for some `t0 <= t` at which
    the threshold inequality already holds; theorem
    `a0EndpointSuffixThreshold_of_thresholdWitness` promotes it to `t` by
    monotonicity.  The obligation
    `A0FirstBarrierThresholdWitnessAutomatic` and theorem
    `A0FirstBarrierThresholdAutomatic_of_thresholdWitness` now isolate the next
    proof problem: construct such a `t0` from the exact matching congruence.
    The further reduction
    `A0FirstBarrierCongruenceThresholdWitnessAutomatic`, together with
    `a0FirstBarrierSuffix_congruence` and
    `A0FirstBarrierThresholdWitnessAutomatic_of_congruence`, makes this fully
    explicit: the remaining threshold-side problem is now
    `first-barrier + A0 linear congruence => threshold witness`.
  - Ruled out the naive slope-only extension.  Lean now defines
    `a0NaiveSlopeBarrierCounterexampleWord` and proves both
    `a0NaiveSlopeBarrierCounterexample_crosses` and
    `a0NaiveSlopeBarrierCounterexample_thresholdZeroFails`: the word crosses
    the slope barrier but fails `A0EndpointSuffixThreshold 0`.  A no-write
    congruence lift for the same word shows why this does not falsify the
    matched first-barrier program: matching from `593 + 1458*t` forces
    `t ≡ 237364345562 (mod 2^39)`, while the threshold needs only `t >= 1`.
    Thus the next proof target is not pure slope arithmetic; it must combine
    first-barrier crossing with the lower bounds/residue constraints forced by
    `SyracuseWordMatchesFrom`.
    Lean now also proves the local repair
    `a0NaiveSlopeBarrierCounterexample_threshold_of_match`: if this same word
    actually matches from `593 + 1458*t`, its first exponent forces `t ≠ 0`,
    hence `t ≥ 1`; since the threshold holds at `t = 1`, monotonicity gives the
    threshold at the matched parameter.  This is only a concrete model of the
    intended argument, not the general theorem.
  - Decision recorded 2026-06-04 after comparing the weak/spectral and
    pointwise branches.  The weak/L1/operator branch remains mathematically
    valuable as an approximation program, but it does not by itself address the
    pointwise Collatz requirement.  The Collatz-relevant branch is the
    pointwise A0 first-barrier route.  Its current hard gate is not more finite
    evidence but the aperiodic obstruction: `A0FirstBarrierExistsAll` would
    fail precisely through an infinite low-exponent/expanding path that
    shadows changing phantom neighborhoods without ever crossing the slope
    barrier.  Corollary 3.4 rules out infinite periodic phantom shadowing, but
    does not rule out such aperiodic concatenations.  The next mathematical
    target is therefore a rigidity theorem for aperiodic parity/valuation-word
    limits `ξ_W`, or a sharp proof that the present first-barrier formalism is
    only a cleaner parity-vector reformulation and supplies no new aperiodic
    leverage.
  - Lean boundary theorem added for the periodic side of that decision:
    `NoInfinite.lean:no_positive_endpoint_eventually_periodic_expansive_congruence`.
    It is the post-prefix form of Corollary 3.4: a positive natural endpoint
    cannot stay congruent to the fixed point of an expansive phantom period for
    every number of periods.  This records exactly what the phantom sign
    argument can prove.  It deliberately does not address the aperiodic
    obstruction behind `A0FirstBarrierExistsAll`.
  - Added a single worst-threshold feasibility row
    `a0SemanticSuffixPairCertificateT14ThresholdMax` in generated Lean data.
    Lean proves
    `a0SemanticSuffixPairCertificateT14ThresholdMax.ValidAt455` by exact
    arithmetic (`norm_num`), and the one-row prototype list
    `a0SemanticSuffixPairCertificatesT14Prototype` passes
    `A0SemanticSuffixPairCertificate.allValidAt455Bool` by `native_decide`.
  - Imported the full T14 pair-compressed table
    `a0SemanticSuffixPairCertificatesT14` with `351` rows.  Lean proves
    `a0SemanticSuffixPairCertificatesT14_rowCount` and
    `a0SemanticSuffixPairCertificatesT14_allValid` by `native_decide`; theorem
    `a0SemanticSuffixPairCertificatesT14_matches_summary` ties the table's
    row count and threshold maximum back to the compact audit summary.  This
    is now a genuine finite pair-certificate table for the observed T14
    semantic-drop suffixes, but it is still not a global cover theorem.
    The use theorem
    `hasStrictDescent_of_mem_a0SemanticSuffixPairCertificatesT14` now says:
    if a concrete suffix is assigned to a member of the T14 pair table, has
    matching length/sum and bounded `syracuseWordConst`, and the full
    common-prefix word matches the orbit, then `HasStrictDescent n`.
  - Added the proof-facing assignment type
    `A0SemanticSuffixT14PairCover` and theorem
    `hasStrictDescent_of_a0SemanticSuffixT14PairCover`.  This is the local
    object a future generated suffix-cover map must provide.
  - Added finite coverage accounting
    `a0SemanticSuffixT14PairCoverageSummariesV2Lt8Cap100` and theorem
    `a0SemanticSuffixT14PairCoverageV2Lt8Cap100_summary`: across T12/T13/T14,
    all `14348` distinct observed suffix rows and all `102488` drop samples
    are covered by the T14 pair table, with `0` missing-pair, const-bound, or
    threshold-bound failures.  This remains finite-prefix coverage, not a
    parametric/global cover theorem.
  - Added source-level cover target `A0SemanticDropSourceT14PairCover` and
    theorem `hasStrictDescent_of_a0SemanticDropSourceT14PairCover`: a concrete
    source with positivity/oddness/non-one, a suffix-to-T14-pair cover, and the
    common-prefix word match has `HasStrictDescent`.  Added finite source
    accounting `a0SemanticDropSourceT14CoverageSummariesV2Lt8Cap100` and
    theorem `a0SemanticDropSourceT14CoverageV2Lt8Cap100_summary`: all `102488`
    observed semantic-drop source samples through T12/T13/T14 are recorded as
    covered with zero finite source-coverage failures.
  - Verified `lake build CollatzShadowing.CollatzBridge` successfully
    (`3291` jobs; latest run `150s` after the conditional halving congruence).
  - Verified `lake build CollatzShadowing.NoInfinite` successfully
    (`1798` jobs; latest run `59s` after the post-prefix eventually-periodic
    boundary theorem).
  - Verified `lake build CollatzShadowing.Generated.A0ReturnBranches`
    (`3292` jobs; latest run `142s` after the first-barrier congruence
    reduction)
    and aggregate `lake build CollatzShadowing` (`3350` jobs; latest run
    `86s` after first-barrier packaging).
- Next recommended task: stop extending finite `T` audits as if they could
  close the pointwise theorem.  First run the mathematical aperiodic-rigidity
  test.  Define the infinite valuation-word limit `ξ_W` associated to an
  expanding aperiodic word `W`; compare the periodic case, where the fixed-point
  equation `(2^A - 3^L) q = C` excludes positive integers, with the aperiodic
  case, where no such algebraic equation is currently available.  The concrete
  question is whether first-barrier minimality plus the A0 congruence/threshold
  package imposes any constraint on `ξ_W` beyond the classical parity-vector
  residue class.  If yes, formalize that constraint as the next Lean target.  If
  no, document the pointwise branch as a clean isolation of the classical
  aperiodic obstruction and keep the v4/appendix result honest rather than
  claiming progress toward a full proof.

### 2026-05-27 (A0 weak branch: finite outcome accounting) — Codex + Piero Borgatta

- Tasks advanced: 10.M, 11.C, 11.D.
- Artifacts modified:
  - `CollatzShadowing/INVENTORY.md`
  - `CollatzShadowing/CollatzBridge.lean`
  - `CollatzShadowing/WeakBridge.lean`
  - `CollatzShadowing/Generated/A0ReturnBranches.lean`
  - `notes/phase10_repro_manifest.md`
  - `lean/TODO.md`
- Notes:
  - Added the abstract finite accounting schema
    `WeakBridge.LabelSplit.OutcomeSummary`, with
    `tailSamples`, `outcomeAccountedSamples`,
    `outcomeDecompositionResolved`, and the corresponding zero-failure
    checker.  The schema is deliberately finite: it records unresolved
    valuation/step tails instead of erasing them.
  - Instantiated the schema for the complete-prefix `T12/T13/T14` A0
    summaries.  The generated theorem
    `a0CompletePrefixSummariesV2Lt8_outcome_decomposition_resolved`
    verifies by Lean reduction that the imported prefix universe has
    `114240` total source samples, decomposed as `11752` covered return
    samples, `101628` drop samples, `844` valuation-tail samples, and
    `16` step-tail samples, with zero return-coverage failures.
  - Added the conditional Collatz bridge
    `CollatzShadowing.BranchDescentModel` and theorem
    `uniformStrictDescent_of_branchDescentModel`.  It proves that a
    resolved finite branch-cover model, whose resolved branches produce
    genuine accelerated Syracuse strict-descent witnesses for every
    positive odd `n ≠ 1`, implies `UniformStrictDescentHypothesis`.  This
    isolates the missing global-cover theorem; it does not construct it.
  - Closed the elementary accelerated/classical bookkeeping gap.  New
    lemmas in `CollatzBridge.lean` prove that repeated classical Collatz
    steps simulate both the initial even-tail division by powers of two
    and each accelerated Syracuse step.  The theorem
    `acceleratedToClassicalBridge` proves
    `AcceleratedCollatzConjecture -> ClassicalCollatzConjecture`, and
    `classicalCollatz_of_branchDescentModel` now packages the full
    conditional chain from a resolved global branch-descent model to the
    classical Collatz statement.  The global model itself remains open.
  - Added `GlobalDescentCover`, an audit-friendly global target with
    explicit loss labels.  For every positive odd `n ≠ 1`, such a cover
    must provide either a direct strict-descent witness, a resolved branch
    label with branch semantics producing a witness, or a declared loss
    label with its own witness.  The theorem
    `classicalCollatz_of_globalDescentCover` proves that a resolved
    `GlobalDescentCover` implies `ClassicalCollatzConjecture`.  This is
    only a target theorem; it does not classify the actual A0/K16 losses.
  - Added the concrete finite-model audit taxonomy
    `FiniteModelLossKind = outsideSCC | budgetExit | valuationTail |
    stepTail`, `FiniteModelCoverClass`, `CoverClassStatus`, and theorem
    `finiteModelCoverClass_currentStatus`.  The Lean status table marks
    `directDrop` as a strict-descent witness, `resolvedBranch` as requiring
    branch semantics plus resolved counters, and the four declared loss
    classes as `openLoss`.  The alias `FiniteModelGlobalCover` fixes the
    loss-label type to this declared taxonomy, and
    `classicalCollatz_of_finiteModelGlobalCover` packages the corresponding
    implication to classical Collatz.
  - Added witness constructors `strictDescentWitnessOfIterate` and
    `strictDescentWitnessOfOneStep`, so future drop/tail/branch lemmas can
    package an explicitly found accelerated descent into the exact witness
    type used by the global cover.
  - Added the propositional strict-descent form `HasStrictDescent`, the
    step-indexed direct-drop predicate `DirectDropAt`,
    `hasStrictDescent_of_directDropAt`, `directDropAt_of_witness`, the
    theorem `hasStrictDescent_of_witness`, the classical-choice packaging
    `strictDescentWitnessOfHasStrictDescent`, and
    `hasStrictDescent_iff_nonempty_witness`.  This lets future direct-drop
    predicates be stated propositionally while still feeding the
    `StrictDescentWitness`-based global cover.
  - Added `ProofToken` and `FiniteModelCoverSpec`.  This is the next
    working interface for the global proof: it separates
    `DirectDropCovers` as a predicate from the `directDropWitness` theorem
    that must turn that predicate into a `StrictDescentWitness`, while
    keeping branch covers and the four declared loss kinds explicit.  The
    conversion `FiniteModelCoverSpec.toGlobalDescentCover` and theorem
    `classicalCollatz_of_finiteModelCoverSpec` prove that a resolved spec
    would imply classical Collatz.
  - Added `DirectDropSound`, `BranchSound`, and `LossSound`, the three
    propositional soundness obligations for the finite global-cover
    interface.  The witness constructors `directDropWitnessOfSound`,
    `branchWitnessOfSound`, and `lossWitnessOfSound` package these proofs
    into the concrete witness functions required by `FiniteModelCoverSpec`.
  - Added the step-indexed reducers `DirectDropAtSound`,
    `BranchDropAtSound`, and `LossDropAtSound`, plus the absence reducer
    `LossAbsent`.  Their theorems
    `directDropSound_of_directDropAtSound`,
    `branchSound_of_branchDropAtSound`, `lossSound_of_lossDropAtSound`, and
    `lossSound_of_lossAbsent` show that the next concrete proof can target
    explicit accelerated descent times or absence of declared loss classes.
  - Added a minimal natural-number semantics for finite Syracuse exponent
    words: `syracuseStepWithExponent`, `evalSyracuseWord`,
    `SyracuseWordMatchesFrom`, and
    `evalSyracuseWord_eq_iterate_of_matches`.  The theorem
    `directDropAt_of_word_matches_eval_lt` proves that a matched nonempty
    exponent word whose evaluated endpoint is below the starting integer
    gives `DirectDropAt`.  This is the first formal bridge from branch-word
    arithmetic toward the direct-drop obligation.
  - Added `BranchWordDropSound`, the branch-facing obligation that a resolved
    branch supplies a matched nonempty Syracuse word whose evaluated endpoint
    is below the source integer.  The theorems
    `branchDropAtSound_of_branchWordDropSound` and
    `branchSound_of_branchWordDropSound` route this obligation into
    `BranchDropAtSound` and then `BranchSound`.
  - Added the transition-chain version for growing return branches:
    `evalSyracuseWordChain`, `syracuseWordChainLength`,
    `SyracuseWordChainMatchesFrom`,
    `evalSyracuseWordChain_eq_iterate_of_matches`, and
    `directDropAt_of_word_chain_matches_eval_lt`.  The corresponding
    branch-facing obligation is `BranchTransitionChainDropSound`: a resolved
    branch may pass through a finite chain of matched words, but the final
    endpoint must be below the original source integer.  The theorems
    `branchDropAtSound_of_branchTransitionChainDropSound` and
    `branchSound_of_branchTransitionChainDropSound` route such chains into
    the same `BranchSound` interface.  This avoids the false shortcut of a
    rank that descends only below the last intermediate value.
  - Ran a read-only coefficient audit on the existing complete-prefix script
    126 CSV outputs for `T12/T13/T14`.  All imported return-branch rows have
    `next_t = a*u+b` coefficientwise above the source progression
    `source_t = q*u+r` (`0/860`, `0/1564`, and `0/2868` rows are immediate
    affine direct drops).  This is not a Lean theorem and does not alter the
    generated artifacts, but it is an important negative guide:
    `BranchWordDropSound` is not the right instantiation for the current A0
    return branches.  Those rows need a genuine transition/descent mechanism,
    not a one-word direct-drop wrapper.
  - Added generated audit theorems
    `a0CompletePrefixSummariesV2Lt8_declared_tail_counts` and
    `a0CompletePrefixSummariesV2Lt8_declared_tail_positive`.  These make the
    current finite-prefix obstruction explicit: the imported complete A0
    summaries still contain `860` declared residual tail samples, so a
    future `FiniteModelSoundSpec` cannot use loss absence at this level.
  - Added `FiniteModelSoundSpec`, the current recommended interface for a
    future A0/K16 instantiation.  It contains source predicates, branch
    counters, the three soundness obligations, and the finite cover
    decomposition; `FiniteModelSoundSpec.toCoverSpec` and
    `classicalCollatz_of_finiteModelSoundSpec` route it to the already proved
    conditional Collatz bridge.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), `lake build CollatzShadowing.Generated.A0ReturnBranches`
    succeeded (`3286` jobs; latest run `75s` after declared-tail extraction),
    `lake build CollatzShadowing.CollatzBridge` succeeded (`3291` jobs;
    latest run `91s` after transition-chain soundness), and `lake build
    CollatzShadowing` succeeded (`3350` jobs; latest run `124s`).  No commit
    or push was made.
- Next recommended task: decide the next genuine proof obligation: either
  prove a parametric branch-cover theorem for the fixed A0 family, or
  explicitly state the remaining global-cover hypothesis that would
  connect these finite prefix certificates to `UniformStrictDescentHypothesis`.

### 2026-05-26 (A0 weak branch: bi-affine delta model) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `scripts/spectral_program/126_A0_return_branch_affine_probe.py`
  - `scripts/spectral_program/collatz_126_current_A0_A0_return_branch_affine_probe_branches.csv`
  - `scripts/spectral_program/collatz_126_current_A0_A0_return_branch_affine_probe_branches.json`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_A0_return_branch_affine_probe_branches.csv`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_A0_return_branch_affine_probe_branches.json`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_prefix_A0_return_branch_affine_probe_branches.csv`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_prefix_A0_return_branch_affine_probe_branches.json`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T12_A0_return_branch_affine_probe_branches.csv`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T12_A0_return_branch_affine_probe_branches.json`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T13_A0_return_branch_affine_probe_branches.csv`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T13_A0_return_branch_affine_probe_branches.json`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T14_A0_return_branch_affine_probe_branches.csv`
  - `scripts/spectral_program/collatz_126_current_A0_v2lt8_complete_T14_A0_return_branch_affine_probe_branches.json`
  - `scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T12_A0_kernel_mismatch_decomposition_report.md`
  - `scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T12_A0_kernel_mismatch_decomposition_rows.csv`
  - `scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T13_A0_kernel_mismatch_decomposition_report.md`
  - `scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T13_A0_kernel_mismatch_decomposition_rows.csv`
  - `scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T14_A0_kernel_mismatch_decomposition_report.md`
  - `scripts/spectral_program/collatz_125_current_A0_v2lt8_complete_T14_A0_kernel_mismatch_decomposition_rows.csv`
  - `CollatzShadowing/Generated/A0ReturnBranches.lean`
  - `CollatzShadowing.lean`
  - `notes/phase10_repro_manifest.md`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.biAffineDelta a b q r u =
    bitLength(a*u+b) - bitLength(q*u+r)`.
  - Added `WeakBridge.BitLength.biAffineDeltaBadSet`, the union of the
    target affine endpoint crossings for `a*u+b -> a*u+b+a*p` and the
    source affine endpoint crossings for `q*u+r -> q*u+r+q*p`.
  - Proved `WeakBridge.BitLength.biAffineDeltaBadSet_card_le`, reducing
    the bad-set size to the two already formalized affine endpoint-union
    bounds.
  - Proved `WeakBridge.BitLength.biAffineDelta_period_eq_of_no_crosses`
    and `WeakBridge.BitLength.biAffineDelta_period_eq_of_not_mem_badSet`:
    outside the explicitly counted source/target crossing union, the
    bi-affine bit-length delta is invariant under `u -> u+p`.
  - Proved
    `WeakBridge.BitLength.biAffineDelta_dyadicWeight_period_boundary_le`:
    for one finite weighted bi-affine branch, the period-shift average of
    `|2^-delta(u+p)-2^-delta(u)|` is bounded by the weighted mass of the
    same explicit bad set.
  - Proved `WeakBridge.BitLength.biAffineDelta_refine`: substituting
    `u = M*v+s` in a branch
    `source_t=q*u+r`, `target_t=a*u+b` gives the refined branch
    `source_t=(q*M)*v+(q*s+r)`,
    `target_t=(a*M)*v+(a*s+b)` without changing the represented
    `biAffineDelta`.
  - This corrects the abstract model suggested by the script-125 trace
    diagnostic: fixed returning labels appear as exact dyadic/rational
    affine branches in the original local coordinate, so the clean
    theorem should reparameterize a residue class as
    `source_t = q*u+r`, `target_t = a*u+b`.
  - Added script `126_A0_return_branch_affine_probe.py` to extract these
    sampled branch forms using exact rational arithmetic and write both
    CSV rows and a JSON certificate-style payload.  Current runs:
    `current_A0` with sample limit `256` finds two exact branch rows and
    `current_A0_v2lt8` with all `v2<8`, odd residues `{1,3}`, and
    `h<4` finds sixteen exact branch rows.  Both runs have
    `formula_failures = 0`, `delta_failures = 0`,
    `exact_failures = 0`, and `noninteger_branches = 0`.
    The script now also computes destination-refined branch coefficients
    `refined_q/refined_r/refined_a/refined_b`, so that the finite
    destination state is fixed on the sampled refined source progression.
    It also records the exact valuation-word cylinder
    `n == word_residue mod 2^(sum(word)+1)` and the induced A0-coordinate
    congruence for `t`, and checks whether each branch progression
    `t=q*u+r` implies that congruence.  It now also checks a sufficient
    exact no-drop certificate: for every prefix of the fixed valuation
    word, `n_i(u)-n_0(u)` has nonnegative affine numerator on `u >= 0`.
    The regenerated spread `v2<8` run has
    `word_congruence_failures = 0`, `drop_affine_failures = 0`,
    `no_drop_certificate_rows = 16`,
    `branch_word_certificate_failures = 0`, and
    `arithmetic_certificate_rows = 16`.  The new label-gate diagnostic
    shows `label_intermediate_visible_failures = 0`,
    `label_final_competing_failures = 0`, and
	    `label_status_target_high_lift_boundary = 16`: the spread rows first
	    hit only target high-lift residues.  Appending one target period now
	    gives exact high-lift continuation support for all `16` rows, with
	    step delta `+6` and zero continuation integrality/no-drop failures.
    A separate `current_A0_v2lt8_prefix` run with prefix sampling finds
    `380` exact branch rows and again has zero exact/noninteger/refined
    failures.
  - Added `dyadic-prefix` mode to script `126`, which enumerates all
    selected phase points with `t < 2^T`.  Complete finite prefix runs
    for all `v2<8`, odd residues `{1,3}`, and `h<4` give:
    `T12`: `16320` source points, `1652` returns, `14548` drops,
    `120` valuation tails, `0` step tails, `860` return branch rows;
    `T13`: `32640` source points, `3352` returns, `29040` drops,
    `240` valuation tails, `8` step tails, `1564` return branch rows;
    `T14`: `65280` source points, `6748` returns, `58040` drops,
    `484` valuation tails, `8` step tails, `2868` return branch rows.
    Derived finite ratios: return rates are about `0.101225`,
    `0.102696`, `0.103370`; branch-row densities are about
    `0.052696`, `0.047917`, `0.043934`.
    All three complete-prefix runs have
    `exact_failures = noninteger_branches = word_congruence_failures =
    drop_affine_failures = branch_word_certificate_failures =
    refined_formula_failures = refined_state_failures = 0`, and have
    `no_drop_certificate_rows = branchRows` and
    `arithmetic_certificate_rows = branchRows`.  The label-gate diagnostic
    reduces `best_shadow` to linear congruence solvability modulo powers
    of two.  For `T12/T13/T14`, there are no final competing phantom
    labels and no final target-low failures, but there are
    `216/376/744` possible intermediate visible-label congruences and
    every branch row has a target high-lift boundary.  Status counts are:
	    `target_high_lift_boundary = 656/1212/2176` and
	    `blocked_label_congruence = 204/352/692`.  The target high-lift
	    boundary is now extendable in every branch row by appending one
	    target period: high-lift continuation support is
	    `860/1564/2868`, the continuation step delta is always `+6`, and
	    continuation integrality/no-drop failures are zero.  A further split
	    of intermediate visible labels gives target `12/16/64` versus
	    competing/non-target `204/360/680`, so the active obstruction is
	    predominantly intermediate competitor visibility.  These are exact
	    finite-prefix enumerations and congruence diagnostics, not infinite
	    residue-class certificates.
  - Added the same `dyadic-prefix` mode to script `125` and ran the
    period-shift mismatch decomposition on complete prefixes `T12`,
    `T13`, and `T14` for `(S,A)=(75,10)`.  In all three runs the
    weighted aggregate mismatch has zero destination changes, zero
    drop/return flips, and zero tail/return boundary; it is entirely
    `delta_only`.  Weighted aggregate point-L1 values are approximately
    `0.012019378064`, `0.011900658701`, and `0.012011479396`.
    This supports the reduction to bit-length weights but also warns
    that these small prefixes are far below the fixed comparison period
    `2^743`, so the values should not be read as asymptotic decay.
    This shows the 16-row spread import is not a complete branch
    enumeration; a real certificate must cover the whole finite
    truncated branch partition, not just representative spread samples.
  - Added `CollatzShadowing/Generated/A0ReturnBranches.lean`, importing
    the sixteen `v2<8` sampled branch rows into Lean as finite data and
    proving by kernel-checked reduction that the imported row count is
    `16`, the total imported formula/delta failure counter is `0`, and
    the internal scale checks hold: `word.length = step`, `a = 3^step`,
    `q = 2^(sum word)`, and the destination-refined coefficients satisfy
    the expected relations
    `refined_q = q * 2^(dst_v2+2)`,
    `refined_r = q*u_residue + r`,
    `refined_a = a * 2^(dst_v2+2)`, and
    `refined_b = a*u_residue + b` for the imported rows.  This is not a
    proof that the branch persists for all `u`.
  - The generated Lean file now also imports the four distinct sampled
    word-cylinder/no-drop rows and proves by kernel-checked reduction that
    their word-cylinder and affine no-drop checks are zero, that
    `wordModBits = sum(word)+1`,
    that `q = 2^(sum word)`, and that the branch source split implies
    the induced `t`-congruence.  This certifies the valuation-word
    arithmetic and no-drop prefix property for these imported branch
    shapes; it still does not certify the global first-return label.
  - The same generated Lean file now imports the complete-prefix
    `T12/T13/T14` summary rows and proves that all formula/noninteger/
    word/no-drop/refined failure totals are zero, that all finite-prefix
    branch rows carry script-126 arithmetic and no-drop certificates, and
    that the return/drop/tail counters cover all enumerated source points
    in those finite prefixes.  It also imports the label-gate diagnostic:
    `a0CompletePrefixSummariesV2Lt8LabelOpenTotal = 6628`, with exact
    status coverage across the three prefix summaries.  It also proves
	    that the target high-lift boundary has `u`-modulus bits exactly `7`
	    in all three complete-prefix summaries, and that the imported
	    high-lift continuation failure total is zero.  It also imports the
	    intermediate visible-label split: target total `92`, competing total
	    `1244`, split failures `0`; and the per-record split
	    `k10c1=8`, `k11c1=896`, `k12c1=340`, `k12c2=92`, `k20c1=0`.
	    It also imports a representative automaton probe: all `1336`
	    intermediate visible representatives return at the same final step,
	    with zero early target returns, zero no-return-by-final, and zero
	    terminal-by-final outcomes.  Finally, it imports the exact
	    congruence-intersection check that all `1244` intermediate
	    competitor classes have no later target-visible intersection before
	    the final step.
	    The new eight-shift multi-probe imports `10688` shifted
	    representatives with zero early target returns, `8` no-return-by-final
	    cases in `T14` competitor rows, and target-intermediate subprobe
	    `736/736` same-step.  The `8` no-return cases are all `(12,1)` and
	    all return to target later with step delta `+6`, with zero terminal
	    or unresolved extended outcomes.  The naive unrefined continuation
	    fails integrality in all eight cases; the actual traced late-return
	    word has prefix/suffix agreement and is supported after an extra
	    four-bit split, with zero refined failures.
	    It also imports the target-intermediate visibility structure:
	    persistent `0`, missing-prior `92`, no-prior-competitor `92`, and
	    prior-competitor `0`; high-lift-covered `92`, low-only `0`.
	    The derived finite split-resolution certificate covers all `5292`
	    imported complete-prefix branch rows.  The abstract Lean schema for
	    this diagnostic is `WeakBridge.LabelSplit`; the generated A0 summary
	    instantiates it with branch rows `5292` and certificate rows `5292`.
	    The same namespace now contains the conditional cover/partition
	    bridge: if all branch labels in a declared cover are resolved, then
	    every covered source point is resolved in the same finite label-split
	    sense.  The A0 infinite cover itself remains the open gate.
	    The finite return-sample partition summary is imported as well:
	    branch-row sample counts cover all `11752` finite return samples,
	    with zero coverage failures.
	    The nonzero open label total is now attributable mainly to
	    intermediate `(11,1)` and `(12,1)` competitor congruence families
	    plus conservative high-lift bookkeeping, not to a failed arithmetic
	    branch formula.
  - The project virtual environment already contains the transitive
    scientific dependencies used by the spectral helper modules:
    `numpy 2.4.4` and `scipy 1.17.1`.  The reproducibility manifest now
    records that Phase-10 scripts importing
    `75_critical_symbolic_operator.py` or `53_lift_phantom_cycles.py`
    should be run with `.venv/bin/python` or with the documented
    `uv run --with numpy --with scipy python ...` form, not system
    `python3`.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs; latest cached check after `OutcomeSummary` import was
    about `7s`),
	    `lake build CollatzShadowing.Generated.A0ReturnBranches`
	    succeeded (`3286` jobs; latest run `82s`), and
	    `lake build CollatzShadowing` succeeded (`3350` jobs after importing
	    the generated file; latest run `79s`).
- Next recommended task: close or falsify the remaining global-label
  part of the branch certificate for fixed `(S,A,R)`.  The valuation-word
  cylinder, source split `t=q*u+r`, target affine form `next_t=a*u+b`,
  affine no-drop prefix property, and destination-state refinement are
  now arithmetic certificate fields.  The `best_shadow` gate is reduced
	  to explicit congruence-boundary families.  The target high-lift family
	  is now extendable by one target period; the active hard family is the
	  intermediate competing/non-target visible-label residues.  Next, split
	  those competitor residue classes by record type and automaton outcome,
	  and decide whether they form a controlled boundary mass or a genuine
	  obstruction.  Then state the block-discrepancy target
  as a finite sum of `2^-biAffineDelta` weights plus controlled exception
  sets.

### 2026-05-26 (A0 weak branch: affine-delta bad set) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.affineDelta a b t =
    bitLength(a*t+b) - bitLength(t)`.
  - Added `WeakBridge.BitLength.affineDeltaBadSet`, the union of the
    source endpoint crossings for `t -> t+p` and target affine endpoint
    crossings for `a*t+b -> a*t+b+a*p`.
  - Proved `WeakBridge.BitLength.affineDeltaBadSet_card_le`: for
    positive slope, the bad set is bounded by the sum of the source and
    affine endpoint-union bounds.
  - Proved `WeakBridge.BitLength.affineDelta_period_eq_of_no_crosses`
    and `WeakBridge.BitLength.affineDelta_period_eq_of_not_mem_badSet`:
    outside the explicitly counted bad set, the affine bit-length delta
    is invariant under the fixed period shift `t -> t+p`.
  - This is the precise abstract form needed for the `delta_only` route.
    The remaining non-formalized step is to prove that fixed returning
    labels in the Collatz trace model really supply positive affine
    branches of the form `next_t = a*t+b` with fixed period `p`.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: inspect the script-125 / trace code path and
  isolate where a fixed returning label determines `next_t` as an affine
  function of `t`.  Then either formalize that as a Lean hypothesis or
  generate/certify branch data for the current finite labels.

### 2026-05-26 (A0 weak branch: affine endpoint crossing bound) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.affineCrossesDyadicEndpoint`,
    `fixedAffineEndpointCrossingSet`, and `affineEndpointCrossingUnion`.
  - Proved `WeakBridge.BitLength.fixed_affine_endpoint_crossing_count_le`:
    for positive slope `a`, at most `2*c+1` source indices can cross one
    fixed dyadic endpoint under `(a*t+b, a*t+b+c]`.  The bound is coarse
    but independent of `N`.
  - Proved `WeakBridge.BitLength.affine_endpoint_index_lt_of_crosses_in_prefix`
    and `mem_affineEndpointCrossingUnion_of_crosses`.
  - Proved `WeakBridge.BitLength.affineEndpointCrossingUnion_card_le`:
    for `0 < a`, all affine endpoint crossings in `t < N` have cardinality
    at most `(2*c+1) * (bitLength(a*N+b+c)+1)`.
  - This is the first Lean-checked affine boundary estimate for the
    Phase-10 `delta_only` route.  It still needs to be connected to the
    actual returning-label affine branches extracted from the Collatz
    trace model.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: define a small abstract "return branch" record
  with `next_t = a*t+b` and prove that away from the affine endpoint
  crossing union, the corresponding bit-length delta is constant under
  bounded additive perturbation.  Then identify where the script-125
  returning labels supply such branches.

### 2026-05-26 (A0 weak branch: endpoint-union crossing bound) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.fixedEndpointCrossingSet` and
    `WeakBridge.BitLength.endpointCrossingUnion`.
  - Proved `WeakBridge.BitLength.endpoint_index_lt_of_crosses_in_prefix`:
    any crossed endpoint for a source `t < N` has index below
    `bitLength(N+c)+1`.
  - Proved `WeakBridge.BitLength.mem_endpointCrossingUnion_of_crosses`:
    every concrete crossing in the prefix belongs to the finite endpoint
    union.
  - Proved `WeakBridge.BitLength.endpointCrossingUnion_card_le`:
    the finite endpoint union has cardinality at most
    `c * (bitLength(N+c)+1)`.
  - This gives the expected coarse `O(c log N)` boundary size for fixed
    additive perturbation `c`.  It is not yet the affine return-branch
    theorem, and it does not prove low-`v2` decay by itself.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: convert this identity-branch boundary count to
  the monotone affine case.  The needed form is for
  `F(t)=a*t+b`: compare `F(t)` and `F(t)+c`, count crossings of dyadic
  endpoints in `F([0,N))`, and track the factor introduced by the slope
  `a`.

### 2026-05-26 (A0 weak branch: fixed endpoint crossing count) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.crossesDyadicEndpoint` and
    `WeakBridge.BitLength.dyadicBackNeighborhood`.
  - Proved `WeakBridge.BitLength.dyadic_boundary_mem_back_neighborhood`:
    if `(t,t+c]` crosses `2^k`, then `t` lies in the backward window
    `[2^k-c, 2^k)`.
  - Proved `WeakBridge.BitLength.fixed_dyadic_endpoint_crossing_count_le`:
    for fixed `N,c,k`, at most `c` values of `t < N` cross the fixed
    endpoint `2^k` under the perturbation `(t,t+c]`.
  - This is still local to one endpoint.  The next missing step is a
    finite union/count over all endpoints relevant to a dyadic block, and
    then the affine pullback version for `a*t+b`.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: prove a finite endpoint-union bound for
  `t < N`, likely of size `O(c * bitLength(N+c))`, then specialize or
  adapt it to monotone affine return branches.

### 2026-05-26 (A0 weak branch: dyadic-boundary crossing lemmas) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.exists_dyadic_boundary_of_bitLength_add_ne`:
    if `n != 0` and `bitLength(n+c) != bitLength n`, then some power
    `2^k` lies in `(n, n+c]`.
  - Added `WeakBridge.BitLength.exists_dyadic_boundary_of_bitLength_sub_ne`:
    if `c <= n`, `n-c != 0`, and subtraction changes bit length, then
    some power `2^k` lies in `(n-c, n]`.
  - These are the exact formal boundary statements needed before any
    finite/asymptotic count.  They do not yet count how often the event
    occurs for affine forms.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: prove a counting bound for intervals crossing
  dyadic endpoints, first for identity intervals `(t,t+c]`, then for
  monotone affine intervals `(a*t+b, a*t+b+c]` or
  `(a*t+b-c, a*t+b]`.

### 2026-05-26 (A0 weak branch: bit-length same-window lemmas) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.bitLength_eq_succ_of_pow_le_lt`: if
    `2^k <= n < 2^(k+1)`, then `bitLength n = k+1`.
  - Added `WeakBridge.BitLength.bitLength_add_eq_of_same_window` and
    `WeakBridge.BitLength.bitLength_sub_eq_of_same_window`: adding or
    subtracting a perturbation preserves bit length when both endpoints
    remain in the same dyadic window.
  - These lemmas make the archimedean boundary explicit: the only places
    where a bounded additive perturbation can change bit length are the
    short neighborhoods of dyadic window endpoints.  The next step is to
    count or average those neighborhoods for the affine return branches.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: prove a finite counting lemma for dyadic-window
  endpoint neighborhoods, then apply it to affine forms `a*t+b` on fixed
  source congruence classes.

### 2026-05-26 (A0 weak branch: bit-length scale primitive) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.BitLength.bitLength`, matching Python's
    `int.bit_length` at zero and `Nat.log 2 n + 1` for positive `n`.
  - Proved `WeakBridge.BitLength.bitLength_two_mul` and
    `WeakBridge.BitLength.bitLength_mul_two`: for `n != 0`,
    multiplying by `2` increases bit length by exactly one.
  - This is only the first formal primitive for the revised 10.M route.
    It does not yet prove affine bit-length average cancellation, but it
    gives the exact homogeneous dyadic scaling identity needed by that
    future lemma.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: formulate the affine perturbation step:
  compare `bitLength (a * t + b)` with `bitLength (a * (2 * t) + b)`
  outside explicitly counted threshold intervals, then lift that to
  adjacent dyadic block averages for the `2^-delta` weights.

### 2026-05-26 (A0 weak branch: delta boundary route corrected) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `lean/TODO.md`
- Notes:
  - Ran a non-persistent diagnostic using the existing script-`125`
    tracing code to compare actual adjacent dyadic block averages
    `[0,N)` vs `[N,2N)` for selected phases and the killed/truncated
    kernel with `S=75,A=10`.
  - The period-pair diagnostic from script `125` can show positive
    density of `delta_only` changes, so the naive route "delta changes
    only on a small boundary" is too strong as a global proof strategy.
  - The actual adjacent-block averages are much smaller and compatible
    with script `122`; for example phase `0|3|0` drops from block L1
    about `0.006874` at `N=2^12` to about `0.000156` at `N=2^24` in the
    sampled check.
  - Interpretation: the next theorem should not try only to prove small
    pointwise boundary mass.  It should prove dyadic scale-invariance or
    block-average cancellation for affine bit-length weights of the form
    `2^{-(bit_length(next_t)-bit_length(t))}` on fixed returning labels.
  - No new script or note file was created in this step.
- Next recommended task: formulate the affine bit-length average lemma
  precisely.  Candidate target: for fixed positive affine return branches
  on a congruence class, prove that the adjacent dyadic block discrepancy
  of `2^{-(bit_length(F(t))-bit_length(t))}` tends to zero, with separate
  exceptional sets for drops, valuation tails, and non-return tails.

### 2026-05-26 (A0 weak branch: delta-only boundary reduction) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.FiniteSplit.dyadicWeight δ = 2^{-δ}` and basic
    bounds `dyadicWeight_nonneg`, `dyadicWeight_le_one`, and
    `abs_dyadicWeight_sub_le_one`.
  - Added the Lean theorem
    `WeakBridge.FiniteSplit.weighted_dyadic_delta_boundary_le`: if two
    finite delta fields agree off a boundary predicate, then the weighted
    average of `|2^{-delta_1}-2^{-delta_2}|` is bounded by the weighted
    mass of that boundary.
  - This matches the script-`125` reduction where the residual killed
    kernel mismatch is `delta_only`.  It does not prove that the actual
    Collatz bit-length boundary has small mass; that remains the open
    10.M estimate.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: define the concrete boundary predicate for the
  A0 returning phases, probably in terms of `bit_length(next_t)` changing
  under `t -> t + 2^m`, then prove or falsify that its block-average mass
  tends to zero for each fixed low-`v2` phase/truncation.

### 2026-05-26 (A0 weak branch: finite low/tail split lemma) — Codex + Piero Borgatta

- Tasks advanced: 10.N; 10.M remains the active missing mathematical
  input.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.FiniteSplit.weightedSubsum` and
    `WeakBridge.FiniteSplit.weightedSubmass` to name predicate-restricted
    finite weighted sums.
  - Added the Lean theorem
    `WeakBridge.FiniteSplit.weighted_sum_le_low_plus_tail`: for a
    nonnegative finite weight `mu`, if a discrepancy `d` is bounded by
    `B` on a tail predicate `High`, then the full weighted sum is bounded
    by the exact low contribution plus `B` times the high-tail mass.
  - This is only the formal low/tail bookkeeping lemma.  It does not
    identify the Collatz low set, does not prove the low-`v2` decay, and
    does not close Gate 10.B.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: keep 10.M as the main target.  State a
  Collatz-specific finite lemma for the returning-phase `delta_only`
  obstruction, then try to reduce it to a bit-length/`delta` boundary
  estimate on fixed bounded congruential return labels.

### 2026-05-26 (A0 weak branch: real high-v2 tail mass lemma) — Codex + Piero Borgatta

- Tasks advanced: 10.L.
- Artifacts modified:
  - `CollatzShadowing/WeakBridge.lean`
  - `lean/TODO.md`
- Notes:
  - Added `WeakBridge.TailCount.tailCount` and
    `WeakBridge.TailCount.totalCount` to name the two-prefix source-tail
    numerator and denominator used by the A0 high-`v2` source model.
  - Added the Lean theorem
    `WeakBridge.TailCount.dyadic_tail_mass_le`, upgrading the existing
    integer bound `tail_count * 2^q <= total_count` to the real mass
    statement `tail_count / total_count <= 1 / 2^q` whenever the total
    positive source count is nonzero.
  - This closes only the high-`v2` tail half of the A0 weak double-limit
    split.  It does not prove low-`v2` decay, Gate 10.B, spectral gap, or
    Collatz.
  - Verification: `lake build CollatzShadowing.WeakBridge` succeeded
    (`3285` jobs), and `lake build CollatzShadowing` succeeded (`3349`
    jobs).
- Next recommended task: attack 10.M by formulating the returning-phase
  bit-length/`delta` boundary lemma; the current evidence says the
  residual killed-kernel mismatch is `delta_only`, so the next proof
  target should bound block averages of
  `|2^-delta(t+2^m)-2^-delta(t)|` on fixed bounded congruential return
  labels.

### 2026-05-25 (A0 weak branch: top-Haar formulation) — Codex + Piero Borgatta

- Tasks advanced: 10.M.
- Artifacts produced or updated:
  - `scripts/spectral_program/122_A0_top_haar_decay_summary.py`
  - `scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_report.md`
  - `scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_phase_fits.csv`
  - `scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_threshold_fits.csv`
  - `scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_case_points.csv`
  - `scripts/spectral_program/123_A0_bounded_periodicity_probe.py`
  - `scripts/spectral_program/collatz_123_current_A0_A0_bounded_periodicity_probe_report.md`
  - `scripts/spectral_program/collatz_123_current_A0_large_m_A0_bounded_periodicity_probe_report.md`
  - `scripts/spectral_program/124_A0_tail_grid_probe.py`
  - `scripts/spectral_program/collatz_124_current_A0_A0_tail_grid_probe_report.md`
  - `scripts/spectral_program/collatz_124_current_A0_spread_A0_tail_grid_probe_report.md`
  - `scripts/spectral_program/125_A0_kernel_mismatch_decomposition.py`
  - `scripts/spectral_program/collatz_125_current_A0_spread_A0_kernel_mismatch_decomposition_report.md`
  - `notes/phase10_A0_low_v2_mechanism_2026-05-25.md`
  - `notes/phase10_A0_dyadic_discrepancy_lemma_2026-05-25.md`
  - `notes/phase10_index.md`
  - `notes/phase10_master_report.md`
  - `notes/phase10_repro_manifest.md`
  - `lean/TODO.md`
- Notes:
  - Script `122` rewrites script-`111` A0 phase-strata data in top
    dyadic Haar form:
    `root_haar_l1(N) = ||mean_[N,2N) - mean_[0,N)||_1 = 2 * row_l1(N)`.
  - Threshold fits remain near alpha `0.6`; for `v2 < 8`, latest root
    component is `0.0005326722352`, about `93.2%` of total root drift.
  - This sharpens 10.M: prove top dyadic block-discrepancy decay for
    each fixed low-`v2` phase.  The exact high-`v2` tail from 10.L then
    supplies the outer `R -> infinity` step.
  - The candidate proof route is now stated and corrected in
    `notes/phase10_A0_dyadic_discrepancy_lemma_2026-05-25.md`: bounded
    finite-depth congruential signatures should be exactly periodic modulo
    a power of two, intermediate high-valuation tails should have dyadic
    mass `<= S * 2^-A`, and the genuine bottlenecks are the archimedean
    `delta/drop` boundary term and the return-depth tail.
  - Script `123` confirms the split: for `S=25,A=8`, pure valuation-word
    mismatches vanish at large `m` (`0/128` for all tested phases at
    `m=192,193,200`), while the actual kernel keeps small residual
    mismatches (`0/128` to `9/128`) and the `shadow_return` tail rates are
    still around `0.82`-`0.87`.
  - Script `124` with distributed block sampling shows the symbolic tail
    is pessimistic: at `S=75,A=10`, symbolic return-tail mean is `0.5`,
    but killed-kernel unresolved tail mean is `0`; two tested phases are
    full-return phases and two are full-drop phases on the distributed
    sample.
  - Script `125` decomposes the remaining killed-kernel mismatch.  For all
    tested `(S,A)`, nonzero pointwise L1 is entirely `delta_only`; there
    are no destination-label changes, no drop/return flips, and no
    tail/return boundaries.  At `S=75,A=10`, aggregate point L1 mean is
    `0.02276611328` and nonzero rate is `0.1821289062`.
- Next recommended task: state and test the bit-length/`delta` boundary
  lemma for returning phases.  The target should bound the block average of
  `|2^-delta(t+2^m)-2^-delta(t)|` on fixed bounded congruential return
  labels.

### 2026-05-25 (A0 weak branch: exact high-v2 tail) — Codex + Piero Borgatta

- Tasks advanced: 10.K, 10.L; 10.M opened as the active proof target.
- Artifacts produced or updated:
  - `CollatzShadowing/WeakBridge.lean`
  - `CollatzShadowing.lean`
  - `scripts/spectral_program/117_A0_v2_tail_formula.py`
  - `scripts/spectral_program/collatz_117_current_A0_A0_v2_tail_formula_report.md`
  - `notes/phase10_A0_v2_tail_formula_2026-05-25.md`
  - `notes/phase10_A0_finite_weak_bridge_2026-05-25.md`
  - `notes/phase10_A0_weak_approximation_theorem_2026-05-25.md`
  - `notes/phase10_index.md`
  - `notes/phase10_master_report.md`
  - `notes/phase10_repro_manifest.md`
  - `lean/TODO.md`
  - `scripts/spectral_program/118_A0_low_v2_phase_decay_probe.py`
  - `scripts/spectral_program/119_A0_low_v2_return_depth_probe.py`
  - `scripts/spectral_program/120_A0_dependency_depth_probe.py`
  - `scripts/spectral_program/121_A0_walsh_haar_probe.py`
  - `scripts/spectral_program/collatz_118_current_A0_A0_low_v2_phase_decay_probe_report.md`
  - `scripts/spectral_program/collatz_119_T14_j64_128_sample_A0_low_v2_return_depth_probe_report.md`
  - `scripts/spectral_program/collatz_120_T14_j128_sample_A0_dependency_depth_probe_report.md`
  - `scripts/spectral_program/collatz_121_T14_j128_sample_A0_walsh_haar_probe_report.md`
  - `notes/phase10_A0_low_v2_mechanism_2026-05-25.md`
- Notes:
  - The finite row-source bridge is formalized as
    `CollatzShadowing.WeakBridge.weighted_action_diff_le`.
  - The high-`v2` A0 source-tail mass is no longer empirical in the
    current script-`111` source model.  It is exactly
    `(floor((L - 1)/2^R) + floor((R' - 1)/2^R))/(L + R' - 2) <= 2^-R`
    for the two compared prefixes with `t=0` excluded.
  - The integer core is formalized as
    `CollatzShadowing.WeakBridge.TailCount.dyadic_tail_count_mul_le`.
  - Verification passed:
    `python3 -m py_compile scripts/spectral_program/117_A0_v2_tail_formula.py`,
    `lake build CollatzShadowing.WeakBridge`, and
    `lake build CollatzShadowing`.
  - Script `118` shows the low-`v2` decay is broad but not uniform by
    phase: for `v2 < 8`, median per-phase alpha is `0.6112066004`, while
    slower phases include `7|3|h`, `7|1|h`, `6|1|h`, and `3|1|h`.
  - Script `119` retraces representative phases and finds
    `prefix_l1 / half_l1 = 0.5` exactly, so the remaining low-`v2`
    obstruction is dyadic block discrepancy.  The largest pieces are
    medium-depth returns (`step 11-25`, `delta 0` or `1-3`), not
    long-return tails.
  - Script `120` tests the naive dependency-depth/local-constancy route.
    It is not clean: for `0|3|0`, return-phase majority error drops from
    `0.712411342` at `m=8` to `0.046751945` at `m=20`, but by then the
    singleton fraction is already `0.389220953`; for the medium-return
    subset, error remains `0.256938037` at `m=18` with singleton fraction
    `0.765021584`.
  - Script `121` computes the Walsh-Haar spectrum.  The signals are rough
    at fine scales, with about half the `L2` Haar energy at block size `2`,
    but the root coefficient is tiny: for `0|3|0` return/phase, root
    half-L1 is `0.000413223985`; for `7|3|0`, it is `0.007874965668`.
    Therefore the precise target is top dyadic Haar coefficient decay, not
    global smoothness or small high-frequency energy.
  - This does not prove Collatz and does not close Gate 10.B.  It removes
    one obstacle from the A0 weak-approximation program.
- Next recommended task: 10.M — prove or falsify fixed-threshold low-`v2`
  decay `D_N(v2 < R) -> 0`; next diagnostic should measure top-Haar
  coefficient decay across larger prefix scales and across all low-`v2`
  phases, not just representative samples.

### 2026-05-20 (conditional Collatz proof bridge) — Codex + Piero Borgatta

- Tasks advanced: 11.A, 11.B, 11.C.
- Artifacts modified:
  - `CollatzShadowing/CollatzBridge.lean`
  - `CollatzShadowing.lean`
  - `CollatzShadowing/INVENTORY.md`
  - `lean/TODO.md`
- Notes:
  - Added a new Lean module for the proof bridge from global accelerated
    strict descent to Collatz-type termination statements.
  - `UniformStrictDescentHypothesis` is now the explicit missing global
    hypothesis: for every positive odd `n ≠ 1`, some finite accelerated
    Syracuse iterate must be positive odd and strictly smaller than `n`.
  - `acceleratedCollatz_of_uniformStrictDescent` is fully formalized and
    proves, by strong induction, that this descent hypothesis implies
    accelerated termination at `1`.
  - `ClassicalCollatzConjecture`, `AcceleratedToClassicalBridge`, and
    `classicalCollatz_of_uniformStrictDescent` separate the standard
    full-Collatz-to-accelerated bookkeeping from the genuinely hard
    finite-shadowing coverage problem.
  - This is not a proof of Collatz: the hard missing step is still to
    prove that the finite phantom-shadowing/CW layer implies
    `UniformStrictDescentHypothesis`.
  - Verification: `lake build CollatzShadowing.CollatzBridge` succeeded
    (`1793` jobs), and `lake build CollatzShadowing` succeeded (`3348`
    jobs).
- Next recommended task: formalize the elementary
  `AcceleratedToClassicalBridge`, then define a precise finite-shadowing
  coverage hypothesis whose conclusion is `UniformStrictDescentHypothesis`.

### 2026-05-20 (finite-rank note synchronized with Lean sensitivity imports) — Codex + Piero Borgatta

- Tasks advanced: 10.G.
- Artifacts modified:
  - `paper/finite_rank_cw_note.tex`
  - `lean/TODO.md`
- Notes:
  - The finite-rank note was updated after the Lean integration of the
    `lift_bits = 5,6` deterministic sensitivity certificates.
  - The sensitivity section now calls these Lean-checked sensitivity
    certificates, cites
    `k16s16KLB5DeterministicGeneratedSpectralRadiusBound` and
    `k16s16KLB6DeterministicGeneratedSpectralRadiusBound`, and records
    the corresponding generated Lean modules in the reproducibility
    table.
  - The production theorem remains the `lift_bits = 4` K16
    deterministic certificate; the `lift_bits = 5,6` certificates are
    robustness checks and still do not imply convergence in
    `lift_bits`, an infinite transfer operator, a spectral gap,
    Conjecture 6, or Collatz.
  - Local TeX rendering could not be run in this environment: `latexmk`,
    `pdflatex`, `latex`, `xelatex`, `lualatex`, and `tectonic` are not
    installed.  The last Lean verification remains the successful
    `lake build CollatzShadowing` run after importing the sensitivity
    modules.
  - After an external compile problem was reported, the TeX note was
    made more portable: nonessential package dependencies
    (`lmodern`, `booktabs`, `microtype`, `seqsplit`) were removed, the
    code macro was changed to use `\detokenize` so underscores in file
    names and Lean declarations do not break compilation, and the
    reproducibility table was converted to a `description` list to
    avoid wide-table failures.
  - After a PDF screenshot showed right-edge clipping in the
    reproducibility section, that section was rewritten as a
    fixed-width minipage with SHA-256 hashes grouped in eight-character
    chunks.  This preserves the data while avoiding overfull monospaced
    lines.
- Next recommended task: render `paper/finite_rank_cw_note.tex` on a
  machine with a TeX installation and perform an editorial pass for
  table width/page breaks before treating it as a shareable PDF.

### 2026-05-16 (Phase 10.G paper-facing finite-rank draft) — Codex + Piero Borgatta

- Tasks advanced: 10.G, 10.J.
- Artifacts modified:
  - `notes/phase10_finite_rank_note_outline.md`
  - `lean/TODO.md`
- Notes:
  - No new analytic metric or Banach-space claim was added.
  - The finite-rank fallback outline now includes a paper-facing draft
    block with finite model declaration, matrix construction, theorem
    statement, finite Collatz-Wielandt proof sketch, Lean boundary,
    sensitivity checks, and limitations.
  - The draft states only the K16 deterministic finite residue-cell
    theorem.  It does not claim an infinite transfer operator, a
    spectral gap, convergence in `K` or `lift_bits`, Conjecture 6, or
    Collatz.
  - The `lift_bits = 5,6` sensitivity checks were regenerated as
    permanent artifacts with prefixes
    `scripts/phantom_taxonomy/deterministic_k16_s16_residue_lb5` and
    `scripts/phantom_taxonomy/deterministic_k16_s16_residue_lb6`.
    Their exact Python certificates verify with the previously reported
    max ratios.
  - Piero then requested Lean imports for those sensitivity checks.
    Generated modules
    `CollatzShadowing/Generated/K16S16KLB5DeterministicCW.lean` and
    `CollatzShadowing/Generated/K16S16KLB6DeterministicCW.lean` now
    expose `k16s16KLB5DeterministicGeneratedSpectralRadiusBound` and
    `k16s16KLB6DeterministicGeneratedSpectralRadiusBound`.  `lake build
    CollatzShadowing.Generated.K16S16KLB5DeterministicCW
    CollatzShadowing.Generated.K16S16KLB6DeterministicCW` succeeds.
  - The older duplicated limitations paragraph was removed from the
    remaining-editorial section to keep the file compact.
- Next recommended task: choose the publication form for the finite-rank
  deliverable: v4 section, standalone note, or supplementary
  computational note.  Do not promote K20 until a production SCC input
  is declared.

### 2026-05-15 (Phase 10.C serious Banach pair) — Codex + Piero Borgatta

- Tasks advanced: 10.C, 10.E.
- Artifacts modified:
  - `notes/phase10_mixed_norm_candidate.md`
  - `lean/TODO.md`
  - `scripts/spectral_program/112_martingale_variation_proxy.py`
  - `scripts/spectral_program/collatz_112_martingale_variation_proxy_report.md`
  - `scripts/spectral_program/116_projected_residual_lift.py`
  - `scripts/spectral_program/collatz_116_T15_d2_tail3_refined_projected_residual_lift_report.md`
  - `notes/phase10_finite_rank_note_outline.md`
- Notes:
  - The active no-collaborator analytic candidate is now a concrete
    Banach pair, not a generic Hölder analogy: `B_s` is
    `L_infty +` weighted martingale variation over the Haar/cylinder
    filtration on `Z_2 x H`, and `B_w = L1(mu)`.
  - Compactness `B_s -> B_w` is supplied by the finite martingale
    truncations `E_N`:
    `||f - E_N f||_1 <= a_{N+1}^{-1} Var_a(f)`.
  - The retained-return Lasota-Yorke target is
    `Var_a(U_ret,s f) <= alpha Var_a(f) + C ||f||_1`, with
    `alpha < 1`.  This is only a target.
  - Hennion/Keller-Liverani remain inactive until `L1Bound`,
    `DepthDistortion`, `BoundaryVariation`, `LossSeparation`, and
    `FiniteApproxMixed` are proved or replaced by precise computable
    hypotheses.
  - Script `112` translates existing child-cylinder TV outputs into
    finite proxies for martingale increments `||d_n K||_1`.  The first
    output is cautionary: on the available `T=15` windows, phase
    increments are nearly flat/slightly decreasing, while full and
    delta increments increase over the tested depths.
  - Existing script-`102` enriched-state diagnostics suggest the
    label-excess obstruction is structurally concentrated: at `T=15`,
    depth `2`, `source_odd_3_or_v2_2` carries about `0.808025` of
    full-over-phase excess on mass `0.562469`, with complement p95 `0`.
    This supports splitting phase variation from structured label
    excess rather than forcing one full-label martingale norm.
  - Script `113` now makes that split explicit.  Current finite proxies
    show phase increments large and nearly flat (`~0.041--0.045`),
    label-excess structurally concentrated, and loss/status nontrivial.
    The reduced analytic target is now phase martingale LY plus
    structured label-excess correction plus weak substochastic loss
    control.
  - Follow-up script-`100` run `T15_d4_tail1` adds one 2-adic depth at
    the same `64` lift budget.  Phase improves only mildly
    `0.0425999 -> ... -> 0.0389357`, while full and delta increments
    increase to `0.0648212` and `0.0600595`.  This reinforces the
    no-Hennion/no-KL status for the current operator.
  - Script `114` checks whether the phase obstruction is localized like
    label-excess.  Current answer: no.  The strongest contributors are
    broad half-space classes such as `source_v2=0` with mass `0.5` and
    contribution about `0.687`, leaving complement mean around
    `0.026--0.028`.
  - Script `115` finds a narrower positive route: the broad phase
    obstruction is mostly a low destination mode.  Projection to
    `dst_v2` captures `0.882872 -> 0.934651` of phase-TV over
    `T15_d4_tail1` depths `0..4`, with residual mean
    `0.00498962 -> 0.00254440`.  On the observable/Koopman side, the
    only live LY repair is now `U = U Pi_v2 + U Q_v2`, with LY attempted
    on `U Q_v2`.
  - Script `116` tests whether this repair survives an explicit lift
    inside each destination `v2` fiber.  The optimistic pair-dependent
    residual is small (`0.00730881 -> 0.00440467` on depths `0..2`),
    but global/uniform lifts are essentially as bad as phase TV, and a
    finite `source PhaseState`-conditioned lift remains too large
    (`0.0163037 -> 0.0197842`).  Thus `Pi_v2` is not yet a valid LY
    repair without a richer canonical lift or new quotient.
  - Follow-up script `116` source-refined run tested
    `(source PhaseState, r mod 2^k)` for `k = 0,2,4,6,8`.  This simple
    refinement does not close the lift problem: at depth `2`,
    `source_refined_b8_residual = 0.0196251`, still far above the
    pair-dependent residual `0.00440467`.
  - After this negative result, the finite-rank K16 fallback was
    reverified as the active rigorous deliverable:
    `python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify ...`
    returns `status=OK`, and
    `lake build CollatzShadowing.Generated.K16S16KDeterministicCW`
    succeeds with `3302 jobs`.
  - The existing K20 smoke CW JSON was also reverified with the Python
    verifier (`status=OK`, max ratio
    `42001755821431/62996587868160`), but remains explicitly not
    production because its SCC input is only a smoke sample.
  - Local K20 promotion was checked and deliberately not run: only
    `orbit_harness_k20_smoke_*`, `deterministic_k20_smoke_*`, and
    `notes/phantom_taxonomy_k20_smoke_scc_report.md` are present.  There
    is no declared production K20 SCC input in the workspace.
- Next recommended task: do not merely increase the residue refinement
  parameter.  Either identify a new quotient/Galerkin interpretation
  that makes the pair-dependent lift canonical, or pause the analytic LY
  route and return to the finite-rank deliverable.  Do not use the
  pair-dependent residual as a theorem-level projection.

### 2026-05-15 (Phase 10.B conditional closure attempt) — Codex + Piero Borgatta

- Tasks advanced: 10.B, 10.C, 10.D.
- Artifacts added/modified:
  - `notes/phase10_gate10B_conditional_closure.md`
  - `notes/phase10_A0_averaged_interpretation.md`
  - `notes/phase10_decision_tree.md`
  - `notes/phase10_reduced_core.md`
  - `lean/TODO.md`
- Notes:
  - A possible no-collaborator solution to 10.B was identified, but only
    in a weak conditional-expectation sense.
  - The proposed infinite source model is `X = Z_2 x H` with
    Haar/counting measure, killed return domain `D`, return map `tau`,
    return exponent `delta`, and source observation
    `pi_V : X -> PhaseState V`.
  - The active candidate operator is the killed weighted forward kernel
    `(U_s f)(x,h) = 1_D(x,h) 2^{-s delta(x,h)}
    f(pi_V(tau(x,h)))`.
  - The A0 quotient is interpreted as
    `E_mu[U_s 1_q | sigma(pi_V)]`, i.e. a conditional expectation, not
    an exact projection and not a claim that source-cell rows are
    constant on PhaseState fibers.
  - Script 107 already verifies finite bookkeeping for the current
    prefix data: row-source residuals are zero and the mixed-cell
    correction at `T=15` is `8/131072`, giving error coefficient
    `0.0001220703125 * ||F||_infty`.
  - Initial provenance audit:
    `T10CriticalSymbolic` is compatible as a finite Haar/counting
    quotient at depth `T=10`; `T10J32HighBitTail.full` is compatible as
    a high-bit prefix quotient with `j_count = 32 = 2^5`.  The
    `core/tail` split remains finite majority bookkeeping, not an
    infinite operator split.
  - Added reproducible checker
    `scripts/spectral_program/111_gate10b_provenance_check.py`; current
    report `scripts/spectral_program/collatz_111_gate10b_provenance_report.md`
    returns `critical_compatible=True` and `high_bit_compatible=True`.
  - P1/P2 analysis found the key obstruction: first return to monitored
    phantom tubes is 2-adic/cylindrical, but the script's `drop below
    start` terminal rule is archimedean and has no canonical `Z_2`
    analogue.  The current best route is to close 10.B for the retained
    2-adic return kernel and treat drop-below/budget events as external
    substochastic loss, or else enlarge the state space with arithmetic
    lift data.
  - P3/P4 now have local proof details: prefix windows are Haar
    cylinder averages, and the capped-valuation/odd-part boundary has
    mass bounded by `2^{-(T-1)}`, matching the observed `T=15` excluded
    mass `8/131072`.
- Next recommended task: if continuing the analytic branch, formulate
  the retained-return operator plus substochastic-loss decomposition as
  the only admissible 10.C/10.D object.  Otherwise keep the finite-rank
  note as the theorem-producing deliverable.  Do not infer
  Hennion/Keller-Liverani or spectral gaps from this.

### 2026-05-15 (Phase 10 no-collaborator route) — Codex + Piero Borgatta

- Tasks advanced: 10.B, 10.G, 10.I, 10.J.
- Artifacts modified:
  - `lean/TODO.md`
  - `notes/phase10_reduced_core.md`
  - `notes/phase10_decision_tree.md`
  - `notes/phase10_finite_rank_note_outline.md`
  - `notes/phase10_collaborator_brief.md`
  - `paper/finite_rank_cw_note.tex`
- Notes:
  - Piero requested explicitly to proceed without a collaborator.
  - Gate 10.B remains open: no exact infinite projection, spectral gap,
    Lasota-Yorke inequality, or Keller-Liverani/Hennion theorem is
    claimed.
  - The active no-collaborator deliverable is now the finite-rank
    computational note based on the K16 deterministic `(K,b)` certificate.
  - `A0-averaged` is retained only as conditional appendix/program
    material; `A1` is archived as a secondary diagnostic.
  - Verified:
    `python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify
    scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json`
    from the repository root, and
    `lake build CollatzShadowing.Generated.K16S16KDeterministicCW`
    from `lean/`.
  - A first standalone TeX draft now exists as
    `paper/finite_rank_cw_note.tex`; local LaTeX rendering was not
    available in the Codex shell (`pdflatex`, `xelatex`, `lualatex`, and
    `tectonic` were not found).
- Next recommended task: render and polish
  `paper/finite_rank_cw_note.tex` in an environment with LaTeX, or
  decide whether to merge it into v4 as a section/supplement. Do not
  resume analytic Phase 10 unless an internal proof-quality
  operator/norm bridge is found.

### 2026-05-13 (Phase 9 v3 publication synced) — Codex + Piero Borgatta

- Tasks advanced: closed Phase 9 (`9.1`-`9.8`) in this TODO after
  Piero confirmed that paper `v3` had already been completed and
  published.
- Artifacts modified:
  - `lean/TODO.md`
- Notes:
  - This was a TODO synchronization, not a new paper-editing session.
  - The v3 Zenodo record is `https://zenodo.org/records/20160154`, with
    DOI `10.5281/zenodo.20160154`.
  - The local workspace still primarily contains v2-named paper files;
    if desired, a later housekeeping pass can mirror the exact v3 PDF,
    supplementary archive name, README DOI update, and checksums into the
    local tree.
- Next recommended task: with Phase 9 closed and Phase 10 now clarified
  as a planning/collaboration roadmap, the next concrete task is 10.A
  if the research program continues immediately; otherwise do local
  housekeeping to mirror the v3 artifacts.

### 2026-05-13 (Phase 10 roadmap refinement for v3 planning) — Codex + Piero Borgatta

- Tasks advanced: refactored Phase 10 from outcome-oriented analytic
  tasks into a planning roadmap for `v4` / companion paper /
  collaboration.
- Artifacts modified:
  - `lean/TODO.md`
- Notes:
  - Phase 10 is now explicitly `v3` planning only: it must not claim a
    spectral gap, close Conjecture 6, or promote speculative hypotheses
    into theorems.
  - The key fork is now Task 10.B: if a natural infinite transfer kernel
    and projection to the finite matrices are identified, continue to the
    analytic branch; otherwise switch to the finite-rank fallback branch.
  - Task 10.G is marked `[~]` because the deterministic finite
    residue-cell `(K,b)` certificate already exists in
    `CollatzShadowing/Generated/K16S16KDeterministicCW.lean`, while the
    general fallback theorem/claim remains to be formulated.
  - Chang 2026 compatibility is included as a column in the literature
    matrix rather than as a separate task.
  - Computational constant hunting is explicitly blocked until the
    candidate Banach space and operator formulation are fixed.
- Next recommended task: continue Phase 9 v3 redaction, especially 9.1
  and 9.5, using the revised Phase-10 wording for the paper's planned
  next steps.

### 2026-05-13 (F.1 deterministic residue-cell closure) — Codex + Piero Borgatta

- Tasks advanced: closed follow-up `F.1` for the declared finite
  residue-cell scope on the `K0 = 16` SCC.
- Artifacts added:
  - `scripts/phantom_taxonomy/deterministic_residue_transfer.py`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_edges.csv`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_KL_edges.csv`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_node_edges.csv`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_source_coverage.csv`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_manifest.json`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_transfer_summary.md`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json`
  - `scripts/phantom_taxonomy/deterministic_k16_s16_residue_exact_cw_certificate.md`
  - `lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean`
- Artifacts modified:
  - `lean/CollatzShadowing.lean`
  - `notes/phantom_taxonomy.md`
  - `notes/phantom_taxonomy_empirical_scc_integration.md`
  - `lean/TODO.md`
  - `scripts/phantom_taxonomy/lean_cw_summary.py`
- Notes:
  - The deterministic generator enumerates all `2^4` finite residue
    subclasses for each of the 1240 raw SCC source states: 19840 cells
    total, 17671 canonical source cells, 2169 shadowed initial cells,
    no no-initial classes, and zero budget exits.
  - The retained certified macro-state space is `(K,b)`: 37 states,
    182 nonzero internal edge types, 17671 source events, 17176
    internal transitions, and 495 exits below start.
  - The exact CW certificate verifies
    `max_ratio = 90833233962213/129559208330288 < 3/4`, with max node
    `K11:b2`.
  - `lean_cw_summary.py` now accepts declaration-prefix and state-type
    arguments, so the deterministic certificate can be imported next to
    the empirical 37-state certificate without namespace collisions.
  - Sensitivity runs at `lift_bits = 5` and `lift_bits = 6` also pass
    with `alpha = 3/4`; their exact max ratios are
    `7332495524923/10616480126384 ≈ 0.690671054590` and
    `64869145309473/97226913303232 ≈ 0.667193301788`.
  - The raw-node and `(K,L,b)` deterministic edge CSVs are retained as
    diagnostics; the exact CW closure uses `(K,b)`.
- Verification:
  - `python3 -m py_compile scripts/phantom_taxonomy/deterministic_residue_transfer.py`
    succeeds.
  - `python3 scripts/phantom_taxonomy/deterministic_residue_transfer.py
    --representatives scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
    --scc-nodes scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_nodes.csv
    --scc-rank 1 --max-k 16 --lift-bits 4 --max-steps 1000
    --out-prefix scripts/phantom_taxonomy/deterministic_k16_s16_residue`
    succeeds with zero budget exits.
  - `python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify
    scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json`
    returns `status=OK`.
  - `lake build CollatzShadowing.Generated.K16S16KDeterministicCW`
    succeeds.
  - `lake build` succeeds.
- Next recommended task: Phase 9 v3 redaction can now cite the
  deterministic finite residue-cell `(K,b)` certificate rather than the
  sampled transition probabilities.

### 2026-05-13 (B closed form and deterministic gap triage) — Codex + Piero Borgatta

- Tasks advanced: restored the deferred formal closed form for
  `PhantomWord.B`; triaged the remaining deterministic-transition gap
  as a theorem-level follow-up outside the completed sampled Phase-7
  branch.
- Artifacts modified:
  - `lean/CollatzShadowing/Auxiliary.lean`
  - `lean/TODO.md`
- New declarations:
  - `PhantomWord.B_closed_form`
- Notes:
  - `B_closed_form` now proves
    `w.B m = (m / w.length) * w.A + (w.vals.take (m % w.length)).sum`.
  - The deterministic-transition gap cannot be closed by the existing
    sampled matrices alone. It requires replacing orbit-harness samples
    with a residue-class transition construction, then rerunning the
    exact CW pipeline on the deterministic matrix.
- Verification:
  - `lake build CollatzShadowing.Auxiliary` succeeds.
- Next recommended task: decide whether to tackle follow-up `F.1`
  before Phase 9, or keep Phase 9 framed honestly as empirical
  taxonomy integration plus Lean-checked generated certificates.

### 2026-05-13 (Phase 8.7 axiom removal) — Codex + Piero Borgatta

- Tasks advanced: **8.7 hardened to a fully Lean-checked generated
  certificate**. The previous trusted generated boundary/`axiom` has
  been removed.
- Artifacts modified:
  - `lean/CollatzShadowing/Generated/T10J32HighBitTailCW.lean`
  - `lean/CollatzShadowing/Generated/T10J32HighBitTailCWData.lean`
  - `lean/CollatzShadowing/Generated/T10J32HighBitTailCWRows00.lean`
    through `lean/CollatzShadowing/Generated/T10J32HighBitTailCWRows13.lean`
  - `scripts/phantom_taxonomy/lean_t10j32_cw.py`
  - `lean/README.md`
  - `lean/TODO.md`
- New/updated declarations:
  - `Generated.T10J32HighBitTailState`
  - `Generated.t10j32HighBitTailMatrix`
  - `Generated.t10j32HighBitTailCWBasis`
  - `Generated.t10j32HighBitTailEvaluatedRows`
  - `Generated.t10j32HighBitTailFiniteCWCertificate`
  - `Generated.t10j32HighBitTailSpectralRadiusBound_97_2000`
- Notes:
  - The generator still computes and checks the positive integer CW
    vector and exact cleared rational row inequalities before writing
    Lean, but it now emits explicit per-row `EvaluatedCWRowBound`
    witnesses. Lean checks each row evaluation over the generated
    `Fin 224` matrix from the exact CSV.
  - The generated row modules avoid recursive `simp` unfolding by using
    explicit summand terms and concrete `change` proofs for nonzero row
    entries.
- Verification:
  - `lake build CollatzShadowing.Generated.T10J32HighBitTailCW`
    succeeds.
  - `lake build` succeeds.
  - `rg -n "\\b(axiom|sorry|admit)\\b" CollatzShadowing/Generated/T10J32HighBitTailCW*.lean ../scripts/phantom_taxonomy/lean_t10j32_cw.py`
    returns no matches.
- Next recommended task: Phase 9 paper redaction by Piero; no remaining
  Phase-7/8 technical task is open on this branch.

### 2026-05-12 (Phase 8.7 and 7.4 closure) — Codex + Piero Borgatta

- Tasks advanced: **8.7 complete**, **7.4 complete**, and **7.5 closed
  as not applicable** after 7.4 outcome (b).
- Artifacts modified:
  - `lean/CollatzShadowing.lean`
  - `lean/CollatzShadowing/Generated/T10J32HighBitTailCW.lean`
  - `scripts/phantom_taxonomy/lean_t10j32_cw.py`
  - `lean/README.md`
  - `lean/TODO.md`
- New declarations:
  - `Generated.t10j32HighBitTailAlpha`
  - `Generated.t10j32HighBitTailAlphaNNReal`
  - `Generated.t10j32HighBitTailCWCertificate`
  - `Generated.t10j32HighBitTailSpectralRadiusBound`
  - `Generated.t10j32HighBitTailSpectralRadiusBound_97_2000`
- Notes:
  - The generator constructs a positive integer CW vector for the
    imported `T = 10, j = 32` full matrix and verifies all cleared
    rational row inequalities exactly against
    `high_bit_tail_edges_T10_j32.csv`.
  - Directly expanding all 224 row certificates in Lean was attempted
    but was too slow in the local Mathlib kernel. The final module
    therefore exposes the exact generator-verified row check as a
    trusted generated Lean boundary and then applies the already proved
    spectral-radius bridge.
  - 7.4 is now marked complete with outcome (b); 7.5 is marked
    complete/not-applicable because its condition was outcome (a).
- Verification:
  - `lake build CollatzShadowing.Generated.T10J32HighBitTailCW`
    succeeds.
  - `lake build` succeeds.
- Next recommended task: Phase 9 paper redaction by Piero; no remaining
  Phase-7/8 technical task is open on this branch.

### 2026-05-12 (Phase 8.5 — empirical PhaseState transfer import) — Codex + Piero Borgatta

- Tasks advanced: **8.5 complete** for the concrete `T = 10, j = 32`
  majority import.
- Artifacts modified:
  - `lean/CollatzShadowing.lean`
  - `lean/CollatzShadowing/Generated/T10CriticalSymbolic.lean`
  - `lean/CollatzShadowing/Generated/T10J32HighBitTail.lean`
  - `scripts/phantom_taxonomy/export_high_bit_tail_edges.py`
  - `scripts/phantom_taxonomy/lean_phase_transfer.py`
  - `scripts/phantom_taxonomy/lean_high_bit_tail.py`
  - `scripts/phantom_taxonomy/high_bit_tail_edges_T10_j32.csv`
  - `lean/README.md`
  - `lean/CollatzShadowing/INVENTORY.md`
  - `lean/CollatzShadowing/EPISODE_INVENTORY.md`
  - `lean/TODO.md`
- New declarations:
  - `Generated.t10CriticalSymbolicFull`
  - `Generated.t10CriticalSymbolicFull_rowSubstochastic`
  - `Generated.t10CriticalSymbolicBaselineDecomposition`
  - `Generated.t10j32HighBitTailCore`
  - `Generated.t10j32HighBitTailTail`
  - `Generated.t10j32HighBitTailFull`
  - `Generated.t10j32HighBitTailFull_eq_core_add_tail`
  - generated row supports and row-sum lemmas for all active
    `core`, `tail`, and `full` rows
  - `Generated.t10j32HighBitTailCore_rowSubstochastic`
  - `Generated.t10j32HighBitTailTail_rowSubstochastic`
  - `Generated.t10j32HighBitTailFull_rowSubstochastic`
  - `Generated.t10j32HighBitTailDecomposition`
- Notes:
  - The generated module imports the exact rational `T = 10`
    critical-symbolic transfer matrix from
    `collatz_75_critical_symbolic_edges.csv`.
  - The baseline decomposition deliberately uses `core = full` and
    `tail = 0`; it checks the generated empirical matrix against the
    `OperatorDecomposition` API but is not yet the majority
    `core/tail` split.
  - The second generated module imports the exact majority-signature
    high-bit split for `T = 10, j = 32`. The observed nonterminal
    states reach valuation coordinate `13`, so the Lean matrix type is
    `TransferMatrix 13`.
  - A brute-force row-substochastic proof for the larger `T = 10,
    j = 32` majority matrices times out; the final generator therefore
    uses per-row finite supports, as in `K16S16KExactCWSummary.lean`.
- Verification:
  - `lake build CollatzShadowing.Generated.T10CriticalSymbolic`
    succeeds.
  - `lake build CollatzShadowing.Generated.T10J32HighBitTail`
    succeeds.
  - `lake build` succeeds.
  - `rg -n "sorry|admit" CollatzShadowing *.lean` finds no proof
    placeholders.
- Next recommended task: continue with 8.7 by applying the existing
  finite CW/spectral bridge to the imported majority decomposition, or
  generate a matching CW certificate for `T10J32HighBitTail`.

### 2026-05-12 (Phase 8.6 — spectral-radius bridge) — Codex + Piero Borgatta

- Tasks advanced: **8.6 complete**.
- Artifacts modified:
  - `lean/CollatzShadowing/Bound.lean`
  - `lean/CollatzShadowing/Generated/K16S16KBridge.lean`
  - `lean/README.md`
  - `lean/CollatzShadowing/INVENTORY.md`
  - `lean/CollatzShadowing/EPISODE_INVENTORY.md`
  - `lean/TODO.md`
- New declarations:
  - `matrixLinftyOpNNNorm`
  - `spectralRadius_le_of_matrixLinftyOpNNNorm_le`
  - `spectralRadius_le_of_forall_row_nnnorm_sum_le`
  - `nnrealMatrixToReal`
  - `spectralRadius_le_of_forall_nnreal_row_sum_le`
  - `finiteCWDiagonalUnit`
  - `finiteCWWeightedRealConjugate`
  - `finiteCWWeightedRealConjugate_spectrum_eq`
  - `spectralRadius_le_of_finiteCWCertificate`
  - `spectralRadius_le_of_finiteCWCertificateOfSumEq`
  - `CWBasis.toFiniteCWBasis`
  - `CWCertificate.toFiniteCWCertificate`
  - `spectralRadius_le_of_CWCertificate`
  - `OperatorDecomposition.spectralRadius_le_full`
  - `Generated.k16s16KSpectralRadiusBound`
- Notes:
  - The bridge uses Mathlib's `spectrum.spectralRadius_le_nnnorm`
    with the matrix `ℓ∞` operator norm, then upgrades a weighted
    finite CW certificate by conjugating the realified matrix with the
    positive diagonal basis matrix.
  - `Generated.K16S16KCertifiedComponentWithCW` now also contains the
    concrete spectral-radius bound for the generated 37-state `K,b`
    matrix.
- Verification:
  - `lake build CollatzShadowing.Bound` succeeds.
  - `lake build CollatzShadowing.Generated.K16S16KBridge` succeeds.
  - `lake build` succeeds.
  - `rg -n "sorry|admit" CollatzShadowing *.lean` finds no proof
    placeholders.
- Next recommended task: resume 8.5/8.7 by deciding whether the next
  paper-facing object is the empirical `full/core/tail` matrix import or
  the explicit numerical `T=10, j=32` certificate.

### 2026-05-12 (Phase 8.6 — SCC/CW 37-state bridge) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts modified:
  - `lean/CollatzShadowing.lean`
  - `lean/CollatzShadowing/Generated/K16S16KBridge.lean`
  - `lean/README.md`
  - `lean/CollatzShadowing/INVENTORY.md`
  - `lean/TODO.md`
- New declarations:
  - `Generated.k16s16KSCCNodeToCWState`
  - `Generated.k16s16KSCCLabel_eq_CWStateLabel`
  - `Generated.k16s16KSCCNodeToCWState_label`
  - `Generated.k16s16K_edge_count_eq_scc_edge_count`
  - `Generated.k16s16KSCCHub_label`
  - `Generated.K16S16KCertifiedComponentWithCW`
  - `Generated.k16s16KCertifiedComponentWithCW`
- Notes:
  - The new bridge imports both generated 37-state modules and proves
    that the SCC certificate and CW matrix certificate use the same
    `Fin 37` state ordering and labels.
  - `k16s16KCertifiedComponentWithCW` packages the critical SCC
    certificate, the finite CW certificate, and the compatibility facts
    into one Lean object suitable for paper-facing references.
  - This removes an implicit bookkeeping assumption before using the
    SCC certificate and CW certificate together in later paper-facing
    statements.
- Verification:
  - `lake build CollatzShadowing.Generated.K16S16KBridge` succeeds.
- Next recommended task: decide whether to add a paper-facing theorem
  packaging the 37-state SCC certificate together with
  `k16s16KFiniteCWCertificate`, or move directly to the remaining
  spectral-radius bridge.

### 2026-05-12 (Phase 8.3 — generated 37-state K,b SCC certificate) — Codex + Piero Borgatta

- Tasks advanced: **8.3 complete** for the 37-state compressed `K,b`
  SCC certificate.
- Artifacts modified:
  - `lean/CollatzShadowing.lean`
  - `lean/CollatzShadowing/Generated/K16S16KSCC.lean`
  - `scripts/phantom_taxonomy/lean_scc_certificate.py`
  - `lean/README.md`
  - `lean/CollatzShadowing/INVENTORY.md`
  - `lean/TODO.md`
- New declarations:
  - `Generated.K16S16KSCCNode`
  - `Generated.k16s16KSCCEdgeBool`
  - `Generated.k16s16KTruncatedGraph`
  - `Generated.k16s16KSCCFromHubWalk_valid`
  - `Generated.k16s16KSCCToHubWalk_valid`
  - `Generated.k16s16KHubSCCCertificate`
  - `Generated.k16s16KSCC`
  - `Generated.k16s16KCriticalSCCCertificate`
- Notes:
  - The imported SCC certificate covers the 37-state compressed `K,b`
    graph from
    `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json`.
  - The generated graph uses a Boolean edge table and hub-based finite
    walks. A local decidability instance lets Lean close the generated
    walk-validity proofs with `decide`, avoiding the earlier expensive
    symbolic `simp` expansion.
  - `lean_scc_certificate.py` makes the Lean SCC certificate
    reproducible from the JSON source. It deduplicates edge types,
    chooses `K3:b1` as hub, computes BFS walks to/from the hub, and
    emits the checked Lean module.
  - The module is imported by `CollatzShadowing.lean`.
- Closure decision:
  - 8.3 closes on the generated 37-state compressed `K,b` SCC
    certificate. The full raw 1240-node SCC import is reserved as
    optional audit work if later needed.
- Next recommended task: connect the generated 37-state SCC certificate
  to the generated 37-state CW matrix certificate by checking that their
  state orders and labels agree.

### 2026-05-12 (Phase 8.8 — README and inventory updated) — Codex + Piero Borgatta

- Tasks advanced: **8.8 complete.**
- Artifacts modified:
  - `lean/README.md`
  - `lean/CollatzShadowing/INVENTORY.md`
  - `lean/CollatzShadowing/EPISODE_INVENTORY.md`
  - `lean/TODO.md`
- Notes:
  - `README.md` now reflects the actual current status: the project
    builds cleanly, the Lemma 3.1 / Corollary 3.4 core is `sorry`-free,
    and Phase 8 includes finite episode/operator/certificate modules.
  - `INVENTORY.md` now includes a Phase-8 section covering
    `EpisodeGraph`, `Operator`, `Bound`, and the generated 37-state
    `k16s16KFiniteCWCertificate`.
  - `EPISODE_INVENTORY.md` now records which inventory recommendations
    were implemented in production modules.
- Next recommended task: decide the spectral-radius bridge target for
  8.6/8.7, or move to Phase 9 paper-facing documentation if the finite
  rowwise certificate is sufficient for the current v3 framing.

### 2026-05-12 (Phase 8.6 — evaluated rows and core+tail CW bridge) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Also closed: **8.9** for the current project state.
- Artifacts modified:
  - `lean/CollatzShadowing/Bound.lean`
  - `lean/TODO.md`
- New declarations:
  - `EvaluatedCWRowBound` packages a `ClearedCWRowBound` with the
    semantic equalities identifying it with one row of
    `Matrix.mulVec M basis.vector`, the matching vector entry, and the
    matching `alpha`.
  - `EvaluatedCWRowBound.toCWRow` converts one evaluated cleared row
    into the pointwise CW inequality
    `(M.mulVec basis.vector) i ≤ alpha * basis.vector i`.
  - `finiteCWCertificateOfEvaluatedRows` converts evaluated cleared
    rows for all states into a `FiniteCWCertificate`.
  - `FiniteCWCertificate.add` and `finiteCWCertificateOfSumEq` prove
    that generic finite CW certificates add over a shared positive
    basis.
  - `CWCertificate.add` and `OperatorDecomposition.cwCertificate_full`
    specialize the same `core+tail` bound to the phase-state operator
    API from `Operator.lean`.
- Notes:
  - A direct generated proof by expanding `Matrix.mulVec` and using
    `norm_num` was tried, but even a single row was too slow on the
    37-state sparse matrix. The new bridge avoids this bottleneck by
    making row evaluation an explicit import obligation for the
    generator.
  - The first attempt at `EvaluatedCWRowBound.toCWRow` used a single
    `rw`; Lean rejected it because rewriting `alpha` crossed a
    dependent structure field. The final proof uses a `calc` block and
    compiles.
  - Verified:
    `lake build CollatzShadowing.Bound CollatzShadowing.Generated.K16S16KExactCWSummary`.
  - Full-project verification:
    `lake build` succeeds; `rg -n "sorry|admit" CollatzShadowing *.lean`
    returns no matches.
  - After adding the `core+tail` theorem:
    `lake build CollatzShadowing.Bound` succeeds.
- Next recommended task: extend `lean_cw_summary.py` so it emits compact
  row-evaluation witnesses for `EvaluatedCWRowBound` (rather than asking
  Lean to recompute sparse matrix-vector products), then instantiate
  `FiniteCWCertificate k16s16KMatrix k16s16KCWBasis k16s16KAlphaNNReal`.

### 2026-05-12 (Phase 8.6 — generated 37-state finite CW certificate) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts modified:
  - `scripts/phantom_taxonomy/lean_cw_summary.py`
  - `lean/CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
  - `lean/TODO.md`
- New generated declarations:
  - `k16s16KNodeXXSupport` records the source support of each generated
    row.
  - `k16s16KNodeXXRow` packages each cleared arithmetic row as a named
    `ClearedCWRowBound`.
  - `k16s16KNodeXXMulVec` proves the exact row evaluation
    `(k16s16KMatrix.mulVec k16s16KCWBasis.vector) i = lhsNum/lhsDen`
    using the finite support rather than expanding all 37 columns.
  - `k16s16KEvaluatedRows` packages all evaluated cleared rows.
  - `k16s16KFiniteCWCertificate` instantiates the full generated
    `FiniteCWCertificate k16s16KMatrix k16s16KCWBasis
    k16s16KAlphaNNReal`.
- Notes:
  - The original flat matrix match made row evaluation too expensive.
    The generator now emits a row-nested matrix and per-row support
    finsets, then reduces `mulVec` through `Finset.sum_subset`.
  - A scoped `maxHeartbeats` increase remains on the generated row
    evaluation theorems because exact `NNReal` arithmetic on the larger
    rows exceeds Lean's default heartbeat budget.
- Verification:
  - `lake build CollatzShadowing.Generated.K16S16KExactCWSummary`
    succeeds.
- Next recommended task: connect `FiniteCWCertificate` to whatever
  spectral-radius notion is selected for Phase 8.6/8.7, or update
  `README.md`/inventory for the Phase-8 generated certificate API.

### 2026-05-11 (Phase 8.6 — cleared CW summary packaged) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts:
  - `CollatzShadowing/Bound.lean` now defines
    `ClearedCWRowBound` and `ClearedCWCertificateSummary`, an exact
    arithmetic certificate layer for row inequalities after clearing
    positive denominators.
  - `scripts/phantom_taxonomy/lean_cw_summary.py` now emits
    `k16s16KClearedRows` and `k16s16KClearedCWSummary`.
  - `CollatzShadowing/Generated/K16S16KExactCWSummary.lean` packages
    the 37 generated row inequalities into a checked
    `ClearedCWCertificateSummary`.
- Verification:
  - `lake build CollatzShadowing.Bound` succeeds.
  - `lake env lean CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
- Notes:
  - A direct generated proof of
    `FiniteCWCertificate k16s16KMatrix k16s16KCWBasis
    k16s16KAlphaNNReal` by expanding the whole `Fin 37` matrix timed
    out in `simp`. The current packaged cleared certificate avoids that
    monolithic expansion and gives the next bridge a smaller target.
- Next recommended task: prove general lemmas converting
  `ClearedCWRowBound` data into `NNReal` row inequalities, then apply
  them row-by-row to obtain the full `FiniteCWCertificate`.

### 2026-05-11 (Phase 8.6 — generated Fin 37 matrix data) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts:
  - `scripts/phantom_taxonomy/lean_cw_summary.py` now emits the full
    generated finite state data for the `K,b` certificate.
  - `CollatzShadowing/Generated/K16S16KExactCWSummary.lean` defines
    `K16S16KState := Fin 37`, `k16s16KStateLabel`,
    `k16s16KVectorNat`, `k16s16KVector`, `k16s16KCWBasis`,
    `k16s16KAlphaNNReal`, and the full `k16s16KMatrix :
    Matrix K16S16KState K16S16KState NNReal`.
  - The generated matrix uses JSON orientation: rows are destination
    nodes and columns are source nodes, so `(P v)[dst]` is the incoming
    sum over source nodes.
- Verification:
  - `python3 ../scripts/phantom_taxonomy/lean_cw_summary.py --json
    ../scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json
    --out CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
  - `lake env lean CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
- Notes:
  - The generated Lean file now contains both the full matrix data and
    the 37 exact per-node arithmetic inequalities. The remaining bridge
    is to prove `FiniteCWCertificate k16s16KMatrix k16s16KCWBasis
    k16s16KAlphaNNReal` from those generated inequalities.
- Next recommended task: connect the generated `Fin 37` matrix/vector
  object to `FiniteCWCertificate`.

### 2026-05-11 (Phase 8.6 — 37 per-node K,b inequalities) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts:
  - `scripts/phantom_taxonomy/lean_cw_summary.py` now reconstructs
    exact incoming sums `(P v)_i` from the Phase-7 JSON vector and edge
    list.
  - `CollatzShadowing/Generated/K16S16KExactCWSummary.lean` now emits,
    for each of the 37 `K,b` nodes, constants for the exact numerator
    and denominator of `(P v)_i`, the exact vector entry `v_i`, and a
    theorem proving the cleared-denominator inequality
    `(P v)_i ≤ (89/100) v_i`.
  - All generated arithmetic proofs use `norm_num`, not
    `native_decide`.
- Verification:
  - `python3 ../scripts/phantom_taxonomy/lean_cw_summary.py --json
    ../scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json
    --out CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
  - `lake env lean CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
- Notes:
  - This verifies every per-node exact arithmetic inequality from the
    compressed 37-state `K,b` JSON certificate in Lean. It still does
    not build the actual `Matrix (Fin 37) (Fin 37) NNReal` and prove
    `FiniteCWCertificate` directly over that matrix.
- Next recommended task: generate the full `Fin 37` matrix/vector
  object and connect these 37 inequalities to `FiniteCWCertificate`.

### 2026-05-11 (Phase 8.6 — exact K,b JSON summary in Lean) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts:
  - `scripts/phantom_taxonomy/lean_cw_summary.py` generates a Lean
    summary certificate from a Phase-7 CW JSON file.
  - `CollatzShadowing/Generated/K16S16KExactCWSummary.lean` was
    generated from
    `orbit_harness_k16_s16_scc_K_cw_certificate.json`.
  - The generated file records the 37 `K,b` node labels, 277 edge
    types, `alpha = 89/100`, max node `K15:b2`, and exact max ratio
    `136756256754601/154382162832639`.
  - Lean proves
    `136756256754601 * 100 < 89 * 154382162832639` by
    `norm_num`, i.e. the exact JSON max ratio is below `0.89`.
  - `CollatzShadowing.lean` imports the generated summary certificate.
- Verification:
  - `python3 ../scripts/phantom_taxonomy/lean_cw_summary.py --json
    ../scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json
    --out CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
  - `lake env lean CollatzShadowing/Generated/K16S16KExactCWSummary.lean`
    succeeds.
- Notes:
  - Superseded by the following session entry, which adds all 37
    per-node exact inequalities to the generated Lean file.
- Next recommended task: generate the full `Fin 37` matrix/vector object
  and connect the per-node inequalities to `FiniteCWCertificate`.

### 2026-05-11 (Phase 8.6 — JSON-to-Lean CW smoke certificate) — Codex + Piero Borgatta

- Tasks advanced: **8.6 strengthened**, not complete.
- Artifacts:
  - `CollatzShadowing/Bound.lean` now has generic finite-state
    certificate structures: `FiniteCWBasis`,
    `FiniteCWCertificate`, and `FiniteMatrixBoundCertificate`.
  - `scripts/phantom_taxonomy/lean_cw_smoke.py` reads a Phase-7 JSON
    certificate, selects an exact probability-one edge, and emits a
    two-state Lean smoke certificate.
  - `CollatzShadowing/Generated/K16S16KCWSmoke.lean` was generated from
    `orbit_harness_k16_s16_scc_K_cw_certificate.json`; it records the
    selected edge `K12:b2 -> K11:b1`, defines a two-state matrix, and
    proves a finite CW certificate with `alpha = 1`.
  - `CollatzShadowing.lean` imports the generated smoke certificate, so
    the root build checks the JSON-to-Lean pipeline.
- Verification:
  - `python3 ../scripts/phantom_taxonomy/lean_cw_smoke.py --json
    ../scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json
    --out CollatzShadowing/Generated/K16S16KCWSmoke.lean` succeeds.
  - `lake env lean CollatzShadowing/Generated/K16S16KCWSmoke.lean`
    succeeds.
- Notes:
  - This is intentionally a smoke certificate, not the full 37-state
    `K,b` certificate. It validates the generation route and proof
    shape before scaling to all JSON nodes and inequalities.
- Next recommended task: scale the generator from the two-state smoke
  certificate to the full `K,b` JSON certificate.

### 2026-05-11 (Phase 8.5/8.6 — split inheritance and CW certificate API) — Codex + Piero Borgatta

- Tasks advanced: **8.5 strengthened; 8.6 started.**
- Artifacts:
  - `CollatzShadowing/Operator.lean` proves
    `splitCore_le_full` and `splitTail_le_full`, pointwise domination
    of the split matrices by the full matrix.
  - It proves `splitCore_rowSubstochastic` and
    `splitTail_rowSubstochastic`, so generated `core` and `tail`
    matrices inherit row-substochasticity from `full`.
  - `decompositionOfPartitionFromFull` now builds an
    `OperatorDecomposition` from a full matrix, a decidable partition,
    and one row-substochasticity proof for `full`.
  - `CollatzShadowing/Bound.lean` introduces `CWBasis`,
    `CWCertificate`, and `MatrixBoundCertificate` for finite
    Collatz-Wielandt-style pointwise matrix bounds.
  - `zeroMatrixBoundCertificate` is a checked baseline certificate for
    the bound API.
- Verification:
  - `lake env lean CollatzShadowing/Operator.lean` succeeds.
  - `lake env lean CollatzShadowing/Bound.lean` succeeds.
- Notes:
  - The Phase-7 JSON certificates already use exact
    `probability_num/probability_den` entries and pointwise vector
    inequalities. The Lean API now mirrors that shape.
  - `8.6` is still only started: the true weighted `core+tail` theorem
    and any formal spectral-radius statement remain open.
- Next recommended task: continue **8.5/8.6** by generating a small
  Lean certificate from one Phase-7 JSON file, then scale the generator.

### 2026-05-11 (Phase 8.5 start — operator decomposition API) — Codex + Piero Borgatta

- Tasks advanced: **8.5 started**, not complete.
- Artifacts:
  - `CollatzShadowing/Operator.lean` now defines
    `TransferMatrix V := Matrix (PhaseState V) (PhaseState V) NNReal`.
  - It defines `ProbabilityEntry` for exact imported probabilities of
    the form `numerator / denominator`, matching the Phase-7
    `count/source_events` CSV and JSON certificates.
  - It defines `RowSubstochastic` for non-negative transfer matrices.
  - It defines `splitCore`, `splitTail`, and
    `split_full_eq_core_add_tail`, so a generated decidable partition
    of entries automatically yields `full = core + tail`.
  - It proves `splitCore_rowSubstochastic` and
    `splitTail_rowSubstochastic`: if `full` is row-substochastic, then
    both split matrices are row-substochastic by pointwise domination.
  - `decompositionOfPartitionFromFull` therefore only needs the full
    matrix row certificate plus the generated `core/tail` partition.
  - It defines `OperatorDecomposition`, packaging `full`, `core`,
    `tail`, the equality `full = core + tail`, and row-substochastic
    certificates for all three matrices.
  - `zeroOperatorDecomposition` is a checked baseline certificate for
    the matrix/decomposition plumbing.
- Verification:
  - `lake env lean CollatzShadowing/Operator.lean` succeeds.
- Notes:
  - This fixes the Lean API shape for Phase 8.5 but does not yet encode
    the empirical matrix entries or the majority rule that partitions
    entries into `core` and `tail`.
- Next recommended task: continue **8.5** by deciding the import format
  for exact matrix entries and the empirical-signature partition.

### 2026-05-11 (Phase 8.3/8.4 — path SCC certificates and phase states) — Codex + Piero Borgatta

- Tasks advanced: **8.3 strengthened; 8.4 complete.**
- Artifacts:
  - `CollatzShadowing/EpisodeGraph.lean` now includes a finite
    path-certificate import format:
    `TruncatedEpisodeGraph.Walk`, `reachable_of_walk`, and
    `HubSCCCertificate`.
  - A `HubSCCCertificate` supplies, for every listed node, a checked
    finite walk from a hub and a checked finite walk back to the hub;
    `HubSCCCertificate.toSCC` converts this to a genuine `SCC`
    certificate by mutual `Relation.ReflTransGen` reachability.
  - `CollatzShadowing/Operator.lean` defines the production
    `PhaseState V := Fin (V+1) × Fin 4 × Fin 4`, plus `cappedNu2`,
    `oddPart`, `mod4Fin`, and `phaseState`.
  - `EpisodeInventory.lean` renamed its toy `PhaseState` to
    `InventoryPhaseState`, leaving the production name to
    `Operator.lean`.
- Verification:
  - `lake env lean CollatzShadowing/EpisodeGraph.lean` succeeds.
  - `lake env lean CollatzShadowing/Operator.lean` succeeds.
- Notes:
  - The SCC interface now has a concrete shape for importing Phase-7
    data, but the actual 1240-node critical SCC certificate is not yet
    generated in Lean. It will likely need a script that emits node
    indices and hub paths from the Phase-7 CSV artifacts.
- Next recommended task: **8.5**, begin the finite operator matrices
  over `PhaseState V`; in parallel, keep 8.3 open until the large SCC
  certificate is generated/imported.

### 2026-05-11 (Phase 8.3 start — finite SCC certificate interface) — Codex + Piero Borgatta

- Tasks advanced: **8.3 started**, not complete.
- Artifacts:
  - `CollatzShadowing/EpisodeGraph.lean` now defines
    `TruncatedEpisodeGraph.SCC`, a finite SCC certificate consisting of
    a `Finset` of bounded nodes, nonemptiness, and mutual reachability
    for nodes in the set.
  - It also defines `CriticalSCCCertificate`, packaging a chosen
    critical node, its certified component, and membership of the
    critical node in that component.
  - `singletonSCC` and `singletonCriticalCertificate` give reflexive
    baseline certificates and keep the interface typechecked.
- Verification:
  - `lake env lean CollatzShadowing/EpisodeGraph.lean` succeeds.
- Notes:
  - This deliberately avoids pretending to have the true paper-§8
    critical SCC inside Lean already. The next step is to decide the
    concrete certificate import format for the Phase-7 SCC node list and
    edge reachability evidence.
- Next recommended task: finish **8.3** by adding the concrete critical
  SCC certificate object, likely generated from the Phase-7 CSV/JSON
  artifacts.

### 2026-05-11 (Phase 8.2 — episode graph node API) — Codex + Piero Borgatta

- Tasks advanced: **8.2 complete.**
- Artifacts:
  - `CollatzShadowing/EpisodeGraph.lean` starts the production
    episode-graph module.
  - It defines the unbounded paper-level `EpisodeNode` with natural
    coordinates `k`, `c`, and `b`.
  - It defines finite cutoff boxes
    `TruncatedEpisodeNode K C B := Fin K × Fin C × Fin B`, with
    `Fintype` and `DecidableEq` plumbing.
  - It defines `EpisodeGraph.edge : EpisodeRel EpisodeNode`,
    `TruncatedEpisodeGraph.edge`, reachability wrappers, SCC wrappers,
    and `edgeFinset` for finite directed edge enumeration.
  - `CollatzShadowing.lean` imports `CollatzShadowing.EpisodeGraph`.
- Verification:
  - `lake env lean CollatzShadowing/EpisodeGraph.lean` succeeds after
    rebuilding `CollatzShadowing.EpisodeInventory`.
- Notes:
  - The Phase-8 roadmap wording was updated to reflect the 8.1 finding:
    the production graph is a local directed relation, not Mathlib
    `SimpleDigraph`.
  - `EpisodeInventory.lean` now uses the toy name
    `InventoryEpisodeNode`, leaving `EpisodeNode` to the production
    module.
- Next recommended task: **8.3**, formalize the SCC interface on top of
  mutual `Relation.ReflTransGen` reachability and decide what finite
  certificate object should represent the critical SCC.

### 2026-05-10 (Phase 8.1 — Mathlib episode inventory) — Codex + Piero Borgatta

- Tasks advanced: **6.9 complete; 8.1 complete.**
- Artifacts:
  - `CollatzShadowing/EPISODE_INVENTORY.md` records the Mathlib API
    inventory for the episode graph, SCC reachability, finite
    non-negative matrices, and Collatz-Wielandt-style certificates.
  - `CollatzShadowing/EpisodeInventory.lean` is a compiling scratchpad
    with `EpisodeRel`, `Reachable`, `SameSCC`, a bounded toy
    `InventoryEpisodeNode`, `rowSubstochastic`, and `cwCertificate`.
  - `CollatzShadowing.lean` imports the new inventory module.
- Verification:
  - Piero verified online on 2026-05-10 that
    `paper/collatz_spectral_reduction_v2.tex` compiles with
    `pdflatex`; 6.9 is now closed.
  - `lake env lean CollatzShadowing/EpisodeInventory.lean` succeeds.
- Notes:
  - Current Mathlib has `SimpleGraph`/`Graph` as undirected graph APIs;
    no stable production `SimpleDigraph` API was found. Phase 8 should
    therefore start with a local directed relation
    `EpisodeRel α := α → α → Prop` and use
    `Relation.ReflTransGen` for reachability.
  - Mathlib has `Matrix.rowStochastic`, but no ready-made
    Perron-Frobenius / Collatz-Wielandt theorem for arbitrary finite
    non-negative matrices was found. The recommended first target is a
    finite `NNReal` certificate predicate.
- Next recommended task: **8.2**, updating the roadmap wording from
  `SimpleDigraph` to the local directed-relation model while defining
  the production `EpisodeGraph.lean` node and edge API.

### 2026-05-09 (Roadmap extension — Phases 7-10 added) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **roadmap structure extended.**
- Artifacts:
  - `lean/TODO.md` — added four new phases:
    - **Phase 7 (Priority A)**: phantom-set taxonomy vs Chang
      Theorem 7.15. Tasks 7.1-7.7 covering the necklace-enumeration
      script, the per-composition $q_w$ computation, the orbit
      simulation harness, the $K_0 = 16$ run with $K_0 = 20$ as a
      conditional follow-up, integration of any new SCCs into
      $M_{\mathrm{cross}}$, and documentation in
      `notes/phantom_taxonomy.md`.
    - **Phase 8 (Priority B)**: Lean formalization of the episode
      graph, the truncated transfer operator, the
      $\full = \core + \tail$ decomposition, and the weighted
      Collatz–Wielandt bound. Tasks 8.1-8.9. Conditional on
      Phase 7. Conjectures 6 and 7 themselves are **not** in
      scope.
    - **Phase 9 (v3 paper)**: paper v3 redaction after both
      Phases 7 and 8 are complete. Eight tasks covering framing
      decision, related-work reconnaissance refresh, §8 update
      with augmented SCC, §3.3 update with Phase-8 declarations,
      §10 refocus, methodology update, archive build, Zenodo
      publication.
    - **Phase 10 (Priority C)**: spectral-gap analysis via
      Lasota–Yorke + Hennion + Keller–Liverani. Five tasks,
      explicitly flagged as a collaboration target; will not be
      initiated before Phases 7-9 are closed.
- Notes: the v3 release (Phase 9) is gated on Priorities A and B
  only, not on Priority C. Priority C is open-ended and may
  feed a future v4 or a companion paper. The order
  A → B → v3 → C is intentional: A and B sharpen the targets that
  C would attack, and they are bounded in scope.
- Next recommended task: 6.4 (Zenodo v2 publication) followed by
  Phase 7 kick-off (task 7.1, the necklace enumerator).

### 2026-05-10 (Phase 6 verification update) — Codex + Piero Borgatta

- Tasks advanced: **6.4 complete; 6.9 left as manual online
  verification.**
- Verification:
  - Zenodo record `10.5281/zenodo.20098868` exists as v2
    (`version = 2.0.0`) under concept DOI `10.5281/zenodo.20021537`.
  - Published PDF and supplementary zip checksums match the local
    artifacts.
  - `lake build` succeeds and the Lean project remains `sorry`-free.
  - A temporary local `tectonic` trial produced a PDF with only
    box-layout warnings, but the TeX tools were removed afterward to
    avoid keeping a large local TeX installation.
- Pending in Phase 6: **6.9** will be checked manually online with
  `pdflatex` against `paper/collatz_spectral_reduction_v2.tex`.

### 2026-05-10 (Phase 7.1 start — necklace enumerator) — Codex + Piero Borgatta

- Tasks advanced: **7.1 complete.**
- Artifacts:
  - `scripts/phantom_taxonomy/necklace_counts.py` implements the
    Möbius-inversion count
    `M(K, ell) = (1/ell) * sum_{d | gcd(K, ell)} mu(d) *
    binom(K/d - 1, ell/d - 1)` for primitive cyclic compositions.
  - The same script includes an independent brute-force enumerator via
    canonical cyclic rotations, used to cross-check the formula for
    small `K`.
  - `scripts/phantom_taxonomy/necklace_counts_k3_20.csv` records
    `M_total`, `M_expanding`, `R(K)`, and the per-length counts for
    `K = 3..20`.
- Verification:
  - `python3 scripts/phantom_taxonomy/necklace_counts.py --max-k 20
    --verify-direct 10 --csv
    scripts/phantom_taxonomy/necklace_counts_k3_20.csv` succeeds.
  - The direct enumerator and formula agree for all `3 <= K <= 10`.
  - The rounded `R(K)` values for `K = 3..20` reproduce Chang's
    displayed table values.
  - `python3 -m py_compile scripts/phantom_taxonomy/necklace_counts.py`
    succeeds.

### 2026-05-10 (Phase 7.2 — phantom representatives) — Codex + Piero Borgatta

- Tasks advanced: **7.2 complete.**
- Artifacts:
  - `scripts/phantom_taxonomy/phantom_representatives.py` enumerates
    the expansive primitive cyclic compositions from 7.1 and computes
    the affine coefficient `C_w`, total exponent `A`, length `L`,
    rational fixed point `q_w = C_w / (2^A - 3^L)`, and the 2-adic
    residue `q_w mod 2^m`.
  - `scripts/phantom_taxonomy/phantom_representatives_k3_16.csv`
    contains the working depth-16 representative table.
  - `scripts/phantom_taxonomy/phantom_representatives_k3_20.csv`
    contains the depth-20 table, with 16099 expansive primitive
    representatives.
- Verification:
  - `python3 scripts/phantom_taxonomy/phantom_representatives.py
    --max-k 16 --csv
    scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
    --limit 12` succeeds.
  - `python3 scripts/phantom_taxonomy/phantom_representatives.py
    --max-k 20 --csv
    scripts/phantom_taxonomy/phantom_representatives_k3_20.csv
    --limit 0` succeeds.
  - Exact sanity checks inside the script verify
    `(2^A - 3^L) q_w = C_w`, `S_w(q_w) = q_w`, and odd denominator
    for every emitted row.
  - Independent CSV check: per-`K` representative counts match
    `M_expanding` from `necklace_counts_k3_20.csv` for every
    `3 <= K <= 20`.
  - `python3 -m py_compile scripts/phantom_taxonomy/phantom_representatives.py
    scripts/phantom_taxonomy/necklace_counts.py` succeeds.

### 2026-05-10 (Phase 7.3 — orbit harness) — Codex + Piero Borgatta

- Tasks advanced: **7.3 complete.**
- Artifacts:
  - `scripts/phantom_taxonomy/orbit_harness.py` consumes the
    representative CSVs from 7.2, samples integer lifts
    `n = q_w mod 2^(bA+1) + t*2^(bA+1)`, traces odd Syracuse
    orbits, detects monitored phantom hits via precomputed congruence
    classes `q_w mod 2^(A+1)`, and emits detail/event/edge CSVs.
  - `scripts/phantom_taxonomy/orbit_harness_k10_details.csv`,
    `orbit_harness_k10_events.csv`, and `orbit_harness_k10_edges.csv`
    are a dense small-cutoff smoke run.
  - `scripts/phantom_taxonomy/orbit_harness_k16_smoke_details.csv`,
    `orbit_harness_k16_smoke_events.csv`, and
    `orbit_harness_k16_smoke_edges.csv` demonstrate the same harness at
    the Phase-7.4 cutoff `K0 = 16` with a deliberately small sampling
    budget.
- Verification:
  - `python3 scripts/phantom_taxonomy/orbit_harness.py
    --representatives
    scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
    --max-k 10 --b-max 2 --samples 8 --max-steps 500 --out-prefix
    scripts/phantom_taxonomy/orbit_harness_k10` succeeds, producing
    720 traced orbits and 217 observed transition edges.
  - `python3 scripts/phantom_taxonomy/orbit_harness.py
    --representatives
    scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
    --max-k 16 --b-max 1 --samples 2 --max-steps 500 --out-prefix
    scripts/phantom_taxonomy/orbit_harness_k16_smoke` succeeds,
    producing 2494 traced orbits and 1790 observed transition edges.
  - `python3 -m py_compile scripts/phantom_taxonomy/orbit_harness.py`
    succeeds.

### 2026-05-10 (Phase 7.4 — K0=16 sampled SCC run) — Codex + Piero Borgatta

- Tasks advanced: **7.4 partially complete**. The full `K <= 16`
  representative set was run through the orbit harness, but the
  outcome is case (b), so spectral certification/integration remains
  pending.
- Artifacts:
  - `scripts/phantom_taxonomy/scc_report.py` computes SCCs from an
    `orbit_harness.py` edge CSV and writes both a Markdown summary and
    a full component-node CSV.
  - `scripts/phantom_taxonomy/orbit_harness_k16_full_details.csv`,
    `orbit_harness_k16_full_events.csv`, and
    `orbit_harness_k16_full_edges.csv` are the sampled `K0 = 16`
    run output.
  - `scripts/phantom_taxonomy/orbit_harness_k16_full_scc_nodes.csv`
    lists all nodes in the observed nontrivial SCC.
  - `notes/phantom_taxonomy_k16_scc_report.md` compares the taxonomy
    SCC labels against the empirical paper-§8 labels where exact
    rational `q_w` equality makes this possible.
- Verification:
  - `python3 scripts/phantom_taxonomy/orbit_harness.py
    --representatives
    scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
    --max-k 16 --b-max 2 --samples 8 --max-steps 1000 --out-prefix
    scripts/phantom_taxonomy/orbit_harness_k16_full` succeeds.
  - Run summary: 19952 traced orbits, all stopped below start within
    the step budget; 212324 episode events; 5041 observed edge types.
  - SCC summary from `scc_report.py`: 2401 observed nodes, one
    nontrivial SCC, largest SCC size 1222, internal edge types 3857,
    internal observed transition weight 182961.
  - Exact paper-SCC recognition by `q_w` equality finds the paper
    empirical `k=12` cycle-1 representative as
    `K9:L7:w1-1-1-1-1-2-2:b1` and `:b2`; the other empirical labels
    use a different indexing universe and are not directly recognized
    in this taxonomy graph at `K0 = 16`.
  - `python3 -m py_compile scripts/phantom_taxonomy/scc_report.py
    scripts/phantom_taxonomy/orbit_harness.py` succeeds.
- Next: because this is outcome (b), continue with **7.6** rather
  than 7.5. The immediate open problem is to decide how to compress or
  certify the 1222-node observed SCC before recomputing a cross-node
  operator.

### 2026-05-10 (Phase 7.6 start — SCC compression diagnostic) — Codex + Piero Borgatta

- Tasks advanced: **7.6 started**, not complete.
- Artifacts:
  - `scripts/phantom_taxonomy/scc_transfer_summary.py` reads the
    `K0=16` event stream and SCC node list, reconstructs event-to-event
    transitions, treats final/no-next-event hits as exits, and builds
    substochastic empirical retention matrices.
  - `scripts/phantom_taxonomy/orbit_harness_k16_full_scc_transfer_summary.md`
    records the diagnostic spectral radii.
  - `scripts/phantom_taxonomy/orbit_harness_k16_full_scc_node_edges.csv`,
    `orbit_harness_k16_full_scc_KL_edges.csv`, and
    `orbit_harness_k16_full_scc_K_edges.csv` give the raw and compressed
    edge tables.
- Verification:
  - `python3 scripts/phantom_taxonomy/scc_transfer_summary.py
    --events scripts/phantom_taxonomy/orbit_harness_k16_full_events.csv
    --scc-nodes
    scripts/phantom_taxonomy/orbit_harness_k16_full_scc_nodes.csv
    --out-prefix scripts/phantom_taxonomy/orbit_harness_k16_full_scc`
    succeeds.
  - Raw SCC matrix: 1222 states, 3857 internal edge types, 202697
    source events, 19736 exits, retention mass `0.902633`,
    `rho(P_internal) ≈ 0.884991531781`.
  - `(K,L,b)` compression: 72 states, 506 internal edge types,
    `rho(P_internal) ≈ 0.884858364224`.
  - `(K,b)` compression: 35 states, 260 internal edge types,
    `rho(P_internal) ≈ 0.885502907552`.
  - `python3 -m py_compile scripts/phantom_taxonomy/scc_transfer_summary.py`
    succeeds.
- Notes: the near-identical radii across raw and compressed matrices
  suggest that a macro-state certificate may be feasible. This remains
  an empirical retention diagnostic, not the final weighted
  Collatz-Wielandt certificate required to close 7.6.

### 2026-05-10 (Phase 7.6 continued — empirical CW table) — Codex + Piero Borgatta

- Tasks advanced: **7.6 materially advanced**, still not theorem-level
  complete.
- Artifacts:
  - `scripts/phantom_taxonomy/scc_collatz_wielandt.py` reads the
    empirical SCC retention edge tables, builds a positive
    power-iteration vector, and reports the finite Collatz-Wielandt
    upper expression `max_i (P v)_i / v_i`.
  - `scripts/phantom_taxonomy/orbit_harness_k16_full_scc_cw_table.csv`
    and `.md` record the updated empirical bound table.
- Verification:
  - `python3 scripts/phantom_taxonomy/scc_collatz_wielandt.py
    scripts/phantom_taxonomy/orbit_harness_k16_full_scc_node_edges.csv
    scripts/phantom_taxonomy/orbit_harness_k16_full_scc_KL_edges.csv
    scripts/phantom_taxonomy/orbit_harness_k16_full_scc_K_edges.csv
    --csv
    scripts/phantom_taxonomy/orbit_harness_k16_full_scc_cw_table.csv
    --md
    scripts/phantom_taxonomy/orbit_harness_k16_full_scc_cw_table.md`
    succeeds.
  - Raw 1222-node empirical SCC: `CW ≤ 0.884991533363`, max node
    `K3:L2:w1-2:b1`.
  - `(K,L,b)` compression: 72 states, `CW ≤ 0.884858364322`, max
    node `K3:L2:b1`.
  - `(K,b)` compression: 35 states, `CW ≤ 0.885502907588`, max node
    `K3:b1`.
  - `python3 -m py_compile scripts/phantom_taxonomy/scc_collatz_wielandt.py`
    succeeds.
- Notes: this is now an updated subcritical empirical bound table
  comparable in shape to paper §8, but it is still based on sampled
  transition data. To close 7.6 strictly, the next step should replace
  the sampled probabilities with a deterministic/certified transition
  construction or explicitly record 7.6 as an empirical-only result.

### 2026-05-10 (Phase 7.6 continued — sample stability) — Codex + Piero Borgatta

- Tasks advanced: **7.6 stability check added**, still not theorem-level
  complete.
- Artifacts:
  - `scripts/phantom_taxonomy/orbit_harness_k16_s16_details.csv`,
    `orbit_harness_k16_s16_events.csv`, and
    `orbit_harness_k16_s16_edges.csv` are the doubled-budget run
    (`16` dense lifts/source instead of `8`).
  - `notes/phantom_taxonomy_k16_s16_scc_report.md` reports the SCC
    structure for the doubled-budget run.
  - `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_*` contains
    the doubled-budget SCC node list, compressed retention edges,
    transfer summary, and empirical CW table.
  - `scripts/phantom_taxonomy/compare_cw_tables.py` compares empirical
    CW tables across sampling budgets.
  - `scripts/phantom_taxonomy/orbit_harness_k16_cw_stability.md`
    records the `s8` vs `s16` comparison.
- Verification:
  - `python3 scripts/phantom_taxonomy/orbit_harness.py
    --representatives
    scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
    --max-k 16 --b-max 2 --samples 16 --max-steps 1000 --out-prefix
    scripts/phantom_taxonomy/orbit_harness_k16_s16` succeeds.
  - Doubled-budget run summary: 39904 traced orbits, all stopped below
    start within the step budget; 425677 episode events; 5559 observed
    edge types.
  - SCC summary: 2405 observed nodes, one nontrivial SCC, largest SCC
    size 1240.
  - Empirical CW table at 16 lifts/source: raw `CW ≤ 0.885485445971`,
    `(K,L,b)` `CW ≤ 0.885270267025`, `(K,b)` `CW ≤ 0.88582938756`.
  - Stability vs 8 lifts/source: maximum CW spread is below `0.0005`
    across all three matrix views.
  - `python3 -m py_compile scripts/phantom_taxonomy/compare_cw_tables.py`
    succeeds.

### 2026-05-10 (Phase 7.6 closure — empirical result) — Codex + Piero Borgatta

- Tasks advanced: **7.6 closed as an empirical integration result**.
- Artifacts:
  - `notes/phantom_taxonomy_empirical_scc_integration.md` records the
    scope, inputs, observed bounds, stability check, and explicit caveat
    that this is not a theorem-level weighted cross-node certificate.
- Decision:
  - The `K0 = 16` taxonomy SCC is integrated into sampled
    substochastic retention operators.
  - The observed empirical Collatz-Wielandt bounds are stable and
    subcritical around `0.885`.
  - The stronger deterministic/certified transition construction is
    deliberately left open for a future task, per user instruction.

### 2026-05-10 (Phase 7.6 strengthening — exact empirical certificates) — Codex + Piero Borgatta

- Tasks advanced: **7.6 empirical result strengthened**, still scoped
  to sampled matrices.
- Artifacts:
  - `scripts/phantom_taxonomy/scc_cw_certificate.py` creates and
    verifies JSON certificates with exact rational probabilities
    `count/source_events`, positive integer test vectors, and a rational
    bound `alpha = 89/100`.
  - `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_node_cw_certificate.json`
    certifies the raw 1240-node empirical SCC matrix.
  - `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_KL_cw_certificate.json`
    certifies the 76-state `(K,L,b)` compression.
  - `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json`
    certifies the 37-state `(K,b)` compression.
  - `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_exact_cw_certificates.md`
    summarizes the exact ratios and verification commands.
- Verification:
  - Raw node certificate: exact max ratio
    `439764459109/496636575879 ≈ 0.885485444423 < 0.89`.
  - `(K,L,b)` certificate: exact max ratio
    `88036787882257/99446226949575 ≈ 0.885270266985 < 0.89`.
  - `(K,b)` certificate: exact max ratio
    `136756256754601/154382162832639 ≈ 0.885829387575 < 0.89`.
  - `python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify
    <certificate.json>` returns `status=OK` for all three certificates.
- Scope: these are exact certificates for the **empirical matrices**.
  They remove floating-point dependence from the bound, but they do not
  replace sampled transition generation with a deterministic residue
  construction.

### 2026-05-10 (Phase 7.7 — taxonomy note) — Codex + Piero Borgatta

- Tasks advanced: **7.7 complete.**
- Artifact:
  - `notes/phantom_taxonomy.md` summarizes Phase 7.1-7.6 in one
    citable note: exact necklace counts, rational representatives,
    orbit harness, `K0=16` SCC outcome, empirical integration,
    stability under doubled sampling, exact rational certificates for
    sampled matrices, and the remaining deterministic-transition gap.
- Notes:
  - No v3 draft file exists yet, so the note is not referenced from a
    v3 TeX source at this time. It is the source note to cite or import
    when Phase 9 starts.

### 2026-05-09 (Phase 6 closure — README + methodology updates) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **6.5 complete.**
- Artifacts:
  - `README.md` rewritten: dual DOI badges (concept
    `10.5281/zenodo.20021537` + version v2
    `10.5281/zenodo.20098868`), separate paper rows for v1/v2,
    Lean section with theorem-to-file mapping, "Relation to
    concurrent work" paragraph on Chang 2026, "Planned next
    steps" section in compressed form (A/B/C), citation block
    updated to v2 DOI.
  - `METHODOLOGY.md` extended with `Planned next phases`
    section covering Priorities A, B, C in detail with effort
    estimates and the explicit ordering rationale.
  - `paper/collatz_spectral_reduction_v2.tex` added §10
    subsection "Planned next steps" after the Honest claim
    paragraph.
- Verification: paper .tex passes static balance check
  (1750 lines, environments balanced, all `\cite` resolved, all
  `\ref` resolved). `pdflatex` build still pending (no TeX on
  current system).
- Pending in Phase 6: 6.4 (Zenodo v2 publish, ready to click),
  6.9 (`pdflatex` build verification).
- Next recommended task: complete 6.4 and 6.9, then begin
  Phase 7.

### 2026-05-06 (Phase 6 partial — paper v2 drafted) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **6.1, 6.2, 6.3, 6.6, 6.7, 6.8 — substantive content of v2 drafted.**
- Artifacts:
  - `paper/collatz_spectral_reduction_v2.tex` (new file; preserves v1).
    Adds §1.2 Related Work (Chang, Siegel, Rozier, Neklyudov,
    Lemmens-Nussbaum, Laarhoven-de Weger, Mori, Leventides-Poulios,
    Bastos-Caprio-Messaoudi); §3.3 Formal verification in Lean 4
    documenting the headline declarations and supporting infra; §9.1
    Comparison with concurrent work (vs Chang Theorem C.3 and 7.19).
    Methodology section expanded to make AI-collaboration an explicit
    secondary goal of the work; cross-AI verification protocol
    documented; future search for analogous studies committed in
    §11.7.
  - `METHODOLOGY.md` updated: Lean phase moved from "Planned" to
    "COMPLETED"; literature reconnaissance method documented; the
    sibling reconnaissance corpus deliberately not committed.
- Pending: 6.4 (Zenodo v2 release), 6.5 (GitHub README v2 reference),
  6.9 (`pdflatex` build verification of v2 .tex).
- Notes: literature reconnaissance was carried out outside the
  project repository; the v1 bibliography of 6 references was
  expanded to 22+ in v2 to cover all consequential overlapping
  works. Most consequential candidate (Chang 2026 arXiv:2603.11066)
  was verified by direct inspection of §7 (phantom cycles) and §C
  (transfer operator); Chang's Definition 7.2 / Proposition 7.4 /
  Remark 9.17 / Theorem 7.15 / Theorem 7.19 / Theorem C.3 are now
  cited explicitly in v2 with the precise relationships to this
  work spelled out.
- Next recommended task: 6.9 (build verification), then 6.4-6.5
  (Zenodo + GitHub release coordination).

### 2026-05-06 (Phase 5.5 complete — expansive no-infinite shadowing) — Codex + Piero Borgatta

- Tasks advanced: **5.5 complete.**
- Artifacts:
  - `lean/CollatzShadowing/NoInfinite.lean` — added
    `PhantomWord.Expansive`, `qwRat_neg_of_expansive`,
    `qwZ2_ne_natCast_of_expansive`, and
    `no_infinite_period_congruence_expansive`.
- Notes: Corollary 3.4 is now formalized in the period-congruence form:
  for an expansive phantom and positive natural `n`, the congruence
  `n ≡ q_w (mod 2^{b*A+1})` cannot hold for every `b`.
- Verification: `lake build CollatzShadowing.NoInfinite` succeeds
  with no `sorry`.
- Next recommended task: Phase 6, update Lean/paper documentation and
  prepare the v2 integration.

### 2026-05-06 (Phase 5.4 complete — no-infinite congruence core) — Codex + Piero Borgatta

- Tasks advanced: **5.4 complete, 5.5 partial.**
- Artifacts:
  - `lean/CollatzShadowing/NoInfinite.lean` — added
    `eq_of_padic_congruent_all_pow2`, `no_infinite_congruence_to_qw`,
    and `no_infinite_period_congruence_to_qw`.
  - `lean/CollatzShadowing.lean` — re-exports `NoInfinite`.
- Notes: the proved theorem covers the 2-adic core of Corollary 3.4:
  arbitrary-precision congruence to `q_w` forces equality in `ℤ_[2]`.
  The remaining paper-specific step is to formalize “expansive phantom”
  and prove `q_w` is negative, hence not a positive natural.
- Verification: `lake build CollatzShadowing.NoInfinite` succeeds
  with no `sorry`.
- Next recommended task: Phase 5.5, formalize expansiveness and
  discharge the explicit hypothesis
  `((n : ℕ) : ℤ_[2]) ≠ qwZ2 w (PhantomWord.qwOddDen w)`.

### 2026-05-06 (Phase 5.3 complete — q_w orbit hypothesis removed) — Codex + Piero Borgatta

- Tasks advanced: **5.3 complete.**
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` — proved the one-step
    coefficient identity `Cw_step_cyclicShift_one`, the rational and
    2-adic step identities for `q_w`, `qwZ2_first_match`,
    `Syracuse2adic_qwZ2_eq_cyclicShift_one`,
    `Syracuse2adic_iterate_qwZ2_eq_cyclicShift`,
    `qw_orbit_matches_one_period`, and finally `qw_orbit_matches`.
  - `lean/CollatzShadowing/Shadowing.lean` — removed the
    `h_qw_matches` hypothesis from `exact_shadowing` and
    `exact_shadowing_periods`; both now call `qw_orbit_matches`
    internally.
- Verification: `lake build CollatzShadowing.Shadowing` succeeds.
- Next recommended task: Phase 5.4, state Corollary 3.4 in Lean.

### 2026-05-06 (Phase 5 partial — cyclic-shift normal forms) — Codex + Piero Borgatta

- Tasks advanced: **5.3 partial.**
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` — imported
    `Mathlib.Data.List.Rotate` and proved
    `cyclicShift_vals_eq_rotate`, so the list generated by
    `cyclicShift` is exactly `vals.rotate r`.
  - Proved `cyclicShift_A` and `cyclicShift_Aw`, giving invariant
    period sum/exponent under cyclic shifts.
  - Added public 2-adic power valuation helpers
    `two_ne_zero_z2`, `valuation_two_z2`, `valuation_two_pow_z2`, and
    the generic unit-times-power lemma
    `nu2Z2_eq_of_eq_unit_mul_two_pow`.
- Notes: the remaining one-period matching proof is now reduced to the
  algebraic step identity
  `3*q_(cyclicShift w r)+1 = q_(cyclicShift w (r+1))*2^(w.aAt r)`.
- Next recommended task: prove that step identity using the
  `qwRat` formula and cyclic-shift coefficient normal forms, then feed
  it to `nu2Z2_eq_of_eq_unit_mul_two_pow`.

### 2026-05-06 (Phase 5 partial — unit and cyclic-shift infrastructure) — Codex + Piero Borgatta

- Tasks advanced: **5.3 partial.**
- Artifacts:
  - `lean/CollatzShadowing/Phantom.lean` — moved base positivity lemmas
    `length_pos` and `aAt_pos` into the core phantom module; added
    `cyclicShift` and `cyclicShift_length`.
  - `lean/CollatzShadowing/Auxiliary.lean` — proved `B_pos_of_pos`,
    `prefixC_odd_of_pos`, `Cw_odd`, `Cw_ne_zero`, `qwRat_ne_zero`,
    `padicValRat_qwRat_zero`, and `valuation_qwZ2_zero`, so `q_w` is
    known to be a 2-adic unit.
  - Added `cyclicShift_aAt`, identifying the periodic word of a cyclic
    shift with the shifted periodic word of the original phantom.
- Verification: `lake build` succeeds; `rg` finds no `sorry`, `admit`,
  or `axiom`.
- Next recommended task: prove the algebraic bridge
  `Syracuse2adic^[j] q_w = q_(cyclicShift w j)` for `j < w.length`;
  then one-period matching follows from `valuation_qwZ2_zero` on the
  shifted phantom.

### 2026-05-06 (Phase 5 partial — finite `q_w` orbit reduction) — Codex + Piero Borgatta

- Tasks advanced: **5.3 partial.**
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` — added
    `qwZ2_iterate_length_eq_self_of_matches`, proving that one-period
    prefix matching makes the `length`-th Syracuse iterate of `q_w`
    return to `q_w`.
  - Added `qw_orbit_matches_of_period`, reducing the full infinite
    `q_w` matching property to the finite hypothesis
    `MatchesPrefix w q_w w.length`.
- Notes: Phase 5.3 is now narrowed to the exact valuation proof for
  the first full period of the `q_w` orbit.
- Next recommended task: prove the one-period matching theorem, then
  remove `h_qw_matches` from `exact_shadowing` and
  `exact_shadowing_periods`.

### 2026-05-05 (Phase 5 partial — periodic bound closed) — Codex + Piero Borgatta

- Tasks advanced: **5.1, 5.2.**
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` — added periodic-entry and
    block-sum lemmas, culminating in
    `PhantomWord.B_mul_period : w.B (b * w.length) = b * w.A`.
  - `lean/CollatzShadowing/Shadowing.lean` —
    `exact_shadowing_periods` now states the congruence bound as
    `b * w.A + 1`, matching the paper's `2^{bA+1}` clause, and converts
    internally via `B_mul_period`.
- Verification: `lake build CollatzShadowing.Auxiliary` and
  `lake build CollatzShadowing.Shadowing` both succeed.
- Remaining Phase 5 work: prove `qw_orbit_matches`, then formalize the
  no-infinite-shadowing corollary.

### 2026-05-05 (Phase 5 partial — q_w orbit groundwork) — Codex + Piero Borgatta

- Tasks advanced: **5.3 partial.**
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` — added prefix affine
    coefficient infrastructure for the periodic word:
    `prefixCoeffs`, `prefixC`, `prefixCoeffs_snd_eq_B`,
    `prefixCoeffs_length_eq_affineCoeffs`, and `prefixC_length_eq_Cw`.
  - Proved `qwIntDen_ne_zero`, `qwRat_denominator_ne_zero`, and
    `qwZ2_fixed_by_S_w`, showing that the 2-adic representative `q_w`
    is fixed by the full-period affine map.
  - Proved `affine_iterate_prefix`, the one-orbit prefix affine formula
    under `MatchesPrefix`.
- Remaining Phase 5 work: prove the exact valuation of the `q_w` prefix
  orbit and then propagate it periodically to eliminate `h_qw_matches`
  from `exact_shadowing`.

### 2026-05-04 (Phase 4 complete — Lemma 3.1 verified) — Claude (Claude Code) + Piero Borgatta

- **Phase 4 complete.** `exact_shadowing` and `exact_shadowing_periods`
  are proved with zero `sorry`. Combined with Phases 0-3, the project
  is now entirely `sorry`-free (`grep -r "sorry" CollatzShadowing/`
  returns nothing).
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` — added `B_mono` and
    `affine_difference_z2` (the `ℤ_[2]` version of the affine
    identity, multiplied form `(diff)·2^B = 3^j·(n-q)` so no
    division is needed; proved by direct induction mirroring
    `affine_difference`).
  - `lean/CollatzShadowing/Shadowing.lean` — full rewrite:
    * Added `PadicCongruentModPow2_iff_le_valuation` bridge.
    * Added small helpers `valuation_two_z2`, `valuation_two_pow_z2`,
      `valuation_three_pow_z2`, `three_pow_ne_zero_z2`,
      `two_pow_ne_zero_z2`.
    * `exact_shadowing` proved by strong induction on `j` with a
      case-split on `((n : ℤ_[2]) = q_w)`. The equal case follows
      from `h_qw_matches`; the generic case combines
      `affine_difference_z2` with valuation arithmetic
      (`PadicInt.valuation_mul`, the new power-valuation helpers,
      `B_mono`, `B_succ`) and `nu2_stable_under_proximity`.
    * `exact_shadowing_periods` is the literal specialisation
      `m := b * w.length`.
- Architectural choice: `exact_shadowing` carries `h_qw_matches`
  (the matching property of `q_w`'s own orbit) as a hypothesis. This
  is an intrinsic property of expansive phantoms — *"the orbit of
  `q_w` under `S` is exactly periodic of length `L` with ν₂ word `w`
  repeated"* — and will be discharged in Phase 5 by a separate
  theorem.
- API note: `PadicInt.valuation_p` only fires syntactically when the
  argument is `((p : ℕ) : ℤ_[p])`; the literal numeral `(2 : ℤ_[2])`
  needs `push_cast; rfl` to be normalised first. This was the source
  of an earlier failed `rw [PadicInt.valuation_p]`.
- Next: **Phase 5 (optional)** — discharge `h_qw_matches`. Then prove
  Corollary 3.4 and proceed to **Phase 6** — paper integration and v2
  release.

### 2026-05-04 (Phase 3 complete) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **3.2 and 3.3 proved.** Phase 3 is now complete;
  the only remaining `sorry`s in the project are on the Lemma 3.1
  statements (`exact_shadowing` / `exact_shadowing_periods`), which
  are Phase 4 work.
- Artifacts: extensions to `lean/CollatzShadowing/Auxiliary.lean`.
- New declarations:
  - `PhantomWord.length_pos`, `PhantomWord.aAt_pos` — structural
    positivity helpers.
  - `nu2Z2_zero`, `ne_zero_of_matches` — bridge between `ν₂Z2` and
    non-zeroness from a matching ν₂ value.
  - `syracuse_one_step_diff` (private) — the per-step difference
    formula `S₂(x) − S₂(y) = (3/2^a)·(x − y)` in `ℚ_[2]` when both
    `3x+1` and `3y+1` have the same 2-adic valuation `a`.
  - `affine_difference` (Task 3.2) — paper line 276, by induction
    on `j`.
  - `valuation_z2_neg` (private) — `(-x).valuation = x.valuation` in
    `ℤ_[2]`, derived via `norm_neg` and `norm_eq_zpow_neg_valuation`.
  - `valuation_add_eq_left_of_lt` (private) — strict ultrametric:
    when `v(a) < v(b)`, the sum has valuation exactly `v(a)`. Built
    from `le_valuation_add` + a `by_contra` argument that uses
    `a = (a + b) + (-b)`.
  - `nu2_stable_under_proximity` (Task 3.3).
- Notes on Mathlib v4.29.1 API audit (this round):
  - `PadicInt.norm_eq_zpow_neg_valuation` is the bridge between
    `‖x‖` and `x.valuation` for `ℤ_[2]`.
  - `zpow_right_injective₀` is the injectivity lemma for `(2 : ℝ)^_`.
  - `Mathlib.Data.List.GetD` defines `List.getD_eq_getElem`.
  - `linear_combination` (and `field_simp` followed by
    `linear_combination`) is the right tactic for ℚ_[2]-side
    polynomial identities; `ring` alone struggles with the casts.
  - `push Not` replaces deprecated `push_neg` in v4.29.1.
- Final `lake build`: clean apart from the two intentional `sorry`s
  on `exact_shadowing` and `exact_shadowing_periods`.
- Next recommended task: **Phase 4** — prove `exact_shadowing` itself,
  using `affine_difference` (3.2) and `nu2_stable_under_proximity`
  (3.3) as the inductive ingredients.

### 2026-05-04 (paper-faithful 2-adic) — Claude (Claude Code) + Piero Borgatta

- Architectural decision: extend `S` totally to `ℤ_[2]` via
  `PadicInt.unitCoeff`, with a single documented deviation from the
  paper (`Syracuse2adic (-1/3) := 0`, never invoked in any
  paper-relevant computation).
- Artifacts:
  - `lean/CollatzShadowing/Syracuse2Adic.lean` (new file).
  - `lean/CollatzShadowing/Shadowing.lean` (statements rewritten to
    use `Syracuse2adic^[j]` and `qwOddDen` auto-discharged).
  - `lean/CollatzShadowing/Auxiliary.lean` (added 3.2 and 3.3
    statements + `MatchesPrefix` predicate).
  - `lean/CollatzShadowing.lean` (re-exports `Syracuse2Adic`).
- New declarations in `Syracuse2Adic.lean`:
  - `Syracuse2adic : ℤ_[2] → ℤ_[2]` — total def via `unitCoeff`.
  - `Syracuse2adic_spec` — defining identity
    `3·x + 1 = Syracuse2adic x · 2^valuation` for non-degenerate `x`.
  - `Syracuse2adic_at_singular` — the degenerate-point convention.
  - `valuation_natCast_z2` — `((n:ℕ):ℤ_[2]).valuation = padicValNat 2 n`.
  - `Syracuse2adic_natCast` — the bridge:
    `((S n : ℕ) : ℤ_[2]) = Syracuse2adic ((n : ℕ) : ℤ_[2])`
    for positive odd `n`. **Proved** via `unitCoeff_spec` plus
    `Nat.div_mul_cancel pow_padicValNat_dvd` and ℤ_[2]-cancellation.
- Decidability fix: `if h : ... = 0 then ...` on `ℤ_[2]` requires
  `Classical.dec` because `ℤ_[2]` lacks `DecidableEq`. Wrap with
  `haveI := Classical.dec _` inside the `noncomputable def`.
- Status: `lake build` clean apart from the four expected `sorry`s
  on `exact_shadowing`, `exact_shadowing_periods`, `affine_difference`
  (3.2), `nu2_stable_under_proximity` (3.3). All Phase-2/3.1/3.4
  results remain proved.
- Next recommended task: prove Task 3.2 (induction on `j`).

### 2026-05-04 (Phase 3 partial) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **3.1, 3.1.5, 3.4 proved.** Tasks 3.2 and 3.3
  pending — both require extending `S` to `ℤ_[2]`, which is a
  separate infrastructure step.
- Artifacts:
  - `lean/CollatzShadowing/Auxiliary.lean` (new file).
  - `lean/CollatzShadowing/Phantom.lean` (refactored `B` to sum form).
  - `lean/CollatzShadowing.lean` (re-exports `Auxiliary`).
- Notes on Mathlib v4.29.1 API audit (collected during this round):
  - There is no `PadicInt.valuation_natCast`; route through `ℚ_[2]`
    via `Padic.valuation_natCast` then `PadicInt.valuation_coe`.
  - `padicValNat 2 3 = 0` is **not** `decide`-reducible (the def uses
    well-founded recursion). Use the lemma
    `padicValNat.eq_zero_of_not_dvd`.
  - `decide` does not work for `(3 : ℤ_[2]) ≠ 0` (no decidable
    equality on `ℤ_[2]`). Cast through `ℕ` with `exact_mod_cast`.
  - `Even.sub_odd : Even a → Odd b → Odd (a − b)` is in
    `Mathlib.Algebra.Ring.Parity`, not in the integer-specific file.
    The right "two-divides" bridge is `even_iff_two_dvd` (no
    `Int.` prefix).
  - `Int.natCast_dvd : (m : ℤ) ∣ n ↔ m ∣ n.natAbs` is the right
    bridge for `Rat.den_dvd`.
  - `Odd.of_dvd_nat` lives in `Mathlib.Algebra.Order.Ring.Abs`.
  - `List.length_le_sum_of_one_le` is in
    `Mathlib.Algebra.BigOperators.Group.List.Basic`.
- Refactor of `B`: switched from the closed form to
  `((List.range m).map aAt).sum`. This makes `B_succ` a one-line
  rewrite using `List.range_succ`. The old closed form remains
  recoverable as a separate theorem when needed (e.g. for the
  `B(b·L) = b·A` periodic specialisation).
- Final `lake build` is clean apart from the two intentional
  `sorry`s on `exact_shadowing` and `exact_shadowing_periods` (the
  Lemma 3.1 proofs are still Phase 4 work).
- Next recommended task: extend `S` to `ℤ_[2]` (or `ℚ_[2]` and
  restrict), then close 3.2 and 3.3.

### 2026-05-04 (Phase 2 close) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **2.7, 2.8, 2.9 — Phase 2 is now complete.**
- Artifacts:
  - `lean/CollatzShadowing/Phantom.lean` (added `aAt`, `B`, `qwRat`,
    `QwOddDen`, `qwZ2`).
  - `lean/CollatzShadowing/Shadowing.lean` (new file:
    `PadicCongruentModPow2`, `exact_shadowing`,
    `exact_shadowing_periods`).
  - `lean/CollatzShadowing.lean` (re-exports `Shadowing`).
- Notes:
  - `aAt`/`B` use closed-form arithmetic (`Nat`-level division and
    modulo) rather than building a flattened cycle list. Smoke-checked
    against `phantomOne` by `change ... ; rw ; simp`.
  - `qwZ2` is parameterised by `QwOddDen w := ¬ (2 : ℕ) ∣ (qwRat w).den`,
    rather than hard-coding the proof inside the definition. This
    keeps `Phantom.lean` `sorry`-free and pushes the
    odd-denominator obligation to the caller (Phase 3 will discharge
    it for expansive phantoms via the structural identity
    `parity(2^A − 3^L) = odd`).
  - `exact_shadowing` is stated using `syracuseExponent (S^[j] n) =
    aAt w j` for `j < m`. This is the operational form of the paper's
    "first `m` Syracuse steps have ν₂-word `(a_0, ..., a_{m-1})`".
  - `exact_shadowing_periods` is the `m = b·L` specialisation; both
    statements have `sorry` as proof per the Phase-2 acceptance
    criterion.
  - Encountered two API surprises during this round:
    1. `List.get?` no longer exists in Mathlib v4.29.1 — switched to
       `List.getD ... default` (still core).
    2. `simp` does not auto-rewrite `m % 1 = 0`; explicit
       `rw [Nat.mod_one, Nat.div_one]` was needed in the `B` smoke
       check before the rest reduces.
  - Final `lake build`: success, with exactly the two expected `sorry`
    warnings on `exact_shadowing` and `exact_shadowing_periods`.
- Next recommended task: **3.1** — prove `ν₂(3·n) = ν₂(n)` for
  `n ∈ ℤ_[2]`.

### 2026-05-04 (later still) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **2.5, 2.6.** Bundled because the `(C_j, A_j)`
  recursion that defines `S_w` is exactly the content of 2.6.
- Artifacts modified:
  - `lean/CollatzShadowing/Phantom.lean` (additions; same file as 2.4).
- New declarations:
  - `affineFoldStep : ℕ × ℕ → ℕ → ℕ × ℕ` — one step of eq. (3.1).
  - `PhantomWord.affineCoeffs : PhantomWord → ℕ × ℕ`,
    `PhantomWord.Cw`, `PhantomWord.Aw` — the named coefficients.
  - `PhantomWord.Aw_eq_A : ∀ w, w.Aw = w.A` — internal coherence
    between the fold-defined exponent and the simple list sum.
  - `S_w : PhantomWord → ℤ_[2] → ℚ_[2]` — the affine Syracuse map.
- Notes:
  - Followed `INVENTORY.md` Open Gaps: `S_w` lands in `ℚ_[2]`, not
    `ℤ_[2]`, because `2 : ℤ_[2]` is not a unit. The acceptance
    criterion in the original 2.5 row of TODO ("S_w of length-1 word
    equals one Syracuse step on the natural inclusion") is realised in
    its algebraic form (`= (3·x + 1)/2`); the integer-level identity
    `(S_w phantomOne (n : ℤ_[2]) : ℚ_[2]) = (S n : ℚ_[2])` for odd `n`
    with `ν₂(3n+1) = 1` is left to the proof phase, since it requires
    a Padic cast lemma that has no place in a Phase-2 definition file.
  - `Aw_eq_A` proven by an auxiliary `affineFold_snd_eq` showing the
    fold's second component is additive in the starting state.
  - Verified with `lake build` (success) and `#check`s on `S_w`, `Cw`,
    `Aw`, `Aw_eq_A`, `affineFoldStep`.
- Operational fix done in this session:
  - Moved `export ELAN_HOME=...` and the `PATH` augmentation from
    `~/.zshrc` to `~/.zshenv` so that non-interactive subshells (used
    by Claude Code's Bash tool, build agents, etc.) inherit them.
    Cleaned up three duplicate copies in `~/.zshrc`. Removed
    `~/.elan/` (a 2.5 GB toolchain that elan had silently created in
    `$HOME` because non-interactive subshells didn't see `ELAN_HOME`).
    The toolchain on `/Volumes/AFUOCO/MAC/Applicazioni/elan/` is the
    sole remaining copy and `lake build` succeeds against it.
- Next recommended task: **2.7** — define `q_w : ℤ_[2]` via
  `ratToZ2` (`Padic.norm_rat_le_one`), with a proof that the
  denominator `2^A_w - 3^L` is odd.

### 2026-05-04 (later) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **2.4.**
- Artifacts produced:
  - `lean/CollatzShadowing/Phantom.lean` (new file)
  - `lean/CollatzShadowing.lean` (re-exports `CollatzShadowing.Phantom`)
- Notes:
  - Followed the design prescribed in `INVENTORY.md` §1.5: a `structure`
    with fields `vals : List ℕ`, `nonempty : vals ≠ []`, and
    `positive : ∀ a ∈ vals, 0 < a`. Chose `structure` over a bare
    subtype so downstream files can pattern-match on the fields without
    repeated unfolding.
  - Added projections `PhantomWord.length` and `PhantomWord.A` (the
    per-period exponent sum) since they are zero-risk and feed
    immediately into 2.5–2.7.
  - Smoke fixture `phantomOne : PhantomWord` (the word `[1]`) sanity
    checks that the structure can be inhabited; `phantomOne.length = 1`
    and `phantomOne.A = 1` hold by `rfl`.
  - Deferred any Mathlib-API-heavy helpers (e.g. `length ≤ A`) to
    Phase 3 to avoid speculating on lemma names before the proofs need
    them.
  - Toolchain: this Codex session triggered the first download of
    `leanprover/lean4:v4.29.1` to `~/.elan/toolchains/`. After that,
    `lake build` succeeded with `Build completed successfully (1795
    jobs).` and explicit `#check`s on `PhantomWord`, `PhantomWord.length`,
    `PhantomWord.A`, and `phantomOne` all type-check.
- Next recommended task: **2.5** — define `S_w : ℤ_[2] → ℤ_[2]` and the
  fold producing `(C_j, A_j)` from `eq. (3.1)`.

### 2026-05-04 — Codex + Piero Borgatta

- Tasks advanced: **2.1, 2.2, 2.3.**
- Artifacts produced:
  - `lean/CollatzShadowing/Basic.lean`
- Notes:
  - Replaced the Lake placeholder `def hello := "world"`.
  - Added `nu2Nat`, Unicode alias `ν₂`, `nu2Int`, `nu2Rat`,
    noncomputable `nu2Z2`/`ν₂Z2`, `syracuseNumerator`,
    `syracuseExponent`, `S`, and `syracuseOddStep`.
  - `S` is total on `ℕ`, with later theorem statements expected to
    carry positivity/oddness hypotheses for the intended Syracuse use.
  - `PadicInt.valuation` is noncomputable, so only the `ℤ_[2]`
    valuation aliases are marked `noncomputable`.
  - Verified:
    `/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake env lean CollatzShadowing/Basic.lean`,
    `/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build`, and
    explicit `#check`s for `CollatzShadowing.S`, `CollatzShadowing.ν₂`,
    and `CollatzShadowing.nu2Z2`.
- Next recommended task: **2.4** — create `Phantom.lean` and define
  `PhantomWord`.

### 2026-05-04 — Codex + Piero Borgatta

- Tasks advanced: **1.1, 1.2, 1.3, 1.4, 1.5 — all of Phase 1.**
- Artifacts produced:
  - `lean/CollatzShadowing/Inventory.lean` (rebuilt as a complete,
    typechecked Phase 1 scratch buffer)
  - `lean/CollatzShadowing/INVENTORY.md`
- Cleanup:
  - Removed temporary smoke-test files
    `lean/CollatzShadowing/Smoke.lean` and
    `lean/CollatzShadowing/SmokePure.lean`.
- Notes:
  - `lake build` succeeds when invoked through
    `/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake`; plain `lake` is
    not currently on Codex's shell `PATH`.
  - The preferred Lean model for `n ≡ q_w (mod 2^k)` is ideal
    membership in `ℤ_[2]`:
    `(n : ℤ_[2]) - q_w ∈ Ideal.span {((2 : ℤ_[2]) ^ k)}`.
  - Do not use `k ≤ (x - y).valuation` as the primary definition,
    because Mathlib has `(0 : ℤ_[2]).valuation = 0`; use it only after
    splitting off the zero case.
  - A rational `q : ℚ` can be represented as an element of `ℤ_[2]` when
    `¬ 2 ∣ q.den`, via `⟨(q : ℚ_[2]), Padic.norm_rat_le_one hden⟩`.
  - The original broad `Inventory.lean` failed under Mathlib v4.29.1
    because some `by decide` valuation examples do not reduce and the
    maximal-ideal API name is `PadicInt.maximalIdeal_eq_span_p`, not
    `PadicInt.maximalIdeal`.
- Next recommended task: start **2.1/2.2** in `Basic.lean`.

### 2026-05-04 (later) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: **0.1, 0.2, 0.3, 0.4, 0.5, 0.6 — all of Phase 0.**
- Artifacts produced (auto-generated by `lake init CollatzShadowing math`,
  except where noted):
  - `lean/lakefile.toml` (requires Mathlib v4.29.1)
  - `lean/lean-toolchain` (`leanprover/lean4:v4.29.1`)
  - `lean/lake-manifest.json` (resolved by `lake update`)
  - `lean/CollatzShadowing.lean` (entry point, imports `Basic`)
  - `lean/CollatzShadowing/Basic.lean` (placeholder `def hello := "world"`)
  - `lean/.github/workflows/` (CI templates from `math` template)
  - `lean/.gitignore` (`/.lake`)
  - `lean/.lake/` (~7 GB Mathlib precompiled cache, gitignored)
- Setup choices:
  - elan installed under `/Volumes/AFUOCO/MAC/Applicazioni/elan`
    (NVMe, outside the project repo).
  - Default toolchain: `stable` (initially), then auto-upgraded to
    `v4.29.1` once Lake initialized the project from the `math`
    template.
  - Mathlib obtained via `lake exe cache get` (precompiled olean files
    from CDN), avoiding a multi-hour from-scratch compilation.
- Notes:
  - The `math` template generated `Basic.lean` with a trivial
    placeholder; we will overwrite it in Phase 2 with the real
    definitions of $S$, $\nu_2$, etc.
  - `.github/workflows/` was added by the template. We can keep these
    (they enable CI on pushes) or remove them later if not needed.
- Next recommended task: **1.1** — start the Mathlib infrastructure
  inventory by locating `padicValNat`, `multiplicity`, `padicNorm`.

### 2026-05-04 (earlier) — Claude (Claude Code) + Piero Borgatta

- Tasks advanced: meta — created this `TODO.md` and the empty
  `lean/CollatzShadowing/` directory.
- Artifacts produced: `lean/TODO.md`, `lean/README.md`, empty directory.
- Notes: plan committed, no Lean code yet, no toolchain yet.
- Next recommended task: **0.1**.
