# Six-port odd Syracuse section from Monks et al.'s 20 mod27 theorem

**Status:** paper-level deduction from an established theorem plus exact elementary modular arithmetic; not yet Lean-formalized. The finite test checks transcription only. No claim of literature priority is made.

## Source and exact strength

Monks, Monks, Monks & Monks, *Strongly sufficient sets and the distribution of arithmetic sequences in the3x+1 graph*, Discrete Mathematics313(4),468–489 (28February2013), [DOI](https://doi.org/10.1016/j.disc.2012.11.019), [full text §6](https://arxiv.org/html/1204.3904#S6), **Theorem6.4**: the set20mod27 is **forward sufficient and cycle sufficient** for the shortcut map T(n)=n/2 if even, (3n+1)/2 if odd. In their definitions this means every divergent T-orbit and every nontrivial positive T-cycle intersects it. “Strongly sufficient” additionally requires a backward-tracing property and is not what Theorem6.4 states.

The proof removes20 from the mod27 graph, prunes transient nodes, and observes that all remaining infinite paths have at most half odd steps, inconsistent with a divergent orbit or nontrivial cycle. Applying the conclusion to every tail of a hypothetical exceptional orbit yields arbitrarily late visits. Neither a time bound nor descent at those visits follows.

## Exact episode equivalence

Take odd positive u with3∤u and put a=ν₂(3u+1)≥1. Between u and its next odd iterate S(u), the shortcut orbit takes exactly a steps. The episode is defined as `(u,S(u)]`: it excludes the source and includes the final odd endpoint. Its visited states are

    T^j(u)=(3u+1)/2^j,  1≤j≤a.

Since2^j is invertible mod27,

    T^j(u)≡20(mod27)  iff  3u+1≡20·2^j(mod27).

The order of2 modulo27 is18 (2^9≡−1; no proper divisor18 gives1). Replace j by its representative j₀∈{1,…,18}. Then j₀≤j≤a and2^j₀≡2^j mod27, so the episode hits20mod27 iff it does so for some1≤j₀≤min(a,18). Reduction mod3 forces j₀ odd. For odd j₀, division by3 turns the congruence into

    u≡(20·2^j₀−1)/3 (mod9).

The nine candidates and residues are

    j₀ : 1  3  5  7  9  11 13 15 17
    u%9: 4  8  6  7  2   0  1  5  3.

Because3∤u, exclude j₀=5,11,17. The remaining six conditions give the following **exact disjoint union E**:

|Port|j₀|Residue mod9|Valuation threshold|CRT cylinder|
|---:|---:|---:|---|---|
|1|1|4|ν₂(3u+1)≥1|u≡13 (mod18)|
|2|3|8|ν₂(3u+1)≥3|u≡53 (mod72)|
|3|7|7|ν₂(3u+1)≥7|u≡853 (mod1152)|
|4|9|2|ν₂(3u+1)≥9|u≡3413 (mod4608)|
|5|13|1|ν₂(3u+1)≥13|u≡54613 (mod73728)|
|6|15|5|ν₂(3u+1)≥15|u≡218453 (mod294912)|

Here the valuation threshold is equivalent to3u+1≡0 mod2^j₀; because3 is odd, there is a unique odd class modulo2^j₀. CRT with the mod9 condition supplies the listed residue modulo9·2^j₀. All mod9 residues differ, so the six progressions are disjoint. Thus

    u∈E iff some shortcut state during its next odd episode is20mod27.

The section's natural density is

    1/18+1/72+1/1152+1/4608+1/73728+1/294912=6935/98304.

Relative to the odd integers it is6935/49152. This density is descriptive, not an ingredient in recurrence.

## Recurrent coverage proof

Suppose u₀,u₁,… is an exceptional positive odd Syracuse orbit, meaning it never reaches1. A deterministic bounded positive orbit is eventually periodic; thus its shortcut expansion is either eventually in a nontrivial cycle or divergent. After the first Syracuse step, no iterate is divisible by3:3u+1 is1mod3 and division by2 preserves nondivisibility.

By Monks Theorem6.4, applied after any shortcut time, the exceptional shortcut orbit contains a later20mod27 state (on a cycle, each traversal supplies one). Hence it has infinitely many hit times. Partition the shortcut tail into its odd-to-odd episodes. Each episode has finite length a_i because its starting integer is positive. Infinitely many hit times cannot occur in finitely many episodes. Infinitely many episodes therefore hit20mod27, and the episode equivalence puts their starting odd integers in E. This proves:

    Every positive odd orbit that never reaches1 visits E infinitely often.

This is deliberately not a claim that every odd orbit visits E; e.g. S(1)=1 and1∉E. Nor is it the claim that the S-orbit itself visits20mod27. The section marks starts of episodes that contain such a shortcut state.

## Direct finite validation performed

For every odd1≤u<200000 with3∤u, computed a with exact integer arithmetic, enumerated all states(3u+1)/2^j for1≤j≤a, and asserted equivalence between a20mod27 hit and membership in the six conditions. Every case passed. CRT residues and the density were computed exactly using fractions.

## Limit and next theorem

This is a coverage reduction, not a descent proof. The positive first-return map R_E exists along exceptional orbits, but the time between returns can be unbounded. Carry the actual episode word, original seed, affine offset, and valuation phase into a certificate. Do not replace the joint constraints by independence or a Markov average.

A useful next formal statement is a generic lemma transferring a recurrent section for shortcut T to the finite marked-episode union E for S, then an exact lemma that first-return branches act affinely on their cylinder quotient. Both bridge existing v6 data to a section whose coverage is proved. The hard open step remains a well-founded descent on all return branches or an exclusion of every coherent infinite survivor path.
