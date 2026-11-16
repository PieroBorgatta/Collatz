# V7 finite-core evidence and semantic audit

Prepared 16 November 2026 by the finite-core subagent for the v7 release.
This is a static source/receipt review, not a new Lean execution. The root
agent owns final compilation, verification and publication.

## Deliverable and scope

`paper/v7_sections/finite_core.tex` is a self-contained mathematical section
covering the finite reciprocal bound, first-arrival product and recoding
height, repeated-visit quadratic occupation, bounded-slope catalogues,
finite-horizon localization and the direction of collision certificates.
All arithmetic domains and nonreturn/first-arrival/source-injectivity
guards are stated. No density theorem, atom-floor estimate, canonical
trace, random law, or mixing theorem is a premise of the finite proofs.

The research-and-citations subagent completed a full mathematical and
scope cross-review of the finite-core section: PASS. The finite-core
subagent independently reviewed `paired_paths.tex` and the main paper's
preserved-prefix, fixed-total routing, tower and conditional off-path
arguments: PASS after the paired-path section explicitly allowed a
contraction charge to terminate at time zero. In particular, the main
conditional bound correctly needs two nonperiodic antichain budgets
and at most one periodic exceptional seed when the observed path first
enters a cycle. These reviews are shared-context AI reviews, not
independent human refereeing or new formal verification.

The section uses only ordinary AMS mathematical environments plus the
v6-style declaration-breaking macro `\ttbr` (package `seqsplit`). Its
citation keys are `terras1976`, `lagarias2003`, `valbuena2026`,
`curry2026` and `weaver9v1`.

## Exact declaration map

All declarations below have the prefix `CollatzShadowing.`. The displayed
paper statements sometimes restrict the implementation's larger natural
number domain to positive odd states. Such a restriction weakens the
statement; it is not a hidden assumption in the Lean sources.

| Paper item | Source file / exact declaration | Semantic scope |
|---|---|---|
| Reciprocal budget `133547/1655 < 81` | `OrbitReciprocal.finite_orbit_reciprocal_sum_le`; `finite_orbit_reciprocal_sum_real_lt_eighty_one` | Finite injective shortcut segment, positive initial state; no statement about later dynamics. |
| Parity moment | `OrbitReciprocal.parity_moment` | Exact polynomial moment over all `2^N` residue representatives, including auxiliary representative zero. |
| Terminal deletion in dyadic counting | `OrbitReciprocal.finite_orbit_dyadic_card_bound`; infrastructure in `FiniteOrbitTransfer` | The `N`-step image is injective only after removing the last `N` time indices. |
| First-arrival transfer | `FirstArrivalBudget.first_arrival_injective`; `shortcut_clock`; `accelerated_first_is_shortcut_first`; `first_arrival_reciprocal_sum_lt_eighty_one` | Odd first arrival is a shortcut first arrival at its exact exponent-sum clock. |
| Product identity | `WordProductEnvelope.inflation_eq_product`; `exact_word_inflation` | All existing positive trajectories, including repeated visits. |
| Product exponential upper | `WordProductEnvelope.inflation_le_exp_of_reciprocal_budget` | Reciprocal budget is explicit; the universal `exp(27)` specialization uses the first-arrival transfer. |
| Existing recoding height | `WordProductEnvelope.comparable_slope_height`; `FirstArrivalBudget.first_arrival_same_profile_height`; `canonical_first_arrival_profile_height` | Image existence is an input. A new word's length and total may change if the cross-multiplied slope condition is preserved. |
| Quadratic loss | `QuadraticOccupation.potential_sq_sub_succ`; `sum_squareLoss_finset_le` | Positive source; repeated visits allowed; exact loss telescopes. |
| Repeated target visits | `QuadraticOccupation.sum_weight_sq_visits_le`; `sum_wordWeight_sq_fiber_le` | Budget `V(n)/u^2`; distinct words from one source have distinct lengths. |
| All-source finite square catalogue | `QuadraticOccupation.tilted_catalogue_le` | Upper `2V(n)`, no source injectivity, no depth or nonreturn assumption. |
| Simpler square catalogue | `IntegerAtomTilt.tilted_integer_atom_le`; `tilted_nonreturn_catalogue_le` | Upper `2n^2`: fixed-depth or nonreturn hypotheses respectively supply source injectivity. |
| Bounded-slope catalogue | `BoundedSlopeCatalogue.subcatalogue_card_le`; `catalogue_finite`; `catalogue_ncard_le`; `catalogue_parameter_bounds`; `catalogue_source_bound` | Rational `R>0`, gain at least `1/R`; cycles allowed. Cardinality and source bound explicit; time/total bounds only existential in this proof. |
| Horizon and tail | `FiniteHorizonBudget.iterate_shifted_growth`; `source_lower_of_horizon`; `reciprocal_square_tail`; `tilted_tail_catalogue`; `tilted_fixed_depth_tail`; `tilted_nonreturn_horizon` | Tail `2/R`; source injectivity cannot be silently dropped for all depths on cycles. |
| Collision upper | `SpineDispersion.collision_spine_budget` | Finite distinguished mass `R_i/R_(i+1)`, positive floor and monotone sequence. |
| Collision lower certificates | `SpineDispersion.collision_defect_ge_of_two_branches`; `collision_defect_ge_lower_allocations` | Existence of actual branch lower masses remains an input. Truncation alone has the opposite inequality direction. |

