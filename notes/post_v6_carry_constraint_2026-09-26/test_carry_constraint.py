#!/usr/bin/env python3
"""Independent finite oracles for the carry-constraint experiment.

These tests do not search the prospective level or prove a uniform bound.
The small-domain oracles use ordinary integer products, nested triangular
convolution, and direct shortcut iteration rather than the probe formulas.
"""
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import unittest

import carry_constraint_probe as probe


HERE = Path(__file__).resolve().parent


def shortcut_word(source, length):
    word = 0
    for step in range(length):
        odd = source & 1
        word |= odd << step
        source = (3 * source + 1) // 2 if odd else source // 2
    return word


def schoolbook_carry(source, columns):
    bits = [(source >> i) & 1 for i in range(columns)]
    carry = 0
    for n in range(columns):
        coefficient = sum(bits[i] * bits[n-i] for i in range(n+1))
        carry = (carry + coefficient) // 2
    return carry


def triangular_numerator(source, columns):
    positions = [i for i in range(columns) if (source >> i) & 1]
    return sum(1 << (i+j) for i in positions for j in positions
               if i+j < columns)


def horizon(level):
    return (589 * (1 << level) + 611) // 612


def exact_source(level):
    return (3 ** (1 << (level+1)) - 1) >> (level+3)


def independent_fiber(level):
    H, K, r = horizon(level), horizon(level+1), level+3
    source = exact_source(level)
    n = r+K
    target = triangular_numerator(1+(source << r), n) >> n
    prefix, high = source % (1 << H), (source >> K) << K
    lower_odd = shortcut_word(source, H).bit_count()
    before, after, labels = Counter(), Counter(), Counter()
    for suffix in range(1 << (K-H)):
        x = high | (suffix << H) | prefix
        carry = triangular_numerator(1+(x << r), n) >> n
        delta = shortcut_word(x+(x*x << (level+2)), K).bit_count() - 2*lower_odd
        labels[carry] += 1
        before[delta] += 1
        if carry == target:
            after[delta] += 1
    return {'v': level, 'candidates': sum(before.values()),
            'retained': sum(after.values()), 'actual_carry': target,
            'maximum_before': max(before), 'maximum_after': max(after),
            'carry_counts': dict(sorted(labels.items())),
            'delta_distribution_before': dict(sorted(before.items())),
            'delta_distribution_after': dict(sorted(after.items()))}


