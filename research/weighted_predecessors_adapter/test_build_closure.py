#!/usr/bin/env python3
"""Regression tests for receipt handling; the stub is NOT a Lean verifier."""
from contextlib import redirect_stdout
from concurrent.futures import ALL_COMPLETED
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().with_name('build_closure.py')
spec = importlib.util.spec_from_file_location('build_closure_under_test', SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

FAKE = '''#!/usr/bin/env python3
import hashlib, json, os, time
from pathlib import Path
import sys
if '--version' in sys.argv:
    print('FAKE TEST ONLY Lean version 4.30.0-rc2')
    raise SystemExit(0)
source=Path(sys.argv[-1]); data=source.read_bytes()
with Path('stub-invocations.txt').open('a') as log: log.write(str(source)+'\\n')
plan=Path('stub-plan.json')
if plan.exists():
    action=json.loads(plan.read_text())
    if action['on']==str(source):
        if action.get('wait_for'):
            deadline=time.monotonic()+10
            while not Path(action['wait_for']).exists():
                if time.monotonic()>deadline: raise RuntimeError('stub barrier timed out')
                time.sleep(0.01)
        target=Path(action['target'])
        if action.get('delete'): target.unlink()
        else: target.write_text(action['text'])
        plan.unlink()
failures=Path('stub-failures.json')
if failures.exists():
    status=json.loads(failures.read_text()).get(str(source),0)
    if status:
        print('FAKE TEST ONLY compilation failure:',source)
        raise SystemExit(status)
output=Path(sys.argv[sys.argv.index('-o')+1]); output.parent.mkdir(parents=True,exist_ok=True)
output.write_bytes(b'FAKE TEST OBJECT: '+hashlib.sha256(data).hexdigest().encode())
Path(sys.argv[sys.argv.index('-i')+1]).write_text('FAKE TEST INTERFACE')
'''

class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='fake-lean-receipt-test-')
        self.root=Path(self.temp.name)
        (self.root/'bin').mkdir()
        executable=self.root/'bin/lean'; executable.write_text(FAKE); executable.chmod(0o755)
        (self.root/'lake-manifest.json').write_text('{}')
        (self.root/'lean-toolchain').write_text('leanprover/lean4:v4.30.0-rc2\n')
        (self.root/'lakefile.toml').write_text('name = "receiptTest"\n')
        (self.root/'B.lean').write_text('-- initial B\n')
        (self.root/'A.lean').write_text('import B\n-- initial A\n')
        self.oldcwd=Path.cwd(); os.chdir(self.root)
        self.environment=patch.dict(os.environ,{'PATH':str(self.root/'bin')+os.pathsep+os.environ['PATH']})
        self.environment.start()
    def tearDown(self):
        self.environment.stop(); os.chdir(self.oldcwd); self.temp.cleanup()
    def run_builder(self,*arguments):
        with patch.object(sys,'argv',['build_closure.py',*(arguments or ['A'])]), redirect_stdout(io.StringIO()):
            return builder.main()
    def receipt(self):
        return json.loads((self.root/'build/weighted-replay/receipt.json').read_text())
    def plan(self,on,target,text='-- mutated\n',delete=False,wait_for=None):
        (self.root/'stub-plan.json').write_text(json.dumps(dict(on=on,target=target,text=text,delete=delete,wait_for=wait_for)))
    def branching_failure(self):
        (self.root/'C.lean').write_text('-- independent C\n')
        (self.root/'D.lean').write_text('import C\n')
        (self.root/'Root.lean').write_text('import A D\n')
        (self.root/'stub-failures.json').write_text(json.dumps({'B.lean':1}))
    def invocations(self):
        return (self.root/'stub-invocations.txt').read_text().splitlines()
    def assert_rejected(self):
        self.assertEqual(self.run_builder(),125)
        self.assertFalse(self.receipt()['complete'])
    def test_stable_resume_and_transitive_invalidation(self):
        self.assertEqual(self.run_builder(),0)
        self.assertTrue(self.receipt()['complete'])
        self.assertEqual(self.invocations(),['B.lean','A.lean'])
        self.assertEqual(self.run_builder(),0)
        self.assertEqual(len(self.invocations()),2)
        (self.root/'B.lean').write_text('-- revised before next run\n')
        self.assertEqual(self.run_builder(),0)
        self.assertEqual(self.invocations(),['B.lean','A.lean','B.lean','A.lean'])
    def test_not_yet_compiled_source_mutation(self):
        self.plan('B.lean','A.lean','import B\n-- edited while B compiled\n')
        self.assert_rejected(); self.assertEqual(self.invocations(),['B.lean'])
        self.assertIn('source:A',self.receipt()['modules']['B']['source_mutations'])
    def test_current_source_mutation(self):
        self.plan('B.lean','B.lean'); self.assert_rejected()
    def test_already_compiled_dependency_mutation(self):
        self.plan('A.lean','B.lean'); self.assert_rejected()
    def test_missing_dependency_during_compile(self):
        self.plan('A.lean','B.lean',delete=True); self.assert_rejected()
    def test_configuration_mutation(self):
        self.plan('B.lean','lean-toolchain','changed toolchain\n'); self.assert_rejected()
    def test_lakefile_mutation(self):
        self.plan('B.lean','lakefile.toml','name = "changedDuringCompile"\n')
        self.assert_rejected()
        self.assertIn('config:lakefile.toml',self.receipt()['modules']['B']['source_mutations'])
    def test_lakefile_change_invalidates_resume(self):
        self.assertEqual(self.run_builder(),0)
        initial_config=self.receipt()['config']
        (self.root/'lakefile.toml').write_text('name = "changedBeforeResume"\n')
        self.assertEqual(self.run_builder(),0)
        self.assertNotEqual(initial_config,self.receipt()['config'])
        self.assertEqual(self.invocations(),['B.lean','A.lean','B.lean','A.lean'])
    def test_mutation_while_reusing_object(self):
        self.assertEqual(self.run_builder(),0)
        original=builder.digest; triggered=False
        def digest_and_mutate(path):
            nonlocal triggered
            value=original(path)
            if path.suffix=='.olean' and not triggered:
                triggered=True
                (self.root/'A.lean').write_text('import B\n-- edited during reuse\n')
            return value
        with patch.object(builder,'digest',digest_and_mutate): self.assert_rejected()
        self.assertTrue(triggered); self.assertEqual(len(self.invocations()),2)
    def test_mutation_after_last_module_check(self):
        original=builder.save_receipt; triggered=False
        def save_and_mutate(path,data):
            nonlocal triggered
            original(path,data)
            if not triggered and data['modules'].get('A',{}).get('returncode')==0:
                triggered=True; (self.root/'B.lean').write_text('-- edited after final module\n')
        with patch.object(builder,'save_receipt',save_and_mutate): self.assert_rejected()
        self.assertIn('source:B',self.receipt()['source_mutations'])
    def test_new_source_inventory_change(self):
        self.plan('A.lean','NewModule.lean')
        self.assert_rejected()
        self.assertEqual(self.receipt()['source_mutations']['source_inventory']['added'],['NewModule'])
    def test_fail_fast_remains_default(self):
        self.branching_failure()
        self.assertEqual(self.run_builder('Root'),1)
        receipt=self.receipt()
        self.assertFalse(receipt['complete'])
        self.assertFalse(receipt['keep_going'])
        self.assertEqual(self.invocations(),['B.lean'])
        self.assertEqual(receipt['failed_modules'],['B'])
        self.assertEqual(receipt['blocked_modules'],['A','C','D','Root'])
    def test_keep_going_completes_independent_branch(self):
        self.branching_failure()
        self.assertEqual(self.run_builder('--keep-going','Root'),1)
        receipt=self.receipt()
        self.assertFalse(receipt['complete'])
        self.assertTrue(receipt['keep_going'])
        self.assertEqual(self.invocations(),['B.lean','C.lean','D.lean'])
        self.assertEqual(receipt['failed_modules'],['B'])
        self.assertEqual(receipt['blocked_modules'],['A','Root'])
        self.assertEqual(receipt['completed_modules'],['C','D'])
        self.assertEqual(receipt['modules']['D']['returncode'],0)
    def test_keep_going_parallel_branches(self):
        self.branching_failure()
        self.assertEqual(self.run_builder('--keep-going','--jobs','2','Root'),1)
        self.assertCountEqual(self.invocations(),['B.lean','C.lean','D.lean'])
        self.assertEqual(self.receipt()['blocked_modules'],['A','Root'])
    def test_keep_going_mutation_stops_globally_after_lean_failure(self):
        self.branching_failure()
        self.plan('C.lean','D.lean','import C\n-- mutated\n')
        self.assertEqual(self.run_builder('--keep-going','Root'),125)
        receipt=self.receipt()
        self.assertFalse(receipt['complete'])
        self.assertEqual(self.invocations(),['B.lean','C.lean'])
        self.assertEqual(receipt['failed_modules'],['B','C'])
        self.assertEqual(receipt['blocked_modules'],['A','D','Root'])
    def test_parallel_mutation_wins_over_later_processed_lean_failure(self):
        self.branching_failure()
        self.plan('C.lean','D.lean','import C\n-- mutated\n',wait_for='stub-b-finished')
        original_wait=builder.wait
        original_digest=builder.digest
        def mark_failed_log_hashed(path):
            value=original_digest(path)
            # B's post-compilation input check has finished before its log
            # is hashed. Only then may C mutate an input, independently of
            # process start timing or the runner's speed.
            if path.name=='B.log':
                (self.root/'stub-b-finished').touch()
            return value
        def mutation_first(futures,return_when):
            done,pending=original_wait(futures,return_when=ALL_COMPLETED)
            return sorted(done,key=lambda future:future.result()[0]['returncode'] != 125),pending
        with patch.object(builder,'wait',mutation_first), patch.object(builder,'digest',mark_failed_log_hashed):
            self.assertEqual(self.run_builder('--keep-going','--jobs','2','Root'),125)
        receipt=self.receipt()
        self.assertEqual(receipt['modules']['B']['returncode'],1)
        self.assertEqual(receipt['modules']['C']['returncode'],125)
        self.assertEqual(receipt['blocked_modules'],['A','D','Root'])
        self.assertCountEqual(self.invocations(),['B.lean','C.lean'])
    def test_final_mutation_check_overrides_failed_build(self):
        self.branching_failure()
        original=builder.save_receipt; triggered=False
        def save_and_mutate(path,data):
            nonlocal triggered
            original(path,data)
            if not triggered and data['modules'].get('B',{}).get('returncode')==1:
                triggered=True
                (self.root/'C.lean').write_text('-- mutated after final failed module\n')
        with patch.object(builder,'save_receipt',save_and_mutate):
            self.assertEqual(self.run_builder('Root'),125)
        self.assertIn('source:C',self.receipt()['source_mutations'])
        self.assertFalse(self.receipt()['complete'])
    def test_keep_going_flag_does_not_invalidate_successful_receipts(self):
        self.assertEqual(self.run_builder(),0)
        original_config=self.receipt()['config']
        self.assertEqual(self.run_builder('--keep-going','A'),0)
        self.assertEqual(self.receipt()['config'],original_config)
        self.assertEqual(self.invocations(),['B.lean','A.lean'])
    def test_blocked_cached_rows_are_not_current_completions(self):
        self.branching_failure()
        (self.root/'stub-failures.json').unlink()
        self.assertEqual(self.run_builder('Root'),0)
        self.assertEqual(self.receipt()['completed_modules'],['A','B','C','D','Root'])
        (self.root/'B.lean').write_text('-- changed dependency\n')
        (self.root/'stub-failures.json').write_text(json.dumps({'B.lean':1}))
        self.assertEqual(self.run_builder('--keep-going','Root'),1)
        receipt=self.receipt()
        self.assertFalse(receipt['complete'])
        self.assertEqual(receipt['completed_modules'],['C','D'])
        self.assertEqual(receipt['blocked_modules'],['A','Root'])
        self.assertEqual(receipt['failed_modules'],['B'])
        self.assertEqual(receipt['modules']['A']['returncode'],0)
        self.assertNotIn('A',receipt['completed_modules'])

if __name__=='__main__': unittest.main(verbosity=2)
