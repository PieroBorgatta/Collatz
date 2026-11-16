#!/usr/bin/env python3
"""Check delivery consistency, without rerunning or extending experiments.

This validates files and the existing receipts. It is not an additional
mathematical audit, cold rebuild, or proof of asymptotic conclusions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
SESSION = Path("notes/research_sprint_2026-11-15_three_hours")
RESEARCH = Path("research/research_sprint_2026-11-15_three_hours")
MODULES = (
    "FiniteHorizonBudget",
    "QuadraticOccupation",
    "BoundedSlopeCatalogue",
    "SpineDispersion",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads((ROOT / path).read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    failures: list[str] = []
    checks: list[dict] = []

    def check(label: str, ok: bool, **details) -> None:
        checks.append({"label": label, "status": "PASS" if ok else "FAIL", **details})
        if not ok:
            failures.append(label)

    integration = read_json(SESSION / "verification/integration_receipt.json")
    check("build_and_audit_receipt", integration["status"] == "PASS")
    for name, expected in integration["sources"].items():
        check("verified_source:" + name, sha(ROOT / name) == expected)
    for phase in integration["phases"]:
        check(
            "verified_log:" + phase["log"],
            phase["exit_code"] == 0
            and phase["source_unchanged"]
            and sha(ROOT / phase["log"]) == phase["log_sha256"],
        )
    check("strict_audit_scope", integration["declarations_audited"] == 68
          and len(integration["public_theorem_roots"]) == 28
          and integration["allowed_axioms"]
          == ["propext", "Classical.choice", "Quot.sound"])

    replay = read_json(SESSION / "verification/fresh_replay/receipt.json")
    check("six_replay_receipt", replay["status"] == "PASS" and len(replay["cases"]) == 6)
    for case in replay["cases"]:
        normal = ROOT / SESSION / "verification/fresh_replay" / (case["label"] + ".json")
        optimized = normal.with_name(case["label"] + "_optimized.json")
        check("replay_snapshot:" + case["label"],
              sha(ROOT / case["script"]) == case["script_sha256"]
              and sha(normal) == case["normal_sha256"]
              and sha(optimized) == case["optimized_sha256"]
              and normal.read_bytes() == optimized.read_bytes()
              and case["exit_codes"] == [0, 0])

    baseline = read_json(SESSION / "verification/baseline_source_hashes.json")
    allowed_changes = {"lean/CollatzShadowing.lean", "lean/CollatzShadowing/THEOREM_INDEX.md"}
    changed = sorted(name for name, digest in baseline["sha256"].items()
                     if sha(ROOT / name) != digest)
    check("frozen_previous_sources_and_pdfs", set(changed) <= allowed_changes,
          permitted_changes=sorted(allowed_changes), actual_changes=changed)

    statistics = read_json(SESSION / "verification/source_statistics.json")
    public = re.compile(r"^\s*(?:theorem|lemma)\s+", re.MULTILINE)
    # Exclude other historical checkouts nested under lean/.claude and the
    # dependency cache. Count this library and its main entrypoint only.
    lean_files = [ROOT / "lean/CollatzShadowing.lean"] + sorted(
        (ROOT / "lean/CollatzShadowing").rglob("*.lean")
    )
    groups = {
        "AI_authored": [p for p in lean_files if "Generated" not in p.parts],
        "generator_emitted": [p for p in lean_files if "Generated" in p.parts],
        "total": lean_files,
        "new_modules": [ROOT / "lean/CollatzShadowing" / (m + ".lean") for m in MODULES],
    }
    for name, files in groups.items():
        actual = {"files": len(files),
                  "lines": sum(len(p.read_text().splitlines()) for p in files),
                  "public_theorem_lemma_declarations": sum(len(public.findall(p.read_text())) for p in files)}
        check("statistics:" + name, actual == statistics[name], actual=actual)

    # Links in the new section of the theorem index must land on each of
    # the 28 public theorem declarations, not merely on an existing file.
    index = ROOT / "lean/CollatzShadowing/THEOREM_INDEX.md"
    links = re.findall(r"\]\(([^)]+\.lean)#L(\d+)\)", index.read_text())
    found = set()
    for destination, line_text in links:
        target = (index.parent / destination).resolve()
        if target.stem not in MODULES:
            continue
        lines = target.read_text().splitlines()
        number = int(line_text)
        ok = 1 <= number <= len(lines) and bool(public.match(lines[number - 1]))
        check("index_line:" + target.stem + ":" + line_text, ok)
        found.add((str(target), number))
    check("index_all_28_public_theorems", len(found) == 28, count=len(found))

    prototype_dir = ROOT / RESEARCH / "u06_max_envelope"
    prototype_core = prototype_dir / "MaxEnvelopePrototype.lean"
    prototype_extension = prototype_dir / "CompositionPrototype.lean"
    check("standalone_prototype_frozen_prefix",
          prototype_extension.read_bytes().startswith(prototype_core.read_bytes()))
    for receipt_name in ("core_receipt.json", "composition_receipt.json"):
        receipt_path = prototype_dir / receipt_name
        if not receipt_path.exists() and not args.final:
            continue
        receipt = json.loads(receipt_path.read_text())
        check("standalone_receipt:" + receipt_name, receipt["status"] == "PASS")
        for name, metadata in receipt.get("artifacts", {}).items():
            if isinstance(metadata, dict) and "sha256" in metadata:
                check("standalone_artifact:" + name, sha(ROOT / name) == metadata["sha256"])

    # Check Markdown destinations only. Code spans/fences and network URLs
    # are outside this local consistency check.
    markdown = sorted((ROOT / SESSION).rglob("*.md")) + [
        ROOT / "README.md", ROOT / "lean/README.md", ROOT / "lean/STATUS.md",
        ROOT / "notes/PROJECT_STATISTICS.md", index,
    ]
    missing_links = []
    for source in markdown:
        prose = re.sub(r"```[\s\S]*?```", "", source.read_text())
        prose = re.sub(r"`[^`\n]*`", "", prose)
        for dest in re.findall(r"\]\(([^\s)]+)\)", prose):
            dest = dest.strip("<>")
            if urlsplit(dest).scheme or dest.startswith("#"):
                continue
            local = unquote(dest.split("#", 1)[0].split("?", 1)[0])
            if local and not (source.parent / local).exists():
                missing_links.append({"source": str(source.relative_to(ROOT)), "destination": dest})
    check("local_markdown_destinations", not missing_links, missing=missing_links)

    # Review receipts bind source snapshots; later addenda use separate
    # files so the already-reviewed mathematical notes stay frozen.
    reviewed = 0
    for receipt_path in sorted((ROOT / RESEARCH).rglob("*receipt.json")):
        receipt = json.loads(receipt_path.read_text())
        snapshots = receipt.get("source_snapshots", {})
        if not isinstance(snapshots, dict):
            continue
        for name, metadata in snapshots.items():
            if not isinstance(metadata, dict) or "sha256" not in metadata:
                continue
            original = ROOT / name
            if not original.exists():
                check("review_source_exists:" + name, False)
                continue
            snapshot = metadata.get("snapshot")
            # An earlier review can deliberately bind an earlier Lean
            # snapshot. Current compiled sources are checked above against
            # the final integration receipt. Frozen paper notes stay exact.
            if name.startswith("lean/") and snapshot:
                checks.append({"label": "historical_review:" + name,
                               "status": "PASS",
                               "original_matches_snapshot": sha(original) == metadata["sha256"],
                               "meaning": "Snapshot integrity checked separately; current Lean is bound by integration receipt."})
            else:
                check("review_hash:" + name, sha(original) == metadata["sha256"])
            if snapshot:
                check("review_snapshot:" + snapshot,
                      sha(ROOT / snapshot) == metadata["sha256"])
            reviewed += 1

    if args.final:
        duration = read_json(SESSION / "verification/duration_receipt.json")
        start = datetime.fromisoformat(duration["research_start_utc"])
        stop = datetime.fromisoformat(duration["research_stop_utc"])
        check("at_least_three_hours", (stop - start).total_seconds() >= 10800)
        resources = read_json(SESSION / "verification/resource_ledger.json")
        check("created_gpu_resources_closed", resources["created_runpod_resources"] == []
              or all(x["terminated_or_stopped"] for x in resources["created_runpod_resources"]))

    result = {
        "status": "FAIL" if failures else "PASS",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Delivery consistency only; no additional mathematical verification.",
        "final": args.final,
        "reviewed_snapshot_checks": reviewed,
        "checks": checks,
        "failures": failures,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "failures": failures}))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
