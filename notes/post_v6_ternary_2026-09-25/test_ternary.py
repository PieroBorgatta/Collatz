"""Independent finite checks for the ordinary-ternary Collatz probe.

The oracle uses Python integer T, quotient/remainder, and prefix values.
No production ternary transition is used to construct expected orbits.
Run with ``python3 -m unittest discover -s <this directory> -v``.
TERNARY_ENGINE may name an existing C executable; otherwise a temporary
executable is compiled from ternary_engine.c.
"""

from __future__ import annotations

import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import ternary_probe as probe


HERE = Path(__file__).resolve().parent


def ordinary_digits(value: int) -> list[int]:
    """Base conversion independent of the implementation under test."""
    if value == 0:
        return [0]
    result = []
    while value:
        value, digit = divmod(value, 3)
        result.append(digit)
    return result[::-1]


def digit_value(digits: list[int]) -> int:
    return sum(digit * 3**place for place, digit in enumerate(reversed(digits)))


def integer_step(value: int) -> int:
    return (3 * value + 1) // 2 if value & 1 else value // 2


def prefix_carries(digits: list[int], incoming: int = 0) -> list[int]:
    """A division carry is the remainder of the whole prefix integer."""
    prefix = incoming
    result = []
    for digit in digits:
        prefix = prefix * 3 + digit
        result.append(prefix % 2)
    return result


def integer_orbit(m: int, steps: int) -> tuple[int, list[int], list[list[int]]]:
    value = 3**m - 1
    bits, ledger = [], []
    for _ in range(steps):
        before = ordinary_digits(value)
        odd = value % 2
        scanned = before + ([1] if odd else [])
        after_value = integer_step(value)
        after = ordinary_digits(after_value)
        row = [odd, len(before), len(after), sum(before), sum(after),
               sum(prefix_carries(scanned)), len(scanned) - len(after),
               before.count(1), after.count(1)]
        bits.append(odd)
        ledger.append(row)
        value = after_value
    return value, bits, ledger


def integer_type_counts(value: int) -> tuple[int, ...]:
    counts = [0] * 6
    prefix = 0
    for digit in ordinary_digits(value):
        counts[3 * (prefix % 2) + digit] += 1
        prefix = prefix * 3 + digit
    return tuple(counts)


