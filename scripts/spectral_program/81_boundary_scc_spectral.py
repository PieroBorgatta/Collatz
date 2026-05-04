"""
81_boundary_scc_spectral.py

Weighted spectral analysis of SCCs touching the boundary layer.

80_boundary_scc_probe.py found that boundary states can lie in a nontrivial
SCC in the full/tail graph. This script asks the quantitative question:

    what is the spectral radius of that SCC after normalization?

If the boundary SCC has rho << 1, then the high local row norm is not
dangerous because boundary recurrence is weak.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_81_boundary_scc_spectral.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def is_boundary(state: tuple[int, int, int], T: int) -> bool:
    return state[0] >= T


def fmt_state(state: tuple[int, int, int]) -> str:
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def tarjan_scc(nodes: set, graph: dict) -> list[list]:
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    comps = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, ()):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for node in nodes:
        if node not in indices:
            strongconnect(node)
    return comps


def spectral_radius_dense_or_sparse(matrix: csr_matrix) -> float:
    n = matrix.shape[0]
    if n == 0 or matrix.nnz == 0:
        return 0.0
    if n <= 128:
        vals = np.linalg.eigvals(matrix.toarray())
        return float(max(abs(v) for v in vals)) if vals.size else 0.0
    vals = eigs(matrix, k=1, which="LM", return_eigenvectors=False, maxiter=20000, tol=1e-10)
    return float(abs(vals[0]))


def setup():
    probe = load_module("78_tail_row_certificate_probe.py", "tail_probe")
    return probe, probe.setup()


def collect_rows(probe, ctx, args: argparse.Namespace, T: int):
    rows = []
    source_counts = Counter()
    groups = defaultdict(list)
    for r in range(1 << T):
        for h in range(1 << args.hit_bits):
            group_rows = [probe.trace_row(ctx, args, T, r, h, j) for j in range(args.j_count)]
            counts = Counter(row["signature"] for row in group_rows)
            core_sig, _ = counts.most_common(1)[0]
            for row in group_rows:
                row["part"] = "core" if row["signature"] == core_sig else "tail"
                rows.append(row)
                source_counts[row["src"]] += 1
                groups[(r, h)].append(row)
    return rows, source_counts


def build_weighted_graph(rows, source_counts, graph_name: str):
    weights = Counter()
    graph = defaultdict(set)
    nodes = set(source_counts)
    for row in rows:
        if row["terminal"]:
            continue
        if graph_name != "full" and row["part"] != graph_name:
            continue
        src = row["src"]
        dst = row["dst"]
        nodes.add(src)
        nodes.add(dst)
        graph[src].add(dst)
        weights[(src, dst)] += row["weight"] / source_counts[src]
    return nodes, graph, weights


def matrix_for_component(comp: list, weights: Counter) -> csr_matrix:
    idx = {state: i for i, state in enumerate(comp)}
    data = []
    rr = []
    cc = []
    comp_set = set(comp)
    for (src, dst), weight in weights.items():
        if src in comp_set and dst in comp_set:
            rr.append(idx[src])
            cc.append(idx[dst])
            data.append(weight)
    return csr_matrix((data, (rr, cc)), shape=(len(comp), len(comp)))


def analyze(T: int, args: argparse.Namespace) -> list[dict]:
    probe, ctx = setup()
    rows, source_counts = collect_rows(probe, ctx, args, T)
    out = []

    for graph_name in ("full", "core", "tail"):
        nodes, graph, weights = build_weighted_graph(rows, source_counts, graph_name)
        comps = tarjan_scc(nodes, graph)
        for comp_id, comp in enumerate(comps):
            comp_set = set(comp)
            has_self_loop = any(n in graph.get(n, ()) for n in comp_set)
            if len(comp) == 1 and not has_self_loop:
                continue
            boundary_count = sum(1 for n in comp if is_boundary(n, T))
            matrix = matrix_for_component(comp, weights)
            row_sums = np.asarray(matrix.sum(axis=1)).ravel()
            rho = spectral_radius_dense_or_sparse(matrix)
            edge_internal = matrix.nnz
            out.append({
                "T": T,
                "j_count": args.j_count,
                "graph": graph_name,
                "component_id": comp_id,
                "size": len(comp),
                "boundary_count": boundary_count,
                "rho": rho,
                "max_internal_row_sum": float(row_sums.max()) if row_sums.size else 0.0,
                "edge_internal": edge_internal,
                "sample_states": ",".join(fmt_state(s) for s in sorted(comp)[:12]),
            })
    out.sort(key=lambda r: (r["graph"], -r["boundary_count"], -r["rho"], -r["size"]))
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spettro SCC boundary.")
    parser.add_argument("--T", type=int, default=10)
    parser.add_argument("--j-count", type=int, default=64)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = analyze(args.T, args)
    write_csv(rows, OUT)
    print("=" * 118)
    print("  Boundary SCC spectral")
    print("=" * 118)
    print(f"  T={args.T}, j_count={args.j_count}")
    print(f"  {'graph':>6} {'size':>6} {'bdy':>5} {'rho':>14} {'max row':>12} {'states'}")
    for row in rows[:20]:
        print(
            f"  {row['graph']:>6} {row['size']:>6} {row['boundary_count']:>5} "
            f"{row['rho']:>14.6g} {row['max_internal_row_sum']:>12.6g} "
            f"{row['sample_states'][:70]}"
        )
    print("\n  Output:")
    print(f"    {OUT.name}")


if __name__ == "__main__":
    main()
