#!/usr/bin/env python3
"""Exact finite arithmetic replay of rotation identities; not cycle exclusion."""

from itertools import product
from math import gcd
import json


def constant(word):
    # Independent expanded formula, rather than the Lean head recursion.
    prefix = 0
    c = 0
    for j, a in enumerate(word):
        c += 3 ** (len(word) - 1 - j) * 2 ** prefix
        prefix += a
    return c


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    checked = 0
    closed = []
    for length in range(1, 7):
        for word in product(range(1, 5), repeat=length):
            a = word[0]
            rotated = word[1:] + word[:1]
            d = 2 ** sum(word) - 3 ** length
            c, cr = constant(word), constant(rotated)
            require(2 ** a * cr == 3 * c + d, "rotation")
            require(gcd(d, 6) == 1, "denominator coprime to six")
            require(gcd(d, c) == gcd(d, cr), "gcd invariance")
            if d > 0 and c % d == 0:
                source = c // d
                state = source
                for exponent in word:
                    numerator = 3 * state + 1
                    two_power = numerator & -numerator
                    require(two_power == 2 ** exponent, "exact cycle valuation")
                    state = numerator // two_power
                require(state == source, "closure")
                closed.append({"word": list(word), "source": source})
            checked += 1
    return {"status": "PASS", "scope": {"length": [1, 6], "exponents": [1, 4]},
            "words_checked": checked, "positive_closed_words": closed,
            "finite_check_only": True}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
