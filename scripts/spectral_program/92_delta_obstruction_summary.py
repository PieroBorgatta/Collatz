"""
92_delta_obstruction_summary.py

Summarize whether full-signature instability is primarily a phase
problem, a delta/weight problem, or a mixed return-signature problem.

This script consumes the CSV files emitted by
88_cylinder_signature_stability.py.  It performs no orbit tracing and no
spectral-radius computation.
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
OUT_REPORT = ROOT / "collatz_92_delta_obstruction_report.md"
OUT_WORST = ROOT / "collatz_92_delta_obstruction_worst.csv"


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


def key(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return row["T"], row["r"], row["h"], row["mode"], row["j_count"]


def is_exact(row: dict[str, str], field: str) -> bool:
    return float(row[field]) == 1.0


def load_delta_distributions(rows: list[dict[str, str]], args: argparse.Namespace) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    out: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["mode"] != "prefix":
            continue
        if int(row["j_count"]) != args.j_count:
            continue
        if row["signature_level"] != "delta":
            continue
        out[(row["T"], row["r"], row["h"])].append(row)
    return out


def signature_summary(dist_rows: list[dict[str, str]], limit: int = 4) -> str:
    if not dist_rows:
        return ""
    ordered = sorted(dist_rows, key=lambda row: (-float(row["fraction"]), row["signature"]))
    return ", ".join(
        f"{row['signature']}:{float(row['fraction']):.4g}" for row in ordered[:limit]
    )


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]]]:
    groups_all = read_csv(Path(args.groups))
    dists_all = read_csv(Path(args.distributions))
    delta_dists = load_delta_distributions(dists_all, args)

    groups = [
        row for row in groups_all
        if row["mode"] == "prefix"
        and int(row["j_count"]) == args.j_count
        and (args.include_boundary or row["boundary_flag"] == "bulk")
    ]
    if not groups:
        raise SystemExit("no matching groups found")

    counts = Counter()
    distinct_delta = Counter()
    distinct_full = Counter()
    dominant_delta = Counter()
    phase_exact_delta_nonexact: list[dict[str, str]] = []
    status_phase_exact_delta_nonexact: list[dict[str, str]] = []
    stable_status_phase_low: list[dict[str, str]] = []

    for row in groups:
        phase_exact = is_exact(row, "phase_majority_fraction")
        delta_exact = is_exact(row, "delta_majority_fraction")
        full_exact = is_exact(row, "full_majority_fraction")
        status_exact = is_exact(row, "status_majority_fraction")
        counts["groups"] += 1
        counts["phase_exact"] += int(phase_exact)
        counts["delta_exact"] += int(delta_exact)
        counts["full_exact"] += int(full_exact)
        counts["phase_exact_delta_nonexact"] += int(phase_exact and not delta_exact)
        counts["phase_exact_full_nonexact"] += int(phase_exact and not full_exact)
        counts["phase_nonexact_delta_exact"] += int((not phase_exact) and delta_exact)
        counts["both_phase_delta_nonexact"] += int((not phase_exact) and (not delta_exact))
        counts["status_phase_exact_delta_nonexact"] += int(status_exact and phase_exact and not delta_exact)
        counts["stable_status_phase_low"] += int(status_exact and float(row["phase_majority_fraction"]) <= args.low_majority)
        distinct_delta[int(row["distinct_delta_count"])] += 1
        distinct_full[int(row["distinct_full_count"])] += 1
        dominant_delta[row["dominant_delta_signature"]] += 1
        if phase_exact and not delta_exact:
            phase_exact_delta_nonexact.append(row)
        if status_exact and phase_exact and not delta_exact:
            status_phase_exact_delta_nonexact.append(row)
        if status_exact and float(row["phase_majority_fraction"]) <= args.low_majority:
            stable_status_phase_low.append(row)

    def pct(n: int) -> float:
        return n / counts["groups"] if counts["groups"] else 0.0

    worst = sorted(
        status_phase_exact_delta_nonexact,
        key=lambda row: (
            float(row["delta_majority_fraction"]),
            float(row["full_majority_fraction"]),
            int(row["T"]),
            int(row["r"]),
            int(row["h"]),
        ),
    )[: args.limit]

    worst_rows: list[dict[str, Any]] = []
    for row in worst:
        dist_rows = delta_dists.get((row["T"], row["r"], row["h"]), [])
        worst_rows.append({
            "T": row["T"],
            "r": row["r"],
            "h": row["h"],
            "source_phase": row["source_phase"],
            "status_majority_fraction": row["status_majority_fraction"],
            "phase_majority_fraction": row["phase_majority_fraction"],
            "delta_majority_fraction": row["delta_majority_fraction"],
            "full_majority_fraction": row["full_majority_fraction"],
            "distinct_delta_count": row["distinct_delta_count"],
            "dominant_delta_signature": row["dominant_delta_signature"],
            "delta_distribution": signature_summary(dist_rows),
        })

    low_phase = sorted(
        stable_status_phase_low,
        key=lambda row: (
            float(row["phase_majority_fraction"]),
            float(row["full_majority_fraction"]),
            int(row["T"]),
            int(row["r"]),
            int(row["h"]),
        ),
    )[: args.limit]

    avg = {
        "status": mean(float(row["status_majority_fraction"]) for row in groups),
        "phase": mean(float(row["phase_majority_fraction"]) for row in groups),
        "delta": mean(float(row["delta_majority_fraction"]) for row in groups),
        "full": mean(float(row["full_majority_fraction"]) for row in groups),
    }

    lines = [
        "# Delta Obstruction Summary",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- distributions file: `{args.distributions}`",
        f"- j_count: `{args.j_count}`",
        f"- include boundary: `{args.include_boundary}`",
        "",
        "## Aggregate",
        "",
        f"- groups: `{counts['groups']}`",
        f"- mean status majority: `{avg['status']:.6g}`",
        f"- mean phase majority: `{avg['phase']:.6g}`",
        f"- mean delta majority: `{avg['delta']:.6g}`",
        f"- mean full majority: `{avg['full']:.6g}`",
        f"- phase exact fraction: `{pct(counts['phase_exact']):.6g}`",
        f"- delta exact fraction: `{pct(counts['delta_exact']):.6g}`",
        f"- full exact fraction: `{pct(counts['full_exact']):.6g}`",
        f"- phase exact but delta non-exact fraction: `{pct(counts['phase_exact_delta_nonexact']):.6g}`",
        f"- phase exact but full non-exact fraction: `{pct(counts['phase_exact_full_nonexact']):.6g}`",
        f"- phase non-exact but delta exact fraction: `{pct(counts['phase_nonexact_delta_exact']):.6g}`",
        f"- both phase and delta non-exact fraction: `{pct(counts['both_phase_delta_nonexact']):.6g}`",
        f"- status+phase exact but delta non-exact groups: `{counts['status_phase_exact_delta_nonexact']}`",
        f"- stable-status phase-majority <= {args.low_majority:g} groups: `{counts['stable_status_phase_low']}`",
        "",
        "## Distinct Delta Counts",
        "",
        "| distinct delta count | groups | fraction |",
        "|---:|---:|---:|",
    ]
    for k, v in sorted(distinct_delta.items()):
        lines.append(f"| {k} | {v} | {v / counts['groups']:.6g} |")

    lines.extend([
        "",
        "## Distinct Full-Signature Counts",
        "",
        "| distinct full count | groups | fraction |",
        "|---:|---:|---:|",
    ])
    for k, v in sorted(distinct_full.items())[:20]:
        lines.append(f"| {k} | {v} | {v / counts['groups']:.6g} |")

    lines.extend([
        "",
        "## Dominant Delta Signatures",
        "",
        "| signature | groups | fraction |",
        "|---|---:|---:|",
    ])
    for sig, v in dominant_delta.most_common(12):
        lines.append(f"| `{sig}` | {v} | {v / counts['groups']:.6g} |")

    lines.extend([
        "",
        "## Worst Status+Phase Exact but Delta Non-Exact Groups",
        "",
        "| T | r | h | phase maj | delta maj | full maj | delta distribution |",
        "|---:|---:|---:|---:|---:|---:|---|",
    ])
    for row in worst_rows:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | "
            f"{float(row['phase_majority_fraction']):.6g} | "
            f"{float(row['delta_majority_fraction']):.6g} | "
            f"{float(row['full_majority_fraction']):.6g} | "
            f"`{row['delta_distribution']}` |"
        )

    lines.extend([
        "",
        "## Worst Stable-Status Phase-Low Groups",
        "",
        "| T | r | h | phase maj | delta maj | full maj | dominant full |",
        "|---:|---:|---:|---:|---:|---:|---|",
    ])
    for row in low_phase:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | "
            f"{float(row['phase_majority_fraction']):.6g} | "
            f"{float(row['delta_majority_fraction']):.6g} | "
            f"{float(row['full_majority_fraction']):.6g} | "
            f"`{row['dominant_full_signature']}` |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "If many groups are phase-exact but delta-non-exact, then the",
        "remaining obstruction is primarily the weight/return exponent rather",
        "than the destination phase.  Such evidence supports a labelled-edge",
        "or return-signature model, not a premature phase-only operator.",
        "",
        "These diagnostics do not imply Conjecture 6, an infinite operator, a",
        "Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral",
        "gap.",
    ])
    return "\n".join(lines) + "\n", worst_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize delta obstruction in script 88 outputs.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--j-count", type=int, default=16)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--low-majority", type=float, default=0.5)
    parser.add_argument("--limit", type=int, default=16)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, worst_rows = summarize(args)
    OUT_REPORT.write_text(report, encoding="utf-8")
    write_csv(worst_rows, OUT_WORST)
    print("=" * 118)
    print("  Delta obstruction summary")
    print("=" * 118)
    print(f"  j_count={args.j_count}")
    print("\n  Output:")
    print(f"    {OUT_REPORT.name}")
    print(f"    {OUT_WORST.name}")


if __name__ == "__main__":
    main()
