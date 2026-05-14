"""
97_truncated_label_block_tv.py

Compute adjacent-block TV after truncating the full return label
(destination phase, delta) by a delta cutoff.

This probes whether the mixed norm can be weaker than full-signature TV
while still retaining destination phase and bounded delta labels.  It
uses the distribution CSV emitted by 88_cylinder_signature_stability.py
and performs no orbit tracing.
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
OUT_REPORT = ROOT / "collatz_97_truncated_label_block_tv_report.md"
OUT_SUMMARY = ROOT / "collatz_97_truncated_label_block_tv_summary.csv"
OUT_WORST = ROOT / "collatz_97_truncated_label_block_tv_worst.csv"


DistKey = tuple[int, int, int, str]


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_SUMMARY, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_97_{safe}_truncated_label_block_tv"
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
    if transform == "status":
        return "return"
    if transform == "phase":
        return "return|" + "|".join(phase)
    if transform == "full":
        return signature
    prefix = "clip_"
    if transform.startswith(prefix):
        cutoff = int(transform[len(prefix):])
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


def load_block_distributions(args: argparse.Namespace, transforms: list[str]):
    count_dists: dict[DistKey, Counter] = defaultdict(Counter)
    weight_dists: dict[DistKey, Counter] = defaultdict(Counter)
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
            j_start = int(row["j_start"])
            r = int(row["r"])
            h = int(row["h"])
            signature = row["signature"]
            count = int(row["count"])
            weight = float(row["weight_sum"])
            starts.add(j_start)
            groups.add((r, h))
            for transform in transforms:
                label = transform_signature(signature, transform)
                key = (r, h, j_start, transform)
                count_dists[key][label] += count
                weight_dists[key][label] += weight
    if not starts:
        raise SystemExit("no matching block distributions found")
    return sorted(starts), groups, count_dists, weight_dists


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    cutoffs = parse_int_list(args.cutoffs)
    transforms = ["status", "phase"] + [f"clip_{cutoff}" for cutoff in cutoffs] + ["full"]
    starts, groups, count_dists, weight_dists = load_block_distributions(args, transforms)
    pairs = list(zip(starts, starts[1:]))
    if not pairs:
        raise SystemExit("need at least two block starts for adjacent-block TV")

    values: dict[str, list[float]] = defaultdict(list)
    weight_values: dict[str, list[float]] = defaultdict(list)
    worst_rows: list[dict[str, Any]] = []

    complete_group_count = 0
    skipped_group_count = 0
    for r, h in sorted(groups):
        has_all_blocks = all((r, h, start, "full") in count_dists for start in starts)
        if not has_all_blocks:
            skipped_group_count += 1
            continue
        complete_group_count += 1
        for a, b in pairs:
            for transform in transforms:
                key_a = (r, h, a, transform)
                key_b = (r, h, b, transform)
                count_tv = total_variation(count_dists[key_a], count_dists[key_b])
                weight_tv = total_variation(weight_dists[key_a], weight_dists[key_b])
                values[transform].append(count_tv)
                weight_values[transform].append(weight_tv)
                if transform in {"full", f"clip_{args.worst_cutoff}", "phase"}:
                    worst_rows.append({
                        "T": args.T,
                        "r": r,
                        "h": h,
                        "block_a_start": a,
                        "block_b_start": b,
                        "block_size": args.block_size,
                        "transform": transform,
                        "count_tv": count_tv,
                        "weight_tv": weight_tv,
                    })

    summary_rows: list[dict[str, Any]] = []
    for transform in transforms:
        tvs = values[transform]
        wtvs = weight_values[transform]
        summary_rows.append({
            "T": args.T,
            "block_size": args.block_size,
            "transform": transform,
            "sample_count": len(tvs),
            "count_mean_tv": mean(tvs) if tvs else 0.0,
            "count_p90_tv": quantile(tvs, 0.90),
            "count_p95_tv": quantile(tvs, 0.95),
            "count_p99_tv": quantile(tvs, 0.99),
            "count_max_tv": max(tvs) if tvs else 0.0,
            "weight_mean_tv": mean(wtvs) if wtvs else 0.0,
            "weight_p90_tv": quantile(wtvs, 0.90),
            "weight_p95_tv": quantile(wtvs, 0.95),
            "weight_p99_tv": quantile(wtvs, 0.99),
            "weight_max_tv": max(wtvs) if wtvs else 0.0,
        })

    worst_rows = sorted(
        worst_rows,
        key=lambda row: (-row["count_tv"], -row["weight_tv"], row["transform"], row["r"], row["h"]),
    )[:args.limit]

    lines = [
        "# Truncated Label Block TV",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- distributions file: `{args.distributions}`",
        f"- T: `{args.T}`",
        f"- block size: `{args.block_size}`",
        f"- block starts: `{', '.join(str(x) for x in starts)}`",
        f"- adjacent pairs: `{', '.join(f'{a}->{b}' for a, b in pairs)}`",
        f"- cutoffs: `{args.cutoffs}`",
        f"- complete groups compared: `{complete_group_count}`",
        f"- groups skipped for incomplete blocks: `{skipped_group_count}`",
        "",
        "## Summary",
        "",
        "| transform | count mean TV | count p95 | count p99 | count max | weight mean TV | weight p95 | weight p99 | weight max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row['transform']}` | "
            f"{row['count_mean_tv']:.6g} | {row['count_p95_tv']:.6g} | "
            f"{row['count_p99_tv']:.6g} | {row['count_max_tv']:.6g} | "
            f"{row['weight_mean_tv']:.6g} | {row['weight_p95_tv']:.6g} | "
            f"{row['weight_p99_tv']:.6g} | {row['weight_max_tv']:.6g} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "If clipped labels have much lower TV than full labels, then the",
        "mixed norm can plausibly retain bounded delta labels and charge the",
        "rest to a tail term.  If clipping barely changes TV, then phase",
        "movement rather than delta tails is the dominant block-Cauchy",
        "obstruction.",
        "",
        "Weighted TV ignores terminal mass because terminal rows have zero",
        "return weight in the source diagnostic.  It should be interpreted",
        "only as a return-weight diagnostic, not as a complete weak norm.",
    ])
    return "\n".join(lines) + "\n", summary_rows, worst_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute block TV after truncating full labels by delta cutoff.")
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=15)
    parser.add_argument("--block-size", type=int, default=32)
    parser.add_argument("--cutoffs", default="2,3,4,5,8")
    parser.add_argument("--worst-cutoff", type=int, default=5)
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
    print("  Truncated label block TV")
    print("=" * 118)
    print(f"  T={args.T}, block_size={args.block_size}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {summary_path.name}")
    print(f"    {worst_path.name}")


if __name__ == "__main__":
    main()
