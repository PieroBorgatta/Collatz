#!/usr/bin/env python3
"""Independent arithmetic checks for the bounded binary-carry experiment."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import binary_carry_probe as probe

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent


def integer_word(n: int, steps: int) -> int:
    word = 0
    for t in range(steps):
        if n % 2:
            word += 2**t
            n = (3*n+1)//2
        else:
            n //= 2
    return word


def independent_columns(p: int, columns: int) -> dict:
    """Plain nested multiplication, with no production-code dependencies."""
    coefficients = [0]*columns
    for i in range(columns):
        for j in range(columns-i):
            coefficients[i+j] += ((p//2**i) % 2)*((p//2**j) % 2)
    carries = [0]
    bits = []
    for coefficient in coefficients:
        q, bit = divmod(coefficient+carries[-1], 2)
        bits.append(bit)
        carries.append(q)
    return {'bits': bits, 'coefficients': coefficients, 'carries': carries}


def packed_columns(p: int, columns: int) -> dict:
    """Recover convolution via one integer product in a carry-free radix."""
    width = max(1, (columns+1).bit_length())
    mask = (1 << width)-1
    polynomial = sum(((p >> i) & 1) << (i*width) for i in range(columns))
    square = polynomial*polynomial
    coefficients = [(square >> (i*width)) & mask for i in range(columns)]
    bits, carries = [], [0]
    for coefficient in coefficients:
        total = coefficient+carries[-1]
        bits.append(total % 2)
        carries.append(total//2)
    return {'bits': bits, 'coefficients': coefficients, 'carries': carries}


def actual_tower(v: int) -> int:
    return (3**(2**(v+1))-1)//2**(v+3)


def actual_horizon(v: int) -> int:
    return (589*2**v+611)//612


def valuation_two(n: int) -> int:
    return (abs(n) & -abs(n)).bit_length()-1


def boundary_carry(p: int, n: int) -> int:
    """Truncated convolution sum using integer prefixes, without column steps."""
    positions = [i for i in range(n) if (p >> i) & 1]
    return sum((p % 2**(n-i))*2**i for i in positions)//2**n


def frozen(name: str, date: str, filename: str) -> dict:
    return json.loads((NOTES/f'post_v6_{name}_{date}'/filename).read_text())


class BinaryCarryTests(unittest.TestCase):
    def test_columns_against_nested_products_and_integer_square(self):
        for p in range(256):
            columns = 17
            observed = probe.squaring_columns(p, columns)
            self.assertEqual(observed, independent_columns(p, columns))
            self.assertEqual(sum(b << i for i, b in enumerate(observed['bits'])),
                             (p*p) % 2**columns)

    def test_packed_oracle_has_no_coefficient_radix_carries(self):
        for columns in range(17):
            for p in (0, 1, 3, 9, 105, 153, 255, 65535):
                self.assertEqual(packed_columns(p, columns),
                                 independent_columns(p, columns))
                self.assertEqual(probe.squaring_columns(p, columns),
                                 packed_columns(p, columns))

    def test_streaming_cascade_against_direct_modular_powers(self):
        for depth in range(7):
            for columns in (0, 1, 7, 19, 64):
                result = probe.streaming_power_rows(depth, columns)
                self.assertEqual(len(result['bits']), depth+1)
                self.assertEqual(len(result['carries']), depth)
                self.assertEqual(len(result['coefficients']), depth)
                for stage in range(depth+1):
                    expected = pow(3, 2**stage, 2**columns)
                    self.assertEqual(result['bits'][stage],
                                     [(expected >> i) & 1 for i in range(columns)])
                    if stage < depth:
                        oracle = packed_columns(expected, columns)
                        self.assertEqual(result['carries'][stage], oracle['carries'])
                        self.assertEqual(result['coefficients'][stage], oracle['coefficients'])

    def test_protocol_generator_depths_and_full_requested_prefixes(self):
        for v in range(5, 10):
            depth, columns = v+2, actual_horizon(v+1)+v+4
            generated = probe.streaming_power_rows(depth, columns)
            for stage, bits in enumerate(generated['bits']):
                actual = pow(3, 2**stage, 2**columns)
                self.assertEqual(bits, [(actual >> i)&1 for i in range(columns)])
                if stage < depth:
                    oracle = packed_columns(actual, columns)
                    self.assertEqual(generated['bits'][stage+1], oracle['bits'])
                    self.assertEqual(generated['carries'][stage], oracle['carries'])
                    self.assertEqual(generated['coefficients'][stage], oracle['coefficients'])
            for level in (v, v+1):
                steps, shift = actual_horizon(level), level+3
                inputs = generated['bits'][level+1][shift:shift+steps]
                self.assertEqual(len(inputs), steps)
                self.assertEqual(probe.tail_word(inputs), integer_word(actual_tower(level), steps))

    def test_square_boundary_carry_is_prefix_function(self):
        for r in range(3, 7):
            for precision in range(1, 7):
                n = r+precision
                for x in range(1, 2**precision, 2):
                    p = 1+2**r*x
                    other = p+2**n
                    a = probe.squaring_columns(p, n+1)
                    b = probe.squaring_columns(other, n+1)
                    self.assertEqual(a['carries'][:n+1], b['carries'][:n+1])
                    self.assertEqual(a['bits'], b['bits'])
                    self.assertEqual(b['carries'][n+1], a['carries'][n+1]+1)
                    truncated = sum(((p >> i)&1)*((p >> j)&1)*2**(i+j)
                                    for i in range(n) for j in range(n-i))
                    self.assertEqual(a['carries'][n], truncated//2**n)

    def test_same_next_input_does_not_close_four_bit_memory(self):
        self.assertEqual(probe.projected_state(105, 3, 12, 4),
                         probe.projected_state(153, 3, 12, 4))
        self.assertEqual(probe.projected_state(105, 3, 12, 4), (1, 9, 0, 11, 0))
        self.assertEqual((105**2 >> 12)&1, 0)
        self.assertEqual((153**2 >> 12)&1, 1)
        a, b = independent_columns(105, 13), independent_columns(153, 13)
        self.assertEqual((a['carries'][13], b['carries'][13]), (1, 0))

    def test_analytic_collisions_preserve_binade_and_high_bits(self):
        for r in range(3, 8):
            for w in (1, 2, 4, 8, 16):
                row = probe.analytic_collision(r, w)
                n, p, other = row['n'], row['P'], row['P_other']
                self.assertEqual(p.bit_length(), other.bit_length())
                self.assertEqual(p >> n, other >> n)
                self.assertEqual(p % 2**(r+1), 1+2**r)
                self.assertEqual(other % 2**(r+1), 1+2**r)
                self.assertEqual(probe.projected_state(p, r, n, w),
                                 probe.projected_state(other, r, n, w))
                self.assertEqual(tuple(row['state']), probe.projected_state(p, r, n, w))
                self.assertEqual(row['output'], (p*p >> n)&1)
                self.assertEqual(row['other_output'], (other*other >> n)&1)
                self.assertNotEqual(row['output'], row['other_output'])
                self.assertEqual(packed_columns(p, n+1),
                                 probe.squaring_columns(p, n+1))
                self.assertEqual(packed_columns(other, n+1),
                                 probe.squaring_columns(other, n+1))

    def test_tower_horizons_and_shortcut_hashes_match_frozen_data(self):
        archive = frozen('margin', '2026-09-25', 'margin_results.json')
        baseline = {row['v']: row for row in archive['levels']}
        for v in range(11):
            self.assertEqual(probe.tower(v), actual_tower(v))
            self.assertEqual(probe.horizon(v), actual_horizon(v))
            word = integer_word(actual_tower(v), actual_horizon(v))
            self.assertEqual(probe.direct_word(actual_tower(v), actual_horizon(v)), word)
            if v >= 5:
                packed = word.to_bytes((actual_horizon(v)+7)//8, 'little')
                self.assertEqual(word.bit_count(), baseline[v]['odd_steps'])
                self.assertEqual(hashlib.sha256(packed).hexdigest(),
                                 baseline[v]['parity_trace_sha256'])

    def test_tail_transducer_on_all_binary_inputs_through_nine_steps(self):
        for steps in range(10):
            for source in range(2**steps):
                inputs = [(source >> i)&1 for i in range(steps)]
                self.assertEqual(probe.tail_word(inputs), integer_word(source, steps))

    def test_exhaustive_projection_finds_first_independently_valid_collision(self):
        expected, input_rows, projected_rows = [], 0, 0
        for r in range(3, 7):
            for n in range(r+2, 13):
                inputs = list(range(1+2**r, 2**n, 2**(r+1)))
                input_rows += len(inputs)
                for w in range(1, min(4, n-r-1)+1):
                    seen, first = {}, None
                    for p in inputs:
                        projected_rows += 1
                        state = (boundary_carry(p, n), p % 2**(r+1),
                                 (p//2**(n-w)) % 2**w,
                                 (p*p//2**(n-w)) % 2**w, 0)
                        output = (p*p//2**n) % 2
                        if state in seen and seen[state][1] != output and first is None:
                            first = {'r': r, 'n': n, 'w': w, 'P': seen[state][0],
                                     'P_other': p, 'state': state,
                                     'output': seen[state][1], 'other_output': output}
                        if state not in seen:
                            seen[state] = p, output
                    expected.append({'r': r, 'n': n, 'w': w,
                                     'distinct_states': len(seen), 'first_collision': first})
        result = probe.exhaustive_collisions()
        self.assertEqual(result['input_rows'], input_rows)
        self.assertEqual(result['projected_rows'], projected_rows)
        self.assertEqual(result['cases'], expected)
        self.assertEqual(result['cases_with_output_collision'],
                         sum(row['first_collision'] is not None for row in expected))

    def test_future_carry_filter_full_distributions_by_integer_boundary_oracle(self):
        for v in range(5):
            q, H, K, r = actual_tower(v), actual_horizon(v), actual_horizon(v+1), v+3
            n = r+K
            target = boundary_carry(1+2**r*q, n)
            lower = integer_word(q, H).bit_count()
            before, after, carry_counts = Counter(), Counter(), Counter()
            maxima = {}
            prefix, high = q % 2**H, (q//2**K)*2**K
            for suffix in range(2**(K-H)):
                x = high+suffix*2**H+prefix
                c = boundary_carry(1+2**r*x, n)
                delta = integer_word(x+2**(v+2)*x*x, K).bit_count()-2*lower
                before[delta] += 1
                carry_counts[c] += 1
                maxima[c] = max(maxima.get(c, delta), delta)
                if c == target:
                    after[delta] += 1
            result = probe.future_carry_fiber(v)
            self.assertEqual(result['delta_distribution_before'], dict(before))
            self.assertEqual(result['delta_distribution_after'], dict(after))
            self.assertEqual(result['carry_counts'], dict(carry_counts))
            self.assertEqual(result['maximum_delta_by_carry'], maxima)
            self.assertEqual(result['candidates'], sum(before.values()))
            self.assertEqual(result['retained'], sum(after.values()))
            self.assertEqual(result['maximum_before'], max(before))
            self.assertEqual(result['maximum_after'], max(after))
            self.assertEqual(result['actual_carry'], target)
            self.assertEqual(result['carry_column'], n)
            for key in ('first_maximum_source', 'first_retained_maximum_source'):
                x = result[key]
                self.assertEqual(x % 2**H, prefix)
                self.assertEqual(x//2**K, high//2**K)
                delta = integer_word(x+2**(v+2)*x*x, K).bit_count()-2*lower
                self.assertEqual(delta, result['maximum_before' if key == 'first_maximum_source' else 'maximum_after'])
                if key == 'first_retained_maximum_source':
                    self.assertEqual(boundary_carry(1+2**r*x, n), target)

    def test_renewal_witnesses_keep_carries_but_violate_prefix_budget(self):
        archive = frozen('renewal', '2026-09-26', 'renewal_results.json')
        for row in archive['threshold_failure_witnesses']:
            v, x = row['v'], int(row['X_hex'], 16)
            q, r = actual_tower(v), v+3
            M = valuation_two(x-q)
            self.assertGreaterEqual(M, row['precision_M'])
            n = M+r
            p, actual_p = 1+2**r*x, 1+2**r*q
            a, b = packed_columns(p, n+1), packed_columns(actual_p, n+1)
            self.assertEqual(a['carries'][:n+1], b['carries'][:n+1])
            self.assertEqual(a['bits'], b['bits'])
            self.assertNotEqual(a['carries'][n+1], b['carries'][n+1])
            self.assertEqual(probe.squaring_columns(p, n+1), a)
            self.assertEqual(probe.squaring_columns(actual_p, n+1), b)
            y = x+2**(v+2)*x*x
            self.assertEqual(y, int(row['Y_hex'], 16))
            H, K = actual_horizon(v), actual_horizon(v+1)
            low, upper = integer_word(x, H), integer_word(y, K)
            self.assertEqual(low, integer_word(q, H))
            self.assertEqual(upper.bit_count()-2*low.bit_count(), row['target_g']+1)
            self.assertEqual(upper >> row['precision_M'],
                             2**(K-row['precision_M'])-1)
            reported = probe.witness_carries(v, x, 'test_renewal', K)
            future_x = boundary_carry(p, r+K)
            future_actual = boundary_carry(actual_p, r+K)
            self.assertEqual(reported['future_witness_carry'], future_x)
            self.assertEqual(reported['future_actual_carry'], future_actual)
            self.assertEqual(reported['retained_by_future_carry_filter'], future_x == future_actual)

    def test_seven_ancestor_witness_is_independently_reconstructed(self):
        row = frozen('seven_ancestors', '2026-09-26', 'seven_results.json')['search']['witness']
        root, a = row['ancestor'], 1+128*row['ancestor']
        self.assertEqual(root % 2, 1)
        self.assertEqual((root-actual_tower(4)) % 3**8, 0)
        values = {}
        for level in row['levels']:
            v = level['v']
            x = (a**(2**(v-4))-1)//2**(v+3)
            self.assertEqual(x, int(level['value_hex'], 16))
            values[v] = x
        for v, key in ((11, 'lower'), (12, 'upper')):
            H = actual_horizon(v)
            word = integer_word(values[v], H)
            self.assertEqual(word.bit_count(), row[key]['odd_steps'])
            self.assertEqual(word, int.from_bytes(bytes.fromhex(row[key]['packed_lsb_first_hex']), 'little'))
            self.assertEqual(2**(v-1)-word.bit_count(), row[key+'_margin'])
        self.assertEqual(row['upper_margin'], 2*row['lower_margin']-86)
        v, x = 11, values[11]
        q, r = actual_tower(v), v+3
        n = valuation_two(x-q)+r
        observed, actual = independent_columns(1+2**r*x, n+1), independent_columns(1+2**r*q, n+1)
        self.assertEqual(observed['carries'][:n+1], actual['carries'][:n+1])
        self.assertEqual(observed['bits'], actual['bits'])
        self.assertNotEqual(observed['carries'][n+1], actual['carries'][n+1])
        K = actual_horizon(v+1)
        record = probe.witness_carries(v, x, 'test_seven', K)
        future_x = boundary_carry(1+2**r*x, r+K)
        future_actual = boundary_carry(1+2**r*q, r+K)
        self.assertEqual(record['future_witness_carry'], future_x)
        self.assertEqual(record['future_actual_carry'], future_actual)
        self.assertEqual(record['retained_by_future_carry_filter'], future_x == future_actual)

    def test_signed_weighted_budget_retains_endpoint_and_anchor(self):
        archive = frozen('margin', '2026-09-25', 'margin_results.json')
        levels = {row['v']: row for row in archive['levels']}
        anchor = 16
        cumulative = Fraction(0)
        result = probe.historical_signed_budget(levels)
        self.assertEqual(result['anchor'], anchor)
        self.assertEqual(result['anchor_margin'], levels[anchor]['margin'])
        for v in range(anchor, 24):
            delta = levels[v+1]['odd_steps']-2*levels[v]['odd_steps']
            cumulative += Fraction(delta, 2**(v+1-anchor))
            endpoint = Fraction(levels[v+1]['margin'], 2**(v+1-anchor))
            self.assertEqual(Fraction(levels[anchor]['margin'])-cumulative, endpoint)
            row = result['partials'][v-anchor]
            self.assertEqual(row['through_pair_v'], v)
            self.assertEqual(row['delta'], delta)
            self.assertEqual(Fraction(**row['signed_partial_loss']), cumulative)
            self.assertEqual(Fraction(**row['scaled_margin']), endpoint)
        # A finite equality cannot certify any unobserved terms after level 24.
        self.assertEqual(cumulative, Fraction(levels[anchor]['margin'])-
                         Fraction(levels[24]['margin'], 2**(24-anchor)))

    def test_frozen_input_hash_tampering_is_rejected(self):
        name = next(iter(probe.PINNED_INPUTS))
        with patch.dict(probe.PINNED_INPUTS, {name: '0'*64}):
            with self.assertRaisesRegex(ValueError, 'changed frozen input'):
                probe.load_inputs()


if __name__ == '__main__':
    unittest.main()
