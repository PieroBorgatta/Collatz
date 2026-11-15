#!/usr/bin/env python3
"""Independent backward branch replay; no asymptotic claim."""
from pathlib import Path
from collections import Counter
import hashlib,json

BASE=Path(__file__).resolve().parent
SPEC=json.loads((BASE/'protocol.json').read_text())

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def inverse(words,target):
    current=target
    for exponent in reversed(words):
        numerator=(current << exponent)-1
        if numerator%3: return None
        current=numerator//3
        if current<=0 or current%2==0: return None
    return current

def constant(words):
    c=0; total=0
    for exponent in words:
        c=3*c+(1 << total)
        total+=exponent
    return c

def replay(words,source,target):
    cur=source
    for exponent in words:
        numerator=3*cur+1
        valuation=(numerator & -numerator).bit_length()-1
        require(valuation==exponent,('valuation',words,source,cur,valuation,exponent))
        cur=numerator>>valuation
    require(cur==target,('endpoint',words,source,target,cur))

def reverse_words(target,remaining,budget,reverse_prefix=()):
    if remaining==0:
        yield tuple(reversed(reverse_prefix)),target
        return
    for exponent in range(1,budget-remaining+2):
        numerator=(target << exponent)-1
        if numerator%3: continue
        child=numerator//3
        if child<=0 or child%2==0: continue
        yield from reverse_words(child,remaining-1,budget-exponent,reverse_prefix+(exponent,))

result={'protocol_sha256':hashlib.sha256((BASE/'protocol.json').read_bytes()).hexdigest(),'pairs':[],'words':0,'edits':0,'transports':0,'identities_checked':0,'signs':{},'signed_shift_counts':{},'max_depth_observed':0}
signs=Counter();shifts=Counter()
for n,y in SPEC['pairs']:
    local={'n':n,'y':y,'words':0,'edits':0,'transports':0,'max_depth':0,'examples':[]}
    seen=set()
    for k in range(SPEC['length_min'],SPEC['length_max']+1):
        for w,u in reverse_words(n,k,SPEC['total_exponent_max']):
            require((w,u) not in seen,('duplicate',w,u))
            seen.add((w,u));local['words']+=1
            replay(w,u,n)
            C=constant(w);A=sum(w)
            require((3**k)*u+C==(1<<A)*n,('old_affine',w,u,n))
            require((1<<A)*n<=(4**k)*u,('budget',w,u,n))
            for i in range(k-1):
                P=sum(w[:i+1]);B=sum(w[i+1:]);q=k-i-1;T=constant(w[i+1:])
                for delta in range(1-w[i],w[-1]):
                    if delta==0: continue
                    local['edits']+=1
                    ws=list(w);ws[i]+=delta;ws[-1]-=delta;wp=tuple(ws)
                    Cp=constant(wp)
                    d=abs(delta)
                    if delta>0:
                        require(Cp-C==((1<<d)-1)*(1<<P)*T,('Cshift+',w,i,delta))
                        R=(1<<B)*(y-n)-((1<<d)-1)*T
                        scale=1<<P
                    else:
                        require(C-Cp==((1<<d)-1)*(1<<(P-d))*T,('Cshift-',w,i,delta))
                        R=(1<<(B+d))*(y-n)+((1<<d)-1)*T
                        scale=1<<(P-d)
                    require(R%2==1,('Rodd',w,i,delta,R))
                    result['identities_checked']+=1
                    v=inverse(wp,y)
                    if v is None: continue
                    replay(wp,v,y)
                    local['transports']+=1;local['max_depth']=max(local['max_depth'],k)
                    signs['positive' if delta>0 else 'negative']+=1;shifts[delta]+=1
                    require((3**k)*(v-u)==scale*R,('residual',w,i,delta,u,v,R))
                    require(R%(3**k)==0,('depth_divisibility',w,i,delta,R))
                    terminal=y-(1<<d)*n if delta>0 else (1<<d)*y-n
                    require(terminal%(3**q)==0,('locality',w,i,delta,q,terminal))
                    if len(local['examples'])<4:
                        local['examples'].append({'word':w,'new_word':wp,'i_one_based':i+1,'delta':delta,'u':u,'v':v,'q':q,'residual':R})
    result['pairs'].append(local)
    for label in ('words','edits','transports'):result[label]+=local[label]
    result['max_depth_observed']=max(result['max_depth_observed'],local['max_depth'])
result['signs']=dict(sorted(signs.items()))
result['signed_shift_counts']={str(k):v for k,v in sorted(shifts.items())}
print(json.dumps(result,indent=2,sort_keys=True))
