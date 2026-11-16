# Literature, attribution, and paired-path audit for v7

Audit date: 16 November 2026. This is an English source and mathematical
scope audit, not a claim of exhaustive coverage or independent refereeing.
The publication bibliography is
[`paper/v7_sections/bibliography.tex`](../../paper/v7_sections/bibliography.tex).
It contains complete entries, DOI links, and version-specific source links
for every citation in the manuscript. This note records what those
citations support and what was actually checked.

## The contribution should be described narrowly

The release contributes an explicit finite arithmetic proof, concrete
constants, local Lean integration, and a precise collection of interfaces
and paired-path deductions. The following general mechanisms have
precedents and are not claimed as new.

| Result or method | Relevant precedent | Permitted v7 description |
|---|---|---|
| Exact parity cylinders and residue lifting | Terras; classical Collatz literature | A retained legality interface, with local formalization |
| Collision-free counting by a split according to parity weight | Curry, Theorem 2.3 | A related finite moment proof with explicit rational constants |
| Uniform reciprocal budget and correction product for finite distinct trajectories | Valbuena, section on finite distinct trajectories | Concrete constants and local checked implementation, not the first universal qualitative bound |
| Integer Green finiteness, with a cycle return factor | Weaver paper 9, pinned v1, Proposition 11 | Prior qualitative conclusion; the quadratic occupation estimate has a direct local proof |
| Paired parity words, stems, and concatenation | Garner; Elia and Tucker | A specific exact two-rule construction and its guarded consequences |
| Smaller sources before descent on constructed cylinders | Weaver paper 21, v3, Theorem 3 | A simpler nearby-companion family, not the first such construction |
| Chosen absorbing words and protected smaller sources | Weaver paper 81, v2 | Existing construction; it does not control the next bits of a supplied source |
| Legal modular routing with linear valuation budget | Weaver and Wren paper 48, v2, Theorem 8 | Existing routing primitive; residue control does not by itself give a small integer source |
| Lower logarithmic predecessor density from a uniform atom floor | Weaver paper 12, v1, Section 2 | An explicitly assumed external input in the conditional budget |
| Canonical trace and fixed-root ancestor decay | Valbuena; attributed discussion in Weaver paper 12 | Existing external results, not newly checked Lean declarations |

Elia and Tucker disprove a particular proposed classification of stems.
Their counterexamples do not prove that every finite automaton or every
possible companion construction must fail. Conversely, adding valid
rules does not establish a complete classification.

## Verified primary bibliographic records

The following metadata were checked at primary publication pages,
official Zenodo records, or versioned rStation sources. A platform
standing or acceptance badge is not treated as independent mathematical
refereeing. The rStation bylines are account identities: `lyapunov_weaver`,
`fourier_wren`, and `cassian_mahler`. They are rendered readably in the
bibliography without an assertion about an account holder's legal name.

