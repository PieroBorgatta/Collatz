#!/usr/bin/env python3
"""Calibration and frozen holdout for a bounded-loss compensation hypothesis."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

from block_engine import analyze_level, horizon

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / 'post_v6_certificates_2026-09-24/certificate_results.json'
FIELDS = ('balance_end', 'minimum_balance', 'minimum_at_step', 'maximum_balance',
          'maximum_at_step', 'maximum_drawdown', 'drawdown_from_step', 'drawdown_to_step')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def first_violation(trace, bits, capacity):
    """Direct credit recurrence; called only when the summary predicts failure."""
    credit = capacity
    for r in range(bits):
        odd = (trace[r // 8] >> (r % 8)) & 1
        credit = min(capacity, credit + (305 - 589 * odd))
        if credit < 0:
            return {'step': r + 1, 'credit': credit}
    return None


def compact_level(v, coefficient=None):
    with tempfile.TemporaryDirectory(prefix='collatz-compensation-') as tmp:
        trace_path = Path(tmp) / 'parities.bin'
        result = analyze_level(v, block_size=256, trace_path=trace_path)
        C = result['drifted_balance']
        row = {key: result[key] for key in ('v', 'horizon', 'budget', 'odd_steps',
               'budget_passed', 'initial_residue_sha256', 'parity_trace_sha256')}
        row['B'] = {key: result[key] for key in FIELDS}
        row['C'] = {key: C[key] for key in FIELDS}
        row['diagnostic_blocks'] = {
            'width': 256, 'count': len(C['blocks']),
            'last_length': C['blocks'][-1]['length'],
            'negative_C_blocks': sum(b['balance_delta'] < 0 for b in C['blocks']),
            'negative_B_blocks': sum(b['balance_delta'] < 0 for b in result['blocks']),
            'scope': 'Diagnostic grouping; the hypothesis checks every binary prefix.'}
        if coefficient is not None:
            D = coefficient * v * v
            margin = D - C['maximum_drawdown']
            row['candidate'] = {'capacity': D, 'minimum_credit': margin,
                                'passed': margin >= 0,
                                'terminal_guarantee_if_passed': result['horizon'] - D,
                                'first_violation': None}
            if margin < 0:
                row['candidate']['first_violation'] = first_violation(
                    trace_path.read_bytes(), result['horizon'], D)
                assert row['candidate']['first_violation'] is not None
            if margin >= 0:
                assert result['balance_end'] >= result['horizon'] - D
                if result['horizon'] >= D:
                    assert result['budget_passed']
        return row


def calibrate():
    old = {r['v']: r['attempts'][0] for r in json.loads(BASELINE.read_text())['rows']}
    rows = []
    for v in range(10, 22):
        row = compact_level(v)
        assert row['odd_steps'] == old[v]['odd_steps']
        assert row['initial_residue_sha256'] == old[v]['initial_residue_sha256']
        rows.append(row)
    coefficient = 1
    while any(r['C']['maximum_drawdown'] > coefficient * r['v'] ** 2 for r in rows):
        coefficient *= 2
    v0 = 10
    while horizon(v0) < coefficient * v0 * v0:
        v0 += 1
    return {'stage': 'calibration', 'levels': list(range(10, 22)),
            'baseline_sha256': sha(BASELINE), 'drift': 1,
            'selection_rule': 'Smallest positive power of two bounding drawdown/v^2 on v=10..21.',
            'selected_coefficient': coefficient, 'sufficient_tail_starts_at_v': v0,
            'rows': rows, 'scope': 'Exploratory fit to existing levels, not a uniform theorem.'}


def holdout(protocol):
    spec = json.loads(protocol.read_text())
    assert spec['holdout_levels'] == [22, 23, 24]
    assert spec['drift'] == 1 and spec['coefficient'] == 128
    assert spec['sufficient_tail_starts_at_v'] == 15
    for name, digest in spec['frozen_inputs_sha256'].items():
        if sha(HERE / name) != digest:
            raise ValueError(f'Frozen input changed: {name}')
    rows = []
    for v in spec['holdout_levels']:
        row = compact_level(v, spec['coefficient'])
        rows.append(row)
        print(json.dumps({'v': v, 'odd_steps': row['odd_steps'],
                          'maximum_drawdown': row['C']['maximum_drawdown'],
                          'candidate': row['candidate']}), flush=True)
    return {'stage': 'holdout', 'protocol_sha256': sha(protocol),
            'levels': spec['holdout_levels'], 'coefficient': spec['coefficient'],
            'all_passed': all(r['candidate']['passed'] for r in rows),
            'failed_levels': [r['v'] for r in rows if not r['candidate']['passed']],
            'rows': rows, 'scope': 'New finite tests of the frozen hypothesis; not a uniform proof.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=('calibration', 'holdout'))
    parser.add_argument('--protocol', type=Path, default=HERE / 'frozen_protocol.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = calibrate() if args.stage == 'calibration' else holdout(args.protocol)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}, indent=2))
