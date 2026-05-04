"""
57_shadowing_family_probe.py

Probe delle famiglie congruenziali che shadowano un ciclo fantasma.

Per un fantasma con punto periodico razionale 2-adico q e parola w con
A = sum(w), il lemma di shadowing dice che ogni intero dispari

    n = r + t * 2^M,     r = q mod 2^M,     M = bA + 1,

segue la parola w ripetuta b volte.

Gli script 55/56 testavano soprattutto il rappresentante minimo t=0. Questo
script varia t per capire se il rientro sotto il valore iniziale dopo
l'uscita dal fantasma resta controllato sull'intera classe congruenziale.

Output:
  - collatz_57_shadowing_family_detail.csv
  - collatz_57_shadowing_family_summary.csv
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path


def load_module(filename: str, name: str):
    path = Path(__file__).with_name(filename)
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def t_values_for_mode(t_max: int, mode: str) -> list[int]:
    if t_max < 0:
        return []
    if mode == "dense":
        return list(range(t_max + 1))
    if mode == "powers":
        values = {0, 1, 2, 3, 5, 7, 11, 15}
        p = 1
        while p <= t_max:
            values.add(p)
            values.add(p - 1)
            values.add(min(t_max, p + 1))
            p <<= 1
        values.add(t_max)
        return sorted(v for v in values if 0 <= v <= t_max)
    raise ValueError(f"unknown mode: {mode}")


def analyze_family(record: dict, b: int, t_values: list[int], max_extra_steps: int) -> list[dict]:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")

    word = record["word"]
    q = record["q"]
    period_len = record["length"]
    period_bits = record["sum_a"]
    modulus_bits = b * period_bits + 1
    modulus = 1 << modulus_bits
    residue = shadows.rational_mod_power_of_two(q, modulus_bits)
    if residue == 0:
        residue = modulus

    expected = word * b
    rows = []

    for t in t_values:
        n0 = residue + t * modulus

        observed = shadowing.valuation_word(n0, len(expected))
        mismatch = shadowing.first_mismatch(observed, expected)
        follows = mismatch is None

        after_shadow = shadowing.iterate_odd(n0, b * period_len)
        extra_periods = shadowing.count_extra_full_periods(
            after_shadow, word, max_extra_periods=8
        )
        stop_steps, max_after, max_ratio_after = shadowing.stopping_below_start(
            after_shadow, n0, max_extra_steps
        )

        rows.append({
            "k": record["k"],
            "cycle_id": record["cycle_id"],
            "period_len": period_len,
            "period_bits": period_bits,
            "period_product": record["product"],
            "b": b,
            "modulus_bits": modulus_bits,
            "residue": residue,
            "t": t,
            "n0": n0,
            "n0_bit_length": n0.bit_length(),
            "follows_word": int(follows),
            "first_mismatch_step": mismatch or "",
            "after_shadow": after_shadow,
            "shadow_growth_ratio": after_shadow / n0,
            "expected_period_growth": record["product"] ** b,
            "extra_full_periods": extra_periods,
            "extra_stop_steps_below_n0": stop_steps if stop_steps is not None else "",
            "extra_max_ratio_from_n0": max_ratio_after,
        })

    return rows


def summarize(rows: list[dict]) -> list[dict]:
    groups = {}
    for row in rows:
        key = (row["k"], row["cycle_id"], row["b"])
        groups.setdefault(key, []).append(row)

    summary_rows = []
    for key, group in sorted(groups.items()):
        k, cycle_id, b = key
        bad = [r for r in group if not r["follows_word"]]
        unresolved = [r for r in group if r["extra_stop_steps_below_n0"] == ""]
        resolved = [r for r in group if r["extra_stop_steps_below_n0"] != ""]

        max_stop_row = max(
            resolved,
            key=lambda r: int(r["extra_stop_steps_below_n0"]),
            default=None,
        )
        max_ratio_row = max(group, key=lambda r: float(r["extra_max_ratio_from_n0"]))
        max_shadow_ratio_row = max(group, key=lambda r: float(r["shadow_growth_ratio"]))

        summary_rows.append({
            "k": k,
            "cycle_id": cycle_id,
            "b": b,
            "period_len": group[0]["period_len"],
            "period_bits": group[0]["period_bits"],
            "period_product": group[0]["period_product"],
            "modulus_bits": group[0]["modulus_bits"],
            "t_count": len(group),
            "t_min": min(int(r["t"]) for r in group),
            "t_max": max(int(r["t"]) for r in group),
            "bad_word_count": len(bad),
            "unresolved_count": len(unresolved),
            "max_stop_steps": int(max_stop_row["extra_stop_steps_below_n0"]) if max_stop_row else "",
            "max_stop_t": int(max_stop_row["t"]) if max_stop_row else "",
            "max_extra_full_periods": max(int(r["extra_full_periods"]) for r in group),
            "max_extra_ratio_from_n0": max_ratio_row["extra_max_ratio_from_n0"],
            "max_extra_ratio_t": max_ratio_row["t"],
            "max_shadow_growth_ratio": max_shadow_ratio_row["shadow_growth_ratio"],
            "max_shadow_growth_t": max_shadow_ratio_row["t"],
        })

    return summary_rows


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict]) -> None:
    print("\n" + "=" * 118)
    print("  FAMILY SHADOWING PROBE")
    print("=" * 118)
    print(f"  {'k':>3} {'id':>3} {'b':>2} {'M':>5} {'t#':>5} {'bad':>5} "
          f"{'unres':>6} {'max stop':>9} {'t':>6} {'extraP':>7} "
          f"{'max ratio':>13} {'t':>6}")
    for r in rows:
        print(f"  {r['k']:>3} {r['cycle_id']:>3} {r['b']:>2} "
              f"{r['modulus_bits']:>5} {r['t_count']:>5} "
              f"{r['bad_word_count']:>5} {r['unresolved_count']:>6} "
              f"{str(r['max_stop_steps']):>9} {str(r['max_stop_t']):>6} "
              f"{r['max_extra_full_periods']:>7} "
              f"{float(r['max_extra_ratio_from_n0']):>13.6g} "
              f"{str(r['max_extra_ratio_t']):>6}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe su n = q mod 2^(bA+1) piu' t*2^(bA+1)."
    )
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-min", type=int, default=1)
    parser.add_argument("--b-max", type=int, default=12)
    parser.add_argument("--t-max", type=int, default=255)
    parser.add_argument("--t-mode", choices=["dense", "powers"], default="dense")
    parser.add_argument("--max-extra-steps", type=int, default=200000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    records = shadowing.phantom_records(args.k_min, args.k_max)
    t_values = t_values_for_mode(args.t_max, args.t_mode)

    print("=" * 118)
    print("  Probe delle famiglie congruenziali phantom")
    print("=" * 118)
    print(f"  k range: {args.k_min}..{args.k_max}")
    print(f"  b range: {args.b_min}..{args.b_max}")
    print(f"  t mode:  {args.t_mode}, count={len(t_values)}, max={max(t_values) if t_values else '-'}")
    print(f"  max extra steps: {args.max_extra_steps}")

    detail_rows = []
    for record in records:
        print(f"  Record k={record['k']} id={record['cycle_id']} "
              f"L={record['length']} A={record['sum_a']} "
              f"product={record['product']:.6f}")
        for b in range(args.b_min, args.b_max + 1):
            detail_rows.extend(
                analyze_family(record, b, t_values, args.max_extra_steps)
            )

    summary_rows = summarize(detail_rows)
    detail_path = "collatz_57_shadowing_family_detail.csv"
    summary_path = "collatz_57_shadowing_family_summary.csv"
    write_csv(detail_rows, detail_path)
    write_csv(summary_rows, summary_path)
    print_summary(summary_rows)
    print(f"\n  Dettaglio: {detail_path}")
    print(f"  Sintesi:   {summary_path}")


if __name__ == "__main__":
    main()
