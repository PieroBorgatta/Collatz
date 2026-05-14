"""
99_error_budget_summary.py

Aggregate the named Phase-10 error-budget diagnostics from the output of
88_cylinder_signature_stability.py.

This script does not trace orbits and does not compute a spectral radius.
It only reports finite proxies for the terms named in
notes/phase10_error_decomposition.md:

  DeltaTail_global, DeltaTail_local,
  A_phase_block, A_label_bounded, BoundaryError.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_DISTS = ROOT / "collatz_88_signature_distribution.csv"
OUT_REPORT = ROOT / "collatz_99_error_budget_summary.md"
OUT_CSV = ROOT / "collatz_99_error_budget_summary.csv"


DistKey = tuple[int, int, int, str]


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_CSV
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_99_{safe}_error_budget_summary"
    return ROOT / f"{stem}.md", ROOT / f"{stem}.csv"


def parse_int_list(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


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


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_delta_signature(signature: str) -> int | None:
    if signature == "terminal":
        return None
    prefix = "return|"
    if not signature.startswith(prefix):
        raise ValueError(f"unexpected delta signature: {signature}")
    return int(signature[len(prefix):])


def parse_full_signature(signature: str) -> tuple[str, tuple[str, ...], int | None]:
    if signature == "terminal":
        return "terminal", (), None
    parts = tuple(signature.split("|"))
    if len(parts) != 5 or parts[0] != "return":
        raise ValueError(f"unexpected full signature: {signature}")
    return "return", parts[1:4], int(parts[4])


def transform_full_signature(signature: str, transform: str) -> str:
    status, phase, delta = parse_full_signature(signature)
    if status == "terminal":
        return "terminal"
    if transform == "phase":
        return "return|" + "|".join(phase)
    if transform == "full":
        return signature
    if transform.startswith("clip_"):
        cutoff = int(transform.removeprefix("clip_"))
        assert delta is not None
        if delta > cutoff:
            return "return|" + "|".join(phase) + f"|tail>{cutoff}"
        return signature
    raise ValueError(f"unknown transform: {transform}")


def total_variation(counter_a: Counter, counter_b: Counter) -> float:
    total_a = sum(counter_a.values())
    total_b = sum(counter_b.values())
    if total_a == 0 and total_b == 0:
        return 0.0
    if total_a == 0 or total_b == 0:
        return 1.0
    keys = set(counter_a) | set(counter_b)
    return 0.5 * sum(abs(counter_a[key] / total_a - counter_b[key] / total_b) for key in keys)


def summarize_delta_tails(args: argparse.Namespace, cutoffs: list[int]) -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]]]:
    by_group: dict[tuple[int, int], Counter] = defaultdict(Counter)
    global_weight: Counter = Counter()
    total_return_weight = 0.0

    with Path(args.distributions).open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if row["mode"] != "prefix":
                continue
            if row["signature_level"] != "delta":
                continue
            if int(row["T"]) != args.T:
                continue
            if int(row["j_start"]) != 0:
                continue
            if int(row["j_count"]) != args.prefix_j_count:
                continue
            delta = parse_delta_signature(row["signature"])
            if delta is None:
                continue
            r = int(row["r"])
            h = int(row["h"])
            weight = float(row["weight_sum"])
            by_group[(r, h)][delta] += weight
            global_weight[delta] += weight
            total_return_weight += weight

    if not by_group:
        raise SystemExit("no matching prefix delta distributions found")

    rows: list[dict[str, Any]] = []
    by_cutoff: dict[int, dict[str, Any]] = {}
    for cutoff in cutoffs:
        tail_weight = sum(weight for delta, weight in global_weight.items() if delta > cutoff)
        group_fractions: list[float] = []
        groups_with_tail = 0
        for weights in by_group.values():
            group_total = sum(weights.values())
            if group_total <= 0:
                continue
            group_tail = sum(weight for delta, weight in weights.items() if delta > cutoff)
            fraction = group_tail / group_total
            group_fractions.append(fraction)
            if fraction > 0:
                groups_with_tail += 1
        record = {
            "term": "DeltaTail",
            "parameter": f"L={cutoff}",
            "global_tail": tail_weight / total_return_weight if total_return_weight else 0.0,
            "local_mean": mean(group_fractions) if group_fractions else 0.0,
            "local_p95": quantile(group_fractions, 0.95),
            "local_p99": quantile(group_fractions, 0.99),
            "local_max": max(group_fractions) if group_fractions else 0.0,
            "groups_with_tail": groups_with_tail,
            "groups": len(group_fractions),
        }
        by_cutoff[cutoff] = record
        rows.append(record)
    return rows, by_cutoff


def load_block_distributions(args: argparse.Namespace, transforms: list[str]):
    dists: dict[DistKey, Counter] = defaultdict(Counter)
    starts: set[int] = set()
    groups: set[tuple[int, int]] = set()

    with Path(args.distributions).open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if row["mode"] != "block":
                continue
            if row["signature_level"] != "full":
                continue
            if int(row["T"]) != args.T:
                continue
            if int(row["j_count"]) != args.block_size:
                continue
            r = int(row["r"])
            h = int(row["h"])
            start = int(row["j_start"])
            count = int(row["count"])
            starts.add(start)
            groups.add((r, h))
            for transform in transforms:
                label = transform_full_signature(row["signature"], transform)
                dists[(r, h, start, transform)][label] += count
    if not starts:
        raise SystemExit("no matching block full-signature distributions found")
    return sorted(starts), groups, dists


def summarize_block_terms(args: argparse.Namespace, cutoffs: list[int]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    transforms = ["phase"] + [f"clip_{cutoff}" for cutoff in cutoffs] + ["full"]
    starts, groups, dists = load_block_distributions(args, transforms)
    pairs = list(zip(starts, starts[1:]))
    if not pairs:
        raise SystemExit("need at least two block starts")

    phase_values: list[float] = []
    label_values: dict[str, list[float]] = defaultdict(list)
    excess_values: dict[str, list[float]] = defaultdict(list)
    complete_groups = 0
    skipped_groups = 0

    for r, h in sorted(groups):
        if not all((r, h, start, "full") in dists for start in starts):
            skipped_groups += 1
            continue
        complete_groups += 1
        for a, b in pairs:
            phase_tv = total_variation(dists[(r, h, a, "phase")], dists[(r, h, b, "phase")])
            phase_values.append(phase_tv)
            for transform in transforms:
                if transform == "phase":
                    continue
                label_tv = total_variation(dists[(r, h, a, transform)], dists[(r, h, b, transform)])
                label_values[transform].append(label_tv)
                excess_values[transform].append(max(0.0, label_tv - phase_tv))

    rows: list[dict[str, Any]] = [
        {
            "term": "A_phase_block",
            "parameter": f"block={args.block_size}",
            "mean": mean(phase_values) if phase_values else 0.0,
            "p95": quantile(phase_values, 0.95),
            "p99": quantile(phase_values, 0.99),
            "max": max(phase_values) if phase_values else 0.0,
            "weak_l1_bound_proxy": 2.0 * (mean(phase_values) if phase_values else 0.0),
            "sup_bound_proxy": 2.0 * (max(phase_values) if phase_values else 0.0),
            "samples": len(phase_values),
        }
    ]

    for transform in [f"clip_{cutoff}" for cutoff in cutoffs] + ["full"]:
        values = label_values[transform]
        excess = excess_values[transform]
        rows.append({
            "term": "A_label_tv",
            "parameter": transform,
            "mean": mean(values) if values else 0.0,
            "p95": quantile(values, 0.95),
            "p99": quantile(values, 0.99),
            "max": max(values) if values else 0.0,
            "weak_l1_bound_proxy": 2.0 * (mean(values) if values else 0.0),
            "sup_bound_proxy": 2.0 * (max(values) if values else 0.0),
            "samples": len(values),
        })
        rows.append({
            "term": "A_label_bounded",
            "parameter": transform,
            "mean": mean(excess) if excess else 0.0,
            "p95": quantile(excess, 0.95),
            "p99": quantile(excess, 0.99),
            "max": max(excess) if excess else 0.0,
            "weak_l1_bound_proxy": 2.0 * (mean(excess) if excess else 0.0),
            "sup_bound_proxy": 2.0 * (max(excess) if excess else 0.0),
            "positive_fraction": sum(1 for value in excess if value > 0) / len(excess) if excess else 0.0,
            "samples": len(excess),
        })

    boundary = {
        "block_starts": starts,
        "pairs": pairs,
        "complete_groups": complete_groups,
        "skipped_groups": skipped_groups,
        "group_count": len(groups),
    }
    rows.append({
        "term": "BoundaryError",
        "parameter": f"block={args.block_size}",
        "complete_groups": complete_groups,
        "skipped_groups": skipped_groups,
        "skipped_fraction": skipped_groups / len(groups) if groups else 0.0,
    })
    return rows, boundary


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def build_report(args: argparse.Namespace, cutoffs: list[int], rows: list[dict[str, Any]], delta_by_cutoff: dict[int, dict[str, Any]], boundary: dict[str, Any]) -> str:
    phase_rows = [row for row in rows if row["term"] == "A_phase_block"]
    label_excess_rows = [row for row in rows if row["term"] == "A_label_bounded"]
    label_tv_rows = [row for row in rows if row["term"] == "A_label_tv"]

    lines = [
        "# Phase 10 Error-Budget Summary",
        "",
        "Status: finite diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- distributions file: `{args.distributions}`",
        f"- T: `{args.T}`",
        f"- prefix j_count for tails: `{args.prefix_j_count}`",
        f"- block size for TV: `{args.block_size}`",
        f"- cutoffs: `{','.join(str(cutoff) for cutoff in cutoffs)}`",
        f"- block starts: `{', '.join(str(x) for x in boundary['block_starts'])}`",
        f"- adjacent pairs: `{', '.join(f'{a}->{b}' for a, b in boundary['pairs'])}`",
        "",
        "## DeltaTail Terms",
        "",
        "| L | global tail | local mean | local p95 | local p99 | local max | groups with tail | groups |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cutoff in cutoffs:
        row = delta_by_cutoff[cutoff]
        lines.append(
            f"| {cutoff} | {row['global_tail']:.6g} | {row['local_mean']:.6g} | "
            f"{row['local_p95']:.6g} | {row['local_p99']:.6g} | {row['local_max']:.6g} | "
            f"{row['groups_with_tail']} | {row['groups']} |"
        )

    lines.extend([
        "",
        "## Block Terms",
        "",
        "| term | parameter | mean | p95 | p99 | max | weak L1 proxy | sup proxy | extra |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in phase_rows:
        lines.append(
            f"| `{row['term']}` | `{row['parameter']}` | {row['mean']:.6g} | "
            f"{row['p95']:.6g} | {row['p99']:.6g} | {row['max']:.6g} | "
            f"{row['weak_l1_bound_proxy']:.6g} | {row['sup_bound_proxy']:.6g} | "
            f"{row['samples']} samples |"
        )
    for row in label_tv_rows:
        lines.append(
            f"| `{row['term']}` | `{row['parameter']}` | {row['mean']:.6g} | "
            f"{row['p95']:.6g} | {row['p99']:.6g} | {row['max']:.6g} | "
            f"{row['weak_l1_bound_proxy']:.6g} | {row['sup_bound_proxy']:.6g} | "
            f"{row['samples']} samples |"
        )
    for row in label_excess_rows:
        lines.append(
            f"| `{row['term']}` | `{row['parameter']}` | {row['mean']:.6g} | "
            f"{row['p95']:.6g} | {row['p99']:.6g} | {row['max']:.6g} | "
            f"{row['weak_l1_bound_proxy']:.6g} | {row['sup_bound_proxy']:.6g} | "
            f"positive {row['positive_fraction']:.6g} |"
        )

    lines.extend([
        "",
        "## Boundary Term",
        "",
        f"- complete groups: `{boundary['complete_groups']}`",
        f"- skipped incomplete groups: `{boundary['skipped_groups']}`",
        f"- total groups seen in block distributions: `{boundary['group_count']}`",
        "",
        "## Interpretation",
        "",
        "These numbers are finite proxies for the named error-budget terms.",
        "`weak L1 proxy` is `2 * mean TV`, motivated by the finite row-TV",
        "bridge for bounded observables under uniform source-cell averaging.",
        "`sup proxy` is `2 * max TV`.  These are still not operator-norm",
        "bounds for the infinite problem: p95 values require a separate",
        "exceptional-mass argument, and no projection to an infinite operator",
        "is implied.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate Phase-10 named error-budget diagnostics.")
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=15)
    parser.add_argument("--prefix-j-count", type=int, default=64)
    parser.add_argument("--block-size", type=int, default=32)
    parser.add_argument("--cutoffs", default="2,3,4,5,8")
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cutoffs = parse_int_list(args.cutoffs)
    delta_rows, delta_by_cutoff = summarize_delta_tails(args, cutoffs)
    block_rows, boundary = summarize_block_terms(args, cutoffs)
    rows = delta_rows + block_rows
    report = build_report(args, cutoffs, rows, delta_by_cutoff, boundary)
    report_path, csv_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(rows, csv_path)

    print("=" * 118)
    print("  Phase 10 error-budget summary")
    print("=" * 118)
    print(f"  T={args.T}, prefix_j_count={args.prefix_j_count}, block_size={args.block_size}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {csv_path.name}")


if __name__ == "__main__":
    main()
