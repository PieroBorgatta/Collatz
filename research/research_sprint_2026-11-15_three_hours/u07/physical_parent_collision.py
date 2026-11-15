#!/usr/bin/env python3
"""One registered finite physical parent diagnostic; no limiting-law claim."""

from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math


HERE = Path(__file__).resolve().parent
PROTOCOL = json.loads((HERE / 'diagnostic_protocol.json').read_text())
MAXIMUM = PROTOCOL['maximum_source']
CUTOFFS = tuple(PROTOCOL['cutoffs'])
TARGETS = tuple(PROTOCOL['targets'])
TARGET_SET = set(TARGETS)
STEP_LIMIT = PROTOCOL['termination_policy']['step_limit']
CDF_FILE = HERE.parent / 'u03' / 'physical_cdf_result.json'
CDF = json.loads(CDF_FILE.read_text())


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def rat(x):
    x = Fraction(x)
    return {'numerator': x.numerator, 'denominator': x.denominator}


expected = {}
for pair in CDF['pairs']:
    for row in pair['cutoff_counts']:
        expected[pair['n'], row['cutoff']] = row['base_odd']
        expected[pair['y'], row['cutoff']] = row['image_odd']


def fresh():
    return {'count': 0, 'zero_count': 0, 'leaf_count': 0,
            'unit_count': 0, 'zero_mass': Fraction(0),
            'leaf_mass': Fraction(0), 'unit_mass': Fraction(0),
            'unit_hist': defaultdict(Fraction),
            'unit_hist_count': defaultdict(int),
            'unit_exponent': {}}


states = {n: fresh() for n in TARGETS}
rows = []
direct_steps = 0
source_count = 0
maximum_state_bits = 1
maximum_length = 0
maximum_total = 0
last_parent_checks = 0
potential_checks = 0


def snapshot(limit):
    for n in TARGETS:
        s = states[n]
        require(s['count'] == expected[n, limit], 'U03 catalogue count mismatch')
        require(s['count'] == s['zero_count'] + s['leaf_count'] + s['unit_count'],
                'Source partition mismatch')
        total = s['unit_mass']
        hist = s['unit_hist']
        require(sum(hist.values(), Fraction(0)) == total, 'Mass partition mismatch')
        out = {'target': n, 'cutoff': limit,
               'all_first_hit_sources': s['count'],
               'zero_arrival_sources': s['zero_count'],
               'nonunit_last_parent_sources': s['leaf_count'],
               'unit_last_parent_sources': s['unit_count'],
               'zero_arrival_weight': rat(s['zero_mass']),
               'nonunit_last_parent_weight': rat(s['leaf_mass']),
               'unit_last_parent_weight': rat(total)}
        if not total:
            require(s['unit_count'] == 0, 'Zero weight with positive unit count')
            out['unit_parent_law'] = None
            rows.append(out)
            continue
        law = {x: mass / total for x, mass in hist.items()}
        require(sum(law.values(), Fraction(0)) == 1, 'Parent law not normalized')
        collision = sum((p * p for p in law.values()), Fraction(0))
        diversity = 1 - collision
        require(0 <= collision <= 1, 'Invalid collision')
        dominant = max(law, key=lambda x: (law[x], -x))
        dominant_p = law[dominant]
        require(diversity <= 2 * (1 - dominant_p), 'Diversity/defect inequality')
        natural_total = s['unit_count']
        natural_collision = sum((Fraction(c, natural_total) ** 2
                                 for c in s['unit_hist_count'].values()), Fraction(0))
        entropy = -sum(float(p) * (math.log(p.numerator) - math.log(p.denominator))
                       for p in law.values())
        out['unit_parent_law'] = {
            'number_of_parents': len(law),
            'dominant_parent': dominant,
            'dominant_probability': rat(dominant_p),
            'collision': rat(collision),
            'diversity': rat(diversity),
            'unweighted_collision': rat(natural_collision),
            'Shannon_nats_float_diagnostic_only': entropy,
            'H2_nats_float_diagnostic_only': -math.log(float(collision)),
            'parents': [
                {'parent': x, 'last_exponent': s['unit_exponent'][x],
                 'source_count': s['unit_hist_count'][x],
                 'weight': rat(hist[x]), 'probability': rat(law[x])}
                for x in sorted(law)
            ]}
        rows.append(out)


