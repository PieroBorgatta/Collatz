#!/usr/bin/env python3
"""Finite modular certificates of descent for the Q_v tower family.

No floating point, full Q_v, or full natural-number orbit is required.
A failed certificate is inconclusive. Mathematical sufficiency is explained
in RESULTS_IT.md; this program is not a Lean proof.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NUM, DEN = 485, 306


def precision_for(v, budget):
    if v < 5 or not 1 <= budget <= 1 << v:
        raise ValueError('require v>=5 and 1<=budget<=2^v')
    assert 3**DEN < 2**NUM
    return (NUM*budget+(2*NUM-3*DEN)*(1 << v)+DEN-1)//DEN


def initial_residue(v, bits):
    """Q_v modulo 2^bits via modular exponentiation only."""
    modulus = 1 << (bits+v+3)
    return (pow(9,1 << v,modulus)-1) >> (v+3)


@lru_cache(maxsize=None)
def block_table(width):
    """T^width(n)=(3^odd*n+C)/2^width for n congruent to residue."""
    if not 1 <= width <= 16:
        raise ValueError('block width must be between 1 and 16')
    table = []
    for residue in range(1 << width):
        x, odd = residue, 0
        for _ in range(width):
            if x & 1:
                x = (3*x+1) >> 1
                odd += 1
            else:
                x >>= 1
        multiplier = 3**odd
        constant = (x << width)-multiplier*residue
        assert constant >= 0
        table.append((odd,multiplier,constant))
    return table


def parity_count(residue, bits, width=16):
    """Count odd steps of T in exactly bits binary divisions.

    Only bits input bits are known. The final Syracuse exponent can be
    incomplete: the sum of the actual exponents is then >=bits, not =bits.
    """
    if bits < 1 or not 0 <= residue < 1 << bits:
        raise ValueError('require positive precision and a residue in range')
    if not 1 <= width <= 16:
        raise ValueError('block width must be between 1 and 16')
    remaining, odd_count, blocks = bits, 0, 0
    mask = (1 << bits)-1
    digest = hashlib.sha256()
    while remaining:
        take = min(width,remaining)
        low = residue & ((1 << take)-1)
        odd,multiplier,constant = block_table(take)[low]
        digest.update(bytes([take]))
        digest.update(low.to_bytes((take+7)//8,'little'))
        odd_count += odd
        remaining -= take
        mask >>= take
        residue = ((multiplier*residue+constant) >> take) & mask
        blocks += 1
    return odd_count, blocks, digest.hexdigest()


def certificate(v, budget, width=16):
    bits = precision_for(v,budget)
    residue = initial_residue(v,bits)
    digest = hashlib.sha256(residue.to_bytes((bits+7)//8,'little')).hexdigest()
    odd_count,blocks,trace = parity_count(residue,bits,width)
    passed = odd_count <= budget
    return {'v':v,'M':1 << v,'budget':budget,'precision_bits':bits,
            'odd_steps':odd_count,'certified':passed,
            'descent_time_upper_bound':odd_count if passed else None,
            'block_width':width,'blocks':blocks,
            'initial_residue_sha256':digest,'block_trace_sha256':trace,
            'scope':'Sufficient certificate only; failure is inconclusive.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-v',type=int,default=21)
    parser.add_argument('--block-width',type=int,default=16)
    parser.add_argument('--output-dir',type=Path,default=HERE)
    args = parser.parse_args()
    if args.max_v < 5 or not 1 <= args.block_width <= 16:
        parser.error('require max-v>=5 and 1<=block-width<=16')
    rows = []
    for v in range(5,args.max_v+1):
        attempts = [certificate(v,1 << (v-1),args.block_width)]
        if not attempts[0]['certified']:
            attempts.append(certificate(v,1 << v,args.block_width))
        row = {'v':v,'attempts':attempts,'certified':attempts[-1]['certified']}
        rows.append(row)
        print(json.dumps(row),flush=True)
    old_path = HERE.parent/'post_v6_levels_2026-09-24/levels_results.json'
    old = json.loads(old_path.read_text())
    overlaps = 0
    for actual in old['actual_cases']:
        row = next((r for r in rows if r['v']==actual['v']),None)
        if row is None or actual['status']!='descended':
            continue
        for attempt in row['attempts']:
            if attempt['certified']:
                assert actual['tau_from_Q'] <= attempt['descent_time_upper_bound']
        overlaps += 1
    result = {
        'scope':'Finite modular certificates, not a uniform theorem for all levels.',
        'rational_upper_bound':{'numerator':NUM,'denominator':DEN,
            'verified_integer_inequality':f'3^{DEN}<2^{NUM}'},
        'minimum_v':5,'maximum_v':args.max_v,'levels':len(rows),
        'certified_levels':[r['v'] for r in rows if r['certified']],
        'inconclusive_levels':[r['v'] for r in rows if not r['certified']],
        'first_budget_failures':[r['v'] for r in rows if not r['attempts'][0]['certified']],
        'previous_full_orbit_overlap':overlaps,
        'total_modular_binary_steps':sum(a['precision_bits'] for r in rows for a in r['attempts']),
        'total_counted_odd_steps':sum(a['odd_steps'] for r in rows for a in r['attempts']),
        'rows':rows,
        'limitations':['Only the listed finite levels are certified.',
            'A certificate gives an upper bound, not the exact first descent time.',
            'A failed budget is inconclusive, not a failure of descent.',
            'These are modular computations, not complete natural-number orbits.',
            'No claim of novelty or Lean formalization is made.']}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'certificate_results.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
