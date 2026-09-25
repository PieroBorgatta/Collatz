"""Independent exact checks of the mixed-prime constraints and their scope."""
from fractions import Fraction
import hashlib
import json
import unittest

import mixed_probe as probe


def elementary_orbit(start, steps):
    bits = []
    for _ in range(steps):
        bit = start % 2
        bits.append(bit)
        start = (3 * start + 1) // 2 if bit else start // 2
    return bits, start


def closed_constant(bits):
    positions = [i for i, bit in enumerate(bits) if bit]
    return sum(2 ** i * 3 ** (len(positions) - index - 1)
               for index, i in enumerate(positions))


def valuation_three(value):
    value = abs(value)
    if value == 0:
        raise ValueError('valuation of zero is not finite')
    count = 0
    while value % 3 == 0:
        value //= 3
        count += 1
    return count


class MixedTests(unittest.TestCase):
    def test_integer_logarithms_against_small_enumeration_and_boundaries(self):
        for value in range(1, 1500):
            binary = next(k for k in range(20) if 2 ** k >= value)
            ternary = max(k for k in range(20) if 3 ** k <= value)
            self.assertEqual(probe.ceil_log2(value), binary)
            self.assertEqual(probe.floor_log3(value), ternary)
        for exponent in (1, 7, 33, 150):
            self.assertEqual(probe.ceil_log2(2 ** exponent), exponent)
            self.assertEqual(probe.ceil_log2(2 ** exponent + 1), exponent + 1)
            self.assertEqual(probe.floor_log3(3 ** exponent - 1), exponent - 1)
            self.assertEqual(probe.floor_log3(3 ** exponent), exponent)

    def test_candidate_counts_against_every_small_binade_position(self):
        for bits in range(1, 7):
            Z = 1 << bits
            for Q in range(Z, 2 * Z):
                for h in range(bits + 2):
                    for s in range(5):
                        candidates = [x for x in range(Z, 2 * Z)
                                      if (x - Q) % (1 << h) == 0
                                      and (x - Q) % (3 ** s) == 0]
                        self.assertEqual(probe.candidate_count(Q, Z, h, s),
                                         len(candidates))
                        modulus = 2 ** h * 3 ** s
                        isolated = modulus > Q - Z and modulus >= 2 * Z - Q
                        self.assertEqual(len(candidates) == 1, isolated)
                        if modulus <= Z // 2:
                            self.assertGreaterEqual(len(candidates), 2)
                        if modulus >= Z:
                            self.assertEqual(len(candidates), 1)

    def test_isolation_threshold_against_direct_candidate_enumeration(self):
        for bits in range(1, 7):
            Z = 1 << bits
            for Q in range(Z, 2 * Z):
                for h in range(bits + 2):
                    expected = next(s for s in range(12)
                                    if sum((x - Q) % (2 ** h * 3 ** s) == 0
                                           for x in range(Z, 2 * Z)) == 1)
                    self.assertEqual(probe.isolation_threshold(Q, Z, h), expected)
        # The left boundary is included; the right boundary is excluded.
        self.assertEqual(probe.candidate_count(12, 8, 2, 0), 2)
        self.assertEqual(probe.candidate_count(10, 8, 1, 1), 1)

    def test_crt_representative_against_complete_small_search(self):
        for Q in (8, 9, 11, 15, 32, 47, 63, 128, 171, 255):
            Z = 1 << (Q.bit_length() - 1)
            for K in range(6):
                for s in range(5):
                    modulus = 2 ** K * 3 ** s
                    if modulus > Z:
                        continue
                    for residue in range(1 << K):
                        X, P, R = probe.crt_representative(Q, K, residue, s)
                        expected_R = next(k for k in range(20) if 2 ** k >= modulus)
                        A = (Q // 2 ** expected_R) * 2 ** expected_R
                        candidates = [x for x in range(A, A + modulus)
                                      if x % (1 << K) == residue
                                      and (x - Q) % (3 ** s) == 0]
                        self.assertEqual(len(candidates), 1)
                        self.assertEqual((X, P, R),
                                         (candidates[0], modulus, expected_R))
                        self.assertLessEqual(Z, X)
                        self.assertLess(X, 2 * Z)
                        self.assertEqual(X >> R, Q >> R)
                        self.assertLess(abs(X - Q), 1 << R)
                        self.assertEqual(elementary_orbit(X, K)[0],
                                         elementary_orbit(residue, K)[0])

    def test_crt_representative_rejects_invalid_inputs_and_oversized_modulus(self):
        invalid = (
            (0, 1, 0, 0), (-1, 1, 0, 0), (10, -1, 0, 0),
            (10, 2, -1, 0), (10, 2, 4, 0), (10, 2, 1, -1),
            (10, 3, 1, 1),
        )
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                probe.crt_representative(*args)

    def test_quadratic_signature_identity_and_ternary_doubling(self):
        for v in (5, 6, 7):
            a = 2 ** (v + 3)
            e = 2 ** (v + 1)
            Q = (3 ** e - 1) // a
            self.assertEqual(probe.tower(v), Q)
            self.assertEqual(probe.quadratic(v, Q), probe.tower(v + 1))
            for X in (1, 2, 17, Q, Q + 1, Q + 3 ** (e // 4)):
                Y = probe.quadratic(v, X)
                self.assertEqual(Y, X + 2 ** (v + 2) * X * X)
                self.assertEqual(1 + 2 * a * Y, (1 + a * X) ** 2)
                self.assertEqual(valuation_three(1 + 2 * a * Y),
                                 2 * valuation_three(1 + a * X))

    def test_precision_doubling_requires_s_below_e(self):
        for v in (5, 6):
            e, a = 2 ** (v + 1), 2 ** (v + 3)
            Q, Q_next = probe.tower(v), probe.tower(v + 1)
            for s in (1, e // 4, e - 1):
                for t in (1, 2, 4):
                    X = Q + 3 ** s * t
                    difference = probe.quadratic(v, X) - Q_next
                    expected = 3 ** (2 * s) * t * (3 ** (e - s) + (a // 2) * t)
                    self.assertEqual(difference, expected)
                    self.assertEqual(valuation_three(difference), 2 * s)
            # Above e, the derivative term controls the valuation: s+e, not 2s.
            s = e + 2
            X = Q + 3 ** s
            actual = valuation_three(probe.quadratic(v, X) - Q_next)
            self.assertEqual(actual, s + e)
            self.assertNotEqual(actual, 2 * s)
            # At the boundary s=e there can be additional cancellation.
            t = next(t for t in (1, 2) if (1 + (a // 2) * t) % 3 == 0)
            X = Q + 3 ** e * t
            self.assertGreater(valuation_three(probe.quadratic(v, X) - Q_next), 2 * e)

    def test_full_and_nearly_full_ternary_precision_already_isolate(self):
        for v in (5, 6, 7, 8):
            Q = probe.tower(v)
            Z = 1 << (Q.bit_length() - 1)
            e, a = 1 << (v + 1), 1 << (v + 3)
            for h in (0, 3, probe.horizon(v)):
                self.assertEqual(probe.candidate_count(Q, Z, h, e), 1)
                self.assertEqual(probe.candidate_count(Q, Z, h, e - 1), 1)
            self.assertEqual(pow(3, e, a), 1)
            for t in (-1, 0, 1, 2):
                X = Q + t * 3 ** e
                multiplier = 1 + a * t
                self.assertEqual(a * X + 1, multiplier * 3 ** e)
                self.assertEqual(multiplier % a, 1)

    def test_uniform_quarter_precision_crt_bound_without_new_orbits(self):
        for v in range(6, 41):
            M = 1 << v
            K = probe.horizon(v + 1)
            self.assertLessEqual(K, 2 * M)
            self.assertGreaterEqual(M, 6 * v + 18)
            # These are exponent comparisons, avoiding enormous new integers.
            self.assertLessEqual(6 * K + 5 * M, 17 * M)
            self.assertLessEqual(17 * M, 18 * M - 6 * v - 18)
        self.assertLess(3 ** 3, 2 ** 5)

    def test_transport_against_elementary_orbits_including_false_congruences(self):
        true_initial = false_initial = 0
        for v in (5, 6, 7):
            Q, a = probe.tower(v), 1 << (v + 3)
            for X in (Q, Q + 1, Q + 9, 1, 2):
                for n in (0, 1, 5, 17):
                    bits, Y = elementary_orbit(X, n)
                    j, C = sum(bits), closed_constant(bits)
                    self.assertEqual((1 << n) * Y, 3 ** j * X + C)
                    for s in (0, 1, 3):
                        row = probe.transport_data(v, X, n, s)
                        modulus = 3 ** (s + j)
                        residue = (pow(2 ** n, -1, modulus)
                                   * (C - pow(a, -1, modulus) * 3 ** j)) % modulus
                        initial = (a * X + 1) % (3 ** s) == 0
                        terminal = Y % modulus == residue
                        self.assertEqual(initial, terminal)
                        self.assertEqual(row['j'], j)
                        self.assertEqual(int(row['C_hex'], 16), C)
                        self.assertEqual(int(row['Y_hex'], 16), Y)
                        self.assertEqual(int(row['word_hex'], 16),
                                         sum(bit << i for i, bit in enumerate(bits)))
                        self.assertEqual(int(row['modulus_hex'], 16), modulus)
                        self.assertEqual(int(row['transformed_residue_hex'], 16), residue)
                        self.assertEqual(a * 2 ** n * Y - a * C + 3 ** j,
                                         3 ** j * (a * X + 1))
                        Z = 1 << (X.bit_length() - 1)
                        width = Fraction(3 ** j * Z, 2 ** n)
                        self.assertEqual(Fraction(modulus, 1) / width,
                                         Fraction(2 ** n * 3 ** s, Z))
                        for key in ('transport_identity', 'ternary_congruence_equivalent',
                                    'precision_ratio_identity'):
                            self.assertIs(row[key], True)
                        true_initial += initial
                        false_initial += not initial
        self.assertGreater(true_initial, 0)
        self.assertGreater(false_initial, 0)

    def test_complete_endpoint_bijection_for_all_small_words_and_intervals(self):
        a = 2 ** (5 + 3)
        for n in range(5):
            two = 1 << n
            for word in range(two):
                bits = [(word >> i) & 1 for i in range(n)]
                j, C = sum(bits), closed_constant(bits)
                multiplier = 3 ** j
                for Z in (8, 16, 32):
                    lower = (multiplier * Z + C + two - 1) // two
                    upper = (2 * multiplier * Z + C + two - 1) // two
                    for s in range(3):
                        actual_endpoints = []
                        for X in range(Z, 2 * Z):
                            observed, endpoint = elementary_orbit(X, n)
                            if observed == bits and (a * X + 1) % (3 ** s) == 0:
                                actual_endpoints.append(endpoint)
                        modulus = 3 ** (s + j)
                        residue = (pow(two, -1, modulus)
                                   * (C - pow(a, -1, modulus) * multiplier)) % modulus
                        congruent_endpoints = [Y for Y in range(lower, upper)
                                               if Y % modulus == residue]
                        with self.subTest(n=n, word=word, Z=Z, s=s):
                            self.assertEqual(actual_endpoints, congruent_endpoints)

    def test_ternary_valuation_and_scalar_input_rejections(self):
        for unit in (-7, -2, -1, 1, 2, 7):
            for exponent in (0, 1, 2, 11, 150):
                self.assertEqual(probe.ternary_valuation(unit * 3 ** exponent), exponent)
        for function in (probe.ceil_log2, probe.floor_log3):
            for invalid in (0, -1):
                with self.assertRaises(ValueError):
                    function(invalid)
        with self.assertRaises(ValueError):
            probe.ternary_valuation(0)
        with self.assertRaises(ValueError):
            probe.tower(-1)
        for args in ((0, 1, 0, 0), (7, 8, 0, 0), (16, 8, 0, 0),
                     (10, 8, -1, 0), (10, 8, 0, -1)):
            with self.assertRaises(ValueError):
                probe.candidate_count(*args)
        for args in ((0, 1, 0), (7, 8, 0), (16, 8, 0), (10, 8, -1)):
            with self.assertRaises(ValueError):
                probe.isolation_threshold(*args)
        for args in ((-1, 1, 0, 0), (5, 0, 1, 1), (5, 1, -1, 1), (5, 1, 1, -1)):
            with self.assertRaises(ValueError):
                probe.transport_data(*args)

    def test_all_twelve_archived_examples_with_independent_integer_iteration(self):
        result = json.loads((probe.HERE / 'mixed_results.json').read_bytes())
        raw_source = (probe.MARGIN / 'margin_results.json').read_bytes()
        source = json.loads(raw_source)
        originals = {(row['v'], row['kind']): row
                     for row in source['generic_quadratic_adversaries']}
        self.assertEqual(len(result['mixed_adversaries']), 12)
        self.assertEqual(set(result['source_sha256'].values()),
                         {hashlib.sha256(raw_source).hexdigest()})
        for key in ('uniform_delta_bound_proved', 'uniform_family_descent_proved',
                    'mathematical_novelty_established'):
            self.assertIs(result[key], False)
        self.assertEqual(result['new_tower_levels'], [])
        self.assertEqual(result['new_lean_declarations'], 0)
        seen = set()
        for row in result['mixed_adversaries']:
            v, s, H, K, R = (row[key] for key in ('v', 's', 'H', 'K', 'R'))
            self.assertIn(v, (6, 8, 10, 12))
            seen.add((v, row['kind'], row['precision_choice']))
            old = originals[(v, row['kind'])]
            X, Y = int(row['X_hex'], 16), int(row['Y_hex'], 16)
            Q, Q_next = probe.tower(v), probe.tower(v + 1)
            a, e = 2 ** (v + 3), 2 ** (v + 1)
            lower, endpoint = elementary_orbit(X, H)
            upper, _ = elementary_orbit(Y, K)
            self.assertEqual(lower, elementary_orbit(int(old['X_hex'], 16), H)[0])
            self.assertEqual(upper, elementary_orbit(int(old['Y_hex'], 16), K)[0])
            self.assertEqual(upper[H:], [1] * (K - H))
            self.assertEqual(Y, X + 2 ** (v + 2) * X * X)
            self.assertNotEqual(X, Q)
            self.assertGreater(s, 0)
            self.assertLess(s, e)
            self.assertEqual((X - Q) % (3 ** s), 0)
            self.assertEqual(X >> R, Q >> R)
            self.assertEqual(X.bit_length(), Q.bit_length())
            self.assertEqual(int(row['crt_modulus_hex'], 16), 2 ** K * 3 ** s)
            self.assertLess(abs(X - Q), 2 ** R)
            self.assertLess(abs(X - Q) * 2 ** row['relative_distance_power2_exponent'], Q)
            self.assertEqual(row['lower_odd'], sum(lower))
            self.assertEqual(row['upper_odd'], sum(upper))
            self.assertEqual(row['lower_margin'], 2 ** (v - 1) - sum(lower))
            self.assertEqual(row['upper_margin'], 2 ** v - sum(upper))
            self.assertGreater(row['lower_margin'], 0)
            self.assertLess(row['upper_margin'], 0)
            self.assertEqual(row['difference_valuation'], valuation_three(X - Q))
            self.assertEqual(row['upper_difference_valuation'], valuation_three(Y - Q_next))
            self.assertEqual(row['signature_valuation'], valuation_three(1 + a * X))
            self.assertEqual(row['upper_signature_valuation'], valuation_three(1 + 2 * a * Y))
            self.assertEqual(row['upper_signature_valuation'], 2 * row['signature_valuation'])
            self.assertEqual(row['same_lower_word_as_Q_v'],
                             lower == elementary_orbit(Q, H)[0])
            self.assertEqual(int(row['transport']['Y_hex'], 16), endpoint)
            self.assertEqual(int(row['transport']['C_hex'], 16), closed_constant(lower))
            for key in ('same_lower_and_upper_words_as_archived_adversary',
                        'same_high_bits_at_positions_ge_R', 'same_binade_as_Q_v'):
                self.assertIs(row[key], True)
        self.assertEqual(len(seen), 12)

    def test_build_example_rejects_untruncated_precision_and_inconsistent_source(self):
        source = json.loads((probe.MARGIN / 'margin_results.json').read_bytes())[
            'generic_quadratic_adversaries'][0]
        v = source['v']
        for s in (0, -1, 1 << (v + 1), (1 << (v + 1)) + 1):
            with self.assertRaises(ValueError):
                probe.build_example(source, s, 'test')
        changed = dict(source, Y_hex=hex(int(source['Y_hex'], 16) + 1))
        with self.assertRaises(AssertionError):
            probe.build_example(changed, 1, 'test')
        changed = dict(source, lower_odd=source['lower_odd'] + 1)
        with self.assertRaises(AssertionError):
            probe.build_example(changed, 1, 'test')


if __name__ == '__main__':
    unittest.main()
