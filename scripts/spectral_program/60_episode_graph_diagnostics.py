"""
60_episode_graph_diagnostics.py

Diagnostica del grafo degli episodi prodotto da 59_shadow_episode_graph.py.

Domanda:
    Lo stato grossolano (k, cycle_id, b) basta per una funzione energia?

Se il grafo osservato contiene componenti fortemente connesse non banali,
allora nessuna energia strettamente decrescente dipendente solo da
(k, cycle_id, b) puo' esistere. Questo non uccide la teoria: significa che
serve una coordinata di fase/residuo.

Questo script misura:
  - SCC del grafo degli episodi;
  - ambiguita' dello stato: per lo stesso (k,c,b), quante mosse residue
    possono restare prima della discesa;
  - quanto migliorano le ambiguita' raffinando con surplus v2 e bit-length
    relativo;
  - una ranking function empirica R(state)=max future episodes osservati.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict


State = tuple[int, int, int]


def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def state_from_row(row: dict) -> State:
    return int(row["k"]), int(row["cycle_id"]), int(row["b"])


def build_graph(transitions: list[dict]) -> dict[State, set[State]]:
    graph: dict[State, set[State]] = defaultdict(set)
    for row in transitions:
        src = (int(row["src_k"]), int(row["src_cycle_id"]), int(row["src_b"]))
        dst = (int(row["dst_k"]), int(row["dst_cycle_id"]), int(row["dst_b"]))
        graph[src].add(dst)
        graph.setdefault(dst, set())
    return graph


def tarjans_scc(graph: dict[State, set[State]]) -> list[list[State]]:
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    components = []

    def strongconnect(v: State) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph[v]:
            if w not in indices:
                strongconnect(w)
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
            components.append(comp)

    for v in graph:
        if v not in indices:
            strongconnect(v)
    return components


def episode_groups(events: list[dict]) -> dict[tuple[int, int, int, int], list[dict]]:
    groups = defaultdict(list)
    for row in events:
        key = (
            int(row["source_k"]),
            int(row["source_cycle_id"]),
            int(row["source_b"]),
            int(row["t"]),
        )
        groups[key].append(row)
    for rows in groups.values():
        rows.sort(key=lambda r: int(r["episode_index"]))
    return groups


def ambiguity_by_key(events: list[dict], key_fn) -> list[dict]:
    groups = episode_groups(events)
    remaining_by_state = defaultdict(list)

    for rows in groups.values():
        total = len(rows)
        for idx, row in enumerate(rows):
            key = key_fn(row)
            remaining = total - idx - 1
            remaining_by_state[key].append(remaining)

    out = []
    for key, vals in remaining_by_state.items():
        vals_sorted = sorted(vals)
        out.append({
            "key": key,
            "count": len(vals),
            "min_remaining": vals_sorted[0],
            "max_remaining": vals_sorted[-1],
            "spread": vals_sorted[-1] - vals_sorted[0],
            "avg_remaining": sum(vals_sorted) / len(vals_sorted),
        })
    out.sort(key=lambda r: (-r["spread"], -r["count"], str(r["key"])))
    return out


def coarse_key(row: dict):
    return int(row["k"]), int(row["cycle_id"]), int(row["b"])


def surplus_key(row: dict):
    k, c, b = coarse_key(row)
    v2 = int(row["v2"])
    period_bits = period_bits_for(k, c)
    surplus = v2 - (b * period_bits + 1)
    return k, c, b, surplus


def bitlen_bucket_key(row: dict):
    k, c, b = coarse_key(row)
    v2 = int(row["v2"])
    period_bits = period_bits_for(k, c)
    surplus = v2 - (b * period_bits + 1)
    bit_bucket = int(row["value_bit_length"]) // 16
    return k, c, b, surplus, bit_bucket


def period_bits_for(k: int, cycle_id: int) -> int:
    # From the phantom records observed so far.
    table = {
        (10, 1): 37,
        (11, 1): 37,
        (12, 1): 9,
        (12, 2): 7,
        (20, 1): 30,
    }
    return table[(k, cycle_id)]


def write_ambiguity(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["key", "count", "min_remaining", "max_remaining", "spread", "avg_remaining"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_sccs(graph: dict[State, set[State]], components: list[list[State]]) -> None:
    nontrivial = [
        c for c in components
        if len(c) > 1 or any(v in graph[v] for v in c)
    ]
    nontrivial.sort(key=lambda c: (-len(c), sorted(c)))

    print("\n" + "=" * 100)
    print("  SCC DEL GRAFO GROSSOLANO (k,cycle,b)")
    print("=" * 100)
    print(f"  stati: {len(graph)}")
    print(f"  componenti: {len(components)}")
    print(f"  SCC non banali: {len(nontrivial)}")
    for comp in nontrivial[:12]:
        print(f"    size={len(comp)}  {sorted(comp)}")


def print_ambiguity(label: str, rows: list[dict]) -> None:
    print("\n" + "=" * 100)
    print(f"  AMBIGUITA': {label}")
    print("=" * 100)
    if not rows:
        print("  Nessuna riga.")
        return
    max_spread = max(r["spread"] for r in rows)
    ambiguous = sum(1 for r in rows if r["spread"] > 0)
    print(f"  chiavi totali: {len(rows)}")
    print(f"  chiavi ambigue: {ambiguous}")
    print(f"  spread massimo: {max_spread}")
    print(f"  {'key':>32} {'count':>8} {'min':>5} {'max':>5} {'spread':>7} {'avg':>8}")
    for r in rows[:15]:
        print(f"  {str(r['key']):>32} {r['count']:>8} {r['min_remaining']:>5} "
              f"{r['max_remaining']:>5} {r['spread']:>7} {r['avg_remaining']:>8.3f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnostica del grafo episodi.")
    parser.add_argument("--events", default="collatz_59_shadow_episode_events.csv")
    parser.add_argument("--transitions", default="collatz_59_shadow_episode_transitions.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    events = read_csv(args.events)
    transitions = read_csv(args.transitions)
    graph = build_graph(transitions)
    components = tarjans_scc(graph)

    print("=" * 100)
    print("  Diagnostica energia per grafo episodi")
    print("=" * 100)
    print(f"  eventi:      {len(events)}")
    print(f"  transizioni: {len(transitions)}")

    print_sccs(graph, components)

    coarse = ambiguity_by_key(events, coarse_key)
    surplus = ambiguity_by_key(events, surplus_key)
    bucket = ambiguity_by_key(events, bitlen_bucket_key)

    write_ambiguity(coarse, "collatz_60_ambiguity_coarse.csv")
    write_ambiguity(surplus, "collatz_60_ambiguity_surplus.csv")
    write_ambiguity(bucket, "collatz_60_ambiguity_surplus_bitbucket.csv")

    print_ambiguity("(k,cycle,b)", coarse)
    print_ambiguity("(k,cycle,b,v2_surplus)", surplus)
    print_ambiguity("(k,cycle,b,v2_surplus,value_bit_bucket)", bucket)

    print("\n  Output:")
    print("    collatz_60_ambiguity_coarse.csv")
    print("    collatz_60_ambiguity_surplus.csv")
    print("    collatz_60_ambiguity_surplus_bitbucket.csv")


if __name__ == "__main__":
    main()
