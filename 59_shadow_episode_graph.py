"""
59_shadow_episode_graph.py

Grafo degli episodi di shadowing.

Il tentativo di certificare un rientro uniforme dopo un singolo fantasma e'
troppo forte: i bit alti liberi di

    n = r + t * 2^(bA+1)

possono codificare un nuovo aggancio a un altro fantasma dopo l'uscita dal
primo. Il modello giusto diventa quindi un grafo di episodi:

    phantom A  ->  phantom B  ->  ...  ->  discesa

Questo script campiona famiglie phantom e, lungo l'orbita, rileva quando il
valore corrente e' vicino a uno dei punti razionali 2-adici negativi q_w.

Per un fantasma w con A=sum(w), la profondita' di shadowing potenziale e':

    b(n,w) = floor((v2(n - q_w) - 1) / A).

Se b >= 1, n segue almeno un periodo completo di w.
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


def make_start(record: dict, b: int, t: int) -> tuple[int, int]:
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    modulus_bits = b * record["sum_a"] + 1
    modulus = 1 << modulus_bits
    residue = shadows.rational_mod_power_of_two(record["q"], modulus_bits)
    if residue == 0:
        residue = modulus
    return residue + t * modulus, modulus_bits


def trace_episodes(n0: int, records: list[dict], max_steps: int) -> dict:
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
            key = (rec["k"], rec["cycle_id"], hit["b"])
            # Avoid logging every internal step of the same episode.
            if key != last_key:
                episodes.append({
                    "step": step,
                    "k": rec["k"],
                    "cycle_id": rec["cycle_id"],
                    "b": hit["b"],
                    "v2": hit["v2"],
                    "value": cur,
                })
                last_key = key

        if step == max_steps:
            break
        _, cur = shadowing.odd_syracuse_step(cur)

    return {
        "stopped": False,
        "stop_step": "",
        "max_value": max_value,
        "episodes": episodes,
    }


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


def analyze(args: argparse.Namespace) -> tuple[list[dict], list[dict], list[dict]]:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    records = shadowing.phantom_records(args.k_min, args.k_max)
    t_values = t_values_for_mode(args.t_max, args.t_mode)

    detail_rows = []
    episode_rows = []
    transitions = Counter()

    for source in records:
        for b0 in range(args.b_min, args.b_max + 1):
            for t in t_values:
                n0, modulus_bits = make_start(source, b0, t)
                result = trace_episodes(n0, records, args.max_steps)
                episodes = result["episodes"]
                keys = [
                    (ep["k"], ep["cycle_id"], ep["b"])
                    for ep in episodes
                ]
                for a, b in zip(keys, keys[1:]):
                    transitions[(a, b)] += 1

                detail_rows.append({
                    "source_k": source["k"],
                    "source_cycle_id": source["cycle_id"],
                    "source_b": b0,
                    "t": t,
                    "n0_bit_length": n0.bit_length(),
                    "modulus_bits": modulus_bits,
                    "stopped": int(result["stopped"]),
                    "stop_step": result["stop_step"],
                    "max_ratio": result["max_value"] / n0,
                    "episode_count": len(episodes),
                    "episode_path": " > ".join(
                        f"k{ep['k']}:c{ep['cycle_id']}:b{ep['b']}@{ep['step']}"
                        for ep in episodes
                    ),
                })

                for idx, ep in enumerate(episodes):
                    episode_rows.append({
                        "source_k": source["k"],
                        "source_cycle_id": source["cycle_id"],
                        "source_b": b0,
                        "t": t,
                        "episode_index": idx,
                        "step": ep["step"],
                        "k": ep["k"],
                        "cycle_id": ep["cycle_id"],
                        "b": ep["b"],
                        "v2": ep["v2"],
                        "value_bit_length": ep["value"].bit_length(),
                    })

    transition_rows = []
    for (src, dst), count in transitions.most_common():
        transition_rows.append({
            "src_k": src[0],
            "src_cycle_id": src[1],
            "src_b": src[2],
            "dst_k": dst[0],
            "dst_cycle_id": dst[1],
            "dst_b": dst[2],
            "count": count,
        })

    return detail_rows, episode_rows, transition_rows


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(detail_rows: list[dict], episode_rows: list[dict], transition_rows: list[dict]) -> None:
    total = len(detail_rows)
    stopped = sum(r["stopped"] for r in detail_rows)
    max_episodes = max((r["episode_count"] for r in detail_rows), default=0)
    max_ratio = max((r["max_ratio"] for r in detail_rows), default=0.0)
    unresolved = total - stopped

    print("\n" + "=" * 110)
    print("  SHADOW EPISODE GRAPH SUMMARY")
    print("=" * 110)
    print(f"  orbite:        {total}")
    print(f"  stopped:       {stopped}")
    print(f"  unresolved:    {unresolved}")
    print(f"  episodi totali:{len(episode_rows)}")
    print(f"  max episodi/orbita: {max_episodes}")
    print(f"  max ratio:     {max_ratio:.6g}")

    print("\n  Top transizioni:")
    print(f"  {'src':>16} {'dst':>16} {'count':>8}")
    for row in transition_rows[:20]:
        src = f"k{row['src_k']}:c{row['src_cycle_id']}:b{row['src_b']}"
        dst = f"k{row['dst_k']}:c{row['dst_cycle_id']}:b{row['dst_b']}"
        print(f"  {src:>16} {dst:>16} {row['count']:>8}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Costruisce un grafo di episodi phantom.")
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-min", type=int, default=1)
    parser.add_argument("--b-max", type=int, default=8)
    parser.add_argument("--t-max", type=int, default=255)
    parser.add_argument("--t-mode", choices=["dense", "powers"], default="dense")
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("=" * 110)
    print("  Grafo degli episodi di shadowing")
    print("=" * 110)
    print(f"  k range: {args.k_min}..{args.k_max}")
    print(f"  b range: {args.b_min}..{args.b_max}")
    print(f"  t mode/max: {args.t_mode}/{args.t_max}")
    print(f"  max steps: {args.max_steps}")

    detail_rows, episode_rows, transition_rows = analyze(args)
    write_csv(detail_rows, "collatz_59_shadow_episode_detail.csv")
    write_csv(episode_rows, "collatz_59_shadow_episode_events.csv")
    write_csv(transition_rows, "collatz_59_shadow_episode_transitions.csv")
    print_summary(detail_rows, episode_rows, transition_rows)

    print("\n  Output:")
    print("    collatz_59_shadow_episode_detail.csv")
    print("    collatz_59_shadow_episode_events.csv")
    print("    collatz_59_shadow_episode_transitions.csv")


if __name__ == "__main__":
    main()
