"""
Orbit-simulation harness for the augmented phantom episode graph.

This is Phase 7.3 of the Lean TODO roadmap.  It consumes the exact
representatives produced by ``phantom_representatives.py`` and samples
integer lifts

    n_0 = q_w mod 2^(bA+1) + t * 2^(bA+1)

for each source phantom word.  Along the odd Syracuse orbit it records
hits on any monitored phantom congruence class and emits a transition
edge list.

The script is intentionally a harness rather than the final exhaustive
run: Phase 7.4 chooses the production cutoff and sampling budget.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Representative:
    node_id: int
    K: int
    L: int
    word: tuple[int, ...]
    C_w: int
    A: int
    q: Fraction

    @property
    def key(self) -> str:
        return f"K{self.K}:L{self.L}:w{'-'.join(map(str, self.word))}"


@dataclass(frozen=True)
class Monitor:
    representative: Representative
    modulus_bits: int
    residue: int

    @property
    def modulus(self) -> int:
        return 1 << self.modulus_bits


def v2_split(m: int) -> tuple[int, int]:
    if m <= 0:
        raise ValueError("odd Syracuse orbit expects positive integers")
    a = 0
    while (m & 1) == 0:
        m >>= 1
        a += 1
    return a, m


def odd_syracuse_step(n: int) -> tuple[int, int]:
    return v2_split(3 * n + 1)


def v2_fraction_difference(n: int, q: Fraction) -> int:
    diff = n * q.denominator - q.numerator
    if diff == 0:
        return 10**9
    diff = abs(diff)
    a = 0
    while (diff & 1) == 0:
        diff >>= 1
        a += 1
    return a


def rational_mod_power_of_two(q: Fraction, bits: int) -> int:
    modulus = 1 << bits
    den = q.denominator % modulus
    if den % 2 == 0:
        raise ValueError(f"even denominator for {q}")
    return (q.numerator % modulus) * pow(den, -1, modulus) % modulus


def read_representatives(path: Path, max_K: int | None = None) -> list[Representative]:
    reps: list[Representative] = []
    with path.open(encoding="utf-8", newline="") as f:
        for idx, row in enumerate(csv.DictReader(f)):
            K = int(row["K"])
            if max_K is not None and K > max_K:
                continue
            reps.append(
                Representative(
                    node_id=len(reps),
                    K=K,
                    L=int(row["L"]),
                    word=tuple(int(x) for x in row["word"].split()),
                    C_w=int(row["C_w"]),
                    A=int(row["A"]),
                    q=Fraction(int(row["q_num"]), int(row["q_den"])),
                )
            )
    return reps


def build_monitors(reps: list[Representative]) -> tuple[list[Monitor], dict[int, dict[int, list[Monitor]]]]:
    monitors: list[Monitor] = []
    by_bits: dict[int, dict[int, list[Monitor]]] = defaultdict(lambda: defaultdict(list))
    for rep in reps:
        bits = rep.A + 1
        residue = rational_mod_power_of_two(rep.q, bits)
        monitor = Monitor(representative=rep, modulus_bits=bits, residue=residue)
        monitors.append(monitor)
        by_bits[bits][residue].append(monitor)
    return monitors, by_bits


def t_values(sample_count: int, mode: str) -> list[int]:
    if sample_count <= 0:
        raise ValueError("sample_count must be positive")
    if mode == "dense":
        return list(range(sample_count))
    if mode == "powers":
        values = {0, 1, 2, 3, 5, 7, sample_count - 1}
        p = 1
        while p < sample_count:
            values.add(p)
            values.add(p - 1)
            values.add(min(sample_count - 1, p + 1))
            p <<= 1
        return sorted(v for v in values if 0 <= v < sample_count)
    raise ValueError(mode)


def best_hit(n: int, by_bits: dict[int, dict[int, list[Monitor]]]) -> tuple[Representative, int, int] | None:
    best: tuple[Representative, int, int] | None = None
    for bits, residue_map in by_bits.items():
        candidates = residue_map.get(n % (1 << bits))
        if not candidates:
            continue
        for monitor in candidates:
            rep = monitor.representative
            v = v2_fraction_difference(n, rep.q)
            b = (v - 1) // rep.A
            if b < 1:
                continue
            current = (rep, b, v)
            if best is None or (b, v, -rep.K, -rep.node_id) > (best[1], best[2], -best[0].K, -best[0].node_id):
                best = current
    return best


def source_start(rep: Representative, b: int, t: int) -> tuple[int, int, int]:
    bits = b * rep.A + 1
    modulus = 1 << bits
    residue = rational_mod_power_of_two(rep.q, bits)
    if residue == 0:
        residue = modulus
    return residue + t * modulus, residue, bits


def trace_orbit(
    source: Representative,
    source_b: int,
    t: int,
    by_bits: dict[int, dict[int, list[Monitor]]],
    max_steps: int,
) -> tuple[dict[str, object], list[dict[str, object]], Counter[tuple[str, str]]]:
    n0, residue, bits = source_start(source, source_b, t)
    cur = n0
    max_value = n0
    events: list[dict[str, object]] = []
    transitions: Counter[tuple[str, str]] = Counter()
    last_event_key: tuple[int, int] | None = None
    last_node_key: str | None = None

    for step in range(max_steps + 1):
        max_value = max(max_value, cur)
        if step > 0 and cur < n0:
            break

        hit = best_hit(cur, by_bits)
        if hit is not None:
            rep, b, v = hit
            event_key = (rep.node_id, b)
            if event_key != last_event_key:
                node_key = f"{rep.key}:b{b}"
                if last_node_key is not None:
                    transitions[(last_node_key, node_key)] += 1
                events.append(
                    {
                        "source_node": source.key,
                        "source_b": source_b,
                        "t": t,
                        "event_index": len(events),
                        "step": step,
                        "node": rep.key,
                        "node_id": rep.node_id,
                        "K": rep.K,
                        "L": rep.L,
                        "b": b,
                        "v2_n_minus_q": v,
                        "value_bit_length": cur.bit_length(),
                    }
                )
                last_event_key = event_key
                last_node_key = node_key

        if step == max_steps:
            break
        _, cur = odd_syracuse_step(cur)

    detail = {
        "source_node": source.key,
        "source_id": source.node_id,
        "source_K": source.K,
        "source_L": source.L,
        "source_b": source_b,
        "t": t,
        "start_residue_bits": bits,
        "start_residue": residue,
        "start_bit_length": n0.bit_length(),
        "stopped_below_start": int(cur < n0),
        "stop_or_final_step": step,
        "episode_count": len(events),
        "max_ratio": max_value / n0,
        "episode_path": " > ".join(f"{e['node']}:b{e['b']}@{e['step']}" for e in events),
    }
    return detail, events, transitions


def run_harness(args: argparse.Namespace) -> tuple[list[dict], list[dict], list[dict]]:
    reps = read_representatives(args.representatives, args.max_k)
    if args.max_sources is not None:
        reps = reps[: args.max_sources]
    _, by_bits = build_monitors(reps)
    samples = t_values(args.samples, args.sample_mode)

    details: list[dict] = []
    events: list[dict] = []
    transitions: Counter[tuple[str, str]] = Counter()

    for source in reps:
        for b in range(args.b_min, args.b_max + 1):
            for t in samples:
                detail, orbit_events, orbit_transitions = trace_orbit(
                    source, b, t, by_bits, args.max_steps
                )
                details.append(detail)
                events.extend(orbit_events)
                transitions.update(orbit_transitions)

    edge_rows = [
        {"src": src, "dst": dst, "count": count}
        for (src, dst), count in transitions.most_common()
    ]
    return details, events, edge_rows


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def print_summary(details: list[dict], events: list[dict], edges: list[dict]) -> None:
    total = len(details)
    stopped = sum(int(row["stopped_below_start"]) for row in details)
    print("orbit_count", total)
    print("stopped_below_start", stopped)
    print("event_count", len(events))
    print("edge_count", len(edges))
    print("max_episode_count", max((int(row["episode_count"]) for row in details), default=0))
    print("max_ratio", f"{max((float(row['max_ratio']) for row in details), default=0.0):.12g}")
    print("top_edges")
    for row in edges[:10]:
        print(f"  {row['count']:>6}  {row['src']} -> {row['dst']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--representatives",
        type=Path,
        default=Path("scripts/phantom_taxonomy/phantom_representatives_k3_16.csv"),
    )
    parser.add_argument("--max-k", type=int, default=10, help="monitor/source cutoff K0")
    parser.add_argument("--b-min", type=int, default=1)
    parser.add_argument("--b-max", type=int, default=2)
    parser.add_argument("--samples", type=int, default=8, help="number of t lifts per source")
    parser.add_argument("--sample-mode", choices=["dense", "powers"], default="dense")
    parser.add_argument("--max-steps", type=int, default=500)
    parser.add_argument("--max-sources", type=int, help="debug limit after K filtering")
    parser.add_argument("--out-prefix", type=Path, default=Path("scripts/phantom_taxonomy/orbit_harness_k10"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    details, events, edges = run_harness(args)
    write_csv(details, args.out_prefix.with_name(args.out_prefix.name + "_details.csv"))
    write_csv(events, args.out_prefix.with_name(args.out_prefix.name + "_events.csv"))
    write_csv(edges, args.out_prefix.with_name(args.out_prefix.name + "_edges.csv"))
    print_summary(details, events, edges)


if __name__ == "__main__":
    main()
