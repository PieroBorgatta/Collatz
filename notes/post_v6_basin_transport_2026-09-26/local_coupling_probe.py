#!/usr/bin/env python3
"""Exact inverse-tree checks; no source census or density estimation.

The tables are finite checks. The uniform obstruction is proved separately
in local_coupling_IT.md, rather than inferred from these finite tables.
AI-assisted development: Codex with Piero Borgatta, 2026-09-26.
"""
import argparse
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


UNITS = (1, 2, 4, 5, 7, 8)
EXPONENTS = {
    r: tuple(a for a in range(1, 7) if pow(2, a, 9) * r % 9 in (4, 7))
    for r in UNITS
}
SMALL_CLOSED = (1, 3, 5, 7, 9, 13, 19)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse(n, a):
    if n == 0 or n % 2 == 0 or a < 1:
        raise ValueError("inverse requires a nonzero odd target and a positive exponent")
    numerator = (1 << a) * n - 1
    if numerator % 3:
        raise ValueError("nonintegral inverse branch")
    child = numerator // 3
    require(child % 2 == 1 and child != 0, "inverse child must be nonzero odd")
    return child


def sibling(n):
    if n <= 1 or n % 2 == 0 or n % 3 == 0:
        raise ValueError("sibling target must be odd >1 and prime to 3")
    return 4 * n + 1 if n % 3 == 1 else 16 * n + 5


def ordinary_odd_part(n):
    if n <= 0:
        raise ValueError("positive numerator required")
    return n // (n & -n)


def minus_step(q):
    if q < 1 or q % 2 == 0:
        raise ValueError("minus map requires a positive odd integer")
    return ordinary_odd_part(3 * q - 1)


def odd_representative(r, modulus):
    n = r
    while n <= 1 or n % 2 == 0:
        n += modulus
    return n


