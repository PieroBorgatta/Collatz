#!/usr/bin/env python3
"""Exact CRT/height checks for truncated binary and ternary tower constraints.

The examples are generic integers, not new levels of the distinguished tower.
No uniform bound on its parity counts is asserted.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
MARGIN = NOTES / 'post_v6_margin_2026-09-25'
sys.path.insert(0, str(MARGIN))
from margin_probe import direct_word, horizon, quadratic
from arithmetic_probe import affine_word


def tower(v):
    if v < 0:
        raise ValueError('nonnegative level expected')
    return (3 ** (1 << (v + 1)) - 1) >> (v + 3)


def ceil_log2(x):
    if x < 1:
        raise ValueError('positive integer expected')
    return (x - 1).bit_length()


def floor_log3(x):
    if x < 1:
        raise ValueError('positive integer expected')
    lo, hi = 0, x.bit_length()
    while lo + 1 < hi:
        middle = (lo + hi) // 2
        if 3 ** middle <= x:
            lo = middle
        else:
            hi = middle
    return lo


def ternary_valuation(x):
    if not x:
        raise ValueError('valuation of zero is not finite')
    x = abs(x)
    result = 0
    while x % 3 == 0:
        x //= 3
        result += 1
    return result


def candidate_count(Q, Z, h, s):
    """Count X=Q mod 2^h*3^s in the integer interval [Z,2Z)."""
    if not 0 < Z <= Q < 2 * Z or min(h, s) < 0:
        raise ValueError('invalid interval or precision')
    modulus = (1 << h) * 3 ** s
    return 1 + (Q - Z) // modulus + (2 * Z - 1 - Q) // modulus


def isolation_threshold(Q, Z, h):
    """Smallest s>=0 for which that class isolates Q in [Z,2Z)."""
    if not 0 < Z <= Q < 2 * Z or h < 0:
        raise ValueError('invalid interval or precision')
    needed = max(Q - Z + 1, 2 * Z - Q)
    two = 1 << h
    ternary_needed = (needed + two - 1) // two
    s = floor_log3(ternary_needed)
    return s + (3 ** s < ternary_needed)


def crt_representative(Q, K, r, s):
    """Preserve residue r mod 2^K and Q mod 3^s in Q's R-bit block.

    P<=Z is a sufficient existence guarantee, not a necessary condition.
    R=ceil(log2(P)); high bits at positions >=R are retained, not those >=K.
    """
    if Q < 1 or min(K, s) < 0 or not 0 <= r < (1 << K):
        raise ValueError('invalid CRT inputs')
    Z = 1 << (Q.bit_length() - 1)
    two, three = 1 << K, 3 ** s
    P = two * three
    if P > Z:
        raise ValueError('CRT width guarantee does not apply')
    residue = r + two * (((Q - r) * pow(two, -1, three)) % three)
    R = ceil_log2(P)
    A = (Q >> R) << R
    X = A + ((residue - A) % P)
    assert Z <= X < 2 * Z and (X >> R) == (Q >> R)
    assert X % two == r and (X - Q) % three == 0
    return X, P, R


def transport_data(v, x, n, s):
    """Check the affine endpoint congruence, with exact rational widths."""
    if v < 0 or x < 1 or min(n, s) < 0:
        raise ValueError('invalid transport inputs')
    word, Y = direct_word(x, n)
    j, multiplier, C = affine_word(word, n)
    a, two = 1 << (v + 3), 1 << n
    modulus = 3 ** (s + j)
    residue = (pow(two, -1, modulus)
               * (C - pow(a, -1, modulus) * multiplier)) % modulus
    identity = a * two * Y - a * C + multiplier == multiplier * (a * x + 1)
    equivalence = ((a * x + 1) % (3 ** s) == 0) == (Y % modulus == residue)
    Z = 1 << (x.bit_length() - 1)
    width = Fraction(multiplier * Z, two)
    ratio_identity = Fraction(modulus, 1) / width == Fraction(two * 3 ** s, Z)
    assert identity and equivalence and ratio_identity
    return {'n': n, 'j': j, 'word_hex': hex(word), 'C_hex': hex(C),
            'Y_hex': hex(Y), 'modulus_hex': hex(modulus),
            'transformed_residue_hex': hex(residue),
            'transport_identity': identity,
            'ternary_congruence_equivalent': equivalence,
            'precision_ratio_identity': ratio_identity}


def build_example(source, s, label):
    v = source['v']
    H, K, e = horizon(v), horizon(v + 1), 1 << (v + 1)
    if not 0 < s < e:
        raise ValueError('these examples use strictly truncated ternary precision')
    Q, Q_next = tower(v), tower(v + 1)
    old_X, old_Y = int(source['X_hex'], 16), int(source['Y_hex'], 16)
    assert old_Y == quadratic(v, old_X) and Q_next == quadratic(v, Q)
    r = old_X & ((1 << K) - 1)
    X, P, R = crt_representative(Q, K, r, s)
    Y = quadratic(v, X)
    lower_word, _ = direct_word(X, H)
    upper_word, _ = direct_word(Y, K)
    assert lower_word == direct_word(old_X, H)[0]
    assert upper_word == direct_word(old_Y, K)[0]
    lower_j, upper_j = lower_word.bit_count(), upper_word.bit_count()
    assert (lower_j, upper_j) == (source['lower_odd'], source['upper_odd'])
    lower_margin, upper_margin = (1 << (v - 1)) - lower_j, (1 << v) - upper_j
    assert lower_margin > 0 > upper_margin and X != Q
    a = 1 << (v + 3)
    assert 1 + 2 * a * Y == (1 + a * X) ** 2
    nu_difference = ternary_valuation(X - Q)
    nu_upper_difference = ternary_valuation(Y - Q_next)
    nu_signature = ternary_valuation(1 + a * X)
    assert nu_difference >= s and nu_upper_difference >= 2 * s
    assert ternary_valuation(1 + 2 * a * Y) == 2 * nu_signature
    if nu_difference < e:
        assert nu_upper_difference == 2 * nu_difference
    retains_actual = lower_word == direct_word(Q, H)[0]
    if source['kind'] == 'actual_prefix':
        assert retains_actual
    assert (X >> R) == (Q >> R) and abs(X - Q) < (1 << R)
    return {'v': v, 'kind': source['kind'], 'precision_choice': label,
            'H': H, 'K': K, 'e': e, 's': s, 'R': R,
            'Q_v_bits': Q.bit_length(), 'high_bits_retained': Q.bit_length() - R,
            'relative_distance_power2_exponent': Q.bit_length() - 1 - R,
            'distance_bound': 'abs(X-Q_v)/Q_v < 2^(-relative_distance_power2_exponent)',
            'lower_odd': lower_j, 'upper_odd': upper_j,
            'lower_margin': lower_margin, 'upper_margin': upper_margin,
            'delta': upper_j - 2 * lower_j,
            'old_signature_valuation': ternary_valuation(1 + a * old_X),
            'difference_valuation': nu_difference,
            'upper_difference_valuation': nu_upper_difference,
            'signature_valuation': nu_signature,
            'upper_signature_valuation': 2 * nu_signature,
            'same_lower_word_as_Q_v': retains_actual,
            'same_lower_and_upper_words_as_archived_adversary': True,
            'same_high_bits_at_positions_ge_R': True,
            'same_binade_as_Q_v': True,
            'X_hex': hex(X), 'Y_hex': hex(Y), 'crt_modulus_hex': hex(P),
            'lower_word_hex': hex(lower_word), 'upper_word_hex': hex(upper_word),
            'transport': transport_data(v, X, H, s),
            'scope': 'Generic pair, X != Q_v; no failure asserted for the actual tower.'}


def run():
    source_path = MARGIN / 'margin_results.json'
    raw = source_path.read_bytes()
    sources = json.loads(raw)['generic_quadratic_adversaries']
    examples, thresholds = [], []
    for v in sorted({row['v'] for row in sources}):
        Q, H, K = tower(v), horizon(v), horizon(v + 1)
        Z, e = 1 << (Q.bit_length() - 1), 1 << (v + 1)
        s_bad = floor_log3(Z >> K)
        s_iso = isolation_threshold(Q, Z, H)
        assert ((1 << K) * 3 ** s_bad) <= Z < ((1 << K) * 3 ** (s_bad + 1))
        assert candidate_count(Q, Z, H, s_iso) == 1
        assert candidate_count(Q, Z, H, s_iso - 1) > 1
        assert candidate_count(Q, Z, H, e - 1) == 1
        assert e // 4 <= s_bad < s_iso < e
        thresholds.append({'v': v, 'H': H, 'K': K, 'e': e, 'Q_v_bits': Q.bit_length(),
                           'quarter_precision': e // 4,
                           'all_upper_classes_guaranteed_through_s': s_bad,
                           'actual_lower_class_isolates_at_s': s_iso,
                           'candidate_count_at_s_iso_minus_1': candidate_count(Q, Z, H, s_iso - 1),
                           'candidate_count_at_s_iso': 1,
                           'candidate_count_at_e_minus_1': 1,
                           'gap_status': 'No universal existence or exclusion claim between thresholds.'})
    by_level = {row['v']: row for row in thresholds}
    for source in sources:
        v = source['v']
        for s, label in ((1 << (v - 1), 'quarter_of_full_ternary_precision'),
                         (by_level[v]['all_upper_classes_guaranteed_through_s'], 'last_guaranteed_precision')):
            row = build_example(source, s, label)
            examples.append(row)
            print(json.dumps({key: row[key] for key in
                              ('v', 'kind', 's', 'high_bits_retained', 'lower_margin', 'upper_margin')}), flush=True)
    return {'scope': 'Exact mixed-prime CRT adversaries and height thresholds; no new actual tower levels.',
            'source_sha256': {str(source_path.relative_to(NOTES.parent)): hashlib.sha256(raw).hexdigest()},
            'thresholds': thresholds, 'mixed_adversaries': examples,
            'uniform_quarter_precision_obstruction': 'Paper proof for generic pairs, every v>=6; finite examples here.',
            'uniform_delta_bound_proved': False, 'uniform_family_descent_proved': False,
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'mathematical_novelty_established': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'mixed_results.json')
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
