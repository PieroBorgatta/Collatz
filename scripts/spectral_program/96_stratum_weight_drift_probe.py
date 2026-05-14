"""
96_stratum_weight_drift_probe.py

Probe simple source/destination stratum weights for a finite drift
ratio.  This is a finite diagnostic for the source-stratum drift ansatz,
not a spectral-radius computation and not a proof of a drift lemma.

For each source cylinder (r,h), the script estimates

    R_W(r,h) =
      (1 / sample_count) sum_return 2^{-delta} W(dst) / W(src).

Terminal/killed samples contribute zero.  A useful infinite drift
program would eventually need a uniform or tail-controlled version of
this ratio for a principled weight W.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_96_stratum_weight_drift_report.md"
OUT_GRID = ROOT / "collatz_96_stratum_weight_drift_grid.csv"
OUT_WORST = ROOT / "collatz_96_stratum_weight_drift_worst.csv"


State = tuple[int, int, int]


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_GRID, OUT_WORST
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_96_{safe}_stratum_weight_drift"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_grid.csv",
        ROOT / f"{stem}_worst.csv",
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
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_float_list(text: str) -> list[float]:
    return [float(x.strip()) for x in text.split(",") if x.strip()]


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


def fmt_state(state: State | None) -> str:
    if state is None:
        return "terminal"
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def state_weight(
    state: State,
    odd3_coeff: float,
    v2eq2_coeff: float,
    v2_coeff: float,
    v2eq2_odd3_coeff: float,
    v2_cap: int,
) -> float:
    v2, odd, _h = state
    exponent = 0.0
    exponent += odd3_coeff if odd == 3 else 0.0
    exponent += v2eq2_coeff if v2 == 2 else 0.0
    exponent += v2eq2_odd3_coeff if v2 == 2 and odd == 3 else 0.0
    exponent += v2_coeff * min(v2, v2_cap)
    return math.exp(exponent)


def setup_tail_module():
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    return tail_mod, tail_mod.setup()


def trace_cells(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[tuple[int, int], State]]:
    tail_mod, ctx = setup_tail_module()
    op, shadowing, records, target, target_key, residue, modulus = ctx
    h_mod = 1 << args.hit_bits
    cells: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    sources: dict[tuple[int, int], State] = {}
    total = (1 << args.T) * h_mod * args.j_count
    seen = 0
    progress_step = max(1, total // 20)

    for r in range(1 << args.T):
        for h in range(h_mod):
            key = (r, h)
            for j in range(args.j_count):
                t = r + (j << args.T)
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
                row.update({"r": r, "h": h, "j": j, "t": t})
                cells[key].append(row)
                sources[key] = row["src"]
                seen += 1
                if args.progress and seen % progress_step == 0:
                    print(f"    traced {seen}/{total} rows")
    flat_cells = []
    for (r, h), rows in cells.items():
        flat_cells.append({"r": r, "h": h, "rows": rows})
    return flat_cells, sources


def evaluate_grid(args: argparse.Namespace, cells: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    odd3_values = parse_float_list(args.odd3_coeffs)
    v2eq2_values = parse_float_list(args.v2eq2_coeffs)
    v2_values = parse_float_list(args.v2_coeffs)
    v2eq2_odd3_values = parse_float_list(args.v2eq2_odd3_coeffs)

    grid_rows: list[dict[str, Any]] = []
    worst_by_best: list[dict[str, Any]] = []
    best_key: tuple[float, float, float, float] | None = None
    best_sort_key: tuple[float, float, float, float] | None = None
    cached_cell_ratios: dict[tuple[float, float, float, float], list[dict[str, Any]]] = {}

    for odd3 in odd3_values:
        for v2eq2 in v2eq2_values:
            for v2c in v2_values:
                for v2eq2_odd3 in v2eq2_odd3_values:
                    ratios = []
                    cell_rows: list[dict[str, Any]] = []
                    for cell in cells:
                        rows = cell["rows"]
                        if not rows:
                            continue
                        src = rows[0]["src"]
                        src_w = state_weight(src, odd3, v2eq2, v2c, v2eq2_odd3, args.v2_cap)
                        total = 0.0
                        return_count = 0
                        return_weight = 0.0
                        for row in rows:
                            if row["terminal"]:
                                continue
                            dst = row["dst"]
                            dst_w = state_weight(dst, odd3, v2eq2, v2c, v2eq2_odd3, args.v2_cap)
                            contribution = row["weight"] * dst_w / src_w
                            total += contribution
                            return_weight += row["weight"]
                            return_count += 1
                        ratio = total / len(rows)
                        ratios.append(ratio)
                        cell_rows.append({
                            "T": args.T,
                            "r": cell["r"],
                            "h": cell["h"],
                            "sample_count": len(rows),
                            "source_phase": fmt_state(src),
                            "return_count": return_count,
                            "return_fraction": return_count / len(rows) if rows else 0.0,
                            "unweighted_return_weight": return_weight / len(rows) if rows else 0.0,
                            "drift_ratio": ratio,
                        })

                    summary = {
                        "T": args.T,
                        "j_count": args.j_count,
                        "odd3_coeff": odd3,
                        "v2eq2_coeff": v2eq2,
                        "v2_coeff": v2c,
                        "v2eq2_odd3_coeff": v2eq2_odd3,
                        "cell_count": len(ratios),
                        "mean_ratio": mean(ratios) if ratios else 0.0,
                        "p50_ratio": quantile(ratios, 0.50),
                        "p90_ratio": quantile(ratios, 0.90),
                        "p95_ratio": quantile(ratios, 0.95),
                        "p99_ratio": quantile(ratios, 0.99),
                        "max_ratio": max(ratios) if ratios else 0.0,
                        "fraction_ge_0_75": sum(1 for x in ratios if x >= 0.75) / len(ratios) if ratios else 0.0,
                        "fraction_ge_1": sum(1 for x in ratios if x >= 1.0) / len(ratios) if ratios else 0.0,
                    }
                    grid_rows.append(summary)
                    sort_key = (
                        1 if summary["fraction_ge_1"] > 0 else 0,
                        summary["p95_ratio"],
                        summary["p99_ratio"],
                        summary["max_ratio"],
                    )
                    key = (odd3, v2eq2, v2c, v2eq2_odd3)
                    cached_cell_ratios[key] = cell_rows
                    if best_sort_key is None or sort_key < best_sort_key:
                        best_sort_key = sort_key
                        best_key = key

    if best_key is not None:
        worst_by_best = sorted(
            cached_cell_ratios[best_key],
            key=lambda row: (-row["drift_ratio"], int(row["r"]), int(row["h"])),
        )[:args.limit]
        for row in worst_by_best:
            row["odd3_coeff"] = best_key[0]
            row["v2eq2_coeff"] = best_key[1]
            row["v2_coeff"] = best_key[2]
            row["v2eq2_odd3_coeff"] = best_key[3]
    return grid_rows, worst_by_best


def summarize(args: argparse.Namespace) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    cells, _sources = trace_cells(args)
    grid_rows, worst_rows = evaluate_grid(args, cells)
    ranked = sorted(grid_rows, key=lambda row: (row["p95_ratio"], row["p99_ratio"], row["max_ratio"]))
    safe_ranked = sorted(
        [row for row in grid_rows if row["fraction_ge_1"] == 0.0],
        key=lambda row: (row["p95_ratio"], row["p99_ratio"], row["max_ratio"]),
    )
    identity = [
        row for row in grid_rows
        if row["odd3_coeff"] == 0.0 and row["v2eq2_coeff"] == 0.0 and row["v2_coeff"] == 0.0
        and row["v2eq2_odd3_coeff"] == 0.0
    ]

    lines = [
        "# Stratum Weight Drift Probe",
        "",
        "Status: finite diagnostic, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- T: `{args.T}`",
        f"- j_count: `{args.j_count}`",
        f"- odd bits: `{args.odd_bits}`",
        f"- hit bits: `{args.hit_bits}`",
        f"- v2 cap: `{args.v2_cap}`",
        f"- include t=0: `{args.include_t_zero}`",
        f"- odd3 coeffs: `{args.odd3_coeffs}`",
        f"- v2eq2 coeffs: `{args.v2eq2_coeffs}`",
        f"- v2 coeffs: `{args.v2_coeffs}`",
        f"- v2eq2_odd3 coeffs: `{args.v2eq2_odd3_coeffs}`",
        "",
        "The diagnostic ratio is",
        "",
        "```text",
        "R_W(r,h) = (1/sample_count) sum_return 2^{-delta} W(dst)/W(src).",
        "```",
        "",
        "Terminal samples contribute zero.",
        "",
        "## Identity Weight",
        "",
    ]
    if identity:
        row = identity[0]
        lines.extend([
            f"- mean ratio: `{row['mean_ratio']:.6g}`",
            f"- p95 ratio: `{row['p95_ratio']:.6g}`",
            f"- p99 ratio: `{row['p99_ratio']:.6g}`",
            f"- max ratio: `{row['max_ratio']:.6g}`",
            f"- fraction >= 1: `{row['fraction_ge_1']:.6g}`",
        ])
    else:
        lines.append("- identity weight was not included in the grid.")

    lines.extend([
        "",
        "## Best Grid Points By p95/p99/max",
        "",
        "| odd3 | v2eq2 | v2 coeff | v2eq2&odd3 | mean | p95 | p99 | max | frac >= 1 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in ranked[:args.limit]:
        lines.append(
            f"| {row['odd3_coeff']:.6g} | {row['v2eq2_coeff']:.6g} | "
            f"{row['v2_coeff']:.6g} | {row['v2eq2_odd3_coeff']:.6g} | "
            f"{row['mean_ratio']:.6g} | {row['p95_ratio']:.6g} | "
            f"{row['p99_ratio']:.6g} | {row['max_ratio']:.6g} | "
            f"{row['fraction_ge_1']:.6g} |"
        )

    lines.extend([
        "",
        "## Best Safe Grid Points",
        "",
        "Here safe means `fraction >= 1` is zero on the tested finite window.",
        "",
        "| odd3 | v2eq2 | v2 coeff | v2eq2&odd3 | mean | p95 | p99 | max |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in safe_ranked[:args.limit]:
        lines.append(
            f"| {row['odd3_coeff']:.6g} | {row['v2eq2_coeff']:.6g} | "
            f"{row['v2_coeff']:.6g} | {row['v2eq2_odd3_coeff']:.6g} | "
            f"{row['mean_ratio']:.6g} | {row['p95_ratio']:.6g} | "
            f"{row['p99_ratio']:.6g} | {row['max_ratio']:.6g} |"
        )

    lines.extend([
        "",
        "## Worst Cells For Best Grid Point",
        "",
        "| r | h | source phase | return frac | base return weight | drift ratio |",
        "|---:|---:|---|---:|---:|---:|",
    ])
    for row in worst_rows:
        lines.append(
            f"| {row['r']} | {row['h']} | `{row['source_phase']}` | "
            f"{row['return_fraction']:.6g} | "
            f"{row['unweighted_return_weight']:.6g} | "
            f"{row['drift_ratio']:.6g} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "A useful source-stratum drift weight should reduce high quantiles and",
        "not create new cells with ratio above one.  This finite diagnostic",
        "does not prove a drift inequality; it only rejects or motivates",
        "simple parametric weights before more serious analysis.",
    ])
    return "\n".join(lines) + "\n", grid_rows, worst_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe simple source-stratum drift weights.")
    parser.add_argument("--T", type=int, default=12)
    parser.add_argument("--j-count", type=int, default=16)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--odd3-coeffs", default="-0.5,0,0.5")
    parser.add_argument("--v2eq2-coeffs", default="-0.5,0,0.5")
    parser.add_argument("--v2-coeffs", default="-0.1,0,0.1")
    parser.add_argument("--v2eq2-odd3-coeffs", default="0")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--output-tag", default=None)
    parser.add_argument("--progress", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, grid_rows, worst_rows = summarize(args)
    report_path, grid_path, worst_path = output_paths(args.output_tag)
    report_path.write_text(report, encoding="utf-8")
    write_csv(grid_rows, grid_path)
    write_csv(worst_rows, worst_path)
    print("=" * 118)
    print("  Stratum weight drift probe")
    print("=" * 118)
    print(f"  T={args.T}, j_count={args.j_count}")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {grid_path.name}")
    print(f"    {worst_path.name}")


if __name__ == "__main__":
    main()
