"""
114_A0_high_v2_tail_split.py

Quantify the high-v2 exceptional-source tail for an A0 key-drift inspection.

This script consumes a script-111 phase-strata CSV, typically

  collatz_111_T14_j64_128_b0_refined_square_key_drift_phase_strata.csv

and reports how much source mass and weighted drift is carried by
threshold sets of the form

  {source v2 >= R}.

It does not retrace Collatz rows and does not prove tail control.  It is a
finite bookkeeping diagnostic for the A0 weak-bridge program.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "collatz_111_T14_j64_128_b0_refined_square_key_drift_phase_strata.csv"


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_114{suffix}_A0_high_v2_tail_split"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_thresholds.csv",
        ROOT / f"{stem}_families.csv",
    )


def parse_stratum(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected phase stratum: {text}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            v2, odd, h = parse_stratum(row["stratum"])
            rows.append(
                {
                    "stratum": row["stratum"],
                    "v2": v2,
                    "odd": odd,
                    "h": h,
                    "source_keys": int(row["source_keys"]),
                    "sample_weight": float(row["sample_weight"]),
                    "weighted_drift": float(row["weighted_drift"]),
                    "max_l1": float(row["max_l1"]),
                    "mean_l1_weighted_by_sample": float(row["mean_l1_weighted_by_sample"]),
                    "contribution_share": float(row["contribution_share"]),
                }
            )
    return rows


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


def parse_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.9g}"
    return str(value)


def threshold_rows(rows: list[dict[str, Any]], thresholds: list[int]) -> list[dict[str, Any]]:
    total_mass = sum(float(row["sample_weight"]) for row in rows)
    total_drift = sum(float(row["weighted_drift"]) for row in rows)
    out: list[dict[str, Any]] = []
    for threshold in thresholds:
        tail = [row for row in rows if int(row["v2"]) >= threshold]
        good = [row for row in rows if int(row["v2"]) < threshold]
        tail_mass = sum(float(row["sample_weight"]) for row in tail)
        tail_drift = sum(float(row["weighted_drift"]) for row in tail)
        good_mass = sum(float(row["sample_weight"]) for row in good)
        good_drift = sum(float(row["weighted_drift"]) for row in good)
        out.append(
            {
                "threshold_v2_ge": threshold,
                "tail_rows": len(tail),
                "good_rows": len(good),
                "tail_sample_weight": tail_mass,
                "good_sample_weight": good_mass,
                "tail_mass_share": tail_mass / total_mass if total_mass else 0.0,
                "good_mass_share": good_mass / total_mass if total_mass else 0.0,
                "tail_weighted_drift": tail_drift,
                "good_weighted_drift": good_drift,
                "tail_contribution_share": tail_drift / total_drift if total_drift else 0.0,
                "good_contribution_share": good_drift / total_drift if total_drift else 0.0,
                "tail_mean_l1": tail_drift / tail_mass if tail_mass else 0.0,
                "good_mean_l1": good_drift / good_mass if good_mass else 0.0,
                "tail_max_l1": max((float(row["max_l1"]) for row in tail), default=0.0),
                "good_max_l1": max((float(row["max_l1"]) for row in good), default=0.0),
                "substochastic_tail_bound_2mass": 2.0 * tail_mass / total_mass if total_mass else 0.0,
            }
        )
    return out


def family_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total_mass = sum(float(row["sample_weight"]) for row in rows)
    total_drift = sum(float(row["weighted_drift"]) for row in rows)
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["v2"]), int(row["odd"]))].append(row)
    out: list[dict[str, Any]] = []
    for (v2, odd), items in sorted(grouped.items()):
        sample_weight = sum(float(row["sample_weight"]) for row in items)
        weighted_drift = sum(float(row["weighted_drift"]) for row in items)
        out.append(
            {
                "family": f"{v2}|{odd}",
                "v2": v2,
                "odd": odd,
                "h_rows": len(items),
                "sample_weight": sample_weight,
                "mass_share": sample_weight / total_mass if total_mass else 0.0,
                "weighted_drift": weighted_drift,
                "contribution_share": weighted_drift / total_drift if total_drift else 0.0,
                "mean_l1": weighted_drift / sample_weight if sample_weight else 0.0,
                "max_l1": max(float(row["max_l1"]) for row in items),
                "mean_l1_over_h": mean(float(row["mean_l1_weighted_by_sample"]) for row in items),
            }
        )
    out.sort(key=lambda row: float(row["contribution_share"]), reverse=True)
    return out


def write_report(
    *,
    args: argparse.Namespace,
    report_path: Path,
    thresholds_path: Path,
    families_path: Path,
    rows: list[dict[str, Any]],
    thresholds: list[dict[str, Any]],
    families: list[dict[str, Any]],
) -> None:
    total_mass = sum(float(row["sample_weight"]) for row in rows)
    total_drift = sum(float(row["weighted_drift"]) for row in rows)
    lines: list[str] = []
    lines.append("# A0 High-v2 Tail Split")
    lines.append("")
    lines.append("Status: finite diagnostic only.  This does not prove tail control.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- input: `{Path(args.input).name}`")
    lines.append(f"- phase rows: `{len(rows)}`")
    lines.append(f"- total sample weight: `{format_float(total_mass)}`")
    lines.append(f"- total weighted drift: `{format_float(total_drift)}`")
    lines.append(f"- thresholds CSV: `{thresholds_path.name}`")
    lines.append(f"- families CSV: `{families_path.name}`")
    lines.append("")
    lines.append("## Threshold Tail")
    lines.append("")
    lines.append(
        "| v2 >= R | tail mass | tail contribution | tail mean L1 | "
        "tail max L1 | 2*mass bound |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for row in thresholds:
        lines.append(
            f"| {row['threshold_v2_ge']} | "
            f"{format_float(row['tail_mass_share'])} | "
            f"{format_float(row['tail_contribution_share'])} | "
            f"{format_float(row['tail_mean_l1'])} | "
            f"{format_float(row['tail_max_l1'])} | "
            f"{format_float(row['substochastic_tail_bound_2mass'])} |"
        )
    lines.append("")
    lines.append("## Top Families")
    lines.append("")
    lines.append("| rank | family | mass | contribution | mean L1 | max L1 |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(families[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['family']}` | "
            f"{format_float(row['mass_share'])} | "
            f"{format_float(row['contribution_share'])} | "
            f"{format_float(row['mean_l1'])} | "
            f"{format_float(row['max_l1'])} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- `2*mass bound` is the crude substochastic row-difference bound.")
    lines.append("- A useful weak theorem may control high-v2 rows through this mass term.")
    lines.append("- The average drift still mostly comes from low-v2 families, not from the max row.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--thresholds", default="4,6,8,10,12,14")
    parser.add_argument("--report-top", type=int, default=12)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    rows = read_rows(input_path)
    thresholds = threshold_rows(rows, parse_ints(args.thresholds))
    families = family_rows(rows)
    report_path, thresholds_path, families_path = output_paths(args.output_tag)
    write_csv(thresholds, thresholds_path)
    write_csv(families, families_path)
    write_report(
        args=args,
        report_path=report_path,
        thresholds_path=thresholds_path,
        families_path=families_path,
        rows=rows,
        thresholds=thresholds,
        families=families,
    )
    print(f"wrote {report_path}")
    print(f"wrote {thresholds_path}")
    print(f"wrote {families_path}")


if __name__ == "__main__":
    main()
