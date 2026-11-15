#!/usr/bin/env python3
"""Exact macro exits and parameter resets. Finite diagnostic, not a proof.

Frozen domains: r=1..12, odd t=1..127, next-mark cap=64;
reset witnesses r=1..12,s=1..20; no threshold fitted to these data.
"""
from fractions import Fraction
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def valuation(n):
    require(n > 0, "valuation domain")
    return (n & -n).bit_length() - 1


def step(n):
    require(n > 0 and n % 2 == 1, "odd positive source")
    z = 3 * n + 1
    a = valuation(z)
    return z >> a, a


def section(n):
    return any(n % m == a for a, m in (
        (13, 18), (53, 72), (853, 1152), (3413, 4608),
        (54613, 73728), (218453, 294912),
    ))


def macro(r, t):
    return 18 * t * 8 ** r - 5


def reset_witness(r, s):
    c = 27 * 9 ** r
    power = 8 ** (s + 1)
    v = (13 * pow(power, -1, c)) % c
    if v % 2 == 0:
        v += c
    if power * v <= 13:
        v += 2 * c
    t = (power * v - 13) // c
    require(t > 0 and t % 2 == 1 and v > 0 and v % 2 == 1, "reset parity")
    require(power * v == c * t + 13, "reset link")
    start = macro(r, t)
    n = start
    for j in range(r):
        middle, a = step(n)
        endpoint, b = step(middle)
        require((a, b) == (1, 2), "macro valuation")
        require(section(n) and not section(middle) and section(endpoint), "macro first return")
        n = endpoint
    require(n == 18 * t * 9 ** r - 5, "macro endpoint")
    after_exit, a = step(n)
    middle, b = step(after_exit)
    target, d = step(middle)
    require((a, b, d) == (3, 1, 2), "exit word")
    require(not section(after_exit) and not section(middle) and section(target), "exit first return")
    require(target == macro(s - 1, v), "reset target")
    require(valuation(target + 5) == 1 + 3 * (s - 1), "reset clock")
    if r >= 9:
        require(start < after_exit and start < middle and start < target, "large-r no descent")
    return {"r": r, "s": s, "t": t, "v": v,
            "initial_clock": r, "next_clock": s - 1,
            "source": start, "target": target,
            "target_exceeds_source": target > start,
            "cofactor_increases": v > t}


def run():
    rows = []
    for r in range(1, 13):
        for t in range(1, 128, 2):
            start = macro(r, t)
            n = start
            for _ in range(r):
                n, a = step(n)
                n, b = step(n)
                require((a, b) == (1, 2), "baseline macro")
            require(n == 18 * t * 9 ** r - 5, "baseline endpoint")
            first, a = step(n)
            z = 27 * t * 9 ** r - 7
            require(a == 1 + valuation(z), "exit valuation formula")
            if z % (2 ** r) == 0:
                require(first < start, "linear-threshold sufficient descent")
            later, word, first_mark = n, [], None
            for j in range(1, 65):
                later, e = step(later)
                word.append(e)
                if section(later) or later == 1:
                    first_mark = {"time": j, "target": later, "word": word}
                    break
            rows.append({"r": r, "t": t, "first_tail_exponent": a,
                         "one_step_drop": first < start,
                         "first_mark": first_mark})
    reset = [reset_witness(r, s) for r in range(1, 13) for s in range(1, 21)]
    threshold = []
    for r in range(1, 13):
        b = 0
        while 2 ** b * 8 ** r < 3 * 9 ** r:
            b += 1
        modulus = 2 ** b
        residue = (7 * pow(27 * 9 ** r, -1, modulus)) % modulus
        require(residue % 2 == 1 and residue > 0, "threshold odd residue")
        for q in range(4):
            t = residue + modulus * q
            endpoint = 18 * t * 9 ** r - 5
            target, _ = step(endpoint)
            require(target < macro(r, t), "optimized threshold sufficient descent")
        threshold.append({"r": r, "b": b, "modulus": modulus,
                          "odd_residue": residue,
                          "conditional_odd_density": str(Fraction(2, modulus))})
    tail_checks = 0
    for r in range(1, 13):
        residue = (9 * pow(9 ** r, -1, 64)) % 64
        q_base = (27 * 9 ** r * residue + 13) // 64
        q_step = 27 * 9 ** r
        for level in range(5):
            modulus = 8 ** level
            root = (-q_base * pow(q_step, -1, modulus)) % modulus
            for size in (1, 2, 8, 64, 257, 4096):
                actual = sum((q_base + q_step * j) % modulus == 0 for j in range(size))
                predicted = 0 if root >= size else 1 + (size - 1 - root) // modulus
                require(actual == predicted, "reset-tail residue count")
                require(size // modulus <= actual <= (size + modulus - 1) // modulus,
                        "reset-tail floor-ceil")
                tail_checks += 1
    return {"status": "PASS", "finite_only": True,
            "domain": {"r": [1, 12], "odd_t": [1, 127], "tail_cap": 64,
                       "reset_s": [1, 20]},
            "summary": {"baseline_cases": len(rows),
                        "one_step_drops": sum(x["one_step_drop"] for x in rows),
                        "unresolved_marks": sum(x["first_mark"] is None for x in rows),
                        "reset_witnesses": len(reset),
                        "clock_increases": sum(x["next_clock"] > x["initial_clock"] for x in reset),
                        "same_clock_cofactor_increases": sum(x["next_clock"] == x["initial_clock"] and x["cofactor_increases"] for x in reset),
                        "exact_reset_tail_profiles": tail_checks},
            "same_clock_example": next(x for x in reset if x["r"] == 9 and x["s"] == 10),
            "threshold_classes": threshold, "baseline": rows, "resets": reset}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], **result["summary"],
                      "same_clock_example": result["same_clock_example"]}, indent=2))
