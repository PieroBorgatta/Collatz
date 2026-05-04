"""
82_boundary_scc_spectral_scaling.py

Scale the weighted SCC spectrum touching the boundary layer across T and
j_count.

The previous script found, for T=10 and j_count=64:

    rho(full SCC touching boundary) ~= 0.03026
    rho(tail SCC touching boundary) ~= 0.01691

This script checks whether that value is stable as we vary:

    T       quotient depth in t mod 2^T
    j_count number of high-bit lifts t = r + j*2^T
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_82_boundary_scc_spectral_scaling.csv"


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


def top_boundary_component(rows: list[dict], graph: str) -> dict | None:
    candidates = [r for r in rows if r["graph"] == graph and r["boundary_count"] > 0]
    if not candidates:
        return None
    return max(candidates, key=lambda r: (r["rho"], r["boundary_count"], r["size"]))


def analyze_one(T: int, j_count: int, args: argparse.Namespace) -> dict:
    scc = load_module("81_boundary_scc_spectral.py", "boundary_scc_spectral")
    local_args = argparse.Namespace(
        T=T,
        j_count=j_count,
        odd_bits=args.odd_bits,
        hit_bits=args.hit_bits,
        v2_cap=args.v2_cap,
        max_steps=args.max_steps,
    )
    rows = scc.analyze(T, local_args)
    full = top_boundary_component(rows, "full")
    tail = top_boundary_component(rows, "tail")
    core = top_boundary_component(rows, "core")
    largest_any = max(rows, key=lambda r: r["rho"]) if rows else None

    return {
        "T": T,
        "j_count": j_count,
        "odd_bits": args.odd_bits,
        "hit_bits": args.hit_bits,
        "full_boundary_rho": full["rho"] if full else 0.0,
        "full_boundary_size": full["size"] if full else 0,
        "full_boundary_count": full["boundary_count"] if full else 0,
        "full_boundary_max_row": full["max_internal_row_sum"] if full else 0.0,
        "tail_boundary_rho": tail["rho"] if tail else 0.0,
        "tail_boundary_size": tail["size"] if tail else 0,
        "tail_boundary_count": tail["boundary_count"] if tail else 0,
        "tail_boundary_max_row": tail["max_internal_row_sum"] if tail else 0.0,
        "core_boundary_rho": core["rho"] if core else 0.0,
        "largest_component_graph": largest_any["graph"] if largest_any else "",
        "largest_component_rho": largest_any["rho"] if largest_any else 0.0,
        "largest_component_size": largest_any["size"] if largest_any else 0,
        "largest_component_boundary_count": largest_any["boundary_count"] if largest_any else 0,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaling spettro SCC boundary.")
    parser.add_argument("--T", default="8,10,12")
    parser.add_argument("--j-counts", default="16,32")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    print("=" * 124)
    print("  Boundary SCC spectral scaling")
    print("=" * 124)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}")
    print(f"  {'T':>4} {'j':>5} {'rho full-bdy':>14} {'rho tail-bdy':>14} {'size':>7} {'bdy':>5} {'largest':>10}")
    for T in parse_csv_ints(args.T):
        for j_count in parse_csv_ints(args.j_counts):
            row = analyze_one(T, j_count, args)
            rows.append(row)
            print(
                f"  {T:>4} {j_count:>5} "
                f"{row['full_boundary_rho']:>14.6g} "
                f"{row['tail_boundary_rho']:>14.6g} "
                f"{row['full_boundary_size']:>7} "
                f"{row['full_boundary_count']:>5} "
                f"{row['largest_component_rho']:>10.6g}"
            )

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")


if __name__ == "__main__":
    main()
