#!/usr/bin/env python3
"""Run the strict new-root audit only after pinned integration reports PASS."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, os, re, subprocess, time

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
LEAN = REPO / 'lean'
AUDIT = OUT / 'AllNewDependencyAudit.lean'
PLAN = OUT / 's14_audit_plan.json'
RECEIPT = OUT / 's14_receipt.json'
LOG = OUT / 's14_all_new_axioms.log'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(): return datetime.now(timezone.utc).isoformat()
def save(r): RECEIPT.write_text(json.dumps(r, indent=2) + '\n')

plan = json.loads(PLAN.read_text())
record = {'status': 'WAITING_FOR_INTEGRATION', 'started_utc': stamp(),
          'scope': 'Strict transitive axiom audit of all 69 public theorem roots in ten new modules.',
          'audit': str(AUDIT.relative_to(REPO)), 'audit_sha256': sha(AUDIT),
          'public_theorem_roots': plan['public_theorem_roots'],
          'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
          'independent_kernel': False, 'cold_dependency_rebuild': False}
save(record)
deadline = time.monotonic() + 14 * 60
while True:
    if os.environ.get('SPRINT_S14_ROOT_CONFIRMED') == '1':
        record['root_confirmed_all_module_builds'] = True
        break
    integration = OUT / 'integration_receipt.json'
    if integration.exists():
        value = json.loads(integration.read_text())
        if value.get('status') == 'FAIL':
            record.update(status='NOT_RUN_INTEGRATION_FAILED', finished_utc=stamp())
            save(record)
            raise SystemExit(1)
        if value.get('status') == 'PASS':
            record['integration_receipt_sha256'] = sha(integration)
            break
    if time.monotonic() >= deadline:
        record.update(status='NOT_RUN_WAIT_TIMEOUT', finished_utc=stamp())
        save(record)
        raise SystemExit(1)
    time.sleep(5)

sources = {}
for item in plan['sources']:
    path = LEAN / 'CollatzShadowing' / (item['module'] + '.lean')
    obj = LEAN / '.lake/build/lib/lean/CollatzShadowing' / (item['module'] + '.olean')
    if not obj.is_file():
        raise RuntimeError(f'Missing compiled module: {obj}')
    actual = sha(path)
    if actual != item['sha256']:
        record.update(status='NOT_RUN_SOURCE_CHANGED', changed_source=str(path.relative_to(REPO)), finished_utc=stamp())
        save(record)
        raise SystemExit(1)
    sources[str(path.relative_to(REPO))] = actual
record.update(status='RUNNING', audit_started_utc=stamp(), sources=sources)
save(record)
command = ['lake', 'env', 'lean', str(AUDIT)]
start = time.monotonic()
with LOG.open('w') as stream:
    result = subprocess.run(command, cwd=LEAN, stdout=stream, stderr=subprocess.STDOUT)
output = LOG.read_text()
passed = re.findall(r'SPRINT_ROOT_AUDIT: PASS ([^;\s]+);', output)
expected = re.findall(r'`(CollatzShadowing\.[A-Za-z0-9_\.]+)', AUDIT.read_text())
unchanged = all(sha(REPO / path) == digest for path,digest in sources.items())
record.update(command=command, exit_code=result.returncode, audit_elapsed_seconds=round(time.monotonic()-start,3),
              log=str(LOG.relative_to(REPO)), log_sha256=sha(LOG), roots_passed=len(passed),
              exact_root_list_match=passed == expected, source_unchanged=unchanged, finished_utc=stamp())
integration_final = OUT / 'integration_receipt.json'
if integration_final.exists():
    record['integration_status_at_finish'] = json.loads(integration_final.read_text()).get('status')
    if record['integration_status_at_finish'] == 'PASS':
        record['integration_receipt_sha256'] = sha(integration_final)
record['status'] = 'PASS' if result.returncode == 0 and passed == expected and len(passed) == plan['public_theorem_roots'] and unchanged and 'SPRINT_DEPENDENCY_AUDIT: PASS; roots: 69' in output else 'FAIL'
save(record)
print(json.dumps(record, indent=2))
raise SystemExit(0 if record['status']=='PASS' else 1)
