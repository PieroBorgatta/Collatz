#!/usr/bin/env python3
"""Independent finite replay: ordinary Collatz, repeated division, affine sums.

This is a software cross-check, not a proof checker or an independent human audit.
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def syracuse(n):
    value, exponent = 3*n+1, 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return value, exponent


def starts(q):
    return (2**(6*q+1)-11)//3, (3*9**(2*q)-11)//8


def optional_int(value):
    return int(value) if value else None


def replay(q, limit):
    n, z = starts(q)
    x, homogeneous_numerator, a_sum = z, z, 0
    homogeneous_time = 0 if x<n else None
    word, low, peak = [], z, z
    while x >= n and len(word) < limit:
        low = min(low, x)
        x, a = syracuse(x)
        peak = max(peak, x)
        word.append(a)
        homogeneous_numerator *= 3
        a_sum += a
        if homogeneous_time is None and homogeneous_numerator < (n << a_sum):
            homogeneous_time = len(word)
    # Recompute the affine constant by its separate recurrence.
    c, total = 0, 0
    for a in word:
        c = 3*c + (1 << total)
        total += a
    assert homogeneous_numerator+c == (x << a_sum)
    return x<n, len(word), a_sum, homogeneous_time, word, x, low, peak


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=HERE)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = args.data_dir
    summary = json.loads((data/'descent_summary.json').read_text())
    assert hashlib.sha256((data/'descent_cases.csv').read_bytes()).hexdigest() == summary['csv_sha256']
    with (data/'descent_cases.csv').open() as stream:
        rows = {int(row['q']):row for row in csv.DictReader(stream)}
    assert len(rows) == summary['total_distinct_parameters']
    assert sum(int(r['steps_observed']) for r in rows.values()) == summary['total_syracuse_steps']
    assert [q for q,r in rows.items() if r['status']=='censored'] == summary['censored_parameters']
    assert sum(r['status']=='descended' for r in rows.values()) == summary['descended']
    for test in summary['bound_tests']:
        bound = Fraction(test['tau_over_q_bound'])
        violations, unknown = [], []
        for q, row in rows.items():
            if row['status']=='descended':
                if Fraction(int(row['tau']), q)>bound:
                    violations.append(q)
            elif int(row['steps_observed'])+1>bound*q:
                violations.append(q)
            else:
                unknown.append(q)
        assert len(violations)==test['violations'] and violations[:20]==test['first_violations']
        assert len(unknown)==test['unknown_due_to_censoring']
    selected = {q for q in rows if q<=127 or q%1024 == 1 and q<=8191}
    selected.update(r['q'] for r in summary['largest_ratios'])
    extended = [q for q in sorted(rows) if 'exhaustive' not in rows[q]['cohorts']]
    selected.update(extended[::8])
    selected.add(max(rows))
    observed_steps = 0
    for q in sorted(selected):
        row = rows[q]
        resolved, k, a_sum, coefficient, word, end, low, peak = replay(q, int(row['cap']))
        assert resolved == (row['status'] == 'descended')
        assert k == int(row['steps_observed']) and a_sum == int(row['exponent_sum'])
        assert optional_int(row['tau']) == (k if resolved else None)
        assert coefficient == optional_int(row['coefficient_time'])
        assert optional_int(row['coefficient_delay']) == (k-coefficient if resolved else None)
        n,z = starts(q)
        prefix = resolved and (not k or (k<2*n and low>=n+k))
        rational = resolved and (not k or (k<3*n and 3**(k+1)*z < (3*n-k)*2**a_sum))
        assert str(bool(prefix)) == row['prefix_gap_certificate']
        assert str(bool(rational)) == row['rational_descent_certificate']
        assert str(resolved and k>0) == row['minimal_parameter_certificate']
        assert n.bit_length()==int(row['source_bits']) and z.bit_length()==int(row['burst_bits'])
        assert end.bit_length()==int(row['endpoint_bits']) and peak.bit_length()==int(row['peak_bits'])
        assert hashlib.sha256(','.join(map(str, word)).encode('ascii')).hexdigest() == row['word_sha256']
        assert hashlib.sha256(end.to_bytes((end.bit_length()+7)//8, 'big')).hexdigest() == row['endpoint_sha256']
        observed_steps += k
    # Independent bridge verification from original n, using ordinary Collatz.
    bridge_cases = 0
    for q in range(1, min(summary['grid_max'], 127)+1, 2):
        n, z = starts(q)
        x, odd_steps, ordinary_steps, exponent_sum = n, 0, 0, 0
        while odd_steps < 4*q+2:
            x = 3*x+1
            ordinary_steps += 1
            a = 0
            while x%2 == 0:
                x //= 2
                a += 1
                ordinary_steps += 1
            exponent_sum += a
            odd_steps += 1
        assert x == z and exponent_sum == 6*q+4
        assert ordinary_steps == 10*q+6
        bridge_cases += 1
    # Test the minimal-parameter deduction on all 255 small exact cylinders.
    source = HERE.parent/'post_v6_transport_2026-09-24/transport_probe.py'
    spec = importlib.util.spec_from_file_location('transport', source)
    transport = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transport)
    word_cases = descent_cases = 0
    for a_sum in range(2, 10):
        for word in transport.positive_compositions(a_sum):
            if word[0] < 2:
                continue
            root, bits = transport.word_root(1, 'C', word)
            for lift in (0, 1, 2):
                q = root + lift*2**bits
                n, x = starts(q)
                for exponent in word:
                    x, actual = syracuse(x)
                    assert exponent == actual
                if x < n:
                    assert lift == 0 and q < 2**a_sum and q < 3*a_sum
                    descent_cases += 1
                word_cases += 1
    result = {'all_checks_passed': True, 'replayed_parameters': len(selected),
              'replayed_suffix_steps': observed_steps, 'original_source_bridges': bridge_cases,
              'word_and_lift_cases': word_cases, 'descending_endpoints': descent_cases,
              'selected_parameters': sorted(selected),
              'scope': 'Finite cross-check, not formal verification or independent human review'}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
