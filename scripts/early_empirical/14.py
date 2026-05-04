import csv
import math


INPUT_FILE = "collatz_13_tronco_comune.csv"
OUTPUT_FILE = "collatz_14_analisi_tronco_comune.csv"
SUMMARY_FILE = "collatz_14_summary_tronco_comune.txt"

CRITICAL_V2 = math.log2(3)


def read_trunk(filename: str):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            rows.append({
                "trunk_step": int(row["trunk_step"]),
                "value": int(row["value"]),
                "v2_from_previous": int(row["v2_from_previous"]),
            })

    return rows


def analyze_trunk(rows):
    start_value = rows[0]["value"]

    analyzed = []

    cumulative_v2 = 0
    max_debt = 0.0
    max_debt_step = 0

    max_value = start_value
    max_value_step = 0

    biggest_drop_ratio = 1.0
    biggest_drop_step = None
    biggest_drop_from = None
    biggest_drop_to = None
    biggest_drop_v2 = None

    for i, row in enumerate(rows):
        step = row["trunk_step"]
        value = row["value"]
        a = row["v2_from_previous"]

        if step == 0:
            analyzed.append({
                **row,
                "ratio_to_start": 1.0,
                "log_value": math.log(value),
                "cumulative_v2": 0,
                "critical_required_v2": 0.0,
                "surplus_v2": 0.0,
                "debt_v2": 0.0,
                "avg_v2_so_far": 0.0,
                "drop_ratio_from_previous": 1.0,
            })
            continue

        previous_value = rows[i - 1]["value"]
        drop_ratio = value / previous_value

        cumulative_v2 += a

        critical_required = step * CRITICAL_V2
        surplus = cumulative_v2 - critical_required
        debt = critical_required - cumulative_v2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if value > max_value:
            max_value = value
            max_value_step = step

        if drop_ratio < biggest_drop_ratio:
            biggest_drop_ratio = drop_ratio
            biggest_drop_step = step
            biggest_drop_from = previous_value
            biggest_drop_to = value
            biggest_drop_v2 = a

        analyzed.append({
            **row,
            "ratio_to_start": value / start_value,
            "log_value": math.log(value),
            "cumulative_v2": cumulative_v2,
            "critical_required_v2": critical_required,
            "surplus_v2": surplus,
            "debt_v2": debt,
            "avg_v2_so_far": cumulative_v2 / step,
            "drop_ratio_from_previous": drop_ratio,
        })

    total_steps = rows[-1]["trunk_step"]
    total_v2 = sum(row["v2_from_previous"] for row in rows[1:])
    final_value = rows[-1]["value"]

    summary = {
        "start_value": start_value,
        "final_value": final_value,
        "total_steps": total_steps,
        "total_v2": total_v2,
        "avg_v2": total_v2 / total_steps,
        "critical_v2": CRITICAL_V2,
        "final_surplus_v2": total_v2 - total_steps * CRITICAL_V2,
        "max_debt": max_debt,
        "max_debt_step": max_debt_step,
        "max_value": max_value,
        "max_value_step": max_value_step,
        "total_ratio": final_value / start_value,
        "biggest_drop_step": biggest_drop_step,
        "biggest_drop_from": biggest_drop_from,
        "biggest_drop_to": biggest_drop_to,
        "biggest_drop_ratio": biggest_drop_ratio,
        "biggest_drop_v2": biggest_drop_v2,
    }

    return analyzed, summary


def export_csv(filename: str, rows: list):
    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, summary: dict, analyzed: list):
    lines = []

    lines.append("ANALISI TRONCO COMUNE COLLATZ/SYRACUSE")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Valore iniziale tronco: {summary['start_value']}")
    lines.append(f"Valore finale: {summary['final_value']}")
    lines.append(f"Salti Syracuse totali: {summary['total_steps']}")
    lines.append("")
    lines.append(f"Soglia critica log2(3): {summary['critical_v2']:.9f}")
    lines.append(f"v2 totale accumulato: {summary['total_v2']}")
    lines.append(f"avg_v2 tronco: {summary['avg_v2']:.9f}")
    lines.append(f"surplus_v2 finale: {summary['final_surplus_v2']:.9f}")
    lines.append("")
    lines.append(f"Massimo debito v2: {summary['max_debt']:.9f}")
    lines.append(f"Step massimo debito: {summary['max_debt_step']}")
    lines.append("")
    lines.append(f"Massimo valore nel tronco: {summary['max_value']}")
    lines.append(f"Step massimo valore: {summary['max_value_step']}")
    lines.append("")
    lines.append("Caduta più violenta:")
    lines.append(f"Step: {summary['biggest_drop_step']}")
    lines.append(f"Da: {summary['biggest_drop_from']}")
    lines.append(f"A: {summary['biggest_drop_to']}")
    lines.append(f"v2: {summary['biggest_drop_v2']}")
    lines.append(f"Ratio: {summary['biggest_drop_ratio']:.12f}")
    lines.append("")
    lines.append("Primi 80 step:")
    lines.append("-" * 120)

    for row in analyzed[:80]:
        lines.append(
            f"step={row['trunk_step']:4d} | "
            f"value={row['value']:20d} | "
            f"v2={row['v2_from_previous']:2d} | "
            f"avg_v2={row['avg_v2_so_far']:.6f} | "
            f"surplus={row['surplus_v2']:+.6f} | "
            f"debt={row['debt_v2']:+.6f} | "
            f"ratio_start={row['ratio_to_start']:.12f}"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = read_trunk(INPUT_FILE)
    analyzed, summary = analyze_trunk(rows)

    export_csv(OUTPUT_FILE, analyzed)
    export_summary(SUMMARY_FILE, summary, analyzed)

    print("Analisi tronco comune completata")
    print("-" * 120)
    print(f"Start tronco: {summary['start_value']}")
    print(f"Finale: {summary['final_value']}")
    print(f"Salti: {summary['total_steps']}")
    print(f"avg_v2: {summary['avg_v2']:.9f}")
    print(f"surplus finale: {summary['final_surplus_v2']:.9f}")
    print()
    print(f"Massimo debito: {summary['max_debt']:.9f} allo step {summary['max_debt_step']}")
    print(f"Massimo valore: {summary['max_value']} allo step {summary['max_value_step']}")
    print()
    print("Caduta più violenta:")
    print(
        f"step {summary['biggest_drop_step']} | "
        f"{summary['biggest_drop_from']} -> {summary['biggest_drop_to']} | "
        f"v2={summary['biggest_drop_v2']} | "
        f"ratio={summary['biggest_drop_ratio']:.12f}"
    )
    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
