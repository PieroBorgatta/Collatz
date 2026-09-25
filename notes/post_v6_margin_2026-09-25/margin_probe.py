#!/usr/bin/env python3
"""Retrospective global-margin checks and exact generic quadratic adversaries.

No new Q_v level is evaluated and no uniform error bound is asserted.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
COMPENSATION = NOTES / 'post_v6_compensation_2026-09-25'
sys.path.insert(0, str(COMPENSATION))
sys.path.insert(0, str(NOTES / 'post_v6_arithmetic_2026-09-25'))
from block_engine import horizon, initial_residue, parity_trace
from arithmetic_probe import word_residue


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rational(x):
    return {'numerator': x.numerator, 'denominator': x.denominator}


def root_tail(v):
    """Sum over i>=0 of 2^ceil((v+i)/2)/2^(i+1), an integer."""
    return (3 if v % 2 else 2) * (1 << (v // 2))


def quadratic_tail(v):
    return v * v + 2 * v + 3


def direct_word(x, steps):
    word = 0
    for i in range(steps):
        bit = x & 1
        word |= bit << i
        x = (3 * x + 1) // 2 if bit else x // 2
    return word, x


def quadratic(v, x):
    return x + (x * x << (v + 2))


def lift_quadratic(v, lower_residue, H, target, K):
    """Invert f_v on a prescribed lift; H<=K<=2H kills the quadratic remainder."""
    if v < 0 or not 1 <= H <= K <= 2 * H:
        raise ValueError('invalid lift precision')
    if not 0 <= lower_residue < (1 << H) or not 0 <= target < (1 << K):
        raise ValueError('residue outside its modulus')
    difference = target - quadratic(v, lower_residue)
    if difference % (1 << H):
        raise ValueError('incompatible lower residue')
    modulus = 1 << (K - H)
    derivative = 1 + (lower_residue << (v + 3))
    correction = ((difference >> H) * pow(derivative, -1, modulus)) % modulus
    result = lower_residue + (correction << H)
    assert quadratic(v, result) % (1 << K) == target
    return result


def adversary(v, kind):
    """Keep high bits of Q_v and a chosen lower cylinder, force an odd upper tail."""
    H, K = horizon(v), horizon(v + 1)
    Q = (9 ** (1 << v) - 1) >> (v + 3)
    Q_next = (9 ** (1 << (v + 1)) - 1) >> (v + 4)
    assert quadratic(v, Q) == Q_next and Q.bit_length() > K
    if kind == 'unit_prefix':
        lower = 1
    elif kind == 'actual_prefix':
        lower = Q % (1 << H)
    else:
        raise ValueError('unknown adversary kind')
    lower_word, _ = direct_word(lower, H)
    upper_head, _ = direct_word(quadratic(v, lower), H)
    target_word = upper_head | (((1 << (K - H)) - 1) << H)
    target_residue = word_residue(target_word, K)
    lifted = lift_quadratic(v, lower, H, target_residue, K)
    # Replacing only the bottom K bits preserves all ordinary high digits.
    X = ((Q >> K) << K) + lifted
    Y = quadratic(v, X)
    actual_lower, _ = direct_word(X, H)
    actual_upper, _ = direct_word(Y, K)
    assert actual_lower == lower_word and actual_upper == target_word
    assert X.bit_length() == Q.bit_length() and (X >> K) == (Q >> K)
    assert abs(X - Q) < 1 << K
    assert Q_next < 4 * Y and Y < 4 * Q_next
    lower_j, upper_j = lower_word.bit_count(), target_word.bit_count()
    assert lower_j < (1 << (v - 1)) and upper_j > (1 << v)
    if kind == 'actual_prefix':
        assert direct_word(Q, H)[0] == actual_lower and (X - Q) % (1 << H) == 0
    return {'v': v, 'kind': kind, 'H': H, 'H_next': K,
            'lower_odd': lower_j, 'upper_head_odd': upper_head.bit_count(),
            'forced_odd_tail_length': K - H, 'upper_odd': upper_j,
            'lower_margin': (1 << (v - 1)) - lower_j,
            'upper_margin': (1 << v) - upper_j,
            'delta': upper_j - 2 * lower_j,
            'X_hex': hex(X), 'Y_hex': hex(Y), 'Q_v_bits': Q.bit_length(),
            'distance_to_Q_v_bits': abs(X - Q).bit_length(),
            'same_lower_word_as_Q_v': kind == 'actual_prefix',
            'same_all_high_bits_above_H_next': True,
            'scope': 'Positive integer pair with exact quadratic relation; X is not Q_v.'}


def references():
    sources = [NOTES / 'post_v6_certificates_2026-09-24' / 'certificate_results.json',
               COMPENSATION / 'calibration_results.json',
               COMPENSATION / 'holdout_results.json']
    raw = [p.read_bytes() for p in sources]
    cert, calibration, holdout = map(json.loads, raw)
    expected = {}
    for row in cert['rows']:
        first = row['attempts'][0]
        expected[row['v']] = {'horizon': first['precision_bits'],
                              'odd_steps': first['odd_steps'],
                              'initial_residue_sha256': first['initial_residue_sha256']}
    for row in calibration['rows'] + holdout['rows']:
        v = row['v']
        if v in expected:
            assert all(row[key] == value for key, value in expected[v].items())
        expected[v] = {key: row[key] for key in ('horizon', 'odd_steps',
                       'initial_residue_sha256', 'parity_trace_sha256')}
    assert sorted(expected) == list(range(5, 25))
    return expected, {str(p.relative_to(NOTES.parent)): sha(data)
                      for p, data in zip(sources, raw)}


def check_reference(row, expected):
    for key, value in expected.items():
        if row[key] != value:
            raise ValueError(f'baseline mismatch: v={row["v"]}, {key}')


def run():
    expected, fingerprints = references()
    levels, pairs = [], []
    previous_residue = None
    for v in range(5, 25):
        H = horizon(v)
        residue = initial_residue(v, H)
        trace = parity_trace(residue, H)
        packed = int.from_bytes(trace, 'little')
        j = packed.bit_count()
        row = {'v': v, 'horizon': H, 'odd_steps': j,
               'margin': (1 << (v - 1)) - j,
               'initial_residue_sha256': sha(residue.to_bytes((H + 7) // 8, 'little')),
               'parity_trace_sha256': sha(trace)}
        check_reference(row, expected[v])
        if levels:
            lower = levels[-1]
            w, h, old_j = lower['v'], lower['horizon'], lower['odd_steps']
            epsilon = 2 * h - H
            assert epsilon in (0, 1)
            mask = (1 << h) - 1
            assert (residue & mask) == (quadratic(w, previous_residue) & mask)
            head = (packed & ((1 << h) - 1)).bit_count()
            delta = j - 2 * old_j
            assert row['margin'] == 2 * lower['margin'] - delta
            pairs.append({'v': w, 'epsilon': epsilon, 'lower_odd': old_j,
                          'upper_odd': j, 'delta': delta,
                          'lower_margin': lower['margin'], 'upper_margin': row['margin'],
                          'upper_head_odd': head, 'upper_tail_odd': j - head,
                          'head_discrepancy': head - old_j,
                          'tail_discrepancy': j - head - old_j,
                          'delta_le_zero': delta <= 0,
                          'delta_le_v_squared': delta <= w * w,
                          'delta_le_4_v_squared': delta <= 4 * w * w,
                          'delta_le_2_times_dyadic_root': delta <= 2 * (1 << ((w + 1) // 2)),
                          'forced_tail_upper_odd': head + H - h,
                          'forced_tail_would_fail_upper_budget': head + H - h > (1 << w),
                          'scope': 'All bound checks are retrospective, not uniform results.'})
        levels.append(row)
        previous_residue = residue
        print(json.dumps({'v': v, 'margin': row['margin'], 'baseline_verified': True}), flush=True)

    targets = []
    for row in levels:
        v, m = row['v'], row['margin']
        targets.append({'v': v, 'margin': m,
                        'quadratic_4_tail_cost': 4 * quadratic_tail(v),
                        'quadratic_4_base_slack': m - 4 * quadratic_tail(v),
                        'root_2_tail_cost': 2 * root_tail(v),
                        'root_2_base_slack': m - 2 * root_tail(v)})
    loss = sum((Fraction(max(0, p['delta']), 1 << (p['v'] + 1 - 15))
                for p in pairs if p['v'] >= 15), Fraction(0))
    signed = sum((Fraction(p['delta'], 1 << (p['v'] + 1 - 15))
                  for p in pairs if p['v'] >= 15), Fraction(0))
    m15, m24 = levels[10]['margin'], levels[-1]['margin']
    assert Fraction(m24, 1 << 9) == m15 - signed
    examples = [adversary(v, kind) for kind, vs in (
        ('unit_prefix', (6, 10, 12)), ('actual_prefix', (8, 10, 12))) for v in vs]
    return {'scope': 'Retrospective exact global margins and generic adversaries; no new tower levels.',
            'source_sha256': fingerprints, 'levels': levels, 'pairs': pairs,
            'conditional_bound_costs': targets,
            'positive_weighted_loss_15_through_23': rational(loss),
            'signed_weighted_loss_15_through_23': rational(signed),
            'remaining_positive_loss_budget_at_anchor_15': rational(Fraction(m15) - loss),
            'generic_quadratic_adversaries': examples,
            'uniform_delta_bound_proved': False, 'uniform_family_descent_proved': False,
            'new_lean_declarations': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'margin_results.json')
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
