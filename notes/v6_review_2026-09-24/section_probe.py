#!/usr/bin/env python3
"""Exact finite checks for the marked-episode section proposed in the v6 review.

The universal coverage theorem is a deduction from Monks et al. (2013),
Theorem 6.4, NOT a consequence of this finite diagnostic.
An episode excludes its odd source and includes its next odd endpoint.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path

PORTS = ((1, 4, 13, 18), (3, 8, 53, 72), (7, 7, 853, 1152),
         (9, 2, 3413, 4608), (13, 1, 54613, 73728),
         (15, 5, 218453, 294912))


def valuation(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def section(n):
    return any(n % modulus == residue for _, _, residue, modulus in PORTS)


def syracuse(n):
    numerator = 3 * n + 1
    return numerator >> valuation(numerator)


def episode_hit(n):
    numerator = 3 * n + 1
    return any((numerator >> j) % 27 == 20
               for j in range(1, valuation(numerator) + 1))


def first_outcome(n, cap=10000):
    path = [n]
    for _ in range(cap):
        n = syracuse(n)
        path.append(n)
        if n == 1:
            return {"kind": "hits_one", "path": path}
        if section(n):
            return {"kind": "section_return", "path": path}
    return {"kind": "unresolved_at_cap", "cap": cap, "path": path}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=1000000)
    parser.add_argument('--output', default=str(Path(__file__).with_name('section_results.json')))
    args = parser.parse_args()
    assert args.limit > 1
    order = next(k for k in range(1, 19) if pow(2, k, 27) == 1)
    assert order == 18
    candidates = [(j, ((20 * 2**j - 1) // 3) % 9) for j in range(1, 19, 2)]
    assert [(j, r) for j, r in candidates if r % 3] == [(j, r) for j, r, _, _ in PORTS]
    for j, r, residue, modulus in PORTS:
        assert modulus == 9 * 2**j
        assert 0 <= residue < modulus and residue % 2 == 1
        assert residue % 9 == r and (3 * residue + 1) % 2**j == 0
    assert len({r for _, r, _, _ in PORTS}) == len(PORTS)
    density = sum((Fraction(1, m) for _, _, _, m in PORTS), Fraction(0))
    assert density == Fraction(6935, 98304)
    checked = 0
    for n in range(1, args.limit, 2):
        if n % 3 == 0:
            continue
        a = valuation(3 * n + 1)
        ports_match = any(n % 9 == r and a >= j for j, r, _, _ in PORTS)
        assert section(n) == ports_match == episode_hit(n), n
        checked += 1
    # Guards against two tempting incorrect formulations.
    assert 47 % 27 == 20 and not section(47) and not episode_hit(47)
    terminal = first_outcome(13)
    assert terminal == {"kind": "hits_one", "path": [13, 5, 1]}
    increasing = first_outcome(31)
    assert increasing == {"kind": "section_return", "path": [31, 47, 71, 107, 161, 121]}
    assert section(31) and section(121)
    # Coefficient identities prove a whole infinite one-step return family:
    # n=661+1152t -> 31+54t, both in port 1, t>=0.
    assert 3 * 661 + 1 == 64 * 31
    assert 3 * 1152 == 64 * 54
    assert 661 % 18 == 31 % 18 == 13
    assert 1152 % 18 == 54 % 18 == 0
    assert 31 % 2 == 1 and 54 % 2 == 0
    assert 661 > 31 and 1152 > 54
    tower_section_checks = 0
    for k in range(4, 2001, 2):
        n = (2**(k + 1) - 11) // 3
        assert valuation(3 * n + 1) == 1
        assert section(n) == (k % 18 == 10)
        if section(n):
            assert syracuse(n) % 27 == 20
            tower_section_checks += 1
    result = {
        "claim_type": "finite arithmetic diagnostic, not a proof of universal coverage or Collatz",
        "episode_convention": "(u,S(u)] excludes source, includes endpoint",
        "limit_exclusive": args.limit, "admissible_odd_sources_checked": checked,
        "mismatches": 0, "order_of_two_mod_27": order,
        "ports": [{"j": j, "residue_mod_9": r, "residue": c, "modulus": m}
                  for j, r, c, m in PORTS],
        "density_all_positive": str(density), "density_relative_to_odds": str(2 * density),
        "increasing_first_return": increasing, "nonreturning_convergent_source": terminal,
        "infinite_one_step_return_family": {
            "source": "661+1152t", "destination": "31+54t", "parameter": "integer t>=0",
            "exact_exponent": 6, "proof": "integer coefficient identities and odd destination",
            "formalization_status": "paper-level, not Lean"},
        "tower_section_members_tested": tower_section_checks,
        "tower_membership": "for even k>=4: n_k in E iff k=10 mod18"
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
