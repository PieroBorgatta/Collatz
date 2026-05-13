"""
Deterministic finite residue-cell transfer for the K0=16 phantom SCC.

This script replaces the sampled Phase-7 orbit-harness transition
counts with an exhaustive enumeration of a declared finite residue-cell
scope.  For each raw SCC state ``(w, b)`` and each residue subdivision

    0 <= t < 2^lift_bits,
    n0 = q_w mod 2^(b A_w + 1) + t * 2^(b A_w + 1),

it first checks that the canonical monitored hit at ``n0`` is really
the requested source state.  If a finer/stronger monitored phantom owns
that integer instead, the class is counted as shadowed.  Canonical
source cells are then traced deterministically until the next distinct
monitored hit or until the odd Syracuse orbit drops below its start.

The output edge CSVs have the same exact-rational shape expected by
``scc_cw_certificate.py``: probabilities are ``count/source_events``.
The coverage CSV and manifest record every finite residue cell in the
declared scope.  This is a deterministic finite residue-cell certificate
for that scope; it is intentionally separate from the older sampled
orbit-harness event stream.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from orbit_harness import (
    Representative,
    best_hit,
    build_monitors,
    odd_syracuse_step,
    read_representatives,
    source_start,
)


@dataclass(frozen=True)
class SourceNode:
    node: str
    rep: Representative
    b: int


@dataclass(frozen=True)
class TraceOutcome:
    status: str
    steps: int
    dst_node: str | None
    max_bit_length: int


def raw_node(rep: Representative, b: int) -> str:
    return f"{rep.key}:b{b}"


def parse_raw_node(node: str, rep_by_key: dict[str, Representative]) -> SourceNode | None:
    try:
        rep_key, b_text = node.rsplit(":b", 1)
        b = int(b_text)
    except ValueError:
        return None
    rep = rep_by_key.get(rep_key)
    if rep is None:
        return None
    return SourceNode(node=node, rep=rep, b=b)


def read_scc_source_nodes(
    path: Path,
    rank: int,
    rep_by_key: dict[str, Representative],
) -> list[SourceNode]:
    sources: list[SourceNode] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if int(row["scc_rank"]) != rank:
                continue
            source = parse_raw_node(row["node"], rep_by_key)
            if source is not None:
                sources.append(source)
    return sources


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


def next_distinct_hit(
    source: SourceNode,
    t: int,
    by_bits: dict[int, dict[int, list]],
    max_steps: int,
) -> TraceOutcome:
    n0, _, _ = source_start(source.rep, source.b, t)
    cur = n0
    max_value = n0
    source_key = (source.rep.node_id, source.b)

    for step in range(1, max_steps + 1):
        _, cur = odd_syracuse_step(cur)
        max_value = max(max_value, cur)
        if cur < n0:
            return TraceOutcome(
                status="below",
                steps=step,
                dst_node=None,
                max_bit_length=max_value.bit_length(),
            )

        hit = best_hit(cur, by_bits)
        if hit is None:
            continue
        rep, b, _ = hit
        if (rep.node_id, b) == source_key:
            continue
        return TraceOutcome(
            status="hit",
            steps=step,
            dst_node=raw_node(rep, b),
            max_bit_length=max_value.bit_length(),
        )

    return TraceOutcome(
        status="budget",
        steps=max_steps,
        dst_node=None,
        max_bit_length=max_value.bit_length(),
    )


def spectral_radius_from_counts(
    internal: Counter[tuple[str, str]],
    source_events: Counter[str],
    iterations: int = 20000,
    tolerance: float = 1e-13,
) -> float:
    nodes = sorted(set(source_events) | {dst for _, dst in internal})
    if not nodes:
        return 0.0
    index = {node: i for i, node in enumerate(nodes)}
    outgoing: list[list[tuple[int, float]]] = [[] for _ in nodes]
    for (src, dst), count in internal.items():
        denominator = source_events[src]
        if denominator == 0:
            continue
        outgoing[index[src]].append((index[dst], count / denominator))

    v = [1.0 / len(nodes)] * len(nodes)
    rho = 0.0
    for _ in range(iterations):
        w = [0.0] * len(nodes)
        for src_index, row in enumerate(outgoing):
            mass = v[src_index]
            if mass == 0.0:
                continue
            for dst_index, probability in row:
                w[dst_index] += mass * probability
        norm = max(abs(value) for value in w)
        if norm == 0.0:
            return 0.0
        w = [value / norm for value in w]
        if max(abs(a - b) for a, b in zip(w, v)) < tolerance:
            return norm
        v = w
        rho = norm
    return rho


def write_edge_csv(
    path: Path,
    internal: Counter[tuple[str, str]],
    source_events: Counter[str],
) -> None:
    rows: list[dict[str, object]] = []
    sources_with_outgoing = {src for src, _ in internal}
    for (src, dst), count in internal.most_common():
        denominator = source_events[src]
        probability = count / denominator
        rows.append(
            {
                "src": src,
                "dst": dst,
                "count": count,
                "source_events": denominator,
                "deterministic_probability": probability,
                "empirical_probability": probability,
            }
        )
    for src in sorted(set(source_events) - sources_with_outgoing):
        rows.append(
            {
                "src": src,
                "dst": src,
                "count": 0,
                "source_events": source_events[src],
                "deterministic_probability": 0.0,
                "empirical_probability": 0.0,
            }
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "src",
            "dst",
            "count",
            "source_events",
            "deterministic_probability",
            "empirical_probability",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_coverage_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "node",
            "K",
            "L",
            "b",
            "total_lift_classes",
            "canonical_source_classes",
            "shadowed_initial_classes",
            "no_initial_classes",
            "internal_hit_classes",
            "external_hit_classes",
            "below_start_classes",
            "budget_classes",
            "max_steps_observed",
            "max_bit_length_observed",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, manifest: dict[str, object]) -> None:
    coverage = manifest["coverage"]
    lines = [
        "# Deterministic K0=16 SCC Residue-Cell Transfer",
        "",
        "This run replaces the sampled orbit-harness transition counts with",
        "deterministic enumeration of all finite residue cells in the declared",
        "scope.",
        "",
        "## Scope",
        "",
        f"- SCC rank: `{manifest['scc_rank']}`",
        f"- raw SCC source nodes: `{coverage['source_nodes']}`",
        f"- lift bits: `{manifest['lift_bits']}`",
        f"- finite lift classes per source: `{coverage['lift_classes_per_source']}`",
        f"- total finite lift classes checked: `{coverage['total_lift_classes']}`",
        f"- canonical source classes: `{coverage['canonical_source_classes']}`",
        f"- shadowed initial classes: `{coverage['shadowed_initial_classes']}`",
        f"- no-initial classes: `{coverage['no_initial_classes']}`",
        f"- budget exits: `{coverage['budget_classes']}`",
        "",
        "The enumeration is finite and explicit: every row of the coverage CSV",
        "sums to `2^lift_bits` classes for its raw SCC source node.",
        "",
        "## Transfer Matrices",
        "",
        "| mode | states | nonzero internal edge types | source events | internal hits | exits | retention mass | rho diagnostic |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode, summary in manifest["modes"].items():
        lines.append(
            "| {mode} | {states} | {edge_types} | {source_events} | {internal} | "
            "{exits} | {retention:.6f} | {rho:.12g} |".format(mode=mode, **summary)
        )
    lines.extend(
        [
            "",
            "The edge CSVs store exact rational probabilities as",
            "`count/source_events`; the decimal probability columns are only",
            "legacy-readable diagnostics.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> dict[str, object]:
    reps = read_representatives(args.representatives, args.max_k)
    _, by_bits = build_monitors(reps)
    rep_by_key = {rep.key: rep for rep in reps}
    sources = read_scc_source_nodes(args.scc_nodes, args.scc_rank, rep_by_key)
    scc_node_set = {source.node for source in sources}
    lift_classes = 1 << args.lift_bits

    coverage_rows: list[dict[str, object]] = []
    mode_internal: dict[str, Counter[tuple[str, str]]] = {
        mode: Counter() for mode in args.modes
    }
    mode_sources: dict[str, Counter[str]] = {mode: Counter() for mode in args.modes}

    global_counts = Counter()
    for source in sources:
        node_counts = Counter()
        max_steps_observed = 0
        max_bit_length_observed = 0
        for t in range(lift_classes):
            n0, _, _ = source_start(source.rep, source.b, t)
            initial = best_hit(n0, by_bits)
            if initial is None:
                node_counts["no_initial"] += 1
                global_counts["no_initial_classes"] += 1
                continue

            initial_rep, initial_b, _ = initial
            if raw_node(initial_rep, initial_b) != source.node:
                node_counts["shadowed_initial"] += 1
                global_counts["shadowed_initial_classes"] += 1
                continue

            node_counts["canonical_source"] += 1
            global_counts["canonical_source_classes"] += 1
            outcome = next_distinct_hit(source, t, by_bits, args.max_steps)
            max_steps_observed = max(max_steps_observed, outcome.steps)
            max_bit_length_observed = max(max_bit_length_observed, outcome.max_bit_length)

            for mode in args.modes:
                src_macro = node_macro(source.node, mode)
                mode_sources[mode][src_macro] += 1

            if outcome.status == "hit" and outcome.dst_node in scc_node_set:
                node_counts["internal_hit"] += 1
                global_counts["internal_hit_classes"] += 1
                assert outcome.dst_node is not None
                for mode in args.modes:
                    src_macro = node_macro(source.node, mode)
                    dst_macro = node_macro(outcome.dst_node, mode)
                    mode_internal[mode][(src_macro, dst_macro)] += 1
            elif outcome.status == "hit":
                node_counts["external_hit"] += 1
                global_counts["external_hit_classes"] += 1
            elif outcome.status == "below":
                node_counts["below_start"] += 1
                global_counts["below_start_classes"] += 1
            elif outcome.status == "budget":
                node_counts["budget"] += 1
                global_counts["budget_classes"] += 1
            else:
                raise ValueError(outcome.status)

        coverage_rows.append(
            {
                "node": source.node,
                "K": source.rep.K,
                "L": source.rep.L,
                "b": source.b,
                "total_lift_classes": lift_classes,
                "canonical_source_classes": node_counts["canonical_source"],
                "shadowed_initial_classes": node_counts["shadowed_initial"],
                "no_initial_classes": node_counts["no_initial"],
                "internal_hit_classes": node_counts["internal_hit"],
                "external_hit_classes": node_counts["external_hit"],
                "below_start_classes": node_counts["below_start"],
                "budget_classes": node_counts["budget"],
                "max_steps_observed": max_steps_observed,
                "max_bit_length_observed": max_bit_length_observed,
            }
        )

    coverage_path = args.out_prefix.with_name(f"{args.out_prefix.name}_source_coverage.csv")
    write_coverage_csv(coverage_path, coverage_rows)

    mode_summaries: dict[str, dict[str, object]] = {}
    for mode in args.modes:
        edge_path = args.out_prefix.with_name(f"{args.out_prefix.name}_{mode}_edges.csv")
        internal = mode_internal[mode]
        source_events = mode_sources[mode]
        write_edge_csv(edge_path, internal, source_events)
        source_total = sum(source_events.values())
        internal_total = sum(internal.values())
        exits = source_total - internal_total
        states = len(set(source_events) | {dst for _, dst in internal})
        mode_summaries[mode] = {
            "edge_csv": str(edge_path),
            "states": states,
            "edge_types": len(internal),
            "source_events": source_total,
            "internal": internal_total,
            "exits": exits,
            "retention": internal_total / source_total if source_total else 0.0,
            "rho": spectral_radius_from_counts(internal, source_events),
        }

    total_lift_classes = len(sources) * lift_classes
    manifest: dict[str, object] = {
        "representatives": str(args.representatives),
        "scc_nodes": str(args.scc_nodes),
        "scc_rank": args.scc_rank,
        "max_k": args.max_k,
        "lift_bits": args.lift_bits,
        "max_steps": args.max_steps,
        "coverage_csv": str(coverage_path),
        "coverage": {
            "source_nodes": len(sources),
            "lift_classes_per_source": lift_classes,
            "total_lift_classes": total_lift_classes,
            "canonical_source_classes": global_counts["canonical_source_classes"],
            "shadowed_initial_classes": global_counts["shadowed_initial_classes"],
            "no_initial_classes": global_counts["no_initial_classes"],
            "internal_hit_classes": global_counts["internal_hit_classes"],
            "external_hit_classes": global_counts["external_hit_classes"],
            "below_start_classes": global_counts["below_start_classes"],
            "budget_classes": global_counts["budget_classes"],
        },
        "modes": mode_summaries,
    }

    report_path = args.out_prefix.with_name(f"{args.out_prefix.name}_transfer_summary.md")
    manifest_path = args.out_prefix.with_name(f"{args.out_prefix.name}_manifest.json")
    manifest["manifest_json"] = str(manifest_path)
    write_report(report_path, manifest)
    manifest["transfer_summary_md"] = str(report_path)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--representatives",
        type=Path,
        default=Path("scripts/phantom_taxonomy/phantom_representatives_k3_16.csv"),
    )
    parser.add_argument(
        "--scc-nodes",
        type=Path,
        default=Path("scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_nodes.csv"),
    )
    parser.add_argument("--scc-rank", type=int, default=1)
    parser.add_argument("--max-k", type=int, default=16)
    parser.add_argument("--lift-bits", type=int, default=4)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument(
        "--modes",
        nargs="+",
        choices=["node", "KL", "K"],
        default=["node", "KL", "K"],
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("scripts/phantom_taxonomy/deterministic_k16_s16_residue"),
    )
    parser.add_argument(
        "--allow-budget-exits",
        action="store_true",
        help="write outputs even if some residue cells hit the step budget",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = run(args)
    coverage = manifest["coverage"]
    print(f"manifest={manifest['manifest_json']}")
    print(f"coverage={manifest['coverage_csv']}")
    print(f"report={manifest['transfer_summary_md']}")
    print(f"source_nodes={coverage['source_nodes']}")
    print(f"total_lift_classes={coverage['total_lift_classes']}")
    print(f"canonical_source_classes={coverage['canonical_source_classes']}")
    print(f"shadowed_initial_classes={coverage['shadowed_initial_classes']}")
    print(f"budget_classes={coverage['budget_classes']}")
    for mode, summary in manifest["modes"].items():
        print(
            f"{mode}: states={summary['states']} edge_types={summary['edge_types']} "
            f"source_events={summary['source_events']} exits={summary['exits']} "
            f"retention={summary['retention']:.6f} rho={summary['rho']:.12g}"
        )
    if coverage["budget_classes"] and not args.allow_budget_exits:
        raise SystemExit("budget exits remain; increase --max-steps or pass --allow-budget-exits")


if __name__ == "__main__":
    main()
