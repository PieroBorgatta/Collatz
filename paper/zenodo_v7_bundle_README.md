# Version 7 supplementary source archive

This archive accompanies **Finite Orbit Budgets, Arithmetic Transport
Barriers, and Paired-Path Certificates for Collatz**, version 7, dated
16 November 2026. The final paper PDF is supplied separately on the same
Zenodo record. Its checksum is recorded in
`paper/zenodo_v7_manifest.json`; the archive contains its complete LaTeX
source, including the two mathematical sections and bibliography.

The concept record is <https://doi.org/10.5281/zenodo.20021537>.
The version-specific DOI, reserved before publication, is
<https://doi.org/10.5281/zenodo.24284425>.
The previous published version is v6,
<https://doi.org/10.5281/zenodo.22936057>. The proof-source baseline for
this continuation is commit
`fd58ccd52b9fda44197d9c13afd6c1ae8200585e`. The manifest identifies the
actual release bytes; a mutable branch name is not their identifier.

## Contents and mathematical status

The focused archive includes:

- All **90 canonical Lean source files**, comprising the umbrella module
  and `lean/CollatzShadowing/**/*.lean`, together with the three Lake and
  toolchain pins. The package includes its generated finite-certificate
  source, so historical Python generators are not needed to compile it.
- The v7 paper source, sections, bibliography and publication metadata.
- Three English audits covering the finite core, literature and novelty,
  and the separate `CollatzShadowing` repository export.
- The three strict dependency-audit Lean files at their original paths;
  the fresh pinned build and audit logs; finite paper-certificate results;
  frozen earlier-PDF checks; the LaTeX build record; and the release receipt.
- A finite arithmetic checker for selected paper certificates, this
  archive builder/verifier, the license, and the research methodology.

Only the finite arithmetic core has corresponding checked Lean
declarations. The transport barriers, conditional off-path budget and
paired-path arguments are paper proofs. The conditional budget keeps its
external logarithmic-density premise explicit. The Python certificate
checker verifies selected finite identities; it does not turn those
paper proofs into Lean theorems or establish global coverage.

The archive contains no dependency cache, downloaded external paper,
Italian historical research note, or earlier paper PDF. The root
repository README and status files are omitted because publication can
subsequently update them. The three historical audit sources are included
because they are needed to reproduce the selected new audits.

## Verify the distributed files

Python 3.10 or later is sufficient for the archive checker. From the
extracted archive root:

```sh
python3 scripts/build_zenodo_v7_bundle.py --verify-only
```

This checks every manifest payload path, role, byte count and SHA-256,
including the builder itself. If the supplementary ZIP is present beside
the extracted files, it also checks its complete member list, rejects
duplicate or unsafe members, and verifies every archived checksum and
the archived manifest. If only the extracted source tree is present,
the command explicitly reports source-only verification.

To check the separate PDF as well, place it at
`paper/collatz_spectral_reduction_v7.pdf` before running that command.
Without the PDF, its expected checksum remains available in the manifest,
but the verifier explicitly reports that it has not checked those bytes.
These integrity checks do not establish mathematical correctness.

## Rebuild the Lean package and selected audits

Install `elan`, the Lean toolchain manager, and the system tools needed
by Lake. From the archive root:

```sh
cd lean
lake build
lake env lean ../notes/research_sprint_2026-11-13/verification/AllNewDependencyAudit.lean
lake env lean ../notes/research_sprint_2026-11-15/verification/AllNewDependencyAudit.lean
lake env lean ../notes/research_sprint_2026-11-15_three_hours/verification/AllNewDependencyAudit.lean
cd ..
python3 scripts/check_v7_paper_certificates.py
```

Lake obtains the dependencies specified by `lean/lake-manifest.json`.
The release pins Lean and Mathlib to **4.29.1**. A fresh installation can
require substantial downloads and compilation; the release's recorded
3404-job build was incremental and used existing dependencies. The logs
in `notes/v7_release_2026-11-16/verification/` are the recorded release
outputs, not an assertion that this source distribution includes all
cached dependency binaries.

Each selected audit enumerates declarations in its stated scope,
including generated and encoded-private declarations where specified,
and rejects transitive axioms outside `propext`, `Classical.choice`, and
`Quot.sound`. These selected audits do not make that claim for every
historical module in the package. Earlier `native_decide` certificates
retain their documented native compilation assumptions.

The pinned version predates later documented Lean kernel soundness
fixes. Acceptance by this pinned toolchain is the reported verification
status. No exploit has been established in these sources, and no
independent current-kernel replay is claimed. A compatible toolchain and
Mathlib migration followed by a fresh independent checker replay remains
separate work. The `CollatzShadowing` repository is an export of the
canonical package, not an independent proof implementation.

## Compile the paper

With a LaTeX installation supplying the packages named in the source:

```sh
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error collatz_spectral_reduction_v7.tex
cd ..
```

Alternatively, run `pdflatex` on that file twice. Bibliography entries are
included as LaTeX source; no external bibliography database is needed.
A local rebuild can produce different PDF metadata or binary bytes, so
the manifest hash identifies the distributed PDF, not every compatible
recompilation. Rebuilding the PDF overwrites that local file and requires
a newly generated manifest if it is to become a new release artifact.

## Rebuild the source archive

Once the final PDF and all declared release files exist:

```sh
python3 scripts/build_zenodo_v7_bundle.py
python3 scripts/build_zenodo_v7_bundle.py --verify-only
```

The builder writes `paper/zenodo_v7_manifest.json` and
`collatz_spectral_reduction_v7_supplementary.zip`. It snapshots the input
bytes, orders members lexicographically, fixes ZIP timestamps to
16 November 2026, and fixes member permissions and compression settings.
Identical inputs under the same Python/zlib implementation reproduce the
same ZIP bytes. Symlink components, hidden or escaping paths, missing
inputs and an unexpected number of canonical Lean sources are rejected.
No `.lake` directory or external manuscript is copied into the archive.

Rebuilding the archive changes its manifest to bind the then-current
files. To check the distributed snapshot, use `--verify-only` first.
The release supplies finite results and a precise research boundary; it
does not prove Collatz, universal descent, a universal smaller-source
cover, or exclusion of every positive cycle.
