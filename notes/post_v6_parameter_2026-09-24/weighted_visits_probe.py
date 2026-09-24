#!/usr/bin/env python3
"""Exact rational sanity checks of the weighted occupation identity.

The universal proof is telescoping, not this finite enumeration.
Hits are indexed by distinct times; arbitrary duplicated words are not allowed.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path


def check_orbit(x, steps):
    n = x
    weight = Fraction(1)
    deposit = Fraction(0)
    visits = defaultdict(Fraction)
    for _ in range(steps + 1):
        visits[n] += weight
        term = weight / (n * (3 * n + 1))
        numerator = 3 * n + 1
        a = (numerator & -numerator).bit_length() - 1
        successor = numerator >> a
        next_weight = weight * Fraction(3, 1 << a)
        assert weight / n - next_weight / successor == term
        assert term > 0
        deposit += term
        n, weight = successor, next_weight
    assert deposit == Fraction(1, x) - weight / n
    assert deposit < Fraction(1, x)
    for target, total in visits.items():
        assert total <= Fraction(target * (3 * target + 1), x)
    if x == 1:
        assert visits[1] == 4 * (1 - Fraction(3, 4) ** (steps + 1))
    return len(visits)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-seed", type=int, default=1999)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("weighted_visits_results.json"))
    args = parser.parse_args()
    if args.max_seed < 1 or args.steps < 0:
        parser.error("require max-seed >= 1 and steps >= 0")
    seeds = range(1, args.max_seed + 1, 2)
    target_checks = sum(check_orbit(x, args.steps) for x in seeds)
    result = {
        "scope": "Finite exact rational checks; proof is the telescoping identity",
        "seeds": len(seeds),
        "max_seed": args.max_seed,
        "last_visit_time": args.steps,
        "one_step_identities_checked": len(seeds) * (args.steps + 1),
        "distinct_source_target_bounds_checked": target_checks,
        "sharp_target_one_geometric_sum_checked": True,
        "all_checks_passed": True,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
