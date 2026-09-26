#!/usr/bin/env python3
"""Exact tower squaring carries, information tests and bounded selection.

Author: Codex + Piero Borgatta, 2026-09-26. Standard library only.
No uniform parity or descent bound is asserted by this finite experiment.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
PINNED_INPUTS = {
    'post_v6_margin_2026-09-25/margin_results.json':
        '837937cb8387577e53f0547a6991e1b606828b82366a94190835c8fbd246ccf5',
    'post_v6_renewal_2026-09-26/renewal_results.json':
        '19802878c6e652d2b8ed7f6eb96cdc1fb14893f8e3be245e6c14835576a09f06',
    'post_v6_seven_ancestors_2026-09-26/seven_results.json':
        '06806b7617a969ed798b7de1216eebc5adb018bfc6d7ac72c3491c3510bb5e45',
}


def horizon(v: int) -> int:
    if v < 0:
        raise ValueError('nonnegative level required')
    return (589 * (1 << v) + 611) // 612


def tower(v: int) -> int:
    if v < 0:
        raise ValueError('nonnegative level required')
    return (3 ** (1 << (v + 1)) - 1) >> (v + 3)


def direct_word(n: int, k: int) -> int:
    if n < 0 or k < 0:
        raise ValueError('nonnegative source and horizon required')
    word = 0
    for t in range(k):
        p = n & 1
        word |= p << t
        n = (3 * n + 1) // 2 if p else n // 2
    return word


def word_hash(word: int, steps: int) -> str:
    return hashlib.sha256(word.to_bytes((steps + 7) // 8, 'little')).hexdigest()


def squaring_columns(p: int, columns: int) -> dict:
    """Schoolbook square with coefficients obtained by carry-free packing.

    Use radix 2**(8*stride)>columns so multiplication does not carry
    between coefficient slots. The subsequent binary carries are explicit.
    This is distinct from the online convolution used by the tower generator.
    """
    if p < 0 or columns < 0:
        raise ValueError('nonnegative input and column count required')
    if columns == 0:
        return {'bits': [], 'coefficients': [], 'carries': [0]}
    stride = max(1, (columns.bit_length() + 7) // 8)
    encoded = bytearray(stride * columns)
    for i in range(columns):
        encoded[i * stride] = (p >> i) & 1
    polynomial = int.from_bytes(encoded, 'little')
    product = (polynomial * polynomial).to_bytes(2 * stride * columns, 'little')
    carry, bits, coefficients, carries = 0, [], [], [0]
    for k in range(columns):
        coefficient = int.from_bytes(product[k*stride:(k+1)*stride], 'little')
        total = carry + coefficient
        bits.append(total & 1)
        carry = total // 2
        coefficients.append(coefficient)
        carries.append(carry)
    return {'bits': bits, 'coefficients': coefficients, 'carries': carries}


def streaming_power_rows(depth: int, columns: int) -> dict:
    """R_0=3; R_(a+1)=R_a², column-major without exponentiation.

    Every output is generated using the previously produced row prefixes.
    The current column of the preceding row is produced before it is used.
    Prefix storage and convolution work grow with the requested precision.
    """
    if depth < 0 or columns < 0:
        raise ValueError('nonnegative depth and precision required')
    bits = [[] for _ in range(depth + 1)]
    carries = [[0] for _ in range(depth)]
    coefficients = [[] for _ in range(depth)]
    for n in range(columns):
        bits[0].append(int(n < 2))
        for a in range(depth):
            row = bits[a]
            coefficient = 2 * sum(row[i] * row[n-i] for i in range((n+1)//2))
            if n % 2 == 0:
                coefficient += row[n//2]
            total = carries[a][-1] + coefficient
            bits[a+1].append(total & 1)
            carries[a].append(total // 2)
            coefficients[a].append(coefficient)
    return {'bits': bits, 'carries': carries, 'coefficients': coefficients}


def bits_integer(bits: list[int]) -> int:
    return sum(b << i for i, b in enumerate(bits))


def tail_word(inputs: list[int]) -> int:
    """Drive the exact shortcut tail with the generated source bits."""
    z, power, word = 0, 1, 0
    for t, h in enumerate(inputs):
        p = (h + z) & 1
        word |= p << t
        z = (3**p * (power * h + z) + p) // 2
        power *= 3**p
        assert 0 <= z < power
    return word


def projected_state(p: int, r: int, n: int, w: int) -> tuple:
    if r < 3 or not 1 <= w <= n or p < 0:
        raise ValueError('valid anchored precision and window required')
    data = squaring_columns(p, n)
    return (data['carries'][n], p % (1 << (r+1)),
            (p >> (n-w)) & ((1 << w)-1),
            ((p*p) >> (n-w)) & ((1 << w)-1), (p >> n) & 1)


def analytic_collision(r: int, w: int) -> dict:
    if r < 3 or w < 1:
        raise ValueError('r>=3 and positive window required')
    a = max(2*r + 1, r+w+2)
    n = 2*a
    p = 1 + (1 << r) + (1 << (n+1))
    other = p + (1 << a)
    state = projected_state(p, r, n, w)
    assert state == projected_state(other, r, n, w)
    assert p.bit_length() == other.bit_length() and p >> n == other >> n
    output, other_output = (p*p >> n) & 1, (other*other >> n) & 1
    assert (output, other_output) == (0, 1)
    return {'r': r, 'w': w, 'n': n, 'a': a, 'P': p, 'P_other': other,
            'X': (p-1) >> r, 'X_other': (other-1) >> r,
            'state': state, 'output': output, 'other_output': other_output,
            'same_binade_and_bits_from_n': True,
            'domain': 'general positive odd roots, not exact tower sources'}


def exhaustive_collisions() -> dict:
    records, input_rows, state_rows = [], 0, 0
    for r in range(3, 7):
        anchor = 1 + (1 << r)
        for n in range(r+2, 13):
            widths = range(1, min(4, n-r-1) + 1)
            seen = {w: {} for w in widths}
            first = {}
            for p in range(anchor, 1 << n, 1 << (r+1)):
                input_rows += 1
                data = squaring_columns(p, n+1)
                square = p*p
                for w in widths:
                    state_rows += 1
                    state = (data['carries'][n], anchor,
                             (p >> (n-w)) & ((1 << w)-1),
                             (square >> (n-w)) & ((1 << w)-1), 0)
                    output = data['bits'][n]
                    old = seen[w].get(state)
                    if old is not None and old[1] != output and w not in first:
                        first[w] = {'r': r, 'n': n, 'w': w, 'P': old[0],
                                    'P_other': p, 'state': state,
                                    'output': old[1], 'other_output': output}
                    seen[w].setdefault(state, (p, output))
            for w in widths:
                records.append({'r': r, 'n': n, 'w': w,
                                'distinct_states': len(seen[w]),
                                'first_collision': first.get(w)})
    return {'input_rows': input_rows, 'projected_rows': state_rows,
            'cases': records,
            'cases_with_output_collision': sum(row['first_collision'] is not None
                                                for row in records)}


def future_carry_fiber(v: int) -> dict:
    H, K, r = horizon(v), horizon(v+1), v+3
    q = tower(v)
    n = r+K
    target = squaring_columns(1 + (q << r), n)['carries'][n]
    lower_word = direct_word(q, H)
    j = lower_word.bit_count()
    prefix = q & ((1 << H)-1)
    high = q >> K << K
    before, after = Counter(), Counter()
    carry_counts = Counter()
    maxima_by_carry = {}
    first_maximum, first_after_maximum = None, None
    best, best_after = -10**9, -10**9
    for t in range(1 << (K-H)):
        x = high | (t << H) | prefix
        assert x > 0 and direct_word(x, H) == lower_word
        p = 1 + (x << r)
        c = squaring_columns(p, n)['carries'][n]
        upper = x + (x*x << (v+2))
        delta = direct_word(upper, K).bit_count() - 2*j
        before[delta] += 1
        carry_counts[c] += 1
        maxima_by_carry[c] = max(maxima_by_carry.get(c, delta), delta)
        if delta > best:
            best, first_maximum = delta, x
        if c == target:
            after[delta] += 1
            if delta > best_after:
                best_after, first_after_maximum = delta, x
    actual_delta = direct_word(tower(v+1), K).bit_count() - 2*j
    assert after and after[actual_delta] > 0
    return {'v': v, 'H': H, 'K': K, 'carry_column': n,
            'actual_carry': target, 'actual_delta': actual_delta,
            'candidates': sum(before.values()), 'retained': sum(after.values()),
            'maximum_before': best, 'maximum_after': best_after,
            'first_maximum_source': first_maximum,
            'first_retained_maximum_source': first_after_maximum,
            'delta_distribution_before': dict(sorted(before.items())),
            'delta_distribution_after': dict(sorted(after.items())),
            'carry_counts': dict(sorted(carry_counts.items())),
            'maximum_delta_by_carry': dict(sorted(maxima_by_carry.items())),
            'future_carry_requires_additional_information': True,
            'diagnostic_level_below_v5': True}


def historical_tower_pair(v: int, baseline: dict[int, dict]) -> dict:
    H, K = horizon(v), horizon(v+1)
    columns, depth = K + v+4, v+2
    generator = streaming_power_rows(depth, columns)
    stage_checks = []
    for a, row in enumerate(generator['bits']):
        modular = pow(3, 1 << a, 1 << columns)
        assert bits_integer(row) == modular
        if a < depth:
            independent = squaring_columns(modular, columns)
            assert independent['bits'] == generator['bits'][a+1]
            assert independent['carries'] == generator['carries'][a]
            assert independent['coefficients'] == generator['coefficients'][a]
            stage_checks.append({'input_stage': a,
                                 'maximum_carry': max(generator['carries'][a]),
                                 'carry_sha256': hashlib.sha256(json.dumps(
                                     generator['carries'][a], separators=(',', ':')).encode()).hexdigest()})
    words = []
    for level, stage, shift, steps in ((v, v+1, v+3, H),
                                        (v+1, v+2, v+4, K)):
        inputs = generator['bits'][stage][shift:shift+steps]
        assert len(inputs) == steps
        word = tail_word(inputs)
        assert word == direct_word(tower(level), steps)
        assert bits_integer(inputs) == (tower(level) & ((1 << steps)-1))
        digest = word_hash(word, steps)
        assert digest == baseline[level]['parity_trace_sha256']
        assert word.bit_count() == baseline[level]['odd_steps']
        words.append({'v': level, 'steps': steps, 'odd_steps': word.bit_count(),
                      'parity_trace_sha256': digest})
    return {'v': v, 'columns': columns, 'squaring_depth': depth,
            'stored_row_bits': (depth+1)*columns,
            'stored_carry_entries': depth*(columns+1),
            'generated_words': words, 'squaring_stage_checks': stage_checks,
            'delta': words[1]['odd_steps'] - 2*words[0]['odd_steps'],
            'exact_seed_3': True, 'all_generated_columns_independently_verified': True}


def witness_carries(v: int, x: int, label: str, K: int | None = None) -> dict:
    q, r = tower(v), v+3
    difference = abs(x-q)
    if difference == 0:
        raise ValueError('distinct source required')
    M = (difference & -difference).bit_length()-1
    n = M+r
    p, actual = 1+(x << r), 1+(q << r)
    dx, dq = squaring_columns(p, n+2), squaring_columns(actual, n+2)
    assert dx['carries'][:n+1] == dq['carries'][:n+1]
    assert dx['bits'][:n+1] == dq['bits'][:n+1]
    assert dx['bits'][n+1] != dq['bits'][n+1]
    assert abs(dx['carries'][n+1] - dq['carries'][n+1]) == 1
    assert (p >> n & 1) != (actual >> n & 1)
    assert dx['coefficients'][n] - dq['coefficients'][n] == 2*((p >> n & 1)-(actual >> n & 1))
    record = {'label': label, 'v': v, 'shared_source_bits_M': M,
              'shared_signature_bits_n': n,
              'equal_carry_entries': n+1, 'all_exposed_carries_equal': True,
              'last_shared_carry': dx['carries'][n],
              'first_different_carry': dx['carries'][n+1],
              'actual_first_different_carry': dq['carries'][n+1],
              'first_different_square_bit': n+1,
              'is_actual_tower_source': False}
    if K is not None:
        boundary = r+K
        future_x = squaring_columns(p, boundary)['carries'][boundary]
        future_q = squaring_columns(actual, boundary)['carries'][boundary]
        record.update({'future_boundary': boundary, 'future_witness_carry': future_x,
                       'future_actual_carry': future_q,
                       'retained_by_future_carry_filter': future_x == future_q})
    return record


def historical_signed_budget(baseline: dict[int, dict]) -> dict:
    anchor, margin = 16, (1 << 15)-baseline[16]['odd_steps']
    loss, records = Fraction(0), []
    for v in range(anchor, 24):
        delta = baseline[v+1]['odd_steps'] - 2*baseline[v]['odd_steps']
        loss += Fraction(delta, 1 << (v-anchor+1))
        next_margin = (1 << v)-baseline[v+1]['odd_steps']
        assert Fraction(next_margin, 1 << (v+1-anchor)) == margin-loss
        records.append({'through_pair_v': v, 'delta': delta,
                        'signed_partial_loss': {'numerator': loss.numerator,
                                                'denominator': loss.denominator},
                        'scaled_margin': {'numerator': (margin-loss).numerator,
                                          'denominator': (margin-loss).denominator}})
    return {'anchor': anchor, 'anchor_margin': margin, 'partials': records,
            'independent_future_bound': False,
            'scope': 'exact retrospective telescoping only'}


def load_inputs() -> dict:
    result = {}
    for name, expected in PINNED_INPUTS.items():
        data = (NOTES / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('changed frozen input: ' + name)
        result[name] = json.loads(data)
    return result


def produce() -> dict:
    inputs = load_inputs()
    margin = inputs['post_v6_margin_2026-09-25/margin_results.json']
    baseline = {row['v']: row for row in margin['levels']}
    renewal = inputs['post_v6_renewal_2026-09-26/renewal_results.json']
    witnesses = []
    for row in renewal['threshold_failure_witnesses']:
        if not 5 <= row['v'] <= 12:
            raise ValueError('unexpected archived witness level')
        record = witness_carries(row['v'], int(row['X_hex'], 16),
                                 'renewal_threshold', row['horizon_K'])
        assert record['shared_source_bits_M'] == row['precision_M']
        witnesses.append(record)
    assert len(witnesses) == 8
    seven = inputs['post_v6_seven_ancestors_2026-09-26/seven_results.json']['search']['witness']
    last = seven['levels'][-2]
    witnesses.append(witness_carries(last['v'], int(last['value_hex'], 16),
                                    'seven_ancestor_counterexample', horizon(last['v']+1)))
    return {'schema': 'tower-binary-carries-v1',
            'scope': 'bounded exact generator, compression falsification and future-carry selection',
            'protocol_sha256': hashlib.sha256((HERE/'PROTOCOL_IT.md').read_bytes()).hexdigest(),
            'pinned_inputs_sha256': PINNED_INPUTS,
            'exact_generator_pairs': [historical_tower_pair(v, baseline) for v in range(5, 10)],
            'archived_witness_carry_checks': witnesses,
            'exhaustive_projection': exhaustive_collisions(),
            'analytic_collision_checks': [analytic_collision(r, w)
                                           for r in range(3, 7) for w in range(1, 5)],
            'future_carry_selection': [future_carry_fiber(v) for v in range(5)],
            'historical_signed_budget': historical_signed_budget(baseline),
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'uniform_delta_bound_proved': False,
            'uniform_family_descent_proved': False,
            'tower_specific_memory_impossibility_proved': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'binary_carry_results.json')
    args = parser.parse_args()
    result = produce()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified_generator_pairs': len(result['exact_generator_pairs']),
                      'witnesses_with_redundant_exposed_carries': len(result['archived_witness_carry_checks']),
                      'projection_cases_with_collision': result['exhaustive_projection']['cases_with_output_collision'],
                      'future_selection': [{key: row[key] for key in
                                           ('v', 'candidates', 'retained', 'maximum_before', 'maximum_after')}
                                           for row in result['future_carry_selection']],
                      'uniform_bound_proved': False}, indent=2))


if __name__ == '__main__':
    main()
