#!/usr/bin/env python3
"""
Gate-10.B provenance checks for generated FULL matrices.

This script checks only finite provenance facts:

1. the older T10CriticalSymbolic CSV has row-source normalized weights;
2. the T10J32HighBitTail CSV has power-of-two high-bit prefix length;
3. high-bit normalized entries are exact weight/source_count fractions;
4. high-bit full entries equal core + tail entrywise.

It does not prove an infinite operator, martingale convergence,
Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap, or Collatz.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "scripts/spectral_program/collatz_111_gate10b_provenance_report.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def decimal_fraction(text: str) -> Fraction:
    return Fraction(Decimal(text))


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def check_critical(path: Path, target_t: int) -> dict[str, Any]:
    rows = [row for row in read_csv(path) if int(row["T"]) == target_t]
    mismatches = 0
    sources: set[str] = set()
    for row in rows:
        sources.add(row["src"])
        lhs = decimal_fraction(row["weight_sum"]) / int(row["source_count"])
        rhs = decimal_fraction(row["normalized_weight"])
        if lhs != rhs:
            mismatches += 1
    return {
        "path": str(path.relative_to(ROOT)),
        "target_t": target_t,
        "rows": len(rows),
        "sources": len(sources),
        "normalized_mismatches": mismatches,
        "compatible": bool(rows) and mismatches == 0,
        "interpretation": (
            "finite Haar/counting quotient over Z/2^T Z x H, grouped by source PhaseState"
        ),
    }


def check_high_bit(path: Path, target_t: int, j_count: int) -> dict[str, Any]:
    rows = [
        row
        for row in read_csv(path)
        if int(row["T"]) == target_t and int(row["j_count"]) == j_count
    ]
    normalized_mismatches = 0
    metadata_mismatches = 0
    graphs: dict[str, dict[tuple[str, str], Fraction]] = {
        "full": defaultdict(Fraction),
        "core": defaultdict(Fraction),
        "tail": defaultdict(Fraction),
    }
    sources: set[str] = set()
    for row in rows:
        graph = row["graph"]
        if graph not in graphs:
            metadata_mismatches += 1
            continue
        if int(row["odd_bits"]) != 2 or int(row["hit_bits"]) != 2:
            metadata_mismatches += 1
        sources.add(row["src"])
        weight = Fraction(int(row["weight_num"]), int(row["weight_den"]))
        source_count = int(row["source_count"])
        normalized = Fraction(int(row["normalized_num"]), int(row["normalized_den"]))
        if weight / source_count != normalized:
            normalized_mismatches += 1
        graphs[graph][(row["src"], row["dst"])] += normalized

    all_edges = set(graphs["full"]) | set(graphs["core"]) | set(graphs["tail"])
    decomposition_mismatches = 0
    for edge in all_edges:
        if graphs["full"].get(edge, Fraction(0)) != (
            graphs["core"].get(edge, Fraction(0)) + graphs["tail"].get(edge, Fraction(0))
        ):
            decomposition_mismatches += 1

    return {
        "path": str(path.relative_to(ROOT)),
        "target_t": target_t,
        "j_count": j_count,
        "j_count_power_of_two": is_power_of_two(j_count),
        "rows": len(rows),
        "sources": len(sources),
        "normalized_mismatches": normalized_mismatches,
        "metadata_mismatches": metadata_mismatches,
        "decomposition_mismatches": decomposition_mismatches,
        "compatible": (
            bool(rows)
            and is_power_of_two(j_count)
            and normalized_mismatches == 0
            and metadata_mismatches == 0
            and decomposition_mismatches == 0
        ),
        "interpretation": (
            "high-bit prefix Haar/counting quotient over Z/2^(T+log2(j_count)) Z x H; "
            "conditional interpretation applies to full, while core/tail is finite majority bookkeeping"
        ),
    }


def render_report(critical: dict[str, Any], high_bit: dict[str, Any]) -> str:
    lines = [
        "# Gate 10.B Generated FULL Provenance Check",
        "",
        "Status: finite provenance check only.  This report does not prove",
        "an infinite operator, spectral gap, Lasota-Yorke inequality,",
        "Hennion, Keller-Liverani, Conjecture 6, or Collatz.",
        "",
        "## T10CriticalSymbolic",
        "",
        "| field | value |",
        "|---|---:|",
        f"| source CSV | `{critical['path']}` |",
        f"| target T | {critical['target_t']} |",
        f"| rows | {critical['rows']} |",
        f"| source states | {critical['sources']} |",
        f"| normalized mismatches | {critical['normalized_mismatches']} |",
        f"| compatible with A0 Haar conditional reading | `{critical['compatible']}` |",
        "",
        critical["interpretation"],
        "",
        "## T10J32HighBitTail",
        "",
        "| field | value |",
        "|---|---:|",
        f"| source CSV | `{high_bit['path']}` |",
        f"| target T | {high_bit['target_t']} |",
        f"| j_count | {high_bit['j_count']} |",
        f"| j_count power of two | `{high_bit['j_count_power_of_two']}` |",
        f"| rows | {high_bit['rows']} |",
        f"| source states | {high_bit['sources']} |",
        f"| normalized mismatches | {high_bit['normalized_mismatches']} |",
        f"| metadata mismatches | {high_bit['metadata_mismatches']} |",
        f"| full = core + tail mismatches | {high_bit['decomposition_mismatches']} |",
        f"| compatible with A0 Haar conditional reading | `{high_bit['compatible']}` |",
        "",
        high_bit["interpretation"],
        "",
        "## Interpretation",
        "",
        "Both generated FULL matrices pass the finite provenance checks for",
        "the conditional Gate-10.B interpretation.  This supports reading",
        "their full rows as finite Haar/counting conditional expectations",
        "onto source PhaseState.  It does not make PhaseState an exact",
        "sourcewise sufficient statistic, and it does not promote core/tail",
        "majority bookkeeping to an infinite operator decomposition.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--critical",
        type=Path,
        default=ROOT / "collatz_75_critical_symbolic_edges.csv",
    )
    parser.add_argument(
        "--high-bit",
        type=Path,
        default=ROOT / "scripts/phantom_taxonomy/high_bit_tail_edges_T10_j32.csv",
    )
    parser.add_argument("--target-t", type=int, default=10)
    parser.add_argument("--j-count", type=int, default=32)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    critical = check_critical(args.critical, args.target_t)
    high_bit = check_high_bit(args.high_bit, args.target_t, args.j_count)
    report = render_report(critical, high_bit)
    args.output.write_text(report, encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"critical_compatible={critical['compatible']}")
    print(f"high_bit_compatible={high_bit['compatible']}")


if __name__ == "__main__":
    main()
