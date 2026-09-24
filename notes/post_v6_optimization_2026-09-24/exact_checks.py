#!/usr/bin/env python3
"""Exact finite consistency checks; not substitutes for the universal Lean proofs."""
from fractions import Fraction
from math import isqrt
from pathlib import Path
import json


def root(r, k):
    return (4**k * (3*r + 1) - 1) // 3


def syracuse(n):
    t = 3*n + 1
    return t // (t & -t)


def conductor(T, C):
    budget = 88*T*C
    lo, hi = 1, budget + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if budget <= mid**6:
            hi = mid
        else:
            lo = mid + 1
    return lo


def run():
    seed_cases = 0
    for a in range(1, 41):
        if a % 3 == 0:
            continue
        r = (4*a)//3 if a % 3 == 1 else (2*a)//3
        for b in range(13):
            for q in range(5):
                Q, B = 3**q, 2*b
                T = root(2*a, B + 2*Q)
                assert B + 2*Q < (16**b + 3)*Q
                for p in range(Q):
                    shift = B//Q + int(p <= B % Q)
                    k = p + shift*Q
                    x, y = root(r, k), root(r, k + Q)
                    assert B < k <= B + Q and k + Q <= B + 2*Q
                    assert 16**b < x < y <= T
                    assert x % 2 == y % 2 == 1
                    assert x % Q == y % Q == root(r, p) % Q
                    assert syracuse(x) == syracuse(y)
                    seed_cases += 1
    conductor_cases = 0
    for T in range(1001):
        for C in range(31):
            m, budget = conductor(T, C), 88*T*C
            assert m >= 1 and budget <= m**6
            assert m == 1 or (m-1)**6 < budget
            assert m <= isqrt(budget) + 1 <= budget + 1 <= 132*T*C + 1
            # Exact real square-budget identity, represented rationally.
            D = Fraction(2*C, 3*m**4)
            assert 88*T*D <= Fraction(2*m*m, 3)
            conductor_cases += 1
    a, b, q, C = 2, 1, 1, 1
    Q = 3**q
    newT = root(2*a, 2*b + 2*Q)
    oldT = root(2*a, (16**b + 3)*Q)
    newm, oldm = conductor(newT, C), 132*oldT*C + 1
    assert newT < oldT and newm < oldm
    result = {
        'seed_cases': seed_cases,
        'seed_range': {'a': [1, 40], 'exclude_multiples_of_3': True,
                       'b': [0, 12], 'q': [0, 4], 'p': 'all residues'},
        'conductor_cases': conductor_cases,
        'conductor_range': {'T': [0, 1000], 'C': [0, 30]},
        'all_checks_passed': True,
        'floating_point_used': False,
        'universal_proof': False,
        'nonreturn_property_computationally_decided': False,
        'illustrative_arithmetic_only': {
            'a': a, 'b': b, 'q': q, 'C': C,
            'new_T': newT, 'old_T': oldT, 'new_m': newm, 'old_m': oldm,
            'new_coefficient': str(Fraction(3, 256*newT*3**newm)),
            'public_analytic_parameters': False,
            'note': 'b=1 and C=1 are arithmetic examples, not the public theorem parameters.'
        }
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
