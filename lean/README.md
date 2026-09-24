# CollatzShadowing — a Lean 4 + Mathlib formalization

A self-contained Lean 4 (Lake) library formalizing the verified core of the
*Phantom Orbit Shadowing* program on the Collatz conjecture. The
`CollatzShadowing` sources have **no `sorry`, `admit`, or project-declared
`axiom`**. The trusted base is qualified below.

> This library does **not** prove the Collatz conjecture. It formalizes a
> shadowing lemma, a no-infinite-shadowing corollary, an expanding-cycle
> exclusion, finite Collatz–Wielandt spectral-radius certificates, and an
> elementary descent bridge — the rigorously verified part of the program.
> Published v6 is the frozen 24 September 2026 snapshot. This working
> tree also contains subsequent developments; see [`STATUS.md`](STATUS.md) and
> [`../README.md`](../README.md) for current scope.

## At a glance

- AI-authored proof modules, including the later precision, cycle, and
  first-barrier developments. Current counts and the historical v5 snapshot
  are separated in [`../notes/PROJECT_STATISTICS.md`](../notes/PROJECT_STATISTICS.md).
- **26 machine-generated certificate modules** (~43,500 lines) under
  `CollatzShadowing/Generated/`, emitted by the Python generators in
  `../scripts/phantom_taxonomy/` and checked by Lean.
- Toolchain: **Lean v4.29.1 + Mathlib v4.29.1** (pinned in `lean-toolchain`
  and `lakefile.toml`); newer versions have not been tested.
- Full declaration → file map: [`CollatzShadowing/` theorem index](CollatzShadowing/THEOREM_INDEX.md).

## Build

```bash
cd lean
lake exe cache get   # download the Mathlib precompiled cache (several GB)
lake build           # build the whole project
```

Verify a single module, e.g. the shadowing core:

```bash
lake build CollatzShadowing.Shadowing
lake build CollatzShadowing.NoInfinite
```

Check there are no proof placeholders (no output = clean):

```bash
grep -rnE 'sorry|admit|^[[:space:]]*axiom' CollatzShadowing --include='*.lean'
```

This source scan establishes only that no placeholder or project-declared
axiom appears. The library currently uses `native_decide` in a small number
of declarations; an axioms audit of headline results is needed to state
their precise trusted base. See [`STATUS.md`](STATUS.md).

## Headline results

| Result | Declaration | Module |
|---|---|---|
| Exact congruential shadowing (Lemma 3.1) | `exact_shadowing`, `exact_shadowing_periods` | `Shadowing` |
| No infinite (periodic) shadowing (Cor. 3.4) | `no_infinite_period_congruence_expansive` | `NoInfinite` |
| No positive integer on an expanding cycle | `no_positive_endpoint_eventually_periodic_expansive_congruence` | `NoInfinite` |
| Distinct outputs arbitrarily close to the 2-adic singular point in finite precision | `singular_outputs_separated_at_every_precision` | `SyracuseSingularity` |
| Exact congruence for every nonempty positive-exponent word and its repeated blocks (full build passed) | `syracuseWordMatches_iff_exactResidue`, `repeatPhantomWord_matches_iff_exactResidue` | `ExactCylinders` |
| Generic weighted Collatz–Wielandt bound | `spectralRadius_le_of_finiteCWCertificate` | `Bound` |
| Single-node spectral bound `ρ ≤ 97/2000` | `t10j32HighBitTailSpectralRadiusBound_97_2000` | `Generated/T10J32HighBitTailCW` |
| Deterministic `(K,b)` bound `ρ ≤ 3/4` (`K₀=16`) | `k16s16KDeterministicGeneratedSpectralRadiusBound` | `Generated/K16S16KDeterministicCW` |
| Finite weak row-`L¹` bridge | `WeakBridge.weighted_action_diff_le` | `WeakBridge` |
| High-`ν₂` source-tail mass `≤ 2⁻ᴿ` | `WeakBridge.TailCount.dyadic_tail_count_mul_le` | `WeakBridge` |
| Descent ⇒ Collatz (elementary) | `classicalCollatz_of_uniformStrictDescent_provedBridge` | `CollatzBridge` |
| Exact precision loss for a matched expansive word | `syracuseWordPhantomPrecision_after_eval_add_sum` | `PrecisionTax` |
| Finite bound on consecutive repetitions of that word | `syracuseWord_matched_block_precision_budget`, `no_infinite_matched_expansive_word` | `PrecisionTax` |
| Necessary equation and contractivity for a positive cycle | `syracuseWordCycleEquationNat`, `syracuseWordCycleContracting` | `CycleConstraints` |
| Exact first-barrier test for a matched finite word | `evalSyracuseWord_lt_iff_source_above_barrier` | `FirstBarrier` |
| Total affine weight of any finite set of visits x→R is at most `R*(3*R+1)/x`, including periodic targets | `WeightedVisits.sum_weight_visits_le` | `WeightedVisits` |

