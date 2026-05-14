"""
106_prefix_label_lift.py

Prefix/Cesaro diagnostic for the cost of lifting the good/bad
component kernel back to retained full return labels.

This script consumes the CSVs produced by 88_cylinder_signature_stability.py.
It does not retrace orbits and does not compute spectral-radius bounds.

For each retained source cell and adjacent prefix pair N -> M, it
computes:

    component_l1 = row L1 drift after collapsing destinations to good/bad
    label_l1     = row L1 drift on retained full return signatures
    label_excess = label_l1 - component_l1

The excess is the finite proxy for the error-budget term
ComponentLabelLift.  It is not a theorem and it does not define an
infinite operator.
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
OUT_REPORT = ROOT / "collatz_106_prefix_label_lift_report.md"
OUT_BY_SOURCE = ROOT / "collatz_106_prefix_label_lift_by_source.csv"
OUT_BY_PAIR = ROOT / "collatz_106_prefix_label_lift_by_pair.csv"
OUT_WORST = ROOT / "collatz_106_prefix_label_lift_worst.csv"

State = tuple[int, int, int]
WindowKey = tuple[str, str, str, str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_SOURCE, OUT_BY_PAIR, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_106_{safe}_prefix_label_lift"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_by_source.csv",
        ROOT / f"{stem}_by_pair.csv",
        ROOT / f"{stem}_worst.csv",
    )


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


def load_prefix_windows(args: argparse.Namespace) -> tuple[dict[WindowKey, dict[str, Any]], dict[str, Any]]:
    groups_raw = read_csv(Path(args.groups))
    dists_raw = read_csv(Path(args.distributions))
    windows: dict[WindowKey, dict[str, Any]] = {}
    skipped_mixed = 0
    skipped_boundary = 0

    for row in groups_raw:
        if row["mode"] != "prefix":
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        if not args.include_boundary and row["boundary_flag"] != "bulk":
            skipped_boundary += 1
            continue
        mixed = source_state_mixed(row)
        if not args.include_mixed_source and mixed != 0:
            skipped_mixed += 1
            continue
        src_state = parse_state(row["source_phase"])
        if src_state is None:
            continue
        key = window_key(row)
        windows[key] = {
            "T": row["T"],
            "r": row["r"],
            "h": row["h"],
            "j_count": int(row["j_count"]),
            "sample_count": int(row["sample_count"]),
            "source_phase": row["source_phase"],
            "source_component": component(src_state, args.bad_rule),
            "component_weights": defaultdict(float),
            "label_weights": defaultdict(float),
            "retained_weight": 0.0,
            "tail_weight": 0.0,
            "terminal_count_fraction": 0.0,
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
        status, dst_state, delta = parse_full_signature(row["signature"])
        sample_count = window["sample_count"]
        if sample_count == 0:
            continue
        if status == "terminal":
            window["terminal_count_fraction"] += int(row["count"]) / sample_count
            continue
        assert dst_state is not None
        assert delta is not None
        weight = float(row["weight_sum"]) / sample_count
        if args.delta_cutoff is not None and delta > args.delta_cutoff:
            window["tail_weight"] += weight
            continue
        dst_comp = component(dst_state, args.bad_rule)
        window["component_weights"][dst_comp] += weight
        window["label_weights"][row["signature"]] += weight
        window["retained_weight"] += weight

    meta = {
        "prefix_windows": len(windows),
        "skipped_mixed_windows": skipped_mixed,
        "skipped_boundary_windows": skipped_boundary,
    }
    return windows, meta


def l1_diff(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    return sum(abs(float(a.get(key, 0.0)) - float(b.get(key, 0.0))) for key in keys)


def prefix_drifts(windows: dict[WindowKey, dict[str, Any]]) -> list[dict[str, Any]]:
    by_cell: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for window in windows.values():
        by_cell[(window["T"], window["r"], window["h"])].append(window)

    rows: list[dict[str, Any]] = []
    for (_T, _r, _h), cell_windows in by_cell.items():
        ordered = sorted(cell_windows, key=lambda row: row["j_count"])
        for a, b in zip(ordered, ordered[1:]):
            if a["source_component"] != b["source_component"]:
                continue
            component_l1 = l1_diff(a["component_weights"], b["component_weights"])
            label_l1 = l1_diff(a["label_weights"], b["label_weights"])
            retained_row_sum_abs_diff = abs(a["retained_weight"] - b["retained_weight"])
            tail_row_sum_abs_diff = abs(a["tail_weight"] - b["tail_weight"])
            label_excess = max(0.0, label_l1 - component_l1)
            rows.append({
                "T": a["T"],
                "r": a["r"],
                "h": a["h"],
                "source_phase": a["source_phase"],
                "source_component": a["source_component"],
                "j_count_a": a["j_count"],
                "j_count_b": b["j_count"],
                "component_l1": component_l1,
                "label_l1": label_l1,
                "label_excess": label_excess,
                "retained_row_sum_abs_diff": retained_row_sum_abs_diff,
                "tail_row_sum_abs_diff": tail_row_sum_abs_diff,
                "retained_weight_a": a["retained_weight"],
                "retained_weight_b": b["retained_weight"],
                "tail_weight_a": a["tail_weight"],
                "tail_weight_b": b["tail_weight"],
            })
    return rows


def summarize_metric(rows: list[dict[str, Any]], metric: str, label: str) -> dict[str, Any]:
    values = [float(row[metric]) for row in rows]
    return {
        "class": label,
        "metric": metric,
        "count": len(values),
        "mean": mean(values) if values else 0.0,
        "p50": quantile(values, 0.50),
        "p90": quantile(values, 0.90),
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
    }


def summarize(args: argparse.Namespace) -> tuple[
    str,
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    windows, meta = load_prefix_windows(args)
    drifts = prefix_drifts(windows)
    if not drifts:
        raise SystemExit("no prefix drifts found")

    metrics = [
        "component_l1",
        "label_l1",
        "label_excess",
        "retained_row_sum_abs_diff",
        "tail_row_sum_abs_diff",
    ]

    source_rows: list[dict[str, Any]] = []
    for source_comp in ("all", "good", "bad"):
        selected = drifts if source_comp == "all" else [
            row for row in drifts if row["source_component"] == source_comp
        ]
        for metric in metrics:
            source_rows.append(summarize_metric(selected, metric, source_comp))

    pair_rows: list[dict[str, Any]] = []
    pair_keys = sorted({(row["j_count_a"], row["j_count_b"]) for row in drifts})
    for a_count, b_count in pair_keys:
        pair_selected = [
            row for row in drifts
            if row["j_count_a"] == a_count and row["j_count_b"] == b_count
        ]
        for source_comp in ("all", "good", "bad"):
            selected = pair_selected if source_comp == "all" else [
                row for row in pair_selected if row["source_component"] == source_comp
            ]
            for metric in ("component_l1", "label_l1", "label_excess"):
                item = summarize_metric(selected, metric, source_comp)
                item["j_count_a"] = a_count
                item["j_count_b"] = b_count
                pair_rows.append(item)

    worst = sorted(
        drifts,
        key=lambda row: (-row["label_excess"], -row["label_l1"], int(row["T"]), int(row["r"]), int(row["h"])),
    )[: args.limit]

    active_T = sorted({row["T"] for row in drifts}, key=int)
    prefix_counts = sorted({row["j_count_a"] for row in drifts} | {row["j_count_b"] for row in drifts})
    cutoff_text = "none" if args.delta_cutoff is None else str(args.delta_cutoff)

    lines = [
        "# Prefix Label-Lift Diagnostic",
        "",
        "Status: finite diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- distributions file: `{args.distributions}`",
        f"- T filter: `{args.T if args.T is not None else 'all'}`",
        f"- active T values: `{', '.join(active_T)}`",
        f"- bad rule: `{args.bad_rule}`",
        f"- bad convention: `{bad_rule_description(args.bad_rule)}`",
        f"- delta cutoff: `{cutoff_text}`",
        f"- include boundary: `{args.include_boundary}`",
        f"- include mixed source cells: `{args.include_mixed_source}`",
        f"- prefix counts: `{', '.join(str(x) for x in prefix_counts)}`",
        f"- prefix windows used: `{meta['prefix_windows']}`",
        f"- skipped mixed-source windows: `{meta['skipped_mixed_windows']}`",
        f"- skipped boundary windows: `{meta['skipped_boundary_windows']}`",
        "",
        "`component_l1` is the substochastic row `L1` prefix drift after",
        "collapsing return destinations to `good/bad`.  `label_l1` is the",
        "same drift on retained full return signatures.  `label_excess` is",
        "the nonnegative difference `label_l1 - component_l1` and is the",
        "finite proxy for `ComponentLabelLift`.",
        "",
        "All summary means are uniform over retained source cells/prefix",
        "pairs.  By default this excludes boundary rows and mixed-source",
        "cells, so the implicit source weight is finite counting measure,",
        "not a proved limiting Haar measure.",
        "",
        "## By Source Component",
        "",
        "| source | metric | count | mean | p90 | p95 | p99 | max |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in source_rows:
        lines.append(
            f"| `{row['class']}` | `{row['metric']}` | {row['count']} | "
            f"{row['mean']:.8g} | {row['p90']:.8g} | {row['p95']:.8g} | "
            f"{row['p99']:.8g} | {row['max']:.8g} |"
        )

    lines.extend([
        "",
        "## By Prefix Pair",
        "",
        "| pair | source | metric | count | mean | p95 | p99 | max |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ])
    for row in pair_rows:
        lines.append(
            f"| `{row['j_count_a']}->{row['j_count_b']}` | `{row['class']}` | "
            f"`{row['metric']}` | {row['count']} | {row['mean']:.8g} | "
            f"{row['p95']:.8g} | {row['p99']:.8g} | {row['max']:.8g} |"
        )

    lines.extend([
        "",
        "## Worst Label-Excess Rows",
        "",
        "| T | r | h | source | pair | component L1 | label L1 | label excess | retained row diff | tail row diff |",
        "|---:|---:|---:|---|---|---:|---:|---:|---:|---:|",
    ])
    for row in worst:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | `{row['source_component']}` | "
            f"`{row['j_count_a']}->{row['j_count_b']}` | "
            f"{row['component_l1']:.8g} | {row['label_l1']:.8g} | "
            f"{row['label_excess']:.8g} | {row['retained_row_sum_abs_diff']:.8g} | "
            f"{row['tail_row_sum_abs_diff']:.8g} |"
        )

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "Small `component_l1` with large `label_excess` means the good/bad",
        "kernel is hiding retained-label drift.  Small `label_excess` would",
        "support, but not prove, lifting the component kernel to retained",
        "labels in a weak averaged norm.  This diagnostic does not define",
        "an infinite operator and does not imply a spectral gap.",
    ])
    return "\n".join(lines) + "\n", source_rows, pair_rows, worst


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure prefix label-lift drift above good/bad component drift.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--delta-cutoff", type=int, default=None)
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
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, source_rows, pair_rows, worst_rows = summarize(args)
    report_path, source_path, pair_path, worst_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(source_rows, source_path)
    write_csv(pair_rows, pair_path)
    write_csv(worst_rows, worst_path)
    print("Prefix label-lift diagnostic written:")
    print(f"  {report_path.name}")
    print(f"  {source_path.name}")
    print(f"  {pair_path.name}")
    print(f"  {worst_path.name}")


if __name__ == "__main__":
    main()