def fraction_record(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def rank_tables():
    mod9 = []
    for r in UNITS:
        n = odd_representative(r, 9)
        s = sibling(n) % 9
        mod9.append({"n_mod9": r, "h_mod9": s,
                     "a": EXPONENTS[r], "b": EXPONENTS[s],
                     "b_minus_a": [b - a for a, b in zip(EXPONENTS[r], EXPONENTS[s])]})
    mod27 = []
    for r in range(1, 27):
        if r % 3 == 0:
            continue
        n = odd_representative(r, 27)
        y = sibling(n)
        for rank, (a, b) in enumerate(zip(EXPONENTS[n % 9], EXPONENTS[y % 9])):
            u, v = inverse(n, a), inverse(y, b)
            require(u % 3 and v % 3, "rank branch must remain continuable")
            mod27.append({"n_mod27": r, "h_mod27": y % 27, "rank": rank,
                          "a": a, "b": b, "b_minus_a": b - a,
                          "child_pair_mod9": [u % 9, v % 9]})
    return mod9, mod27


def quotient_positive_self_loops():
    """Independent parent lifts: these edges are only a quotient model."""
    rows = []
    for r, s, rank, p, q in product(UNITS, UNITS, range(2), range(3), range(3)):
        a, b = EXPONENTS[r][rank], EXPONENTS[s][rank]
        n, y = odd_representative(r + 9 * p, 27), odd_representative(s + 9 * q, 27)
        if (inverse(n, a) % 9, inverse(y, b) % 9) == (r, s) and b > a:
            rows.append({"state_mod9": [r, s], "rank": rank, "a": a, "b": b,
                         "cost": b - a, "parent_lifts_mod27": [n % 27, y % 27],
                         "compatible_with_initial_h_mod27": sibling(n) % 27 == y % 27})
    require(len(rows) == 6, "unexpected quotient loop count")
    require(not any(row["compatible_with_initial_h_mod27"] for row in rows),
            "initial sibling compatibility of quotient loops changed")
    return rows


def finite_rank_tree(depth=14):
    """Only the first two children (exponents 1..6), not all inverse branches."""
    roots = (19, 11, 13, 5, 7, 17)
    states = [(n, sibling(n), 0, n, (), ()) for n in roots]
    rows = []
    for k in range(1, depth + 1):
        next_states = []
        for n, y, loss, root, lower_word, upper_word in states:
            for a, b in zip(EXPONENTS[n % 9], EXPONENTS[y % 9]):
                u, v = inverse(n, a), inverse(y, b)
                require(u > 0 and v > 0 and u % 3 and v % 3,
                        "positive continuable rank tree")
                next_states.append((u, v, loss + b - a, root,
                                    lower_word + (a,), upper_word + (b,)))
        states = next_states
        require(len(states) == len(roots) * 2 ** k, "finite word enumeration incomplete")
        if k in (1, 2, 4, 8, 12, 14):
            worst = max(states, key=lambda z: Fraction(z[1], z[0]))
            rows.append({"depth": k, "words_counted_with_multiplicity": len(states),
                         "minimum_exponent_loss": min(z[2] for z in states),
                         "maximum_exponent_loss": max(z[2] for z in states),
                         "maximum_height_ratio": fraction_record(Fraction(worst[1], worst[0])),
                         "witness_root": worst[3], "witness_lower_endpoint": worst[0],
                         "witness_upper_endpoint": worst[1],
                         "witness_lower_word": worst[4], "witness_upper_word": worst[5]})
    return rows


def obstruction_witness(k, t=1):
    """One actual positive witness, using the rank-zero upper word.

    The accompanying proof covers every valid upper word of length k.
    This routine checks that proof's identities on one explicit word.
    """
    if k < 0 or t < 1:
        raise ValueError("nonnegative depth and positive t required")
    n = 2 * t * 3 ** (k + 2) - 1
    y = sibling(n)
    u, v, negative, B, word = n, y, -11, 0, []
    for i in range(1, k + 1):
        b = EXPONENTS[negative % 9][0]
        require(EXPONENTS[u % 9][0] == 1 and EXPONENTS[v % 9][0] == b,
                "real rank coupling does not match the negative branch")
        u, v, negative = inverse(u, 1), inverse(v, b), inverse(negative, b)
        B += b
        word.append(b)
        q = -negative
        require(q >= 11 and minus_step(q) >= 1, "negative ancestor lower bound")
        require(v == 32 * t * 3 ** (k + 2 - i) * 2 ** B - q,
                "exact positive/negative lift identity")
        require(u == 2 ** (i + 1) * t * 3 ** (k + 2 - i) - 1,
                "exact lower inverse identity")
        require(q <= 11 * 2 ** (B - i), "negative ancestor upper bound")
    require(2 ** B * 23 ** k >= 66 ** k, "exponent growth inequality")
    require(v > 16 * 2 ** (B - k) * u, "height comparison before exponential bound")
    require(v * 23 ** k > 16 * u * 33 ** k, "uniform depth obstruction")
    return {"depth": k, "t": t, "n": n, "h_n": y, "lower_endpoint": u,
            "upper_endpoint": v, "upper_word": word, "upper_sum": B,
            "exponent_loss": B - k, "negative_endpoint_modulus": -negative,
            "height_ratio": fraction_record(Fraction(v, u)),
            "strict_lower_bound": fraction_record(16 * Fraction(33, 23) ** k)}


def all_short_upper_words():
    """Finite check including noncontinuable leaves, unlike the rank tree."""
    rows = []
    for k, t in product(range(1, 6), (1, 2)):
        n = 2 * t * 3 ** (k + 2) - 1
        u = 18 * t * 2 ** k - 1
        states = [(sibling(n), 0)]
        for _ in range(k):
            next_states = []
            for parent, B in states:
                for b in range(1, 7):
                    if ((1 << b) * parent - 1) % 3 == 0:
                        next_states.append((inverse(parent, b), B + b))
            states = next_states
        require(len(states) == 3 * 2 ** (k - 1), "short upper-word enumeration incomplete")
        for v, B in states:
            q = 288 * t * 2 ** B - v
            require(q >= 11 and q % 2 == 1, "short upper-word negative ancestor")
            require(v * 23 ** k > 16 * u * 33 ** k, "short upper-word depth bound")
        leaves = sum(v % 3 == 0 for v, _ in states)
        require(leaves == 2 ** (k - 1), "noncontinuable endpoints not covered")
        rows.append({"depth": k, "t": t, "allowed_exponents_checked": [1, 2, 3, 4, 5, 6],
                     "integer_words": len(states), "noncontinuable_endpoints": leaves})
    return rows


def run():
    closed = {q: minus_step(q) for q in SMALL_CLOSED}
    require(all(target in SMALL_CLOSED for target in closed.values()), "small set is not closed")
    require(11 not in SMALL_CLOSED, "closed set contains the obstruction seed")
    mod9, mod27 = rank_tables()
    witnesses = [obstruction_witness(k) for k in (0, 1, 2, 4, 8, 16, 32, 64)]
    terminating = []
    for k in range(5):
        p = k + 2
        require(pow(2, 3 ** p, 3 ** (p + 1)) == 3 ** (p + 1) - 1,
                "terminating family modular identity")
        t = (2 ** (3 ** p) + 1) // 3 ** (p + 1)
        row = obstruction_witness(k, t)
        require(ordinary_odd_part(3 * row["n"] + 1) == 1,
                "lower target does not immediately reach 1")
        require(ordinary_odd_part(3 * row["h_n"] + 1) == 1,
                "upper target does not immediately reach 1")
        row["both_targets_reach_1_in_one_step"] = True
        terminating.append(row)
    return {"source_census_performed": False, "density_claim": False,
            "finite_checks_are_not_the_uniform_proof": True,
            "admissible_exponents_mod6": EXPONENTS,
            "sibling_table_mod9": mod9, "sibling_transitions_mod27": mod27,
            "quotient_positive_self_loops_not_initially_compatible": quotient_positive_self_loops(),
            "finite_rank_tree_first_two_children": finite_rank_tree(),
            "closed_minus_map_set": closed,
            "equal_depth_obstruction_rank_witnesses": witnesses,
            "all_short_upper_words_including_noncontinuable_leaves": all_short_upper_words(),
            "certified_terminating_family_witnesses": terminating}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: exact residue tables, finite inverse words, closed minus-map set, "
          "and positive equal-depth obstruction witnesses; no source census.")
