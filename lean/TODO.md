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

> *Last updated: 2026-05-04 — Phase 1 complete.*

- **Phase 0 complete.** Lake project initialized with `math` template,
  pinned to **Lean 4 v4.29.1** and **Mathlib v4.29.1**. Mathlib
  precompiled cache downloaded (~7 GB in `lean/.lake/`). `lake build`
  succeeds on the placeholder file `CollatzShadowing/Basic.lean`.
- **Phase 1 complete.** `CollatzShadowing/INVENTORY.md`
  documents the relevant Mathlib API for `padicValNat`, `multiplicity`,
  `padicNorm`, `Padic`, `PadicInt`, coercions, and the chosen
  congruence model in `ℤ_[2]`. `CollatzShadowing/Inventory.lean` is the
  corresponding typechecked Lean scratch buffer.
- The next concrete action is **Phase 2, Task 2.1**: define the
  accelerated Syracuse map and the basic `ν₂` aliases in `Basic.lean`.

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
| 2.1 | [ ] | Define accelerated Syracuse map `S : ℕ → ℕ` for odd inputs. | `Basic.lean` | `#check S` works. |
| 2.2 | [ ] | Define `ν₂` (alias for `padicValNat 2`). | `Basic.lean` | Same. |
| 2.3 | [ ] | Extend `ν₂` to `ℤ_2 \ {0}` (Mathlib should already cover this). | `Basic.lean` | Same. |
| 2.4 | [ ] | Define `PhantomWord := List ℕ` with a positivity constraint on each entry. | `Phantom.lean` | Same. |
| 2.5 | [ ] | Define affine map `S_w : ℤ_2 → ℤ_2` for a phantom word `w`. | `Phantom.lean` | `S_w` of length-1 word equals one Syracuse step on the natural inclusion. |
| 2.6 | [ ] | Define `C_w` and `A_w` via the recursion of paper eq. (3.1). | `Phantom.lean` | Manual check against paper for `w = [1]`. |
| 2.7 | [ ] | Define `q_w := C_w / (2^A_w - 3^L)` as an element of `ℤ_2` (when defined). | `Phantom.lean` | Same. |
| 2.8 | [ ] | Define partial sum `B_m := List.take m (cycle w)).sum`. | `Phantom.lean` | Same. |
| 2.9 | [ ] | State Lemma 3.1 with `:= sorry` proof. | `Shadowing.lean` | `lake build` succeeds, file is non-empty. |

---

## Phase 3 — Auxiliary lemmas

Acceptance: each auxiliary lemma needed for the inductive proof of
Lemma 3.1 is stated and proved.

| ID | Status | Task | Acceptance criterion |
|----|--------|------|----------------------|
| 3.1 | [ ] | `ν₂(3·n) = ν₂(n)` for `n ∈ ℤ_2`. | Proved, no `sorry`. |
| 3.2 | [ ] | After matching the prefix `(a_0, ..., a_{j-1})`, the difference `S^j(n) - S^j(q_w)` is `(3^j / 2^{B_j}) · (n - q_w)` in `ℤ_2`. | Proved. |
| 3.3 | [ ] | If `ν₂(x - y) ≥ a_j + 1`, then `ν₂(3·x + 1) = ν₂(3·y + 1)` and equals `a_j` for both. | Proved. |
| 3.4 | [ ] | The condition `B_m + 1 - B_j ≥ a_j + 1` is equivalent to `B_m ≥ B_{j+1}`. | Trivial (definitional). |

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
