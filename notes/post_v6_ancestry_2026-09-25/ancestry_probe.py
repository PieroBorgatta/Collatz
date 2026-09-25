#!/usr/bin/env python3
"""Exact integer ancestry filters and counterexamples to count-only transfer.

All numerical examples are finite and generic. No uniform tower parity bound
or new actual tower level is claimed.
"""
import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
sys.path.insert(0, str(NOTES / 'post_v6_mixed_2026-09-25'))
from mixed_probe import tower, ceil_log2, ternary_valuation
from margin_probe import quadratic, direct_word, horizon
from arithmetic_probe import word_residue


def power_two_root(n, depth):
    """Floor of the 2^depth-th root, with no floating point."""
    if n < 0 or depth < 0:
        raise ValueError('nonnegative inputs expected')
    for _ in range(depth):
        n = isqrt(n)
    return n


def chain(u, x, depth):
    if u < 0 or x < 1 or depth < 0:
        raise ValueError('positive integer chain expected')
    values = [x]
    for w in range(u, u + depth):
        values.append(quadratic(w, values[-1]))
    return values


def recover_ancestor(v, x, depth):
    if v < 0 or x < 1 or not 0 <= depth <= v:
        raise ValueError('invalid ancestry request')
    signature = 1 + (x << (v + 3))
    z = power_two_root(signature, depth)
    a = 1 << (v - depth + 3)
    if z ** (1 << depth) != signature or (z - 1) % a:
        return None
    anchor = (z - 1) // a
    return anchor if anchor > 0 else None


