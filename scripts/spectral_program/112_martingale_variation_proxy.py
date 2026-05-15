#!/usr/bin/env python3
"""
Martingale-variation proxy from existing Z2 child-cylinder diagnostics.

Input CSVs are produced by 100_z2_cylinder_oscillation.py.  For a binary
parent cylinder with child distributions p0 and p1, the L1 distance from
each child to the parent average is:

    ||p_child - (p0+p1)/2||_1 averaged over children = TV(p0,p1).

Thus the mean child-TV at depth n is the finite proxy for the nth
martingale increment of the observed kernel distribution.  This script
does not prove an infinite operator, a Lasota-Yorke inequality, Hennion,
Keller-Liverani, a spectral gap, or Collatz.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_GLOB = "collatz_100_*_z2_cylinder_oscillation.csv"
OUT_REPORT = ROOT / "collatz_112_martingale_variation_proxy_report.md"
OUT_CSV = ROOT / "collatz_112_martingale_variation_proxy.csv"


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
    prefix = "collatz_100_"
    suffix = "_z2_cylinder_oscillation"
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


def parse_thetas(text: str) -> list[float]:
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def summarize_file(path: Path, theta_values: list[float]) -> list[dict[str, Any]]:
    tag = infer_tag(path)
    meta = parse_tag(tag)
    rows = read_csv(path)
    by_level: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        level = row["signature_level"]
        by_level.setdefault(level, []).append({
            "depth": int(row["depth"]),
            "mean_tv": float(row["mean_tv"]),
            "p95_tv": float(row["p95_tv"]),
            "p99_tv": float(row["p99_tv"]),
            "max_tv": float(row["max_tv"]),
            "samples": int(row["samples"]),
        })

    out: list[dict[str, Any]] = []
    for level, level_rows in sorted(by_level.items()):
        ordered = sorted(level_rows, key=lambda row: row["depth"])
        raw_mean_sum = sum(row["mean_tv"] for row in ordered)
        raw_p95_sum = sum(row["p95_tv"] for row in ordered)
        raw_max_sum = sum(row["max_tv"] for row in ordered)

        base = {
            "input": path.name,
            "tag": tag,
            "T": meta["T"],
            "max_depth": meta["max_depth"],
            "tail_bits": meta["tail_bits"],
            "signature_level": level,
            "depths": ",".join(str(row["depth"]) for row in ordered),
            "mean_tv_by_depth": ",".join(f"{row['mean_tv']:.12g}" for row in ordered),
            "p95_tv_by_depth": ",".join(f"{row['p95_tv']:.12g}" for row in ordered),
            "max_tv_by_depth": ",".join(f"{row['max_tv']:.12g}" for row in ordered),
            "raw_mean_partial_var": raw_mean_sum,
            "raw_p95_partial_var": raw_p95_sum,
            "raw_max_partial_var": raw_max_sum,
            "mean_last_over_first": (
                ordered[-1]["mean_tv"] / ordered[0]["mean_tv"]
                if ordered and ordered[0]["mean_tv"]
                else 0.0
            ),
        }
        out.append(dict(base, weight="none", weighted_mean_partial_var=raw_mean_sum))
        for theta in theta_values:
            weighted = sum((theta ** (-row["depth"])) * row["mean_tv"] for row in ordered)
            out.append(dict(
                base,
                weight=f"theta={theta:g}",
                weighted_mean_partial_var=weighted,
            ))
    return out


def render_report(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Martingale Variation Proxy",
        "",
        "Status: finite diagnostic output only.  This report estimates",
        "martingale-increment sizes from existing child-cylinder TV summaries.",
        "It does not prove an infinite operator, a Lasota-Yorke inequality,",
        "Hennion, Keller-Liverani, a spectral gap, or Collatz.",
        "",
        "For binary child distributions `p0,p1`, the mean child deviation",
        "from the parent average is `TV(p0,p1)`.  Therefore the `mean_tv`",
        "column from script `100` is the natural finite proxy for",
        "`||d_n K||_1` in the martingale-variation pair.",
        "",
        "## Partial Variation Table",
        "",
        "| input | level | weight | depths | mean TV by depth | raw mean sum | weighted mean sum | last/first |",
        "|---|---|---|---|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['input']}` | `{row['signature_level']}` | `{row['weight']}` | "
            f"`{row['depths']}` | `{row['mean_tv_by_depth']}` | "
            f"{row['raw_mean_partial_var']:.6g} | "
            f"{row['weighted_mean_partial_var']:.6g} | "
            f"{row['mean_last_over_first']:.6g} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "A useful martingale Banach pair needs summable increments after the",
        "chosen weights `a_n` are applied.  On the currently available",
        "finite windows, the full and delta mean increments do not yet show",
        "decay across depth; in several runs they increase.  The phase",
        "increments are only nearly flat/slightly decreasing on the tested",
        "windows, not remotely summable at these depths.  This is negative",
        "pressure on exponential weights `a_n = theta^{-n}` unless a later",
        "stratification, state enrichment, or retained-kernel reformulation",
        "changes the increment profile.",
        "",
        "The result is not a disproof: the available depths are shallow, the",
        "sample windows are finite, and the measured signature kernel is not",
        "yet proved to be `E_N U_ret,s I_N`.  It is, however, the right",
        "finite quantity to monitor before invoking Hennion or",
        "Keller-Liverani.",
        "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--glob", default=DEFAULT_GLOB)
    parser.add_argument("--theta", default="0.9,0.75,0.5")
    parser.add_argument("--output", type=Path, default=OUT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=OUT_CSV)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    theta_values = parse_thetas(args.theta)
    paths = sorted(ROOT.glob(args.glob))
    if not paths:
        raise SystemExit(f"no inputs matched {args.glob!r}")

    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(summarize_file(path, theta_values))

    write_csv(rows, args.csv_output)
    args.output.write_text(render_report(rows), encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"wrote {args.csv_output}")


if __name__ == "__main__":
    main()
