#!/usr/bin/env python3
"""Exact finite tests for dyadic freedom after cancellation-tower bursts.

All computations use integer arithmetic. Modular tests classify finite words;
they do not construct an infinite positive orbit or imply divergence.
"""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path


def v2(n):
    if n <= 0:
        raise ValueError('valuation requires a positive integer')
    return (n & -n).bit_length() - 1


def step(n):
    a = v2(3 * n + 1)
    return (3 * n + 1) >> a, a


def cofactor_mod(v, q, bits):
    modulus = 1 << (v + 3 + bits)
    n = (pow(9, (1 << v) * q, modulus) - 1) % modulus
    assert n % (1 << (v + 3)) == 0
    return n >> (v + 3)


def affine(word):
    p, c, a = 1, 0, 0
    for exponent in word:
        c = 3 * c + (1 << a)
        p *= 3
        a += exponent
    return p, c, a


def inverse_cofactor(v, target, bits):
    root = 0
    for b in range(1, bits + 1):
        candidates = (root, root + (1 << (b - 1)))
        good = [q for q in candidates if cofactor_mod(v, q, b) == target % (1 << b)]
        assert len(good) == 1, (v, target, b, candidates)
        root = good[0]
    return root


def word_root(v, phase, word):
    assert v >= 1 and phase in ('B', 'C')
    assert word and word[0] >= 2 and all(a >= 1 for a in word)
    p, c, a = affine(word)
    modulus = 1 << a
    multiplier = pow(3, v + (4 if phase == 'B' else 0), modulus)
    assert ((1 << a) + p - c) % 2 == 0
    target = (((1 << a) + p - c) // 2 * pow(p * multiplier, -1, modulus)) % modulus
    root = inverse_cofactor(v, target, a)
    assert root % 2 == 1
    return root, a


def matches_mod(v, phase, q, word):
    _, _, a = affine(word)
    modulus = 1 << (a + 1)
    multiplier = pow(3, v + (4 if phase == 'B' else 0), modulus)
    n = (2 * multiplier * cofactor_mod(v, q, a + 1) - 1) % modulus
    for desired in word:
        n, actual = step(n)
        if actual != desired:
            return False
    return True


def positive_compositions(n):
    if n == 0:
        yield ()
    for a in range(1, n + 1):
        for rest in positive_compositions(n - a):
            yield (a,) + rest


def run():
    word_cases = 0
    modular_checks = 0
    digest = hashlib.sha256()
    # Exhaust all positive words with first exponent >=2 and sum <=9.
    words = [w for a in range(2, 10) for w in positive_compositions(a) if w[0] >= 2]
    for v in (1, 2, 3, 7, 16, 64):
        for phase in ('B', 'C'):
            for word in words:
                root, a = word_root(v, phase, word)
                actual = [q for q in range(1, 1 << a, 2) if matches_mod(v, phase, q, word)]
                assert actual == [root], (v, phase, word, actual, root)
                # Periodicity on additional positive representatives.
                for j in (1, 2, 17):
                    assert matches_mod(v, phase, root + (j << a), word)
                word_cases += 1
                modular_checks += (1 << (a - 1)) + 3
                digest.update(repr((v, phase, word, root, a)).encode())
    # Independently evaluate actual integers and actual Syracuse trajectories.
    actual_cases = 0
    for v in range(1, 7):
        for q in range(1, 64, 2):
            power = 9 ** ((1 << v) * q)
            cofactor = (power - 1) >> (v + 3)
            assert cofactor % 2 == 1
            for phase in ('B', 'C'):
                y = 9 * power - 10 if phase == 'B' else (power - 5) // 4
                length = v + (2 if phase == 'B' else 0)
                multiplier = 3 ** (v + (4 if phase == 'B' else 0))
                n = y
                for _ in range(length):
                    nxt, a = step(n)
                    assert a == 1 and nxt > n
                    n = nxt
                assert n == 2 * multiplier * cofactor - 1
                word = []
                for _ in range(4):
                    n, a = step(n)
                    word.append(a)
                assert word[0] >= 2
                root, bits = word_root(v, phase, word)
                assert q % (1 << bits) == root
                assert matches_mod(v, phase, q, word)
                actual_cases += 1
    # Any finite number of extra exponent-one steps can follow exponent 2.
    witnesses = []
    for v in (1, 2, 7):
        for length in (1, 2, 4, 8, 16, 32, 64):
            word = (2,) + (1,) * length
            root, bits = word_root(v, 'C', word)
            assert matches_mod(v, 'C', root, word)
            witnesses.append({'v': v, 'word': f'[2] ++ [1]^{length}', 'q_residue': str(root), 'modulus_exponent': bits})
    return {
        'scope': 'Exact finite checks, not a universal proof or an infinite-orbit witness',
        'all_checks_passed': True,
        'words_per_phase_and_v': len(words),
        'unique_word_residue_cases': word_cases,
        'modular_membership_checks': modular_checks,
        'actual_integer_trajectory_cases': actual_cases,
        'residue_certificate_sha256': digest.hexdigest(),
        'delayed_compensation_witnesses': witnesses,
        'limitations': [
            'Different finite suffixes may require different positive q.',
            'A compatible infinite word may correspond only to a non-natural 2-adic parameter.',
            'Parameter-residue frequencies are not natural densities of the exponentially sized starting integers.',
            'No uniform descent or independence claim for a fixed positive orbit.'
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('transport_results.json'))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'delayed_compensation_witnesses'}, indent=2))


if __name__ == '__main__':
    main()
