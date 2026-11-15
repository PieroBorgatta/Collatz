#!/usr/bin/env python3
"""Independent finite arithmetic replay; does not certify an infinite bound."""
import json, math, hashlib
from fractions import Fraction as F
from pathlib import Path

def need(p, why):
    if not p: raise RuntimeError(why)

def T(n): return n//2 if n%2==0 else (3*n+1)//2

def iterate_count(n,k):
    m=0
    for _ in range(k): m+=n%2; n=T(n)
    return n,m

def first_arrival(n,target=5):
    xs=[];seen=set()
    while n not in seen and len(xs)<4096:
        xs.append(n);seen.add(n)
        if n==target:return xs
        if n==1:return None
        n=T(n)
    raise RuntimeError('repeat or cap')

def main():
    total=pair=0
    for j in range(17):
        mod=1<<j; counts=[0]*(j+1);moment=0
        for s in range(mod):
            end,m=iterate_count(s,j)
            need(end<2*3**m,'affine endpoint range')
            end_lift,m_lift=iterate_count(s+mod,j)
            need(m_lift==m and end_lift==end+3**m,'lift')
            need((end%2)+(end_lift%2)==1,'last bit complement')
            counts[m]+=1; moment+=(2**(j-m))*(3**m)
            total+=1;pair+=1
        need(counts==[math.comb(j,m) for m in range(j+1)],'parity binomial distribution')
        need(moment==5**j,'weighted moment')
    segs=checks=0;max_recip=F(0);max_seed=None
    for seed in range(1,8192,2):
        xs=first_arrival(seed)
        if xs is None:continue
        segs+=1
        rec=sum((F(1,n) for n in xs),F(0))
        if rec>max_recip:max_recip,max_seed=rec,seed
        maxj=max(xs).bit_length()-1
        for j in range(1,maxj+1):
            mod=1<<j;A=[n for n in xs[:-j] if mod<=n<2*mod]
            images=[iterate_count(n,j)[0] for n in A]
            need(len(images)==len(set(images)),'trimmed iterate injection')
            vals=[iterate_count(n-mod,j)[1] for n in A]
            for m in set(vals):need(vals.count(m)<=2*3**m,'cell packing')
            M=(3*j)//5
            light=sum(m<M for m in vals);heavy=len(vals)-light
            need(light<3**M,'light packing')
            need(F(heavy)*F(3,2)**M<=F(5,2)**j,'heavy moment bound')
            normalized=F(len(A),mod)
            bound=F(5,4)**j*F(2,3)**M+F(3**M,mod)
            need(normalized<=bound,'dyadic bound')
            full=sum(mod<=n<2*mod for n in xs)
            need(full<=len(A)+j,'finite terminal count')
            checks+=1
    h=F(3125,3456);ell=F(27,32)
    hs=[F(5,4)**s*F(2,3)**((3*s)//5) for s in range(5)]
    ls=[F(3**((3*s)//5),2**s) for s in range(5)]
    B=1+sum(hs)/(1-h)+sum(ls)/(1-ell)
    need(B==F(133547,1655) and B<81,'rational geometric bound')
    need(B-1==F(131892,1655) and B-1<80,'optional exact light improvement')
    return {'status':'PASS','finite_only':True,'moment_depth_range':[0,16],
      'moment_representatives':total,'complemented_pairs':pair,
      'first_arrival_target':5,'odd_seed_upper_exclusive':8192,'segments':segs,
      'band_checks':checks,'max_finite_reciprocal_sum':str(max_recip),
      'max_finite_reciprocal_sum_float':float(max_recip),'max_seed':max_seed,
      'paper_geometric_rational_bound':str(B),
      'paper_optional_exact_light_bound':str(B-1),
      'paper_constant_is_not_certified_by_finite_replay':True}

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
