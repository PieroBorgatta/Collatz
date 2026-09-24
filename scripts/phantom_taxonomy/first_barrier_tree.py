#!/usr/bin/env python3
"""
Small exact audit of the real/2-adic first-barrier criterion.

This enumerates exponent words, not starting integers or sampled orbits.
For a word w it computes

    3^k*n + C_w = 2^S*T_w(n)

and the unique least residue r in [0, 2^(S+1)) satisfying

    3^k*r + C_w = 2^S  (mod 2^(S+1)).

When D_w = 2^S - 3^k is positive, any matched source whose endpoint has
not dropped must satisfy

    D_w*n <= C_w.

Since n = r + t*2^(S+1), this either excludes the whole cylinder or leaves
an explicitly finite set of possible sources.

The exponent alphabet is handled without an arbitrary cap.  After a
computable threshold, D_w > C_w, so every larger next exponent is excluded
for every positive residue.  The search below is deliberately shallow and
is used only to identify structural survivor families.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log2


@dataclass(frozen=True)
class WordState:
    word: tuple[int, ...]
    power_three: int
    constant: int
    power_two: int

    @staticmethod
    def root() -> "WordState":
        return WordState((), 1, 0, 1)

    def extend(self, exponent: int) -> "WordState":
        if exponent <= 0:
            raise ValueError("accelerated exponents must be positive")
        return WordState(
            self.word + (exponent,),
            3 * self.power_three,
            3 * self.constant + self.power_two,
            self.power_two << exponent,
        )

    @property
    def modulus(self) -> int:
        return 2 * self.power_two

    @property
    def residue(self) -> int:
        target = (self.power_two - self.constant) % self.modulus
        return (target * pow(self.power_three, -1, self.modulus)) % self.modulus

    @property
    def denominator(self) -> int:
        return self.power_two - self.power_three

    @property
    def contracting(self) -> bool:
        return self.denominator > 0

    @property
    def finite_nondrop_source_count(self) -> int:
        """Number of sources allowed by the exact non-drop inequality."""
        if not self.contracting:
            raise ValueError("a noncontracting prefix has no finite barrier")
        residue = self.residue
        denominator = self.denominator
        if denominator * residue > self.constant:
            return 0
        return (self.constant - denominator * residue) // (
            denominator * self.modulus
        ) + 1

    def first_finite_nondrop_sources(self, limit: int = 5) -> tuple[int, ...]:
        count = self.finite_nondrop_source_count
        return tuple(
            self.residue + lift * self.modulus
            for lift in range(min(count, limit))
        )

    def largest_child_not_universally_closed(self) -> int:
        """
        Largest exponent a for which the child can have D <= C.

        Every larger a has D > C and is therefore closed for all positive
        exact residues.  Zero means that every positive-exponent child is
        universally closed.
        """
        right = (
            3 * self.power_three
            + 3 * self.constant
            + self.power_two
        )
        exponent = 0
        scaled = self.power_two
        while 2 * scaled <= right:
            scaled *= 2
            exponent += 1
        return exponent


def follows_word(source: int, word: tuple[int, ...]) -> bool:
    """Exact self-check of the residue formula on one representative."""
    value = source
    for exponent in word:
        numerator = 3 * value + 1
        if numerator % (1 << exponent) != 0:
            return False
        quotient = numerator >> exponent
        if quotient % 2 != 1:
            return False
        value = quotient
    return True


def audit(max_depth: int = 14) -> dict[str, object]:
    frontier = [WordState.root()]
    depth_rows: list[dict[str, int]] = []
    finite_buckets: list[
        tuple[tuple[int, ...], int, tuple[int, ...]]
    ] = []
    near_misses: list[
        tuple[Fraction, int, tuple[int, ...], int, int, int]
    ] = []
    maximum_finite_bucket = 0

    for depth in range(1, max_depth + 1):
        next_frontier: list[WordState] = []
        tested_children = 0
        universally_closed_tails = 0
        closed_cylinders = 0
        finite_cylinders = 0

        for state in frontier:
            largest = state.largest_child_not_universally_closed()
            universally_closed_tails += 1
            for exponent in range(1, largest + 1):
                child = state.extend(exponent)
                tested_children += 1
                assert child.residue % 2 == 1
                assert follows_word(child.residue, child.word)

                if not child.contracting:
                    next_frontier.append(child)
                    continue

                source_count = child.finite_nondrop_source_count
                if source_count == 0:
                    closed_cylinders += 1
                    margin = (
                        child.denominator * child.residue
                        - child.constant
                    )
                    near_misses.append(
                        (
                            Fraction(margin, child.constant),
                            margin,
                            child.word,
                            child.denominator,
                            child.constant,
                            child.residue,
                        )
                    )
                    continue

                finite_cylinders += 1
                maximum_finite_bucket = max(
                    maximum_finite_bucket,
                    source_count,
                )
                if len(finite_buckets) < 24:
                    finite_buckets.append(
                        (
                            child.word,
                            source_count,
                            child.first_finite_nondrop_sources(),
                        )
                    )

        depth_rows.append(
            {
                "depth": depth,
                "open_noncontracting": len(next_frontier),
                "tested_children": tested_children,
                "closed_cylinders": closed_cylinders,
                "finite_cylinders": finite_cylinders,
                "analytic_large_exponent_tails": universally_closed_tails,
            }
        )
        frontier = next_frontier

    max_open_residue = max((state.residue for state in frontier), default=0)
    min_open_residue = min((state.residue for state in frontier), default=0)
    critical_ratios = sorted(
        (
            sum(state.word) / len(state.word),
            state.word,
            state.residue,
        )
        for state in frontier
    )[:12]
    near_misses.sort()

    return {
        "max_depth": max_depth,
        "critical_slope": log2(3),
        "depth_rows": depth_rows,
        "finite_buckets": finite_buckets,
        "maximum_finite_bucket": maximum_finite_bucket,
        "final_open_count": len(frontier),
        "final_open_min_residue": min_open_residue,
        "final_open_max_residue": max_open_residue,
        "lowest_final_slopes": critical_ratios,
        "near_misses": near_misses[:12],
    }


def main() -> None:
    result = audit()
    print("first_barrier_tree=ok")
    print("integer_orbit_samples=0")
    print(f"critical_slope={result['critical_slope']:.12f}")
    for row in result["depth_rows"]:
        print(
            "depth={depth} open={open_noncontracting} "
            "tested={tested_children} closed={closed_cylinders} "
            "finite={finite_cylinders} analytic_tails="
            "{analytic_large_exponent_tails}".format(**row)
        )
    print(
        "finite_bucket_max="
        f"{result['maximum_finite_bucket']}"
    )
    print(
        "final_open_residue_range="
        f"{result['final_open_min_residue']}.."
        f"{result['final_open_max_residue']}"
    )
    print("finite_examples=")
    for word, count, sources in result["finite_buckets"][:12]:
        print(f"  word={word} count={count} first_sources={sources}")
    print("lowest_final_slopes=")
    for slope, word, residue in result["lowest_final_slopes"][:8]:
        print(f"  slope={slope:.6f} word={word} residue={residue}")
    print("closest_closed_cylinders=")
    for ratio, margin, word, denominator, constant, residue in result[
        "near_misses"
    ][:8]:
        print(
            f"  ratio={float(ratio):.9g} margin={margin} "
            f"word={word} D={denominator} C={constant} r={residue}"
        )


if __name__ == "__main__":
    main()
