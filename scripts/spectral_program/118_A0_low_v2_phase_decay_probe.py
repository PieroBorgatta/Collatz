"""
118_A0_low_v2_phase_decay_probe.py

Probe the remaining A0 proof target after the exact high-v2 source-tail
count:

  for each fixed threshold R, prove D_N(v2 < R) -> 0.

This script reuses script-111 A0 phase-strata CSVs.  It fits per-phase
row-drift laws

  L1_phase(N) ~= c_phase * N^(-alpha_phase)

and reports which low-v2 phases dominate the latest low component.

This is finite evidence only.  Its purpose is to identify the next
proof mechanism or counterexample family for A0W2/10.M.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GLOB = "collatz_111_*_b0_refined_square_key_drift_phase_strata.csv"


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_118{suffix}_A0_low_v2_phase_decay_probe"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_phase_fits.csv",
        ROOT / f"{stem}_latest_phase_rows.csv",
    )


def parse_filename(path: Path) -> tuple[int, int, int] | None:
    match = re.search(r"_T(\d+)_j(\d+)_(\d+)_b0_", path.name)
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def parse_phase(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected phase stratum: {text}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def parse_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def fit_power(points: list[tuple[float, float]]) -> dict[str, float]:
    valid = [(math.log(N), math.log(value)) for N, value in points if N > 0 and value > 0]
    if len(valid) < 2:
        return {"count": float(len(valid)), "alpha": 0.0, "c": 0.0, "r2": 0.0}
    xs = [x for x, _y in valid]
    ys = [y for _x, y in valid]
    x_bar = mean(xs)
    y_bar = mean(ys)
    ss_xx = sum((x - x_bar) ** 2 for x in xs)
    ss_xy = sum((x - x_bar) * (y - y_bar) for x, y in valid)
    slope = ss_xy / ss_xx if ss_xx else 0.0
    intercept = y_bar - slope * x_bar
    preds = [intercept + slope * x for x in xs]
    ss_res = sum((y - pred) ** 2 for y, pred in zip(ys, preds, strict=True))
    ss_tot = sum((y - y_bar) ** 2 for y in ys)
    return {
        "count": float(len(valid)),
        "alpha": -slope,
        "c": math.exp(intercept),
        "r2": 1.0 - ss_res / ss_tot if ss_tot else 1.0,
    }


def read_cases(pattern: str) -> list[dict[str, Any]]:
    raw_cases: list[dict[str, Any]] = []
    for path in sorted(ROOT.glob(pattern)):
        parsed = parse_filename(path)
        if parsed is None:
            continue
        T, j_left, j_right = parsed
        rows: list[dict[str, Any]] = []
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter=";"):
                v2, odd, h = parse_phase(row["stratum"])
                sample_weight = float(row["sample_weight"])
                weighted_drift = float(row["weighted_drift"])
                rows.append(
                    {
                        "stratum": row["stratum"],
                        "v2": v2,
                        "odd": odd,
                        "h": h,
                        "sample_weight": sample_weight,
                        "weighted_drift": weighted_drift,
                        "row_l1": weighted_drift / sample_weight if sample_weight else 0.0,
                        "max_l1": float(row["max_l1"]),
                    }
                )
        total_mass = sum(float(row["sample_weight"]) for row in rows)
        total_drift = sum(float(row["weighted_drift"]) for row in rows)
        raw_cases.append(
            {
                "source_file": path.name,
                "T": T,
                "j_left": j_left,
                "j_right": j_right,
                "N_left": j_left * (1 << T),
                "N_right": j_right * (1 << T),
                "rows": rows,
                "total_mass": total_mass,
                "total_drift": total_drift,
                "total_D": total_drift / total_mass if total_mass else 0.0,
            }
        )

    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for case in raw_cases:
        grouped[(int(case["N_left"]), int(case["N_right"]))].append(case)

    cases: list[dict[str, Any]] = []
    for rows in grouped.values():
        rows.sort(key=lambda item: (int(item["T"]), int(item["j_left"])), reverse=True)
        cases.append(rows[0])
    cases.sort(key=lambda item: (int(item["N_left"]), int(item["N_right"])))
    return cases


def local_alphas(points: list[tuple[float, float]]) -> list[float]:
    out: list[float] = []
    ordered = sorted(points)
    for (n0, y0), (n1, y1) in zip(ordered, ordered[1:], strict=False):
        if n0 <= 0 or n1 <= 0 or y0 <= 0 or y1 <= 0 or n0 == n1:
            continue
        out.append(-((math.log(y1) - math.log(y0)) / (math.log(n1) - math.log(n0))))
    return out


def analyze(cases: list[dict[str, Any]], thresholds: list[int]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_phase: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        for row in case["rows"]:
            by_phase[str(row["stratum"])].append({**row, **{k: case[k] for k in ("T", "j_left", "j_right", "N_left", "N_right", "total_mass", "total_drift", "total_D", "source_file")}})

    latest_case = max(cases, key=lambda item: int(item["N_left"]))
    latest_total_mass = float(latest_case["total_mass"])
    latest_total_drift = float(latest_case["total_drift"])
    latest_rows: list[dict[str, Any]] = []
    for row in latest_case["rows"]:
        latest_rows.append(
            {
                "stratum": row["stratum"],
                "v2": row["v2"],
                "odd": row["odd"],
                "h": row["h"],
                "N_left": latest_case["N_left"],
                "N_right": latest_case["N_right"],
                "sample_weight": row["sample_weight"],
                "mass_share": row["sample_weight"] / latest_total_mass if latest_total_mass else 0.0,
                "row_l1": row["row_l1"],
                "weighted_drift": row["weighted_drift"],
                "contribution_share": row["weighted_drift"] / latest_total_drift if latest_total_drift else 0.0,
            }
        )
    latest_rows.sort(key=lambda row: float(row["weighted_drift"]), reverse=True)

    phase_fits: list[dict[str, Any]] = []
    for stratum, rows in by_phase.items():
        v2, odd, h = parse_phase(stratum)
        row_points = [(float(row["N_left"]), float(row["row_l1"])) for row in rows]
        contribution_points = [
            (float(row["N_left"]), float(row["weighted_drift"]) / float(row["total_mass"]))
            for row in rows
            if float(row["total_mass"]) > 0
        ]
        row_fit = fit_power(row_points)
        contribution_fit = fit_power(contribution_points)
        locals_row = local_alphas(row_points)
        latest = max(rows, key=lambda row: int(row["N_left"]))
        phase_fits.append(
            {
                "stratum": stratum,
                "v2": v2,
                "odd": odd,
                "h": h,
                "points": int(row_fit["count"]),
                "row_l1_alpha": row_fit["alpha"],
                "row_l1_c": row_fit["c"],
                "row_l1_r2": row_fit["r2"],
                "row_l1_local_alpha_median": median(locals_row) if locals_row else 0.0,
                "row_l1_local_alpha_min": min(locals_row) if locals_row else 0.0,
                "row_l1_local_alpha_max": max(locals_row) if locals_row else 0.0,
                "contribution_alpha": contribution_fit["alpha"],
                "contribution_r2": contribution_fit["r2"],
                "latest_N_left": latest["N_left"],
                "latest_sample_weight": latest["sample_weight"],
                "latest_mass_share": float(latest["sample_weight"]) / float(latest["total_mass"]),
                "latest_row_l1": latest["row_l1"],
                "latest_weighted_drift_component": float(latest["weighted_drift"]) / float(latest["total_mass"]),
                "latest_contribution_share": (
                    float(latest["weighted_drift"]) / float(latest["total_drift"])
                    if float(latest["total_drift"])
                    else 0.0
                ),
                "latest_source_file": latest["source_file"],
            }
        )

    phase_fits.sort(key=lambda row: float(row["latest_weighted_drift_component"]), reverse=True)

    # Add threshold summaries as synthetic rows at the end of phase_fits-like output.
    for threshold in thresholds:
        low_points: list[tuple[float, float]] = []
        for case in cases:
            low_drift = sum(
                float(row["weighted_drift"])
                for row in case["rows"]
                if int(row["v2"]) < threshold
            )
            low_points.append((float(case["N_left"]), low_drift / float(case["total_mass"])))
        fit = fit_power(low_points)
        locals_low = local_alphas(low_points)
        latest_value = sorted(low_points)[-1][1]
        phase_fits.append(
            {
                "stratum": f"LOW_V2_LT_{threshold}",
                "v2": -1,
                "odd": -1,
                "h": -1,
                "points": int(fit["count"]),
                "row_l1_alpha": fit["alpha"],
                "row_l1_c": fit["c"],
                "row_l1_r2": fit["r2"],
                "row_l1_local_alpha_median": median(locals_low) if locals_low else 0.0,
                "row_l1_local_alpha_min": min(locals_low) if locals_low else 0.0,
                "row_l1_local_alpha_max": max(locals_low) if locals_low else 0.0,
                "contribution_alpha": fit["alpha"],
                "contribution_r2": fit["r2"],
                "latest_N_left": sorted(low_points)[-1][0],
                "latest_sample_weight": 0.0,
                "latest_mass_share": 0.0,
                "latest_row_l1": latest_value,
                "latest_weighted_drift_component": latest_value,
                "latest_contribution_share": latest_value / float(latest_case["total_D"]) if float(latest_case["total_D"]) else 0.0,
                "latest_source_file": latest_case["source_file"],
            }
        )

    return phase_fits, latest_rows


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
    cases: list[dict[str, Any]],
    phase_fits: list[dict[str, Any]],
    latest_rows: list[dict[str, Any]],
    report_path: Path,
    phase_fits_path: Path,
    latest_path: Path,
) -> None:
    real_phase_fits = [row for row in phase_fits if not str(row["stratum"]).startswith("LOW_V2_LT_")]
    threshold_rows = [row for row in phase_fits if str(row["stratum"]).startswith("LOW_V2_LT_")]
    latest_case = max(cases, key=lambda item: int(item["N_left"]))
    low_real = [row for row in real_phase_fits if int(row["v2"]) < args.low_v2_report]
    slow_low = sorted(
        [row for row in low_real if int(row["points"]) >= args.min_points],
        key=lambda row: (float(row["row_l1_alpha"]), -float(row["latest_weighted_drift_component"])),
    )
    dominant_low = sorted(
        low_real,
        key=lambda row: float(row["latest_weighted_drift_component"]),
        reverse=True,
    )
    alpha_values = [float(row["row_l1_alpha"]) for row in low_real if int(row["points"]) >= args.min_points]

    lines: list[str] = []
    lines.append("# A0 Low-v2 Phase Decay Probe")
    lines.append("")
    lines.append("Status: finite diagnostic for A0W2 / TODO 10.M.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- input glob: `{args.input_glob}`")
    lines.append(f"- cases after dedupe: `{len(cases)}`")
    lines.append(f"- latest case: `{latest_case['source_file']}`")
    lines.append(f"- phase fits CSV: `{phase_fits_path.name}`")
    lines.append(f"- latest rows CSV: `{latest_path.name}`")
    lines.append("")
    lines.append("## Threshold Low-v2 Fits")
    lines.append("")
    lines.append("| threshold | points | alpha | R2 | latest low component | latest / total D |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for row in threshold_rows:
        threshold = str(row["stratum"]).replace("LOW_V2_LT_", "")
        lines.append(
            f"| {threshold} | {row['points']} | "
            f"{format_float(row['row_l1_alpha'])} | "
            f"{format_float(row['row_l1_r2'])} | "
            f"{format_float(row['latest_weighted_drift_component'])} | "
            f"{format_float(row['latest_contribution_share'])} |"
        )
    lines.append("")
    lines.append("## Dominant Latest Low-v2 Phases")
    lines.append("")
    lines.append(f"Low-v2 report cutoff: `v2 < {args.low_v2_report}`.")
    lines.append("")
    lines.append("| rank | phase | alpha | R2 | latest row L1 | latest component | contribution |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|")
    for rank, row in enumerate(dominant_low[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['stratum']}` | "
            f"{format_float(row['row_l1_alpha'])} | "
            f"{format_float(row['row_l1_r2'])} | "
            f"{format_float(row['latest_row_l1'])} | "
            f"{format_float(row['latest_weighted_drift_component'])} | "
            f"{format_float(row['latest_contribution_share'])} |"
        )
    lines.append("")
    lines.append("## Slowest Low-v2 Phase Fits")
    lines.append("")
    lines.append("| rank | phase | alpha | local alpha median | latest component | contribution |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(slow_low[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['stratum']}` | "
            f"{format_float(row['row_l1_alpha'])} | "
            f"{format_float(row['row_l1_local_alpha_median'])} | "
            f"{format_float(row['latest_weighted_drift_component'])} | "
            f"{format_float(row['latest_contribution_share'])} |"
        )
    lines.append("")
    lines.append("## Aggregate Signal")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    lines.append(f"| low phase count | `{len(low_real)}` |")
    lines.append(f"| median low phase alpha | `{format_float(median(alpha_values) if alpha_values else 0.0)}` |")
    lines.append(f"| min low phase alpha | `{format_float(min(alpha_values) if alpha_values else 0.0)}` |")
    lines.append(f"| max low phase alpha | `{format_float(max(alpha_values) if alpha_values else 0.0)}` |")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The exact high-v2 mass tail is already discharged.  This diagnostic asks")
    lines.append("whether fixed low-v2 phases decay individually or whether a slow phase")
    lines.append("needs a new state coordinate.  A proof route would explain these phase")
    lines.append("fits by a finite dependency-depth or residue-period cancellation lemma.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-glob", default=DEFAULT_GLOB)
    parser.add_argument("--thresholds", default="4,6,8,10,12,14")
    parser.add_argument("--low-v2-report", type=int, default=8)
    parser.add_argument("--min-points", type=int, default=4)
    parser.add_argument("--report-top", type=int, default=16)
    parser.add_argument("--output-tag", default="current_A0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = read_cases(args.input_glob)
    if not cases:
        raise SystemExit(f"no cases matched {args.input_glob!r}")
    thresholds = parse_ints(args.thresholds)
    phase_fits, latest_rows = analyze(cases, thresholds)
    report_path, phase_fits_path, latest_path = output_paths(args.output_tag)
    write_csv(phase_fits, phase_fits_path)
    write_csv(latest_rows, latest_path)
    write_report(
        args=args,
        cases=cases,
        phase_fits=phase_fits,
        latest_rows=latest_rows,
        report_path=report_path,
        phase_fits_path=phase_fits_path,
        latest_path=latest_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {phase_fits_path}")
    print(f"wrote {latest_path}")


if __name__ == "__main__":
    main()
