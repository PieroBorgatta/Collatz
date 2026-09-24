# Weighted predecessor adapter

An independent overlay for Lech Mazur's hash-pinned public Collatz predecessor
source release. It replaces the non-returning-seed counting argument with a
weighted occupation bound. The main `lean/` project and the published Zenodo v6
artifacts are not modified by this overlay.

**Verification status: PASS** on [CI 36005012141](https://github.com/PieroBorgatta/Collatz/actions/runs/36005012141),
commit `171150edde2dcf0329e8c82b18c02bbc3cdc40ec`. The modular replay checked
all **395 local modules**, including both final theorems. This final run
validated and reused 394 previously compiled source/dependency/object receipts
and compiled the remaining module. Both dependency audits passed, with only
`propext`, `Classical.choice`, and `Quot.sound`.

The weighted audit inspected 4,672 local declarations; the two-seed audit
traversed 43,248 reachable declarations without a module boundary. The required
new lemmas were reached and the respective forbidden old seed dependencies
were absent within each audit's declared scope. The
[verification manifest and preserved evidence](../../notes/post_v6_adapter_2026-09-24/verification_manifest.json)
record the exact inputs and checks. This is a pinned Lean replay, with cached
external package objects, not an independent kernel or mathematical review.

The target statement is the existing positive-lower-density theorem: for each
positive ordinary Collatz target `a` not divisible by 3, there are `c>0` and
`X0` such that at least `c*X` positive integers below `X` reach `a`, for every
natural `X≥X0`. This is not a new statement of the Collatz conjecture or a claim
of priority for the external density theorem.

## What changes

- `WeightedPathOccupation.lean` proves the telescoping occupation estimate for
  the external Syracuse map and its exact valuation-word weights.
- `WeightedTerminalAdapter.lean` identifies the external terminal incidences
  with exact paths and transfers the bound to the concrete singleton seed.
- `WeightedCensus.lean` propagates an abstract source-charge bound through the
  residue census, mass estimate, and distinct-predecessor count.
- `WeightedFrozenSeed.lean` chooses a large predecessor in a supplied ternary
  residue using a finite lift, without a bound on possible cycles.
- `WeightedPredecessorDensity.lean` composes those lemmas with the external
  analytic input and its explicit mixing theorem.

The source-charge coefficient becomes `R*(3*R+1)` in place of `R`. The loss
also affects the subsequent choice of the mixing parameter; no improvement of
the numerical density constant is claimed. Choosing the seed **from a supplied
good residue** is a finite procedure. This does not yet implement an executable
algorithm selecting a good residue or computing all constants from the target.

## A second route: two bounded candidate seeds

`TwoSeedNonreturn.lean` uses injectivity of a deterministic map on its periodic
points: two distinct predecessors with the same next iterate cannot both be
periodic. Two consecutive representatives of the explicit ternary residue
family have the same Syracuse image, so at least one has no positive return.
Both lie below an explicit bound independent of which residue was selected.

`TwoSeedDensity.lean` carries that bound through the frozen-seed argument and
the original nonreturning census. It defines a coefficient and cutoff depending
only on the public target after specialization to the external numerical mixing
constant. Writing `G(r,k) = ndGeneralTargetRoot r k`, the parameters are

```text
b = 2^80
Nseed = explicitLogarithmicSeedGeneration b C
q = ndRootCoreBackwardConductor b (explicitSeedFloor b Nseed / 4) Nseed
T = G(2*a, (16^b + 3)*3^q)
m = 132*T*C + 1
c = 3/(256*T*3^m)
```

The cutoff is `32*(H+1)`, with `H` the explicit interval-height bound at the
generation prescribed in the module. The constants do not contain an
existentially chosen good residue or a selected nonreturning seed.

This second route retains the original census coefficient at the chosen seed
and replaces that seed by its uniform upper bound `T` in the public constant.
It does not decide which candidate is nonperiodic. No practical evaluation of
the enormous constants, automatic numerical improvement over the weighted
route, or independent reproof of the external analytic inputs is claimed.
The underlying fact about periodic points is elementary; no priority claim is
made for that fact. See the [two-seed audit](../../notes/post_v6_adapter_2026-09-24/TWO_SEED_AUDIT.md)
for the parameter order and remaining verification limits.
A separate [algebraic comparison](../../notes/post_v6_adapter_2026-09-24/COEFFICIENT_COMPARISON_IT.md)
proves `T<R^2` for aligned explicit candidates and a factor greater than three
in the associated coefficient formulas. That comparison is paper-level,
not Lean-verified; it neither identifies the current weighted chooser with
those candidates nor compares the cutoffs.

## Further optimization under verification

Four additional modules are being checked separately from the verified
395-module snapshot above. `CompactSeedNonreturn` replaces the root bound
`G(2*a,(16^b+3)*3^q)` by `G(2*a,2*b+2*3^q)`. `OptimizedConductor` preserves
the full sixth-power mixing decay and chooses the least positive m with
`88*T*C ≤ m^6`. `OptimizedDensity` connects these choices to the same census;
`OptimizedComparison` states strict improvements in both the coefficient and
cutoff. These new modules and their audit are **pending CI verification**.
See the [optimization report](../../notes/post_v6_optimization_2026-09-24/RESULTS_IT.md).

## Reproduce in a separate directory

Requirements: Python 3, curl, Git, elan/Lake, and enough space for the pinned
Mathlib cache. The exact toolchain is Lean `4.30.0-rc2`; Mathlib is pinned to
`5450b53e5ddc75d46418fabb605edbf36bd0beb6` by the upstream lock file.

From the repository root, choose a fresh directory outside the repository:

```bash
python3 research/weighted_predecessors_adapter/prepare.py /absolute/fresh/project
cd /absolute/fresh/project
lake exe cache get
lake env python3 /absolute/Collatz/research/weighted_predecessors_adapter/build_closure.py \
  WeightedPredecessorDensity TwoSeedDensity OptimizedComparison CollatzPredecessorDensity
lake env lean /absolute/Collatz/research/weighted_predecessors_adapter/WeightedDependencyAudit.lean
lake env lean /absolute/Collatz/research/weighted_predecessors_adapter/TwoSeedDependencyAudit.lean
lake env lean /absolute/Collatz/research/weighted_predecessors_adapter/OptimizedDependencyAudit.lean
```

The preparation script authenticates both downloaded ZIPs before executing the
upstream assembler, preserves its Lean sources and configuration, and runs its
source verifier. `--archives /directory` instead reads `supplement.zip` and
`baseline.zip` from that directory, verifying the same hashes.

The compiler checks local modules in dependency order, using one worker by
default. `--jobs 2` or `--jobs 3` allows bounded parallelism when memory permits.
Each Lean process is limited to 4 GB and 600 seconds; a failure or timeout is
recorded and is not successful verification. `--keep-going` checks independent
branches after a proof error and records blocked descendants, while any detected
source or configuration mutation stops scheduling globally. CI uses this option
to expose independent errors in the same run; success still requires every
module in the requested closure. Outputs and a resumable receipt
are written under `build/weighted-replay/`. A resumed module must match its
source/dependency fingerprint and the hash of its compiled object.

This is a direct Lean compilation of the local import closure, not `lake build`
and not an independent LeanChecker run. External package objects are reused
from the pinned cache. The root dependency audit checks the theorem's standard
axioms and verifies both that the new occupation/seed lemmas are reached and
that the old non-returning-seed route is absent from the weighted theorem's local
proof closure. The two-seed route deliberately reuses that census after proving
a bounded nonreturning seed exists; it needs its own dependency and axiom audit.

On the development Mac, commands use
`DEVELOPER_DIR=/Library/Developer/CommandLineTools`. Locating the isolated
project and caches on the internal disk does not change the mathematical
sources or the pinned versions.

## Source provenance

The two upstream source archives are the v1.1 predecessor supplement and its
slim v2.1 baseline. Their exact URLs, byte counts, and SHA-256 digests appear in
`prepare.py`. Upstream source, its assembler, and derived code are Apache-2.0;
see `LICENSE` and `UPSTREAM_NOTICE`. The baseline sources are fetched during
preparation rather than republished here. The accompanying upstream paper is
not part of this source-license grant.

Modifications and new proofs were produced with AI assistance under Piero
Borgatta's direction. Compilation and dependency checks do not constitute
independent human mathematical review of the full analytic argument.

## Optional aggregate diagnostic

`build_bundle.py` can generate a source aggregate and a transformation manifest
in the prepared project. It hoists imports, isolates each source in a section,
and alpha-renames the two colliding private `coefficient_cast` identifiers.
`BundleDependencyAudit.lean` audits the resulting root proofs if it compiles.
This widens the elaboration context and is **not** equivalent to a successful
modular build. The initial local aggregate attempt was interrupted under memory
pressure; no successful aggregate verification is claimed. CI uses the original
module boundaries exclusively.

```bash
lake env python3 /absolute/Collatz/research/weighted_predecessors_adapter/build_bundle.py \
  CollatzPredecessorDensity WeightedPredecessorDensity TwoSeedDensity
lake env lean --threads=1 -M4096 -DautoImplicit=false -DrelaxedAutoImplicit=false \
  -o .lake/build/lib/lean/WeightedVerifiedBundle.olean WeightedVerifiedBundle.lean
lake env lean /absolute/Collatz/research/weighted_predecessors_adapter/BundleDependencyAudit.lean
```
