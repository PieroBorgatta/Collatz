#!/usr/bin/env python3
"""Exact finite checks supporting the paper-level notes, not their full proofs.

AI-assisted development: Codex with Piero Borgatta, 2026-09-26.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product


def require(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)


# Curry's deliberately weaker exponent choices in LITERATURE_IT.md.
require(5**50 < 2**69 * 3**30, "first Curry exponent inequality")
require(3**30 < 2**49, "second Curry exponent inequality")

# Bernoulli exponents in {1,2}: terms from j=3 onward vanish modulo 8.
residues = Counter()
for a, b in product((1, 2), repeat=2):
    x = -(pow(3, -1, 8) + 2**a * pow(9, -1, 8)
          + 2**(a+b) * pow(27, -1, 8)) % 8
    residues[x] += 1
nu = tuple(F(residues[r], 4) for r in (1, 3, 5, 7))
uniform = (F(1, 4),) * 4
matrix = (uniform, (F(1, 2), 0, F(1, 2), 0),
          uniform, (0, F(1, 2), 0, F(1, 2)))
image = tuple(sum(nu[i] * matrix[i][j] for i in range(4)) for j in range(4))
require(nu == (F(1, 2), F(1, 4), 0, F(1, 4)), "coded distribution modulo 8")
require(image == uniform and image != nu, "Haar-kernel projection obstruction")

# Exact affine coefficients of the two-return family in CRITICAL_MAP_IT.md.
states = ((205087, 1179648), (307631, 1769472), (461447, 2654208),
          (692171, 3981312), (1038257, 5971968),
          (778693, 4478976), (146005, 839808))
for (a, b), (c, d), exponent in zip(states, states[1:], (1, 1, 1, 1, 2, 4)):
    require(3*a + 1 == 2**exponent*c and 3*b == 2**exponent*d,
            "affine iterate identity")
    require(c % 2 == 1 and d % 2 == 0, "exact odd endpoint")
for a, b in states[1:6]:
    require(a > states[0][0] and b > states[0][1], "no descent before step six")
require(states[6][0] < states[0][0] and states[6][1] < states[0][1],
        "descent at step six")
for index in (0, 5):
    a, b = states[index]
    require(a % 18 == 13 and b % 18 == 0, "marked source and first return")
require(states[6][0] % 1152 == 853 and states[6][1] % 1152 == 0,
        "second return residue")
require(tuple(a % 72 for a, _ in states[1:5]) == (47, 71, 35, 17)
        and all(b % 72 == 0 for _, b in states[1:5]), "intermediate residues")

print("PASS: two exponent inequalities, exact modulo-8 projection, affine pilot identities and residues.")
print("These checks do not prove the infinite-measure construction, density hypothesis, or Collatz.")
