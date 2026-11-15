#!/usr/bin/env python3
"""Finite adversarial tree-coupling diagnostic, not a basin-density test."""
from pathlib import Path
from collections import Counter
import hashlib,json

HERE=Path(__file__).resolve().parent
CONFIG=json.loads((HERE/'protocol.json').read_text())
INTERNAL={1:(2,4),2:(1,3),4:(2,6),5:(3,5),7:(4,6),8:(1,5)}

def check(ok,msg):
    if not ok: raise RuntimeError(msg)

def step(x):
    t=3*x+1
    a=(t&-t).bit_length()-1
    return t>>a,a

def inverse(x,a):
    z=(1<<a)*x-1
    check(a>0 and z%3==0,'nonintegral inverse')
    q=z//3
    check(q>0 and q%2==1 and q%3!=0,'noninternal child')
    check(step(q)==(x,a),'forward replay failed')
    return q

def exponents(x): return INTERNAL[x%9]

def greedy_exp(z,a,d):
    desired=a-d
    lim=max(12,desired+6)
    candidates=[]
    for b in range(1,lim+1):
        v=((1<<b)*z-1)
        if v%3==0 and (v//3)%3!=0:
            candidates.append(b)
    check(bool(candidates),'greedy range incomplete')
    return min(candidates,key=lambda b:(abs(d+b-a),b))

def edges(policy,u,v,A,B):
    aa=exponents(u); bb=exponents(v); d=B-A
    if policy=='ordinal': return [(s,aa[s],bb[s]) for s in range(2)]
    if policy=='pair_minimax':
        sigma=min(range(2),key=lambda f:(max(abs(d+bb[s^f]-aa[s]) for s in range(2)),sum(abs(d+bb[s^f]-aa[s]) for s in range(2)),f))
        return [(s,aa[s],bb[s^sigma]) for s in range(2)]
    rr=[(s,a,greedy_exp(v,a,d)) for s,a in enumerate(aa)]
    if policy=='greedy_capped' and rr[0][2]==rr[1][2]:
        rr=[min(rr,key=lambda e:(abs(d+e[2]-e[1]),e[1]))]
    return rr

def reconstruct(n,y,policy,depth,code):
    u,v,A,B=n,y,0,0
    wa=[];wb=[]
    for i in range(depth-1,-1,-1):
        s=(code>>i)&1
        ee=[e for e in edges(policy,u,v,A,B) if e[0]==s]
        check(len(ee)==1,'witness discarded')
        _,a,b=ee[0]
        u=inverse(u,a);v=inverse(v,b);A+=a;B+=b
        wa.append(a);wb.append(b)
    return {'source':u,'image':v,'A':A,'B':B,'source_inverse_exponents':wa,'image_inverse_exponents':wb,'source_forward_exponents':wa[::-1],'image_forward_exponents':wb[::-1],'rank_bits':format(code,f'0{depth}b') if depth else ''}

def summarize(nodes,depth,n,y,policy):
    counts=Counter(v for u,v,A,B,c in nodes)
    hist=Counter(B-A for u,v,A,B,c in nodes)
    maxr=max(nodes,key=lambda t:t[1]/t[0])
    minr=min(nodes,key=lambda t:t[1]/t[0])
    # Float only locates initial candidates; exact comparison certifies maxima/minima.
    for t in nodes:
        if t[1]*maxr[0]>maxr[1]*t[0]: maxr=t
        if t[1]*minr[0]<minr[1]*t[0]: minr=t
    maxd=max(nodes,key=lambda t:(t[3]-t[2],t[1],t[4]))
    h=hashlib.sha256()
    for row in nodes:h.update((','.join(map(str,row))+'\n').encode())
    return {'depth':depth,'codes':len(nodes),'distinct_images':len(counts),'max_image_load':max(counts.values(),default=0),'debt_min':min(hist,default=None),'debt_max':max(hist,default=None),'debt_histogram':dict(sorted(hist.items())),'height_counts':{str(D):sum(v<=D*u for u,v,A,B,c in nodes) for D in CONFIG['height_thresholds']},'max_ratio':{'num':maxr[1],'den':maxr[0],'approx':maxr[1]/maxr[0],'witness':reconstruct(n,y,policy,depth,maxr[4])},'min_ratio':{'num':minr[1],'den':minr[0],'approx':minr[1]/minr[0]},'max_debt_witness':reconstruct(n,y,policy,depth,maxd[4]),'physical_rows_sha256':h.hexdigest()}

def main():
    result={'scope':'fixed binary inverse-code subtree, not natural density','protocol_sha256':hashlib.sha256((HERE/'protocol.json').read_bytes()).hexdigest(),'runs':[],'root_checks':[]}
    for n in CONFIG['targets']:
        y=int(CONFIG['canonical_siblings'][str(n)])
        for root in (n,y):
            x=root;seen=set()
            for k in range(1000):
                if x==1:break
                check(x not in seen,'unexpected root cycle')
                seen.add(x);x=step(x)[0]
            check(x==1,'root termination check incomplete')
            result['root_checks'].append({'root':root,'first_hit_1_steps':k,'positive_self_return':False})
        ordinal=None
        for policy in CONFIG['policies']:
            nodes=[(n,y,0,0,0)]
            run={'target':n,'sibling':y,'policy':policy,'levels':[summarize(nodes,0,n,y,policy)]}
            for depth in range(1,CONFIG['max_depth']+1):
                nxt=[]
                for u,v,A,B,code in nodes:
                    for s,a,b in edges(policy,u,v,A,B):
                        nxt.append((inverse(u,a),inverse(v,b),A+a,B+b,2*code+s))
                nodes=nxt
                row=summarize(nodes,depth,n,y,policy)
                if policy in ('ordinal','pair_minimax','greedy_capped'):
                    check(row['distinct_images']==len(nodes),'claimed injective policy collided')
                run['levels'].append(row)
            if policy=='ordinal':ordinal=run['levels']
            if policy=='pair_minimax':
                check([r['physical_rows_sha256'] for r in ordinal]==[r['physical_rows_sha256'] for r in run['levels']],'minimax differs from ordinal')
            result['runs'].append(run)
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
