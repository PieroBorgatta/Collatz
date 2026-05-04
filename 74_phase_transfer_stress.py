"""
74_phase_transfer_stress.py

Scenario-level stress test for the refined phase transfer operator.

This script preserves the key result of 73_phase_transfer_operator.py across
three samples in one CSV:

  - canonical dense_b8_t255 loaded from collatz_62_*;
  - wide dense_b8_t1023 regenerated on the fly;
  - deep powers_b16_t65535 regenerated on the fly.

The tested phase states are deliberately small:

    (odd_bits, hit_bits) in {(1,2), (2,2), (4,2), (8,2), (4,3), (8,3)}

The central question:

    does hit_index mod 4 or mod 8 keep rho < 1 across samples?
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_74_phase_transfer_stress.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_int_csv(path: Path) -> list[dict[str, int]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def generate_critical(*, b_max: int, t_max: int, t_mode: str, max_steps: int):
    critical = load_module("62_critical_return_map.py", "critical_return_map")
    args = argparse.Namespace(
        k_min=10,
        k_max=24,
        b_min=1,
        b_max=b_max,
        t_max=t_max,
        t_mode=t_mode,
        max_steps=max_steps,
        target_k=12,
        target_cycle=2,
        target_b=1,
    )
    return critical.analyze(args)


def main() -> None:
    phase = load_module("73_phase_transfer_operator.py", "phase_transfer_operator")
    configs = [(1, 2), (2, 2), (4, 2), (8, 2), (4, 3), (8, 3)]
    scenarios = [
        (
            "canonical_dense_b8_t255",
            read_int_csv(ROOT / "collatz_62_critical_returns.csv"),
            read_int_csv(ROOT / "collatz_62_critical_terminals.csv"),
        ),
        (
            "wide_dense_b8_t1023",
            *generate_critical(b_max=8, t_max=1023, t_mode="dense", max_steps=5000),
        ),
        (
            "deep_powers_b16_t65535",
            *generate_critical(b_max=16, t_max=65535, t_mode="powers", max_steps=5000),
        ),
    ]

    rows = []
    print("=" * 118)
    print("  Phase transfer stress")
    print("=" * 118)
    print(f"  {'scenario':<28} {'odd':>4} {'hit':>4} {'states':>8} {'rho':>14} {'verdict':>12}")
    for label, returns, terminals in scenarios:
        for odd_bits, hit_bits in configs:
            summary, _ = phase.run_config(
                returns,
                terminals,
                odd_bits=odd_bits,
                hit_bits=hit_bits,
                v2_cap=32,
                s=1.0,
            )
            row = {"scenario": label}
            row.update(summary)
            rows.append(row)
            verdict = "subcritical" if summary["rho"] < 1.0 else "supercritical"
            print(
                f"  {label:<28} {odd_bits:>4} {hit_bits:>4} "
                f"{summary['state_count']:>8} {summary['rho']:>14.6g} {verdict:>12}"
            )

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")


if __name__ == "__main__":
    main()
