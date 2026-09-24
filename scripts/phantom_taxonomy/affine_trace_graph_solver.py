#!/usr/bin/env python3
"""
Exact solver for scalar affine trace labels on a finite exponent graph.

An edge ``u --e--> v`` transports a rational formal point by

    x_v = (3*x_u + 1) / 2^e.

Equivalently,

    2^e*x_v - 3*x_u = 1.

The solver performs rational Gaussian elimination on these equations.  If
the unique solution is negative at every node, a common denominator turns it
into natural labels

    x_v = -C_v / D,

which satisfy the checker equations with the odd normalization ``q = 3``:

    D + 2^e*C_v = 3*C_u.

No integer orbit values and no residue ranges are enumerated.  The purpose is
to decide whether a proposed finite SCC carries one coherent scalar affine
trace.  Inconsistent cycles are rejected exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from math import gcd, lcm


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    exponent: int

    def __post_init__(self) -> None:
        if self.exponent <= 0:
            raise ValueError("accelerated Syracuse exponents must be positive")


@dataclass(frozen=True)
class AffineTraceSolution:
    status: str
    points: dict[str, Fraction] | None
    denominator: int | None
    constants: dict[str, int] | None

    @property
    def compatible(self) -> bool:
        return self.status == "compatible_negative_trace"


def _rref(
    matrix: list[list[Fraction]],
    variable_count: int,
) -> tuple[list[list[Fraction]], list[int], bool]:
    """Reduced row-echelon form over the rationals."""
    rows = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(variable_count):
        selected = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column] != 0
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]

        for row in range(len(rows)):
            if row == pivot_row:
                continue
            factor = rows[row][column]
            if factor == 0:
                continue
            rows[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]

        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    inconsistent = any(
        all(row[column] == 0 for column in range(variable_count))
        and row[variable_count] != 0
        for row in rows
    )
    return rows, pivot_columns, inconsistent


def solve_affine_trace(
    nodes: tuple[str, ...],
    edges: tuple[Edge, ...],
) -> AffineTraceSolution:
    """
    Solve the exact formal-point equations and, when possible, return
    primitive common-denominator natural labels.
    """
    if not nodes:
        raise ValueError("the graph must contain at least one node")
    if len(set(nodes)) != len(nodes):
        raise ValueError("node names must be unique")

    node_index = {node: index for index, node in enumerate(nodes)}
    matrix: list[list[Fraction]] = []
    for edge in edges:
        if edge.source not in node_index or edge.target not in node_index:
            raise ValueError("every edge endpoint must be a declared node")
        row = [Fraction(0) for _ in range(len(nodes) + 1)]
        row[node_index[edge.source]] -= 3
        row[node_index[edge.target]] += 1 << edge.exponent
        row[-1] = 1
        matrix.append(row)

    rows, pivots, inconsistent = _rref(matrix, len(nodes))
    if inconsistent:
        return AffineTraceSolution("inconsistent_cycles", None, None, None)
    if len(pivots) < len(nodes):
        return AffineTraceSolution("underdetermined", None, None, None)

    points = {node: Fraction(0) for node in nodes}
    for row, pivot in zip(rows, pivots):
        if pivot < len(nodes):
            points[nodes[pivot]] = row[-1]

    if any(point >= 0 for point in points.values()):
        return AffineTraceSolution(
            "unique_but_not_negative",
            points,
            None,
            None,
        )

    denominator = lcm(*(point.denominator for point in points.values()))
    constants = {
        node: int(-point * denominator)
        for node, point in points.items()
    }
    common = reduce(gcd, (denominator, *constants.values()))
    denominator //= common
    constants = {
        node: constant // common
        for node, constant in constants.items()
    }

    assert denominator > 0
    assert all(constant > 0 for constant in constants.values())
    assert all(
        denominator
        + (1 << edge.exponent) * constants[edge.target]
        == 3 * constants[edge.source]
        for edge in edges
    )
    assert all(
        points[node] == Fraction(-constants[node], denominator)
        for node in nodes
    )
    return AffineTraceSolution(
        "compatible_negative_trace",
        points,
        denominator,
        constants,
    )


def word_constant(word: tuple[int, ...]) -> tuple[int, int, int]:
    """Return ``(3^length, C_word, 2^sum)`` by exact affine composition."""
    power_three = 1
    constant = 0
    power_two = 1
    for exponent in word:
        constant = 3 * constant + power_two
        power_three *= 3
        power_two *= 1 << exponent
    return power_three, constant, power_two


def word_formal_fixed_point(word: tuple[int, ...]) -> Fraction:
    """Formal rational fixed point ``C/(2^A-3^L)``."""
    power_three, constant, power_two = word_constant(word)
    denominator = power_two - power_three
    if denominator == 0:
        raise ValueError("degenerate word has no unique fixed point")
    return Fraction(constant, denominator)


def _assert_solution(
    solution: AffineTraceSolution,
    *,
    denominator: int,
    constants: dict[str, int],
) -> None:
    assert solution.compatible
    assert solution.denominator == denominator
    assert solution.constants == constants


def _self_test() -> None:
    one = solve_affine_trace(
        ("a",),
        (Edge("a", "a", 1),),
    )
    _assert_solution(one, denominator=1, constants={"a": 1})

    one_two = solve_affine_trace(
        ("a", "b"),
        (Edge("a", "b", 1), Edge("b", "a", 2)),
    )
    _assert_solution(
        one_two,
        denominator=1,
        constants={"a": 5, "b": 7},
    )

    hidden = solve_affine_trace(
        ("a", "b", "c"),
        (
            Edge("a", "b", 1),
            Edge("b", "c", 1),
            Edge("c", "a", 2),
        ),
    )
    _assert_solution(
        hidden,
        denominator=11,
        constants={"a": 19, "b": 23, "c": 29},
    )

    # Two genuinely different cycles at node a demand both -1 and -5.
    incompatible_branch = solve_affine_trace(
        ("a", "b"),
        (
            Edge("a", "a", 1),
            Edge("a", "b", 1),
            Edge("b", "a", 2),
        ),
    )
    assert incompatible_branch.status == "inconsistent_cycles"

    # Branching is allowed when all cycles encode the same formal point.
    compatible_branch = solve_affine_trace(
        ("a", "b"),
        (
            Edge("a", "a", 1),
            Edge("a", "b", 1),
            Edge("b", "a", 1),
        ),
    )
    _assert_solution(
        compatible_branch,
        denominator=1,
        constants={"a": 1, "b": 1},
    )

    # The exponent-2 self-loop has fixed point +1, so it cannot be encoded
    # by natural C in the negative point -C/D.
    contractive = solve_affine_trace(
        ("a",),
        (Edge("a", "a", 2),),
    )
    assert contractive.status == "unique_but_not_negative"
    assert contractive.points == {"a": Fraction(1)}

    # Direct word-level fixed points agree with the graph labels above.
    assert word_formal_fixed_point((1,)) == Fraction(-1)
    assert word_formal_fixed_point((1, 2)) == Fraction(-5)
    assert word_formal_fixed_point((1, 1, 2)) == Fraction(-19, 11)
    assert word_formal_fixed_point((2,)) == Fraction(1)

    # The incompatible branching graph contains the cycles
    # [1]^(r+1) ++ [2].  Their exact fixed points are already distinct at
    # every checked symbolic index; the accompanying note proves the closed
    # formula is injective for all r.
    branching_points = [
        word_formal_fixed_point((1,) * (r + 1) + (2,))
        for r in range(8)
    ]
    assert len(set(branching_points)) == len(branching_points)

    print("affine_trace_graph_solver=ok")
    print("integer_orbit_samples=0")
    print("single_cycle_examples=3")
    print("compatible_branching_examples=1")
    print("incompatible_branching_examples=1")
    print("nonnegative_fixed_point_rejections=1")
    print("branching_cycle_fixed_points=8/8_distinct")
    print("decision=scalar_trace_requires_cycle-coherent_formal_point")


if __name__ == "__main__":
    _self_test()
