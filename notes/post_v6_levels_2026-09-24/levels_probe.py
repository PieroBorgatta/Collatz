#!/usr/bin/env python3
"""Exact checks of level recurrence, finite precision, and residual descent.

The modular part never constructs the huge integers represented by high v.
Only the explicitly bounded actual-level sweep constructs complete integers.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def valuation(n):
    if n <= 0:
        raise ValueError('positive input required')
    return (n & -n).bit_length()-1


def step(n):
    numerator = 3*n+1
    a = valuation(numerator)
    return numerator >> a, a


def quotient(v):
    if v < 1:
        raise ValueError('v must be positive')
    return (pow(9, 1 << v)-1) >> (v+3)


def quotient_mod(v, bits):
    return (pow(9, 1 << v, 1 << (v+3+bits))-1) >> (v+3)


def level_residues(levels, bits):
    mask = (1 << bits)-1
    q = 5 & mask
    values = {1:q}
    for v in range(1, levels+1):
        q = (q + (q*q << (v+2))) & mask
        values[v+1] = q
    return values


def common_prefix(x, y, v):
    """Use v+3 bits; the larger divergent exponent is only a lower bound."""
    bits = v+3
    mask = (1 << bits)-1
    x, y = x & mask, y & mask
    if valuation((y-x) & mask) != v+2:
        raise ValueError('pair does not have the required exact precision')
    word, total = [], 0
    while True:
        nx, ny = 3*x+1, 3*y+1
        ax, ay = min(valuation(nx), bits), min(valuation(ny), bits)
        if ax != ay:
            m = min(ax, ay)
            assert total+m == v+2 and max(ax,ay) == bits
            return {'v':v, 'common_steps':len(word), 'common_sum':total,
                    'smaller_divergent_exponent':m,
                    'larger_divergent_exponent_at_least':m+1,
                    'larger_branch':'current' if ax>ay else 'higher',
                    'word':word}
        assert ax < bits-1
        word.append(ax)
        total += ax
        bits -= ax
        mask = (1 << bits)-1
        x, y = (nx >> ax)&mask, (ny >> ay)&mask


def limit_from_recurrence(bits):
    anchor = max(1, bits-2)
    return level_residues(anchor-1, bits)[anchor]


def limit_from_log_series(bits):
    modulus = 1 << bits
    total = 0
    # log(9)/8 = sum (-1)^(j+1) * 2^(3j-3) / j in Q_2.
    # For j>bits, valuation >=2*j-2 >=bits: omitted terms vanish.
    for j in range(1, bits+1):
        t = valuation(j)
        power = 3*j-3-t
        if power < bits:
            term = ((1 << power)*pow(j >> t, -1, modulus)) % modulus
            total += term if j%2 else -term
    return total % modulus


def certified_prefix(residue, bits):
    word = []
    residue %= 1 << bits
    while bits > 0:
        numerator = 3*residue+1
        a = valuation(numerator)
        if a >= bits:
            break  # The exact valuation is unknown at this precision.
        word.append(a)
        bits -= a
        residue = (numerator >> a) % (1 << bits)
    return word, bits


def actual_case(v, pair, cap=None):
    if v < 5:
        raise ValueError('the source family starts at v=5')
    q = (1 << (v-1))-1
    n = ((1 << (3*(1 << v)-5))-11)//3
    z = (3*pow(81,q)-11)//8
    expected = quotient(v)
    bridge_word = []
    for _ in range(3):
        z,a = step(z)
        bridge_word.append(a)
        assert z > n
    assert bridge_word == [2,2,v-4] and z == expected and z > 6*n
    if v >= 6:
        assert z > (n << (v+1))
    y = z
    for a in pair['word']:
        y,actual = step(y)
        assert actual == a and y > n
    y1,a1 = step(y)
    other = quotient(v+1)
    for a in pair['word']:
        other,actual = step(other)
        assert actual == a
    _,a2 = step(other)
    assert a1 != a2 and min(a1,a2) == pair['smaller_divergent_exponent']
    assert ('current' if a1>a2 else 'higher') == pair['larger_branch']
    k, total, y = 0, 0, z
    cap = 8*(1 << v) if cap is None else cap
    digest = hashlib.sha256()
    while y >= n and k < cap:
        y,a = step(y)
        digest.update(f'{a},'.encode('ascii'))
        k += 1
        total += a
    resolved = y < n
    if resolved:
        assert k > pair['common_steps']
    return {'v':v, 'q':q, 'status':'descended' if resolved else 'censored',
            'tau_from_Q':k if resolved else None, 'steps_observed':k,
            'exponent_sum':total, 'cap':cap, 'source_bits':n.bit_length(),
            'Q_bits':z.bit_length(), 'common_steps':pair['common_steps'],
            'common_sum':pair['common_sum'], 'divergent_exponents':[a1,a2],
            'word_sha256':digest.hexdigest()}


def compare_previous(row, old):
    """Compare exact stopping times or compatible censored observations.

    The previous experiment starts three steps earlier, at z_q. Exponent
    sums can only be compared if both observations end at the same step.
    """
    new_end = row['steps_observed']+3
    old_end = int(old['steps_observed'])
    new_resolved = row['status'] == 'descended'
    old_resolved = old['status'] == 'descended'
    if new_resolved and old_resolved:
        assert row['tau_from_Q']+3 == int(old['tau'])
        assert new_end == old_end
    elif new_resolved:
        assert new_end > old_end
    elif old_resolved:
        assert int(old['tau']) > new_end
    if new_end == old_end:
        assert row['exponent_sum']+row['v'] == int(old['exponent_sum'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=HERE)
    parser.add_argument('--levels', type=int, default=512)
    parser.add_argument('--precision', type=int, default=4096)
    parser.add_argument('--actual-max-v', type=int, default=18)
    args = parser.parse_args()
    if not 5 <= args.actual_max_v <= args.levels or args.precision < args.levels+3:
        parser.error('require 5<=actual-max-v<=levels and precision>=levels+3')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    residues = level_residues(args.levels, args.precision)
    pairs = [common_prefix(residues[v],residues[v+1],v) for v in range(1,args.levels+1)]
    direct_levels = sorted(v for v in
        {1,2,3,5,16,args.levels//2,args.levels,args.levels+1}
        if 1 <= v <= args.levels+1)
    for v in direct_levels:
        assert residues[v] == quotient_mod(v,args.precision)
    limit = limit_from_recurrence(args.precision)
    assert limit == limit_from_log_series(args.precision)
    assert limit == quotient_mod(max(1,args.precision-2),args.precision)
    word, remaining = certified_prefix(limit,args.precision)
    for pair in pairs:
        v = pair['v']
        assert valuation((limit-residues[v]) % (1 << args.precision)) == v+2
        prefix_sum, count = 0, 0
        for a in word:
            if prefix_sum+a > v+1:
                break
            prefix_sum += a
            count += 1
        assert pair['word'] == word[:count] and pair['common_sum'] == prefix_sum
    actual = []
    for v in range(5,args.actual_max_v+1):
        row = actual_case(v,pairs[v-1])
        actual.append(row)
        print(json.dumps(row),flush=True)
    previous_path = HERE.parent/'post_v6_descent_2026-09-24/descent_cases.csv'
    with previous_path.open() as stream:
        previous = {int(r['q']):r for r in csv.DictReader(stream)}
    overlaps = 0
    for row in actual:
        old = previous.get(row['q'])
        if old:
            compare_previous(row,old)
            overlaps += 1
    result = {
        'scope':'Finite exact checks supporting informal proofs; no infinite-family descent claim',
        'all_checks_passed':True,'modular_level_pairs':len(pairs),
        'direct_modular_power_checks':len(direct_levels),'precision_bits':args.precision,
        'three_limit_computations_agree':True,'certified_limit_prefix_steps':len(word),
        'certified_limit_prefix_sum':sum(word),'remaining_precision_bits':remaining,
        'actual_cases':actual,'actual_steps':sum(r['steps_observed'] for r in actual),
        'censored_levels':[r['v'] for r in actual if r['status']=='censored'],
        'previous_experiment_overlap':overlaps,
        'pairs':pairs,
        'limitations':['High modular levels are not full natural-number orbit tests.',
                      'The larger divergent exponent is a lower bound in the modular records.',
                      'The finite log-series comparison does not prove transcendence.',
                      'Mahler is a separately cited classical input, not a Lean-checked dependency.',
                      'The stopping-time cap is censoring, not a divergence test.']}
    (args.output_dir/'levels_results.json').write_text(json.dumps(result,indent=2)+'\n')
    prefix = {'precision_bits':args.precision,'word':word,'sum':sum(word),
              'remaining_bits':remaining,'next_exponent_at_least':remaining,
              'residue_hex':hex(limit),'scope':'Certified finite prefix, not an infinite natural orbit'}
    (args.output_dir/'limit_prefix.json').write_text(json.dumps(prefix,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('modular_level_pairs','certified_limit_prefix_steps',
        'certified_limit_prefix_sum','actual_steps','censored_levels','previous_experiment_overlap')},indent=2))


if __name__ == '__main__':
    main()
