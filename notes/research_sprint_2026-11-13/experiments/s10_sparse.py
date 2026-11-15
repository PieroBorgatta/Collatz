#!/usr/bin/env python3
"""Finite prefix checks only; the uniform estimate is a paper deduction."""
from fractions import Fraction
from math import prod
import json

def T(n):
    return n//2 if n%2==0 else (3*n+1)//2

def iterate(n,k):
    for _ in range(k): n=T(n)
    return n

def segment(u,target=5):
    values=[]; seen=set(); n=u
    for _ in range(2048):
        if n in seen: raise RuntimeError('unexpected cycle before known terminal')
        seen.add(n); values.append(n)
        if n==target: return values
        if n==1: return None
        n=T(n)
    raise RuntimeError('exploration cap')

def require(c,m):
    if not c: raise RuntimeError(m)

def main():
    count=trim_checks=0; max_sum=Fraction(0); max_product=Fraction(0)
    sum_seed=product_seed=None; collision=None; max_length=0
    for u in range(1,4096,2):
        xs=segment(u)
        if xs is None: continue
        count+=1; L=len(xs)-1; max_length=max(max_length,L)
        recip=sum((Fraction(1,x) for x in xs),Fraction(0))
        odds=[x for x in xs[:-1] if x%2]
        P=prod((Fraction(3*x+1,3*x) for x in odds),start=Fraction(1))
        if recip>max_sum: max_sum,sum_seed=recip,u
        if P>max_product: max_product,product_seed=P,u
        for N in range(1,17):
            prefix=xs[:max(0,len(xs)-N)]
            images=[iterate(x,N) for x in prefix]
            require(len(images)==len(set(images)),'trimmed prefix collision')
            require(len(xs)-len(prefix)<=N,'terminal exception count')
            trim_checks+=1
            if collision is None:
                first={}
                for x in xs:
                    y=iterate(x,N)
                    if y in first:
                        collision={'source':u,'target':5,'N':N,'inputs':[first[y],x],'image':y}
                        break
                    first[y]=x
        # Exact telescoping for the accelerated odd path to target 5.
        A=k=0; n=u
        while n!=5:
            m=3*n+1; a=(m&-m).bit_length()-1
            n=m//(1<<a); A+=a; k+=1
        require(P==Fraction((1<<A)*5,3**k*u),'affine product identity')
    return {'status':'PASS','finite_only':True,'source_domain':'odd u<=4095 reaching known nonreturn target 5',
            'segments':count,'trim_injectivity_checks':trim_checks,'N_range':[1,16],
            'max_shortcut_length':max_length,
            'max_reciprocal_sum':{'source':sum_seed,'fraction':str(max_sum),'float':float(max_sum)},
            'max_affine_product':{'source':product_seed,'fraction':str(max_product),'float':float(max_product)},
            'collision_without_trim':collision}

if __name__=='__main__': print(json.dumps(main(),indent=2,sort_keys=True))
