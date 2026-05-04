"""
71_exception_tail_profile.py

Profile the tail of deep critical returns discovered in
70_delta_exception_stress.py.

For each stress scenario and each depth d, compute

    N_d = #{returns with delta_t_bits <= -d}

and the empirical decay relative to the number of sampled returns. This is
the numerical object that a future proof would need to replace by a rigorous
counting lemma.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUMMARY_PATH = ROOT / "collatz_70_delta_exception_stress_summary.csv"
EXCEPTIONS_PATH = ROOT / "collatz_70_delta_exception_rows.csv"
OUT_TAIL = ROOT / "collatz_71_exception_tail_profile.csv"
OUT_SOURCE = ROOT / "collatz_71_exception_source_profile.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    summary_rows = read_csv(SUMMARY_PATH)
    exception_rows = read_csv(EXCEPTIONS_PATH)
    totals = {row["label"]: int(row["returns"]) for row in summary_rows}

    deltas_by_label: dict[str, list[int]] = defaultdict(list)
    source_counts: dict[tuple[str, int, int, int], list[int]] = defaultdict(list)
    for row in exception_rows:
        label = row["label"]
        delta = int(row["delta_t_bits"])
        deltas_by_label[label].append(delta)
        key = (
            label,
            int(row["source_k"]),
            int(row["source_cycle_id"]),
            int(row["source_b"]),
        )
        source_counts[key].append(delta)

    tail_rows = []
    for label, deltas in sorted(deltas_by_label.items()):
        total = totals[label]
        max_depth = -min(deltas)
        for d in range(11, max_depth + 1):
            count = sum(1 for delta in deltas if delta <= -d)
            if count == 0:
                continue
            fraction = count / total
            tail_rows.append({
                "label": label,
                "depth_d": d,
                "tail_count": count,
                "total_returns": total,
                "tail_fraction": fraction,
                "minus_log2_fraction": -math.log2(fraction),
            })

    source_rows = []
    for (label, k, cycle_id, b), deltas in sorted(source_counts.items()):
        source_rows.append({
            "label": label,
            "source_k": k,
            "source_cycle_id": cycle_id,
            "source_b": b,
            "exception_count": len(deltas),
            "min_delta_t_bits": min(deltas),
            "median_delta_t_bits": sorted(deltas)[len(deltas) // 2],
            "max_depth": -min(deltas),
        })
    source_rows.sort(key=lambda r: (r["label"], -r["exception_count"], -r["max_depth"]))

    write_csv(tail_rows, OUT_TAIL)
    write_csv(source_rows, OUT_SOURCE)

    print("=" * 112)
    print("  Exception tail profile")
    print("=" * 112)
    for label in sorted(deltas_by_label):
        rows = [r for r in tail_rows if r["label"] == label]
        print(f"\n  {label}")
        for row in rows[:8]:
            print(
                f"    d>={row['depth_d']:>2}: count={row['tail_count']:>4} "
                f"fraction={row['tail_fraction']:.6g} "
                f"-log2={row['minus_log2_fraction']:.3f}"
            )
        if len(rows) > 8:
            print("    ...")
            for row in rows[-5:]:
                print(
                    f"    d>={row['depth_d']:>2}: count={row['tail_count']:>4} "
                    f"fraction={row['tail_fraction']:.6g} "
                    f"-log2={row['minus_log2_fraction']:.3f}"
                )

    print("\n  Top source profiles:")
    for row in source_rows[:15]:
        print(
            f"    {row['label']:<20} k={row['source_k']} c={row['source_cycle_id']} "
            f"b={row['source_b']:<2} count={row['exception_count']:<3} "
            f"max_depth={row['max_depth']}"
        )

    print("\n  Output:")
    print(f"    {OUT_TAIL.name}")
    print(f"    {OUT_SOURCE.name}")


if __name__ == "__main__":
    main()
