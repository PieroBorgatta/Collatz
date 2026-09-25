#!/usr/bin/env python3
"""Exact, fixed timing tests for conditional quadratic descent transfer.

Finite evidence only. Horizons are chosen from the lower descent certificate,
never by waiting for the upper orbit to descend or satisfy a coefficient test.
This is retrospective exploration of available data, not preregistration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "post_v6_levels_2026-09-24/levels_results.json"


def family(v: int) -> tuple[int, int]:
    if v < 5:
        raise ValueError("This experiment uses v >= 5")
    return (pow(9, 1 << v) - 1) >> (v + 3), ((1 << (3 * (1 << v) - 5)) - 11) // 3


def step(x: int) -> tuple[int, int]:
    if x <= 0 or x % 2 == 0:
        raise ValueError("Syracuse input must be positive and odd")
    raw = 3 * x + 1
    a = (raw & -raw).bit_length() - 1
    return raw >> a, a


def horizons(v: int, k: int) -> dict[str, int]:
    # These four formulas are fixed before inspecting any upper orbit.
    return {"double": 2 * k, "linear_3v": 2 * k + 3 * v,
            "quadratic_v2": 2 * k + v * v,
            "quarter_level": 2 * k + (1 << (v - 2))}


def trace_at(start: int, source: int, times: set[int]) -> tuple[dict[int, tuple[int, int]], int | None]:
    if not times or min(times) < 0:
        raise ValueError("Need nonnegative observation times")
    y, total = start, 0
    first = 0 if y < source else None
    snapshots = {0: (y, total)} if 0 in times else {}
    for j in range(1, max(times) + 1):
        y, a = step(y)
        total += a
        if first is None and y < source:
            first = j
        if j in times:
            snapshots[j] = y, total
    return snapshots, first


def check_pair(v: int, lower_record: dict, upper_record: dict) -> dict:
    X, N = family(v)
    Y, M = family(v + 1)
    c = 1 << (v + 2)
    assert Y == X + c * X * X
    assert M == 96 * N * N + 704 * N + 1287
    k = lower_record["tau_from_Q"]
    lower, tau = trace_at(X, N, {k})
    x, A = lower[k]
    assert tau == k and A == lower_record["exponent_sum"] and x < N
    p = pow(3, k)
    assert p * X < N << A  # The positive affine correction was not discarded.
    rules = horizons(v, k)
    # The baseline time is observed for independent agreement, not used by rules.
    upper_tau = upper_record["tau_from_Q"]
    upper, observed_tau = trace_at(Y, M, set(rules.values()) | {upper_tau})
    assert observed_tau == upper_tau
    assert upper[upper_tau][1] == upper_record["exponent_sum"]
    attempts = []
    for name, ell in rules.items():
        y, B = upper[ell]
        q = pow(3, ell)
        # alpha = c * (3^ell / 2^B) / (3^k / 2^A)^2.
        alpha_ok = (c * q << (2 * A)) <= (96 * p * p << B)
        time_ok = ell <= N
        certificate = ell < 3 * M and 3 * q * Y < (3 * M - ell) << B
        descended = upper_tau <= ell
        transfer = alpha_ok and time_ok
        assert not transfer or certificate
        assert not certificate or descended
        attempts.append({"rule": name, "ell": ell, "B": B,
                         "alpha_le_96": alpha_ok, "ell_le_lower_source": time_ok,
                         "transfer_certified": transfer,
                         "generic_certificate_passed": certificate,
                         "upper_descent_by_horizon": descended,
                         "upper_endpoint_below_source": y < M})
    return {"v": v, "lower_tau": k, "lower_A": A, "upper_tau": upper_tau,
            "lag_over_double": upper_tau - 2 * k, "attempts": attempts}


def cone_counterexample(a: int = 4) -> dict:
    if a < 4 or a % 2:
        raise ValueError("a must be even and at least 4")
    x = ((1 << a) - 1) // 3
    y = 96 * x * x - x + 2
    xx, actual_a = step(x)
    yy, b = step(y)
    alpha, beta, gamma = 4 * (1 << (2 * a)), -65 * (1 << (a - 3)), 5
    assert actual_a == a and b == 3
    assert yy == alpha * xx * xx + beta * xx + gamma
    assert alpha > 96 and beta < 0 and gamma <= 1287
    return {"a": a, "b": b, "x": x, "y": y,
            "next_x": xx, "next_y": yy,
            "coefficients_before": [96, -1, 2],
            "coefficients_after": [alpha, beta, gamma],
            "scope": "Generic compatible pair; reachability from Q_v not established"}


def run(max_v: int = 17) -> dict:
    if not 5 <= max_v <= 17:
        raise ValueError("Existing independent full-orbit baseline covers pairs v=5..17")
    raw = BASELINE.read_bytes()
    records = {r["v"]: r for r in json.loads(raw)["actual_cases"]}
    pairs = [check_pair(v, records[v], records[v + 1]) for v in range(5, max_v + 1)]
    summary = {}
    for name in horizons(5, 5):
        entries = [(p["v"], next(a for a in p["attempts"] if a["rule"] == name)) for p in pairs]
        summary[name] = {
            "certified_pairs": [v for v, a in entries if a["transfer_certified"]],
            "inconclusive_pairs": [v for v, a in entries if not a["transfer_certified"]],
            "upper_descent_not_yet_occurred": [v for v, a in entries if not a["upper_descent_by_horizon"]]}
    return {"scope": "Finite tests of fixed timing rules, not uniform induction or a novelty claim",
            "baseline_sha256": hashlib.sha256(raw).hexdigest(),
            "max_lower_v": max_v, "pair_count": len(pairs),
            "all_consistency_checks_passed": True,
            "summary": summary, "cone_counterexample": cone_counterexample(), "pairs": pairs}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-v", type=int, default=17)
    parser.add_argument("--output", type=Path, default=HERE / "induction_results.json")
    args = parser.parse_args()
    result = run(args.max_v)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"pair_count": result["pair_count"], "summary": result["summary"]}, indent=2))
