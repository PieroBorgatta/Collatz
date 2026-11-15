#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
from coupling_policies import edges,inverse
H=Path(__file__).resolve().parent
P=json.loads((H/'harmonic_protocol.json').read_text())
Q=1<<P['harmonic_bits']

def mass_interval(rows):
    a=sum(Q//u for u,v,A,B in rows)
    return {'scaled_lower':a,'scaled_upper':a+len(rows),'scale':Q,'lower_float':a/Q,'upper_float':(a+len(rows))/Q}

def summarize(nodes,k):
    allmass=mass_interval(nodes)
    vals=[]
    for D in P['height_thresholds']:
        good=[t for t in nodes if t[1]<=D*t[0]]
        selected={}
        for row in good:
            if row[1] not in selected or row[0]<selected[row[1]][0]:selected[row[1]]=row
        h=mass_interval(good);s=mass_interval(list(selected.values()))
        vals.append({'D':D,'good_codes':len(good),'distinct_good_images':len(selected),'good_mass':h,'selected_mass':s,'good_fraction_lower':h['scaled_lower']/allmass['scaled_upper'],'good_fraction_upper':h['scaled_upper']/allmass['scaled_lower'],'selected_fraction_lower':s['scaled_lower']/allmass['scaled_upper'],'selected_fraction_upper':s['scaled_upper']/allmass['scaled_lower']})
    return {'depth':k,'codes':len(nodes),'source_harmonic_mass':allmass,'height_rows':vals}

R={'protocol_sha256':hashlib.sha256((H/'harmonic_protocol.json').read_bytes()).hexdigest(),'runs':[]}
for n in P['targets']:
    y=4*n+1 if n%3==1 else 16*n+5
    for policy in P['policies']:
        nodes=[(n,y,0,0)];rows=[]
        for k in range(1,P['max_depth']+1):
            nxt=[]
            for u,v,A,B in nodes:
                for s,a,b in edges(policy,u,v,A,B):nxt.append((inverse(u,a),inverse(v,b),A+a,B+b))
            nodes=nxt
            if k in P['record_depths']:rows.append(summarize(nodes,k))
        R['runs'].append({'n':n,'y':y,'policy':policy,'levels':rows})
print(json.dumps(R,sort_keys=True,separators=(',',':')))
