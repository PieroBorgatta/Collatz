# Project Statistics — data for the v5 methodology retrospective

Generated 2026-06-05 by read-only inspection of the repository (git, `wc`,
`grep`). All counts are reproducible from the commands noted in each section.

> **Honesty note.** **Every file in this repository — all code and all prose —
> was produced by AI assistants (Claude, Codex, Gemini) under the author's
> direction. The author typed none of it by hand**; his contribution is
> direction, decisions, editing-by-instruction, and all external actions
> (Zenodo, compilation, pushes). The splits below are *within* the AI output:
> **AI-authored** (source reasoned line by line) vs **generator-emitted**
> (bulk certificate output from AI-written scripts). Credibility rests on NOT
> inflating these numbers — never quote a total without that split.
>
> **Repository totals (all AI-produced; human-typed: 0 lines):**
> ≈ 140,000 lines = Lean 51,318 + Python 54,009 + notes 28,716 + LaTeX 6,183.
> Of which: AI-authored source ≈ 61,800 (Lean proofs 7,805 + Python 54,009);
> generator-emitted ≈ 43,513 (Lean certificates); prose ≈ 34,899.

---

## 1. Code — the honest split

### Lean 4 (Mathlib)

| | files | lines | theorems/lemmas |
|---|---:|---:|---:|
| **AI-authored** (proof modules, reasoned line by line) | 14 | **7,805** | **302** |
| **Generator-emitted** (certificate output of AI-written scripts) | 26 | 43,513 | 966 |
| **Total** | 40 | 51,318 | 1,268 |

- Hand-written defs: 195. Total defs (incl. generated): 3,069.
- Structures/inductives: 50.
- `sorry` / `admit` / `axiom` in `CollatzShadowing`: **0** (machine-verified).
- The 43,513 generator-emitted lines are exact finite certificates emitted
  by the Python generators (CW row witnesses, residue-cell matrices, SCC
  walks). They are verified by Lean but were **not** reasoned line by line;
  never report the 51k total as "AI-authored proof".

AI-authored modules (lines):

| module | lines | role |
|---|---:|---|
| `CollatzBridge.lean` | 3,200 | descent bridge + first-barrier machinery |
| `Auxiliary.lean` | 1,222 | shadowing auxiliary lemmas |
| `WeakBridge.lean` | 1,162 | A0 weak-bridge finite lemmas, BitLength, TailCount |
| `Bound.lean` | 498 | generic weighted Collatz–Wielandt bound |
| `Phantom.lean` | 323 | phantom words, `C_w`, `A_w`, `q_w` |
| `EpisodeGraph.lean` | 253 | episode graph / SCC interfaces |
| `Operator.lean` | 231 | phase states, `full = core + tail` |
| `Shadowing.lean` | 190 | Lemma 3.1 (exact shadowing) |
| `Syracuse2Adic.lean` | 180 | 2-adic Syracuse extension |
| `Inventory.lean` | 172 | Mathlib API scratch buffer (not proof content) |
| `NoInfinite.lean` | 153 | Cor. 3.4 + expanding-cycle exclusion |
| `EpisodeInventory.lean` | 102 | Phase-8 API scratch buffer |
| `Basic.lean` | 96 | accelerated Syracuse map `S`, `ν₂` |
| `CollatzShadowing.lean` | 23 | module entry point |

### Python

| folder | files | lines | role |
|---|---:|---:|---|
| `scripts/spectral_program/` | 83 | 28,802 | spectral + Phase-10 frontier (→ script 126) |
| `scripts/early_empirical/` | 42 | 14,889 | legacy quasi-Lyapunov work (**phase one**) |
| `scripts/phantom_taxonomy/` | 16 | 4,164 | taxonomy, SCC, deterministic certificates, Lean generators |
| (root-level legacy `*_fast.py`) | 10 | 6,154 | earliest scripts at repo root |
| **Total** | 151 | 54,009 | |

All 151 Python files are git-tracked (**0 untracked** — nothing slipped the
count). Excludes `.venv/` (third-party libraries) and
`collatz_supplementary_v2/` (a duplicate copy of project files). All
AI-authored.

### Prose / other

- Working notes (`notes/*.md`): 54 files, 28,716 lines.
- Paper LaTeX (`paper/*.tex`): 5 files (v1–v4 + finite-rank note), 6,183 lines.

---

## 2. Git history

- Commits on `main`: **84**.
- Span: **2026-04-28 → 2026-06-04** = **37 days (~5.3 weeks)**.
- Tags: 0. Branch refs (incl. remotes/worktrees): 9.
- Churn across all history: **850,357 insertions / 555,773 deletions**.
  - ⚠️ Inflated by regenerated certificates, committed PDFs and other
    binaries; this is "lines ever touched", **not** lines hand-typed.