class TernaryPythonTests(unittest.TestCase):
    def test_conversion_and_padded_words(self):
        for value in range(1, 2000):
            expected = ordinary_digits(value)
            self.assertEqual(probe.to_digits(value), expected)
            self.assertEqual(probe.from_digits(expected), value)
            self.assertEqual(probe.from_digits([0, 0] + expected), value)

    def test_division_exhaustive_including_incoming_carry(self):
        for length in range(1, 7):
            for word in itertools.product(range(3), repeat=length):
                digits = list(word)
                for incoming in (0, 1):
                    with self.subTest(word=word, incoming=incoming):
                        numerator = incoming * 3**length + digit_value(digits)
                        quotient, remainder = divmod(numerator, 2)
                        expected = ordinary_digits(quotient)
                        expected = [0] * (length - len(expected)) + expected
                        result, outgoing, carries = probe.divide_digits(digits, incoming)
                        self.assertEqual(result, expected)
                        self.assertEqual(outgoing, remainder)
                        self.assertEqual(carries, sum(prefix_carries(digits, incoming)))

    def test_single_steps_and_all_ledger_columns(self):
        for value in range(1, 2500):
            before = ordinary_digits(value)
            odd = value % 2
            scanned = before + ([1] if odd else [])
            expected = ordinary_digits(integer_step(value))
            digits, row = probe.step_digits(before)
            self.assertEqual(digits, expected)
            self.assertEqual(row, [odd, len(before), len(expected), sum(before),
                                   sum(expected), sum(prefix_carries(scanned)),
                                   len(scanned) - len(expected), before.count(1),
                                   expected.count(1)])
            self.assertIn(row[6], (0, 1))

    def test_python_orbits_against_integer_iteration(self):
        for m in (1, 2, 3, 4, 7, 8, 13, 16, 32, 65):
            for steps in (0, 1, 2, 7, 31, 97):
                with self.subTest(m=m, steps=steps):
                    value, bits, ledger = integer_orbit(m, steps)
                    result = probe.simulate_digits(m, steps)
                    self.assertEqual(result["digits"], ordinary_digits(value))
                    self.assertEqual(result["bits"], bits)
                    self.assertEqual(result["ledger"], ledger)

    def test_integer_replay_rejects_trace_and_endpoint_corruption(self):
        m, steps = 160, 47
        value, bits, _ = integer_orbit(m, steps)
        final = bytes(digit + 48 for digit in ordinary_digits(value))
        self.assertGreater(len(final), 96)  # Several complete 32-digit chunks.
        probe.check_integer_replay(m, bits, final)
        probe.check_integer_replay(1, [], b"2")
        for index in (0, steps // 2, steps - 1):
            altered = bits.copy()
            altered[index] ^= 1
            with self.subTest(trace_index=index), self.assertRaises(AssertionError):
                probe.check_integer_replay(m, altered, final)
        for index in (0, 31, 32, 63, 64, len(final) - 1):
            altered = bytearray(final)
            altered[index] = 48 + (altered[index] - 48 + 1) % 3
            with self.subTest(digit_index=index), self.assertRaises(AssertionError):
                probe.check_integer_replay(m, bits, bytes(altered))
        # Preserve length, digit sum and every digit count, while changing
        # position: aggregate digit checks alone cannot detect this endpoint.
        i, j = next((i, j) for i in range(1, len(final))
                    for j in range(i + 1, len(final)) if final[i] != final[j])
        altered = bytearray(final)
        altered[i], altered[j] = altered[j], altered[i]
        self.assertEqual(sorted(altered), sorted(final))
        with self.assertRaises(AssertionError):
            probe.check_integer_replay(m, bits, bytes(altered))

    def test_carry_type_counts_and_two_odd_transition_certificate(self):
        for value in range(1, 1500):
            self.assertEqual(probe.carry_types(ordinary_digits(value)),
                             integer_type_counts(value))
        expected_drifts = [(0, 0, -2, 1, 0, 1), (0, 0, 2, -1, 0, -1)]
        drifts = []
        for value, expected in zip((51, 403), expected_drifts):
            self.assertEqual(value % 2, 1)
            before = probe.carry_types(ordinary_digits(value))
            after = probe.carry_types(ordinary_digits(integer_step(value)))
            drift = tuple(a - b for a, b in zip(before, after))
            self.assertEqual(drift, expected)
            drifts.append(drift)
        self.assertEqual(tuple(a + b for a, b in zip(*drifts)), (0,) * 6)
        # At rho=306/589 the cancelled inequalities still demand 566<=0.
        self.assertEqual(sum(589 * (value % 2) - 306 for value in (51, 403)), 566)

    def test_clock_is_exact_integer_floor(self):
        for steps in (0, 1, 2, 7, 31, 120, 1000):
            expected = []
            for r in range(steps + 1):
                k = 0
                while 3 ** (k + 1) <= 2**r:
                    k += 1
                expected.append(k)
            self.assertEqual(probe.exact_clock(steps), expected)

    def test_length_lemma_only_in_its_proved_window(self):
        for m in range(1, 50):
            value, odd_count, r = 3**m - 1, 0, 0
            while 4**r < 3**m:
                k = 0
                while 3 ** (k + 1) <= 2**r:
                    k += 1
                self.assertEqual(len(ordinary_digits(value)), m + odd_count - k)
                odd_count += value % 2
                value = integer_step(value)
                r += 1
        # The window is a substantive hypothesis, not a universal formula.
        value, bits, _ = integer_orbit(1, 8)
        self.assertNotEqual(len(ordinary_digits(value)), 1 + sum(bits) - 5)

    def test_first_seam_padded_scans_and_modular_bits_agree(self):
        for v in range(0, 10):
            r, m = v + 3, 2 ** (v + 1)
            quotient, remainder = divmod(3**m - 1, 2**r)
            self.assertEqual(remainder, 0)
            digits = ordinary_digits(quotient)
            padded = [0] * (m - len(digits)) + digits
            c0, c1 = sum(prefix_carries(padded, 0)), sum(prefix_carries(padded, 1))
            bit_sum = sum(1 - 2 * ((pow(3, i, 2 ** (r + 1)) >> r) & 1)
                          for i in range(1, m + 1))
            result = probe.first_seam(v)
            self.assertEqual((result["v"], result["r"], result["m"]), (v, r, m))
            self.assertEqual(result["carry_difference"], c1 - c0)
            self.assertEqual(result["carry_difference"], bit_sum)
            self.assertEqual(result["dyadic_bound_squared_numerator"], m * (r*r - 1)**2)
            self.assertEqual(result["dyadic_bound_squared_denominator"], 2)
            self.assertEqual(result["bound_holds"], 2 * bit_sum**2 <= m * (r*r - 1)**2)
            self.assertTrue(result["bound_holds"])

    def test_first_seam_half_period_and_bound_threshold(self):
        for r in range(3, 12):
            m, q = 2 ** (r - 2), 2 ** (r + 1)
            self.assertEqual(pow(3, m, q), 1 + q // 2)
            self.assertEqual(pow(3, 2 * m, q), 1)
            for i in range(2 * m):
                a, b = pow(3, i, q), pow(3, i + m, q)
                self.assertEqual((a >> r) ^ (b >> r), 1)
        self.assertGreater((17**2 - 1)**2, 2 * 2**(17 - 2))
        self.assertLess((18**2 - 1)**2, 2 * 2**(18 - 2))


class TernaryCEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = tempfile.TemporaryDirectory(prefix="ternary-test-")
        cls.addClassCleanup(cls.work.cleanup)
        if os.environ.get("TERNARY_ENGINE"):
            cls.engine = Path(os.environ["TERNARY_ENGINE"]).resolve()
        else:
            compiler = shutil.which("clang") or shutil.which("cc")
            if compiler is None:
                raise RuntimeError("A C compiler or TERNARY_ENGINE is required")
            cls.engine = Path(cls.work.name) / "ternary-engine"
            env = os.environ.copy()
            if sys.platform == "darwin":
                env.setdefault("DEVELOPER_DIR", "/Library/Developer/CommandLineTools")
            subprocess.run([compiler, "-std=c11", "-O2", "-Wall", "-Wextra", "-Wpedantic",
                            str(HERE / "ternary_engine.c"), "-o", str(cls.engine)],
                           check=True, capture_output=True, text=True, env=env)

    def test_c_orbits_trace_endpoints_ledger_and_aggregates(self):
        for m, steps in itertools.product((1, 2, 3, 7, 16, 33, 64), (0, 1, 7, 8, 9, 73)):
            with self.subTest(m=m, steps=steps):
                trace = Path(self.work.name) / "trace.bin"
                digits_file = Path(self.work.name) / "digits.txt"
                ledger_file = Path(self.work.name) / "ledger.json"
                run = subprocess.run([str(self.engine), "--m", str(m), "--steps", str(steps),
                                      "--trace", str(trace), "--digits", str(digits_file),
                                      "--ledger", str(ledger_file)],
                                     check=True, capture_output=True, text=True)
                data = json.loads(run.stdout)
                value, bits, ledger = integer_orbit(m, steps)
                final = ordinary_digits(value)
                packed = bytearray((steps + 7) // 8)
                for i, bit in enumerate(bits):
                    packed[i // 8] |= bit << (i % 8)
                self.assertEqual(trace.read_bytes(), bytes(packed))
                self.assertEqual(digits_file.read_text(), "".join(map(str, final)))
                self.assertEqual(json.loads(ledger_file.read_text()), ledger)
                expected = {
                    "m": m, "steps": steps, "odd_steps": sum(bits),
                    "initial_length": m, "final_length": len(final),
                    "initial_digit_sum": 2*m, "final_digit_sum": sum(final),
                    "initial_count_ones": 0, "final_count_ones": final.count(1),
                    "final_digit_counts": [final.count(d) for d in range(3)],
                    "total_leading_digits_removed": sum(row[6] for row in ledger),
                    "total_carry_ones": sum(row[5] for row in ledger),
                    "total_scanned_digits": sum(row[1] + row[0] for row in ledger),
                    "minimum_step_carry_ones": min((row[5] for row in ledger), default=0),
                    "maximum_step_carry_ones": max((row[5] for row in ledger), default=0),
                    "total_state_digit_sum_before": sum(row[3] for row in ledger),
                    "total_state_digit_sum_after": sum(row[4] for row in ledger),
                }
                for key, expected_value in expected.items():
                    self.assertEqual(data[key], expected_value, key)

    def test_c_rejects_invalid_options_before_allocation(self):
        invalid = [[], ["--m", "1"], ["--m", "0", "--steps", "0"],
                   ["--m", "-1", "--steps", "0"], ["--m", "+1", "--steps", "0"],
                   ["--m", "1.0", "--steps", "0"], ["--m", "1", "--steps", "-1"],
                   ["--m", "1", "--steps", "0", "--m", "2"],
                   ["--m", "1", "--steps", "0", "--steps", "0"],
                   ["--m", "1", "--steps", "0", "--unknown", "x"],
                   ["--m", str(2**64), "--steps", "0"],
                   ["--m", str(2**64 - 1), "--steps", "1"],
                   ["--m", "1", "--steps", str(2**63)]]
        for args in invalid:
            with self.subTest(args=args):
                run = subprocess.run([str(self.engine)] + args, capture_output=True, text=True)
                self.assertEqual(run.returncode, 2)
                self.assertTrue(run.stderr)
                self.assertFalse(run.stdout)


if __name__ == "__main__":
    unittest.main()
