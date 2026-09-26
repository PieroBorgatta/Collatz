#!/usr/bin/env python3
"""Exact finite checks of signed transport inequalities, not a density test.

AI-assisted development: Codex with Piero Borgatta, 2026-09-26.
All inverse words with exponents 1..6 and depths 1..5 are considered for
six fixed target pairs; final corrections range from 1-a_k through 24.
Additional infinite-fiber representatives test larger negative shifts.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse(word, target):
    node = target
    for exponent in reversed(word):
        require(exponent > 0, "nonpositive exponent")
        node, remainder = divmod((1 << exponent) * node - 1, 3)
        require(remainder == 0 and node > 0 and node % 2 == 1, "invalid inverse")
    return node


def actual_replay(word, source):
    node = source
    for exponent in word:
        numerator = 3 * node + 1
        valuation = (numerator & -numerator).bit_length() - 1
        require(exponent == valuation, "prescribed exponent is not actual")
        node = numerator >> valuation
    return node


def verify(word, u, n, y, delta):
    changed = word[:-1] + [word[-1] + delta]
    v = inverse(changed, y)
    require(actual_replay(word, u) == n, "original replay")
    require(actual_replay(changed, v) == y, "changed replay")
    k, A = len(word), sum(word)
    C = 2**A * n - 3**k * u
    require(C > 0 and 3**k*v + C == 2**(A+delta)*y, "shared affine offset")
    r = F(2)**delta * F(y, n)
    require(F(v) == r*u + (r-1)*F(C, 3**k), "signed ratio identity")
    if r >= 1:
        require(v >= r*u, "expansion bound")
    else:
        require(v <= r*u, "compression bound")
    if delta >= 0:
        difference = 2**delta*y - n
        representative_bound = max(n, 2**delta*y)
    else:
        difference = y - 2**(-delta)*n
        representative_bound = max(y, 2**(-delta)*n)
    require(difference != 0 and difference % 3**k == 0, "nonzero ternary difference")
    require(3**k <= abs(difference) <= representative_bound, "bounded-shift exclusion")
    return v, r


def run():
    pairs = ((5, 85), (7, 29), (11, 181), (13, 53), (17, 277), (5, 17))
    records, examples = [], []
    for n, y in pairs:
        frontier = [(n, [])]
        for k in range(1, 6):
            next_frontier = []
            for node, inverse_word in frontier:
                for exponent in range(1, 7):
                    child, rem = divmod((node << exponent)-1, 3)
                    if rem == 0 and child > 0:
                        next_frontier.append((child, inverse_word + [exponent]))
            frontier = next_frontier
            row = {"n": n, "y": y, "depth": k, "inverse_words": len(frontier),
                   "valid_shifts": 0, "positive_shifts": 0, "negative_shifts": 0,
                   "zero_shifts": 0, "expanding": 0, "compressing": 0}
            for u, inverse_word in frontier:
                word = list(reversed(inverse_word))
                for delta in range(1-word[-1], 25):
                    if pow(2, delta, 3**k)*y % (3**k) != n % (3**k):
                        continue
                    v, r = verify(word, u, n, y, delta)
                    row["valid_shifts"] += 1
                    row["positive_shifts" if delta > 0 else
                        "negative_shifts" if delta < 0 else "zero_shifts"] += 1
                    row["expanding" if r >= 1 else "compressing"] += 1
                    if delta < 0 and len(examples) < 8:
                        examples.append({"n": n, "y": y, "word": word,
                                         "delta": delta, "source": u, "image_odd_part": v})
            records.append(row)
    fibers = []
    for j in range(5):
        word = [1, 1+6*j]
        source = inverse(word, 17)
        image, ratio = verify(word, source, 17, 277, 5-6*j)
        require(image == 3939, "signed fiber no longer agrees")
        fibers.append({"word": word, "delta": 5-6*j, "source": source,
                       "image_odd_part": image,
                       "scale_numerator": ratio.numerator,
                       "scale_denominator": ratio.denominator})

    # Check the image-counting split directly on integers, independently
    # of Collatz or the affine identities: arbitrary dyadic factors allowed.
    dyadic_cases = 0
    for cutoff in (31, 64, 127, 256):
        for odd_bound in (1, 3, 8, 25):
            images = {z for z in range(1, cutoff+1)
                      if z // (z & -z) <= odd_bound}
            for Fmax in range(5):
                bound = (Fmax+1)*odd_bound + F(cutoff, 2**(Fmax+1))
                require(len(images) <= bound, "distinct dyadic-image bound")
                dyadic_cases += 1
    return {"scope": "finite exact arithmetic, not asymptotic evidence",
            "word_checks": records, "negative_examples": examples,
            "colliding_fiber": fibers, "dyadic_counting_cases": dyadic_cases,
            "total_valid_shifts": sum(row["valid_shifts"] for row in records),
            "source_census_expanded": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(f"PASS: {result['total_valid_shifts']} signed word transports, "
          f"5 fiber representatives, {result['dyadic_counting_cases']} dyadic counting cases.")
