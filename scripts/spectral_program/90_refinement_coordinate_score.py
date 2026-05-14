"""
90_refinement_coordinate_score.py

Global refinement-coordinate scorer for Gate 10.B diagnostics.

This script consumes the cylinder summary produced by
88_cylinder_signature_stability.py, selects stable-status but
phase-unstable bulk groups, and scores simple candidate refinement
coordinates across all selected groups.

It does not compute a spectral-radius bound.  It is a modeling
diagnostic: a strong coordinate score suggests a possible finite
symbolic refinement; a weak score suggests moving toward a countable
return-signature model or the finite-rank fallback.
"""

from __future__ import annotations

import argparse
import csv
import math
from importlib import util
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GROUPS = ROOT / "collatz_88_cylinder_group_summary.csv"
OUT_DETAILS = ROOT / "collatz_90_refinement_coordinate_details.csv"
OUT_GROUP_SCORES = ROOT / "collatz_90_refinement_coordinate_group_scores.csv"
OUT_SUMMARY = ROOT / "collatz_90_refinement_coordinate_summary.csv"
OUT_REPORT = ROOT / "collatz_90_refinement_coordinate_report.md"


def load_inspector():
    path = ROOT / "89_phase_split_inspector.py"
    spec = util.spec_from_file_location("phase_split_inspector", path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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


def read_candidate_groups(args: argparse.Namespace) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with Path(args.groups).open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["mode"] != "prefix":
                continue
            if int(row["j_count"]) != args.j_count:
                continue
            if not args.include_boundary and row["boundary_flag"] != "bulk":
                continue
            if args.h is not None and int(row["h"]) != args.h:
                continue
            if float(row["status_majority_fraction"]) < args.min_status_majority:
                continue
            if float(row["phase_majority_fraction"]) > args.max_phase_majority:
                continue
            rows.append(row)

    rows.sort(
        key=lambda row: (
            float(row["phase_majority_fraction"]),
            float(row["full_majority_fraction"]),
            int(row["T"]),
            int(row["r"]),
            int(row["h"]),
        )
    )
    if args.limit_groups > 0:
        return rows[: args.limit_groups]
    return rows


def coordinate_names(args: argparse.Namespace) -> list[str]:
    coords: list[str] = []
    for mod in (2, 4, 8, 16, 32, 64):
        if args.j_count // mod >= args.min_avg_bucket_size:
            coords.append(f"j_mod_{mod}")
    for shift, mod in ((1, 2), (2, 4), (3, 8), (4, 16), (5, 32)):
        if args.j_count / mod >= args.min_avg_bucket_size:
            coords.append(f"j_shift_{shift}_mod_{mod}")
    for mod in (2, 4, 8, 16, 32):
        coords.append(f"step_mod_{mod}")
    coords.append("delta")
    for mod in (2, 4, 8, 16, 32, 64):
        coords.append(f"next_t_mod_{mod}")
    return coords


def augment_detail(row: dict[str, Any]) -> dict[str, Any]:
    j = int(row["j"])
    step = int(row["step"])
    next_t_raw = row["next_t"]
    next_t = int(next_t_raw) if next_t_raw != "" else None

    for mod in (2, 4, 8, 16, 32, 64):
        row[f"j_mod_{mod}"] = j % mod
    for shift, mod in ((1, 2), (2, 4), (3, 8), (4, 16), (5, 32)):
        row[f"j_shift_{shift}_mod_{mod}"] = (j >> shift) % mod
    for mod in (2, 4, 8, 16, 32):
        row[f"step_mod_{mod}"] = step % mod
    for mod in (2, 4, 8, 16, 32, 64):
        row[f"next_t_mod_{mod}"] = "NA" if next_t is None else next_t % mod
    if row["delta"] == "":
        row["delta"] = "NA"
    return row


def trace_group(inspector, ctx, args: argparse.Namespace, group: dict[str, str]) -> list[dict[str, Any]]:
    T = int(group["T"])
    r = int(group["r"])
    h = int(group["h"])
    details: list[dict[str, Any]] = []
    for j in range(args.j_count):
        t = r + (j << T)
        if t == 0 and not args.include_t_zero:
            continue
        row = inspector.trace_detail(ctx, args, T, r, h, j)
        row.update({
            "source_phase": group["source_phase"],
            "source_status_majority_fraction": group["status_majority_fraction"],
            "source_phase_majority_fraction": group["phase_majority_fraction"],
            "source_full_majority_fraction": group["full_majority_fraction"],
        })
        details.append(augment_detail(row))
    return details


def score_groups(inspector, details_by_group: list[tuple[dict[str, str], list[dict[str, Any]]]], args: argparse.Namespace):
    group_scores: list[dict[str, Any]] = []
    coords = coordinate_names(args)
    for group, details in details_by_group:
        for coord in coords:
            for target in ("phase_signature", "full_signature"):
                quality = inspector.coordinate_quality(details, coord, target)
                if quality["avg_bucket_size"] < args.min_avg_bucket_size:
                    continue
                group_scores.append({
                    "T": int(group["T"]),
                    "r": int(group["r"]),
                    "h": int(group["h"]),
                    "source_phase": group["source_phase"],
                    "source_phase_majority_fraction": group["phase_majority_fraction"],
                    "source_full_majority_fraction": group["full_majority_fraction"],
                    **quality,
                })
    return group_scores


def summarize_scores(group_scores: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in group_scores:
        buckets.setdefault((row["target"], row["coordinate"]), []).append(row)

    summary: list[dict[str, Any]] = []
    for (target, coord), rows in buckets.items():
        weighted = [float(row["weighted_purity"]) for row in rows]
        min_bucket = [float(row["min_bucket_purity"]) for row in rows]
        pure = [
            row for row in rows
            if math.isclose(float(row["weighted_purity"]), 1.0)
            and math.isclose(float(row["min_bucket_purity"]), 1.0)
        ]
        strong = [
            row for row in rows
            if float(row["weighted_purity"]) >= args.strong_purity
            and float(row["min_bucket_purity"]) >= args.min_bucket_purity
        ]
        summary.append({
            "target": target,
            "coordinate": coord,
            "groups": len(rows),
            "mean_weighted_purity": mean(weighted) if weighted else 0.0,
            "median_weighted_purity": median(weighted) if weighted else 0.0,
            "p10_weighted_purity": quantile(weighted, 0.10),
            "min_weighted_purity": min(weighted) if weighted else 0.0,
            "mean_min_bucket_purity": mean(min_bucket) if min_bucket else 0.0,
            "p10_min_bucket_purity": quantile(min_bucket, 0.10),
            "min_min_bucket_purity": min(min_bucket) if min_bucket else 0.0,
            "perfect_group_fraction": len(pure) / len(rows) if rows else 0.0,
            "strong_group_fraction": len(strong) / len(rows) if rows else 0.0,
            "mean_bucket_count": mean(float(row["bucket_count"]) for row in rows) if rows else 0.0,
            "mean_avg_bucket_size": mean(float(row["avg_bucket_size"]) for row in rows) if rows else 0.0,
            "mean_distinct_target_count": mean(float(row["distinct_target_count"]) for row in rows) if rows else 0.0,
        })

    summary.sort(
        key=lambda row: (
            row["target"],
            -float(row["mean_weighted_purity"]),
            -float(row["p10_weighted_purity"]),
            -float(row["strong_group_fraction"]),
            row["coordinate"],
        )
    )
    return summary


def best_rows(summary: list[dict[str, Any]], target: str, n: int = 12) -> list[dict[str, Any]]:
    rows = [row for row in summary if row["target"] == target]
    rows.sort(
        key=lambda row: (
            -float(row["mean_weighted_purity"]),
            -float(row["p10_weighted_purity"]),
            -float(row["strong_group_fraction"]),
            row["coordinate"],
        )
    )
    return rows[:n]


def make_report(groups: list[dict[str, str]], summary: list[dict[str, Any]], args: argparse.Namespace) -> str:
    phase_rows = best_rows(summary, "phase_signature")
    full_rows = best_rows(summary, "full_signature")

    def table(rows: list[dict[str, Any]]) -> list[str]:
        lines = [
            "| coordinate | groups | mean purity | p10 purity | min purity | mean min-bucket | strong groups | perfect groups |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in rows:
            lines.append(
                f"| `{row['coordinate']}` | {row['groups']} | "
                f"{float(row['mean_weighted_purity']):.6g} | "
                f"{float(row['p10_weighted_purity']):.6g} | "
                f"{float(row['min_weighted_purity']):.6g} | "
                f"{float(row['mean_min_bucket_purity']):.6g} | "
                f"{float(row['strong_group_fraction']):.6g} | "
                f"{float(row['perfect_group_fraction']):.6g} |"
            )
        return lines

    lines = [
        "# Refinement Coordinate Score Report",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- selected groups: `{len(groups)}`",
        f"- j_count: `{args.j_count}`",
        f"- max phase majority: `{args.max_phase_majority}`",
        f"- min status majority: `{args.min_status_majority}`",
        f"- h filter: `{args.h if args.h is not None else 'all'}`",
        f"- include boundary groups: `{args.include_boundary}`",
        f"- include t=0: `{args.include_t_zero}`",
        f"- minimum average bucket size: `{args.min_avg_bucket_size}`",
        f"- strong purity threshold: `{args.strong_purity}`",
        f"- minimum bucket purity threshold: `{args.min_bucket_purity}`",
        "",
        "## Best Global Coordinates for Destination Phase",
        "",
        *table(phase_rows),
        "",
        "## Best Global Coordinates for Full Signature",
        "",
        *table(full_rows),
        "",
        "## Interpretation",
        "",
        "The ranking aggregates coordinate quality group-by-group.  It does",
        "not use a coordinate that has one bucket per lift as evidence, because",
        "coordinates with average bucket size below the configured threshold",
        "are excluded.",
        "",
        "A high destination-phase score supports trying a finite symbolic",
        "refinement of the phase quotient.  A weaker full-signature score",
        "means the weight exponent or return signature still carries",
        "unmodeled information.",
        "",
        "These diagnostics do not imply Conjecture 6, an infinite operator, a",
        "Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral",
        "gap.",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score candidate refinement coordinates globally.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--j-count", type=int, default=64)
    parser.add_argument("--limit-groups", type=int, default=0, help="0 means all matching groups")
    parser.add_argument("--max-phase-majority", type=float, default=0.5)
    parser.add_argument("--min-status-majority", type=float, default=1.0)
    parser.add_argument("--h", type=int, default=None)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--min-avg-bucket-size", type=float, default=2.0)
    parser.add_argument("--strong-purity", type=float, default=0.9)
    parser.add_argument("--min-bucket-purity", type=float, default=0.5)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--progress", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inspector = load_inspector()
    groups = read_candidate_groups(args)
    if not groups:
        raise SystemExit("no matching groups found; run 88 first or loosen filters")

    ctx = inspector.setup()
    details_by_group = []
    all_details: list[dict[str, Any]] = []

    print("=" * 118)
    print("  Refinement coordinate score")
    print("=" * 118)
    print(f"  selected_groups={len(groups)}, j_count={args.j_count}")
    for idx, group in enumerate(groups, start=1):
        if args.progress:
            print(
                f"  [{idx}/{len(groups)}] T={group['T']} r={group['r']} h={group['h']} "
                f"phase_majority={float(group['phase_majority_fraction']):.6g}"
            )
        details = trace_group(inspector, ctx, args, group)
        details_by_group.append((group, details))
        all_details.extend(details)

    group_scores = score_groups(inspector, details_by_group, args)
    summary = summarize_scores(group_scores, args)

    write_csv(all_details, OUT_DETAILS)
    write_csv(group_scores, OUT_GROUP_SCORES)
    write_csv(summary, OUT_SUMMARY)
    OUT_REPORT.write_text(make_report(groups, summary, args), encoding="utf-8")

    print("\n  Output:")
    print(f"    {OUT_DETAILS.name}")
    print(f"    {OUT_GROUP_SCORES.name}")
    print(f"    {OUT_SUMMARY.name}")
    print(f"    {OUT_REPORT.name}")


if __name__ == "__main__":
    main()