- **Terras (`terras1976`).** Riho Terras, *A stopping time problem on the
  positive integers*, Acta Arithmetica 30 (1976), no. 3, 241–252.
  [Publisher DOI](https://doi.org/10.4064/aa-30-3-241-252).
- **Lagarias (`lagarias2003`).** Jeffrey C. Lagarias, annotated bibliography
  of the 1963–1999 literature, first submitted 13 September 2003. The
  bibliography pins [arXiv version 13](https://arxiv.org/abs/math/0309224v13),
  dated 11 January 2011. This is a survey, not a new proof premise.
- **Krasikov and Lagarias (`krasikovlagarias2003`).** Ilia Krasikov and
  Jeffrey C. Lagarias, *Bounds for the 3x+1 problem using difference
  inequalities*, Acta Arithmetica 109 (2003), no. 3, 237–258.
  [Publisher DOI](https://doi.org/10.4064/aa109-3-4);
  [primary arXiv v1](https://arxiv.org/abs/math/0205002v1), 30 April 2002.
- **Garner (`garner1985`).** Lynn E. Garner, *On heights in the Collatz
  3n+1 problem*, Discrete Mathematics 55 (1985), no. 1, 57–64.
  [Publisher DOI](https://doi.org/10.1016/S0012-365X(85)80020-0).
  The publisher blocked full-text retrieval in this session. Its role
  here is historical attribution, supported also by the primary paper
  of Elia and Tucker; a fresh full Garner proof audit is not claimed.
- **Elia and Tucker (`eliatucker2015`).** Marcus Elia and Amanda Tucker,
  *Consecutive integers and the Collatz conjecture*, Integers 15 (2015),
  Article A54, published 30 December 2015.
  [Official journal PDF](https://math.colgate.edu/~integers/p54/p54.pdf);
  [arXiv:1511.09141v1](https://arxiv.org/abs/1511.09141v1),
  30 November 2015. The relevant block/stem definitions and counterexample
  argument were read. No journal DOI is invented for this article.
- **Curry (`curry2026`).** Michael John Curry, preprint on explicit
  windowed sparsity and logarithmic-floor exclusion, 24 August 2026.
  [Official Zenodo record](https://doi.org/10.5281/zenodo.22087163).
  The record has no version field. The locally cached PDF exactly matches
  its official MD5 `f3c9170c6c8131b2c01f02e421a4c98a`. Theorem 2.3 and
  Proposition 3.1 were read for methodological precedence, not imported
  as premises of the finite core.
- **Valbuena (`valbuena2026`).** Lucas Valbuena, *Collatz matrix
  obstructions, synchronization, and basin densities: three papers and
  Lean artifacts*, version 2026.09.28.5, 28 September 2026.
  [Official Zenodo record](https://doi.org/10.5281/zenodo.23025885),
  whose resource type is **Software**, not a refereed journal article.
  The manuscript on basin densities and canonical traces was read at
  [commit a7275d5a73814d3d9a400c6fe6577de9542b03a3](https://github.com/x1xhlol/collatz-two-coordinate-obstruction/blob/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/tao-basin-densities.tex).
  Its finite-trajectory section already proves the uniform reciprocal
  tail and uniform product, including a product tending to one when
  the odd source states become large. The local release does not claim
  to have rebuilt this external development.
- **Weaver paper 9 (`weaver9v1`).** Lyapunov Weaver, *Ternary Syracuse
  laws: tail conditioning, moment growth, and predecessor bounds*,
  [v1](https://rstation.ai/problems/collatz/papers/9/v1),
  21 October 2026, 04:48 UTC. Proposition 11 supplies the relevant
  integer Green precedent. Version 2 has a different title and is not
  silently substituted for the cited version.
- **Weaver paper 12 (`weaver12`).** Lyapunov Weaver, *First-landing bounds
  and canonical inverse laws for Collatz*,
  [v1](https://rstation.ai/problems/collatz/papers/12/v1),
  21 October 2026, 08:59:32 UTC. Section 2 derives the lower logarithmic
  density using its Input D before invoking natural-density existence.
  This is an unnumbered display; browser line numbers are not equation
  numbers. Section 8 and the discussion after Theorem 9 explicitly
  attribute canonical trace and fixed-root nonatomicity to Valbuena.
- **Weaver paper 21 (`weaver21`).** Lyapunov Weaver, *Smaller Collatz
  sources before first descent: power gains and conditional exponent
  shells*, [v3](https://rstation.ai/problems/collatz/papers/21/v3),
  23 October 2026, 19:46 UTC. Theorem 3 is a direct smaller-source
  precedent. Its refinement of source cylinders does not control a
  prescribed infinite future.
- **Weaver and Wren paper 48 (`weaver48`).** Lyapunov Weaver and Fourier
  Wren, *Hierarchical Syracuse renewal and linear valuation budgets for
  modular routing*, [v2](https://rstation.ai/problems/collatz/papers/48/v2),
  28 October 2026, 05:46 UTC. The linear-routing statement is **Theorem 8**
  in Section 9. It permits a common length and total; its absolute
  constants are not numerically tabulated.
- **Weaver paper 81 (`weaver81`).** Lyapunov Weaver, *Linear absorbing
  words and protected smaller-source certificates for Collatz*,
  [v2](https://rstation.ai/problems/collatz/papers/81/v2),
  1 November 2026, 21:59 UTC. The chosen absorbing word constrains the
  compatible source cylinder. It does not force an arbitrary supplied
  integer to follow that word.
- **Weaver paper 150 (`weaver150`).** Lyapunov Weaver, *Critical barriers
  and memory costs in Collatz inverse dynamics*,
  [v2](https://rstation.ai/problems/collatz/papers/150/v2),
  15 November 2026, 21:53:21 UTC. Corollary 4 makes a necessary
  Haar-singular component of any empirical ternary limit quantitative,
  with exact fraction `(a* − log₂3)/(a* − 1)`, approximately 0.08855.
  It does not exclude a divergent orbit. Haar policy ceilings are not
  promoted to pointwise no-go theorems for arbitrary integer paths.
- **Mahler paper 152 (`mahler152`).** **Cassian Mahler**, not Lyapunov
  Weaver, *Slope–Ballot Duality, Exact Binary Escape Thresholds, and
  Parity-Trap Shifts Exceeding the 3/4 Collatz Survival Barrier*,
  [v1](https://rstation.ai/problems/collatz/papers/152/v1),
  15 November 2026, 21:47:04 UTC. The observed length-22 terminal word
  is attributed to Section 4, equation (4.4). No large search or
  survival certificate in that source is claimed as independently replayed.
- **El Jaouhari (`eljaouhari2026`).** Naoufal El Jaouhari, *Uniform
  Syracuse atoms and exact density regularity with quantitative Collatz
  predecessor counts*, **v1**, 14 October 2026.
  [Official Zenodo record](https://doi.org/10.5281/zenodo.23377671),
  resource type **Preprint**, CC BY 4.0. The external atom floor and its
  analytic/formal dependencies were not independently rebuilt here.
- **Tao (`tao2022`).** Terence Tao, *Almost all orbits of the Collatz map
  attain almost bounded values*, Forum of Mathematics, Pi 10 (2022),
  e12, 1–56. [Publisher DOI](https://doi.org/10.1017/fmp.2022.8).
  Its quantifier is almost all starting values in logarithmic density.
- **Lean documentation (`lean4322`, `lean4340`).** Official release notes
  for [4.32.2, 28 July 2026](https://lean-lang.org/doc/reference/latest/releases/v4.32.2/)
  and [4.34.0, 14 September 2026](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/)
  explicitly document soundness fixes. Acceptance by the pinned 4.29.1
  toolchain is not represented as a new-kernel replay.
- **Frozen v6 (`borgatta_v6`).** Piero Borgatta, *Exact Exponent Cylinders,
  Precision Budgets, and Singular Coding in Accelerated Syracuse
  Dynamics*, version 6.0.0, 24 September 2026,
  [Zenodo DOI](https://doi.org/10.5281/zenodo.22936057).

## Conditional budget: dependency and cycle audit

The v7 conditional theorem assumes directly, for every nonperiodic unit
`v`, a lower relative-odd logarithmic predecessor density of `α/(4v)`.
This is the exact statement used; natural-density existence, a canonical
trace, a Doob law, and mixing are not additional premises of its proof.
The lower statement is already derived from the external atom input in
Weaver paper 12. Referencing that derivation does not make it a locally
checked theorem.

For a finite forward antichain, determinism makes its predecessor basins
disjoint. Finite addition of lower limits and the normalized odd harmonic
sum bound give reciprocal sum at most `4/α`; no infinite interchange is
used. First arrival, a different last parent, and inverse prefix-freeness
are essential guards on catalogues. A merger identity alone supplies
none of these guards automatically.

The observed finite segment may enter a cycle without repeating a state.
The catalogue at the first cyclic point is exceptional. All other seeds
form one nonperiodic antichain; the exceptional nonperiodic seeds form
a second. Its periodic seeds lie on one nested inverse cyclic chain,
so prefix-freeness selects at most one. This proves the stated cost
`b exp(27)(8/α + 1)`. The smaller constant `4 b exp(27)/α` applies when
all displayed targets are nonperiodic. A global lower construction is
still required before this conditional upper budget can exclude divergence.

## Paired-path proofs and exact finite checks

All assertions in `paired_paths.tex` are paper proofs. They are not new
Lean declarations. The finite-core section has its own separate source
and dependency audit. Cross-review is by collaborating AI agents with
shared context, not independent human referees.

The legality argument uses the final odd quotient criterion, not an
affine identity alone. It checks positivity of the translated seed and
endpoint. A seed realizing the mixed terminal language cannot be `1`,
so the translated seed `b−2` is positive. At block boundaries, the
`12 → 21` and `212 → 113` relations preserve a difference of two.
The second observed block has slope `27/32`, so the full block language
is not called expansive. An explicitly chosen macro-subfamily is
expansive at every nonempty prefix.

For the attributed terminal word `w*` and its displayed modified partner
`g*`, direct integer arithmetic gives:

| Quantity | Exact value |
|---|---:|
| Length of either word | 22 |
| Total exponent of either word | 34 |
| `C(w*)` | 118309227953 |
| `C(g*)` | 181071347171 |
| Difference | `62762119218 = 2·3^22` |
| Least observed prefix gain | `3^21/2^33 > 1` |

Thus `F(g*)(x−2) = F(w*)(x)` follows directly. The partner here starts
with exponent 4 and has source `x−2`; it is not silently identified with
the differently parametrized partner in Mahler's source. The external
literal observed word is attributed; legality, unit repair, gain, and
last-parent difference are proved in v7 itself. This small exact check
is not a replay of Mahler's larger certificates.

For a minimum divergent unit seed, a first exponent at least two gives
an immediate smaller divergent unit. Its first exponent is therefore
one. If the orbit remained forever in the two-block language, `b−2`
would have an unbounded subsequence, hence a divergent orbit. Its unit
repair after the first alternative exponent gives a smaller divergent
unit. This proves necessary exit without the external density premise.

The exit bounds charge valuations to the actual height buffer
`log((z−1)/(b−1))`. The reference comparison includes the reached state
at time zero; the forced run can have length zero. Along a minimum
divergent unit orbit, every subsequent unit remains at least `b`.
The constructed collapse family is a negative control for keeping the
same companion: the companion reaches one while the observed path is
large. Its following forced contraction eventually descends below `b`.
It is neither a divergent orbit nor a counterexample to Collatz.

The missing global theorem must compose exits, companion changes, and
later contractions. Local height charges alone do not prove amortization,
because later expansive segments can replenish the buffer. No claim of
global novelty, complete exit coverage, universal descent, or Collatz
resolution follows from this audit.

## Source-bound verification boundary

Primary version downloads were inspected for the cited mathematical
interfaces. They were kept temporarily for reading, not copied wholesale
into this publication. The following two new-source byte receipts pin
the particularly recent material used in the release:

| Primary download | Bytes | SHA-256 |
|---|---:|---|
| `collatz_150/versions/2/download` | 33025 | `8bcd93813e26f02bdd851835c3f2fba0dbaa8dc6b3d50ff41296c05c6999b661` |
| `collatz_152/versions/1/download` | 74958 | `b7d8dd4f3cbe5dbfc7bf9ce687fd98c1eb518cccdea6205274c51399f9c9e759` |

The rStation primary API supplied the version metadata, including the
author correction for paper 152. Official Zenodo APIs supplied creator,
publication date, version, DOI, and resource type. No source's platform
status is used as a proof premise. No external asymptotic theorem or
external formal artifact is reported as independently recompiled.
