#!/usr/bin/env python3
"""Exact finite checks for carry propagation at the original ternary seam.

The seam is an internal statistic of one padded upper state. It is not the
Collatz doubling error E or Delta. No new tower level is certified here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PREVIOUS = ROOT / 'notes/post_v6_ternary_2026-09-25'
spec = importlib.util.spec_from_file_location('frozen_ternary_probe', PREVIOUS / 'ternary_probe.py')
assert spec and spec.loader
ternary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ternary)


def quotient_word(width: int, r: int) -> list[int]:
    """Long division of the word 2^width by 2^r, preserving padding."""
    if width < 1 or r < 1:
        raise ValueError('positive width and divisor exponent required')
    result, carry, divisor = [], 0, 1 << r
    for _ in range(width):
        digit, carry = divmod(3 * carry + 2, divisor)
        result.append(digit)
    if carry:
        raise ValueError('the initial quotient is not integral')
    return result


def canonical(digits: list[int]) -> list[int]:
    start = 0
    while start + 1 < len(digits) and digits[start] == 0:
        start += 1
    return digits[start:]


def decode_chunks(digits: list[int]) -> int:
    value = 0
    for start in range(0, len(digits), 32):
        chunk = digits[start:start + 32]
        value = value * pow(3, len(chunk)) + int(''.join(map(str, chunk)), 3)
    return value


def power_model(width: int, s: int) -> tuple[list[int], list[int]]:
    """Digits of floor(3^width/2^s) and its prefix parity model."""
    if width < 0 or s < 1:
        raise ValueError('nonnegative width and positive s required')
    digits, carries, residue, divisor = [], [], 1, 1 << s
    for _ in range(width):
        digits.append((3 * (residue & (divisor - 1))) >> s)
        residue = (3 * residue) & (2 * divisor - 1)
        carries.append(residue >> s)
    return digits, carries


def carry_scan(digits: list[int]) -> list[int]:
    carry, result = 0, []
    for digit in digits:
        carry = (carry + digit) % 2
        result.append(carry)
    return result


def affine_constant(bits: list[int]) -> tuple[int, int]:
    c, j = 0, 0
    for i, bit in enumerate(bits):
        if bit not in (0, 1):
            raise ValueError('binary word required')
        if bit:
            c = 3 * c + (1 << i)
            j += 1
    return c, j


def explicit_bound(r: int, t: int) -> dict:
    if r < 3 or t < 0:
        raise ValueError('r>=3 and t>=0 required')
    m, s = 1 << (r - 2), r + t
    numerator = m * (1 << t) * (r - 1)**2 * (s + 1)**2
    return {'model_bound_squared_numerator': numerator,
            'model_bound_squared_denominator': 2,
            'uniform_edge_error': 0,
            'model_bound_below_m': numerator < 2 * m * m,
            'actual_bound_below_m': numerator < 2 * m * m}


def max_nontrivial_depth(r: int) -> int:
    t = 0
    while explicit_bound(r, t)['actual_bound_below_m']:
        t += 1
    return t - 1


def checkpoint_state(digits: list[int], integer: int, base_width: int,
                     r: int, t: int, bits: list[int], model_digits: list[int],
                     model_carries: list[int]) -> tuple[dict, list[int]]:
    c, j = affine_constant(bits)
    s, width = r + t, base_width + j
    b = (1 << r) * c - pow(3, j)
    assert len(bits) == t
    assert (1 << t) * integer == pow(3, j) * ((pow(3, base_width) - 1) >> r) + c
    assert (1 << s) * integer == pow(3, width) + b
    assert pow(3, j) - (1 << j) <= c <= (1 << (t - j)) * (pow(3, j) - (1 << j))
    assert abs(b) < pow(3, j) * (1 << (s - j))
    assert decode_chunks(digits) == integer
    padded = [0] * (width - len(digits)) + digits
    assert len(padded) == width
    assert integer // pow(3, j) == ((pow(3, base_width) - 1) >> s)
    assert padded[:base_width] == model_digits[:base_width]
    actual_carries = carry_scan(padded)
    assert actual_carries[:base_width] == model_carries[:base_width]
    tail_value = integer % pow(3, j)
    residue = ((pow(3, base_width) - 1) >> r) & ((1 << t) - 1)
    residual_value, residual_bits = residue, []
    for _ in range(t):
        bit = residual_value & 1
        residual_bits.append(bit)
        residual_value = (3 * residual_value + 1) // 2 if bit else residual_value // 2
    assert residual_bits == bits and residual_value == tail_value
    assert 0 <= tail_value < pow(3, j)
    first_change = next((i + 1 for i, (a, b0) in enumerate(zip(padded, model_digits)) if a != b0), None)
    return ({'steps': t, 'odd_steps': j, 'parity_word': ''.join(map(str, bits)),
             'affine_C': c, 'boundary_B': b, 'padded_width': width,
             'canonical_length': len(digits),
             'original_prefix_length': base_width,
             'first_changed_digit_one_based': first_change,
             'changed_original_carries': 0,
             'append_tail_digits': ''.join(map(str, padded[base_width:])),
             'append_tail_value': tail_value,
             'low_binary_residue': residue,
             'append_tail_carry_ones': sum(actual_carries[base_width:]),
             'carry_ones_total': sum(actual_carries),
             'quotient_identity_verified': True,
             'full_ternary_sha256': hashlib.sha256(bytes(padded)).hexdigest(),
             'integer_endpoint_verified': True,
             'all_original_digits_and_carries_verified': True}, actual_carries)


def replay_level(v: int) -> dict:
    if v < 0:
        raise ValueError('v must be nonnegative')
    r, m = v + 3, 1 << (v + 1)
    checkpoints = sorted({0, 1, 2, 4, 8, 16, 32, r, 2 * r})
    words = [canonical(quotient_word(width, r)) for width in (m, 2 * m)]
    integers = [(pow(3, width) - 1) >> r for width in (m, 2 * m)]
    bits = [[], []]
    records = []
    for t in range(max(checkpoints) + 1):
        if t in checkpoints:
            model_digits, model_carries = power_model(2 * m + t, r + t)
            lower, _ = checkpoint_state(words[0], integers[0], m, r, t, bits[0], model_digits, model_carries)
            upper, upper_carries = checkpoint_state(words[1], integers[1], 2 * m, r, t, bits[1], model_digits, model_carries)
            model_seam = sum(model_carries[m:2*m]) - sum(model_carries[:m])
            actual_seam = sum(upper_carries[m:2*m]) - sum(upper_carries[:m])
            signed_error = actual_seam - model_seam
            bound = explicit_bound(r, t)
            assert signed_error == 0
            assert 2 * model_seam**2 <= bound['model_bound_squared_numerator']
            assert 2 * actual_seam**2 <= bound['model_bound_squared_numerator']
            paired_carries = upper['carry_ones_total'] - 2 * lower['carry_ones_total']
            tail_difference = upper['append_tail_carry_ones'] - 2 * lower['append_tail_carry_ones']
            tail_bound = max(upper['odd_steps'], 2 * lower['odd_steps'])
            assert paired_carries == model_seam + tail_difference
            assert abs(tail_difference) <= tail_bound <= 2 * t
            records.append({'t': t, 'lower': lower, 'upper': upper,
                            'model_seam_difference': model_seam,
                            'actual_seam_difference': actual_seam,
                            'signed_boundary_error': signed_error,
                            'paired_total_carry_difference': paired_carries,
                            'append_tail_carry_difference': tail_difference,
                            'append_tail_difference_bound': tail_bound,
                            'paired_carry_identity_verified': True,
                            **bound, 'model_and_actual_bounds_verified': True})
        if t == max(checkpoints):
            break
        for side in (0, 1):
            odd = integers[side] & 1
            words[side], ledger = ternary.step_digits(words[side])
            assert ledger[0] == odd
            integers[side] = (3 * integers[side] + 1) // 2 if odd else integers[side] // 2
            bits[side].append(odd)
    return {'v': v, 'r': r, 'm': m, 'checkpoints': records}


def threshold_table() -> list[dict]:
    result = []
    for t in (0, 1, 2, 4, 8, 16, 32, 64):
        r = 3
        while not explicit_bound(r, t)['actual_bound_below_m']:
            r += 1
        result.append({'t': t, 'first_r_for_bound_below_m': r, 'first_v': r - 3,
                       'scope': 'Evaluation of the proved bound, not an orbit computation.'})
    return result


def raw_sum_obstruction(r: int) -> dict:
    """A deterministic obstruction for one uncentred window, NOT for the seam."""
    m, t = 1 << (r - 2), 1 << (r - 2)
    s = r + t
    # These powers 3^i are strictly below 2^s: all their top bits vanish.
    i, power = 0, 1
    while i < m and 3 * power < (1 << s):
        power *= 3
        i += 1
    _, carries = power_model(m, s)
    raw_sum = m - 2 * sum(carries)
    lower_bound = 2 * i - m
    assert raw_sum >= lower_bound
    return {'r': r, 'm': m, 't': t, 'initial_zero_top_bits': i,
            'single_window_raw_sum': raw_sum,
            'rigorous_lower_bound': lower_bound,
            'scope': 'S(0,m) only; no lower bound on the two-window seam or on Delta.'}


def produce(max_v: int = 16) -> dict:
    if not 5 <= max_v <= 18:
        raise ValueError('max-v must be between 5 and 18')
    levels = [replay_level(v) for v in range(5, max_v + 1)]
    old = json.loads((PREVIOUS / 'ternary_results.json').read_text())
    old_seams = {row['v']: row['carry_difference'] for row in old['first_seams']}
    for row in levels:
        assert row['checkpoints'][0]['actual_seam_difference'] == old_seams[row['v']]
    paths = [PREVIOUS / 'ternary_probe.py', PREVIOUS / 'ternary_results.json']
    return {'schema': 1,
            'scope': 'Exact original-prefix and append-tail decomposition; bounds for an internal padded seam; no bound on E or Delta.',
            'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            'levels': levels,
            'thresholds_for_nontrivial_actual_bound': threshold_table(),
            'depth_limits_by_r': [{'r': r, 'v': r - 3,
                                   'model_and_actual_max_depth': max_nontrivial_depth(r)}
                                  for r in (18, 19, 20, 22, 25, 32, 40, 50, 64, 100)],
            'raw_single_window_obstructions': [raw_sum_obstruction(r) for r in (8, 10, 12, 14)],
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'uniform_doubling_error_bound': 'Open',
            'mathematical_priority': 'Not established',
            'literature_asymptotic_bound': 'See LITERATURE_IT.md: absolute constants not made explicit; not numerically certified here.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-v', type=int, default=16)
    args = parser.parse_args()
    result = produce(args.max_v)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'levels': len(result['levels']),
                      'state_checkpoints': 2 * sum(len(row['checkpoints']) for row in result['levels']),
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
