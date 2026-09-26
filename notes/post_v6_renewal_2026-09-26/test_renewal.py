#!/usr/bin/env python3
"""Independent finite-orbit checks of sharp quadratic-cylinder information bounds."""
from collections import Counter
import hashlib
from math import comb
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import renewal_probe as probe


def orbit(n, length):
    """Integer oracle: never uses the modular predictor or parity inverse."""
    outputs = []
    for _ in range(length):
        outputs.append(n % 2)
        if n % 2:
            n = (3 * n + 1) // 2
        else:
            n //= 2
    return outputs, n


def packed_word(outputs):
    return sum(bit * 2**i for i, bit in enumerate(outputs))


def quadratic(v, n):
    return n + 2**(v + 2) * n * n


def tower(v):
    return (3**(2**(v + 1)) - 1) // 2**(v + 3)


def horizon(v):
    return (589 * 2**v + 611) // 612


class RenewalTests(unittest.TestCase):
    def test_direct_integer_orbits(self):
        for n in range(129):
            for length in range(17):
                self.assertEqual(probe.direct_word(n, length),
                                 packed_word(orbit(n, length)[0]))

    def test_quadratic_permutation_and_inverse_exhaustive(self):
        for v in range(5):
            for bits in range(10):
                modulus = 2**bits
                image = {}
                for n in range(modulus):
                    target = quadratic(v, n) % modulus
                    self.assertNotIn(target, image)
                    image[target] = n
                    self.assertEqual(probe.f(v, n), quadratic(v, n))
                    self.assertEqual(probe.inverse_f(v, target, bits), n)
                self.assertEqual(set(image), set(range(modulus)))

    def test_cylinder_extrema_and_binomial_multiplicities(self):
        # Enumerate every source lift, not merely the claimed parity interval.
        for v in range(3):
            for K in range(8):
                lower_words = [orbit(x, K)[0] for x in range(2**K)]
                upper_words = [orbit(quadratic(v, x), K)[0]
                               for x in range(2**K)]
                for H in range(K + 1):
                    for M in range(H, K + 1):
                        for a in range(2**M):
                            j = sum(lower_words[a][:H])
                            counts = Counter()
                            for x in range(a, 2**K, 2**M):
                                self.assertEqual(lower_words[x][:H], lower_words[a][:H])
                                self.assertEqual(upper_words[x][:M], upper_words[a][:M])
                                counts[sum(upper_words[x]) - 2*j] += 1
                            result = probe.cylinder_envelope(
                                j, H, K, packed_word(upper_words[a]), M)
                            self.assertEqual(result['minimum'], min(counts))
                            self.assertEqual(result['maximum'], max(counts))
                            self.assertEqual(result['free_bits'], K-M)
                            self.assertEqual(result['upper_prefix_odd'], sum(upper_words[a][:M]))
                            self.assertEqual(counts, Counter({min(counts)+s: comb(K-M, s)
                                                             for s in range(K-M+1)}))

    def test_minimum_precision_exhaustive_including_failure(self):
        for K in range(7):
            for word in range(2**K):
                bits = [(word // 2**i) % 2 for i in range(K)]
                for H in range(K + 1):
                    for j in range(H + 1):
                        bounds = [(M, sum(bits[:M]) + K-M - 2*j)
                                  for M in range(H, K + 1)]
                        for g in range(-2*H-1, K+2):
                            expected = next((M for M, value in bounds if value <= g), None)
                            self.assertEqual(probe.minimum_precision(j, H, K, word, g), expected)

    def test_unknown_upper_word_suffix_cannot_change_envelope(self):
        for K in range(1, 8):
            for H in range(K+1):
                for M in range(H, K+1):
                    for prefix in range(2**M):
                        upper0 = prefix
                        upper1 = prefix + (2**K - 2**M)
                        self.assertEqual(probe.cylinder_envelope(H//2, H, K, upper0, M),
                                         probe.cylinder_envelope(H//2, H, K, upper1, M))

    def test_paired_block_oracle_sharpness_and_offset(self):
        for v in range(3):
            for t in range(1, 4):
                for b in range(1, 3):
                    end = 2*t + 2*b - 1
                    lower = [orbit(x, t+b)[0] for x in range(2**end)]
                    upper = [orbit(2*quadratic(v, x), 2*t+2*b)[0]
                             for x in range(2**end)]
                    for B in range(max(t+b, 2*t-1), end+1):
                        for a in range(2**B):
                            counts = Counter()
                            for x in range(a, 2**end, 2**B):
                                self.assertEqual(lower[x], lower[a])
                                self.assertEqual(upper[x][:2*t], upper[a][:2*t])
                                counts[sum(upper[x][2*t:]) - 2*sum(lower[x][t:])] += 1
                            result = probe.block_reward_envelope(v, a, t, b, B)
                            self.assertEqual(result['minimum'], min(counts))
                            self.assertEqual(result['maximum'], max(counts))
                            self.assertEqual(result['lower_block_odd'], sum(lower[a][t:]))
                            self.assertEqual(result['fixed_upper_steps'], B-(2*t-1))
                            self.assertEqual(result['free_upper_steps'], end-B)
                            self.assertEqual(counts, Counter({min(counts)+s: comb(end-B, s)
                                                             for s in range(end-B+1)}))

    def test_extremal_lifts_both_directions_and_endpoint_precisions(self):
        for v in range(3):
            for K in range(8):
                for M in range(K+1):
                    for residue in range(min(2**M, 16)):
                        for high in (0, 5):
                            x = high * 2**K + residue
                            for all_ones in (False, True):
                                X = probe.extremal_lift(v, x, K, M, all_ones)
                                actual = orbit(quadratic(v, X), K)[0]
                                expected = orbit(quadratic(v, x), M)[0]
                                expected += [int(all_ones)] * (K-M)
                                self.assertEqual(actual, expected)
                                self.assertEqual(X % 2**M, x % 2**M)
                                self.assertEqual(X // 2**K, x // 2**K)
                                self.assertEqual(orbit(X, M)[0], orbit(x, M)[0])
                                if high:
                                    self.assertGreater(X, 0)
        self.assertEqual(probe.extremal_lift(0, 0, 0, 0), 0)

    def test_tower_thresholds_and_concrete_witnesses(self):
        baseline = {}
        for v in range(5, 10):
            outputs = orbit(tower(v), horizon(v))[0]
            data = packed_word(outputs).to_bytes((len(outputs)+7)//8, 'little')
            baseline[v] = {'odd_steps': sum(outputs),
                           'parity_trace_sha256': hashlib.sha256(data).hexdigest()}
        witnesses = 0
        for v in range(5, 9):
            row = probe.threshold_record(v, baseline)
            H, K, Q = horizon(v), horizon(v+1), tower(v)
            lower, upper = orbit(Q, H)[0], orbit(tower(v+1), K)[0]
            target = 2 * 2**((v+1)//2)
            bounds = [sum(upper[:M]) + K-M - 2*sum(lower) for M in range(H, K+1)]
            expected = next((H+i for i, value in enumerate(bounds) if value <= target), None)
            self.assertEqual(row['minimum_source_precision'], expected)
            self.assertEqual(row['delta_actual'], sum(upper)-2*sum(lower))
            witness = probe.witness_record(row)
            if witness is None:
                self.assertTrue(expected is None or expected == H)
                continue
            witnesses += 1
            X, Y = int(witness['X_hex'], 16), int(witness['Y_hex'], 16)
            M = expected-1
            self.assertEqual(Y, quadratic(v, X))
            self.assertGreater(X, 0)
            self.assertNotEqual(X, Q)
            self.assertEqual(X.bit_length(), Q.bit_length())
            self.assertEqual(X % 2**M, Q % 2**M)
            self.assertEqual(X // 2**K, Q // 2**K)
            self.assertEqual(orbit(X, H)[0], lower)
            self.assertEqual(sum(orbit(Y, K)[0]) - 2*sum(lower), target+1)
            self.assertIsNone(probe.integer_ancestor(v, X))
        self.assertGreater(witnesses, 0)

    def test_integer_ancestry_requires_square_and_correct_root_class(self):
        for v in range(1, 9):
            self.assertEqual(probe.integer_ancestor(v, tower(v)), tower(v-1))
        for v in range(1, 6):
            # This oracle enumerates the forward polynomial, including all
            # predecessors possible for x<=256, without using square roots.
            preimages = {quadratic(v-1, n): n for n in range(1, 257)}
            for x in range(1, 257):
                self.assertEqual(probe.integer_ancestor(v, x), preimages.get(x))
            for n in (1, 2, 3, 7, 32, 257):
                self.assertEqual(probe.integer_ancestor(v, quadratic(v-1, n)), n)
        self.assertIsNone(probe.integer_ancestor(2, 1))  # signature 33 is not a square
        self.assertIsNone(probe.integer_ancestor(2, 7))  # signature 15^2, wrong root mod16

    def check_positive_loop(self, v, k, length, prefix_length=None):
        row = probe.positive_loop(v, k, length, prefix_length)
        h = v+3 if prefix_length is None else prefix_length
        start = max(h, length+k+1)
        precision = 2*start+2*length+k-1
        X, U = int(row['X_hex'], 16), int(row['U_hex'], 16)
        Q = tower(v)
        self.assertEqual(U, 2*quadratic(v, X))
        self.assertGreater(X, 0)
        self.assertEqual(row['is_actual_tower_source'], X == Q)
        self.assertEqual(X.bit_length(), Q.bit_length())
        self.assertEqual(X // 2**precision, Q // 2**precision)
        self.assertEqual(X % 2**h, Q % 2**h)
        self.assertEqual(orbit(X, h)[0], orbit(Q, h)[0])
        lower = orbit(X, start)[1]
        upper = orbit(U, 2*start)[1]
        rewards = []
        for i in range(length+1):
            self.assertEqual((lower % 2**k, upper % 2**k), (0, 2**k-1))
            if i < length:
                low_bits, lower = orbit(lower, 1)
                up_bits, upper = orbit(upper, 2)
                rewards.append(sum(up_bits)-2*sum(low_bits))
        self.assertEqual(rewards, [2]*length)
        self.assertEqual(row['total_reward'], sum(rewards))
        self.assertEqual(row['states_checked'], length+1)
        self.assertEqual(row['source_precision'], precision)
        self.assertEqual(row['paired_start_time'], start)
        self.assertEqual(row['preserved_actual_lower_prefix_length'], h)
        self.assertEqual(row['loop_lies_within_lower_target_horizon'], start+length <= horizon(v))
        return row

    def test_positive_loops_within_horizon_keep_only_declared_prefix(self):
        for v, k, length in ((5, 3, 8), (8, 4, 16), (12, 8, 64)):
            row = self.check_positive_loop(v, k, length)
            self.assertTrue(row['loop_lies_within_lower_target_horizon'])
            self.assertLess(row['preserved_actual_lower_prefix_length'], horizon(v))
            self.assertFalse(row['is_actual_tower_source'])

    def test_positive_loop_preserving_full_prefix_is_after_horizon(self):
        row = self.check_positive_loop(5, 3, 8, horizon(5))
        self.assertFalse(row['loop_lies_within_lower_target_horizon'])
        # Independently obtained by single-bit inverse enumeration.
        self.assertEqual(int(row['X_hex'], 16), 0x2b56bc6f000003068c797ebd)
        self.assertEqual(row['source_precision'], 80)

    def test_actual_short_projection_loop_is_distinct_from_constructed_source(self):
        row = probe.actual_projection_loop(5, 18, 1, 1)
        Q = tower(5)
        lower, upper = orbit(Q, 18)[1], orbit(2*quadratic(5, Q), 36)[1]
        lower_bits, next_lower = orbit(lower, 1)
        upper_bits, next_upper = orbit(upper, 2)
        self.assertEqual((lower % 2, upper % 2), (0, 1))
        self.assertEqual((next_lower % 2, next_upper % 2), (0, 1))
        self.assertEqual(lower_bits, [0])
        self.assertEqual(upper_bits, [1, 1])
        self.assertEqual(row['integer_state_pairs_hex'],
                         [[hex(lower), hex(upper)], [hex(next_lower), hex(next_upper)]])
        self.assertEqual(row['total_reward'], 2)
        self.assertTrue(row['is_actual_tower_source'])
        self.assertNotEqual(lower, next_lower)
        self.assertNotEqual(upper, next_upper)
        constructed = self.check_positive_loop(5, 1, 1, 18)
        self.assertFalse(constructed['is_actual_tower_source'])

    def test_repeated_mod2_pair_does_not_imply_maximum_reward(self):
        Q = tower(5)
        for t in (15, 28):
            lower, upper = orbit(Q, t)[1], orbit(2*quadratic(5, Q), 2*t)[1]
            lower_bits, next_lower = orbit(lower, 1)
            upper_bits, next_upper = orbit(upper, 2)
            self.assertEqual((lower % 2, upper % 2), (0, 1))
            self.assertEqual((next_lower % 2, next_upper % 2), (0, 1))
            self.assertEqual(sum(upper_bits)-2*sum(lower_bits), 1)
            with self.assertRaises(ValueError):
                probe.actual_projection_loop(5, t, 1, 1)

    def test_invalid_arguments(self):
        invalid_calls = [
            lambda: probe.direct_word(-1, 1),
            lambda: probe.direct_word(1, -1),
            lambda: probe.cylinder_envelope(2, 1, 3, 0, 2),
            lambda: probe.cylinder_envelope(0, 2, 3, 0, 1),
            lambda: probe.cylinder_envelope(0, 1, 3, 8, 2),
            lambda: probe.minimum_precision(0, 2, 1, 0, 0),
            lambda: probe.inverse_f(0, 4, 2),
            lambda: probe.extremal_lift(0, 1, 2, 3),
            lambda: probe.block_reward_envelope(0, 1, 0, 1, 1),
            lambda: probe.block_reward_envelope(0, 1, 2, 2, 3),
            lambda: probe.block_reward_envelope(0, 1, 2, 1, 6),
            lambda: probe.integer_ancestor(0, 1),
            lambda: probe.integer_ancestor(1, 0),
            lambda: probe.positive_loop(5, 0, 1),
            lambda: probe.positive_loop(5, 1, 0),
            lambda: probe.positive_loop(5, 1, 1, -1),
            lambda: probe.positive_loop(5, 3, 100),  # required precision exceeds source height
            lambda: probe.actual_projection_loop(5, 0, 1, 1),  # initial lower source is odd
            lambda: probe.actual_projection_loop(5, 31, 1, 1),  # beyond target horizon
        ]
        for call in invalid_calls:
            with self.assertRaises(ValueError):
                call()


if __name__ == '__main__':
    unittest.main()
