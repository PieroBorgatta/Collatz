"""
93_delta_tail_weight.py

Summarize weighted delta tails in the output of
88_cylinder_signature_stability.py.

This is a Gate-10.B/10.C diagnostic only.  It does not trace orbits and
does not compute any spectral-radius estimate.  The goal is to measure
whether the return-exponent label delta has a small weighted tail after
the 2^{-delta} normalization already present in script 88.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GROUPS = ROOT / "collatz_88_cylinder_group_summary.csv"
DEFAULT_DISTS = ROOT / "collatz_88_signature_distribution.csv"
OUT_REPORT = ROOT / "collatz_93_delta_tail_weight_report.md"
OUT_BY_DELTA = ROOT / "collatz_93_delta_tail_weight_by_delta.csv"
OUT_THRESHOLDS = ROOT / "collatz_93_delta_tail_weight_thresholds.csv"
OUT_WORST = ROOT / "collatz_93_delta_tail_weight_worst_groups.csv"


GroupKey = tuple[str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_DELTA, OUT_THRESHOLDS, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_93_{safe}_delta_tail_weight"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_by_delta.csv",
        ROOT / f"{stem}_thresholds.csv",
        ROOT / f"{stem}_worst_groups.csv",
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


def parse_delta_signature(signature: str) -> int | None:
    if signature == "terminal":
        return None
    prefix = "return|"
    if not signature.startswith(prefix):
        raise ValueError(f"unexpected delta signature: {signature}")
    return int(signature[len(prefix):])


def load_matching_groups(args: argparse.Namespace) -> dict[GroupKey, dict[str, Any]]:
    rows = read_csv(Path(args.groups))
    groups: dict[GroupKey, dict[str, Any]] = {}
    for row in rows:
        if row["mode"] != "prefix":
            continue
        if int(row["j_count"]) != args.j_count:
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        if not args.include_boundary and row["boundary_flag"] != "bulk":
            continue
        key = (row["T"], row["r"], row["h"])
        groups[key] = {
            "T": row["T"],
            "r": row["r"],
            "h": row["h"],
            "source_phase": row["source_phase"],
            "sample_count": int(row["sample_count"]),
            "return_fraction": float(row["return_fraction"]),
            "phase_majority_fraction": float(row["phase_majority_fraction"]),
            "delta_majority_fraction": float(row["delta_majority_fraction"]),
            "full_majority_fraction": float(row["full_majority_fraction"]),
            "full_weight": float(row["full_weight"]),
            "by_delta": defaultdict(float),
            "by_delta_count": Counter(),
            "terminal_count": 0,
        }
    if not groups:
        raise SystemExit("no matching prefix groups found")
    return groups


def stream_delta_distributions(args: argparse.Namespace, groups: dict[GroupKey, dict[str, Any]]) -> None:
    with Path(args.distributions).open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if row["mode"] != "prefix":
                continue
            if int(row["j_count"]) != args.j_count:
                continue
            if row["signature_level"] != "delta":
                continue
            if args.T is not None and int(row["T"]) != args.T:
                continue
            key = (row["T"], row["r"], row["h"])
            if key not in groups:
                continue
            delta = parse_delta_signature(row["signature"])
            count = int(row["count"])
            weight = float(row["weight_sum"])
            if delta is None:
                groups[key]["terminal_count"] += count
                continue
            groups[key]["by_delta"][delta] += weight
            groups[key]["by_delta_count"][delta] += count


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    groups = load_matching_groups(args)
    stream_delta_distributions(args, groups)

    global_weight = Counter()
    global_count = Counter()
    total_terminal_count = 0
    total_sample_count = 0
    return_groups = []

    for row in groups.values():
        total_terminal_count += row["terminal_count"]
        total_sample_count += row["sample_count"]
        group_return_weight = sum(row["by_delta"].values())
        row["return_weight"] = group_return_weight
        if group_return_weight > 0:
            return_groups.append(row)
        for delta, weight in row["by_delta"].items():
            global_weight[delta] += weight
        for delta, count in row["by_delta_count"].items():
            global_count[delta] += count

    total_weight = sum(global_weight.values())
    total_return_count = sum(global_count.values())
    max_delta_seen = max(global_weight) if global_weight else 0
    max_threshold = max(args.max_threshold, max_delta_seen)

    by_delta_rows: list[dict[str, Any]] = []
    cumulative_weight = 0.0
    cumulative_count = 0
    for delta in range(max_delta_seen + 1):
        weight = float(global_weight.get(delta, 0.0))
        count = int(global_count.get(delta, 0))
        cumulative_weight += weight
        cumulative_count += count
        by_delta_rows.append({
            "delta": delta,
            "count": count,
            "count_fraction": count / total_return_count if total_return_count else 0.0,
            "weight_sum": weight,
            "weight_fraction": weight / total_weight if total_weight else 0.0,
            "cumulative_count_fraction": cumulative_count / total_return_count if total_return_count else 0.0,
            "cumulative_weight_fraction": cumulative_weight / total_weight if total_weight else 0.0,
        })

    threshold_rows: list[dict[str, Any]] = []
    group_tail_by_threshold: dict[int, list[tuple[float, dict[str, Any]]]] = {}
    for threshold in range(max_threshold + 1):
        retained_weight = sum(weight for delta, weight in global_weight.items() if delta <= threshold)
        tail_weight = total_weight - retained_weight
        retained_count = sum(count for delta, count in global_count.items() if delta <= threshold)
        tail_count = total_return_count - retained_count
        group_tails: list[tuple[float, dict[str, Any]]] = []
        for row in return_groups:
            row_tail = sum(weight for delta, weight in row["by_delta"].items() if delta > threshold)
            fraction = row_tail / row["return_weight"] if row["return_weight"] else 0.0
            group_tails.append((fraction, row))
        fractions = [fraction for fraction, _row in group_tails]
        group_tail_by_threshold[threshold] = sorted(group_tails, key=lambda item: item[0], reverse=True)
        threshold_rows.append({
            "threshold_delta": threshold,
            "retained_count": retained_count,
            "tail_count": tail_count,
            "tail_count_fraction": tail_count / total_return_count if total_return_count else 0.0,
            "retained_weight": retained_weight,
            "tail_weight": tail_weight,
            "tail_weight_fraction": tail_weight / total_weight if total_weight else 0.0,
            "return_groups": len(return_groups),
            "group_tail_mean": mean(fractions) if fractions else 0.0,
            "group_tail_p95": quantile(fractions, 0.95),
            "group_tail_max": max(fractions) if fractions else 0.0,
            "groups_with_tail": sum(1 for fraction in fractions if fraction > 0),
        })

    worst_threshold = min(args.worst_threshold, max_threshold)
    worst_rows: list[dict[str, Any]] = []
    for fraction, row in group_tail_by_threshold.get(worst_threshold, [])[:args.limit]:
        worst_rows.append({
            "T": row["T"],
            "r": row["r"],
            "h": row["h"],
            "source_phase": row["source_phase"],
            "return_weight": row["return_weight"],
            "tail_fraction": fraction,
            "phase_majority_fraction": row["phase_majority_fraction"],
            "delta_majority_fraction": row["delta_majority_fraction"],
            "full_majority_fraction": row["full_majority_fraction"],
            "delta_weight_profile": ", ".join(
                f"{delta}:{weight:.6g}" for delta, weight in sorted(row["by_delta"].items())
            ),
        })

    active_T = sorted({row["T"] for row in groups.values()}, key=int)
    active_h = sorted({row["h"] for row in groups.values()}, key=int)
    return_group_fraction = len(return_groups) / len(groups) if groups else 0.0
    terminal_fraction = total_terminal_count / total_sample_count if total_sample_count else 0.0

    lines = [
        "# Delta Tail Weight Diagnostic",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- distributions file: `{args.distributions}`",
        f"- T filter: `{args.T if args.T is not None else 'all'}`",
        f"- active T values: `{', '.join(active_T)}`",
        f"- j_count: `{args.j_count}`",
        f"- include boundary: `{args.include_boundary}`",
        "",
        "## Aggregate",
        "",
        f"- groups: `{len(groups)}`",
        f"- h values: `{', '.join(active_h)}`",
        f"- groups with nonzero return weight: `{len(return_groups)}`",
        f"- nonzero-return group fraction: `{return_group_fraction:.6g}`",
        f"- total sample count: `{total_sample_count}`",
        f"- terminal count fraction: `{terminal_fraction:.6g}`",
        f"- return count: `{total_return_count}`",
        f"- weighted return mass: `{total_weight:.12g}`",
        f"- max delta observed: `{max_delta_seen}`",
        "",
        "Here `weight_sum` is the weight already emitted by script 88, i.e.",
        "the return contribution normalized by `2^{-delta}`.  Terminal rows",
        "have zero return weight in this diagnostic.",
        "",
        "## Delta Weight Distribution",
        "",
        "| delta | count fraction | weight fraction | cumulative weight fraction |",
        "|---:|---:|---:|---:|",
    ]
    for row in by_delta_rows:
        lines.append(
            f"| {row['delta']} | "
            f"{row['count_fraction']:.6g} | "
            f"{row['weight_fraction']:.6g} | "
            f"{row['cumulative_weight_fraction']:.6g} |"
        )

    lines.extend([
        "",
        "## Tail Thresholds",
        "",
        "| keep delta <= L | tail count frac | tail weight frac | group tail mean | group tail p95 | group tail max | groups with tail |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in threshold_rows:
        if row["threshold_delta"] <= args.max_threshold or row["threshold_delta"] == max_delta_seen:
            lines.append(
                f"| {row['threshold_delta']} | "
                f"{row['tail_count_fraction']:.6g} | "
                f"{row['tail_weight_fraction']:.6g} | "
                f"{row['group_tail_mean']:.6g} | "
                f"{row['group_tail_p95']:.6g} | "
                f"{row['group_tail_max']:.6g} | "
                f"{row['groups_with_tail']} |"
            )

    lines.extend([
        "",
        f"## Worst Groups for L = {worst_threshold}",
        "",
        "| T | r | h | tail frac | return weight | phase maj | delta maj | full maj | delta weights |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ])
    for row in worst_rows:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | "
            f"{row['tail_fraction']:.6g} | "
            f"{row['return_weight']:.6g} | "
            f"{row['phase_majority_fraction']:.6g} | "
            f"{row['delta_majority_fraction']:.6g} | "
            f"{row['full_majority_fraction']:.6g} | "
            f"`{row['delta_weight_profile']}` |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "A small global weighted delta tail would support a Banach model with",
        "an explicit return-exponent tail weight.  It would not by itself",
        "identify a canonical infinite operator, prove compactness, prove",
        "Lasota-Yorke, or justify the finite matrices as exact projections.",
        "",
        "If the group-level tail p95 or max remains large at feasible L, then",
        "a finite labelled quotient is not resolving the obstruction uniformly;",
        "one should treat the labelled countable-state or finite-rank fallback",
        "branches as the safer mathematical alternatives.",
    ])
    return "\n".join(lines) + "\n", by_delta_rows, threshold_rows, worst_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize weighted delta tails in script 88 outputs.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--j-count", type=int, default=8)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--max-threshold", type=int, default=8)
    parser.add_argument("--worst-threshold", type=int, default=4)
    parser.add_argument("--limit", type=int, default=16)
    parser.add_argument(
        "--output-tag",
        default=None,
        help="optional filename tag used to keep multiple 93 outputs side by side",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, by_delta_rows, threshold_rows, worst_rows = summarize(args)
    report_path, by_delta_path, thresholds_path, worst_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(by_delta_rows, by_delta_path)
    write_csv(threshold_rows, thresholds_path)
    write_csv(worst_rows, worst_path)
    print("=" * 118)
    print("  Delta tail weight diagnostic")
    print("=" * 118)
    print(f"  T={args.T if args.T is not None else 'all'}, j_count={args.j_count}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {by_delta_path.name}")
    print(f"    {thresholds_path.name}")
    print(f"    {worst_path.name}")


if __name__ == "__main__":
    main()
