"""
Rational and 2-adic representatives for expansive primitive phantoms.

This is Phase 7.2 of the Lean TODO roadmap.  It starts from the
primitive cyclic-composition enumeration of ``necklace_counts.py`` and,
for each expansive word w = (a_0, ..., a_{L-1}), computes

    S_w(n) = (3^L n + C_w) / 2^A,
    q_w = C_w / (2^A - 3^L),

with exact rational arithmetic.  The emitted residue is the 2-adic
representative of q_w modulo 2^m, where the default is m = A + 1, the
one-period shadowing modulus used later by the episode graph scripts.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from necklace_counts import enumerate_primitive_necklaces, is_expanding


@dataclass(frozen=True)
class PhantomRepresentative:
    K: int
    L: int
    word: str
    C_w: int
    A: int
    denominator: int
    q_num: int
    q_den: int
    q_decimal: str
    residue_bits: int
    q_mod_2_power: int


def affine_constant(word: tuple[int, ...]) -> tuple[int, int]:
    """Return (C_w, A) for the affine Syracuse block S_w."""
    c = 0
    total_a = 0
    for a in word:
        c = 3 * c + (1 << total_a)
        total_a += a
    return c, total_a


def rational_periodic_point(word: tuple[int, ...]) -> tuple[int, int, Fraction]:
    """Return (C_w, A, q_w), with q_w in lowest terms."""
    c, total_a = affine_constant(word)
    length = len(word)
    denominator = (1 << total_a) - (3**length)
    q = Fraction(c, denominator)
    return c, total_a, q


def rational_mod_power_of_two(q: Fraction, bits: int) -> int:
    """Return the residue of an odd-denominator rational modulo 2^bits."""
    if bits <= 0:
        raise ValueError("bits must be positive")
    modulus = 1 << bits
    den = q.denominator % modulus
    if den % 2 == 0:
        raise ValueError(f"q has even denominator modulo 2^{bits}: {q}")
    return (q.numerator % modulus) * pow(den, -1, modulus) % modulus


def verify_representative(word: tuple[int, ...], c: int, total_a: int, q: Fraction) -> None:
    """Exact sanity checks for the fixed-point equation."""
    length = len(word)
    denominator = (1 << total_a) - (3**length)
    if total_a != sum(word):
        raise AssertionError(f"A mismatch for {word}: {total_a} != {sum(word)}")
    if denominator % 2 == 0:
        raise AssertionError(f"even denominator for {word}: {denominator}")
    if denominator * q != c:
        raise AssertionError(f"fixed-point identity failed for {word}: {denominator} * {q} != {c}")
    image = Fraction((3**length) * q + c, 1 << total_a)
    if image != q:
        raise AssertionError(f"q_w is not fixed by S_w for {word}: {image} != {q}")


def decimal_preview(q: Fraction, digits: int = 12) -> str:
    return f"{float(q):.{digits}g}"


def representative_for_word(
    word: tuple[int, ...],
    residue_bits: int | None,
) -> PhantomRepresentative:
    c, total_a, q = rational_periodic_point(word)
    verify_representative(word, c, total_a, q)
    bits = residue_bits if residue_bits is not None else total_a + 1
    return PhantomRepresentative(
        K=sum(word),
        L=len(word),
        word=" ".join(map(str, word)),
        C_w=c,
        A=total_a,
        denominator=(1 << total_a) - (3 ** len(word)),
        q_num=q.numerator,
        q_den=q.denominator,
        q_decimal=decimal_preview(q),
        residue_bits=bits,
        q_mod_2_power=rational_mod_power_of_two(q, bits),
    )


def expansive_representatives(
    min_K: int,
    max_K: int,
    residue_bits: int | None,
) -> list[PhantomRepresentative]:
    if min_K < 1 or max_K < min_K:
        raise ValueError("require 1 <= min_K <= max_K")

    rows: list[PhantomRepresentative] = []
    for K in range(min_K, max_K + 1):
        for L in range(2, K + 1):
            if not is_expanding(K, L):
                continue
            for word in sorted(enumerate_primitive_necklaces(K, L)):
                rows.append(representative_for_word(word, residue_bits))
    return rows


def write_csv(rows: list[PhantomRepresentative], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-k", type=int, default=3, help="smallest K to enumerate")
    parser.add_argument("--max-k", type=int, default=16, help="largest K to enumerate")
    parser.add_argument(
        "--residue-bits",
        type=int,
        help="fixed modulus exponent m for q_w mod 2^m; defaults per row to A+1",
    )
    parser.add_argument("--csv", type=Path, help="optional CSV output path")
    parser.add_argument("--limit", type=int, help="print only the first N rows")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = expansive_representatives(args.min_k, args.max_k, args.residue_bits)
    if args.csv:
        write_csv(rows, args.csv)

    printable = rows[: args.limit] if args.limit is not None else rows
    print("K,L,word,C_w,A,denominator,q_num,q_den,residue_bits,q_mod_2_power")
    for row in printable:
        print(
            f"{row.K},{row.L},{row.word},{row.C_w},{row.A},{row.denominator},"
            f"{row.q_num},{row.q_den},{row.residue_bits},{row.q_mod_2_power}"
        )
    if args.limit is not None and args.limit < len(rows):
        print(f"... {len(rows) - args.limit} additional row(s) omitted")
    print(f"total_expansive_primitive_representatives={len(rows)}")


if __name__ == "__main__":
    main()
