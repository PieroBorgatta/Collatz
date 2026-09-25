#!/usr/bin/env python3
"""Exact tail transducer and unequal-horizon carry accounting.

Three representations are checked: tail integers, padded ternary tails,
and direct integer Collatz orbits. Finite identities are not a density bound.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def tail_step(j: int, z: int, h: int) -> tuple[int, int, int]:
    if j < 0 or h not in (0, 1):
        raise ValueError('nonnegative length and a binary input required')
    power = 3**j
    if not 0 <= z < power:
        raise ValueError('tail outside its padded range')
    p = (h + z) & 1
    if p:
        return j + 1, (3 * (power * h + z) + 1) // 2, p
    return j, (power * h + z) // 2, p


def digit_step(digits: list[int], h: int) -> tuple[list[int], int, int]:
    """MSB-first division with incoming h; append quotient digit 2 if odd.

    A counts outgoing one-carries on the original tail, before the append.
    Leading zeroes are significant. This algorithm does not use tail_step.
    """
    if h not in (0, 1):
        raise ValueError('binary input required')
    carry, ones, result = h, 0, []
    for digit in digits:
        if digit not in (0, 1, 2):
            raise ValueError('ternary digits required')
        q, carry = divmod(3 * carry + digit, 2)
        result.append(q)
        ones += carry
    p = carry
    if p:
        result.append(2)
    return result, p, ones


def decode(digits: list[int]) -> int:
    result = 0
    for start in range(0, len(digits), 32):
        chunk = digits[start:start + 32]
        result = result * 3**len(chunk) + int(''.join(map(str, chunk)), 3)
    return result


def packed(bits: list[int]) -> bytes:
    data = bytearray((len(bits) + 7) // 8)
    for i, bit in enumerate(bits):
        data[i // 8] |= bit << (i % 8)
    return bytes(data)


def block_predict(j: int, z_residue: int, inputs: list[int]) -> list[int]:
    """Predict k outputs using only z mod 2^k and the k future inputs.

    This consumes k bits of precision; it does NOT return a refreshed tail
    residue for another block. j is known at the beginning of the block.
    """
    k = len(inputs)
    if j < 0 or not 0 <= z_residue < (1 << k) or any(h not in (0, 1) for h in inputs):
        raise ValueError('valid length, residue and binary inputs required')
    source = sum(h << t for t, h in enumerate(inputs))
    state = (pow(3, j, 1 << k) * source + z_residue) & ((1 << k) - 1)
    result = []
    for t in range(k):
        p = state & 1
        result.append(p)
        state = ((3 * state + 1) // 2 if p else state // 2) & ((1 << (k-t-1)) - 1)
    return result


def replay(n: int, steps: int, checkpoints: tuple[int, ...] = ()) -> dict:
    if n < 0 or steps < 0 or any(t < 0 or t > steps for t in checkpoints):
        raise ValueError('nonnegative orbit and valid checkpoints required')
    j, z, power, full, head = 0, 0, 1, n, n
    digits, bits, records = [], [], []
    total_inputs, total_carries, interior_sums, digit_cells = 0, 0, 0, 0
    weighted_carries = 0
    ledger = hashlib.sha256()
    block_outputs: list[int] = []
    block_checks = 0
    for t in range(steps + 1):
        if t in checkpoints:
            records.append({'steps': t, 'odd_steps': j,
                            'tail_digit_sum': sum(digits),
                            'parity_sha256': hashlib.sha256(packed(bits)).hexdigest(),
                            'parity_without_first_step_sha256': hashlib.sha256(packed(bits[1:])).hexdigest()})
        if t == steps:
            break
        if t % 16 == 0:
            size = min(16, steps - t)
            block_outputs = block_predict(j, z & ((1 << size) - 1),
                                          [(head >> i) & 1 for i in range(size)])
            block_checks += 1
        h, old_sum, old_j = head & 1, sum(digits), j
        # Inline the recurrence with cached 3^j; public tail_step is also tested.
        p = (h + z) & 1
        next_z = (3 * (power * h + z) + 1) // 2 if p else (power * h + z) // 2
        next_digits, digit_p, a = digit_step(digits, h)
        next_sum = sum(next_digits)
        assert digit_p == p == (full & 1)
        assert p == block_outputs[t % 16]
        assert 2 * next_sum == old_sum + p + 3 * h + 2 * a
        j += p
        if p:
            power *= 3
        z, digits = next_z, next_digits
        head >>= 1
        full = (3 * full + 1) // 2 if p else full // 2
        assert 0 <= z < power and len(digits) == j
        assert full == power * head + z
        total_inputs += h
        total_carries += a
        weighted_carries += a << t
        digit_cells += old_j
        if t:
            interior_sums += old_sum
        bits.append(p)
        # Canonical JSON lines, with a trailing newline for every row.
        ledger.update((json.dumps([h, p, old_j, old_sum, a, next_sum],
                                  separators=(',', ':')) + '\n').encode())
    s_final = sum(digits)
    assert decode(digits) == z
    assert j == 2 * s_final + interior_sums - 3 * total_inputs - 2 * total_carries
    binary_parity = int.from_bytes(packed(bits), 'little')
    residue = n & ((1 << steps) - 1)
    assert binary_parity == (s_final << steps) - 3 * residue - 2 * weighted_carries
    c = (z << steps) - power * residue
    assert power - (1 << j) <= c <= (power - (1 << j)) << (steps - j)
    assert power * ((1 << steps) - residue - 1) + (1 << j) >= (1 << steps)
    return {'steps': steps, 'odd_steps': j,
            'terminal_tail_length': len(digits),
            'terminal_tail_digit_sum': s_final,
            'input_ones': total_inputs,
            'tail_digit_sum_interior': interior_sums,
            'tail_carry_ones_sum': total_carries,
            'tail_digit_cells_scanned': digit_cells,
            'finite_precision_blocks_checked': block_checks,
            'parity_sha256': hashlib.sha256(packed(bits)).hexdigest(),
            'terminal_tail_sha256': hashlib.sha256(bytes(digits)).hexdigest(),
            'ledger_sha256': ledger.hexdigest(),
            'identities_verified': True,
            'direct_integer_parity_at_every_step_verified': True,
            'weighted_telescope_verified': True,
            'sharp_normalized_bounds_verified': True,
            'input_only_lower_bound_verified': True,
            'checkpoints': records}


def horizon(v: int) -> int:
    return (589 * (1 << v) + 611) // 612


def paired_level(v: int, baseline: dict[int, dict]) -> dict:
    r, m, h = v + 3, 1 << (v + 1), horizon(v)
    lower_n = (3**m - 1) >> r
    upper_n = (3**(2*m) - 1) >> r  # 2 Q_(v+1), not Q_(v+1).
    upper_time, next_time = 2 * h + r, horizon(v + 1) + 1
    lower = replay(lower_n, h)
    upper = replay(upper_n, upper_time, (next_time,))
    j_next = upper['checkpoints'][0]['odd_steps']
    assert lower['odd_steps'] == baseline[v]['odd_steps']
    assert j_next == baseline[v + 1]['odd_steps']
    assert lower['parity_sha256'] == baseline[v]['parity_trace_sha256']
    assert upper['checkpoints'][0]['parity_without_first_step_sha256'] == baseline[v + 1]['parity_trace_sha256']
    delta = j_next - 2 * lower['odd_steps']
    actual_tail_odds = upper['odd_steps'] - j_next
    e = upper['odd_steps'] - 2 * lower['odd_steps']
    terms = {
        'terminal_digit_sum_term': 2 * upper['terminal_tail_digit_sum'] - 4 * lower['terminal_tail_digit_sum'],
        'interior_digit_sum_term': upper['tail_digit_sum_interior'] - 2 * lower['tail_digit_sum_interior'],
        'input_term': -3 * (upper['input_ones'] - 2 * lower['input_ones']),
        'carry_term': -2 * (upper['tail_carry_ones_sum'] - 2 * lower['tail_carry_ones_sum']),
    }
    assert sum(terms.values()) == e == delta + actual_tail_odds
    return {'v': v, 'r': r, 'm': m, 'lower_time': h, 'upper_time': upper_time,
            'next_Q_time': next_time - 1, 'upper_extra_steps': upper_time - next_time,
            'lower': lower, 'upper': upper, 'delta': delta,
            'upper_extra_odd_steps': actual_tail_odds, 'E': e,
            'unequal_horizon_terms': terms,
            'absolute_sum_of_terms': sum(abs(x) for x in terms.values()),
            'unequal_horizon_identity_verified': True,
            'frozen_margin_counts_match': True,
            'frozen_margin_complete_parity_hashes_match': True}


def memory_examples(max_j: int = 7) -> list[dict]:
    result = []
    for j in range(1, max_j + 1):
        modulus, states = 3**j, set()
        z = modulus - 1
        while z not in states:
            states.add(z)
            new_j, z, p = tail_step(j, z, z & 1)
            assert new_j == j and p == 0
        assert z == modulus - 1
        assert states == {x for x in range(modulus) if x % 3}
        k = (modulus - 1).bit_length()
        outputs = set()
        for z in states:
            state_j, state_z, word = j, z, 0
            for t in range(k):
                state_j, state_z, p = tail_step(state_j, state_z, 0)
                word |= p << t
            outputs.add(word)
        assert len(outputs) == len(states)
        result.append({'tail_length': j, 'reachable_states': len(states),
                       'common_time': j + len(states) - 1,
                       'zero_input_distinguishing_steps': k,
                       'distinct_output_words': len(outputs)})
    return result


def produce(max_v: int = 12) -> dict:
    if not 5 <= max_v <= 23:
        raise ValueError('supported historical comparison: 5<=max_v<=23')
    baseline_path = ROOT / 'notes/post_v6_margin_2026-09-25/margin_results.json'
    raw = json.loads(baseline_path.read_text())
    baseline = {row['v']: row for row in raw['levels']}
    rows = [paired_level(v, baseline) for v in range(5, max_v + 1)]
    ternary_path = ROOT / 'notes/post_v6_ternary_2026-09-25/ternary_results.json'
    previous_pairs = {row['v']: row for row in json.loads(ternary_path.read_text())['pairs']}
    for row in rows:
        if row['v'] in previous_pairs:
            old = previous_pairs[row['v']]
            assert (row['delta'], row['E'], row['upper_extra_steps'], row['upper_extra_odd_steps']) == (
                old['delta'], old['E'], old['extra_upper_tail_length'], old['extra_upper_tail_odd_steps'])
            row['previous_C_ternary_pair_matches'] = True
        else:
            row['previous_C_ternary_pair_matches'] = None
    return {'schema': 1, 'scope': 'Exact finite tail accounting; no uniform parity-density bound.',
            'baseline_sha256': hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
            'previous_C_ternary_sha256': hashlib.sha256(ternary_path.read_bytes()).hexdigest(),
            'levels': rows, 'memory_examples': memory_examples(),
            'total_steps': sum(row[s]['steps'] for row in rows for s in ('lower', 'upper')),
            'total_tail_digit_cells': sum(row[s]['tail_digit_cells_scanned'] for row in rows for s in ('lower', 'upper')),
            'new_tower_levels': [], 'new_lean_declarations': 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-v', type=int, default=12)
    args = parser.parse_args()
    data = produce(args.max_v)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'pairs': len(data['levels']),
                      'steps': data['total_steps'], 'tail_digit_cells': data['total_tail_digit_cells']}))


if __name__ == '__main__':
    main()
