#!/usr/bin/env python3
"""Boundary, negative-result, and independent small-orbit checks."""
import json
import unittest
from fractions import Fraction

from induction_probe import BASELINE, check_pair, cone_counterexample, family, horizons, step, trace_at


def slow_step(x):
    y, a = 3 * x + 1, 0
    while y % 2 == 0:
        y //= 2
        a += 1
    return y, a


class InductionTests(unittest.TestCase):
    def test_negative_coefficient_cone_family(self):
        for a in range(4, 42, 2):
            row = cone_counterexample(a)
            self.assertEqual(slow_step(row["x"]), (row["next_x"], a))
            self.assertEqual(slow_step(row["y"]), (row["next_y"], 3))
            alpha = Fraction(96 * 2 ** (2 * a), 3 * 2 ** 3)
            beta = Fraction(2 ** a, 2 ** 3) * (-1 - Fraction(2 * 96, 3))
            gamma = Fraction(Fraction(96, 3) + 1 + 3 * 2 + 1, 2 ** 3)
            self.assertEqual([alpha, beta, gamma], row["coefficients_after"])
        self.assertEqual(cone_counterexample()["coefficients_after"], [1024, -130, 5])

    def test_fixed_horizons(self):
        self.assertEqual(horizons(8, 67), {"double": 134, "linear_3v": 158,
                         "quadratic_v2": 198, "quarter_level": 198})

    def test_visit_does_not_mean_final_endpoint(self):
        self.assertEqual(trace_at(9, 9, {1, 2}), ({1: (7, 2), 2: (11, 3)}, 1))

    def test_algebraic_equality_boundary(self):
        N, X, c, w, wp = 3, 7, 128, Fraction(1, 4), Fraction(3, 64)
        self.assertEqual(c * wp, 96 * w * w)
        self.assertLess(w * X, N)
        self.assertLess(wp * (X + c * X * X), 96 * N * N + 96 * N)
        # Removing the strict lower homogeneous bound loses strictness.
        N = X = c = w = 1
        wp = 96
        self.assertEqual(wp * (X + c * X * X), 96 * N * N + 96 * N)

    def test_independent_small_orbits_and_fraction_comparisons(self):
        records = {r["v"]: r for r in json.loads(BASELINE.read_text())["actual_cases"]}
        for v in (5, 6, 8):
            row = check_pair(v, records[v], records[v + 1])
            X, N = family(v)
            Y, M = family(v + 1)
            y, B, first = Y, 0, None
            times = {a["ell"] for a in row["attempts"]}
            snapshots = {}
            for j in range(1, max(times | {row["upper_tau"]}) + 1):
                y, b = slow_step(y)
                B += b
                if y < M and first is None:
                    first = j
                if j in times:
                    snapshots[j] = (y, B)
            self.assertEqual(first, row["upper_tau"])
            w = Fraction(3 ** row["lower_tau"], 2 ** row["lower_A"])
            self.assertLess(w * X, N)
            for attempt in row["attempts"]:
                ell = attempt["ell"]
                y, B = snapshots[ell]
                wp = Fraction(3 ** ell, 2 ** B)
                self.assertEqual(B, attempt["B"])
                self.assertEqual((2 ** (v + 2)) * wp / w ** 2 <= 96, attempt["alpha_le_96"])
                self.assertEqual(3 * wp * Y < 3 * M - ell, attempt["generic_certificate_passed"])
                self.assertEqual(y < M, attempt["upper_endpoint_below_source"])

    def test_altered_baseline_rejected(self):
        records = {r["v"]: r for r in json.loads(BASELINE.read_text())["actual_cases"]}
        bad_lower = dict(records[5], exponent_sum=13)
        with self.assertRaises(AssertionError):
            check_pair(5, bad_lower, records[6])
        bad_upper = dict(records[6], tau_from_Q=29)
        with self.assertRaises(AssertionError):
            check_pair(5, records[5], bad_upper)

    def test_generic_certificate_small_grid(self):
        # Independent arithmetic implementation, including time zero and x<N.
        for x in range(1, 64, 2):
            y, A, minimum = x, 0, x
            for k in range(9):
                for N in range(1, 65):
                    if k < 3 * N and 3 ** (k + 1) * x < 2 ** A * (3 * N - k):
                        self.assertLess(minimum, N)
                y, a = slow_step(y)
                A += a
                minimum = min(minimum, y)

    def test_input_boundaries(self):
        for x in (0, -1, 2):
            with self.assertRaises(ValueError):
                step(x)
        self.assertEqual(trace_at(1, 2, {0}), ({0: (1, 0)}, 0))
        with self.assertRaises(ValueError):
            trace_at(1, 2, set())


if __name__ == "__main__":
    unittest.main()
