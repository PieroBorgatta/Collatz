# Collatz / Syracuse — Spectral Reduction via Phantom Orbit Shadowing

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20021538.svg)](https://doi.org/10.5281/zenodo.20021538)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8025--2405-A6CE39?logo=orcid)](https://orcid.org/0009-0001-8025-2405)

This repository contains the computational and theoretical material for a
proposed structural reduction of the Collatz conjecture to a finite
spectral problem.

> **Honest claim**: this is *not* a proof of Collatz. It is a research
> program that reduces the open structural content of the conjecture to
> two explicit a priori estimates on a family of finite nonnegative
> matrices, supported by numerical evidence with a 16× safety margin
> from the criticality threshold.

## Main artifact

The principal document is the paper

**[`paper/collatz_spectral_reduction.tex`](paper/collatz_spectral_reduction.tex)**

(LaTeX source; compile with `pdflatex` or via Overleaf — see below).

## Summary of the contribution

We construct a chain of structural reductions:

1. **Shadowing lemma** (rigorous theorem, Section 3 of the paper). Every
   positive integer $n$ that satisfies the residue condition
   $n \equiv q_w \pmod{2^{bA+1}}$ shadows a phantom periodic word $w$
   for exactly $b$ periods of the Syracuse map. Here $q_w \in \mathbb{Q}_{<0}$
   is the rational fixed point of the affine composition $S_w$.

2. **Episode graph** (empirical, Section 4). The dynamics of integer
   rebels are encoded as walks on a graph whose vertices are
   `(phantom, depth)` pairs. A single nontrivial strongly connected
   component (SCC) supports the slowest descent; its critical vertex is
   `(k=12, c=2, b=1)`.

3. **Finite transfer operator** (Section 5). For each truncation depth
   $T$ and high-bit lift count $j$ we construct an exact finite matrix
   $\mathrm{FULL}_{T,j}$ on the refined phase quotient
   `(v2(t), odd(t) mod 4, hit_index mod 4)`.

4. **Weighted perturbative bound** (Section 6). Using a Collatz–Wielandt
   estimate against the right Perron eigenvector of $\mathrm{FULL}_{T,j}$,
   we obtain a true upper bound
   $\rho(\mathrm{FULL}_{T,j}) \le \mathrm{bound}(T, j)$
   that is computable for every finite $(T, j)$.

5. **Numerical evidence** (Section 7). Across $T \le 16$ and $j \le 32$,
   $\mathrm{bound}(T, j) \le 0.052$ with monotone but geometrically
   decaying increments. Cauchy stability in $j$ is verified to $j=128$.

6. **Cross-node certificate** (Section 8). The assembled cross-node
   transfer operator on the SCC has spectral radius $0.0366$ — strictly
   less than the single-node worst-case bound at the critical vertex.

The two open conjectures (Section 9) are:

- **Conjecture 9.1 (uniform bound in $T$)**: there exists $B_\infty < 1$
  such that $\sup_{T,j} \mathrm{bound}(T,j) \le B_\infty$.
- **Conjecture 9.2 (signature closure in $j$)**: the empirical
  transition signatures stabilize for $j$ large with explicit decay rate.

Resolving either conjecture rigorously (we believe via Lasota–Yorke +
Hennion's theorem + Keller–Liverani perturbation theory) would yield a
proof of orbit boundedness for the Syracuse map.

## How to compile the paper

The repository contains the LaTeX source. To compile:

**Option A — Overleaf (no installation):**
Upload `paper/collatz_spectral_reduction.tex` to a new Overleaf
project. Overleaf compiles it to PDF in the browser.

**Option B — local with TeX Live / MacTeX:**
```bash
cd paper
pdflatex collatz_spectral_reduction.tex
pdflatex collatz_spectral_reduction.tex   # second pass for TOC
```

## Reproducing the numerical results

The supporting Python scripts are in the repository root, numbered
roughly chronologically by when they were developed (`01_*` through
`87_*`). The key scripts referenced in the paper are:

| Script | Computes |
|---|---|
| `54_phantom_rational_shadows.py` | Phantom rational representatives $q_w$ |
| `55_shadowing_congruence.py` | Numerical verification of the shadowing lemma |
| `59_shadow_episode_graph.py` | Episode graph construction |
| `60_episode_graph_diagnostics.py` | SCC identification |
| `75_critical_symbolic_operator.py` | Finite transfer operator at the critical node |
| `77_high_bit_tail_bound.py` | CORE/TAIL decomposition |
| `83_perturbation_gap_scaling.py` | Spectral gap scaling in $T, j$ |
| `84_weighted_perturbation_bound.py` | Weighted Collatz–Wielandt bound |
| `85_truncation_stability.py` | Cauchy/signature stability in $j$ |
| `86_scc_node_certificates.py` | Per-node bounds on the SCC |
| `87_cross_node_transfer.py` | Assembled cross-node operator |

To run them you need Python 3.10+, NumPy, and SciPy:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy
.venv/bin/python 87_cross_node_transfer.py --T 8 --j-count 8
```

CSV outputs from each script are excluded from the repository (they
are large and regenerated deterministically) but are produced under
predictable filenames `collatz_NN_*.csv`.

## Earlier work in this repository

The repository also contains earlier exploratory work on an empirical
quasi-Lyapunov function

$$ H(n) = \log(n) + 0.28 D_{\max,80} - 0.03 C_{\max,80} + 0.30 P_{\max,80} $$

(see `collatz_report_finale*.md` and `collatz_report_teoria_gravita*.md`).
This phase produced empirical observations (the gravitational debt
metaphor, the role of $\nu_2 = 1$ corridors, the existence of confluence
families) that motivated and ultimately reorganized into the spectral
program above. The lemma document
[`collatz_shadowing_lemma_v1.md`](collatz_shadowing_lemma_v1.md) is the
working notebook from which the paper was distilled.

## Citation

If you use this material, please cite the Zenodo deposit:

> Borgatta, P. (2026). *A Spectral Reduction of the Collatz Conjecture
> via Phantom Orbit Shadowing* (Version 1) [Preprint]. Zenodo.
> [https://doi.org/10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538)

BibTeX:

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

CC BY 4.0 (see `LICENSE`).

## Contact

Piero Borgatta — Independent Researcher

- Email: `info@pieroborgatta.com`
- ORCID: [0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405)

Constructive feedback from researchers in symbolic dynamics, $p$-adic
dynamical systems, and transfer operator theory is explicitly welcome.
