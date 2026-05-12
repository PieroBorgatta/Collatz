"""
SCC report for augmented phantom-taxonomy episode graphs.

The input is an edge CSV emitted by ``orbit_harness.py``.  Nodes are the
taxonomy labels

    K{A}:L{L}:w{a_0-...-a_{L-1}}:b{b}

and edges are observed transitions between monitored phantom episodes.
The report is intentionally topological: spectral certificates, when
needed, are delegated to later Phase-7 follow-up tasks.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


PAPER_SCC_Q_LABELS = {
    "-5739192681529/2404426874857": "paper empirical k=10",
    "-2199012694031/709849655971": "paper empirical k=11",
    "-2123/1675": "paper empirical k=12 cycle 1",
    "-817/601": "paper empirical k=12 cycle 2",
    "-104312644103/30307317785": "paper empirical k=20",
}


@dataclass(frozen=True)
class ComponentSummary:
    index: int
    size: int
    internal_edge_count: int
    total_internal_weight: int
    sample_nodes: tuple[str, ...]


def read_edges(path: Path) -> list[tuple[str, str, int]]:
    edges: list[tuple[str, str, int]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            edges.append((row["src"], row["dst"], int(row["count"])))
    return edges


def build_graph(edges: list[tuple[str, str, int]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for src, dst, _ in edges:
        graph[src].add(dst)
        graph.setdefault(dst, set())
    return graph


def tarjan_scc(graph: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    components: list[list[str]] = []

    def strongconnect(v: str) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph[v]:
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
            components.append(sorted(comp))

    for node in sorted(graph):
        if node not in indices:
            strongconnect(node)
    return components


def summarize_components(
    graph: dict[str, set[str]],
    edges: list[tuple[str, str, int]],
    components: list[list[str]],
) -> list[ComponentSummary]:
    node_to_component = {}
    for idx, comp in enumerate(components):
        for node in comp:
            node_to_component[node] = idx

    edge_count = defaultdict(int)
    edge_weight = defaultdict(int)
    for src, dst, count in edges:
        c_src = node_to_component[src]
        c_dst = node_to_component[dst]
        if c_src == c_dst:
            edge_count[c_src] += 1
            edge_weight[c_src] += count

    summaries = []
    for idx, comp in enumerate(components):
        nontrivial = len(comp) > 1 or any(node in graph[node] for node in comp)
        if not nontrivial:
            continue
        summaries.append(
            ComponentSummary(
                index=idx,
                size=len(comp),
                internal_edge_count=edge_count[idx],
                total_internal_weight=edge_weight[idx],
                sample_nodes=tuple(comp[:12]),
            )
        )
    summaries.sort(key=lambda c: (-c.size, -c.total_internal_weight, c.sample_nodes))
    return summaries


def read_representative_q_map(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            node_prefix = f"K{row['K']}:L{row['L']}:w{'-'.join(row['word'].split())}"
            out[node_prefix] = f"{row['q_num']}/{row['q_den']}"
    return out


def paper_label_for_node(node: str, q_map: dict[str, str]) -> str | None:
    prefix = node.rsplit(":b", 1)[0]
    return PAPER_SCC_Q_LABELS.get(q_map.get(prefix, ""))


def write_markdown(
    path: Path,
    edge_path: Path,
    graph: dict[str, set[str]],
    edges: list[tuple[str, str, int]],
    summaries: list[ComponentSummary],
    q_map: dict[str, str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    all_nodes = sorted(graph)
    paper_hits = [(node, paper_label_for_node(node, q_map)) for node in all_nodes]
    paper_hits = [(node, label) for node, label in paper_hits if label is not None]

    lines = [
        "# Augmented Phantom Taxonomy SCC Report",
        "",
        f"Input edge CSV: `{edge_path}`",
        "",
        f"- Nodes with at least one observed edge: {len(graph)}",
        f"- Directed observed edge types: {len(edges)}",
        f"- Nontrivial SCCs: {len(summaries)}",
        f"- Largest nontrivial SCC size: {summaries[0].size if summaries else 0}",
        "",
        "## Paper-SCC Comparison",
        "",
        "The paper §8 SCC is expressed in empirical cycle labels `(k,c,b)`,",
        "whereas this Phase-7 taxonomy graph is expressed in primitive",
        "cyclic-composition labels `(K,L,word,b)`. Exact comparison is only",
        "possible when a taxonomy representative has the same rational `q_w`",
        "as one of the listed empirical representatives.",
        "",
    ]
    if paper_hits:
        lines.append("Recognized empirical representatives present in the observed graph:")
        lines.append("")
        for node, label in paper_hits:
            lines.append(f"- `{node}` -> {label}")
    else:
        lines.append("No empirical paper-SCC representative was recognized by exact `q_w` equality in the observed graph.")
    lines.extend(["", "## Nontrivial SCCs", ""])
    for idx, summary in enumerate(summaries[:30], start=1):
        lines.extend(
            [
                f"### SCC {idx}",
                "",
                f"- Size: {summary.size}",
                f"- Internal edge types: {summary.internal_edge_count}",
                f"- Internal observed transition weight: {summary.total_internal_weight}",
                "- Sample nodes:",
                "",
            ]
        )
        for node in summary.sample_nodes:
            label = paper_label_for_node(node, q_map)
            suffix = f" ({label})" if label else ""
            lines.append(f"  - `{node}`{suffix}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_component_csv(
    path: Path,
    summaries: list[ComponentSummary],
    q_map: dict[str, str],
) -> None:
    rows = []
    for rank, summary in enumerate(summaries, start=1):
        for node in summary.sample_nodes:
            # The markdown intentionally samples nodes, but the CSV writer is
            # patched below in main with the full component node lists.
            rows.append((rank, summary.size, summary.internal_edge_count, summary.total_internal_weight, node))
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scc_rank",
                "scc_size",
                "internal_edge_types",
                "internal_observed_weight",
                "node",
                "paper_label",
            ],
        )
        writer.writeheader()
        for rank, size, edge_count, weight, node in rows:
            writer.writerow(
                {
                    "scc_rank": rank,
                    "scc_size": size,
                    "internal_edge_types": edge_count,
                    "internal_observed_weight": weight,
                    "node": node,
                    "paper_label": paper_label_for_node(node, q_map) or "",
                }
            )


def write_full_component_csv(
    path: Path,
    summaries: list[ComponentSummary],
    components: list[list[str]],
    q_map: dict[str, str],
) -> None:
    if not summaries:
        return
    component_by_index = {summary.index: summary for summary in summaries}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scc_rank",
                "scc_index",
                "scc_size",
                "internal_edge_types",
                "internal_observed_weight",
                "node",
                "paper_label",
            ],
        )
        writer.writeheader()
        for rank, summary in enumerate(summaries, start=1):
            for node in components[summary.index]:
                writer.writerow(
                    {
                        "scc_rank": rank,
                        "scc_index": summary.index,
                        "scc_size": summary.size,
                        "internal_edge_types": summary.internal_edge_count,
                        "internal_observed_weight": summary.total_internal_weight,
                        "node": node,
                        "paper_label": paper_label_for_node(node, q_map) or "",
                    }
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--representatives", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--components-csv", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    edges = read_edges(args.edges)
    graph = build_graph(edges)
    components = tarjan_scc(graph)
    summaries = summarize_components(graph, edges, components)
    q_map = read_representative_q_map(args.representatives)
    write_markdown(args.out, args.edges, graph, edges, summaries, q_map)
    if args.components_csv:
        write_full_component_csv(args.components_csv, summaries, components, q_map)

    print(f"nodes={len(graph)}")
    print(f"edge_types={len(edges)}")
    print(f"nontrivial_sccs={len(summaries)}")
    print(f"largest_scc={summaries[0].size if summaries else 0}")
    print(f"report={args.out}")
    if args.components_csv:
        print(f"components_csv={args.components_csv}")


if __name__ == "__main__":
    main()
