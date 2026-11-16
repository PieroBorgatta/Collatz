# CollatzShadowing standalone repository audit

16 November 2026. This audit concerns the separate standalone distribution,
not a new mathematical result. Its synchronization is part of the v7 release
milestone. The repository remains public.

## Identification and decision

- Repository: <https://github.com/PieroBorgatta/CollatzShadowing>.
- Visibility: public; default branch: `main`.
- Original remote main: `cfd5b203abb99eaeda216cf858c8d73d82dbcf61`.
- Last previous push reported by GitHub: 8 June 2026.
- The synchronization was prepared in a fresh clone, preserving the
  previous repository history and frozen releases.

**Update warranted.** The standalone package had 40 library Lean files,
including the entrypoint and 26 generated certificate modules. It did not
contain the v6 singularity correction or the later finite arithmetic
library. The synchronized package has 90 library Lean files: 89 under the
namespace directory plus the entrypoint, including the same 26 generated
certificate files. Both snapshots use Lean 4.29.1 and Mathlib 4.29.1, so no
toolchain migration is involved.

The initial export is pinned to canonical commit
`fd58ccd52b9fda44197d9c13afd6c1ae8200585e`. The standalone proof/configuration
identity records the exact verified bytes separately from later changes
to release documentation and its pinned source links.

## Prepared changes

1. A narrow, reproducible exporter copies the canonical library, Lake
   configuration, theorem-index documents, status and three strict
   November dependency audits. `SOURCE_MANIFEST.json` binds 101 exported
   files by original/destination path, size and SHA-256; Lean and
   configuration files are byte-for-byte copies. Parent-directory links
   in documentation are rewritten to the pinned canonical Git commit.
2. The English README identifies finite results and open hypotheses,
   states that the package does not prove Collatz, and separates the
   library from paper-only research and standalone prototypes.
3. The standalone CI verifies the source manifest, builds the package,
   permits only the nine specifically named legacy native axioms, and
   reruns three scoped strict November audits. API documentation deployment
   remains available through a manual `build_docs` input on `main`, rather
   than blocking every release push on the potentially lengthy docgen
   build. The [previous successful workflow](https://github.com/PieroBorgatta/CollatzShadowing/actions/runs/27125118486)
   took approximately 2h41m in total, of which approximately 2h36m was
   documentation generation.
4. `AGENTS.md` and the README record the user's new policy: keep the
   repository public, and push only a completed agreed milestone or an
   explicit user-authorized push. Local development is not automatically
   published after every session.

The standalone is not an uncontrolled mirror of the whole research tree:
experiments, external formal projects, credentials, manuscript drafts,
package caches and standalone maximal-gain prototypes are excluded.

## Licensing

The old standalone package explicitly used MIT; the current canonical
snapshot uses CC BY 4.0. The original MIT notice is preserved byte for byte
as `LICENSE-MIT`, and earlier MIT grants are expressly not revoked. The
current exported snapshot's `LICENSE` and SPDX value match the canonical
CC BY 4.0 source. README and `PROVENANCE.md` explain this version scope
prominently, rather than silently applying MIT to new CC BY material.

## Validation and publication handoff

`python3 tools/export_from_collatz.py --check` verifies every exported file
and the complete Lean source inventory. `git diff --check` passes.

The standalone build uses an empty standalone `.lake/build` directory and
reuses only the canonical checkout's existing dependency packages. Its
library output remains separate from the concurrent canonical build.
**The build passed all 3404 jobs**, exit code 0, in 2052.495 seconds.
Two existing nonfatal style warnings concerned an unused variable and
`simpa` versus `simp`; the proof sources were not changed to silence them.

All three strict dependency audits then passed with exit code 0:

| Audit | Verified scope |
|---|---|
| 13 November | 69 named public roots and their transitive dependencies |
| 15 November | All 136 compiled declarations in seven modules, including 14 encoded-private declarations |
| Additional finite catalogue modules | All 68 compiled declarations in four modules, including five encoded-private declarations |

The allowed transitive axioms in these scopes are only `propext`,
`Classical.choice` and `Quot.sound`. This does not remove the nine explicitly
allowed native certificates elsewhere in the historical library.

The standalone `verification/` directory contains the build log, three
audit logs, `build_receipt.json`, `audits_receipt.json` and
`source_identity.json`. The 96 proof/audit/configuration files have aggregate
SHA-256 `7aeef562183ea57603dfbd11687432ff0fab50538f8ffdb0ac3230f0b4773a3e`
under the recorded identity algorithm. They use Lean 4.29.1, compiler commit
`f72c35b3f637c8c6571d353742168ab66cc22c00`, and Mathlib 4.29.1, commit
`5e932f97dd25535344f80f9dd8da3aab83df0fe6`.

These are a fresh standalone package build and scoped dependency checks,
not a cold Mathlib rebuild, a toolchain migration or an independent-kernel
replay. Later documentation-only exports retain this verification evidence
only when the recorded proof/configuration identity remains unchanged.

Publication status and version identifiers are tracked in the standalone
README. The stable concept DOI is `10.5281/zenodo.20021537`; the preceding
v6 DOI is `10.5281/zenodo.22936057`. Public pushes are reserved for completed,
reviewed milestones or an explicit user instruction.
