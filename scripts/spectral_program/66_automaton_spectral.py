"""
66_automaton_spectral.py

Spettro pesato dell'automa bulk/eccezioni del nodo critico.

Costruiamo una matrice di trasferimento sui blocchi del return map critico.
Ogni ritorno da un hit critico al successivo produce un edge

    block_i -> block_j

con peso

    2^(-s * delta_t_bits).

Le visite terminali non producono edge: rappresentano massa che esce dal
sistema critico. Se il raggio spettrale della matrice normalizzata per
occorrenze del blocco sorgente e' < 1, l'automa osservato e' subcritico a
quell'esponente s.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict

import numpy as np


BLOCKS = [
    "BULK",
    "E1_v2_20",
    "E2_odd_mod4_1",
    "E3_odd_mod8_3",
    "E4_hit_7",
    "E5_v2_21",
]


def read_csv_int(path: str) -> list[dict[str, int]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


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


def terminal_block(row: dict[str, int]) -> str:
    return classify(row["t_v2"], row["odd_mod_256"], row["hit_index"])


def build_matrix(returns: list[dict[str, int]], terminals: list[dict[str, int]], s: float):
    idx = {b: i for i, b in enumerate(BLOCKS)}
    weighted = np.zeros((len(BLOCKS), len(BLOCKS)), dtype=float)
    source_counts = Counter()
    terminal_counts = Counter()

    for row in returns:
        src = source_block(row)
        dst = dest_block(row)
        source_counts[src] += 1
        weighted[idx[src], idx[dst]] += 2.0 ** (-s * row["delta_t_bits"])

    for row in terminals:
        block = terminal_block(row)
        source_counts[block] += 1
        terminal_counts[block] += 1

    M = np.zeros_like(weighted)
    for block, i in idx.items():
        denom = source_counts[block]
        if denom:
            M[i, :] = weighted[i, :] / denom

    return M, source_counts, terminal_counts, weighted


def spectral_radius(M: np.ndarray) -> float:
    vals = np.linalg.eigvals(M)
    return float(max(abs(v) for v in vals)) if vals.size else 0.0


def scan(returns: list[dict[str, int]], terminals: list[dict[str, int]], s_values: list[float]) -> list[dict]:
    rows = []
    for s in s_values:
        M, source_counts, terminal_counts, weighted = build_matrix(returns, terminals, s)
        rows.append({
            "s": s,
            "rho": spectral_radius(M),
            "total_sources": sum(source_counts.values()),
            "terminal_sources": sum(terminal_counts.values()),
        })
    return rows


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_matrix(M: np.ndarray) -> None:
    print("\n  Matrice normalizzata:")
    print(" " * 16 + " ".join(f"{b[:8]:>10}" for b in BLOCKS))
    for block, row in zip(BLOCKS, M):
        print(f"  {block[:14]:<14} " + " ".join(f"{x:>10.4g}" for x in row))


def print_summary(rows: list[dict], returns: list[dict[str, int]], terminals: list[dict[str, int]], s: float) -> None:
    M, source_counts, terminal_counts, weighted = build_matrix(returns, terminals, s)
    print("=" * 112)
    print("  Spettro pesato dell'automa critico")
    print("=" * 112)
    print(f"  returns:   {len(returns)}")
    print(f"  terminals: {len(terminals)}")
    print(f"\n  Scan rho(s):")
    print(f"  {'s':>6} {'rho':>14} {'verdetto':>12}")
    for row in rows:
        verdict = "subcritical" if row["rho"] < 1 else "supercritical"
        print(f"  {row['s']:>6.2f} {row['rho']:>14.6g} {verdict:>12}")

    print(f"\n  Dettaglio a s={s:g}: rho={spectral_radius(M):.6g}")
    print(f"  {'block':<18} {'sources':>8} {'terminal':>8} {'exit%':>8}")
    for block in BLOCKS:
        src = source_counts[block]
        term = terminal_counts[block]
        exit_frac = term / src if src else 0.0
        print(f"  {block:<18} {src:>8} {term:>8} {exit_frac:>8.4f}")
    print_matrix(M)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spettro dell'automa critico.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--terminals", default="collatz_62_critical_terminals.csv")
    parser.add_argument("--s", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    returns = read_csv_int(args.returns)
    terminals = read_csv_int(args.terminals)
    s_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    rows = scan(returns, terminals, s_values)
    write_csv(rows, "collatz_66_automaton_spectral.csv")
    print_summary(rows, returns, terminals, args.s)
    print("\n  Output: collatz_66_automaton_spectral.csv")


if __name__ == "__main__":
    main()
