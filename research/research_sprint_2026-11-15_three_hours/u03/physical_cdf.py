#!/usr/bin/env python3
"""Complete finite physical first-arrival catalogues; no asymptotic conclusion."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

MAXIMUM = 1 << 18
CUTOFFS = [1 << k for k in (10, 12, 14, 16, 18)]
BASES = (5, 7, 31, 593)
LOADS = (1, 2, 4, 8, 16, 32, 64, 128)
DILATIONS = (1, 2, 4, 8, 16, 32)
MAX_UNCACHED_STEPS = 10000


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def step(x):
    require(x > 0 and x % 2 == 1, 'Syracuse domain')
    z = 3 * x + 1
    a = (z & -z).bit_length() - 1
    return z >> a, a


def sibling(n):
    y = 4 * n + 1
    return y if y % 3 else 16 * n + 5


def rat(q):
    return {'numerator': q.numerator, 'denominator': q.denominator}


def lift_count(x, limit):
    require(0 < x <= limit and x % 2 == 1, 'dyadic lift source')
    return (limit // x).bit_length()


TARGETS = tuple(sorted(set(BASES) | {sibling(n) for n in BASES}))
# cache[x][target] = exact first-arrival (length, total, maximum valuation).
cache = {1: {}}
unknown = []
checked_edges = 0
for u in range(1, MAXIMUM + 1, 2):
    if u in cache:
        continue
    path = []
    seen = set()
    x = u
    while x not in cache:
        if x in seen or len(path) >= MAX_UNCACHED_STEPS:
            unknown.append(u)
            break
        seen.add(x)
        nxt, a = step(x)
        path.append((x, nxt, a))
        x = nxt
    if x not in cache:
        continue
    records = cache[x]
    for z, nxt, a in reversed(path):
        require(nxt in cache, 'cache recurrence successor')
        records = {t: (k + 1, total + a, max(maximum, a))
                   for t, (k, total, maximum) in records.items()}
        if z in TARGETS:
            records[z] = (0, 0, 0)
        cache[z] = records
        checked_edges += 1
require(not unknown, 'Unresolved sources; complete-catalogue claim prohibited')

# Independent direct traversal: no cache stopping, no cached-profile recurrence.
catalogues = {t: [] for t in TARGETS}
source_visits = 0
maximum_k = 0
maximum_A = 0
maximum_state_bits = 1
for u in range(1, MAXIMUM + 1, 2):
    x, k, total, maximum = u, 0, 0, 0
    direct = {}
    direct_seen = set()
    while True:
        require(x not in direct_seen, 'Unexpected direct cycle')
        direct_seen.add(x)
        maximum_state_bits = max(maximum_state_bits, x.bit_length())
        if x in TARGETS and x not in direct:
            direct[x] = (k, total, maximum)
        if x == 1:
            break
        require(k < MAX_UNCACHED_STEPS, 'Unexpected direct timeout')
        z = 3 * x + 1
        a = 0
        while z % 2 == 0:
            z //= 2
            a += 1
        x = z
        k += 1
        total += a
        maximum = max(maximum, a)
        source_visits += 1
    maximum_k = max(maximum_k, k)
    maximum_A = max(maximum_A, total)
    require(direct == cache[u], 'Independent first-arrival profile mismatch')
    for target, (length, A, max_a) in direct.items():
        rho = Fraction(1 << A, 3 ** length)
        product = rho * Fraction(target, u)
        require(product >= 1, 'Affine product below one')
        catalogues[target].append((u, rho, length, A, max_a, product))

for n in BASES:
    y = sibling(n)
    require(step(n)[0] == step(y)[0], 'Targets are not siblings')
    require(not (set(x[0] for x in catalogues[n]) &
                 set(x[0] for x in catalogues[y])), 'Sibling basins intersect')


def matched_row(U, V, m, C, n, y, limit):
    selected = []
    image_index = 0
    used = 0
    loads = {}
    max_height = Fraction(0)
    max_ratio = Fraction(0)
    height_witness = None
    for source in U:
        if image_index == len(V):
            break
        image = V[image_index]
        if image[1] > C * source[1]:
            continue
        u, v = source[0], image[0]
        height = Fraction(v, u)
        ratio = image[1] / source[1]
        # Exact finite analogue of the universal product-envelope height lemma.
        require(height <= Fraction(y, n) * C * source[5], 'Height-envelope violation')
        selected.append((u, v))
        loads[v] = loads.get(v, 0) + 1
        if height > max_height:
            max_height = height
            height_witness = [u, v]
        max_ratio = max(max_ratio, ratio)
        used += 1
        if used == m:
            used = 0
            image_index += 1
    require(max(loads.values(), default=0) <= m, 'Incoming capacity exceeded')
    ordinary_total = sum(lift_count(row[0], limit) for row in U)
    ordinary_selected = sum(lift_count(u, limit) for u, _ in selected)
    digest = hashlib.sha256(json.dumps(selected, separators=(',', ':')).encode()).hexdigest()
    return {'load': m, 'slope_dilation': C, 'selected_odd': len(selected),
            'total_odd': len(U), 'image_catalogue_odd': len(V),
            'selected_ordinary': ordinary_selected, 'total_ordinary': ordinary_total,
            'selected_fraction_odd': rat(Fraction(len(selected), len(U))) if U else None,
            'selected_fraction_ordinary': rat(Fraction(ordinary_selected, ordinary_total)) if ordinary_total else None,
            'distinct_images': len(loads), 'maximum_incoming_load': max(loads.values(), default=0),
            'maximum_actual_height': rat(max_height), 'maximum_actual_slope_ratio': rat(max_ratio),
            'height_witness': height_witness, 'selected_pairs_sha256': digest}


pairs = []
for n in BASES:
    y = sibling(n)
    U = sorted(catalogues[n], key=lambda r: (r[1], r[0]))
    V = sorted(catalogues[y], key=lambda r: (r[1], r[0]))
    summaries = []
    for cutoff in CUTOFFS:
        uc = [r for r in U if r[0] <= cutoff]
        vc = [r for r in V if r[0] <= cutoff]
        summaries.append({'cutoff': cutoff, 'base_odd': len(uc), 'image_odd': len(vc),
                          'base_ordinary': sum(lift_count(r[0], cutoff) for r in uc),
                          'image_ordinary': sum(lift_count(r[0], cutoff) for r in vc),
                          'base_cap6_odd': sum(r[4] <= 6 for r in uc),
                          'image_cap6_odd': sum(r[4] <= 6 for r in vc)})
    full_costs = []
    physicalU = sorted(U)
    physicalV = sorted(V)
    for m in LOADS:
        if not U or len(U) > m * len(V):
            full_costs.append({'load': m, 'full_matching_exists_in_catalogue': False})
            continue
        C = max(V[i // m][1] / row[1] for i, row in enumerate(U))
        slope_height = max(Fraction(V[i // m][0], row[0]) for i, row in enumerate(U))
        D = max(Fraction(physicalV[i // m][0], row[0]) for i, row in enumerate(physicalU))
        require(slope_height <= Fraction(y, n) * C * max(r[5] for r in U), 'Full slope-envelope mismatch')
        full_costs.append({'load': m, 'full_matching_exists_in_catalogue': True,
                           'minimal_full_slope_dilation': rat(C),
                           'actual_height_of_full_slope_matching': rat(slope_height),
                           'minimal_full_physical_height': rat(D)})
    pairs.append({'n': n, 'y': y, 'cutoff_counts': summaries,
                  'finite_products': {'maximum_base': rat(max((r[5] for r in U), default=Fraction(0))),
                                      'maximum_image': rat(max((r[5] for r in V), default=Fraction(0)))},
                  'full_rank_costs': full_costs,
                  'selected_matchings': [matched_row(U, V, m, C, n, y, MAXIMUM)
                                        for m in LOADS for C in DILATIONS]})

out = {'status': 'PASS', 'scope': 'Complete finite certified physical catalogues only; no eta, H or asymptotic claim.',
       'maximum_source': MAXIMUM, 'odd_sources_certified_to_one': MAXIMUM // 2,
       'unresolved_sources': unknown, 'targets': list(TARGETS),
       'memoized_edges_checked': checked_edges, 'direct_forward_steps': source_visits,
       'maximum_direct_syracuse_length_to_one': maximum_k,
       'maximum_direct_total_valuation_to_one': maximum_A,
       'maximum_direct_state_bits': maximum_state_bits,
       'all_catalogues_agree_with_independent_direct_forward': True,
       'normal_optimization_invariant_guards': True, 'pairs': pairs}
print(json.dumps(out, sort_keys=True, separators=(',', ':')))
