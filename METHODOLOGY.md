# Methodology and Research Program

## Research program

This document is the methodological backbone of an ongoing personal
research program by **Piero Borgatta**, an independent researcher,
exploring a single question:

> *Can an independent researcher, in iterative collaboration with
> contemporary large language model assistants, produce useful
> non-standard attempts at long-standing open mathematical problems?*

The program does not assume the answer is yes. It is an experimental
methodology in itself, with the present work on the Collatz conjecture
as its first concrete attempt.

The intended pattern across multiple problems is:

1. **Conceptual seed**: a structural intuition about why a problem
   resists standard approaches, expressed in informal — sometimes
   physical — language.
2. **Iterative dialogue**: the intuition is unpacked, formalized, and
   stress-tested in extended sessions with one or more LLMs.
3. **Computational validation**: claims are reduced, where possible,
   to deterministic experiments on finite objects. Reproducibility is
   non-negotiable.
4. **Honest reduction**: the open content of the problem is isolated
   as explicit conjectures on finite, well-defined mathematical
   objects.
5. **External submission**: the artifact is published openly with
   full disclosure of methodology, and submitted to domain experts
   for scrutiny.
6. **Formal verification (planned)**: the rigorously stated lemmas
   are mechanically verified in a proof assistant (Lean 4 with
   Mathlib is the intended target).

The program is conscious of its limits. It does not claim to compete
with state-of-the-art AI-for-math systems such as DeepMind's
AlphaProof, which uses a tightly integrated Lean back-end and
reinforcement-learning components. The methodology here is closer to
*sustained expert prompting and iterative refinement* of
general-purpose LLMs, with reproducibility and external review as
the primary safeguards. The aim is to learn what this lighter
approach can and cannot achieve.

## Authorship

**Piero Borgatta** is the sole human author. His direct contribution
to this work consists of:

- the conceptual framing: the *gravitational debt* metaphor for orbit
  expansion, the empirical observation that $\nu_2 = 1$ corridors are
  the locus of explosive growth, and the structural intuition that
  integer rebels shadow $2$-adic phantom orbits associated with
  negative rational fixed points of the Syracuse map;
- the strategic direction of the research: the decision to abandon
  the empirical quasi-Lyapunov $H$ function (when its false-alarm
  pattern proved structurally inseparable from genuine rebels) and
  to pivot to the spectral reduction via shadowing and transfer
  operators;
- editorial and strategic decisions: which experiments to run, when
  to stop scaling, when to publish.

The technical execution — Python implementation, mathematical
formalization, and manuscript drafting — was developed in
collaboration with LLM systems, as detailed below.

## AI assistance, by phase

### Early empirical phase (`scripts/early_empirical/`)

Scripts numbered roughly `01` through `48`, plus `validate_*.py`.
Topics: orbit profiling, debt accumulation metrics, family
identification in inverse trees, false-alarm classification,
empirical search for the candidate quasi-Lyapunov $H$ function.

Developed with assistance from:
- **OpenAI Codex**, and
- **Google Gemini**.

The author guided the empirical questions and validated the results
manually against worked examples.

### Spectral program phase (`scripts/spectral_program/`)

Scripts numbered `49` through `87`. Topics: phantom rational
representatives, shadowing congruence verification, episode graph
construction, strongly connected component identification, the
critical symbolic operator, the CORE/TAIL decomposition, the weighted
Collatz–Wielandt bound, truncation stability, per-node and cross-node
SCC certificates.

These scripts, the mathematical formalization of Lemma 3.1 (the
exact congruential shadowing lemma), the construction of the transfer
operator in Section 5, the weighted bound of Section 6, the
conditional reduction theorem of Section 9, and the entire LaTeX
manuscript were developed with substantial assistance from
**Anthropic's Claude**, accessed via the Claude Code interface in
extended interactive sessions.

In particular, the following content originated in conversation with
Claude:

- the proof of Lemma 3.1 (induction on the bit valuation of the
  difference $S^j(n) - S^j(q_w)$);
- the construction of the refined phase state
  $(\nu_2(t), \mathrm{odd}(t) \bmod 4, h \bmod 4)$;
- the empirical core/tail signature decomposition;
- the derivation of the weighted Collatz–Wielandt bound and the
  observation that the right Perron eigenvector of FULL (rather than
  CORE) is the correct test vector;
- the cross-node operator construction and the topological
  interpretation of the SCC as a star centered on $(12, 2, 1)$;
- the formulation of the open conjectures and the conditional
  reduction theorem.

The author's role in this phase was to ask follow-up questions, to
suggest experiments, and to make strategic decisions about scope and
publication timing.

### Paper drafting

The LaTeX manuscript `paper/collatz_spectral_reduction.tex` was
drafted by Claude, refined through several iterations with the
author's strategic feedback (what to emphasize, what to cut, the
honesty obligations to include), and compiled to PDF by the author.

## What has been verified

- All numerical results in Sections 7 and 8 of the paper are
  deterministic and reproducible from the scripts in
  `scripts/spectral_program/`. Anyone with Python 3.10+, NumPy, and
  SciPy can re-run them.
- Cross-script imports (`load_module`) have been smoke-tested.
- The shadowing lemma has been numerically verified for $b \le 10$ on
  the empirical phantom set $k \le 24$ (script
  `55_shadowing_congruence.py`).
- The cross-node bound has been computed at $T = 8$, $j = 8$ over 5
  representative SCC nodes.

## What has *not* been verified

- **No human mathematician has reviewed the proofs.** Lemma 3.1, the
  conditional reduction theorem, the derivation of the weighted
  bound, and all formal definitions rest on AI-assisted
  formalization. External expert review is invited.
