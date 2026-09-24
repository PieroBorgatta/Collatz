#!/usr/bin/env python3
"""Assemble hash-pinned upstream sources and add this independent overlay."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile


ARCHIVES = {
    "supplement": (
        "https://www.proofatlas.ai/papers/positive-lower-density-collatz-predecessors/"
        "positive-lower-density-collatz-predecessors-v1.1-source.zip",
        55103, "55ceb4df0cca17ae728dc65b30bf5077000e1b47f2dc322454eea9f637ac75b3"),
    "baseline": (
        "https://www.proofatlas.ai/papers/positive-density-log-time-collatz/"
        "positive-density-log-time-collatz-v2.1-source.zip",
        914975, "23f5cac4d66e696401144658752cf180a13ce70373a122f00693e1e1fe969c1f"),
}
MODULES = ["WeightedPathOccupation", "WeightedTerminalAdapter", "WeightedCensus",
           "WeightedFrozenSeed", "WeightedPredecessorDensity",
           "TwoSeedNonreturn", "TwoSeedDensity"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--archives", type=Path,
                        help="Use local supplement.zip and baseline.zip instead of downloading")
    args = parser.parse_args()
    destination = args.destination.absolute()
    if destination.exists() or destination.is_symlink():
        parser.error("Choose a fresh destination; existing directories are not modified.")
    package = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="collatz-weighted-assembly-") as temp:
        temp = Path(temp)
        receipts = {}
        for name, (url, size, expected) in ARCHIVES.items():
            if args.archives:
                data = (args.archives / (name + ".zip")).read_bytes()
            else:
                data = subprocess.check_output([
                    "curl", "--fail", "--location", "--silent", "--show-error",
                    "--proto", "=https", "--proto-redir", "=https",
                    "--max-time", "60", "--max-filesize", str(size), url], timeout=70)
            actual = hashlib.sha256(data).hexdigest()
            if len(data) != size or actual != expected:
                raise ValueError("Archive identity mismatch: " + name)
            (temp / (name + ".zip")).write_bytes(data)
            receipts[name] = {"url": url, "bytes": size, "sha256": actual}
        with zipfile.ZipFile(io.BytesIO((temp / "supplement.zip").read_bytes())) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError("Duplicate archive members")
            for name in names:
                p = PurePosixPath(name)
                if p.is_absolute() or ".." in p.parts or "\\" in name:
                    raise ValueError("Unsafe archive member: " + name)
            archive.extractall(temp / "supplement")
        assembler = temp / "supplement/collatz-predecessor-density/scripts/assemble.py"
        subprocess.run([sys.executable, str(assembler), "--baseline-zip",
                        str(temp / "baseline.zip"), "--output", str(destination)], check=True)
        for name in MODULES:
            shutil.copyfile(package / (name + ".lean"), destination / (name + ".lean"))
        # The serial compiler only needs the existing Lake search path. Keep
        # the upstream configuration intact so its source verifier still passes.
        subprocess.run([sys.executable, str(destination / "scripts/verify-assembly.py")],
                       check=True)
        (destination / "weighted-overlay.json").write_text(json.dumps({
            "archives": receipts,
            "modules": {name: hashlib.sha256((destination / (name + ".lean")).read_bytes()).hexdigest()
                        for name in MODULES},
            "baseline_sources_modified": False,
            "compiled": False,
        }, indent=2) + "\n")
    print("Prepared", destination)


if __name__ == "__main__":
    main()
