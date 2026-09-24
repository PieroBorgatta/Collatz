#!/usr/bin/env python3
"""Compile a local Lean import closure with bounded parallelism in an authenticated assembly.

Run under `lake env python3` after fetching the pinned Mathlib cache. External
package objects are reused; every local module is compiled on the first run.
Resume only from this script's matching source/dependency/object receipts.
With --keep-going, Lean failures block their descendants but independent
branches continue. Input mutations always stop scheduling globally.
"""

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_receipt(path, data):
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def local_sources(root):
    return {str(p.relative_to(root)).removesuffix(".lean").replace("/", "."): p
            for p in root.rglob("*.lean")
            if not any(part in {".lake", "build"} for part in p.relative_to(root).parts)}


def input_changes(paths, expected):
    """Compare the live inputs to the bytes used for this run's import graph."""
    changes = {}
    for name, path in paths.items():
        try:
            actual = digest(path)
        except OSError as error:
            actual = "unreadable: " + str(error)
        if actual != expected[name]:
            changes[name] = {"expected_sha256": expected[name], "observed": actual}
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--jobs", type=int, default=1, choices=range(1, 5))
    parser.add_argument("--keep-going", action="store_true",
                        help="Continue independent branches after Lean errors; never after input mutations")
    args = parser.parse_args()
    root = Path.cwd()
    evidence = root / "build/weighted-replay"
    evidence.mkdir(parents=True, exist_ok=True)
    receipt = evidence / "receipt.json"
    old = json.loads(receipt.read_text()) if receipt.exists() else {}
    version = subprocess.check_output(["lean", "--version"], text=True).strip()
    assert "4.30.0-rc2" in version, version
    options = ["--threads=1", "--tstack=65536", "-M4096",
               "-DautoImplicit=false", "-DrelaxedAutoImplicit=false",
               "-Dpp.unicode.fun=true"]
    config = {"lean": version, "options": options,
              "lock_sha256": digest(root / "lake-manifest.json"),
              "toolchain_sha256": digest(root / "lean-toolchain"),
              "lakefile_sha256": digest(root / "lakefile.toml")}
    local = local_sources(root)
    # Parse and fingerprint the same captured bytes. A later source edit must
    # fail this run rather than attaching a new hash to an old fingerprint.
    source_bytes = {name: path.read_bytes() for name, path in local.items()}
    source_hashes = {name: hashlib.sha256(data).hexdigest()
                     for name, data in source_bytes.items()}
    source_texts = {name: data.decode("utf-8") for name, data in source_bytes.items()}
    del source_bytes
    input_paths = {"source:" + name: path for name, path in local.items()}
    expected_inputs = {"source:" + name: value for name, value in source_hashes.items()}
    for filename, key in (("lake-manifest.json", "lock_sha256"),
                          ("lean-toolchain", "toolchain_sha256"),
                          ("lakefile.toml", "lakefile_sha256")):
        input_paths["config:" + filename] = root / filename
        expected_inputs["config:" + filename] = config[key]

    def changed_inputs(check_inventory=False):
        changes = input_changes(input_paths, expected_inputs)
        if check_inventory:
            current = set(local_sources(root))
            initial = set(local)
            if current != initial:
                changes["source_inventory"] = {
                    "added": sorted(current - initial), "removed": sorted(initial - current)}
        return changes
    order, imports, visiting = [], {}, set()
    external_roots = {"Mathlib", "Lean", "Std", "Init", "Lake", "Batteries",
                      "Aesop", "Qq", "ProofWidgets", "Plausible", "ImportGraph",
                      "LeanSearchClient", "Cli"}

    def visit(name):
        if name not in local:
            if name.split(".")[0] not in external_roots:
                raise ValueError("Missing local import source: " + name)
            return
        if name in imports:
            return
        if name in visiting:
            raise ValueError("Import cycle: " + name)
        visiting.add(name)
        children = []
        for match in re.finditer(r"^\s*(?:public\s+)?import\s+([^\n]+)",
                                 source_texts[name], re.M):
            children.extend(match.group(1).split("--")[0].split())
        for child in children:
            visit(child)
        visiting.remove(name)
        imports[name] = children
        order.append(name)

    for target in args.targets:
        if target not in local:
            raise ValueError("Missing local target: " + target)
        visit(target)
    can_resume = old.get("config") == config
    result = {"config": config, "targets": args.targets, "local_modules": len(order),
              "external_packages_rebuilt": False, "lake_build_performed": False,
              "independent_leanchecker": False, "complete": False,
              "keep_going": args.keep_going, "completed_modules": [],
              "failed_modules": [], "blocked_modules": [],
              "source_snapshot": source_hashes,
              "modules": dict(old.get("modules", {})) if can_resume else {}}
    fingerprints = {}
    for name in order:
        tree = {"source": source_hashes[name],
                "imports": {d: fingerprints[d] for d in imports[name] if d in local}}
        fingerprints[name] = hashlib.sha256(json.dumps(tree, sort_keys=True).encode()).hexdigest()

    def compile_module(name):
        source = local[name]
        source_hash = source_hashes[name]
        changes = changed_inputs()
        if changes:
            return {"source_sha256": source_hash, "fingerprint": fingerprints[name],
                    "returncode": 125, "source_mutations": changes}, "input-changed"
        out = root / ".lake/build/lib/lean" / Path(*name.split("."))
        olean = out.with_suffix(".olean")
        previous = old.get("modules", {}).get(name, {})
        if (can_resume and previous.get("returncode") == 0 and
                previous.get("source_sha256") == source_hash and
                previous.get("fingerprint") == fingerprints[name] and olean.exists() and
                previous.get("olean_sha256") == digest(olean)):
            changes = changed_inputs()
            if changes:
                return {"source_sha256": source_hash, "fingerprint": fingerprints[name],
                        "returncode": 125, "source_mutations": changes}, "input-changed"
            return previous, "reuse"
        out.parent.mkdir(parents=True, exist_ok=True)
        log = evidence / (name + ".log")
        command = ["lean", *options, "-o", str(olean),
                   "-i", str(out.with_suffix(".ilean")), str(source.relative_to(root))]
        started = time.monotonic()
        with log.open("wb") as output:
            try:
                proc = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                      timeout=args.timeout,
                                      env=dict(os.environ, LEAN_NUM_THREADS="1"))
                status = proc.returncode
            except subprocess.TimeoutExpired:
                status = 124
        changes = changed_inputs()
        if changes:
            status = 125  # Any source/dependency/config mutation invalidates this run.
        row = {"source_sha256": source_hash, "fingerprint": fingerprints[name],
               "returncode": status, "elapsed_seconds": round(time.monotonic() - started, 3),
               "command": command, "log_sha256": digest(log)}
        if changes:
            row["source_mutations"] = changes
        if status == 0:
            row["olean_sha256"] = digest(olean)
        return row, "compiled"

    pending, completed, active, failed = list(order), set(), {}, set()
    failure = 0

    def save_progress():
        # Historical rows in `modules` remain available for a later resume;
        # only this list attests which modules were checked in this run.
        result["completed_modules"] = sorted(completed)
        result["failed_modules"] = sorted(failed)
        # In fail-fast mode, or after an input mutation, every unstarted
        # module is blocked by the global stop. With keep-going, only failed
        # dependencies (transitively) block a pending module.
        if failure and (failure == 125 or not args.keep_going):
            blocked = set(pending)
        else:
            unavailable = set(failed)
            pending_names = set(pending)
            for name in order:
                if name in pending_names and any(d in unavailable for d in imports[name]):
                    unavailable.add(name)
            blocked = unavailable - failed
        result["blocked_modules"] = sorted(blocked)
        save_receipt(receipt, result)

    # Retire a previous complete receipt before starting work on this snapshot.
    save_progress()
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        while pending or active:
            if failure != 125 and (not failure or args.keep_going):
                for name in list(pending):
                    if len(active) >= args.jobs:
                        break
                    if all(d not in local or d in completed for d in imports[name]):
                        pending.remove(name)
                        print(f"START {name}", flush=True)
                        active[pool.submit(compile_module, name)] = name
            if not active:
                if failure:
                    break
                raise ValueError("No ready module in dependency graph")
            finished, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in finished:
                name = active.pop(future)
                row, mode = future.result()
                result["modules"][name] = row
                status = row["returncode"]
                if status == 0:
                    completed.add(name)
                else:
                    failed.add(name)
                    # Input invalidation must dominate any Lean error,
                    # irrespective of concurrent completion order.
                    failure = 125 if status == 125 or failure == 125 else failure or status
                save_progress()
                print(f"[{len(completed)}/{len(order)}] {mode} {name}: "
                      f"exit={status} seconds={row.get('elapsed_seconds')}", flush=True)
                if status:
                    if "source_mutations" in row:
                        print(json.dumps({"source_mutations": row["source_mutations"]}), flush=True)
                    elif (evidence / (name + ".log")).exists():
                        print((evidence / (name + ".log")).read_text(errors="replace"), flush=True)
    # Includes reused and already completed modules, and catches an edit made
    # after its individual check, including in an already failed build.
    # Adding/removing sources also changes the run.
    changes = changed_inputs(check_inventory=True)
    if changes:
        failure = 125
        result["source_mutations"] = changes
        print(json.dumps({"source_mutations": changes}), flush=True)
    if failure:
        save_progress()
        return failure
    result["complete"] = True
    save_progress()
    print(f"SUCCESS: {len(order)} local modules checked; external packages cached.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
