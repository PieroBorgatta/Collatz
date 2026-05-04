import csv
import math
from collections import Counter


INPUT_FILE = "collatz_05_top_debito.csv"
OUTPUT_FILE = "collatz_06_pattern_v2_top_debito.csv"
SEQUENCES_FILE = "collatz_06_sequenze_v2_top_debito.txt"

TOP_N = 100
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


def read_top_numbers(filename: str, top_n: int):
    numbers = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            numbers.append(int(row["start"]))

            if len(numbers) >= top_n:
                break

    return numbers


def analyze_v2_pattern(start: int, max_steps: int = 10_000):
    n = start
    seq = []

    cumulative_v2 = 0
    max_debt = 0.0
    max_debt_step = 0

    max_value = start
    peak_step = 0

    first_surplus_step = None
    first_descent_step = None

    for step in range(1, max_steps + 1):
        n, a = syracuse(n)
        seq.append(a)

        cumulative_v2 += a

        debt = step * CRITICAL_V2 - cumulative_v2
        surplus = cumulative_v2 - step * CRITICAL_V2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if n > max_value:
            max_value = n
            peak_step = step

        if first_surplus_step is None and surplus > 0:
            first_surplus_step = step

        if first_descent_step is None and n < start:
            first_descent_step = step

        if n == 1:
            break

    counter = Counter(seq)

    count_1 = counter.get(1, 0)
    count_2 = counter.get(2, 0)
    count_3 = counter.get(3, 0)
    count_4_plus = sum(v for k, v in counter.items() if k >= 4)

    max_run_1 = longest_run(seq, 1)

    seq_until_debt_peak = seq[:max_debt_step]
    seq_until_peak = seq[:peak_step]
    seq_until_descent = seq[:first_descent_step] if first_descent_step else seq

    return {
        "start": start,
        "classe_mod_1024": start % 1024,
        "steps_total": len(seq),
        "max_value": max_value,
        "peak_step": peak_step,
        "max_debt": max_debt,
        "max_debt_step": max_debt_step,
        "first_surplus_step": first_surplus_step,
        "first_descent_step": first_descent_step,
        "max_run_1": max_run_1,
        "count_1": count_1,
        "count_2": count_2,
        "count_3": count_3,
        "count_4_plus": count_4_plus,
        "ratio_1": count_1 / len(seq),
        "ratio_2": count_2 / len(seq),
        "ratio_3": count_3 / len(seq),
        "ratio_4_plus": count_4_plus / len(seq),
        "avg_v2": sum(seq) / len(seq),
        "prefix_30": ",".join(map(str, seq[:30])),
        "until_debt_peak": ",".join(map(str, seq_until_debt_peak)),
        "until_peak": ",".join(map(str, seq_until_peak)),
        "until_descent": ",".join(map(str, seq_until_descent)),
        "full_sequence": ",".join(map(str, seq)),
    }


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


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_sequences(filename: str, rows: list):
    lines = []

    for row in rows:
        lines.append("=" * 120)
        lines.append(f"n = {row['start']}")
        lines.append(f"classe mod 1024 = {row['classe_mod_1024']}")
        lines.append(f"max_debt = {row['max_debt']:.6f}")
        lines.append(f"max_debt_step = {row['max_debt_step']}")
        lines.append(f"peak_step = {row['peak_step']}")
        lines.append(f"first_descent_step = {row['first_descent_step']}")
        lines.append(f"max_run_1 = {row['max_run_1']}")
        lines.append(f"avg_v2 = {row['avg_v2']:.6f}")
        lines.append("")
        lines.append("Sequenza fino al massimo debito:")
        lines.append(row["until_debt_peak"])
        lines.append("")
        lines.append("Sequenza fino al rientro sotto start:")
        lines.append(row["until_descent"])
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    numbers = read_top_numbers(INPUT_FILE, TOP_N)

    rows = []

    print("Analisi pattern v2 sui top debito")
    print(f"Numeri analizzati: {len(numbers)}")
    print("-" * 120)

    for n in numbers:
        row = analyze_v2_pattern(n)
        rows.append(row)

        print(
            f"n={n:10d} | "
            f"max_debt={row['max_debt']:8.3f} | "
            f"debt_step={row['max_debt_step']:4d} | "
            f"max_run_1={row['max_run_1']:3d} | "
            f"ratio_1={row['ratio_1']:.3f} | "
            f"avg_v2={row['avg_v2']:.3f}"
        )

    rows.sort(key=lambda x: x["max_debt"], reverse=True)

    export_csv(OUTPUT_FILE, rows)
    export_sequences(SEQUENCES_FILE, rows)

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Sequenze generate: {SEQUENCES_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SEQUENCES_FILE}'")


if __name__ == "__main__":
    main()
