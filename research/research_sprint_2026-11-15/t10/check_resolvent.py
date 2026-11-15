#!/usr/bin/env python3
"""Exact stationary-cylinder and odometer checks, independent implementation.

The forward cycle recurrence is used only in exact rational arithmetic.
No downloaded code or previous agent's program is imported.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rho_step(previous):
    q = 3 * len(previous)
    L = 2 * (q // 3)
    orbit = [pow(2, i, q) for i in range(L)]
    need(len(set(orbit)) == L and pow(2, L, q) == 1, 'doubling cycle')
    forcing = []
    for x in orbit:
        forcing.append(F(3, 2) * previous[((2*x-1)//3) % len(previous)]
                       if x % 3 == 2 else F(0))
    boundary = sum((b * 2**(L-i) for i, b in enumerate(forcing)), F(0)) / (2**L-1)
    values = [F(0)] * q
    current = boundary
    for x, b in zip(orbit, forcing):
        values[x] = current
        current = 2 * (current-b)
    need(current == boundary, 'exact forward boundary')
    need(sum(values, F(0)) == q, 'probability mass')
    for x, value in enumerate(values):
        rhs = F(1, 2)*values[(2*x) % q]
        if x % 3 == 2:
            rhs += F(3, 2)*previous[((2*x-1)//3) % len(previous)]
        need(value == rhs and value >= 0, 'binary recursion')
    return values


def main():
    levels = [[F(1)]]
    for _ in range(6):
        levels.append(rho_step(levels[-1]))
    results = []
    for k in range(6):
        f, nxt = levels[k], levels[k+1]
        q = len(f)
        odometer = [(4*y+1) % q for y in range(q)]
        orbit = [0]
        for _ in range(q-1):
            orbit.append(odometer[orbit[-1]])
        need(len(set(orbit)) == q and odometer[orbit[-1]] == 0, 'odometer cycle')
        g = [nxt[(3*y+1) % len(nxt)] for y in range(q)]
        correlations = [sum((f[y]*f[(pow(4, j, 3*q)*(3*y+1)-1)//3 % q]
                             for y in range(q)), F(0)) / q for j in range(1, q+1)]
        weighted_correlation = F(0)
        for y in range(q):
            value = F(0)
            image = y
            for j in range(1, q+1):
                image = odometer[image]
                value += 4**(q-j)*f[image]
            value *= F(3, 4**q-1)
            need(value == g[y], 'finite cyclic resolvent')
            need(g[y] == F(1,4)*g[odometer[y]] + F(3,4)*f[odometer[y]], 'one step resolvent')
        H = sum((a*b for a,b in zip(g, f)), F(0)) / q
        C_resolvent = F(3, 4**q-1) * sum((4**(q-j)*c for j,c in enumerate(correlations, 1)), F(0))
        need(H == C_resolvent, 'autocorrelation resolvent')
        energy = sum((x*x for x in f), F(0))/q
        energy_next = sum((x*x for x in nxt), F(0))/len(nxt)
        need(energy_next-energy == F(2,3)*H, 'energy increment')
        need(sum(g, F(0)) == q, 'flat resolvent mean is one')
        results.append({'k': k, 'modulus': q, 'H': str(H), 'H_float': float(H),
                        'C_1': str(correlations[0]), 'C_1_float': float(correlations[0]),
                        'energy': str(energy), 'energy_next': str(energy_next),
                        'pointwise_resolvent_checks': q})
    # A paired spike at A_j=(3^j-1)/2 is carried exactly to B_j=2*3^j-1.
    # On A_j the two resolved spikes have height (1/2)*3^j, so each
    # contributes at least 1/4 to the adjacent odometer autocorrelation.
    cylinders = []
    for j in range(1, 9):
        a = (3**j-1)//2; b = 2*3**j-1; depth = 2*j
        need(4*a+1 == b and a % 3 == 1 and b % 3 == 2, 'paired spike affine map')
        for old_a, old_b, old_depth in cylinders:
            common = 3**min(depth, old_depth)
            need((a-old_a) % common != 0 and (b-old_b) % common != 0, 'paired disjointness')
        need(F(1,2)**2 * 3**(2*j) * F(1,3**depth) == F(1,4), 'each paired cost')
        cylinders.append((a,b,depth))
    return {'status':'PASS', 'asymptotic_claim':False,
            'constructor':'Independent exact forward doubling-cycle solution',
            'levels':results, 'pointwise_checks':sum(r['modulus'] for r in results),
            'paired_spikes_checked':len(cylinders),
            'paired_correlation_lower_bound':str(F(len(cylinders),4)),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
