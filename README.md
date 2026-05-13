# A Spectral Reduction of the Collatz Conjecture via Phantom Orbit Shadowing

[![DOI (latest)](https://img.shields.io/badge/DOI%20(latest)-10.5281%2Fzenodo.20021537-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20021537)
[![DOI (v3)](https://img.shields.io/badge/DOI%20(v3)-10.5281%2Fzenodo.20160154-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20160154)
[![DOI (v2)](https://img.shields.io/badge/DOI%20(v2)-10.5281%2Fzenodo.20098868-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20098868)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8025--2405-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0001-8025-2405)

A research program reducing the open structural content of the Collatz
conjecture to a finite spectral problem on a family of nonnegative
matrices, supported by numerical evidence with a 16× safety margin from
the criticality threshold. The foundational shadowing lemma, the
generic weighted Collatz–Wielandt bound, and two specific generated
finite numerical certificates (the deterministic phantom-taxonomy
certificate at $K_0 = 16$ and the single-node $T = 10$, $j = 32$
certificate) are mechanically verified in Lean 4 with Mathlib
(`sorry`-free, `axiom`-free).

> **This is not a proof of the Collatz conjecture.** It is a structural
> reduction that isolates two explicit a priori estimates whose
> resolution would imply boundedness of all Syracuse orbits.

> **About this project.** This is the first artifact of a personal
> research program by an independent researcher exploring whether
> iterative collaboration with large language model assistants can
> support non-standard attempts at open mathematical problems. See
> [`METHODOLOGY.md`](METHODOLOGY.md) for the methodology, the
> contribution split between human and AI, the cross-AI verification
> protocol, and the planned next phases.

## Paper

The current authoritative version is **v3** (May 2026), which extends
v2 with a finite phantom-set taxonomy at depth $K_0 = 16$ via Möbius
inversion of necklace counts, a deterministic finite-residue-cell
Collatz–Wielandt certificate on the compressed $(K, b)$ macro-state
space (37 states, exact max ratio $< 3/4$), and an extended Lean 4
formalization covering the episode graph, the truncated transfer
operator with phase-state quotient, the generic weighted
Collatz–Wielandt bound, and two specific generated finite numerical
certificates (single-node at $T = 10$, $j = 32$ with bound $97/2000$;
deterministic finite residue-cell at $K_0 = 16$ with bound $3/4$).

| Format | Link |
|---|---|
| **PDF (v3)** | [`paper/collatz_spectral_reduction_v3.pdf`](paper/collatz_spectral_reduction_v3.pdf) |
| **LaTeX source (v3)** | [`paper/collatz_spectral_reduction_v3.tex`](paper/collatz_spectral_reduction_v3.tex) |
| **PDF (v2, archival)** | [`paper/collatz_spectral_reduction_v2.pdf`](paper/collatz_spectral_reduction_v2.pdf) |
| **LaTeX source (v2, archival)** | [`paper/collatz_spectral_reduction_v2.tex`](paper/collatz_spectral_reduction_v2.tex) |
| **PDF (v1, archival)** | [`paper/collatz_spectral_reduction.pdf`](paper/collatz_spectral_reduction.pdf) |
| **LaTeX source (v1, archival)** | [`paper/collatz_spectral_reduction.tex`](paper/collatz_spectral_reduction.tex) |
| **Frozen citable v3** | [Zenodo, doi:10.5281/zenodo.20160154](https://doi.org/10.5281/zenodo.20160154) |
| **Frozen citable v2** | [Zenodo, doi:10.5281/zenodo.20098868](https://doi.org/10.5281/zenodo.20098868) |
| **Frozen citable v1** | [Zenodo, doi:10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538) |
| **Latest version (concept DOI)** | [doi:10.5281/zenodo.20021537](https://doi.org/10.5281/zenodo.20021537) |

## Lean 4 formalization

The shadowing core, the generic weighted Collatz–Wielandt bound, and
two specific generated finite numerical certificates are mechanically
verified in [Lean 4](https://leanprover.github.io/) with Mathlib
(Lean v4.29.1, Mathlib v4.29.1). The Lean project is `sorry`-free and
`axiom`-free.

| Theorem (paper) | Lean declaration | File |
|---|---|---|
| Lemma 3.1 (Exact shadowing) | `exact_shadowing` | [`lean/CollatzShadowing/Shadowing.lean`](lean/CollatzShadowing/Shadowing.lean) |
| Periodic specialization | `exact_shadowing_periods` | [`lean/CollatzShadowing/Shadowing.lean`](lean/CollatzShadowing/Shadowing.lean) |
| Cor. 3.4 (No infinite shadowing) | `no_infinite_period_congruence_expansive` | [`lean/CollatzShadowing/NoInfinite.lean`](lean/CollatzShadowing/NoInfinite.lean) |
| Episode graph + finite-walk SCC certificate | `HubSCCCertificate`, `CriticalSCCCertificate` | [`lean/CollatzShadowing/EpisodeGraph.lean`](lean/CollatzShadowing/EpisodeGraph.lean) |
| Phase-state quotient + `FULL = CORE + TAIL` decomposition | `OperatorDecomposition`, `RowSubstochastic` | [`lean/CollatzShadowing/Operator.lean`](lean/CollatzShadowing/Operator.lean) |
| Generic weighted Collatz–Wielandt bound | `FiniteCWCertificate`, `spectralRadius_le_of_finiteCWCertificate` | [`lean/CollatzShadowing/Bound.lean`](lean/CollatzShadowing/Bound.lean) |
| Single-node spectral bound at $T = 10$, $j = 32$ | `t10j32HighBitTailSpectralRadiusBound_97_2000` (≤ 97/2000) | [`lean/CollatzShadowing/Generated/T10J32HighBitTailCW.lean`](lean/CollatzShadowing/Generated/T10J32HighBitTailCW.lean) |
| Deterministic finite-residue-cell certificate at $K_0 = 16$ | `k16s16KDeterministicGeneratedSpectralRadiusBound` (≤ 3/4) | [`lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean`](lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean) |
| Empirical 37-node CW baseline (historical) | `k16s16KFiniteCWCertificate`, `k16s16KSpectralRadiusBound` | [`lean/CollatzShadowing/Generated/K16S16KExactCWSummary.lean`](lean/CollatzShadowing/Generated/K16S16KExactCWSummary.lean) |

To rebuild from scratch:

```bash
cd lean
lake exe cache get   # downloads Mathlib precompiled cache
lake build           # builds the full project
```

Build instructions and a complete inventory of the Mathlib API used are
in [`lean/README.md`](lean/README.md),
[`lean/CollatzShadowing/INVENTORY.md`](lean/CollatzShadowing/INVENTORY.md),
and [`lean/CollatzShadowing/EPISODE_INVENTORY.md`](lean/CollatzShadowing/EPISODE_INVENTORY.md)
(Phase-8 modules).

## Summary

We construct a chain of structural reductions:

1. **Shadowing lemma** (rigorous theorem, mechanically verified in Lean).
   Every positive integer satisfying $n \equiv q_w \pmod{2^{bA+1}}$
   shadows a $2$-adic phantom periodic word $w$ for exactly $b$ periods
   of the Syracuse map. Here $q_w \in \mathbb{Q}_{<0}$ is the rational
   fixed point of the affine composition $S_w$.

2. **Episode graph** (empirical). Integer rebel orbits are encoded as
   walks on a graph whose vertices are `(phantom, depth)` pairs. A
   single nontrivial strongly connected component supports the slowest
   descent; its critical vertex is `(k=12, c=2, b=1)`.

3. **Finite transfer operator**. For each truncation depth $T$ and
   high-bit lift count $j$ we construct an exact finite matrix
   $\mathrm{FULL}_{T,j}$ on the refined phase quotient
   `(v2(t), odd(t) mod 4, hit_index mod 4)`.

4. **Weighted perturbative bound**. A Collatz–Wielandt estimate against
   the right Perron eigenvector of $\mathrm{FULL}_{T,j}$ yields a true
   upper bound $\rho(\mathrm{FULL}_{T,j}) \le \mathrm{bound}(T, j)$
   computable for every finite $(T, j)$.

5. **Numerical evidence**. $\mathrm{bound}(T, j) \le 0.052$ across
   $T \le 16$ and $j \le 32$, with monotone but geometrically decaying
   increments. Cauchy stability in $j$ verified to $j = 128$.

6. **Cross-node certificate**. The assembled cross-node transfer
   operator on the SCC has spectral radius $0.0366$ — strictly below
   the single-node worst-case bound at the critical vertex.

7. **Phantom-set taxonomy at $K_0 = 16$** (new in v3). M\"obius
   enumeration of all $1247$ primitive expansive cyclic compositions
   with $K \le 16$, exact rational $2$-adic representatives, orbit
   harness identifying a single nontrivial taxonomy SCC of $1222$ raw
   states; deterministic finite-residue-cell Collatz–Wielandt
   certificate on the compressed $(K, b)$ macro-state space with exact
   max ratio $90833233962213/129559208330288 < 3/4$, monotonically
   improving at $\mathrm{lift\_bits} \in \{4, 5, 6\}$.

8. **Lean-checked finite operator certificates** (new in v3). The
   single-node spectral bound at $T = 10, j = 32$ is exposed as
   `t10j32HighBitTailSpectralRadiusBound_97_2000` (≤ $97/2000$). The
   deterministic taxonomy certificate is exposed as
   `k16s16KDeterministicGeneratedSpectralRadiusBound` (≤ $3/4$). Both
   bridges target Mathlib's real `spectralRadius`; the project is
   `sorry`-free and `axiom`-free.

The two open conjectures isolated by this reduction are:

- **Uniform bound in $T$**: $\sup_{T,j} \mathrm{bound}(T, j) < 1$.
- **Signature closure in $j$**: empirical transition signatures
  stabilize for large $j$ with explicit decay rate.

We believe both can be approached via Lasota–Yorke + Hennion's theorem +
Keller–Liverani spectral perturbation theory, but we have not carried
this out. The v3 deterministic finite-residue-cell certificate closes
the taxonomy-completeness side of the v2 open scope; it does not
close the asymptotic-in-$T$ side.

## Relation to concurrent work

The most directly related concurrent work is **Chang (2026)**,
*Exploring Collatz Dynamics with Human-LLM Collaboration*
([arXiv:2603.11066](https://arxiv.org/abs/2603.11066)). Chang
independently introduces the same 2-adic *phantom cycles* construction
(his Definition 7.2 corresponds to our $q_w$ via
$\sigma \leftrightarrow w$, $K \leftrightarrow A$,
$\ell \leftrightarrow L$, $\rho \leftrightarrow q_w$), proves a
per-block 2-adic repulsion identity (his Prop. 7.4, of which our
shadowing lemma is the iterated form), establishes Phantom Universality
(every primitive cyclic composition is a phantom family), and obtains
unconditional bounds (per-orbit gain rate $R \le 0.0893$ and a depth-2
spectral bound $\rho(\widetilde{B}_2^{\mathrm{ext}}) \le 5/32$). Chang
identifies the same distributional-to-pointwise gap that obstructs our
Conjectures 6 and 7.

Differences: Chang aggregates over the entire phantom universe with
M\"obius-inversion-based counts; this work concentrates on a single
critical SCC with finer phase resolution and a different (non-nilpotent)
transfer operator. The two programs are complementary —
*broad-shallow* vs *narrow-deep* — and they reach quantitatively similar
bounds by very different routes, which we read as evidence that the
underlying phenomenology is robust.

See §1.2 and §10.1 of [paper v3](paper/collatz_spectral_reduction_v3.tex)
for the full literature comparison (renumbered from §9.1 in v2 due to
the inserted §9 on the phantom-set taxonomy).

## Planned next steps

After the v3 release, Priority A (taxonomy) and Priority B (Lean
formalization of the finite operator layer) are **complete**.
The remaining priority is the analytic program of Priority C, now
expressed as a gated A–J roadmap with explicit kill-switch and a
finite-rank fallback baseline already in place. See
[`lean/TODO.md`](lean/TODO.md) Phase 10 for the operational table and
§11.1 of [`paper/collatz_spectral_reduction_v3.tex`](paper/collatz_spectral_reduction_v3.tex)
for the published version.

- **Priority A — Phantom-set taxonomy** (closed in v3). A finite
  enumeration of all primitive expansive compositions up to depth
  $K_0 = 16$ produces a single nontrivial strongly connected component
  of $1222$ raw states; the deterministic finite-residue-cell
  Collatz–Wielandt certificate on the compressed $(K, b)$ macro-state
  space yields exact max ratio
  $90833233962213 / 129559208330288 < 3/4$, monotonically improving
  under finer residue refinement. The certificate is imported as
  `k16s16KDeterministicGeneratedSpectralRadiusBound` in Lean.

- **Priority B — Lean formalization of the episode graph and
  transfer operator** (closed in v3). The new modules
  `EpisodeGraph.lean`, `Operator.lean`, and `Bound.lean` formalize
  the episode graph, the phase-state quotient, the truncated transfer
  operator, the empirical signature decomposition, and the generic
  weighted Collatz–Wielandt bound. The single-$(T, j)$ certificate at
  $T = 10, j = 32$ is generated and Lean-checked under
  `Generated/T10J32HighBitTailCW.lean` (≤ $97/2000$) with no `axiom`,
  `sorry`, or `admit`.

- **Priority C — Transfer-operator roadmap toward Conjecture 6**
  (program for v4 / companion / collaboration). Restructured as a
  gated 10-step sequence (A)–(J):
  1. (A) literature and hypothesis matrix, with Chang 2026
     compatibility as a column;
  2. (B) identify the correct infinite phase space behind
     $\mathrm{FULL}_{T, j}$ (load-bearing question; kill-switch
     source);
  3. (C) compare candidate Banach spaces;
  4. (D) explicit transfer-operator formulation;
  5. (E) target Lasota–Yorke inequality;
  6. (F) conditional skeletons (Hennion + Keller–Liverani);
  7. (G) finite-rank / truncated-operator fallback — **already a
     partial baseline**, namely the deterministic finite-residue-cell
     certificate of v3 at $K_0 = 16, \mathrm{lift\_bits} = 4$, with
     sensitivity at $\{5, 6\}$ confirming the bound;
  8. (H) computational experiments for constants, sequenced strictly
     after (C) and (D);
  9. (I) collaboration package;
  10. (J) decision (v4 vs companion vs coauthored) with binding
      kill-switch: if (B) concludes the finite matrices are not
      exact projections of any natural infinite kernel, (E) and (F)
      are skipped and (G) is the program output.

  Open-ended and intentionally flagged as a collaboration target.
  Steps (A)–(D) are planning artifacts attackable solo with
  AI-assisted research; (E)–(F) require analytic expertise beyond
  the author's; (G) is partially closed; (I)–(J) close the program.

## Repository structure

```
.
├── paper/                          Paper (PDF + LaTeX source, v1, v2 and v3)
│   ├── collatz_spectral_reduction.pdf      (v1, archival)
│   ├── collatz_spectral_reduction.tex      (v1, archival)
│   ├── collatz_spectral_reduction_v2.pdf   (v2, archival)
│   ├── collatz_spectral_reduction_v2.tex   (v2, archival)
│   ├── collatz_spectral_reduction_v3.pdf   (v3, authoritative)
│   └── collatz_spectral_reduction_v3.tex   (v3, authoritative)
│
├── lean/                           Lean 4 + Mathlib formalization
│   ├── CollatzShadowing/
│   │   ├── Basic.lean              ν₂, accelerated Syracuse map
│   │   ├── Phantom.lean            PhantomWord, q_w, S_w
│   │   ├── Syracuse2Adic.lean      Total 2-adic extension
│   │   ├── Auxiliary.lean          Supporting lemmas (incl. B_closed_form)
│   │   ├── Shadowing.lean          Lemma 3.1 (sorry-free)
│   │   ├── NoInfinite.lean         Corollary 3.4 (sorry-free)
│   │   ├── EpisodeGraph.lean       Episode graph + finite-walk SCC cert (v3)
│   │   ├── Operator.lean           PhaseState quotient, OperatorDecomposition (v3)
│   │   ├── Bound.lean              Generic weighted Collatz–Wielandt bound (v3)
│   │   ├── Generated/
│   │   │   ├── T10CriticalSymbolic.lean       Exact T=10 critical-symbolic matrix
│   │   │   ├── T10J32HighBitTail.lean         Exact T=10, j=32 CORE+TAIL decomp
│   │   │   ├── T10J32HighBitTailCW.lean       Spectral bound ≤ 97/2000 (v3)
│   │   │   ├── T10J32HighBitTailCWData.lean   CW data
│   │   │   ├── T10J32HighBitTailCWRows00–13.lean   224 evaluated rows
│   │   │   ├── K16S16KSCC.lean                K0=16 taxonomy SCC certificate
│   │   │   ├── K16S16KExactCWSummary.lean     Empirical 37-node CW baseline
│   │   │   ├── K16S16KBridge.lean             SCC + CW bridge
│   │   │   ├── K16S16KDeterministicCW.lean    Deterministic ≤ 3/4 bound (v3)
│   │   │   └── K16S16KCWSmoke.lean            Regression smoke test
│   │   ├── Inventory.lean          Mathlib API scratch buffer
│   │   ├── INVENTORY.md            Mathlib API inventory
│   │   └── EPISODE_INVENTORY.md    Phase-8 modules inventory (v3)
│   ├── CollatzShadowing.lean       Module entry point
│   ├── lakefile.toml
│   ├── lean-toolchain
│   ├── README.md
│   └── TODO.md                     Operational TODO + session log (Phases 0–10)
│
├── scripts/
│   ├── spectral_program/           Numerical core, v1/v2 (39 scripts, 49–87)
│   │   ├── 54_phantom_rational_shadows.py
│   │   ├── 55_shadowing_congruence.py
│   │   ├── 59_shadow_episode_graph.py
│   │   ├── 60_episode_graph_diagnostics.py
│   │   ├── 75_critical_symbolic_operator.py
│   │   ├── 77_high_bit_tail_bound.py
│   │   ├── 84_weighted_perturbation_bound.py
│   │   ├── 85_truncation_stability.py
│   │   ├── 86_scc_node_certificates.py
│   │   ├── 87_cross_node_transfer.py
│   │   └── ...
│   │
│   ├── phantom_taxonomy/           Phantom-set taxonomy at K_0 = 16 (v3)
│   │   ├── necklace_counts.py                  Möbius enumeration M(K, ℓ)
│   │   ├── phantom_representatives.py          Exact rational q_w
│   │   ├── orbit_harness.py                    Integer-lift orbit harness
│   │   ├── scc_transfer_summary.py             Substochastic retention
│   │   ├── scc_collatz_wielandt.py             Empirical CW expressions
│   │   ├── scc_cw_certificate.py               Exact rational CW verifier
│   │   ├── deterministic_residue_transfer.py   Deterministic residue cells (v3)
│   │   ├── lean_scc_certificate.py             Lean SCC generator
│   │   ├── lean_cw_summary.py                  Lean CW summary generator
│   │   ├── lean_phase_transfer.py              T=10 critical-symbolic generator
│   │   ├── lean_high_bit_tail.py               Operator decomp generator
│   │   ├── lean_t10j32_cw.py                   T=10, j=32 CW generator
│   │   ├── lean_cw_smoke.py                    Smoke certificate generator
│   │   └── ...                                 CSVs, JSON certificates, notes
│   │
│   └── early_empirical/            Legacy quasi-Lyapunov work (50 scripts, 01–48)
│
├── notes/
│   ├── collatz_shadowing_lemma_v1.md     Working notebook for the paper
│   ├── phantom_taxonomy.md               v3 taxonomy summary
│   ├── phantom_taxonomy_k16_scc_report.md            K0=16 SCC report
│   ├── phantom_taxonomy_k16_s16_scc_report.md        SCC details
│   ├── phantom_taxonomy_empirical_scc_integration.md Empirical → deterministic
│   └── archive/                          Earlier reports (Italian)
│
├── README.md
├── METHODOLOGY.md                   AI assistance, methodology, planned next phases
├── LICENSE                          CC BY 4.0
└── .gitignore
```

The Python scripts are numbered roughly chronologically by the order in
which they were developed. The ones referenced in the paper are listed
in its supplementary appendix.

## Methodology and AI disclosure

The author led the research direction throughout: the conceptual
framing (gravitational debt, $\nu_2 = 1$ corridors, the shadowing
intuition, the pivot to the spectral program), the strategic choices,
the decision to publish at this stage. The technical work — Python
implementation, mathematical formalization of the shadowing lemma and
the weighted bound, the **Lean 4 verification** of the shadowing core,
and the LaTeX manuscript — was developed in iterative collaboration
with large language model assistants:

- **OpenAI Codex** and **Google Gemini** for the early empirical
  scripts (`scripts/early_empirical/`).
- **Anthropic's Claude** (via the Claude Code interface) for the
  spectral program (`scripts/spectral_program/`), the formalization
  of the shadowing lemma and the weighted Collatz–Wielandt bound, the
  Lean 4 verification, and the drafting of the paper.

The Lean phase explicitly used **cross-AI checking** (alternating
Claude and Codex) to catch Mathlib API mismatches that one assistant
missed.

As of v3, the work has not been reviewed by a human mathematical
expert. Numerical results are deterministic and reproducible from the
supplementary scripts (including the v3 exact-rational deterministic
finite-residue-cell certificate); the Lean code is mechanically
checkable with a single `lake build` invocation. Mathematical claims
that are not yet formalized rest on AI-assisted formalization and have
not been externally validated; the work is submitted explicitly to
invite expert scrutiny.

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full methodology
description, the contribution split, the cross-AI verification
protocol, the literature reconnaissance method, and the planned next
phases.

Constructive feedback from researchers in symbolic dynamics, $p$-adic
dynamical systems, and transfer operator theory is explicitly invited.

## Citation

If you use this material, please cite the v3 (current authoritative)
version:

> Borgatta, P. (2026). *A Spectral Reduction of the Collatz Conjecture
> via Phantom Orbit Shadowing* (Version 3) [Preprint]. Zenodo.
> [https://doi.org/10.5281/zenodo.20160154](https://doi.org/10.5281/zenodo.20160154)

```bibtex
@misc{borgatta2026collatz_v3,
  author       = {Borgatta, Piero},
  title        = {A Spectral Reduction of the Collatz Conjecture
                  via Phantom Orbit Shadowing},
  year         = {2026},
  version      = {3.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20160154},
  url          = {https://doi.org/10.5281/zenodo.20160154},
  note         = {Source code and Lean 4 formalization:
                  \url{https://github.com/PieroBorgatta/Collatz}.
                  Concept DOI (latest version):
                  \url{https://doi.org/10.5281/zenodo.20021537}}
}
```

To cite the v2 version specifically, use DOI
`10.5281/zenodo.20098868`. To cite the v1 (archival) version, use DOI
`10.5281/zenodo.20021538`.

## License

Released under the [Creative Commons Attribution 4.0 International
License](https://creativecommons.org/licenses/by/4.0/).

## Contact

Piero Borgatta — Independent Researcher

- Email: `info@pieroborgatta.com`
- ORCID: [0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405)

Constructive feedback from researchers in symbolic dynamics, $p$-adic
dynamical systems, and transfer operator theory is explicitly welcome.
