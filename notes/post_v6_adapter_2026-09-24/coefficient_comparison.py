#!/usr/bin/env python3
"""Exact finite checks for the paper-level coefficient comparison.

These are the same integer inequalities and parameter grid used in the
2026-09-24 audit. The script also writes a machine-readable report beside
itself. It does not invoke Lean, align the actual weighted theorem's chooser,
or attempt to materialize the enormous density-coefficient denominators.
"""

from fractions import Fraction
import json
from pathlib import Path


count = 0
max_ratio = (Fraction(0), None)
for a in range(1, 201):
    if a % 3 == 0:
        continue
    r = (4 * a) // 3 if a % 3 == 1 else (2 * a) // 3
    b0 = 3 * r + 1
    assert b0 >= 4 and 6 * a + 1 <= 4 * b0
    for q in range(5):
        Q = 3 ** q
        for X in range(2, 9):
            n = (X + 3) * Q
            T = (4 ** n * (6 * a + 1) - 1) // 3
            for p in range(Q):
                k = p + (X + 1) * Q
                R = (4 ** k * b0 - 1) // 3
                P = R * (3 * R + 1)
                B = 3 * R + 1
                assert 2 * k >= n + 1
                assert R >= 85 and R < T
                assert b0 * (3 * T + 1) <= B * B
                assert 4 * (3 * T + 1) <= B * B
                assert 4 * T <= 3 * R * R + 2 * R - 1
                assert T < R * R < P
                assert P > 3 * T
                count += 1
                ratio = Fraction(T, R * R)
                if ratio > max_ratio[0]:
                    max_ratio = (ratio, (a, q, X, p, R, T, P))

assert count == 113498
print("Exact integer checks:", count)
print("Grid: 1<=a<=200, 3 does not divide a; 0<=q<=4; 2<=X<=8; 0<=p<3^q")
print("Largest T/R^2 in this finite grid:", max_ratio)
a, q, X, p, R, T, P = max_ratio[1]
print("At this example, exact P/T =", Fraction(P, T))
grid_example = dict(a=a, q=q, X=X, p=p, R=R, T=T, P=P)

# This is beyond the stated X>=2 assumptions, not a failure of the theorem.
a, X, q, p = 2, 1, 0, 0
r = 1
Q = 1
k = 2
n = 4
R = (4 ** k * 4 - 1) // 3
T = (4 ** n * 13 - 1) // 3
assert T > R * R
print("X=1 excluded example: R=", R, "T=", T, "R^2=", R * R)

report = {
    "audit_date": "2026-09-24",
    "status": "PASS: finite exact-integer consistency checks",
    "checked_tuples": count,
    "grid": {
        "a_inclusive": [1, 200],
        "exclude_a_divisible_by_3": True,
        "q_inclusive": [0, 4],
        "X_inclusive": [2, 8],
        "p": "every integer 0 <= p < 3^q",
    },
    "arithmetic": "Python integers and fractions.Fraction; no floating point",
    "checked_per_tuple": [
        "2*k >= n+1",
        "R >= 85 and R < T",
        "b0*(3*T+1) <= (3*R+1)^2",
        "4*(3*T+1) <= (3*R+1)^2",
        "4*T <= 3*R^2+2*R-1",
        "T < R^2 < P",
        "P > 3*T",
    ],
    "largest_T_over_R_squared_in_finite_grid": {
        "numerator": max_ratio[0].numerator,
        "denominator": max_ratio[0].denominator,
        "example": grid_example,
        "global_extremality_proved": False,
    },
    "excluded_X_one_example": dict(a=a, q=q, X=X, p=p, R=R, T=T, R_squared=R * R),
    "interpretation": {
        "general_comparison": "paper-level proof in the companion Markdown report",
        "comparison_formalized_in_Lean": False,
        "Lean_compiler_invoked": False,
        "actual_weighted_chooser_alignment_established": False,
        "coefficient_comparison_condition": "same C in Nat and same candidate R; m(Z)=132*Z*C+1",
        "enormous_coefficient_denominators_evaluated": False,
        "cutoff_dominance_established": False,
        "finite_checks_replace_general_proof": False,
    },
}
output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print("Machine-readable report:", output)
