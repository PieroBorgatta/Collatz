# Reproduction and independent-review protocol

This protocol separates a fresh-machine replay with the pinned Lean compiler
from independent kernel checking and mathematical review. The latter two are
not claimed by a successful GitHub Actions run.

1. Read `verification_manifest.json` and check out its `verified_code_commit`
   in a fresh clone. Verify the recorded source hashes before building.
2. Use the repository's exact `lean/lean-toolchain` and `lake-manifest.json`.
   The current main library uses Lean/Mathlib 4.29.1; do not combine it with
   the separate predecessor adapter's Lean 4.30.0-rc2 environment.
3. Run `lake build` from `lean/` and preserve the complete output. Mathlib
   cache reuse must be recorded; it is not a rebuild of every dependency.
4. Run `lake env lean ../notes/post_v6_transport_2026-09-24/DependencyAudit.lean`.
   All eleven roots and the complete named type/body traversal must pass;
   the only permitted axioms are `propext`, `Classical.choice`, `Quot.sound`.
5. Run `python3 ../notes/post_v6_transport_2026-09-24/transport_probe.py --output /tmp/tower-transport-results.json`
   and compare the JSON to the archived result. These finite checks supplement
   the Lean theorems; they do not replace them.
6. Independently read the elaborated statements of
   `finite_suffix_residue`, `phaseC_tower_burst`,
   `tower_finite_suffix_arbitrarily_large`, and `finite_suffix_bounded_iff`.
   Check the domain restrictions, the final parity bit, and the quantifier
   order against `RESULTS_IT.md` and `REVIEW_IT.md`.

A separate future portability audit should rebuild on a corrected, mutually
compatible Lean/Mathlib release, preserving the old verification snapshot.
For an independent kernel implementation, verify its supported export format
and complete dependency support before treating its output as a replay.
Neither a command wrapper around Lean nor a second run of `#print axioms`
constitutes such independent kernel checking. No untested independent-checker
command is supplied here.

On the development Mac, prefix Git/Lake commands with
`DEVELOPER_DIR=/Library/Developer/CommandLineTools`.
