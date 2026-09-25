#!/usr/bin/env python3
"""Cross-language replay boundaries and rejection of altered evidence."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from verify_holdout import validate_document, validate_row

VERIFIER = Path(sys.argv.pop(1)).resolve()
HERE = Path(__file__).resolve().parent


class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((HERE / 'calibration_results.json').read_text())['rows'][0]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.bin'
            result = subprocess.run([str(VERIFIER), '--v', '10', '--trace', str(path)],
                                    check=True, capture_output=True, text=True)
            cls.actual, cls.trace = json.loads(result.stdout), path.read_bytes()

    def test_different_block_widths(self):
        for width in (1, 7, 16, 31, 32):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'trace.bin'
                result = subprocess.run([str(VERIFIER), '--v', '10', '--block-width', str(width),
                                         '--trace', str(path)], check=True, capture_output=True, text=True)
                validate_row(self.expected, json.loads(result.stdout), path.read_bytes())
                self.assertEqual(path.read_bytes(), self.trace)

    def test_altered_parity_and_padding_rejected(self):
        for index, mask in ((0, 1), (-1, 128)):
            trace = bytearray(self.trace)
            trace[index] ^= mask
            with self.assertRaises(ValueError):
                validate_row(self.expected, self.actual, trace)

    def test_altered_witness_rejected(self):
        expected = copy.deepcopy(self.expected)
        expected['C']['drawdown_to_step'] += 1
        with self.assertRaisesRegex(ValueError, 'extrema/witness mismatch'):
            validate_row(expected, self.actual, self.trace)

    def test_altered_candidate_decision_rejected(self):
        expected = copy.deepcopy(self.expected)
        D = 128 * expected['v'] ** 2
        expected['candidate'] = {'capacity': D,
            'minimum_credit': D - expected['C']['maximum_drawdown'],
            'passed': False, 'terminal_guarantee_if_passed': expected['horizon'] - D,
            'first_violation': None}
        with self.assertRaisesRegex(ValueError, 'Candidate decision mismatch'):
            validate_row(expected, self.actual, self.trace)

    def test_out_of_range_inputs_rejected(self):
        for args in (['--v', '25'], ['--v', '4'], ['--v', '10', '--block-width', '33']):
            result = subprocess.run([str(VERIFIER)] + args, capture_output=True)
            self.assertEqual(result.returncode, 2)

    def test_missing_holdout_decision_rejected(self):
        document = json.loads((HERE / 'holdout_results.json').read_text())
        validate_document(document)
        del document['rows'][0]['candidate']
        with self.assertRaisesRegex(ValueError, 'Missing candidate decisions'):
            validate_document(document)

    def test_altered_holdout_summary_rejected(self):
        source = json.loads((HERE / 'holdout_results.json').read_text())
        for field, value in [('coefficient', 256), ('all_passed', False),
                             ('failed_levels', [22]), ('protocol_sha256', '0' * 64)]:
            document = copy.deepcopy(source)
            document[field] = value
            with self.assertRaises(ValueError):
                validate_document(document)


if __name__ == '__main__':
    unittest.main()
