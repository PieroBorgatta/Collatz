"""
53_lift_phantom_cycles.py

Genealogia dei cicli fantasma della mappa Syracuse deterministica mod 2^k.

Idea
----
Per ogni k costruiamo la mappa sui residui dispari:

    f_k(r) = odd_part(3r + 1) mod 2^k.

Un ciclo e' "phantom" se il suo prodotto

    prod = 3^L / 2^(sum a_i)

e' > 1. Questi cicli sono espansivi a scala finita, ma non sono
automaticamente cicli reali nei naturali. Per capire se sono ostacoli veri,
bisogna vedere se sopravvivono come una catena compatibile quando si passa da
mod 2^k a mod 2^(k+1).

Questo script costruisce il grafo genealogico:

    ciclo a k+1  ->  ciclo/bacino padre a k

ottenuto proiettando un residuo del ciclo figlio modulo 2^k e seguendo la
mappa f_k fino al ciclo a cui appartiene.

Interpretazione
---------------
- Phantom che ha figli phantom: persistenza di una struttura espansiva.
- Phantom senza figli phantom: morte del corridoio espansivo.
- Phantom a k+1 con padre non-phantom: nascita locale da cifre alte.

La congettura strutturale da testare e':

    non esiste un ramo infinito di cicli phantom compatibili.

Se fosse dimostrabile, i ribelli sarebbero spiegati come agganci temporanei a
cicli espansivi modulari che si estinguono nell'inverse limit 2-adico.
"""

from __future__ import annotations

import argparse
import csv
import time
from collections import defaultdict
from math import log2

import numpy as np


def v2_split(m: int) -> tuple[int, int]:
    a = 0
    while (m & 1) == 0:
        m >>= 1
        a += 1
    return a, m


def build_map(k: int) -> tuple[np.ndarray, np.ndarray]:
    half = 1 << (k - 1)
    mask = (1 << k) - 1
    next_idx = np.empty(half, dtype=np.uint32)
    a_of = np.empty(half, dtype=np.uint16)

    for i in range(half):
        r = (i << 1) | 1
        a, m_odd = v2_split(3 * r + 1)
        a_of[i] = a
        next_idx[i] = ((m_odd & mask) - 1) >> 1

    return next_idx, a_of


def find_cycles(k: int) -> dict:
    next_idx, a_of = build_map(k)
    half = len(next_idx)

    state = np.zeros(half, dtype=np.uint8)  # 0 unknown, 1 current path, 2 done
    cycle_of = np.full(half, -1, dtype=np.int32)
    in_path_pos = np.full(half, -1, dtype=np.int32)
    cycles = []

    for start in range(half):
        if state[start] != 0:
            continue

        path = []
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            in_path_pos[cur] = len(path)
            path.append(cur)
            cur = int(next_idx[cur])

        if state[cur] == 1:
            pos = int(in_path_pos[cur])
            cyc_indices = path[pos:]
            cyc_id = len(cycles)
            a_values = [int(a_of[i]) for i in cyc_indices]
            sum_a = sum(a_values)
            length = len(cyc_indices)
            log2_product = length * log2(3) - sum_a
            product = 2.0 ** log2_product
            cycles.append({
                "cycle_id": cyc_id,
                "indices": cyc_indices,
                "length": length,
                "sum_a": sum_a,
                "avg_a": sum_a / length,
                "log2_product": log2_product,
                "product": product,
                "is_phantom": product > 1.0,
            })
            for idx in cyc_indices:
                cycle_of[idx] = cyc_id

        for idx in path:
            state[idx] = 2
            in_path_pos[idx] = -1

    basin_of = compute_basin_ids(cycle_of, next_idx)
    basin_sizes = np.bincount(basin_of, minlength=len(cycles))
    for c in cycles:
        c["basin_size"] = int(basin_sizes[c["cycle_id"]])
        c["first_residue"] = (int(c["indices"][0]) << 1) | 1
        if c["length"] <= 40:
            c["residues"] = [(int(i) << 1) | 1 for i in c["indices"]]

    return {
        "k": k,
        "next_idx": next_idx,
        "a_of": a_of,
        "cycle_of": cycle_of,
        "basin_of": basin_of,
        "cycles": cycles,
    }


def compute_basin_ids(cycle_of: np.ndarray, next_idx: np.ndarray) -> np.ndarray:
    basin_of = cycle_of.copy()
    half = len(next_idx)

    for start in range(half):
        if basin_of[start] >= 0:
            continue
        path = []
        cur = start
        while basin_of[cur] < 0:
            path.append(cur)
            cur = int(next_idx[cur])
        basin = int(basin_of[cur])
        for idx in path:
            basin_of[idx] = basin

    return basin_of


def project_child_to_parent(child_cycle: dict, parent_level: dict) -> int:
    """Proietta un ciclo a k+1 su k e ritorna il cycle_id del padre."""
    k = parent_level["k"]
    residue_child = child_cycle["first_residue"]
    residue_parent = residue_child & ((1 << k) - 1)
    parent_idx = (residue_parent - 1) >> 1
    return int(parent_level["basin_of"][parent_idx])


def summarize_level(level: dict) -> dict:
    cycles = level["cycles"]
    phantoms = [c for c in cycles if c["is_phantom"]]
    return {
        "k": level["k"],
        "states": 1 << (level["k"] - 1),
        "cycles": len(cycles),
        "phantoms": len(phantoms),
        "max_product": max((c["product"] for c in cycles), default=0.0),
        "max_phantom_basin": max((c["basin_size"] for c in phantoms), default=0),
        "total_phantom_basin": sum(c["basin_size"] for c in phantoms),
    }