- Authors (`git shortlog -sn --all`, via `.mailmap`):
  - **Codex** — 52 (committed under the default placeholder
    `Your Name <you@example.com>`; remapped via `.mailmap` to reflect AI
    authorship),
  - **Piero Borgatta** — 35 (machine-local emails consolidated via `.mailmap`).
  - The raw commit objects/hashes are **unchanged**; `.mailmap` fixes
    display and statistics only (no history rewrite).

---

## 3. Versions (Zenodo)

| version | DOI | framing |
|---|---|---|
| concept (latest) | 10.5281/zenodo.20021537 | — |
| v1 | 10.5281/zenodo.20021538 | original spectral program (proposed as a possible Collatz resolution) |
| v2 | 10.5281/zenodo.20098868 | Lean shadowing core + Chang comparison |
| v3 | 10.5281/zenodo.20160154 | conditional reduction + taxonomy + extended Lean |
| v4 | 10.5281/zenodo.20544464 | verified core, two barriers, repositioning |
| **v5 (current)** | 10.5281/zenodo.20554750 | methodology retrospective + this statistics + honest close |

The v1→v5 arc (ambition → honest repositioning → retrospective) is the
narrative spine of the methodology paper.

---

## 4. Approaches tried and abandoned (qualitative — methodology data)

A real strength for an honest case study: the program explored and *killed*
many branches, and ended by proving its own ceiling.

1. Early quasi-Lyapunov / "gravitational-debt" heuristics (`early_empirical`).
2. Finite transfer operators + weighted Collatz–Wielandt bounds (kept as finite certificates).
3. `ℤ₂` martingale Banach space — **failed** (negative 2-adic child-cylinder oscillation).
4. A0 weak averaged bridge — partial; blocked by the distributional→pointwise barrier.
5. A1 refined-square kernel — diagnostic side branch only.
6. Pointwise first-barrier branch — conditional; **negatively resolved** in v4 (non-transport lemma).
7. Four "revolutionary" pivots (Galois/anabelian; non-standard models/independence; exotic Banach; holomorphic extension) — all rejected with explicit structural reasons.

---

## 5. Human / AI contribution split (qualitative)

- **Human (author):** research direction, conceptual framing, strategic
  decisions, the decision to publish each version, all external actions
  (Zenodo, compilation, pushes).
- **AI assistants:** OpenAI Codex + Google Gemini (early empirical scripts);
  Anthropic Claude (spectral program, Lean formalization, drafting);
  **cross-AI checking** (alternating Claude/Codex) for the Lean work and for
  auditing each other's proposals.
- See `METHODOLOGY.md` for the full disclosure.

---

## 6. Soft metrics — TO BE FILLED BY PIERO (do not fabricate)

These are NOT cleanly measurable from the repo. Fill them honestly, labelled
as estimates; **do not invent an "AI work hours" number** — LLM inference
time is not comparable to human labour hours.

- Human hours (author's own work — direction, review, decisions, external actions), estimate: **≈ 8 h**.
- Interactive AI-chat session time (wall-clock), estimate: **≈ 60 h** (session wall-clock, *not* a fabricated "AI inference hours" figure).
- Number of AI sessions (Claude Code + Codex): not yet determined — to be investigated later from logs.
- Approx. number of conversational turns/messages: not yet determined — to be investigated later.
- Token volume: not logged — to be investigated later.
- Distinct AI models used over the project: Claude (Code), Codex, Gemini (exact variants to be detailed later).

Honest framing for the paper: report **interaction volume + wall-clock span +
your estimated human hours**, each clearly labelled. That is defensible; a
single "AI hours" figure is not.

---

## 7. Reproduce these numbers

```bash
# Lean hand-written vs generated
git ls-files '*.lean' | grep -v '/Generated/' | xargs wc -l | tail -1
git ls-files '*/Generated/*.lean' | xargs wc -l | tail -1
git ls-files '*.lean' | grep -v '/Generated/' | xargs grep -hE '^[[:space:]]*(theorem|lemma)[[:space:]]' | wc -l
# Python
git ls-files 'scripts/**/*.py' | xargs wc -l | tail -1
# git history + churn
git rev-list --count HEAD
git log --numstat --format= | awk '$1~/^[0-9]+$/{i+=$1} $2~/^[0-9]+$/{d+=$2} END{print i,d}'
# sorry/axiom check (expect 0)
grep -rnE 'sorry|admit|^[[:space:]]*axiom' lean/CollatzShadowing --include='*.lean'
```
