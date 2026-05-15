#!/usr/bin/env python3
"""
Finite low-mode projection test for the phase martingale obstruction.

For each 2-adic child-cylinder pair, compare the full destination-phase
TV with TV after projecting destination phase to low coordinates:
status, destination v2, odd part, hit coordinate, and pairs of these.

This tests the possible repair:

    U = finite/low-mode part + residual,

where Lasota-Yorke would be attempted only on the residual.  The output
is finite diagnostic evidence only.  It does not prove an infinite
operator, Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap, or
Collatz.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_115_phase_low_mode_projection_report.md"
OUT_CSV = ROOT / "collatz_115_phase_low_mode_projection.csv"

MODES = (
    "status",
    "dst_v2",
    "dst_odd",
    "dst_h",
    "dst_v2_odd",
    "dst_v2_h",
    "dst_odd_h",
    "phase",
)


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ints(text: str) -> list[int]:
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_CSV
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_115_{safe}_phase_low_mode_projection"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}.csv"


def projected_signature(row: dict[str, Any], mode: str):
    if row["terminal"]:
        return ("terminal",)
    v2, odd, h = row["dst"]
    if mode == "status":
        return ("return",)
    if mode == "dst_v2":
        return ("return", v2)
    if mode == "dst_odd":
        return ("return", odd)
    if mode == "dst_h":
        return ("return", h)
    if mode == "dst_v2_odd":
        return ("return", v2, odd)
    if mode == "dst_v2_h":
        return ("return", v2, h)
    if mode == "dst_odd_h":
        return ("return", odd, h)
    if mode == "phase":
        return ("return", v2, odd, h)
    raise ValueError(f"unknown mode: {mode}")


def distribution(rows: Iterable[dict[str, Any]], mode: str) -> Counter:
    out = Counter()
    for row in rows:
        out[projected_signature(row, mode)] += 1
    return out


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
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
    }


def analyze_T(z2, tail_mod, ctx, args: argparse.Namespace, T: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    h_mod = 1 << args.hit_bits
    max_j = 1 << (args.max_depth + 1 + args.tail_bits)
    total_groups = (1 << T) * h_mod
    progress_step = max(1, total_groups // 20)

    tv_values: dict[tuple[int, str], list[float]] = defaultdict(list)
    residual_values: dict[tuple[int, str], list[float]] = defaultdict(list)
    samples_by_depth: Counter[int] = Counter()

    seen = 0
    for r in range(1 << T):
        for h in range(h_mod):
            rows = z2.trace_rows_for_group(
                tail_mod=tail_mod,
                ctx=ctx,
                args=args,
                T=T,
                r=r,
                h=h,
                max_j=max_j,
            )
            for depth in range(args.max_depth + 1):
                for q in range(1 << depth):
                    rows0 = z2.child_rows(rows, depth, q, 0)
                    rows1 = z2.child_rows(rows, depth, q, 1)
                    if not rows0 or not rows1:
                        continue
                    phase_tv = z2.total_variation(
                        distribution(rows0, "phase"),
                        distribution(rows1, "phase"),
                    )
                    samples_by_depth[depth] += 1
                    for mode in MODES:
                        mode_tv = z2.total_variation(
                            distribution(rows0, mode),
                            distribution(rows1, mode),
                        )
                        tv_values[(depth, mode)].append(mode_tv)
                        residual_values[(depth, mode)].append(max(0.0, phase_tv - mode_tv))
            seen += 1
            if args.progress and seen % progress_step == 0:
                print(f"    T={T}: processed {seen}/{total_groups} source groups")

    rows_out: list[dict[str, Any]] = []
    for depth in range(args.max_depth + 1):
        phase_mean = summarize(tv_values[(depth, "phase")])["mean"]
        for mode in MODES:
            tv_summary = summarize(tv_values[(depth, mode)])
            residual_summary = summarize(residual_values[(depth, mode)])
            rows_out.append({
                "T": T,
                "depth": depth,
                "mode": mode,
                "mode_mean_tv": tv_summary["mean"],
                "mode_p95_tv": tv_summary["p95"],
                "mode_p99_tv": tv_summary["p99"],
                "mode_max_tv": tv_summary["max"],
                "phase_mean_tv": phase_mean,
                "residual_mean": residual_summary["mean"],
                "residual_p95": residual_summary["p95"],
                "residual_p99": residual_summary["p99"],
                "residual_max": residual_summary["max"],
                "mean_capture_fraction": (
                    tv_summary["mean"] / phase_mean if phase_mean else 0.0
                ),
                "samples": samples_by_depth[depth],
            })
    meta = {
        "T": T,
        "max_j": max_j,
        "source_groups": total_groups,
        "samples": sum(samples_by_depth.values()),
    }
    return rows_out, meta


def build_report(args: argparse.Namespace, meta_rows: list[dict[str, Any]], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Phase Low-Mode Projection Test",
        "",
        "Status: finite diagnostic output only.  This report tests whether",
        "phase martingale variation is mostly captured by low-dimensional",
        "destination coordinates.  It does not prove Lasota-Yorke, Hennion,",
        "Keller-Liverani, a spectral gap, or Collatz.",
        "",
        "## Inputs",
        "",
        f"- T values: `{args.T}`",
        f"- max depth: `{args.max_depth}`",
        f"- tail bits: `{args.tail_bits}`",
        f"- odd bits: `{args.odd_bits}`",
        f"- hit bits: `{args.hit_bits}`",
        f"- v2 cap: `{args.v2_cap}`",
        "",
        "## Trace Meta",
        "",
        "| T | max j | source groups | child-pair samples |",
        "|---:|---:|---:|---:|",
    ]
    for meta in meta_rows:
        lines.append(
            f"| {meta['T']} | {meta['max_j']} | {meta['source_groups']} | {meta['samples']} |"
        )

    lines.extend([
        "",
        "## Low-Mode Capture",
        "",
        "| depth | mode | mode mean TV | phase mean TV | residual mean | residual p95 | capture |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ])
    mode_order = {mode: i for i, mode in enumerate(MODES)}
    for row in sorted(rows, key=lambda r: (int(r["depth"]), -float(r["mean_capture_fraction"]), mode_order[r["mode"]])):
        lines.append(
            f"| {row['depth']} | `{row['mode']}` | "
            f"{row['mode_mean_tv']:.6g} | {row['phase_mean_tv']:.6g} | "
            f"{row['residual_mean']:.6g} | {row['residual_p95']:.6g} | "
            f"{row['mean_capture_fraction']:.6g} |"
        )

    proper_modes = {"status", "dst_v2", "dst_odd", "dst_h", "dst_v2_h", "dst_odd_h"}
    best_by_depth: dict[int, dict[str, Any]] = {}
    for row in rows:
        if row["mode"] not in proper_modes:
            continue
        depth = int(row["depth"])
        old = best_by_depth.get(depth)
        if old is None or row["mean_capture_fraction"] > old["mean_capture_fraction"]:
            best_by_depth[depth] = row

    lines.extend([
        "",
        "## Best Proper Low Mode",
        "",
        "The table excludes `phase` and `dst_v2_odd`, since `dst_v2_odd`",
        "coincides with the full phase variation on the tested windows.",
        "",
        "| depth | best mode | capture | residual mean | residual p95 |",
        "|---:|---|---:|---:|---:|",
    ])
    for depth in sorted(best_by_depth):
        row = best_by_depth[depth]
        lines.append(
            f"| {depth} | `{row['mode']}` | "
            f"{row['mean_capture_fraction']:.6g} | "
            f"{row['residual_mean']:.6g} | {row['residual_p95']:.6g} |"
        )

    lines.extend([
        "",
        "## Reading",
        "",
        "A successful finite/low-mode repair would require some low mode to",
        "capture most phase variation and leave a small residual.  If the",
        "best low modes still leave residuals comparable to the original",
        "phase TV, then a finite-rank projection does not repair LY for the",
        "current phase quotient.",
        "",
        "On the current tested windows, the best proper mode is usually",
        "`dst_v2` or the equivalent `dst_v2_h`.  This is a plausible repair",
        "signal only if the residual after removing the `dst_v2` marginal",
        "continues to decay under deeper 2-adic refinement.  The diagnostic",
        "is not a projection theorem: a proof would still need a canonical",
        "projection/lift and an operator-norm estimate for the residual.",
        "",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", default="15")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--tail-bits", type=int, default=3)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output-tag", default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--csv-output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    z2 = load_module("100_z2_cylinder_oscillation.py", "z2_cylinder")
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()

    all_rows: list[dict[str, Any]] = []
    meta_rows: list[dict[str, Any]] = []
    print("=" * 118)
    print("  Phase low-mode projection test")
    print("=" * 118)
    print(f"  T={args.T}, max_depth={args.max_depth}, tail_bits={args.tail_bits}")

    for T in parse_csv_ints(args.T):
        rows, meta = analyze_T(z2, tail_mod, ctx, args, T)
        all_rows.extend(rows)
        meta_rows.append(meta)
        print(
            f"  T={T}: max_j={meta['max_j']}, source groups={meta['source_groups']}, "
            f"samples={meta['samples']}"
        )

    default_report, default_csv = output_paths(args.output_tag)
    report_path = args.output or default_report
    csv_path = args.csv_output or default_csv
    write_csv(all_rows, csv_path)
    report_path.write_text(build_report(args, meta_rows, all_rows), encoding="utf-8")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {csv_path.name}")


if __name__ == "__main__":
    main()
