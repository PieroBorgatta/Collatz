#!/usr/bin/env python3
"""Independent integer replay of the frozen seven-ancestor falsification.

The oracle uses the closed form of G and the full integer Collatz orbit.
It neither generates an ancestry chain nor truncates a parity residue.
This is an implementation cross-check, not external scientific review.
"""
from functools import lru_cache
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seven_probe as probe


def closed_G(u, depth, x):
    numerator = (1 + 2**(u+3)*x)**(2**depth) - 1
    denominator = 2**(u+depth+3)
    value, remainder = divmod(numerator, denominator)
    if remainder:
        raise AssertionError('nonintegral closed-form ancestor composition')
    return value


def Q(v):
    return (9**(2**v) - 1) // 2**(v+3)


def H(v):
    return (589*2**v + 611) // 612


@lru_cache(maxsize=None)
def full_orbit(n, steps):
    data = bytearray((steps+7)//8)
    odd = 0
    for t in range(steps):
        p = n & 1
        odd += p
        data[t//8] |= p << (t % 8)
        n = (3*n+1) >> 1 if p else n >> 1
    return bytes(data), odd, n


def first_root_at_least(u, depth, target):
    """Monotone integer binary search, independent of repeated square roots."""
    lo, hi = 0, 1
    while closed_G(u, depth, hi) < target:
        hi *= 2
    while lo+1 < hi:
        mid = (lo+hi)//2
        if closed_G(u, depth, mid) < target:
            lo = mid
        else:
            hi = mid
    return hi


def interval_oracle(v):
    u = v-7
    boundary = 2**(Q(v+1).bit_length()-1)
    L = first_root_at_least(u, 8, boundary)
    U = first_root_at_least(u, 8, 2*boundary)-1
    q, step = Q(u), 2*3**(2**(u-1))
    first = L + (q-L) % step
    last = U - (U-q) % step
    return {'v': v, 'u': u, 'L': L, 'U': U, 'Q_u': q, 'step': step,
            'ternary_precision': 2**(u-1),
            't_min': (first-q)//step, 't_max': (last-q)//step,
            'first': first, 'last': last, 'count': (last-first)//step+1}


def v3(n):
    if n == 0:
        return None
    answer = 0
    n = abs(n)
    while n % 3 == 0:
        n //= 3
        answer += 1
    return answer


class SevenAncestorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pre = json.loads((HERE/'presearch_interval.json').read_text())
        cls.result = json.loads((HERE/'seven_results.json').read_text())
        cls.search = cls.result['search']
        cls.replayed = []
        for row in cls.search['visited']:
            x = row['ancestor']
            lower, upper = closed_G(4, 7, x), closed_G(4, 8, x)
            low_trace, low_j, _ = full_orbit(lower, H(11))
            up_trace, up_j, _ = full_orbit(upper, H(12))
            cls.replayed.append({'source': x, 'lower': lower, 'upper': upper,
                                 'low_trace': low_trace, 'up_trace': up_trace,
                                 'lower_margin': 2**10-low_j,
                                 'upper_margin': 2**11-up_j})

    def test_frozen_protocol_and_interval_hash_agree(self):
        digest = hashlib.sha256((HERE/'PROTOCOL_IT.md').read_bytes()).hexdigest()
        self.assertEqual(self.pre['protocol_sha256'], digest)
        self.assertEqual(self.result['protocol_sha256'], digest)
        self.assertFalse(self.pre['parity_outcomes_examined'])
        self.assertEqual(self.result['new_tower_levels'], [])
        self.assertEqual(self.result['new_lean_declarations'], 0)
        for key, value in interval_oracle(11).items():
            if key != 'ternary_precision':
                self.assertEqual(self.pre[key], value)

    def test_closed_form_matches_small_compositions(self):
        for u in range(5):
            for x in range(1, 18):
                actual = probe.chain(u, x, 8)
                expected = [closed_G(u, d, x) for d in range(9)]
                self.assertEqual(actual, expected)
                self.assertEqual(expected[0], x)
        for u in range(5):
            for d in range(6):
                self.assertEqual(closed_G(u, d, Q(u)), Q(u+d))

    def test_independent_binary_search_and_four_interval_boundaries(self):
        for v in (10, 11):
            expected = interval_oracle(v)
            self.assertEqual(probe.candidate_interval(v), expected)
            u, L, U = expected['u'], expected['L'], expected['U']
            boundary = 2**(Q(v+1).bit_length()-1)
            self.assertLess(closed_G(u, 8, L-1), boundary)
            self.assertGreaterEqual(closed_G(u, 8, L), boundary)
            self.assertLess(closed_G(u, 8, U), 2*boundary)
            self.assertGreaterEqual(closed_G(u, 8, U+1), 2*boundary)
            self.assertLess(expected['first']-expected['step'], L)
            self.assertGreater(expected['last']+expected['step'], U)
            self.assertEqual(expected['first'] % 2, 1)
            self.assertEqual(expected['last'] % 2, 1)
        self.assertEqual(interval_oracle(11)['count'], 2991085)
        self.assertEqual((self.pre['t_min'], self.pre['t_max']), (-38252, 2952832))

    def test_small_intervals_exhaustively(self):
        # Finite enumeration tests empty intervals and inclusive endpoints.
        for u in range(3):
            for depth in range(4):
                for boundary in range(1, 33):
                    values = [x for x in range(1, 2*boundary)
                              if boundary <= closed_G(u, depth, x) < 2*boundary]
                    L, U = probe.ancestor_interval(u, u+depth, boundary)
                    self.assertEqual(list(range(L, U+1)), values)

    def test_all_sixty_full_integer_parity_traces(self):
        self.assertEqual(len(self.replayed), 60)
        for row, actual in zip(self.search['visited'], self.replayed):
            self.assertEqual(row['lower_margin'], actual['lower_margin'])
            self.assertEqual(row['upper_margin'], actual['upper_margin'])
            for prefix, source, length in (('low', actual['lower'], H(11)),
                                            ('up', actual['upper'], H(12))):
                packed = actual[prefix+'_trace']
                key = 'lower_trace_sha256' if prefix == 'low' else 'upper_trace_sha256'
                self.assertEqual(hashlib.sha256(packed).hexdigest(), row[key])
                # Compare every parity byte, rather than relying only on SHA.
                self.assertEqual(probe.trace(source, length), packed)
                self.assertEqual(len(packed), (length+7)//8)
                if length % 8:
                    self.assertEqual(packed[-1] >> (length % 8), 0)

    def test_first_failure_and_search_order(self):
        rows = self.search['visited']
        expected_t = list(range(-38252, -38192))
        self.assertEqual([r['t'] for r in rows], expected_t)
        self.assertEqual([r['ancestor'] for r in rows],
                         [Q(4)+2*3**8*t for t in expected_t])
        failures = [i for i, row in enumerate(self.replayed)
                    if row['lower_margin'] >= 0 > row['upper_margin']]
        self.assertEqual(failures, [59])
        self.assertEqual(self.replayed[-1]['source'], 14476219056859)
        self.assertEqual((self.replayed[-1]['lower_margin'], self.replayed[-1]['upper_margin']),
                         (34, -18))
        self.assertEqual(self.search['status'], 'counterexample')
        self.assertEqual(self.search['visited_count'], 60)
        self.assertFalse(self.search['interval_exhausted'])
        self.assertEqual(self.search['limit'], 100000)

    def test_witness_full_ancestry_congruences_binades_and_record(self):
        witness = self.search['witness']
        x = 14476219056859
        self.assertEqual(witness['t'], -38193)
        self.assertEqual(witness['ancestor'], x)
        self.assertFalse(witness['is_actual_tower'])
        self.assertEqual(witness, probe.record_candidate(11, -38193))
        self.assertEqual(len(witness['levels']), 9)
        for depth, row in enumerate(witness['levels']):
            w = 4+depth
            n = closed_G(4, depth, x)
            self.assertEqual(int(row['value_hex'], 16), n)
            self.assertEqual(row['v'], w)
            self.assertEqual(n.bit_length(), Q(w).bit_length())
            self.assertEqual(row['bits'], n.bit_length())
            self.assertEqual(n % 2, 1)
            self.assertEqual((n-Q(w)) % 3**(2**(w-1)), 0)
            self.assertEqual(row['required_ternary_precision'], 2**(w-1))
            self.assertEqual(row['difference_valuation3'], v3(n-Q(w)))
            self.assertEqual(row['signature_valuation3'], v3(1+2**(w+3)*n))
            self.assertEqual(row['difference_valuation3'], 9*2**depth)
            if depth:
                root = isqrt(1+2**(w+3)*n)
                self.assertEqual(root*root, 1+2**(w+3)*n)
                self.assertEqual((root-1) % 2**(w+2), 0)
                self.assertEqual((root-1)//2**(w+2), closed_G(4, depth-1, x))
            self.assertEqual(probe.recover_ancestor(w, n, depth), x)
        for label, key, length in (('lower', 'low_trace', H(11)), ('upper', 'up_trace', H(12))):
            packed = self.replayed[-1][key]
            self.assertEqual(witness[label]['packed_lsb_first_hex'], packed.hex())
            self.assertEqual(witness[label]['length'], length)
            self.assertEqual(witness[label]['odd_steps'],
                             2**(10 if label == 'lower' else 11)-witness[label+'_margin'])

    def test_actual_tower_comparison_uses_full_historical_words(self):
        actual = self.result['actual_tower_comparison']
        self.assertTrue(actual['is_actual_tower'])
        self.assertEqual(actual['t'], 0)
        self.assertEqual(actual['ancestor'], Q(4))
        baseline = json.loads((HERE.parent/'post_v6_margin_2026-09-25/margin_results.json').read_text())
        levels = {row['v']: row for row in baseline['levels']}
        for w, label in ((11, 'lower'), (12, 'upper')):
            packed, odd, _ = full_orbit(Q(w), H(w))
            self.assertEqual(actual[label]['packed_lsb_first_hex'], packed.hex())
            self.assertEqual(actual[label]['odd_steps'], odd)
            self.assertEqual(actual[label]['parity_trace_sha256'], hashlib.sha256(packed).hexdigest())
            self.assertEqual(actual[label]['parity_trace_sha256'], levels[w]['parity_trace_sha256'])
            self.assertEqual(actual[label+'_margin'], 2**(w-1)-odd)
            self.assertGreaterEqual(actual[label+'_margin'], 0)
        for row in actual['levels']:
            self.assertEqual(int(row['value_hex'], 16), Q(row['v']))
            self.assertIsNone(row['difference_valuation3'])
            self.assertEqual(row['signature_valuation3'], 2**(row['v']+1))

    def test_bounded_search_reports_partial_and_stops_at_first_failure(self):
        for limit in (1, 59, 60, 61):
            result = probe.search(11, limit)
            self.assertEqual(result['visited'], self.search['visited'][:min(limit, 60)])
            self.assertEqual(result['visited_count'], min(limit, 60))
            self.assertFalse(result['interval_exhausted'])
            self.assertEqual(result['status'], 'partial_no_counterexample' if limit < 60 else 'counterexample')
            if limit < 60:
                self.assertIsNone(result['witness'])
            else:
                self.assertEqual(result['witness'], self.search['witness'])

    def test_twelve_filtered_roots_at_v10_are_only_a_finite_success(self):
        old = json.loads((HERE.parent/'post_v6_ancestry_2026-09-25/ancestry_results.json').read_text())
        retained = [row for row in old['exhaustive_ancestry_filter']['rows']
                    if row['quarter_ternary_constraint']]
        expected = list(range(672605, 674388, 162))
        self.assertEqual([r['anchor'] for r in retained], expected)
        self.assertEqual(len(retained), 12)
        for row in retained:
            x = row['anchor']
            for w, depth, label in ((10, 7, 'lower'), (11, 8, 'upper')):
                n = closed_G(3, depth, x)
                packed, odd, _ = full_orbit(n, H(w))
                self.assertEqual(probe.trace(n, H(w)), packed)
                self.assertEqual(row[label+'_margin'], 2**(w-1)-odd)
            self.assertGreaterEqual(row['upper_margin'], 0)
        self.assertEqual(min(row['upper_margin'] for row in retained), 6)
        partial, complete = probe.search(10, 11), probe.search(10, 12)
        self.assertEqual(partial['status'], 'partial_no_counterexample')
        self.assertFalse(partial['interval_exhausted'])
        self.assertEqual(complete['status'], 'finite_case_verified')
        self.assertTrue(complete['interval_exhausted'])
        self.assertEqual(complete['visited_count'], 12)
        self.assertIsNone(complete['witness'])
        self.assertEqual([r['ancestor'] for r in complete['visited']], expected)

    def test_invalid_limits_and_candidate_boundaries(self):
        for call in (lambda: probe.candidate_interval(9),
                     lambda: probe.search(11, 0),
                     lambda: probe.record_candidate(11, self.pre['t_min']-1),
                     lambda: probe.record_candidate(11, self.pre['t_max']+1)):
            with self.assertRaises(ValueError):
                call()
        self.assertEqual(probe.valuation3(0), None)
        self.assertEqual(probe.valuation3(-2*3**9), 9)
        self.assertEqual(probe.valuation3(10), 0)


if __name__ == '__main__':
    unittest.main()
