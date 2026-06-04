"""
112_family_weighted_norm_probe.py

Probe source-family weights for the refined square A1 prefix drift.

Script 111 showed that the T=14, j=32->64, b=10 drift is not caused by a
tiny exceptional list; it is broad but concentrated by source family, mainly
low v2 and odd residue 1/3 mod 4.  This script tests whether simple
family-dependent weights can lower a finite weighted-norm proxy without
creating a large exceptional set.

For kernels K_left and K_right on

  (PhaseState, t mod 2^b) -> (PhaseState, next_t mod 2^b),

the script reports two different finite quantities:

  source_weighted_l1:
      average row L1 after reweighting the source measure by V(src).
      This can hide mass, so it is reported with distortion diagnostics.

  operator_weighted_l1:
      average of sum_dst |Delta K(src,dst)| V(dst)/V(src).
      This is the more relevant finite proxy for a weighted strong norm.

This is a finite diagnostic only.  It is not a Banach-space theorem and does
not close Gate 10.B.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from importlib import util
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
DOMINANT_FAMILIES = {"0|3", "0|1", "1|3", "1|1"}
TOP_RESIDUE_BANDS = {6, 26}


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_csv_floats(text: str) -> list[float]:
    return [float(x.strip()) for x in text.split(",") if x.strip()]


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_112{suffix}_family_weighted_norm_probe"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_grid.csv",
        ROOT / f"{stem}_worst_rows.csv",
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


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.9g}"
    return str(value)


def parse_key(key: str) -> dict[str, Any]:
    if "|rlo" in key:
        phase, residue = key.rsplit("|rlo", 1)
        _bits_text, value_text = residue.split("=", 1)
        rlo = int(value_text)
    else:
        phase = key
        rlo = -1
    parts = phase.split("|")
    v2 = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else -1
    odd = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else -1
    h = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else -1
    return {
        "key": key,
        "phase": phase,
        "v2": v2,
        "odd": odd,
        "h": h,
        "family": f"{v2}|{odd}",
        "rlo": rlo,
        "rlo_mod_32": rlo % 32 if rlo >= 0 else -1,
    }


def factor_list(name: str, values: list[float]) -> list[dict[str, Any]]:
    return [{"name": f"{name}_x{value:g}", "kind": name, "factor": value} for value in values]


def candidate_specs(factors: list[float]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = [{"name": "identity", "kind": "identity", "factor": 1.0}]
    specs.extend(factor_list("dominant4", factors))
    specs.extend(factor_list("low_v2_le1", factors))
    specs.extend(factor_list("odd1", factors))
    specs.extend(factor_list("odd3", factors))
    specs.extend(factor_list("rlo_mod32_6_26", factors))
    return specs


def family_weight(parsed: dict[str, Any], spec: dict[str, Any]) -> float:
    kind = spec["kind"]
    factor = float(spec["factor"])
    if kind == "identity":
        return 1.0
    if kind == "dominant4":
        return factor if parsed["family"] in DOMINANT_FAMILIES else 1.0
    if kind == "low_v2_le1":
        return factor if int(parsed["v2"]) in (0, 1) else 1.0
    if kind == "odd1":
        return factor if int(parsed["odd"]) == 1 else 1.0
    if kind == "odd3":
        return factor if int(parsed["odd"]) == 3 else 1.0
    if kind == "rlo_mod32_6_26":
        return factor if int(parsed["rlo_mod_32"]) in TOP_RESIDUE_BANDS else 1.0
    raise ValueError(f"unknown candidate kind: {kind}")


def build_diff_rows(
    *,
    rows: list[dict[str, Any]],
    bits: int,
    left: int,
    right: int,
) -> list[dict[str, Any]]:
    mod110 = load_module("110_refined_square_probe.py", "refined_square_probe")
    k_left = mod110.kernel_for(rows, j_count=left, bits=bits)
    k_right = mod110.kernel_for(rows, j_count=right, bits=bits)
    all_keys = sorted(set(k_left) | set(k_right))
    out: list[dict[str, Any]] = []

    for key in all_keys:
        left_info = k_left.get(key)
        right_info = k_right.get(key)
        left_row = left_info["row"] if left_info else {}
        right_row = right_info["row"] if right_info else {}
        left_count = int(left_info["sample_count"]) if left_info else 0
        right_count = int(right_info["sample_count"]) if right_info else 0
        sample_weight = 0.5 * float(left_count + right_count)
        parsed_src = parse_key(key)
        diff_edges: list[tuple[float, dict[str, Any], str]] = []
        l1 = 0.0
        for dst in sorted(set(left_row) | set(right_row)):
            delta = abs(float(right_row.get(dst, 0.0)) - float(left_row.get(dst, 0.0)))
            if delta == 0.0:
                continue
            l1 += delta
            diff_edges.append((delta, parse_key(dst), dst))
        out.append(
            {
                "source_key": key,
                "source_parsed": parsed_src,
                "sample_weight": sample_weight,
                "sample_count_left": left_count,
                "sample_count_right": right_count,
                "identity_l1": l1,
                "diff_edges": diff_edges,
            }
        )
    return out


def score_candidate(diff_rows: list[dict[str, Any]], spec: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source_weighted_num = 0.0
    source_weighted_den = 0.0
    identity_num = 0.0
    identity_den = 0.0
    operator_num = 0.0
    source_weights: list[float] = []
    identity_row_values: list[float] = []
    operator_row_values: list[float] = []
    weighted_operator_pairs: list[tuple[float, float]] = []
    weighted_source_pairs: list[tuple[float, float]] = []
    dominant_weighted_mass = 0.0
    dominant_base_mass = 0.0
    total_base_mass = 0.0
    total_source_weighted_mass = 0.0
    rows_out: list[dict[str, Any]] = []

    for row in diff_rows:
        src = row["source_parsed"]
        base_weight = float(row["sample_weight"])
        source_value = family_weight(src, spec)
        source_weights.append(source_value)
        identity_l1 = float(row["identity_l1"])
        weighted_l1 = 0.0
        for delta, dst, _dst_key in row["diff_edges"]:
            dst_value = family_weight(dst, spec)
            weighted_l1 += float(delta) * dst_value / source_value

        identity_num += base_weight * identity_l1
        identity_den += base_weight
        operator_num += base_weight * weighted_l1
        source_weighted_num += base_weight * source_value * identity_l1
        source_weighted_den += base_weight * source_value
        total_base_mass += base_weight
        total_source_weighted_mass += base_weight * source_value
        if src["family"] in DOMINANT_FAMILIES:
            dominant_base_mass += base_weight
            dominant_weighted_mass += base_weight * source_value

        identity_row_values.append(identity_l1)
        operator_row_values.append(weighted_l1)
        weighted_operator_pairs.append((weighted_l1, base_weight))
        weighted_source_pairs.append((identity_l1, base_weight * source_value))
        rows_out.append(
            {
                "candidate": spec["name"],
                "source_key": row["source_key"],
                "source_family": src["family"],
                "source_rlo_mod_32": src["rlo_mod_32"],
                "sample_weight": base_weight,
                "source_weight": source_value,
                "identity_l1": identity_l1,
                "operator_weighted_l1": weighted_l1,
                "operator_minus_identity": weighted_l1 - identity_l1,
                "sample_count_left": row["sample_count_left"],
                "sample_count_right": row["sample_count_right"],
            }
        )

    identity_mean = identity_num / identity_den if identity_den else 0.0
    operator_mean = operator_num / identity_den if identity_den else 0.0
    source_weighted_mean = (
        source_weighted_num / source_weighted_den if source_weighted_den else 0.0
    )
    weight_min = min(source_weights) if source_weights else 0.0
    weight_max = max(source_weights) if source_weights else 0.0
    summary = {
        "candidate": spec["name"],
        "kind": spec["kind"],
        "factor": float(spec["factor"]),
        "source_keys": len(diff_rows),
        "identity_l1_mean": identity_mean,
        "source_weighted_l1_mean": source_weighted_mean,
        "source_weighted_improvement": (
            identity_mean - source_weighted_mean
        ) / identity_mean if identity_mean else 0.0,
        "operator_weighted_l1_mean": operator_mean,
        "operator_weighted_improvement": (
            identity_mean - operator_mean
        ) / identity_mean if identity_mean else 0.0,
        "operator_weighted_p95": weighted_quantile(weighted_operator_pairs, 0.95),
        "operator_weighted_p99": weighted_quantile(weighted_operator_pairs, 0.99),
        "operator_weighted_max": max(operator_row_values) if operator_row_values else 0.0,
        "source_weighted_p95": weighted_quantile(weighted_source_pairs, 0.95),
        "source_weighted_p99": weighted_quantile(weighted_source_pairs, 0.99),
        "identity_p95": weighted_quantile(
            [(value, float(row["sample_weight"])) for value, row in zip(identity_row_values, diff_rows, strict=True)],
            0.95,
        ),
        "identity_max": max(identity_row_values) if identity_row_values else 0.0,
        "fraction_operator_rows_worse": (
            sum(
                1
                for row in rows_out
                if float(row["operator_weighted_l1"]) > float(row["identity_l1"])
            )
            / len(rows_out)
            if rows_out
            else 0.0
        ),
        "fraction_operator_rows_ge_identity_max": (
            sum(
                1
                for row in rows_out
                if float(row["operator_weighted_l1"]) >= max(identity_row_values)
            )
            / len(rows_out)
            if rows_out and identity_row_values
            else 0.0
        ),
        "source_weight_min": weight_min,
        "source_weight_max": weight_max,
        "source_weight_distortion": weight_max / weight_min if weight_min else math.inf,
        "source_weighted_mass_ratio": (
            total_source_weighted_mass / total_base_mass if total_base_mass else 0.0
        ),
        "dominant_base_mass_share": dominant_base_mass / total_base_mass if total_base_mass else 0.0,
        "dominant_source_weighted_mass_share": (
            dominant_weighted_mass / total_source_weighted_mass
            if total_source_weighted_mass
            else 0.0
        ),
        "operator_row_mean_unweighted": mean(operator_row_values) if operator_row_values else 0.0,
        "operator_row_median_unweighted": median(operator_row_values) if operator_row_values else 0.0,
        "operator_row_p95_unweighted": quantile(operator_row_values, 0.95),
    }
    rows_out.sort(
        key=lambda item: (
            -float(item["operator_weighted_l1"]),
            -float(item["operator_minus_identity"]),
            str(item["source_key"]),
        )
    )
    return summary, rows_out


def write_report(
    *,
    report_path: Path,
    grid_path: Path,
    worst_path: Path,
    args: argparse.Namespace,
    traced_rows: int,
    terminal_rows: int,
    grid_rows: list[dict[str, Any]],
) -> None:
    identity = next(row for row in grid_rows if row["candidate"] == "identity")
    by_operator = sorted(grid_rows, key=lambda row: float(row["operator_weighted_l1_mean"]))
    by_source = sorted(grid_rows, key=lambda row: float(row["source_weighted_l1_mean"]))
    safe_operator = [
        row for row in by_operator
        if float(row["source_weight_distortion"]) <= args.max_report_distortion
        and float(row["operator_weighted_max"]) <= args.max_report_multiplier * float(identity["identity_max"])
    ]

    lines: list[str] = []
    lines.append("# Family Weighted Norm Probe")
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
    lines.append(f"- candidate factors: `{args.factors}`")
    lines.append(f"- grid CSV: `{grid_path.name}`")
    lines.append(f"- worst rows CSV: `{worst_path.name}`")
    lines.append("")
    lines.append("## Identity Baseline")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    for key in (
        "identity_l1_mean",
        "identity_p95",
        "identity_max",
        "dominant_base_mass_share",
    ):
        lines.append(f"| `{key}` | `{format_float(identity[key])}` |")
    lines.append("")
    lines.append("## Best Operator-Weighted Candidates")
    lines.append("")
    lines.append(
        "| rank | candidate | operator mean | improvement | p95 | max | "
        "rows worse | distortion | dominant weighted share |"
    )
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|")
    for rank, row in enumerate(by_operator[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['candidate']}` | "
            f"{format_float(row['operator_weighted_l1_mean'])} | "
            f"{format_float(row['operator_weighted_improvement'])} | "
            f"{format_float(row['operator_weighted_p95'])} | "
            f"{format_float(row['operator_weighted_max'])} | "
            f"{format_float(row['fraction_operator_rows_worse'])} | "
            f"{format_float(row['source_weight_distortion'])} | "
            f"{format_float(row['dominant_source_weighted_mass_share'])} |"
        )
    lines.append("")
    lines.append("## Best Source-Measure Candidates")
    lines.append("")
    lines.append(
        "| rank | candidate | source-weighted mean | improvement | p95 | "
        "distortion | dominant weighted share |"
    )
    lines.append("|---:|---|---:|---:|---:|---:|---:|")
    for rank, row in enumerate(by_source[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['candidate']}` | "
            f"{format_float(row['source_weighted_l1_mean'])} | "
            f"{format_float(row['source_weighted_improvement'])} | "
            f"{format_float(row['source_weighted_p95'])} | "
            f"{format_float(row['source_weight_distortion'])} | "
            f"{format_float(row['dominant_source_weighted_mass_share'])} |"
        )
    lines.append("")
    lines.append("## Safe-Window Operator Candidates")
    lines.append("")
    lines.append(
        f"Filter: distortion <= `{args.max_report_distortion}` and "
        f"operator max <= `{args.max_report_multiplier}` times identity max."
    )
    lines.append("")
    lines.append("| rank | candidate | operator mean | improvement | p95 | max |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(safe_operator[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['candidate']}` | "
            f"{format_float(row['operator_weighted_l1_mean'])} | "
            f"{format_float(row['operator_weighted_improvement'])} | "
            f"{format_float(row['operator_weighted_p95'])} | "
            f"{format_float(row['operator_weighted_max'])} |"
        )
    lines.append("")
    lines.append("## Interpretation Guardrails")
    lines.append("")
    lines.append("- Source-weighted improvement alone can hide the bad source families.")
    lines.append("- Operator-weighted improvement is more relevant, because it uses `V(dst)/V(src)`.")
    lines.append("- A useful candidate should improve the operator mean without a large max or distortion penalty.")
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
    parser.add_argument("--factors", default="0.25,0.5,0.75,1.25,1.5,2,4")
    parser.add_argument("--worst-limit", type=int, default=100)
    parser.add_argument("--report-top", type=int, default=10)
    parser.add_argument("--max-report-distortion", type=float, default=4.0)
    parser.add_argument("--max-report-multiplier", type=float, default=1.25)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    j_counts = parse_csv_ints(args.j_counts)
    if len(j_counts) != 2:
        raise SystemExit("this probe expects exactly two j-counts, e.g. 32,64")

    factors = parse_csv_floats(args.factors)
    mod110 = load_module("110_refined_square_probe.py", "refined_square_probe")
    rows = mod110.trace_rows(args)
    terminal_rows = sum(1 for row in rows if row["terminal"])
    diff_rows = build_diff_rows(rows=rows, bits=args.bits, left=j_counts[0], right=j_counts[1])

    grid_rows: list[dict[str, Any]] = []
    worst_rows: list[dict[str, Any]] = []
    best_operator: dict[str, Any] | None = None
    best_rows: list[dict[str, Any]] = []
    for spec in candidate_specs(factors):
        summary, rows_out = score_candidate(diff_rows, spec)
        grid_rows.append(summary)
        if best_operator is None or float(summary["operator_weighted_l1_mean"]) < float(
            best_operator["operator_weighted_l1_mean"]
        ):
            best_operator = summary
            best_rows = rows_out

    if best_operator is not None:
        worst_rows = best_rows[: args.worst_limit]

    report_path, grid_path, worst_path = output_paths(args.output_tag)
    write_csv(grid_rows, grid_path)
    write_csv(worst_rows, worst_path)
    write_report(
        report_path=report_path,
        grid_path=grid_path,
        worst_path=worst_path,
        args=args,
        traced_rows=len(rows),
        terminal_rows=terminal_rows,
        grid_rows=grid_rows,
    )
    print(f"wrote {report_path}")
    print(f"wrote {grid_path}")
    print(f"wrote {worst_path}")


if __name__ == "__main__":
    main()
