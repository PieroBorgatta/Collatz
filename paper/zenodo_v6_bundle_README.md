# Version 6 supplementary source archive

This archive accompanies **Exact Exponent Cylinders, Precision Budgets, and
Singular Coding in Accelerated Syracuse Dynamics (v6)**. The complete paper
PDF is supplied separately on the same Zenodo record. The LaTeX source is
`paper/collatz_spectral_reduction_v6.tex`.

The archive is a **self-contained source snapshot of the Lean package**:
`lean/CollatzShadowing/**/*.lean`, the umbrella module, `lean/lakefile.toml`,
`lean/lake-manifest.json`, and `lean/lean-toolchain`. It includes earlier Lean
modules and generated certificate source because the v6 umbrella build
depends on them. No published v1–v5 PDF or unrelated project script is
included. The generated Lean certificates are sufficient to rebuild the
package; their historical Python generators are not part of this focused
archive. The new v6-facing Lean modules are:

- `A0InfiniteSubfamily.lean`
- `AffineTraceGraph.lean`
- `CycleConstraints.lean`
- `ExactCylinders.lean`
- `FirstBarrier.lean`
- `PrecisionTax.lean`
- `PrecisionTemplates.lean`
- `SwitchingPrecision.lean`
- `SyracuseSingularity.lean`
- `ThreeTraceObstruction.lean`

Their declarations and limitations are described in the paper. The modified
umbrella `lean/CollatzShadowing.lean` imports them. The corrected source
comment in `lean/CollatzShadowing/Syracuse2Adic.lean` accompanies the v4
erratum. `lean/scripts/phantom_taxonomy/switching_defect_probe.py` is a
finite arithmetic diagnostic, not a Lean theorem or a global Collatz proof.

## Reproduce the checks

Install the Lean toolchain manager `elan` and Python 3. From this archive's
root:

```sh
cd lean
lake build
cd ..
python3 lean/scripts/phantom_taxonomy/switching_defect_probe.py --depth 12
python3 scripts/build_zenodo_v6_bundle.py --verify-only
```

Lake resolves Mathlib from the included lock file. The toolchain is Lean
4.29.1, with Mathlib commit recorded in `lean/lake-manifest.json`. A newer
Lean release requires its own compatible Mathlib migration and fresh audit.
On macOS, an unaccepted Xcode license may obstruct `lake`; selecting the
installed Command Line Tools with
`DEVELOPER_DIR=/Library/Developer/CommandLineTools` can avoid that local
toolchain issue.

`paper/zenodo_v6_manifest.json` lists every archive payload entry with its
SHA-256 and byte count, plus the separately supplied PDF checksum. The
bundled verification command checks these source entries and checks the PDF
when it is placed at `paper/collatz_spectral_reduction_v6.pdf`.

This is version 6 of the concept record
<https://doi.org/10.5281/zenodo.20021537>, following the published v5
<https://doi.org/10.5281/zenodo.20554750>. The v6 paper explicitly corrects
the 2-adic continuity claim in published v4
<https://doi.org/10.5281/zenodo.20544464>. It does not prove the Collatz
conjecture.
