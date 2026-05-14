"""
95_bad_cell_stratification.py

Stratify unstable high-bit cells by source phase coordinates in the
output of 88_cylinder_signature_stability.py.

This is a Gate-10.B diagnostic only.  It asks whether phase/full
instability and weighted full-tail mass are spread uniformly or
concentrated in a small set of source-phase classes.
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
OUT_REPORT = ROOT / "collatz_95_bad_cell_stratification_report.md"
OUT_STRATA = ROOT / "collatz_95_bad_cell_stratification_strata.csv"
OUT_TOP = ROOT / "collatz_95_bad_cell_stratification_top.csv"


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_STRATA, OUT_TOP
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_95_{safe}_bad_cell_stratification"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_strata.csv",
        ROOT / f"{stem}_top.csv",
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


def infer_final_j(rows: list[dict[str, str]], requested: int | None) -> int:
    if requested is not None:
        return requested
    prefix_j = [int(row["j_count"]) for row in rows if row["mode"] == "prefix"]
    if not prefix_j:
        raise SystemExit("could not infer final j_count")
    return max(prefix_j)


def parse_source_phase(text: str) -> dict[str, int | str]:
    out: dict[str, int | str] = {"v2": "unknown", "odd": "unknown", "h": "unknown"}
    for part in text.split("|"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        out[key] = int(value)
    return out


def load_groups(args: argparse.Namespace) -> tuple[int, list[dict[str, Any]]]:
    raw_rows = read_csv(Path(args.groups))
    final_j = infer_final_j(raw_rows, args.j_count)
    rows: list[dict[str, Any]] = []
    for row in raw_rows:
        if row["mode"] != "prefix":
            continue
        if int(row["j_count"]) != final_j:
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        if not args.include_boundary and row["boundary_flag"] != "bulk":
            continue
        phase = parse_source_phase(row["source_phase"])
        enriched: dict[str, Any] = dict(row)
        enriched.update({
            "T": int(row["T"]),
            "r": int(row["r"]),
            "h_cell": int(row["h"]),
            "sample_count": int(row["sample_count"]),
            "source_v2": phase["v2"],
            "source_odd": phase["odd"],
            "source_h": phase["h"],
            "terminal_fraction": float(row["terminal_fraction"]),
            "return_fraction": float(row["return_fraction"]),
            "status_majority_fraction": float(row["status_majority_fraction"]),
            "phase_majority_fraction": float(row["phase_majority_fraction"]),
            "delta_majority_fraction": float(row["delta_majority_fraction"]),
            "full_majority_fraction": float(row["full_majority_fraction"]),
            "tail_weight_fraction": float(row["tail_weight_fraction"]),
            "phase_exact": float(row["phase_majority_fraction"]) == 1.0,
            "full_exact": float(row["full_majority_fraction"]) == 1.0,
            "status_exact": float(row["status_majority_fraction"]) == 1.0,
            "phase_low": float(row["phase_majority_fraction"]) <= args.low_majority,
            "full_low": float(row["full_majority_fraction"]) <= args.low_majority,
            "high_tail": float(row["tail_weight_fraction"]) >= args.high_tail,
        })
        rows.append(enriched)
    if not rows:
        raise SystemExit("no matching final-prefix groups found")
    return final_j, rows


def summarize_stratum(rows: list[dict[str, Any]], stratum: str, value: str) -> dict[str, Any]:
    count = len(rows)

    def frac(flag: str) -> float:
        return sum(1 for row in rows if row[flag]) / count if count else 0.0

    return {
        "stratum": stratum,
        "value": value,
        "count": count,
        "mean_terminal_fraction": mean(row["terminal_fraction"] for row in rows),
        "mean_return_fraction": mean(row["return_fraction"] for row in rows),
        "status_exact_fraction": frac("status_exact"),
        "phase_exact_fraction": frac("phase_exact"),
        "full_exact_fraction": frac("full_exact"),
        "phase_low_fraction": frac("phase_low"),
        "full_low_fraction": frac("full_low"),
        "high_tail_fraction": frac("high_tail"),
        "mean_phase_majority": mean(row["phase_majority_fraction"] for row in rows),
        "mean_delta_majority": mean(row["delta_majority_fraction"] for row in rows),
        "mean_full_majority": mean(row["full_majority_fraction"] for row in rows),
        "mean_tail_weight_fraction": mean(row["tail_weight_fraction"] for row in rows),
        "max_tail_weight_fraction": max(row["tail_weight_fraction"] for row in rows),
    }


def make_strata(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[("source_v2", str(row["source_v2"]))].append(row)
        groups[("source_odd", str(row["source_odd"]))].append(row)
        groups[("source_h", str(row["source_h"]))].append(row)
        groups[("source_v2_odd", f"{row['source_v2']}|{row['source_odd']}")].append(row)
        groups[("source_phase", row["source_phase"])].append(row)
    return [summarize_stratum(items, key[0], key[1]) for key, items in sorted(groups.items())]


def top_rows(strata: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    candidates = [row for row in strata if row["count"] >= args.min_count]
    out: list[dict[str, Any]] = []
    ranking_specs = [
        ("phase_low_fraction", True),
        ("full_low_fraction", True),
        ("high_tail_fraction", True),
        ("mean_tail_weight_fraction", True),
        ("phase_exact_fraction", False),
        ("full_exact_fraction", False),
    ]
    seen: set[tuple[str, str, str]] = set()
    for metric, reverse in ranking_specs:
        ranked = sorted(
            candidates,
            key=lambda row: (
                row[metric] if reverse else -row[metric],
                row["count"],
            ),
            reverse=True,
        )[:args.limit]
        for row in ranked:
            marker = (metric, row["stratum"], row["value"])
            if marker in seen:
                continue
            seen.add(marker)
            tagged = dict(row)
            tagged["ranking_metric"] = metric
            out.append(tagged)
    return out


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    final_j, rows = load_groups(args)
    strata = make_strata(rows)
    tops = top_rows(strata, args)

    global_row = summarize_stratum(rows, "global", "all")
    active_T = sorted({str(row["T"]) for row in rows}, key=int)

    def table_for(metric: str, title: str, reverse: bool = True) -> list[str]:
        candidates = [row for row in strata if row["count"] >= args.min_count]
        ranked = sorted(candidates, key=lambda row: row[metric], reverse=reverse)[:args.limit]
        lines = [
            "",
            f"## {title}",
            "",
            "| stratum | value | count | phase exact | full exact | phase low | full low | high tail | mean full maj | mean tail |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in ranked:
            lines.append(
                f"| `{row['stratum']}` | `{row['value']}` | {row['count']} | "
                f"{row['phase_exact_fraction']:.6g} | "
                f"{row['full_exact_fraction']:.6g} | "
                f"{row['phase_low_fraction']:.6g} | "
                f"{row['full_low_fraction']:.6g} | "
                f"{row['high_tail_fraction']:.6g} | "
                f"{row['mean_full_majority']:.6g} | "
                f"{row['mean_tail_weight_fraction']:.6g} |"
            )
        return lines

    lines = [
        "# Bad Cell Stratification",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- T filter: `{args.T if args.T is not None else 'all'}`",
        f"- active T values: `{', '.join(active_T)}`",
        f"- final prefix j_count: `{final_j}`",
        f"- include boundary: `{args.include_boundary}`",
        f"- low majority threshold: `{args.low_majority}`",
        f"- high tail threshold: `{args.high_tail}`",
        f"- minimum displayed stratum count: `{args.min_count}`",
        "",
        "## Global",
        "",
        f"- groups: `{global_row['count']}`",
        f"- phase exact fraction: `{global_row['phase_exact_fraction']:.6g}`",
        f"- full exact fraction: `{global_row['full_exact_fraction']:.6g}`",
        f"- phase-low fraction: `{global_row['phase_low_fraction']:.6g}`",
        f"- full-low fraction: `{global_row['full_low_fraction']:.6g}`",
        f"- high full-tail-weight fraction: `{global_row['high_tail_fraction']:.6g}`",
        f"- mean full majority: `{global_row['mean_full_majority']:.6g}`",
        f"- mean full-tail-weight fraction: `{global_row['mean_tail_weight_fraction']:.6g}`",
    ]

    lines.extend(table_for("phase_low_fraction", "Largest Phase-Low Fractions"))
    lines.extend(table_for("full_low_fraction", "Largest Full-Low Fractions"))
    lines.extend(table_for("high_tail_fraction", "Largest High-Tail Fractions"))
    lines.extend(table_for("phase_exact_fraction", "Smallest Phase-Exact Fractions", reverse=False))

    lines.extend([
        "",
        "## Interpretation",
        "",
        "If bad cells concentrate in a few source strata, a drift/tail norm",
        "may be realistic: the bad set can be penalized or isolated.  If bad",
        "cells are spread evenly across all source strata, the analytic",
        "branch becomes harder and the finite-rank fallback becomes more",
        "attractive.",
        "",
        "This diagnostic does not identify an infinite operator and does not",
        "prove any tail, compactness, or spectral statement.",
    ])
    return "\n".join(lines) + "\n", strata, tops


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stratify bad high-bit cells by source phase.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--j-count", type=int, default=None)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--low-majority", type=float, default=0.5)
    parser.add_argument("--high-tail", type=float, default=0.75)
    parser.add_argument("--min-count", type=int, default=64)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, strata, tops = summarize(args)
    report_path, strata_path, top_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(strata, strata_path)
    write_csv(tops, top_path)
    print("=" * 118)
    print("  Bad-cell stratification")
    print("=" * 118)
    print(f"  T={args.T if args.T is not None else 'all'}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {strata_path.name}")
    print(f"    {top_path.name}")


if __name__ == "__main__":
    main()
