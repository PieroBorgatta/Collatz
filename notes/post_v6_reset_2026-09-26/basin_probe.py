#!/usr/bin/env python3
"""Exact finite predecessor census, not an asymptotic density estimator.

AI-assisted development: Codex with Piero Borgatta, 2026-09-26.
See PROTOCOL_IT.md for fixed cutoffs and interpretation limits.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


def step(n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("Syracuse source must be positive odd")
    m = 3 * n + 1
    return m // (m & -m)


def sibling(n):
    if n <= 1 or n % 2 == 0 or n % 3 == 0:
        raise ValueError("target must be odd >1 and prime to 3")
    return 4 * n + 1 if n % 3 == 1 else 16 * n + 5


def census(bound, max_new_steps=10000):
    """All starts <=bound, including evens; exact finite termination checked.

    Each odd node has one outgoing edge. Starting weights are the number
    of powers of two multiplying that odd part without exceeding bound.
    Propagate weights from leaves to 1 in decreasing depth order.
    """
    if bound < 1:
        raise ValueError("positive bound required")
    depth = {1: 0}
    successor = {}
    counts = Counter()
    for u in range(1, bound + 1, 2):
        counts[u] += (bound // u).bit_length()
        n, path, seen = u, [], set()
        while n not in depth:
            if n in seen:
                raise RuntimeError(f"nontrivial cycle encountered from {u}")
            if len(path) >= max_new_steps:
                raise RuntimeError(f"fixed exploration cap reached from {u}")
            seen.add(n)
            path.append(n)
            nxt = step(n)
            successor[n] = nxt
            n = nxt
        distance = depth[n]
        for n in reversed(path):
            distance += 1
            depth[n] = distance
    for n in sorted(depth, key=depth.get, reverse=True):
        if n != 1:
            counts[successor[n]] += counts[n]
    if counts[1] != bound:
        raise RuntimeError(f"incomplete census at 1: {counts[1]} starts, expected {bound}")
    return counts, {"visited_odd_nodes": len(depth),
                    "maximum_accelerated_depth": max(depth.values()),
                    "largest_visited_integer": max(depth)}


def direct_counts(bound):
    """Independent ordinary-map replay for the small-domain test only."""
    counts = Counter()
    for source in range(1, bound + 1):
        n, visited = source, set()
        for _ in range(10000):
            if n % 2:
                visited.add(n)
            if n == 1:
                break
            n = 3 * n + 1 if n % 2 else n // 2
        else:
            raise RuntimeError("direct replay cap")
        counts.update(visited)
    return counts


def orbit_siblings(source=27):
    n, spine = source, []
    while n != 1:
        if n in spine or len(spine) >= 10000:
            raise RuntimeError("spine did not terminate within fixed cap")
        spine.append(n)
        n = step(n)
    # The first source 27 is divisible by 3: exclude it from selected pairs.
    pairs = [(n, sibling(n)) for n in spine if n % 3]
    sibling_targets = {y for _, y in pairs}
    if len(sibling_targets) != len(pairs):
        raise RuntimeError("selected sibling targets are not distinct")
    if sibling_targets & set(spine + [1]):
        raise RuntimeError("selected sibling target lies on the original spine")
    return pairs


def run():
    small = census(2048)[0]
    if small != direct_counts(2048):
        raise RuntimeError("small census disagrees with independent ordinary-map replay")
    targets = [n for n in range(5, 1024, 2) if n % 3]
    for n in targets:
        y = sibling(n)
        if not n < y <= 16 * n + 5 or y % 3 == 0:
            raise RuntimeError(f"invalid selected sibling domain for {n}: {y}")
        if step(n) != step(y):
            raise RuntimeError(f"selected sibling does not share the successor of {n}: {y}")
    pairs = orbit_siblings()
    results = []
    for exponent in (14, 16, 18, 20):
        bound = 1 << exponent
        counts, stats = census(bound)
        rows = []
        for n in targets:
            y = sibling(n)
            cn, cy = counts[n], counts[y]
            if cn <= 0:
                raise RuntimeError(f"missing base target {n} at cutoff {bound}")
            rows.append({"n": n, "y": y, "base_count": cn,
                         "sibling_count": cy,
                         "scaled_ratio_float": (1 + math.log(n)) * cy / cn})
        sibling_mass = sum(counts[y] for _, y in pairs)
        if sibling_mass > bound:
            raise RuntimeError(f"sibling mass {sibling_mass} exceeds cutoff {bound}")
        minimum = min(rows, key=lambda row: row["scaled_ratio_float"])
        result = {"bound": bound, **stats, "rows": rows,
                  "minimum_scaled_ratio_row": minimum,
                  "zero_sibling_counts": sum(row["sibling_count"] == 0 for row in rows),
                  "orbit_27_sibling_count_sum": sibling_mass,
                  "orbit_27_sibling_targets": len(pairs)}
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if k != "rows"}), flush=True)
    return {"protocol": "PROTOCOL_IT.md", "inclusive_source_cutoffs": True,
            "small_direct_replay_bound": 2048, "targets_per_cutoff": len(targets),
            "asymptotic_claim": False, "universal_constant_fitted": False,
            "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
