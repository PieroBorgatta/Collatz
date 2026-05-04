# Lean 4 Formalization — Collatz Spectral Reduction

Machine-verified proofs of the mathematical content of
[`../paper/collatz_spectral_reduction.tex`](../paper/collatz_spectral_reduction.tex).

> **Status: Not yet built.** See [`TODO.md`](TODO.md) for the
> formalization plan and current progress.

## Goal

Produce a Lean 4 + Mathlib formalization of:

- **Lemma 3.1** of the paper (the exact congruential shadowing lemma)
- **Corollary 3.4** (no positive integer can shadow an expansive
  phantom forever)

When complete, these will be incorporated into a revised version (`v2`)
of the preprint on Zenodo.

## Build instructions (once Phase 0 is complete)

```bash
cd lean
lake build
```

The first build will download Mathlib and compile it; this may take
30 minutes to an hour and require several GB of disk space.

To verify a specific module:

```bash
lake build CollatzShadowing.Shadowing
```

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
