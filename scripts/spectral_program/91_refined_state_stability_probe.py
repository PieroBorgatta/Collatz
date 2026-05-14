"""
91_refined_state_stability_probe.py

Probe whether a candidate refinement coordinate improves signature
stability inside the phase-unstable groups selected by
90_refinement_coordinate_score.py.

This script reads the detail CSV produced by script 90.  It does not
trace orbits and does not compute spectral-radius bounds.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_DETAILS = ROOT / "collatz_90_refinement_coordinate_details.csv"
OUT_SUMMARY = ROOT / "collatz_91_refined_state_summary.csv"
OUT_REPORT = ROOT / "collatz_91_refined_state_report.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def quantile(vals: list[float], q: float) -> float:
    if not vals:
        return 0.0
    ordered = sorted(vals)
    idx = int(round((len(ordered) - 1) * q))
    return ordered[idx]


def majority_fraction(rows: list[dict[str, str]], target: str) -> float:
    if not rows:
        return 0.0
    counts = Counter(row[target] for row in rows)
    return counts.most_common(1)[0][1] / len(rows)


def source_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["T"], row["r"], row["h"]


def coord_value(row: dict[str, str], coord: str) -> str:
    parts = [part.strip() for part in coord.split("+") if part.strip()]
    if len(parts) == 1:
        return row.get(parts[0], "NA")
    return "|".join(f"{part}={row.get(part, 'NA')}" for part in parts)


def refined_key(row: dict[str, str], coord: str) -> tuple[str, str, str, str]:
    return row["T"], row["r"], row["h"], coord_value(row, coord)


def summarize_coordinate(rows: list[dict[str, str]], coord: str, target: str, args: argparse.Namespace) -> dict[str, Any]:
    source_groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    refined_groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        parts = [part.strip() for part in coord.split("+") if part.strip()]
        if any(part not in row for part in parts):
            continue
        source_groups[source_key(row)].append(row)
        refined_groups[refined_key(row, coord)].append(row)

    source_majorities = [majority_fraction(group_rows, target) for group_rows in source_groups.values()]
    cell_majorities = []
    cell_sizes = []
    for group_rows in refined_groups.values():
        if len(group_rows) < args.min_cell_size:
            continue
        cell_majorities.append(majority_fraction(group_rows, target))
        cell_sizes.append(len(group_rows))

    exact_cells = [x for x in cell_majorities if x == 1.0]
    strong_cells = [x for x in cell_majorities if x >= args.strong_threshold]

    return {
        "coordinate": coord,
        "target": target,
        "source_groups": len(source_groups),
        "refined_cells": len(cell_majorities),
        "mean_source_majority": mean(source_majorities) if source_majorities else 0.0,
        "mean_cell_majority": mean(cell_majorities) if cell_majorities else 0.0,
        "median_cell_majority": median(cell_majorities) if cell_majorities else 0.0,
        "p10_cell_majority": quantile(cell_majorities, 0.10),
        "min_cell_majority": min(cell_majorities) if cell_majorities else 0.0,
        "exact_cell_fraction": len(exact_cells) / len(cell_majorities) if cell_majorities else 0.0,
        "strong_cell_fraction": len(strong_cells) / len(cell_majorities) if cell_majorities else 0.0,
        "mean_cell_size": mean(cell_sizes) if cell_sizes else 0.0,
        "min_cell_size": min(cell_sizes) if cell_sizes else 0,
    }


def make_report(summary_rows: list[dict[str, Any]], args: argparse.Namespace) -> str:
    def rows_for(target: str) -> list[dict[str, Any]]:
        rows = [row for row in summary_rows if row["target"] == target]
        rows.sort(
            key=lambda row: (
                -float(row["mean_cell_majority"]),
                -float(row["p10_cell_majority"]),
                -float(row["exact_cell_fraction"]),
                row["coordinate"],
            )
        )
        return rows

    def table(rows: list[dict[str, Any]]) -> list[str]:
        lines = [
            "| coordinate | source groups | cells | source mean | cell mean | p10 cell | min cell | exact cells | strong cells | cell size |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in rows:
            lines.append(
                f"| `{row['coordinate']}` | {row['source_groups']} | {row['refined_cells']} | "
                f"{float(row['mean_source_majority']):.6g} | "
                f"{float(row['mean_cell_majority']):.6g} | "
                f"{float(row['p10_cell_majority']):.6g} | "
                f"{float(row['min_cell_majority']):.6g} | "
                f"{float(row['exact_cell_fraction']):.6g} | "
                f"{float(row['strong_cell_fraction']):.6g} | "
                f"{float(row['mean_cell_size']):.6g} |"
            )
        return lines

    lines = [
        "# Refined State Stability Probe",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- details file: `{args.details}`",
        f"- coordinates: `{','.join(args.coordinates)}`",
        f"- minimum cell size: `{args.min_cell_size}`",
        f"- strong threshold: `{args.strong_threshold}`",
        "",
        "## Destination Phase",
        "",
        *table(rows_for("phase_signature")),
        "",
        "## Full Weighted Signature",
        "",
        *table(rows_for("full_signature")),
        "",
        "## Interpretation",
        "",
        "A good phase-refinement coordinate should raise the cell-majority",
        "statistics for `phase_signature`.  It is not enough for defining a",
        "weighted transfer operator unless the same or an augmented coordinate",
        "also controls `full_signature`.",
        "",
        "These diagnostics do not imply Conjecture 6, an infinite operator, a",
        "Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral",
        "gap.",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe refined-state signature stability from script 90 details.")
    parser.add_argument("--details", default=str(DEFAULT_DETAILS))
    parser.add_argument("--coordinates", default="j_mod_8,j_mod_16,j_mod_32")
    parser.add_argument("--min-cell-size", type=int, default=4)
    parser.add_argument("--strong-threshold", type=float, default=0.9)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.coordinates = [coord.strip() for coord in args.coordinates.split(",") if coord.strip()]
    rows = read_rows(Path(args.details))
    if not rows:
        raise SystemExit("empty detail file; run 90_refinement_coordinate_score.py first")

    summary_rows = []
    for coord in args.coordinates:
        for target in ("phase_signature", "full_signature"):
            summary_rows.append(summarize_coordinate(rows, coord, target, args))

    write_csv(summary_rows, OUT_SUMMARY)
    OUT_REPORT.write_text(make_report(summary_rows, args), encoding="utf-8")

    print("=" * 118)
    print("  Refined state stability probe")
    print("=" * 118)
    print(f"  rows={len(rows)}, coordinates={','.join(args.coordinates)}")
    print("\n  Output:")
    print(f"    {OUT_SUMMARY.name}")
    print(f"    {OUT_REPORT.name}")


if __name__ == "__main__":
    main()
