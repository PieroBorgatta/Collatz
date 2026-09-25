"""Exact independent tests without rerunning the large margin experiment."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import margin_probe as probe


def elementary_bits(start, steps):
    result = []
    for _ in range(steps):
        odd = start % 2
        result.append(odd)
        start = (3 * start + 1) // 2 if odd else start // 2
    return result, start


def valuation_two(nonzero):
    value, count = abs(nonzero), 0
    if not value:
        raise ValueError('finite valuation needs a nonzero integer')
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


class MarginTests(unittest.TestCase):
    def test_horizon_rounding_and_credit_constants(self):
        for v in range(5, 101):
            exact = Fraction(589 * (1 << v), 612)
            H, following = probe.horizon(v), probe.horizon(v + 1)
            self.assertLess(H - 1, exact)
            self.assertLessEqual(exact, H)
            epsilon = 2 * H - following
            self.assertIn(epsilon, (0, 1))
            residue = (589 * (1 << (v - 2))) % 153
            self.assertNotEqual(residue, 0)
            self.assertEqual(epsilon, int(residue <= 76))
            self.assertEqual(epsilon, 2 * probe.horizon(v + 24)
                             - probe.horizon(v + 25))
            K = 589 * (1 << (v - 1)) - 305 * H
            K_next = 589 * (1 << v) - 305 * following
            self.assertEqual(K_next, 2 * K + 305 * epsilon)
            if v >= 15:
                self.assertGreater(K, 128 * v * v)

    def test_margin_recurrence_and_signed_telescoping(self):
        # Alternating extreme counts exercise positive and negative errors.
        for anchor in (5, 15, 16):
            levels = list(range(anchor, anchor + 13))
            counts = [0 if i % 3 == 0 else probe.horizon(v) if i % 3 == 1
                      else probe.horizon(v) // 2 for i, v in enumerate(levels)]
            margins = [(1 << (v - 1)) - j for v, j in zip(levels, counts)]
            errors = [counts[i + 1] - 2 * counts[i]
                      for i in range(len(counts) - 1)]
            for n in range(1, len(levels)):
                self.assertEqual(margins[n], 2 * margins[n - 1] - errors[n - 1])
                signed = sum((Fraction(errors[i], 1 << (i + 1))
                              for i in range(n)), Fraction(0))
                positive = sum((Fraction(max(0, errors[i]), 1 << (i + 1))
                                for i in range(n)), Fraction(0))
                self.assertEqual(Fraction(margins[n], 1 << n), margins[0] - signed)
                self.assertGreaterEqual(Fraction(margins[n], 1 << n),
                                        margins[0] - positive)

    def test_tail_formulas_have_exact_finite_remainders(self):
        for v in range(5, 41):
            for steps in range(21):
                polynomial = sum((Fraction((v + i) ** 2, 1 << (i + 1))
                                  for i in range(steps)), Fraction(0))
                root = sum((Fraction(1 << ((v + i + 1) // 2), 1 << (i + 1))
                            for i in range(steps)), Fraction(0))
                self.assertEqual(probe.quadratic_tail(v), polynomial
                                 + Fraction(probe.quadratic_tail(v + steps),
                                            1 << steps))
                self.assertEqual(probe.root_tail(v), root
                                 + Fraction(probe.root_tail(v + steps),
                                            1 << steps))

    def test_conditional_bound_propagation_and_anchor_costs(self):
        for anchor, coefficient, tail, bound in (
                (17, 4, probe.quadratic_tail, lambda v: v * v),
                (16, 2, probe.root_tail, lambda v: 1 << ((v + 1) // 2))):
            slack = 131
            margin = coefficient * tail(anchor) + slack
            for v in range(anchor, anchor + 20):
                expected = (1 << (v - anchor)) * slack + coefficient * tail(v)
                self.assertEqual(margin, expected)
                self.assertGreater(margin, 0)
                # Equality is the worst case when every error saturates the bound.
                margin = 2 * margin - coefficient * bound(v)
        self.assertEqual(2 * probe.root_tail(15), 768)
        self.assertEqual(2 * probe.root_tail(16), 1024)
        self.assertEqual(2 * probe.root_tail(17), 1536)
        self.assertEqual(4 * probe.quadratic_tail(16), 1164)
        self.assertEqual(4 * probe.quadratic_tail(17), 1304)

    def test_quadratic_isometry_and_finite_permutations(self):
        for v in (0, 1, 5):
            for bits in range(1, 8):
                modulus = 1 << bits
                image = [probe.quadratic(v, x) % modulus for x in range(modulus)]
                self.assertEqual(set(image), set(range(modulus)))
                for x in range(modulus):
                    for y in range(x):
                        self.assertEqual(valuation_two(probe.quadratic(v, x)
                                                       - probe.quadratic(v, y)),
                                         valuation_two(x - y))

    def test_quadratic_lift_against_complete_small_bruteforce(self):
        for v in (0, 2, 5):
            for H in range(1, 6):
                for K in range(H, 2 * H + 1):
                    modulus = 1 << K
                    for lower in range(1 << H):
                        images = {}
                        for x in range(lower, modulus, 1 << H):
                            # Use the polynomial itself, not the lifting derivative.
                            target = (x + 2 ** (v + 2) * x * x) % modulus
                            images.setdefault(target, []).append(x)
                        for target, solutions in images.items():
                            self.assertEqual(len(solutions), 1)
                            self.assertEqual(probe.lift_quadratic(v, lower, H,
                                                                  target, K),
                                             solutions[0])

    def test_quadratic_lift_rejects_invalid_or_incompatible_inputs(self):
        invalid = (
            (-1, 0, 1, 0, 1),
            (0, 0, 0, 0, 0),
            (0, 0, 2, 0, 1),
            (0, 0, 2, 0, 5),
            (0, -1, 2, 0, 3),
            (0, 4, 2, 0, 3),
            (0, 0, 2, -1, 3),
            (0, 0, 2, 8, 3),
            (0, 0, 2, 1, 3),
        )
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                probe.lift_quadratic(*args)

    def test_generic_adversaries_by_elementary_iteration(self):
        for v, kind in ((6, 'unit_prefix'), (8, 'actual_prefix')):
            row = probe.adversary(v, kind)
            X, Y = int(row['X_hex'], 16), int(row['Y_hex'], 16)
            H, K = row['H'], row['H_next']
            Q = (9 ** (2 ** v) - 1) // (2 ** (v + 3))
            Q_next = (9 ** (2 ** (v + 1)) - 1) // (2 ** (v + 4))
            low_bits, _ = elementary_bits(X, H)
            upper_bits, _ = elementary_bits(Y, K)
            self.assertEqual(Y, X + 2 ** (v + 2) * X ** 2)
            self.assertEqual(upper_bits[H:], [1] * (K - H))
            self.assertEqual(row['lower_odd'], sum(low_bits))
            self.assertEqual(row['upper_odd'], sum(upper_bits))
            self.assertEqual(row['upper_head_odd'], sum(upper_bits[:H]))
            self.assertEqual(row['lower_margin'], 2 ** (v - 1) - sum(low_bits))
            self.assertEqual(row['upper_margin'], 2 ** v - sum(upper_bits))
            self.assertEqual(row['delta'], sum(upper_bits) - 2 * sum(low_bits))
            self.assertGreater(row['lower_margin'], 0)
            self.assertLess(row['upper_margin'], 0)
            self.assertGreater(X, 0)
            self.assertNotEqual(X, Q)
            self.assertEqual(X >> K, Q >> K)
            self.assertEqual(X.bit_length(), Q.bit_length())
            self.assertLess(abs(X - Q), 1 << K)
            self.assertLess(Q_next, 4 * Y)
            self.assertLess(Y, 4 * Q_next)
            if kind == 'actual_prefix':
                self.assertEqual(low_bits, elementary_bits(Q, H)[0])
                self.assertEqual((X - Q) % (1 << H), 0)
            else:
                self.assertEqual(low_bits, [1, 0] * (H // 2) + [1] * (H % 2))

    def test_baseline_covers_exactly_existing_levels_and_known_anchors(self):
        baseline, fingerprints = probe.references()
        self.assertEqual(sorted(baseline), list(range(5, 25)))
        self.assertEqual(len(fingerprints), 3)
        first_root_anchor = first_quadratic_anchor = None
        for v, row in sorted(baseline.items()):
            self.assertEqual(row['horizon'], probe.horizon(v))
            margin = (1 << (v - 1)) - row['odd_steps']
            if margin >= 2 * probe.root_tail(v) and first_root_anchor is None:
                first_root_anchor = v
            if margin >= 4 * probe.quadratic_tail(v) and first_quadratic_anchor is None:
                first_quadratic_anchor = v
            if v <= 8:
                Q = (9 ** (1 << v) - 1) // (1 << (v + 3))
                bits, _ = elementary_bits(Q, row['horizon'])
                self.assertEqual(sum(bits), row['odd_steps'])
                residue_bytes = (Q % (1 << row['horizon'])).to_bytes(
                    (row['horizon'] + 7) // 8, 'little')
                self.assertEqual(hashlib.sha256(residue_bytes).hexdigest(),
                                 row['initial_residue_sha256'])
                if 'parity_trace_sha256' in row:
                    packed = sum(bit << i for i, bit in enumerate(bits)).to_bytes(
                        (row['horizon'] + 7) // 8, 'little')
                    self.assertEqual(hashlib.sha256(packed).hexdigest(),
                                     row['parity_trace_sha256'])
        self.assertEqual(first_root_anchor, 16)
        self.assertEqual(first_quadratic_anchor, 17)

    def test_baseline_rejects_changed_counts_horizons_and_hashes(self):
        baseline, _ = probe.references()
        expected = baseline[15]
        original = {'v': 15, **expected}
        probe.check_reference(original, expected)
        for key, value in expected.items():
            changed = dict(original)
            changed[key] = value + 1 if isinstance(value, int) else 'altered-' + value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,
                                                             'baseline mismatch'):
                probe.check_reference(changed, expected)

    def test_overlapping_baselines_reject_tampered_source_file(self):
        # Intercept reads; the actual frozen baseline files are never modified.
        original_read = Path.read_bytes

        def changed_read(path):
            raw = original_read(path)
            if path == probe.COMPENSATION / 'calibration_results.json':
                data = json.loads(raw)
                data['rows'][0]['odd_steps'] += 1
                return json.dumps(data).encode()
            return raw

        with patch.object(Path, 'read_bytes', changed_read):
            with self.assertRaises(AssertionError):
                probe.references()


if __name__ == '__main__':
    unittest.main()
