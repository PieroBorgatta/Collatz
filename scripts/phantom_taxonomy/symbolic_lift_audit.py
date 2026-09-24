#!/usr/bin/env python3
"""
Exact symbolic audit of the unstable K16 residue cell t = 0 (mod 16).

The script does not enumerate a range of lift parameters.  For an affine
family x(u) = base + coefficient*u and every monitored q = p/d, it factors

    d*x(u) - p

at the common power of two in `coefficient`.  Eligibility is then either
constant or one exactly solved linear congruence modulo a power of two.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from orbit_harness import (
    Representative,
    best_hit,
    build_monitors,
    odd_syracuse_step,
    read_representatives,
)


REPRESENTATIVES = Path(__file__).with_name("phantom_representatives_k3_16.csv")

SOURCE_KEY = "K10:L7:w1-1-1-1-1-1-4"
SOURCE_SHADOW_KEY = "K16:L12:w1-1-1-1-1-1-4-1-1-1-1-2"
DEST_K9_KEY = "K9:L6:w1-1-1-1-1-4"
DEST_K15_KEY = "K15:L11:w1-1-1-1-1-4-1-1-1-1-2"
DEST_K16_KEY = "K16:L11:w1-1-1-1-1-4-1-1-1-1-3"


@dataclass(frozen=True)
class AffineFamily:
    name: str
    base: int
    coefficient: int

    @property
    def common_v2(self) -> int:
        return v2(self.coefficient)


@dataclass(frozen=True)
class Candidate:
    key: str
    A: int
    common_v2: int
    scaled_constant: int | None
    scaled_coefficient: int | None
    eligibility_bits: int | None
    eligibility_residue: int | None
    constant_valuation: int | None

    @property
    def is_variable(self) -> bool:
        return self.scaled_constant is not None


def v2(value: int) -> int:
    """Two-adic valuation of a nonzero integer."""
    if value == 0:
        raise ValueError("v2(0) is not used in this finite rational audit")
    value = abs(value)
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return exponent


def root_residue(constant: int, odd_coefficient: int, bits: int) -> int:
    """Unique u modulo 2^bits with constant + odd_coefficient*u = 0."""
    if bits < 0:
        raise ValueError("bits must be nonnegative")
    if odd_coefficient % 2 == 0:
        raise ValueError("coefficient must be odd")
    if bits == 0:
        return 0
    modulus = 1 << bits
    return (-constant * pow(odd_coefficient, -1, modulus)) % modulus


def candidate_for(
    representative: Representative,
    family: AffineFamily,
) -> Candidate | None:
    """
    Return the exact eligibility description, or None if never eligible.

    A monitor with word sum A needs valuation at least A+1.
    """
    denominator = representative.q.denominator
    numerator = representative.q.numerator
    constant = denominator * family.base - numerator
    coefficient = denominator * family.coefficient
    s = family.common_v2
    assert v2(coefficient) == s

    constant_v2 = v2(constant)
    threshold = representative.A + 1
    if constant_v2 < s:
        if constant_v2 < threshold:
            return None
        return Candidate(
            key=representative.key,
            A=representative.A,
            common_v2=s,
            scaled_constant=None,
            scaled_coefficient=None,
            eligibility_bits=None,
            eligibility_residue=None,
            constant_valuation=constant_v2,
        )

    scaled_constant = constant >> s
    scaled_coefficient = coefficient >> s
    assert scaled_coefficient % 2 == 1
    eligibility_bits = max(threshold - s, 0)
    eligibility_residue = root_residue(
        scaled_constant,
        scaled_coefficient,
        eligibility_bits,
    )
    return Candidate(
        key=representative.key,
        A=representative.A,
        common_v2=s,
        scaled_constant=scaled_constant,
        scaled_coefficient=scaled_coefficient,
        eligibility_bits=eligibility_bits,
        eligibility_residue=eligibility_residue,
        constant_valuation=None,
    )


def candidates_for(
    representatives: list[Representative],
    family: AffineFamily,
) -> list[Candidate]:
    return [
        candidate
        for representative in representatives
        if (candidate := candidate_for(representative, family)) is not None
    ]


def variable_signature(candidate: Candidate) -> tuple[int, int, int, int]:
    assert candidate.scaled_constant is not None
    assert candidate.scaled_coefficient is not None
    assert candidate.eligibility_bits is not None
    assert candidate.eligibility_residue is not None
    return (
        candidate.scaled_constant,
        candidate.scaled_coefficient,
        candidate.eligibility_bits,
        candidate.eligibility_residue,
    )


def hit_signature(hit: tuple[Representative, int, int]) -> tuple[str, int, int]:
    representative, b, valuation = hit
    return representative.key, b, valuation


def main() -> None:
    representatives = read_representatives(REPRESENTATIVES, max_K=16)
    assert len(representatives) == 1247

    source = AffineFamily("source", base=1407, coefficient=1 << 15)
    destination = AffineFamily(
        "one_step_destination",
        base=2111,
        coefficient=3 * (1 << 14),
    )

    source_candidates = candidates_for(representatives, source)
    destination_candidates = candidates_for(representatives, destination)

    source_by_key = {candidate.key: candidate for candidate in source_candidates}
    destination_by_key = {
        candidate.key: candidate for candidate in destination_candidates
    }

    assert set(source_by_key) == {SOURCE_KEY, SOURCE_SHADOW_KEY}
    assert set(destination_by_key) == {
        DEST_K9_KEY,
        DEST_K15_KEY,
        DEST_K16_KEY,
    }

    assert variable_signature(source_by_key[SOURCE_KEY]) == (50, 1163, 0, 0)
    assert variable_signature(source_by_key[SOURCE_SHADOW_KEY]) == (
        20027,
        465905,
        2,
        1,
    )
    assert variable_signature(destination_by_key[DEST_K9_KEY]) == (4, 93, 0, 0)
    assert variable_signature(destination_by_key[DEST_K15_KEY]) == (
        18619,
        433137,
        2,
        1,
    )
    assert variable_signature(destination_by_key[DEST_K16_KEY]) == (
        14397,
        334833,
        3,
        3,
    )

    # Exact threshold cylinders used in the note.
    assert root_residue(50, 1163, 2) == 2
    assert root_residue(50, 1163, 6) == 42
    assert root_residue(4, 93, 5) == 12
    assert root_residue(14397, 334833, 19) == 287475

    # The competing destination cylinders are disjoint, and on both the
    # baseline K9 scaled form is odd.
    assert {1, 5}.isdisjoint({3})
    assert (4 + 93 * 1) % 2 == 1
    assert (4 + 93 * 3) % 2 == 1

    _, monitors_by_bits = build_monitors(representatives)
    expected_examples = {
        0: ((SOURCE_KEY, 1, 16), (DEST_K9_KEY, 1, 16)),
        1: ((SOURCE_SHADOW_KEY, 1, 17), (DEST_K15_KEY, 1, 16)),
        3: ((SOURCE_KEY, 1, 15), (DEST_K16_KEY, 1, 18)),
        12: ((SOURCE_KEY, 1, 16), (DEST_K9_KEY, 2, 19)),
        42: ((SOURCE_KEY, 2, 23), (DEST_K9_KEY, 1, 15)),
    }
    for u, (expected_source, expected_destination) in expected_examples.items():
        n = source.base + source.coefficient * u
        exponent, y = odd_syracuse_step(n)
        assert exponent == 1
        assert y == destination.base + destination.coefficient * u
        source_hit = best_hit(n, monitors_by_bits)
        destination_hit = best_hit(y, monitors_by_bits)
        assert source_hit is not None
        assert destination_hit is not None
        assert hit_signature(source_hit) == expected_source
        assert hit_signature(destination_hit) == expected_destination

    print(f"loaded_monitors={len(representatives)}")
    print("source_candidates=2")
    for candidate in source_candidates:
        print(f"  {candidate.key}: {variable_signature(candidate)}")
    print("destination_candidates=3")
    for candidate in destination_candidates:
        print(f"  {candidate.key}: {variable_signature(candidate)}")
    print("canonical_source=not(u=1 mod 4) and not(u=42 mod 64)")
    print("canonical_destination=u=3 mod 8 -> K16; otherwise -> K9")
    print("fixed_examples=5")
    print("symbolic_audit=ok")


if __name__ == "__main__":
    main()
