import csv
import math
from collections import Counter


INPUT_ENTRY_FILE = "collatz_13_ingressi_autostrada.csv"
OUTPUT_FILE = "collatz_15_pre_ingresso_autostrada.csv"
SUMMARY_FILE = "collatz_15_summary_pre_ingresso.txt"

TRUNK_VALUE = 8216025965
CRITICAL_V2 = math.log2(3)


def v2(x: int) -> int:
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def syracuse(n: int):
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


def read_entries(filename: str):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            rows.append({
                "start": int(row["start"]),
                "entry_step": int(row["entry_step"]),
                "entry_value": int(row["entry_value"]),
                "max_before_entry": int(row["max_before_entry"]),
                "ratio_max_before_entry": float(row["ratio_max_before_entry"]),
                "total_steps_to_1": int(row["total_steps_to_1"]),
                "steps_from_entry_to_1": int(row["steps_from_entry_to_1"]),
                "start_mod_1024": int(row["start_mod_1024"]),
                "start_mod_4096": int(row["start_mod_4096"]),
                "start_mod_65536": int(row["start_mod_65536"]),
            })

    return rows


def longest_run(seq, value):
    best = 0
    current = 0

    for x in seq:
        if x == value:
            current += 1
            best = max(best, current)
        else:
            current = 0

    return best


