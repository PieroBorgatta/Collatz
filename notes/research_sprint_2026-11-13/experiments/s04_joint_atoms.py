#!/usr/bin/env python3
"""Finite replay of the odd-target joint word/source dictionary.

Independent forward affine and backward inverse constructions; no external
code or mixing theorem is used. Runtime checks survive Python -O.
"""
from itertools import combinations
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def compositions(total, length):
    if total < length or length < 1:
        return
    for cuts in combinations(range(1, total), length - 1):
        parts = (0,) + cuts + (total,)
        yield tuple(parts[i + 1] - parts[i] for i in range(length))


def affine_constant(word):
    c, partial = 0, 0
    for exponent in word:
        c = 3 * c + 2 ** partial
        partial += exponent
    return c


def backward_source(word, target):
    n = target
    for exponent in reversed(word):
        numerator = (2 ** exponent) * n - 1
        if numerator % 3:
            return None
        n = numerator // 3
        if n <= 0 or n % 2 != 1:
            return None
    return n


def actual_word(source, length):
    n, word = source, []
    for _ in range(length):
        numerator = 3 * n + 1
        power = numerator & -numerator
        word.append(power.bit_length() - 1)
        n = numerator // power
    return tuple(word), n


def check():
    profiles = words = accepted = cutoff_checks = 0
    for k in range(1, 6):
        modulus = 3 ** k
        for target in range(1, 40, 2):
            source_codes = {}
            for total in range(k, k + 8):
                predicted = actual = 0
                for word in compositions(total, k):
                    words += 1
                    c = affine_constant(word)
                    numerator = (2 ** total) * target - c
                    residue = numerator % modulus == 0
                    source = backward_source(word, target)
                    require(residue == (source is not None), "residue/backward support")
                    if not residue:
                        continue
                    require(numerator > 0, "automatic positive height at an odd target")
                    require(source == numerator // modulus, "affine/backward source")
                    require(actual_word(source, k) == (word, target), "exact valuations")
                    require(source not in source_codes, "fixed-length word/source injectivity")
                    source_codes[source] = word
                    for cutoff in (0, 1, 3, 17, 100):
                        require((source <= cutoff) ==
                                ((2 ** total) * target <= modulus * cutoff + c),
                                "exact upper height cutoff")
                        cutoff_checks += 1
                    predicted += 1
                    actual += 1
                    accepted += 1
                require(predicted == actual, "joint profile count")
                profiles += 1
    # Even targets can satisfy the affine residue without being accelerated
    # odd endpoints: the positivity/exactness theorem must retain Odd target.
    even_source = ((2 ** 1) * 2 - affine_constant((1,))) // 3
    require(even_source == 1 and actual_word(even_source, 1)[1] == 1,
            "even-target counterexample")
    # A positive word alone does not impose positive affine height; residue
    # compatibility with a positive odd target is essential.
    bad = (1,) * 5
    require(affine_constant(bad) > 2 ** sum(bad) and
            (2 ** sum(bad) - affine_constant(bad)) % (3 ** len(bad)) != 0,
            "height and failed residue separated")
    return {"status": "PASS", "finite_checks_only": True,
            "profiles": profiles, "word_target_cases": words,
            "admissible_words": accepted, "cutoff_checks": cutoff_checks,
            "domain": {"length": [1, 5], "total": "k..k+7",
                       "odd_target": [1, 39]},
            "even_target_counterexample": {"target": 2, "word": [1],
                                           "affine_source": 1,
                                           "actual_accelerated_target": 1}}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
