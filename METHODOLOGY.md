# Methodology and Provenance

This document describes, in full and without omission, how the
material in this repository was produced. It is intended for readers
who want to evaluate the work with appropriate calibration.

## Authorship

**Piero Borgatta** is the sole human author. He is an independent
researcher with no formal mathematical training and no academic
affiliation. His direct contribution to this work consists of:

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

The author made no direct contribution to the formalization, the
proofs, the implementation of the scripts, or the drafting of the
paper.

## AI assistance

All technical execution of this project was carried out with
substantial assistance from large language model systems. A
breakdown by phase:

### Early empirical phase (`scripts/early_empirical/`)

Scripts numbered roughly `01` through `48`, plus `validate_*.py`.
Topics: orbit profiling, debt accumulation metrics, family
identification in inverse trees, false-alarm classification,
empirical search for the candidate quasi-Lyapunov $H$ function.

These scripts were developed with assistance from:
- **OpenAI Codex**, and
- **Google Gemini**.

The author guided the empirical questions and validated the results
manually against worked examples; he did not write or audit the code.

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
author's strategic feedback (what to emphasize, what to cut, what
honesty obligations to include), and compiled to PDF by the author
on Overleaf.

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
  bound, and all formal definitions rest entirely on AI-generated
  formalization. Subtle errors in definitions, inductive
  arguments, quantifier scope, or implicit assumptions cannot be
  excluded.
- **The phantom set is empirical.** The list of expansive phantom
  cycles up to $k = 24$ used in the construction has not been proved
  exhaustive; the empirical sweeps to $b \le 16$, $t \le 65535$ found
  no additional SCC, but this is not a proof.
- **The asymptotic behavior of bound$(T, j)$ is extrapolated, not
  proved.** The geometric decay of increments observed for
  $T \le 16$ and $j \le 128$ is consistent with a finite limit but
  is not a rigorous bound on the limit.

## Why this disclosure

Two reasons:

1. **Honesty toward readers.** A reader scrutinizing the proof of
   Lemma 3.1 should know that the proof was not produced by a trained
   mathematician. Most likely subtle issues cluster around: the
   precise meaning of $\nu_2$ on rationals in $\Z_2$, the implicit
   identifications between integers and $2$-adic integers, the
   handling of edge cases in the induction. A skeptical re-reading
   is the appropriate response.

2. **Solicitation of expert review.** The whole point of releasing
   this material is to invite scrutiny by experts in symbolic
   dynamics, $p$-adic dynamics, and transfer operator theory. Hiding
   the AI assistance would defeat that purpose: experts must read
   with full information about the provenance of the formalization.

## How to engage

- **For the math**: read Sections 3, 5, and 6 of the paper. If you
  find an error, an unjustified step, or an implicit assumption
  worth flagging, please contact the author.
- **For the numerics**: clone the repository, install NumPy and
  SciPy, and re-run any of the scripts in
  `scripts/spectral_program/`. The numerical claims should
  reproduce exactly.
- **For collaboration**: the author is an independent researcher
  open to collaboration with anyone willing to take the proofs
  seriously. Co-authorship on a corrected version is on the table.

## Contact

Piero Borgatta — `info@pieroborgatta.com` — ORCID
[0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405).
