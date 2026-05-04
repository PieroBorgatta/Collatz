"""
70_delta_exception_stress.py

Stress test for the deep-return exception threshold discovered by
69_exception_pattern_miner.py.

In the original dense sample for the critical return map, the 31 atomic
exceptions isolated by the refinement loop were exactly:

    delta_t_bits <= -11.

This script reruns the critical return map on wider samples without
overwriting the canonical collatz_62_* files, then records how many deep
negative returns appear and how they scale with the sampled family.

Interpretation:
  - If deep exceptions grow at the same rate as all returns, the atomic
    subcritical result was just memorization.
  - If they remain rare, with bounded depth and stable residues, the proof
    target becomes precise: bound the deep-exception set and prove the
    remaining return operator is subcritical.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_SUMMARY = ROOT / "collatz_70_delta_exception_stress_summary.csv"
OUT_EXCEPTIONS = ROOT / "collatz_70_delta_exception_rows.csv"


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


def scenario_args(
    *,
    label: str,
    b_max: int,
    t_max: int,
    t_mode: str,
    max_steps: int,
    threshold: int,
) -> argparse.Namespace:
    return argparse.Namespace(
        label=label,
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
        threshold=threshold,
    )


def compact_counter(counter: Counter, limit: int = 12) -> str:
    return ",".join(f"{k}:{v}" for k, v in counter.most_common(limit))


def analyze_scenario(args: argparse.Namespace) -> tuple[dict, list[dict]]:
    critical = load_module("62_critical_return_map.py", "critical_return_map")
    return_rows, terminal_rows = critical.analyze(args)
    exceptions = [row for row in return_rows if row["delta_t_bits"] <= args.threshold]

    total_weight = sum(2.0 ** (-row["delta_t_bits"]) for row in return_rows)
    exception_weight = sum(2.0 ** (-row["delta_t_bits"]) for row in exceptions)
    delta_counter = Counter(row["delta_t_bits"] for row in return_rows)
    exception_delta_counter = Counter(row["delta_t_bits"] for row in exceptions)
    exception_source_counter = Counter(
        (row["source_k"], row["source_cycle_id"], row["source_b"])
        for row in exceptions
    )
    exception_hit_counter = Counter(row["hit_index"] for row in exceptions)
    exception_v2_counter = Counter(row["from_t_v2"] for row in exceptions)

    summary = {
        "label": args.label,
        "b_max": args.b_max,
        "t_mode": args.t_mode,
        "t_max": args.t_max,
        "max_steps": args.max_steps,
        "threshold": args.threshold,
        "returns": len(return_rows),
        "terminals": len(terminal_rows),
        "exceptions": len(exceptions),
        "exception_fraction": len(exceptions) / len(return_rows) if return_rows else 0.0,
        "min_delta_t_bits": min((row["delta_t_bits"] for row in return_rows), default=0),
        "max_delta_t_bits": max((row["delta_t_bits"] for row in return_rows), default=0),
        "total_weight_s1": total_weight,
        "exception_weight_s1": exception_weight,
        "exception_weight_fraction_s1": exception_weight / total_weight if total_weight else 0.0,
        "delta_distribution": compact_counter(delta_counter),
        "exception_delta_distribution": compact_counter(exception_delta_counter),
        "exception_source_distribution": compact_counter(exception_source_counter),
        "exception_hit_distribution": compact_counter(exception_hit_counter),
        "exception_from_t_v2_distribution": compact_counter(exception_v2_counter),
    }

    exception_rows = []
    for row in exceptions:
        out = {"label": args.label}
        out.update(row)
        exception_rows.append(out)
    return summary, exception_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stress test delle eccezioni delta_t_bits profonde.")
    parser.add_argument("--threshold", type=int, default=-11)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument(
        "--scenario",
        choices=["quick", "wide", "deep", "all"],
        default="all",
        help="quick=dense 255; wide=dense 1023; deep=powers 65535 with b<=16; all runs all three.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = []
    if args.scenario in ("quick", "all"):
        scenarios.append(scenario_args(
            label="dense_b8_t255",
            b_max=8,
            t_max=255,
            t_mode="dense",
            max_steps=args.max_steps,
            threshold=args.threshold,
        ))
    if args.scenario in ("wide", "all"):
        scenarios.append(scenario_args(
            label="dense_b8_t1023",
            b_max=8,
            t_max=1023,
            t_mode="dense",
            max_steps=args.max_steps,
            threshold=args.threshold,
        ))
    if args.scenario in ("deep", "all"):
        scenarios.append(scenario_args(
            label="powers_b16_t65535",
            b_max=16,
            t_max=65535,
            t_mode="powers",
            max_steps=args.max_steps,
            threshold=args.threshold,
        ))

    summaries = []
    all_exceptions = []
    print("=" * 116)
    print("  Delta exception stress test")
    print("=" * 116)
    for sc in scenarios:
        print(f"\n  Scenario: {sc.label}")
        summary, exception_rows = analyze_scenario(sc)
        summaries.append(summary)
        all_exceptions.extend(exception_rows)
        print(
            f"    returns={summary['returns']:,} terminals={summary['terminals']:,} "
            f"exceptions={summary['exceptions']:,} "
            f"frac={summary['exception_fraction']:.6f} "
            f"min_delta={summary['min_delta_t_bits']}"
        )
        print(f"    exception deltas: {summary['exception_delta_distribution']}")
        print(f"    exception sources: {summary['exception_source_distribution']}")

    write_csv(summaries, OUT_SUMMARY)
    write_csv(all_exceptions, OUT_EXCEPTIONS)
    print("\n  Output:")
    print(f"    {OUT_SUMMARY.name}")
    print(f"    {OUT_EXCEPTIONS.name}")


if __name__ == "__main__":
    main()