def write_cycle_summary(levels: list[dict], path: str) -> None:
    rows = []
    for level in levels:
        for c in level["cycles"]:
            if not c["is_phantom"] and c["length"] != 1:
                continue
            rows.append({
                "k": level["k"],
                "cycle_id": c["cycle_id"],
                "is_phantom": int(c["is_phantom"]),
                "length": c["length"],
                "sum_a": c["sum_a"],
                "avg_a": c["avg_a"],
                "product": c["product"],
                "log2_product": c["log2_product"],
                "basin_size": c["basin_size"],
                "first_residue": c["first_residue"],
            })

    fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def write_edges(levels: list[dict], path: str) -> list[dict]:
    rows = []
    by_k = {level["k"]: level for level in levels}

    for child_level in levels[1:]:
        parent_level = by_k[child_level["k"] - 1]
        parent_cycles = parent_level["cycles"]

        for child in child_level["cycles"]:
            parent_id = project_child_to_parent(child, parent_level)
            parent = parent_cycles[parent_id]
            rows.append({
                "parent_k": parent_level["k"],
                "parent_cycle_id": parent_id,
                "parent_is_phantom": int(parent["is_phantom"]),
                "parent_product": parent["product"],
                "child_k": child_level["k"],
                "child_cycle_id": child["cycle_id"],
                "child_is_phantom": int(child["is_phantom"]),
                "child_product": child["product"],
                "child_length": child["length"],
                "child_basin_size": child["basin_size"],
            })

    fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    return rows


def print_genealogy(levels: list[dict], edges: list[dict]) -> None:
    print("\n" + "=" * 78)
    print("  RIEPILOGO LIVELLI")
    print("=" * 78)
    print(f"  {'k':>3} {'states':>9} {'cycles':>7} {'phantoms':>9} "
          f"{'max_prod':>12} {'max_ph_basin':>14} {'tot_ph_basin':>14}")
    for level in levels:
        s = summarize_level(level)
        marker = "  <-- phantom" if s["phantoms"] else ""
        print(f"  {s['k']:>3} {s['states']:>9} {s['cycles']:>7} {s['phantoms']:>9} "
              f"{s['max_product']:>12.6f} {s['max_phantom_basin']:>14} "
              f"{s['total_phantom_basin']:>14}{marker}")

    print("\n" + "=" * 78)
    print("  LIFT k -> k+1 DEI CICLI PHANTOM")
    print("=" * 78)

    edges_by_parent = defaultdict(list)
    for e in edges:
        edges_by_parent[(e["parent_k"], e["parent_cycle_id"])].append(e)

    for level in levels[:-1]:
        phantom_cycles = [c for c in level["cycles"] if c["is_phantom"]]
        if not phantom_cycles:
            continue
        for parent in phantom_cycles:
            key = (level["k"], parent["cycle_id"])
            children = edges_by_parent.get(key, [])
            phantom_children = [e for e in children if e["child_is_phantom"]]
            all_child_ids = [e["child_cycle_id"] for e in children]
            ph_child_ids = [e["child_cycle_id"] for e in phantom_children]
            print(f"  k={level['k']:>2} id={parent['cycle_id']:>2} "
                  f"L={parent['length']:>3} prod={parent['product']:>10.6f} "
                  f"basin={parent['basin_size']:>6}  ->  "
                  f"k={level['k']+1}: children={all_child_ids or '-'} "
                  f"phantom_children={ph_child_ids or '-'}")

    print("\n" + "=" * 78)
    print("  NASCITE PHANTOM DA PADRI NON-PHANTOM")
    print("=" * 78)
    births = [
        e for e in edges
        if e["child_is_phantom"] and not e["parent_is_phantom"]
    ]
    if not births:
        print("  Nessuna nascita phantom osservata.")
    else:
        for e in births:
            print(f"  k={e['child_k']:>2} child id={e['child_cycle_id']:>2} "
                  f"prod={e['child_product']:>10.6f} "
                  f"nasce dal padre k={e['parent_k']} id={e['parent_cycle_id']} "
                  f"prod={e['parent_product']:.6f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genealogia dei cicli phantom della mappa Syracuse mod 2^k."
    )
    parser.add_argument("--k-min", type=int, default=6)
    parser.add_argument("--k-max", type=int, default=22)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    k_min = args.k_min
    k_max = args.k_max

    print("=" * 78)
    print("  Genealogia dei cicli fantasma mod 2^k")
    print("=" * 78)
    print(f"  Range: k={k_min}..{k_max}")

    levels = []
    for k in range(k_min, k_max + 1):
        t0 = time.time()
        level = find_cycles(k)
        elapsed = time.time() - t0
        levels.append(level)
        s = summarize_level(level)
        print(f"  k={k:>2}: states={s['states']:>8}, cycles={s['cycles']:>3}, "
              f"phantoms={s['phantoms']:>2}, max_prod={s['max_product']:>10.6f}, "
              f"time={elapsed:>6.2f}s")

    cycle_path = "collatz_53_phantom_cycle_summary.csv"
    edge_path = "collatz_53_phantom_lift_edges.csv"
    write_cycle_summary(levels, cycle_path)
    edges = write_edges(levels, edge_path)
    print_genealogy(levels, edges)

    print("\n" + "=" * 78)
    print("  OUTPUT")
    print("=" * 78)
    print(f"  Cicli: {cycle_path}")
    print(f"  Edge genealogici: {edge_path}")


if __name__ == "__main__":
    main()
