#!/usr/bin/env python3
"""Replay deterministic finite error checks; no asymptotic claim follows.

The normal and optimized executions must produce identical bytes. Every
child script checks its guards explicitly, independently of assert removal.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CASES = [('physical_cdf', 'u03/physical_cdf.py'), ('physical_parent_collision', 'u07/physical_parent_collision.py'), ('affine_transport', 'u10/affine_transport.py'), ('minimum_parent_seeds', 'u12/minimum_parent_seeds.py'), ('minimal_prefix', 'u13/check_minimal_prefix.py'), ('calibrated_prefix', 'u13calibrated/check_calibrated_prefix.py')]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run_case(case, out):
    label, relative = case
    source = REPO / 'research/research_sprint_2026-11-15_three_hours' / relative
    source_hash = sha(source.read_bytes())
    start = time.monotonic()
    outputs = []
    codes = []
    for optimized in (False, True):
        command = [sys.executable] + (['-O'] if optimized else []) + [str(source)]
        result = subprocess.run(command, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        codes.append(result.returncode)
        suffix = '_optimized' if optimized else ''
        (out / f'{label}{suffix}.json').write_bytes(result.stdout)
        (out / f'{label}{suffix}.stderr').write_bytes(result.stderr)
        outputs.append(result.stdout)
    same = outputs[0] == outputs[1]
    unchanged = sha(source.read_bytes()) == source_hash
    values = []
    try:
        values = [json.loads(data) for data in outputs]
    except (ValueError, UnicodeDecodeError):
        pass
    ok = codes == [0, 0] and same and unchanged and len(values) == 2 and all(value.get("status") == "PASS" for value in values)
    return {'label': label, 'script': str(source.relative_to(REPO)),
            'script_sha256': source_hash, 'exit_codes': codes,
            'normal_optimized_identical': same, 'source_unchanged': unchanged,
            'normal_sha256': sha(outputs[0]), 'optimized_sha256': sha(outputs[1]),
            'status': 'PASS' if ok else 'FAIL',
            'elapsed_seconds': round(time.monotonic() - start, 3)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'verification/fresh_replay')
    options = parser.parse_args()
    out = options.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_case, case, out) for case in CASES]
        results = []
        for future in as_completed(futures):
            result = future.result()
            print(json.dumps(result), flush=True)
            results.append(result)
    results.sort(key=lambda item: item['label'])
    record = {'status': 'PASS' if all(r['status'] == 'PASS' for r in results) else 'FAIL',
              'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'meaning': 'Finite error checks only; no proof of asymptotic mass, H, or Collatz.',
              'cases': results}
    (out / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n')
    raise SystemExit(0 if record['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
