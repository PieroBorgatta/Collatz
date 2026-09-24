#!/usr/bin/env python3
"""Regression tests for censoring and the distinction between the two starts."""
import unittest
from descent_probe import evaluate, candidate_tests
from verify_descent import optional_int, starts, syracuse


class FirstPassageTests(unittest.TestCase):
    def test_already_below(self):
        row, word = evaluate(1, 0, 0)
        self.assertEqual((row['tau'], row['coefficient_time'], word), (0, 0, []))

    def test_censored_with_no_homogeneous_crossing(self):
        row, _ = evaluate(11, 2, 0)
        self.assertEqual((row['status'], row['steps_observed'], row['coefficient_time']),
                         ('censored', 22, None))
        table = {r['tau_over_q_bound']:r for r in candidate_tests([row])}
        self.assertEqual(table['2']['violations'], 1)
        self.assertEqual(table['5/2']['unknown_due_to_censoring'], 1)

    def test_integer_censoring_boundary(self):
        row = {'q': 11, 'status': 'censored', 'steps_observed': 27, 'tau': None}
        table = {r['tau_over_q_bound']:r for r in candidate_tests([row])}
        self.assertEqual(table['5/2']['violations'], 1)  # tau>=28>27.5

    def test_blank_csv_integer(self):
        self.assertIsNone(optional_int(''))
        self.assertEqual(optional_int('0'), 0)

    def test_original_and_residual_times_differ(self):
        n,z = starts(3)
        x=n
        for _ in range(13):
            x,_ = syracuse(x)
        self.assertEqual(x, 132859)
        self.assertLess(x,n)
        self.assertGreater(z,n)
        row,_ = evaluate(3)
        self.assertEqual(row['tau'],1)


if __name__ == '__main__':
    unittest.main()
