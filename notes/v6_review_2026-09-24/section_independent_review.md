# Independent adversarial review: Monks section transfer

24 September 2026. Arithmetic and logic reviewed independently. No canonical files edited. The deductions below are paper-level proofs plus finite integer regression checks, not Lean declarations or priority claims.

## Verdict

The six progression formula, exceptional-orbit recurrence transfer, and cancellation-tower intersection are correct. Three presentation conditions matter:

1. An episode must exclude its source and include its destination: post-source T states `(3u+1)/2^j`, `1<=j<=a`. If it includes the source, the stated iff is false: 47 is 20 mod 27, but 47 is not in E and its sole post-source state is 71.
2. The first-return map on E is partial in general. Example: `13 in E`, but `S(13)=5`, `S(5)=1`, and no later iterate is in E. Exceptional starts do have future E visits.
3. `31 -> 47 -> 71 -> 107 -> 161 -> 121` refutes unconditional first-return descent in the ordinary integer value on all E. Since 31 converges, it does not refute a claim restricted to hypothetical nonconvergent starts.

## Source check

Monks et al., *Strongly sufficient sets and the distribution of arithmetic sequences in the 3x+1 graph*, [primary full text](https://arxiv.org/html/1204.3904), defines its shortcut map as `T(x)=x/2` for even x and `(3x+1)/2` for odd x. In section 6, forward sufficient means meeting every divergent forward orbit; cycle sufficient means meeting every nontrivial cycle. Theorem 6.4 establishes both for `20 mod 27`. Its proof explicitly uses the nontrivial-cycle/divergent-orbit split. The result does not assert that every convergent orbit visits the residue class.

## Exact arithmetic derivation

Let u>0 be odd, 3 not dividing u, and `a=v2(3u+1)`. On its post-source episode, the condition of a marked state is

    exists j in {1,...,a}: (3u+1)/2^j = 20 mod 27.

Since 2 is invertible modulo 27, this is equivalent to

    exists j in {1,...,a}: 3u+1 = 20*2^j mod 27.

The order of 2 modulo 27 is 18. Replace any j with the unique `j0 in {1,...,18}` congruent to j modulo 18; then `j0<=j<=a`, and division by `2^j0` is still integral. The congruence forces j0 odd. For j0=1,3,5,7,9,11,13,15,17 the resulting u mod 9 is respectively 4,8,6,7,2,0,1,5,3. Removing the three classes divisible by 3 leaves exactly:

| j0 | u mod 9 | odd u and a>=j0 | final progression |
|---:|---:|---|---|
|1|4|automatic a>=1|13 mod 18|
|3|8|3u+1 divisible by 8|53 mod 72|
|7|7|3u+1 divisible by 128|853 mod 1152|
|9|2|3u+1 divisible by 512|3413 mod 4608|
|13|1|3u+1 divisible by 8192|54613 mod 73728|
|15|5|3u+1 divisible by 32768|218453 mod 294912|

Each final progression is the unique CRT solution modulo `9*2^j0`. They are pairwise disjoint because their residues modulo 9 differ. Their total natural density is `6935/98304`; relative to all positive odd integers it is `6935/49152`.

## Recurrence transfer

Define exceptional as never hitting 1. For a deterministic positive-integer orbit, repetition implies eventual periodicity. If there is no repetition, every finite set of integers is visited only finitely often, so the orbit tends to infinity. Thus an exceptional T orbit is either divergent to infinity or eventually reaches a nontrivial cycle.

Every tail of an exceptional orbit is exceptional. Theorem 6.4 therefore supplies marked T hits at arbitrarily large times. There are infinitely many odd episodes, and each episode has finite positive length a. Except for a possible initial source hit, every marked hit belongs to exactly one post-source episode `(u,S(u)]`; finitely many episodes cannot account for arbitrarily large marked hit times. After the first S step, all odd sources are coprime to 3. The exact iff above therefore gives E visits at arbitrarily large accelerated times.

This proves recurrence in time, not a uniform bound on passage or return time. In an eventual nontrivial cycle, the same finite E values may recur; recurrence need not mean infinitely many distinct E integers.

## Rank target

A precise sufficient criterion is a fixed function `rho:E -> W`, where `<_W` is well founded, such that every exceptional u in E has some strictly positive accelerated time k with `S^k(u) in E` and `rho(S^k(u)) <_W rho(u)`. Exceptionality persists under iteration; well-foundedness then contradicts existence of an exceptional E point. Section coverage contradicts existence of any exceptional start.

The codomain cannot be arbitrary reals with ordinary strict decrease: infinite strictly decreasing real sequences exist. Use natural ranks, a lexicographic well-founded order, or an explicitly proved well-founded relation. The label/state used by rho must have coherent transition semantics, not be freely reset.

Under Collatz, the exceptional domain is empty, so this criterion is vacuously satisfiable (for example by a constant natural rank). Consequently it is an equivalent target, not a solved reduction of difficulty. An operational checker applicable to every E seed should certify `hits 1` OR `finite future E return with rank decrease`, and handle the first-return map's partiality explicitly.

## Counterexample and tower check

The exact S trajectory `31,47,71,107,161,121` has E membership `true,false,false,false,false,true`. Hence its first E return is 121>31. This defeats globally asserting that the first-return value itself decreases, with the exceptional-only caveat above.

For even k>=4, define `n_k=(2^(k+1)-11)/3`. Then `3n_k+1=2*(2^k-5)` has valuation exactly 1. Its sole post-source episode state is `S(n_k)=2^k-5`. Therefore

    n_k in E iff 2^k-5=20 mod 27 iff 2^k=25 mod 27
                iff k=10 mod 18.

The last equivalence uses `25=2^10 mod 27` and order 18. At those k, n_k is automatically in `13 mod 18`, hence is coprime to 3. Thus restricting to the recurrent section retains an infinite subsequence of the v6 adverse tower; it does not remove the central cancellation obstruction.

## Independent finite checks

Using arbitrary-precision Python integer arithmetic:

- Recomputed every CRT progression by exhaustive search over its finite modulus; unique solution in each case, exactly as listed.
- Checked all 333,333 odd positive u<1,000,000 with 3 not dividing u: post-source episode hits 20 mod 27 iff u belongs to E; zero mismatches.
- Checked the claimed first-return segment and all intermediate membership flags exactly.
- Checked all even k from 4 through 1000: tower membership and marked first step occur exactly when k=10 mod 18; zero mismatches.

These checks guard against transcription errors; the modular proofs above give the universal statements.
