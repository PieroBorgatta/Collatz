#!/usr/bin/env python3
"""Finite small-level part of the first-separation obstruction.

The infinite tail uses Chim's external theorem and an informal derivation
in RESULTS_IT.md. This script does not prove that external theorem.
"""
import json
from pathlib import Path
import argparse
from fractions import Fraction

from modular_certificate import initial_residue
from verify_certificates import recurrence_residue

HERE = Path(__file__).resolve().parent


def first_separation(v, bits=256):
    if not 5 <= v <= 36 or bits <= v+2:
        raise ValueError('require 5<=v<=36 and bits>v+2')
    values = [initial_residue(j,bits) for j in (v,v+1)]
    assert values == [recurrence_residue(j,bits) for j in (v,v+1)]
    remaining, total, word = bits, 0, []
    while True:
        nums = [3*x+1 for x in values]
        exponents = [(x & -x).bit_length()-1 for x in nums]
        if max(exponents) >= remaining:
            raise ValueError('insufficient precision to determine both exponents')
        if exponents[0] != exponents[1]:
            assert min(exponents)+total == v+2
            break
        a = exponents[0]
        word.append(a)
        total += a
        remaining -= a
        values = [(x >> a) & ((1 << remaining)-1) for x in nums]
    checks = []
    for j,a in zip((v,v+1),exponents):
        divisions = total+a
        # Q_j/N_j > 3*2^(2-j)*(9/8)^(2^j), (9/8)^6>2.
        # Thus the post-separation endpoint/N_j is strictly greater than
        # 3^(len(word)+2) / 2^deficit. Negative deficit is automatic.
        deficit = j+divisions-((1 << j)//6)-2
        power3 = 3**(len(word)+2)
        lower_bound_above_one = deficit <= 0 or power3 > 2**deficit
        assert lower_bound_above_one
        checks.append({'level':j,'exponent':a,'total_divisions':divisions,
            'power_of_three':len(word)+2,'power_of_two_deficit':deficit,
            'endpoint_strictly_above_source':True})
    return {'lower_level':v,'precision_bits':bits,'common_word':word,
            'common_sum':total,'branches':checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'separation_results.json')
    args = parser.parse_args()
    assert 9**6 > 2*8**6
    # Conservative arithmetic using 0.69<ln2<0.70 and ln3<1.10.
    upper_coefficient = 8500*(2*Fraction(70,100)+Fraction(485,100))*Fraction(110,100)/Fraction(69,100)**3
    upper_cutoff = 180*(2*Fraction(70,100)+Fraction(485,100))*Fraction(70,100)
    assert upper_coefficient < 180000 and upper_cutoff < 800
    polynomial = 450000*(37+2)*(37+803)
    assert 6*polynomial < 2**37
    rows = [first_separation(v) for v in range(5,37)]
    result = {'scope':'Finite part plus arithmetic threshold; the infinite tail depends on Chim 2025.',
        'finite_pair_range':[5,36],'pairs':len(rows),'branches':2*len(rows),
        'all_endpoints_strictly_above_own_source':True,
        'tail_threshold':{'v':37,'valuation_upper_bound':polynomial,
            'six_times_bound':6*polynomial,'power_of_two':2**37,
            'base_inequality_passed':True,
            'induction_identity':'2*(v+2)*(v+803)-(v+3)*(v+804)=v^2+803v+800>0'},
        'rounding_checks':{'coefficient_upper_bound':str(upper_coefficient),
            'cutoff_upper_bound':str(upper_cutoff),'passed':True},
        'rows':rows,
        'limitations':['The external logarithmic-form theorem is not machine-proved here.',
            'The finite modular calculations do not prove the infinite tail by themselves.',
            'Later steps are not controlled by this obstruction.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['finite_pair_range','pairs','branches','tail_threshold']}))


if __name__ == '__main__':
    main()
