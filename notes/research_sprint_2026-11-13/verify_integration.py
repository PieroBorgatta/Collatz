#!/usr/bin/env python3
"""Build the new modules in bounded independent pairs, then the full library.

Installed pinned dependencies are reused. This is not a cold rebuild or an
independent-kernel replay. Source mutation during a phase is a failure.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
LEAN = REPO / "lean"
OUT = HERE / "verification"
PAIRS = [
    ["RootPoolBudget", "CapacityAllocation"],
    ["ReturnBlocks", "RelativeMassFlow"],
    ["WordSurgery", "CycleRotation"],
    ["SiblingPool", "FiniteOrbitTransfer"],
    ["JointAtomDictionary", "AffinePositivity"],
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    modules = [name for pair in PAIRS for name in pair]
    paths = [LEAN / "CollatzShadowing" / f"{name}.lean" for name in modules]
    paths.append(LEAN / "CollatzShadowing.lean")
    receipt = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Pinned incremental builds; at most two new independent modules per phase.",
        "phases": [],
    }
    for index, pair in enumerate(PAIRS + [[]], 1):
        before = {str(p.relative_to(REPO)): digest(p) for p in paths}
        command = ["lake", "build"] + [f"CollatzShadowing.{name}" for name in pair]
        log = OUT / (f"build_pair_{index:02d}.log" if pair else "integrated_build.log")
        started = time.monotonic()
        with log.open("w") as stream:
            result = subprocess.run(command, cwd=LEAN, stdout=stream, stderr=subprocess.STDOUT)
        unchanged = all(digest(REPO / name) == value for name, value in before.items())
        phase = {"command": command, "exit_code": result.returncode,
                 "source_unchanged": unchanged, "elapsed_seconds": round(time.monotonic() - started, 3),
                 "log": str(log.relative_to(HERE)), "log_sha256": digest(log)}
        receipt["phases"].append(phase)
        receipt["status"] = "RUNNING" if result.returncode == 0 and unchanged else "FAIL"
        (OUT / "integration_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(phase), flush=True)
        if result.returncode != 0 or not unchanged:
            raise SystemExit(1)
    receipt["status"] = "PASS"
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["sources"] = {str(p.relative_to(REPO)): digest(p) for p in paths}
    (OUT / "integration_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
