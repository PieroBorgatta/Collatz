#!/usr/bin/env python3
"""Exact finite checks of the deliberately non-Syracuse countermodel."""
from fractions import Fraction as F
from pathlib import Path
import json


def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)


def law(m):
    q=3**m
    mu=[F(3,4*q) if r%3 else F(0) for r in range(q)]
    for j in range(1,m):
        n=2*3**j-1
        if 2*j <= m:
            period=3**(2*j)
            for r in range(n%period,q,period):
                mu[r] += F(3**j,q)
        else:
            mu[n%q] += F(1,3**j)
    mu[-1] += F(3,2*q)
    require(sum(mu)==1,'mass')
    require(all(x>=0 for x in mu),'nonnegative')
    require(all(mu[r]==0 for r in range(0,q,3)),'unit support')
    return mu


def value_integer(n):
    require(n>0,'positive integer')
    if n%3==0:
        return F(0)
    v=F(3,4)
    for j in range(1,n.bit_length()+1):
        if (n-(2*3**j-1))%(3**(2*j))==0:
            v+=3**j
    return v


def main():
    protocol=json.loads((Path(__file__).resolve().parent/'protocol.json').read_text())
    depths=protocol['abstract_model']['depths']
    laws={m:law(m) for m in depths}
    projective=0
    refinements=[]
    for m in depths:
        if m+1 in laws:
            q=3**m
            coarse=[sum(laws[m+1][r+t*q] for t in range(3)) for r in range(q)]
            require(coarse==laws[m],'projective consistency')
            projective += q
        for n in depths:
            if n < m:
                continue
            qm=3**m
            lift=3**(n-m)
            error=sum(abs(p-laws[m][r%qm]/lift) for r,p in enumerate(laws[n]))
            bound=F(1,3**(m//2))
            require(error <= bound,'L1 refinement bound')
            refinements.append({'coarse_depth':m,'fine_depth':n,'L1_error':str(error),'bound':str(bound)})
    spikes=[]
    for j in range(1,9):
        n=2*3**j-1
        y=16*n+5
        fn=value_integer(n)
        fy=value_integer(y)
        require(fn==F(3,4)+3**j,'spike value')
        require(fy==F(3,4),'sibling background')
        spikes.append({'j':j,'n':n,'sibling':y,'F_n':str(fn),'F_sibling':str(fy),'ratio':str(fy/fn)})
    q= laws[1][1]*F(1,2)
    require(q==F(1,8),'artificial joint atom')
    actual_atom=F(0)
    require(pow(2,-1,3)==2,'actual affine endpoint at total1')
    f2=value_integer(2)
    stationary_rhs=F(1,2)*value_integer(4)+F(3,2)*value_integer(1)
    require(f2==F(3,4) and stationary_rhs==F(3,2),'stationary residual')
    require(f2 != stationary_rhs,'countermodel must not accidentally be stationary')
    out={'status':'PASS','scope':'Abstract normalized cylinder law; explicitly fails Syracuse stationarity and exact word-atom dictionary.',
         'depths':depths,'projective_residue_checks':projective,'refinement_checks':refinements,'spikes':spikes,
         'joint_Q_1_residue1_total1':str(q),'actual_affine_atom_residue1_total1':str(actual_atom),
         'word_count_integrality_failure':str(2*q),'F_2':str(f2),'stationary_rhs_at_2':str(stationary_rhs)}
    print(json.dumps(out,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    main()
