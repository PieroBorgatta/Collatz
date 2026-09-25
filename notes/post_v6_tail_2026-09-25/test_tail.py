"""Independent integer, finite-state and accounting tests for the tail model."""

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("tail_under_test", HERE / "tail_probe.py")
assert SPEC and SPEC.loader
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def padded_digits(value, width):
    result = [0] * width
    for i in range(width - 1, -1, -1):
        value, result[i] = divmod(value, 3)
    assert value == 0
    return result


def integer_T(value):
    return (3 * value + 1) // 2 if value % 2 else value // 2


def orbit(value, steps):
    bits = []
    for _ in range(steps):
        bits.append(value % 2)
        value = integer_T(value)
    return value, bits


def packed_oracle(bits):
    value = sum(bit * 2**i for i, bit in enumerate(bits))
    return value.to_bytes((len(bits) + 7) // 8, "little")


def outgoing_carry_sum(digits, incoming):
    # Long-division remainders from entire integer prefixes, not a digit-state
    # transition: this also keeps the effect of significant leading zeroes.
    prefix, result = incoming, 0
    for digit in digits:
        prefix = 3 * prefix + digit
        result += prefix % 2
    return result


def oracle_replay(n, steps):
    full, j, digits = n, 0, []
    bits, sums, carries, inputs, rows = [], [0], [], [], []
    for t in range(steps):
        h, p = (n // 2**t) % 2, full % 2
        z = full - 3**j * (n // 2**t)
        assert digits == padded_digits(z, j)
        a, old_sum = outgoing_carry_sum(digits, h), sum(digits)
        full = integer_T(full)
        next_j = j + p
        next_z = full - 3**next_j * (n // 2**(t + 1))
        digits = padded_digits(next_z, next_j)
        rows.append([h, p, j, old_sum, a, sum(digits)])
        j = next_j
        bits.append(p)
        inputs.append(h)
        carries.append(a)
        sums.append(sum(digits))
    ledger_bytes = b"".join((json.dumps(row, separators=(",", ":")) + "\n").encode() for row in rows)
    return {
        "steps": steps, "odd_steps": j, "terminal_tail_length": j,
        "terminal_tail_digit_sum": sums[-1], "input_ones": sum(inputs),
        "tail_digit_sum_interior": sum(sums[1:-1]),
        "tail_carry_ones_sum": sum(carries),
        "tail_digit_cells_scanned": sum(row[2] for row in rows),
        "parity_sha256": hashlib.sha256(packed_oracle(bits)).hexdigest(),
        "terminal_tail_sha256": hashlib.sha256(bytes(digits)).hexdigest(),
        "ledger_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "rows": rows, "bits": bits, "carries": carries,
    }


class TailTests(unittest.TestCase):
    def test_exact_recurrence_on_every_small_padded_state(self):
        for j in range(6):
            for z in range(3**j):
                for h in (0, 1):
                    nj, nz, p = probe.tail_step(j, z, h)
                    value = h * 3**j + z
                    self.assertEqual((nj, nz, p), (j + value % 2, integer_T(value), value % 2))
                    self.assertGreaterEqual(nz, 0)
                    self.assertLess(nz, 3**nj)

    def test_digit_scan_incoming_carry_and_mass_all_words_through_six(self):
        for j in range(7):
            for word in itertools.product(range(3), repeat=j):
                digits = list(word)
                z = sum(d * 3**(j - i - 1) for i, d in enumerate(digits))
                for h in (0, 1):
                    result, p, a = probe.digit_step(digits, h)
                    value = h * 3**j + z
                    self.assertEqual(p, value % 2)
                    self.assertEqual(result, padded_digits(integer_T(value), j + p))
                    self.assertEqual(a, outgoing_carry_sum(digits, h))
                    self.assertEqual(2 * sum(result), sum(digits) + 3 * h + 2 * a + p)
                    self.assertLessEqual(a, j)
                    self.assertEqual(digits, list(word))  # Caller state is preserved.

    def test_digit_and_integer_transitions_agree_including_empty_tail(self):
        for j in range(6):
            for z in range(3**j):
                digits = padded_digits(z, j)
                for h in (0, 1):
                    nj, nz, p = probe.tail_step(j, z, h)
                    output, dp, _ = probe.digit_step(digits, h)
                    self.assertEqual(dp, p)
                    self.assertEqual(len(output), nj)
                    self.assertEqual(output, padded_digits(nz, nj))
        self.assertEqual(probe.digit_step([], 0), ([], 0, 0))
        self.assertEqual(probe.digit_step([], 1), ([2], 1, 0))

    def test_replay_integer_oracle_counts_hashes_and_checkpoints(self):
        for n in range(97):
            for steps in range(17):
                expected = oracle_replay(n, steps)
                checkpoints = tuple(sorted({0, steps // 2, steps}))
                actual = probe.replay(n, steps, checkpoints)
                for key, value in expected.items():
                    if key not in ("rows", "bits", "carries"):
                        self.assertEqual(actual[key], value, (n, steps, key))
                self.assertTrue(actual["identities_verified"])
                self.assertEqual([row["steps"] for row in actual["checkpoints"]], list(checkpoints))
                for record in actual["checkpoints"]:
                    t = record["steps"]
                    prefix = oracle_replay(n, t)
                    self.assertEqual(record["odd_steps"], prefix["odd_steps"])
                    self.assertEqual(record["tail_digit_sum"], prefix["terminal_tail_digit_sum"])
                    self.assertEqual(record["parity_sha256"], prefix["parity_sha256"])
                    self.assertEqual(record["parity_without_first_step_sha256"],
                                     hashlib.sha256(packed_oracle(prefix["bits"][1:])).hexdigest())

    def test_unweighted_and_weighted_telescopes_from_integer_orbits(self):
        for n in (0, 1, 2, 3, 7, 27, 255, 3**40 - 1, 2**61 - 1):
            for steps in (0, 1, 2, 7, 16, 40, 80):
                data = oracle_replay(n, steps)
                self.assertEqual(data["odd_steps"] + 2 * data["tail_carry_ones_sum"],
                                 data["tail_digit_sum_interior"] + 2 * data["terminal_tail_digit_sum"]
                                 - 3 * data["input_ones"])
                parity_value = sum(bit * 2**i for i, bit in enumerate(data["bits"]))
                weighted_carries = sum(a * 2**i for i, a in enumerate(data["carries"]))
                self.assertEqual(parity_value, data["terminal_tail_digit_sum"] * 2**steps
                                 - 3 * (n % 2**steps) - 2 * weighted_carries)
                actual = probe.replay(n, steps)
                self.assertTrue(actual["weighted_telescope_verified"])
                self.assertEqual(actual["ledger_sha256"], data["ledger_sha256"])

    def test_sharp_normalized_bounds_and_extremal_parity_words(self):
        for t in range(10):
            by_word = {}
            for residue in range(2**t):
                tail, bits = orbit(residue, t)
                j = sum(bits)
                c = 2**t * tail - 3**j * residue
                lower = 3**j - 2**j
                upper = 2**(t - j) * lower
                self.assertLessEqual(lower, c)
                self.assertLessEqual(c, upper)
                self.assertGreaterEqual(tail, 0)
                self.assertLess(tail, 3**j)
                self.assertGreaterEqual(3**j * (2**t - residue - 1) + 2**j, 2**t)
                by_word[tuple(bits)] = c
            for j in range(t + 1):
                self.assertEqual(by_word[(1,) * j + (0,) * (t-j)], 3**j - 2**j)
                self.assertEqual(by_word[(0,) * (t-j) + (1,) * j],
                                 2**(t-j) * (3**j - 2**j))

    def test_reachable_unit_tails_by_inverse_two_at_a_common_time(self):
        for target_j in range(1, 6):
            j, z = 0, 0
            for _ in range(target_j):
                j, z, p = probe.tail_step(j, z, 1)
                self.assertEqual(p, 1)
            modulus, count = 3**target_j, 2 * 3**(target_j - 1)
            self.assertEqual((j, z), (target_j, modulus - 1))
            visited, suffix = set(), []
            for k in range(count):
                self.assertNotIn(z, visited)
                visited.add(z)
                # Leading zero input symbols make every target reachable at
                # the SAME time, rather than only somewhere along a cycle.
                inputs = [0] * (count - 1 - k) + [1] * target_j + suffix
                n = sum(bit * 2**i for i, bit in enumerate(inputs))
                endpoint, parities = orbit(n, len(inputs))
                self.assertEqual(len(inputs), target_j + count - 1)
                self.assertEqual(sum(parities), target_j)
                self.assertEqual(endpoint, z)
                h = z % 2
                nj, nz, p = probe.tail_step(j, z, h)
                self.assertEqual((nj, p), (target_j, 0))
                self.assertEqual(nz, z * pow(2, -1, modulus) % modulus)
                suffix.append(h)
                z = nz
            self.assertEqual(z, modulus - 1)
            self.assertEqual(visited, {value for value in range(modulus) if value % 3})
        self.assertEqual(probe.tail_step(0, 0, 0), (0, 0, 0))

    def test_distinguishability_of_all_states_through_length_four(self):
        steps = (2 * 3**4 - 1).bit_length()
        outputs = {}
        for initial_j in range(5):
            for initial_z in range(3**initial_j):
                j, z, bits = initial_j, initial_z, []
                for t in range(steps):
                    j, z, p = probe.tail_step(j, z, int(t == 0))
                    bits.append(p)
                # One shared input word (1 then zeroes) distinguishes even
                # states with different lengths, since 3^j+z ranges disjointly.
                _, expected = orbit(3**initial_j + initial_z, steps)
                self.assertEqual(bits, expected)
                self.assertNotIn(tuple(bits), outputs)
                outputs[tuple(bits)] = (initial_j, initial_z)
        self.assertEqual(len(outputs), sum(3**j for j in range(5)))

    def test_finite_binary_input_to_parity_bijection(self):
        for t in range(10):
            outputs = set()
            for n in range(2**t):
                j, z, bits = 0, 0, []
                for i in range(t):
                    j, z, p = probe.tail_step(j, z, (n >> i) & 1)
                    bits.append(p)
                endpoint, expected = orbit(n, t)
                self.assertEqual(bits, expected)
                self.assertEqual(z, endpoint)
                outputs.add(tuple(bits))
            self.assertEqual(len(outputs), 2**t)

    def test_block_prediction_all_small_unit_tails_and_future_inputs(self):
        for initial_j in range(4):
            tails = [0] if initial_j == 0 else [z for z in range(3**initial_j) if z % 3]
            for initial_z in tails:
                for k in range(6):
                    for inputs_tuple in itertools.product((0, 1), repeat=k):
                        inputs = list(inputs_tuple)
                        predicted = probe.block_predict(initial_j, initial_z % 2**k, inputs)
                        j, z, full_outputs = initial_j, initial_z, []
                        for h in inputs:
                            j, z, p = probe.tail_step(j, z, h)
                            full_outputs.append(p)
                        source = 3**initial_j * sum(h * 2**i for i, h in enumerate(inputs)) + initial_z
                        _, integer_outputs = orbit(source, k)
                        self.assertEqual(predicted, full_outputs)
                        self.assertEqual(predicted, integer_outputs)
                        self.assertEqual(inputs, list(inputs_tuple))

    def test_block_equivalence_classes_are_exactly_tail_residues(self):
        j, k = 3, 2
        tails = [z for z in range(3**j) if z % 3]
        by_tail = {}
        for z in tails:
            signatures = []
            for source in range(2**k):
                inputs = [(source >> i) & 1 for i in range(k)]
                _, outputs = orbit(3**j * source + z, k)
                prediction = probe.block_predict(j, z % 2**k, inputs)
                self.assertEqual(prediction, outputs)
                signatures.append(tuple(outputs))
            by_tail[z] = signatures
        for first, second in itertools.product(tails, repeat=2):
            equivalent = first % 2**k == second % 2**k
            self.assertEqual(by_tail[first] == by_tail[second], equivalent)
            # Distinct residue classes can be distinguished even with any
            # one fixed common input word, not only by some chosen suffix.
            for a, b in zip(by_tail[first], by_tail[second]):
                self.assertEqual(a == b, equivalent)

    def test_zero_length_blocks_and_invalid_block_precision(self):
        for j in range(11):
            self.assertEqual(probe.block_predict(j, 0, []), [])
        for args in ((0, 1, []), (-1, 0, []), (1, -1, [0]),
                     (1, 2, [1]), (1, 0, [2]), (1, 0, [-1])):
            with self.assertRaises(ValueError):
                probe.block_predict(*args)

    def test_paired_unequal_horizons_against_direct_integer_orbits(self):
        baseline = {}
        for v in range(5, 9):
            m, r = 2**(v + 1), v + 3
            _, bits = orbit((3**m - 1) // 2**r, probe.horizon(v))
            baseline[v] = {"odd_steps": sum(bits),
                           "parity_trace_sha256": hashlib.sha256(packed_oracle(bits)).hexdigest()}
        for v in range(5, 8):
            result = probe.paired_level(v, baseline)
            r, m, h = v + 3, 2**(v + 1), probe.horizon(v)
            _, lower = orbit((3**m - 1) // 2**r, h)
            upper_time = 2 * h + r
            _, upper = orbit((3**(2*m) - 1) // 2**r, upper_time)
            next_time = probe.horizon(v + 1) + 1
            expected_e = sum(upper) - 2 * sum(lower)
            expected_delta = sum(upper[:next_time]) - 2 * sum(lower)
            self.assertEqual(result["E"], expected_e)
            self.assertEqual(result["delta"], expected_delta)
            self.assertEqual(result["upper_extra_odd_steps"], sum(upper[next_time:]))
            self.assertEqual(result["upper_extra_steps"], upper_time - next_time)
            self.assertEqual(sum(result["unequal_horizon_terms"].values()), expected_e)

    def test_invalid_states_and_checkpoints_are_rejected(self):
        for args in ((-1, 0, 0), (0, -1, 0), (0, 1, 0), (2, 9, 1), (1, 0, 2)):
            with self.assertRaises(ValueError):
                probe.tail_step(*args)
        for args in (([3], 0), ([-1], 1), ([0], -1), ([], 2)):
            with self.assertRaises(ValueError):
                probe.digit_step(*args)
        for args in ((-1, 2), (1, -1), (1, 2, (-1,)), (1, 2, (3,))):
            with self.assertRaises(ValueError):
                probe.replay(*args)


if __name__ == "__main__":
    unittest.main()
