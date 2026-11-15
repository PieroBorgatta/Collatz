#!/usr/bin/env python3
"""Exact fixed-target census of balanced two-exponent Syracuse surgery.

The domain and caps below were fixed before executing the census.  This is
a finite experiment on odd sources, not an asymptotic density estimate.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import json

TARGETS = (5, 7, 31, 593)
CUTOFFS = (1024, 4096, 16384, 65536)
DELTAS = (-5, -3, -1, 1, 3, 5)
HEIGHT_FACTORS = (1, 4, 16, 64)
MAX_STEPS = 2048


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


@lru_cache(maxsize=None)
def step(n):
    require(n > 0 and n % 2 == 1, "odd positive source")
    numerator = 3 * n + 1
    power = numerator & -numerator
    return numerator // power, power.bit_length() - 1


def sibling(n):
    return 4 * n + 1 if n % 3 == 1 else 16 * n + 5


def valuation3(n):
    require(n != 0, "distinct odd targets cannot be dyadic multiples")
    n = abs(n)
    result = 0
    while n % 3 == 0:
        n //= 3
        result += 1
    return result


def first_word(source, target):
    n, word = source, []
    for _ in range(MAX_STEPS):
        if n == target:
            return tuple(word)
        if n == 1:
            return None
        n, exponent = step(n)
        word.append(exponent)
    raise RuntimeError(("trajectory cap reached", source, target))


def word_const(word):
    result, partial = 0, 0
    for exponent in word:
        result = 3 * result + (1 << partial)
        partial += exponent
    return result


def replay(source, word):
    n = source
    for exponent in word:
        n, actual = step(n)
        require(actual == exponent, "nonexact modified word")
    return n


def run():
    targets = []
    totals = Counter()
    for target in TARGETS:
        upper_target = sibling(target)
        bounds = {
            delta: valuation3(upper_target - (1 << delta) * target)
            if delta > 0 else valuation3((1 << -delta) * upper_target - target)
            for delta in DELTAS
        }
        sources, accepted = [], []
        failures = Counter()
        for source in range(1, max(CUTOFFS) + 1, 2):
            word = first_word(source, target)
            if word is None:
                continue
            k, total = len(word), sum(word)
            sources.append((source, k))
            totals["base_odd_sources"] += 1
            if k < 2:
                continue
            old_constant = word_const(word)
            power2, power3 = 1 << total, 3 ** k
            require(power3 * source + old_constant == power2 * target,
                    "original affine identity")
            suffix_constants = [0] * (k + 1)
            for index in range(k - 1, -1, -1):
                suffix_constants[index] = (3 ** (k - 1 - index)
                                           + (1 << word[index]) * suffix_constants[index + 1])
            partials = []
            partial = 0
            for exponent in word:
                partial += exponent
                partials.append(partial)
            for delta in DELTAS:
                for index in range(k - 1):
                    if word[index] + delta < 1 or word[-1] - delta < 1:
                        continue
                    totals["positive_exponent_edits"] += 1
                    # i=index+1 is the number of exponents through the edit.
                    tail_depth = k - index - 1
                    if tail_depth > bounds[delta]:
                        failures["necessary_tail_congruence"] += 1
                        continue
                    totals["necessary_tail_congruence_pass"] += 1
                    prefix_sum = partials[index]
                    suffix_constant = suffix_constants[index + 1]
                    if delta > 0:
                        difference = ((1 << delta) - 1) * (1 << prefix_sum) * suffix_constant
                    else:
                        d = -delta
                        difference = -((1 << d) - 1) * (1 << (prefix_sum - d)) * suffix_constant
                    new_constant = old_constant + difference
                    numerator = power2 * upper_target - new_constant
                    if numerator <= 0:
                        failures["nonpositive_source"] += 1
                        continue
                    if numerator % power3:
                        failures["full_ternary_congruence"] += 1
                        continue
                    image = numerator // power3
                    require(image % 2 == 1, "odd transported source")
                    modified = list(word)
                    modified[index] += delta
                    modified[-1] -= delta
                    require(sum(modified) == total, "sum preserved")
                    require(word_const(modified) == new_constant, "constant-shift formula")
                    require(replay(image, modified) == upper_target, "modified endpoint")
                    # This checks the necessary congruence independently.
                    necessary = (upper_target - (1 << delta) * target) if delta > 0 else (
                        (1 << -delta) * upper_target - target)
                    require(necessary % (3 ** tail_depth) == 0, "tail obstruction")
                    accepted.append((source, image, k, index + 1, delta))
                    totals["actual_transport_codes"] += 1
        rows = []
        for cutoff in CUTOFFS:
            base = [(u, depth) for u, depth in sources if u <= cutoff]
            codes = [code for code in accepted if code[0] <= cutoff]
            physical_pairs = {(u, v) for u, v, *_ in codes}
            image_load = Counter(v for u, v in physical_pairs)
            label_load = Counter(v for u, v, *_ in codes)
            height_rows = []
            for factor in HEIGHT_FACTORS:
                bounded = [code for code in codes if code[1] <= factor * code[0]]
                pairs = {(u, v) for u, v, *_ in bounded}
                load = Counter(v for u, v in pairs)
                covered = {u for u, _ in pairs}
                height_rows.append({
                    "factor": factor,
                    "codes": len(bounded),
                    "distinct_pairs": len(pairs),
                    "covered_odd_sources": len(covered),
                    "coverage_fraction": str(Fraction(len(covered), len(base))) if base else "0",
                    "distinct_odd_images": len(load),
                    "max_distinct_source_load": max(load.values(), default=0),
                    "max_successful_depth": max((code[2] for code in bounded), default=0),
                })
            rows.append({
                "cutoff": cutoff,
                "base_odd_sources": len(base),
                "base_depth_histogram": dict(sorted(Counter(d for _, d in base).items())),
                "transport_codes": len(codes),
                "physical_pairs": len(physical_pairs),
                "distinct_odd_images": len(image_load),
                "max_distinct_source_load": max(image_load.values(), default=0),
                "max_label_load": max(label_load.values(), default=0),
                "successful_depth_histogram": dict(sorted(Counter(code[2] for code in codes).items())),
                "minimum_expansion": str(min((Fraction(v, u) for u, v, *_ in codes), default=Fraction(0))),
                "maximum_expansion": str(max((Fraction(v, u) for u, v, *_ in codes), default=Fraction(0))),
                "height_caps": height_rows,
            })
        by_image = {}
        for code in accepted:
            by_image.setdefault(code[1], []).append(code)
        collisions = [
            {"image": image, "sources": sorted({code[0] for code in codes}),
             "codes": codes}
            for image, codes in sorted(by_image.items())
            if len({code[0] for code in codes}) > 1
        ][:3]
        targets.append({"target": target, "sibling": upper_target,
                        "maximum_tail_depth_per_delta": bounds,
                        "failures": dict(failures), "rows": rows,
                        "first_ten_witnesses": accepted[:10],
                        "collision_witnesses": collisions})
    return {"status": "PASS", "scope": "finite odd-source census, first arrival",
            "domain": {"targets": TARGETS, "cutoffs": CUTOFFS,
                       "deltas": DELTAS, "height_factors": HEIGHT_FACTORS,
                       "max_steps": MAX_STEPS},
            "totals": dict(totals), "results": targets,
            "asymptotic_density_claim": False, "H_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
