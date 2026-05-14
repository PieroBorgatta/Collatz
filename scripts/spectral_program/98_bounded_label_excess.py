"""
98_bounded_label_excess.py

Decompose adjacent-block full-label TV into destination-phase TV plus
the excess caused by bounded return labels such as delta.

This consumes the distribution CSV emitted by
88_cylinder_signature_stability.py and performs no orbit tracing.
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
OUT_REPORT = ROOT / "collatz_98_bounded_label_excess_report.md"
OUT_SUMMARY = ROOT / "collatz_98_bounded_label_excess_summary.csv"
OUT_WORST = ROOT / "collatz_98_bounded_label_excess_worst.csv"


DistKey = tuple[int, int, int, str]


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_SUMMARY, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_98_{safe}_bounded_label_excess"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_summary.csv",
        ROOT / f"{stem}_worst.csv",
    )


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
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_full_signature(signature: str) -> tuple[str, tuple[str, ...], int | None]:
    if signature == "terminal":
        return "terminal", (), None
    parts = tuple(signature.split("|"))
    if len(parts) != 5 or parts[0] != "return":
        raise ValueError(f"unexpected full signature: {signature}")
    return "return", parts[1:4], int(parts[4])


def transform_signature(signature: str, transform: str) -> str:
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


def load_distributions(args: argparse.Namespace, transforms: list[str]):
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
                dists[(r, h, start, transform)][transform_signature(row["signature"], transform)] += count
    if not starts:
        raise SystemExit("no matching distributions found")
    return sorted(starts), groups, dists


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    cutoffs = parse_int_list(args.cutoffs)
    transforms = ["phase"] + [f"clip_{cutoff}" for cutoff in cutoffs] + ["full"]
    starts, groups, dists = load_distributions(args, transforms)
    pairs = list(zip(starts, starts[1:]))
    if not pairs:
        raise SystemExit("need at least two block starts")

    records: list[dict[str, Any]] = []
    skipped = 0
    for r, h in sorted(groups):
        if not all((r, h, start, "full") in dists for start in starts):
            skipped += 1
            continue
        for a, b in pairs:
            tvs = {
                transform: total_variation(dists[(r, h, a, transform)], dists[(r, h, b, transform)])
                for transform in transforms
            }
            phase_tv = tvs["phase"]
            for transform in transforms:
                if transform == "phase":
                    continue
                records.append({
                    "T": args.T,
                    "r": r,
                    "h": h,
                    "block_a_start": a,
                    "block_b_start": b,
                    "block_size": args.block_size,
                    "transform": transform,
                    "phase_tv": phase_tv,
                    "label_tv": tvs[transform],
                    "excess_over_phase": max(0.0, tvs[transform] - phase_tv),
                })

    summary_rows: list[dict[str, Any]] = []
    for transform in [t for t in transforms if t != "phase"]:
        rows = [row for row in records if row["transform"] == transform]
        excess = [row["excess_over_phase"] for row in rows]
        label_tv = [row["label_tv"] for row in rows]
        phase_tv = [row["phase_tv"] for row in rows]
        summary_rows.append({
            "T": args.T,
            "block_size": args.block_size,
            "transform": transform,
            "sample_count": len(rows),
            "phase_mean_tv": mean(phase_tv) if phase_tv else 0.0,
            "label_mean_tv": mean(label_tv) if label_tv else 0.0,
            "excess_mean": mean(excess) if excess else 0.0,
            "excess_p90": quantile(excess, 0.90),
            "excess_p95": quantile(excess, 0.95),
            "excess_p99": quantile(excess, 0.99),
            "excess_max": max(excess) if excess else 0.0,
            "fraction_excess_positive": sum(1 for value in excess if value > 0) / len(excess) if excess else 0.0,
        })

    worst = sorted(records, key=lambda row: (-row["excess_over_phase"], -row["label_tv"], row["r"], row["h"]))[:args.limit]

    lines = [
        "# Bounded Label Excess",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- distributions file: `{args.distributions}`",
        f"- T: `{args.T}`",
        f"- block size: `{args.block_size}`",
        f"- block starts: `{', '.join(str(x) for x in starts)}`",
        f"- cutoffs: `{args.cutoffs}`",
        f"- skipped incomplete groups: `{skipped}`",
        "",
        "## Summary",
        "",
        "| transform | phase mean TV | label mean TV | excess mean | excess p95 | excess p99 | excess max | excess positive frac |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row['transform']}` | "
            f"{row['phase_mean_tv']:.6g} | {row['label_mean_tv']:.6g} | "
            f"{row['excess_mean']:.6g} | {row['excess_p95']:.6g} | "
            f"{row['excess_p99']:.6g} | {row['excess_max']:.6g} | "
            f"{row['fraction_excess_positive']:.6g} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "This measures the bounded-label penalty left after destination-phase",
        "movement is already accounted for.  A small excess would support a",
        "weak norm that treats bounded delta variation as a lower-order",
        "term.  A persistent excess means the label process itself needs",
        "regularity, not only tail control.",
    ])
    return "\n".join(lines) + "\n", summary_rows, worst


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure bounded label TV excess over phase TV.")
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=15)
    parser.add_argument("--block-size", type=int, default=32)
    parser.add_argument("--cutoffs", default="2,3,4,5,8")
    parser.add_argument("--limit", type=int, default=32)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, summary_rows, worst_rows = summarize(args)
    report_path, summary_path, worst_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(summary_rows, summary_path)
    write_csv(worst_rows, worst_path)
    print("=" * 118)
    print("  Bounded label excess")
    print("=" * 118)
    print(f"  T={args.T}, block_size={args.block_size}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {summary_path.name}")
    print(f"    {worst_path.name}")


if __name__ == "__main__":
    main()
