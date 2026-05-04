"""
72_exception_congruence_miner.py

Mine modular predictors for deep critical-return exceptions.

This script reruns the wide dense scenario and, for each dominant phantom
source, searches congruence rules of the form

    source_t mod 2^m == r
    from_odd_mod_256 mod 2^m == r

that enrich the event

    delta_t_bits <= threshold.

This is a stricter question than 69_exception_pattern_miner.py: instead of
describing already-isolated atoms, it asks whether deep returns are predictable
from 2-adic residues inside a fixed source family.
"""

from __future__ import annotations

import argparse
import csv
import math
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_RULES = ROOT / "collatz_72_exception_congruence_rules.csv"
OUT_SOURCE_SUMMARY = ROOT / "collatz_72_exception_source_summary.csv"


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


def scenario_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        k_min=10,
        k_max=24,
        b_min=1,
        b_max=args.b_max,
        t_max=args.t_max,
        t_mode="dense",
        max_steps=args.max_steps,
        target_k=12,
        target_cycle=2,
        target_b=1,
    )


def source_key(row: dict[str, int]) -> tuple[int, int, int]:
    return row["source_k"], row["source_cycle_id"], row["source_b"]


def score_rule(pos: int, total: int, baseline: float) -> float:
    if total == 0 or pos == 0:
        return 0.0
    precision = pos / total
    lift = precision / baseline if baseline else 0.0
    # Prefer rules that are both enriched and not supported by a single row.
    return math.log2(1.0 + lift) * math.sqrt(pos)


def mine_rules(rows: list[dict[str, int]], threshold: int, min_pos: int) -> tuple[list[dict], list[dict]]:
    groups: dict[tuple[int, int, int], list[dict[str, int]]] = {}
    for row in rows:
        groups.setdefault(source_key(row), []).append(row)

    rule_rows = []
    summary_rows = []
    for key, group in sorted(groups.items()):
        positives = [row for row in group if row["delta_t_bits"] <= threshold]
        if len(positives) < min_pos:
            continue
        baseline = len(positives) / len(group)
        min_delta = min(row["delta_t_bits"] for row in positives)
        summary_rows.append({
            "source_k": key[0],
            "source_cycle_id": key[1],
            "source_b": key[2],
            "rows": len(group),
            "exceptions": len(positives),
            "baseline_exception_rate": baseline,
            "min_delta_t_bits": min_delta,
        })

        candidates = []
        for col, max_m in (("source_t", 12), ("from_odd_mod_256", 8), ("from_t_v2", 6), ("hit_index", 5)):
            for m in range(1, max_m + 1):
                mod = 1 << m
                residues = sorted({row[col] % mod for row in group})
                for residue in residues:
                    covered = [row for row in group if row[col] % mod == residue]
                    pos = sum(1 for row in covered if row["delta_t_bits"] <= threshold)
                    if pos < min_pos:
                        continue
                    total = len(covered)
                    precision = pos / total
                    lift = precision / baseline
                    candidates.append({
                        "source_k": key[0],
                        "source_cycle_id": key[1],
                        "source_b": key[2],
                        "rule": f"{col} mod {mod} == {residue}",
                        "positive_rows": pos,
                        "covered_rows": total,
                        "precision": precision,
                        "baseline": baseline,
                        "lift": lift,
                        "min_delta_t_bits": min(row["delta_t_bits"] for row in covered if row["delta_t_bits"] <= threshold),
                        "score": score_rule(pos, total, baseline),
                    })
        candidates.sort(key=lambda r: (r["score"], r["positive_rows"], r["precision"]), reverse=True)
        rule_rows.extend(candidates[:20])

    summary_rows.sort(key=lambda r: (-r["exceptions"], r["source_k"], r["source_b"]))
    rule_rows.sort(key=lambda r: (r["source_k"], r["source_cycle_id"], r["source_b"], -r["score"]))
    return summary_rows, rule_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mina congruenze modulari per edge profondi.")
    parser.add_argument("--threshold", type=int, default=-11)
    parser.add_argument("--t-max", type=int, default=1023)
    parser.add_argument("--b-max", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--min-pos", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    critical = load_module("62_critical_return_map.py", "critical_return_map")
    rows, terminals = critical.analyze(scenario_args(args))
    summary_rows, rule_rows = mine_rules(rows, args.threshold, args.min_pos)
    write_csv(summary_rows, OUT_SOURCE_SUMMARY)
    write_csv(rule_rows, OUT_RULES)

    print("=" * 112)
    print("  Exception congruence miner")
    print("=" * 112)
    print(f"  returns:   {len(rows):,}")
    print(f"  terminals: {len(terminals):,}")
    print(f"  threshold: delta_t_bits <= {args.threshold}")
    print("\n  Dominant sources:")
    for row in summary_rows[:12]:
        print(
            f"    k={row['source_k']} c={row['source_cycle_id']} b={row['source_b']} "
            f"exceptions={row['exceptions']:>3}/{row['rows']:<5} "
            f"rate={row['baseline_exception_rate']:.4f} min_delta={row['min_delta_t_bits']}"
        )

    print("\n  Top modular rules:")
    for row in rule_rows[:20]:
        print(
            f"    k={row['source_k']} c={row['source_cycle_id']} b={row['source_b']} "
            f"{row['rule']:<34} pos={row['positive_rows']:>3}/{row['covered_rows']:<4} "
            f"precision={row['precision']:.3f} lift={row['lift']:.1f}"
        )

    print("\n  Output:")
    print(f"    {OUT_SOURCE_SUMMARY.name}")
    print(f"    {OUT_RULES.name}")


if __name__ == "__main__":
    main()
