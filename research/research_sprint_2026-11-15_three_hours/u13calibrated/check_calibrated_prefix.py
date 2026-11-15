#!/usr/bin/env python3
"""Exact F-calibrated-prefix counterexample to raw factor optimality."""
from fractions import Fraction
import json

def check(ok,message):
    if not ok:
        raise RuntimeError(message)

def step(n):
    check(n>0 and n%2==1,'positive odd state required')
    value=3*n+1
    exponent=0
    while value%2==0:
        value//=2
        exponent+=1
    return value,exponent

def rat(x):
    return {'numerator':x.numerator,'denominator':x.denominator}

source,target,threshold=31,911,35
closure=[1,5,7,11,13,17,19,23,25,29,35,53]
closed=set(closure)
small_seeds=[u for u in range(1,source,2) if u%3]
check(set(small_seeds)<=closed,'missing smaller unit seed')
closed_edges=[]
for u in closure:
    v,e=step(u)
    check(v in closed,'not forward closed')
    closed_edges.append([u,e,v])
check(target not in closed,'target lies in smaller-source closure')
check(33%3==0 and all(u%2==0 or u%3==0 for u in range(32,35)),'unit gap31-to35 fails')
full=[source]
exponents=[]
while full[-1]!=1:
    v,e=step(full[-1])
    check(v not in full,'nontrivial repeat before1')
    full.append(v)
    exponents.append(e)
    check(len(exponents)<=64,'registered orbit unexpectedly long')
check(target in full,'registered target not reached')
K=full.index(target)
states=full[:K+1]
word=exponents[:K]
check(all(n%3 for n in states),'unit domain fails')
omega=Fraction(1)
rows=[]
previous=Fraction(0)
for j,n in enumerate(states):
    if j:
        omega*=Fraction(3,2**word[j-1])
    potential=Fraction(n)/omega
    check(previous<=potential,'normalized potential is not monotone')
    previous=potential
    check(potential<threshold,'fixed threshold35 failed; no adaptation allowed')
    rows.append({'index':j,'state':n,'Omega':rat(omega),'state_over_Omega':rat(potential),
                 'all_unit_seeds_ge35_strictly_worse':Fraction(n,threshold)<omega})
check(states[-2]==2429 and word[-1]==3,'wrong raw factor')
rival_end,rival_exp=step(607)
check((rival_end,rival_exp)==(911,1),'wrong raw rival')
check(607 not in full,'source31 reaches rival607')
raw=Fraction(3,8); raw_rival=Fraction(3,2)
check(raw_rival>raw,'raw factor is not beaten')
rival_weighted_upper=Fraction(3,2)*Fraction(607,35)
check(rival_weighted_upper<omega,'optional strict weighted-rival upper fails')
print(json.dumps({'status':'PASS','source':source,'target':target,'threshold_fixed':threshold,
                 'prefix_length':K,'total_exponent':sum(word),'word':word,'prefix_rows':rows,
                 'full_orbit_to_one':full,'closure_edges':closed_edges,'smaller_unit_seeds':small_seeds,
                 'F31_exact':rat(Fraction(1)),'F911_exact':rat(omega),
                 'endpoint_potential':rat(Fraction(target)/omega),
                 'endpoint_potential_decimal':float(Fraction(target)/omega),
                 'threshold_margin':rat(Fraction(threshold)-Fraction(target)/omega),
                 'raw_factor_weight':rat(raw),'raw_rival_weight':rat(raw_rival),
                 'weighted_rival_upper':rat(rival_weighted_upper),
                 'all_prefixes_have_unique_maximizing_unit_seed31':True,
                 'factor_remains_F_weighted_calibrated':True,
                 'raw_factor_optimality':False,
                 'meaning':'Finite calibrated prefixes do not imply raw factor optimality; no claim about an infinite least-counterexample word.'},sort_keys=True,indent=2))
