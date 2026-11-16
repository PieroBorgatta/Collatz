#!/usr/bin/env python3
"""Check the literal finite arithmetic certificates displayed in the v7 paper.

This standard-library checker uses integers and Fraction throughout. It does
not check Lean, parse all LaTeX claims, replay external search certificates,
or establish coverage of any infinite integer orbit. The universal claims
remain the responsibility of the paper proofs and the separately audited
Lean development. Paper hashes bind each report to the inspected source.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


Word = tuple[int, ...]
W1: Word = (1, 2)
V1: Word = (2, 1)
W2: Word = (2, 1, 2)
V2: Word = (1, 1, 3)
W_STAR: Word = (1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1)
G_STAR: Word = (4,) + (1,) * 15 + (2, 2, 1, 4, 3, 3)
MACRO_A: Word = W1 * 4
MACRO_B: Word = W1 * 3 + W2


class VerificationError(ValueError):
    """An exact certificate disagrees with the displayed paper value."""


def require(condition: bool, message: str) -> None:
    # Deliberately not an assert: python -O must not remove a check.
    if not condition:
        raise VerificationError(message)


def equal(actual: Any, expected: Any, label: str) -> None:
    require(actual == expected, f"{label}: got {actual!r}, expected {expected!r}")


def affine(word: Word) -> tuple[int, int, int]:
    """Return P,Q,C for F_word(x)=(P*x+C)/Q, with Q=2**sum(word)."""
    constant = 0
    total = 0
    for gap in word:
        require(type(gap) is int and gap > 0, "word exponents must be positive integers")
        constant = 3 * constant + 2**total
        total += gap
    result = (3 ** len(word), 2**total, constant)

    # Independently compose rational affine steps in their forward order.
    slope, offset = Fraction(1), Fraction(0)
    for gap in word:
        slope = Fraction(3, 2**gap) * slope
        offset = Fraction(3 * offset + 1, 2**gap)
    equal((slope, offset), (Fraction(result[0], result[1]), Fraction(constant, result[1])),
          "integer recurrence versus rational affine composition")
    return result


def gains(word: Word) -> list[Fraction]:
    total = 0
    result = []
    for index, gap in enumerate(word, 1):
        total += gap
        result.append(Fraction(3**index, 2**total))
    return result


def cylinder(word: Word) -> tuple[int, int]:
    """Solve P*x+C == Q (mod 2Q), the final-odd-quotient condition."""
    p, q, c = affine(word)
    modulus = 2 * q
    residue = ((q - c) * pow(p, -1, modulus)) % modulus
    require(residue > 0 and residue % 2 == 1, "a positive odd cylinder representative is required")
    equal((p * residue + c) % modulus, q, "exact odd endpoint congruence")
    return residue, modulus


def trajectory(seed: int, word: Word) -> list[int]:
    require(seed > 0 and seed % 2 == 1, "trajectory seed must be positive odd")
    states = [seed]
    for index, gap in enumerate(word):
        numerator = 3 * states[-1] + 1
        quotient, remainder = divmod(numerator, 2**gap)
        require(remainder == 0 and quotient > 0 and quotient % 2 == 1,
                f"incorrect exact valuation {gap} at step {index}, seed {seed}")
        states.append(quotient)
    p, q, c = affine(word)
    equal(Fraction(p * seed + c, q), states[-1], "trajectory versus affine endpoint")
    return states


def cylinder_certificate(word: Word) -> dict[str, Any]:
    residue, modulus = cylinder(word)
    states = trajectory(residue, word)
    # For every nonnegative integer h, the i-th state of residue+h*modulus
    # differs by this positive even integer times h. Thus every intermediate
    # quotient stays positive odd, not just the representative that we replay.
    for index in range(len(word) + 1):
        p, q, _ = affine(word[:index])
        step = Fraction(p * modulus, q)
        require(step.denominator == 1 and step.numerator > 0 and step.numerator % 2 == 0,
                "cylinder lift must preserve every positive odd intermediate state")
    return {"word": word, "residue": residue, "modulus": modulus,
            "least_endpoint": states[-1], "least_last_parent": states[-2] if word else None}


def serializable(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    return value


def verify() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, **details: Any) -> None:
        checks.append({"name": name, "status": "pass", **details})

    for name, observed, companion, expected in (
        ("paired block 12 to 21", W1, V1, (9, 8, 5, 7, 11, 9, 16)),
        ("paired block 212 to 113", W2, V2, (27, 32, 29, 19, 57, 55, 64)),
    ):
        p, q, cw = affine(observed)
        pv, qv, cv = affine(companion)
        rw, mw = cylinder(observed)
        rv, mv = cylinder(companion)
        equal((p, q, cw, cv, rw, rv, mw), expected, name)
        equal((pv, qv, mv), (p, q, mw), name + " matching length and total")
        equal(cv - cw, -2 * (q - p), name + " translation constant")
        equal(rv, rw - 2, name + " translated exact cylinder")
        observed_cert = cylinder_certificate(observed)
        companion_cert = cylinder_certificate(companion)
        require(rw > 2 and observed_cert["least_endpoint"] > 2,
                name + " positivity guard")
        equal(companion_cert["least_endpoint"], observed_cert["least_endpoint"] - 2,
              name + " translated endpoint")
        record(name, observed=observed_cert, companion=companion_cert,
               affine_constants=[cw, cv])

    equal(Fraction(5, 8 - 9), Fraction(-5), "first observed fixed point")
    equal(Fraction(29, 32 - 27), Fraction(29, 5), "second observed fixed point")
    record("observed block fixed points", W1_fixed_point=-5, W2_fixed_point=Fraction(29, 5))

    pw, qw, cw = affine(W_STAR)
    pg, qg, cg = affine(G_STAR)
    equal((len(W_STAR), sum(W_STAR), len(G_STAR), sum(G_STAR)), (22, 34, 22, 34),
          "terminal word lengths and totals")
    equal((cw, cg), (118309227953, 181071347171), "terminal affine constants")
    equal((pg, qg), (pw, qw), "terminal homogeneous gains")
    equal(cg - cw, 62762119218, "terminal displayed constant difference")
    equal(cg - cw, 2 * 3**22, "terminal merger identity")
    wc, gc = cylinder_certificate(W_STAR), cylinder_certificate(G_STAR)
    equal((gc["residue"], gc["modulus"]), (wc["residue"] - 2, wc["modulus"]),
          "terminal translated legality cylinder")
    equal(wc["least_endpoint"], gc["least_endpoint"], "terminal common endpoint")
    equal((W_STAR[-1], G_STAR[-1]), (1, 3), "terminal last exponents")
    require(wc["least_last_parent"] != gc["least_last_parent"], "terminal last-parent separation")
    record("length-22 terminal merger", observed=wc, companion=gc,
           constants=[cw, cg], difference=cg - cw)

    for label, prefix, partner_prefix, first_gap, expected_gamma in (
        ("prefix W1", W1, V1, 2, Fraction(4, 3)),
        ("prefix W2", W2, V2, 1, Fraction(2, 3)),
        ("empty prefix", (), (), 4, Fraction(16, 3)),
    ):
        observed = prefix + W_STAR
        alternative = partner_prefix + G_STAR
        residue, modulus = cylinder(observed)
        equal(alternative[0], first_gap, label + " first companion exponent")
        gamma = gains(alternative[1:])[-1] / gains(observed)[-1]
        equal(gamma, expected_gamma, label + " stripped relative gain")
        representatives = []
        # Two CRT representatives cover the two unit residue classes modulo 3.
        for unit_class in (1, 2):
            seed = residue + ((unit_class - residue) * pow(modulus, -1, 3) % 3) * modulus
            equal(seed % 3, unit_class, label + " unit CRT class")
            observed_states = trajectory(seed, observed)
            companion_states = trajectory(seed - 2, alternative)
            equal(companion_states[-1], observed_states[-1], label + " mixed merger")
            unit_seed = seed - 2 if unit_class == 1 else companion_states[1]
            require(unit_seed > 0 and unit_seed % 2 == 1 and unit_seed % 3 != 0,
                    label + " repaired unit source")
            if unit_class == 2:
                equal(unit_seed, Fraction(3 * seed - 5, 2**first_gap), label + " repair formula")
            # All further positive seeds in this combined cylinder are
            # seed+3*modulus*h. Their repaired seeds have this exact even
            # increment divisible by three, so unit status is preserved.
            unit_increment = Fraction(3 * modulus) if unit_class == 1 else Fraction(
                9 * modulus, 2**first_gap)
            require(unit_increment.denominator == 1 and unit_increment.numerator % 6 == 0,
                    label + " symbolic unit-cylinder lift")
            if label != "prefix W2":
                require(unit_seed < seed, label + " smaller unit source")
                require(unit_increment <= 3 * modulus, label + " descent preserved along cylinder lift")
            representatives.append({"seed_class_mod_3": unit_class, "seed": seed,
                                    "repaired_unit_seed": unit_seed,
                                    "seed_increment": 3 * modulus,
                                    "repaired_seed_increment": unit_increment})
        record("unit repair: " + label, first_gap=first_gap, stripped_gamma=gamma,
               crt_representatives=representatives)

    for label, word, length, total in (
        ("A", MACRO_A, 8, 12), ("B", MACRO_B, 9, 14), ("w_star", W_STAR, 22, 34)
    ):
        equal((len(word), sum(word)), (length, total), label + " length and total")
        prefix_gains = gains(word)
        require(all(gain > 1 for gain in prefix_gains), label + " strict prefix expansion")
        record("all prefix gains: " + label, minimum=min(prefix_gains), final=prefix_gains[-1])
    equal(min(gains(MACRO_B)), Fraction(2187, 2048), "B minimum prefix gain")
    equal(gains(MACRO_B)[-1], Fraction(19683, 16384), "B total gain")
    equal(min(gains(W_STAR)), Fraction(3**21, 2**33), "terminal minimum prefix gain")
    equal([sum(W_STAR[:i]) for i in range(1, 23)],
          [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 21, 23, 25, 26, 28, 29, 31, 33, 34],
          "terminal displayed prefix totals")
    require(MACRO_A != MACRO_B[:len(MACRO_A)] and MACRO_B != MACRO_A[:len(MACRO_B)],
            "macro pair must be a prefix code")
    require(MACRO_A + MACRO_B != MACRO_B + MACRO_A, "macros must not be powers of a common word")
    record("macro prefix code and distinct word powers")

    block_mass = Fraction(1, 2**3) + Fraction(1, 2**5)
    language_mass = Fraction(1, 2**34) / (1 - block_mass)
    equal(language_mass, Fraction(1, 27 * 2**29), "displayed cylinder-mass geometric value")
    record("finite rational value of the cylinder-mass formula", block_mass=block_mass,
           terminal_mass=Fraction(1, 2**34), geometric_value=language_mass)
    require(9**6 > 16 * 8**5, "collapse-family K=5 expansion threshold")
    record("collapse-family expansion threshold", K=5, gain=Fraction(9**6, 16 * 8**5))

    def high(n: int) -> Fraction:
        return Fraction(5, 4)**n * Fraction(2, 3)**(3 * n // 5)

    def low(n: int) -> Fraction:
        return Fraction(3**(3 * n // 5), 2**n)

    high_ratio, low_ratio = high(5), low(5)
    equal((high_ratio, low_ratio), (Fraction(3125, 3456), Fraction(27, 32)),
          "finite-packing five-band ratios")
    for s in range(5):
        equal(high(5 + s), high_ratio * high(s), "high five-band factorization")
        equal(low(5 + s), low_ratio * low(s), "low five-band factorization")
    high_base, low_base = sum((high(s) for s in range(5)), Fraction(0)), sum(
        (low(s) for s in range(5)), Fraction(0))
    equal((high_base, low_base), (Fraction(3271, 576), Fraction(51, 16)),
          "finite-packing five-band base sums")
    high_bound, low_bound = high_base / (1 - high_ratio), low_base / (1 - low_ratio)
    equal((high_bound, low_bound), (Fraction(19626, 331), Fraction(102, 5)),
          "finite-packing geometric constants")
    total = 2 + high_bound + low_bound - 1
    equal(total, Fraction(133547, 1655), "displayed finite reciprocal constant")
    require(total < 81, "finite reciprocal constant must be strictly smaller than 81")
    equal(Fraction(81, 3), 27, "first-arrival exponential budget coefficient")
    record("finite-packing displayed rational constants", high_ratio=high_ratio, low_ratio=low_ratio,
           high_base=high_base, low_base=low_base, high_bound=high_bound, low_bound=low_bound,
           terminal_error_bound=2, zero_band_saving=1, total=total, upper_bound=81,
           positive_margin=81 - total, exponential_coefficient=27)

    root = Path(__file__).resolve().parents[1]
    sources = {}
    for relative in ("paper/v7_sections/paired_paths.tex", "paper/v7_sections/finite_core.tex"):
        source = root / relative
        require(source.is_file(), f"paper source missing: {relative}")
        sources[relative] = hashlib.sha256(source.read_bytes()).hexdigest()
    return serializable({
        "schema_version": 1,
        "status": "pass",
        "arithmetic": "exact Python integers and fractions.Fraction; no floating-point comparisons",
        "scope": "literal finite arithmetic certificates transcribed from the identified paper sources",
        "limitations": ["not a Lean check", "not an external-certificate replay",
                        "does not parse or prove every LaTeX statement",
                        "no infinite-orbit coverage or global Collatz conclusion"],
        "paper_source_sha256": sources,
        "check_count": len(checks),
        "checks": checks,
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit only a machine-readable JSON report")
    args = parser.parse_args()
    try:
        report = verify()
    except (VerificationError, OSError) as error:
        if args.json:
            print(json.dumps({"schema_version": 1, "status": "fail", "error": str(error)}, indent=2))
        else:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"PASS: {report['check_count']} exact finite arithmetic certificate groups")
        print("Paired blocks, terminal merger, unit repairs, macro prefix gains, and finite-packing constants agree.")
        print("Scope: finite paper arithmetic only; not Lean verification or global orbit coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
