#!/usr/bin/env python3
"""Exact finite certificate: full-depth minimal prefixes need not have minimal factors."""
import json

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def step(n):
    check(n > 0 and n % 2 == 1, 'positive odd state required')
    value = 3*n+1
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return value, exponent

CASES = [
    (27,167,[1,3,5,7,9,11,13,15,17,19,21,23,25,29,35,53],445,111,False),
    (27,911,[1,3,5,7,9,11,13,15,17,19,21,23,25,29,35,53],2429,607,False),
    (31,911,[1,5,7,11,13,17,19,23,25,29,35,53],2429,607,True),
]
rows=[]
for source,target,closure,original_parent,rival_parent,unit_domain in CASES:
    closed=set(closure)
    required=[n for n in range(1,source,2) if not unit_domain or n%3]
    check(set(required) <= closed, 'a smaller source is omitted')
    edges=[]
    for n in closure:
        nxt, e=step(n)
        check(nxt in closed, 'certificate is not forward closed')
        edges.append([n,e,nxt])
    check(target not in closed, 'target is in closed certificate')
    states=[source]
    word=[]
    while states[-1] != target:
        nxt,e=step(states[-1])
        check(nxt not in states, 'cycle before registered target')
        states.append(nxt)
        word.append(e)
        check(len(word)<=32, 'registered path unexpectedly long')
    check(states[-2] == original_parent and word[-1] == 3, 'wrong final factor')
    rival_end, rival_e=step(rival_parent)
    check(rival_end == target and rival_e == 1, 'wrong one-step rival')
    check(source <= rival_parent < original_parent, 'rival does not separate source/factor minimality')
    if unit_domain:
        check(all(n%3 for n in states) and rival_parent%3, 'unit-domain certificate fails')
    # Transitivity: a smaller source reaching any endpoint would reach target.
    # The forward-closed set proves that none reaches target at any depth.
    rows.append({'source':source,'target':target,'domain':'positive odd units' if unit_domain else 'positive odds',
                 'closure_edges':edges,'states':states,'word':word,'length':len(word),
                 'all_smaller_sources_certified':required,'full_depth_prefix_minimality':True,
                 'nonminimal_factor':{'original_parent':original_parent,'exponent':3,
                                      'smaller_rival_parent':rival_parent,'rival_exponent':1},
                 'is_counterexample_to_Collatz':False})
print(json.dumps({'status':'PASS','cases':rows,'meaning':'Finite local implication fails; infinite least-counterexample bridge remains open.'},sort_keys=True,indent=2))
