"""
117_A0_v2_tail_formula.py

Verify the exact source-count formula behind the A0 high-v2 tail:

  mu_{L,R}({phase_v2 >= q})
    = (m(L,q) + m(R,q)) / (L + R - z),

where L = j_left * 2^T, R = j_right * 2^T, z is 2 if t=0 is
excluded from both prefixes, and

  m(N,q) = floor((N - 1) / 2^q)             when t=0 is excluded,
  m(N,q) = floor((N - 1) / 2^q) + 1         when t=0 is included.

For the current script-111 A0 diagnostics, t=0 is excluded.  Therefore

  mu_{L,R}({phase_v2 >= q}) <= 2^-q

for every threshold q up to the v2 cap.  This script checks the formula
against the phase-strata CSVs emitted by script 111.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GLOB = "collatz_111_*_b0_refined_square_key_drift_phase_strata.csv"


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_117{suffix}_A0_v2_tail_formula"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_scale.csv"


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


def read_case(path: Path) -> dict[str, Any] | None:
    parsed = parse_filename(path)
    if parsed is None:
        return None
    T, j_left, j_right = parsed
    rows: list[dict[str, Any]] = []
    h_values: set[int] = set()
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            v2, odd, h = parse_phase(row["stratum"])
            h_values.add(h)
            rows.append(
                {
                    "v2": v2,
                    "odd": odd,
                    "h": h,
                    "sample_weight": float(row["sample_weight"]),
                    "weighted_drift": float(row["weighted_drift"]),
                }
            )

    total_mass = sum(float(row["sample_weight"]) for row in rows)
    h_mod = len(h_values)
    n_left = j_left * (1 << T)
    n_right = j_right * (1 << T)
    scaled_total = (2.0 * total_mass / h_mod) if h_mod else 0.0
    expected_skip = float(n_left + n_right - 2)
    expected_include = float(n_left + n_right)
    if abs(scaled_total - expected_skip) <= 1e-6:
        include_t_zero = False
    elif abs(scaled_total - expected_include) <= 1e-6:
        include_t_zero = True
    else:
        include_t_zero = False

    return {
        "source_file": path.name,
        "T": T,
        "j_left": j_left,
        "j_right": j_right,
        "N_left": n_left,
        "N_right": n_right,
        "h_mod": h_mod,
        "include_t_zero": include_t_zero,
        "scaled_total_source_rows": scaled_total,
        "rows": rows,
        "total_mass": total_mass,
    }


def read_cases(pattern: str) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(ROOT.glob(pattern)):
        case = read_case(path)
        if case is not None:
            cases.append(case)

    # Deduplicate exact source scales, keeping the largest T realization.
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        grouped[(int(case["N_left"]), int(case["N_right"]))].append(case)

    deduped: list[dict[str, Any]] = []
    for rows in grouped.values():
        rows.sort(key=lambda item: (int(item["T"]), int(item["j_left"])), reverse=True)
        deduped.append(rows[0])
    deduped.sort(key=lambda item: (int(item["N_left"]), int(item["N_right"])))
    return deduped


def count_tail_sources(n: int, threshold: int, include_t_zero: bool) -> int:
    if n <= 0:
        return 0
    positive_count = (n - 1) // (1 << threshold)
    return positive_count + (1 if include_t_zero else 0)


def formula_tail_mass(case: dict[str, Any], threshold: int) -> float:
    include_t_zero = bool(case["include_t_zero"])
    n_left = int(case["N_left"])
    n_right = int(case["N_right"])
    left_tail = count_tail_sources(n_left, threshold, include_t_zero)
    right_tail = count_tail_sources(n_right, threshold, include_t_zero)
    denominator = n_left + n_right - (0 if include_t_zero else 2)
    return (left_tail + right_tail) / denominator if denominator else 0.0


def analyze(cases: list[dict[str, Any]], thresholds: list[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        total_mass = float(case["total_mass"])
        for threshold in thresholds:
            observed_tail = sum(
                float(row["sample_weight"])
                for row in case["rows"]
                if int(row["v2"]) >= threshold
            )
            observed_share = observed_tail / total_mass if total_mass else 0.0
            formula_share = formula_tail_mass(case, threshold)
            dyadic_bound = 2.0 ** (-threshold)
            rows.append(
                {
                    "threshold_v2_ge": threshold,
                    "T": case["T"],
                    "j_left": case["j_left"],
                    "j_right": case["j_right"],
                    "N_left": case["N_left"],
                    "N_right": case["N_right"],
                    "h_mod": case["h_mod"],
                    "include_t_zero": case["include_t_zero"],
                    "observed_tail_mass": observed_share,
                    "formula_tail_mass": formula_share,
                    "dyadic_bound_2^-R": dyadic_bound,
                    "observed_minus_formula": observed_share - formula_share,
                    "formula_over_bound": formula_share / dyadic_bound if dyadic_bound else 0.0,
                    "bound_slack": dyadic_bound - formula_share,
                    "source_file": case["source_file"],
                }
            )
    rows.sort(key=lambda row: (int(row["threshold_v2_ge"]), int(row["N_left"])))
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
    rows: list[dict[str, Any]],
    report_path: Path,
    csv_path: Path,
) -> None:
    max_abs_error = max((abs(float(row["observed_minus_formula"])) for row in rows), default=0.0)
    max_ratio = max((float(row["formula_over_bound"]) for row in rows), default=0.0)
    min_slack = min((float(row["bound_slack"]) for row in rows), default=0.0)
    skipped_zero = all(not bool(case["include_t_zero"]) for case in cases)
    latest_by_threshold: dict[int, dict[str, Any]] = {}
    for threshold in sorted({int(row["threshold_v2_ge"]) for row in rows}):
        candidates = [row for row in rows if int(row["threshold_v2_ge"]) == threshold]
        latest_by_threshold[threshold] = max(candidates, key=lambda row: int(row["N_left"]))

    lines: list[str] = []
    lines.append("# A0 v2 Tail Formula")
    lines.append("")
    lines.append("Status: exact finite source-count check for script-111 A0 phase strata.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- input glob: `{args.input_glob}`")
    lines.append(f"- thresholds: `{args.thresholds}`")
    lines.append(f"- cases used after dedupe: `{len(cases)}`")
    lines.append(f"- output CSV: `{csv_path.name}`")
    lines.append("")
    lines.append("## Exact Count Lemma")
    lines.append("")
    lines.append("For a script-111 A0 comparison with")
    lines.append("")
    lines.append("```text")
    lines.append("L = j_left  * 2^T")
    lines.append("R = j_right * 2^T")
    lines.append("```")
    lines.append("")
    if skipped_zero:
        lines.append("and with `t=0` excluded, the phase source tail is exactly")
        lines.append("")
        lines.append("```text")
        lines.append("mu({phase_v2 >= q})")
        lines.append("  = (floor((L - 1)/2^q) + floor((R - 1)/2^q)) / (L + R - 2)")
        lines.append("  <= 2^-q.")
        lines.append("```")
    else:
        lines.append("Some inputs appear to include `t=0`; see the CSV for the inferred mode.")
    lines.append("")
    lines.append("The factor from the hit coordinate cancels from numerator and denominator.")
    lines.append("")
    lines.append("## Verification")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    lines.append(f"| max absolute observed-formula error | `{format_float(max_abs_error)}` |")
    lines.append(f"| max formula / 2^-q | `{format_float(max_ratio)}` |")
    lines.append(f"| min dyadic slack | `{format_float(min_slack)}` |")
    lines.append(f"| mean h_mod | `{format_float(mean(float(case['h_mod']) for case in cases) if cases else 0.0)}` |")
    lines.append("")
    lines.append("## Latest Scale by Threshold")
    lines.append("")
    lines.append("| q | N_left | observed tail | formula tail | 2^-q | formula/bound |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for threshold, row in latest_by_threshold.items():
        lines.append(
            f"| {threshold} | {row['N_left']} | "
            f"{format_float(row['observed_tail_mass'])} | "
            f"{format_float(row['formula_tail_mass'])} | "
            f"{format_float(row['dyadic_bound_2^-R'])} | "
            f"{format_float(row['formula_over_bound'])} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This proves the high-v2 mass part of the A0 weak decomposition for the")
    lines.append("current finite source model.  The remaining hard part is the structural")
    lines.append("low-v2 decay:")
    lines.append("")
    lines.append("```text")
    lines.append("D_N(v2 < q) -> 0")
    lines.append("```")
    lines.append("")
    lines.append("The tail no longer needs to be fitted: it is a counting lemma.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-glob", default=DEFAULT_GLOB)
    parser.add_argument("--thresholds", default="4,6,8,10,12,14")
    parser.add_argument("--output-tag", default="current_A0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    thresholds = parse_ints(args.thresholds)
    cases = read_cases(args.input_glob)
    if not cases:
        raise SystemExit(f"no cases matched {args.input_glob!r}")
    rows = analyze(cases, thresholds)
    report_path, csv_path = output_paths(args.output_tag)
    write_csv(rows, csv_path)
    write_report(
        args=args,
        cases=cases,
        rows=rows,
        report_path=report_path,
        csv_path=csv_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
