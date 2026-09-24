#!/usr/bin/env python3
"""Replay finite certificates using recurrence and direct modular Syracuse steps.

This verifier imports neither the certificate producer nor its block tables.
The last exponent is only known to be at least the remaining precision.
Finite arithmetic replay is not a proof of the sufficiency theorem or a Lean
verification. Levels above --max-v are explicitly reported as not replayed.
"""
import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
NUMERATOR, DENOMINATOR = 485, 306


class VerificationError(ValueError):
    """A certificate is malformed or disagrees with the independent replay."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def integer(value, name, minimum=0):
    require(type(value) is int and value >= minimum,
            f'{name}: expected an integer >= {minimum}')
    return value


def recurrence_residue(v, bits):
    """Q_v mod 2^bits, from Q_1=5 and the quadratic recurrence only."""
    integer(v, 'v', 1)
    integer(bits, 'precision_bits', 1)
    mask = (1 << bits) - 1
    residue = 5 & mask
    for level in range(1, v):
        residue = (residue + (residue * residue << (level + 2))) & mask
    return residue


def direct_syracuse_count(residue, bits):
    """Count odd steps through bits divisions, truncating the final exponent.

    Exact steps retain the known residue modulo the remaining power of two.
    If the next numerator vanishes modulo that power, its valuation is only
    bounded below: record that bound and stop without inventing an endpoint.
    """
    integer(bits, 'precision_bits', 1)
    require(type(residue) is int and 0 <= residue < (1 << bits),
            'residue is outside the supplied precision')
    require(residue & 1 == 1, 'the starting residue must be odd')
    remaining, count = bits, 0
    mask = (1 << bits) - 1
    exponent_digest = hashlib.sha256()
    while remaining:
        numerator = 3 * residue + 1
        exponent = (numerator & -numerator).bit_length() - 1
        count += 1
        if exponent >= remaining:
            # All these bits vanish. No higher bit of the true input is known.
            return {
                'odd_steps': count,
                'exact_exponent_steps': count - 1,
                'exact_exponent_sum': bits - remaining,
                'final_exponent_lower_bound': remaining,
                'final_exponent_is_exact': False,
                'exact_exponent_prefix_sha256': exponent_digest.hexdigest(),
            }
        require(exponent >= 1, 'a modular Syracuse state ceased to be odd')
        exponent_digest.update(str(exponent).encode('ascii') + b'\n')
        remaining -= exponent
        mask >>= exponent
        residue = (numerator >> exponent) & mask
    raise VerificationError('the direct replay ended without a final exponent')


def validate_attempt(attempt):
    """Check cheap record invariants, without claiming its orbit was replayed."""
    require(isinstance(attempt, dict), 'attempt must be an object')
    v = integer(attempt.get('v'), 'v', 5)
    budget = integer(attempt.get('budget'), 'budget', 1)
    require(budget <= (1 << v), 'budget exceeds 2^v')
    require(attempt.get('M') == 1 << v and type(attempt.get('M')) is int,
            'M does not equal 2^v')
    bits = integer(attempt.get('precision_bits'), 'precision_bits', 1)
    # A ceiling is calculated independently by divmod, not by the producer.
    dividend = NUMERATOR * budget + (2 * NUMERATOR - 3 * DENOMINATOR) * (1 << v)
    quotient, remainder = divmod(dividend, DENOMINATOR)
    expected_bits = quotient + (remainder != 0)
    require(bits == expected_bits, 'precision_bits disagrees with the 485/306 formula')
    count = integer(attempt.get('odd_steps'), 'odd_steps', 1)
    require(count <= bits, 'odd_steps exceeds the number of available binary steps')
    passed = attempt.get('certified')
    require(type(passed) is bool and passed == (count <= budget),
            'certified disagrees with odd_steps <= budget')
    upper = attempt.get('descent_time_upper_bound')
    require((type(upper) is int and upper == count) if passed else upper is None,
            'descent_time_upper_bound disagrees with the certificate decision')
    digest = attempt.get('initial_residue_sha256')
    require(isinstance(digest, str) and len(digest) == 64
            and all(c in '0123456789abcdef' for c in digest),
            'initial_residue_sha256 is not a lowercase SHA-256 digest')
    return v, budget, bits


def verify_attempt(attempt):
    """Return independent evidence, or raise VerificationError on disagreement."""
    require(3 ** DENOMINATOR < 2 ** NUMERATOR,
            'the claimed rational logarithm bound is false')
    v, budget, bits = validate_attempt(attempt)
    residue = recurrence_residue(v, bits)
    digest = hashlib.sha256(residue.to_bytes((bits + 7) // 8, 'little')).hexdigest()
    require(digest == attempt['initial_residue_sha256'],
            'initial_residue_sha256 disagrees with the quadratic recurrence')
    replay = direct_syracuse_count(residue, bits)
    require(replay['odd_steps'] == attempt['odd_steps'],
            'odd_steps disagrees with the direct modular Syracuse replay')
    passed = replay['odd_steps'] <= budget
    require(passed == attempt['certified'],
            'certified disagrees with the independently counted steps')
    return {
        'v': v, 'budget': budget, 'precision_bits': bits,
        'initial_residue_sha256': digest, 'certified': passed,
        'descent_time_upper_bound': replay['odd_steps'] if passed else None,
        **replay,
    }


def verify_document(document, max_v=18):
    """Check document consistency and independently replay the selected levels."""
    integer(max_v, 'max_v', 5)
    require(isinstance(document, dict), 'the JSON root must be an object')
    rational = document.get('rational_upper_bound')
    require(isinstance(rational, dict)
            and rational.get('numerator') == NUMERATOR
            and rational.get('denominator') == DENOMINATOR
            and rational.get('verified_integer_inequality') == '3^306<2^485',
            'the document does not specify the expected rational bound')
    require(3 ** DENOMINATOR < 2 ** NUMERATOR, 'the integer bound is false')
    rows = document.get('rows')
    require(isinstance(rows, list) and bool(rows), 'rows must be a nonempty list')
    minimum = integer(document.get('minimum_v'), 'minimum_v', 5)
    maximum = integer(document.get('maximum_v'), 'maximum_v', minimum)
    require(minimum == 5, 'minimum_v must be 5')
    require(len(rows) == maximum - minimum + 1, 'the level range is incomplete')
    require(type(document.get('levels')) is int and document['levels'] == len(rows),
            'levels disagrees with the row count')
    passed_levels, failed_levels, first_failures = [], [], []
    total_bits = total_count = 0
    replayed = []
    for expected_v, row in zip(range(minimum, maximum + 1), rows):
        require(isinstance(row, dict) and type(row.get('v')) is int
                and row['v'] == expected_v, 'rows are missing, duplicated or out of order')
        attempts = row.get('attempts')
        require(isinstance(attempts, list) and 1 <= len(attempts) <= 2,
                f'v={expected_v}: expected one or two attempts')
        expected_budgets = [1 << (expected_v - 1)]
        if len(attempts) == 2:
            expected_budgets.append(1 << expected_v)
        independent_attempts = []
        for expected_budget, attempt in zip(expected_budgets, attempts):
            v, budget, bits = validate_attempt(attempt)
            require(v == expected_v and budget == expected_budget,
                    f'v={expected_v}: unexpected attempt level or budget')
            total_bits += bits
            total_count += attempt['odd_steps']
            if v <= max_v:
                independent_attempts.append(verify_attempt(attempt))
        require(len(attempts) == (1 if attempts[0]['certified'] else 2),
                f'v={expected_v}: the fallback budget does not follow the first decision')
        require(type(row.get('certified')) is bool
                and row['certified'] == attempts[-1]['certified'],
                f'v={expected_v}: row decision disagrees with the final attempt')
        (passed_levels if row['certified'] else failed_levels).append(expected_v)
        if not attempts[0]['certified']:
            first_failures.append(expected_v)
        if independent_attempts:
            replayed.append({'v': expected_v, 'attempts': independent_attempts})
    for name, expected in [
        ('certified_levels', passed_levels), ('inconclusive_levels', failed_levels),
        ('first_budget_failures', first_failures),
        ('total_modular_binary_steps', total_bits),
        ('total_counted_odd_steps', total_count),
    ]:
        require(document.get(name) == expected, f'{name} disagrees with the records')
    replayed_levels = [row['v'] for row in replayed]
    skipped = list(range(max(max_v + 1, minimum), maximum + 1))
    return {
        'status': 'verified' if not skipped else 'partial_replay_verified',
        'rational_bound_integer_check': True,
        'input_level_range': [minimum, maximum],
        'replayed_levels': replayed_levels,
        'not_replayed_levels': skipped,
        'replayed_attempts': sum(len(row['attempts']) for row in replayed),
        'replayed_binary_steps': sum(a['precision_bits'] for row in replayed
                                     for a in row['attempts']),
        'replayed_odd_steps': sum(a['odd_steps'] for row in replayed
                                  for a in row['attempts']),
        'rows': replayed,
        'limitations': [
            'Only replayed_levels received independent arithmetic replay.',
            'The final exponent in each attempt is only a lower bound.',
            'Block traces and comparisons to earlier full orbits are not replayed.',
            'This verifies finite certificate arithmetic, not the sufficiency theorem.',
            'No uniform all-level theorem or Lean verification is asserted.',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE / 'certificate_results.json')
    parser.add_argument('--output', type=Path, default=HERE / 'verification_results.json')
    parser.add_argument('--max-v', type=int, default=18,
                        help='highest level to replay independently (default: 18)')
    args = parser.parse_args()
    if args.max_v < 5:
        parser.error('max-v must be at least 5')
    try:
        data = args.input.read_bytes()
        document = json.loads(data)
        result = verify_document(document, args.max_v)
        result['input_sha256'] = hashlib.sha256(data).hexdigest()
    except (OSError, json.JSONDecodeError, VerificationError) as error:
        parser.exit(1, f'Certificate verification failed: {error}\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in [
        'status', 'replayed_levels', 'not_replayed_levels',
        'replayed_attempts', 'replayed_binary_steps', 'replayed_odd_steps',
    ]}), flush=True)


if __name__ == '__main__':
    main()
