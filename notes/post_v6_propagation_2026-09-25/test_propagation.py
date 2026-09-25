"""Independent integer and finite-word checks for carry propagation."""

from fractions import Fraction
import hashlib
import importlib.util
import itertools
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("propagation_under_test", HERE / "propagation_probe.py")
assert SPEC and SPEC.loader
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def integer_digits(value, width=None):
    """Ordinary integer division oracle, independent of the digit engines."""
    result = []
    while value:
        value, digit = divmod(value, 3)
        result.insert(0, digit)
    result = result or [0]
    if width is not None:
        if width == 0:
            assert result == [0]
            return []
        assert len(result) <= width
        result = [0] * (width - len(result)) + result
    return result


def integer_orbit(initial, steps):
    states, bits = [initial], []
    for _ in range(steps):
        value = states[-1]
        bit = value % 2
        bits.append(bit)
        states.append((3 * value + 1) // 2 if bit else value // 2)
    return states, bits


def integer_prefix_carries(value, width):
    return [(value // 3**(width - i)) % 2 for i in range(1, width + 1)]


def checkpoint_arguments(width, r, t):
    initial, remainder = divmod(3**width - 1, 2**r)
    assert remainder == 0
    states, bits = integer_orbit(initial, t)
    model, carries = probe.power_model(width + t, r + t)
    return [integer_digits(states[-1]), states[-1], width, r, t,
            bits, model, carries]


class PropagationTests(unittest.TestCase):
    def test_quotient_words_against_integer_division_and_remainders(self):
        for width in range(1, 25):
            for r in range(1, 9):
                with self.subTest(width=width, r=r):
                    quotient, remainder = divmod(3**width - 1, 2**r)
                    if remainder:
                        with self.assertRaises(ValueError):
                            probe.quotient_word(width, r)
                    else:
                        word = probe.quotient_word(width, r)
                        self.assertEqual(word, integer_digits(quotient, width))
                        self.assertEqual(probe.decode_chunks(word), quotient)

    def test_power_model_digits_and_each_prefix_carry(self):
        for width in range(33):
            for s in range(1, 13):
                with self.subTest(width=width, s=s):
                    digits, carries = probe.power_model(width, s)
                    value = 3**width // 2**s
                    self.assertEqual(digits, integer_digits(value, width))
                    expected = [(3**i // 2**s) % 2 for i in range(1, width + 1)]
                    self.assertEqual(carries, expected)
                    self.assertEqual(probe.carry_scan(digits), expected)

    def test_affine_constant_and_extrema_over_every_word_through_nine(self):
        for t in range(10):
            grouped = [[] for _ in range(t + 1)]
            for word in itertools.product((0, 1), repeat=t):
                # Apply the prescribed affine branches to two rational inputs.
                # They need not be actual parity words of those test inputs.
                zero, one = Fraction(0), Fraction(1)
                for bit in word:
                    zero = (3 * zero + 1) / 2 if bit else zero / 2
                    one = (3 * one + 1) / 2 if bit else one / 2
                c, j = probe.affine_constant(list(word))
                self.assertEqual(c, zero * 2**t)
                self.assertEqual(j, sum(word))
                self.assertEqual((one - zero) * 2**t, 3**j)
                grouped[j].append(c)
            for j, values in enumerate(grouped):
                self.assertEqual(min(values), 3**j - 2**j)
                self.assertEqual(max(values), 2**(t - j) * (3**j - 2**j))
        with self.assertRaises(ValueError):
            probe.affine_constant([0, 2, 1])

    def test_prefix_identity_for_small_odd_integral_quotients(self):
        cases = 0
        for width in range(1, 19):
            for r in range(1, 8):
                initial, remainder = divmod(3**width - 1, 2**r)
                if remainder or initial % 2 != 1:
                    continue
                cases += 1
                states, bits = integer_orbit(initial, 12)
                for t in (0, 1, 2, 3, 7, 12):
                    with self.subTest(width=width, r=r, t=t):
                        j, value = sum(bits[:t]), states[t]
                        model, carries = probe.power_model(width + t, r + t)
                        row, actual = probe.checkpoint_state(
                            integer_digits(value), value, width, r, t,
                            bits[:t], model, carries,
                        )
                        padded_width = width + j
                        expected = integer_prefix_carries(value, padded_width)
                        self.assertEqual(actual, expected)
                        self.assertEqual(2**(r + t) * value,
                                         3**padded_width + row["boundary_B"])
                        self.assertEqual(row["original_prefix_length"], width)
                        for i in range(1, width + 1):
                            self.assertEqual(value // 3**(padded_width - i),
                                             3**i // 2**(r + t))
                        changed = sum(a != b for a, b in zip(expected[:width], carries[:width]))
                        self.assertEqual(row["changed_original_carries"], changed)
                        self.assertEqual(changed, 0)
                        self.assertTrue(row["all_original_digits_and_carries_verified"])
                        if row["first_changed_digit_one_based"] is not None:
                            self.assertGreater(row["first_changed_digit_one_based"], width)
                        tail = value % 3**j
                        self.assertEqual(row["append_tail_value"], tail)
                        self.assertEqual(row["append_tail_digits"],
                                         "".join(map(str, integer_digits(tail, j))))
                        self.assertEqual(row["append_tail_carry_ones"], sum(expected[width:]))
                        self.assertEqual(row["carry_ones_total"], sum(expected))
                        self.assertEqual(row["low_binary_residue"], initial % 2**t)
        self.assertGreater(cases, 10)

    def test_generic_quotient_identity_all_small_residues_and_lifts(self):
        for t in range(11):
            for residue in range(2**t):
                residue_states, residue_bits = integer_orbit(residue, t)
                c, j = probe.affine_constant(residue_bits)
                tail = residue_states[-1]
                self.assertLess(tail, 3**j)
                self.assertGreaterEqual(tail, 0)
                inverse_numerator = 2**t * tail - c
                self.assertEqual(inverse_numerator, 3**j * residue)
                self.assertEqual(inverse_numerator % 3**j, 0)
                self.assertGreaterEqual(inverse_numerator, 0)
                self.assertLess(inverse_numerator, 3**j * 2**t)
                for quotient in (0, 1, 2, 7):
                    initial = quotient * 2**t + residue
                    states, bits = integer_orbit(initial, t)
                    endpoint = states[-1]
                    self.assertEqual(bits, residue_bits)
                    self.assertEqual(endpoint // 3**j, initial // 2**t)
                    self.assertEqual(endpoint, 3**j * quotient + tail)
                    self.assertEqual(endpoint % 3**j, tail)

    def test_replay_all_small_level_state_checkpoints_with_integer_T(self):
        for v in range(6):
            result = probe.replay_level(v)
            r, m = v + 3, 2**(v + 1)
            self.assertIn(32, [row["t"] for row in result["checkpoints"]])
            for side, width in (("lower", m), ("upper", 2 * m)):
                states, bits = integer_orbit((3**width - 1) // 2**r, 32)
                for checkpoint in result["checkpoints"]:
                    t, record = checkpoint["t"], checkpoint[side]
                    j, value = sum(bits[:t]), states[t]
                    digits = integer_digits(value)
                    padded = integer_digits(value, width + j)
                    self.assertEqual(record["odd_steps"], j)
                    self.assertEqual(record["parity_word"], "".join(map(str, bits[:t])))
                    self.assertEqual(record["canonical_length"], len(digits))
                    self.assertEqual(record["padded_width"], width + j)
                    self.assertEqual(record["full_ternary_sha256"], hashlib.sha256(bytes(padded)).hexdigest())
                    self.assertEqual(record["affine_C"], 2**t * value - 3**j * states[0])
                    self.assertEqual(record["boundary_B"], 2**(r + t) * value - 3**(width + j))

    def test_replay_seam_is_original_upper_windows_not_doubling_error(self):
        for v in range(6):
            result = probe.replay_level(v)
            r, m = result["r"], result["m"]
            states, bits = integer_orbit((3**(2 * m) - 1) // 2**r, 32)
            lower_states, lower_bits = integer_orbit((3**m - 1) // 2**r, 32)
            for checkpoint in result["checkpoints"]:
                t = checkpoint["t"]
                width = 2 * m + sum(bits[:t])
                carries = integer_prefix_carries(states[t], width)
                actual = sum(carries[m:2*m]) - sum(carries[:m])
                model = [(3**i // 2**(r + t)) % 2 for i in range(1, 2 * m + 1)]
                expected_model = sum(model[m:]) - sum(model[:m])
                self.assertEqual(checkpoint["actual_seam_difference"], actual)
                self.assertEqual(checkpoint["model_seam_difference"], expected_model)
                self.assertEqual(checkpoint["signed_boundary_error"], actual - expected_model)
                self.assertEqual(actual, expected_model)
                self.assertEqual(checkpoint["uniform_edge_error"], 0)
                lower_j = sum(lower_bits[:t])
                lower_carries = integer_prefix_carries(lower_states[t], m + lower_j)
                total_difference = sum(carries) - 2 * sum(lower_carries)
                tail_difference = sum(carries[2*m:]) - 2 * sum(lower_carries[m:])
                self.assertEqual(total_difference, expected_model + tail_difference)
                self.assertEqual(checkpoint["paired_total_carry_difference"], total_difference)
                self.assertEqual(checkpoint["append_tail_carry_difference"], tail_difference)
                tail_bound = max(sum(bits[:t]), 2 * lower_j)
                self.assertEqual(checkpoint["append_tail_difference_bound"], tail_bound)
                self.assertLessEqual(abs(tail_difference), tail_bound)
                self.assertLessEqual(tail_bound, 2 * t)

    def test_finite_dyadic_fourier_bound_and_explicit_constants(self):
        for r in range(3, 9):
            m = 2**(r - 2)
            for t in range(9):
                with self.subTest(r=r, t=t):
                    bits = [(3**i // 2**(r + t)) % 2 for i in range(1, 2 * m + 1)]
                    seam = sum(bits[m:]) - sum(bits[:m])
                    bound = probe.explicit_bound(r, t)
                    numerator = m * 2**t * (r - 1)**2 * (r + t + 1)**2
                    self.assertEqual(bound["model_bound_squared_numerator"], numerator)
                    self.assertEqual(bound["model_bound_squared_denominator"], 2)
                    self.assertLessEqual(2 * seam**2, numerator)
                    self.assertEqual(bound["uniform_edge_error"], 0)
                    self.assertEqual(bound["actual_bound_below_m"], bound["model_bound_below_m"])
                    if t == 0:
                        signed_first_window = sum(1 - 2 * bit for bit in bits[:m])
                        self.assertEqual(seam, signed_first_window)

    def test_bound_thresholds_and_monotonic_depth(self):
        for row in probe.threshold_table():
            t, first = row["t"], row["first_r_for_bound_below_m"]
            self.assertEqual(row["first_v"], first - 3)
            for r in range(3, first + 9):
                m = 2**(r - 2)
                numerator = m * 2**t * (r - 1)**2 * (r + t + 1)**2
                expected = numerator < 2 * m**2
                self.assertEqual(expected, r >= first)
                self.assertEqual(probe.explicit_bound(r,t)["actual_bound_below_m"], expected)
        for r in range(3, 41):
            last = probe.max_nontrivial_depth(r)
            for field in ("actual_bound_below_m", "model_bound_below_m"):
                flags = [probe.explicit_bound(r, t)[field] for t in range(max(4, last + 4))]
                self.assertEqual(flags, [t <= last for t in range(len(flags))])

    def test_zero_odd_steps_give_complete_model_identity(self):
        for r in range(3, 6):
            for t in range(5):
                width = 2**(r + t - 2)
                arguments = checkpoint_arguments(width, r, t)
                self.assertEqual(arguments[5], [0] * t)
                record, carries = probe.checkpoint_state(*arguments)
                self.assertEqual(record["odd_steps"], 0)
                self.assertEqual(record["affine_C"], 0)
                self.assertEqual(record["boundary_B"], -1)
                self.assertIsNone(record["first_changed_digit_one_based"])
                self.assertEqual(record["changed_original_carries"], 0)
                self.assertEqual(carries, arguments[7][:width])

    def test_checkpoint_rejects_corrupted_word_state_and_history(self):
        arguments = checkpoint_arguments(16, 6, 7)
        probe.checkpoint_state(*arguments)
        for mutation in ("digits", "integer", "history", "model", "model_carry"):
            changed = [list(x) if isinstance(x, list) else x for x in arguments]
            if mutation == "digits":
                changed[0][-1] = (changed[0][-1] + 1) % 3
            elif mutation == "integer":
                changed[1] += 1
            elif mutation == "history":
                changed[5][0] ^= 1
            elif mutation == "model":
                changed[6][0] = (changed[6][0] + 1) % 3
            else:
                changed[7][0] ^= 1
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                probe.checkpoint_state(*changed)


if __name__ == "__main__":
    unittest.main()
