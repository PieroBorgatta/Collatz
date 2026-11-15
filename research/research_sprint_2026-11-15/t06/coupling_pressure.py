#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction
import json,hashlib
from coupling_policies import edges,inverse,check
H=Path(__file__).resolve().parent
P=json.loads((H/'pressure_protocol.json').read_text())

def mass(A,k):
    m=max(A,default=0)
    return Fraction(3**k*sum(1<<(m-a) for a in A),1<<m)

def data(nodes,k):
    image={}
    for u,v,A,B in nodes:
        if v in image:
            prev=image[v]
            check(prev[3]==B,'same image has different exact word totals')
            if A<prev[2]:image[v]=(u,v,A,B)
        else:image[v]=(u,v,A,B)
    src=mass([A for u,v,A,B in nodes],k)
    capped=mass([A for u,v,A,B in image.values()],k)
    im=mass([B for u,v,A,B in image.values()],k)
    return {'depth':k,'codes':len(nodes),'images':len(image),'source_mass':str(src),'source_mass_float':float(src),'selected_source_mass':str(capped),'selected_source_fraction':float(capped/src),'image_mass':str(im),'image_mass_float':float(im)}

R={'pressure_protocol_sha256':hashlib.sha256((H/'pressure_protocol.json').read_bytes()).hexdigest(),'runs':[]}
for n in P['targets']:
    y=4*n+1 if n%3==1 else 16*n+5
    for policy in P['policies']:
        nodes=[(n,y,0,0)]
        rows=[data(nodes,0)]
        for k in range(1,P['max_depth']+1):
            nxt=[]
            for u,v,A,B in nodes:
                for s,a,b in edges(policy,u,v,A,B):
                    nxt.append((inverse(u,a),inverse(v,b),A+a,B+b))
            nodes=nxt;rows.append(data(nodes,k))
        R['runs'].append({'n':n,'y':y,'policy':policy,'levels':rows})
print(json.dumps(R,sort_keys=True,separators=(',',':')))
