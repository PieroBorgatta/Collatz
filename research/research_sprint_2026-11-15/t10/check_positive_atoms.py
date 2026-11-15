#!/usr/bin/env python3
"""Exact finite check of integer positivity and the critical tilted law.

The finite replay is not the proof of its uniform all-depth bound.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json,hashlib


def need(ok,message):
    if not ok:raise RuntimeError(message)


@lru_cache(None)
def words(total,length):
    if length==0:return ((),) if total==0 else ()
    if total<length:return ()
    return tuple((a,)+rest for a in range(1,total-length+2) for rest in words(total-a,length-1))


def AB(word):
    a=F(1);b=F(0)
    for e in word:
        a*=F(3,2**e);b+=a/3
    return a,b


def critical_step(previous):
    q=3*len(previous);L=2*(q//3);cycle=[pow(2,i,q) for i in range(L)]
    force=[F(9,4)*previous[((2*x-1)//3)%len(previous)] if x%3==2 else F(0) for x in cycle]
    boundary=sum((b*4**(L-i) for i,b in enumerate(force)),F(0))/(4**L-1)
    out=[F(0)]*q;v=boundary
    for x,b in zip(cycle,force):out[x]=v;v=4*(v-b)
    need(v==boundary and sum(out,F(0))==q,'critical tilted probability law')
    return out


def main():
    levels=[[F(1)]]
    for _ in range(6):levels.append(critical_step(levels[-1]))
    atom_checks=prefix_checks=source_checks=truncated_checks=0
    for k,law in enumerate(levels):
        for n in range(1,130,2):
            need(law[n%len(law)]<=2*n*n,('critical atom bound',k,n))
            atom_checks+=1
    for k in range(1,6):
        for n in range(1,130,2):
            partial=F(0)
            for D in range(k,13):
                sources=[];a=F(3**k,2**D)
                for w in words(D,k):
                    A,B=AB(w);source=(n-B)/A
                    if source.denominator!=1:continue
                    need(source>0 and source.numerator%2==1,'positive odd inverse')
                    need(A<=n and source<=n/A,'terminal multiplier barrier')
                    sources.append(int(source));partial+=A*A
                    for i in range(1,k+1):
                        ai,bi=AB(w[:i]);yi=(n-bi)/ai
                        need(yi.denominator==1 and yi>0 and ai<=n,'all prefix barrier')
                        prefix_checks+=1
                need(len(sources)==len(set(sources)),'same-total source injectivity')
                need(F(len(sources))<=n/a,'fiber source count')
                source_checks+=1
            need(partial<=levels[k][n%len(levels[k])],'truncated tilt sum')
            truncated_checks+=1
    return {'status':'PASS','finite_only':True,'atom_checks':atom_checks,
            'all_positive_prefix_checks':prefix_checks,'fixed_total_source_fibers':source_checks,
            'truncated_tilt_comparisons':truncated_checks,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
