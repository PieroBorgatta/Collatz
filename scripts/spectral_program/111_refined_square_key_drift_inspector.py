"""
111_refined_square_key_drift_inspector.py

Inspect which refined source keys contribute most to the square A1 prefix
drift measured by script 110.

The diagnostic compares two prefix kernels on

  (PhaseState, t mod 2^b) -> (PhaseState, next_t mod 2^b)

and ranks source keys by their weighted contribution to the row L1 drift.
This is finite evidence only.  It does not define an infinite operator and
does not close Gate 10.B.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_111{suffix}_refined_square_key_drift"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_top_keys.csv",
        ROOT / f"{stem}_phase_strata.csv",
        ROOT / f"{stem}_residue_strata.csv",
    )


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
        return f"{value:.9g}"
    return str(value)


def parse_refined_key(key: str, bits: int) -> dict[str, int | str]:
    if "|rlo" not in key:
        phase = key
        rlo = -1
    else:
        phase, residue = key.rsplit("|rlo", 1)
        _bits_text, value_text = residue.split("=", 1)
        rlo = int(value_text)
    parts = phase.split("|")
    parsed: dict[str, int | str] = {
        "source_key": key,
        "source_phase": phase,
        "source_v2": parts[0] if len(parts) > 0 else "",
        "source_odd": parts[1] if len(parts) > 1 else "",
        "source_h": parts[2] if len(parts) > 2 else "",
        "rlo": rlo,
    }
    if rlo >= 0:
        parsed["rlo_mod_8"] = rlo % 8
        parsed["rlo_mod_16"] = rlo % 16
        parsed["rlo_mod_32"] = rlo % 32
        parsed["rlo_mod_64"] = rlo % 64
        parsed["rlo_mod_128"] = rlo % 128
        parsed["rlo_mod_bits"] = rlo % (1 << bits)
    return parsed


def destination_delta_summary(left: dict[str, float], right: dict[str, float], keep: int) -> str:
    keys = set(left) | set(right)
    deltas = []
    for dst in keys:
        delta = float(right.get(dst, 0.0)) - float(left.get(dst, 0.0))
        if delta != 0.0:
            deltas.append((abs(delta), delta, dst))
    deltas.sort(reverse=True)
    return " | ".join(f"{dst}:{delta:+.6g}" for _abs_delta, delta, dst in deltas[:keep])


def add_stratum(
    strata: dict[str, dict[str, Any]],
    *,
    name: str,
    row: dict[str, Any],
) -> None:
    item = strata.setdefault(
        name,
        {
            "stratum": name,
            "source_keys": 0,
            "sample_weight": 0.0,
            "weighted_drift": 0.0,
            "max_l1": 0.0,
            "l1_values": [],
        },
    )
    item["source_keys"] += 1
    item["sample_weight"] += float(row["sample_weight"])
    item["weighted_drift"] += float(row["weighted_drift"])
    item["max_l1"] = max(float(item["max_l1"]), float(row["l1_diff"]))
    item["l1_values"].append(float(row["l1_diff"]))


def finalize_strata(
    strata: dict[str, dict[str, Any]],
    *,
    total_weighted_drift: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in strata.values():
        l1_values = item.pop("l1_values")
        sample_weight = float(item["sample_weight"])
        weighted_drift = float(item["weighted_drift"])
        item["mean_l1_unweighted"] = mean(l1_values) if l1_values else 0.0
        item["mean_l1_weighted_by_sample"] = (
            weighted_drift / sample_weight if sample_weight else 0.0
        )
        item["contribution_share"] = (
            weighted_drift / total_weighted_drift if total_weighted_drift else 0.0
        )
        rows.append(item)
    rows.sort(key=lambda row: float(row["weighted_drift"]), reverse=True)
    return rows


def inspect_pair(
    *,
    rows: list[dict[str, Any]],
    bits: int,
    left: int,
    right: int,
    top: int,
    top_dst: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    mod110 = load_module("110_refined_square_probe.py", "refined_square_probe")
    k_left = mod110.kernel_for(rows, j_count=left, bits=bits)
    k_right = mod110.kernel_for(rows, j_count=right, bits=bits)
    all_keys = sorted(set(k_left) | set(k_right))

    detail_rows: list[dict[str, Any]] = []
    total_sample_weight = 0.0
    total_weighted_drift = 0.0
    missing_left = 0
    missing_right = 0

    for key in all_keys:
        left_info = k_left.get(key)
        right_info = k_right.get(key)
        if left_info is None:
            missing_left += 1
        if right_info is None:
            missing_right += 1

        left_row = left_info["row"] if left_info else {}
        right_row = right_info["row"] if right_info else {}
        left_count = int(left_info["sample_count"]) if left_info else 0
        right_count = int(right_info["sample_count"]) if right_info else 0
        sample_weight = 0.5 * float(left_count + right_count)
        l1 = mod110.l1_diff(left_row, right_row)
        weighted_drift = sample_weight * l1
        total_sample_weight += sample_weight
        total_weighted_drift += weighted_drift

        parsed = parse_refined_key(key, bits)
        detail_rows.append(
            {
                **parsed,
                "bits": bits,
                "j_left": left,
                "j_right": right,
                "sample_count_left": left_count,
                "sample_count_right": right_count,
                "sample_weight": sample_weight,
                "l1_diff": l1,
                "weighted_drift": weighted_drift,
                "terminal_fraction_left": (
                    float(left_info["terminal_fraction"]) if left_info else 0.0
                ),
                "terminal_fraction_right": (
                    float(right_info["terminal_fraction"]) if right_info else 0.0
                ),
                "return_mass_left": (
                    float(left_info["weighted_return_mass"]) if left_info else 0.0
                ),
                "return_mass_right": (
                    float(right_info["weighted_return_mass"]) if right_info else 0.0
                ),
                "support_left": len(left_row),
                "support_right": len(right_row),
                "largest_destination_deltas": destination_delta_summary(
                    left_row,
                    right_row,
                    top_dst,
                ),
            }
        )

    for row in detail_rows:
        row["contribution_share"] = (
            float(row["weighted_drift"]) / total_weighted_drift
            if total_weighted_drift
            else 0.0
        )

    detail_rows.sort(key=lambda row: float(row["weighted_drift"]), reverse=True)
    top_rows = detail_rows[:top]

    phase_strata: dict[str, dict[str, Any]] = {}
    residue_strata: dict[str, dict[str, Any]] = {}
    for row in detail_rows:
        add_stratum(phase_strata, name=str(row["source_phase"]), row=row)
        if int(row.get("rlo", -1)) >= 0:
            add_stratum(
                residue_strata,
                name=f"rlo_mod_32={row['rlo_mod_32']}",
                row=row,
            )

    summary = {
        "bits": bits,
        "j_left": left,
        "j_right": right,
        "source_keys_left": len(k_left),
        "source_keys_right": len(k_right),
        "source_keys_union": len(all_keys),
        "missing_left_keys": missing_left,
        "missing_right_keys": missing_right,
        "total_sample_weight": total_sample_weight,
        "total_weighted_drift": total_weighted_drift,
        "weighted_l1_mean": (
            total_weighted_drift / total_sample_weight if total_sample_weight else 0.0
        ),
        "top_10_contribution_share": sum(
            float(row["contribution_share"]) for row in detail_rows[:10]
        ),
        "top_25_contribution_share": sum(
            float(row["contribution_share"]) for row in detail_rows[:25]
        ),
        "top_100_contribution_share": sum(
            float(row["contribution_share"]) for row in detail_rows[:100]
        ),
    }
    return (
        top_rows,
        finalize_strata(phase_strata, total_weighted_drift=total_weighted_drift),
        finalize_strata(residue_strata, total_weighted_drift=total_weighted_drift),
        summary,
    )


def write_report(
    *,
    report_path: Path,
    top_path: Path,
    phase_path: Path,
    residue_path: Path,
    args: argparse.Namespace,
    traced_rows: int,
    terminal_rows: int,
    summary: dict[str, Any],
    top_rows: list[dict[str, Any]],
    phase_rows: list[dict[str, Any]],
    residue_rows: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# Refined Square Key Drift Inspector")
    lines.append("")
    lines.append("Status: finite diagnostic only.  This does not close Gate 10.B.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- T: `{args.T}`")
    lines.append(f"- j-counts: `{args.j_counts}`")
    lines.append(f"- bits: `{args.bits}`")
    lines.append(f"- traced rows: `{traced_rows}`")
    lines.append(f"- terminal rows: `{terminal_rows}`")
    lines.append(f"- top keys CSV: `{top_path.name}`")
    lines.append(f"- phase strata CSV: `{phase_path.name}`")
    lines.append(f"- residue strata CSV: `{residue_path.name}`")
    lines.append("")
    lines.append("## Global Drift")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    for key, value in summary.items():
        lines.append(f"| `{key}` | `{format_float(value)}` |")
    lines.append("")
    lines.append("## Top Source Keys")
    lines.append("")
    lines.append(
        "| rank | source key | L1 drift | contribution | samples left/right | "
        "return mass left/right | largest destination deltas |"
    )
    lines.append("|---:|---|---:|---:|---:|---:|---|")
    for rank, row in enumerate(top_rows[: min(args.report_top, len(top_rows))], start=1):
        lines.append(
            f"| {rank} | `{row['source_key']}` | "
            f"{format_float(row['l1_diff'])} | "
            f"{format_float(row['contribution_share'])} | "
            f"{row['sample_count_left']}/{row['sample_count_right']} | "
            f"{format_float(row['return_mass_left'])}/"
            f"{format_float(row['return_mass_right'])} | "
            f"`{row['largest_destination_deltas']}` |"
        )
    lines.append("")
    lines.append("## Dominant Phase Strata")
    lines.append("")
    lines.append("| rank | source phase | contribution | source keys | weighted mean L1 | max L1 |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(phase_rows[:10], start=1):
        lines.append(
            f"| {rank} | `{row['stratum']}` | "
            f"{format_float(row['contribution_share'])} | "
            f"{row['source_keys']} | "
            f"{format_float(row['mean_l1_weighted_by_sample'])} | "
            f"{format_float(row['max_l1'])} |"
        )
    lines.append("")
    lines.append("## Dominant Residue Strata")
    lines.append("")
    lines.append("| rank | residue stratum | contribution | source keys | weighted mean L1 | max L1 |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(residue_rows[:10], start=1):
        lines.append(
            f"| {rank} | `{row['stratum']}` | "
            f"{format_float(row['contribution_share'])} | "
            f"{row['source_keys']} | "
            f"{format_float(row['mean_l1_weighted_by_sample'])} | "
            f"{format_float(row['max_l1'])} |"
        )
    lines.append("")
    lines.append("## Reading Rule")
    lines.append("")
    lines.append("- High top-key concentration means a few refined classes drive A1 drift.")
    lines.append("- Low concentration means the obstruction is diffuse and A1 is less promising.")
    lines.append("- Phase strata identify structural source states worth isolating in a future norm.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, default=14)
    parser.add_argument("--j-counts", default="32,64")
    parser.add_argument("--bits", type=int, default=10)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=14)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--top", type=int, default=100)
    parser.add_argument("--top-dst", type=int, default=5)
    parser.add_argument("--report-top", type=int, default=25)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    j_counts = parse_csv_ints(args.j_counts)
    if len(j_counts) != 2:
        raise SystemExit("this inspector expects exactly two j-counts, e.g. 32,64")
    if args.bits < 0:
        raise SystemExit("--bits must be nonnegative")

    mod110 = load_module("110_refined_square_probe.py", "refined_square_probe")
    rows = mod110.trace_rows(args)
    terminal_rows = sum(1 for row in rows if row["terminal"])
    top_rows, phase_rows, residue_rows, summary = inspect_pair(
        rows=rows,
        bits=args.bits,
        left=j_counts[0],
        right=j_counts[1],
        top=args.top,
        top_dst=args.top_dst,
    )

    report_path, top_path, phase_path, residue_path = output_paths(args.output_tag)
    write_csv(top_rows, top_path)
    write_csv(phase_rows, phase_path)
    write_csv(residue_rows, residue_path)
    write_report(
        report_path=report_path,
        top_path=top_path,
        phase_path=phase_path,
        residue_path=residue_path,
        args=args,
        traced_rows=len(rows),
        terminal_rows=terminal_rows,
        summary=summary,
        top_rows=top_rows,
        phase_rows=phase_rows,
        residue_rows=residue_rows,
    )
    print(f"wrote {report_path}")
    print(f"wrote {top_path}")
    print(f"wrote {phase_path}")
    print(f"wrote {residue_path}")


if __name__ == "__main__":
    main()
