"""
104_component_block_cauchy.py

Component-level adjacent-block drift for the Phase 10 two-component
kernel candidate.

This script consumes the CSVs produced by 88_cylinder_signature_stability.py.
It does not retrace orbits and does not compute spectral-radius bounds.

For each block window, it collapses full return signatures into weighted
mass toward the declared destination component:

    good -> good, good -> bad, bad -> good, bad -> bad.

It then compares adjacent high-lift blocks.  The main quantity is the
subprobability row L1 drift

    sum_{dst in {good,bad}} |K_block_a(src,dst) - K_block_b(src,dst)|,

with terminal/killed events recorded separately.  This is a finite
diagnostic for a possible mixed-norm approximation term, not a theorem.
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
OUT_REPORT = ROOT / "collatz_104_component_block_cauchy_report.md"
OUT_BY_SOURCE = ROOT / "collatz_104_component_block_cauchy_by_source.csv"
OUT_BY_ENTRY = ROOT / "collatz_104_component_block_cauchy_by_entry.csv"
OUT_BY_PAIR = ROOT / "collatz_104_component_block_cauchy_by_pair.csv"
OUT_WORST = ROOT / "collatz_104_component_block_cauchy_worst.csv"

State = tuple[int, int, int]
WindowKey = tuple[str, str, str, str, str, str]


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_SOURCE, OUT_BY_ENTRY, OUT_BY_PAIR, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_104_{safe}_component_block_cauchy"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_by_source.csv",
        ROOT / f"{stem}_by_entry.csv",
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


def parse_full_signature(text: str) -> tuple[str, State | None]:
    if text == "terminal":
        return "terminal", None
    parts = text.split("|")
    if len(parts) != 5 or parts[0] != "return":
        raise ValueError(f"unexpected full signature: {text}")
    return "return", (int(parts[1]), int(parts[2]), int(parts[3]))


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


def load_block_windows(args: argparse.Namespace) -> tuple[dict[WindowKey, dict[str, Any]], dict[str, Any]]:
    groups_raw = read_csv(Path(args.groups))
    dists_raw = read_csv(Path(args.distributions))
    windows: dict[WindowKey, dict[str, Any]] = {}
    skipped_mixed = 0
    skipped_boundary = 0

    for row in groups_raw:
        if row["mode"] != "block":
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
            "mode": row["mode"],
            "j_start": int(row["j_start"]),
            "j_count": int(row["j_count"]),
            "sample_count": int(row["sample_count"]),
            "source_phase": row["source_phase"],
            "source_component": component(src_state, args.bad_rule),
            "source_state_mixed": mixed,
            "boundary_flag": row["boundary_flag"],
            "count_terminal": 0.0,
            "count_good": 0.0,
            "count_bad": 0.0,
            "weight_good": 0.0,
            "weight_bad": 0.0,
        }

    for row in dists_raw:
        if row["mode"] != "block" or row["signature_level"] != "full":
            continue
        if args.T is not None and int(row["T"]) != args.T:
            continue
        key = window_key(row)
        window = windows.get(key)
        if window is None:
            continue
        status, dst_state = parse_full_signature(row["signature"])
        sample_count = window["sample_count"]
        count_frac = int(row["count"]) / sample_count if sample_count else 0.0
        weight = float(row["weight_sum"]) / sample_count if sample_count else 0.0
        if status == "terminal":
            window["count_terminal"] += count_frac
            continue
        assert dst_state is not None
        dst_comp = component(dst_state, args.bad_rule)
        window[f"count_{dst_comp}"] += count_frac
        window[f"weight_{dst_comp}"] += weight

    meta = {
        "block_windows": len(windows),
        "skipped_mixed_windows": skipped_mixed,
        "skipped_boundary_windows": skipped_boundary,
    }
    return windows, meta


def adjacent_drifts(windows: dict[WindowKey, dict[str, Any]]) -> list[dict[str, Any]]:
    by_cell: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for window in windows.values():
        cell_key = (window["T"], window["r"], window["h"], str(window["j_count"]))
        by_cell[cell_key].append(window)

    rows: list[dict[str, Any]] = []
    for (_T, _r, _h, _block_size), cell_windows in by_cell.items():
        ordered = sorted(cell_windows, key=lambda row: row["j_start"])
        by_start = {row["j_start"]: row for row in ordered}
        if not ordered:
            continue
        block_size = ordered[0]["j_count"]
        for a in ordered:
            b = by_start.get(a["j_start"] + block_size)
            if b is None:
                continue
            if a["source_component"] != b["source_component"]:
                continue
            source_comp = a["source_component"]
            abs_good = abs(a["weight_good"] - b["weight_good"])
            abs_bad = abs(a["weight_bad"] - b["weight_bad"])
            row_sum_a = a["weight_good"] + a["weight_bad"]
            row_sum_b = b["weight_good"] + b["weight_bad"]
            count_tv = 0.5 * (
                abs(a["count_terminal"] - b["count_terminal"])
                + abs(a["count_good"] - b["count_good"])
                + abs(a["count_bad"] - b["count_bad"])
            )
            rows.append({
                "T": a["T"],
                "r": a["r"],
                "h": a["h"],
                "source_phase": a["source_phase"],
                "source_component": source_comp,
                "block_a_start": a["j_start"],
                "block_b_start": b["j_start"],
                "block_size": block_size,
                "weighted_l1": abs_good + abs_bad,
                "row_sum_abs_diff": abs(row_sum_a - row_sum_b),
                "count_tv_terminal_good_bad": count_tv,
                "terminal_abs_diff": abs(a["count_terminal"] - b["count_terminal"]),
                "dst_good_abs_diff": abs_good,
                "dst_bad_abs_diff": abs_bad,
                "row_sum_a": row_sum_a,
                "row_sum_b": row_sum_b,
                "count_terminal_a": a["count_terminal"],
                "count_terminal_b": b["count_terminal"],
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
    list[dict[str, Any]],
]:
    windows, meta = load_block_windows(args)
    drifts = adjacent_drifts(windows)
    if not drifts:
        raise SystemExit("no adjacent block drifts found")

    source_rows: list[dict[str, Any]] = []
    metrics = [
        "weighted_l1",
        "row_sum_abs_diff",
        "count_tv_terminal_good_bad",
        "terminal_abs_diff",
    ]
    for source_comp in ("all", "good", "bad"):
        selected = drifts if source_comp == "all" else [
            row for row in drifts if row["source_component"] == source_comp
        ]
        for metric in metrics:
            source_rows.append(summarize_metric(selected, metric, source_comp))

    pair_rows: list[dict[str, Any]] = []
    pair_keys = sorted(
        {(row["block_a_start"], row["block_b_start"]) for row in drifts},
        key=lambda pair: (int(pair[0]), int(pair[1])),
    )
    for a_start, b_start in pair_keys:
        pair_selected = [
            row for row in drifts
            if row["block_a_start"] == a_start and row["block_b_start"] == b_start
        ]
        for source_comp in ("all", "good", "bad"):
            selected = pair_selected if source_comp == "all" else [
                row for row in pair_selected if row["source_component"] == source_comp
            ]
            item = summarize_metric(selected, "weighted_l1", source_comp)
            item["block_a_start"] = a_start
            item["block_b_start"] = b_start
            pair_rows.append(item)

    entry_specs = [
        ("good", "good", "dst_good_abs_diff", "K_GG"),
        ("good", "bad", "dst_bad_abs_diff", "K_GB"),
        ("bad", "good", "dst_good_abs_diff", "K_BG"),
        ("bad", "bad", "dst_bad_abs_diff", "K_BB"),
    ]
    entry_rows: list[dict[str, Any]] = []
    for source_comp, dst_comp, metric, entry in entry_specs:
        selected = [row for row in drifts if row["source_component"] == source_comp]
        summary = summarize_metric(selected, metric, entry)
        summary["source_component"] = source_comp
        summary["dst_component"] = dst_comp
        entry_rows.append(summary)

    worst = sorted(drifts, key=lambda row: (-row["weighted_l1"], int(row["T"]), int(row["r"]), int(row["h"])))[: args.limit]

    active_T = sorted({row["T"] for row in drifts}, key=int)
    block_sizes = sorted({row["block_size"] for row in drifts})
    block_pairs = sorted({(row["block_a_start"], row["block_b_start"]) for row in drifts})

    lines = [
        "# Component Block-Cauchy Diagnostic",
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
        f"- include boundary: `{args.include_boundary}`",
        f"- include mixed source cells: `{args.include_mixed_source}`",
        f"- block sizes: `{', '.join(str(x) for x in block_sizes)}`",
        f"- adjacent block pairs: `{', '.join(f'{a}->{b}' for a, b in block_pairs)}`",
        f"- block windows used: `{meta['block_windows']}`",
        f"- skipped mixed-source windows: `{meta['skipped_mixed_windows']}`",
        f"- skipped boundary windows: `{meta['skipped_boundary_windows']}`",
        "",
        "The weighted `L1` metric is the row difference in substochastic",
        "return weights after collapsing destinations to `good/bad`.",
        "Terminal/killed events are measured separately in count TV.",
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
        "## By Block Entry",
        "",
        "| entry | source | destination | count | mean abs drift | p95 | p99 | max |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ])
    for row in entry_rows:
        lines.append(
            f"| `{row['class']}` | `{row['source_component']}` | `{row['dst_component']}` | "
            f"{row['count']} | {row['mean']:.8g} | {row['p95']:.8g} | "
            f"{row['p99']:.8g} | {row['max']:.8g} |"
        )

    lines.extend([
        "",
        "## By Adjacent Pair",
        "",
        "| pair | source | count | mean weighted L1 | p95 | p99 | max |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])
    for row in pair_rows:
        lines.append(
            f"| `{row['block_a_start']}->{row['block_b_start']}` | `{row['class']}` | "
            f"{row['count']} | {row['mean']:.8g} | {row['p95']:.8g} | "
            f"{row['p99']:.8g} | {row['max']:.8g} |"
        )

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "Small means here would support a weak averaged block-kernel",
        "approximation target.  Large p95/max values block any uniform",
        "operator-norm claim unless an exceptional-source mechanism is",
        "proved.  These diagnostics do not define an infinite operator and",
        "do not imply a spectral gap.",
    ])
    return "\n".join(lines) + "\n", source_rows, entry_rows, pair_rows, worst


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize good/bad component drift between adjacent high-bit blocks.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--distributions", default=str(DEFAULT_DISTS))
    parser.add_argument("--T", type=int, default=None)
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
    report, source_rows, entry_rows, pair_rows, worst_rows = summarize(args)
    report_path, source_path, entry_path, pair_path, worst_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(source_rows, source_path)
    write_csv(entry_rows, entry_path)
    write_csv(pair_rows, pair_path)
    write_csv(worst_rows, worst_path)
    print("Component block-Cauchy diagnostic written:")
    print(f"  {report_path.name}")
    print(f"  {source_path.name}")
    print(f"  {entry_path.name}")
    print(f"  {pair_path.name}")
    print(f"  {worst_path.name}")


if __name__ == "__main__":
    main()
