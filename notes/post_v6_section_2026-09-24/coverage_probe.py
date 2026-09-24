#!/usr/bin/env python3
"""Exact certificate for hitting 1 or residue 20 mod27 under shortcut Collatz.

Mathematical certificate: the 54 residue/parity edges, together with exact
coefficient inequalities for the rank stated in RESULTS_IT.md. Finite
trajectory checks are supplementary and are not the proof of coverage.
"""
import json
from pathlib import Path


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def T(n):
    return n//2 if n%2 == 0 else (3*n+1)//2


def weight(r):
    if r in [8,17]: return 1
    if r in [2,4,5,11,14,22,23]: return 2
    return 4


def coeff(r): return 3*weight(r)+1


def synthesize_core_potential():
    """Solve difference constraints on the specified regular residue graph.

    The stopping residue and exceptional classes are supplied by the
    mathematical design, not discovered by this finite solver. The
    unbounded valuation counter is proved separately in Lean.
    """
    core = set(range(27)) - {13, 20, 26}
    levels = {r: 0 for r in core}
    edges = []
    for z in range(54):
        source, destination = z % 27, T(z) % 27
        if source in core and destination in core:
            edges.append((source, destination, -1 if z % 2 else 1))
    # Bellman-Ford with a virtual source of zero-cost edges to every vertex.
    for iteration in range(len(core)):
        changed = False
        for source, destination, cost in edges:
            bound = levels[source] + cost
            if levels[destination] > bound:
                levels[destination] = bound
                changed = True
        if not changed:
            break
    else:
        raise ValueError('The regular graph has a negative constraint cycle')
    minimum = min(levels.values())
    levels = {r: level - minimum for r, level in levels.items()}
    assert all(levels[s] <= levels[r] + c for r, s, c in edges)
    assert all(2 ** levels[r] == weight(r) for r in core)
    return {'method': 'integer difference constraints (Bellman-Ford)',
            'specified_excluded_residues': [13, 20, 26],
            'regular_edges': len(edges), 'relaxation_passes': iteration + 1,
            'levels': levels,
            'derived_coefficients': {r: 3 * 2 ** levels[r] + 1 for r in core}}


def terminal(n): return n == 1 or n%27 == 20


def rank(n):
    assert n > 0
    if terminal(n): return 0
    r=n%27
    if r == 13: return 1
    if r == 26: return v2(n+1)+2
    return coeff(r)*n+3


def build_certificate():
    rows=[]
    for z in range(54):
        r=z%27
        s=T(z)%27
        parity=z%2
        row={'residue_mod54': z, 'source_mod27':r, 'destination_mod27':s,
             'parity': 'odd' if parity else 'even'}
        if r==20:
            row['case']='terminal_source'
        elif r==13:
            assert s==20
            row['case']='13_to_20'
        elif r==26:
            assert s==(26 if parity else 13)
            row['case']='26_precision_tax' if parity else '26_to_13'
        elif s==20:
            row['case']='core_to_terminal'
        elif s==13:
            row['case']='core_to_13'
        elif s==26:
            row['case']='core_to_26'
        else:
            p,q=coeff(r),coeff(s)
            row.update({'source_coefficient':p,'destination_coefficient':q})
            if parity:
                # If n>=3, (2p-3q)n-q >= 3(2p-3q)-q > 0.
                assert 2*p-3*q>0
                assert 3*(2*p-3*q)-q>0
                row.update({'case':'core_odd','linear_slope':2*p-3*q,
                            'margin_at_n3':3*(2*p-3*q)-q})
            else:
                # R(n)-R(Tn)=(2p-q)n/2 >0 for positive even n.
                assert 2*p-q>0
                row.update({'case':'core_even','linear_slope':2*p-q})
        rows.append(row)
    return rows


def main():
    synthesis = synthesize_core_potential()
    rows=build_certificate()
    from collections import Counter
    # Finite supplement tests every initial source individually (no induction assumed).
    samples=1000000
    for n in range(1,samples+1):
        if not terminal(n):
            assert T(n)>0
            assert rank(T(n))<rank(n),(n,T(n),rank(n),rank(T(n)))
    # Test long red26 runs, well beyond the million-prefix sample.
    # 2^s u-1=26 mod27 iff 2^s u=0 mod27, so u=27 always works.
    tower_checks=[]
    for s in [1,2,10,100,1000,10000]:
        n=(1<<s)*27-1
        assert n%27==26 and v2(n+1)==s
        assert rank(T(n))==rank(n)-1
        tower_checks.append(s)
    out={'description':'Exact finite edge certificate for universal hitting of 1 or 20mod27',
         'finite_core_synthesis': synthesis,
         'weights':{str(r):weight(r) for r in range(27) if r not in [13,20,26]},
         'coefficients':{str(r):coeff(r) for r in range(27) if r not in [13,20,26]},
         'case_counts':dict(Counter(row['case'] for row in rows)),
         'exact_edges':rows,
         'supplementary_one_step_rank_checks':samples,
         'supplementary_residue26_precision_exponents':tower_checks,
         'all_checks_passed':True}
    Path(__file__).with_name('coverage_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='exact_edges'},indent=2))


if __name__=='__main__':main()
