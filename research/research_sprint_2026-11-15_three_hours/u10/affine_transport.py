#!/usr/bin/env python3
"""Preregistered finite physical basin transfers, with exact path certificates.

This file establishes no uniform mass, independence or asymptotic statement.
All guards remain active under Python -O. No external code is executed.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math

MAXIMUM = 1 << 18
CUTOFFS = tuple(1 << k for k in (10, 12, 14, 16, 18))
BASES = (5, 7, 31, 593)
MULTIPLIERS = (2, 3, 5, 7, 11, 13)
MAX_STEPS = 10000


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sibling(n):
    return 4 * n + 1 if n % 3 == 1 else 16 * n + 5


def odd_part(x):
    require(x > 0, 'positive physical source required')
    return x >> ((x & -x).bit_length() - 1)


def syracuse(x):
    require(x > 0 and x % 2 == 1, 'positive odd Syracuse state required')
    z = 3 * x + 1
    a = (z & -z).bit_length() - 1
    return z >> a


def rational(q):
    return {'numerator': q.numerator, 'denominator': q.denominator}


TARGETS = tuple(sorted(set(BASES) | {sibling(n) for n in BASES}))
BIT = {n: 1 << j for j, n in enumerate(TARGETS)}
MASK_CACHE = {1: 0}
UNRESOLVED = []
MEMO_EDGES = 0


def get_mask(start):
    global MEMO_EDGES
    x = odd_part(start)
    if x in MASK_CACHE:
        return MASK_CACHE[x]
    path = []
    seen = set()
    while x not in MASK_CACHE:
        if x in seen or len(path) >= MAX_STEPS:
            UNRESOLVED.append(start)
            raise RuntimeError('Unresolved source; a no-hit/completeness claim is forbidden')
        seen.add(x)
        y = syracuse(x)
        path.append((x, y))
        x = y
    mask = MASK_CACHE[x]
    for x, y in reversed(path):
        require(y in MASK_CACHE, 'path recurrence lacks successor certificate')
        mask |= BIT.get(x, 0)
        MASK_CACHE[x] = mask
        MEMO_EDGES += 1
    return mask


# All registered sources and images, including every root source once.
REGISTERED_STARTS = set()
for u in range(1, MAXIMUM + 1, 2):
    REGISTERED_STARTS.add(u)
    for p in MULTIPLIERS:
        REGISTERED_STARTS.add(odd_part(p * u))
for start in sorted(REGISTERED_STARTS):
    get_mask(start)

# Fully independent path traversal: no memoized stopping or bit valuation.
DIRECT_STEPS = 0
MAX_BITS = 1
MAX_LENGTH = 0
for start in sorted(REGISTERED_STARTS):
    x = start
    seen = set()
    mask = 0
    steps = 0
    while True:
        require(x not in seen, 'nontrivial cycle found during direct certification')
        seen.add(x)
        mask |= BIT.get(x, 0)
        MAX_BITS = max(MAX_BITS, x.bit_length())
        if x == 1:
            break
        require(steps < MAX_STEPS, 'direct traversal timeout; classification prohibited')
        x = 3 * x + 1
        while x % 2 == 0:
            x //= 2
        steps += 1
        DIRECT_STEPS += 1
    MAX_LENGTH = max(MAX_LENGTH, steps)
    require(mask == MASK_CACHE[start], 'memoized/direct membership disagreement')

# These target pairs are genuinely disjoint in the certified finite domain.
for start in REGISTERED_STARTS:
    mask = MASK_CACHE[start]
    for n in BASES:
        require(not ((mask & BIT[n]) and (mask & BIT[sibling(n)])),
                'a paired target basin is not disjoint')

rows = []
full_selected = {}
for n in BASES:
    y = sibling(n)
    require(syracuse(n) == syracuse(y), 'canonical sibling has a different successor')
    for p in MULTIPLIERS:
        selected_full = []
        for cutoff in CUTOFFS:
            base_count = selected_count = image_base_count = image_y_count = neither_count = 0
            base_ordinary = selected_ordinary = 0
            selected = []
            for u in range(1, cutoff + 1, 2):
                initial = MASK_CACHE[u]
                image = MASK_CACHE[odd_part(p * u)]
                if image & BIT[y]:
                    image_y_count += 1
                if p == 2:
                    require(initial == image, 'doubling does not preserve the entire odd orbit')
                if not (initial & BIT[n]):
                    continue
                base_count += 1
                lifts = (cutoff // u).bit_length()
                base_ordinary += lifts
                if image & BIT[y]:
                    selected_count += 1
                    selected_ordinary += lifts
                    selected.append(u)
                elif image & BIT[n]:
                    image_base_count += 1
                else:
                    neither_count += 1
            require(base_count == selected_count + image_base_count + neither_count,
                    'finite conditional classes do not partition source basin')
            require(p != 2 or selected_count == 0, 'smooth doubling control transferred a source')
            total_sources = cutoff // 2
            eta = Fraction(selected_count, base_count) if base_count else None
            ordinary_eta = Fraction(selected_ordinary, base_ordinary) if base_ordinary else None
            joint_product_ratio = (Fraction(selected_count * total_sources,
                                            base_count * image_y_count)
                                   if base_count and image_y_count else None)
            cost = Fraction(p, eta) if eta else None
            ordinary_cost = Fraction(p, ordinary_eta) if ordinary_eta else None
            rows.append({
                'n': n, 'y': y, 'p': p, 'cutoff': cutoff,
                'physical_odd_inputs': total_sources,
                'source_basin_odd': base_count,
                'selected_transfer_odd': selected_count,
                'source_basin_ordinary': base_ordinary,
                'selected_transfer_ordinary': selected_ordinary,
                'image_basin_y_odd_marginal': image_y_count,
                'image_stays_in_base_odd': image_base_count,
                'image_in_neither_odd': neither_count,
                'eta_odd': rational(eta) if eta is not None else None,
                'eta_ordinary': rational(ordinary_eta) if ordinary_eta is not None else None,
                'finite_joint_over_product_of_marginals':
                    rational(joint_product_ratio) if joint_product_ratio is not None else None,
                'exact_height': p, 'maximum_incoming_load': 1 if selected_count else 0,
                'distinct_odd_images': selected_count,
                'distinct_ordinary_images': selected_ordinary,
                'height_over_eta_odd': rational(cost) if cost is not None else None,
                'height_over_eta_ordinary': rational(ordinary_cost) if ordinary_cost is not None else None,
                'cost_odd_over_one_plus_log_n': float(cost) / (1 + math.log(n)) if cost else None,
                'cost_ordinary_over_one_plus_log_n':
                    float(ordinary_cost) / (1 + math.log(n)) if ordinary_cost else None,
                'image_cutoff': p * cutoff,
                'selected_sources_sha256': hashlib.sha256(
                    json.dumps(selected, separators=(',', ':')).encode()).hexdigest(),
                'first_witnesses': [[u, p * u] for u in selected[:5]],
            })
            if cutoff == MAXIMUM:
                selected_full = selected
        full_selected[f'{n}:{p}'] = selected_full

# Preregistered cross-check against U03, without importing or executing it.
old_path = Path(__file__).resolve().parent.parent / 'u03/physical_cdf_result.json'
old = json.loads(old_path.read_text())
for pair in old['pairs']:
    n = pair['n']
    for count in pair['cutoff_counts']:
        row = next(r for r in rows if r['n'] == n and r['p'] == 2 and
                   r['cutoff'] == count['cutoff'])
        require(row['source_basin_odd'] == count['base_odd'], 'U03 base count mismatch')
        require(row['source_basin_ordinary'] == count['base_ordinary'], 'U03 lift count mismatch')

output = {
    'status': 'PASS',
    'scope': 'Finite physical affine transports only; no uniform eta, H or iid claim.',
    'maximum_source': MAXIMUM, 'source_odd_count': MAXIMUM // 2,
    'multipliers': list(MULTIPLIERS), 'targets': list(TARGETS),
    'registered_unique_odd_starts_certified_to_one': len(REGISTERED_STARTS),
    'unresolved_sources': UNRESOLVED, 'memoized_edges_checked': MEMO_EDGES,
    'independent_direct_steps': DIRECT_STEPS,
    'maximum_direct_odd_length_to_one': MAX_LENGTH,
    'maximum_direct_state_bits': MAX_BITS,
    'all_direct_masks_agree': True, 'all_U03_counts_agree': True,
    'normal_optimized_guards_active': True,
    'rows': rows,
    'all_selected_sources_sha256': hashlib.sha256(json.dumps(
        full_selected, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
}
print(json.dumps(output, sort_keys=True, separators=(',', ':')))
