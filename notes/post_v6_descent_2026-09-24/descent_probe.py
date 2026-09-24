#!/usr/bin/env python3
"""Exact, bounded first-passage study for the v=1 cancellation towers.

Standard library only. No floating-point decisions or conjectural shortcuts.
The cap is censoring, never a proof of divergence. See RESULTS_IT.md for scope.
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
TRANSPORT = HERE.parent / 'post_v6_transport_2026-09-24/transport_probe.py'
spec = importlib.util.spec_from_file_location('tower_transport', TRANSPORT)
transport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)


def sources(q):
    if q < 1 or q % 2 != 1:
        raise ValueError('q must be positive and odd')
    return ((1 << (6*q + 1)) - 11)//3, (3*pow(81, q) - 11)//8


def integer_hash(n):
    return hashlib.sha256(n.to_bytes((n.bit_length()+7)//8, 'big')).hexdigest()


def word_hash(word):
    # Unambiguous encoding even for exponents exceeding 255.
    return hashlib.sha256(','.join(map(str, word)).encode('ascii')).hexdigest()


def evaluate(q, cap_multiplier=16, cap_constant=256):
    n, z = sources(q)
    x, a_sum, peak, low = z, 0, z, z
    word = []
    cap = cap_multiplier*q + cap_constant
    while x >= n and len(word) < cap:
        low = min(low, x)
        numerator = 3*x + 1
        exponent = (numerator & -numerator).bit_length() - 1
        x = numerator >> exponent
        word.append(exponent)
        a_sum += exponent
        peak = max(peak, x)
    k = len(word)
    resolved = x < n
    pz = pow(3, k)*z
    # Reconstruct the affine correction independently at the endpoint.
    correction = (x << a_sum) - pz
    assert correction >= 0 and (k == 0 or correction > 0)
    # For every pre-passage iterate y>=low, product bound gives
    # homogeneous part >= y*(1-j/(3*n)).  low>=n+k and k<2*n
    # certify that the homogeneous threshold cannot have crossed earlier.
    prefix_certificate = resolved and (k == 0 or (k < 2*n and low >= n+k))
    rational_certificate = resolved and (k == 0 or (
        k < 3*n and 3*pz < ((3*n-k) << a_sum)))
    # Fall back to direct homogeneous tracking when the cheap certificate fails.
    coefficient_time = None
    if prefix_certificate:
        coefficient_time = k
    else:
        homogeneous_numerator, total_a = z, 0
        if z < n:
            coefficient_time = 0
        for j, exponent in enumerate(word, 1):
            homogeneous_numerator *= 3
            total_a += exponent
            if coefficient_time is None and homogeneous_numerator < (n << total_a):
                coefficient_time = j
    if resolved and k:
        assert word[0] >= 2
        assert 3**(k + 4*q + 2) < 1 << (a_sum + 6*q + 4)
        assert q < 3*a_sum and q < 1 << a_sum
        assert q <= 3*(a_sum-k)
    row = {
        'q': q, 'status': 'descended' if resolved else 'censored',
        'steps_observed': k, 'tau': k if resolved else None,
        'exponent_sum': a_sum, 'cap': cap,
        'coefficient_time': coefficient_time,
        'coefficient_delay': k-coefficient_time if resolved else None,
        'prefix_gap_certificate': prefix_certificate,
        'rational_descent_certificate': rational_certificate,
        'minimal_parameter_certificate': resolved and k > 0,
        'source_bits': n.bit_length(), 'burst_bits': z.bit_length(),
        'peak_bits': peak.bit_length(), 'endpoint_bits': x.bit_length(),
        'prepassage_gap_bits': (low-n).bit_length() if k else None,
        'word_sha256': word_hash(word), 'endpoint_sha256': integer_hash(x),
    }
    return row, word


def parameters(grid_max, extended):
    cohorts = {}
    def add(q, tag):
        cohorts.setdefault(q, set()).add(tag)
    for q in range(1, grid_max+1, 2):
        add(q, 'exhaustive')
    adversarial = []
    if extended:
        for h in range(10, 17):
            for sign in (-1, 1):
                add((1 << h)+sign, 'power_of_two_neighbor')
        rng = random.Random(20260924)
        for q in rng.sample(range(8193, 65536, 2), 24):
            add(q, 'seeded_sample')
        for length in range(4, 17):
            root, bits = transport.word_root(1, 'C', (2,)+(1,)*length)
            for lift in (0, 1, 2):
                q = root + (lift << bits)
                if q <= 65537:
                    add(q, 'prescribed_growth_prefix')
                    adversarial.append({'q': q, 'ones': length, 'root': root,
                                        'modulus_exponent': bits, 'lift': lift})
    return cohorts, adversarial


def ratio(row):
    return Fraction(row['tau'], row['q'])


def candidate_tests(rows):
    tests = []
    for bound in map(Fraction, ('1', '3/2', '2', '5/2', '3', '4')):
        violations, unknown = [], []
        for row in rows:
            if row['status'] == 'descended':
                if ratio(row) > bound:
                    violations.append(row['q'])
            elif row['steps_observed'] >= bound.numerator*row['q']//bound.denominator:
                # Every observed iterate, including the last, is >=n.
                # Hence tau>steps_observed; this can already refute a bound.
                violations.append(row['q'])
            else:
                unknown.append(row['q'])
        tests.append({'tau_over_q_bound': str(bound), 'violations': len(violations),
                      'first_violations': violations[:20],
                      'unknown_due_to_censoring': len(unknown)})
    return tests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=HERE)
    parser.add_argument('--grid-max', type=int, default=8191)
    parser.add_argument('--no-extended', action='store_true')
    args = parser.parse_args()
    if args.grid_max < 1:
        parser.error('--grid-max must be positive')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cohorts, adversarial = parameters(args.grid_max, not args.no_extended)
    rows, records, selected_words = [], [], {}
    best = Fraction(-1)
    for index, q in enumerate(sorted(cohorts), 1):
        row, word = evaluate(q)
        row['cohorts'] = '|'.join(sorted(cohorts[q]))
        rows.append(row)
        if row['status'] == 'descended' and ratio(row) > best:
            best = ratio(row)
            records.append({'q': q, 'tau': row['tau'], 'ratio': str(best)})
            selected_words[str(q)] = word
        if q in (1, 3, 5, 11, 31, 127):
            selected_words[str(q)] = word
        if index % 512 == 0 or index == len(cohorts):
            print(json.dumps({'cases_done': index, 'cases_total': len(cohorts),
                              'q': q, 'censored': sum(r['status'] == 'censored' for r in rows)}), flush=True)
    csv_path = args.output_dir/'descent_cases.csv'
    with csv_path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    resolved = [r for r in rows if r['status'] == 'descended']
    grid = [r for r in rows if 'exhaustive' in r['cohorts']]
    bound_tests = candidate_tests(rows)
    bins = []
    for bits in range(1, args.grid_max.bit_length()+1):
        group = [r for r in grid if r['q'].bit_length() == bits and r['tau'] is not None]
        if group:
            worst = max(group, key=ratio)
            bins.append({'q_min': min(r['q'] for r in group),
                         'q_max': max(r['q'] for r in group), 'count': len(group),
                         'sum_tau_over_sum_q': str(Fraction(sum(r['tau'] for r in group), sum(r['q'] for r in group))),
                         'max_ratio': str(ratio(worst)), 'worst_q': worst['q']})
    summary = {
        'scope': 'Bounded exact experiment; no universal descent or novelty claim',
        'grid_max': args.grid_max, 'exhaustive_odd_parameters': len(grid),
        'extended_enabled': not args.no_extended, 'seed': 20260924,
        'total_distinct_parameters': len(rows), 'max_parameter': max(cohorts),
        'total_syracuse_steps': sum(r['steps_observed'] for r in rows),
        'descended': len(resolved),
        'censored_parameters': [r['q'] for r in rows if r['status'] == 'censored'],
        'record_ratios': records,
        'largest_ratios': [{k:r[k] for k in ('q','tau','exponent_sum','cohorts')} for r in sorted(resolved, key=ratio, reverse=True)[:16]],
        'bound_tests': bound_tests, 'dyadic_bins': bins,
        'coefficient_delay_cases': [r['q'] for r in resolved if r['coefficient_delay'] != 0],
        'prefix_certificate_failures': [r['q'] for r in resolved if not r['prefix_gap_certificate']],
        'rational_certificate_failures': [r['q'] for r in resolved if not r['rational_descent_certificate']],
        'csv_sha256': hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        'limitations': [
            'The cap 16*q+256 censors unresolved cases; none is inferred to diverge.',
            'The time is counted from z(q), against n(q), not from z(q) against itself.',
            'The q=1 case already lies below the threshold, so tau=0.',
            'A finite maximum does not establish a uniform linear bound.',
            'No independence or natural-density assertion for the sparse source family.',
            'The Python implementation is not extracted from Lean or formally verified.'
        ],
    }
    witnesses = {'words': selected_words, 'prescribed_prefix_parameters': adversarial}
    for name, data in [('descent_summary.json', summary), ('descent_witnesses.json', witnesses)]:
        (args.output_dir/name).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('total_distinct_parameters','total_syracuse_steps','descended','censored_parameters','record_ratios','coefficient_delay_cases')}, indent=2))


if __name__ == '__main__':
    main()
