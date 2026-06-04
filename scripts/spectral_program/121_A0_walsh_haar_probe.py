"""
121_A0_walsh_haar_probe.py

Walsh-Haar diagnostic for the remaining A0 low-v2 problem.

For a fixed source phase, trace the vector-valued return signal over the
ordered source samples in a dyadic prefix.  The value at each sample is the
weighted destination phase vector, with terminal/nonselected rows equal to
zero.  The script then computes dyadic Haar jumps:

  || mean(left child) - mean(right child) ||_1

at every scale.

The top-scale jump is the adjacent half-block discrepancy measured by
script 119; half of it is the script-111 prefix drift.  The full scale
profile tests whether low-v2 decay should be attacked by Walsh-Haar /
2-adic discrepancy estimates rather than finite local constancy.

This is finite evidence only.
"""

from __future__ import annotations

import argparse
import csv
import math
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_121{suffix}_A0_walsh_haar_probe"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_scale.csv"


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


def parse_csv_text(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


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


def signal_label(row: dict[str, Any], level: str) -> str:
    if row["terminal"]:
        return "terminal"
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


def quantile(values: np.ndarray, q: float) -> float:
    if values.size == 0:
        return 0.0
    return float(np.quantile(values, q))


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
                "terminal": int(row["terminal"]),
                "step": row.get("step"),
                "delta": row.get("delta"),
                "dst": fmt_dst(row.get("dst")),
                "kernel_weight": float(row.get("weight") or 0.0),
            }
        )
    return rows


def build_signal(traced: list[dict[str, Any]], *, filter_name: str, level: str) -> tuple[np.ndarray, list[str]]:
    labels = sorted(
        {
            signal_label(row, level)
            for row in traced
            if keep_row(row, filter_name) and not bool(row["terminal"])
        }
    )
    label_index = {label: idx for idx, label in enumerate(labels)}
    values = np.zeros((len(traced), max(1, len(labels))), dtype=np.float64)
    if not labels:
        return values, labels
    for idx, row in enumerate(traced):
        if not keep_row(row, filter_name) or row["terminal"]:
            continue
        values[idx, label_index[signal_label(row, level)]] += float(row["kernel_weight"])
    return values, labels


def haar_spectrum(values: np.ndarray) -> list[dict[str, Any]]:
    n = values.shape[0]
    if n == 0 or n & (n - 1):
        raise ValueError(f"signal length must be a power of two, got {n}")
    total_l2_energy = 0.0
    spectra: list[dict[str, Any]] = []
    current = values
    child_size = 1
    scale_index = 0
    while current.shape[0] >= 2:
        left = current[0::2]
        right = current[1::2]
        diff = left - right
        node_l1 = np.abs(diff).sum(axis=1) / child_size
        node_l2 = np.square(diff).sum(axis=1) / (2.0 * child_size)
        scale_l2_energy = float(node_l2.sum())
        total_l2_energy += scale_l2_energy
        spectra.append(
            {
                "scale_index_from_fine": scale_index,
                "child_size": child_size,
                "block_size": 2 * child_size,
                "node_count": int(diff.shape[0]),
                "weighted_l1_variation": float((2.0 * child_size / n) * node_l1.sum()),
                "mean_node_l1": float(node_l1.mean()) if node_l1.size else 0.0,
                "p95_node_l1": quantile(node_l1, 0.95),
                "max_node_l1": float(node_l1.max()) if node_l1.size else 0.0,
                "l2_haar_energy": scale_l2_energy,
                "top_prefix_l1_if_root": 0.5 * float(node_l1[0]) if diff.shape[0] == 1 else 0.0,
                "root_half_l1_if_root": float(node_l1[0]) if diff.shape[0] == 1 else 0.0,
            }
        )
        current = left + right
        child_size *= 2
        scale_index += 1

    for row in spectra:
        row["l2_energy_share"] = (
            float(row["l2_haar_energy"]) / total_l2_energy if total_l2_energy else 0.0
        )
    return spectra


