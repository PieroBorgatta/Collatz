"""
113_A0_decay_law_probe.py

Estimate the finite decay law for the phase-only A0 prefix drift using
existing script-110 by-pair CSV outputs.

The target diagnostic is

  D_N ~= c N^{-alpha},

where D_N is the weighted row-L1 mean for the comparison N -> 2N.
This is a finite trend fit only.  It is not a proof that D_N -> 0.
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
DEFAULT_GLOB = "collatz_110_*_refined_square_probe_by_pair.csv"


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_113{suffix}_A0_decay_law_probe"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_points.csv"


def parse_T(path: Path) -> int | None:
    match = re.search(r"_T(\d+)_", path.name)
    if match is None:
        return None
    return int(match.group(1))


def read_points(pattern: str) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for path in sorted(ROOT.glob(pattern)):
        T = parse_T(path)
        if T is None:
            continue
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter=";"):
                if int(row["bits"]) != 0:
                    continue
                j_left = int(row["j_left"])
                j_right = int(row["j_right"])
                if j_right != 2 * j_left:
                    continue
                scale_left = j_left * (1 << T)
                scale_right = j_right * (1 << T)
                points.append(
                    {
                        "source_file": path.name,
                        "T": T,
                        "j_left": j_left,
                        "j_right": j_right,
                        "N_left": scale_left,
                        "N_right": scale_right,
                        "weighted_l1_mean": float(row["weighted_l1_mean"]),
                        "weighted_l1_p95": float(row["weighted_l1_p95"]),
                        "weighted_l1_p99": float(row["weighted_l1_p99"]),
                        "weighted_l1_max": float(row["weighted_l1_max"]),
                        "source_keys": int(row["common_source_keys"]),
                    }
                )
    return points


def dedupe_points(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for point in points:
        grouped[(int(point["N_left"]), int(point["N_right"]))].append(point)

    out: list[dict[str, Any]] = []
    for (N_left, N_right), rows in sorted(grouped.items()):
        means = [float(row["weighted_l1_mean"]) for row in rows]
        p95s = [float(row["weighted_l1_p95"]) for row in rows]
        p99s = [float(row["weighted_l1_p99"]) for row in rows]
        maxes = [float(row["weighted_l1_max"]) for row in rows]
        out.append(
            {
                "N_left": N_left,
                "N_right": N_right,
                "replicates": len(rows),
                "T_values": ",".join(str(row["T"]) for row in rows),
                "j_pairs": ",".join(f"{row['j_left']}->{row['j_right']}" for row in rows),
                "weighted_l1_mean": mean(means),
                "weighted_l1_mean_min": min(means),
                "weighted_l1_mean_max": max(means),
                "weighted_l1_p95": mean(p95s),
                "weighted_l1_p99": mean(p99s),
                "weighted_l1_max": mean(maxes),
                "source_files": " | ".join(row["source_file"] for row in rows),
            }
        )
    return out


def linear_fit_loglog(points: list[dict[str, Any]]) -> dict[str, float]:
    valid = [
        (math.log(float(point["N_left"])), math.log(float(point["weighted_l1_mean"])))
        for point in points
        if float(point["N_left"]) > 0 and float(point["weighted_l1_mean"]) > 0
    ]
    if len(valid) < 2:
        return {
            "count": float(len(valid)),
            "alpha": 0.0,
            "log_c": 0.0,
            "c": 0.0,
            "r2": 0.0,
        }
    xs = [x for x, _y in valid]
    ys = [y for _x, y in valid]
    x_bar = mean(xs)
    y_bar = mean(ys)
    ss_xx = sum((x - x_bar) ** 2 for x in xs)
    ss_xy = sum((x - x_bar) * (y - y_bar) for x, y in valid)
    slope = ss_xy / ss_xx if ss_xx else 0.0
    intercept = y_bar - slope * x_bar
    predictions = [intercept + slope * x for x in xs]
    ss_res = sum((y - y_hat) ** 2 for y, y_hat in zip(ys, predictions, strict=True))
    ss_tot = sum((y - y_bar) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot else 1.0
    return {
        "count": float(len(valid)),
        "alpha": -slope,
        "log_c": intercept,
        "c": math.exp(intercept),
        "r2": r2,
    }


def add_fit_residuals(points: list[dict[str, Any]], fit: dict[str, float]) -> None:
    c = float(fit["c"])
    alpha = float(fit["alpha"])
    for point in points:
        N = float(point["N_left"])
        observed = float(point["weighted_l1_mean"])
        predicted = c * (N ** (-alpha)) if N > 0 else 0.0
        point["fit_predicted_mean"] = predicted
        point["fit_ratio_observed_over_predicted"] = (
            observed / predicted if predicted > 0 else 0.0
        )
        point["log_residual"] = (
            math.log(observed) - math.log(predicted)
            if observed > 0 and predicted > 0
            else 0.0
        )


def local_exponents(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ordered = sorted(points, key=lambda point: int(point["N_left"]))
    for left, right in zip(ordered, ordered[1:], strict=False):
        N0 = float(left["N_left"])
        N1 = float(right["N_left"])
        D0 = float(left["weighted_l1_mean"])
        D1 = float(right["weighted_l1_mean"])
        if N0 <= 0.0 or N1 <= 0.0 or D0 <= 0.0 or D1 <= 0.0 or N0 == N1:
            alpha = 0.0
        else:
            alpha = -((math.log(D1) - math.log(D0)) / (math.log(N1) - math.log(N0)))
        rows.append(
            {
                "N_from": int(left["N_left"]),
                "N_to": int(right["N_left"]),
                "D_from": D0,
                "D_to": D1,
                "local_alpha": alpha,
            }
        )
    return rows


def leave_one_out_fits(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ordered = sorted(points, key=lambda point: int(point["N_left"]))
    for omitted in ordered:
        kept = [point for point in ordered if point is not omitted]
        fit = linear_fit_loglog(kept)
        rows.append(
            {
                "omitted_N_left": int(omitted["N_left"]),
                "omitted_D": float(omitted["weighted_l1_mean"]),
                "alpha": fit["alpha"],
                "c": fit["c"],
                "r2": fit["r2"],
            }
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
        return f"{value:.9g}"
    return str(value)


def write_report(
    *,
    args: argparse.Namespace,
    raw_points: list[dict[str, Any]],
    points: list[dict[str, Any]],
    fit: dict[str, float],
    report_path: Path,
    csv_path: Path,
) -> None:
    lines: list[str] = []
    lines.append("# A0 Decay Law Probe")
    lines.append("")
    lines.append("Status: finite trend fit only.  This does not prove `D_N -> 0`.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- input glob: `{args.input_glob}`")
    lines.append(f"- raw A0 points: `{len(raw_points)}`")
    lines.append(f"- deduped scales: `{len(points)}`")
    lines.append(f"- output CSV: `{csv_path.name}`")
    lines.append("")
    lines.append("## Fit")
    lines.append("")
    lines.append("Model:")
    lines.append("")
    lines.append("```text")
    lines.append("D_N ~= c N^{-alpha}")
    lines.append("```")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    for key in ("count", "alpha", "c", "log_c", "r2"):
        lines.append(f"| `{key}` | `{format_float(fit[key])}` |")
    lines.append("")
    local_rows = local_exponents(points)
    loo_rows = leave_one_out_fits(points)
    local_alphas = [float(row["local_alpha"]) for row in local_rows]
    loo_alphas = [float(row["alpha"]) for row in loo_rows]
    if local_alphas:
        lines.append("Local consecutive exponents:")
        lines.append("")
        lines.append("| N_i -> N_{i+1} | local alpha |")
        lines.append("|---:|---:|")
        for row in local_rows:
            lines.append(
                f"| {row['N_from']} -> {row['N_to']} | "
                f"{format_float(row['local_alpha'])} |"
            )
        lines.append("")
        lines.append("Local alpha summary:")
        lines.append("")
        lines.append("| metric | value |")
        lines.append("|---|---:|")
        lines.append(f"| `min` | `{format_float(min(local_alphas))}` |")
        lines.append(f"| `median` | `{format_float(median(local_alphas))}` |")
        lines.append(f"| `max` | `{format_float(max(local_alphas))}` |")
        lines.append("")
    if loo_alphas:
        lines.append("Leave-one-out fits:")
        lines.append("")
        lines.append("| omitted N | alpha | R2 |")
        lines.append("|---:|---:|---:|")
        for row in loo_rows:
            lines.append(
                f"| {row['omitted_N_left']} | "
                f"{format_float(row['alpha'])} | "
                f"{format_float(row['r2'])} |"
            )
        lines.append("")
        lines.append("Leave-one-out alpha summary:")
        lines.append("")
        lines.append("| metric | value |")
        lines.append("|---|---:|")
        lines.append(f"| `min` | `{format_float(min(loo_alphas))}` |")
        lines.append(f"| `median` | `{format_float(median(loo_alphas))}` |")
        lines.append(f"| `max` | `{format_float(max(loo_alphas))}` |")
        lines.append("")
    lines.append("## Points")
    lines.append("")
    lines.append(
        "| N -> 2N | D_N | p95 | p99 | max | replicates | predicted | obs/pred |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for point in points:
        lines.append(
            f"| {point['N_left']} -> {point['N_right']} | "
            f"{format_float(point['weighted_l1_mean'])} | "
            f"{format_float(point['weighted_l1_p95'])} | "
            f"{format_float(point['weighted_l1_p99'])} | "
            f"{format_float(point['weighted_l1_max'])} | "
            f"{point['replicates']} | "
            f"{format_float(point['fit_predicted_mean'])} | "
            f"{format_float(point['fit_ratio_observed_over_predicted'])} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- Positive `alpha` is finite evidence for decay of the weak A0 drift.")
    lines.append("- High `r2` on few points is not a theorem and can be misleading.")
    lines.append("- The max column is tracked separately because the target is weak averaged control.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-glob", default=DEFAULT_GLOB)
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_points = read_points(args.input_glob)
    points = dedupe_points(raw_points)
    fit = linear_fit_loglog(points)
    add_fit_residuals(points, fit)
    report_path, csv_path = output_paths(args.output_tag)
    write_csv(points, csv_path)
    write_report(
        args=args,
        raw_points=raw_points,
        points=points,
        fit=fit,
        report_path=report_path,
        csv_path=csv_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
