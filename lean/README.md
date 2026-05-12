# Lean 4 Formalization — Collatz Spectral Reduction

Machine-verified proofs of the mathematical content of
[`../paper/collatz_spectral_reduction.tex`](../paper/collatz_spectral_reduction.tex).

> **Status: builds cleanly.** The Lean core for Lemma 3.1 and
> Corollary 3.4 is `sorry`-free. Phase 8 adds finite episode-graph and
> operator-certificate infrastructure, including a generated 37-state
> SCC certificate, Collatz-Wielandt certificate, and Mathlib
> spectral-radius bound for the empirical `K,b` matrix, plus a generated
> exact `T = 10` critical-symbolic transfer-matrix import and a generated
> `T = 10, j = 32` majority core/tail import.

## Goal

Produce a Lean 4 + Mathlib formalization of:

- **Lemma 3.1** of the paper (the exact congruential shadowing lemma)
- **Corollary 3.4** (no positive integer can shadow an expansive
  phantom forever)

Those two results are formalized and build without `sorry`. The current
extension work formalizes Phase-8 finite operator/certificate APIs that
support the later spectral-reduction layer.

## Build Instructions

```bash
cd lean
lake build
```

The first build downloads Mathlib cache artifacts and may require
several GB of disk space.

To verify a specific module:

```bash
lake build CollatzShadowing.Shadowing
```

Useful Phase-8 targets:

```bash
lake build CollatzShadowing.Bound
lake build CollatzShadowing.Generated.K16S16KExactCWSummary
lake build CollatzShadowing.Generated.K16S16KSCC
lake build CollatzShadowing.Generated.K16S16KBridge
lake build CollatzShadowing.Generated.T10CriticalSymbolic
lake build CollatzShadowing.Generated.T10J32HighBitTail
```

To check for proof placeholders:

```bash
rg -n "sorry|admit" CollatzShadowing *.lean
```

No output means the searched Lean files contain no explicit proof
placeholders.

## Main Modules

- `CollatzShadowing.Basic`: accelerated Syracuse map and valuation
  aliases.
- `CollatzShadowing.Phantom`: phantom words, affine folds, periodic
  exponent sums, and the 2-adic fixed point `q_w`.
- `CollatzShadowing.Syracuse2Adic`: the 2-adic Syracuse extension and
  natural-number bridge.
- `CollatzShadowing.Shadowing`: paper Section 3, Lemma 3.1.
- `CollatzShadowing.NoInfinite`: paper Corollary 3.4.
- `CollatzShadowing.EpisodeGraph`: Phase-8 directed-relation episode
  graph and SCC certificate interfaces.
- `CollatzShadowing.Operator`: finite phase states and
  `full = core + tail` operator decomposition API.
- `CollatzShadowing.Bound`: finite Collatz-Wielandt certificate API,
  cleared-denominator arithmetic bridge, evaluated row bridge, and
  finite `core + tail` spectral-radius bridge.
- `CollatzShadowing.Generated.K16S16KExactCWSummary`: generated exact
  37-state empirical `K,b` matrix certificate, including
  `k16s16KFiniteCWCertificate`.
- `CollatzShadowing.Generated.K16S16KSCC`: generated 37-state empirical
  `K,b` SCC certificate with hub-based finite walks.
- `CollatzShadowing.Generated.K16S16KBridge`: checked bridge showing
  that the generated SCC and CW certificates use the same `Fin 37`
  state ordering and labels; it also exposes the packaged object
  `k16s16KCertifiedComponentWithCW` and the concrete theorem
  `k16s16KSpectralRadiusBound`.
- `CollatzShadowing.Generated.T10CriticalSymbolic`: generated exact
  empirical `T = 10` critical-symbolic `TransferMatrix`, its
  row-substochasticity proof, and a baseline `OperatorDecomposition`
  with `core = full` and `tail = 0`.
- `CollatzShadowing.Generated.T10J32HighBitTail`: generated exact
  empirical `T = 10, j = 32` majority-signature `core` and `tail`
  matrices, with `full` definitionally equal to `core + tail`, generated
  row-substochasticity certificates, and
  `t10j32HighBitTailDecomposition`.

## Plan and progress

See [`TODO.md`](TODO.md) for the detailed phase-by-phase plan, current
status of each task, and the session log of what each AI/human
collaboration session accomplished.

## Methodology disclosure

The Lean formalization is being carried out by the project author
collaboratively with multiple AI assistants (Claude, Codex, Gemini),
following the same disclosed methodology as the rest of the project.
See [`../METHODOLOGY.md`](../METHODOLOGY.md) for the full disclosure.

The crucial difference between AI-assisted Lean formalization and
AI-assisted ordinary mathematics is that **Lean is a mechanical
verifier**: a Lean proof is correct if and only if `lake build`
succeeds with no `sorry`s and no errors. AI assistants can produce
plausible-looking incorrect Lean code, but unlike ordinary prose
proofs, the verification is automatic. Successful builds are
therefore much stronger evidence than AI-generated prose.

## License

Same as the parent repository: [CC BY 4.0](../LICENSE).