## Mathematical proof checks

The reciprocal proof in the paper reproduces the actual local argument:

1. Exact lift and moment over all binary parity representatives.
2. At fixed odd count `m`, reduced endpoints lie below `2*3^m`.
3. Light classes cost less than `3^M`; heavy classes cost at most
   `(5/2)^N*(2/3)^M`.
4. Restoring the last `N` temporal points adds `N/2^N` to a normalized
   dyadic band, with `M=floor(3N/5)`.
5. The five-step envelope ratios are `3125/3456` and `27/32`.
6. Their total budgets are `19626/331` and `102/5`, while terminal
   deletion costs at most two. The band containing only the possible
   state one saves one unit, giving exactly `133547/1655`.

For first arrivals, the product is written `mathcal P_k`; the universal
constant is `P_0=exp(27)`, avoiding a collision with the empty product.
The recoding argument needs only the original path's first-arrival upper
and the new path's nonnegative affine constant. It does not require the
new path to be a first arrival, and it does not prove that path exists.

The repeated-visit bound follows from

`phi_k^2 - phi_(k+1)^2 = Omega_k^2*(6*x_k+1)/(x_k^2*(3*x_k+1)^2)`.

Grouping by source is essential; treating repeated visits as distinct
source labels would not justify the smaller `2n^2` bound on a cycle.

For collision defects, adding omitted squared masses decreases the
defect. Thus a computed partial defect is an upper bound on the full
defect. Two actual branch lower masses do supply a lower certificate,
because the same argument applies to every finite extension before a
justified limit; normalized sample frequencies do not supply those
actual masses.

## Source-bound historical verification

The seven-module receipt is
`notes/research_sprint_2026-11-15/verification/integration_receipt.json`
(136 audited compiled declarations, 14 encoded-private helpers). The
four-module receipt is
`notes/research_sprint_2026-11-15_three_hours/verification/integration_receipt.json`
(68 audited compiled declarations, five encoded-private helpers, full
incremental build reported as 3404 jobs). Their allowed transitive axioms
are exactly `propext`, `Classical.choice`, `Quot.sound`.

The later receipt matches every listed current source hash, including
`lean/CollatzShadowing.lean`. The earlier receipt's selected seven module
hashes still match, but its old main entrypoint hash does not: four imports
were intentionally added later. Therefore the entire earlier source
snapshot must not be called byte-identical to the current tree.

The separate Ubuntu checkpoint receipt is
`notes/research_sprint_2026-11-15_three_hours/verification/checkpoint_ci_receipt.json`,
run `43777436364` at commit `b20698f854b72e8bbeba0aa9d7c89ad351422dae`.
It explicitly distinguishes cross-platform replay from an independent
kernel implementation. Its audit output and twelve finite arithmetic
outputs were byte-identical to the corresponding local evidence.

These are historical checks on Lean/Mathlib `v4.29.1`; they are not new
executions in this subtask. Final release verification belongs to root.

## Current source hashes reviewed

