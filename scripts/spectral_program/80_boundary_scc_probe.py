"""
80_boundary_scc_probe.py

Does the high-norm boundary layer self-feed?

79_boundary_tail_scaling.py showed that the largest tail row norm comes from
rare states with v2(t) >= T. A local row norm can be high without threatening
global contraction if those states do not form a persistent strongly connected
component.

This script builds the observed full/core/tail transition graph for

    t = r + j * 2^T

and reports SCC structure, with special attention to boundary states:

    boundary := v2(t) >= T.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict, deque
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_SCC = ROOT / "collatz_80_boundary_scc_summary.csv"
OUT_EDGES = ROOT / "collatz_80_boundary_scc_edges.csv"


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


def fmt_state(state: tuple[int, int, int]) -> str:
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def is_boundary(state: tuple[int, int, int], T: int) -> bool:
    return state[0] >= T


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


def reachable_boundary_cycle(nodes: set, graph: dict, T: int) -> tuple[int, int]:
    boundary_nodes = {n for n in nodes if is_boundary(n, T)}
    boundary_with_out_to_boundary = 0
    boundary_with_return_path = 0

    reverse = defaultdict(set)
    for src, dsts in graph.items():
        for dst in dsts:
            reverse[dst].add(src)

    for src in boundary_nodes:
        if any(dst in boundary_nodes for dst in graph.get(src, ())):
            boundary_with_out_to_boundary += 1

        # Check if some outgoing neighbor can reach this boundary source.
        found = False
        for start in graph.get(src, ()):
            seen = {start}
            q = deque([start])
            while q and not found:
                cur = q.popleft()
                if cur == src:
                    found = True
                    break
                for nxt in graph.get(cur, ()):
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)
        if found:
            boundary_with_return_path += 1
    return boundary_with_out_to_boundary, boundary_with_return_path


def setup():
    probe = load_module("78_tail_row_certificate_probe.py", "tail_probe")
    return probe, probe.setup()


def build_rows(probe, ctx, args: argparse.Namespace, T: int):
    rows = []
    groups = defaultdict(list)
    for r in range(1 << T):
        for h in range(1 << args.hit_bits):
            group_rows = [
                probe.trace_row(ctx, args, T, r, h, j)
                for j in range(args.j_count)
            ]
            counts = Counter(row["signature"] for row in group_rows)
            core_sig, _ = counts.most_common(1)[0]
            for row in group_rows:
                row["T"] = T
                row["r"] = r
                row["h"] = h
                row["part"] = "core" if row["signature"] == core_sig else "tail"
                rows.append(row)
                groups[(r, h)].append(row)
    return rows


def analyze(T: int, args: argparse.Namespace) -> tuple[dict, list[dict]]:
    probe, ctx = setup()
    rows = build_rows(probe, ctx, args, T)

    graphs = {"full": defaultdict(set), "core": defaultdict(set), "tail": defaultdict(set)}
    edge_counts = {name: Counter() for name in graphs}
    edge_weights = {name: Counter() for name in graphs}
    nodes = set()

    for row in rows:
        src = row["src"]
        nodes.add(src)
        if row["terminal"]:
            continue
        dst = row["dst"]
        nodes.add(dst)
        for name in ("full", row["part"]):
            graphs[name][src].add(dst)
            edge_counts[name][(src, dst)] += 1
            edge_weights[name][(src, dst)] += row["weight"]

    summary_rows = []
    edge_rows = []
    for name, graph in graphs.items():
        comps = tarjan_scc(nodes, graph)
        nontrivial = []
        boundary_comps = []
        for comp in comps:
            comp_set = set(comp)
            has_self_loop = any(n in graph.get(n, ()) for n in comp)
            if len(comp) > 1 or has_self_loop:
                nontrivial.append(comp)
                if any(is_boundary(n, T) for n in comp):
                    boundary_comps.append(comp)

        b_out, b_cycle = reachable_boundary_cycle(nodes, graph, T)
        largest = max((len(c) for c in comps), default=0)
        largest_boundary = max((len(c) for c in boundary_comps), default=0)
        boundary_nodes = [n for n in nodes if is_boundary(n, T)]
        summary_rows.append({
            "T": T,
            "j_count": args.j_count,
            "graph": name,
            "node_count": len(nodes),
            "edge_count": sum(len(v) for v in graph.values()),
            "scc_count": len(comps),
            "nontrivial_scc_count": len(nontrivial),
            "largest_scc": largest,
            "boundary_node_count": len(boundary_nodes),
            "boundary_nontrivial_scc_count": len(boundary_comps),
            "largest_boundary_scc": largest_boundary,
            "boundary_nodes_with_boundary_edge": b_out,
            "boundary_nodes_with_return_path": b_cycle,
        })

        for (src, dst), count in edge_counts[name].most_common(200):
            edge_rows.append({
                "T": T,
                "j_count": args.j_count,
                "graph": name,
                "src": fmt_state(src),
                "dst": fmt_state(dst),
                "src_boundary": int(is_boundary(src, T)),
                "dst_boundary": int(is_boundary(dst, T)),
                "count": count,
                "weight": edge_weights[name][(src, dst)],
            })

    return summary_rows, edge_rows


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SCC della boundary layer.")
    parser.add_argument("--T", default="10")
    parser.add_argument("--j-count", type=int, default=64)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    all_summary = []
    all_edges = []
    print("=" * 120)
    print("  Boundary SCC probe")
    print("=" * 120)
    print(f"  j_count={args.j_count}, odd_bits={args.odd_bits}, hit_bits={args.hit_bits}")
    print(f"  {'T':>4} {'graph':>6} {'nodes':>7} {'edges':>7} {'nontr SCC':>10} {'bdy SCC':>8} {'bdy return':>10}")
    for T in parse_csv_ints(args.T):
        summary, edges = analyze(T, args)
        all_summary.extend(summary)
        all_edges.extend(edges)
        for row in summary:
            print(
                f"  {T:>4} {row['graph']:>6} {row['node_count']:>7} "
                f"{row['edge_count']:>7} {row['nontrivial_scc_count']:>10} "
                f"{row['boundary_nontrivial_scc_count']:>8} "
                f"{row['boundary_nodes_with_return_path']:>10}"
            )

    write_csv(all_summary, OUT_SCC)
    write_csv(all_edges, OUT_EDGES)
    print("\n  Output:")
    print(f"    {OUT_SCC.name}")
    print(f"    {OUT_EDGES.name}")


if __name__ == "__main__":
    main()
