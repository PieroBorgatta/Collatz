"""
62_critical_return_map.py

Analisi del nodo critico del grafo episodi: k=12, cycle=2, b=1.

La diagnostica precedente mostra che (12,2,1) e' l'hub ambiguo:
puo' essere terminale oppure precedere molte altre visite. Questo script
studia il primo ritorno da (12,2,1) a (12,2,1), confrontando:

  - bit-length del valore reale;
  - v2(n-q);
  - bit-length del parametro locale t;
  - v2(t);
  - odd part di t modulo potenze di 2.

Scopo: trovare una quantita' che decresca sul return map critico.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from importlib import util
from pathlib import Path


def load_module(filename: str, name: str):
    path = Path(__file__).with_name(filename)
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def v2_int(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    out = 0
    while (n & 1) == 0:
        n >>= 1
        out += 1
    return out


def v2_fraction_difference(n: int, q) -> int:
    diff_num = n * q.denominator - q.numerator
    if diff_num == 0:
        return 10**9
    return v2_int(diff_num)


def target_record(records: list[dict], k: int, cycle_id: int) -> dict:
    for rec in records:
        if rec["k"] == k and rec["cycle_id"] == cycle_id:
            return rec
    raise KeyError((k, cycle_id))


def residue_for(record: dict, b: int) -> tuple[int, int, int]:
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    bits = b * record["sum_a"] + 1
    modulus = 1 << bits
    residue = shadows.rational_mod_power_of_two(record["q"], bits)
    if residue == 0:
        residue = modulus
    return residue, modulus, bits


def local_t(n: int, record: dict, b: int) -> tuple[int, int]:
    residue, modulus, bits = residue_for(record, b)
    assert (n - residue) % modulus == 0
    return (n - residue) // modulus, bits


def best_shadow(n: int, records: list[dict]) -> dict | None:
    best = None
    for rec in records:
        v = v2_fraction_difference(n, rec["q"])
        b = (v - 1) // rec["sum_a"]
        if b < 1:
            continue
        score = (b, v)
        if best is None or score > best["score"]:
            best = {"record": rec, "b": b, "v2": v, "score": score}
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


def make_start(record: dict, b: int, t: int) -> int:
    residue, modulus, _ = residue_for(record, b)
    return residue + t * modulus


def trace_target_hits(n0: int, records: list[dict], target: tuple[int, int, int], max_steps: int) -> list[dict]:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    target_rec = target_record(records, target[0], target[1])

    cur = n0
    hits = []
    last_key = None
    for step in range(max_steps + 1):
        if step > 0 and cur < n0:
            return hits
        hit = best_shadow(cur, records)
        if hit is not None:
            rec = hit["record"]
            key = (rec["k"], rec["cycle_id"], hit["b"])
            if key != last_key:
                if key == target:
                    t, bits = local_t(cur, target_rec, target[2])
                    odd = 0 if t == 0 else t >> v2_int(t)
                    hits.append({
                        "step": step,
                        "value_bit_length": cur.bit_length(),
                        "v2_n_minus_q": hit["v2"],
                        "local_t_bit_length": t.bit_length(),
                        "local_t_v2": v2_int(t),
                        "local_t_odd_mod_256": odd & 255,
                        "local_t_odd_mod_4096": odd & 4095,
                    })
                last_key = key
        if step == max_steps:
            break
        _, cur = shadowing.odd_syracuse_step(cur)
    return hits


def analyze(args: argparse.Namespace) -> tuple[list[dict], list[dict]]:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    records = shadowing.phantom_records(args.k_min, args.k_max)
    sources = records
    target = (args.target_k, args.target_cycle, args.target_b)
    t_values = t_values_for_mode(args.t_max, args.t_mode)

    return_rows = []
    terminal_rows = []
    for source in sources:
        for b0 in range(args.b_min, args.b_max + 1):
            for t0 in t_values:
                n0 = make_start(source, b0, t0)
                hits = trace_target_hits(n0, records, target, args.max_steps)
                for i, hit in enumerate(hits):
                    if i + 1 < len(hits):
                        nxt = hits[i + 1]
                        return_rows.append({
                            "source_k": source["k"],
                            "source_cycle_id": source["cycle_id"],
                            "source_b": b0,
                            "source_t": t0,
                            "hit_index": i,
                            "delta_step": nxt["step"] - hit["step"],
                            "delta_value_bits": nxt["value_bit_length"] - hit["value_bit_length"],
                            "delta_t_bits": nxt["local_t_bit_length"] - hit["local_t_bit_length"],
                            "delta_t_v2": nxt["local_t_v2"] - hit["local_t_v2"],
                            "from_value_bits": hit["value_bit_length"],
                            "to_value_bits": nxt["value_bit_length"],
                            "from_t_bits": hit["local_t_bit_length"],
                            "to_t_bits": nxt["local_t_bit_length"],
                            "from_t_v2": hit["local_t_v2"],
                            "to_t_v2": nxt["local_t_v2"],
                            "from_odd_mod_256": hit["local_t_odd_mod_256"],
                            "to_odd_mod_256": nxt["local_t_odd_mod_256"],
                        })
                    else:
                        terminal_rows.append({
                            "source_k": source["k"],
                            "source_cycle_id": source["cycle_id"],
                            "source_b": b0,
                            "source_t": t0,
                            "hit_index": i,
                            "remaining_after_hit": len(hits) - i - 1,
                            "value_bits": hit["value_bit_length"],
                            "t_bits": hit["local_t_bit_length"],
                            "t_v2": hit["local_t_v2"],
                            "odd_mod_256": hit["local_t_odd_mod_256"],
                        })
    return return_rows, terminal_rows


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(return_rows: list[dict], terminal_rows: list[dict]) -> None:
    print("\n" + "=" * 110)
    print("  CRITICAL RETURN MAP SUMMARY")
    print("=" * 110)
    print(f"  returns:   {len(return_rows)}")
    print(f"  terminals: {len(terminal_rows)}")
    if not return_rows:
        return
    print(f"  delta value bits min/max: "
          f"{min(r['delta_value_bits'] for r in return_rows)} / "
          f"{max(r['delta_value_bits'] for r in return_rows)}")
    print(f"  delta t bits min/max: "
          f"{min(r['delta_t_bits'] for r in return_rows)} / "
          f"{max(r['delta_t_bits'] for r in return_rows)}")
    print(f"  delta t v2 min/max: "
          f"{min(r['delta_t_v2'] for r in return_rows)} / "
          f"{max(r['delta_t_v2'] for r in return_rows)}")
    print("\n  delta_t_bits distribution:")
    for val, count in Counter(r["delta_t_bits"] for r in return_rows).most_common(12):
        print(f"    {val:>4}: {count}")
    print("\n  delta_value_bits distribution:")
    for val, count in Counter(r["delta_value_bits"] for r in return_rows).most_common(12):
        print(f"    {val:>4}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analizza il return map del nodo critico.")
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-min", type=int, default=1)
    parser.add_argument("--b-max", type=int, default=8)
    parser.add_argument("--t-max", type=int, default=255)
    parser.add_argument("--t-mode", choices=["dense", "powers"], default="dense")
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--target-k", type=int, default=12)
    parser.add_argument("--target-cycle", type=int, default=2)
    parser.add_argument("--target-b", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("=" * 110)
    print("  Return map del nodo critico")
    print("=" * 110)
    print(f"  target: k={args.target_k}, cycle={args.target_cycle}, b={args.target_b}")
    print(f"  b range: {args.b_min}..{args.b_max}; t {args.t_mode}/{args.t_max}")

    return_rows, terminal_rows = analyze(args)
    write_csv(return_rows, "collatz_62_critical_returns.csv")
    write_csv(terminal_rows, "collatz_62_critical_terminals.csv")
    print_summary(return_rows, terminal_rows)
    print("\n  Output:")
    print("    collatz_62_critical_returns.csv")
    print("    collatz_62_critical_terminals.csv")


if __name__ == "__main__":
    main()
