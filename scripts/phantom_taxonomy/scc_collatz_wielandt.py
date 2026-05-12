"""
Empirical Collatz-Wielandt table for compressed SCC retention matrices.

Input edge tables come from ``scc_transfer_summary.py`` and have rows

    src, dst, count, source_events, empirical_probability.

For each table this script builds the substochastic matrix P and a
positive test vector v by power iteration on P + epsilon.  It then
reports

    max_i (P v)_i / v_i,

which is the finite-dimensional Collatz-Wielandt upper expression for
the empirical matrix.  This is still empirical: the matrix itself comes
from the sampled Phase-7.4 run.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_probability_edges(path: Path) -> tuple[list[str], dict[str, list[tuple[str, float]]]]:
    nodes: set[str] = set()
    rows: list[tuple[str, str, float]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            src = row["src"]
            dst = row["dst"]
            p = float(row["empirical_probability"])
            nodes.add(src)
            nodes.add(dst)
            rows.append((src, dst, p))
    ordered = sorted(nodes)
    outgoing: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for src, dst, p in rows:
        outgoing[src].append((dst, p))
    for node in ordered:
        outgoing.setdefault(node, [])
    return ordered, outgoing


def multiply(
    nodes: list[str],
    outgoing: dict[str, list[tuple[str, float]]],
    vector: dict[str, float],
    epsilon: float = 0.0,
) -> dict[str, float]:
    out = {node: 0.0 for node in nodes}
    if epsilon:
        eps_mass = epsilon * sum(vector.values())
        for node in nodes:
            out[node] += eps_mass
    for src in nodes:
        src_mass = vector[src]
        if src_mass == 0:
            continue
        for dst, p in outgoing[src]:
            out[dst] += src_mass * p
    return out


def positive_power_vector(
    nodes: list[str],
    outgoing: dict[str, list[tuple[str, float]]],
    epsilon: float,
    iterations: int,
    tolerance: float,
) -> tuple[float, dict[str, float]]:
    n = len(nodes)
    v = {node: 1.0 / n for node in nodes}
    rho = 0.0
    for _ in range(iterations):
        w = multiply(nodes, outgoing, v, epsilon=epsilon)
        norm = max(abs(x) for x in w.values())
        if norm == 0:
            return 0.0, v
        w = {node: value / norm for node, value in w.items()}
        if max(abs(w[node] - v[node]) for node in nodes) < tolerance:
            rho = norm
            v = w
            break
        rho = norm
        v = w
    return rho, v


def collatz_wielandt_upper(
    nodes: list[str],
    outgoing: dict[str, list[tuple[str, float]]],
    v: dict[str, float],
) -> tuple[float, str, float]:
    pv = multiply(nodes, outgoing, v)
    ratios = [(pv[node] / v[node], node, pv[node]) for node in nodes if v[node] > 0]
    return max(ratios)


def row_sum_stats(nodes: list[str], outgoing: dict[str, list[tuple[str, float]]]) -> tuple[float, float, str]:
    row_sums = []
    for node in nodes:
        row_sums.append((sum(p for _, p in outgoing[node]), node))
    max_sum, max_node = max(row_sums)
    min_sum, _ = min(row_sums)
    return min_sum, max_sum, max_node


def analyze_file(path: Path, epsilon: float, iterations: int, tolerance: float) -> dict[str, object]:
    nodes, outgoing = read_probability_edges(path)
    rho_eps, v = positive_power_vector(nodes, outgoing, epsilon, iterations, tolerance)
    cw_upper, cw_node, pv_at_node = collatz_wielandt_upper(nodes, outgoing, v)
    row_min, row_max, row_max_node = row_sum_stats(nodes, outgoing)
    return {
        "name": path.stem,
        "path": str(path),
        "states": len(nodes),
        "edge_types": sum(len(outgoing[node]) for node in nodes),
        "epsilon": epsilon,
        "rho_power_perturbed": rho_eps,
        "cw_upper": cw_upper,
        "cw_max_node": cw_node,
        "pv_at_max_node": pv_at_node,
        "v_at_max_node": v[cw_node],
        "row_sum_min": row_min,
        "row_sum_max": row_max,
        "row_sum_max_node": row_max_node,
        "status": "OK" if cw_upper < 1.0 else "FAIL",
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    lines = [
        "# Empirical Collatz-Wielandt Table for K0=16 SCC",
        "",
        "The matrix is the empirical substochastic retention matrix produced",
        "from the sampled taxonomy SCC. The reported bound is",
        "`max_i (P v)_i / v_i` for a positive power-iteration vector `v`.",
        "",
        "| matrix | states | edge types | max row sum | CW upper | status | max node |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {name} | {states} | {edge_types} | {row_sum_max:.12g} | "
            "{cw_upper:.12g} | {status} | `{cw_max_node}` |".format(**row)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edge_csv", type=Path, nargs="+")
    parser.add_argument("--epsilon", type=float, default=1e-12)
    parser.add_argument("--iterations", type=int, default=20000)
    parser.add_argument("--tolerance", type=float, default=1e-14)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--md", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [analyze_file(path, args.epsilon, args.iterations, args.tolerance) for path in args.edge_csv]
    write_csv(rows, args.csv)
    write_markdown(rows, args.md)
    for row in rows:
        print(
            f"{row['name']}: states={row['states']} edge_types={row['edge_types']} "
            f"cw_upper={row['cw_upper']:.12g} status={row['status']} "
            f"max_node={row['cw_max_node']}"
        )


if __name__ == "__main__":
    main()
