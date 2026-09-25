#!/usr/bin/env python3
"""Exact finite checks of prefix-preserving arithmetic word conditions.

The paper arguments are separate: this program neither proves Chim's theorem
nor proves the bounded-loss hypothesis for all levels.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
COMPENSATION = HERE.parent / 'post_v6_compensation_2026-09-25'
sys.path.insert(0, str(COMPENSATION))
from block_engine import horizon, initial_residue, parity_trace


def digest_int(n):
    if n < 0:
        raise ValueError('nonnegative fingerprint expected')
    return hashlib.sha256(n.to_bytes(max(1, (n.bit_length() + 7) // 8), 'little')).hexdigest()


@lru_cache(maxsize=None)
def leaf_affine(word, length):
    odd, multiplier, constant = 0, 1, 0
    for i in range(length):
        if (word >> i) & 1:
            odd += 1
            multiplier *= 3
            constant = 3 * constant + (1 << i)
    return odd, multiplier, constant


def affine_word(word, length):
    """Return p,3^p,C for a chronological word packed least-significant bit first."""
    if length < 0 or word < 0 or word.bit_length() > length:
        raise ValueError('word outside its length')
    if length <= 16:
        return leaf_affine(word, length)
    left = length // 2
    p, P, A = affine_word(word & ((1 << left) - 1), left)
    j, J, B = affine_word(word >> left, length - left)
    return p + j, P * J, J * A + (B << left)


def word_residue(word, length):
    p, P, C = affine_word(word, length)
    return (-C * pow(P, -1, 1 << length)) % (1 << length)


def modular_power(base, exponent, bits):
    mask = (1 << bits) - 1
    result = 1
    while exponent:
        if exponent & 1:
            result = result * base & mask
        exponent >>= 1
        if exponent:
            base = base * base & mask
    return result & mask


def analyze_word(v, prefix, r, block, b, expect_reachable=None):
    k, P, A = affine_word(prefix, r)
    j, J, B = affine_word(block, b)
    p, n = k + j, r + b
    C = J * A + (B << r)
    full_multiplier = P * J
    L = v + 3 + n
    E = (1 << (v + 1)) + p
    c = (C << (v + 3)) - full_multiplier
    require_positive_loss = 589 * j > 305 * b
    assert require_positive_loss and p >= 1
    assert full_multiplier - (1 << p) <= C
    assert C <= (full_multiplier - (1 << p)) << (n - p)
    assert c > 1 and c % 2 and c % 3
    s = v + r + j + 1
    assert b < 2 * j and c >= 1 << s and L <= 2 * s
    numerator_mod = (modular_power(3, E, L) + c) & ((1 << L) - 1)
    reachable = numerator_mod == 0
    if expect_reachable is not None:
        assert reachable == expect_reachable
    # A second form keeps the prefix and the cylinder residue of the block.
    beta_residue = (-B * pow(J, -1, 1 << b)) % (1 << b)
    short_c = ((A - (beta_residue << r)) << (v + 3)) - P
    short_E = (1 << (v + 1)) + k
    centered_c = ((short_c + (1 << (L - 1))) & ((1 << L) - 1)) - (1 << (L - 1))
    short_power = modular_power(3, short_E, L)
    assert ((short_power + short_c) & ((1 << L) - 1) == 0) == reachable
    assert ((short_power + centered_c) & ((1 << L) - 1) == 0) == reachable
    return {'v': v, 'r': r, 'k': k, 'b': b, 'j': j,
            'block_loss': 589 * j - 305 * b, 'capacity': 128 * v * v,
            'violates_capacity': 589 * j - 305 * b > 128 * v * v,
            'word_reachable_from_Q_v': reachable,
            'modulus_exponent_L': L, 'power_exponent_E': E,
            'full_constant_bits': c.bit_length(), 'full_constant_sha256': digest_int(c),
            'height_lower_bound_bits_s': s, 'L_le_2s': L <= 2 * s,
            'full_chim_rhs_over_L_strict_lower_bound': 36000000,
            'short_constant_bits': abs(short_c).bit_length(),
            'centered_short_constant_bits': abs(centered_c).bit_length(),
            'centered_short_constant_sign': 1 if centered_c > 0 else -1,
            'scope': 'The Chim comparison concerns the full-word representation only.'}


def high_complexity_word(t):
    codes = {'0': '11010', '1': '10110'}
    text = ''.join(codes[bit] for i in range(1 << t) for bit in format(i, f'0{t}b'))
    word = int(text[::-1], 2)
    assert len(text) == 5 * t * (1 << t)
    assert text.count('1') == 3 * t * (1 << t) and '111' not in text
    factors = {text[i * 5 * t:(i + 1) * 5 * t] for i in range(1 << t)}
    assert len(factors) == 1 << t
    return word, len(text)


def run():
    baseline_raw = (COMPENSATION / 'holdout_results.json').read_bytes()
    baseline = json.loads(baseline_raw)
    actual = []
    for old in baseline['rows']:
        v, H = old['v'], old['horizon']
        trace = parity_trace(initial_residue(v, H), H)
        assert hashlib.sha256(trace).hexdigest() == old['parity_trace_sha256']
        packed = int.from_bytes(trace, 'little')
        r, end = old['C']['drawdown_from_step'], old['C']['drawdown_to_step']
        b = end - r
        prefix, block = packed & ((1 << r) - 1), (packed >> r) & ((1 << b) - 1)
        row = analyze_word(v, prefix, r, block, b, expect_reachable=True)
        assert row['block_loss'] == old['C']['maximum_drawdown']
        row['source_parity_sha256'] = old['parity_trace_sha256']
        actual.append(row)
        print(json.dumps({'v': v, 'full_constant_bits': row['full_constant_bits'],
                          'L': row['modulus_exponent_L'], 'congruence_verified': True}), flush=True)
    constructed = []
    for t in (8, 10):
        word, n = high_complexity_word(t)
        v = 2 * t
        assert n <= horizon(v)
        row = analyze_word(v, 0, 0, word, n, expect_reachable=False)
        assert row['violates_capacity']
        row.update({'t': t, 'factor_length': 5 * t, 'distinct_aligned_factors': 1 << t,
                    'maximum_ones_run': 2, 'scope': 'Generic admissible words; not observed words of Q_v.'})
        constructed.append(row)
    return {'scope': 'Exact finite checks of arithmetic equivalences and paper-level obstructions.',
            'source_holdout_sha256': hashlib.sha256(baseline_raw).hexdigest(),
            'actual_worst_blocks': actual, 'constructed_high_complexity_words': constructed,
            'uniform_compensation_proved': False, 'new_lean_declarations': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'arithmetic_results.json')
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