def ancestor_interval(u, v, Z=None):
    """Inclusive anchor interval whose terminal value lies in [Z,2Z)."""
    if not 0 <= u <= v:
        raise ValueError('invalid levels')
    if Z is None:
        Z = 1 << (tower(v).bit_length() - 1)
    if Z < 1:
        raise ValueError('positive interval boundary expected')
    depth = v - u
    a, A = 1 << (v + 3), 1 << (u + 3)
    lower_signature, upper_signature = 1 + a * Z, 1 + a * (2 * Z - 1)
    lower = power_two_root(lower_signature, depth)
    lower += lower ** (1 << depth) < lower_signature
    upper = power_two_root(upper_signature, depth)
    L = max(1, (lower - 1 + A - 1) // A)
    U = (upper - 1) // A
    return L, U


def inverse_quadratic(v, target, bits):
    if v < 0 or bits < 0:
        raise ValueError('nonnegative level and precision expected')
    if bits == 0:
        return 0
    x, precision = target & 1, 1
    while precision < bits:
        precision = min(2 * precision, bits)
        modulus = 1 << precision
        derivative = 1 + (x << (v + 3))
        x = (x - (quadratic(v, x) - target)
             * pow(derivative, -1, modulus)) & (modulus - 1)
    return x


def inverse_chain(u, v, target, bits):
    if not 0 <= u <= v or bits < 0:
        raise ValueError('invalid chain or precision')
    residue = target & ((1 << bits) - 1)
    for w in range(v - 1, u - 1, -1):
        residue = inverse_quadratic(w, residue, bits)
    return residue


def class_count(L, U, r, bits):
    if bits < 0:
        raise ValueError('negative precision')
    if L > U:
        return 0
    modulus = 1 << bits
    first = L + ((r - L) & (modulus - 1))
    return max(0, (U - first) // modulus + 1)


def isolation_bits(Q, L, U):
    if not L <= Q <= U:
        raise ValueError('anchor must belong to the interval')
    return ceil_log2(max(Q - L, U - Q) + 1)


def word_candidate(v, word, n, depth):
    if not 0 <= depth <= v or n < 0:
        raise ValueError('invalid word ancestry')
    terminal = word_residue(word, n)
    u = v - depth
    residue = inverse_chain(u, v, terminal, n)
    L, U = ancestor_interval(u, v)
    count = class_count(L, U, residue, n)
    first = L + ((residue - L) & ((1 << n) - 1))
    return {'anchor_residue_hex': hex(residue), 'L_hex': hex(L), 'U_hex': hex(U),
            'count_hex': hex(count), 'first_hex': hex(first) if count else None}


def pure_residue(v, k, bits):
    """F_v(k) mod 2^bits without constructing the enormous full power."""
    if min(v, k, bits) < 0:
        raise ValueError('nonnegative inputs expected')
    shift = v + 3
    modulus = 1 << (shift + bits)
    return (pow(3, k << (v + 1), modulus) - 1) >> shift


def pure_parameter(v, residue, bits):
    """Unique exponent parameter k mod 2^bits giving the desired residue."""
    if min(v, bits) < 0 or not 0 <= residue < (1 << bits):
        raise ValueError('invalid pure-power residue')
    shift = v + 3
    mask = (1 << (shift + bits)) - 1
    target = 1 + (residue << shift)
    power = pow(3, 1 << (v + 1), mask + 1)
    accumulator, k = 1, 0
    for i in range(bits):
        if ((target - accumulator) >> (shift + i)) & 1:
            k |= 1 << i
            accumulator = accumulator * power & mask
        power = power * power & mask
    assert accumulator == target and pure_residue(v, k, bits) == residue
    return k


def record_chain(v, depth, anchor, kind, metadata):
    u, H, K = v - depth, horizon(v), horizon(v + 1)
    values = chain(u, anchor, depth + 1)
    X, Y = values[-2:]
    low_word, _ = direct_word(X, H)
    up_word, _ = direct_word(Y, K)
    lower_margin = (1 << (v - 1)) - low_word.bit_count()
    upper_margin = (1 << v) - up_word.bit_count()
    assert anchor != tower(u) and lower_margin > 0 > upper_margin
    levels = []
    for w, value in enumerate(values, u):
        Q = tower(w)
        assert value.bit_length() == Q.bit_length() and value % 2 == 1
        signature_nu = ternary_valuation(1 + (value << (w + 3)))
        difference_nu = ternary_valuation(value - Q)
        assert difference_nu >= (1 << (w - 1))
        assert signature_nu >= (1 << (w - 1))
        levels.append({'v': w, 'X_hex': hex(value), 'Q_bits': Q.bit_length(),
                       'same_binade': True, 'odd': True, 'difference_valuation': difference_nu,
                       'signature_valuation': signature_nu,
                       'quarter_precision': 1 << (w - 1)})
        if w > u:
            assert recover_ancestor(w, value, w - u) == anchor
    actual_lower = direct_word(tower(v), H)[0]
    actual_upper = direct_word(tower(v + 1), K)[0]
    return {'v': v, 'depth_before_lower_level': depth, 'anchor_level': u,
            'kind': kind, 'H': H, 'K': K, 'levels': levels,
            'lower_word_hex': hex(low_word), 'upper_word_hex': hex(up_word),
            'lower_margin': lower_margin, 'upper_margin': upper_margin,
            'actual_lower_margin': (1 << (v - 1)) - actual_lower.bit_count(),
            'actual_upper_margin': (1 << v) - actual_upper.bit_count(),
            'same_complete_lower_word': low_word == actual_lower,
            'not_the_actual_tower': True, **metadata}


def one_ancestor_example(v):
    """Retain actual lower word, quarter ternary precision and three binades."""
    u, H, K = v - 1, horizon(v), horizon(v + 1)
    Q = tower(u)
    L, U = ancestor_interval(u, v + 1)
    s = 1 << (u - 1)
    P = (1 << H) * 3 ** s
    p = ((U - Q) // P + 1).bit_length() - 1
    assert 0 < p <= K - H and Q + P * ((1 << p) - 1) <= U
    head = direct_word(tower(v + 1), H)[0]
    target_word = head | (((1 << p) - 1) << H)
    n = H + p
    desired_anchor = inverse_chain(u, v + 1, word_residue(target_word, n), n)
    difference = (desired_anchor - Q) & ((1 << n) - 1)
    assert difference & ((1 << H) - 1) == 0
    t = ((difference >> H) * pow(3 ** s, -1, 1 << p)) & ((1 << p) - 1)
    anchor = Q + P * t
    assert L <= anchor <= U and t > 0
    row = record_chain(v, 1, anchor, 'one_ancestor_actual_lower_word',
                       {'anchor_increment_modulus_hex': hex(P), 't_hex': hex(t),
                        'forced_upper_odd_bits_after_H': p, 'forced_word_length': n})
    assert row['same_complete_lower_word']
    assert int(row['upper_word_hex'], 16) & ((1 << n) - 1) == target_word
    return row


def deeper_margin_example(v, depth, search_limit=2000):
    """Bounded exploratory search; keep ternary precision, not the lower word."""
    u = v - depth
    Q = tower(u)
    P = 2 * 3 ** (1 << (u - 1))
    _, U = ancestor_interval(u, v + 1)
    for t in range(1, search_limit + 1):
        anchor = Q + P * t
        if anchor > U:
            break
        X, Y = chain(u, anchor, depth + 1)[-2:]
        low, _ = direct_word(X, horizon(v))
        high, _ = direct_word(Y, horizon(v + 1))
        if low.bit_count() < (1 << (v - 1)) and high.bit_count() > (1 << v):
            row = record_chain(v, depth, anchor, 'deeper_ancestry_positive_margin',
                               {'anchor_increment_modulus_hex': hex(P), 't_hex': hex(t),
                                'search_limit': search_limit, 'first_successful_t': t,
                                'selection': 'Exploratory deterministic search, not held-out validation.'})
            assert not row['same_complete_lower_word']
            return row
    raise ValueError('No example found within the finite search and height range')


def exhaustive_small_anchor_case():
    """Every odd anchor in one finite ancestry/height interval, before filtering."""
    u, v = 3, 10
    L, U = ancestor_interval(u, v + 1)
    q, s = tower(u), 1 << (u - 1)
    three = 3 ** s
    rows = []
    for anchor in range(L + ((1 - L) % 2), U + 1, 2):
        X, Y = chain(u, anchor, v + 1 - u)[-2:]
        m = (1 << (v - 1)) - direct_word(X, horizon(v))[0].bit_count()
        upper_m = (1 << v) - direct_word(Y, horizon(v + 1))[0].bit_count()
        rows.append({'anchor': anchor, 'lower_margin': m, 'upper_margin': upper_m,
                     'quarter_ternary_constraint': (anchor - q) % three == 0})
    retained = [r for r in rows if r['quarter_ternary_constraint']]
    return {'v': v, 'anchor_level': u, 'depth_before_lower_level': v - u,
            'height_fixed_at_level': v + 1, 'L': L, 'U': U,
            'ternary_precision_at_anchor': s, 'ternary_modulus': three,
            'anchor_Q': q, 'odd_anchor_count': len(rows),
            'lower_margin_nonnegative_count': sum(r['lower_margin'] >= 0 for r in rows),
            'upper_margin_negative_count': sum(r['upper_margin'] < 0 for r in rows),
            'negative_upper_with_nonnegative_lower_count': sum(r['lower_margin'] >= 0 > r['upper_margin'] for r in rows),
            'retained_anchor_count': len(retained),
            'retained_upper_margin_minimum': min(r['upper_margin'] for r in retained),
            'retained_upper_negative_count': sum(r['upper_margin'] < 0 for r in retained),
            'selection': 'Exploratory finite interval, exhaustively enumerated; not held-out validation.',
            'scope': 'This finite filtering success is not extrapolated to other levels or depths.',
            'rows': rows}


def run():
    mixed_path = NOTES / 'post_v6_mixed_2026-09-25/mixed_results.json'
    margin_path = NOTES / 'post_v6_margin_2026-09-25/margin_results.json'
    raw_mixed, raw_margin = mixed_path.read_bytes(), margin_path.read_bytes()
    mixed, margin = json.loads(raw_mixed), json.loads(raw_margin)
    filters = []
    for v in (6, 8, 10, 12):
        H = horizon(v)
        word = direct_word(tower(v), H)[0]
        for depth in (1, 2, 3):
            u = v - depth
            Q = tower(u)
            L, U = ancestor_interval(u, v)
            N = U - L + 1
            candidate = word_candidate(v, word, H, depth)
            h_iso = isolation_bits(Q, L, U)
            assert class_count(L, U, Q, h_iso) == 1
            if h_iso:
                assert class_count(L, U, Q, h_iso - 1) > 1
            if depth >= 2:
                assert U < (1 << H) and int(candidate['count_hex'], 16) == 1
                assert int(candidate['first_hex'], 16) == Q
            assert N <= Q // (1 << depth) + 1
            filters.append({'v': v, 'depth': depth, 'anchor_level': u, 'H': H,
                            'anchor_Q_bits': Q.bit_length(), 'anchor_count_hex': hex(N),
                            'anchor_count_bit_length': N.bit_length(),
                            'all_words_injective_from_bits': ceil_log2(N),
                            'actual_word_isolates_from_bits': h_iso, **candidate})
    old_ancestry = []
    for row in mixed['mixed_adversaries']:
        X, v = int(row['X_hex'], 16), row['v']
        one, two = recover_ancestor(v, X, 1), recover_ancestor(v, X, 2)
        old_ancestry.append({'v': v, 'kind': row['kind'], 'precision_choice': row['precision_choice'],
                             'has_one_integer_ancestor': one is not None,
                             'has_two_integer_ancestors': two is not None})
    pure_examples = []
    for row in margin['generic_quadratic_adversaries']:
        if row['kind'] != 'actual_prefix' or row['v'] not in (10, 12):
            continue
        v, K = row['v'], row['H_next']
        residue = int(row['X_hex'], 16) & ((1 << K) - 1)
        k = pure_parameter(v, residue, K)
        assert k > 1 and k % 2 == 1
        low = direct_word(residue, horizon(v))[0]
        upper_residue = pure_residue(v + 1, k, K)
        high = direct_word(upper_residue, K)[0]
        assert upper_residue == quadratic(v, residue) & ((1 << K) - 1)
        assert low.bit_count() == row['lower_odd'] and high.bit_count() == row['upper_odd']
        pure_examples.append({'v': v, 'K': K, 'k_hex': hex(k), 'residue_hex': hex(residue),
                              'upper_residue_hex': hex(upper_residue),
                              'lower_margin': row['lower_margin'], 'upper_margin': row['upper_margin'],
                              'k_not_one': True, 'same_binade_as_Q_v': False,
                              'scope': 'Exact modular certificate of a pure-power family with another exponent k; full integer not constructed.'})
    examples = [one_ancestor_example(v) for v in (10, 12)]
    examples += [deeper_margin_example(10, depth) for depth in (2, 3, 4, 5)]
    exhaustive = exhaustive_small_anchor_case()
    for row in examples:
        print(json.dumps({k: row[k] for k in ('v', 'depth_before_lower_level', 'lower_margin',
                                            'upper_margin', 'same_complete_lower_word')}), flush=True)
    return {'scope': 'Finite exact ancestry filters and generic chains; no uniform parity bound.',
            'source_sha256': {str(p.relative_to(NOTES.parent)): hashlib.sha256(raw).hexdigest()
                              for p, raw in ((mixed_path, raw_mixed), (margin_path, raw_margin))},
            'ancestry_filters': filters, 'previous_mixed_examples': old_ancestry,
            'pure_power_parameter_examples': pure_examples, 'coherent_counterexamples': examples,
            'exhaustive_ancestry_filter': exhaustive,
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'uniform_delta_bound_proved': False, 'uniform_family_descent_proved': False,
            'mathematical_novelty_established': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'ancestry_results.json')
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
