#!/usr/bin/env python3
"""Exact finite checks of three observations in the November review.

These checks support the arithmetic replay; universal statements require
the symbolic arguments in the reports and are not new Lean theorems.
"""

from fractions import Fraction
from math import gcd, prod
import json


def syracuse(n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("positive odd source required")
    numerator = 3 * n + 1
    power = numerator & -numerator
    return numerator // power, power.bit_length() - 1


def section(n):
    return any(n % modulus == residue for residue, modulus in (
        (13, 18), (53, 72), (853, 1152), (3413, 4608),
        (54613, 73728), (218453, 294912),
    ))


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def check_returns():
    checked = 0
    for r in range(1, 9):
        for t in range(1, 6):
            for j in range(r):
                x = 18 * t * 8 ** (r - j) * 9 ** j - 5
                y = 216 * t * 8 ** (r - j - 1) * 9 ** j - 7
                z = 18 * t * 8 ** (r - j - 1) * 9 ** (j + 1) - 5
                require(syracuse(x) == (y, 1), "first step")
                require(syracuse(y) == (z, 2), "second step")
                require(section(x) and section(z) and not section(y), "first return")
                require(x < y and x < z, "growth")
                require(z - x == 18 * t * 8 ** (r - j - 1) * 9 ** j,
                        "increment")
                checked += 1
    return {"pairs_checked": checked, "r": [1, 8], "t": [1, 5]}


def check_dissipation():
    checked = 0
    for source in range(1, 200, 2):
        current, weight, accumulated = source, Fraction(1), Fraction(0)
        for _ in range(32):
            endpoint, exponent = syracuse(current)
            next_weight = weight * Fraction(3, 2 ** exponent)
            loss = weight / (current * (3 * current + 1))
            require(weight / current - next_weight / endpoint == loss,
                    "dissipation identity")
            accumulated += loss
            require(accumulated + next_weight / endpoint == Fraction(1, source),
                    "telescoping identity")
            require(accumulated <= Fraction(1, source), "shared budget")
            current, weight = endpoint, next_weight
            checked += 1
    return {"identities_checked": checked, "odd_sources": 100, "steps_per_source": 32}


def check_factors():
    for v in range(1, 8):
        factors = [(9 ** (2 ** j) + 1) // 2 for j in range(v)]
        require(prod(factors) == (9 ** (2 ** v) - 1) // (2 ** (v + 3)),
                "tower factorization")
        require(all(f > 1 and f % 2 == 1 for f in factors), "odd factors")
        require(all(gcd(factors[i], factors[j]) == 1
                    for i in range(v) for j in range(i)), "coprime factors")
    return {"levels_checked": 7, "v": [1, 7]}


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "finite_checks_only": True,
                      "returns": check_returns(),
                      "dissipation": check_dissipation(),
                      "factorization": check_factors()}, indent=2))
