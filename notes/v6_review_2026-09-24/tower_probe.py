#!/usr/bin/env python3
"""Exact adversarial probe for the cancellation tower in Collatz project v6.
No floating point is used for word identities, macro exit, or first descent.
Floating point logarithms are used only for human-readable ratio diagnostics.
This is a finite diagnostic, not a global Collatz proof.
"""
import argparse
import json
import math
from pathlib import Path


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def step(n):
    t = 3 * n + 1
    e = v2(t)
    return t >> e, e


def family(k):
    assert k >= 4 and k % 2 == 0
    n = ((1 << (k + 1)) - 11) // 3
    assert 3 * n == (1 << (k + 1)) - 11 and n > 0 and n % 2
    return n


def macro(k):
    """Exact first departure from repeated negative [1,2] cycle -5,-7."""
    n = family(k)
    r, rem = divmod(k - 1, 3)
    h = rem + 1
    p = 9 ** r
    x = (1 << h) * p - 5
    if h == 1:
        terminal = [3]
        y = (3 * p - 7) // 4
        assert 4 * y + 7 == 3 ** (2 * r + 1)
    elif h == 2:
        terminal = [1, 1]
        y = 9 * p - 10
        assert y + 10 == 3 ** (2 * r + 2)
    else:
        terminal = [1, 4]
        y = (9 * p - 5) // 4
        assert 4 * y + 5 == 3 ** (2 * r + 2)
    word = [1] + [1, 2] * r + terminal
    t = n
    minimum = n
    for index, expected_e in enumerate(word):
        t, actual_e = step(t)
        assert expected_e == actual_e, (k, index, expected_e, actual_e)
        minimum = min(minimum, t)
        if index == 2 * r:
            assert t == x
    assert t == y
    if k >= 30:
        assert minimum == n, (k, 'descent before macro exit')
        assert y > n
    return n, y, r, h, len(word), minimum < n


def first_descent(n, cap):
    t = n
    peak = n
    exponent_sum = 0
    for length in range(1, cap + 1):
        t, e = step(t)
        exponent_sum += e
        peak = max(peak, t)
        if t < n:
            return {'steps': length, 'valuation_sum': exponent_sum,
                    'endpoint': str(t), 'peak_bit_length': peak.bit_length()}
    return {'steps': None, 'cap': cap, 'last_value': str(t)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-k', type=int, default=2000)
    parser.add_argument('--cap', type=int, default=100000)
    parser.add_argument('--output', default=str(Path(__file__).with_name('tower_results.json')))
    args = parser.parse_args()
    data = []
    for k in range(4, args.max_k + 1, 2):
        n, y, r, h, length, early_drop = macro(k)
        first = first_descent(n, args.cap)
        data.append({'k': k, 'r': r, 'h': h, 'source_bit_length': n.bit_length(),
                     'macro_steps': length, 'macro_endpoint_bit_length': y.bit_length(),
                     'macro_endpoint_above_source': y > n,
                     'descent_in_macro': early_drop,
                     'log2_macro_ratio': math.log2(y) - math.log2(n),
                     'first_descent': first})
    summary = {'max_k': args.max_k, 'tested_families': len(data),
               'all_exact_macro_checks_passed': True,
               'all_k_at_least_30_have_no_drop_through_macro_exit': all(
                   not row['descent_in_macro'] for row in data if row['k'] >= 30),
               'finite_first_descent_observed': sum(row['first_descent']['steps'] is not None for row in data),
               'max_first_descent': max((row['first_descent']['steps'], row['k']) for row in data if row['first_descent']['steps'] is not None),
               'selected': [row for row in data if row['k'] in [4, 6, 8, 10, 12, 20, 30, 40, 60, 100, 200, 500, 1000, 2000]]}
    Path(args.output).write_text(json.dumps({'summary': summary, 'rows': data}, indent=2) + '\n')
    print(json.dumps({key: value for key, value in summary.items() if key != 'selected'}, indent=2))


if __name__ == '__main__':
    main()
