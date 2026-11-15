#!/usr/bin/env python3
"""Finite arithmetic checks. Proofs and asymptotics are in the T08 note.

Guards remain active with -O. This does not execute downloaded source code.
"""
from bisect import bisect_right
from fractions import Fraction as F
from itertools import product
from math import log
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def step(x):
    require(x > 0 and x % 2 == 1, 'positive odd step domain')
    z = 3*x+1
    a = (z & -z).bit_length()-1
    return z >> a, a


def constant(word):
    total=0
    prefix=1
    k=len(word)
    for i,a in enumerate(word):
        total += 3**(k-1-i)*prefix
        prefix <<= a
    return total


def main():
    here=Path(__file__).resolve().parent
    protocol=json.loads((here/'protocol.json').read_text())
    cylinder_rows=[]
    replay_count=0
    disjoint_count=0
    for cap in protocol['cylinders']['caps']:
        theta=1-F(1,2**cap)
        for length in protocol['cylinders']['lengths']:
            cells=[]
            mass=F(0)
            for word in product(range(1,cap+1), repeat=length):
                total=sum(word)
                modulus=2**(total+1)
                residue=((2**total-constant(word))*pow(3**length,-1,modulus))%modulus
                require(residue%2 == 1,'word cylinder must be odd')
                mass += F(1,modulus)
                for lift in protocol['cylinders']['lifts']:
                    x=residue+lift*modulus
                    got=[]
                    for _ in word:
                        x,a=step(x)
                        got.append(a)
                    require(tuple(got)==word, f'exact replay failed {cap,length,word,lift}')
                    replay_count += 1
                cells.append((modulus,residue))
            require(mass==theta**length/2,'exact cylinder mass')
            cells.sort()
            for i,(q,r) in enumerate(cells):
                for q2,r2 in cells[i+1:]:
                    require(r2%q != r,'cylinder intersection')
                    disjoint_count += 1
            cylinder_rows.append({'cap':cap,'length':length,'words':len(cells),'odd_absolute_density':str(mass)})

    targets=protocol['counting']['targets']
    caps=protocol['counting']['caps']
    max_source=protocol['counting']['odd_sources_max']
    max_new=protocol['counting']['max_new_orbit_steps']
    qualified={(cap,n):[] for cap in caps for n in targets}
    max_steps=0
    max_state=0
    for source in range(1,max_source+1,2):
        x=source
        seen=set()
        hits={}
        running_max=0
        steps=0
        while x not in seen:
            require(steps < max_new,'incomplete finite orbit')
            if x in targets and x not in hits:
                hits[x]=running_max
            seen.add(x)
            max_state=max(max_state,x)
            x,a=step(x)
            running_max=max(running_max,a)
            steps += 1
        max_steps=max(max_steps,steps)
        for cap in caps:
            for n in targets:
                if n in hits and hits[n] <= cap:
                    qualified[cap,n].append(source)

    rows=[]
    exact_checks=0
    float_checks=0
    ordinary_checks=0
    for cap in caps:
        theta=1-F(1,2**cap)
        alpha=log(cap)/log(cap/float(theta)) if cap >= 2 else None
        for target in targets:
            good=qualified[cap,target]
            goodset=set(good)
            for cutoff in protocol['counting']['cutoffs']:
                count=bisect_right(good,cutoff)
                for r in protocol['counting']['r_values']:
                    early=sum(cap**k for k in range(r))
                    bound=early+F(cutoff,2)*theta**r+cap**r
                    require(count <= bound,f'finite count failed {cap,target,cutoff,r,count,bound}')
                    exact_checks += 1
                ordinary=0
                for u in range(1,cutoff+1):
                    odd=u >> ((u & -u).bit_length()-1)
                    ordinary += odd in goodset
                if alpha is not None:
                    require(count <= 3*cutoff**alpha+1e-9,'optimized odd diagnostic')
                    require(ordinary <= 9*cutoff**alpha+1e-9,'ordinary diagnostic')
                    float_checks += 1
                    ordinary_checks += 1
                rows.append({'cap':cap,'target':target,'cutoff':cutoff,'odd_count':count,'ordinary_count':ordinary})

    result={'status':'PASS','scope':'Exact finite cylinder and count checks; optimized power bounds are floating diagnostics only.',
            'cylinder_rows':cylinder_rows,'cylinder_replays':replay_count,'disjoint_pairs_checked':disjoint_count,
            'odd_sources_checked':(max_source+1)//2,'max_distinct_steps_observed':max_steps,'max_odd_state_observed':max_state,
            'finite_fraction_inequalities_checked':exact_checks,'optimized_float_diagnostics':float_checks,
            'ordinary_float_diagnostics':ordinary_checks,'count_rows':rows}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    main()
