"""
108_source_refinement_collapse.py

Score finite source-state refinements for the Phase-10 Gate-10.B bridge.

The diagnostic starts from script-88 CSVs.  Each retained source cell
`(T,r,h)` has a weighted destination-phase row.  The question is whether
these rows can be collapsed to a smaller source alphabet without a large
weak L1 error.

This script compares candidate source keys such as:

  phase
  phase + r mod 2^a
  phase + top a bits of r
  phase + both r mod 32 and top a bits of r

It does not retrace orbits, does not generate Lean code, and does not
prove a limiting operator.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GROUPS = ROOT / "collatz_88_cylinder_group_summary.csv"
DEFAULT_DISTS = ROOT / "collatz_88_signature_distribution.csv"
OUT_REPORT = ROOT / "collatz_108_source_refinement_collapse_report.md"
OUT_BY_CANDIDATE = ROOT / "collatz_108_source_refinement_collapse_by_candidate.csv"

State = tuple[int, int, int]
WindowKey = tuple[str, str, str, str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_CANDIDATE
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_108_{safe}_source_refinement_collapse"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_candidate.csv"


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


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "mean": mean(values) if values else 0.0,
        "median": median(values) if values else 0.0,
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
    }


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


def parse_full_signature(text: str) -> tuple[str, State | None, int | None]:
    if text == "terminal":
        return "terminal", None, None
    parts = text.split("|")
    if len(parts) != 5 or parts[0] != "return":
        raise ValueError(f"unexpected full signature: {text}")
    state = (int(parts[1]), int(parts[2]), int(parts[3]))
    delta = int(parts[4])
    return "return", state, delta


def source_state_mixed(row: dict[str, str]) -> int:
    if "source_state_mixed" in row:
        return int(row["source_state_mixed"])
    if "source_state_count" in row:
        return int(int(row["source_state_count"]) > 1)
    return 0


def window_key(row: dict[str, str]) -> WindowKey:
    return (
        row["T"],
        row["r"],
        row["h"],
        row["mode"],
        row["j_start"],
        row["j_count"],
    )


def l1_diff(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    return sum(abs(a.get(key, 0.0) - b.get(key, 0.0)) for key in keys)


def key_low(window: dict[str, Any], bits: int) -> str:
    return f"{window['source_phase']}|rlo{bits}={window['r'] % (1 << bits)}"


def key_high(window: dict[str, Any], bits: int) -> str:
    T = int(window["T"])
    shift = max(0, T - bits)
    return f"{window['source_phase']}|rhi{bits}={window['r'] >> shift}"


def key_low5_high(window: dict[str, Any], bits: int) -> str:
    T = int(window["T"])
    shift = max(0, T - bits)
    return (
        f"{window['source_phase']}|rlo5={window['r'] % 32}"
        f"|rhi{bits}={window['r'] >> shift}"
    )


def build_candidates(max_bits: int) -> list[tuple[str, Any]]:
    candidates: list[tuple[str, Any]] = [("phase", lambda window: window["source_phase"])]
    for bits in range(1, max_bits + 1):
        candidates.append((f"phase+rlo{bits}", lambda window, b=bits: key_low(window, b)))
    for bits in range(1, max_bits + 1):
        candidates.append((f"phase+rhi{bits}", lambda window, b=bits: key_high(window, b)))
    for bits in range(1, min(max_bits, 6) + 1):
        candidates.append((f"phase+rlo5+rhi{bits}", lambda window, b=bits: key_low5_high(window, b)))
    candidates.append(("source_cell", lambda window: f"{window['T']}|{window['r']}|{window['h']}"))
    return candidates


def load_windows(args: argparse.Namespace) -> dict[WindowKey, dict[str, Any]]:
    windows: dict[WindowKey, dict[str, Any]] = {}
    with Path(args.groups).open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["mode"] != "prefix":
                continue
            if args.T is not None and int(row["T"]) != args.T:
                continue
            if not args.include_boundary and row["boundary_flag"] != "bulk":
                continue
            if not args.include_mixed_source and source_state_mixed(row) != 0:
                continue
            key = window_key(row)
            windows[key] = {
                "T": int(row["T"]),
                "r": int(row["r"]),
                "h": int(row["h"]),
                "j_count": int(row["j_count"]),
                "sample_count": int(row["sample_count"]),
                "source_phase": row["source_phase"],
                "phase_weights": defaultdict(float),
                "tail_weight": 0.0,
                "retained_weight": 0.0,
            }

    with Path(args.distributions).open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["mode"] != "prefix" or row["signature_level"] != "full":
                continue
            if args.T is not None and int(row["T"]) != args.T:
                continue
            key = window_key(row)
            window = windows.get(key)
            if window is None:
                continue
            status, dst_state, delta = parse_full_signature(row["signature"])
            if status == "terminal":
                continue
            assert dst_state is not None
            assert delta is not None
            weight = float(row["weight_sum"]) / window["sample_count"] if window["sample_count"] else 0.0
            if args.delta_cutoff is not None and delta > args.delta_cutoff:
                window["tail_weight"] += weight
                continue
            phase_key = f"{dst_state[0]}|{dst_state[1]}|{dst_state[2]}"
            window["phase_weights"][phase_key] += weight
            window["retained_weight"] += weight
    return windows


def average_row(rows: list[dict[str, Any]]) -> dict[str, float]:
    out: dict[str, float] = defaultdict(float)
    if not rows:
        return {}
    scale = 1.0 / len(rows)
    for row in rows:
        for dst, value in row["phase_weights"].items():
            out[dst] += float(value) * scale
    return dict(out)


def score_candidate(
    *,
    name: str,
    key_fn,
    j_count: int,
    windows: list[dict[str, Any]],
) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for window in windows:
        groups[key_fn(window)].append(window)

    diffs: list[float] = []
    group_sizes = []
    worst_key = ""
    worst_key_mean = -1.0
    for key, rows in groups.items():
        averaged = average_row(rows)
        group_diffs = [l1_diff(row["phase_weights"], averaged) for row in rows]
        diffs.extend(group_diffs)
        group_sizes.append(len(rows))
        group_mean = mean(group_diffs) if group_diffs else 0.0
        if group_mean > worst_key_mean:
            worst_key = key
            worst_key_mean = group_mean

    stats = summarize(diffs)
    size_stats = summarize([float(size) for size in group_sizes])
    singleton_count = sum(1 for size in group_sizes if size == 1)
    row: dict[str, Any] = {
        "candidate": name,
        "j_count": j_count,
        "source_cells": len(windows),
        "key_count": len(groups),
        "mean_cells_per_key": len(windows) / len(groups) if groups else 0.0,
        "median_cells_per_key": size_stats["median"],
        "p95_cells_per_key": size_stats["p95"],
        "singleton_key_fraction": singleton_count / len(groups) if groups else 0.0,
        "worst_key": worst_key,
        "worst_key_mean": worst_key_mean,
    }
    for key, value in stats.items():
        row[f"collapse_l1_{key}"] = value
    return row


def score_all(windows: dict[WindowKey, dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    by_count: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for window in windows.values():
        by_count[window["j_count"]].append(window)

    rows: list[dict[str, Any]] = []
    candidates = build_candidates(args.max_bits)
    for j_count in sorted(by_count):
        current = by_count[j_count]
        for name, key_fn in candidates:
            rows.append(score_candidate(name=name, key_fn=key_fn, j_count=j_count, windows=current))
    return rows


def render_report(args: argparse.Namespace, rows: list[dict[str, Any]]) -> str:
    cutoff_text = "none" if args.delta_cutoff is None else str(args.delta_cutoff)
    lines = [
        "# Source-Refinement Collapse Diagnostic",
        "",
        "Status: finite source-quotient diagnostic, not an operator theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- distributions file: `{args.distributions}`",
        f"- T filter: `{args.T if args.T is not None else 'all'}`",
        f"- delta cutoff: `{cutoff_text}`",
        f"- max bits: `{args.max_bits}`",
        f"- include boundary: `{args.include_boundary}`",
        f"- include mixed source cells: `{args.include_mixed_source}`",
        "",
        "## Best Nontrivial Candidates By Prefix",
        "",
        "Rows below exclude the overfit `source_cell` key and require at",
        f"least `{args.min_mean_cells}` mean source cells per key.",
        "",
        "| j_count | candidate | collapse mean | p95 | p99 | max | keys | mean cells/key | singleton frac | worst key mean |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    by_count: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_count[int(row["j_count"])].append(row)

    for j_count in sorted(by_count):
        eligible = [
            row for row in by_count[j_count]
            if row["candidate"] != "source_cell"
            and float(row["mean_cells_per_key"]) >= args.min_mean_cells
        ]
        for row in sorted(eligible, key=lambda item: item["collapse_l1_mean"])[:10]:
            lines.append(
                f"| {j_count} | `{row['candidate']}` | "
                f"{row['collapse_l1_mean']:.8g} | {row['collapse_l1_p95']:.8g} | "
                f"{row['collapse_l1_p99']:.8g} | {row['collapse_l1_max']:.8g} | "
                f"{row['key_count']} | {row['mean_cells_per_key']:.8g} | "
                f"{row['singleton_key_fraction']:.8g} | {row['worst_key_mean']:.8g} |"
            )

    lines.extend([
        "",
        "## Baselines",
        "",
        "| j_count | phase collapse mean | source-cell collapse mean | source-cell keys |",
        "|---:|---:|---:|---:|",
    ])
    for j_count in sorted(by_count):
        phase = next(row for row in by_count[j_count] if row["candidate"] == "phase")
        source_cell = next(row for row in by_count[j_count] if row["candidate"] == "source_cell")
        lines.append(
            f"| {j_count} | {phase['collapse_l1_mean']:.8g} | "
            f"{source_cell['collapse_l1_mean']:.8g} | {source_cell['key_count']} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "A good source refinement should lower collapse error without making",
        "almost every source cell its own key.  A near-zero value for",
        "`source_cell` is only the trivial identity refinement.",
        "",
        "This diagnostic does not prove convergence.  It only identifies",
        "finite alphabets worth testing before a Lean import or Banach-space",
        "bridge is attempted.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score source-state refinements by collapse error.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--delta-cutoff", type=int, default=5)
    parser.add_argument("--no-delta-cutoff", action="store_true")
    parser.add_argument("--max-bits", type=int, default=10)
    parser.add_argument("--min-mean-cells", type=float, default=16.0)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--include-mixed-source", action="store_true")
    parser.add_argument("--output-tag", default=None)
    args = parser.parse_args()
    if args.no_delta_cutoff:
        args.delta_cutoff = None
    return args


def main() -> None:
    args = parse_args()
    windows = load_windows(args)
    rows = score_all(windows, args)
    report = render_report(args, rows)
    report_path, rows_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(rows, rows_path)
    print("Source-refinement collapse diagnostic written:")
    print(f"  {report_path.name}")
    print(f"  {rows_path.name}")


if __name__ == "__main__":
    main()
