#!/usr/bin/env python3
"""Exact finite probes of capped threshold allocation.

Synthetic finite profiles only: this script supplies no Collatz mass estimate.
The Lean statements are in CollatzShadowing/CapacityAllocation.lean.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def bound(scores, cap, demand, threshold):
    hinge = sum((max(h - threshold, F(0)) for h in scores), F(0))
    return max(demand - cap * hinge, F(0)) / threshold


def encoded(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def run():
    profiles = checks = exact_threshold_checks = 0
    score_values = tuple(map(F, (0, 1, 3, 10)))
    coefficients = (F(0), F(1, 2), F(1))
    thresholds = (F(1, 2), F(1), F(2), F(3), F(10), F(11))
    for size in range(1, 4):
        for scores in product(score_values, repeat=size):
            for allocation in product(coefficients, repeat=size):
                mass = sum((c * h for c, h in zip(allocation, scores)), F(0))
                count = sum(allocation, F(0))
                profiles += 1
                for threshold in thresholds:
                    for demand in (F(0), mass / 2, mass):
                        require(bound(scores, F(1), demand, threshold) <= count,
                                "threshold lower bound")
                        checks += 1
                    is_threshold = all(
                        (h <= threshold or c == 1) and
                        (h >= threshold or c == 0)
                        for c, h in zip(allocation, scores)
                    )
                    if is_threshold:
                        require(bound(scores, F(1), mass, threshold) == count,
                                "threshold saturation, including ties")
                        exact_threshold_checks += 1

    scores = (F(10), F(1), F(1))
    allocation = (F(1), F(1), F(1))
    demand = F(12)
    threshold = F(1)
    improved = bound(scores, F(1), demand, threshold)
    uniform = demand / max(scores)
    require(improved == F(3) and improved > uniform,
            "strict improvement over maximum-score conversion")
    require(improved == sum(allocation), "full allocation attains threshold")
    partial = (F(1), F(1, 2), F(0))
    partial_demand = F(21, 2)
    partial_bound = bound(scores, F(1), partial_demand, threshold)
    require(partial_bound == sum(partial) == F(3, 2),
            "partial allocation and threshold ties")

    # Dropping the aggregate capacity is invalid, even though an individual
    # code might have unit coefficient before duplicate labels are grouped.
    bad_scores, bad_allocation = (F(10), F(1)), (F(2), F(0))
    bad_demand = F(20)
    invalid_bound = bound(bad_scores, F(1), bad_demand, F(1))
    require(invalid_bound > sum(bad_allocation), "missing cap counterexample")

    # Distinct labels can still name the same physical cell. Their total
    # coefficient is two and cannot be treated as a physical-cell cap of one.
    duplicate_physical_cells = (7, 7)
    require(len(set(duplicate_physical_cells)) == 1 and
            sum((F(1), F(1))) == 2, "duplicate-label diagnostic")

    return {
        "status": "PASS",
        "scope": "finite synthetic allocation; no analytic Collatz input",
        "profiles_checked": profiles,
        "lower_bound_checks": checks,
        "exact_threshold_checks": exact_threshold_checks,
        "strict_improvement": {
            "scores": [encoded(x) for x in scores],
            "allocation": [encoded(x) for x in allocation],
            "demand": encoded(demand),
            "threshold": encoded(threshold),
            "hinge_bound": encoded(improved),
            "uniform_maximum_bound": encoded(uniform),
            "improvement_factor": encoded(improved / uniform),
            "integer_count_bound_from_hinge": 3,
            "integer_count_bound_from_uniform_maximum": 2,
        },
        "partial_threshold_certificate": {
            "allocation": [encoded(x) for x in partial],
            "demand": encoded(partial_demand),
            "attained_bound": encoded(partial_bound),
        },
        "missing_cap_counterexample": {
            "demand": encoded(bad_demand),
            "incorrect_bound_with_cap_one": encoded(invalid_bound),
            "actual_allocation": encoded(sum(bad_allocation)),
        },
        "duplicate_labels_are_not_distinct_cells": True,
    }


if __name__ == "__main__":
    result = json.dumps(run(), ensure_ascii=False, indent=2) + "\n"
    destination = Path(__file__).resolve().parents[1] / "verification/s05_capacity.json"
    destination.write_text(result)
    print(result, end="")
