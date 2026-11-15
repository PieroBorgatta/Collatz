#!/usr/bin/env python3
"""Independent exact replay: inverse steps, ordinary iteration, finite trimming.

No surgery congruence prefilter or source affine constant is used to construct
images. Finite checks do not establish an asymptotic sparsity estimate.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import hashlib
import json


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def odd_step(n):
    require(n > 0 and n % 2 == 1, "positive odd source")
    m, a = 3 * n + 1, 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def shortcut(n):
    require(n > 0, "positive shortcut source")
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def to_target(source, target, cap=2048):
    value, word, values, seen = source, [], [source], set()
    for _ in range(cap + 1):
        if value == target:
            return word, values
        if value == 1:
            return None
        require(value not in seen, "unexpected positive cycle")
        seen.add(value)
        value, a = odd_step(value)
        word.append(a)
        values.append(value)
    raise RuntimeError("first-arrival cap exceeded")


def inverse_steps(word, target):
    value = target
    for a in reversed(word):
        numerator = 2 ** a * value - 1
        if numerator % 3:
            return None
        value = numerator // 3
        require(value > 0 and value % 2 == 1, "inverse odd positivity")
    return value


def replay_word(source, word, target):
    value = source
    for a in word:
        value, actual_a = odd_step(value)
        require(actual_a == a, "exact exponent mismatch")
    require(value == target, "word target mismatch")


def surgery_checks(reference):
    outcomes, accepted_total, candidates_total = [], 0, 0
    for n in (5, 7, 31, 593):
        y = 4 * n + 1 if n % 3 == 1 else 16 * n + 5
        base = 0
        depth = Counter()
        successes = []
        for u in range(1, 1025, 2):
            path = to_target(u, n)
            if path is None:
                continue
            word, _ = path
            k = len(word)
            base += 1
            depth[k] += 1
            for i in range(k - 1):
                for delta in (-5, -3, -1, 1, 3, 5):
                    modified = list(word)
                    modified[i] += delta
                    modified[-1] -= delta
                    if min(modified) <= 0:
                        continue
                    candidates_total += 1
                    # Deliberately no terminal or global congruence filter.
                    v = inverse_steps(modified, y)
                    if v is None:
                        continue
                    replay_word(v, modified, y)
                    q = k - i - 1
                    numerator = y - 2 ** delta * n if delta > 0 else 2 ** (-delta) * y - n
                    require(numerator % 3 ** q == 0, "necessary filter rejects true image")
                    successes.append((u, v, i, delta, tuple(modified)))
        row = next(r for r in reference["results"] if r["target"] == n)["rows"][0]
        require(row["cutoff"] == 1024, "reference cutoff")
        pairs = {(u, v) for u, v, *_ in successes}
        incoming = defaultdict(set)
        for u, v in pairs:
            incoming[v].add(u)
        observed = {
            "base_odd_sources": base,
            "base_depth_histogram": {str(k): v for k, v in sorted(depth.items())},
            "transport_codes": len(successes),
            "physical_pairs": len(pairs),
            "distinct_odd_images": len(incoming),
            "max_distinct_source_load": max(map(len, incoming.values()), default=0),
        }
        for key, value in observed.items():
            require(row[key] == value, f"S06 independent mismatch {n}/{key}")
        for original in row["height_caps"]:
            factor = original["factor"]
            selected = [code for code in successes if code[1] <= factor * code[0]]
            p = {(u, v) for u, v, *_ in selected}
            sources, images = {u for u, _ in p}, {v for _, v in p}
            require(len(selected) == original["codes"], "height code mismatch")
            require(len(p) == original["distinct_pairs"], "height pair mismatch")
            require(len(sources) == original["covered_odd_sources"], "coverage mismatch")
            require(len(images) == original["distinct_odd_images"], "image mismatch")
        accepted_total += len(successes)
        outcomes.append({"target": n, "sibling": y, **observed})
    replay_word(16853, [7, 1], 593)
    replay_word(16867, [1, 7], 593)
    v = inverse_steps([4, 4], 9493)
    require(v == 270021, "collision inverse")
    replay_word(v, [4, 4], 9493)
    return {"cutoff": 1024, "positive_edits_without_prefilter": candidates_total,
            "accepted_codes": accepted_total, "rows": outcomes,
            "collision": {"sources": [16853, 16867], "image": v, "target": 9493}}


def section(n):
    return any(n % m == a for a, m in ((13, 18), (53, 72), (853, 1152),
        (3413, 4608), (54613, 73728), (218453, 294912)))


def macro_checks():
    count = 0
    for r in range(1, 9):
        for s in range(1, 13):
            coefficient, denominator = 27 * 9 ** r, 8 ** (s + 1)
            t = (pow(coefficient, -1, 2 * denominator) * (denominator - 13)) % (2 * denominator)
            require(t > 0 and t % 2 == 1, "macro t domain")
            v, rem = divmod(coefficient * t + 13, denominator)
            require(rem == 0 and v > 0 and v % 2 == 1, "macro v domain")
            n = 18 * t * 8 ** r - 5
            target = 18 * v * 8 ** (s - 1) - 5
            value, marks = n, []
            word = [1, 2] * r + [3, 1, 2]
            for j, a in enumerate(word, 1):
                value, actual_a = odd_step(value)
                require(actual_a == a, "macro exact exponent")
                if section(value):
                    marks.append(j)
            require(value == target, "macro endpoint")
            require(marks == list(range(2, 2 * r + 1, 2)) + [2 * r + 3], "first-return times")
            count += 1
    r, t, v = 9, 11050630593, 13456854401
    replay_word(18 * t * 8 ** r - 5, [1, 2] * r + [3, 1, 2], 18 * v * 8 ** r - 5)
    return {"parameter_pairs": count, "self_clock_witness_replayed": True}


def clock(q):
    require(q > 0, "zero/negative clock input excluded")
    power = 0
    while q % 2 == 0:
        q //= 2
        power += 1
    return power // 3


def clock_checks():
    profiles, period_profiles, error_checks = 0, 0, 0
    for q0 in (1, 2, 63, 8 ** 8):
        for b in (1, 3, 27):
            for start in (0, 1, 17):
                offset = q0 + b * start
                for R in range(5):
                    P = 8 ** R
                    full = Counter(min(clock(offset + b * j), R) for j in range(P))
                    for k in range(R):
                        require(full[k] == 7 * 8 ** (R - k - 1), "period frequency")
                    require(full[R] == 1, "period overflow")
                    period_profiles += 1
                    for U in sorted({1, max(1, P - 1), P, P + 1}):
                        values = [clock(offset + b * j) for j in range(U)]
                        count = sum(k >= R for k in values)
                        require(U // P <= count <= (U + P - 1) // P, "tail floor/ceil")
                        average = Fraction(sum((-1) ** k for k in values), U)
                        bound = Fraction(4, P) + Fraction(2 * (P + 1), U)
                        require(abs(average - Fraction(7, 9)) <= bound, "clock mean error")
                        profiles += 1
                        error_checks += 1
                        for threshold in (0, 1, 3, 8):
                            indicator_mean = Fraction(sum(k >= threshold for k in values), U)
                            require(abs(indicator_mean - Fraction(1, 8 ** threshold)) <= bound,
                                    "clock indicator error")
                            error_checks += 1
    try:
        clock(0)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("q=0 was accepted")
    return {"tail_profiles": profiles, "full_period_profiles": period_profiles,
            "bounded_observable_error_checks": error_checks,
            "offsets": [0, 1, 17], "R_includes_zero": True}


def finite_segment_checks():
    paths, trims, identities = 0, 0, 0
    for u in range(1, 1025, 2):
        path = to_target(u, 5)
        if path is None:
            continue
        word, odd_values = path
        shortcut_values, value = [u], u
        while value != 5:
            value = shortcut(value)
            shortcut_values.append(value)
            require(len(shortcut_values) <= 4096, "shortcut cap")
        require(len(set(shortcut_values)) == len(shortcut_values), "segment not injective")
        L = len(shortcut_values) - 1
        for N in sorted(set((0, 1, 2, 3, L, L + 1, L + 5))):
            prefix = shortcut_values[:max(0, len(shortcut_values) - N)]
            shifted = []
            for x in prefix:
                for _ in range(N):
                    x = shortcut(x)
                shifted.append(x)
            require(len(set(shifted)) == len(shifted), "truncated iterate collision")
            require(len(shortcut_values) - len(prefix) <= N, "terminal error")
            trims += 1
        product = Fraction(1)
        for x in odd_values[:-1]:
            product *= 1 + Fraction(1, 3 * x)
        require(product == Fraction(2 ** sum(word) * 5, 3 ** len(word) * u), "affine product")
        paths += 1
        identities += 1
    witness = [7, 11, 17, 26, 13, 20, 10, 5]
    shifted = []
    for x in witness:
        for _ in range(5):
            x = shortcut(x)
        shifted.append(x)
    require(len(set(shifted)) < len(shifted), "missing full-segment counterexample")
    return {"segments": paths, "trim_checks": trims, "product_identities": identities,
            "N_equals_or_exceeds_L": True, "untrimmed_collision_reproduced": True}


def main():
    root = Path(__file__).resolve().parents[1]
    ref = json.loads((root / 'verification/s06_surgery.json').read_text())
    return {"status": "PASS", "scope": "independent exact finite replay only",
            "surgery": surgery_checks(ref), "macro": macro_checks(),
            "clock": clock_checks(), "finite_segments": finite_segment_checks()}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2, sort_keys=True))
