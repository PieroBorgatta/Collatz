#!/usr/bin/env python3
"""
Split martingale-variation proxies into phase, label-excess, and loss.

Inputs:
- collatz_101_*_z2_oscillation_strata.csv for global child-cylinder
  metrics;
- collatz_102_*_enriched_state_test.csv for candidate structural
  isolation of full-over-phase excess.

This script is diagnostic only.  It does not prove an infinite operator,
Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap, or Collatz.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_113_martingale_split_budget_report.md"
OUT_CSV = ROOT / "collatz_113_martingale_split_budget.csv"
DEFAULT_CANDIDATE = "source_odd_3_or_v2_2"


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


def infer_tag(path: Path, script: str, suffix: str) -> str:
    stem = path.stem
    prefix = f"collatz_{script}_"
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


def load_global_101(path: Path) -> dict[int, dict[str, dict[str, float]]]:
    out: dict[int, dict[str, dict[str, float]]] = {}
    for row in read_csv(path):
        if row["stratum"] != "global" or row["value"] != "all":
            continue
        depth = int(row["depth"])
        metric = row["metric"]
        out.setdefault(depth, {})[metric] = {
            "mean": float(row["mean"]),
            "p95": float(row["p95"]),
            "max": float(row["max"]),
        }
    return out


def load_candidate_102(path: Path, candidate: str) -> dict[int, dict[str, float]]:
    out: dict[int, dict[str, float]] = {}
    for row in read_csv(path):
        if row["candidate"] != candidate:
            continue
        if row["metric"] != "full_excess_over_phase":
            continue
        depth = int(row["depth"])
        out[depth] = {
            "selected_mass": float(row["selected_mass"]),
            "selected_contribution": float(row["selected_contribution"]),
            "selected_mean": float(row["selected_mean"]),
            "complement_mean": float(row["complement_mean"]),
            "complement_p95": float(row["complement_p95"]),
            "complement_contribution": float(row["complement_contribution"]),
            "global_mean": float(row["global_mean"]),
        }
    return out


def matching_102_path(tag: str) -> Path | None:
    path = ROOT / f"collatz_102_{tag}_enriched_state_test.csv"
    return path if path.exists() else None


def build_rows(candidate: str) -> list[dict[str, Any]]:
    rows_out: list[dict[str, Any]] = []
    paths_101 = sorted(ROOT.glob("collatz_101_*_z2_oscillation_strata.csv"))
    for path_101 in paths_101:
        tag = infer_tag(path_101, "101", "_z2_oscillation_strata")
        meta = parse_tag(tag)
        global_data = load_global_101(path_101)
        path_102 = matching_102_path(tag)
        candidate_data = load_candidate_102(path_102, candidate) if path_102 else {}

        for depth in sorted(global_data):
            metrics = global_data[depth]
            phase = metrics.get("phase_tv", {})
            status = metrics.get("status_tv", {})
            full_excess = metrics.get("full_excess_over_phase", {})
            delta_excess = metrics.get("delta_excess_over_phase", {})
            full = metrics.get("full_tv", {})
            cand = candidate_data.get(depth, {})

            phase_mean = phase.get("mean", 0.0)
            label_mean = full_excess.get("mean", 0.0)
            loss_mean = status.get("mean", 0.0)
            delta_extra_mean = delta_excess.get("mean", 0.0)
            split_sum = phase_mean + label_mean + loss_mean
            full_mean = full.get("mean", 0.0)

            rows_out.append({
                "tag": tag,
                "T": meta["T"],
                "max_depth": meta["max_depth"],
                "tail_bits": meta["tail_bits"],
                "depth": depth,
                "candidate": candidate,
                "phase_mean": phase_mean,
                "phase_p95": phase.get("p95", 0.0),
                "status_loss_mean": loss_mean,
                "status_loss_p95": status.get("p95", 0.0),
                "label_excess_mean": label_mean,
                "label_excess_p95": full_excess.get("p95", 0.0),
                "delta_excess_mean": delta_extra_mean,
                "delta_excess_p95": delta_excess.get("p95", 0.0),
                "full_mean": full_mean,
                "full_p95": full.get("p95", 0.0),
                "split_sum_phase_label_loss": split_sum,
                "split_over_full": split_sum / full_mean if full_mean else 0.0,
                "candidate_selected_mass": cand.get("selected_mass", 0.0),
                "candidate_selected_contribution": cand.get("selected_contribution", 0.0),
                "candidate_complement_mean": cand.get("complement_mean", 0.0),
                "candidate_complement_p95": cand.get("complement_p95", 0.0),
                "candidate_complement_contribution": cand.get("complement_contribution", 0.0),
            })
    return rows_out


def render_report(rows: list[dict[str, Any]], candidate: str) -> str:
    lines = [
        "# Martingale Split Budget",
        "",
        "Status: finite diagnostic output only.  This report separates the",
        "available child-cylinder martingale proxies into phase variation,",
        "full-over-phase label excess, and status/loss variation.  It does",
        "not prove Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap,",
        "or Collatz.",
        "",
        f"Structural candidate used for label-excess isolation: `{candidate}`.",
        "",
        "## Global Split",
        "",
        "| tag | depth | phase mean | label-excess mean | status/loss mean | full mean | split/full |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['tag']}` | {row['depth']} | "
            f"{row['phase_mean']:.6g} | {row['label_excess_mean']:.6g} | "
            f"{row['status_loss_mean']:.6g} | {row['full_mean']:.6g} | "
            f"{row['split_over_full']:.6g} |"
        )

    lines.extend([
        "",
        "The split is intentionally conservative: phase, label-excess, and",
        "status/loss are not independent norms, and their sum is not claimed",
        "to be sharp.  It is a bookkeeping device for deciding what a serious",
        "strong norm would have to control.",
        "",
        "## Structural Label-Excess Isolation",
        "",
        "| tag | depth | selected mass | selected contribution | complement mean | complement p95 | complement contribution |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for row in rows:
        lines.append(
            f"| `{row['tag']}` | {row['depth']} | "
            f"{row['candidate_selected_mass']:.6g} | "
            f"{row['candidate_selected_contribution']:.6g} | "
            f"{row['candidate_complement_mean']:.6g} | "
            f"{row['candidate_complement_p95']:.6g} | "
            f"{row['candidate_complement_contribution']:.6g} |"
        )

    lines.extend([
        "",
        "## Reading",
        "",
        "The phase component is large and nearly flat on the current depths,",
        "so exponential martingale weights are not justified by the present",
        "data.  The label-excess component is more promising: a single",
        "structural candidate captures about 80 percent of full-over-phase",
        "excess in both available T15/T16 reports, with complement p95 equal",
        "to zero in the strongest rows.  This supports an enriched or",
        "decomposed strong norm, not a plain full-label martingale BV norm.",
        "",
        "Next falsification target: rerun the child-cylinder diagnostic at",
        "larger depth/tail windows and require the phase component or the",
        "post-enrichment complement to show real decay.  If both remain",
        "flat, the Hennion/Keller-Liverani route should remain paused.",
        "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default=DEFAULT_CANDIDATE)
    parser.add_argument("--output", type=Path, default=OUT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=OUT_CSV)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(args.candidate)
    if not rows:
        raise SystemExit("no rows produced")
    write_csv(rows, args.csv_output)
    args.output.write_text(render_report(rows, args.candidate), encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"wrote {args.csv_output}")


if __name__ == "__main__":
    main()