def analyze(
    *,
    phase: tuple[int, int, int],
    traced: list[dict[str, Any]],
    filters: list[str],
    levels: list[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for filter_name in filters:
        for level in levels:
            values, labels = build_signal(traced, filter_name=filter_name, level=level)
            nonzero_rows = int(np.count_nonzero(np.abs(values).sum(axis=1)))
            support = len(labels)
            spectrum = haar_spectrum(values)
            for row in spectrum:
                rows.append(
                    {
                        "phase": fmt_phase(phase),
                        "filter": filter_name,
                        "signature_level": level,
                        "sample_count": values.shape[0],
                        "nonzero_rows": nonzero_rows,
                        "nonzero_fraction": nonzero_rows / values.shape[0] if values.shape[0] else 0.0,
                        "support": support,
                        **row,
                    }
                )
    rows.sort(
        key=lambda row: (
            row["phase"],
            row["filter"],
            row["signature_level"],
            int(row["scale_index_from_fine"]),
        )
    )
    return rows


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
    root_rows = [row for row in rows if int(row["node_count"]) == 1]
    high_energy = sorted(rows, key=lambda row: float(row["l2_energy_share"]), reverse=True)
    coarse_rows = [
        row for row in rows
        if int(row["block_size"]) >= max(2, (int(row["sample_count"]) // 64))
    ]

    lines: list[str] = []
    lines.append("# A0 Walsh-Haar Probe")
    lines.append("")
    lines.append("Status: finite Walsh-Haar diagnostic for A0W2 / TODO 10.M.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- T: `{args.T}`")
    lines.append(f"- j_count: `{args.j_count}`")
    lines.append(f"- phases: `{args.phases}`")
    lines.append(f"- filters: `{args.filters}`")
    lines.append(f"- signature levels: `{args.signature_levels}`")
    lines.append(f"- output CSV: `{csv_path.name}`")
    lines.append("")
    lines.append("## Root Coefficients")
    lines.append("")
    lines.append("| phase | filter | level | samples | support | root half L1 | prefix L1 | L2 energy share |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|")
    for row in root_rows:
        lines.append(
            f"| `{row['phase']}` | `{row['filter']}` | `{row['signature_level']}` | "
            f"{row['sample_count']} | {row['support']} | "
            f"{format_float(row['root_half_l1_if_root'])} | "
            f"{format_float(row['top_prefix_l1_if_root'])} | "
            f"{format_float(row['l2_energy_share'])} |"
        )
    lines.append("")
    lines.append("## Largest L2 Haar Energy Shares")
    lines.append("")
    lines.append("| rank | phase | filter | level | block size | nodes | weighted L1 variation | L2 share |")
    lines.append("|---:|---|---|---|---:|---:|---:|---:|")
    for rank, row in enumerate(high_energy[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['phase']}` | `{row['filter']}` | `{row['signature_level']}` | "
            f"{row['block_size']} | {row['node_count']} | "
            f"{format_float(row['weighted_l1_variation'])} | "
            f"{format_float(row['l2_energy_share'])} |"
        )
    lines.append("")
    lines.append("## Coarse-Scale Tail")
    lines.append("")
    lines.append("| phase | filter | level | block size | nodes | weighted L1 variation | L2 share |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for row in coarse_rows:
        lines.append(
            f"| `{row['phase']}` | `{row['filter']}` | `{row['signature_level']}` | "
            f"{row['block_size']} | {row['node_count']} | "
            f"{format_float(row['weighted_l1_variation'])} | "
            f"{format_float(row['l2_energy_share'])} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The root row is the adjacent half-block discrepancy; half of it is the")
    lines.append("script-111 prefix drift for the same phase/filter/level.  A promising")
    lines.append("Walsh-Haar proof route would show that coarse-scale coefficients decay")
    lines.append("for fixed low-v2 phases, while high-frequency energy remains harmless")
    lines.append("under prefix averaging.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, default=14)
    parser.add_argument("--j-count", type=int, default=128)
    parser.add_argument("--phases", default="0|3|0,7|3|0")
    parser.add_argument("--filters", default="return,medium_return")
    parser.add_argument("--signature-levels", default="phase,phase_delta")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=14)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--report-top", type=int, default=16)
    parser.add_argument("--output-tag", default="T14_j128_sample")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    phases = parse_phases(args.phases)
    filters = parse_csv_text(args.filters)
    levels = parse_csv_text(args.signature_levels)
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()
    rows: list[dict[str, Any]] = []
    for phase in phases:
        traced = trace_phase(tail_mod=tail_mod, ctx=ctx, args=args, phase=phase)
        rows.extend(analyze(phase=phase, traced=traced, filters=filters, levels=levels))
    report_path, csv_path = output_paths(args.output_tag)
    write_csv(rows, csv_path)
    write_report(args=args, rows=rows, report_path=report_path, csv_path=csv_path)
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
