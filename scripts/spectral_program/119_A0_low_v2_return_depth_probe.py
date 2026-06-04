"""
119_A0_low_v2_return_depth_probe.py

Retrace selected A0 low-v2 source phases and decompose their prefix drift
by return depth and bit-growth bins.

The goal is to diagnose the proof mechanism behind:

  D_N(v2 < R) -> 0.

For a source phase p, the script compares the phase-only row kernel for
the prefix [0, L) against [0, R), where:

  L = j_left * 2^T,
  R = j_right * 2^T.

It also computes the adjacent half-block drift [0, L) vs [L, R), because
K_R - K_L is the averaged version of that block discrepancy.

This is a finite diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_119{suffix}_A0_low_v2_return_depth_probe"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_phase_summary.csv",
        ROOT / f"{stem}_bin_summary.csv",
    )


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_phase(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected phase {text!r}; expected v2|odd|h")
    return int(parts[0]), int(parts[1]), int(parts[2])


def parse_phases(text: str) -> list[tuple[int, int, int]]:
    return [parse_phase(item.strip()) for item in text.split(",") if item.strip()]


def fmt_phase(phase: tuple[int, int, int]) -> str:
    return f"{phase[0]}|{phase[1]}|{phase[2]}"


def fmt_dst(dst: tuple[int, int, int] | None) -> str:
    if dst is None:
        return "terminal"
    return f"{dst[0]}|{dst[1]}|{dst[2]}"


def phase_progression(v2: int, odd: int, n_stop: int) -> range:
    if v2 < 0:
        raise ValueError("v2 must be nonnegative")
    modulus = 1 << (v2 + 2)
    start = odd << v2
    if start <= 0:
        start += modulus
    return range(start, n_stop, modulus)


def step_bin(step: int | None) -> str:
    if step is None:
        return "step_none"
    if step <= 10:
        return "step_001_010"
    if step <= 25:
        return "step_011_025"
    if step <= 50:
        return "step_026_050"
    if step <= 100:
        return "step_051_100"
    if step <= 250:
        return "step_101_250"
    if step <= 500:
        return "step_251_500"
    return "step_gt_500"


def delta_bin(delta: int | None) -> str:
    if delta is None:
        return "terminal"
    if delta <= -4:
        return "delta_le_-4"
    if delta <= -1:
        return "delta_-3_-1"
    if delta == 0:
        return "delta_0"
    if delta <= 3:
        return "delta_1_3"
    if delta <= 6:
        return "delta_4_6"
    return "delta_ge_7"


def l1_diff(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    return sum(abs(float(a.get(key, 0.0)) - float(b.get(key, 0.0))) for key in keys)


def row_from_weights(weights: Counter[str], denom: int) -> dict[str, float]:
    if denom <= 0:
        return {}
    return {dst: weight / denom for dst, weight in weights.items()}


def top_deltas(a: dict[str, float], b: dict[str, float], keep: int) -> str:
    rows = []
    for key in set(a) | set(b):
        delta = float(b.get(key, 0.0)) - float(a.get(key, 0.0))
        if delta != 0.0:
            rows.append((abs(delta), delta, key))
    rows.sort(reverse=True)
    return " | ".join(f"{key}:{delta:+.8g}" for _abs_delta, delta, key in rows[:keep])


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


def trace_phase(
    *,
    tail_mod,
    ctx,
    args: argparse.Namespace,
    phase: tuple[int, int, int],
) -> dict[str, Any]:
    op, shadowing, records, target, target_key, residue, modulus = ctx
    v2, odd, h = phase
    n_left = args.j_left * (1 << args.T)
    n_right = args.j_right * (1 << args.T)

    left_weights: Counter[str] = Counter()
    right_weights: Counter[str] = Counter()
    second_weights: Counter[str] = Counter()
    left_bins: dict[str, Counter[str]] = defaultdict(Counter)
    right_bins: dict[str, Counter[str]] = defaultdict(Counter)
    second_bins: dict[str, Counter[str]] = defaultdict(Counter)
    left_count = 0
    right_count = 0
    second_count = 0
    left_terminal = 0
    right_terminal = 0
    second_terminal = 0
    return_steps: list[int] = []
    terminal_steps: list[int] = []
    unresolved = 0

    for t in phase_progression(v2, odd, n_right):
        if t == 0 and not args.include_t_zero:
            continue
        row = tail_mod.trace_row(
            op=op,
            shadowing=shadowing,
            records=records,
            target=target,
            target_key=target_key,
            residue=residue,
            modulus=modulus,
            t=t,
            h=h,
            odd_bits=args.odd_bits,
            hit_bits=args.hit_bits,
            v2_cap=args.v2_cap,
            max_steps=args.max_steps,
        )
        is_left = t < n_left
        is_second = n_left <= t < n_right
        if t < n_right:
            right_count += 1
        if is_left:
            left_count += 1
        if is_second:
            second_count += 1

        unresolved += int(row.get("unresolved", 0) or 0)
        if row["terminal"]:
            terminal_steps.append(int(row.get("step") or 0))
            if t < n_right:
                right_terminal += 1
            if is_left:
                left_terminal += 1
            if is_second:
                second_terminal += 1
            continue

        return_steps.append(int(row.get("step") or 0))
        dst = fmt_dst(row["dst"])
        weight = float(row["weight"])
        bins = (
            f"step:{step_bin(row.get('step'))}",
            f"delta:{delta_bin(row.get('delta'))}",
            f"step_delta:{step_bin(row.get('step'))}|{delta_bin(row.get('delta'))}",
        )
        right_weights[dst] += weight
        if is_left:
            left_weights[dst] += weight
        if is_second:
            second_weights[dst] += weight
        for bin_name in bins:
            right_bins[bin_name][dst] += weight
            if is_left:
                left_bins[bin_name][dst] += weight
            if is_second:
                second_bins[bin_name][dst] += weight

    left_row = row_from_weights(left_weights, left_count)
    right_row = row_from_weights(right_weights, right_count)
    second_row = row_from_weights(second_weights, second_count)
    prefix_l1 = l1_diff(left_row, right_row)
    half_l1 = l1_diff(left_row, second_row)

    bin_rows: list[dict[str, Any]] = []
    for bin_name in sorted(set(left_bins) | set(right_bins) | set(second_bins)):
        left_bin_row = row_from_weights(left_bins.get(bin_name, Counter()), left_count)
        right_bin_row = row_from_weights(right_bins.get(bin_name, Counter()), right_count)
        second_bin_row = row_from_weights(second_bins.get(bin_name, Counter()), second_count)
        bin_rows.append(
            {
                "phase": fmt_phase(phase),
                "bin": bin_name,
                "prefix_l1_piece": l1_diff(left_bin_row, right_bin_row),
                "half_l1_piece": l1_diff(left_bin_row, second_bin_row),
                "left_weight_mass": sum(left_bins.get(bin_name, Counter()).values()) / left_count if left_count else 0.0,
                "right_weight_mass": sum(right_bins.get(bin_name, Counter()).values()) / right_count if right_count else 0.0,
                "second_weight_mass": sum(second_bins.get(bin_name, Counter()).values()) / second_count if second_count else 0.0,
                "top_prefix_deltas": top_deltas(left_bin_row, right_bin_row, args.top_dst),
            }
        )
    bin_rows.sort(key=lambda row: float(row["prefix_l1_piece"]), reverse=True)

    summary = {
        "phase": fmt_phase(phase),
        "T": args.T,
        "j_left": args.j_left,
        "j_right": args.j_right,
        "N_left": n_left,
        "N_right": n_right,
        "left_count": left_count,
        "right_count": right_count,
        "second_count": second_count,
        "prefix_l1": prefix_l1,
        "half_l1": half_l1,
        "prefix_l1_over_half_l1": prefix_l1 / half_l1 if half_l1 else 0.0,
        "left_terminal_fraction": left_terminal / left_count if left_count else 0.0,
        "right_terminal_fraction": right_terminal / right_count if right_count else 0.0,
        "second_terminal_fraction": second_terminal / second_count if second_count else 0.0,
        "left_return_mass": sum(left_weights.values()) / left_count if left_count else 0.0,
        "right_return_mass": sum(right_weights.values()) / right_count if right_count else 0.0,
        "second_return_mass": sum(second_weights.values()) / second_count if second_count else 0.0,
        "return_step_median": median(return_steps) if return_steps else 0.0,
        "return_step_p95": quantile([float(x) for x in return_steps], 0.95),
        "terminal_step_median": median(terminal_steps) if terminal_steps else 0.0,
        "terminal_step_p95": quantile([float(x) for x in terminal_steps], 0.95),
        "unresolved": unresolved,
        "support_left": len(left_row),
        "support_right": len(right_row),
        "support_second": len(second_row),
        "top_prefix_deltas": top_deltas(left_row, right_row, args.top_dst),
        "top_half_deltas": top_deltas(left_row, second_row, args.top_dst),
    }
    return {"summary": summary, "bins": bin_rows}


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


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def write_report(
    *,
    args: argparse.Namespace,
    summaries: list[dict[str, Any]],
    bins: list[dict[str, Any]],
    report_path: Path,
    summary_path: Path,
    bins_path: Path,
) -> None:
    lines: list[str] = []
    lines.append("# A0 Low-v2 Return Depth Probe")
    lines.append("")
    lines.append("Status: finite retrace diagnostic for A0W2 / TODO 10.M.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- T: `{args.T}`")
    lines.append(f"- j_left/j_right: `{args.j_left}/{args.j_right}`")
    lines.append(f"- phases: `{args.phases}`")
    lines.append(f"- summary CSV: `{summary_path.name}`")
    lines.append(f"- bin CSV: `{bins_path.name}`")
    lines.append("")
    lines.append("## Phase Summary")
    lines.append("")
    lines.append("| phase | count L/R | prefix L1 | half L1 | prefix/half | return mass L/R | terminal L/R | return step median/p95 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in summaries:
        lines.append(
            f"| `{row['phase']}` | {row['left_count']}/{row['right_count']} | "
            f"{format_float(row['prefix_l1'])} | "
            f"{format_float(row['half_l1'])} | "
            f"{format_float(row['prefix_l1_over_half_l1'])} | "
            f"{format_float(row['left_return_mass'])}/{format_float(row['right_return_mass'])} | "
            f"{format_float(row['left_terminal_fraction'])}/{format_float(row['right_terminal_fraction'])} | "
            f"{format_float(row['return_step_median'])}/{format_float(row['return_step_p95'])} |"
        )
    lines.append("")
    lines.append("## Top Bin Pieces")
    lines.append("")
    lines.append("| phase | bin | prefix L1 piece | half L1 piece | mass L/R | top deltas |")
    lines.append("|---|---|---:|---:|---:|---|")
    for row in bins[: args.report_bins]:
        lines.append(
            f"| `{row['phase']}` | `{row['bin']}` | "
            f"{format_float(row['prefix_l1_piece'])} | "
            f"{format_float(row['half_l1_piece'])} | "
            f"{format_float(row['left_weight_mass'])}/{format_float(row['right_weight_mass'])} | "
            f"`{row['top_prefix_deltas']}` |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("For equal half-block sizes, `K_right - K_left` should be roughly half")
    lines.append("of the adjacent block discrepancy.  A ratio near `0.5` confirms that")
    lines.append("the observed prefix drift is ordinary block averaging.  The bin rows")
    lines.append("then identify whether the drift is concentrated in return-depth tails,")
    lines.append("bit-growth tails, or broad low-depth movement.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, default=14)
    parser.add_argument("--j-left", type=int, default=64)
    parser.add_argument("--j-right", type=int, default=128)
    parser.add_argument("--phases", default="0|3|0,1|3|0,3|1|0,7|3|0")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=14)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--top-dst", type=int, default=5)
    parser.add_argument("--report-bins", type=int, default=24)
    parser.add_argument("--output-tag", default="T14_j64_128_sample")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.j_left >= args.j_right:
        raise SystemExit("--j-left must be smaller than --j-right")
    phases = parse_phases(args.phases)
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()
    summaries: list[dict[str, Any]] = []
    bin_rows: list[dict[str, Any]] = []
    for phase in phases:
        result = trace_phase(tail_mod=tail_mod, ctx=ctx, args=args, phase=phase)
        summaries.append(result["summary"])
        bin_rows.extend(result["bins"])
    bin_rows.sort(key=lambda row: float(row["prefix_l1_piece"]), reverse=True)

    report_path, summary_path, bins_path = output_paths(args.output_tag)
    write_csv(summaries, summary_path)
    write_csv(bin_rows, bins_path)
    write_report(
        args=args,
        summaries=summaries,
        bins=bin_rows,
        report_path=report_path,
        summary_path=summary_path,
        bins_path=bins_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {bins_path}")


if __name__ == "__main__":
    main()
