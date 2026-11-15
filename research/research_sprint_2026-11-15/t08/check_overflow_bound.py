#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)

def T(x):
    return x//2 if x%2==0 else (3*x+1)//2

def S_with_a(x):
    z=3*x+1
    a=(z & -z).bit_length()-1
    return z>>a,a

def main():
    here=Path(__file__).resolve().parent
    p=json.loads((here/'protocol_addendum_overflow.json').read_text())
    require(5**10<2**24,'early integer certificate')
    require(5**8<2**20,'overflow integer certificate')
    require(3**8<2**15,'main lift geometric certificate')
    require(2**9<5**4,'error lift geometric certificate')
    binomial_checks=0
    for L in p['binomial_L']:
        r=L//8
        B=L+2*r
        early=sum(comb(B,k) for k in range(r+1))
        overflow=sum(comb(L,j) for j in range(r+1))
        require(early**4<=2**(3*L),f'early bound {L}')
        require(overflow**4<=2**(3*L),f'overflow bound {L}')
        binomial_checks += 2
    lift_checks=0
    for M in p['lift_caps']:
        theta=1-F(1,2**M)
        for L in p['lift_L']:
            r=L//8
            for e in range(L+1):
                re=(L-e)//8
                require(r-re <= (e+7)//8,'floor difference')
                require(theta**(8*re) <= 2**(8+e)*theta**(8*r),'lift factor bound raised to eight')
                lift_checks += 1
    clock_checks=0
    overflow_events=0
    for source in range(1,p['clock_odd_sources_max']+1,2):
        parity=[0]
        x=source
        for _ in range(max(p['clock_L'])):
            parity.append(parity[-1]+x%2)
            x=T(x)
        clocks=[0]
        x=source
        for _ in range(max(p['clock_L'])//8):
            x,a=S_with_a(x)
            clocks.append(clocks[-1]+a)
        for L in p['clock_L']:
            r=L//8
            if clocks[r]>L:
                require(parity[L]<=r,'clock overflow implication')
                overflow_events += 1
            clock_checks += 1
    print(json.dumps({'status':'PASS','scope':'Exact finite checks of binomial, clock and lift bounds; no asymptotic result inferred from data.',
                      'integer_certificates':4,'binomial_checks':binomial_checks,'lift_checks':lift_checks,
                      'clock_checks':clock_checks,'clock_overflow_events':overflow_events},sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    main()
