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
the target without an unknown cycle-height bound. A further verified construction
uses compact seeds and preserves the sixth-power mixing decay. Its coefficient
is strictly larger and its cutoff strictly smaller than the previous uniform
two-seed formulas. All 399 local modules and three dependency audits passed in
[CI 36009718722](https://github.com/PieroBorgatta/Collatz/actions/runs/36009718722).
This replay is separate from the main-library build and reuses checked compiled
receipts and pinned external package objects; the
[optimization report](notes/post_v6_optimization_2026-09-24/RESULTS_IT.md) records
the theorem statements, comparisons, and preserved evidence. A
[short mathematical note](notes/compact_seeds_sixth_power_note_2026-09-24.md)
isolates the two quantitative improvements and their external assumptions.
A further main-library development transports the cancellation-tower parameter
through its exit and following growth burst. For each fixed v≥1, every finite
suffix with first exponent at least two and remaining exponents positive is
realized by exactly one odd parameter class modulo `2^(sum exponents)`.
The phase-C theorem connects this to actual orbits from the original tower
sources and provides arbitrarily large positive parameters. A separate
bounded-parameter criterion retains the least residue and the real parameter
limit. The aggregate build (3,374 jobs) and the strict eleven-root dependency audit
passed in [CI 36015103652](https://github.com/PieroBorgatta/Collatz/actions/runs/36015103652).
Only the three standard axioms occur in the new roots. See the
[transport report](notes/post_v6_transport_2026-09-24/RESULTS_IT.md) for exact
quantifiers, the obstruction to finite-pattern exclusions, and reproduction.
This finite-suffix theorem does not construct an infinite positive orbit or
prove a descending return to the marked section. The earlier
[parameter note](notes/post_v6_parameter_2026-09-24/IDEAS_IT.md) remains a dated
snapshot; its phase-A formulas have not been formalized by this continuation.

The next [descent study](notes/post_v6_descent_2026-09-24/RESULTS_IT.md) checks
all 4,096 odd parameters q≤8191 in the v=1 family and 34 additional parameters.
All return from the burst endpoint below their original source; the largest
observed extra-step ratio is 24/11, which disproves the proposed bound 2q.
A paper proof shows that a fixed descending suffix can work for at most one
parameter, its least positive residue. This is a necessary condition, not
a uniform descent theorem; no new Lean declaration or mathematical priority
is claimed. The report also identifies Andrei–Kudlek–Niculescu (2000) as prior
art for the repeated [1,2] compression and distinguishes the existing
literature from this family's specific experiment.
The full experiment and separate arithmetic replay passed in
[CI 36019056755](https://github.com/PieroBorgatta/Collatz/actions/runs/36019056755)
with byte-identical results; the existing Lean build and audits also passed.

The subsequent [level study](notes/post_v6_levels_2026-09-24/RESULTS_IT.md)
examines q=2^(v−1)−1 and Q_v=(9^(2^v)−1)/2^(v+3). It proves at paper
level that two levels share exactly those initial exponent words whose
sum is at most v+1; these shared prefixes cannot reach below the original
source. Using Mahler's classical transcendence theorem, it also shows that
the residual stopping times tend to infinity as v increases, allowing
infinite values: this does not prove that any individual orbit diverges.
The exact experiment checks 512 modular pairs and 14 full integer orbits
(213,894 residual steps), all of which descend after their shared prefixes.
Thirteen cases overlap the previous experiment. No infinite-family descent,
new Lean declaration, or mathematical priority is claimed.
The full level experiment passed in
[CI 36023967396](https://github.com/PieroBorgatta/Collatz/actions/runs/36023967396)
with both result files byte-identical.

The [modular certificate study](notes/post_v6_certificates_2026-09-24/RESULTS_IT.md)
then gives a sufficient parity-count criterion for descent below the original
source. It certifies every level v=5,…,21 using residues only; a separate
recurrence/Syracuse implementation replays all 20 attempts. The cases
v=19,20,21 extend the previous range with certified upper bounds, not exact
stopping times. A separate application of Chim's 2025 theorem on two p-adic
logarithms, together with 32 finite modular checks, proves at paper level
that the first differing step of adjacent levels also stays above their
respective sources. The uniform parity-count bound remains open. These
proofs are not Lean declarations, and no mathematical priority is claimed.
The full experiment and independent replay passed in
[CI 36027655913](https://github.com/PieroBorgatta/Collatz/actions/runs/36027655913),
with three byte-identical result files; the existing Lean build and audits
also passed on the same code commit.

The [conditional transfer study](notes/post_v6_induction_2026-09-25/RESULTS_IT.md)
formalizes the general sufficient descent certificate and a quadratic
transfer criterion in `DescentCertificate.lean` and `QuadraticTransfer.lean`.
The transfer requires an explicit relative-weight bound on the upper orbit;
that bound is not proved uniformly. A retrospective exact experiment retains
all 52 attempts on 13 adjacent pairs: the simple timing rules `2t_v`,
`2t_v+3v`, and `2t_v+v²` fail to cover the observed family. A compatible
counterexample also rules out invariance of the proposed coefficient cone
under its generic hypotheses. These results do not close the induction,
and the Lean declarations are not claims of new mathematical discoveries.
The [full Lean build and strict audit](https://github.com/PieroBorgatta/Collatz/actions/runs/36118390826)
and the [exact experimental replay](https://github.com/PieroBorgatta/Collatz/actions/runs/36118390748)
passed on commit `8be3116`; the downloaded result file is byte-identical.

The [bounded-loss compensation study](notes/post_v6_compensation_2026-09-25/RESULTS_IT.md)
then freezes a stronger working hypothesis before evaluating levels 22–24:
every downward excursion of `305r−589J(r)` is at most `128v²` for v≥15.
All three held-out levels pass. Independent Python and C/GMP implementations
agree on the full parity trace hashes and every extremum, extending the
finite descent certificates through v24. The hypothesis remains unproved.
A separate argument shows why a proof retaining only an initial residue
and a coarse height interval must preserve almost all available bits;
this limits that abstraction, not proofs using the exact tower arithmetic.
The published freeze, complete data, and verification procedure are in the report.
The [full experiment and independent replay](https://github.com/PieroBorgatta/Collatz/actions/runs/36122256203)
passed on commit `df44e7f`, with four byte-identical downloaded result files;
the existing Lean build and audits also passed.

The [arithmetic word study](notes/post_v6_arithmetic_2026-09-25/RESULTS_IT.md)
preserves the complete prefix when translating a bad block into a tower
congruence. It proves at paper level that the existing explicit Chim
specialization cannot exclude positive-loss blocks in this full-word
encoding: its upper bound always exceeds the required modulus exponent
by a factor greater than 36 million. A signed alternative leaves possible
cancellations open. Exact checks reproduce the three previously held-out
levels. High-complexity admissible words show that parity density alone
does not force low complexity of the parity word. A bridge to recent
digital-complexity results for powers of 3 remains unproved. These words
are not counterexamples from the distinguished tower.
The compensation hypothesis remains open; no Lean declaration or claim
of mathematical priority is added. A targeted literature review and an
unsent specialist-review note accompany the results.
The [arithmetic replay](https://github.com/PieroBorgatta/Collatz/actions/runs/36125838578)
and [existing Lean build and audits](https://github.com/PieroBorgatta/Collatz/actions/runs/36125838530)
passed on commit `5f452f2`; the downloaded arithmetic result is byte-identical.

The [global margin study](notes/post_v6_margin_2026-09-25/RESULTS_IT.md)
then reduces the terminal parity-count target to an exact weighted budget
of errors between consecutive levels. A specified square-root-scale error
bound would propagate the verified positive margin from level 16, but that
bound remains unproved and was selected retrospectively. The study also
proves why the quadratic relation and a complete lower parity certificate
alone cannot imply such a bound: generic positive integer lifts can keep
that certificate and the high bits while violating the upper budget.
These are not counterexamples from Q_v. All existing levels 5–24 are
replayed, with six explicit quadratic adversaries; no new tower level,
Lean declaration, or mathematical priority is claimed.

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
