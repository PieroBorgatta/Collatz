"""
120_A0_dependency_depth_probe.py

Measure 2-adic dependency depth for selected A0 low-v2 source phases.

For a fixed phase, trace t in the prefix [0, j_count * 2^T), then group
the resulting signatures by t mod 2^m.  If bounded-depth return signatures
are nearly determined by t mod 2^m at moderate m, the remaining A0W2 proof
target may be attacked as a residue-period/discrepancy lemma.

This is finite evidence only.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_120{suffix}_A0_dependency_depth_probe"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_depth.csv"


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
    modulus = 1 << (v2 + 2)
    start = odd << v2
    if start <= 0:
        start += modulus
    return range(start, n_stop, modulus)


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


def signature(row: dict[str, Any], level: str) -> str:
    if row["terminal"]:
        return "terminal"
    if level == "status":
        return "return"
    if level == "phase":
        return str(row["dst"])
    if level == "delta":
        return delta_bin(row["delta"])
    if level == "phase_delta":
        return f"{row['dst']}|{delta_bin(row['delta'])}"
    if level == "full":
        return f"{row['dst']}|delta={row['delta']}"
    raise ValueError(f"unknown signature level: {level}")


def keep_row(row: dict[str, Any], filter_name: str) -> bool:
    if filter_name == "all":
        return True
    if filter_name == "return":
        return not bool(row["terminal"])
    if filter_name == "medium_return":
        if row["terminal"]:
            return False
        step = int(row["step"] or 0)
        delta = int(row["delta"] or 0)
        return 11 <= step <= 25 and 0 <= delta <= 3
    if filter_name == "step_11_25":
        return (not bool(row["terminal"])) and 11 <= int(row["step"] or 0) <= 25
    raise ValueError(f"unknown filter: {filter_name}")


def parse_csv_text(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def trace_phase(
    *,
    tail_mod,
    ctx,
    args: argparse.Namespace,
    phase: tuple[int, int, int],
) -> list[dict[str, Any]]:
    op, shadowing, records, target, target_key, residue, modulus = ctx
    v2, odd, h = phase
    n_stop = args.j_count * (1 << args.T)
    rows: list[dict[str, Any]] = []
    for t in phase_progression(v2, odd, n_stop):
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
        rows.append(
            {
                "t": t,
                "terminal": int(row["terminal"]),
                "step": row.get("step"),
                "delta": row.get("delta"),
                "dst": fmt_dst(row.get("dst")),
                "kernel_weight": float(row.get("weight") or 0.0),
            }
        )
    return rows


def majority_error_count(signatures: list[str]) -> int:
    if not signatures:
        return 0
    counts = Counter(signatures)
    return len(signatures) - counts.most_common(1)[0][1]


def majority_error_weight(items: list[tuple[str, float]]) -> float:
    if not items:
        return 0.0
    weights: Counter[str] = Counter()
    total = 0.0
    for sig, weight in items:
        weights[sig] += weight
        total += weight
    return total - max(weights.values(), default=0.0)


def analyze_depths(
    *,
    phase: tuple[int, int, int],
    traced: list[dict[str, Any]],
    filters: list[str],
    levels: list[str],
    depths: list[int],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for filter_name in filters:
        filtered = [row for row in traced if keep_row(row, filter_name)]
        for level in levels:
            total_count = len(filtered)
            total_kernel_weight = sum(float(row["kernel_weight"]) for row in filtered)
            for depth in depths:
                modulus = 1 << depth
                groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
                for row in filtered:
                    groups[int(row["t"]) % modulus].append(row)
                mixed_cells = 0
                singleton_cells = 0
                count_error = 0
                weight_error = 0.0
                cell_sizes: list[int] = []
                for group in groups.values():
                    cell_sizes.append(len(group))
                    if len(group) == 1:
                        singleton_cells += 1
                    sigs = [signature(row, level) for row in group]
                    if len(set(sigs)) > 1:
                        mixed_cells += 1
                    count_error += majority_error_count(sigs)
                    weight_error += majority_error_weight(
                        [(signature(row, level), float(row["kernel_weight"])) for row in group]
                    )
                out.append(
                    {
                        "phase": fmt_phase(phase),
                        "filter": filter_name,
                        "signature_level": level,
                        "depth_m": depth,
                        "modulus": modulus,
                        "rows": total_count,
                        "kernel_weight": total_kernel_weight,
                        "cells": len(groups),
                        "mixed_cells": mixed_cells,
                        "mixed_cell_fraction": mixed_cells / len(groups) if groups else 0.0,
                        "singleton_cells": singleton_cells,
                        "singleton_fraction": singleton_cells / len(groups) if groups else 0.0,
                        "mean_cell_size": mean(cell_sizes) if cell_sizes else 0.0,
                        "count_majority_error": count_error / total_count if total_count else 0.0,
                        "kernel_weight_majority_error": (
                            weight_error / total_kernel_weight if total_kernel_weight else 0.0
                        ),
                    }
                )
    return out


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
    rows: list[dict[str, Any]],
    report_path: Path,
    csv_path: Path,
) -> None:
    focus = [
        row for row in rows
        if row["filter"] in ("medium_return", "return")
        and row["signature_level"] in ("phase", "phase_delta")
    ]
    lines: list[str] = []
    lines.append("# A0 Dependency Depth Probe")
    lines.append("")
    lines.append("Status: finite diagnostic for the low-v2 residue-period route.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- T: `{args.T}`")
    lines.append(f"- j_count: `{args.j_count}`")
    lines.append(f"- phases: `{args.phases}`")
    lines.append(f"- depths: `{args.depths}`")
    lines.append(f"- output CSV: `{csv_path.name}`")
    lines.append("")
    lines.append("## Focus Rows")
    lines.append("")
    lines.append("| phase | filter | level | m | rows | cells | singleton | count error | weight error |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|")
    for row in focus:
        lines.append(
            f"| `{row['phase']}` | `{row['filter']}` | `{row['signature_level']}` | "
            f"{row['depth_m']} | {row['rows']} | {row['cells']} | "
            f"{format_float(row['singleton_fraction'])} | "
            f"{format_float(row['count_majority_error'])} | "
            f"{format_float(row['kernel_weight_majority_error'])} |"
        )
    lines.append("")
    lines.append("## Reading Rule")
    lines.append("")
    lines.append("A useful proof lemma would show majority error falling with `m` before")
    lines.append("the cells become mostly singletons.  If error only disappears when")
    lines.append("singleton fraction is high, the finite data are over-resolving rather")
    lines.append("than revealing a stable residue-period mechanism.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_depths(text: str) -> list[int]:
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, default=14)
    parser.add_argument("--j-count", type=int, default=128)
    parser.add_argument("--phases", default="0|3|0,7|3|0")
    parser.add_argument("--depths", default="8,10,12,14,16,18,20")
    parser.add_argument("--filters", default="return,medium_return")
    parser.add_argument("--signature-levels", default="phase,phase_delta")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=14)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--output-tag", default="T14_j128_sample")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    phases = parse_phases(args.phases)
    depths = parse_depths(args.depths)
    filters = parse_csv_text(args.filters)
    levels = parse_csv_text(args.signature_levels)
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()
    rows: list[dict[str, Any]] = []
    for phase in phases:
        traced = trace_phase(tail_mod=tail_mod, ctx=ctx, args=args, phase=phase)
        rows.extend(
            analyze_depths(
                phase=phase,
                traced=traced,
                filters=filters,
                levels=levels,
                depths=depths,
            )
        )
    report_path, csv_path = output_paths(args.output_tag)
    write_csv(rows, csv_path)
    write_report(args=args, rows=rows, report_path=report_path, csv_path=csv_path)
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
