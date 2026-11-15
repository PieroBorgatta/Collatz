#!/usr/bin/env python3
"""Exact countermodel checks: regularity alone does not control integer traces.

The function is NOT the stationary Syracuse density. Independent cylinder
intersection calculations check the closed formulas used in the proof.
"""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json

HERE=Path(__file__).resolve().parent
C=Q(3,4)

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def val3(n):
    n=abs(n)
    if n==0: return None
    out=0
    while n%3==0: n//=3;out+=1
    return out

def center(j): return 2*3**j-1

def trace(x):
    if x%3==0: return Q(0)
    if x==-1: return C
    d=val3(x+1)
    if d and (x-center(d))%(3**(2*d))==0: return C+3**d
    return C

def rho_by_intersections(x,m):
    # All j>m have the same image cylinder at depth m. Sum their masses.
    value=C if x%3 else Q(0)
    for j in range(1,m+1):
        depth=min(m,2*j)
        if (x-center(j))%(3**depth)==0:
            value+=Q(3**j,3**max(0,2*j-m))
    if (x+1)%(3**m)==0:
        value+=Q(1,2) # 3^m * sum_{j>m} 3^{-j}
    return value

def rho_closed(x,m):
    if x%3==0: return Q(0)
    if (x+1)%(3**m)==0: return C+Q(3,2)
    d=val3(x+1)
    if not d: return C
    if (x-center(d))%(3**min(m,2*d))!=0: return C
    return C+Q(3**d,3**max(0,2*d-m))

def energy_closed(m):
    middle=sum((Q(3**m,3**(2*j)) for j in range(m//2+1,m)),Q(0))
    return Q(9,8)+m//2+middle+Q(9,4*3**m)

def l1_closed(m):
    middle=sum((Q(2,3**j)*(1-Q(3**m,3**(2*j))) for j in range(m//2+1,m)),Q(0))
    return middle+Q(3,3**m)-Q(27,8*3**(2*m))

def main():
    plan=json.loads((HERE/'protocol.json').read_text())
    rows=[];pairs=0;density_checks=0;witnesses=0
    js=plan['centers_j'];ms=plan['cylinder_depths_m']
    for j in js:
        for l in js:
            if j>=l: continue
            require(val3(center(l)-center(j))==j,'disjointness valuation')
            require(j<min(2*j,2*l),'disjointness conductor')
            pairs+=1
        partial=C*Q(2,3)+sum((Q(1,3**i) for i in range(1,j+1)),Q(0))
        require(partial==1-Q(1,2*3**j),'partial mass')
        require(trace(center(j))==C+3**j,'trace spike')
        for m in ms:
            if m<2*j:
                q=4*3**m-1 if m<=j else center(j)+2*3**m
                require((q-center(j))%(3**m)==0,'background witness residue')
                require(trace(q)==C,'background witness trace')
                witnesses+=1
    xs=plan['integer_checks']+[center(j) for j in js]+[-1,-11]
    for m in ms:
        for x in xs:
            require(rho_by_intersections(x,m)==rho_closed(x,m),'conditional density formula')
            density_checks+=1
        en=energy_closed(m);l1=l1_closed(m)
        require(en<=Q(m,2)+Q(9,4),'linear energy bound')
        require(en<=32*m*m,'quadratic source envelope')
        require(0<=l1<=Q(1,3**(m//2)),'exponential L1 bound')
        rows.append({'m':m,'energy':str(en),'l1_error':str(l1),
                     'l1_bound':str(Q(1,3**(m//2)))})
    residue_counts=0
    for m in range(1,8):
        vals=[rho_by_intersections(x,m) for x in range(3**m)]
        require(sum(vals,Q(0))/3**m==1,'conditional mass one')
        require(sum((v*v for v in vals),Q(0))/3**m==energy_closed(m),'independent energy')
        residue_counts+=len(vals)
    left=trace(2);right=Q(1,2)*trace(4)+Q(3,2)*trace(1)
    require(left==Q(3,4) and right==Q(3,2) and left!=right,'stationary defect')
    require((C+3)/center(1)>Q(1,2),'finite spike ratio')
    result={'status':'PASS','model_is_syracuse_stationary':False,
            'pairwise_disjointness_checks':pairs,'conditional_density_checks':density_checks,
            'inf_envelope_background_witnesses':witnesses,
            'full_residue_checks':residue_counts,'full_residue_levels':7,
            'stationary_defect_at_2':{'F(2)':str(left),'LF(2)':str(right)},
            'energy_and_l1_rows':rows}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__': main()
