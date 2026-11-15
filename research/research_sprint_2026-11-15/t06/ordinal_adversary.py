#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
P=json.loads((H/'adversary_protocol.json').read_text())

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def lowexp(z):
    for b in range(1,7):
        num=(1<<b)*z-1
        if num%3==0 and (num//3)%2!=0 and (num//3)%3!=0:return b
    raise RuntimeError('no minimal child')

def inv(z,b):
    num=(1<<b)*z-1
    require(num%3==0,'noninteger')
    v=num//3
    require(v%2!=0 and v%3!=0,'bad child')
    return v

rows=[]
for t in P['t_values']:
    n=18*3**t-1;y=16*n+5
    z=-11;u=n;v=y;B=0;bb=[]
    for i in range(t):
        b=lowexp(z);require(lowexp(u)==1,'base exponent')
        require(lowexp(v)==b,'ordinal mismatch')
        z=inv(z,b);u=inv(u,1);v=inv(v,b);B+=b;bb.append(b)
        require(z<0 and z!=-1,'negative path hit−1')
        require(u==18*2**(i+1)*3**(t-i-1)-1,'source formula')
        require(v==288*2**B*3**(t-i-1)+z,'image formula')
        require(v>0,'image nonpositive')
    require(u==18*2**t-1,'final source')
    require(v>=277*2**B,'image lower')
    require(2**B*11*7**t>=3*18**t,'negative growth bound')
    require(v*66*7**t>=u*277*9**t,'height bound')
    ext=[]
    for R in P['extra_rank_blocks']:
        a=1+6*R;b=lowexp(z)+6*R
        U=inv(u,a);V=inv(v,b)
        require(U>0 and V>0,'extension positivity')
        require(V*u>v*U,'extended ratio should strictly grow')
        ext.append({'rank':2*R,'source':U,'image':V})
    rows.append({'t':t,'target':n,'sibling':y,'source':u,'image':v,'B':B,'negative_endpoint':z,'negative_exponents':bb,'extensions':ext})
print(json.dumps({'protocol_sha256':hashlib.sha256((H/'adversary_protocol.json').read_bytes()).hexdigest(),'cases':len(rows),'status':'PASS','rows':rows},sort_keys=True,separators=(',',':')))
