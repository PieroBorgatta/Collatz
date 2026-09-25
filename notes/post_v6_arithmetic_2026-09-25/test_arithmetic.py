"""Independent small-case checks; no new tower holdout is inspected here."""
import itertools
import random
import unittest

from arithmetic_probe import (
    affine_word, analyze_word, high_complexity_word, horizon,
    modular_power, word_residue,
)


def elementary_trace(start, length):
    """Use the integer T rule, independently of the affine/block engines."""
    state, word = start, 0
    for position in range(length):
        bit = state % 2
        word |= bit << position
        state = (3 * state + 1) // 2 if bit else state // 2
    return word, state


def closed_constant(word, length):
    positions = [i for i in range(length) if word & (1 << i)]
    return sum(2 ** i * 3 ** (len(positions) - h - 1)
               for h, i in enumerate(positions))


class ArithmeticTests(unittest.TestCase):
    def test_final_integrality_is_equivalent_to_every_parity(self):
        # Includes every word and every initial residue, not just valid words.
        for length in range(9):
            modulus = 1 << length
            traces = [elementary_trace(x, length)[0]
                      for x in range(modulus)]
            self.assertEqual(len(set(traces)), modulus)
            for word in range(modulus):
                p = word.bit_count()
                constant = closed_constant(word, length)
                residue = word_residue(word, length)
                self.assertEqual(traces[residue], word)
                for start in range(modulus):
                    integral = (3 ** p * start + constant) % modulus == 0
                    self.assertEqual(integral, traces[start] == word)

    def test_affine_identity_for_positive_lifts_and_exact_constant(self):
        for length in range(9):
            modulus = 1 << length
            for word in range(modulus):
                p, multiplier, constant = affine_word(word, length)
                self.assertEqual((p, multiplier, constant),
                                 (word.bit_count(), 3 ** word.bit_count(),
                                  closed_constant(word, length)))
                for lift in (0, 1, 7):
                    start = word_residue(word, length) + lift * modulus
                    observed, endpoint = elementary_trace(start, length)
                    self.assertEqual(observed, word)
                    self.assertEqual(modulus * endpoint,
                                     multiplier * start + constant)

    def test_recursive_affine_composition_across_leaf_boundary(self):
        rng = random.Random(0xC011A72)
        for length in (17, 31, 32, 33, 63, 64, 80, 129):
            for _ in range(5):
                word = rng.getrandbits(length)
                p, multiplier, constant = affine_word(word, length)
                self.assertEqual(constant, closed_constant(word, length))
                for split in (0, 1, 16, length // 2, length):
                    k, left_multiplier, left_constant = affine_word(
                        word & ((1 << split) - 1), split)
                    j, right_multiplier, right_constant = affine_word(
                        word >> split, length - split)
                    self.assertEqual(p, k + j)
                    self.assertEqual(multiplier,
                                     left_multiplier * right_multiplier)
                    self.assertEqual(constant,
                                     right_multiplier * left_constant
                                     + (right_constant << split))

    def test_tight_constant_extrema(self):
        for length in range(11):
            extrema = {}
            for word in range(1 << length):
                count = word.bit_count()
                value = closed_constant(word, length)
                extrema.setdefault(count, []).append(value)
            for count, values in extrema.items():
                minimum = 3 ** count - 2 ** count
                maximum = 2 ** (length - count) * minimum
                self.assertEqual(min(values), minimum)
                self.assertEqual(max(values), maximum)

    def test_both_congruences_against_small_integer_tower_orbits(self):
        # Reachable and unreachable blocks, including a deliberately false
        # prefix, test that the prefix has not been silently discarded.
        reachable_count = unreachable_count = false_prefix_count = 0
        for v in (5, 6, 7):
            tower = (9 ** (1 << v) - 1) // (1 << (v + 3))
            actual_word, _ = elementary_trace(tower, 12)
            for r in range(7):
                actual_prefix = actual_word & ((1 << r) - 1)
                prefixes = [actual_prefix]
                if r:
                    prefixes.append(actual_prefix ^ 1)
                for prefix in prefixes:
                    for b in range(1, 6):
                        actual_block = (actual_word >> r) & ((1 << b) - 1)
                        for block in range(1 << b):
                            j = block.bit_count()
                            if 589 * j <= 305 * b:
                                continue
                            expected = (prefix == actual_prefix
                                        and block == actual_block)
                            row = analyze_word(v, prefix, r, block, b)
                            self.assertEqual(row['word_reachable_from_Q_v'],
                                             expected)
                            k, P, A = affine_word(prefix, r)
                            _, J, B = affine_word(block, b)
                            L = v + 3 + r + b
                            modulus = 1 << L
                            c = (1 << (v + 3)) * (J * A + (B << r)) - P * J
                            direct_full = (3 ** ((1 << (v + 1)) + k + j)
                                           + c) % modulus == 0
                            a = word_residue(block, b)
                            short_c = (1 << (v + 3)) * (A - (a << r)) - P
                            direct_short = (3 ** ((1 << (v + 1)) + k)
                                            + short_c) % modulus == 0
                            self.assertEqual(direct_full, expected)
                            self.assertEqual(direct_short, expected)
                            reachable_count += expected
                            unreachable_count += not expected
                            false_prefix_count += prefix != actual_prefix
        self.assertGreater(reachable_count, 0)
        self.assertGreater(unreachable_count, reachable_count)
        self.assertGreater(false_prefix_count, 0)

    def test_height_lower_bound_for_all_small_positive_loss_blocks(self):
        for r in range(5):
            for prefix in range(1 << r):
                k = prefix.bit_count()
                A = closed_constant(prefix, r)
                for b in range(1, 7):
                    for block in range(1 << b):
                        j = block.bit_count()
                        if 589 * j <= 305 * b:
                            continue
                        B = closed_constant(block, b)
                        C = 3 ** j * A + (B << r)
                        for v in (5, 9):
                            c = (C << (v + 3)) - 3 ** (k + j)
                            s, L = v + r + j + 1, v + 3 + r + b
                            self.assertGreaterEqual(c, 1 << s)
                            self.assertLessEqual(L, 2 * s)
                            self.assertEqual(c % 2, 1)
                            self.assertNotEqual(c % 3, 0)

    def test_short_form_nonzero_and_centering_in_the_small_horizon(self):
        for v in (5, 6, 7):
            tower = (9 ** (1 << v) - 1) // (1 << (v + 3))
            for r in range(9):
                prefix, endpoint = elementary_trace(tower, r)
                k = prefix.bit_count()
                A = closed_constant(prefix, r)
                for b in range(1, 8):
                    self.assertLessEqual(r + b, 1 << v)
                    for a in (0, 1, (1 << b) - 1):
                        L = v + 3 + r + b
                        modulus = 1 << L
                        c = ((A - (a << r)) << (v + 3)) - 3 ** k
                        numerator = 3 ** ((1 << (v + 1)) + k) + c
                        self.assertEqual(numerator,
                                         (endpoint - a) << (v + 3 + r))
                        self.assertGreater(numerator, 0)
                        centered = (c + modulus // 2) % modulus - modulus // 2
                        self.assertLessEqual(-modulus // 2, centered)
                        self.assertLess(centered, modulus // 2)
                        self.assertNotEqual(centered, 0)
                        self.assertEqual(centered % modulus, c % modulus)

    def test_high_complexity_words_and_horizon_inequalities(self):
        for t in (1, 2, 3, 5, 8, 10):
            word, length = high_complexity_word(t)
            self.assertEqual(length, 5 * t * (1 << t))
            self.assertEqual(word.bit_count(), 3 * t * (1 << t))
            self.assertEqual(word & (word >> 1) & (word >> 2), 0)
            self.assertNotEqual(word & (word >> 1), 0)
            width = 5 * t
            factors = {(word >> (i * width)) & ((1 << width) - 1)
                       for i in range(1 << t)}
            self.assertEqual(len(factors), 1 << t)
            # Decode using codewords stated explicitly in chronological order.
            decoded = set()
            for factor in factors:
                bits = []
                for i in range(t):
                    code = (factor >> (5 * i)) & 31
                    self.assertIn(code, (0b01011, 0b01101))
                    bits.append(0 if code == 0b01011 else 1)
                decoded.add(tuple(bits))
            self.assertEqual(decoded, set(itertools.product((0, 1), repeat=t)))
            loss = 589 * word.bit_count() - 305 * length
            self.assertEqual(loss, 242 * t * (1 << t))
            if t >= 8:
                self.assertLessEqual(length, horizon(2 * t))
                self.assertGreater(loss, 128 * (2 * t) ** 2)
            if t <= 5:
                self.assertEqual(elementary_trace(word_residue(word, length),
                                                  length)[0], word)
        for t in range(8, 65):
            self.assertLessEqual(10 * t, 1 << t)
            self.assertLessEqual(5 * t * (1 << t), 1 << (2 * t - 1))
            self.assertLess(1 << (2 * t - 1), horizon(2 * t))
            self.assertGreater(242 * (1 << t), 512 * t)
        self.assertEqual(horizon(16), 63074)

    def test_periodic_words_have_the_rational_fixed_point_cylinder(self):
        for period in range(1, 6):
            for word in range(1 << period):
                j = word.bit_count()
                B = closed_constant(word, period)
                denominator = 2 ** period - 3 ** j
                self.assertEqual(denominator % 2, 1)
                for repetitions in range(1, 5):
                    length = period * repetitions
                    modulus = 1 << length
                    repeated = sum(word << (i * period)
                                   for i in range(repetitions))
                    rational_residue = B * pow(denominator, -1, modulus) % modulus
                    self.assertEqual(word_residue(repeated, length),
                                     rational_residue)
                    self.assertEqual(elementary_trace(rational_residue,
                                                      length)[0], repeated)

    def test_modular_power_against_builtin_integer_power(self):
        for base in (0, 1, 2, 3, 9, 29):
            for exponent in (0, 1, 2, 7, 32, 257):
                for bits in (0, 1, 2, 7, 16, 65, 130):
                    self.assertEqual(modular_power(base, exponent, bits),
                                     pow(base, exponent, 1 << bits))


if __name__ == '__main__':
    unittest.main()