for u in range(1, MAXIMUM + 1, 2):
    x, k, total = u, 0, 0
    previous, last_exponent = None, None
    seen = set()
    hits = set()
    while True:
        require(x > 0 and x % 2 == 1, 'Positive odd domain violated')
        require(x not in seen, 'Unexpected cycle; completeness prohibited')
        seen.add(x)
        maximum_state_bits = max(maximum_state_bits, x.bit_length())
        if x in TARGET_SET and x not in hits:
            n = x
            hits.add(n)
            s = states[n]
            s['count'] += 1
            numerator = u * 3 ** k
            denominator = n * (1 << total)
            require(0 < numerator <= denominator, 'Affine potential outside (0,1]')
            weight = Fraction(numerator, denominator)
            potential_checks += 1
            if k == 0:
                require(u == n and previous is None, 'Invalid empty arrival')
                s['zero_count'] += 1
                s['zero_mass'] += weight
            else:
                require(previous is not None and last_exponent is not None,
                        'Missing last-parent witness')
                require((1 << last_exponent) * n == 3 * previous + 1,
                        'Last-parent affine identity failed')
                last_parent_checks += 1
                if previous % 3 == 0:
                    require(k == 1 and u == previous,
                            'A nonunit last parent has a nontrivial odd ancestor')
                    s['leaf_count'] += 1
                    s['leaf_mass'] += weight
                else:
                    s['unit_count'] += 1
                    s['unit_mass'] += weight
                    s['unit_hist'][previous] += weight
                    s['unit_hist_count'][previous] += 1
                    if previous in s['unit_exponent']:
                        require(s['unit_exponent'][previous] == last_exponent,
                                'One parent has two exponents')
                    s['unit_exponent'][previous] = last_exponent
        if x == 1:
            break
        require(k < STEP_LIMIT, 'Timeout; completeness prohibited')
        z = 3 * x + 1
        a = (z & -z).bit_length() - 1
        require(a >= 1, 'Nonpositive valuation')
        previous, last_exponent = x, a
        x = z >> a
        k += 1
        total += a
        direct_steps += 1
    source_count += 1
    maximum_length = max(maximum_length, k)
    maximum_total = max(maximum_total, total)
    if u + 1 in CUTOFFS:
        snapshot(u + 1)

require(source_count == MAXIMUM // 2, 'Wrong source count')
require(len(rows) == len(CUTOFFS) * len(TARGETS), 'Wrong row count')
require(direct_steps == CDF['direct_forward_steps'], 'Forward step count mismatch')
for row in rows:
    if row['target'] == 593 and row['cutoff'] == MAXIMUM:
        require(any(p['parent'] == 395 for p in row['unit_parent_law']['parents']),
                'Registered parent395 not observed')

result = {
    'status': 'PASS',
    'scope': 'Finite first-arrival weighted parent frontiers only; no limiting law, lower, H or Collatz claim.',
    'maximum_source': MAXIMUM,
    'odd_sources_certified_to_one': source_count,
    'direct_forward_steps': direct_steps,
    'maximum_direct_state_bits': maximum_state_bits,
    'maximum_length_to_one': maximum_length,
    'maximum_total_valuation_to_one': maximum_total,
    'potential_checks': potential_checks,
    'last_parent_checks': last_parent_checks,
    'all_counts_match_U03': True,
    'unresolved_sources': [],
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'protocol_sha256': hashlib.sha256((HERE / 'diagnostic_protocol.json').read_bytes()).hexdigest(),
    'U03_result_sha256': hashlib.sha256(CDF_FILE.read_bytes()).hexdigest(),
    'rows': rows}
print(json.dumps(result, sort_keys=True, indent=2))
