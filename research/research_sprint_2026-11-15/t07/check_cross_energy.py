#!/usr/bin/env python3
"""Finite check of a new algebraic energy identity, not of its uniform bound."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,math

HERE=Path(__file__).resolve().parent
builder=HERE.parent/'t03/stationary_cylinders.py'
spec=importlib.util.spec_from_file_location('t03_builder',builder)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    plan=json.loads((HERE/'cross_energy_protocol.json').read_text())
    previous=[1.0];exact_previous=[Q(1)];rows=[]
    for k in plan['k']:
        size=3**(k+1)
        current,_=mod.density_step(previous,size)
        old_energy=math.fsum(x*x for x in previous)/len(previous)
        new_energy=math.fsum(x*x for x in current)/len(current)
        corr=math.fsum(current[3*y+1]*previous[y] for y in range(len(previous)))/len(previous)
        error=abs(new_energy-old_energy-(2/3)*corr)
        require(error<=plan['float_tolerance'],'cross energy identity')
        row={'k':k,'N_k':old_energy,'N_next':new_energy,'correlator':corr,'increment':new_energy-old_energy,'error':error}
        if k in plan['rational_exact_k']:
            exact,_=mod.density_step(exact_previous,size,exact=True)
            old=sum((x*x for x in exact_previous),Q())/len(exact_previous)
            new=sum((x*x for x in exact),Q())/len(exact)
            ec=sum((exact[3*y+1]*exact_previous[y] for y in range(len(exact_previous))),Q())/len(exact_previous)
            require(new-old==Q(2,3)*ec,'exact cross energy')
            row['exact']={'N_k':str(old),'N_next':str(new),'correlator':str(ec),'status':'PASS'}
            exact_previous=exact
        rows.append(row);previous=current
    print(json.dumps({'status':'PASS','uniform_correlator_bound_proved':False,'rows':rows},sort_keys=True,indent=2))
if __name__=='__main__':main()
