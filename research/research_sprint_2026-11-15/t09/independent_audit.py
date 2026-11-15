#!/usr/bin/env python3
"""Independent finite error checks for the T07/T08 paper deductions.

No T07/T08 implementation is imported. Countermodel arrays are obtained by
averaging disjoint Haar cylinders directly; capped basins by forward orbits.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SPEC = json.loads((ROOT / 'protocol.json').read_text())


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def pow3(e):
    return F(3 ** e) if e >= 0 else F(1, 3 ** (-e))


def step(x):
    y = 3 * x + 1
    a = 0
    while y % 2 == 0:
        y //= 2
        a += 1
    return y, a


def path(seed):
    seen = set()
    states, exponents = [], []
    x = seed
    for _ in range(SPEC['orbit_step_limit']):
        if x in seen:
            return states, exponents
        seen.add(x)
        states.append(x)
        x, a = step(x)
        exponents.append(a)
    raise RuntimeError(('incomplete orbit', seed))


def direct_caps():
    xmax = SPEC['odd_source_cutoff']
    inputs = list(range(1, xmax + 1, 2))
    orbits = {u: path(u) for u in inputs}
    first8 = {}
    for u in inputs:
        x = u
        aa = []
        for _ in range(max(SPEC['prefix_lengths'])):
            x, a = step(x)
            aa.append(a)
        first8[u] = aa
    cutoff_list = [1, 2, 3, 8, 32, 128, 512, xmax]
    checks = 0
    results = []
    for M in SPEC['caps']:
        theta = F(2**M - 1, 2**M)
        prefix = {r: {u for u in inputs if all(a <= M for a in first8[u][:r])}
                  for r in SPEC['prefix_lengths']}
        for n in SPEC['targets']:
            selected = set()
            depths = {}
            for u, (states, exponents) in orbits.items():
                if n not in states:
                    continue
                j = states.index(n)
                if all(a <= M for a in exponents[:j]):
                    selected.add(u)
                    depths[u] = j
            for X in cutoff_list:
                actual = sum(u <= X for u in selected)
                for r in SPEC['prefix_lengths']:
                    pcount = sum(u <= X for u in prefix[r])
                    early = sum(u <= X and depths[u] < r for u in selected)
                    early_bound = sum(M**k for k in range(r))
                    bound = early_bound + F(X, 2) * theta**r + M**r
                    need(pcount <= F(X, 2) * theta**r + M**r,
                         ('prefix-rounding', M, X, r, pcount))
                    need(early <= early_bound, ('short-words', M, n, X, r))
                    need(actual <= early + pcount, ('depth-split', M, n, X, r))
                    need(actual <= bound, ('finite-capped-bound', M, n, X, r))
                    checks += 4
                ordinary = 0
                scale = X
                while scale >= 1:
                    ordinary += sum(u <= scale for u in selected)
                    scale //= 2
                item = {'M': M, 'target': n, 'X': X, 'odd_count': actual,
                        'ordinary_lift_count': ordinary}
                if M >= 2:
                    with localcontext() as ctx:
                        ctx.prec = 70
                        md = Decimal(M)
                        td = Decimal(theta.numerator) / Decimal(theta.denominator)
                        alpha = md.ln() / (md / td).ln()
                        power = (alpha * Decimal(X).ln()).exp()
                        need(Decimal(actual) <= 3 * power, ('optimized-odd', item))
                        need(Decimal(ordinary) <= 9 * power, ('optimized-ordinary', item))
                        need(alpha >= Decimal(2) / Decimal(3), ('alpha-lower', M))
                        deficit_lower = Decimal(1) / (Decimal(2)**M * 2 * md.ln())
                        need(1-alpha >= deficit_lower, ('deficit-lower', M))
                        item['alpha_decimal'] = str(alpha)
                        item['optimized_bounds_decimal_only'] = True
                results.append(item)
    return {'status': 'PASS', 'source_orbits_completed': len(orbits),
            'exact_finite_inequality_checks': checks, 'finite_rows': len(results),
            'optimized_numeric_checks_not_a_proof': True, 'rows': results}


def average_by_cylinders(m):
    modulus = 3**m
    base = [F(1, 2)] if m == 0 else [F(3, 4) if r % 3 else F(0)
                                               for r in range(modulus)]
    values = base[:]
    J = m + SPEC['countermodel_spike_truncation_extra']
    for j in range(1, J + 1):
        center, depth, amplitude = 2 * 3**j - 1, 2*j, 3**j
        if depth >= m:
            values[center % modulus] += amplitude * pow3(m-depth)
        else:
            q = 3**depth
            for residue in range(center % q, modulus, q):
                values[residue] += amplitude
    # All omitted centers are -1 modulo3^m. Their total mass is geometric.
    values[modulus-1] += F(3**m, 2 * 3**J)
    return values, base, J


def model_checks():
    rows = []
    previous = None
    consistency = 0
    for m in SPEC['countermodel_depths']:
        values, base, J = average_by_cylinders(m)
        modulus = 3**m
        need(sum(values, F()) / modulus == 1, ('Haar-mass', m))
        need(all(v >= 0 for v in values), ('nonnegative', m))
        energy = sum((v*v for v in values), F()) / modulus
        if m == 0:
            expected = F(1)
            l1 = F(15, 16)
        else:
            r = m // 2
            expected = (F(r) + F(5, 4) + F(9, 8 * 9**r)) if m % 2 == 0 else (
                       F(r) + F(3, 2) + F(3, 8 * 9**r))
            need(energy <= F(m,2) + F(11,8), ('linear-energy', m))
            # Integrate |F-rho_m| using the disjoint exact spike cylinders.
            l1 = F(1,2)
            for j in range(1, J+1):
                center = 2*3**j-1
                p = values[center % modulus] - F(3,4)
                amp = F(3**j)
                l1 += (abs(amp-p)-p) / (3**(2*j))
            l1 += F(1, 2*3**J) - F(3, 8*3**(2*J))
            closed = sum((2*pow3(-j)-2*pow3(m-3*j)
                          for j in range(m//2+1, m)),F())
            closed += 3*pow3(-m) - F(27,8)*pow3(-2*m)
            need(l1 == closed, ('L1-closed-form', m, l1, closed))
            need(l1 <= pow3(-(m//2)), ('L1-critical-upper', m))
            for j in range(1, 11):
                n = 2*3**j-1
                sibling = 16*n+5
                need(values[sibling % modulus] == F(3,4), ('sibling-background',m,j))
                if m >= 2*j:
                    need(values[n % modulus] == F(3,4)+3**j, ('resolved-trace',m,j))
        need(energy == expected, ('exact-energy',m,energy,expected))
        if previous is not None:
            coarse = len(previous)
            for r in range(coarse):
                need((values[r]+values[r+coarse]+values[r+2*coarse])/3 == previous[r],
                     ('conditional-consistency',m,r))
                consistency += 1
        rows.append({'depth':m,'residues':modulus,'mass':'1','L2_energy':str(energy),
                     'L1_error':str(l1),'status':'PASS'})
        previous = values
    return {'status':'PASS','conditional_consistency_checks':consistency,
            'exact_energy_formulas_independent':True,'rows':rows,
            'stationarity_counterexample':{'x':2,'F_x':'3/4','LF_x':'3/2'},
            'not_actual_syracuse_density':True}


if __name__ == '__main__':
    print(json.dumps({'status':'PASS','finite_only':True,
                      'capped_counts':direct_caps(),'countermodel':model_checks()},
                     indent=2,sort_keys=True))
