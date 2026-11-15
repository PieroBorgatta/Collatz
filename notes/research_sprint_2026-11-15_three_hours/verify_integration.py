#!/usr/bin/env python3
"""Pinned incremental integration and transitive all-declaration audit.

Reuses the installed pinned dependencies. No cold or independent-kernel
rebuild is claimed. Every phase fails if any protected source changes.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
LEAN = REPO / 'lean'
OUT = HERE / 'verification'
MODULES = ['FiniteHorizonBudget', 'QuadraticOccupation', 'BoundedSlopeCatalogue', 'SpineDispersion']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def main():
    OUT.mkdir(exist_ok=True)
    paths = [LEAN / 'CollatzShadowing' / f'{m}.lean' for m in MODULES]
    paths += [LEAN / 'CollatzShadowing.lean', LEAN / 'lean-toolchain',
              LEAN / 'lakefile.toml', LEAN / 'lake-manifest.json',
              OUT / 'AllNewDependencyAudit.lean']
    snapshot = {str(p.relative_to(REPO)): digest(p) for p in paths}
    receipt = {'status': 'RUNNING', 'started_utc': stamp(),
               'scope': 'Pinned incremental full library build and all-declaration transitive axiom audit of four additional November 15–16 modules.',
               'cold_dependency_rebuild': False, 'independent_kernel_replay': False,
               'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
               'sources': snapshot, 'phases': []}
    public = []
    for module in MODULES:
        source = (LEAN / 'CollatzShadowing' / f'{module}.lean').read_text()
        public += [f'CollatzShadowing.{module}.{name}' for name in
                   re.findall(r'^theorem\s+([A-Za-z0-9_]+)', source, re.M)]
    receipt['public_theorem_roots'] = public
    steps = [(['lake', 'build'], OUT / 'integrated_build.log'),
             (['lake', 'env', 'lean', str(OUT / 'AllNewDependencyAudit.lean')],
              OUT / 'all_new_axioms.log')]
    target = OUT / 'integration_receipt.json'
    target.write_text(json.dumps(receipt, indent=2) + '\n')
    for command, log in steps:
        before = {name: digest(REPO / name) for name in snapshot}
        start = time.monotonic()
        with log.open('w') as stream:
            proc = subprocess.run(command, cwd=LEAN, stdout=stream, stderr=subprocess.STDOUT)
        unchanged = all(digest(REPO / name) == h for name, h in before.items())
        phase = {'command': command, 'exit_code': proc.returncode,
                 'source_unchanged': unchanged, 'elapsed_seconds': round(time.monotonic() - start, 3),
                 'log': str(log.relative_to(REPO)), 'log_sha256': digest(log)}
        receipt['phases'].append(phase)
        print(json.dumps(phase), flush=True)
        if proc.returncode != 0 or not unchanged:
            receipt.update(status='FAIL', finished_utc=stamp())
            target.write_text(json.dumps(receipt, indent=2) + '\n')
            raise SystemExit(1)
        target.write_text(json.dumps(receipt, indent=2) + '\n')
    output = (OUT / 'all_new_axioms.log').read_text()
    roots = re.findall(r'SPRINT_EXTRA3H_ROOT: PASS ([^;\s]+);', output)
    summary = re.search(r'SPRINT_EXTRA3H_AUDIT: PASS; declarations: (\d+); encoded-private: (\d+); modules: (\d+)', output)
    receipt['declarations_audited'] = len(roots)
    receipt['all_public_theorems_present'] = all(root in roots for root in public)
    receipt['audit_summary'] = {'declarations': int(summary[1]), 'encoded_private': int(summary[2]),
                                'modules': int(summary[3])} if summary else None
    receipt['source_snapshot_unchanged'] = all(digest(REPO / name) == h for name, h in snapshot.items())
    ok = summary and int(summary[1]) == len(roots) and int(summary[3]) == len(MODULES)
    ok = bool(ok and receipt['all_public_theorems_present'] and receipt['source_snapshot_unchanged'])
    receipt.update(status='PASS' if ok else 'FAIL', finished_utc=stamp())
    target.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'public_theorems': len(public),
                      'audit_summary': receipt['audit_summary']}), flush=True)
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
