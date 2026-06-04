"""
122_A0_top_haar_decay_summary.py

Summarize the top dyadic Haar coefficient decay for the current A0
phase-strata data.

Scripts 119 and 121 show that, for a fixed source phase, the script-111
prefix row drift is exactly half of the adjacent dyadic half-block
discrepancy:

  prefix_l1(N) = 0.5 * || mean_[N,2N) - mean_[0,N) ||_1.

Thus the root/top Haar coefficient on the doubled block is

  root_haar_l1(N) = 2 * row_l1(N).

This script does not retrace Collatz orbits.  It recasts the existing
script-111 A0 phase-strata CSVs into the proof-facing quantity needed for
TODO 10.M:

  for each fixed low-v2 source phase, root_haar_l1(N) -> 0.

Finite evidence only.
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


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_122{suffix}_A0_top_haar_decay_summary"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_phase_fits.csv",
        ROOT / f"{stem}_threshold_fits.csv",
        ROOT / f"{stem}_case_points.csv",
    )


def parse_filename(path: Path) -> tuple[int, int, int] | None:
    match = re.search(r"_T(\d+)_j(\d+)_(\d+)_b0_", path.name)
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def parse_phase(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected phase stratum {text!r}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def parse_ints(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def fit_power(points: list[tuple[float, float]]) -> dict[str, float]:
    valid = [(math.log(n), math.log(y)) for n, y in points if n > 0 and y > 0]
    if len(valid) < 2:
        return {"points": float(len(valid)), "alpha": 0.0, "c": 0.0, "r2": 0.0}
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
        "points": float(len(valid)),
        "alpha": -slope,
        "c": math.exp(intercept),
        "r2": 1.0 - ss_res / ss_tot if ss_tot else 1.0,
    }


def local_alphas(points: list[tuple[float, float]]) -> list[float]:
    out: list[float] = []
    ordered = sorted(points)
    for (n0, y0), (n1, y1) in zip(ordered, ordered[1:], strict=False):
        if n0 <= 0 or n1 <= 0 or y0 <= 0 or y1 <= 0 or n0 == n1:
            continue
        out.append(-((math.log(y1) - math.log(y0)) / (math.log(n1) - math.log(n0))))
    return out


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
                prefix_row_l1 = weighted_drift / sample_weight if sample_weight else 0.0
                rows.append(
                    {
                        "stratum": row["stratum"],
                        "v2": v2,
                        "odd": odd,
                        "h": h,
                        "sample_weight": sample_weight,
                        "weighted_drift": weighted_drift,
                        "prefix_row_l1": prefix_row_l1,
                        "root_haar_l1": 2.0 * prefix_row_l1,
                        "max_l1": float(row["max_l1"]),
                    }
                )
        total_mass = sum(float(row["sample_weight"]) for row in rows)
        total_prefix_drift = sum(float(row["weighted_drift"]) for row in rows)
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
                "total_prefix_drift": total_prefix_drift,
                "total_prefix_D": (
                    total_prefix_drift / total_mass if total_mass else 0.0
                ),
                "total_root_haar_D": (
                    2.0 * total_prefix_drift / total_mass if total_mass else 0.0
                ),
            }
        )

    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for case in raw_cases:
        grouped[(int(case["N_left"]), int(case["N_right"]))].append(case)

    cases: list[dict[str, Any]] = []
    for same_scale in grouped.values():
        same_scale.sort(key=lambda item: (int(item["T"]), int(item["j_left"])), reverse=True)
        cases.append(same_scale[0])
    cases.sort(key=lambda item: (int(item["N_left"]), int(item["N_right"])))
    return cases


def phase_rows(cases: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_phase: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        for row in case["rows"]:
            by_phase[str(row["stratum"])].append(
                {
                    **row,
                    "T": case["T"],
                    "j_left": case["j_left"],
                    "j_right": case["j_right"],
                    "N_left": case["N_left"],
                    "N_right": case["N_right"],
                    "total_mass": case["total_mass"],
                    "total_prefix_drift": case["total_prefix_drift"],
                    "total_prefix_D": case["total_prefix_D"],
                    "total_root_haar_D": case["total_root_haar_D"],
                    "source_file": case["source_file"],
                }
            )
    return by_phase


def analyze_phases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fits: list[dict[str, Any]] = []
    by_phase = phase_rows(cases)
    for stratum, rows in by_phase.items():
        v2, odd, h = parse_phase(stratum)
        root_points = [
            (float(row["N_left"]), float(row["root_haar_l1"]))
            for row in rows
        ]
        component_points = [
            (
                float(row["N_left"]),
                2.0 * float(row["weighted_drift"]) / float(row["total_mass"]),
            )
            for row in rows
            if float(row["total_mass"]) > 0
        ]
        root_fit = fit_power(root_points)
        component_fit = fit_power(component_points)
        locals_root = local_alphas(root_points)
        latest = max(rows, key=lambda row: int(row["N_left"]))
        latest_component = (
            2.0 * float(latest["weighted_drift"]) / float(latest["total_mass"])
            if float(latest["total_mass"])
            else 0.0
        )
        fits.append(
            {
                "stratum": stratum,
                "v2": v2,
                "odd": odd,
                "h": h,
                "points": int(root_fit["points"]),
                "root_haar_alpha": root_fit["alpha"],
                "root_haar_c": root_fit["c"],
                "root_haar_r2": root_fit["r2"],
                "root_haar_local_alpha_median": median(locals_root) if locals_root else 0.0,
                "root_haar_local_alpha_min": min(locals_root) if locals_root else 0.0,
                "root_haar_local_alpha_max": max(locals_root) if locals_root else 0.0,
                "root_component_alpha": component_fit["alpha"],
                "root_component_r2": component_fit["r2"],
                "latest_N_left": latest["N_left"],
                "latest_sample_weight": latest["sample_weight"],
                "latest_mass_share": (
                    float(latest["sample_weight"]) / float(latest["total_mass"])
                    if float(latest["total_mass"])
                    else 0.0
                ),
                "latest_prefix_row_l1": latest["prefix_row_l1"],
                "latest_root_haar_l1": latest["root_haar_l1"],
                "latest_root_component": latest_component,
                "latest_root_component_share": (
                    latest_component / float(latest["total_root_haar_D"])
                    if float(latest["total_root_haar_D"])
                    else 0.0
                ),
                "latest_source_file": latest["source_file"],
            }
        )
    fits.sort(key=lambda row: float(row["latest_root_component"]), reverse=True)
    return fits


def analyze_thresholds(cases: list[dict[str, Any]], thresholds: list[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    latest_case = max(cases, key=lambda item: int(item["N_left"]))
    for threshold in thresholds:
        prefix_points: list[tuple[float, float]] = []
        root_points: list[tuple[float, float]] = []
        for case in cases:
            low_prefix_drift = sum(
                float(row["weighted_drift"])
                for row in case["rows"]
                if int(row["v2"]) < threshold
            )
            prefix_component = (
                low_prefix_drift / float(case["total_mass"])
                if float(case["total_mass"])
                else 0.0
            )
            prefix_points.append((float(case["N_left"]), prefix_component))
            root_points.append((float(case["N_left"]), 2.0 * prefix_component))
        root_fit = fit_power(root_points)
        locals_root = local_alphas(root_points)
        latest_root = sorted(root_points)[-1][1]
        rows.append(
            {
                "threshold": threshold,
                "phase_count_latest": sum(
                    1 for row in latest_case["rows"] if int(row["v2"]) < threshold
                ),
                "points": int(root_fit["points"]),
                "root_haar_alpha": root_fit["alpha"],
                "root_haar_c": root_fit["c"],
                "root_haar_r2": root_fit["r2"],
                "root_haar_local_alpha_median": median(locals_root) if locals_root else 0.0,
                "root_haar_local_alpha_min": min(locals_root) if locals_root else 0.0,
                "root_haar_local_alpha_max": max(locals_root) if locals_root else 0.0,
                "latest_N_left": sorted(root_points)[-1][0],
                "latest_root_haar_component": latest_root,
                "latest_prefix_component": latest_root / 2.0,
                "latest_total_root_haar_D": latest_case["total_root_haar_D"],
                "latest_component_share": (
                    latest_root / float(latest_case["total_root_haar_D"])
                    if float(latest_case["total_root_haar_D"])
                    else 0.0
                ),
                "latest_source_file": latest_case["source_file"],
            }
        )
    return rows


def case_points(cases: list[dict[str, Any]], thresholds: list[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        item: dict[str, Any] = {
            "source_file": case["source_file"],
            "T": case["T"],
            "j_left": case["j_left"],
            "j_right": case["j_right"],
            "N_left": case["N_left"],
            "N_right": case["N_right"],
            "phase_count": len(case["rows"]),
            "total_mass": case["total_mass"],
            "total_prefix_D": case["total_prefix_D"],
            "total_root_haar_D": case["total_root_haar_D"],
        }
        for threshold in thresholds:
            low_prefix_drift = sum(
                float(row["weighted_drift"])
                for row in case["rows"]
                if int(row["v2"]) < threshold
            )
            prefix_component = low_prefix_drift / float(case["total_mass"])
            item[f"root_haar_v2_lt_{threshold}"] = 2.0 * prefix_component
            item[f"prefix_D_v2_lt_{threshold}"] = prefix_component
        rows.append(item)
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
    cases: list[dict[str, Any]],
    phase_fit_rows: list[dict[str, Any]],
    threshold_rows: list[dict[str, Any]],
    report_path: Path,
    phase_path: Path,
    threshold_path: Path,
    points_path: Path,
) -> None:
    latest_case = max(cases, key=lambda item: int(item["N_left"]))
    low_rows = [row for row in phase_fit_rows if int(row["v2"]) < args.low_v2_report]
    low_with_points = [
        row for row in low_rows if int(row["points"]) >= args.min_points
    ]
    dominant_low = sorted(
        low_rows, key=lambda row: float(row["latest_root_component"]), reverse=True
    )
    slow_low = sorted(
        low_with_points,
        key=lambda row: (
            float(row["root_haar_alpha"]),
            -float(row["latest_root_component"]),
        ),
    )
    alphas = [float(row["root_haar_alpha"]) for row in low_with_points]

    lines: list[str] = []
    lines.append("# A0 Top Haar Decay Summary")
    lines.append("")
    lines.append("Status: finite diagnostic for TODO `10.M`; not a proof.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- input glob: `{args.input_glob}`")
    lines.append(f"- cases after dedupe: `{len(cases)}`")
    lines.append(f"- latest case: `{latest_case['source_file']}`")
    lines.append(f"- phase fits CSV: `{phase_path.name}`")
    lines.append(f"- threshold fits CSV: `{threshold_path.name}`")
    lines.append(f"- case points CSV: `{points_path.name}`")
    lines.append("")
    lines.append("## Identity Used")
    lines.append("")
    lines.append("For the A0 phase rows tested in scripts `119` and `121`:")
    lines.append("")
    lines.append("```text")
    lines.append("root_haar_l1(N) = ||mean_[N,2N) - mean_[0,N)||_1")
    lines.append("                = 2 * prefix_row_l1(N).")
    lines.append("```")
    lines.append("")
    lines.append("So the fitted exponent is unchanged from script `118`, but the")
    lines.append("quantity is now exactly the top dyadic block-discrepancy coefficient.")
    lines.append("")
    lines.append("## Threshold Fits")
    lines.append("")
    lines.append("| v2 cutoff | phases latest | points | alpha | R2 | latest root component | share of total root |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")
    for row in threshold_rows:
        lines.append(
            f"| < {row['threshold']} | {row['phase_count_latest']} | "
            f"{row['points']} | {format_float(row['root_haar_alpha'])} | "
            f"{format_float(row['root_haar_r2'])} | "
            f"{format_float(row['latest_root_haar_component'])} | "
            f"{format_float(row['latest_component_share'])} |"
        )
    lines.append("")
    lines.append("## Dominant Latest Low-v2 Phases")
    lines.append("")
    lines.append(f"Low-v2 report cutoff: `v2 < {args.low_v2_report}`.")
    lines.append("")
    lines.append("| rank | phase | alpha | latest root Haar L1 | latest root component | share |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(dominant_low[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['stratum']}` | "
            f"{format_float(row['root_haar_alpha'])} | "
            f"{format_float(row['latest_root_haar_l1'])} | "
            f"{format_float(row['latest_root_component'])} | "
            f"{format_float(row['latest_root_component_share'])} |"
        )
    lines.append("")
    lines.append("## Slowest Low-v2 Phase Fits")
    lines.append("")
    lines.append("| rank | phase | alpha | local alpha median | latest root component | share |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for rank, row in enumerate(slow_low[: args.report_top], start=1):
        lines.append(
            f"| {rank} | `{row['stratum']}` | "
            f"{format_float(row['root_haar_alpha'])} | "
            f"{format_float(row['root_haar_local_alpha_median'])} | "
            f"{format_float(row['latest_root_component'])} | "
            f"{format_float(row['latest_root_component_share'])} |"
        )
    lines.append("")
    lines.append("## Aggregate Low-v2 Signal")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    lines.append(f"| low phase count | `{len(low_rows)}` |")
    lines.append(f"| fit-qualified low phase count | `{len(low_with_points)}` |")
    lines.append(f"| median low phase alpha | `{format_float(median(alphas) if alphas else 0.0)}` |")
    lines.append(f"| min low phase alpha | `{format_float(min(alphas) if alphas else 0.0)}` |")
    lines.append(f"| max low phase alpha | `{format_float(max(alphas) if alphas else 0.0)}` |")
    lines.append("")
    lines.append("## Theorem-Oriented Reading")
    lines.append("")
    lines.append("For fixed `R`, there are finitely many phases with `v2 < R`.")
    lines.append("If each such phase has vanishing top Haar coefficient, then the")
    lines.append("weighted low-`v2` block discrepancy vanishes:")
    lines.append("")
    lines.append("```text")
    lines.append("D_N(v2 < R) -> 0.")
    lines.append("```")
    lines.append("")
    lines.append("Together with the exact high-`v2` source-tail count from script `117`,")
    lines.append("this is the current A0 weak-bridge proof target.  The present data")
    lines.append("support power-law decay near alpha ~= 0.6 for aggregate thresholds,")
    lines.append("but a proof still requires a structural dyadic discrepancy lemma.")
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
    phase_fit_rows = analyze_phases(cases)
    threshold_rows = analyze_thresholds(cases, thresholds)
    points_rows = case_points(cases, thresholds)
    report_path, phase_path, threshold_path, points_path = output_paths(args.output_tag)
    write_csv(phase_fit_rows, phase_path)
    write_csv(threshold_rows, threshold_path)
    write_csv(points_rows, points_path)
    write_report(
        args=args,
        cases=cases,
        phase_fit_rows=phase_fit_rows,
        threshold_rows=threshold_rows,
        report_path=report_path,
        phase_path=phase_path,
        threshold_path=threshold_path,
        points_path=points_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {phase_path}")
    print(f"wrote {threshold_path}")
    print(f"wrote {points_path}")


if __name__ == "__main__":
    main()
