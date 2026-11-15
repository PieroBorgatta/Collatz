#!/usr/bin/env python3
"""Independent finite first-crossing audit of Paper146 §5.

No exponent cap is used: at a first crossing the total is in a width<1
logarithmic interval, so every relevant word is enumerated exactly.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


@lru_cache(None)
def compositions(total, length):
    if length == 0:
        return ((),) if total == 0 else ()
    if total < length:
        return ()
    return tuple((a,)+tail for a in range(1, total-length+2)
                 for tail in compositions(total-a, length-1))


def stats(word):
    A=F(1);B=F(0);multipliers=[]
    for e in word:
        A *= F(3, 2**e)
        B += A/3
        multipliers.append(A)
    return A,B,B/A,multipliers


@lru_cache(None)
def stopped(threshold, length):
    values=[]
    # Since threshold>=1 and 3^n/2^d>threshold, d<2n.
    for total in range(length,2*length+1):
        final=F(3**length,2**total)
        if not threshold<final<=F(3,2)*threshold:
            continue
        for word in compositions(total,length):
            a,b,v,seq=stats(word)
            if all(t<=threshold for t in seq[:-1]):
                values.append((word,a,b,v))
    return tuple(values)


def mass(words):
    return sum((F(3**len(w),4**sum(w)) for w,*_ in words), F(0))


def residue(x,q):
    return x.numerator*pow(x.denominator,-1,q)%q


def main():
    checks=prefix_checks=spacing_checks=actual=0
    maximum_ratio=F(0);maximum_fixture=None
    thresholds=[F(1),F(3,2),F(2),F(3),F(4)]
    for threshold in thresholds:
        words={n:stopped(threshold,n) for n in range(1,9)}
        for n in range(1,8):
            if not words[n]:
                continue
            dn=sum(words[n][0][0]);a_n=words[n][0][1]
            need(all(sum(w)==dn and a==a_n for w,a,b,v in words[n]), 'unique stopped total')
            support={residue(b,3**n) for w,a,b,v in words[n]}
            pn=mass(words[n]);r=threshold/a_n
            need(F(2,3)<=r<1, 'threshold ratio')
            for m in range(n+1,9):
                k=m-n
                for K in (1,2,4):
                    good=[z for z in words[m] if z[3]<=K and residue(z[2],3**n) in support]
                    lhs=mass(good)
                    rhs_sum=F(0);Delta=1
                    while r*2**Delta<F(3,2)**k:
                        rhs_sum += F(1,2**Delta)*mass(stopped(r*2**Delta,k))
                        Delta+=1
                    rhs=2*K*pn*rhs_sum
                    need(lhs<=rhs, ('equation14',str(threshold),n,m,K,str(lhs),str(rhs)))
                    checks+=1;actual+=bool(lhs)
                    if rhs and lhs/rhs>maximum_ratio:
                        maximum_ratio=lhs/rhs;maximum_fixture=[str(threshold),n,m,K]
                    for w,av,bv,Vv in good:
                        u=w[:n];au,bu,Vu,seq=stats(u);Delta=sum(u)-dn
                        need(Delta>=1 and au==a_n/F(2**Delta), 'surviving total loss')
                        need(Vu<=F(3,2)*2**Delta*K, 'equation13')
                        need(F(3**n,4**sum(u))==F(3**n,4**dn)*F(1,4**Delta), 'probability cost')
                        prefix_checks+=1
                    # Complete fixed-total prefix census at every Delta actually used.
                    for Delta in sorted({sum(w[:n])-dn for w,av,bv,Vv in good}):
                        counts={z:0 for z in support}
                        for u in compositions(dn+Delta,n):
                            au,bu,Vu,seq=stats(u)
                            if all(a<=threshold for a in seq) and Vu<=F(3,2)*2**Delta*K:
                                z=residue(bu,3**n)
                                if z in counts:counts[z]+=1
                        need(all(c<=2*2**Delta*K for c in counts.values()), 'spacing count')
                        spacing_checks+=len(counts)
    return {'status':'PASS','finite_only':True,'maximum_stopped_length':8,
            'inequalities_checked':checks,'nonzero_left_sides':actual,
            'physical_prefix_checks':prefix_checks,'complete_spacing_fiber_checks':spacing_checks,
            'maximum_lhs_rhs_ratio':str(maximum_ratio),'maximum_ratio_fixture':maximum_fixture,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
