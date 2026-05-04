"""
61_phase_refinement.py

Trova la fase aritmetica mancante nel grafo degli episodi.

Gli stati grossolani

    (k, cycle_id, b)

non bastano: il grafo osservato contiene una SCC non banale. Questo script
raffina ogni episodio con una fase locale:

    t_local mod 2^m

dove, per l'episodio corrente,

    n = r + t_local * 2^M,
    r = q mod 2^M,
    M = bA + 1.

La fase e' locale: viene ricalcolata rispetto al fantasma attuale, non e' il
t iniziale dell'orbita.

Per m = 0..m_max misura:
  - numero di stati raffinati;
  - SCC non banali e dimensione massima;
  - ambiguita' residua: per uno stesso stato raffinato, quanti episodi
    possono ancora mancare prima della discesa.

Se per qualche m il grafo diventa aciclico o quasi aciclico, abbiamo trovato
un candidato stato finito per una funzione energia.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path


def load_module(filename: str, name: str):
    path = Path(__file__).with_name(filename)
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def v2_fraction_difference(n: int, q) -> int:
    diff_num = n * q.denominator - q.numerator
    if diff_num == 0:
        return 10**9
    diff_num = abs(diff_num)
    a = 0
    while (diff_num & 1) == 0:
        diff_num >>= 1
        a += 1
    return a


def best_shadow(n: int, records: list[dict]) -> dict | None:
    best = None
    for rec in records:
        v = v2_fraction_difference(n, rec["q"])
        b = (v - 1) // rec["sum_a"]
        if b < 1:
            continue
        score = (b, v)
        if best is None or score > best["score"]:
            best = {
                "record": rec,
                "v2": v,
                "b": b,
                "score": score,
            }
    return best


def t_values_for_mode(t_max: int, mode: str) -> list[int]:
    if mode == "dense":
        return list(range(t_max + 1))
    if mode == "powers":
        values = {0, 1, 2, 3, 5, 7, 11, 15, t_max}
        p = 1
        while p <= t_max:
            values.add(p)
            values.add(p - 1)
            values.add(min(t_max, p + 1))
            p <<= 1
        return sorted(v for v in values if 0 <= v <= t_max)
    raise ValueError(mode)


def residue_for(record: dict, b: int) -> tuple[int, int, int]:
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    period_bits = record["sum_a"]
    modulus_bits = b * period_bits + 1
    modulus = 1 << modulus_bits
    residue = shadows.rational_mod_power_of_two(record["q"], modulus_bits)
    if residue == 0:
        residue = modulus
    return residue, modulus, modulus_bits


def make_start(record: dict, b: int, t: int) -> tuple[int, int]:
    residue, modulus, modulus_bits = residue_for(record, b)
    return residue + t * modulus, modulus_bits


def v2_int(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    out = 0
    while (n & 1) == 0:
        n >>= 1
        out += 1
    return out


def local_phase_features(n: int, record: dict, b: int, phase_bits: int) -> tuple[int, int, int, int]:
    residue, modulus, modulus_bits = residue_for(record, b)
    assert (n - residue) % modulus == 0
    local_t = (n - residue) // modulus
    if phase_bits == 0:
        phase = 0
        odd_phase = 0
    else:
        phase = local_t & ((1 << phase_bits) - 1)
        if local_t == 0:
            odd_phase = 0
        else:
            odd_phase = (local_t >> v2_int(local_t)) & ((1 << phase_bits) - 1)
    t_v2 = v2_int(local_t)
    return phase, t_v2, odd_phase, modulus_bits


def trace_episodes(
    n0: int,
    records: list[dict],
    max_steps: int,
    phase_bits_max: int,
) -> dict:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")

    cur = n0
    episodes = []
    max_value = n0
    last_key = None

    for step in range(max_steps + 1):
        if cur > max_value:
            max_value = cur
        if step > 0 and cur < n0:
            return {
                "stopped": True,
                "stop_step": step,
                "max_value": max_value,
                "episodes": episodes,
            }

        hit = best_shadow(cur, records)
        if hit is not None:
            rec = hit["record"]
            coarse = (rec["k"], rec["cycle_id"], hit["b"])
            if coarse != last_key:
                phase_mod_max, t_v2, odd_phase_mod_max, modulus_bits = local_phase_features(
                    cur, rec, hit["b"], phase_bits_max
                )
                episodes.append({
                    "step": step,
                    "k": rec["k"],
                    "cycle_id": rec["cycle_id"],
                    "b": hit["b"],
                    "v2": hit["v2"],
                    "phase_mod_max": phase_mod_max,
                    "t_v2": t_v2,
                    "odd_phase_mod_max": odd_phase_mod_max,
                    "modulus_bits": modulus_bits,
                    "value_bit_length": cur.bit_length(),
                })
                last_key = coarse

        if step == max_steps:
            break
        _, cur = shadowing.odd_syracuse_step(cur)

    return {
        "stopped": False,
        "stop_step": "",
        "max_value": max_value,
        "episodes": episodes,
    }


def collect_paths(args: argparse.Namespace) -> tuple[list[list[dict]], dict]:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    records = shadowing.phantom_records(args.k_min, args.k_max)
    t_values = t_values_for_mode(args.t_max, args.t_mode)
    paths = []
    stats = {
        "orbits": 0,
        "stopped": 0,
        "unresolved": 0,
        "max_episodes": 0,
        "max_ratio": 0.0,
    }

    for source in records:
        for b0 in range(args.b_min, args.b_max + 1):
            for t in t_values:
                n0, _ = make_start(source, b0, t)
                result = trace_episodes(n0, records, args.max_steps, args.phase_bits_max)
                paths.append(result["episodes"])
                stats["orbits"] += 1
                stats["stopped"] += int(result["stopped"])
                stats["max_episodes"] = max(stats["max_episodes"], len(result["episodes"]))
                stats["max_ratio"] = max(stats["max_ratio"], result["max_value"] / n0)
    stats["unresolved"] = stats["orbits"] - stats["stopped"]
    return paths, stats


def state_for_episode(ep: dict, phase_bits: int, mode: str) -> tuple:
    if phase_bits == 0:
        phase = 0
    elif mode == "low":
        phase = ep["phase_mod_max"] & ((1 << phase_bits) - 1)
    elif mode == "odd":
        phase = ep["odd_phase_mod_max"] & ((1 << phase_bits) - 1)
    else:
        raise ValueError(mode)

    if mode == "odd":
        t_v2 = ep["t_v2"]
        # Cap huge v2(t)=infinity for t=0, and also avoid unbounded state names.
        t_v2_bucket = min(t_v2, 64)
        return int(ep["k"]), int(ep["cycle_id"]), int(ep["b"]), t_v2_bucket, phase
    return int(ep["k"]), int(ep["cycle_id"]), int(ep["b"]), phase


def build_graph(paths: list[list[dict]], phase_bits: int, mode: str) -> dict[tuple, set[tuple]]:
    graph = defaultdict(set)
    for path in paths:
        states = [state_for_episode(ep, phase_bits, mode) for ep in path]
        for state in states:
            graph.setdefault(state, set())
        for src, dst in zip(states, states[1:]):
            graph[src].add(dst)
    return graph


def tarjans_scc(graph: dict[tuple, set[tuple]]) -> list[list[tuple]]:
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    components = []

    def strongconnect(v):
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


def ambiguity(paths: list[list[dict]], phase_bits: int, mode: str) -> dict:
    remaining = defaultdict(list)
    for path in paths:
        total = len(path)
        for idx, ep in enumerate(path):
            state = state_for_episode(ep, phase_bits, mode)
            remaining[state].append(total - idx - 1)

    max_spread = 0
    ambiguous = 0
    worst_state = ""
    worst_count = 0
    for state, vals in remaining.items():
        spread = max(vals) - min(vals)
        if spread > 0:
            ambiguous += 1
        if spread > max_spread:
            max_spread = spread
            worst_state = state
            worst_count = len(vals)

    return {
        "ambiguous_states": ambiguous,
        "max_remaining_spread": max_spread,
        "worst_state": worst_state,
        "worst_state_count": worst_count,
    }


def analyze_phase(paths: list[list[dict]], phase_bits: int, mode: str) -> dict:
    graph = build_graph(paths, phase_bits, mode)
    components = tarjans_scc(graph)
    nontrivial = [
        c for c in components
        if len(c) > 1 or any(v in graph[v] for v in c)
    ]
    max_scc_size = max((len(c) for c in nontrivial), default=0)
    edges = sum(len(v) for v in graph.values())
    amb = ambiguity(paths, phase_bits, mode)
    return {
        "mode": mode,
        "phase_bits": phase_bits,
        "states": len(graph),
        "edges": edges,
        "scc_count": len(components),
        "nontrivial_scc_count": len(nontrivial),
        "max_scc_size": max_scc_size,
        **amb,
    }


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict], stats: dict) -> None:
    print("\n" + "=" * 116)
    print("  PHASE REFINEMENT SUMMARY")
    print("=" * 116)
    print(f"  orbite: {stats['orbits']}  stopped: {stats['stopped']}  "
          f"unresolved: {stats['unresolved']}  max episodi: {stats['max_episodes']}  "
          f"max ratio: {stats['max_ratio']:.6g}")
    print(f"  {'mode':>5} {'m':>3} {'states':>8} {'edges':>8} {'SCC*':>6} {'maxSCC':>7} "
          f"{'ambig':>7} {'spread':>7} {'worst':>32} {'count':>7}")
    for row in rows:
        print(f"  {row['mode']:>5} {row['phase_bits']:>3} {row['states']:>8} {row['edges']:>8} "
              f"{row['nontrivial_scc_count']:>6} {row['max_scc_size']:>7} "
              f"{row['ambiguous_states']:>7} {row['max_remaining_spread']:>7} "
              f"{str(row['worst_state']):>32} {row['worst_state_count']:>7}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Raffina il grafo episodi con fase locale.")
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-min", type=int, default=1)
    parser.add_argument("--b-max", type=int, default=8)
    parser.add_argument("--t-max", type=int, default=255)
    parser.add_argument("--t-mode", choices=["dense", "powers"], default="dense")
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--phase-bits-max", type=int, default=12)
    parser.add_argument("--phase-mode", choices=["low", "odd", "both"], default="both")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("=" * 116)
    print("  Raffinamento per fase locale t mod 2^m")
    print("=" * 116)
    print(f"  k range: {args.k_min}..{args.k_max}")
    print(f"  b range: {args.b_min}..{args.b_max}")
    print(f"  t mode/max: {args.t_mode}/{args.t_max}")
    print(f"  phase bits max: {args.phase_bits_max}")

    paths, stats = collect_paths(args)
    modes = ["low", "odd"] if args.phase_mode == "both" else [args.phase_mode]
    rows = [
        analyze_phase(paths, m, mode)
        for mode in modes
        for m in range(args.phase_bits_max + 1)
    ]
    write_csv(rows, "collatz_61_phase_refinement_summary.csv")
    print_summary(rows, stats)
    print("\n  Output: collatz_61_phase_refinement_summary.csv")


if __name__ == "__main__":
    main()
