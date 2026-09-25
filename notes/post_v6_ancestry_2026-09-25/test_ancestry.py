"""Independent small arithmetic and integer-orbit checks of ancestry claims."""
import json
from pathlib import Path
import unittest

import ancestry_probe as probe


def closed_descendant(u, anchor, depth):
    a, d = 2 ** (u + 3), 2 ** depth
    numerator = (1 + a * anchor) ** d - 1
    assert numerator % (a * d) == 0
    return numerator // (a * d)


def elementary_word(start, steps):
    word = 0
    for i in range(steps):
        bit = start % 2
        word += bit << i
        start = (3 * start + 1) // 2 if bit else start // 2
    return word, start


def valuation_three(nonzero):
    value, exponent = abs(nonzero), 0
    if value == 0:
        raise ValueError('valuation of zero is not finite')
    while value % 3 == 0:
        value //= 3
        exponent += 1
    return exponent


class AncestryTests(unittest.TestCase):
    def test_power_two_roots_by_exhaustion_and_perfect_power_boundaries(self):
        for depth in range(5):
            exponent = 1 << depth
            for value in range(257):
                expected = max(k for k in range(value + 1) if k ** exponent <= value)
                self.assertEqual(probe.power_two_root(value, depth), expected)
        for depth in range(1, 5):
            for root in (2, 7, 31, 257):
                power = root ** (1 << depth)
                self.assertEqual(probe.power_two_root(power - 1, depth), root - 1)
                self.assertEqual(probe.power_two_root(power, depth), root)
                self.assertEqual(probe.power_two_root(power + 1, depth), root)

    def test_chains_by_closed_power_and_discrete_binade_inheritance(self):
        for u in range(4):
            for anchor in range(1, 65):
                values = probe.chain(u, anchor, 4)
                expected = [closed_descendant(u, anchor, depth) for depth in range(5)]
                self.assertEqual(values, expected)
                for depth in range(4):
                    w = u + depth
                    lower, upper = values[depth], values[depth + 1]
                    B, B_next = lower.bit_length() - 1, upper.bit_length() - 1
                    self.assertIn(B_next, (w + 2 + 2 * B, w + 3 + 2 * B))
                    self.assertEqual(B, (B_next - w - 2) // 2)
                    self.assertEqual(probe.recover_ancestor(w + 1, upper, depth + 1),
                                     anchor)
        # The last INTEGER below a binade boundary is essential to the lemma.
        for w in range(6):
            for B in range(8):
                Z, c = 1 << B, 1 << (w + 2)
                maximum = c * (2 * Z - 1) ** 2 + (2 * Z - 1)
                self.assertLess(maximum, 4 * c * Z * Z)

    def test_ancestor_recovery_by_bruteforce_and_root_congruence(self):
        for v in range(1, 5):
            for depth in range(v + 1):
                u = v - depth
                images = {closed_descendant(u, x, depth): x for x in range(1, 129)}
                for value in range(1, 129):
                    self.assertEqual(probe.recover_ancestor(v, value, depth),
                                     images.get(value))
        # A perfect square is not sufficient: the root must equal 1 mod a_u.
        self.assertEqual(1 + 16 * 3, 7 ** 2)
        self.assertIsNone(probe.recover_ancestor(1, 3, 1))
        self.assertIsNone(probe.recover_ancestor(1, 4, 1))

    def test_ancestor_intervals_against_complete_small_search(self):
        for u in range(3):
            for depth in range(4):
                v = u + depth
                Q_u, Q_v = probe.tower(u), probe.tower(v)
                Z = 1 << (Q_v.bit_length() - 1)
                values = [x for x in range(1, 2 * Q_u + 1)
                          if Z <= closed_descendant(u, x, depth) < 2 * Z]
                L, U = probe.ancestor_interval(u, v)
                self.assertEqual(list(range(L, U + 1)), values)
                self.assertLessEqual(L, Q_u)
                self.assertLessEqual(Q_u, U)
                self.assertGreaterEqual(closed_descendant(u, 2 * Q_u, depth), 2 * Z)
                self.assertLessEqual(len(values), Q_u // (1 << depth) + 1)
                for anchor in values:
                    for back in range(depth + 1):
                        self.assertEqual(closed_descendant(u, anchor, back).bit_length(),
                                         probe.tower(u + back).bit_length())
                for custom_Z in (1, 2, 4, 8, 16, 32, 64):
                    candidates = [x for x in range(1, 2 * custom_Z)
                                  if custom_Z <= closed_descendant(u, x, depth) < 2 * custom_Z]
                    L, U = probe.ancestor_interval(u, v, custom_Z)
                    self.assertEqual(list(range(L, U + 1)), candidates)

    def test_binary_inverses_against_complete_small_permutations(self):
        for bits in range(8):
            modulus = 1 << bits
            for v in (0, 2, 5):
                inverse = {(x + 2 ** (v + 2) * x * x) % modulus: x
                           for x in range(modulus)}
                self.assertEqual(len(inverse), modulus)
                for target, expected in inverse.items():
                    self.assertEqual(probe.inverse_quadratic(v, target, bits), expected)
            for u in range(3):
                for depth in range(4):
                    inverse = {closed_descendant(u, x, depth) % modulus: x
                               for x in range(modulus)}
                    self.assertEqual(len(inverse), modulus)
                    for target, expected in inverse.items():
                        self.assertEqual(probe.inverse_chain(u, u + depth, target, bits),
                                         expected)

    def test_class_count_and_isolation_bits_by_direct_enumeration(self):
        for L in range(1, 12):
            for U in range(L, L + 12):
                for bits in range(6):
                    modulus = 1 << bits
                    for residue in range(modulus):
                        expected = sum(x % modulus == residue for x in range(L, U + 1))
                        self.assertEqual(probe.class_count(L, U, residue, bits), expected)
                for Q in range(L, U + 1):
                    expected_bits = next(bits for bits in range(8)
                                         if sum((x - Q) % (1 << bits) == 0
                                                for x in range(L, U + 1)) == 1)
                    self.assertEqual(probe.isolation_bits(Q, L, U), expected_bits)

    def test_exact_number_of_terminal_words_and_odd_subset(self):
        for u in range(3):
            for depth in range(4):
                v = u + depth
                L, U = probe.ancestor_interval(u, v)
                anchors = list(range(L, U + 1))
                odd_anchors = [x for x in anchors if x % 2]
                for bits in range(9):
                    words = {elementary_word(closed_descendant(u, x, depth), bits)[0]
                             for x in anchors}
                    self.assertEqual(len(words), min(len(anchors), 1 << bits))
                    if bits:
                        odd_words = {elementary_word(closed_descendant(u, x, depth), bits)[0]
                                     for x in odd_anchors}
                        self.assertEqual(len(odd_words),
                                         min(len(odd_anchors), 1 << (bits - 1)))
                        self.assertTrue(all(word & 1 for word in odd_words))

    def test_word_candidates_against_elementary_word_enumeration(self):
        for v, depth in ((2, 0), (2, 1), (3, 1), (3, 2), (4, 2)):
            u = v - depth
            L, U = probe.ancestor_interval(u, v)
            for bits in range(7):
                by_word = {}
                for x in range(L, U + 1):
                    word = elementary_word(closed_descendant(u, x, depth), bits)[0]
                    by_word.setdefault(word, []).append(x)
                for word in range(1 << bits):
                    row = probe.word_candidate(v, word, bits, depth)
                    expected = by_word.get(word, [])
                    self.assertEqual(int(row['L_hex'], 16), L)
                    self.assertEqual(int(row['U_hex'], 16), U)
                    self.assertEqual(int(row['count_hex'], 16), len(expected))
                    self.assertEqual(None if row['first_hex'] is None
                                     else int(row['first_hex'], 16),
                                     expected[0] if expected else None)
                    residue = int(row['anchor_residue_hex'], 16)
                    self.assertLess(residue, 1 << bits)
                    self.assertEqual(elementary_word(closed_descendant(u, residue, depth),
                                                     bits)[0], word)

    def test_two_ancestors_isolate_the_actual_word_at_existing_small_levels(self):
        for v in range(5, 13):
            H, Q_v, Q_u = probe.horizon(v), probe.tower(v), probe.tower(v - 2)
            word, _ = elementary_word(Q_v, H)
            row = probe.word_candidate(v, word, H, 2)
            L, U = probe.ancestor_interval(v - 2, v)
            self.assertEqual(int(row['count_hex'], 16), 1)
            self.assertEqual(int(row['first_hex'], 16), Q_u)
            self.assertEqual(probe.recover_ancestor(v, Q_v, 2), Q_u)
            self.assertLess(Q_u, 1 << H)
            self.assertLessEqual(U - L + 1, 1 << H)
            h_iso = probe.isolation_bits(Q_u, L, U)
            self.assertLessEqual(h_iso, H)
            self.assertEqual(probe.class_count(L, U, Q_u % (1 << h_iso), h_iso), 1)
            if h_iso:
                self.assertGreater(probe.class_count(L, U, Q_u % (1 << (h_iso - 1)),
                                                    h_iso - 1), 1)

    def test_archived_actual_prefix_adversaries_cannot_have_two_ancestors(self):
        previous = Path(__file__).resolve().parent.parent / 'post_v6_mixed_2026-09-25'
        records = json.loads((previous / 'mixed_results.json').read_bytes())['mixed_adversaries']
        checked = 0
        for row in records:
            if row['kind'] != 'actual_prefix':
                continue
            v, X = row['v'], int(row['X_hex'], 16)
            Q, H = probe.tower(v), probe.horizon(v)
            self.assertNotEqual(X, Q)
            self.assertEqual(X.bit_length(), Q.bit_length())
            self.assertEqual(elementary_word(X, H)[0], elementary_word(Q, H)[0])
            self.assertIsNone(probe.recover_ancestor(v, X, 2))
            checked += 1
        self.assertEqual(checked, 6)

    def test_pure_parameters_against_small_exact_powers_and_permutations(self):
        for v in range(4):
            e, a = 1 << (v + 1), 1 << (v + 3)
            for bits in range(9):
                modulus = 1 << bits
                observed = set()
                for parameter in range(modulus):
                    exact = (3 ** (e * parameter) - 1) // a
                    residue = exact % modulus
                    observed.add(residue)
                    self.assertEqual(probe.pure_residue(v, parameter, bits), residue)
                    self.assertEqual(probe.pure_parameter(v, residue, bits), parameter)
                    if bits:
                        self.assertEqual(residue % 2, parameter % 2)
                self.assertEqual(observed, set(range(modulus)))
        recorded = json.loads((Path(__file__).resolve().parent / 'ancestry_results.json').read_bytes())
        self.assertEqual(len(recorded['pure_power_parameter_examples']), 2)
        for row in recorded['pure_power_parameter_examples']:
            v, bits, k = row['v'], row['K'], int(row['k_hex'], 16)
            self.assertGreater(k, 1)
            self.assertEqual(k % 2, 1)
            # The full pure-power integer is enormous; builtin modular pow
            # independently checks the certificate without constructing it.
            lower = (pow(3, (1 << (v + 1)) * k, 1 << (v + 3 + bits)) - 1) >> (v + 3)
            upper = (pow(3, (1 << (v + 2)) * k, 1 << (v + 4 + bits)) - 1) >> (v + 4)
            self.assertEqual(lower, int(row['residue_hex'], 16))
            self.assertEqual(upper, int(row['upper_residue_hex'], 16))
            self.assertEqual(upper, (lower + 2 ** (v + 2) * lower * lower) % (1 << bits))
            self.assertEqual(row['lower_margin'], 2 ** (v - 1)
                             - elementary_word(lower, probe.horizon(v))[0].bit_count())
            self.assertEqual(row['upper_margin'], 2 ** v
                             - elementary_word(upper, bits)[0].bit_count())
            self.assertGreater(row['lower_margin'], 0)
            self.assertLess(row['upper_margin'], 0)
            self.assertIs(row['same_binade_as_Q_v'], False)

    def test_all_six_coherent_counterexamples_by_independent_orbits(self):
        result = json.loads((Path(__file__).resolve().parent / 'ancestry_results.json').read_bytes())
        examples = result['coherent_counterexamples']
        self.assertEqual(len(examples), 6)
        for key in ('uniform_delta_bound_proved', 'uniform_family_descent_proved',
                    'mathematical_novelty_established'):
            self.assertIs(result[key], False)
        self.assertEqual(result['new_tower_levels'], [])
        self.assertEqual(result['new_lean_declarations'], 0)
        for row in examples:
            v, u, depth = row['v'], row['anchor_level'], row['depth_before_lower_level']
            levels = row['levels']
            self.assertEqual(u + depth, v)
            self.assertEqual(len(levels), depth + 2)
            values = [int(item['X_hex'], 16) for item in levels]
            anchor = values[0]
            self.assertNotEqual(anchor, probe.tower(u))
            self.assertEqual(anchor, probe.tower(u)
                             + int(row['anchor_increment_modulus_hex'], 16)
                             * int(row['t_hex'], 16))
            for offset, (item, value) in enumerate(zip(levels, values)):
                w = u + offset
                Q = probe.tower(w)
                self.assertEqual(item['v'], w)
                self.assertEqual(value, closed_descendant(u, anchor, offset))
                self.assertGreater(value, 0)
                self.assertEqual(value % 2, 1)
                self.assertEqual(value.bit_length(), Q.bit_length())
                self.assertEqual(item['difference_valuation'], valuation_three(value - Q))
                self.assertEqual(item['signature_valuation'],
                                 valuation_three(1 + 2 ** (w + 3) * value))
                self.assertGreaterEqual(item['difference_valuation'], 1 << (w - 1))
                self.assertGreaterEqual(item['signature_valuation'], 1 << (w - 1))
            X, Y = values[-2:]
            lower = elementary_word(X, row['H'])[0]
            upper = elementary_word(Y, row['K'])[0]
            actual_lower = elementary_word(probe.tower(v), row['H'])[0]
            actual_upper = elementary_word(probe.tower(v + 1), row['K'])[0]
            self.assertEqual(lower, int(row['lower_word_hex'], 16))
            self.assertEqual(upper, int(row['upper_word_hex'], 16))
            self.assertEqual(row['lower_margin'], 2 ** (v - 1) - lower.bit_count())
            self.assertEqual(row['upper_margin'], 2 ** v - upper.bit_count())
            self.assertEqual(row['actual_lower_margin'], 2 ** (v - 1) - actual_lower.bit_count())
            self.assertEqual(row['actual_upper_margin'], 2 ** v - actual_upper.bit_count())
            self.assertGreater(row['lower_margin'], 0)
            self.assertLess(row['upper_margin'], 0)
            self.assertEqual(row['same_complete_lower_word'], lower == actual_lower)
            if depth == 1:
                self.assertEqual(lower, actual_lower)
                forced = row['forced_upper_odd_bits_after_H']
                self.assertEqual((upper >> row['H']) & ((1 << forced) - 1),
                                 (1 << forced) - 1)
            else:
                self.assertNotEqual(lower, actual_lower)

    def test_complete_finite_ancestry_filter_by_elementary_iteration(self):
        result = json.loads((Path(__file__).resolve().parent / 'ancestry_results.json').read_bytes())
        sample = result['exhaustive_ancestry_filter']
        v, u, depth = sample['v'], sample['anchor_level'], sample['depth_before_lower_level']
        L, U = sample['L'], sample['U']
        self.assertEqual((v, u, depth, sample['height_fixed_at_level']), (10, 3, 7, 11))
        self.assertEqual((L, U), (672594, 674416))
        Q_upper = (3 ** (1 << (v + 2)) - 1) // (1 << (v + 4))
        Z = 1 << (Q_upper.bit_length() - 1)
        self.assertLess(closed_descendant(u, L - 1, depth + 1), Z)
        self.assertGreaterEqual(closed_descendant(u, L, depth + 1), Z)
        self.assertLess(closed_descendant(u, U, depth + 1), 2 * Z)
        self.assertGreaterEqual(closed_descendant(u, U + 1, depth + 1), 2 * Z)
        anchors = [x for x in range(L, U + 1) if x % 2]
        self.assertEqual(len(anchors), 911)
        self.assertEqual([row['anchor'] for row in sample['rows']], anchors)
        anchor_Q = (3 ** (1 << (u + 1)) - 1) // (1 << (u + 3))
        modulus = 3 ** (1 << (u - 1))
        self.assertEqual((anchor_Q, modulus), (sample['anchor_Q'], sample['ternary_modulus']))
        lower_nonnegative = upper_negative = both = 0
        retained = []
        for anchor, row in zip(anchors, sample['rows']):
            X = closed_descendant(u, anchor, depth)
            Y = closed_descendant(u, anchor, depth + 1)
            lower = (1 << (v - 1)) - elementary_word(X, probe.horizon(v))[0].bit_count()
            upper = (1 << v) - elementary_word(Y, probe.horizon(v + 1))[0].bit_count()
            keep = (anchor - anchor_Q) % modulus == 0
            self.assertEqual((row['lower_margin'], row['upper_margin'],
                              row['quarter_ternary_constraint']), (lower, upper, keep))
            lower_nonnegative += lower >= 0
            upper_negative += upper < 0
            both += lower >= 0 and upper < 0
            if keep:
                retained.append(upper)
        self.assertEqual(sample['odd_anchor_count'], len(anchors))
        self.assertEqual(sample['lower_margin_nonnegative_count'], lower_nonnegative)
        self.assertEqual(sample['upper_margin_negative_count'], upper_negative)
        self.assertEqual(sample['negative_upper_with_nonnegative_lower_count'], both)
        self.assertEqual((lower_nonnegative, upper_negative, both), (815, 36, 33))
        self.assertEqual(sample['retained_anchor_count'], len(retained))
        self.assertEqual(sample['retained_upper_margin_minimum'], min(retained))
        self.assertEqual(sample['retained_upper_negative_count'], sum(m < 0 for m in retained))
        self.assertEqual((len(retained), min(retained)), (12, 6))


if __name__ == '__main__':
    unittest.main()
