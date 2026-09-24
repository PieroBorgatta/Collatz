#!/usr/bin/env python3
"""Exact finite checks for the post-tower parameter formulas.

The universal arguments are in IDEAS_IT.md. These checks do not prove
Collatz, independence, or descent after the classified next exponent.
Only the Python standard library is needed; no float arithmetic is used.
"""
import argparse
from collections import Counter
import json
from pathlib import Path


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def step(n):
    a = v2(3 * n + 1)
    return (3 * n + 1) >> a, a


def qmod(v, q, bits):
    """Q_v(q) mod 2^bits without constructing the integer 9^(2^v q)."""
    modulus = 1 << (v + 3 + bits)
    numerator = (pow(9, (1 << v) * q, modulus) - 1) % modulus
    assert numerator % (1 << (v + 3)) == 0
    return numerator >> (v + 3)


def lift_root(function, bits):
    """Lift a permutation's zero, checking both children at each level."""
    root = 0
    levels = []
    for j in range(1, bits + 1):
        children = (root, root + (1 << (j - 1)))
        good = [q for q in children if function(q, j) == 0]
        assert len(good) == 1, (j, children, good)
        root = good[0]
        levels.append(root)
    return levels


def theta_roots(bits):
    # 81^theta = 17; order of 81 mod 2^(j+4) is exactly 2^j.
    def residual(t, j):
        return (pow(81, t, 1 << (j + 4)) - 17) % (1 << (j + 4))
    return lift_root(residual, bits)


def check_burst(r, phase):
    if phase == "B":
        assert r % 2 == 0
        v = v2(r)
        q = r >> v
        y = 9 ** (r + 1) - 10
        length = v + 2
        coefficient = v + 4
    else:
        assert phase == "C" and r % 2 == 1
        v = v2(r + 1)
        q = (r + 1) >> v
        y = (9 ** (r + 1) - 5) // 4
        length = v
        coefficient = v
    q_exact = (9 ** ((1 << v) * q) - 1) >> (v + 3)
    assert q_exact % 2 == 1
    n = y
    for _ in range(length):
        nxt, a = step(n)
        assert a == 1 and nxt > n
        n = nxt
    assert n == 2 * 3 ** coefficient * q_exact - 1
    nxt, a = step(n)
    assert a == 1 + v2(3 ** (coefficient + 1) * q_exact - 1)
    assert a >= 2
    assert qmod(v, q, 20) == q_exact % (1 << 20)
    return length, a


def run(max_r, residue_bits, root_bits):
    bursts = Counter()
    for r in range(1, max_r + 1):
        check_burst(r, "B" if r % 2 == 0 else "C")
        bursts["B" if r % 2 == 0 else "C"] += 1

    theta = theta_roots(root_bits)
    phase_a = 0
    # Check every threshold separately against exact integer valuations.
    for t in range((max_r + 1) // 2):
        y = (27 * 81 ** t - 7) // 4
        actual = step(y)[1]
        assert actual == v2(81 ** (t + 1) - 17) - 2
        for j in range(1, min(16, root_bits) + 1):
            assert (actual >= j + 2) == ((t + 1 - theta[j - 1]) % (1 << j) == 0)
        phase_a += 1

    distributions = []
    roots = []
    q1_checks = 0
    for v in range(1, 13):
        for phase in ("B", "C"):
            r = (1 << v) if phase == "B" else (1 << v) - 1
            length, a = check_burst(r, phase)
            assert a == (2 if v % 2 == 0 else 3)
            y = 9 ** (r + 1) - 10 if phase == "B" else (9 ** (r + 1) - 5) // 4
            n = y
            for _ in range(length + 1):
                n, _ = step(n)
                if phase == "B" or v >= 2:
                    assert n > y
            if phase == "B" or v >= 2:
                assert 3 ** (length + 1) > 2 ** (length + a)
            q1_checks += 1
    # Each period is an exhaustive parameter residue calculation, not a
    # random sample. One residue retains valuation >= residue_bits + 1.
    for v in (1, 2, 3, 4, 7, 16, 64, 128):
        image = [qmod(v, q, residue_bits) for q in range(1, 1 << residue_bits, 2)]
        assert sorted(image) == list(range(1, 1 << residue_bits, 2))
        if residue_bits >= 3:
            assert all(value % 8 == 5 * q % 8 for q, value in zip(range(1, 1 << residue_bits, 2), image))
        for phase, exponent in (("B", v + 5), ("C", v + 1)):
            counts = Counter()
            multiplier = pow(3, exponent, 1 << residue_bits)
            for value in image:
                residue = (multiplier * value - 1) % (1 << residue_bits)
                a = 1 + v2(residue) if residue else residue_bits + 1
                counts[str(a) if residue else f">={a}"] += 1
            expected = {str(a): 1 << (residue_bits - a) for a in range(2, residue_bits + 1)}
            expected[f">={residue_bits + 1}"] = 1
            assert dict(counts) == expected
            def residual(q, j):
                return (pow(3, exponent, 1 << j) * qmod(v, q, j) - 1) % (1 << j)
            levels = lift_root(residual, root_bits)
            assert levels[0] == 1
            for q in (1, 3, 5, 7, 17, 101, 65537):
                for j, root in enumerate(levels, 1):
                    assert (residual(q, j) == 0) == ((q - root) % (1 << j) == 0)
            roots.append({"phase": phase, "v": v, "bits": root_bits, "root": str(levels[-1])})
            distributions.append({"phase": phase, "v": v, "counts": expected})

    return {
        "scope": "Finite exact validation; universal proofs on paper, not yet Lean",
        "max_r": max_r,
        "post_tower_bursts_checked": dict(bursts),
        "phase_A_exact_steps_checked": phase_a,
        "q1_subfamilies_checked": q1_checks,
        "residue_bits": residue_bits,
        "root_bits": root_bits,
        "theta_root": str(theta[-1]),
        "residue_distributions": distributions,
        "root_certificates": roots,
        "all_checks_passed": True,
        "not_claimed": ["descent below original seed", "independence along orbits", "Collatz convergence", "absolute mathematical priority"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-r", type=int, default=2048)
    parser.add_argument("--residue-bits", type=int, default=12)
    parser.add_argument("--root-bits", type=int, default=96)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("parameter_results.json"))
    args = parser.parse_args()
    if args.max_r < 1 or args.residue_bits < 2 or args.root_bits < 1:
        parser.error("require max-r >= 1, residue-bits >= 2 and root-bits >= 1")
    result = run(args.max_r, args.residue_bits, args.root_bits)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("residue_distributions", "root_certificates")}, indent=2))


if __name__ == "__main__":
    main()
