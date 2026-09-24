# Bounded semantic audit: initial core seed and persistence

Date: 2026-09-24. Read-only examination of ten immediate source files in
`/tmp/collatz-predecessor-audit/assembled/Erdos1135`. No compilation or axiom audit was run as part of this review.

## Finding

In the inspected seed/persistence chain I found no assumed positive density, no assumed lower bound on the number of distinct integer predecessors, and no use of a nonreturn hypothesis. The lower bound supplied to the persistence theorem is a finite-generation **weighted marked mass**, obtained separately from a mean over finitely many ternary residue classes. It is not already a count of distinct integer sources. Its conversion to such a count is precisely the later step handled by the new occupation/charge argument.

This is a bounded semantic review, not an independent verification of the entire analytic library. Imported mixing, histogram capacity, tail and transport lemmas remain explicit review boundaries below.

## 1. What the initial seed assertion actually says

`ExplicitUnitSupportedCoreSeed.explicit_exists_unit_ge_of_supported_mean` is a finite averaging lemma. Its input is a function g on ZMod(3^q) supported on units, with g=0 on nonunits and full mean (2/3)*P. The finite averaging lemma itself does not need an additional nonnegativity hypothesis. The number of unit residues is 2*3^(q-1), so some unit y satisfies g(y)>=P. Its proof sums over units and applies `Finset.exists_le_of_sum_le`; it does not count Collatz predecessors.

`exists_unit_rootCoreBackwardMark_ge_full_product` instantiates this with `ndRootCoreBackwardMark` and `ndRootCoreProbabilityProduct`. In `Geom2ShiftedWideSymmetricCoreBackwardMean`, the identity

    mean(backwardMark at conductor q) = (2/3)*probabilityProduct

is proved by induction on the finite number of generations, using an exact filtered-kernel mean identity and the sum of selected-word atoms. At generation zero the reference density has full mean 2/3. Nothing here asserts that every residue corresponds to a successful fixed target; that separate bridge is supplied by the finite residue lift.

The singleton state itself has label type Unit, root R and outer weight 1; its denominator is proved to be 1. `rootCoreSingletonState_markedMass_eq_backwardMark` identifies its finite forward marked mass with the backward mark at R modulo the finite conductor. Thus choosing R in the good residue transfers the mean argument into an actual finite path family. In the new general-target route, the target-reaching property comes from `generalTargetRoot_reaches`, rather than any preexisting density theorem.

## 2. Why the probability product is bounded below

`Geom2ShiftedWideSymmetricExplicitCoreProduct.coreProbabilityProduct_ge_255_div_256` proves a product lower bound from per-generation probability deficits. The inspected proof establishes 0<=f_j<=1 and a summable geometric deficit bound. It then uses the elementary finite-product inequality

    product(f_j) >= 1 - sum(1-f_j).

The chosen floor b>=2^80 and cap_j>=16+j/100 make the total deficit at most 1/256. This is a probability estimate for selected tuples, not an assumed abundance of distinct integer predecessors. Its inputs are explicit strip/cap tail lemmas and deterministic growth of the floor; no target a, predecessor count, or nonreturn property occurs in the theorem statement or displayed proof.

## 3. The geometric tuples are a reference law, not a stochastic assumption on an orbit

`Tao/Syracuse/ValuationDistribution.lean` defines `geom2PNatListPMF` recursively by PMF.pure at length zero and a geometric-law bind/map at the next length. Independence belongs to this constructed reference distribution. The atom of an exponent tuple is proved to be 2^(-sum a_i), and the PMF is supported exactly on lists of the specified length.

`Geom2ShiftedWideSymmetricReferenceDensityTransport` builds the selected words as a finite union of exact first-crossing/overshoot word sets. Their prefix-disjointness is an explicit input to the reference prefix-family estimates. The probability reasoning therefore controls disjoint cylinders in the reference word space. It does not state that valuations along an individual deterministic Collatz orbit are independent.

In `Geom2ShiftedWideSymmetricCoreBackwardMean`, sums over actual unit-child incidences are identified with the filtered reference kernels through exact finite transport identities. This is the bridge used in the seed argument; it is not replaced by an independence heuristic.

