#!/usr/bin/env python3
"""One bounded exact audit of minimum unit seeds; not an asymptotic test."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
TARGET = 593
MAXIMUM_SEED = 6325
MAXIMUM_LENGTH = 10000
MAXIMUM_BITS = 1024


def fail(message):
    raise RuntimeError(message)


def trajectory(start):
    states = [start]
    exponents = []
    seen = {start}
    while states[-1] != 1:
        x = states[-1]
        numerator = 3 * x + 1
        divisor = numerator & -numerator
        exponent = divisor.bit_length() - 1
        y = numerator // divisor
        if exponent < 1 or y < 1 or y % 2 != 1:
            fail('invalid accelerated step')
        if 2 ** exponent * y != 3 * x + 1:
            fail('affine step mismatch')
        if len(exponents) >= MAXIMUM_LENGTH or y.bit_length() > MAXIMUM_BITS:
            fail('unresolved bounded trajectory')
        if y in seen and y != 1:
            fail('cycle before1; cannot certify absent hits')
        exponents.append(exponent)
        states.append(y)
        seen.add(y)
    return states, exponents


def main():
    root_states, root_exponents = trajectory(TARGET)
    if root_states.count(TARGET) != 1:
        fail('target return before1')
    branches = {}
    counts = {}
    empty = []
    sources = 0
    steps = 0
    longest = 0
    bits = 0
    hit_sources = 0
    for seed in range(1, MAXIMUM_SEED + 1, 2):
        if seed % 3 == 0:
            continue
        sources += 1
        states, exponents = trajectory(seed)
        steps += len(exponents)
        longest = max(longest, len(exponents))
        bits = max(bits, max(x.bit_length() for x in states))
        if TARGET not in states:
            continue
        hit_sources += 1
        k = states.index(TARGET)
        if k == 0:
            empty.append(seed)
            continue
        parent = states[k - 1]
        exponent = exponents[k - 1]
        if parent % 3 == 0:
            fail('unit seed reached nonunit parent')
        if 3 * parent + 1 != 2 ** exponent * TARGET:
            fail('last-parent mismatch')
        counts[parent] = counts.get(parent, 0) + 1
        if parent not in branches:
            weight = Fraction(3 ** k, 2 ** sum(exponents[:k]))
            inflation = Fraction(TARGET, seed) / weight
            product = Fraction(1)
            for x in states[:k]:
                product *= Fraction(3 * x + 1, 3 * x)
            if inflation != product or inflation < 1:
                fail('product/weight mismatch')
            branches[parent] = {
                'minimum_unit_seed_in_scanned_domain': seed,
                'last_parent': parent,
                'last_exponent': exponent,
                'length': k,
                'total_valuation': sum(exponents[:k]),
                'states_to_first_hit': states[:k + 1],
                'exponents': exponents[:k],
                'homogeneous_weight': {'numerator': weight.numerator,
                                       'denominator': weight.denominator},
                'exact_inflation': {'numerator': inflation.numerator,
                                    'denominator': inflation.denominator},
            }
    ordered = sorted(branches.values(), key=lambda x: x['minimum_unit_seed_in_scanned_domain'])
    for record in ordered:
        record['hit_sources_in_branch'] = counts[record['last_parent']]
    labels = [r['minimum_unit_seed_in_scanned_domain'] for r in ordered]
    harmonic = sum((Fraction(1, u) for u in labels), Fraction(0))
    harmonic_minus_best = harmonic - (max((Fraction(1, u) for u in labels), default=Fraction(0)))
    data = {
        'status': 'PASS',
        'target': TARGET,
        'maximum_seed': MAXIMUM_SEED,
        'source_domain': 'odd positive integers not divisible by3',
        'certified_sources_to_one': sources,
        'direct_steps': steps,
        'maximum_length_to_one': longest,
        'maximum_state_bits': bits,
        'target_states_to_one': root_states,
        'target_exponents_to_one': root_exponents,
        'target_has_positive_return': False,
        'hit_sources_including_empty': hit_sources,
        'empty_arrival_sources': empty,
        'branches': ordered,
        'minimum_second_parent_seed': labels[1] if len(labels) >= 2 else None,
        'harmonic_seed_mass_minus_best': {'numerator': harmonic_minus_best.numerator,
                                          'denominator': harmonic_minus_best.denominator},
        'unresolved_sources': 0,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'protocol_sha256': hashlib.sha256((HERE / 'protocol.json').read_bytes()).hexdigest(),
        'scope': 'Exact finite minimum-label and witness certificate only; no claim about limiting Doob probabilities or logarithmic asymptotic seed bounds.',
    }
    print(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