## Modules

**Shadowing core**
- `Basic` — accelerated Syracuse map `S`, valuation `ν₂`.
- `Phantom` — phantom words, affine fold, `C_w`, `A_w`, fixed point `q_w = C_w/(2^A − 3^L)`.
- `Syracuse2Adic` — a total 2-adic map agreeing with `S` on positive odd
  integers. The map is discontinuous at `−1/3`; it is not a
  continuous extension to all `ℤ₂`.
- `SyracuseSingularity` — two families of positive odd natural inputs with
  numerator divisible by arbitrarily large powers of `2` but accelerated
  outputs fixed at `1` and `7`.
- `Auxiliary` — supporting lemmas (ultrametric stability, `B`-recursion, …).
- `Shadowing` — Lemma 3.1.
- `NoInfinite` — Cor. 3.4 and the expanding-cycle exclusion.

**Finite operator / certificate layer**
- `EpisodeGraph` — directed-relation episode graph, SCC interfaces.
- `Operator` — finite phase states, `full = core + tail` decomposition.
- `Bound` — finite Collatz–Wielandt certificate API and the spectral-radius bridge to Mathlib's `spectralRadius`.

**Phase-10 finite bridges**
- `WeakBridge` — the A0 weak-bridge finite lemmas: weighted row-`L¹` action bound, the exact high-`ν₂` tail count, the `BitLength`/dyadic-boundary development, and the `LabelSplit` schema.
- `CollatzBridge` — the elementary descent bridge (`UniformStrictDescentHypothesis ⇒ Collatz`) and the conditional first-barrier machinery (open hypotheses isolated as named `Prop`s, not faked).

**Later arithmetic and trace results**
- `A0InfiniteSubfamily` — strict descent on two explicit infinite residue
  subfamilies of the A0 source cylinder.
- `PrecisionTax` and `PrecisionTemplates` — exact 2-adic precision loss
  under repeated matched expansive words, including `[1]`, `[1,2]`,
  and `[2,1]`; the bound is local to one fixed word.
- `SwitchingPrecision` and `AffineTraceGraph` — compatible changes of an
  affine phantom label and obstructions to arbitrary relabeling or a common
  scalar rational fixed point for incompatible cycles.
- `ThreeTraceObstruction` — an explicit lasso showing that the three short
  precision counters alone do not form a global decreasing rank.
- `CycleConstraints` — necessary equation, contractivity, modular
  divisibility, and a first-contracting-prefix estimate for a hypothetical
  positive cycle.
- `ExactCylinders` — a finite word matches exactly when its affine
  numerator is `2^A` modulo `2^(A+1)`; `k` repetitions use modulus
  `2^(kA+1)`. The unique residue class and density are paper-level
  deductions, not Lean declarations here.
- `FirstBarrier` — exact residue and affine threshold tests for a matched
  finite word. These do not establish a barrier for every infinite orbit.

**Generated/** — finite certificates emitted by AI-written Python generators (CW row witnesses, residue-cell matrices, SCC walks). Verified by Lean; not reasoned line by line.

`Inventory` / `EpisodeInventory` are Mathlib-API scratch buffers, not proof content.

## Reusing this library

`lean/` is already a standalone Lake project. To depend on it, point a
`require` at this repository (subdirectory `lean`) at the pinned toolchain.
A citable, frozen snapshot is on Zenodo (concept DOI
[10.5281/zenodo.20021537](https://doi.org/10.5281/zenodo.20021537)).

## Methodology

Built by the author in cross-AI collaboration (Claude, Codex, Gemini), with
all formal claims funnelled through Lean: a proof counts only if `lake build`
succeeds with no `sorry`. See [`../METHODOLOGY.md`](../METHODOLOGY.md) and the
phase log in [`TODO.md`](TODO.md).

## License

[CC BY 4.0](../LICENSE), as the parent repository.
