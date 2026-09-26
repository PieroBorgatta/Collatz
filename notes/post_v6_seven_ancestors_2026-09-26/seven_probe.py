#!/usr/bin/env python3
"""Frozen, finite falsification of the seven-ancestor margin filter."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'post_v6_ancestry_2026-09-25'))
from ancestry_probe import ancestor_interval, chain, recover_ancestor, tower
from block_engine import horizon, parity_trace

DEPTH = 7
LIMIT = 100000


def candidate_interval(v):
    if v < 10:
        raise ValueError('the frozen candidate formula starts at v=10')
    u = v - DEPTH
    L, U = ancestor_interval(u, v + 1)
    q, s = tower(u), 1 << (u - 1)
    step = 2 * 3**s
    t_min, t_max = -((q - L) // step), (U - q) // step
    return {'v': v, 'u': u, 'L': L, 'U': U, 'Q_u': q, 'step': step,
            'ternary_precision': s, 't_min': t_min, 't_max': t_max,
            'first': q + step * t_min, 'last': q + step * t_max,
            'count': max(0, t_max - t_min + 1)}


def trace(n, length):
    return parity_trace(n & ((1 << length) - 1), length)


def trace_record(packed, length):
    return {'length': length, 'odd_steps': int.from_bytes(packed, 'little').bit_count(),
            'packed_lsb_first_hex': packed.hex(),
            'parity_trace_sha256': hashlib.sha256(packed).hexdigest()}


def valuation3(n):
    if n == 0:
        return None  # infinite valuation, distinct from a finite integer
    n, out = abs(n), 0
    while n % 3 == 0:
        n //= 3
        out += 1
    return out


def record_candidate(v, t):
    info = candidate_interval(v)
    if not info['t_min'] <= t <= info['t_max']:
        raise ValueError('candidate outside the frozen height interval')
    x = info['Q_u'] + info['step'] * t
    values = chain(info['u'], x, DEPTH + 1)
    X, Y = values[-2:]
    low = trace_record(trace(X, horizon(v)), horizon(v))
    high = trace_record(trace(Y, horizon(v + 1)), horizon(v + 1))
    levels = []
    for w, n in enumerate(values, info['u']):
        q = tower(w)
        precision = 1 << (w - 1)
        assert n % 2 == 1 and n.bit_length() == q.bit_length()
        assert (n - q) % 3**precision == 0
        assert recover_ancestor(w, n, w - info['u']) == x
        levels.append({'v': w, 'value_hex': hex(n), 'bits': n.bit_length(),
                       'same_binade_as_Q': True, 'odd': True,
                       'required_ternary_precision': precision,
                       'difference_valuation3': valuation3(n - q),
                       'signature_valuation3': valuation3(1 + (n << (w + 3)))})
    return {'t': t, 'ancestor': x, 'levels': levels,
            'lower': low, 'upper': high,
            'lower_margin': (1 << (v - 1)) - low['odd_steps'],
            'upper_margin': (1 << v) - high['odd_steps'],
            'is_actual_tower': t == 0}


def search(v=11, limit=LIMIT):
    if limit < 1:
        raise ValueError('positive search limit required')
    info = candidate_interval(v)
    rows, witness = [], None
    for t in range(info['t_min'], min(info['t_max'] + 1, info['t_min'] + limit)):
        x = info['Q_u'] + info['step'] * t
        X, Y = chain(info['u'], x, DEPTH + 1)[-2:]
        low, high = trace(X, horizon(v)), trace(Y, horizon(v + 1))
        ml = (1 << (v - 1)) - int.from_bytes(low, 'little').bit_count()
        mu = (1 << v) - int.from_bytes(high, 'little').bit_count()
        rows.append({'t': t, 'ancestor': x, 'lower_margin': ml, 'upper_margin': mu,
                     'lower_trace_sha256': hashlib.sha256(low).hexdigest(),
                     'upper_trace_sha256': hashlib.sha256(high).hexdigest()})
        if ml >= 0 > mu:
            witness = record_candidate(v, t)
            break
    exhausted = len(rows) == info['count']
    status = ('counterexample' if witness is not None else
              'finite_case_verified' if exhausted else 'partial_no_counterexample')
    return {'interval': info, 'limit': limit, 'order': 'increasing integer t, including negatives',
            'visited_count': len(rows), 'interval_exhausted': exhausted,
            'status': status, 'visited': rows, 'witness': witness}


def produce():
    pre = json.loads((HERE / 'presearch_interval.json').read_text())
    protocol_hash = hashlib.sha256((HERE / 'PROTOCOL_IT.md').read_bytes()).hexdigest()
    assert protocol_hash == pre['protocol_sha256']
    interval = candidate_interval(11)
    for key, value in interval.items():
        if key != 'ternary_precision':
            assert pre[key] == value
    result = search()
    actual = record_candidate(11, 0)
    baseline = json.loads((HERE.parent / 'post_v6_margin_2026-09-25/margin_results.json').read_text())
    for level, label in ((11, 'lower'), (12, 'upper')):
        frozen = next(row for row in baseline['levels'] if row['v'] == level)
        assert actual[label]['parity_trace_sha256'] == frozen['parity_trace_sha256']
    return {'protocol_sha256': protocol_hash, 'search': result,
            'actual_tower_comparison': actual,
            'scope': 'Finite falsification test of the frozen filter, not of Collatz or the exact Q family.',
            'new_tower_levels': [], 'new_lean_declarations': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'seven_results.json')
    args = parser.parse_args()
    result = produce()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    s = result['search']
    print(json.dumps({'status': s['status'], 'total_candidates': s['interval']['count'],
                      'visited': s['visited_count'],
                      'witness': ({k: s['witness'][k] for k in
                                   ('t', 'ancestor', 'lower_margin', 'upper_margin')}
                                  if s['witness'] else None)}, indent=2))


if __name__ == '__main__':
    main()
