# Phantom Orbit Shadowing for the Collatz Conjecture

[![DOI (latest)](https://img.shields.io/badge/DOI%20(latest)-10.5281%2Fzenodo.20021537-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.20021537)
[![DOI (v6)](https://img.shields.io/badge/DOI%20(v6)-10.5281%2Fzenodo.22936057-1682d4?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.22936057)
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

> **This is not a proof of the Collatz conjecture.** The working tree now
> includes results produced after the published v1–v6 papers. Published v6
> corrects the accelerated 2-adic continuity claim made in v4 and
> records the precise limit of its coding argument.

> **About this project.** A personal research program by an independent
> researcher exploring whether iterative collaboration with large language
> model (LLM) assistants can support non-standard attempts at open
> problems. Verifying the practical limits of that collaboration is an
> explicit secondary goal. See [`METHODOLOGY.md`](METHODOLOGY.md).

## Paper

The latest published version is **v6**, published on 24 September 2026 at
[doi:10.5281/zenodo.22936057](https://doi.org/10.5281/zenodo.22936057).
The v1–v6 PDFs are immutable Zenodo snapshots; their checksums are fixed in
[`scripts/published_pdf_checksums.json`](scripts/published_pdf_checksums.json)
and checked by
[`scripts/check_published_pdfs.py`](scripts/check_published_pdfs.py).
The v6 manuscript ([TeX](paper/collatz_spectral_reduction_v6.tex),
[local PDF](paper/collatz_spectral_reduction_v6.pdf)) contains the
mathematical continuation and an explicit erratum to v4. Its PDF and
supplementary archive have been verified against the published record.
Further working-tree developments are post-v6 and are not part of that archive.

| Version | Framing | LaTeX | Publication |
|---|---|---|---|
| **v6 (latest published)** | Exact cylinders, precision budgets, singularity and v4 erratum | [`paper/collatz_spectral_reduction_v6.tex`](paper/collatz_spectral_reduction_v6.tex) | [Zenodo doi:10.5281/zenodo.22936057](https://doi.org/10.5281/zenodo.22936057) |
| v5 | Methodology retrospective; verified core + Reservoir library | [`paper/collatz_spectral_reduction_v5.tex`](paper/collatz_spectral_reduction_v5.tex) | [Zenodo doi:10.5281/zenodo.20554750](https://doi.org/10.5281/zenodo.20554750) |
| v4 | Verified core, two barriers, repositioning | [`paper/collatz_spectral_reduction_v4.tex`](paper/collatz_spectral_reduction_v4.tex) | [Zenodo doi:10.5281/zenodo.20544464](https://doi.org/10.5281/zenodo.20544464) |
| v3 | Conditional spectral reduction + taxonomy + extended Lean | [`paper/collatz_spectral_reduction_v3.tex`](paper/collatz_spectral_reduction_v3.tex) | [Zenodo doi:10.5281/zenodo.20160154](https://doi.org/10.5281/zenodo.20160154) |
| v2 | Lean shadowing core + Chang comparison | [`paper/collatz_spectral_reduction_v2.tex`](paper/collatz_spectral_reduction_v2.tex) | [Zenodo doi:10.5281/zenodo.20098868](https://doi.org/10.5281/zenodo.20098868) |
| v1 (archival) | Original spectral program | [`paper/collatz_spectral_reduction.tex`](paper/collatz_spectral_reduction.tex) | [Zenodo doi:10.5281/zenodo.20021538](https://doi.org/10.5281/zenodo.20021538) |

Concept DOI (all versions):
[10.5281/zenodo.20021537](https://doi.org/10.5281/zenodo.20021537).

## Published v4 and the v6 correction

**The conjecture splits into two genuinely distinct hard halves, behind
two different walls:**

- **No divergent orbits.** Barrier: *distributional-to-pointwise*.
  [Tao's 2022 theorem](https://arxiv.org/abs/1909.03562) gives
  almost-bounded values for almost all starts in logarithmic density;
  [Inselmann's 2024 preprint](https://arxiv.org/abs/2402.03276v3)
  gives subpower descent for almost all starts in natural density.
  Neither establishes every-`n` descent. The weak/operator branch here
  yields finite averaged information; the first-barrier branch still has
  open pointwise hypotheses.
- **No nontrivial cycles.** Barrier: *Diophantine approximation of
  `log₂3`*. Partial exclusions exist. In particular,
  [Hercher (2023)](https://arxiv.org/abs/2201.00406) excludes nontrivial
  cycles with at most 91 local minima; this is a bound on that specific
  cycle statistic. [Barina's project](https://pcbarina.fit.vut.cz/) reports
  exhaustive convergence verification below `2^71` on 15 January 2025
  and below `2075 × 2^60` on 24 September 2026. These are finite bounds;
  the global cycle question remains open. The dated source review is in
  [`notes/collatz_literature_audit_2026-09-24.md`](notes/collatz_literature_audit_2026-09-24.md).

**What published v6 establishes or corrects:**

- For **all** infinite positive-exponent words, the assertion that a
  **non-eventually-periodic** word cannot represent a positive integer is
  equivalent to the no-unbounded-orbit problem. Here eventual periodicity
  permits a finite prefix before the repeating tail; for example, `3`
  has exponent word `1,4,2,2,…`. A bounded positive orbit gives an
  eventually periodic word. Conversely, a repeated tail block is either
  expansive, excluded for positive integers by the precision budget, or
  contracting, so its affine block iteration is bounded. This paper-level
  observation does not establish the assertion,
  nor does it cover a selected subclass of such words.
- The accelerated 2-adic map is discontinuous at `−1/3`; v4's global
  continuity and conjugacy claim was false. Infinite words
  of positive exponents are used only on the invariant domain where every
  accelerated step is defined and stays odd. A later Lean theorem gives
  positive odd inputs arbitrarily close in finite 2-adic precision to the
  singular point whose accelerated outputs remain `1` and `7`.
- A nonempty positive-exponent word is matched exactly when its affine
  numerator equals `2^A` modulo `2^(A+1)`; repeated blocks have the
  corresponding modulus `2^(kA+1)`. This is checked in
  `ExactCylinders.lean`; the single residue class and density are
  paper-level corollaries. [Ross's 2026 Zenodo v3](https://doi.org/10.5281/zenodo.22181823)
  already states the mathematical one-class result, so v6 claims local
  formal integration.
- A **new Lean-checked fact**: no positive integer lies on an expanding
  cycle (post-prefix congruence form,
  `no_positive_endpoint_eventually_periodic_expansive_congruence`),
  generalizing the no-infinite-shadowing corollary.
- The first-barrier Lean theorem requires both
  `A0FirstBarrierExistsAll` and `A0FirstBarrierThresholdAutomatic` as open
  hypotheses, and concludes only for the A0 family.

## Lean 4 formalization

The Lake project pins Lean v4.29.1 and Mathlib v4.29.1; portability to a
newer toolchain has not been checked. The `CollatzShadowing` sources are
`sorry`-, `admit`- and project-declared-`axiom`-free. Some proofs use
`native_decide`, so this source scan alone is not a kernel-only trust audit.

| Result | Lean declaration | File |
|---|---|---|
| Exact shadowing (Lemma 3.1) | `exact_shadowing`, `exact_shadowing_periods` | [`Shadowing.lean`](lean/CollatzShadowing/Shadowing.lean) |
| No infinite (periodic) shadowing (Cor. 3.4) | `no_infinite_period_congruence_expansive` | [`NoInfinite.lean`](lean/CollatzShadowing/NoInfinite.lean) |
| No integer on an expanding cycle (post-prefix form) — **new** | `no_positive_endpoint_eventually_periodic_expansive_congruence` | [`NoInfinite.lean`](lean/CollatzShadowing/NoInfinite.lean) |
| Distinct accelerated outputs at every precision near the singular point | `singular_outputs_separated_at_every_precision` | [`SyracuseSingularity.lean`](lean/CollatzShadowing/SyracuseSingularity.lean) |
| Exact cylinder for a nonempty positive-exponent word (full library build passed) | `syracuseWordMatches_iff_exactResidue`, `repeatPhantomWord_matches_iff_exactResidue` | [`ExactCylinders.lean`](lean/CollatzShadowing/ExactCylinders.lean) |
| Single-node CW spectral bound `ρ ≤ 97/2000` | `t10j32HighBitTailSpectralRadiusBound_97_2000` | [`Generated/T10J32HighBitTailCW.lean`](lean/CollatzShadowing/Generated/T10J32HighBitTailCW.lean) |
| Deterministic `(K,b)` CW bound `ρ ≤ 3/4` (`K₀=16`) | `k16s16KDeterministicGeneratedSpectralRadiusBound` | [`Generated/K16S16KDeterministicCW.lean`](lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean) |
| Generic weighted Collatz–Wielandt bound | `spectralRadius_le_of_finiteCWCertificate` | [`Bound.lean`](lean/CollatzShadowing/Bound.lean) |
| Finite weak row-`L¹` bridge | `WeakBridge.weighted_action_diff_le` | [`WeakBridge.lean`](lean/CollatzShadowing/WeakBridge.lean) |
| Exact high-`ν₂` source-tail mass `≤ 2⁻ᴿ` | `WeakBridge.TailCount.dyadic_tail_count_mul_le`, `dyadic_tail_mass_le` | [`WeakBridge.lean`](lean/CollatzShadowing/WeakBridge.lean) |
| Bit-length / `δ`-boundary period estimate | `WeakBridge.BitLength.biAffineDelta_dyadicWeight_period_boundary_le` | [`WeakBridge.lean`](lean/CollatzShadowing/WeakBridge.lean) |
| Descent bridge (elementary): descent ⇒ Collatz | `classicalCollatz_of_uniformStrictDescent_provedBridge` | [`CollatzBridge.lean`](lean/CollatzShadowing/CollatzBridge.lean) |
| Conditional cylinder descent (first-barrier) | `A0EndpointSuffixExitAll_of_firstBarrier` | [`CollatzBridge.lean`](lean/CollatzShadowing/CollatzBridge.lean) |
| Matched expansive word loses exact 2-adic precision | `syracuseWordPhantomPrecision_after_eval_add_sum` | [`PrecisionTax.lean`](lean/CollatzShadowing/PrecisionTax.lean) |
| Necessary equation and contractivity for positive cycles | `syracuseWordCycleEquationNat`, `syracuseWordCycleContracting` | [`CycleConstraints.lean`](lean/CollatzShadowing/CycleConstraints.lean) |

Supporting modules: `Basic`, `Phantom`, `Syracuse2Adic`,
`SyracuseSingularity`, `Auxiliary`
(shadowing infrastructure); `EpisodeGraph`, `Operator`, `Bound`
(finite episode-graph / transfer-operator / Collatz–Wielandt layer);
`A0InfiniteSubfamily`, `PrecisionTax`, `PrecisionTemplates`,
`SwitchingPrecision`, `AffineTraceGraph`, `ThreeTraceObstruction`,
`CycleConstraints`, `ExactCylinders`, and `FirstBarrier` (later arithmetic and trace work);
`Generated/*` (machine-generated finite certificates). Current result map:
[`lean/CollatzShadowing/THEOREM_INDEX.md`](lean/CollatzShadowing/THEOREM_INDEX.md).
Earlier API inventory in
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
- [`lean/scripts/phantom_taxonomy/switching_defect_probe.py`](lean/scripts/phantom_taxonomy/switching_defect_probe.py)
  — finite diagnostic of affine switching defects and cancellation
  towers; it is experimental and supplies no global proof.

## Relation to concurrent work

The most directly related concurrent work is **Chang (2026)**,
*Exploring Collatz Dynamics with Human–LLM Collaboration*
([arXiv:2603.11066](https://arxiv.org/abs/2603.11066)); the current arXiv
v6 was updated on 2026-04-22. Chang reports a much broader human–LLM
structural survey: 29 paradigms, 630 formal results, and large-scale
computation, while explicitly not claiming a proof of Collatz.

The overlap is real: Chang independently uses 2-adic *phantom cycles* and
identifies the same distributional-to-pointwise gap that v4 locates inside
this program’s own objects. The distinction is the output geometry. Chang is
broad and survey-like, with rich methodology/error-correction logs; this
repository is narrower but has a `sorry`-free Lean 4 core and exact finite
certificates. The two programs are best read as complementary evidence about
the same obstruction, not as competing proof claims.

## Current direction

The post-v6 continuation develops a six-progression arithmetic section,
an explicit shortcut stopping rank for the classical sufficient residue
`20 mod 27`, and universal formulas for cancellation towers. It includes
an infinite family of descending section returns, an increasing first
return, and marked sources with arbitrarily long no-descent prefixes.
Within that approach, the remaining objective is a rank controlling eventual returns
to the section; coverage itself does not provide descent. The detailed
development and verification record are in
[`notes/post_v6_section_2026-09-24/RESULTS_IT.md`](notes/post_v6_section_2026-09-24/RESULTS_IT.md).

A further direction controls repeated visits by their affine weights:
`WeightedVisits.sum_weight_visits_le` bounds the total weight of any
finite set of visits from x to R by `R*(3*R+1)/x`, without excluding
periodic targets. Three subsequent Lean modules transfer the bound to
exact exponent words, group repeated sources, and prove a lower bound
on the number of distinct ordinary Collatz predecessors. The resulting
finite counting theorem explicitly assumes the analytic mass estimate;
it is not an unconditional density theorem. The separate overlay below
connects this bound to the pinned external analytic library. Independent
mathematical review of that full analytic argument remains open.
See [the counting report](notes/post_v6_counting_2026-09-24/RESULTS_IT.md).

A separate [predecessor adapter](research/weighted_predecessors_adapter/README.md)
ports the weighted argument to the exact external path types and proves a
second route using two bounded candidate seeds, giving constants uniform in
the target without an unknown cycle-height bound. All 395 local modules and
both final dependency audits passed in
[CI 36005012141](https://github.com/PieroBorgatta/Collatz/actions/runs/36005012141).
This replay is separate from the main-library build and reuses authenticated
compiled receipts and pinned external package objects; the
[continuation report](notes/post_v6_adapter_2026-09-24/RESULTS_IT.md) records
the exact verification boundary and preserved evidence.
Separately, exact parameter
formulas describe a second growth burst after the cancellation towers
and classify the following valuation by lifted residue roots; those
formulas remain paper-level results with exact finite checks.
See [the research note](notes/post_v6_parameter_2026-09-24/IDEAS_IT.md)
for proofs, experiments, and the open conditions on both applications.

The earlier Lean modules add exact finite exponent cylinders and a local
precision budget for repeated expansive words, compatible label-switch
identities, counterexamples to
naive global rankings, and necessary constraints on positive cycles. A
single odd residue class and its density follow from the exact cylinder
theorem at paper level; those corollaries are not yet Lean declarations. A
paper-level cancellation family in v6 shows why a constant affine
switching defect alone does not bound the next precision counter. A
proof of Collatz still requires a pointwise argument covering every
positive odd starting value. The current status and proposed research
tests are recorded in [`lean/STATUS.md`](lean/STATUS.md).

## Repository structure

```
.
├── paper/                       Published v1–v6 PDFs/sources
├── lean/                        Lean 4 + Mathlib formalization
│   └── CollatzShadowing/
│       ├── Basic, Phantom, Syracuse2Adic, Auxiliary
│       ├── SyracuseSingularity.lean  Arithmetic witness near the 2-adic singular point
│       ├── Shadowing.lean       Exact shadowing (sorry-free)
│       ├── NoInfinite.lean      No-infinite-shadowing + expanding-cycle (sorry-free)
│       ├── EpisodeGraph, Operator, Bound   Finite operator / CW layer
│       ├── WeakBridge.lean      A0 weak-bridge finite lemmas
│       ├── CollatzBridge.lean   Conditional descent / first-barrier bridge
│       ├── PrecisionTax, SwitchingPrecision, ThreeTraceObstruction
│       ├── CycleConstraints, ExactCylinders, FirstBarrier, A0InfiniteSubfamily
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
choices. The technical work is developed through a multi-AI workflow:
Google Gemini for broad exploratory ideas; Claude Code Opus 4.7/4.8 for
validation, refinement, pruning, proof planning, and drafting; OpenAI Codex
for repository operations, Python, Lean, scripts, builds, TODOs, Markdown,
and patching; and aider-desk connected to DeepSeek v4 Flash API as an
external-opinion channel whose critiques were fed back into Claude Code
before further Codex implementation. Lean 4 + Mathlib is the arbiter for
formal claims: cross-AI agreement is useful, but a proof counts only when
the project builds without source-level `sorry`, `admit`, or user-declared
`axiom`. Some finite proofs use `native_decide`, so their trusted base
includes the native compiler; see [`lean/STATUS.md`](lean/STATUS.md) for
the axioms and toolchain audit.

v4/v5 are published products of that process. Published v6 states
the correction to the global accelerated coding claim in v4 and delimits
the resulting paper-level observation. It makes no universal impossibility
claim about other methods.
The work has not been reviewed by a human mathematical expert; expert
scrutiny is explicitly invited. See [`METHODOLOGY.md`](METHODOLOGY.md).

## Citation

```bibtex
@misc{borgatta2026collatz_v6,
  author    = {Borgatta, Piero},
  title     = {Exact Exponent Cylinders, Precision Budgets,
               and Singular Coding in Accelerated Syracuse Dynamics},
  year      = {2026},
  version   = {6.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22936057},
  url       = {https://doi.org/10.5281/zenodo.22936057},
  note      = {Source and Lean 4 formalization:
               \url{https://github.com/PieroBorgatta/Collatz}.
               Concept DOI: \url{https://doi.org/10.5281/zenodo.20021537}}
}
```

## License

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
The separate `research/weighted_predecessors_adapter/` package is Apache-2.0;
its license and `UPSTREAM_NOTICE` preserve attribution to Lech Mazur and the
external baseline authors.

## Contact

Piero Borgatta — Independent Researcher · `info@pieroborgatta.com` ·
ORCID [0009-0001-8025-2405](https://orcid.org/0009-0001-8025-2405)

Constructive feedback from researchers in symbolic dynamics, `p`-adic
dynamical systems, transfer-operator theory, and Diophantine approximation
is explicitly welcome.
