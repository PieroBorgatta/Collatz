#!/usr/bin/env python3
"""Bind frozen sprint evidence after the requested research period ends."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SESSION = Path("notes/research_sprint_2026-11-15_three_hours")
RESEARCH = Path("research/research_sprint_2026-11-15_three_hours")
DESTINATION = SESSION / "verification/delivery_manifest.json"


def main() -> None:
    verification = ROOT / SESSION / "verification"
    duration = json.loads((verification / "duration_receipt.json").read_text())
    elapsed = (datetime.fromisoformat(duration["research_stop_utc"])
               - datetime.fromisoformat(duration["research_start_utc"])).total_seconds()
    if elapsed < 10800:
        raise SystemExit("Requested research period has not elapsed")
    consistency = json.loads((verification / "delivery_consistency_final.json").read_text())
    if consistency["status"] != "PASS" or not consistency["final"]:
        raise SystemExit("Final delivery consistency check has not passed")
    resources = json.loads((verification / "resource_ledger.json").read_text())
    if resources["final_resource_audit_pending"]:
        raise SystemExit("Resource ledger is not final")

    paths = set()
    for folder in (ROOT / SESSION, ROOT / RESEARCH):
        for path in folder.rglob("*"):
            if not path.is_file() or path == ROOT / DESTINATION:
                continue
            if path.name == ".DS_Store" or "__pycache__" in path.parts:
                continue
            if path.suffix in {".pyc", ".olean", ".ilean", ".c", ".o"}:
                continue
            paths.add(path.relative_to(ROOT))

    baseline = json.loads((verification / "baseline_source_hashes.json").read_text())
    integration = json.loads((verification / "integration_receipt.json").read_text())
    paths.update(Path(p) for p in baseline["sha256"])
    paths.update(Path(p) for p in integration["sources"])
    paths.update(map(Path, [".github/workflows/lean.yml", "README.md",
                           "lean/README.md", "lean/STATUS.md",
                           "notes/PROJECT_STATISTICS.md"]))

    hashes = {}
    for relative in sorted(paths):
        data = (ROOT / relative).read_bytes()
        hashes[str(relative)] = {"sha256": hashlib.sha256(data).hexdigest(),
                                 "bytes": len(data)}
    result = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Delivery file integrity. Mathematical and experimental statuses are specified by the individual receipts. Historical failed attempts are retained as evidence, not claimed as passing proofs.",
        "research_elapsed_seconds": elapsed,
        "initial_commit": duration["initial_commit"],
        "integrated_library_modules": 4,
        "integrated_public_theorems": 28,
        "integrated_declarations_audited": 68,
        "standalone_unique_public_theorems": 9,
        "standalone_declarations_audited": 22,
        "standalone_core_copy_counted_twice": False,
        "finite_replay_suites": 6,
        "distinct_agents": 15,
        "files": hashes,
        "manifest_self_excluded": True,
        "published_v7_created": False,
        "GPU_used": False,
        "Collatz_proved": False,
    }
    (ROOT / DESTINATION).write_text(json.dumps(result, indent=2) + "\n")
    for relative, metadata in hashes.items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != metadata["sha256"]:
            raise SystemExit("File changed during manifest creation: " + relative)
    print(json.dumps({"status": "PASS", "files_bound": len(hashes),
                      "research_elapsed_seconds": elapsed}))


if __name__ == "__main__":
    main()
