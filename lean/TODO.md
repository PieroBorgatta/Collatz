# Lean 4 Formalization Plan — Collatz Spectral Reduction

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

> *Last updated: 2026-05-13 — **Phase 5 complete: Lemma 3.1 and Corollary 3.4 formalized**. Project is `sorry`-free. **Phase 6 complete**: paper v2 drafted, Lean note written, Related Work + Chang comparison done, GitHub README updated, METHODOLOGY.md updated, Zenodo v2 published, and `pdflatex` verified online by Piero. **Phase 7 complete for the current branch**: tasks 7.1-7.4, 7.6, and 7.7 are complete; 7.4 closes with the full `K0=16` sampled run and SCC report, outcome (b), so 7.5 is not applicable. **F.1 is closed for the declared finite residue-cell scope**: `deterministic_residue_transfer.py` enumerates all `2^4` finite residue subclasses for each of the 1240 raw SCC source states, writes exact deterministic transition matrices, and the `(K,b)` matrix has an exact CW certificate with max ratio `90833233962213/129559208330288 < 3/4`. **Phase 8 complete for the current branch**: 8.1-8.9 are complete; 8.3 closes on the generated 37-state compressed `K,b` SCC certificate; 8.5 has the matrix/decomposition API, a generated exact import of the empirical `T = 10` critical-symbolic full transfer matrix, and an exact generated `T = 10, j = 32` majority `core/tail` `OperatorDecomposition`; 8.6 connects finite CW certificates to Mathlib `spectralRadius`; 8.7 exposes the `T = 10, j = 32` numerical spectral-radius bound `97/2000 = 0.0485` through a fully expanded Lean-checked 224-row CW certificate generated from the exact CSV.*

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
    └── NoInfinite.lean       Corollary 3.4
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
| F.1 | [x] | Close the deterministic-transition gap in `notes/phantom_taxonomy.md` / Phase 7.6. | Completed for the declared finite residue-cell scope on macro-state space `(K,b)`. `deterministic_residue_transfer.py` enumerates all `2^4` residue subclasses for each of the 1240 raw SCC source states, classifies 19840 cells with zero budget exits, writes exact rational deterministic matrices plus coverage manifest, and reruns the exact CW pipeline on the 37-state `(K,b)` matrix. Certificate: `deterministic_k16_s16_residue_K_cw_certificate.json`, max ratio `90833233962213/129559208330288 < 3/4`. |

---

## Phase 9 — v3 paper redaction

Acceptance: a published `v3` of the preprint on Zenodo, after
Phases 7 and 8 are complete (Phase 9 is therefore conditional on
both). Phase 9 does **not** depend on Phase 10 (Priority C).

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 9.1 | [ ] | Decide v3 framing. | Working title: paper v3 either (a) the same paper extended with a §11 "Phantom-set completeness at depth $K_0$" subsection plus an updated §3.3 that reflects the broader Lean coverage, or (b) a companion preprint focused on the taxonomy result, with v2 unchanged. Decision committed in `notes/v3_outline.md`. |
| 9.2 | [ ] | Update §1.2 (Related Work) with any new arXiv work appearing between v2 and v3. | Reconnaissance pass run per `METHODOLOGY.md` "Literature reconnaissance method". |
| 9.3 | [ ] | Update §8 (Cross-node certificate) with the augmented SCC of Phase 7, if any. | Tables refreshed; new bounds reported. |
| 9.4 | [ ] | Update §3.3 (Formal verification) to cover the Phase-8 additions: `EpisodeGraph`, `Operator`, `Bound`. | Section enumerates the Phase-8 declarations with file references. |
| 9.5 | [ ] | Update §10 "Planned next steps" to reflect Phases 7 and 8 as completed and to refocus on Priority C (Phase 10). | Subsection retitled or revised. |
| 9.6 | [ ] | Update §11 (Methodology) with the v2→v3 Lean session log and any new methodological observations. | Cross-AI verification protocol stress-tested by the Phase-8 sessions; lessons documented. |
| 9.7 | [ ] | Build the v3 supplementary archive (Zenodo zip) including the updated `lean/`, the Phase-7 enumeration code under `scripts/phantom_taxonomy/`, and the v3 PDF. | Zip exists, `pdflatex` clean run, archive < 50 MB. |
| 9.8 | [ ] | Publish v3 on Zenodo as new version of the existing record; update GitHub README with the new version DOI. | Zenodo shows v3 with new version DOI under the same concept DOI; README badges updated. |

---

## Phase 10 — Priority C: spectral-gap analysis (collaboration target)

Acceptance: a partial result on $\{\full_T\}_{T \ge T_0}$ via
Lasota–Yorke + Hennion + Keller–Liverani that does not require
closing Conjecture 6 of the paper outright. Open-ended;
intentionally flagged as a **collaboration target** with researchers
who work on transfer operators on $p$-adic or symbolic systems.
Will not be initiated before Phases 7-9 are closed.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 10.1 | [ ] | Identify candidate Banach space of $2$-adic Lipschitz functions adapted to the refined phase quotient. | Working note documenting the choice and its justification. |
| 10.2 | [ ] | Prove (or, in collaboration, formulate) a Lasota–Yorke inequality for $\full_T$ on the chosen space. | Lemma with explicit constants, even if depending on $T$. |
| 10.3 | [ ] | Apply Hennion's theorem to extract quasi-compactness and a spectral gap. | Theorem with explicit gap estimate. |
| 10.4 | [ ] | Apply Keller–Liverani perturbation theory to control the dependence on $T$. | Continuity statement on the dominant eigenvalue across $T$. |
| 10.5 | [ ] | Decide whether the resulting partial bound is integrated into a v4 paper, into a companion paper, or into a co-authored work. | Decision committed; downstream tasks listed. |

Note: tasks 10.1-10.4 require analytic expertise beyond what the
author can provide in isolation. Concrete progress on Priority C
presupposes either an external collaborator or a substantial
self-study phase that is not on the current program.

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
- Artifacts modified:
  - `notes/phantom_taxonomy.md`
  - `notes/phantom_taxonomy_empirical_scc_integration.md`
  - `lean/TODO.md`
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
