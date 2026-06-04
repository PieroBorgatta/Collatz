"""
115_A0_decomposition_decay_probe.py

Test the A0 proof decomposition across all available script-111 A0 phase
strata:

  D_N <= D_N(v2 < R) + 2 * mu_N(v2 >= R).

For each threshold R, the script reports:

  low_component_N = sum_{v2<R} weighted_drift / total_mass
  tail_mass_N     = sum_{v2>=R} sample_weight / total_mass
  tail_bound_N    = 2 * tail_mass_N
  proof_bound_N   = low_component_N + tail_bound_N

and fits a power law to the low component:

  low_component_N ~= c_R N^{-alpha_R}.

This is finite evidence only.  It does not prove a uniform tail estimate or
the A0 weak approximation theorem.
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
    stem = f"collatz_115{suffix}_A0_decomposition_decay_probe"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_by_threshold_scale.csv",
        ROOT / f"{stem}_fits.csv",
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


def read_phase_file(path: Path) -> dict[str, Any] | None:
    parsed = parse_filename(path)
    if parsed is None:
        return None
    T, j_left, j_right = parsed
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            v2, odd, h = parse_phase(row["stratum"])
            rows.append(
                {
                    "v2": v2,
                    "odd": odd,
                    "h": h,
                    "stratum": row["stratum"],
                    "sample_weight": float(row["sample_weight"]),
                    "weighted_drift": float(row["weighted_drift"]),
                    "max_l1": float(row["max_l1"]),
                }
            )
    total_mass = sum(float(row["sample_weight"]) for row in rows)
    total_drift = sum(float(row["weighted_drift"]) for row in rows)
    return {
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
        "global_max_l1": max((float(row["max_l1"]) for row in rows), default=0.0),
    }


def read_cases(pattern: str) -> list[dict[str, Any]]:
    cases = []
    for path in sorted(ROOT.glob(pattern)):
        case = read_phase_file(path)
        if case is not None:
            cases.append(case)
    # Deduplicate exact scale repeats, preferring the largest T file if needed.
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        grouped[(int(case["N_left"]), int(case["N_right"]))].append(case)
    deduped: list[dict[str, Any]] = []
    for key, rows in sorted(grouped.items()):
        rows.sort(key=lambda item: (int(item["T"]), int(item["j_left"])), reverse=True)
        deduped.append(rows[0])
    return deduped


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


def local_alpha(points: list[tuple[float, float]]) -> list[float]:
    values: list[float] = []
    ordered = sorted(points)
    for (N0, value0), (N1, value1) in zip(ordered, ordered[1:], strict=False):
        if N0 <= 0 or N1 <= 0 or value0 <= 0 or value1 <= 0 or N0 == N1:
            continue
        values.append(-((math.log(value1) - math.log(value0)) / (math.log(N1) - math.log(N0))))
    return values


def analyze(cases: list[dict[str, Any]], thresholds: list[int]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_scale: list[dict[str, Any]] = []
    fits: list[dict[str, Any]] = []
    for threshold in thresholds:
        low_points: list[tuple[float, float]] = []
        bound_points: list[tuple[float, float]] = []
        tail_mass_points: list[tuple[float, float]] = []
        for case in cases:
            rows = case["rows"]
            total_mass = float(case["total_mass"])
            total_drift = float(case["total_drift"])
            low = [row for row in rows if int(row["v2"]) < threshold]
            tail = [row for row in rows if int(row["v2"]) >= threshold]
            low_drift = sum(float(row["weighted_drift"]) for row in low)
            tail_drift = sum(float(row["weighted_drift"]) for row in tail)
            low_mass = sum(float(row["sample_weight"]) for row in low)
            tail_mass = sum(float(row["sample_weight"]) for row in tail)
            low_component = low_drift / total_mass if total_mass else 0.0
            tail_component = tail_drift / total_mass if total_mass else 0.0
            tail_mass_share = tail_mass / total_mass if total_mass else 0.0
            tail_bound = 2.0 * tail_mass_share
            proof_bound = low_component + tail_bound
            row = {
                "threshold_v2_ge": threshold,
                "T": case["T"],
                "j_left": case["j_left"],
                "j_right": case["j_right"],
                "N_left": case["N_left"],
                "N_right": case["N_right"],
                "total_D": case["total_D"],
                "low_component": low_component,
                "tail_actual_component": tail_component,
                "tail_mass_share": tail_mass_share,
                "tail_bound_2mass": tail_bound,
                "proof_bound_low_plus_2mass": proof_bound,
                "low_mass_share": low_mass / total_mass if total_mass else 0.0,
                "tail_contribution_share": tail_drift / total_drift if total_drift else 0.0,
                "low_contribution_share": low_drift / total_drift if total_drift else 0.0,
                "low_mean_l1_on_low_mass": low_drift / low_mass if low_mass else 0.0,
                "tail_mean_l1_on_tail_mass": tail_drift / tail_mass if tail_mass else 0.0,
                "tail_max_l1": max((float(row["max_l1"]) for row in tail), default=0.0),
                "low_max_l1": max((float(row["max_l1"]) for row in low), default=0.0),
                "source_file": case["source_file"],
            }
            by_scale.append(row)
            low_points.append((float(case["N_left"]), low_component))
            bound_points.append((float(case["N_left"]), proof_bound))
            tail_mass_points.append((float(case["N_left"]), tail_mass_share))

        fit_low = fit_power(low_points)
        fit_bound = fit_power(bound_points)
        fit_tail = fit_power(tail_mass_points)
        locals_low = local_alpha(low_points)
        latest = max(
            [row for row in by_scale if int(row["threshold_v2_ge"]) == threshold],
            key=lambda row: int(row["N_left"]),
        )
        fits.append(
            {
                "threshold_v2_ge": threshold,
                "points": int(fit_low["count"]),
                "low_alpha": fit_low["alpha"],
                "low_c": fit_low["c"],
                "low_r2": fit_low["r2"],
                "low_local_alpha_median": median(locals_low) if locals_low else 0.0,
                "low_local_alpha_min": min(locals_low) if locals_low else 0.0,
                "low_local_alpha_max": max(locals_low) if locals_low else 0.0,
                "proof_bound_alpha": fit_bound["alpha"],
                "proof_bound_r2": fit_bound["r2"],
                "tail_mass_alpha": fit_tail["alpha"],
                "tail_mass_r2": fit_tail["r2"],
                "latest_N_left": latest["N_left"],
                "latest_total_D": latest["total_D"],
                "latest_low_component": latest["low_component"],
                "latest_tail_actual_component": latest["tail_actual_component"],
                "latest_tail_mass_share": latest["tail_mass_share"],
                "latest_tail_bound_2mass": latest["tail_bound_2mass"],
                "latest_proof_bound": latest["proof_bound_low_plus_2mass"],
                "latest_bound_over_total_D": (
                    latest["proof_bound_low_plus_2mass"] / latest["total_D"]
                    if latest["total_D"]
                    else 0.0
                ),
            }
        )
    fits.sort(key=lambda row: (float(row["latest_bound_over_total_D"]), -float(row["low_alpha"])))
    by_scale.sort(key=lambda row: (int(row["threshold_v2_ge"]), int(row["N_left"])))
    return by_scale, fits


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


def write_report(
    *,
    args: argparse.Namespace,
    cases: list[dict[str, Any]],
    by_scale: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    report_path: Path,
    by_scale_path: Path,
    fits_path: Path,
) -> None:
    lines: list[str] = []
    lines.append("# A0 Decomposition Decay Probe")
    lines.append("")
    lines.append("Status: finite diagnostic only.  This does not prove the A0 theorem.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- input glob: `{args.input_glob}`")
    lines.append(f"- deduped cases: `{len(cases)}`")
    lines.append(f"- thresholds: `{args.thresholds}`")
    lines.append(f"- by-scale CSV: `{by_scale_path.name}`")
    lines.append(f"- fits CSV: `{fits_path.name}`")
    lines.append("")
    lines.append("## Cases")
    lines.append("")
    lines.append("| N -> 2N | T | j pair | total D | max row L1 |")
    lines.append("|---:|---:|---:|---:|---:|")
    for case in sorted(cases, key=lambda item: int(item["N_left"])):
        lines.append(
            f"| {case['N_left']} -> {case['N_right']} | "
            f"{case['T']} | {case['j_left']}->{case['j_right']} | "
            f"{format_float(case['total_D'])} | "
            f"{format_float(case['global_max_l1'])} |"
        )
    lines.append("")
    lines.append("## Threshold Summary")
    lines.append("")
    lines.append(
        "| rank | R | low alpha | low R2 | tail-mass alpha | latest low | "
        "latest tail mass | latest 2mass | bound/total |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for rank, row in enumerate(fits, start=1):
        lines.append(
            f"| {rank} | {row['threshold_v2_ge']} | "
            f"{format_float(row['low_alpha'])} | "
            f"{format_float(row['low_r2'])} | "
            f"{format_float(row['tail_mass_alpha'])} | "
            f"{format_float(row['latest_low_component'])} | "
            f"{format_float(row['latest_tail_mass_share'])} | "
            f"{format_float(row['latest_tail_bound_2mass'])} | "
            f"{format_float(row['latest_bound_over_total_D'])} |"
        )
    lines.append("")
    lines.append("## Reading Rule")
    lines.append("")
    lines.append("- `low alpha` estimates decay of `D_N(v2 < R)`.")
    lines.append("- `tail-mass alpha` estimates decay of the exceptional source mass for fixed R.")
    lines.append("- `bound/total` compares the proof-style bound to the observed total at the latest scale.")
    lines.append("- A useful threshold has a decaying low part and a not-too-loose tail bound.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-glob", default=DEFAULT_GLOB)
    parser.add_argument("--thresholds", default="4,6,8,10,12,14")
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    thresholds = parse_ints(args.thresholds)
    cases = read_cases(args.input_glob)
    by_scale, fits = analyze(cases, thresholds)
    report_path, by_scale_path, fits_path = output_paths(args.output_tag)
    write_csv(by_scale, by_scale_path)
    write_csv(fits, fits_path)
    write_report(
        args=args,
        cases=cases,
        by_scale=by_scale,
        fits=fits,
        report_path=report_path,
        by_scale_path=by_scale_path,
        fits_path=fits_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {by_scale_path}")
    print(f"wrote {fits_path}")


if __name__ == "__main__":
    main()
