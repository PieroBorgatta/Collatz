#!/usr/bin/env python3
"""Exact checks of last-exponent transport; no new source census.

AI-assisted development: Codex with Piero Borgatta, 2026-09-26.
Fixed checks: adversarial family k=1..7, signed fiber j=0..4,
and ternary residue permutations k=1..6. Infinite claims have paper proofs.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse(word, target):
    require(target > 0 and target % 2 == 1, "positive odd target")
    node = target
    for exponent in reversed(word):
        require(exponent >= 1, "positive exponent")
        numerator = (node << exponent) - 1
        require(numerator % 3 == 0, "inverse integrality")
        node = numerator // 3
        require(node > 0 and node % 2 == 1, "positive odd inverse")
    return node


def replay(word, source):
    node = source
    for exponent in word:
        numerator = 3 * node + 1
        actual = (numerator & -numerator).bit_length() - 1
        require(actual == exponent, "actual valuation differs")
        node = numerator >> actual
    return node


def constant(word):
    result = 0
    prefix_sum = 0
    for index, exponent in enumerate(word):
        result += 3 ** (len(word) - index - 1) * 2 ** prefix_sum
        prefix_sum += exponent
    return result


def checked_transport(word, n, y, delta):
    k, total = len(word), sum(word)
    require(k > 0 and word[-1] + delta >= 1, "admissible signed correction")
    require(pow(2, delta, 3**k) * y % (3**k) == n % (3**k), "target congruence")
    changed = word[:-1] + [word[-1] + delta]
    source, transported = inverse(word, n), inverse(changed, y)
    require(replay(word, source) == n, "old exact replay")
    require(replay(changed, transported) == y, "new exact replay")
    offset = constant(word)
    require(offset == constant(changed), "last exponent changed the constant")
    require(3**k * transported + offset == 2**(total + delta) * y,
            "new affine identity")
    if delta >= 0:
        q, remainder = divmod(2**delta * y - n, 3**k)
        require(remainder == 0 and q > 0, "positive correction quotient")
        require(transported == source + 2**total * q, "source transport identity")
        require(n * transported > (n + 3**k) * source, "strict height cost")
    return source, transported, changed


def run():
    rows = []
    for k in range(1, 8):
        modulus = 3**k
        n = (-5 * pow(14, -1, modulus)) % modulus
        if n % 2 == 0:
            n += modulus
        y, period = 16*n + 5, 2*3**(k-1)
        node = (2*n - 1) // 3
        inverse_exponents = [1]
        for _ in range(k-1):
            for exponent in range(1, 7):
                candidate, remainder = divmod((node << exponent) - 1, 3)
                if remainder == 0 and candidate > 0 and candidate % 3:
                    node = candidate
                    inverse_exponents.append(exponent)
                    break
            else:
                raise RuntimeError("no continuing inverse exponent")
        word = list(reversed(inverse_exponents))
        delta = period - 1
        require(n % 3 == 2 and 0 < n < 2*modulus, "bad-family domain")
        require((14*n + 5) % modulus == 0, "bad-family residue")
        require(all(pow(2, d, modulus) * y % modulus != n % modulus
                    for d in range(delta)), "correction not minimal")
        source, transported, _ = checked_transport(word, n, y, delta)
        rows.append({"k": k, "n": n, "y": y, "word": word,
                     "source": source, "period": period, "minimum_delta": delta,
                     "transported_source_bits": transported.bit_length(),
                     "transported_source_sha256": hashlib.sha256(
                         str(transported).encode()).hexdigest()})

    # Signed optimization collapses infinitely many last exponents.
    # These five representatives also independently check negative shifts.
    fibers = []
    for j in range(5):
        a = 1 + 6*j
        source, transported, changed = checked_transport([1, a], 17, 277, 5 - 6*j)
        require(changed == [1, 6] and transported == 3939, "signed fiber")
        fibers.append({"last_exponent": a, "source": source,
                       "delta": 5 - 6*j, "image": transported})
    weights = [Fraction(9, 2**(2+6*j)) for j in range(5)]
    ratio = Fraction(1, 64)
    require(sum(weights) == weights[0] * (1-ratio**5)/(1-ratio),
            "exact geometric fiber sum")

    # The two sibling formulas permute their entire ternary residue classes.
    permutations = []
    for k in range(1, 7):
        modulus, period = 3**k, 2*3**(k-1)
        logarithms = {pow(2, d, modulus): d for d in range(period)}
        require(len(logarithms) == period, "multiplicative order")
        for residue, multiplier, offset in ((1, 4, 1), (2, 16, 5)):
            deltas = []
            for n in range(residue, modulus, 3):
                y = multiplier*n + offset
                deltas.append(logarithms[n * pow(y, -1, modulus) % modulus])
            require(sorted(deltas) == list(range(1, period, 2)),
                    "odd-logarithm permutation")
        permutations.append({"k": k, "modulus": modulus,
                             "residues_per_class": 3**(k-1), "passed": True})
    return {"scope": "finite exact arithmetic checks, not basin-density evidence",
            "bad_family": rows, "signed_fiber": fibers,
            "residue_permutations": permutations}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: 7 adversarial words, 5 signed fiber cases, 12 residue permutations.")
