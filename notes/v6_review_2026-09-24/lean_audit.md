# Independent Lean audit — 24 September 2026

Scope: current `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean` working tree, not independently downloaded Zenodo archive. No existing project source was edited. No applicable AGENTS.md was found in checked ancestors. Local working tree already contains many modified and untracked files; this audit does not identify them as its own changes.

## Verdict

The inspected development states its limits candidly. It contains genuine, reusable local arithmetic theorems and finite certificates; it does not establish a global descent theorem or rule out arbitrary aperiodic orbits. The strongest next mathematical contribution is likely a checker that proves **all transitions and all branch coverage obligations for an infinite arithmetic family**, not additional finite spectral matrices without their missing orbit semantics.

`UniformStrictDescentHypothesis` is essentially equivalent to Collatz: Collatz implies an iterate at 1, strictly below every odd n>1; the development proves the reverse by strong induction. Thus its conditional bridge organizes obligations but should not be marketed as a major simplification of the conjecture by itself.

## Observed verification

- 49 Lean source files under `CollatzShadowing/`, including 26 generated files; 53,435 lines total, 9,922 nongenerated lines. These counts are organizational, not a measure of mathematical novelty.
- Scan `rg -n 'sorry|admit|^[[:space:]]*axiom|native_decide|unsafe|implemented_by|run_tac|#eval' CollatzShadowing --glob '*.lean'` found only 9 `native_decide` occurrences: `CollatzBridge.lean:669,693,714`, and `Generated/A0ReturnBranches.lean:1753,2125,2131,2137,2152,2377`. No source placeholders/project-declared axioms were found.
- `DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build` completed successfully with `Build completed successfully (3360 jobs)`. This is an incremental full-target check, using pre-existing project artifacts, not an independent clean rebuild.
- Operational side effect and repair: initial plain `lake build` used license-blocked system Git, misread mathlib origin, deleted `.lake/packages/mathlib`, and failed clone (exit 69). Exact mathlib v4.29.1 rev `5e932f97dd25535344f80f9dd8da3aab83df0fe6` was restored via shallow clone using the existing CommandLineTools. `lake exe cache unpack` then restored 7,872 dependency artifacts from local cache (no multi-GB network download). All other source/dependency files were preserved.
- Completed fresh elaboration and `#print axioms` results are recorded below.

## Exact mathematical scope and references

Paths in this section are relative to `lean/`.

1. `CollatzShadowing/ExactCylinders.lean:162`: for any nonempty list w of strictly positive exponents and natural n, actual Syracuse matching is equivalent to `(3^L*n+C_w) % 2^(A+1) = 2^A`. This is the useful semantic checker lemma: the last parity bit ensures exact valuation, not merely integrality. `:222` gives k>0 repeated blocks with modulus `2^(k*A+1)`. Unique odd residue and natural density are elementary paper-level consequences, not declarations in this file.
2. `CollatzShadowing/PrecisionTax.lean:103`: under `2^sum(w)<3^length(w)` and actual matching, the same affine phantom precision decreases by exactly `sum(w)`. `:179` telescopes **consecutive copies of the same w**; `:231` bounds the number of consumed bits; `:306` excludes an infinite actual run of that fixed positive-sum expansive word. These do not produce a single globally decreasing counter across arbitrary word changes.
3. `CollatzShadowing/NoInfinite.lean:124`: no fixed positive integer is congruent to one expansive phantom at all growing precisions. `:145` is the same claim about a positive endpoint; its prose explicitly excludes any conclusion about aperiodic switching. This is not exclusion of all positive cycles (which necessarily have contracting affine slope).
4. `CollatzShadowing/CycleConstraints.lean:30,54,72,92`: necessary cycle equation `(2^A-3^L)n=C`, positive-cycle contractivity, and divisibility sieve. These are correct useful necessary conditions, not a classification or exclusion of every nontrivial cycle. `:201` supplies the elementary `3n≤j*3^j` first-contracting-prefix bound.
5. `CollatzShadowing/FirstBarrier.lean:120`: the signed barrier gap is exactly `2^A*(n-endpoint)`. `:144` proves source-above-barrier iff strict descent. Therefore checking the barrier at the actual source is algebraically equivalent to testing the desired descent; an independent bound on an entire residue cylinder is needed to make this a genuine proof engine.
6. `CollatzShadowing/SwitchingPrecision.lean:46,70`: compatible label transport requires two exact coefficient equations, odd scale q, and nonzero numerators; then precision decreases by the step exponent. `:187` constructs an arbitrary relabeling that sets precision to any requested k. Unconstrained relabeling is unusable as a rank.
7. `CollatzShadowing/ThreeTraceObstruction.lean:178`: verified real segment `743 -> 1115 -> 1673 -> 1255`; the triples at 743 and 1255 are both `(3,2,1)`, with `(2,5,1)` at 1115. No strictly decreasing state function depending only on that triple can validate both macroedges. `:294` recovers a hidden compatible trace `ν₂(11n+19)` losing four bits across this lasso. This constructive obstruction is valuable: it prevents a seductive but invalid global inference.
8. `CollatzShadowing/A0InfiniteSubfamily.lean:99,212`: strict descent for two infinite residue subfamilies, including `2663+8192*u`. This is a genuine infinite-family result, still covering only a portion of A0.
9. `CollatzShadowing/SyracuseSingularity.lean:86`: for every R, two positive odd natural inputs satisfy `2^R | 3n+1`, with outputs 1 and 7. It is finite-precision arithmetic evidence for discontinuity at -1/3; the topological discontinuity statement itself is not formalized. `Syracuse2Adic.lean:70` is a totalization with special value 0 at the singular point.
10. `CollatzShadowing/Bound.lean:356`: a valid positive-vector finite CW certificate implies Mathlib's real spectral-radius bound for a finite nonnegative matrix. `Generated/K16S16KDeterministicCW.lean:2973` instantiates this on the declared 37-state matrix, with alpha 3/4 defined at `:67`. It is not a theorem about the infinite transfer operator. `Generated/K16S16KBridge.lean:57` packages matching labels/SCC/CW data; its obligations do not identify every integer trajectory with matrix behavior.
11. `CollatzShadowing/CollatzBridge.lean:58`: `UniformStrictDescentHypothesis` is a definition of an unproved proposition, not an axiom or theorem. `:2609` assumes it and concludes classical Collatz. `:1118` (`A0FirstBarrierExistsAll`) and `:1127` (`A0FirstBarrierThresholdAutomatic`) are both named open propositions; `:1323` requires both even to conclude the A0 family exit theorem.

