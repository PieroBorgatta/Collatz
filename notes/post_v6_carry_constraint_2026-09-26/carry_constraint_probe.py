#!/usr/bin/env python3
"""A fixed level-16 test of the future-carry class, not the exact tower.

Author: Codex + Piero Borgatta, 2026-09-26. The carry constraint is an
exact linear slab on free source bits. Its parity bound is being tested.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
PINNED = {
    'post_v6_binary_carries_2026-09-26/binary_carry_results.json':
        '4ba6d3b2b02ee1fab2345a3735d0b3eba17a0b02fd8965614de40ac2bed292f1',
    'post_v6_margin_2026-09-25/margin_results.json':
        '837937cb8387577e53f0547a6991e1b606828b82366a94190835c8fbd246ccf5',
    'post_v6_compensation_2026-09-25/block_engine.py':
        'f5deaad568c9af6c26fa04706b510cf073a2ee50821436a7920f675d47c515ce',
    'post_v6_arithmetic_2026-09-25/arithmetic_probe.py':
        '02d51066d68c7cf6cc28f4127399ca4d95554ee86792f894f9c2e1d7a33d01b5',
}
PROTOCOL_SHA256 = '9584df9345d36a838661fc1acfbfe5b238c58a86e1bd20a1488c1c4e2d7d5d9a'
PRESEARCH_SHA256 = '831c761a18ea3371942fa326538b15fd5b2e1a8cd6198480ecbb4f166569d842'


def load_inputs() -> dict:
    data = {}
    for name, digest in PINNED.items():
        raw = (NOTES/name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('changed frozen input: ' + name)
        if name.endswith('.json'):
            data[name] = json.loads(raw)
    return data


# Verify source digests before executing reused engines.
load_inputs()
sys.path.insert(0, str(NOTES/'post_v6_compensation_2026-09-25'))
sys.path.insert(0, str(NOTES/'post_v6_arithmetic_2026-09-25'))
from block_engine import parity_trace
from arithmetic_probe import affine_word


def horizon(v: int) -> int:
    if v < 0:
        raise ValueError('nonnegative level required')
    return (589*(1 << v) + 611)//612


def tower(v: int) -> int:
    if v < 0:
        raise ValueError('nonnegative level required')
    return (3**(1 << (v+1))-1) >> (v+3)


def quadratic(v: int, x: int) -> int:
    return x + (x*x << (v+2))


def digest_int(n: int) -> str:
    return hashlib.sha256(n.to_bytes(max(1, (n.bit_length()+7)//8), 'little')).hexdigest()


def packed_trace(n: int, steps: int) -> bytes:
    return parity_trace(n & ((1 << steps)-1), steps)


def direct_trace(n: int, steps: int) -> bytes:
    """Elementary full-integer orbit, independent of modular trace engine."""
    data = bytearray((steps+7)//8)
    for i in range(steps):
        p = n & 1
        data[i//8] |= p << (i%8)
        n = (3*n+1)//2 if p else n//2
    return bytes(data)


def fast_carry(p: int, n: int) -> dict:
    """Certified last-column evaluation of the schoolbook square carry.

    Reversal gives each convolution coefficient by an integer popcount.
    Unrolling B columns leaves an earlier carry bounded by max(n-B-1,0).
    Extend the suffix only when the two rigorous integer bounds disagree.
    """
    if p < 0 or n < 0:
        raise ValueError('nonnegative input and column required')
    if n == 0:
        return {'carry': 0, 'columns_used': 0, 'lower': 0, 'upper': 0,
                'last_coefficients': [], 'omitted_carry_upper': 0}
    p &= (1 << n)-1
    reverse = int(format(p, f'0{n}b')[::-1], 2)
    B = min(n, n.bit_length()+2)
    while True:
        coefficients = [(p & (reverse >> s)).bit_count() for s in range(B)]
        numerator = sum(value << (B-1-s) for s, value in enumerate(coefficients))
        omitted_upper = max(n-B-1, 0)
        lo, hi = numerator >> B, (numerator+omitted_upper) >> B
        if lo == hi:
            return {'carry': lo, 'columns_used': B, 'lower': lo, 'upper': hi,
                    'last_coefficients': coefficients,
                    'omitted_carry_upper': omitted_upper}
        if B == n:
            raise AssertionError('complete carry bounds cannot disagree')
        B = min(n, 2*B)


def source_carry(v: int, x: int, K: int) -> dict:
    if min(v, x, K) < 0:
        raise ValueError('nonnegative level, source and precision required')
    return fast_carry(1 + (x << (v+3)), K+v+3)


def linear_carry(v: int, u: int, H: int, K: int, x: int) -> dict:
    """The exact carry slab after a fixed source prefix.

    Free-bit pairs have columns >=2*(r+H)>=r+K and are absent from F_N.
    High bits >=K are likewise absent. No orbit/parity count enters here.
    """
    if v < 0 or not 1 <= H <= K <= 2*H or not 0 <= u < (1 << H):
        raise ValueError('valid level, prefix and doubled horizons required')
    if x < 0 or x % (1 << H) != u:
        raise ValueError('source outside the prefix class')
    r, F = v+3, K-H
    n, p0 = r+K, 1+(u << r)
    denominator = 1 << n
    constant = fast_carry(p0, n)['carry']*denominator + (p0*p0 % denominator)
    suffix = (x >> H) & ((1 << F)-1)
    weighted = 0
    for j in range(F):
        if (suffix >> j) & 1:
            weight = (p0 & ((1 << (F-j))-1)) << (r+H+j+1)
            weighted += weight
    return {'carry': (constant+weighted)//denominator,
            'constant_numerator': constant,
            'weighted_suffix_numerator': weighted,
            'denominator': denominator, 'suffix_ones': suffix.bit_count()}


def inverse_quadratic(v: int, y: int, bits: int) -> int:
    """Simultaneous Newton lift of f_v inverse and derivative inverse.

    Avoid extended Euclid on large arbitrary odd derivatives. Each step
    doubles certified precision using only integer products and masks.
    """
    if v < 0 or bits < 0 or not 0 <= y < (1 << bits):
        raise ValueError('valid level, target and precision required')
    if bits == 0:
        return 0
    x, unit, precision = y & 1, 1, 1
    c = 1 << (v+2)
    while precision < bits:
        next_precision = min(bits, 2*precision)
        mask = (1 << next_precision)-1
        error = (x+c*x*x-y) & mask
        x = (x-error*unit) & mask
        unit = (unit*(2-(1+2*c*x)*unit)) & mask
        precision = next_precision
    return x


@lru_cache(maxsize=None)
def _prefix_inverse(prefix_word: int, H: int, K: int) -> tuple[int, int]:
    odd, _, constant = affine_word(prefix_word, H)
    modulus = 1 << K
    base = (-(constant+(1 << H))*pow(3, -odd, modulus)) & (modulus-1)
    return odd, base


@lru_cache(maxsize=None)
def _inverse_three(exponent: int, bits: int) -> int:
    return pow(3, -exponent, 1 << bits)


def sparse_suffix_residue(prefix_word: int, H: int, K: int,
                          zero_positions: tuple[int, ...] | list[int]) -> int:
    if not 0 <= H <= K or not 0 <= prefix_word < (1 << H):
        raise ValueError('valid prefix and horizon required')
    positions = tuple(sorted(zero_positions))
    if len(set(positions)) != len(positions) or any(not H <= p < K for p in positions):
        raise ValueError('distinct suffix zero positions required')
    odd, residue = _prefix_inverse(prefix_word, H, K)
    for ordinal, position in enumerate(positions):
        exponent = odd+position-H-ordinal
        residue -= _inverse_three(exponent, K-position) << position
    return residue & ((1 << K)-1)


def masks(H: int, K: int) -> list[tuple[int, ...]]:
    if not 0 <= H <= K:
        raise ValueError('valid suffix required')
    if H == K:
        return [()]
    positions = sorted(set(H+i*(K-H-1)//511 for i in range(512)))
    proposed = [()] + [(p,) for p in positions]
    proposed += [tuple(sorted(set((p, H+K-1-p)))) for p in positions]
    return list(dict.fromkeys(proposed))


def small_fiber(v: int) -> dict:
    H, K = horizon(v), horizon(v+1)
    q, r = tower(v), v+3
    u, high = q % (1 << H), q >> K << K
    target = source_carry(v, q, K)['carry']
    j = int.from_bytes(direct_trace(q, H), 'little').bit_count()
    distribution, retained, counts = Counter(), Counter(), Counter()
    for t in range(1 << (K-H)):
        x = high | (t << H) | u
        linear = linear_carry(v, u, H, K, x)
        c = source_carry(v, x, K)['carry']
        assert linear['carry'] == c
        delta = int.from_bytes(direct_trace(quadratic(v, x), K), 'little').bit_count()-2*j
        distribution[delta] += 1
        counts[c] += 1
        if c == target:
            retained[delta] += 1
    return {'v': v, 'candidates': sum(distribution.values()),
            'retained': sum(retained.values()),
            'actual_carry': target,
            'maximum_before': max(distribution), 'maximum_after': max(retained),
            'delta_distribution_before': dict(sorted(distribution.items())),
            'delta_distribution_after': dict(sorted(retained.items())),
            'carry_counts': dict(sorted(counts.items())),
            'all_linear_and_fast_carries_equal': True}


def pilot_examples() -> list[dict]:
    examples = [(5, 33, '2b56d4af8c0770d18c797ebd'),
                (6, 67, '3ab2473486d2d269777d317f5b6bcf488f240210a40c5433d'),
                (7, 149, 'd75446ae5f13214622d2592bd62d3165be377235f0c4403b517d3f7216caf9e038930dd68817781d65f54748417cbc1cc3d')]
    result = []
    for v, position, text in examples:
        x, q, H, K = int(text, 16), tower(v), horizon(v), horizon(v+1)
        low, up = direct_trace(x, H), direct_trace(quadratic(v, x), K)
        actual_up_prefix = int.from_bytes(direct_trace(tower(v+1), H), 'little')
        expected = actual_up_prefix | (((1 << (K-H))-1) << H)
        expected &= ~(1 << position)
        assert int.from_bytes(up, 'little') == expected
        assert low == direct_trace(q, H)
        assert x >> K == q >> K and x.bit_length() == q.bit_length()
        c, c_actual = source_carry(v, x, K)['carry'], source_carry(v, q, K)['carry']
        assert c == c_actual == linear_carry(v, q % (1 << H), H, K, x)['carry']
        result.append({'v': v, 'zero_position': position, 'X_hex': hex(x),
                       'carry': c, 'delta': int.from_bytes(up, 'little').bit_count()-2*int.from_bytes(low, 'little').bit_count(),
                       'diagnostic_only': True, 'chosen_before_level16_protocol': True})
    return result


def search(pre: dict, baseline: dict[int, dict], progress: bool = False) -> dict:
    v, H, K = pre['v'], pre['H'], pre['K']
    assert (v, H, K) == (16, horizon(16), horizon(17))
    q, q_next = tower(v), tower(v+1)
    low, up = packed_trace(q, H), packed_trace(q_next, K)
    for level, packed in ((v, low), (v+1, up)):
        assert hashlib.sha256(packed).hexdigest() == baseline[level]['parity_trace_sha256']
        assert int.from_bytes(packed, 'little').bit_count() == baseline[level]['odd_steps']
    j = int.from_bytes(low, 'little').bit_count()
    upper_prefix = int.from_bytes(up, 'little') & ((1 << H)-1)
    base_word = upper_prefix | (((1 << (K-H))-1) << H)
    target = source_carry(v, q, K)
    high, u = q >> K << K, q % (1 << H)
    visits, witness = [], None
    candidates = masks(H, K)
    assert [list(p) for p in candidates] == pre['candidate_zero_positions']
    assert len(candidates) == pre['candidate_count']
    for index, positions in enumerate(candidates):
        word = base_word
        for position in positions:
            word &= ~(1 << position)
        y = sparse_suffix_residue(upper_prefix, H, K, positions)
        low_x = inverse_quadratic(v, y, K)
        assert quadratic(v, low_x) % (1 << K) == y
        x = high | low_x
        assert x > 0 and x % 2 == 1 and x % (1 << H) == u
        assert x.bit_length() == q.bit_length()
        delta = word.bit_count()-2*j
        carry = source_carry(v, x, K)
        visits.append({'index': index, 'zero_positions': positions,
                       'carry': carry['carry'], 'columns_used': carry['columns_used'],
                       'delta': delta, 'source_residue_sha256': digest_int(low_x)})
        if progress and index % 32 == 0:
            print(json.dumps({'visited': index+1, 'target_carry': target['carry'],
                              'current_carry': carry['carry']}), flush=True)
        if carry['carry'] == target['carry'] and delta > pre['g']:
            upper_source = quadratic(v, x)
            actual_low, actual_high = packed_trace(x, H), packed_trace(upper_source, K)
            assert actual_low == low
            assert int.from_bytes(actual_high, 'little') == word
            # Full-integer replay does not use the modular trace recursion.
            assert direct_trace(x, H) == actual_low
            assert direct_trace(upper_source, K) == actual_high
            linear = linear_carry(v, u, H, K, x)
            assert linear['carry'] == carry['carry']
            assert pre['anchor_margin'] == (1 << (v-1))-j
            upper_odd = word.bit_count()
            witness = {'v': v, 'candidate_index': index, 'zero_positions': positions,
                       'X_hex': hex(x), 'Y_hex': hex(upper_source),
                       'source_bits': x.bit_length(), 'same_source_binade': True,
                       'source_low_H_and_high_from_K_equal': True,
                       'same_lower_complete_word': True, 'exact_quadratic_relation': True,
                       'is_actual_tower_source': x == q,
                       'lower_odd': j, 'upper_odd': upper_odd, 'delta': delta,
                       'target_g': pre['g'], 'lower_margin': pre['anchor_margin'],
                       'upper_margin': (1 << v)-upper_odd,
                       'carry_certificate': carry, 'actual_carry_certificate': target,
                       'linear_carry': {name: (hex(value) if name in
                                          ('constant_numerator','weighted_suffix_numerator','denominator')
                                          else value) for name, value in linear.items()},
                       'lower_word_lsb_first_hex': actual_low.hex(),
                       'upper_word_lsb_first_hex': actual_high.hex(),
                       'lower_word_sha256': hashlib.sha256(actual_low).hexdigest(),
                       'upper_word_sha256': hashlib.sha256(actual_high).hexdigest(),
                       'full_integer_parity_replay_matches': True}
            assert not witness['is_actual_tower_source']
            assert witness['upper_margin'] == 2*witness['lower_margin']-delta
            break
    return {'status': 'counterexample' if witness else 'finite_family_no_counterexample',
            'candidate_count': len(candidates), 'visited_count': len(visits),
            'family_exhausted': len(visits) == len(candidates),
            'actual_carry': target['carry'], 'actual_delta': baseline[v+1]['odd_steps']-2*j,
            'actual_upper_margin': baseline[v+1]['margin'],
            'visited': visits, 'witness': witness}


def produce(progress: bool = False) -> dict:
    inputs = load_inputs()
    raw_protocol = (HERE/'PROTOCOL_IT.md').read_bytes()
    if hashlib.sha256(raw_protocol).hexdigest() != PROTOCOL_SHA256:
        raise ValueError('changed frozen protocol')
    raw_presearch = (HERE/'presearch.json').read_bytes()
    if hashlib.sha256(raw_presearch).hexdigest() != PRESEARCH_SHA256:
        raise ValueError('changed frozen candidate list')
    pre = json.loads(raw_presearch)
    assert pre['protocol_sha256'] == PROTOCOL_SHA256
    margin = inputs['post_v6_margin_2026-09-25/margin_results.json']
    baseline = {row['v']: row for row in margin['levels']}
    small = [small_fiber(v) for v in range(5)]
    previous = inputs['post_v6_binary_carries_2026-09-26/binary_carry_results.json']
    for row, old in zip(small, previous['future_carry_selection']):
        assert row['candidates'] == old['candidates'] and row['retained'] == old['retained']
        for key in ('delta_distribution_before', 'delta_distribution_after', 'carry_counts'):
            assert {str(k): val for k, val in row[key].items()} == old[key]
    return {'schema': 'tower-future-carry-constraint-v1',
            'scope': 'exact linear carry constraint and fixed class-certificate falsification at v16',
            'protocol_sha256': PROTOCOL_SHA256, 'pinned_inputs_sha256': PINNED,
            'presearch_sha256': PRESEARCH_SHA256,
            'small_fiber_rechecks': small, 'exploratory_pilot_witnesses': pilot_examples(),
            'level16_search': search(pre, baseline, progress),
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'uniform_exact_tower_bound_proved': False,
            'collatz_counterexample_claimed': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'carry_constraint_results.json')
    parser.add_argument('--progress', action='store_true')
    args = parser.parse_args()
    result = produce(args.progress)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    s = result['level16_search']
    w = s['witness']
    print(json.dumps({'status': s['status'], 'visited': s['visited_count'],
                      'candidates': s['candidate_count'],
                      'witness': None if w is None else {key: w[key] for key in
                               ('candidate_index','zero_positions','delta','target_g','lower_margin','upper_margin')},
                      'actual_delta': s['actual_delta'], 'actual_upper_margin': s['actual_upper_margin']}, indent=2))


if __name__ == '__main__':
    main()
