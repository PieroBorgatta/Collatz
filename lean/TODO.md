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

> *Last updated: 2026-05-04 — Phase 3 complete (3.1, 3.1.5, 3.2, 3.3, 3.4 all proved).*

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
  one rewrite, at the cost of moving `B_closed_form` (the closed-form
  identity) to a future TODO.
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
- **Phase 3 complete.** Tasks 3.2 and 3.3 are proved:
  * `affine_difference` (3.2): induction on `j` using
    `syracuse_one_step_diff` (the per-step formula
    `S₂(x) − S₂(y) = (3/2^a)(x − y)` derived from `Syracuse2adic_spec`
    and `linear_combination` in `ℚ_[2]`) plus `B_succ` and `field_simp`.
  * `nu2_stable_under_proximity` (3.3): strict-ultrametric
    `valuation_add_eq_left_of_lt` (custom helper via `le_valuation_add`
    and a contradiction using `valuation_z2_neg`).
- Next concrete action: **Phase 4** — prove `exact_shadowing` (Lemma
  3.1), the only remaining `sorry` in the project.

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
| 4.1 | [ ] | Write the induction skeleton on `j` from `0` to `m-1`. | Compiles with `sorry` only at induction steps. |
| 4.2 | [ ] | Prove the base case `j = 0`. | No `sorry` in base case. |
| 4.3 | [ ] | Prove the inductive step using lemmas 3.1–3.4. | No `sorry` in step. |
| 4.4 | [ ] | Verify the special case `m = bA` (full periods). | Stated as a corollary. |
| 4.5 | [ ] | Final `lake build` clean run. | Zero warnings, zero `sorry`. |

---

## Phase 5 — Corollary 3.4 (optional)

Acceptance: Corollary 3.4 (no positive integer can shadow `w^∞` for
all `m`) is formalized and proved.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 5.1 | [ ] | State Corollary 3.4 in Lean. | Compiles with `sorry`. |
| 5.2 | [ ] | Prove it (uses Lemma 3.1 plus the fact that `q_w` is not a positive integer for expansive phantoms). | No `sorry`. |

---

## Phase 6 — Integration into v2 of the paper

Acceptance: a published `v2` of the preprint on Zenodo that
incorporates the Lean formalization.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 6.1 | [ ] | Write `lean/README.md` describing the project, build instructions, and the verified theorem statement. | File exists, builds verified by reading. |
| 6.2 | [ ] | Add a paragraph to paper Section 3 noting the Lean formalization, with a hash/commit reference to the verified state. | Paper compiles. |
| 6.3 | [ ] | Update `METHODOLOGY.md` "Planned next phase" section to "Completed", with reference to the Lean files. | Done. |
| 6.4 | [ ] | Recompile PDF, replace on Zenodo, publish as new version (v2). | Zenodo shows v2 with new DOI; concept DOI now points to v2. |
| 6.5 | [ ] | Update GitHub README with v2 reference. | Commit pushed. |

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
