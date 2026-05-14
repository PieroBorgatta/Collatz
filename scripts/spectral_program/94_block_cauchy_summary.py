"""
94_block_cauchy_summary.py

Summarize adjacent-block distribution drift in the output of
88_cylinder_signature_stability.py.

This is a Gate-10.B diagnostic for a possible Cesaro/high-lift
interpretation.  It reports total-variation drift between adjacent
high-bit blocks and relates that drift to final-prefix majority
statistics.  It does not prove convergence and does not compute any
spectral radius.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GROUPS = ROOT / "collatz_88_cylinder_group_summary.csv"
DEFAULT_DRIFT = ROOT / "collatz_88_block_drift.csv"
OUT_REPORT = ROOT / "collatz_94_block_cauchy_report.md"
OUT_BY_LEVEL = ROOT / "collatz_94_block_cauchy_by_level.csv"
OUT_BY_CLASS = ROOT / "collatz_94_block_cauchy_by_class.csv"
OUT_WORST = ROOT / "collatz_94_block_cauchy_worst.csv"


GroupKey = tuple[str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_LEVEL, OUT_BY_CLASS, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_94_{safe}_block_cauchy"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_by_level.csv",
        ROOT / f"{stem}_by_class.csv",
        ROOT / f"{stem}_worst.csv",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = q * (len(ordered) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def infer_final_j(groups: list[dict[str, str]], requested: int | None) -> int:
    if requested is not None:
        return requested
    prefix_j = [int(row["j_count"]) for row in groups if row["mode"] == "prefix"]
    if not prefix_j:
        raise SystemExit("could not infer final j_count from group summary")
    return max(prefix_j)


def load_groups(args: argparse.Namespace) -> tuple[int, dict[GroupKey, dict[str, str]]]:
    rows = read_csv(Path(args.groups))
    final_j = infer_final_j(rows, args.j_count)
    groups: dict[GroupKey, dict[str, str]] = {}
    for row in rows:
        if row["mode"] != "prefix":
            continue
        if int(row["j_count"]) != final_j:
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        if not args.include_boundary and row["boundary_flag"] != "bulk":
            continue
        groups[(row["T"], row["r"], row["h"])] = row
    if not groups:
        raise SystemExit("no matching final-prefix groups found")
    return final_j, groups


def load_drift(args: argparse.Namespace, groups: dict[GroupKey, dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(args.block_drift).open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if args.T is not None and int(row["T"]) != args.T:
                continue
            key = (row["T"], row["r"], row["h"])
            group = groups.get(key)
            if group is None:
                continue
            out = dict(row)
            out["tv_distance"] = float(row["tv_distance"])
            out["dominant_changed"] = int(row["dominant_changed"])
            out["phase_majority_fraction"] = float(group["phase_majority_fraction"])
            out["delta_majority_fraction"] = float(group["delta_majority_fraction"])
            out["full_majority_fraction"] = float(group["full_majority_fraction"])
            out["status_majority_fraction"] = float(group["status_majority_fraction"])
            out["full_tail_weight_fraction"] = float(group["tail_weight_fraction"])
            out["source_phase"] = group["source_phase"]
            rows.append(out)
    if not rows:
        raise SystemExit("no matching block-drift rows found")
    return rows


def summarize_records(records: list[dict[str, Any]], label: str) -> dict[str, Any]:
    tvs = [row["tv_distance"] for row in records]
    changed = [row["dominant_changed"] for row in records]
    return {
        "class": label,
        "count": len(records),
        "mean_tv": mean(tvs) if tvs else 0.0,
        "p50_tv": quantile(tvs, 0.50),
        "p90_tv": quantile(tvs, 0.90),
        "p95_tv": quantile(tvs, 0.95),
        "p99_tv": quantile(tvs, 0.99),
        "max_tv": max(tvs) if tvs else 0.0,
        "dominant_flip_fraction": mean(changed) if changed else 0.0,
    }


def group_classes(group: dict[str, str], args: argparse.Namespace) -> list[str]:
    classes = ["all"]
    if float(group["status_majority_fraction"]) == 1.0:
        classes.append("status_exact")
    if float(group["phase_majority_fraction"]) == 1.0:
        classes.append("phase_exact")
    if float(group["full_majority_fraction"]) == 1.0:
        classes.append("full_exact")
    if float(group["phase_majority_fraction"]) <= args.low_majority:
        classes.append("phase_low")
    if float(group["full_majority_fraction"]) <= args.low_majority:
        classes.append("full_low")
    if float(group["tail_weight_fraction"]) >= args.high_tail:
        classes.append("high_full_tail_weight")
    return classes


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    final_j, groups = load_groups(args)
    drift_rows = load_drift(args, groups)

    by_level: list[dict[str, Any]] = []
    level_records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    class_level_records: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in drift_rows:
        level = row["signature_level"]
        level_records[level].append(row)
        group = groups[(row["T"], row["r"], row["h"])]
        for cls in group_classes(group, args):
            class_level_records[(cls, level)].append(row)

    for level in sorted(level_records):
        item = summarize_records(level_records[level], "all")
        item["signature_level"] = level
        by_level.append(item)

    by_class: list[dict[str, Any]] = []
    for (cls, level), records in sorted(class_level_records.items()):
        item = summarize_records(records, cls)
        item["signature_level"] = level
        by_class.append(item)

    worst = sorted(
        [row for row in drift_rows if row["signature_level"] == args.worst_level],
        key=lambda row: (
            -row["tv_distance"],
            row["dominant_changed"],
            int(row["T"]),
            int(row["r"]),
            int(row["h"]),
        ),
    )[:args.limit]
    worst_rows: list[dict[str, Any]] = []
    for row in worst:
        worst_rows.append({
            "T": row["T"],
            "r": row["r"],
            "h": row["h"],
            "signature_level": row["signature_level"],
            "block_a_start": row["block_a_start"],
            "block_b_start": row["block_b_start"],
            "block_size": row["block_size"],
            "tv_distance": row["tv_distance"],
            "dominant_a": row["dominant_a"],
            "dominant_b": row["dominant_b"],
            "dominant_changed": row["dominant_changed"],
            "phase_majority_fraction": row["phase_majority_fraction"],
            "delta_majority_fraction": row["delta_majority_fraction"],
            "full_majority_fraction": row["full_majority_fraction"],
            "full_tail_weight_fraction": row["full_tail_weight_fraction"],
            "source_phase": row["source_phase"],
        })

    active_T = sorted({row["T"] for row in drift_rows}, key=int)
    block_sizes = sorted({row["block_size"] for row in drift_rows}, key=int)
    block_pairs = sorted({(row["block_a_start"], row["block_b_start"]) for row in drift_rows}, key=lambda x: (int(x[0]), int(x[1])))

    lines = [
        "# Block-Cauchy Drift Summary",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- block drift file: `{args.block_drift}`",
        f"- T filter: `{args.T if args.T is not None else 'all'}`",
        f"- active T values: `{', '.join(active_T)}`",
        f"- final prefix j_count: `{final_j}`",
        f"- include boundary: `{args.include_boundary}`",
        f"- block sizes: `{', '.join(block_sizes)}`",
        f"- adjacent block pairs: `{', '.join(f'{a}->{b}' for a, b in block_pairs[:8])}`",
        "",
        "## Aggregate By Signature Level",
        "",
        "| level | count | mean TV | p90 | p95 | p99 | max | dominant flip frac |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in by_level:
        lines.append(
            f"| `{row['signature_level']}` | {row['count']} | "
            f"{row['mean_tv']:.6g} | {row['p90_tv']:.6g} | "
            f"{row['p95_tv']:.6g} | {row['p99_tv']:.6g} | "
            f"{row['max_tv']:.6g} | {row['dominant_flip_fraction']:.6g} |"
        )

    lines.extend([
        "",
        "## Selected Classes",
        "",
        "| class | level | count | mean TV | p95 | max | dominant flip frac |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])
    selected_classes = {"all", "status_exact", "phase_low", "full_low", "high_full_tail_weight"}
    for row in by_class:
        if row["class"] not in selected_classes:
            continue
        lines.append(
            f"| `{row['class']}` | `{row['signature_level']}` | {row['count']} | "
            f"{row['mean_tv']:.6g} | {row['p95_tv']:.6g} | "
            f"{row['max_tv']:.6g} | {row['dominant_flip_fraction']:.6g} |"
        )

    lines.extend([
        "",
        f"## Worst `{args.worst_level}` Drifts",
        "",
        "| T | r | h | TV | changed | dominant A | dominant B | phase maj | full maj | full tail weight |",
        "|---:|---:|---:|---:|---:|---|---|---:|---:|---:|",
    ])
    for row in worst_rows:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | "
            f"{row['tv_distance']:.6g} | {row['dominant_changed']} | "
            f"`{row['dominant_a']}` | `{row['dominant_b']}` | "
            f"{row['phase_majority_fraction']:.6g} | "
            f"{row['full_majority_fraction']:.6g} | "
            f"{row['full_tail_weight_fraction']:.6g} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Small adjacent-block TV would be evidence for a Cesaro/high-lift",
        "distributional model.  It is not the same as local constancy, and",
        "it does not prove convergence as block size or prefix length tends",
        "to infinity.",
        "",
        "Dominant-signature flips are stricter in one sense and weaker in",
        "another: rare flips can coexist with substantial TV drift when the",
        "same dominant signature keeps changing its mass.  Any future",
        "Keller-Liverani target should use a normed distributional error,",
        "not majority stability alone.",
    ])
    return "\n".join(lines) + "\n", by_level, by_class, worst_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize adjacent-block Cauchy diagnostics from script 88.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--block-drift", default=str(DEFAULT_DRIFT))
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--j-count", type=int, default=None)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--low-majority", type=float, default=0.5)
    parser.add_argument("--high-tail", type=float, default=0.75)
    parser.add_argument("--worst-level", default="full", choices=("status", "phase", "delta", "full"))
    parser.add_argument("--limit", type=int, default=16)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, by_level, by_class, worst_rows = summarize(args)
    report_path, by_level_path, by_class_path, worst_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(by_level, by_level_path)
    write_csv(by_class, by_class_path)
    write_csv(worst_rows, worst_path)
    print("=" * 118)
    print("  Block-Cauchy drift summary")
    print("=" * 118)
    print(f"  T={args.T if args.T is not None else 'all'}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {by_level_path.name}")
    print(f"    {by_class_path.name}")
    print(f"    {worst_path.name}")


if __name__ == "__main__":
    main()
