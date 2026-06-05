# Phantom Orbit Shadowing for the Collatz Conjecture

[![DOI (latest)](https://img.shields.io/badge/DOI%20(latest)-10.5281%2Fzenodo.20021537-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20021537)
[![DOI (v5)](https://img.shields.io/badge/DOI%20(v5)-10.5281%2Fzenodo.20554750-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20554750)
[![DOI (v4)](https://img.shields.io/badge/DOI%20(v4)-10.5281%2Fzenodo.20544464-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20544464)
[![DOI (v3)](https://img.shields.io/badge/DOI%20(v3)-10.5281%2Fzenodo.20160154-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20160154)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8025--2405-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0001-8025-2405)

An AI-assisted research program on the Collatz conjecture. It builds a
**mechanically verified core** (an exact congruential shadowing lemma, a
no-infinite-shadowing corollary, finite Collatz–Wielandt spectral-radius
certificates, and a phantom-set taxonomy), all formalized in Lean 4 +
Mathlib and `sorry`-free.

> **This is not a proof of the Collatz conjecture, and v4 does not claim
> progress toward one.** v4 is a *consolidation and repositioning*: it
> states precisely what is verified, identifies the two distinct barriers
> the program runs into, proves *why* the current approaches stop there,
> and records the decision about what to do next.

> **About this project.** A personal research program by an independent
> researcher exploring whether iterative collaboration with large language
> model (LLM) assistants can support non-standard attempts at open
> problems. Verifying the practical limits of that collaboration is an
> explicit secondary goal. See [`METHODOLOGY.md`](METHODOLOGY.md).

## Paper

The latest version is **v5** (a methodology retrospective and honest close).
The core mathematical paper is **v4** (consolidation and limitations): the
verified core, an honest map of the two barriers, and the repositioning.

| Version | Framing | LaTeX | Frozen PDF |
|---|---|---|---|
| **v5 (current)** | Methodology retrospective; verified core + Reservoir library | [`paper/collatz_spectral_reduction_v5.tex`](paper/collatz_spectral_reduction_v5.tex) | [Zenodo doi:10.5281/zenodo.20554750](https://doi.org/10.5281/zenodo.20554750) |
| v4 | Verified core, two barriers, repositioning | [`paper/collatz_spectral_reduction_v4.tex`](paper/collatz_spectral_reduction_v4.tex) | [Zenodo doi:10.5281/zenodo.20544464](https://doi.org/10.5281/zenodo.20544464) |
| v3 | Conditional spectral reduction + taxonomy + extended Lean | [`paper/collatz_spectral_reduction_v3.tex`](paper/collatz_spectral_reduction_v3.tex) | [Zenodo doi:10.5281/zenodo.20160154](https://doi.org/10.5281/zenodo.20160154) |
| v2 | Lean shadowing core + Chang comparison | [`paper/collatz_spectral_reduction_v2.tex`](paper/collatz_spectral_reduction_v2.tex) | [Zenodo doi:10.5281/zenodo.20098868](https://doi.org/10.5281/zenodo.20098868) |
| v1 (archival) | Original spectral program | [`paper/collatz_spectral_reduction.tex`](paper/collatz_spectral_reduction.tex) | [Zenodo doi:10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538) |

Concept DOI (always resolves to the latest version):
[10.5281/zenodo.20021537](https://doi.org/10.5281/zenodo.20021537).

## What v4 establishes

**The conjecture splits into two genuinely distinct hard halves, behind
two different walls:**

- **No divergent orbits.** Barrier: *distributional-to-pointwise*. Density-1
  descent is known (Terras/Everett; Tao 2019, almost-all); every-`n`
  descent is not, and no pointwise obstruction is known. Both analytic
  branches of this program (a weak/operator branch and a pointwise
  first-barrier branch) provably fall into this barrier.
- **No nontrivial cycles.** Barrier: *Diophantine approximation of
  `log₂3`*. Partial exclusions exist (Steiner 1-cycles; Simons 2-cycles;
  Simons–de Weger `m`-cycles to `m≈68`; verification to `~2^69`), but the
  full statement is open behind Baker-type bounds.

**Main new results in v4:**

- A **negative resolution** of the pointwise first-barrier route: within
  the present phantom/2-adic formalism, the sought aperiodic rigidity on
  the orbit limit `ξ_W` is *logically equivalent* to the divergence
  conjecture itself (a non-transport lemma: the parity-vector conjugacy
  carries eventual periodicity to dynamical pre-periodicity, **not** to
  rationality). This is a paper-level argument conditional on the standard
  Lagarias coding.
- A **new Lean-checked fact**: no positive integer lies on an expanding
  cycle (post-prefix congruence form,
  `no_positive_endpoint_eventually_periodic_expansive_congruence`),
  generalizing the no-infinite-shadowing corollary.
- The resulting **repositioning** (see *Planned next steps*).

## Lean 4 formalization

Verified with Lean v4.29.1 + Mathlib v4.29.1. The `CollatzShadowing`
sources are `sorry`-, `admit`- and `axiom`-free.

| Result | Lean declaration | File |
|---|---|---|
| Exact shadowing (Lemma 3.1) | `exact_shadowing`, `exact_shadowing_periods` | [`Shadowing.lean`](lean/CollatzShadowing/Shadowing.lean) |
| No infinite (periodic) shadowing (Cor. 3.4) | `no_infinite_period_congruence_expansive` | [`NoInfinite.lean`](lean/CollatzShadowing/NoInfinite.lean) |
| No integer on an expanding cycle (post-prefix form) — **new** | `no_positive_endpoint_eventually_periodic_expansive_congruence` | [`NoInfinite.lean`](lean/CollatzShadowing/NoInfinite.lean) |
| Single-node CW spectral bound `ρ ≤ 97/2000` | `t10j32HighBitTailSpectralRadiusBound_97_2000` | [`Generated/T10J32HighBitTailCW.lean`](lean/CollatzShadowing/Generated/T10J32HighBitTailCW.lean) |
| Deterministic `(K,b)` CW bound `< 3/4` (`K₀=16`) | `k16s16KDeterministicGeneratedSpectralRadiusBound` | [`Generated/K16S16KDeterministicCW.lean`](lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean) |
| Generic weighted Collatz–Wielandt bound | `spectralRadius_le_of_finiteCWCertificate` | [`Bound.lean`](lean/CollatzShadowing/Bound.lean) |
| Finite weak row-`L¹` bridge | `WeakBridge.weighted_action_diff_le` | [`WeakBridge.lean`](lean/CollatzShadowing/WeakBridge.lean) |
| Exact high-`ν₂` source-tail mass `≤ 2⁻ᴿ` | `WeakBridge.TailCount.dyadic_tail_count_mul_le`, `dyadic_tail_mass_le` | [`WeakBridge.lean`](lean/CollatzShadowing/WeakBridge.lean) |
| Bit-length / `δ`-boundary period estimate | `WeakBridge.BitLength.biAffineDelta_dyadicWeight_period_boundary_le` | [`WeakBridge.lean`](lean/CollatzShadowing/WeakBridge.lean) |
| Descent bridge (elementary): descent ⇒ Collatz | `classicalCollatz_of_uniformStrictDescent_provedBridge` | [`CollatzBridge.lean`](lean/CollatzShadowing/CollatzBridge.lean) |
| Conditional cylinder descent (first-barrier) | `A0EndpointSuffixExitAll_of_firstBarrier` | [`CollatzBridge.lean`](lean/CollatzShadowing/CollatzBridge.lean) |

Supporting modules: `Basic`, `Phantom`, `Syracuse2Adic`, `Auxiliary`
(shadowing infrastructure); `EpisodeGraph`, `Operator`, `Bound`
(finite episode-graph / transfer-operator / Collatz–Wielandt layer);
`Generated/*` (machine-generated finite certificates). API inventory in
[`lean/CollatzShadowing/INVENTORY.md`](lean/CollatzShadowing/INVENTORY.md)
and [`lean/CollatzShadowing/EPISODE_INVENTORY.md`](lean/CollatzShadowing/EPISODE_INVENTORY.md).

To rebuild:

```bash
cd lean
lake exe cache get   # downloads Mathlib precompiled cache
lake build           # builds the full project
```

## Scripts

- [`scripts/spectral_program/`](scripts/spectral_program/) — the spectral
  and Phase-10 frontier (through script 126): episode graph, finite
  `FULL = CORE + TAIL` operators, weighted Collatz–Wielandt bounds,
  truncation/Cauchy stability, the 2-adic cylinder and martingale
  diagnostics, and the A0 weak-bridge program (decay law, high-`ν₂` tail,
  Walsh–Haar / dyadic-discrepancy probes, bounded-periodicity and
  kernel-mismatch decomposition, affine return-branch certificates).
- [`scripts/phantom_taxonomy/`](scripts/phantom_taxonomy/) — Möbius/necklace
  enumeration of primitive cyclic compositions, exact 2-adic
  representatives, the orbit harness, SCC/Collatz–Wielandt certificates,
  the deterministic residue-cell transfer, and the Lean certificate
  generators.
- [`scripts/early_empirical/`](scripts/early_empirical/) — legacy
  quasi-Lyapunov work.

## Relation to concurrent work

The most directly related concurrent work is **Chang (2026)**,
*Exploring Collatz Dynamics with Human–LLM Collaboration*
([arXiv:2603.11066](https://arxiv.org/abs/2603.11066)), which independently
introduces the same 2-adic *phantom cycles* construction and obtains
unconditional aggregate bounds. Chang identifies the same
distributional-to-pointwise gap that v4 locates precisely in this
program’s own objects. The two programs are complementary —
*broad-shallow* aggregation vs *narrow-deep* single-SCC resolution.

## Planned next steps (v4 repositioning)

1. **Stop** treating the weak/operator branch and the pointwise
   first-barrier branch as *direct routes to the conjecture*. By the v4
   results, further finite refinement (more `T`, `j`, cylinders, suffixes)
   cannot cross the divergence barrier *by these routes*. The weak branch
   may continue only as a separate, honestly labeled
   operator-approximation study.
2. **Redirect** mathematical effort to the cycle half, the only half where
   partial theorems and tools (linear forms in logarithms; continued
   fractions of `log₂3`; computation) genuinely bite. The realistic,
   finishable target is the **structural layer in Lean** (cycle equation,
   the `A/L ≈ log₂3` condition, elementary exclusions, the link to
   verification). Note the limit: a usable form of Baker’s theorem is, to
   our knowledge, not in Mathlib, so the deep analytic exclusions are not
   cheaply formalizable.
3. **Consolidate** the verified assets (the v4 paper).
4. **Continue** the methodology study of AI-assisted mathematics,
   including the program’s capacity to recognize and *prove* its own
   ceiling.

## Repository structure

```
.
├── paper/                       Paper sources (v1–v4) + PDFs
├── lean/                        Lean 4 + Mathlib formalization
│   └── CollatzShadowing/
│       ├── Basic, Phantom, Syracuse2Adic, Auxiliary
│       ├── Shadowing.lean       Exact shadowing (sorry-free)
│       ├── NoInfinite.lean      No-infinite-shadowing + expanding-cycle (sorry-free)
│       ├── EpisodeGraph, Operator, Bound   Finite operator / CW layer
│       ├── WeakBridge.lean      A0 weak-bridge finite lemmas
│       ├── CollatzBridge.lean   Conditional descent / first-barrier bridge
│       └── Generated/           Machine-generated finite certificates
├── scripts/
│   ├── spectral_program/        Spectral + Phase-10 frontier (→126)
│   ├── phantom_taxonomy/        Taxonomy, SCC, deterministic certificates
│   └── early_empirical/         Legacy quasi-Lyapunov work
├── notes/                       Working notes, decision logs, repro manifest
├── README.md
├── METHODOLOGY.md
└── LICENSE                      CC BY 4.0
```

## Methodology and AI disclosure

The author leads the research direction, conceptual framing, and strategic
choices. The technical work — Python implementation, the Lean 4
formalization, and the manuscripts — is developed in iterative
collaboration with LLM assistants (OpenAI Codex and Google Gemini for the
early empirical scripts; Anthropic’s Claude for the spectral program, the
Lean verification, and drafting), using **cross-AI checking** (alternating
Claude and Codex) for the formalization. v4 itself is a product of that
process: the cross-AI loop converged on a precise *negative* result about
the program’s own approach — which we regard as a positive methodological
finding, distinct from progress on the mathematics. The work has not been
reviewed by a human mathematical expert; expert scrutiny is explicitly
invited. See [`METHODOLOGY.md`](METHODOLOGY.md).

## Citation

```bibtex
@misc{borgatta2026collatz_v5,
  author    = {Borgatta, Piero},
  title     = {Cross-AI, Lean-Verified Mathematics:
               A Case Study on the Collatz Conjecture},
  year      = {2026},
  version   = {5.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20554750},
  url       = {https://doi.org/10.5281/zenodo.20554750},
  note      = {Source and Lean 4 formalization:
               \url{https://github.com/PieroBorgatta/Collatz}.
               Concept DOI: \url{https://doi.org/10.5281/zenodo.20021537}}
}
```

## License

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

## Contact

Piero Borgatta — Independent Researcher · `info@pieroborgatta.com` ·
ORCID [0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405)

Constructive feedback from researchers in symbolic dynamics, `p`-adic
dynamical systems, transfer-operator theory, and Diophantine approximation
is explicitly welcome.
