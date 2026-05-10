# A Spectral Reduction of the Collatz Conjecture via Phantom Orbit Shadowing

[![DOI (latest)](https://img.shields.io/badge/DOI%20(latest)-10.5281%2Fzenodo.20021537-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20021537)
[![DOI (v2)](https://img.shields.io/badge/DOI%20(v2)-10.5281%2Fzenodo.20098868-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20098868)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8025--2405-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0001-8025-2405)

A research program reducing the open structural content of the Collatz
conjecture to a finite spectral problem on a family of nonnegative
matrices, supported by numerical evidence with a 16× safety margin from
the criticality threshold. The foundational shadowing lemma is
mechanically verified in Lean 4 with Mathlib (`sorry`-free).

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

The current authoritative version is **v2** (May 2026), which adds the
completed Lean 4 formalization of the shadowing core, an explicit
comparison with the concurrent work of Chang (2026, arXiv:2603.11066),
an expanded related-work section, and an extended methodology section.

| Format | Link |
|---|---|
| **PDF (v2)** | [`paper/collatz_spectral_reduction_v2.pdf`](paper/collatz_spectral_reduction_v2.pdf) |
| **LaTeX source (v2)** | [`paper/collatz_spectral_reduction_v2.tex`](paper/collatz_spectral_reduction_v2.tex) |
| **PDF (v1, archival)** | [`paper/collatz_spectral_reduction.pdf`](paper/collatz_spectral_reduction.pdf) |
| **LaTeX source (v1, archival)** | [`paper/collatz_spectral_reduction.tex`](paper/collatz_spectral_reduction.tex) |
| **Frozen citable v2** | [Zenodo, doi:10.5281/zenodo.20098868](https://doi.org/10.5281/zenodo.20098868) |
| **Frozen citable v1** | [Zenodo, doi:10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538) |
| **Latest version (concept DOI)** | [doi:10.5281/zenodo.20021537](https://doi.org/10.5281/zenodo.20021537) |

## Lean 4 formalization

The shadowing core of the paper is mechanically verified in
[Lean 4](https://leanprover.github.io/) with Mathlib (Lean v4.29.1,
Mathlib v4.29.1). The Lean project is `sorry`-free.

| Theorem (paper) | Lean declaration | File |
|---|---|---|
| Lemma 3.1 (Exact shadowing) | `exact_shadowing` | [`lean/CollatzShadowing/Shadowing.lean`](lean/CollatzShadowing/Shadowing.lean) |
| Periodic specialization | `exact_shadowing_periods` | [`lean/CollatzShadowing/Shadowing.lean`](lean/CollatzShadowing/Shadowing.lean) |
| Cor. 3.4 (No infinite shadowing) | `no_infinite_period_congruence_expansive` | [`lean/CollatzShadowing/NoInfinite.lean`](lean/CollatzShadowing/NoInfinite.lean) |

To rebuild from scratch:

```bash
cd lean
lake exe cache get   # downloads Mathlib precompiled cache
lake build           # builds the full project
```

Build instructions and a complete inventory of the Mathlib API used are
in [`lean/README.md`](lean/README.md) and
[`lean/CollatzShadowing/INVENTORY.md`](lean/CollatzShadowing/INVENTORY.md).

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

The two open conjectures isolated by this reduction are:

- **Uniform bound in $T$**: $\sup_{T,j} \mathrm{bound}(T, j) < 1$.
- **Signature closure in $j$**: empirical transition signatures
  stabilize for large $j$ with explicit decay rate.

We believe both can be approached via Lasota–Yorke + Hennion's theorem +
Keller–Liverani spectral perturbation theory, but we have not carried
this out.

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

See §1.2 and §9.1 of [paper v2](paper/collatz_spectral_reduction_v2.tex)
for the full literature comparison.

## Planned next steps

After the v2 release, the program continues in the following order
(see [`METHODOLOGY.md`](METHODOLOGY.md) for the extended discussion):

1. **Priority A — Phantom-set taxonomy vs Chang Theorem 7.15.**
   For a depth cutoff $K_0$ (initially $K_0 = 16$, possibly pushed to
   $K_0 = 20$), enumerate all primitive cyclic compositions of
   valuations with expansive drift via M\"obius inversion of necklace
   counts, compute their 2-adic representatives, simulate sufficiently
   many integer orbits in each residue class, and verify that no SCC
   outside the one reported in §8 of the paper appears. Bounded but
   non-trivial scripting; estimated one to two weeks of focused work.

2. **Priority B — Lean formalization of the episode graph and the
   truncated transfer operator.** Conditional on Priority A. Introduce
   in Lean a `SimpleDigraph` on nodes $(k, c, b)$, formalize the SCC
   computation, define `FULL_{T,j}` and the `CORE + TAIL`
   decomposition, and prove that the weighted Collatz–Wielandt bound
   is a true upper bound on the spectral radius for each finite
   $(T, j)$. Combinatorial work; no new mathematics, but the Mathlib
   graph and matrix infrastructure required is non-trivial. Estimated
   two to four weeks of LLM-assisted Lean sessions.

3. **Priority C — Spectral-gap analysis toward Conjecture 6.** A
   Lasota–Yorke inequality on a Banach space of 2-adic Lipschitz
   functions, Hennion's theorem for quasi-compactness, and
   Keller–Liverani perturbation theory to control the dependence on
   $T$. Recent literature on quasi-compactness with countable branches
   ([arXiv:2406.19929](https://arxiv.org/abs/2406.19929)) and on
   certified spectral approximation
   ([arXiv:2602.19435](https://arxiv.org/abs/2602.19435)) provides a
   starting point. Open-ended and intentionally flagged as a
   collaboration target: making concrete progress here requires
   bringing in a researcher who works in transfer operators on
   $p$-adic or symbolic systems.

A and B are bounded and scriptable. C is open-ended and
collaboration-dependent; it will not be attempted before A and B are
closed.

## Repository structure

```
.
├── paper/                          Paper (PDF + LaTeX source, v1 and v2)
│   ├── collatz_spectral_reduction.pdf      (v1)
│   ├── collatz_spectral_reduction.tex      (v1)
│   ├── collatz_spectral_reduction_v2.pdf
│   └── collatz_spectral_reduction_v2.tex
│
├── lean/                           Lean 4 + Mathlib formalization
│   ├── CollatzShadowing/
│   │   ├── Basic.lean              ν₂, accelerated Syracuse map
│   │   ├── Phantom.lean            PhantomWord, q_w, S_w
│   │   ├── Syracuse2Adic.lean      Total 2-adic extension
│   │   ├── Auxiliary.lean          Supporting lemmas
│   │   ├── Shadowing.lean          Lemma 3.1 (sorry-free)
│   │   ├── NoInfinite.lean         Corollary 3.4 (sorry-free)
│   │   ├── Inventory.lean          Mathlib API scratch buffer
│   │   └── INVENTORY.md            Mathlib API inventory
│   ├── CollatzShadowing.lean       Module entry point
│   ├── lakefile.toml
│   ├── lean-toolchain
│   ├── README.md
│   └── TODO.md                     Operational TODO + session log
│
├── scripts/
│   ├── spectral_program/           Current frontier (39 scripts, 49–87)
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
│   └── early_empirical/            Legacy quasi-Lyapunov work (50 scripts, 01–48)
│
├── notes/
│   ├── collatz_shadowing_lemma_v1.md     Working notebook for the paper
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

As of v2, the work has not been reviewed by a human mathematical
expert. Numerical results are deterministic and reproducible from the
supplementary scripts; the Lean code is mechanically checkable with a
single `lake build` invocation. Mathematical claims that are not yet
formalized rest on AI-assisted formalization and have not been
externally validated; the work is submitted explicitly to invite
expert scrutiny.

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full methodology
description, the contribution split, the cross-AI verification
protocol, the literature reconnaissance method, and the planned next
phases.

Constructive feedback from researchers in symbolic dynamics, $p$-adic
dynamical systems, and transfer operator theory is explicitly invited.

## Citation

If you use this material, please cite the v2 (current authoritative)
version:

> Borgatta, P. (2026). *A Spectral Reduction of the Collatz Conjecture
> via Phantom Orbit Shadowing* (Version 2) [Preprint]. Zenodo.
> [https://doi.org/10.5281/zenodo.20098868](https://doi.org/10.5281/zenodo.20098868)

```bibtex
@misc{borgatta2026collatz_v2,
  author       = {Borgatta, Piero},
  title        = {A Spectral Reduction of the Collatz Conjecture
                  via Phantom Orbit Shadowing},
  year         = {2026},
  version      = {2.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20098868},
  url          = {https://doi.org/10.5281/zenodo.20098868},
  note         = {Source code and Lean 4 formalization:
                  \url{https://github.com/PieroBorgatta/Collatz}.
                  Concept DOI (latest version):
                  \url{https://doi.org/10.5281/zenodo.20021537}}
}
```

To cite the v1 (archival) version specifically, use DOI
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
