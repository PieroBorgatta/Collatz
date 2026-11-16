#!/usr/bin/env python3
"""Build or verify the focused, reproducible Zenodo v7 source archive.

Only Python's standard library is required. This verifies artifact integrity;
it does not execute Lean, compile the paper, or establish theorem correctness.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PDF = "paper/collatz_spectral_reduction_v7.pdf"
MANIFEST = "paper/zenodo_v7_manifest.json"
ARCHIVE = "collatz_spectral_reduction_v7_supplementary.zip"
FIXED_ZIP_DATE = (2026, 11, 16, 0, 0, 0)
EXPECTED_LEAN_FILES = 90
PROOF_BASELINE = "fd58ccd52b9fda44197d9c13afd6c1ae8200585e"
SECTION_ROOT = "paper/v7_sections"
RELEASE_ROOT = "notes/v7_release_2026-11-16"

STATIC_FILES = {
    "LICENSE": "license",
    "METHODOLOGY.md": "research-methodology",
    "paper/collatz_spectral_reduction_v7.tex": "paper-source",
    "paper/zenodo_v7_title.md": "publication-metadata",
    "paper/zenodo_v7_description.html": "publication-metadata",
    "paper/zenodo_v7_references.json": "publication-metadata",
    "paper/zenodo_v7_bundle_README.md": "archive-readme",
    "lean/lakefile.toml": "lean-build-pin",
    "lean/lake-manifest.json": "lean-build-pin",
    "lean/lean-toolchain": "lean-build-pin",
    f"{RELEASE_ROOT}/FINITE_CORE_AUDIT_EN.md": "english-semantic-audit",
    f"{RELEASE_ROOT}/LITERATURE_NOVELTY_AUDIT_EN.md": "english-literature-audit",
    f"{RELEASE_ROOT}/SHADOWING_REPOSITORY_AUDIT_EN.md": "english-export-audit",
    "notes/research_sprint_2026-11-13/verification/AllNewDependencyAudit.lean": "strict-dependency-audit-source",
    "notes/research_sprint_2026-11-15/verification/AllNewDependencyAudit.lean": "strict-dependency-audit-source",
    "notes/research_sprint_2026-11-15_three_hours/verification/AllNewDependencyAudit.lean": "strict-dependency-audit-source",
    f"{RELEASE_ROOT}/verification/main_build.log": "recorded-pinned-build",
    f"{RELEASE_ROOT}/verification/november13_axioms.log": "recorded-strict-dependency-audit",
    f"{RELEASE_ROOT}/verification/november15_axioms.log": "recorded-strict-dependency-audit",
    f"{RELEASE_ROOT}/verification/catalogue_collision_axioms.log": "recorded-strict-dependency-audit",
    f"{RELEASE_ROOT}/verification/paper_certificates.json": "recorded-finite-paper-certificates",
    f"{RELEASE_ROOT}/verification/frozen_pdfs.log": "recorded-frozen-pdf-check",
    f"{RELEASE_ROOT}/verification/latex_build.json": "recorded-paper-build",
    f"{RELEASE_ROOT}/verification/release_receipt.json": "release-verification-receipt",
    "scripts/check_v7_paper_certificates.py": "finite-paper-certificate-checker",
    "scripts/build_zenodo_v7_bundle.py": "archive-builder-and-verifier",
}

TRUST_LIMITS = [
    "The manifest and archive verifier check source integrity, not mathematical correctness.",
    "The finite arithmetic core has corresponding Lean declarations; the transport, conditional-budget and paired-path arguments are paper proofs.",
    "The three selected strict audits inspect transitive axioms only in their stated module scopes; they do not certify every historical module.",
    "The full package also contains earlier native_decide certificates with their documented native compilation assumptions.",
    "Lean and Mathlib are pinned to v4.29.1, predating later documented kernel soundness fixes; no independent current-kernel replay is claimed.",
    "Recorded builds can reuse dependency caches; this archive is not a cold dependency rebuild or an independent proof implementation.",
    "The paper's external analytic inputs and cited manuscripts are not imported as newly checked Lean theorems.",
    "The release proves neither Collatz nor universal descent, a smaller-source cover, or exclusion of every positive cycle.",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked_name(name: str) -> str:
    """Accept only canonical relative POSIX names usable on all hosts."""
    if not isinstance(name, str) or not name or any(c in name for c in "\\\x00:"):
        raise ValueError(f"Unsafe archive path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or path.as_posix() != name:
        raise ValueError(f"Noncanonical archive path: {name!r}")
    if any(part in (".", "..") or part.startswith(".") for part in path.parts):
        raise ValueError(f"Hidden or escaping archive path: {name!r}")
    return name


def checked_path(name: str, *, required: bool = True) -> Path:
    """Reject symlink components before reading or writing beneath ROOT."""
    checked_name(name)
    source = ROOT
    for part in PurePosixPath(name).parts:
        source = source / part
        if source.is_symlink():
            raise ValueError(f"Symlink is not allowed: {name}")
    if not source.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f"Path escapes the source root: {name}")
    if required and not source.is_file():
        raise ValueError(f"Required regular source file missing: {name}")
    if source.exists() and not source.is_file():
        raise ValueError(f"Expected a regular file: {name}")
    return source


def discover(folder: str, suffix: str) -> list[str]:
    checked_name(folder)
    base = ROOT / folder
    # Check every directory component before walking the selected source tree.
    if not base.is_dir():
        raise ValueError(f"Required source directory missing: {folder}")
    cursor = ROOT
    for part in PurePosixPath(folder).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"Symlink source directory is not allowed: {folder}")
    files = []
    for source in sorted(base.rglob("*")):
        name = source.relative_to(ROOT).as_posix()
        if source.is_symlink():
            raise ValueError(f"Symlink under source directory: {name}")
        if source.is_file() and source.suffix == suffix:
            checked_path(name)
            files.append(name)
    return files


def payload() -> dict[str, str]:
    files = dict(STATIC_FILES)
    lean = ["lean/CollatzShadowing.lean"]
    lean.extend(discover("lean/CollatzShadowing", ".lean"))
    if len(lean) != EXPECTED_LEAN_FILES:
        raise ValueError(f"Expected {EXPECTED_LEAN_FILES} canonical Lean sources, found {len(lean)}")
    for name in lean:
        files[name] = "canonical-lean-source"
    sections = discover(SECTION_ROOT, ".tex")
    required_sections = {f"{SECTION_ROOT}/{name}.tex" for name in ("finite_core", "paired_paths", "bibliography")}
    if not required_sections.issubset(sections):
        raise ValueError(f"Missing paper sections: {sorted(required_sections - set(sections))}")
    for name in sections:
        files[name] = "paper-source"
    for name in files:
        checked_name(name)
    return dict(sorted(files.items()))


def manifest_metadata() -> dict:
    return {
        "schema": "collatz-zenodo-v7-source-manifest-1",
        "version": "v7",
        "release_date": "2026-11-16",
        "concept_doi": "10.5281/zenodo.20021537",
        "version_doi": "10.5281/zenodo.24284425",
        "previous_version_doi": "10.5281/zenodo.22936057",
        "proof_source_baseline_commit": PROOF_BASELINE,
        "canonical_lean_file_count": EXPECTED_LEAN_FILES,
        "lean_toolchain": checked_path("lean/lean-toolchain").read_text(encoding="utf-8").strip(),
        "paper_pdf_distribution": "separate PDF on the same Zenodo record; not a ZIP payload member",
        "verification_scope": "artifact integrity; recorded proof checks are described by their separate sources, logs and receipt",
        "trust_limits": TRUST_LIMITS,
    }


def json_bytes(manifest: dict) -> bytes:
    return (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"Duplicate JSON key: {key}")
        obj[key] = value
    return obj


def validate_record(entry: object, *, with_role: bool) -> dict:
    required = {"path", "bytes", "sha256"} | ({"role"} if with_role else set())
    if not isinstance(entry, dict) or set(entry) != required:
        raise ValueError(f"Invalid manifest file record: {entry!r}")
    checked_name(entry["path"])
    if type(entry["bytes"]) is not int or entry["bytes"] < 0:
        raise ValueError(f"Invalid byte count: {entry['path']}")
    if not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
        raise ValueError(f"Invalid SHA-256: {entry['path']}")
    return entry


def validate_manifest(manifest: object) -> dict:
    metadata = manifest_metadata()
    if not isinstance(manifest, dict) or set(manifest) != set(metadata) | {"paper_pdf", "files"}:
        raise ValueError("Unexpected manifest schema or fields")
    for key, expected in metadata.items():
        if manifest[key] != expected:
            raise ValueError(f"Unexpected manifest metadata: {key}")
    pdf = validate_record(manifest["paper_pdf"], with_role=False)
    if pdf["path"] != PDF:
        raise ValueError("Unexpected separately supplied PDF path")
    entries = manifest["files"]
    if not isinstance(entries, list):
        raise ValueError("Manifest files must be a list")
    expected = payload()
    actual = {}
    for entry in entries:
        validate_record(entry, with_role=True)
        name = entry["path"]
        if name in actual:
            raise ValueError(f"Duplicate manifest payload path: {name}")
        actual[name] = entry["role"]
    if actual != expected:
        raise ValueError("Manifest payload paths or roles differ from the declared v7 source scope")
    if list(actual) != sorted(actual):
        raise ValueError("Manifest payload entries are not in canonical order")
    return manifest


def verify_source_files(manifest: dict) -> None:
    for entry in manifest["files"]:
        data = checked_path(entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError(f"Source checksum mismatch: {entry['path']}")
    print(f"Source checksums OK: {len(manifest['files'])} entries, including {EXPECTED_LEAN_FILES} canonical Lean files")
    pdf_path = checked_path(PDF, required=False)
    if pdf_path.exists():
        data = pdf_path.read_bytes()
        entry = manifest["paper_pdf"]
        if not data.startswith(b"%PDF-") or len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError(f"Separate PDF checksum mismatch: {PDF}")
        print(f"Separate PDF checksum OK: {PDF}")
    else:
        print("Separate PDF not present; the manifest records its hash for comparison with the Zenodo PDF")


def zipinfo(name: str) -> ZipInfo:
    info = ZipInfo(checked_name(name), FIXED_ZIP_DATE)
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = ZIP_DEFLATED
    return info


def verify_archive(manifest_bytes: bytes, manifest: dict) -> None:
    archive_path = checked_path(ARCHIVE)
    records = {entry["path"]: entry for entry in manifest["files"]}
    expected = set(records) | {MANIFEST}
    with ZipFile(archive_path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
        if duplicates:
            raise ValueError(f"Duplicate ZIP members: {duplicates}")
        for info in infos:
            checked_name(info.filename)
            if info.is_dir() or stat.S_IFMT(info.external_attr >> 16) != stat.S_IFREG:
                raise ValueError(f"Nonregular ZIP member: {info.filename}")
            if (info.create_system != 3 or info.external_attr != 0o100644 << 16
                    or info.date_time != FIXED_ZIP_DATE or info.compress_type != ZIP_DEFLATED
                    or info.flag_bits & 1 or info.extra or info.comment):
                raise ValueError(f"Noncanonical ZIP metadata: {info.filename}")
        actual = set(names)
        if actual != expected:
            raise ValueError(f"ZIP members differ: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
        if names != sorted(names) or archive.comment:
            raise ValueError("ZIP ordering or archive comment is not canonical")
        for info in infos:
            if info.filename == MANIFEST:
                if info.file_size != len(manifest_bytes) or archive.read(info) != manifest_bytes:
                    raise ValueError("ZIP manifest differs from the saved manifest")
            else:
                entry = records[info.filename]
                if info.file_size != entry["bytes"]:
                    raise ValueError(f"ZIP member size mismatch: {info.filename}")
                data = archive.read(info)
                if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
                    raise ValueError(f"ZIP checksum mismatch: {info.filename}")
    print(f"ZIP OK: {ARCHIVE} ({archive_path.stat().st_size} bytes, SHA-256 {digest(archive_path.read_bytes())})")


def atomic_write(name: str, data: bytes) -> None:
    target = checked_path(name, required=False)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{target.name}.", dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def build() -> None:
    pdf_data = checked_path(PDF).read_bytes()
    if not pdf_data.startswith(b"%PDF-"):
        raise ValueError(f"Final PDF required before freezing the archive: {PDF}")
    # Snapshot every payload byte once, so the manifest and archive use the same
    # data even if an unrelated process subsequently edits a working-tree file.
    roles = payload()
    snapshot = {name: checked_path(name).read_bytes() for name in roles}
    entries = [{"path": name, "role": roles[name], "bytes": len(data), "sha256": digest(data)}
               for name, data in snapshot.items()]
    manifest = manifest_metadata() | {
        "paper_pdf": {"path": PDF, "bytes": len(pdf_data), "sha256": digest(pdf_data)},
        "files": entries,
    }
    validate_manifest(manifest)
    manifest_bytes = json_bytes(manifest)
    atomic_write(MANIFEST, manifest_bytes)
    archive_path = checked_path(ARCHIVE, required=False)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{archive_path.name}.", dir=archive_path.parent, delete=False) as stream:
            temporary = Path(stream.name)
        members = snapshot | {MANIFEST: manifest_bytes}
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for name in sorted(members):
                archive.writestr(zipinfo(name), members[name], compress_type=ZIP_DEFLATED, compresslevel=9)
        os.replace(temporary, archive_path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    verify_source_files(manifest)
    verify_archive(manifest_bytes, manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="check the saved manifest, sources, optional separate PDF, and ZIP when present")
    args = parser.parse_args()
    try:
        if args.verify_only:
            manifest_bytes = checked_path(MANIFEST).read_bytes()
            manifest = validate_manifest(json.loads(manifest_bytes, object_pairs_hook=reject_duplicate_keys))
            if json_bytes(manifest) != manifest_bytes:
                raise ValueError("Manifest JSON is not canonically serialized")
            verify_source_files(manifest)
            if checked_path(ARCHIVE, required=False).exists():
                verify_archive(manifest_bytes, manifest)
            else:
                print("Source-only verification complete: ZIP absent from this extracted source tree")
        else:
            build()
    except (OSError, ValueError, BadZipFile, RuntimeError) as exc:
        raise SystemExit(f"v7 archive check failed: {exc}") from exc


if __name__ == "__main__":
    main()
