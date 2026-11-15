#!/usr/bin/env python3
"""Bounded terminal replacement check, independent of T02's construction."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json

BASE=Path(__file__).resolve().parent
SPEC=json.loads((BASE/'terminal_protocol.json').read_text())

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def inverse(w,target):
    x=target
    for a in reversed(w):
        q=(x<<a)-1
        if q%3:return None
        x=q//3
        if x<=0 or x%2==0:return None
    return x

def replay(w,u,target):
    x=u
    for a in w:
        q=3*x+1;actual=(q&-q).bit_length()-1
        require(actual==a,('bad-valuation',w,u,a,actual))
        x=q>>a
    require(x==target,('bad-endpoint',w,u,target,x))

def constant(w):
    C=0;A=0
    for a in w:C=3*C+(1<<A);A+=a
    return C

def backwards(target,length,budget,tail=()):
    if length==0:
        yield tuple(reversed(tail)),target
    else:
        for a in range(1,budget-length+2):
            q=(target<<a)-1
            if q%3:continue
            child=q//3
            if child<=0 or child%2==0:continue
            yield from backwards(child,length-1,budget-a,tail+(a,))

def compositions(total,length):
    if length==0:
        if total==0:yield ()
        return
    if total<length:return
    for cs in combinations(range(1,total),length-1):
        bounds=(0,)+cs+(total,)
        yield tuple(bounds[i+1]-bounds[i] for i in range(length))

result={'protocol_sha256':hashlib.sha256((BASE/'terminal_protocol.json').read_bytes()).hexdigest(),'source_words':0,'candidate_replacements':0,'actual_transports':0,'off_diagonal':0,'diagonal':0,'diagonal_examples':[],'off_diagonal_examples':[],'parameters':{},'pairs':[]}
parameters=Counter()
for n,y in SPEC['pairs']:
    local={'n':n,'y':y,'source_words':0,'actual_transports':0,'diagonal':0,'off_diagonal':0}
    for k in range(SPEC['length_min'],SPEC['length_max']+1):
        for w,u in backwards(n,k,SPEC['total_exponent_max']):
            local['source_words']+=1
            replay(w,u,n)
            for L in SPEC['old_tail_lengths']:
                if L>k:continue
                p=k-L;pref=w[:p];alpha=w[p:];P=sum(pref);B=sum(alpha)
                for M in SPEC['new_tail_lengths']:
                    for D in SPEC['net_total_shifts']:
                        new_total=B+D
                        for beta in compositions(new_total,M):
                            result['candidate_replacements']+=1
                            wp=pref+beta;v=inverse(wp,y)
                            if v is None:continue
                            replay(wp,v,y)
                            F=1<<max(D,0);G=1<<max(-D,0)
                            R=(1<<B)*((3**L)*F*y-(3**M)*G*n)+(3**M)*G*constant(alpha)-(3**L)*G*constant(beta)
                            require(G*(3**(p+L+M))*(v-u)==(1<<P)*R,('residual',n,y,w,wp,D,R,u,v))
                            require(R%(3**(p+L+M))==0,('full-divisibility',n,y,w,wp,D,R))
                            require((R==0)==(u==v),('diagonal-equivalence',n,y,w,wp,D,R,u,v))
                            local['actual_transports']+=1
                            parameters[(L,M,D)]+=1
                            label='diagonal' if u==v else 'off_diagonal'
                            local[label]+=1
                            sample={'n':n,'y':y,'u':u,'v':v,'word':w,'new_word':wp,'L':L,'M':M,'D':D,'residual':R}
                            if len(result[label+'_examples'])<5:result[label+'_examples'].append(sample)
    for key in ('source_words','actual_transports','off_diagonal','diagonal'):result[key]+=local[key]
    result['pairs'].append(local)
result['parameters']={','.join(map(str,k)):v for k,v in sorted(parameters.items())}
print(json.dumps(result,indent=2,sort_keys=True))