## Trust and release discipline

`STATUS.md:65` accurately distinguishes the absence of textual axioms from `native_decide`'s compiler trust. `.github/workflows/lean.yml:22` explicitly allows only the nine existing generated native axioms, plus `propext`, `Classical.choice`, and `Quot.sound`. This is much better than advertising a blanket kernel-only proof, but it is not itself evidence that remote CI has run successfully.

`STATUS.md:72` notes the pinned Lean 4.29.1 predates soundness fixes in later releases and requests rechecking on Lean 4.34 with matching Mathlib. This audit has not independently verified those release claims or migrated the toolchain. A later-toolchain replay and ideally an independent checker pass are appropriate release goals; none of this demonstrates exploitation of a soundness bug here.

## Concrete research implications

- Preserve the exact finite-cylinder API as the semantic foundation of any generated proof.
- Require every future certificate to declare its integer domain, exact transition, all branch coverage, any boundary exceptions, and rank decrease. A spectral inequality alone proves none of those.
- Formalize the v6 signed defect/cancellation identity and critical equal-valuation cases before a global ledger conjecture. The ledger/constant-defect arithmetic is explicitly paper-only in `STATUS.md:47`.
- Use the 743 lasso as a mandatory regression obstruction for any proposed finite set of precision counters. A local hidden trace repairs one lasso but does not imply a finite complete trace set exists.
- A publishable intermediate success would be an explicit, independently checkable infinite family strictly larger than the existing A0 leaves, with all coverage obligations proved. It would improve the program even without approaching full Collatz.

## Fresh verification completed

- `DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean CollatzShadowing/ExactCylinders.lean` exited 0 with no output. This freshly elaborated the current exact-cylinder source against the installed pinned dependencies.
- `lake env lean --stdin`, importing `CollatzShadowing`, exited 0 while printing axiom dependencies for 13 selected declarations. The following 12 depend **only** on `[propext, Classical.choice, Quot.sound]`: `exact_shadowing`, `no_infinite_period_congruence_expansive`, `syracuseWordMatches_iff_exactResidue`, `repeatPhantomWord_matches_iff_exactResidue`, `syracuseWordPhantomPrecision_after_eval_add_sum`, `syracuseWordCycleContracting`, `evalSyracuseWord_lt_iff_source_above_barrier`, `concrete_shortTrace_lasso`, `hiddenTrace_lasso_tax`, `singular_outputs_separated_at_every_precision`, `Generated.k16s16KDeterministicGeneratedSpectralRadiusBound`, `classicalCollatz_of_uniformStrictDescent_provedBridge`.
- The thirteenth, `smallOddHasDirectDropWithin100Bool`, also depends on `CollatzShadowing.smallOddHasDirectDropWithin100Bool._native.native_decide.ax_1_1`, as expected and documented.
- Axiom absence does not eliminate explicit mathematical premises: the last headline Collatz implication still assumes `UniformStrictDescentHypothesis` in its type.
- This was a selected declaration audit, not exhaustive independent rechecking of all 49 project modules or of the Lean kernel.

Further design constraint: no finite acyclic certificate with a uniform bound on Syracuse depth can cover every positive integer, because sources `n=2^(m+1)-1` realize arbitrarily long all-one growth words. A finite global certificate must encode unbounded behavior by parametric loops and well-founded measures (or another genuine unbounded mechanism). Increasing trie depth alone cannot bypass this obstruction.
