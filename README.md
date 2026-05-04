# A Spectral Reduction of the Collatz Conjecture via Phantom Orbit Shadowing

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20021537-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20021537)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8025--2405-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0001-8025-2405)

A research program reducing the open structural content of the Collatz
conjecture to a finite spectral problem on a family of nonnegative
matrices, supported by numerical evidence with a 16× safety margin from
the criticality threshold.

> **This is not a proof of the Collatz conjecture.** It is a structural
> reduction that isolates two explicit a priori estimates whose
> resolution would imply boundedness of all Syracuse orbits.

> **About this project.** This is the first artifact of a personal
> research program by an independent researcher exploring whether
> iterative collaboration with large language model assistants can
> support non-standard attempts at open mathematical problems. See
> [`METHODOLOGY.md`](METHODOLOGY.md) for the methodology, the
> contribution split between human and AI, and the planned formal
> verification phase (Lean 4 / Mathlib).

## Paper

| Format | Link |
|---|---|
| **PDF** | [`paper/collatz_spectral_reduction.pdf`](paper/collatz_spectral_reduction.pdf) |
| **LaTeX source** | [`paper/collatz_spectral_reduction.tex`](paper/collatz_spectral_reduction.tex) |
| **Frozen citable version** | [Zenodo, doi:10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538) |

## Summary

We construct a chain of structural reductions:

1. **Shadowing lemma** (rigorous theorem). Every positive integer
   satisfying $n \equiv q_w \pmod{2^{bA+1}}$ shadows a $2$-adic phantom
   periodic word $w$ for exactly $b$ periods of the Syracuse map. Here
   $q_w \in \mathbb{Q}_{<0}$ is the rational fixed point of the affine
   composition $S_w$.

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

## Repository structure

```
.
├── paper/                          Paper (PDF + LaTeX source)
│   ├── collatz_spectral_reduction.pdf
│   └── collatz_spectral_reduction.tex
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
├── METHODOLOGY.md                   AI assistance and provenance disclosure
├── LICENSE                          CC BY 4.0
└── .gitignore
```

The scripts are numbered roughly chronologically by the order in which
they were developed. The ones referenced in the paper are listed in
its supplementary appendix.

## Methodology and AI disclosure

The author led the research direction throughout: the conceptual
framing (gravitational debt, $\nu_2 = 1$ corridors, the shadowing
intuition), the strategic choices, the decision to publish at this
stage. The technical work — Python implementation, mathematical
formalization of the shadowing lemma and the weighted bound, and the
LaTeX manuscript — was developed in iterative collaboration with
large language model assistants:

- **OpenAI Codex** and **Google Gemini** for the early empirical
  scripts (`scripts/early_empirical/`).
- **Anthropic's Claude** (via the Claude Code interface) for the
  spectral program (`scripts/spectral_program/`), the formalization
  of the shadowing lemma and the weighted Collatz–Wielandt bound, and
  the drafting of the paper.

As of this version, the work has not been reviewed by a human
mathematical expert. Numerical results are deterministic and
reproducible from the supplementary scripts. Mathematical claims rest
on AI-assisted formalization and have not been externally validated;
the work is submitted explicitly to invite expert scrutiny.

A planned next phase is to mechanically verify the shadowing lemma in
**Lean 4 with Mathlib**. A revised version of this preprint will
incorporate the formal verification when complete.

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full methodology
description and the contribution split.

Constructive feedback from researchers in symbolic dynamics, $p$-adic
dynamical systems, and transfer operator theory is explicitly invited.

## Citation

If you use this material, please cite:

> Borgatta, P. (2026). *A Spectral Reduction of the Collatz Conjecture
> via Phantom Orbit Shadowing* (Version 1) [Preprint]. Zenodo.
> [https://doi.org/10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538)

```bibtex
@misc{borgatta2026collatz,
  author       = {Borgatta, Piero},
  title        = {A Spectral Reduction of the Collatz Conjecture
                  via Phantom Orbit Shadowing},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20021538},
  url          = {https://doi.org/10.5281/zenodo.20021538},
  note         = {Source code: \url{https://github.com/PieroBorgatta/Collatz}}
}
```

## License

Released under the [Creative Commons Attribution 4.0 International
License](https://creativecommons.org/licenses/by/4.0/).

## Contact

Piero Borgatta — Independent Researcher

- Email: `info@pieroborgatta.com`
- ORCID: [0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405)

Constructive feedback from researchers in symbolic dynamics, $p$-adic
dynamical systems, and transfer operator theory is explicitly welcome.
