"""
79_boundary_tail_scaling.py

Scaling of the high-bit tail bound with increasing lift count j.

78_tail_row_certificate_probe.py revealed that the worst tail row is a
boundary-layer state with v2(t) approximately equal to T. This script measures
how the tail row bound scales when we increase j_count, separating:

  - all states;
  - bulk states:     v2(t) < T;
  - boundary states: v2(t) >= T.

The intended proof shape becomes:

    M = CORE + TAIL_bulk + TAIL_boundary

where the bulk tail has a small uniform row norm, while the boundary layer
must be controlled by a separate valuation-counting lemma.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_79_boundary_tail_scaling.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def analyze(T: int, j_count: int, args: argparse.Namespace) -> dict:
    probe = load_module("78_tail_row_certificate_probe.py", "tail_probe")
    ctx = probe.setup()
    local_args = argparse.Namespace(
        T=str(T),
        j_count=j_count,
        odd_bits=args.odd_bits,
        hit_bits=args.hit_bits,
        v2_cap=args.v2_cap,
        max_steps=args.max_steps,
    )
    state_rows, group_rows = probe.analyze_T(ctx, local_args, T)

    all_max = max((row["tail_row_sum"] for row in state_rows), default=0.0)
    bulk_rows = [row for row in state_rows if int(row["state"].split("|")[0].split("=")[1]) < T]
    boundary_rows = [row for row in state_rows if int(row["state"].split("|")[0].split("=")[1]) >= T]
    bulk_max = max((row["tail_row_sum"] for row in bulk_rows), default=0.0)
    boundary_max = max((row["tail_row_sum"] for row in boundary_rows), default=0.0)

    top_all = max(state_rows, key=lambda row: row["tail_row_sum"])
    top_bulk = max(bulk_rows, key=lambda row: row["tail_row_sum"]) if bulk_rows else None
    top_boundary = max(boundary_rows, key=lambda row: row["tail_row_sum"]) if boundary_rows else None

    total_sources = sum(row["source_count"] for row in state_rows)
    boundary_sources = sum(row["source_count"] for row in boundary_rows)
    tail_weight_total = sum(row["tail_weight"] for row in state_rows)
    tail_weight_boundary = sum(row["tail_weight"] for row in boundary_rows)

    return {
        "T": T,
        "j_count": j_count,
        "state_count": len(state_rows),
        "all_max_tail_row": all_max,
        "bulk_max_tail_row": bulk_max,
        "boundary_max_tail_row": boundary_max,
        "top_all_state": top_all["state"],
        "top_all_source_count": top_all["source_count"],
        "top_all_tail_weight": top_all["tail_weight"],
        "top_bulk_state": top_bulk["state"] if top_bulk else "",
        "top_bulk_source_count": top_bulk["source_count"] if top_bulk else 0,
        "top_bulk_tail_weight": top_bulk["tail_weight"] if top_bulk else 0.0,
        "top_boundary_state": top_boundary["state"] if top_boundary else "",
        "top_boundary_source_count": top_boundary["source_count"] if top_boundary else 0,
        "top_boundary_tail_weight": top_boundary["tail_weight"] if top_boundary else 0.0,
        "total_sources": total_sources,
        "boundary_sources": boundary_sources,
        "boundary_source_fraction": boundary_sources / total_sources if total_sources else 0.0,
        "tail_weight_total": tail_weight_total,
        "tail_weight_boundary": tail_weight_boundary,
        "boundary_tail_weight_fraction": tail_weight_boundary / tail_weight_total if tail_weight_total else 0.0,
        "group_count": len(group_rows),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaling della boundary layer tail.")
    parser.add_argument("--T", type=int, default=10)
    parser.add_argument("--j-counts", default="8,16,32,64")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    print("=" * 118)
    print("  Boundary tail scaling")
    print("=" * 118)
    print(f"  T={args.T}, odd_bits={args.odd_bits}, hit_bits={args.hit_bits}")
    print(f"  {'j':>5} {'all max':>10} {'bulk max':>10} {'boundary':>10} {'boundary src%':>14} {'top state':<22}")
    for j_count in parse_csv_ints(args.j_counts):
        row = analyze(args.T, j_count, args)
        rows.append(row)
        print(
            f"  {j_count:>5} {row['all_max_tail_row']:>10.6g} "
            f"{row['bulk_max_tail_row']:>10.6g} "
            f"{row['boundary_max_tail_row']:>10.6g} "
            f"{row['boundary_source_fraction']:>14.6g} "
            f"{row['top_all_state']:<22}"
        )

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")


if __name__ == "__main__":
    main()
