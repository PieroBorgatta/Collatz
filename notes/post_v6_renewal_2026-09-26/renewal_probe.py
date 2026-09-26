#!/usr/bin/env python3
"""Sharp information budgets for prefix-only quadratic-pair certificates.

This does not exclude certificates using the exact tower source beyond
its exposed binary prefix. Historical traces are replayed, not extended.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
COMPENSATION = ROOT / 'notes/post_v6_compensation_2026-09-25'
ARITHMETIC = ROOT / 'notes/post_v6_arithmetic_2026-09-25'
sys.path.insert(0, str(COMPENSATION))
sys.path.insert(0, str(ARITHMETIC))
from block_engine import horizon, initial_residue, parity_trace
from arithmetic_probe import word_residue


def f(v: int, x: int) -> int:
    if v < 0:
        raise ValueError('nonnegative level required')
    return x + (x * x << (v + 2))


def direct_word(x: int, k: int) -> int:
    if x < 0 or k < 0:
        raise ValueError('nonnegative state and horizon required')
    word = 0
    for t in range(k):
        p = x & 1
        word |= p << t
        x = (3 * x + 1) // 2 if p else x // 2
    return word


def cylinder_envelope(lower_odd: int, H: int, K: int,
                      upper_word: int, M: int) -> dict:
    if not 0 <= lower_odd <= H <= M <= K or upper_word < 0 or upper_word.bit_length() > K:
        raise ValueError('valid horizons, weight, word and precision required')
    prefix_odd = (upper_word & ((1 << M) - 1)).bit_count()
    low = prefix_odd - 2 * lower_odd
    return {'minimum': low, 'maximum': low + K - M,
            'free_bits': K - M, 'upper_prefix_odd': prefix_odd}


def minimum_precision(lower_odd: int, H: int, K: int,
                      upper_word: int, g: int) -> int | None:
    """Earliest M>=H whose sharp cylinder upper bound is at most g.

    Binary search uses only the queried prefixes' counts. No random model
    or fitted density enters the stopping condition.
    """
    if cylinder_envelope(lower_odd, H, K, upper_word, K)['maximum'] > g:
        return None
    lo, hi = H, K
    while lo < hi:
        mid = (lo + hi) // 2
        if cylinder_envelope(lower_odd, H, K, upper_word, mid)['maximum'] <= g:
            hi = mid
        else:
            lo = mid + 1
    return lo


def inverse_f(v: int, target: int, bits: int) -> int:
    if v < 0 or bits < 0 or not 0 <= target < (1 << bits):
        raise ValueError('valid quadratic target and precision required')
    x, precision = target & 1, min(1, bits)
    while precision < bits:
        precision = min(2 * precision, bits)
        modulus = 1 << precision
        derivative = 1 + (x << (v + 3))
        x = (x - (f(v, x) - target) * pow(derivative, -1, modulus)) & (modulus - 1)
    return x


def integer_ancestor(v: int, x: int) -> int | None:
    """Positive integer predecessor under f_(v-1), with its congruence check."""
    if v < 1 or x < 1:
        raise ValueError('positive level and integer required')
    signature = 1 + (x << (v+3))
    root = isqrt(signature)
    scale = 1 << (v+2)
    if root * root != signature or (root-1) % scale:
        return None
    candidate = (root-1) // scale
    return candidate if candidate > 0 else None


def extremal_lift(v: int, x: int, K: int, M: int, all_ones: bool = True) -> int:
    """Keep x's low M and high >=K bits, force the remaining upper outputs.

    The representative is positive if x>=2^K. This function also permits
    small nonnegative test inputs for which the representative can be zero.
    """
    if v < 0 or x < 0 or not 0 <= M <= K:
        raise ValueError('valid level, source and precision required')
    prefix = direct_word(f(v, x), M)
    target_word = prefix | ((((1 << (K-M)) - 1) << M) if all_ones else 0)
    target_residue = word_residue(target_word, K)
    low = inverse_f(v, target_residue, K)
    result = ((x >> K) << K) | low
    assert (result - x) % (1 << M) == 0
    assert result >> K == x >> K
    assert direct_word(f(v, result), K) == target_word
    return result


def block_reward_envelope(v: int, x: int, t: int, b: int, B: int) -> dict:
    """Exact range for the next b lower / 2b WW-upper steps.

    B initial source bits must already fix both histories and the next
    lower block. Only the forced upper prefix enters the computed bound.
    """
    start, end = 2 * t - 1, 2 * t + 2 * b - 1
    if v < 0 or x < 0 or t < 1 or b < 1 or not max(t+b, start) <= B <= end:
        raise ValueError('invalid paired block or source precision')
    lower_word = direct_word(x, t+b)
    lower_odd = ((lower_word >> t) & ((1 << b) - 1)).bit_count()
    # WW=2f(x): its first output is zero; subsequent outputs are those of f(x).
    upper_word = direct_word(f(v, x), B)
    fixed = B - start
    fixed_odd = ((upper_word >> start) & ((1 << fixed) - 1)).bit_count()
    minimum = fixed_odd - 2 * lower_odd
    return {'minimum': minimum, 'maximum': minimum + end - B,
            'fixed_upper_steps': fixed, 'free_upper_steps': end - B,
            'lower_block_odd': lower_odd}


@lru_cache(maxsize=None)
def tower_trace(v: int) -> tuple[int, str]:
    bits = horizon(v)
    packed = parity_trace(initial_residue(v, bits), bits)
    return int.from_bytes(packed, 'little'), hashlib.sha256(packed).hexdigest()


def threshold_record(v: int, baseline: dict[int, dict]) -> dict:
    H, K = horizon(v), horizon(v + 1)
    lower, low_hash = tower_trace(v)
    upper, upper_hash = tower_trace(v + 1)
    j, j_next = lower.bit_count(), upper.bit_count()
    for level, count, digest in ((v, j, low_hash), (v+1, j_next, upper_hash)):
        assert baseline[level]['odd_steps'] == count
        assert baseline[level]['parity_trace_sha256'] == digest
    g, delta = 2 * (1 << ((v + 1) // 2)), j_next - 2 * j
    M = minimum_precision(j, H, K, upper, g)
    record = {'v': v, 'H': H, 'K': K, 'lower_odd': j, 'upper_odd': j_next,
              'delta_actual': delta, 'target_g': g,
              'target_is_uniform_candidate_only_from_v16': v >= 16,
              'required_observed_upper_zeroes': K - 2*j - g,
              'minimum_source_precision': M,
              'unexposed_bits_at_certificate': None if M is None else K-M,
              'lower_parity_sha256': low_hash, 'upper_parity_sha256': upper_hash,
              'old_complete_parity_hashes_match': True,
              'envelope_at_H': cylinder_envelope(j, H, K, upper, H)}
    if M is not None:
        at = cylinder_envelope(j, H, K, upper, M)
        before = cylinder_envelope(j, H, K, upper, M-1) if M > H else None
        assert at['maximum'] <= g and (before is None or before['maximum'] > g)
        actual_zeroes_suffix = K - M - (upper >> M).bit_count()
        assert at['maximum'] == delta + actual_zeroes_suffix
        record.update({'envelope_at_minimum': at, 'envelope_one_bit_before': before,
                       'actual_suffix_zeroes': actual_zeroes_suffix,
                       'minimality_verified': True})
    else:
        assert delta > g
        record['minimality_verified'] = True
    return record


def witness_record(row: dict) -> dict | None:
    v, K, H, minimum = row['v'], row['K'], row['H'], row['minimum_source_precision']
    if minimum is None or minimum == H:
        return None
    M, Q = minimum - 1, (3**(1 << (v+1)) - 1) >> (v+3)
    X = extremal_lift(v, Q, K, M)
    Y = f(v, X)
    low, upper = direct_word(X, H), direct_word(Y, K)
    actual_lower, _ = tower_trace(v)
    assert low == actual_lower
    assert X > 0 and X != Q and X.bit_length() == Q.bit_length()
    assert upper >> M == (1 << (K-M)) - 1
    defect = upper.bit_count() - 2 * low.bit_count()
    assert defect == row['target_g'] + 1 == row['envelope_one_bit_before']['maximum']
    ancestor = integer_ancestor(v, X)
    second = integer_ancestor(v-1, ancestor) if ancestor is not None else None
    # Two positive integer ancestors plus this binade and lower word would
    # force X=Q, by the earlier ancestry lemma. No tower counterexample arises.
    assert second is None
    return {'v': v, 'precision_M': M, 'horizon_K': K, 'target_g': row['target_g'],
            'witness_delta': defect, 'X_hex': hex(X), 'Y_hex': hex(Y),
            'preserves_low_M_and_high_from_K': True,
            'same_lower_full_parity_word': True, 'same_source_binade': True,
            'exact_quadratic_relation': True, 'is_actual_tower_source': False,
            'has_one_positive_integer_ancestor': ancestor is not None,
            'has_two_positive_integer_ancestors': second is not None}


def block_examples() -> list[dict]:
    records = []
    for v, t, b in ((5, 5, 2), (8, 9, 4), (12, 17, 8)):
        Q = (3**(1 << (v+1)) - 1) >> (v+3)
        B, end = 2*t-1, 2*t+2*b-1
        envelope = block_reward_envelope(v, Q, t, b, B)
        X = extremal_lift(v, Q, end, B)
        lower = direct_word(X, t+b)
        up = direct_word(2*f(v, X), 2*t+2*b)
        reward = ((up >> (2*t)) & ((1 << (2*b))-1)).bit_count() - 2*((lower >> t) & ((1 << b)-1)).bit_count()
        assert direct_word(X, t+b) == direct_word(Q, t+b)
        assert direct_word(2*f(v, X), 2*t) == direct_word(2*f(v, Q), 2*t)
        assert reward == envelope['maximum']
        records.append({'v': v, 't': t, 'lower_block_length': b,
                        'source_precision_before': B, 'source_precision_needed': end,
                        'fresh_bits_for_exact_prediction': 2*b, **envelope,
                        'maximum_reward_attained': reward,
                        'witness_X_hex': hex(X), 'same_past_pair_verified': True,
                        'next_lower_block_preserved': True, 'is_actual_tower_source': False})
    return records


def positive_loop(v: int, k: int, L: int, prefix_length: int | None = None) -> dict:
    """A finite positive self-loop in the projection to two residues.

    The default preserves only the first v+3 actual lower parities, NOT
    the full lower horizon. Other parameters can return the tower itself
    when its finite parity word already has the requested run pattern.
    """
    if v < 5 or k < 1 or L < 1:
        raise ValueError('v>=5 and positive width/duration required')
    h = v+3 if prefix_length is None else prefix_length
    if h < 0:
        raise ValueError('nonnegative preserved prefix required')
    t = max(h, L+k+1)
    a, K = t+L+k, 2*t+2*L+k-1
    Q = (3**(1 << (v+1)) - 1) >> (v+3)
    if Q < (1 << K):
        raise ValueError('source too short to preserve its binade in this construction')
    lower_prefix = direct_word(Q, h)
    lower_residue = word_residue(lower_prefix, a)  # zero outputs from h to a
    fixed_upper = direct_word(f(v, lower_residue), 2*t-1)
    target_word = fixed_upper | (((1 << (2*L+k))-1) << (2*t-1))
    target_residue = word_residue(target_word, K)
    X = ((Q >> K) << K) | inverse_f(v, target_residue, K)
    U = 2*f(v, X)
    assert X > 0 and X.bit_length() == Q.bit_length()
    assert X >> K == Q >> K
    assert direct_word(X, a) == lower_prefix
    assert direct_word(f(v, X), K) == target_word
    lower_state, upper_state = X, U
    for _ in range(t):
        lower_state = (3*lower_state+1)//2 if lower_state & 1 else lower_state//2
    for _ in range(2*t):
        upper_state = (3*upper_state+1)//2 if upper_state & 1 else upper_state//2
    mask, rewards = (1 << k)-1, []
    for i in range(L+1):
        assert (lower_state & mask, upper_state & mask) == (0, mask)
        if i == L:
            break
        low_p, up_count = lower_state & 1, 0
        lower_state = (3*lower_state+1)//2 if low_p else lower_state//2
        for _ in range(2):
            p = upper_state & 1
            up_count += p
            upper_state = (3*upper_state+1)//2 if p else upper_state//2
        rewards.append(up_count - 2*low_p)
    assert rewards == [2]*L
    return {'v': v, 'residue_bits': k, 'loop_steps': L,
            'preserved_actual_lower_prefix_length': h,
            'full_lower_horizon': horizon(v),
            'paired_start_time': t, 'source_precision': K,
            'loop_lies_within_lower_target_horizon': t+L <= horizon(v),
            'projected_state': [0, mask], 'per_step_reward': 2,
            'total_reward': sum(rewards), 'states_checked': L+1,
            'X_hex': hex(X), 'U_hex': hex(U),
            'same_Q_binade_and_high_bits_from_K': True,
            'exact_quadratic_pair': True, 'is_actual_tower_source': X == Q,
            'scope': 'Finite loop of the residue projection; not a numerical or infinite Collatz cycle.'}


def actual_projection_loop(v: int, t: int, k: int, L: int) -> dict:
    """Verify a specified short projected loop directly on the actual tower."""
    if v < 5 or t < 0 or k < 1 or L < 1 or t+L > horizon(v):
        raise ValueError('valid loop within the lower target horizon required')
    Q = (3**(1 << (v+1)) - 1) >> (v+3)
    U = 2*f(v, Q)
    lower, upper = Q, U
    for _ in range(t):
        lower = (3*lower+1)//2 if lower & 1 else lower//2
    for _ in range(2*t):
        upper = (3*upper+1)//2 if upper & 1 else upper//2
    mask, states, rewards = (1 << k)-1, [], []
    for i in range(L+1):
        if (lower & mask, upper & mask) != (0, mask):
            raise ValueError('specified actual trajectory has no such projected loop')
        states.append([hex(lower), hex(upper)])
        if i == L:
            break
        p, count = lower & 1, 0
        lower = (3*lower+1)//2 if p else lower//2
        for _ in range(2):
            q = upper & 1
            count += q
            upper = (3*upper+1)//2 if q else upper//2
        rewards.append(count-2*p)
    if rewards != [2]*L:
        raise ValueError('specified actual projected loop does not have reward two per step')
    return {'v': v, 'paired_start_time': t, 'residue_bits': k,
            'loop_steps': L, 'projected_state': [0, mask],
            'per_step_reward': 2, 'total_reward': sum(rewards),
            'integer_state_pairs_hex': states,
            'is_actual_tower_source': True,
            'loop_lies_within_lower_target_horizon': True,
            'scope': 'A finite repeated residue pair on the actual orbit, not an integer cycle or a bound on the total defect.'}


def produce(max_v: int = 23) -> dict:
    if not 5 <= max_v <= 23:
        raise ValueError('comparison restricted to historical pairs v=5..23')
    baseline_path = ROOT / 'notes/post_v6_margin_2026-09-25/margin_results.json'
    baseline = {r['v']: r for r in json.loads(baseline_path.read_text())['levels']}
    rows = [threshold_record(v, baseline) for v in range(5, max_v+1)]
    witnesses = [w for row in rows if row['v'] <= 12 for w in [witness_record(row)] if w is not None]
    loops = [positive_loop(v, k, L) for v, k, L in ((5, 3, 8), (8, 4, 16), (12, 8, 64))]
    assert all(not row['is_actual_tower_source'] for row in loops)
    actual_loop = actual_projection_loop(5, 18, 1, 1)
    assert actual_loop['is_actual_tower_source']
    return {'schema': 1,
            'scope': 'Sharp prefix-cylinder certificates with exact quadratic pairing; not a bound on the singleton tower.',
            'baseline_sha256': hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
            'levels': rows, 'threshold_failure_witnesses': witnesses,
            'local_renewal_witnesses': block_examples(),
            'positive_residue_loops': loops,
            'actual_short_projection_loop': actual_loop,
            'unique_historical_levels_replayed': list(range(5, max_v+2)),
            'unique_historical_steps_replayed': sum(horizon(v) for v in range(5, max_v+2)),
            'new_tower_levels': [], 'new_lean_declarations': 0,
            'uniform_near_full_precision_claim': False,
            'uniform_delta_bound_proved': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-v', type=int, default=23)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = produce(args.max_v)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'pairs': len(data['levels']), 'steps': data['unique_historical_steps_replayed'],
                      'threshold_witnesses': len(data['threshold_failure_witnesses'])}))


if __name__ == '__main__':
    main()
