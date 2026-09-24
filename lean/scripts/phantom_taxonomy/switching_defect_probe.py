#!/usr/bin/env python3
"""Finite exploratory probe for affine Syracuse label switches.

This checks finitely many representatives of exact first-exponent cylinders.
It is a diagnostic for certificate design, not a proof of global coverage or
of the Collatz conjecture. The affine-root classification itself is exact for
the stated cylinder; sampled valuation counts depend on ``--depth``.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Label:
    d: int
    c: int

    def at(self, n: int) -> int:
        return self.d * n + self.c

    def __str__(self) -> str:
        return f"n+{self.c}" if self.d == 1 else f"{self.d}n+{self.c}"


LABELS = (Label(1, 1), Label(1, 5), Label(1, 7))
ODD_Q = (1, 3, 5)


def v2(n: int) -> int | None:
    """Return the finite 2-adic valuation, or None for zero (infinity)."""
    if n == 0:
        return None
    n = abs(n)
    return (n & -n).bit_length() - 1


def exact_first_exponent_residue(e: int) -> tuple[int, int]:
    """Unique residue r mod 2^(e+1) with 3r+1 = 2^e mod 2^(e+1)."""
    modulus = 1 << (e + 1)
    residue = ((1 << e) - 1) * pow(3, -1, modulus) % modulus
    return residue, modulus


def affine_cylinder_type(slope: int, shift: int, residue: int, bits: int) -> str:
    """Classify v2(slope*n+shift) on n = residue mod 2^bits.

    A nonconstant form has either a constant valuation or one 2-adic root
    inside the cylinder, represented by a unique nested residue tower.
    """
    if slope == 0:
        return "identically zero" if shift == 0 else f"constant v2={v2(shift)}"
    threshold = bits + v2(slope)  # v2(slope) is finite here.
    at_residue = slope * residue + shift
    observed = v2(at_residue)
    if observed is None or observed >= threshold:
        return "root tower"
    return f"constant v2={observed}"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_explicit_family(depth: int) -> list[tuple[int, int, int, int]]:
    """Check the n_k family, including its exact [1] cylinder membership."""
    samples = []
    for k in range(4, 2 * depth + 1, 2):
        numerator = (1 << (k + 1)) - 11
        require(numerator % 3 == 0, f"n_{k} is not integral")
        n = numerator // 3
        m = (3 * n + 1) // 2
        source = n + 1
        defect = 8
        target = m + 5
        require(n > 0 and n % 2 == 1 and n % 4 == 3, f"n_{k} not in [1] cylinder")
        require(v2(3 * n + 1) == 1 and m == (1 << k) - 5, f"wrong first step at k={k}")
        require(2 * target == 3 * source + defect, f"ledger failed at k={k}")
        require(v2(source) == v2(defect) == 3, f"source/defect valuation failed at k={k}")
        require(v2(target) == k, f"unbounded cancellation formula failed at k={k}")
        if n < (1 << depth):
            samples.append((k, n, m, v2(target)))
    return samples


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--depth", type=int, default=12,
        help="enumerate positive representatives n < 2^depth (default: 12; range: 6..18)",
    )
    args = parser.parse_args()
    if not 6 <= args.depth <= 18:
        parser.error("--depth must be between 6 and 18")

    limit = 1 << args.depth
    print(f"Finite exploratory diagnostic: 0 < n < 2^{args.depth}; no global-coverage claim.")
    print("Labels:", ", ".join(map(str, LABELS)), "; odd q:", ODD_Q)
    for e in range(1, 5):
        r, modulus = exact_first_exponent_residue(e)
        bits = e + 1
        require(v2(3 * r + 1) == e, f"incorrect exact residue for exponent {e}")
        counts: Counter[str] = Counter()
        defect_towers = 0
        destination_towers = 0
        max_cancellation_gain = 0
        for source in LABELS:
            for destination in LABELS:
                for q in ODD_Q:
                    slope = 3 * destination.d - q * source.d
                    shift = destination.d + (1 << e) * destination.c - q * source.c
                    defect_type = affine_cylinder_type(slope, shift, r, bits)
                    # The destination numerator is 2^e*F_j(m), affine in n.
                    target_slope = 3 * destination.d
                    target_shift = destination.d + (1 << e) * destination.c
                    target_type = affine_cylinder_type(target_slope, target_shift, r, bits)
                    defect_towers += defect_type == "root tower"
                    destination_towers += target_type == "root tower"

                    for n in range(r, limit, modulus):
                        if n == 0:
                            continue
                        num = 3 * n + 1
                        require(v2(num) == e, f"nonexact sample n={n}, e={e}")
                        m = num // (1 << e)
                        initial = source.at(n)
                        final = destination.at(m)
                        defect = slope * n + shift
                        require(
                            (1 << e) * final == q * initial + defect,
                            f"affine identity failed at n={n}, e={e}",
                        )
                        a, b = v2(initial), v2(defect)
                        final_scaled_valuation = v2(final) + e
                        if b is None or a < b:
                            counts["source lower"] += 1
                            require(final_scaled_valuation == a, "source-lower tax failed")
                        elif b < a:
                            counts["defect lower"] += 1
                            require(final_scaled_valuation == b, "defect-lower tax failed")
                        else:
                            counts["equal/cancellation"] += 1
                            gain = final_scaled_valuation - a
                            require(gain >= 1, "equal-valuation cancellation failed")
                            max_cancellation_gain = max(max_cancellation_gain, gain)

        print(
            f"e={e}, exact n≡{r} (mod {modulus}): "
            f"source-lower={counts['source lower']}, "
            f"defect-lower={counts['defect lower']}, "
            f"equal/cancellation={counts['equal/cancellation']}; "
            f"max sampled cancellation gain={max_cancellation_gain}; "
            f"defect root towers={defect_towers}/27, "
            f"destination root towers={destination_towers}/27"
        )

    source, destination, q, e = Label(1, 1), Label(1, 5), 3, 1
    r, modulus = exact_first_exponent_residue(e)
    slope = 3 * destination.d - q * source.d
    shift = destination.d + (1 << e) * destination.c - q * source.c
    print("Critical fixed-cylinder switch:")
    print(
        f"  [1]: n≡{r} (mod {modulus}); {source} -> {destination}, q={q}; "
        f"E(n)={shift if slope == 0 else f'{slope}n+{shift}'} "
        f"({affine_cylinder_type(slope, shift, r, e + 1)})."
    )
    print(
        "  pulled-back destination numerator 2*(m+5)=3n+11: "
        f"{affine_cylinder_type(3, 11, r, e + 1)}."
    )
    samples = check_explicit_family(args.depth)
    print("  self-checked n_k=(2^(k+1)-11)/3 for every even 4<=k<=2*depth.")
    print(
        "  samples within enumeration: "
        + ", ".join(f"k={k}: n={n}, m={m}, v2(m+5)={p}" for k, n, m, p in samples)
    )
    print("Interpretation: bounded defect valuation alone cannot bound destination precision.")


if __name__ == "__main__":
    main()