## 4. What is assumed, and what is proved, in persistence

`ExplicitUnitSupportedFrozenSeed.explicit_good_marked_margin_logarithmic_full` assumes:

- a fixed finite state U and its geometric floor/span hypotheses;
- an explicit fine-scale mixing statement `syracFineScaleMixingAt 6 C`;
- cap bounds;
- a late enough seed generation N and later generation n;
- `(255/256)*U.denominator <= U.coreMarkedSequence ... N`.

The local name `hseed` in this theorem means this last finite marked-mass inequality. It does **not** mean the nonreturn assumption used by the old terminal census.

Its proof combines three estimates: core marked-mass variation between N and n, discrepancy between the core mark and terminal unit mass, and the discarded bad depth-shift mass. Explicit tail budgets pay these errors, yielding `(175/256)*denominator` for the good terminal unit mass and hence at least 2/3 for a singleton. The same fixed seed works for all sufficiently late n and all eligible physical windows X.

`ExplicitCoreVariation.explicit_core_marked_difference` is obtained by telescoping finite increments and dominating their sum by a summable tail. The increment bound comes from reference-density mixing and an upper bound on histogram capacity. `ExplicitTerminalVariation` uses the same mixing law and an upper bound for adaptive histogram pairing; `Geom2ShiftedWideSymmetricTerminalDepthShiftMarkedLoss` bounds the discarded marked mass by a tail. None of these displayed arguments assumes a count lower bound or a density theorem.

The marked terminal mass includes the reference-density marker, which need not be <=1. A lower bound for that mass is therefore not itself the desired unmarked mass lower bound, and still less a bound on distinct physical sources. Removing that marker via the two-conductor census and then controlling source multiplicity are genuine remaining steps. This distinction prevents a circular reading of the initial `hseed` hypothesis.

## 5. Import names that look circular

`ExplicitOnePeriodSeedToCount.lean` imports modules whose names include `ExplicitPositiveDensityPair` and other seed-to-count results. This is broad module organization. The lemma reused by `ExplicitUnitSupportedCoreSeed` is `explicitBackwardConductor_ge`, whose proof is directly an induction on the conductor recursion. It does not invoke a positive-density conclusion. The generic persistence theorem similarly has a proof consisting of the three variation bounds and elementary inequalities.

This observation distinguishes syntactic import closure from logical proof dependency. A future generated constant-dependency report would give a more exhaustive machine-readable confirmation; the present review does not claim to have audited all transitive proofs of imported helpers.

## 6. Remaining boundaries

The bounded review did not reprove the Fourier/fine-scale mixing theorem, the geometric tail library, the histogram capacity bounds, or every exact reference transport identity. These are substantial analytic/combinatorial ingredients, not consequences established by the new weighted adapter. The planned serial Lean compilation checks their imported proof terms, but an independent mathematical review of those ingredients remains a separate task.

I found no new parameter loop: the good finite residue is chosen at the seed conductor fixed by b,C,Nseed; R is then selected; only afterwards is the larger occupation coefficient R(3R+1) used to choose the later mixing conductor m. Uniform persistence allows that later choice without changing the seed.

## Files inspected (ten)

1. ND/PositiveDensity/ExplicitUnitSupportedFrozenSeed.lean
2. ND/PositiveDensity/ExplicitUnitSupportedCoreSeed.lean
3. ND/PositiveDensity/ExplicitOnePeriodSeedToCount.lean
4. ND/PositiveDensity/Geom2ShiftedWideSymmetricCoreBackwardMean.lean
5. ND/PositiveDensity/Geom2ShiftedWideSymmetricExplicitCoreProduct.lean
6. ND/PositiveDensity/ExplicitCoreVariation.lean
7. ND/PositiveDensity/ExplicitTerminalVariation.lean
8. ND/PositiveDensity/Geom2ShiftedWideSymmetricTerminalDepthShiftMarkedLoss.lean
9. ND/PositiveDensity/Geom2ShiftedWideSymmetricReferenceDensityTransport.lean
10. Tao/Syracuse/ValuationDistribution.lean
