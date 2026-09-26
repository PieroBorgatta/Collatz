"""Independent finite checks for the new basin diagnostic, 2026-09-26."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from basin_probe import census, direct_counts, orbit_siblings, sibling, step
from verify_basin_results import compare


class BasinCensusTests(unittest.TestCase):
    def test_ordinary_replay_matches_weighted_odd_graph(self):
        for bound in (1, 2, 3, 17, 128, 1024):
            self.assertEqual(census(bound)[0], direct_counts(bound))

    def test_selected_sibling_domains(self):
        for n in range(5, 1000, 2):
            if n % 3:
                y = sibling(n)
                self.assertEqual(step(y), step(n))
                self.assertTrue(n < y <= 16 * n + 5)
                self.assertNotEqual(y % 3, 0)
                self.assertEqual(y % 2, 1)

    def test_invalid_sources_rejected(self):
        for n in (0, 1, 2, 3, 9, -5):
            with self.assertRaises(ValueError):
                sibling(n)
        for n in (0, 2, -1):
            with self.assertRaises(ValueError):
                step(n)

    def test_unfinished_path_is_an_error(self):
        with self.assertRaises(RuntimeError):
            census(3, max_new_steps=1)

    def test_sibling_basins_are_disjoint_by_individual_sources(self):
        pairs = orbit_siblings()
        targets = {y for _, y in pairs}
        counts = Counter()
        for source in range(1, 2049):
            n, visited_targets = source, set()
            while True:
                if n in targets:
                    visited_targets.add(n)
                if n == 1:
                    break
                n = 3 * n + 1 if n % 2 else n // 2
            self.assertLessEqual(len(visited_targets), 1)
            counts.update(visited_targets)
        weighted = census(2048)[0]
        for y in targets:
            self.assertEqual(counts[y], weighted[y])

    def test_comparison_only_tolerates_display_ratio_rounding(self):
        expected = {"count": 7, "complete": True, "exact_float": 1.0,
                    "rows": [{"scaled_ratio_float": 1.0}]}
        rounded = copy.deepcopy(expected)
        rounded["rows"][0]["scaled_ratio_float"] += 5e-13
        compare(expected, rounded)

        mismatches = {
            "integer value": {"count": 8},
            "integer type": {"count": 7.0},
            "boolean type": {"complete": 1},
            "shorter list": {"rows": []},
            "longer list": {"rows": expected["rows"] * 2},
            "list type": {"rows": {}},
            "ratio outside tolerance": {"rows": [{"scaled_ratio_float": 1.000001}]},
            "ratio type": {"rows": [{"scaled_ratio_float": 1}]},
            "other float changed": {"exact_float": 1.0 + 5e-13},
            "extra key": {"extra": 0},
        }
        for label, changed in mismatches.items():
            with self.subTest(label=label):
                actual = {**expected, **changed}
                with self.assertRaises(ValueError):
                    compare(expected, actual)
        with self.assertRaises(ValueError):
            compare(expected, {"count": 7})

    def test_optimized_python_rejects_altered_json(self):
        verifier = Path(__file__).with_name("verify_basin_results.py")
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "expected.json"
            altered = Path(directory) / "altered.json"
            expected.write_text(json.dumps({"base_count": 7}))
            altered.write_text(json.dumps({"base_count": 8}))
            result = subprocess.run(
                [sys.executable, "-O", str(verifier), str(expected), str(altered)],
                capture_output=True, text=True, timeout=10, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError: root.base_count", result.stderr)
        self.assertNotIn("Exact integer census matches", result.stdout)


if __name__ == "__main__":
    unittest.main()