- **The phantom set is empirical.** The list of expansive phantom
  cycles up to $k = 24$ used in the construction has not been proved
  exhaustive; the empirical sweeps to $b \le 16$, $t \le 65535$ found
  no additional SCC, but this is not a proof.
- **The asymptotic behavior of bound$(T, j)$ is extrapolated, not
  proved.** The geometric decay of increments observed for
  $T \le 16$ and $j \le 128$ is consistent with a finite limit but
  is not a rigorous bound on the limit.

## Formal verification phase: COMPLETED

The most concrete next step in the research program — formal
mechanical verification of Lemma 3.1 — has been carried out in
**Lean 4 with Mathlib** (Lean v4.29.1, Mathlib v4.29.1). The
project is `sorry`-free.

Verified in Lean:

- `CollatzShadowing.exact_shadowing` — Lemma 3.1, the exact
  congruential shadowing lemma, paper-faithful in the 2-adic form.
- `CollatzShadowing.exact_shadowing_periods` — the periodic
  specialization with congruence bound `2^(b·A+1)`.
- `CollatzShadowing.no_infinite_period_congruence_expansive` —
  Corollary 3.4 (no infinite shadowing) for expansive phantoms.

Supporting infrastructure (~2,300 lines total across
`Basic.lean`, `Phantom.lean`, `Syracuse2Adic.lean`,
`Auxiliary.lean`, `Shadowing.lean`, `NoInfinite.lean`,
plus the `INVENTORY.md`/`Inventory.lean` Mathlib-API inventory):

- the paper-faithful 2-adic extension
  `Syracuse2adic : ℤ_2 → ℤ_2` of the accelerated Syracuse map;
- the structural `PhantomWord` datatype with positivity constraints;
- the discharge of the odd-denominator hypothesis on `q_w`
  for every phantom (no auxiliary hypothesis needed);
- the affine difference identity in `ℤ_2` and `ℚ_2`;
- the strict-ultrametric `ν₂`-stability under proximity;
- the matching property of `q_w`'s own `Syracuse2adic`-orbit;
- the periodicity identity `B(b·L) = b·A` to recover the
  paper's congruence bound.

The verification was carried out across approximately three
calendar days of focused sessions, alternating Anthropic Claude
(via Claude Code) and OpenAI Codex as primary technical
assistants. Cross-AI review caught several Mathlib v4.29.1 API
mismatches that one assistant missed.

The Lean formalization verifies the *shadowing core only*. It
does **not** formalize the episode graph (paper §4), the
transfer operator (paper §5), the weighted bound (paper §6), or
the conditional reduction theorem (paper §9). Those rest on
deterministic numerical computation and on the conjectures of
paper §9.

A revised version of the preprint (`v2`,
`paper/collatz_spectral_reduction_v2.tex`) incorporates the
formalization status, an updated literature comparison
(notably with Chang 2026, arXiv:2603.11066), and an explicit
methodology section.

## Literature reconnaissance method

Standard institutional signals (department seminars, ad-hoc
discussions, workshop announcements) that ordinarily flag related
work for institutionally embedded researchers are absent here, so
literature surveillance has to be made explicit.

The reconnaissance for this work was carried out as a separate
AI-assisted pipeline (kept in a sibling directory, not committed
to this public project repository because it consists largely of
third-party PDFs and intermediate scratch documents). The pipeline:

1. **Topic seeding.** A curated list of arXiv-relevant keywords
   covering the five main angles of the work: Collatz/Syracuse
   core, transfer-operator spectral theory, $p$-adic dynamics,
   non-negative matrices and Perron–Frobenius, and shadowing in
   non-Archimedean settings.
2. **Bulk metadata fetch.** ArXiv API queries on each topic,
   producing a few hundred candidate papers across the relevant
   `math.*` categories.
3. **Deduplication and ranking.** Papers ranked by a simple
   keyword-hit score against the topic seeds, plus presence in
   "core Collatz" listings; top 100 retained.
4. **PDF fetch and review.** Top 100 PDFs fetched; an LLM-assisted
   pass produced a paragraph-level review of each, flagging
   conceptual overlap with the present framework.
5. **Manual verification of the most consequential candidates.**
   Direct inspection of relevant sections of the highest-overlap
   papers (Chang 2026 §7 and §C; Siegel 2023 Part I.5; Rozier 2025
   Lemma 1) by the author.
6. **Synthesis.** A "related work" analysis written from the
   reviewed corpus, then condensed into §1.2 of the v2 paper.

Going forward, the reconnaissance will be repeated periodically
(monthly arXiv listing scans, citation-graph monitoring of seed
papers, MathSciNet/zbMATH searches under primary MSC 11B83 and
37N99 with secondary 47A10 and 11S99). Any newly surfaced related
work will trigger an addendum or revised version, posted in the
public repository within a reasonable time-frame.

The reconnaissance corpus, scripts, and intermediate scratch
documents are deliberately **not** committed to the project
repository: they would add tens of MB of third-party content
without independent value beyond what is already condensed into
the v2 paper. The reconnaissance method itself — what to do, which
sources to consult, how to rank — is documented above and is the
reusable artifact.

## How to engage

- **For the math**: read Sections 3, 5, and 6 of the paper. If you
  find an error, an unjustified step, or an implicit assumption
  worth flagging, please contact the author.
- **For the numerics**: clone the repository, install NumPy and
  SciPy, and re-run any of the scripts in
  `scripts/spectral_program/`. The numerical claims should
  reproduce exactly.
- **For collaboration**: the author is open to collaboration with
  anyone willing to take the proofs seriously. Co-authorship on a
  corrected version is on the table.

## Contact

Piero Borgatta — `info@pieroborgatta.com` — ORCID
[0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405).
