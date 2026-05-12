"""
Primitive cyclic-composition counts for Phase 7.1.

The object counted here is a primitive cyclic composition of weight K
and length ell: a cyclic orbit of positive integer words

    (k_1, ..., k_ell),  k_i >= 1,  sum k_i = K,

whose least rotational period is ell.

The closed form is the standard Mobius inversion of necklace counts:

    M(K, ell) = 1/ell * sum_{d | gcd(K, ell)}
                    mu(d) * binom(K/d - 1, ell/d - 1).

For small K the script also enumerates compositions directly and checks
that the brute-force canonical-necklace count matches the formula.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path


LOG2_3 = math.log2(3)

# Chang, arXiv:2603.11066v6, Table 2: exact R(K) values displayed
# rounded to four significant figures for K = 3, ..., 20.
CHANG_TABLE2_R_SCI = {
    3: "1.062e-2",
    4: "1.573e-2",
    5: "1.047e-2",
    6: "8.670e-3",
    7: "7.603e-3",
    8: "4.676e-3",
    9: "4.730e-3",
    10: "3.604e-3",
    11: "2.858e-3",
    12: "2.526e-3",
    13: "2.065e-3",
    14: "1.727e-3",
    15: "1.548e-3",
    16: "1.218e-3",
    17: "1.128e-3",
    18: "9.702e-4",
    19: "7.819e-4",
    20: "7.495e-4",
}


@dataclass(frozen=True)
class CountRow:
    K: int
    ell: int
    count: int
    expanding: bool


def divisors(n: int) -> list[int]:
    """Return the positive divisors of n in increasing order."""
    if n <= 0:
        raise ValueError("n must be positive")
    small: list[int] = []
    large: list[int] = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def mobius(n: int) -> int:
    """Return the Mobius function mu(n)."""
    if n <= 0:
        raise ValueError("n must be positive")
    x = n
    primes = 0
    p = 2
    while p * p <= x:
        if x % p == 0:
            multiplicity = 0
            while x % p == 0:
                x //= p
                multiplicity += 1
            if multiplicity > 1:
                return 0
            primes += 1
        p += 1 if p == 2 else 2
    if x > 1:
        primes += 1
    return -1 if primes % 2 else 1


def primitive_necklace_count(K: int, ell: int) -> int:
    """Count primitive cyclic compositions of weight K and length ell."""
    if K < 0 or ell < 0:
        raise ValueError("K and ell must be nonnegative")
    if ell < 2 or ell > K:
        return 0
    total = 0
    for d in divisors(math.gcd(K, ell)):
        total += mobius(d) * math.comb(K // d - 1, ell // d - 1)
    count, remainder = divmod(total, ell)
    if remainder != 0:
        raise ArithmeticError(f"nonintegral count for K={K}, ell={ell}")
    return count


def compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    """Yield all positive compositions of total into parts parts."""
    if parts == 0:
        if total == 0:
            yield ()
        return
    if parts == 1:
        if total >= 1:
            yield (total,)
        return
    for head in range(1, total - parts + 2):
        for tail in compositions(total - head, parts - 1):
            yield (head, *tail)


def rotations(word: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
    for i in range(len(word)):
        yield word[i:] + word[:i]


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotations(word))


def is_primitive_word(word: tuple[int, ...]) -> bool:
    """True iff word has full rotational period."""
    n = len(word)
    for period in divisors(n):
        if period == n:
            continue
        if n % period == 0 and all(word[i] == word[i % period] for i in range(n)):
            return False
    return True


def enumerate_primitive_necklaces(K: int, ell: int) -> set[tuple[int, ...]]:
    """Brute-force primitive cyclic compositions, represented canonically."""
    necklaces: set[tuple[int, ...]] = set()
    for word in compositions(K, ell):
        if is_primitive_word(word):
            necklaces.add(canonical_rotation(word))
    return necklaces


def is_expanding(K: int, ell: int) -> bool:
    """The phantom drift condition ell * log2(3) - K > 0."""
    return ell * LOG2_3 > K


def count_rows(max_K: int) -> list[CountRow]:
    rows: list[CountRow] = []
    for K in range(3, max_K + 1):
        for ell in range(2, K + 1):
            count = primitive_necklace_count(K, ell)
            rows.append(CountRow(K=K, ell=ell, count=count, expanding=is_expanding(K, ell)))
    return rows


def R_of_K(K: int) -> float:
    total = 0.0
    for ell in range(2, K + 1):
        if is_expanding(K, ell):
            total += primitive_necklace_count(K, ell) * (LOG2_3 - K / ell)
    return math.ldexp(total, -K)


def summarize(max_K: int) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for K in range(3, max_K + 1):
        total = 0
        expanding = 0
        by_ell: list[str] = []
        for ell in range(2, K + 1):
            count = primitive_necklace_count(K, ell)
            total += count
            if is_expanding(K, ell):
                expanding += count
            if count:
                by_ell.append(f"{ell}:{count}")
        out.append(
            {
                "K": K,
                "M_total": total,
                "M_expanding": expanding,
                "R_K": f"{R_of_K(K):.12g}",
                "M_by_ell": " ".join(by_ell),
            }
        )
    return out


def rounded_table_value(x: float) -> str:
    """Format like the scientific notation printed in Chang Table 2."""
    return f"{x:.3e}".replace("e-0", "e-").replace("e+0", "e+")


def verify_direct(max_K: int) -> None:
    for K in range(3, max_K + 1):
        for ell in range(2, K + 1):
            formula = primitive_necklace_count(K, ell)
            direct = len(enumerate_primitive_necklaces(K, ell))
            if formula != direct:
                raise AssertionError(
                    f"direct mismatch for K={K}, ell={ell}: formula={formula}, direct={direct}"
                )


def verify_chang_table2() -> None:
    for K, expected in CHANG_TABLE2_R_SCI.items():
        actual = rounded_table_value(R_of_K(K))
        if actual != expected:
            raise AssertionError(f"Chang Table 2 mismatch for K={K}: {actual} != {expected}")


def write_csv(rows: Iterable[dict[str, object]], path: Path) -> None:
    materialized = list(rows)
    if not materialized:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(materialized[0].keys()))
        writer.writeheader()
        writer.writerows(materialized)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, default=20, help="largest K to print")
    parser.add_argument(
        "--verify-direct",
        type=int,
        default=10,
        metavar="K",
        help="brute-force check formula for all 3 <= K <= this value",
    )
    parser.add_argument(
        "--skip-chang-table-check",
        action="store_true",
        help="do not compare R(K), K=3..20, with Chang Table 2 rounded values",
    )
    parser.add_argument("--csv", type=Path, help="optional summary CSV output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_k < 3:
        raise SystemExit("--max-k must be at least 3")
    if args.verify_direct:
        verify_direct(args.verify_direct)
    if not args.skip_chang_table_check:
        verify_chang_table2()

    rows = summarize(args.max_k)
    if args.csv:
        write_csv(rows, args.csv)

    print("K,M_total,M_expanding,R_K,M_by_ell")
    for row in rows:
        print(
            f"{row['K']},{row['M_total']},{row['M_expanding']},"
            f"{row['R_K']},{row['M_by_ell']}"
        )


if __name__ == "__main__":
    main()
