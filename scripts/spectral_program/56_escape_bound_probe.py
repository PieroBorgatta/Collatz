"""
56_escape_bound_probe.py

Stress test del prossimo obiettivo teorico:

    dopo lo shadowing di un ciclo fantasma, quanto rapidamente l'orbita
    torna sotto il valore iniziale?

Usa i rappresentanti minimi

    n_b = q mod 2^(bA + 1)

per ciascun fantasma e per b = 1..B. Il lemma di shadowing garantisce che
questi numeri seguono b periodi completi del fantasma. Qui misuriamo solo la
fase successiva: il "pagamento del debito".

Questo e' un esperimento, non un teorema. Serve a capire quale forma potrebbe
avere un bound dimostrabile.
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path


def load_shadowing_module():
    path = Path(__file__).with_name("55_shadowing_congruence.py")
    spec = util.spec_from_file_location("shadowing", path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def summarize(rows: list[dict]) -> list[dict]:
    groups = {}
    for row in rows:
        key = (row["k"], row["cycle_id"])
        groups.setdefault(key, []).append(row)

    summary = []
    for (k, cycle_id), group in sorted(groups.items()):
        unresolved = [r for r in group if r["extra_stop_steps_below_n0"] == ""]
        resolved = [r for r in group if r["extra_stop_steps_below_n0"] != ""]
        max_stop_row = max(
            resolved,
            key=lambda r: int(r["extra_stop_steps_below_n0"]),
            default=None,
        )
        max_ratio_row = max(group, key=lambda r: float(r["extra_max_ratio_from_n0"]))
        max_extra_periods = max(int(r["extra_full_periods"]) for r in group)
        max_v2_surplus = max(
            int(r["v2_n0_minus_q"]) - int(r["modulus_bits"])
            for r in group
        )

        summary.append({
            "k": k,
            "cycle_id": cycle_id,
            "period_len": group[0]["period_len"],
            "period_bits": group[0]["period_bits"],
            "period_product": group[0]["period_product"],
            "b_min": min(int(r["b"]) for r in group),
            "b_max": max(int(r["b"]) for r in group),
            "max_n0_bit_length": max(int(r["n0_bit_length"]) for r in group),
            "unresolved_count": len(unresolved),
            "max_stop_steps": int(max_stop_row["extra_stop_steps_below_n0"]) if max_stop_row else "",
            "max_stop_at_b": int(max_stop_row["b"]) if max_stop_row else "",
            "max_extra_full_periods": max_extra_periods,
            "max_v2_surplus": max_v2_surplus,
            "max_extra_ratio_from_n0": max_ratio_row["extra_max_ratio_from_n0"],
            "max_extra_ratio_at_b": max_ratio_row["b"],
        })

    return summary


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict]) -> None:
    print("\n" + "=" * 104)
    print("  ESCAPE BOUND PROBE")
    print("=" * 104)
    print(f"  {'k':>3} {'id':>3} {'b range':>9} {'n0 bits':>8} {'unres':>6} "
          f"{'max stop':>9} {'at b':>5} {'extraP':>7} {'v2+':>5} "
          f"{'max ratio':>13} {'at b':>5}")
    for r in rows:
        b_range = f"{r['b_min']}..{r['b_max']}"
        print(f"  {r['k']:>3} {r['cycle_id']:>3} {b_range:>9} "
              f"{r['max_n0_bit_length']:>8} {r['unresolved_count']:>6} "
              f"{str(r['max_stop_steps']):>9} {str(r['max_stop_at_b']):>5} "
              f"{r['max_extra_full_periods']:>7} {r['max_v2_surplus']:>5} "
              f"{float(r['max_extra_ratio_from_n0']):>13.6g} "
              f"{r['max_extra_ratio_at_b']:>5}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe del rientro sotto n0 dopo shadowing phantom."
    )
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-max", type=int, default=25)
    parser.add_argument("--max-extra-steps", type=int, default=200000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    shadowing = load_shadowing_module()

    print("=" * 104)
    print("  Probe del pagamento del debito post-shadowing")
    print("=" * 104)
    print(f"  k range: {args.k_min}..{args.k_max}")
    print(f"  b max:   {args.b_max}")
    print(f"  max extra steps: {args.max_extra_steps}")

    records = shadowing.phantom_records(args.k_min, args.k_max)
    rows = []
    for record in records:
        print(f"  Analizzo k={record['k']} id={record['cycle_id']} "
              f"L={record['length']} A={record['sum_a']}...")
        rows.extend(shadowing.analyze_record(record, args.b_max, args.max_extra_steps))

    detail_path = "collatz_56_escape_bound_detail.csv"
    summary_path = "collatz_56_escape_bound_summary.csv"
    summary_rows = summarize(rows)

    write_csv(rows, detail_path)
    write_csv(summary_rows, summary_path)
    print_summary(summary_rows)

    print(f"\n  Dettaglio: {detail_path}")
    print(f"  Sintesi:   {summary_path}")


if __name__ == "__main__":
    main()