def analyze_until_entry(start: int, entry_value: int):
    n = start

    seq_v2 = []
    values = [start]

    cumulative_v2 = 0

    max_debt = 0.0
    max_debt_step = 0

    max_value = start
    max_value_step = 0

    first_positive_surplus_step = None
    first_descent_step = None

    for step in range(1, 100_000):
        n, a = syracuse(n)

        seq_v2.append(a)
        values.append(n)

        cumulative_v2 += a

        debt = step * CRITICAL_V2 - cumulative_v2
        surplus = cumulative_v2 - step * CRITICAL_V2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if n > max_value:
            max_value = n
            max_value_step = step

        if first_positive_surplus_step is None and surplus > 0:
            first_positive_surplus_step = step

        if first_descent_step is None and n < start:
            first_descent_step = step

        if n == entry_value:
            break

    counter = Counter(seq_v2)

    steps = len(seq_v2)
    total_v2 = sum(seq_v2)
    avg_v2 = total_v2 / steps if steps else 0

    final_surplus = total_v2 - steps * CRITICAL_V2
    final_debt = steps * CRITICAL_V2 - total_v2

    return {
        "start": start,
        "entry_value": entry_value,
        "entry_step_computed": steps,

        "max_value_pre_entry": max_value,
        "max_value_step_pre_entry": max_value_step,
        "ratio_max_pre_entry": max_value / start,

        "total_v2_pre_entry": total_v2,
        "avg_v2_pre_entry": avg_v2,

        "final_surplus_at_entry": final_surplus,
        "final_debt_at_entry": final_debt,

        "max_debt_pre_entry": max_debt,
        "max_debt_step_pre_entry": max_debt_step,

        "first_positive_surplus_step_pre_entry": first_positive_surplus_step,
        "first_descent_step_pre_entry": first_descent_step,

        "count_1": counter.get(1, 0),
        "count_2": counter.get(2, 0),
        "count_3": counter.get(3, 0),
        "count_4_plus": sum(v for k, v in counter.items() if k >= 4),

        "ratio_1": counter.get(1, 0) / steps if steps else 0,
        "ratio_2": counter.get(2, 0) / steps if steps else 0,
        "ratio_3": counter.get(3, 0) / steps if steps else 0,
        "ratio_4_plus": sum(v for k, v in counter.items() if k >= 4) / steps if steps else 0,

        "max_run_1": longest_run(seq_v2, 1),
        "prefix_80_v2": ",".join(map(str, seq_v2[:80])),
        "full_v2_pre_entry": ",".join(map(str, seq_v2)),
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list):
    rows_by_debt = sorted(rows, key=lambda x: x["max_debt_pre_entry"], reverse=True)
    rows_by_ratio = sorted(rows, key=lambda x: x["ratio_max_pre_entry"], reverse=True)
    rows_by_entry = sorted(rows, key=lambda x: x["entry_step_computed"], reverse=True)

    avg_entry_step = sum(r["entry_step_computed"] for r in rows) / len(rows)
    avg_v2 = sum(r["avg_v2_pre_entry"] for r in rows) / len(rows)
    avg_ratio_1 = sum(r["ratio_1"] for r in rows) / len(rows)

    lines = []

    lines.append("ANALISI PRE-INGRESSO NELL'AUTOSTRADA GRAVITAZIONALE")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Tronco comune: {TRUNK_VALUE}")
    lines.append(f"Numeri analizzati: {len(rows)}")
    lines.append("")
    lines.append(f"Entry step medio: {avg_entry_step:.6f}")
    lines.append(f"avg_v2 medio pre-ingresso: {avg_v2:.6f}")
    lines.append(f"ratio_1 medio pre-ingresso: {avg_ratio_1:.6f}")
    lines.append("")
    lines.append("Top 20 massimo debito pre-ingresso:")
    lines.append("-" * 120)

    for r in rows_by_debt[:20]:
        lines.append(
            f"n={r['start']:10d} | "
            f"entry={r['entry_step_computed']:4d} | "
            f"max_debt={r['max_debt_pre_entry']:9.6f} | "
            f"debt_step={r['max_debt_step_pre_entry']:4d} | "
            f"ratio_max={r['ratio_max_pre_entry']:12.3f} | "
            f"avg_v2={r['avg_v2_pre_entry']:.6f} | "
            f"ratio_1={r['ratio_1']:.6f} | "
            f"max_run_1={r['max_run_1']}"
        )

    lines.append("")
    lines.append("Top 20 massimo rapporto pre-ingresso:")
    lines.append("-" * 120)

    for r in rows_by_ratio[:20]:
        lines.append(
            f"n={r['start']:10d} | "
            f"entry={r['entry_step_computed']:4d} | "
            f"ratio_max={r['ratio_max_pre_entry']:12.3f} | "
            f"max_debt={r['max_debt_pre_entry']:9.6f} | "
            f"avg_v2={r['avg_v2_pre_entry']:.6f} | "
            f"ratio_1={r['ratio_1']:.6f} | "
            f"max_run_1={r['max_run_1']}"
        )

    lines.append("")
    lines.append("Top 20 ingresso più tardivo:")
    lines.append("-" * 120)

    for r in rows_by_entry[:20]:
        lines.append(
            f"n={r['start']:10d} | "
            f"entry={r['entry_step_computed']:4d} | "
            f"max_debt={r['max_debt_pre_entry']:9.6f} | "
            f"ratio_max={r['ratio_max_pre_entry']:12.3f} | "
            f"avg_v2={r['avg_v2_pre_entry']:.6f} | "
            f"ratio_1={r['ratio_1']:.6f} | "
            f"max_run_1={r['max_run_1']}"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    entries = read_entries(INPUT_ENTRY_FILE)

    rows = []

    print("Analisi pre-ingresso nell'autostrada comune")
    print("-" * 120)

    for idx, entry in enumerate(entries, start=1):
        row = analyze_until_entry(entry["start"], entry["entry_value"])

        # Aggiungiamo dati modulari dal file ingressi
        row["start_mod_1024"] = entry["start_mod_1024"]
        row["start_mod_4096"] = entry["start_mod_4096"]
        row["start_mod_65536"] = entry["start_mod_65536"]
        row["total_steps_to_1"] = entry["total_steps_to_1"]
        row["steps_from_entry_to_1"] = entry["steps_from_entry_to_1"]

        rows.append(row)

        print(
            f"{idx:2d}) n={row['start']:10d} | "
            f"entry={row['entry_step_computed']:4d} | "
            f"max_debt={row['max_debt_pre_entry']:9.6f} | "
            f"ratio_max={row['ratio_max_pre_entry']:12.3f} | "
            f"avg_v2={row['avg_v2_pre_entry']:.6f} | "
            f"ratio_1={row['ratio_1']:.3f}"
        )

    rows.sort(key=lambda x: x["max_debt_pre_entry"], reverse=True)

    export_csv(OUTPUT_FILE, rows)
    export_summary(SUMMARY_FILE, rows)

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