def full_packed_square_carry(source, columns):
    """Multiply a polynomial in a carry-free radix, normalize every column.

    Unlike the production carry routine, this oracle neither reverses bits
    nor bounds an omitted prefix. The radix exceeds every convolution
    coefficient, so an ordinary integer product stores all coefficients.
    """
    if columns == 0:
        return 0
    stride = max(1, (columns.bit_length()+7)//8)
    raw = (source % (1 << columns)).to_bytes((columns+7)//8, 'little')
    slots = bytearray(stride*columns)
    for i in range(columns):
        slots[stride*i] = (raw[i//8] >> (i % 8)) & 1
    polynomial = int.from_bytes(slots, 'little')
    coefficients = (polynomial*polynomial).to_bytes(2*len(slots), 'little')
    carry = 0
    for offset in range(0, len(slots), stride):
        coefficient = int.from_bytes(coefficients[offset:offset+stride], 'little')
        carry = (carry+coefficient)//2
    return carry


def elementary_trace(source, length):
    packed = bytearray((length+7)//8)
    for step in range(length):
        if source & 1:
            packed[step//8] += 1 << (step % 8)
            source = (3*source+1) >> 1
        else:
            source >>= 1
    return bytes(packed)


class CarryConstraintTests(unittest.TestCase):
    def test_fast_carry_against_nested_schoolbook(self):
        for n in range(10):
            for source in range(1 << n):
                result = probe.fast_carry(source, n)
                expected = schoolbook_carry(source, n)
                self.assertEqual(result['carry'], expected, (source, n))
                self.assertEqual(full_packed_square_carry(source, n), expected)
                self.assertEqual(result['lower'], expected)
                self.assertEqual(result['upper'], expected)
        for n in range(10, 65):
            sources = [0, (1 << n)-1, 1 << (n-1), (1 << n)+3,
                       sum(1 << i for i in range(0, n, 2)),
                       sum(1 << i for i in range(1, n, 3))]
            for source in sources:
                result = probe.fast_carry(source, n)
                self.assertEqual(result['carry'], schoolbook_carry(source, n))
                self.assertEqual(result['lower'], result['upper'])
                self.assertLessEqual(result['columns_used'], n)
                self.assertLess(result['carry'], n)

    def test_triangle_against_schoolbook(self):
        for n in range(9):
            for source in range(1 << n):
                self.assertEqual(triangular_numerator(source, n) >> n,
                                 schoolbook_carry(source, n))

    def test_source_carry_truncation_and_shift(self):
        for v in range(4):
            r = v+3
            for K in range(9):
                for x in range(1 << K):
                    expected = schoolbook_carry(1+(x << r), r+K)
                    self.assertEqual(probe.source_carry(v, x, K)['carry'], expected)
                    high_x = x+(1 << (K+4))
                    self.assertEqual(probe.source_carry(v, high_x, K)['carry'], expected)

    def test_inverse_quadratic_against_brute_permutation(self):
        for v in range(6):
            for bits in range(10):
                modulus = 1 << bits
                image = [(x+(x*x << (v+2))) % modulus
                         for x in range(modulus)]
                self.assertEqual(len(set(image)), modulus)
                for x, target in enumerate(image):
                    self.assertEqual(probe.inverse_quadratic(v, target, bits), x,
                                     (v, bits, target))

    def test_sparse_suffix_residue_against_direct_parity_permutation(self):
        # Direct iteration enumerates the complete inverse lookup table.
        # No affine or inverse-word formula is used by this oracle.
        inverse = {}
        for bits in range(11):
            lookup = {shortcut_word(x, bits): x for x in range(1 << bits)}
            self.assertEqual(len(lookup), 1 << bits)
            inverse[bits] = lookup
        for H in range(5):
            for F in range(7):
                K = H+F
                for prefix in range(1 << H):
                    base = prefix | (((1 << F)-1) << H)
                    for count in range(min(3, F)+1):
                        for offsets in combinations(range(F), count):
                            zeros = [H+offset for offset in offsets]
                            word = base
                            for position in zeros:
                                word &= ~(1 << position)
                            actual = probe.sparse_suffix_residue(prefix, H, K, zeros)
                            self.assertEqual(actual, inverse[K][word],
                                             (prefix, H, K, zeros))

    def test_linear_carry_against_full_triangular_convolution(self):
        for v in range(3):
            r = v+3
            for H in range(1, 5):
                for K in range(H, 2*H+1):
                    for low in range(1 << H):
                        for suffix in range(1 << (K-H)):
                            x = low | (suffix << H)
                            expected = triangular_numerator(1+(x << r), r+K)
                            result = probe.linear_carry(v, low, H, K, x)
                            self.assertEqual(result['constant_numerator'] +
                                             result['weighted_suffix_numerator'],
                                             expected, (v, H, K, x))
                            self.assertEqual(result['denominator'], 1 << (r+K))
                            self.assertEqual(result['carry'], expected >> (r+K))
                            self.assertEqual(result['suffix_ones'], suffix.bit_count())
                            # Fixed source bits from K upward cannot enter
                            # the triangular carry numerator at column r+K.
                            high_result = probe.linear_carry(v, low, H, K,
                                                            x+(1 << (K+3)))
                            self.assertEqual(high_result, result)

    def test_masks_match_frozen_prospective_input_without_search(self):
        data = json.loads((HERE/'presearch.json').read_text())
        actual = [list(zeros) for zeros in probe.masks(data['H'], data['K'])]
        self.assertEqual(actual, data['candidate_zero_positions'])
        self.assertEqual(len(actual), data['candidate_count'])
        for H, K in ((0, 0), (0, 1), (2, 3), (3, 8)):
            values = probe.masks(H, K)
            self.assertEqual(len(values), len(set(values)))
            for zeros in values:
                self.assertEqual(zeros, tuple(sorted(set(zeros))))
                self.assertTrue(all(H <= position < K for position in zeros))

    def test_all_small_fibers_against_independent_oracle_and_frozen_archive(self):
        archived = json.loads((HERE.parent/'post_v6_binary_carries_2026-09-26'/
                               'binary_carry_results.json').read_text())
        old = {row['v']: row for row in archived['future_carry_selection']}
        for v in range(5):
            expected = independent_fiber(v)
            result = probe.small_fiber(v)
            for key, value in expected.items():
                actual = result[key]
                if isinstance(value, dict):
                    actual = {int(k): count for k, count in actual.items()}
                    previous = {int(k): count for k, count in old[v][key].items()}
                else:
                    previous = old[v][key]
                self.assertEqual(actual, value, (v, key))
                self.assertEqual(previous, value, (v, key))

    def test_archived_level16_witness_with_independent_words_and_carry(self):
        data = json.loads((HERE/'carry_constraint_results.json').read_text())
        pre = json.loads((HERE/'presearch.json').read_text())
        search, H, K, v = data['level16_search'], pre['H'], pre['K'], pre['v']
        witness = search['witness']
        self.assertIsNotNone(witness)
        self.assertEqual(search['status'], 'counterexample')
        self.assertEqual(search['visited_count'], witness['candidate_index']+1)
        self.assertEqual(witness['zero_positions'],
                         pre['candidate_zero_positions'][witness['candidate_index']])
        self.assertTrue(all(row['carry'] != search['actual_carry'] or
                            row['delta'] <= pre['g'] for row in search['visited'][:-1]))
        self.assertEqual(hashlib.sha256((HERE/'PROTOCOL_IT.md').read_bytes()).hexdigest(),
                         pre['protocol_sha256'])
        self.assertEqual(hashlib.sha256((HERE/'presearch.json').read_bytes()).hexdigest(),
                         data['presearch_sha256'])
        x, y = int(witness['X_hex'], 16), int(witness['Y_hex'], 16)
        q = exact_source(v)
        self.assertEqual(y, x+(x*x << (v+2)))
        self.assertGreater(x, 0)
        self.assertEqual(x % 2, 1)
        self.assertNotEqual(x, q)
        self.assertEqual(x % (1 << H), q % (1 << H))
        self.assertEqual(x >> K, q >> K)
        self.assertEqual(x.bit_length(), q.bit_length())
        lower, upper = elementary_trace(x, H), elementary_trace(y, K)
        self.assertEqual(lower.hex(), witness['lower_word_lsb_first_hex'])
        self.assertEqual(upper.hex(), witness['upper_word_lsb_first_hex'])
        self.assertEqual(hashlib.sha256(lower).hexdigest(), witness['lower_word_sha256'])
        self.assertEqual(hashlib.sha256(upper).hexdigest(), witness['upper_word_sha256'])
        baseline = json.loads((HERE.parent/'post_v6_margin_2026-09-25'/
                               'margin_results.json').read_text())
        historical = {row['v']: row for row in baseline['levels']}
        self.assertEqual(hashlib.sha256(lower).hexdigest(),
                         historical[v]['parity_trace_sha256'])
        low_count = sum(byte.bit_count() for byte in lower)
        upper_count = sum(byte.bit_count() for byte in upper)
        self.assertEqual(low_count, witness['lower_odd'])
        self.assertEqual(upper_count, witness['upper_odd'])
        self.assertEqual(upper_count-2*low_count, witness['delta'])
        self.assertGreater(witness['delta'], pre['g'])
        self.assertEqual((1 << v)-upper_count, witness['upper_margin'])
        self.assertEqual(witness['upper_margin'], 2*pre['anchor_margin']-witness['delta'])
        self.assertEqual(search['actual_delta'],
                         historical[v+1]['odd_steps']-2*historical[v]['odd_steps'])
        self.assertEqual(search['actual_upper_margin'], historical[v+1]['margin'])
        n, target = pre['N'], search['actual_carry']
        self.assertEqual(full_packed_square_carry(1+(x << (v+3)), n), target)
        self.assertEqual(full_packed_square_carry(1+(q << (v+3)), n), target)
        numerator = int(witness['linear_carry']['constant_numerator'], 16) + \
            int(witness['linear_carry']['weighted_suffix_numerator'], 16)
        self.assertTrue(target*(1 << n) <= numerator < (target+1)*(1 << n))


if __name__ == '__main__':
    unittest.main(verbosity=2)
