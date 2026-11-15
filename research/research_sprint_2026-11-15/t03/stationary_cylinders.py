#!/usr/bin/env python3
"""Frozen cylinder-law diagnostic. No arithmetic trace error bound is claimed."""

from array import array
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

MAX_M = 12
KS = tuple(range(1, 11))
NEGATIVE_CONTROLS = (-1, -5, -17, -11)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unit_cycle(modulus):
    period = 2 * (modulus // 3)
    cycle = array("I")
    value = 1
    for _ in range(period):
        cycle.append(value)
        value = (2 * value) % modulus
    require(value == 1 and len(set(cycle)) == period, "unit cycle incomplete")
    return cycle


def density_step(previous, modulus, exact=False):
    cycle = unit_cycle(modulus)
    period = len(cycle)
    zero = Fraction(0) if exact else 0.0
    half = Fraction(1, 2) if exact else 0.5
    three_halves = Fraction(3, 2) if exact else 1.5
    forcing = [] if exact else array("d")
    for index in range(period):
        value = cycle[(index + 1) % period]
        forcing.append(previous[(value - 1) // 3] if value % 3 == 1 else zero)
    # One backward pass with a zero boundary gives the numerator of the
    # periodic solution. The return multiplier is exactly 2**(-period).
    current = zero
    for index in range(period - 1, -1, -1):
        current = half * current + three_halves * forcing[index]
    factor = Fraction(1, 2**period) if exact else math.ldexp(1.0, -period)
    boundary = current / (1 - factor)
    result = [zero] * modulus if exact else array("d", [0.0]) * modulus
    current = boundary
    for index in range(period - 1, -1, -1):
        current = half * current + three_halves * forcing[index]
        result[cycle[index]] = current
    require(current == boundary if exact else abs(current - boundary) <= 1e-12,
            "periodic boundary mismatch")
    max_residual = zero
    for index, value in enumerate(cycle):
        next_value = cycle[(index + 1) % period]
        rhs = half * result[next_value] + three_halves * forcing[index]
        max_residual = max(max_residual, abs(result[value] - rhs))
        require(result[value] > 0, "nonpositive unit density")
    require(all(result[value] == 0 for value in range(0, modulus, 3)),
            "mass outside units")
    total = sum(result) if exact else math.fsum(result)
    if exact:
        require(total == modulus and max_residual == 0, "exact law failure")
    else:
        require(abs(total - modulus) <= 1e-12 * modulus, "mass normalization")
        require(max_residual <= 1e-9, "stationary equation residual")
    return result, {"modulus": modulus, "unit_count": len(cycle),
                    "mass_error": float(total - modulus),
                    "maximum_equation_residual": float(max_residual)}


def main():
    previous = array("d", [1.0])
    exact_previous = [Fraction(1)]
    profiles = []
    controls = []
    checks = []
    cumulative = {k: [0.0, 0.0] for k in KS}
    negative_cumulative = {n: 0.0 for n in NEGATIVE_CONTROLS}
    for m in range(1, MAX_M + 1):
        modulus = 3**m
        current, check = density_step(previous, modulus)
        check["m"] = m
        if m <= 4:
            exact_current, exact_check = density_step(exact_previous, modulus, exact=True)
            error = max(abs(float(a) - b) for a, b in zip(exact_current, current))
            require(error <= 1e-12, "exact/float discrepancy")
            check["fraction_replay"] = {"status": "PASS", "maximum_float_error": error,
                                        "exact_mass_error": exact_check["mass_error"]}
            exact_previous = exact_current
        checks.append(check)
        for k in KS:
            n = 2 * 3**k - 1
            sibling = 16 * n + 5
            base, upper = current[n % modulus], current[sibling % modulus]
            cumulative[k][0] += base
            cumulative[k][1] += upper
            profiles.append({"m": m, "k": k, "n": n, "h": sibling,
                             "rho_n": base, "rho_h": upper, "rho_h_over_n": upper / base,
                             "cesaro_n": cumulative[k][0] / m,
                             "cesaro_h": cumulative[k][1] / m,
                             "target_fixed_limit_not_reached": True,
                             "no_return_certified": False})
        for n in NEGATIVE_CONTROLS:
            value = current[n % modulus]
            negative_cumulative[n] += value
            controls.append({"m": m, "x": n, "rho": value,
                             "cesaro_rho": negative_cumulative[n] / m})
        previous = current
    script = Path(__file__).read_bytes()
    print(json.dumps({"status": "PASS", "protocol": "T03_STATIONARY_PROTOCOL_IT.md",
                      "script_sha256": hashlib.sha256(script).hexdigest(),
                      "arithmetic_trace_error_bound": False,
                      "asymptotic_orbit_or_density_claim": False,
                      "max_m": MAX_M, "ks": KS, "checks": checks,
                      "profiles": profiles, "negative_controls": controls}, indent=2))


if __name__ == "__main__":
    main()
