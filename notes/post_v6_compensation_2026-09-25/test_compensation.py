#!/usr/bin/env python3
import itertools
import json
from pathlib import Path
import random
import tempfile
import unittest

from block_engine import direct_trace, horizon, initial_residue, parity_trace, summarize_trace
from compensation_probe import first_violation, holdout


def packed(word):
    return sum(bit << i for i, bit in enumerate(word)).to_bytes((len(word) + 7) // 8, 'little')


class CompensationTests(unittest.TestCase):
    def test_recursive_trace_against_elementary_replay(self):
        rng = random.Random(20260925)
        for bits in (1, 2, 7, 8, 15, 16, 17, 31, 33, 65, 137, 513):
            for _ in range(4):
                residue = rng.randrange(1 << bits)
                expected = direct_trace(residue, bits)
                for width in (1, 5, 16):
                    self.assertEqual(parity_trace(residue, bits, width), expected)
                self.assertEqual(parity_trace(residue, bits, method='linear'), expected)

    def test_initial_residue_against_full_integer(self):
        for v in range(5, 12):
            Q = (9 ** (1 << v) - 1) // (1 << (v + 3))
            for bits in (1, 17, horizon(v)):
                self.assertEqual(initial_residue(v, bits), Q % (1 << bits))

    def test_extrema_and_witnesses_exhaustively(self):
        for n in range(1, 8):
            for word in itertools.product((0, 1), repeat=n):
                for drift in (0, 1):
                    values = [0]
                    for bit in word:
                        values.append(values[-1] + 306 - drift - 589 * bit)
                    best = min(((values[s] - values[t], s, t)
                                for s in range(n + 1) for t in range(s, n + 1)),
                               key=lambda x: (-x[0], x[1], x[2]))
                    for block in (1, 3, 256):
                        row = summarize_trace(packed(word), n, block, drift)
                        self.assertEqual(row['maximum_drawdown'], best[0])
                        self.assertEqual((row['drawdown_from_step'], row['drawdown_to_step']), best[1:])
                        self.assertEqual(row['minimum_at_step'], values.index(min(values)))
                        self.assertEqual(row['maximum_at_step'], values.index(max(values)))

    def test_credit_identity_and_first_failure(self):
        for word in itertools.product((0, 1), repeat=8):
            for D in (0, 284, 700):
                C = peak = 0
                credit, first = D, None
                for r, bit in enumerate(word, 1):
                    delta = 305 - 589 * bit
                    C += delta
                    peak = max(peak, C)
                    credit = min(D, credit + delta)
                    self.assertEqual(credit, D + C - peak)
                    if credit < 0 and first is None:
                        first = {'step': r, 'credit': credit}
                self.assertEqual(first_violation(packed(word), len(word), D), first)

    def test_terminal_success_does_not_imply_bounded_loss(self):
        # A negative credit excursion can later be followed by terminal success.
        word = [1] * 4 + [0] * 8
        row = summarize_trace(packed(word), len(word), drift=1)
        self.assertGreater(row['balance_end'] + len(word), 0)
        self.assertGreater(row['maximum_drawdown'], 1000)
        self.assertIsNotNone(first_violation(packed(word), len(word), 1000))

    def test_rounding_and_tail_threshold(self):
        for v in range(5, 60):
            H, K = horizon(v), 1 << (v - 1)
            self.assertTrue(0 <= 306 * H - 589 * K < 306)
            self.assertLess(306 * H - 589 * (K + 1), 0)
            self.assertGreater(horizon(v + 1) * v * v, H * (v + 1) ** 2)
        self.assertLess(horizon(14), 128 * 14 ** 2)
        self.assertGreaterEqual(horizon(15), 128 * 15 ** 2)

    def test_partial_trace_boundary(self):
        with self.assertRaises(ValueError):
            summarize_trace(bytes([255]), 3)
        row = summarize_trace(bytes([5]), 3, block_size=2)
        self.assertEqual([b['length'] for b in row['blocks']], [2, 1])
        self.assertEqual(row['odd_steps'], 2)

    def test_changed_frozen_engine_rejected_before_holdout(self):
        spec = {'holdout_levels': [22, 23, 24], 'drift': 1, 'coefficient': 128,
                'sufficient_tail_starts_at_v': 15,
                'frozen_inputs_sha256': {'block_engine.py': '0' * 64}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'
            path.write_text(json.dumps(spec))
            with self.assertRaisesRegex(ValueError, 'Frozen input changed'):
                holdout(path)


if __name__ == '__main__':
    unittest.main()