| File in `lean/CollatzShadowing/` | SHA-256 |
|---|---|
| `OrbitReciprocal.lean` | `750ee15525eea3dd9f7ea7cb1a90a9d07425680555949e322251a073c24875e0` |
| `FiniteOrbitTransfer.lean` | `c66576be359bd599eb56b46872b8d82adff9fa50c18ed15f777f069713660507` |
| `FirstArrivalBudget.lean` | `cb9230c960720263a30f910e4acb51101bd3639b7736bbf122a23343db1789c7` |
| `WordProductEnvelope.lean` | `85b5ad253999ac5f6786f203b114511a9418cf6757c02fae69c509d3de4a355b` |
| `IntegerAtomTilt.lean` | `39320f3fd4f45feafce25c7b0fac7fb4d3c1c9562368c9ccc5072b3151d1b701` |
| `FiniteHorizonBudget.lean` | `acddcaf114d5a8dff1d118df3fa88f00ab4956e38f987c45e7f5f347bb2dc9a5` |
| `QuadraticOccupation.lean` | `5af51a6b1a263905d324a2f76b9aea3e11b22843c3e293d664ad1d6fc2f0c935` |
| `BoundedSlopeCatalogue.lean` | `a3581a63341dadb22967c745825451410534756e2d69f7e1fc81659e72b1eafb` |
| `SpineDispersion.lean` | `79af91e4b456506c4bb5f9a276d70c3989b54a25178c9a79889e348ba0add0b3` |

## Attribution and primary-source checks

The version-bound Valbuena source at commit
`a7275d5a73814d3d9a400c6fe6577de9542b03a3` was read directly at
https://raw.githubusercontent.com/x1xhlol/collatz-two-coordinate-obstruction/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/tao-basin-densities.tex.
Its Section 2, *Uniform control of finite distinct trajectories*,
Lemma `ct-packing`, explicitly proves a uniform reciprocal tail and
uniform correction-product bound for every finite distinct shortcut
trajectory. Thus neither principle is claimed as new here. The local
contribution is the exact parity-moment derivation, the concrete
constant `133547/1655`, and integration into the checked finite core.
The prior method uses an entropy packing recurrence and strong induction.

The antecedent separation by odd-step count is acknowledged to Michael
John Curry, Theorem 2.3 of the Zenodo preprint
https://doi.org/10.5281/zenodo.22087163, 24 August 2026. The citation
subagent verified the primary metadata and theorem/proof in the cached
PDF, whose MD5 matches the publisher's metadata. This antecedent
collision-free window-counting method is not used as an external proof
premise: the paper reproduces the finite moment/counting derivation.

The source https://rstation.ai/problems/collatz/papers/9/v1 was opened
directly on 16 November 2026. Its metadata identify the author handle
`lyapunov_weaver`, version 1, 21 October 2026 at 04:48 UTC, and title
*Ternary Syracuse laws: tail conditioning, moment growth, and predecessor
bounds*. Proposition11 is cited for prior Green finiteness only, and is
not imported as a proof premise for the elementary finite theorem.
It is an author manuscript on an AI-agent platform; platform acceptance
must not be described as independent peer review or formal verification.

Suggested bibliography entries for parent to align:

- `terras1976`: R. Terras, *A stopping time problem on the positive
  integers*, Acta Arithmetica 30 (1976), 241--252,
  https://doi.org/10.4064/aa-30-3-241-252.
- `lagarias2003`: J. C. Lagarias, *The 3x+1 problem: An annotated
  bibliography (1963--1999)*, arXiv:math/0309224.
- `valbuena2026`: Lucas Valbuena, *Collatz basin densities and canonical
  traces from first-passage stabilization*, 7 October 2026, the pinned
  source above, Section 2.
- `curry2026`: Michael John Curry, *An Explicit Windowed Sparsity Bound
  for Divergent 3x+1 Orbits, with Logarithmic-Floor Exclusion beyond the
  Harmonic Barrier*, Zenodo preprint, 24 August 2026,
  https://doi.org/10.5281/zenodo.22087163, Theorem 2.3.
- `weaver9v1`: the version-bound primary manuscript identified above.

No priority is claimed for classical exact parity coding, uniform
finite-path reciprocal and correction-product bounds, Green finiteness,
elementary first-split probability algebra, or the
reciprocal-square summation estimate. The finite section should be
presented as an explicit, locally verified continuation of v6, with
the separately stated open lower/coverage obligations left open.
