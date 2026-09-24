#!/usr/bin/env python3
"""Check the repository copies of the immutable Zenodo v1–v6 PDFs offline."""

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name("published_pdf_checksums.json")


def check() -> int:
    records = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    versions = [record["version"] for record in records]
    if versions != [f"v{i}" for i in range(1, 7)]:
        print("Published PDF manifest must list v1 through v6 exactly once.", file=sys.stderr)
        return 1

    failed = False
    for record in records:
        rel = Path(record["path"])
        if rel.is_absolute() or ".." in rel.parts:
            print(f"Invalid manifest path: {rel}", file=sys.stderr)
            failed = True
            continue
        path = ROOT / rel
        if not path.is_file():
            print(f"Missing published PDF: {rel}", file=sys.stderr)
            failed = True
            continue
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(chunk)
                md5.update(chunk)
                sha256.update(chunk)
        good = (
            size == record["size_bytes"]
            and md5.hexdigest() == record["zenodo_md5"]
            and sha256.hexdigest() == record["sha256"]
        )
        print(f"{record['version']}: {'OK' if good else 'MISMATCH'} ({rel})")
        failed |= not good
    return int(failed)


if __name__ == "__main__":
    sys.exit(check())
