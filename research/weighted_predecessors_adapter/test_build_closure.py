#!/usr/bin/env python3
"""Regression tests for receipt handling; the stub is NOT a Lean verifier."""
from contextlib import redirect_stdout
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
import hashlib, json, os
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
        target=Path(action['target'])
        if action.get('delete'): target.unlink()
        else: target.write_text(action['text'])
        plan.unlink()
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
    def run_builder(self):
        with patch.object(sys,'argv',['build_closure.py','A']), redirect_stdout(io.StringIO()):
            return builder.main()
    def receipt(self):
        return json.loads((self.root/'build/weighted-replay/receipt.json').read_text())
    def plan(self,on,target,text='-- mutated\n',delete=False):
        (self.root/'stub-plan.json').write_text(json.dumps(dict(on=on,target=target,text=text,delete=delete)))
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

if __name__=='__main__': unittest.main(verbosity=2)
