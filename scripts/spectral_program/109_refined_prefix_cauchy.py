"""
109_refined_prefix_cauchy.py

Measure prefix/Cesaro drift for finite refined source alphabets.

This is the next diagnostic after 108_source_refinement_collapse.py.
Script 108 asks whether source-cell rows can be collapsed to a candidate
source key at a fixed prefix length.  This script asks whether the
averaged row attached to that candidate key changes when the prefix
length is increased.

The diagnostic consumes script-88 CSVs.  It does not define an infinite
operator, prove convergence, or generate Lean code.
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
OUT_REPORT = ROOT / "collatz_109_refined_prefix_cauchy_report.md"
OUT_BY_PAIR = ROOT / "collatz_109_refined_prefix_cauchy_by_pair.csv"

State = tuple[int, int, int]
WindowKey = tuple[str, str, str, str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_PAIR
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_109_{safe}_refined_prefix_cauchy"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_pair.csv"


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


def weighted_quantile(pairs: list[tuple[float, float]], q: float) -> float:
    positive = sorted((value, weight) for value, weight in pairs if weight > 0.0)
    if not positive:
        return 0.0
    total = sum(weight for _value, weight in positive)
    threshold = q * total
    running = 0.0
    for value, weight in positive:
        running += weight
        if running >= threshold:
            return value
    return positive[-1][0]


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
    return sum(abs(float(a.get(key, 0.0)) - float(b.get(key, 0.0))) for key in keys)


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


def load_windows(args: argparse.Namespace) -> dict[int, list[dict[str, Any]]]:
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

    by_count: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for window in windows.values():
        by_count[int(window["j_count"])].append(window)
    return dict(sorted(by_count.items()))


def average_row(rows: list[dict[str, Any]]) -> dict[str, float]:
    out: dict[str, float] = defaultdict(float)
    if not rows:
        return {}
    scale = 1.0 / len(rows)
    for row in rows:
        for dst, value in row["phase_weights"].items():
            out[dst] += float(value) * scale
    return dict(out)


def candidate_rows(
    *,
    key_fn,
    windows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for window in windows:
        grouped[key_fn(window)].append(window)
    out = {}
    for key, rows in grouped.items():
        out[key] = {
            "row": average_row(rows),
            "cell_count": len(rows),
            "tail_mean": mean([float(row["tail_weight"]) for row in rows]) if rows else 0.0,
            "retained_mean": mean([float(row["retained_weight"]) for row in rows]) if rows else 0.0,
        }
    return out


def score_pair(
    *,
    name: str,
    key_fn,
    left_count: int,
    right_count: int,
    left_windows: list[dict[str, Any]],
    right_windows: list[dict[str, Any]],
) -> dict[str, Any]:
    left = candidate_rows(key_fn=key_fn, windows=left_windows)
    right = candidate_rows(key_fn=key_fn, windows=right_windows)
    common = sorted(set(left) & set(right))
    diffs = [l1_diff(left[key]["row"], right[key]["row"]) for key in common]
    weights = [
        0.5 * (float(left[key]["cell_count"]) + float(right[key]["cell_count"]))
        for key in common
    ]
    weighted_pairs = list(zip(diffs, weights, strict=True))
    total_weight = sum(weights)
    weighted_mean = (
        sum(diff * weight for diff, weight in weighted_pairs) / total_weight
        if total_weight
        else 0.0
    )
    stats = summarize(diffs)
    size_left = [float(item["cell_count"]) for item in left.values()]
    size_right = [float(item["cell_count"]) for item in right.values()]
    left_cell_count = sum(int(item["cell_count"]) for item in left.values())
    right_cell_count = sum(int(item["cell_count"]) for item in right.values())
    row: dict[str, Any] = {
        "candidate": name,
        "j_left": left_count,
        "j_right": right_count,
        "source_cells_left": left_cell_count,
        "source_cells_right": right_cell_count,
        "keys_left": len(left),
        "keys_right": len(right),
        "common_keys": len(common),
        "missing_left_keys": len(set(right) - set(left)),
        "missing_right_keys": len(set(left) - set(right)),
        "mean_cells_per_key_left": left_cell_count / len(left) if left else 0.0,
        "mean_cells_per_key_right": right_cell_count / len(right) if right else 0.0,
        "median_cells_per_key_left": median(size_left) if size_left else 0.0,
        "median_cells_per_key_right": median(size_right) if size_right else 0.0,
        "source_weighted_l1_mean": weighted_mean,
        "source_weighted_l1_p95": weighted_quantile(
            [(diff, weight) for diff, weight in weighted_pairs], 0.95
        ),
        "source_weighted_l1_p99": weighted_quantile(
            [(diff, weight) for diff, weight in weighted_pairs], 0.99
        ),
        "source_weighted_l1_max": max(diffs) if diffs else 0.0,
    }
    for key, value in stats.items():
        row[f"key_l1_{key}"] = value
    return row


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.9g}"
    return str(value)


def write_report(
    *,
    rows: list[dict[str, Any]],
    by_count: dict[int, list[dict[str, Any]]],
    args: argparse.Namespace,
    path: Path,
) -> None:
    counts = sorted(by_count)
    lines: list[str] = []
    lines.append("# Refined Prefix-Cauchy Diagnostic")
    lines.append("")
    lines.append("Status: finite diagnostic only.  This report does not prove")
    lines.append("existence or convergence of an infinite operator.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- groups CSV: `{args.groups}`")
    lines.append(f"- distributions CSV: `{args.distributions}`")
    lines.append(f"- T filter: `{args.T}`")
    lines.append(f"- prefix counts: `{', '.join(str(count) for count in counts)}`")
    lines.append(f"- delta cutoff: `{args.delta_cutoff}`")
    lines.append(f"- max low/high bits: `{args.max_bits}`")
    lines.append(f"- include boundary cells: `{args.include_boundary}`")
    lines.append(f"- include mixed source cells: `{args.include_mixed_source}`")
    lines.append("")
    lines.append("## Retained Source Cells")
    lines.append("")
    lines.append("| j_count | retained cells |")
    lines.append("|---:|---:|")
    for count in counts:
        lines.append(f"| {count} | {len(by_count[count])} |")
    lines.append("")
    lines.append("## Best Candidate Rows")
    lines.append("")
    lines.append(
        "Candidates are ranked by source-cell-weighted L1 drift among common "
        "candidate keys.  The minimum mean-cell filter prevents the table "
        "from being dominated by the overfit `source_cell` baseline."
    )
    lines.append("")
    filtered = [
        row
        for row in rows
        if min(
            float(row["mean_cells_per_key_left"]),
            float(row["mean_cells_per_key_right"]),
        )
        >= args.min_mean_cells
    ]
    best = sorted(filtered, key=lambda row: float(row["source_weighted_l1_mean"]))[:15]
    lines.append(
        "| candidate | j_left | j_right | keys | mean cells/key | "
        "weighted L1 mean | weighted L1 p95 | key L1 p95 |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in best:
        mean_cells = min(
            float(row["mean_cells_per_key_left"]),
            float(row["mean_cells_per_key_right"]),
        )
        lines.append(
            f"| `{row['candidate']}` | {row['j_left']} | {row['j_right']} | "
            f"{row['common_keys']} | {format_float(mean_cells)} | "
            f"{format_float(row['source_weighted_l1_mean'])} | "
            f"{format_float(row['source_weighted_l1_p95'])} | "
            f"{format_float(row['key_l1_p95'])} |"
        )
    lines.append("")
    lines.append("## Selected Candidate Rows")
    lines.append("")
    selected_names = {"phase", "phase+rlo5", "phase+rlo10", "phase+rlo11", "phase+rlo12", "source_cell"}
    selected = [row for row in rows if row["candidate"] in selected_names]
    selected.sort(key=lambda row: (int(row["j_left"]), int(row["j_right"]), str(row["candidate"])))
    lines.append(
        "| candidate | j_left | j_right | keys | mean cells/key | "
        "weighted L1 mean | weighted L1 p95 | key L1 p95 | max |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in selected:
        mean_cells = min(
            float(row["mean_cells_per_key_left"]),
            float(row["mean_cells_per_key_right"]),
        )
        lines.append(
            f"| `{row['candidate']}` | {row['j_left']} | {row['j_right']} | "
            f"{row['common_keys']} | {format_float(mean_cells)} | "
            f"{format_float(row['source_weighted_l1_mean'])} | "
            f"{format_float(row['source_weighted_l1_p95'])} | "
            f"{format_float(row['key_l1_p95'])} | "
            f"{format_float(row['source_weighted_l1_max'])} |"
        )
    lines.append("")
    lines.append("## Interpretation Guardrails")
    lines.append("")
    lines.append("- Smaller drift is evidence for a finite averaged-kernel story, not a theorem.")
    lines.append("- The `source_cell` row is an overfit baseline, not a usable finite quotient.")
    lines.append("- A useful analytic alphabet must balance drift against state explosion.")
    lines.append("- These rows compare destination `PhaseState` distributions only.")
    lines.append("- Any infinite-operator claim still requires a topology, norm, and convergence proof.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--groups", type=Path, default=DEFAULT_GROUPS)
    parser.add_argument("--distributions", type=Path, default=DEFAULT_DISTS)
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--delta-cutoff", type=int, default=5)
    parser.add_argument("--no-delta-cutoff", action="store_true")
    parser.add_argument("--max-bits", type=int, default=12)
    parser.add_argument("--min-mean-cells", type=float, default=4.0)
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--include-mixed-source", action="store_true")
    parser.add_argument("--output-tag", default=None)
    args = parser.parse_args()
    if args.no_delta_cutoff:
        args.delta_cutoff = None
    return args


def main() -> None:
    args = parse_args()
    by_count = load_windows(args)
    counts = sorted(by_count)
    if len(counts) < 2:
        raise SystemExit("need at least two prefix j_count values")

    rows: list[dict[str, Any]] = []
    candidates = build_candidates(args.max_bits)
    for left_count, right_count in zip(counts, counts[1:], strict=False):
        left_windows = by_count[left_count]
        right_windows = by_count[right_count]
        for name, key_fn in candidates:
            rows.append(
                score_pair(
                    name=name,
                    key_fn=key_fn,
                    left_count=left_count,
                    right_count=right_count,
                    left_windows=left_windows,
                    right_windows=right_windows,
                )
            )

    report_path, csv_path = output_paths(args.output_tag)
    write_csv(rows, csv_path)
    write_report(rows=rows, by_count=by_count, args=args, path=report_path)
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
