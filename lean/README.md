# CollatzShadowing — a Lean 4 + Mathlib formalization

A self-contained Lean 4 (Lake) library formalizing the verified core of the
*Phantom Orbit Shadowing* program on the Collatz conjecture. The
`CollatzShadowing` sources are **`sorry`-, `admit`- and `axiom`-free**.

> This library does **not** prove the Collatz conjecture. It formalizes a
> shadowing lemma, a no-infinite-shadowing corollary, an expanding-cycle
> exclusion, finite Collatz–Wielandt spectral-radius certificates, and an
> elementary descent bridge — the rigorously verified part of the program.
> See the project paper (v4) and [`../README.md`](../README.md) for scope.

## At a glance

- **14 AI-authored modules** (~7,800 lines, ~300 theorems/lemmas) — Lean proofs written by the AI line by line.
- **26 machine-generated certificate modules** (~43,500 lines) under
  `CollatzShadowing/Generated/`, emitted by the Python generators in
  `../scripts/phantom_taxonomy/` and checked by Lean.
- Toolchain: **Lean v4.29.1 + Mathlib v4.29.1** (pinned in `lean-toolchain`
  and `lakefile.toml`).
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

## Headline results

| Result | Declaration | Module |
|---|---|---|
| Exact congruential shadowing (Lemma 3.1) | `exact_shadowing`, `exact_shadowing_periods` | `Shadowing` |
| No infinite (periodic) shadowing (Cor. 3.4) | `no_infinite_period_congruence_expansive` | `NoInfinite` |
| No positive integer on an expanding cycle | `no_positive_endpoint_eventually_periodic_expansive_congruence` | `NoInfinite` |
| Generic weighted Collatz–Wielandt bound | `spectralRadius_le_of_finiteCWCertificate` | `Bound` |
| Single-node spectral bound `ρ ≤ 97/2000` | `t10j32HighBitTailSpectralRadiusBound_97_2000` | `Generated/T10J32HighBitTailCW` |
| Deterministic `(K,b)` bound `< 3/4` (`K₀=16`) | `k16s16KDeterministicGeneratedSpectralRadiusBound` | `Generated/K16S16KDeterministicCW` |
| Finite weak row-`L¹` bridge | `WeakBridge.weighted_action_diff_le` | `WeakBridge` |
| High-`ν₂` source-tail mass `≤ 2⁻ᴿ` | `WeakBridge.TailCount.dyadic_tail_count_mul_le` | `WeakBridge` |
| Descent ⇒ Collatz (elementary) | `classicalCollatz_of_uniformStrictDescent_provedBridge` | `CollatzBridge` |

## Modules

**Shadowing core**
- `Basic` — accelerated Syracuse map `S`, valuation `ν₂`.
- `Phantom` — phantom words, affine fold, `C_w`, `A_w`, fixed point `q_w = C_w/(2^A − 3^L)`.
- `Syracuse2Adic` — the 2-adic extension `S̃ : ℤ₂ → ℤ₂` and the `ℕ` bridge.
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
