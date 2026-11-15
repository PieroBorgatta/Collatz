#!/usr/bin/env python3
"""Frozen finite profile matching; no asymptotic density conclusion."""

from bisect import bisect_right
from collections import defaultdict
import hashlib
import json

TARGETS = (5, 7, 31, 593)
CUTOFFS = (256, 1024, 4096)
DILATIONS = (4, 16, 64)
CAP = 10000


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def step(n):
    require(n > 0 and n % 2 == 1, "odd positive source")
    value = 3 * n + 1
    power = value & -value
    return value // power, power.bit_length() - 1


def sibling(n):
    return 4 * n + 1 if n % 3 == 1 else 16 * n + 5


def graph(bound):
    depth, edges = {1: 0}, {}
    for source in range(1, bound + 1, 2):
        value, path, seen = source, [], set()
        while value not in depth:
            require(value not in seen, "nontrivial cycle in finite census")
            require(len(path) < CAP, "incomplete finite census")
            seen.add(value)
            path.append(value)
            edges[value] = step(value)
            value = edges[value][0]
        distance = depth[value]
        for value in reversed(path):
            distance += 1
            depth[value] = distance
    return depth, edges


def groups(target, bound, edges):
    memo = {1: None, target: (0, 0)}
    result = defaultdict(list)
    for source in range(1, bound + 1, 2):
        value, path = source, []
        while value not in memo:
            path.append(value)
            value = edges[value][0]
        profile = memo[value]
        for value in reversed(path):
            if profile is not None:
                profile = (profile[0] + 1, profile[1] + edges[value][1])
            memo[value] = profile
        if memo[source] is not None:
            result[memo[source]].append(source)
    return result


def word(source, target):
    result = []
    while source != target:
        require(len(result) < CAP, "word reconstruction cap")
        source, exponent = step(source)
        result.append(exponent)
    return result


def match(base, images, dilation):
    pairs = []
    for profile, sources in sorted(base.items()):
        targets = images.get(profile, [])
        j = 0
        for source in sources:
            if j < len(targets) and targets[j] <= dilation * source:
                pairs.append((source, targets[j], profile))
                j += 1
    return pairs


def run():
    bound = max(CUTOFFS) * max(DILATIONS)
    depth, edges = graph(bound)
    rows = []
    for target in TARGETS:
        upper = sibling(target)
        full_base = groups(target, max(CUTOFFS), edges)
        full_images = groups(upper, bound, edges)
        for cutoff in CUTOFFS:
            base = {p: values[:bisect_right(values, cutoff)] for p, values in full_base.items()}
            base = {p: values for p, values in base.items() if values}
            base_count = sum(map(len, base.values()))
            for dilation in DILATIONS:
                images = {p: values[:bisect_right(values, dilation * cutoff)]
                          for p, values in full_images.items()}
                pairs = match(base, images, dilation)
                require(len({u for u, _, _ in pairs}) == len(pairs), "source collision")
                require(len({v for _, v, _ in pairs}) == len(pairs), "image collision")
                for source, image, profile in pairs:
                    old, new = word(source, target), word(image, upper)
                    require((len(old), sum(old)) == profile == (len(new), sum(new)),
                            "joint profile mismatch")
                    require(image <= dilation * source, "height cost")
                rows.append({"n": target, "y": upper, "X": cutoff, "D": dilation,
                             "base_odd_count": base_count,
                             "image_odd_count": sum(map(len, images.values())),
                             "matched_sources": len(pairs), "load": 1,
                             "eta_numerator": len(pairs), "eta_denominator": base_count,
                             "missing_profile_sources": sum(len(values) for p, values in base.items()
                                                            if not images.get(p)),
                             "sample_pairs": pairs[:8],
                             "pairs_sha256": hashlib.sha256(json.dumps(pairs).encode()).hexdigest()})
    return {"protocol": "PROFILE_TRANSPORT_PROTOCOL_IT.md", "status": "PASS",
            "finite_odd_sources_only": True, "asymptotic_claim": False,
            "graph_odd_nodes": len(depth), "maximum_accelerated_depth": max(depth.values()),
            "rows": rows}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
