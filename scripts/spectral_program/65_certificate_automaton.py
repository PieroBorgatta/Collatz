"""
65_certificate_automaton.py

Prima versione di automa di certificazione per il nodo critico.

Usa le regole trovate da 64_exception_splitter.py per partizionare i ritorni
critici in blocchi:

    E1, E2, ..., Ek, BULK

e misura per ciascun blocco:
  - pressione interna;
  - massa;
  - distribuzione delta_t_bits;
  - quali blocchi seguono dopo un ritorno.

L'obiettivo e' trasformare "bulk contrae, eccezioni rare espandono" in un
automa finito su cui calcolare pressioni/SCC.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict


def read_returns(path: str) -> list[dict[str, int]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def read_terminals(path: str) -> list[dict[str, int]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def classify_hit(row: dict[str, int], terminal: bool = False) -> str:
    # Rules from the s=1 splitter run, ordered greedily.
    t_v2 = row["t_v2"] if terminal else row["from_t_v2"]
    odd_mod = row["odd_mod_256"] if terminal else row["from_odd_mod_256"]
    hit_index = row["hit_index"]

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


def pressure(rows: list[dict[str, int]], terminal_count: int, s: float) -> float:
    total = len(rows) + terminal_count
    if total == 0:
        return 0.0
    weighted = sum(2.0 ** (-s * r["delta_t_bits"]) for r in rows)
    return weighted / total


def block_stats(rows: list[dict[str, int]], terminals: list[dict[str, int]], s: float) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[classify_hit(row)].append(row)
    terminal_groups = Counter(classify_hit(row, terminal=True) for row in terminals)

    out = []
    for name in sorted(set(groups) | set(terminal_groups)):
        group = groups.get(name, [])
        terminal_count = terminal_groups.get(name, 0)
        deltas = [r["delta_t_bits"] for r in group]
        bad = sum(1 for d in deltas if d < 0)
        out.append({
            "block": name,
            "count": len(group),
            "terminal_count": terminal_count,
            "bad_count": bad,
            "precision_bad": bad / len(group) if group else 0.0,
            "delta_min": min(deltas) if deltas else "",
            "delta_max": max(deltas) if deltas else "",
            "delta_mode": Counter(deltas).most_common(1)[0][0] if deltas else "",
            "pressure": pressure(group, terminal_count, s),
        })
    return out


def transition_stats(rows: list[dict[str, int]], terminals: list[dict[str, int]]) -> list[dict]:
    # Group by original orbit and hit_index order.
    by_orbit = defaultdict(list)
    for row in rows:
        key = (
            row["source_k"],
            row["source_cycle_id"],
            row["source_b"],
            row["source_t"],
        )
        by_orbit[key].append({
            "hit_index": row["hit_index"],
            "block": classify_hit(row),
            "terminal": False,
        })
    for row in terminals:
        key = (
            row["source_k"],
            row["source_cycle_id"],
            row["source_b"],
            row["source_t"],
        )
        by_orbit[key].append({
            "hit_index": row["hit_index"],
            "block": classify_hit(row, terminal=True),
            "terminal": True,
        })

    counts = Counter()
    for seq in by_orbit.values():
        seq.sort(key=lambda r: r["hit_index"])
        blocks = [r["block"] for r in seq]
        for a, b in zip(blocks, blocks[1:]):
            counts[(a, b)] += 1
        if blocks:
            counts[(blocks[-1], "TERMINAL")] += 1

    out = []
    for (src, dst), count in counts.most_common():
        out.append({
            "src": src,
            "dst": dst,
            "count": count,
        })
    return out


def sccs(transitions: list[dict]) -> list[list[str]]:
    graph = defaultdict(set)
    for row in transitions:
        src = row["src"]
        dst = row["dst"]
        if dst == "TERMINAL":
            graph.setdefault(src, set())
            continue
        graph[src].add(dst)
        graph.setdefault(dst, set())

    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    comps = []

    def strong(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph[v]:
            if w not in indices:
                strong(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for v in graph:
        if v not in indices:
            strong(v)
    return comps


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(stats: list[dict], transitions: list[dict], comps: list[list[str]]) -> None:
    print("=" * 110)
    print("  Automazione critica: blocchi bulk/eccezioni")
    print("=" * 110)
    print(f"  {'block':<18} {'n':>7} {'term':>7} {'bad':>6} {'prec':>8} "
          f"{'dmin':>6} {'dmax':>6} {'mode':>6} {'P':>12}")
    for row in stats:
        print(f"  {row['block']:<18} {row['count']:>7} {row['terminal_count']:>7} "
              f"{row['bad_count']:>6} {row['precision_bad']:>8.4f} "
              f"{row['delta_min']:>6} {row['delta_max']:>6} {row['delta_mode']:>6} "
              f"{row['pressure']:>12.6g}")

    self_loops = {
        (row["src"], row["dst"])
        for row in transitions
        if row["src"] == row["dst"]
    }
    nontrivial = [
        c for c in comps
        if len(c) > 1 or any((v, v) in self_loops for v in c)
    ]
    print("\n  SCC non banali:")
    if not nontrivial:
        print("    nessuna")
    else:
        for comp in nontrivial:
            print(f"    {comp}")

    print("\n  Top transizioni blocchi:")
    for row in transitions[:20]:
        print(f"    {row['src']:<18} -> {row['dst']:<18} {row['count']:>7}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automa bulk/eccezioni per il return map critico.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--terminals", default="collatz_62_critical_terminals.csv")
    parser.add_argument("--s", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_returns(args.returns)
    terminals = read_terminals(args.terminals)
    stats = block_stats(rows, terminals, args.s)
    transitions = transition_stats(rows, terminals)
    comps = sccs(transitions)
    write_csv(stats, "collatz_65_certificate_blocks.csv")
    write_csv(transitions, "collatz_65_certificate_transitions.csv")
    print_summary(stats, transitions, comps)
    print("\n  Output:")
    print("    collatz_65_certificate_blocks.csv")
    print("    collatz_65_certificate_transitions.csv")


if __name__ == "__main__":
    main()
