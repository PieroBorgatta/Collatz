#!/usr/bin/env python3
"""Independent C/GMP replay; does not import the Python parity producer."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_row(expected, actual, trace):
    v = expected['v']
    require(type(v) is int and 10 <= v <= 24, 'Invalid level')
    quotient, remainder = divmod(589 * (1 << v), 612)
    H = quotient + bool(remainder)
    require(expected['horizon'] == actual['precision_bits'] == H, 'Precision mismatch')
    require(actual['v'] == v, 'Level mismatch')
    require(len(trace) == (H + 7) // 8, 'Trace length mismatch')
    require(not (H % 8) or trace[-1] >> (H % 8) == 0, 'Nonzero padding')
    digest = hashlib.sha256(trace).hexdigest()
    require(digest == expected['parity_trace_sha256'], 'Parity trace mismatch')
    odd = sum(byte.bit_count() for byte in trace)
    require(odd == actual['odd_steps'] == expected['odd_steps'], 'Odd count mismatch')
    for key in ('B', 'C'):
        require(expected[key] == actual[key], f'{key} extrema/witness mismatch')
    require(actual['B']['balance_end'] == 306 * H - 589 * odd, 'B total mismatch')
    require(actual['C']['balance_end'] == 305 * H - 589 * odd, 'C total mismatch')
    require(expected['budget'] == 1 << (v - 1), 'Budget mismatch')
    require(expected['budget_passed'] == (odd <= expected['budget']), 'Certificate mismatch')
    if 'candidate' in expected:
        D = 128 * v * v
        margin = D - actual['C']['maximum_drawdown']
        first = None
        if margin < 0:
            credit = D
            for r in range(H):
                bit = (trace[r // 8] >> (r % 8)) & 1
                credit = min(D, credit + (305 - 589 * bit))
                if credit < 0:
                    first = {'step': r + 1, 'credit': credit}
                    break
            require(first is not None, 'Missing first violation')
        require(expected['candidate'] == {'capacity': D, 'minimum_credit': margin,
                 'passed': margin >= 0, 'terminal_guarantee_if_passed': H - D,
                 'first_violation': first}, 'Candidate decision mismatch')
    return {'v': v, 'precision_bits': H, 'odd_steps': odd,
            'parity_trace_sha256': digest, 'profiles_and_witnesses_match': True,
            'candidate_passed': expected.get('candidate', {}).get('passed')}


def validate_document(document):
    """Reject inconsistent decisions before invoking the independent replay."""
    levels = document['levels']
    require(levels == list(range(10, 22)) or levels == [22, 23, 24], 'Unexpected level range')
    rows = document['rows']
    require([row['v'] for row in rows] == levels, 'Missing or reordered levels')
    if levels == [22, 23, 24]:
        require(document.get('stage') == 'holdout', 'Wrong stage')
        require(document.get('coefficient') == 128, 'Changed coefficient')
        protocol_hash = hashlib.sha256((HERE / 'frozen_protocol.json').read_bytes()).hexdigest()
        require(document.get('protocol_sha256') == protocol_hash, 'Wrong frozen protocol')
        require(all(isinstance(row.get('candidate'), dict) for row in rows), 'Missing candidate decisions')
        require(all(type(row['candidate'].get('passed')) is bool for row in rows), 'Invalid candidate decisions')
        passed = all(row['candidate']['passed'] for row in rows)
        failed = [row['v'] for row in rows if not row['candidate']['passed']]
        require(type(document.get('all_passed')) is bool and document['all_passed'] == passed,
                'Altered all_passed summary')
        require(document.get('failed_levels') == failed, 'Altered failed_levels summary')
    else:
        require(document.get('stage') == 'calibration', 'Wrong stage')
        require(document.get('drift') == 1, 'Changed drift')
        coefficient = 1
        while any(row['C']['maximum_drawdown'] > coefficient * row['v'] ** 2 for row in rows):
            coefficient *= 2
        require(document.get('selected_coefficient') == coefficient, 'Changed calibration coefficient')
        require(document.get('sufficient_tail_starts_at_v') == 15, 'Changed tail threshold')
    return rows


def verify_document(document, executable):
    rows = validate_document(document)
    levels = document['levels']
    evidence = []
    for row in rows:
        with tempfile.TemporaryDirectory(prefix='collatz-gmp-replay-') as tmp:
            path = Path(tmp) / 'trace.bin'
            process = subprocess.run([str(executable), '--v', str(row['v']), '--trace', str(path)],
                                     check=True, capture_output=True, text=True)
            actual = json.loads(process.stdout)
            evidence.append(validate_row(row, actual, path.read_bytes()))
    return {'status': 'verified', 'levels': levels, 'rows': evidence,
            'scope': 'Different initialization and execution algorithms; all parity bits compared by SHA-256.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE / 'holdout_results.json')
    parser.add_argument('--verifier', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=HERE / 'verification_results.json')
    args = parser.parse_args()
    result = verify_document(json.loads(args.input.read_text()), args.verifier.resolve())
    result['input_sha256'] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'levels': result['levels']}))
