"""
Exact rational certificate for SCC Collatz-Wielandt bounds.

The input transition matrix may be empirical, as in the original
sampled orbit-harness runs, or deterministic, as in the residue-cell
transfer closure.  This script certifies the *matrix bound*: it converts
edge probabilities to exact fractions count/source_events, constructs a
positive integer test vector, and verifies exactly that

    (P v)_i <= alpha * v_i

for a user-supplied rational alpha.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


def read_edges(path: Path) -> tuple[list[str], dict[str, list[tuple[str, Fraction]]]]:
    nodes: set[str] = set()
    rows: list[tuple[str, str, Fraction]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            src = row["src"]
            dst = row["dst"]
            probability = Fraction(int(row["count"]), int(row["source_events"]))
            nodes.add(src)
            nodes.add(dst)
            rows.append((src, dst, probability))
    ordered = sorted(nodes)
    outgoing: dict[str, list[tuple[str, Fraction]]] = defaultdict(list)
    for src, dst, probability in rows:
        outgoing[src].append((dst, probability))
    for node in ordered:
        outgoing.setdefault(node, [])
    return ordered, outgoing


def multiply_float(nodes: list[str], outgoing: dict[str, list[tuple[str, Fraction]]], vector: dict[str, float]) -> dict[str, float]:
    out = {node: 0.0 for node in nodes}
    for src in nodes:
        mass = vector[src]
        for dst, probability in outgoing[src]:
            out[dst] += mass * float(probability)
    return out


def power_vector(nodes: list[str], outgoing: dict[str, list[tuple[str, Fraction]]], iterations: int) -> dict[str, float]:
    v = {node: 1.0 / len(nodes) for node in nodes}
    for _ in range(iterations):
        w = multiply_float(nodes, outgoing, v)
        norm = max(abs(value) for value in w.values())
        if norm == 0:
            break
        v = {node: value / norm for node, value in w.items()}
        floor = 1e-18
        v = {node: max(value, floor) for node, value in v.items()}
    return v


def integer_vector(float_vector: dict[str, float], scale: int) -> dict[str, int]:
    return {node: max(1, int(round(value * scale))) for node, value in float_vector.items()}


def verify_exact(
    nodes: list[str],
    outgoing: dict[str, list[tuple[str, Fraction]]],
    vector: dict[str, int],
    alpha: Fraction,
) -> tuple[bool, Fraction, str]:
    incoming_sum = {node: Fraction(0, 1) for node in nodes}
    for src in nodes:
        for dst, probability in outgoing[src]:
            incoming_sum[dst] += probability * vector[src]

    max_ratio = Fraction(0, 1)
    max_node = nodes[0] if nodes else ""
    ok = True
    for node in nodes:
        ratio = incoming_sum[node] / vector[node]
        if ratio > max_ratio:
            max_ratio = ratio
            max_node = node
        if ratio > alpha:
            ok = False
    return ok, max_ratio, max_node


def write_certificate(
    path: Path,
    edge_path: Path,
    nodes: list[str],
    outgoing: dict[str, list[tuple[str, Fraction]]],
    vector: dict[str, int],
    alpha: Fraction,
    max_ratio: Fraction,
    max_node: str,
) -> None:
    edges = []
    for src in nodes:
        for dst, probability in outgoing[src]:
            edges.append(
                {
                    "src": src,
                    "dst": dst,
                    "probability_num": probability.numerator,
                    "probability_den": probability.denominator,
                }
            )
    payload = {
        "edge_csv": str(edge_path),
        "orientation": "incoming form: (P v)[dst] = sum_src probability(src,dst) * v[src]",
        "alpha_num": alpha.numerator,
        "alpha_den": alpha.denominator,
        "max_ratio_num": max_ratio.numerator,
        "max_ratio_den": max_ratio.denominator,
        "max_ratio_decimal": float(max_ratio),
        "max_node": max_node,
        "nodes": nodes,
        "vector": vector,
        "edges": edges,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def verify_certificate(path: Path) -> tuple[bool, Fraction, str, Fraction]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    nodes = list(payload["nodes"])
    outgoing: dict[str, list[tuple[str, Fraction]]] = defaultdict(list)
    for edge in payload["edges"]:
        outgoing[edge["src"]].append(
            (edge["dst"], Fraction(int(edge["probability_num"]), int(edge["probability_den"])))
        )
    for node in nodes:
        outgoing.setdefault(node, [])
    vector = {node: int(payload["vector"][node]) for node in nodes}
    alpha = Fraction(int(payload["alpha_num"]), int(payload["alpha_den"]))
    ok, max_ratio, max_node = verify_exact(nodes, outgoing, vector, alpha)
    return ok, max_ratio, max_node, alpha


def parse_alpha(text: str) -> Fraction:
    if "/" in text:
        num, den = text.split("/", 1)
        return Fraction(int(num), int(den))
    return Fraction(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--edge-csv", type=Path)
    mode.add_argument("--verify", type=Path)
    parser.add_argument("--alpha", default="89/100")
    parser.add_argument("--scale", type=int, default=10**15)
    parser.add_argument("--iterations", type=int, default=50000)
    parser.add_argument("--certificate", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.verify:
        ok, max_ratio, max_node, alpha = verify_certificate(args.verify)
        print(f"certificate={args.verify}")
        print(f"alpha={alpha} ({float(alpha):.12g})")
        print(f"max_ratio={max_ratio} ({float(max_ratio):.12g})")
        print(f"max_node={max_node}")
        print(f"status={'OK' if ok else 'FAIL'}")
        raise SystemExit(0 if ok else 1)

    if args.certificate is None:
        raise SystemExit("--certificate is required with --edge-csv")
    alpha = parse_alpha(args.alpha)
    nodes, outgoing = read_edges(args.edge_csv)
    v_float = power_vector(nodes, outgoing, args.iterations)
    vector = integer_vector(v_float, args.scale)
    ok, max_ratio, max_node = verify_exact(nodes, outgoing, vector, alpha)
    write_certificate(args.certificate, args.edge_csv, nodes, outgoing, vector, alpha, max_ratio, max_node)
    print(f"certificate={args.certificate}")
    print(f"states={len(nodes)}")
    print(f"alpha={alpha} ({float(alpha):.12g})")
    print(f"max_ratio={max_ratio} ({float(max_ratio):.12g})")
    print(f"max_node={max_node}")
    print(f"status={'OK' if ok else 'FAIL'}")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
