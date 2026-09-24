#!/usr/bin/env python3
"""Build or verify the focused, self-contained Zenodo v6 source archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PDF = Path("paper/collatz_spectral_reduction_v6.pdf")
MANIFEST = Path("paper/zenodo_v6_manifest.json")
ARCHIVE = Path("collatz_spectral_reduction_v6_supplementary.zip")
FIXED_ZIP_DATE = (2026, 9, 24, 0, 0, 0)

V6_LEAN_MODULES = {
    "A0InfiniteSubfamily.lean",
    "AffineTraceGraph.lean",
    "CycleConstraints.lean",
    "ExactCylinders.lean",
    "FirstBarrier.lean",
    "PrecisionTax.lean",
    "PrecisionTemplates.lean",
    "SwitchingPrecision.lean",
    "SyracuseSingularity.lean",
    "ThreeTraceObstruction.lean",
}

STATIC_FILES = {
    "LICENSE": "license",
    "paper/collatz_spectral_reduction_v6.tex": "v6-paper-source",
    "paper/zenodo_v6_title.md": "zenodo-metadata",
    "paper/zenodo_v6_description.html": "zenodo-metadata",
    "paper/zenodo_v6_bundle_README.md": "archive-readme",
    "lean/lakefile.toml": "lean-build-pin",
    "lean/lake-manifest.json": "lean-build-pin",
    "lean/lean-toolchain": "lean-build-pin",
    "lean/README.md": "lean-documentation",
    "lean/STATUS.md": "lean-documentation",
    "lean/TODO.md": "lean-documentation",
    "lean/CollatzShadowing/THEOREM_INDEX.md": "lean-documentation",
    "lean/scripts/phantom_taxonomy/switching_defect_probe.py": "v6-diagnostic",
    "notes/collatz_literature_audit_2026-09-24.md": "v6-literature-audit",
    "scripts/build_zenodo_v6_bundle.py": "archive-builder-and-verifier",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload() -> dict[str, str]:
    files = dict(STATIC_FILES)
    # Only the canonical package. A recursive search from lean/ would also
    # pick up hidden Claude worktrees with stale duplicate Lean files.
    lean_sources = [ROOT / "lean/CollatzShadowing.lean"]
    lean_sources.extend(sorted((ROOT / "lean/CollatzShadowing").rglob("*.lean")))
    for source in lean_sources:
        name = source.relative_to(ROOT).as_posix()
        if any(part.startswith(".") for part in source.relative_to(ROOT).parts):
            raise RuntimeError(f"Hidden path under canonical package: {name}")
        files[name] = (
            "v6-lean-module"
            if source.name in V6_LEAN_MODULES
            else "lean-source-dependency"
        )
    seen_new = {Path(path).name for path, role in files.items() if role == "v6-lean-module"}
    if seen_new != V6_LEAN_MODULES:
        raise RuntimeError(f"Expected v6 modules not found: {sorted(V6_LEAN_MODULES - seen_new)}")
    return dict(sorted(files.items()))


def zipinfo(name: str) -> ZipInfo:
    info = ZipInfo(name, FIXED_ZIP_DATE)
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = ZIP_DEFLATED
    return info


def verify_source_files(manifest: dict) -> None:
    errors = []
    for entry in manifest["files"]:
        source = ROOT / entry["path"]
        if not source.is_file():
            errors.append(f"missing {entry['path']}")
            continue
        data = source.read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            errors.append(f"checksum mismatch {entry['path']}")
    pdf_path = ROOT / manifest["paper_pdf"]["path"]
    if pdf_path.is_file():
        data = pdf_path.read_bytes()
        if len(data) != manifest["paper_pdf"]["bytes"] or digest(data) != manifest["paper_pdf"]["sha256"]:
            errors.append(f"checksum mismatch {pdf_path.relative_to(ROOT)}")
        else:
            print(f"PDF OK: {pdf_path.relative_to(ROOT)}")
    else:
        print("PDF not present in extracted source archive; it is supplied separately")
    if errors:
        raise RuntimeError("; ".join(errors))
    print(f"Source checksums OK: {len(manifest['files'])} payload entries")


def verify_archive(manifest_bytes: bytes, manifest: dict) -> None:
    archive_path = ROOT / ARCHIVE
    with ZipFile(archive_path) as archive:
        expected = {entry["path"] for entry in manifest["files"]} | {MANIFEST.as_posix()}
        actual = set(archive.namelist())
        if actual != expected:
            raise RuntimeError(f"ZIP members differ: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
        if archive.read(MANIFEST.as_posix()) != manifest_bytes:
            raise RuntimeError("ZIP manifest differs from saved manifest")
        for entry in manifest["files"]:
            data = archive.read(entry["path"])
            if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
                raise RuntimeError(f"ZIP checksum mismatch: {entry['path']}")
    print(f"ZIP OK: {ARCHIVE} ({archive_path.stat().st_size} bytes, SHA-256 {digest(archive_path.read_bytes())})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="verify files against the saved manifest")
    args = parser.parse_args()

    if args.verify_only:
        manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        verify_source_files(manifest)
        if (ROOT / ARCHIVE).is_file():
            verify_archive((ROOT / MANIFEST).read_bytes(), manifest)
        return

    pdf_path = ROOT / PDF
    if not pdf_path.is_file():
        raise SystemExit(f"Final v6 PDF required before freezing the archive: {pdf_path}")
    pdf_data = pdf_path.read_bytes()
    if not pdf_data.startswith(b"%PDF-"):
        raise SystemExit(f"Not a PDF: {pdf_path}")

    entries = []
    for name, role in payload().items():
        source = ROOT / name
        if not source.is_file():
            raise SystemExit(f"Required source missing: {source}")
        if source.is_symlink() or any(parent.is_symlink() for parent in source.parents if parent != ROOT and ROOT in parent.parents):
            raise SystemExit(f"Symlink is not allowed in the archive: {source}")
        if not source.resolve().is_relative_to(ROOT.resolve()):
            raise SystemExit(f"Path escapes repository root: {source}")
        data = source.read_bytes()
        entries.append({"path": name, "role": role, "bytes": len(data), "sha256": digest(data)})

    manifest = {
        "schema": "collatz-zenodo-v6-source-manifest-1",
        "version": "v6",
        "concept_doi": "10.5281/zenodo.20021537",
        "previous_version_doi": "10.5281/zenodo.20554750",
        "lean_toolchain": (ROOT / "lean/lean-toolchain").read_text(encoding="utf-8").strip(),
        "paper_pdf": {"path": PDF.as_posix(), "bytes": len(pdf_data), "sha256": digest(pdf_data), "distribution": "separate file on the same Zenodo record"},
        "files": entries,
    }
    manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    (ROOT / MANIFEST).write_bytes(manifest_bytes)

    with ZipFile(ROOT / ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for entry in entries:
            archive.writestr(zipinfo(entry["path"]), (ROOT / entry["path"]).read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
        archive.writestr(zipinfo(MANIFEST.as_posix()), manifest_bytes, compress_type=ZIP_DEFLATED, compresslevel=9)

    verify_source_files(manifest)
    verify_archive(manifest_bytes, manifest)


if __name__ == "__main__":
    main()
