#!/usr/bin/env python3
"""Preserve dyadic factors in the frozen finite profile matching.

This supplementary check changes no target, cutoff, dilation or matching.
It counts ordinary sources rather than unweighted odd parts.
"""

import hashlib
import json
import root_profile_transport as profile


def ordinary_reaches(source, target):
    value = source
    for _ in range(20000):
        if value == target:
            return True
        if value == 1:
            return False
        value = value // 2 if value % 2 == 0 else 3 * value + 1
    raise RuntimeError("incomplete ordinary replay")


def lifts(source, cutoff):
    result = []
    value = source
    while value <= cutoff:
        result.append(value)
        value *= 2
    return result


def run():
    bound = max(profile.CUTOFFS) * max(profile.DILATIONS)
    _, edges = profile.graph(bound)
    rows, independent_sources = [], 0
    for target in profile.TARGETS:
        upper = profile.sibling(target)
        full_base = profile.groups(target, max(profile.CUTOFFS), edges)
        full_images = profile.groups(upper, bound, edges)
        for cutoff in profile.CUTOFFS:
            base = {p: [u for u in values if u <= cutoff] for p, values in full_base.items()}
            base = {p: values for p, values in base.items() if values}
            ordinary_base = sum(len(lifts(u, cutoff)) for values in base.values() for u in values)
            if cutoff == min(profile.CUTOFFS):
                direct = sum(ordinary_reaches(u, target) for u in range(1, cutoff + 1))
                profile.require(direct == ordinary_base, "ordinary base-count mismatch")
                independent_sources += cutoff
            for dilation in profile.DILATIONS:
                images = {p: [v for v in values if v <= dilation * cutoff]
                          for p, values in full_images.items()}
                pairs = profile.match(base, images, dilation)
                ordinary_pairs = []
                for source, image, _ in pairs:
                    for exponent, ordinary_source in enumerate(lifts(source, cutoff)):
                        ordinary_image = image * 2 ** exponent
                        profile.require(ordinary_image <= dilation * cutoff, "ordinary height")
                        if cutoff == min(profile.CUTOFFS):
                            profile.require(ordinary_reaches(ordinary_source, target), "source path")
                            profile.require(ordinary_reaches(ordinary_image, upper), "image path")
                        ordinary_pairs.append((ordinary_source, ordinary_image))
                profile.require(len({a for a, _ in ordinary_pairs}) == len(ordinary_pairs),
                                "ordinary source collision")
                profile.require(len({b for _, b in ordinary_pairs}) == len(ordinary_pairs),
                                "ordinary image collision")
                rows.append({"n": target, "y": upper, "X": cutoff, "D": dilation,
                             "ordinary_base_count": ordinary_base,
                             "ordinary_matched_sources": len(ordinary_pairs),
                             "load": 1, "eta_numerator": len(ordinary_pairs),
                             "eta_denominator": ordinary_base,
                             "pairs_sha256": hashlib.sha256(json.dumps(ordinary_pairs).encode()).hexdigest()})
    return {"status": "PASS", "factors_preserved": True, "asymptotic_claim": False,
            "independent_ordinary_sources": independent_sources, "rows": rows}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
