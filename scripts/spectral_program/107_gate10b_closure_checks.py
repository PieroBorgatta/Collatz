"""
107_gate10b_closure_checks.py

Finite Gate-10.B closure checks for the prefix/Cesaro branch.

This script consumes the CSVs produced by 88_cylinder_signature_stability.py.
It does not retrace orbits and does not compute spectral-radius bounds.

It verifies finite bookkeeping lemmas needed before the analytic
Gate-10.B question can be posed cleanly:

1. retained-source averaging correction;
2. row-source identity for the empirical prefix kernel;
3. component/phase/label contraction and excess;
4. retained-label tail split.

These are finite checks only.  They do not prove an infinite operator,
mixed-norm convergence, a Lasota-Yorke inequality, or a spectral gap.
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
DEFAULT_DISTS = ROOT / "collatz_88_signature_distribution.csv"
OUT_REPORT = ROOT / "collatz_107_gate10b_closure_checks_report.md"
OUT_BY_PAIR = ROOT / "collatz_107_gate10b_closure_checks_by_pair.csv"

State = tuple[int, int, int]
WindowKey = tuple[str, str, str, str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_PAIR
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_107_{safe}_gate10b_closure_checks"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_pair.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


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


def parse_state(text: str) -> State | None:
    if text == "terminal":
        return None
    parts = {}
    for item in text.split("|"):
        key, value = item.split("=", 1)
        parts[key] = int(value)
    return (parts["v2"], parts["odd"], parts["h"])


def parse_full_signature(text: str) -> tuple[str, State | None, int | None]:
    if text == "terminal":
        return "terminal", None, None
    parts = text.split("|")
    if len(parts) != 5 or parts[0] != "return":
        raise ValueError(f"unexpected full signature: {text}")
    state = (int(parts[1]), int(parts[2]), int(parts[3]))
    delta = int(parts[4])
    return "return", state, delta


def bad_state(state: State, rule: str) -> bool:
    v2, odd, _h = state
    if rule == "odd3_v2_0_or_2":
        return odd == 3 and v2 in {0, 2}
    if rule == "v2_2_odd3":
        return v2 == 2 and odd == 3
    if rule == "v2_0_odd3":
        return v2 == 0 and odd == 3
    if rule == "odd3":
        return odd == 3
    if rule == "v2_2":
        return v2 == 2
    if rule == "odd3_or_v2_2":
        return odd == 3 or v2 == 2
    raise ValueError(f"unknown bad rule: {rule}")


def component(state: State, rule: str) -> str:
    return "bad" if bad_state(state, rule) else "good"


def bad_rule_description(rule: str) -> str:
    descriptions = {
        "odd3_v2_0_or_2": "src_odd == 3 and src_v2 in {0, 2}",
        "v2_2_odd3": "src_v2 == 2 and src_odd == 3",
        "v2_0_odd3": "src_v2 == 0 and src_odd == 3",
        "odd3": "src_odd == 3",
        "v2_2": "src_v2 == 2",
        "odd3_or_v2_2": "src_odd == 3 or src_v2 == 2",
    }
    return descriptions[rule]


def window_key(row: dict[str, str]) -> WindowKey:
    return (
        row["T"],
        row["r"],
        row["h"],
        row["mode"],
        row["j_start"],
        row["j_count"],
    )


def source_state_mixed(row: dict[str, str]) -> int:
    if "source_state_mixed" in row:
        return int(row["source_state_mixed"])
    if "source_state_count" in row:
        return int(int(row["source_state_count"]) > 1)
    return 0


def l1_diff(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    return sum(abs(float(a.get(key, 0.0)) - float(b.get(key, 0.0))) for key in keys)


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "mean": mean(values) if values else 0.0,
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
    }


def load_windows(args: argparse.Namespace) -> tuple[dict[WindowKey, dict[str, Any]], dict[str, Any]]:
    groups_raw = read_csv(Path(args.groups))
    dists_raw = read_csv(Path(args.distributions))
    windows: dict[WindowKey, dict[str, Any]] = {}
    all_prefix_cells_by_count: dict[int, set[tuple[str, str, str]]] = defaultdict(set)
    retained_cells_by_count: dict[int, set[tuple[str, str, str]]] = defaultdict(set)
    skipped_mixed_by_count: dict[int, int] = defaultdict(int)
    skipped_boundary_by_count: dict[int, int] = defaultdict(int)

    for row in groups_raw:
        if row["mode"] != "prefix":
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        j_count = int(row["j_count"])
        cell = (row["T"], row["r"], row["h"])
        all_prefix_cells_by_count[j_count].add(cell)
        mixed = source_state_mixed(row)
        boundary = row["boundary_flag"] != "bulk"
        if not args.include_boundary and boundary:
            skipped_boundary_by_count[j_count] += 1
            continue
        if not args.include_mixed_source and mixed != 0:
            skipped_mixed_by_count[j_count] += 1
            continue
        src_state = parse_state(row["source_phase"])
        if src_state is None:
            continue
        retained_cells_by_count[j_count].add(cell)
        key = window_key(row)
        sample_count = int(row["sample_count"])
        windows[key] = {
            "T": row["T"],
            "r": row["r"],
            "h": row["h"],
            "j_count": j_count,
            "sample_count": sample_count,
            "source_phase": row["source_phase"],
            "source_component": component(src_state, args.bad_rule),
            "group_full_weight": float(row["full_weight"]),
            "group_terminal_fraction": float(row["terminal_fraction"]),
            "label_weights": defaultdict(float),
            "phase_weights": defaultdict(float),
            "component_weights": defaultdict(float),
            "tail_weight": 0.0,
            "retained_weight": 0.0,
            "full_count_sum": 0,
            "full_weight_sum": 0.0,
            "terminal_count": 0,
            "full_rows_seen": 0,
        }

    for row in dists_raw:
        if row["mode"] != "prefix" or row["signature_level"] != "full":
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        key = window_key(row)
        window = windows.get(key)
        if window is None:
            continue
        count = int(row["count"])
        weight_sum = float(row["weight_sum"])
        sample_count = window["sample_count"]
        status, dst_state, delta = parse_full_signature(row["signature"])
        window["full_count_sum"] += count
        window["full_weight_sum"] += weight_sum
        window["full_rows_seen"] += 1
        if status == "terminal":
            window["terminal_count"] += count
            continue
        assert dst_state is not None
        assert delta is not None
        normalized_weight = weight_sum / sample_count if sample_count else 0.0
        if args.delta_cutoff is not None and delta > args.delta_cutoff:
            window["tail_weight"] += normalized_weight
            continue
        dst_comp = component(dst_state, args.bad_rule)
        phase_key = f"{dst_state[0]}|{dst_state[1]}|{dst_state[2]}"
        window["phase_weights"][phase_key] += normalized_weight
        window["label_weights"][row["signature"]] += normalized_weight
        window["component_weights"][dst_comp] += normalized_weight
        window["retained_weight"] += normalized_weight

    identity_residuals = {
        "max_full_count_residual": 0,
        "max_full_weight_residual": 0.0,
        "max_terminal_fraction_residual": 0.0,
        "windows_with_count_residual": 0,
        "windows_with_weight_residual": 0,
        "windows_with_terminal_residual": 0,
    }
    for window in windows.values():
        count_resid = abs(window["full_count_sum"] - window["sample_count"])
        weight_resid = abs(window["full_weight_sum"] - window["group_full_weight"])
        terminal_fraction = window["terminal_count"] / window["sample_count"] if window["sample_count"] else 0.0
        terminal_resid = abs(terminal_fraction - window["group_terminal_fraction"])
        identity_residuals["max_full_count_residual"] = max(
            identity_residuals["max_full_count_residual"], count_resid
        )
        identity_residuals["max_full_weight_residual"] = max(
            identity_residuals["max_full_weight_residual"], weight_resid
        )
        identity_residuals["max_terminal_fraction_residual"] = max(
            identity_residuals["max_terminal_fraction_residual"], terminal_resid
        )
        if count_resid:
            identity_residuals["windows_with_count_residual"] += 1
        if weight_resid > args.tolerance:
            identity_residuals["windows_with_weight_residual"] += 1
        if terminal_resid > args.tolerance:
            identity_residuals["windows_with_terminal_residual"] += 1

    source_rows = []
    for j_count in sorted(all_prefix_cells_by_count):
        full_count = len(all_prefix_cells_by_count[j_count])
        retained_count = len(retained_cells_by_count[j_count])
        excluded_count = full_count - retained_count
        source_rows.append({
            "j_count": j_count,
            "full_source_cells": full_count,
            "retained_source_cells": retained_count,
            "excluded_source_cells": excluded_count,
            "skipped_mixed_windows": skipped_mixed_by_count[j_count],
            "skipped_boundary_windows": skipped_boundary_by_count[j_count],
            "excluded_fraction": excluded_count / full_count if full_count else 0.0,
            "mean_error_coeff": 2 * excluded_count / full_count if full_count else 0.0,
        })

    meta = {
        "source_rows": source_rows,
        "identity_residuals": identity_residuals,
        "window_count": len(windows),
    }
    return windows, meta


def pair_checks(windows: dict[WindowKey, dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    by_cell: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for window in windows.values():
        by_cell[(window["T"], window["r"], window["h"])].append(window)

    by_pair_values: dict[tuple[int, int], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    by_pair_counts: dict[tuple[int, int], int] = defaultdict(int)
    component_phase_violations = 0
    phase_label_violations = 0
    component_label_violations = 0
    min_component_phase_excess = float("inf")
    min_phase_label_excess = float("inf")
    min_label_excess = float("inf")

    for cell_windows in by_cell.values():
        ordered = sorted(cell_windows, key=lambda row: row["j_count"])
        for a, b in zip(ordered, ordered[1:]):
            if a["source_component"] != b["source_component"]:
                continue
            pair = (a["j_count"], b["j_count"])
            component_l1 = l1_diff(a["component_weights"], b["component_weights"])
            phase_l1 = l1_diff(a["phase_weights"], b["phase_weights"])
            label_l1 = l1_diff(a["label_weights"], b["label_weights"])
            component_phase_excess = phase_l1 - component_l1
            phase_label_excess = label_l1 - phase_l1
            label_excess = label_l1 - component_l1
            tail_abs_diff = abs(a["tail_weight"] - b["tail_weight"])
            retained_abs_diff = abs(a["retained_weight"] - b["retained_weight"])
            if component_phase_excess < -args.tolerance:
                component_phase_violations += 1
            if phase_label_excess < -args.tolerance:
                phase_label_violations += 1
            if label_excess < -args.tolerance:
                component_label_violations += 1
            min_component_phase_excess = min(min_component_phase_excess, component_phase_excess)
            min_phase_label_excess = min(min_phase_label_excess, phase_label_excess)
            min_label_excess = min(min_label_excess, label_excess)
            by_pair_counts[pair] += 1
            by_pair_values[pair]["component_l1"].append(component_l1)
            by_pair_values[pair]["phase_l1"].append(phase_l1)
            by_pair_values[pair]["label_l1"].append(label_l1)
            by_pair_values[pair]["component_phase_excess"].append(max(0.0, component_phase_excess))
            by_pair_values[pair]["phase_label_excess"].append(max(0.0, phase_label_excess))
            by_pair_values[pair]["label_excess"].append(max(0.0, label_excess))
            by_pair_values[pair]["tail_abs_diff"].append(tail_abs_diff)
            by_pair_values[pair]["retained_row_sum_abs_diff"].append(retained_abs_diff)
            by_pair_values[pair]["tail_weight_a"].append(a["tail_weight"])
            by_pair_values[pair]["tail_weight_b"].append(b["tail_weight"])

    rows: list[dict[str, Any]] = []
    for pair in sorted(by_pair_values):
        values = by_pair_values[pair]
        row: dict[str, Any] = {
            "pair": f"{pair[0]}->{pair[1]}",
            "count": by_pair_counts[pair],
        }
        for metric in (
            "component_l1",
            "phase_l1",
            "label_l1",
            "component_phase_excess",
            "phase_label_excess",
            "label_excess",
            "tail_abs_diff",
            "retained_row_sum_abs_diff",
            "tail_weight_a",
            "tail_weight_b",
        ):
            stats = summarize(values[metric])
            for key, value in stats.items():
                row[f"{metric}_{key}"] = value
        rows.append(row)

    for row in rows:
        row["component_to_phase_violations"] = component_phase_violations
        row["phase_to_label_violations"] = phase_label_violations
        row["component_to_label_violations"] = component_label_violations
        row["min_raw_component_phase_excess"] = (
            min_component_phase_excess if min_component_phase_excess != float("inf") else 0.0
        )
        row["min_raw_phase_label_excess"] = (
            min_phase_label_excess if min_phase_label_excess != float("inf") else 0.0
        )
        row["min_raw_label_excess"] = min_label_excess if min_label_excess != float("inf") else 0.0
    return rows


def average_row(rows: list[dict[str, Any]], key: str) -> dict[str, float]:
    if not rows:
        return {}
    out: dict[str, float] = defaultdict(float)
    scale = 1.0 / len(rows)
    for row in rows:
        for dst, value in row[key].items():
            out[dst] += float(value) * scale
    return dict(out)


def source_phase_collapse_checks(windows: dict[WindowKey, dict[str, Any]]) -> list[dict[str, Any]]:
    by_count_phase: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for window in windows.values():
        by_count_phase[(window["j_count"], window["source_phase"])].append(window)

    values_by_count: dict[int, list[float]] = defaultdict(list)
    cells_by_count: dict[int, int] = defaultdict(int)
    phases_by_count: dict[int, int] = defaultdict(int)
    worst_by_count: dict[int, tuple[str, float]] = {}

    for (j_count, source_phase), rows in by_count_phase.items():
        phases_by_count[j_count] += 1
        cells_by_count[j_count] += len(rows)
        averaged = average_row(rows, "phase_weights")
        diffs = [l1_diff(row["phase_weights"], averaged) for row in rows]
        values_by_count[j_count].extend(diffs)
        group_mean = mean(diffs) if diffs else 0.0
        current = worst_by_count.get(j_count)
        if current is None or group_mean > current[1]:
            worst_by_count[j_count] = (source_phase, group_mean)

    out = []
    for j_count in sorted(values_by_count):
        stats = summarize(values_by_count[j_count])
        worst_phase, worst_mean = worst_by_count[j_count]
        row: dict[str, Any] = {
            "j_count": j_count,
            "source_cells": cells_by_count[j_count],
            "source_phase_classes": phases_by_count[j_count],
            "worst_source_phase": worst_phase,
            "worst_source_phase_mean": worst_mean,
        }
        for key, value in stats.items():
            row[f"phase_collapse_l1_{key}"] = value
        out.append(row)
    return out


def render_report(
    args: argparse.Namespace,
    meta: dict[str, Any],
    pair_rows: list[dict[str, Any]],
    collapse_rows: list[dict[str, Any]],
) -> str:
    identity = meta["identity_residuals"]
    cutoff_text = "none" if args.delta_cutoff is None else str(args.delta_cutoff)
    lines = [
        "# Gate 10.B Closure Checks",
        "",
        "Status: finite bookkeeping diagnostic, not an infinite-operator theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- distributions file: `{args.distributions}`",
        f"- T filter: `{args.T if args.T is not None else 'all'}`",
        f"- bad rule: `{args.bad_rule}`",
        f"- bad convention: `{bad_rule_description(args.bad_rule)}`",
        f"- delta cutoff: `{cutoff_text}`",
        f"- include boundary: `{args.include_boundary}`",
        f"- include mixed source cells: `{args.include_mixed_source}`",
        f"- retained prefix windows: `{meta['window_count']}`",
        "",
        "## Source Averaging",
        "",
        "| j_count | full cells | retained cells | excluded | excluded fraction | mean error coeff | skipped mixed | skipped boundary |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in meta["source_rows"]:
        lines.append(
            f"| {row['j_count']} | {row['full_source_cells']} | "
            f"{row['retained_source_cells']} | {row['excluded_source_cells']} | "
            f"{row['excluded_fraction']:.10g} | {row['mean_error_coeff']:.10g} | "
            f"{row['skipped_mixed_windows']} | {row['skipped_boundary_windows']} |"
        )

    lines.extend([
        "",
        "For bounded row diagnostics `F`, the finite retained-source mean",
        "differs from the complete-cell mean by at most:",
        "",
        "```text",
        "2 * excluded_fraction * ||F||_infty.",
        "```",
        "",
        "This is a finite correction only; it is not a Haar-limit theorem.",
        "",
        "## Row-Source Identity Checks",
        "",
        "| check | value |",
        "|---|---:|",
        f"| max full-count residual | {identity['max_full_count_residual']} |",
        f"| windows with count residual | {identity['windows_with_count_residual']} |",
        f"| max full-weight residual | {identity['max_full_weight_residual']:.12g} |",
        f"| windows with weight residual | {identity['windows_with_weight_residual']} |",
        f"| max terminal-fraction residual | {identity['max_terminal_fraction_residual']:.12g} |",
        f"| windows with terminal residual | {identity['windows_with_terminal_residual']} |",
        "",
        "A zero residual means the CSV full-signature rows exactly define",
        "the empirical row-source prefix kernel used by later diagnostics.",
        "It does not identify that empirical kernel with `E U_s I`.",
        "",
        "## Prefix Pair Checks",
        "",
        "| pair | rows | component mean | phase mean | label mean | comp-phase excess | phase-label excess | tail-diff mean | tail-a mean | tail-b mean | violations |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in pair_rows:
        lines.append(
            f"| `{row['pair']}` | {row['count']} | "
            f"{row['component_l1_mean']:.8g} | {row['phase_l1_mean']:.8g} | "
            f"{row['label_l1_mean']:.8g} | "
            f"{row['component_phase_excess_mean']:.8g} | "
            f"{row['phase_label_excess_mean']:.8g} | "
            f"{row['tail_abs_diff_mean']:.8g} | {row['tail_weight_a_mean']:.8g} | "
            f"{row['tail_weight_b_mean']:.8g} | "
            f"{row['component_to_phase_violations']}/"
            f"{row['phase_to_label_violations']}/"
            f"{row['component_to_label_violations']} |"
        )

    lines.extend([
        "",
        "The contraction checks are the finite projection inequalities:",
        "",
        "```text",
        "||pi_component p - pi_component q||_1",
        "  <= ||pi_phase p - pi_phase q||_1",
        "  <= ||p - q||_1.",
        "",
        "||pi_*p - pi_*q||_1 <= ||p - q||_1.",
        "```",
        "",
        "`phase_l1` is the drift most directly aligned with the current",
        "Lean `TransferMatrix V` state space.  The label excess terms are",
        "stronger diagnostics.  If they do not tend to zero, they cannot be",
        "silently absorbed into a labelled infinite operator.",
        "",
        "The tail columns are finite source-averaged checks of the split",
        "`K_N = K_N^{<=L} + K_N^{>L}`.  They do not provide uniform",
        "sourcewise tail control.",
        "",
        "## Source-Phase Collapse Checks",
        "",
        "| j_count | source cells | phase classes | collapse mean | collapse p95 | collapse p99 | collapse max | worst phase | worst phase mean |",
        "|---:|---:|---:|---:|---:|---:|---:|---|---:|",
    ])
    for row in collapse_rows:
        lines.append(
            f"| {row['j_count']} | {row['source_cells']} | "
            f"{row['source_phase_classes']} | "
            f"{row['phase_collapse_l1_mean']:.8g} | "
            f"{row['phase_collapse_l1_p95']:.8g} | "
            f"{row['phase_collapse_l1_p99']:.8g} | "
            f"{row['phase_collapse_l1_max']:.8g} | "
            f"`{row['worst_source_phase']}` | "
            f"{row['worst_source_phase_mean']:.8g} |"
        )

    lines.extend([
        "",
        "This measures the weak error incurred by replacing retained source",
        "cells `(T,r,h)` with rows indexed only by their source `PhaseState`.",
        "A nonzero value is not a bug: it means a `PhaseState -> PhaseState`",
        "matrix is an additional averaged quotient, not an exact projection",
        "of the source-cell kernel.",
        "",
        "## Non-Claims",
        "",
        "This report does not prove a limiting kernel, Banach boundedness,",
        "Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap, or",
        "Conjecture 6.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finite Gate-10.B closure bookkeeping checks.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--delta-cutoff", type=int, default=5)
    parser.add_argument("--bad-rule", default="odd3_v2_0_or_2", choices=[
        "odd3_v2_0_or_2",
        "v2_2_odd3",
        "v2_0_odd3",
        "odd3",
        "v2_2",
        "odd3_or_v2_2",
    ])
    parser.add_argument("--include-boundary", action="store_true")
    parser.add_argument("--include-mixed-source", action="store_true")
    parser.add_argument(
        "--no-delta-cutoff",
        action="store_true",
        help="Keep all return labels instead of sending delta > cutoff to the tail.",
    )
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--output-tag", default=None)
    args = parser.parse_args()
    if args.no_delta_cutoff:
        args.delta_cutoff = None
    return args


def main() -> None:
    args = parse_args()
    windows, meta = load_windows(args)
    pair_rows = pair_checks(windows, args)
    collapse_rows = source_phase_collapse_checks(windows)
    report = render_report(args, meta, pair_rows, collapse_rows)
    report_path, pair_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(pair_rows, pair_path)
    print("Gate 10.B closure checks written:")
    print(f"  {report_path.name}")
    print(f"  {pair_path.name}")


if __name__ == "__main__":
    main()
