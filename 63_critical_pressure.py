"""
63_critical_pressure.py

Pressione empirica del return map critico (12,2,1).

Il return map critico non e' monotono punto per punto: spesso il bit-length
del parametro locale t aumenta. Allora il prossimo criterio naturale non e'
una ranking function deterministica semplice, ma una pressione:

    P(s) = log sum_{ritorni} 2^{-s * delta_bits}

normalizzata rispetto alle occorrenze critiche osservate.

Se una versione esatta di questa pressione fosse < 0, l'insieme di orbite che
ritorna indefinitamente al nodo critico avrebbe dimensione/volume decrescente.
Questo non e' ancora Collatz, ma e' il ponte verso un argomento tipo survival
sets / Hausdorff dimension.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter


def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def pressure(return_rows: list[dict], terminal_count: int, s: float) -> float:
    total = len(return_rows) + terminal_count
    if total == 0:
        return float("-inf")
    weighted = 0.0
    for row in return_rows:
        delta = int(row["delta_t_bits"])
        weighted += 2.0 ** (-s * delta)
    return math.log(weighted / total) if weighted > 0 else float("-inf")


def summarize(return_rows: list[dict], terminal_rows: list[dict]) -> list[dict]:
    terminal_count = len(terminal_rows)
    out = []
    for s in [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
        p = pressure(return_rows, terminal_count, s)
        out.append({
            "s": s,
            "pressure_log": p,
            "pressure_exp": math.exp(p) if p > -1e100 else 0.0,
        })
    return out


def print_summary(return_rows: list[dict], terminal_rows: list[dict], pressure_rows: list[dict]) -> None:
    total = len(return_rows) + len(terminal_rows)
    ret_frac = len(return_rows) / total if total else 0.0
    term_frac = len(terminal_rows) / total if total else 0.0
    deltas = [int(r["delta_t_bits"]) for r in return_rows]

    print("=" * 96)
    print("  Pressione empirica del nodo critico")
    print("=" * 96)
    print(f"  occorrenze totali: {total}")
    print(f"  ritorni:           {len(return_rows)} ({ret_frac:.4f})")
    print(f"  terminali:         {len(terminal_rows)} ({term_frac:.4f})")
    if deltas:
        print(f"  delta_t_bits min/max: {min(deltas)} / {max(deltas)}")
        print("\n  Distribuzione delta_t_bits:")
        for delta, count in Counter(deltas).most_common(16):
            print(f"    {delta:>4}: {count:>8}  ({count/len(deltas):.4f} dei ritorni)")

    print("\n  Pressione normalizzata P_s = sum(2^(-s*delta))/occ_total:")
    print(f"  {'s':>6} {'log P_s':>14} {'P_s':>14} {'verdetto':>12}")
    for row in pressure_rows:
        verdict = "contract" if row["pressure_exp"] < 1.0 else "expand"
        print(f"  {row['s']:>6.2f} {row['pressure_log']:>14.6f} "
              f"{row['pressure_exp']:>14.6f} {verdict:>12}")


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pressione empirica del return map critico.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--terminals", default="collatz_62_critical_terminals.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    return_rows = read_csv(args.returns)
    terminal_rows = read_csv(args.terminals)
    pressure_rows = summarize(return_rows, terminal_rows)
    write_csv(pressure_rows, "collatz_63_critical_pressure.csv")
    print_summary(return_rows, terminal_rows, pressure_rows)
    print("\n  Output: collatz_63_critical_pressure.csv")


if __name__ == "__main__":
    main()
