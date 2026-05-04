"""
67_weighted_edge_inspector.py

Ispeziona le transizioni che dominano lo spettro pesato dell'automa critico.

Per ogni ritorno critico calcola:

    weight = 2^(-s * delta_t_bits)

e raggruppa per edge block_i -> block_j. Le code con delta_t_bits negativo
producono pesi enormi; questo script le rende esplicite.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict


def read_csv_int(path: str) -> list[dict[str, int]]:
    out = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            out.append({k: int(v) for k, v in row.items()})
    return out


def classify(t_v2: int, odd_mod: int, hit_index: int) -> str:
    if t_v2 == 20:
        return "E1_v2_20"
    if odd_mod & 3 == 1:
        return "E2_odd_mod4_1"
    if odd_mod & 7 == 3:
        return "E3_odd_mod8_3"
    if hit_index == 7:
        return "E4_hit_7"
    if t_v2 == 21:
        return "E5_v2_21"
    return "BULK"


def source_block(row: dict[str, int]) -> str:
    return classify(row["from_t_v2"], row["from_odd_mod_256"], row["hit_index"])


def dest_block(row: dict[str, int]) -> str:
    return classify(row["to_t_v2"], row["to_odd_mod_256"], row["hit_index"] + 1)


def inspect(rows: list[dict[str, int]], s: float):
    edge_stats = defaultdict(lambda: {
        "count": 0,
        "weight": 0.0,
        "bad": 0,
        "min_delta": 10**9,
        "max_delta": -10**9,
    })

    row_out = []
    for row in rows:
        src = source_block(row)
        dst = dest_block(row)
        delta = row["delta_t_bits"]
        weight = 2.0 ** (-s * delta)
        key = (src, dst)
        st = edge_stats[key]
        st["count"] += 1
        st["weight"] += weight
        st["bad"] += int(delta < 0)
        st["min_delta"] = min(st["min_delta"], delta)
        st["max_delta"] = max(st["max_delta"], delta)
        row_out.append({
            **row,
            "src_block": src,
            "dst_block": dst,
            "weight": weight,
        })

    edge_rows = []
    for (src, dst), st in edge_stats.items():
        edge_rows.append({
            "src": src,
            "dst": dst,
            **st,
            "avg_weight": st["weight"] / st["count"],
            "bad_fraction": st["bad"] / st["count"],
        })
    edge_rows.sort(key=lambda r: -r["weight"])
    row_out.sort(key=lambda r: -r["weight"])
    return edge_rows, row_out


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(edge_rows: list[dict], row_rows: list[dict]) -> None:
    print("=" * 112)
    print("  Transizioni pesate dominanti")
    print("=" * 112)
    print(f"  {'src':<18} {'dst':<18} {'count':>7} {'bad':>5} {'dmin':>5} "
          f"{'dmax':>5} {'weight':>14} {'bad%':>8}")
    for r in edge_rows[:20]:
        print(f"  {r['src']:<18} {r['dst']:<18} {r['count']:>7} {r['bad']:>5} "
              f"{r['min_delta']:>5} {r['max_delta']:>5} {r['weight']:>14.6g} "
              f"{r['bad_fraction']:>8.4f}")

    print("\n  Top singole righe:")
    print(f"  {'src':<18} {'dst':<18} {'delta':>6} {'weight':>12} "
          f"{'src_b':>5} {'t':>6} {'hit':>5} {'from_v2':>8} {'odd256':>7}")
    for r in row_rows[:20]:
        print(f"  {r['src_block']:<18} {r['dst_block']:<18} {r['delta_t_bits']:>6} "
              f"{r['weight']:>12.6g} {r['source_b']:>5} {r['source_t']:>6} "
              f"{r['hit_index']:>5} {r['from_t_v2']:>8} {r['from_odd_mod_256']:>7}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ispeziona edge pesati critici.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--s", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_csv_int(args.returns)
    edge_rows, row_rows = inspect(rows, args.s)
    write_csv(edge_rows, "collatz_67_weighted_edges.csv")
    write_csv(row_rows[:500], "collatz_67_top_weighted_rows.csv")
    print_summary(edge_rows, row_rows)
    print("\n  Output:")
    print("    collatz_67_weighted_edges.csv")
    print("    collatz_67_top_weighted_rows.csv")


if __name__ == "__main__":
    main()
