"""
Empirical transfer summary for an observed phantom-taxonomy SCC.

This script is the first Phase-7.6 bridge from the raw SCC found at
K0=16 to something operator-like.  It reads the event stream emitted by
``orbit_harness.py`` and the SCC node list emitted by ``scc_report.py``.
For each event whose node lies in the SCC, it records either

    node -> next event node

or, when the orbit has no next monitored event, an exit from the SCC.
The induced substochastic matrix on the SCC has entries

    P[i,j] = observed_count(i -> j inside SCC) / observed_count(events at i).

Its spectral radius is an empirical retention diagnostic, not the final
weighted Collatz-Wielandt certificate.  It is deliberately labeled as a
diagnostic so that Phase 7.6 can decide how much compression is needed
before attempting the true cross-node operator.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def read_scc_nodes(path: Path, rank: int) -> set[str]:
    out: set[str] = set()
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if int(row["scc_rank"]) == rank:
                out.add(row["node"])
    return out


def event_node(row: dict[str, str]) -> str:
    return f"{row['node']}:b{row['b']}"


def orbit_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["source_node"], row["source_b"], row["t"]


def read_event_groups(path: Path) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            groups[orbit_key(row)].append(row)
    for rows in groups.values():
        rows.sort(key=lambda r: int(r["event_index"]))
    return groups


def node_macro(node: str, mode: str) -> str:
    prefix, b = node.rsplit(":b", 1)
    parts = prefix.split(":")
    K = parts[0]
    L = parts[1]
    if mode == "node":
        return node
    if mode == "K":
        return f"{K}:b{b}"
    if mode == "KL":
        return f"{K}:{L}:b{b}"
    raise ValueError(mode)


def transition_counts(
    groups: dict[tuple[str, str, str], list[dict[str, str]]],
    scc_nodes: set[str],
    macro_mode: str,
) -> tuple[Counter[tuple[str, str]], Counter[str], Counter[str]]:
    internal = Counter()
    source_events = Counter()
    exits = Counter()

    for rows in groups.values():
        nodes = [event_node(row) for row in rows]
        for idx, src in enumerate(nodes):
            if src not in scc_nodes:
                continue
            src_macro = node_macro(src, macro_mode)
            source_events[src_macro] += 1
            if idx + 1 >= len(nodes):
                exits[src_macro] += 1
                continue
            dst = nodes[idx + 1]
            if dst not in scc_nodes:
                exits[src_macro] += 1
                continue
            dst_macro = node_macro(dst, macro_mode)
            internal[(src_macro, dst_macro)] += 1

    return internal, source_events, exits


def spectral_radius_from_counts(
    internal: Counter[tuple[str, str]],
    source_events: Counter[str],
    iterations: int = 10000,
    tolerance: float = 1e-13,
) -> tuple[float, int]:
    nodes = sorted(source_events)
    index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    if n == 0:
        return 0.0, 0

    # Power iteration on the nonnegative substochastic matrix.
    outgoing: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for (src, dst), count in internal.items():
        if src not in index or dst not in index:
            continue
        outgoing[index[src]].append((index[dst], count / source_events[src]))

    v = [1.0 / n] * n
    rho = 0.0
    for _ in range(iterations):
        w = [0.0] * n
        for i, row in enumerate(outgoing):
            mass = v[i]
            if mass == 0:
                continue
            for j, weight in row:
                w[j] += mass * weight
        norm = max(abs(x) for x in w)
        if norm == 0:
            return 0.0, n
        w = [x / norm for x in w]
        if max(abs(a - b) for a, b in zip(w, v)) < tolerance:
            rho = norm
            break
        v = w
        rho = norm
    return rho, n


def write_edge_csv(
    path: Path,
    internal: Counter[tuple[str, str]],
    source_events: Counter[str],
) -> None:
    rows = []
    for (src, dst), count in internal.most_common():
        rows.append(
            {
                "src": src,
                "dst": dst,
                "count": count,
                "source_events": source_events[src],
                "empirical_probability": count / source_events[src],
            }
        )
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    mode_summaries: list[dict[str, object]],
) -> None:
    lines = [
        "# K0=16 SCC Empirical Transfer Summary",
        "",
        "This is an empirical retention diagnostic for the observed taxonomy",
        "SCC. It is not yet the weighted cross-node Collatz-Wielandt",
        "certificate required to close Phase 7.6.",
        "",
        "| mode | states | internal edge types | source events | exits | retention mass | rho(P_internal) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in mode_summaries:
        lines.append(
            "| {mode} | {states} | {edge_types} | {source_events} | {exits} | "
            "{retention:.6f} | {rho:.12g} |".format(**row)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--scc-nodes", type=Path, required=True)
    parser.add_argument("--scc-rank", type=int, default=1)
    parser.add_argument("--out-prefix", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scc_nodes = read_scc_nodes(args.scc_nodes, args.scc_rank)
    groups = read_event_groups(args.events)

    summaries: list[dict[str, object]] = []
    for mode in ["node", "KL", "K"]:
        internal, source_events, exits = transition_counts(groups, scc_nodes, mode)
        rho, states = spectral_radius_from_counts(internal, source_events)
        edge_path = args.out_prefix.with_name(f"{args.out_prefix.name}_{mode}_edges.csv")
        write_edge_csv(edge_path, internal, source_events)
        source_total = sum(source_events.values())
        exit_total = sum(exits.values())
        internal_total = sum(internal.values())
        summaries.append(
            {
                "mode": mode,
                "states": states,
                "edge_types": len(internal),
                "source_events": source_total,
                "exits": exit_total,
                "retention": internal_total / source_total if source_total else 0.0,
                "rho": rho,
            }
        )
        print(
            f"{mode}: states={states} edge_types={len(internal)} "
            f"source_events={source_total} exits={exit_total} "
            f"retention={summaries[-1]['retention']:.6f} rho={rho:.12g}"
        )

    report_path = args.out_prefix.with_name(f"{args.out_prefix.name}_transfer_summary.md")
    write_report(report_path, summaries)
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
