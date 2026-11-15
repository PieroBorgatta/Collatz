#!/usr/bin/env python3
"""Independent augmenting-path and vertex-cover certificate for profile transport."""
from collections import defaultdict, deque
from pathlib import Path
import hashlib
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def exact_word(source, target):
    n, word, seen = source, [], set()
    for _ in range(10001):
        if n == target:
            return tuple(word)
        if n == 1:
            return None
        require(n not in seen, "unexpected orbit repetition")
        seen.add(n)
        n = 3 * n + 1
        exponent = 0
        while n % 2 == 0:
            n //= 2
            exponent += 1
        word.append(exponent)
    raise RuntimeError("explicit first-arrival cap exhausted")


def catalogue(target, cutoff):
    answer = {}
    for source in range(1, cutoff + 1, 2):
        word = exact_word(source, target)
        if word is not None:
            answer[source] = (len(word), sum(word))
    require(len(answer) == len(set(answer)), "duplicate physical source")
    return answer


def maximum_matching_with_cover(left, adjacency):
    right_owner = {}

    def augment(u, visited):
        for v in adjacency[u]:
            if v in visited:
                continue
            visited.add(v)
            if v not in right_owner or augment(right_owner[v], visited):
                right_owner[v] = u
                return True
        return False

    for u in sorted(left, reverse=True):
        augment(u, set())
    matched_left = {u: v for v, u in right_owner.items()}
    require(len(matched_left) == len(right_owner), "matching repeats a source")
    # Alternating residual reachability gives a vertex-cover certificate.
    reached_left = set(left) - set(matched_left)
    reached_right = set()
    queue = deque(reached_left)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if matched_left.get(u) == v or v in reached_right:
                continue
            reached_right.add(v)
            require(v in right_owner, "augmenting path remains")
            owner = right_owner[v]
            if owner not in reached_left:
                reached_left.add(owner)
                queue.append(owner)
    cover_left = set(left) - reached_left
    cover_right = reached_right
    for u in left:
        for v in adjacency[u]:
            require(u in cover_left or v in cover_right, "uncovered graph edge")
    require(len(cover_left) + len(cover_right) == len(right_owner),
            "matching/cover cardinality gap")
    return sorted((u, v) for v, u in right_owner.items()), len(cover_left), len(cover_right)


def main():
    base = Path(__file__).resolve().parents[1]
    reference = json.loads((base / 'verification/root_profile_transport.json').read_text())
    rows = []
    for n in (5, 7, 31, 593):
        y = 4 * n + 1 if n % 3 == 1 else 16 * n + 5
        left = catalogue(n, 256)
        all_right = catalogue(y, 64 * 256)
        for D in (16, 64):
            right = {v: profile for v, profile in all_right.items() if v <= D * 256}
            by_profile = defaultdict(list)
            for v, profile in right.items():
                by_profile[profile].append(v)
            adjacency = {u: sorted((v for v in by_profile.get(profile, []) if v <= D * u), reverse=True)
                         for u, profile in left.items()}
            pairs, cover_left, cover_right = maximum_matching_with_cover(left, adjacency)
            for u, v in pairs:
                require(left[u] == right[v] and v <= D * u, "inadmissible matched edge")
            missing = sum(profile not in by_profile for profile in left.values())
            expected = next(r for r in reference['rows']
                            if (r['n'], r['X'], r['D']) == (n, 256, D))
            observed = {'base_odd_count': len(left), 'image_odd_count': len(right),
                        'matched_sources': len(pairs), 'missing_profile_sources': missing}
            for key, value in observed.items():
                require(expected[key] == value, f"reference mismatch {n}/{D}/{key}")
            for u, v, profile in expected['sample_pairs']:
                require(u in left and v in right, "reference sample outside physical catalogue")
                require(left[u] == right[v] == tuple(profile) and v <= D * u,
                        "reference sample violates graph support")
            rows.append({'n': n, 'y': y, 'X': 256, 'D': D, **observed,
                         'edges': sum(map(len, adjacency.values())),
                         'cover_left_card': cover_left, 'cover_right_card': cover_right,
                         'matching_card_equals_vertex_cover': True,
                         'matching_sha256': hashlib.sha256(json.dumps(pairs).encode()).hexdigest(),
                         'sample_pairs': [[u, v, list(left[u])] for u, v in pairs[:8]]})
    return {'status': 'PASS', 'scope': 'eight finite odd-source cases; no asymptotic claim',
            'algorithm': 'augmenting paths plus explicit vertex-cover optimality certificate',
            'capacities': {'source': 1, 'image': 1}, 'rows': rows}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2, sort_keys=True))
