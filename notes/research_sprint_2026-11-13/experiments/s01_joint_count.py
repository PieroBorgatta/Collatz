#!/usr/bin/env python3
"""Independent finite census for the odd-target correction of rStation Lemma 3.1.
No external code is executed. All arithmetic is integral.
"""
from itertools import product
import json

def compositions(total,length):
    if length==0:
        if total==0: yield ()
        return
    if length==1:
        if total>=1: yield (total,)
        return
    for first in range(1,total-length+2):
        for rest in compositions(total-first,length-1):yield (first,)+rest

def const(word):
    c,a=0,0
    for e in word:
        c=3*c+2**a
        a+=e
    return c

def run(source,length):
    n,total=source,0
    for _ in range(length):
        q=3*n+1
        power=q&-q
        total+=power.bit_length()-1
        n=q//power
    return n,total

def check():
    cases=0
    for k in range(1,5):
        modulus=3**k
        for A in range(k,k+6):
            words=list(compositions(A,k))
            residues={}
            for w in words:
                r=const(w)*pow(2**A,-1,modulus)%modulus
                residues[r]=residues.get(r,0)+1
            for target in range(1,40,2):
                # Positive affine constant implies x < 2**A * target / 3**k.
                upper=(2**A*target-1)//modulus
                actual=sum(run(x,k)==(target,A) for x in range(1,upper+1,2))
                predicted=residues.get(target%modulus,0)
                if actual!=predicted:raise RuntimeError((k,A,target,actual,predicted))
                cases+=1
    return {'odd_target_cases':cases,'status':'PASS',
            'domain':{'k':[1,4],'A':'k..k+5','positive_odd_targets':[1,39]},
            'printed_even_target_counterexample':{'k':1,'A':1,'target':2,
              'residue_word_count':1,'actual_Syracuse_sources':0}}
if __name__=='__main__':print(json.dumps(check(),indent=2))
