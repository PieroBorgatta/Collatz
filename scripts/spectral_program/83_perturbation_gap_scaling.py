"""
83_perturbation_gap_scaling.py

Measure the perturbative gap

    gap(T, j) = rho(FULL_{T,j}) - rho(CORE_{T,j})

across a grid of (T, j_count) values.

Why this script.

    77_high_bit_tail_bound.py decomposes the critical return operator as

        FULL = CORE + TAIL

    and reports rho(FULL), rho(CORE), ||TAIL||_inf for a single j_count.
    82_boundary_scc_spectral_scaling.py shows that rho(FULL) plateaus near
    0.030-0.031 as T and j grow.

    The decisive question for the perturbation-bound strategy of the lemma
    (collatz_shadowing_lemma_v1.md) is not what rho(FULL) does in isolation
    but what the gap rho(FULL) - rho(CORE) does as we scale T and j.

    If gap(T, j) stays uniformly bounded (and small), then the inequality

        rho(FULL) <= rho(CORE) + perturbation

    is asymptotically tight: the high-bit tail contributes a uniformly
    controllable correction. That is the form the lemma needs.

    If gap(T, j) grows with T or j, the current core/tail split is the wrong
    decomposition: CORE is shrinking faster than FULL and the perturbation
    bound is hopeless.

The script reuses 77.analyze_T as the per-cell engine. For each (T, j) it
records the full row plus the gap and the perturbative bound, and writes a
single CSV plus a compact console table.
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_83_perturbation_gap_scaling.csv"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaling del gap perturbativo CORE vs FULL.")
    parser.add_argument("--T", default="6,8,10,12")
    parser.add_argument("--j-counts", default="8,16,32,64")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--keep-rows", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")

    Ts = parse_csv_ints(args.T)
    js = parse_csv_ints(args.j_counts)

    rows = []
    print("=" * 132)
    print("  Perturbation gap scaling: rho(FULL) - rho(CORE)")
    print("=" * 132)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, v2_cap={args.v2_cap}")
    header = (
        f"  {'T':>3} {'j':>4} {'states':>7} {'stable%':>8} "
        f"{'rho_full':>11} {'rho_core':>11} {'gap':>11} "
        f"{'tail_inf':>11} {'bound':>11} {'tail_w%':>9}"
    )
    print(header)
    print("-" * len(header))

    for T in Ts:
        for j_count in js:
            cell_args = argparse.Namespace(
                T=str(T),
                j_count=j_count,
                odd_bits=args.odd_bits,
                hit_bits=args.hit_bits,
                v2_cap=args.v2_cap,
                max_steps=args.max_steps,
                keep_rows=args.keep_rows,
            )
            summary, _ = tail_mod.analyze_T(cell_args, T)
            gap = summary["rho_full"] - summary["rho_core"]
            row = {
                "T": T,
                "j_count": j_count,
                "state_count": summary["state_count"],
                "stable_fraction": summary["stable_fraction"],
                "rho_full": summary["rho_full"],
                "rho_core": summary["rho_core"],
                "rho_tail": summary["rho_tail"],
                "gap_full_minus_core": gap,
                "norm_inf_tail": summary["norm_inf_tail"],
                "rho_core_plus_tail_inf": summary["rho_core_plus_tail_inf"],
                "tail_weight_fraction": summary["tail_weight_fraction"],
                "tail_event_fraction": summary["tail_event_fraction"],
                "terminal_fraction": summary["terminal_fraction"],
            }
            rows.append(row)
            print(
                f"  {T:>3} {j_count:>4} {summary['state_count']:>7} "
                f"{summary['stable_fraction']:>8.4f} "
                f"{summary['rho_full']:>11.6g} {summary['rho_core']:>11.6g} "
                f"{gap:>11.6g} {summary['norm_inf_tail']:>11.6g} "
                f"{summary['rho_core_plus_tail_inf']:>11.6g} "
                f"{summary['tail_weight_fraction']:>9.4f}"
            )

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")

    print("\n  Trend of gap = rho(FULL) - rho(CORE) per j (rows = T):")
    js_sorted = sorted(set(r["j_count"] for r in rows))
    Ts_sorted = sorted(set(r["T"] for r in rows))
    head = "    T \\ j " + "  ".join(f"{j:>10}" for j in js_sorted)
    print(head)
    for T in Ts_sorted:
        cells = []
        for j in js_sorted:
            match = next((r for r in rows if r["T"] == T and r["j_count"] == j), None)
            cells.append(f"{match['gap_full_minus_core']:>10.6g}" if match else " " * 10)
        print(f"    {T:>5} " + "  ".join(cells))


if __name__ == "__main__":
    main()
