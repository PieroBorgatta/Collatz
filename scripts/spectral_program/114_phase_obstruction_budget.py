#!/usr/bin/env python3
"""
Phase obstruction budget from script-101 child-cylinder strata.

The previous split budget identified phase martingale variation as the
main obstruction.  This diagnostic asks whether that phase obstruction is
localized in a small structural component or spread across broad source
classes.

This is finite diagnostic output only.  It does not prove or disprove an
infinite operator, Lasota-Yorke, Hennion, Keller-Liverani, a spectral
gap, or Collatz.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_114_phase_obstruction_budget_report.md"
OUT_CSV = ROOT / "collatz_114_phase_obstruction_budget.csv"
STRUCTURAL_STRATA = {
    "source_v2",
    "source_odd",
    "source_v2_odd",
    "r_v2",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def infer_tag(path: Path) -> str:
    stem = path.stem
    prefix = "collatz_101_"
    suffix = "_z2_oscillation_strata"
    if stem.startswith(prefix) and stem.endswith(suffix):
        return stem[len(prefix) : -len(suffix)]
    return stem


def parse_tag(tag: str) -> dict[str, str]:
    out = {"T": "unknown", "max_depth": "unknown", "tail_bits": "unknown"}
    m = re.search(r"T(\d+)", tag)
    if m:
        out["T"] = m.group(1)
    m = re.search(r"d(\d+)", tag)
    if m:
        out["max_depth"] = m.group(1)
    m = re.search(r"tail(\d+)", tag)
    if m:
        out["tail_bits"] = m.group(1)
    return out


def build_rows() -> list[dict[str, Any]]:
    rows_out: list[dict[str, Any]] = []
    for path in sorted(ROOT.glob("collatz_101_*_z2_oscillation_strata.csv")):
        tag = infer_tag(path)
        meta = parse_tag(tag)
        rows = read_csv(path)
        globals_by_depth: dict[int, dict[str, float]] = {}
        for row in rows:
            if row["metric"] == "phase_tv" and row["stratum"] == "global":
                globals_by_depth[int(row["depth"])] = {
                    "mean": float(row["mean"]),
                    "p95": float(row["p95"]),
                    "max": float(row["max"]),
                }
        for row in rows:
            if row["metric"] != "phase_tv":
                continue
            if row["stratum"] not in STRUCTURAL_STRATA:
                continue
            depth = int(row["depth"])
            glob = globals_by_depth[depth]
            mass = float(row["mass_fraction"])
            selected_mean = float(row["mean"])
            selected_contribution = float(row["contribution_fraction"])
            complement_mass = max(0.0, 1.0 - mass)
            if complement_mass:
                complement_mean = (
                    glob["mean"] - mass * selected_mean
                ) / complement_mass
            else:
                complement_mean = 0.0
            rows_out.append({
                "tag": tag,
                "T": meta["T"],
                "max_depth": meta["max_depth"],
                "tail_bits": meta["tail_bits"],
                "depth": depth,
                "stratum": row["stratum"],
                "value": row["value"],
                "selected_mass": mass,
                "selected_mean": selected_mean,
                "selected_p95": float(row["p95"]),
                "selected_max": float(row["max"]),
                "selected_contribution": selected_contribution,
                "complement_mass": complement_mass,
                "complement_mean": complement_mean,
                "global_mean": glob["mean"],
                "global_p95": glob["p95"],
                "global_max": glob["max"],
                "mean_reduction_if_removed": glob["mean"] - complement_mean,
            })
    return sorted(
        rows_out,
        key=lambda row: (row["tag"], row["depth"], row["selected_contribution"]),
        reverse=True,
    )


def render_report(rows: list[dict[str, Any]], limit_per_depth: int) -> str:
    lines = [
        "# Phase Obstruction Budget",
        "",
        "Status: finite diagnostic output only.  This report asks whether",
        "the phase martingale obstruction is localized in small structural",
        "source classes.  It does not prove Lasota-Yorke, Hennion,",
        "Keller-Liverani, a spectral gap, or Collatz.",
        "",
        "## Top Phase-TV Structural Contributions",
        "",
        "| tag | depth | stratum | value | mass | selected mean | contribution | complement mean | global mean |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((row["tag"], int(row["depth"])), []).append(row)
    for key in sorted(grouped):
        ranked = sorted(
            grouped[key],
            key=lambda row: row["selected_contribution"],
            reverse=True,
        )[:limit_per_depth]
        for row in ranked:
            lines.append(
                f"| `{row['tag']}` | {row['depth']} | `{row['stratum']}` | "
                f"`{row['value']}` | {row['selected_mass']:.6g} | "
                f"{row['selected_mean']:.6g} | "
                f"{row['selected_contribution']:.6g} | "
                f"{row['complement_mean']:.6g} | "
                f"{row['global_mean']:.6g} |"
            )

    lines.extend([
        "",
        "## Reading",
        "",
        "The phase obstruction is not a small exceptional set.  The strongest",
        "single structural contributors usually have mass about `1/2` and",
        "contribution about `0.66--0.69`; after removing them, the complement",
        "mean is still around `0.025--0.028`.  This makes a finite-rank",
        "exceptional correction less plausible for the phase term than for",
        "the label-excess term.",
        "",
        "Consequently, the Banach-pair route needs a structural phase theorem",
        "or a different operator/quotient.  Merely isolating a bad labelled",
        "component does not solve the phase martingale obstruction.",
        "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit-per-depth", type=int, default=4)
    parser.add_argument("--output", type=Path, default=OUT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=OUT_CSV)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows()
    if not rows:
        raise SystemExit("no rows produced")
    write_csv(rows, args.csv_output)
    args.output.write_text(render_report(rows, args.limit_per_depth), encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"wrote {args.csv_output}")


if __name__ == "__main__":
    main()
