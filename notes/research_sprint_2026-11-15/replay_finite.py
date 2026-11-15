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
CASES = [('dyadic', 't01/verify_dyadic.py'),
         ('two_edit', 't02/check_two_edit_residuals.py'),
         ('stationary', 't03/stationary_cylinders.py'),
         ('independent_two_edit', 't04/independent_two_edit.py'),
         ('independent_terminal', 't04/independent_terminal.py'),
         ('independent_math', 't09/independent_audit.py'),
         ('cap_overflow', 't08/check_overflow_bound.py'),
         ('odometer_resolvent', 't10/check_resolvent.py'),
         ('delayed_support', 't10/check_delayed_support.py'),
         ('positive_integer_atoms', 't10/check_positive_atoms.py')]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run_case(case, out):
    label, relative = case
    source = REPO / 'research/research_sprint_2026-11-15' / relative
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
    ok = codes == [0, 0] and same and unchanged and len(values) == 2
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
    with ThreadPoolExecutor(max_workers=3) as pool:
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
