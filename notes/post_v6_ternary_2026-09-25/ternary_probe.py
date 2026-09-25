#!/usr/bin/env python3
"""Ordinary base-3 Collatz replay and a first-seam arithmetic certificate.

The digit engines do not use binary residues or convert the evolving state to
an integer. Integer conversion helpers are used only in independent small tests.
No uniform estimate on the full doubling discrepancy is asserted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BASELINE = ROOT / 'notes/post_v6_margin_2026-09-25/margin_results.json'


def to_digits(n: int) -> list[int]:
    if n <= 0:
        raise ValueError('positive integer required')
    out = []
    while n:
        n, d = divmod(n, 3)
        out.append(d)
    return out[::-1]


def from_digits(digits: list[int]) -> int:
    n = 0
    for d in digits:
        if d not in (0, 1, 2):
            raise ValueError('invalid ternary digit')
        n = 3 * n + d
    return n


def divide_digits(digits: list[int], incoming: int = 0) -> tuple[list[int], int, int]:
    if incoming not in (0, 1):
        raise ValueError('incoming carry must be 0 or 1')
    q, carry, count = [], incoming, 0
    for d in digits:
        if d not in (0, 1, 2):
            raise ValueError('invalid ternary digit')
        digit, carry = divmod(3 * carry + d, 2)
        q.append(digit)
        count += carry
    return q, carry, count


def carry_types(digits: list[int]) -> tuple[int, ...]:
    counts, c = [0] * 6, 0
    for d in digits:
        if d not in (0, 1, 2):
            raise ValueError('invalid ternary digit')
        counts[3 * c + d] += 1
        c = (c + d) % 2
    return tuple(counts)


def step_digits(digits: list[int]) -> tuple[list[int], list[int]]:
    if not digits or digits[0] not in (1, 2):
        raise ValueError('positive canonical ternary word required')
    total = sum(digits)
    odd = total % 2
    q, final_carry, carry_count = divide_digits(digits + ([1] if odd else []))
    assert final_carry == 0
    removed = int(q[0] == 0)
    after = q[removed:]
    row = [odd, len(digits), len(after), total, sum(after), carry_count,
           removed, digits.count(1), after.count(1)]
    assert 2 * row[4] == row[3] + odd + 2 * carry_count
    return after, row


def simulate_digits(m: int, steps: int) -> dict:
    if m < 1 or steps < 0:
        raise ValueError('m positive, steps nonnegative required')
    digits, bits, ledger = [2] * m, [], []
    for _ in range(steps):
        digits, row = step_digits(digits)
        ledger.append(row)
        bits.append(row[0])
    return {'digits': digits, 'bits': bits, 'ledger': ledger}


def exact_clock(steps: int) -> list[int]:
    """floor(log_3(2^t)), t=0..steps, using exact integer comparisons."""
    if steps < 0:
        raise ValueError('steps must be nonnegative')
    power, k, out = 1, 0, [0]
    for t in range(1, steps + 1):
        candidate = 3 * power
        if candidate.bit_length() <= t:  # candidate odd >1, never equals 2^t
            power, k = candidate, k + 1
        out.append(k)
    return out


def horizon(v: int) -> int:
    if v < 5:
        raise ValueError('level must be at least 5')
    return (589 * (1 << v) + 611) // 612


def packed(bits: list[int]) -> bytes:
    data = bytearray((len(bits) + 7) // 8)
    for i, bit in enumerate(bits):
        data[i // 8] |= bit << (i % 8)
    return bytes(data)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def first_seam(v: int) -> dict:
    if v < 0:
        raise ValueError('nonnegative level required')
    r, m = v + 3, 1 << (v + 1)
    q, residue, carry0 = 1 << (r + 1), 1, 0
    for _ in range(m):
        residue = (3 * residue) & (q - 1)
        carry0 += (residue >> r) & 1
    difference = m - 2 * carry0
    numerator = m * (r * r - 1) ** 2
    assert 2 * difference * difference <= numerator
    return {'v': v, 'r': r, 'm': m, 'carry_count_incoming_zero': carry0,
            'carry_count_incoming_one': m - carry0,
            'carry_difference': difference,
            'dyadic_bound_squared_numerator': numerator,
            'dyadic_bound_squared_denominator': 2,
            'bound_holds': True, 'dyadic_bound_strictly_below_m': numerator < 2 * m * m}


def run_engine(engine: Path, m: int, steps: int) -> dict:
    with tempfile.TemporaryDirectory(prefix='ternary-') as temp:
        temp = Path(temp)
        trace, digits, ledger = [temp / name for name in ('trace.bin', 'digits.ternary', 'ledger.json')]
        result = subprocess.run([str(engine), '--m', str(m), '--steps', str(steps),
                                 '--trace', str(trace), '--digits', str(digits),
                                 '--ledger', str(ledger)], check=True, capture_output=True, text=True)
        raw_trace, raw_digits = trace.read_bytes(), digits.read_bytes()
        bits = [(raw_trace[i // 8] >> (i % 8)) & 1 for i in range(steps)]
        assert raw_trace == packed(bits)
        return {'summary': json.loads(result.stdout), 'bits': bits,
                'digits': raw_digits, 'ledger': json.loads(ledger.read_text())}


def check_integer_replay(m: int, bits: list[int], final_digits: bytes) -> None:
    """Independent binary-integer oracle, including the full final state."""
    value = pow(3, m) - 1
    for bit in bits:
        assert value & 1 == bit
        value = (3 * value + 1) // 2 if value & 1 else value // 2
    # Decode bounded chunks to avoid Python's decimal/string digit limit.
    endpoint = 0
    for start in range(0, len(final_digits), 32):
        chunk = final_digits[start:start + 32]
        endpoint = endpoint * pow(3, len(chunk)) + int(chunk, 3)
    assert endpoint == value


def validate_ledger(run: dict, m: int, steps: int, clock: list[int]) -> None:
    rows, stats = run['ledger'], run['summary']
    assert len(rows) == steps == len(run['bits'])
    length, total, ones, odds, carry, removed, scanned = m, 2 * m, 0, 0, 0, 0, 0
    for t, row in enumerate(rows, 1):
        b, before_l, after_l, before_s, after_s, c, z, before_o, after_o = row
        assert (before_l, before_s, before_o) == (length, total, ones)
        assert b == run['bits'][t - 1] == before_s % 2
        assert 2 * after_s == before_s + b + 2 * c
        assert after_l == before_l + b - z
        odds += b
        removed += z
        carry += c
        scanned += before_l + b
        assert removed == clock[t]
        assert after_l == m + odds - clock[t]
        length, total, ones = after_l, after_s, after_o
    digits = run['digits']
    assert len(digits) == length and sum(d - 48 for d in digits) == total
    assert digits.count(b'1') == ones
    expected = {'m': m, 'steps': steps, 'odd_steps': odds, 'initial_length': m,
                'final_length': length, 'initial_digit_sum': 2 * m,
                'final_digit_sum': total, 'initial_count_ones': 0, 'final_count_ones': ones,
                'final_digit_counts': [digits.count(str(d).encode()) for d in range(3)],
                'total_leading_digits_removed': removed, 'total_carry_ones': carry,
                'total_scanned_digits': scanned,
                'minimum_step_carry_ones': min((r[5] for r in rows), default=0),
                'maximum_step_carry_ones': max((r[5] for r in rows), default=0),
                'total_state_digit_sum_before': sum(r[3] for r in rows),
                'total_state_digit_sum_after': sum(r[4] for r in rows)}
    assert all(stats[key] == val for key, val in expected.items())


def produce(engine: Path, max_level: int = 16, seam_max: int = 22) -> dict:
    if not 6 <= max_level <= 24 or seam_max < 5:
        raise ValueError('max-level must be 6..24; seam-max at least 5')
    baseline = {row['v']: row for row in json.loads(BASELINE.read_text())['levels']}
    levels, runs = [], {}
    max_steps = 2 * (horizon(max_level - 1) + max_level + 2)
    clock = exact_clock(max_steps)
    for v in range(5, max_level + 1):
        m, r, h = 1 << (v + 1), v + 3, horizon(v)
        length = h + r
        steps = length if v == 5 else 2 * (horizon(v - 1) + v + 2)
        run = run_engine(engine, m, steps)
        validate_ledger(run, m, steps, clock)
        check_integer_replay(m, run['bits'], run['digits'])
        assert run['bits'][:r] == [0] * r
        q_trace = packed(run['bits'][r:length])
        j = sum(run['bits'][:length])
        assert j == baseline[v]['odd_steps']
        assert digest(q_trace) == baseline[v]['parity_trace_sha256']
        rows = run['ledger']
        levels.append({'v': v, 'm': m, 'r': r, 'horizon_Q': h, 'horizon_R': length,
                       'steps_simulated': steps, 'odd_steps_Q_at_H': j,
                       'baseline_trace_matches': True,
                       'full_integer_replay_and_endpoint_verified': True,
                       'Q_trace_sha256': digest(q_trace),
                       'R_full_trace_sha256': digest(packed(run['bits'])),
                       'final_ternary_sha256': digest(run['digits']),
                       'ledger_sha256': digest(json.dumps(rows, separators=(',', ':')).encode()),
                       'length_at_L': rows[length - 1][2],
                       'leading_digits_removed_at_L': clock[length],
                       'every_step_clock_and_mass_identity_verified': True,
                       'engine_summary': run['summary']})
        runs[v] = {'bits': run['bits'], 'length_at_L': rows[length - 1][2],
                   'length_at_end': rows[-1][2], 'J_at_L': j}
    pairs = []
    for v in range(5, max_level):
        lower, upper = runs[v], runs[v + 1]
        length = horizon(v) + v + 3
        upper_length = horizon(v + 1) + v + 4
        epsilon = 2 * horizon(v) - horizon(v + 1)
        tail_length = 2 * length - upper_length
        tail_odds = sum(upper['bits'][upper_length:2 * length])
        delta = upper['J_at_L'] - 2 * lower['J_at_L']
        error = sum(upper['bits']) - 2 * lower['J_at_L']
        correction = clock[2 * length] - 2 * clock[length]
        length_defect = upper['length_at_end'] - 2 * lower['length_at_L']
        assert epsilon in (0, 1) and correction in (0, 1)
        assert tail_length == v + 2 + epsilon
        assert error == delta + tail_odds == length_defect + correction
        pairs.append({'v': v, 'L': length, 'epsilon': epsilon, 'delta': delta,
                      'E': error, 'extra_upper_tail_length': tail_length,
                      'extra_upper_tail_odd_steps': tail_odds,
                      'length_defect': length_defect, 'clock_correction': correction,
                      'exact_relations_verified': True})
    seams = [first_seam(v) for v in range(5, seam_max + 1)]
    for row in seams:
        if row['v'] <= 12:
            # A single long division by 2^r; independent of modular-bit formula.
            word, c, divisor = [], 0, 1 << row['r']
            for _ in range(row['m']):
                digit, c = divmod(3 * c + 2, divisor)
                word.append(digit)
            assert c == 0
            _, last0, count0 = divide_digits(word, 0)
            _, last1, count1 = divide_digits(word, 1)
            assert (last0, last1) == (1, 0)
            assert count1 - count0 == row['carry_difference']
            row['direct_padded_word_check'] = True
        else:
            row['direct_padded_word_check'] = False
    flow = []
    for n in (51, 403):
        nxt = (3 * n + 1) // 2
        a, b = carry_types(to_digits(n)), carry_types(to_digits(nxt))
        flow.append({'n': n, 'T_n': nxt, 'types_before': a, 'types_after': b,
                     'drift_before_minus_after': [x - y for x, y in zip(a, b)]})
    assert all(sum(row['drift_before_minus_after'][i] for row in flow) == 0 for i in range(6))
    return {'schema': 1, 'scope': 'Independent finite ternary replay; first-seam paper bound only; no bound on E or Delta.',
            'input_sha256': {'notes/post_v6_margin_2026-09-25/margin_results.json': digest(BASELINE.read_bytes())},
            'levels': levels, 'pairs': pairs, 'first_seams': seams,
            'six_type_potential_obstruction': flow,
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'first_seam_bound_status': 'Paper proof; priority not established; not formalized in Lean.',
            'uniform_doubling_error_bound': 'Open'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-level', type=int, default=16)
    parser.add_argument('--seam-max', type=int, default=22)
    args = parser.parse_args()
    result = produce(args.engine.resolve(), args.max_level, args.seam_max)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'levels': len(result['levels']), 'pairs': len(result['pairs']),
                      'first_seams': len(result['first_seams']), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
