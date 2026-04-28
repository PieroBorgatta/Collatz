import csv
import math
from collections import Counter


INPUT_FILE = "collatz_05_top_debito.csv"
OUTPUT_FILE = "collatz_07_rientro_definitivo.csv"
TOP_N = 500

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


def analyze_number(start: int, max_steps: int = 100_000):
    n = start

    seq_v2 = []
    values = [start]

    cumulative_v2 = 0
    max_debt = 0.0
    max_debt_step = 0

    max_value = start
    peak_step = 0
    max_ratio = 1.0

    first_descent_step = None
    first_positive_surplus_step = None

    last_above_start_step = 0

    for step in range(1, max_steps + 1):
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
            peak_step = step
            max_ratio = n / start

        if first_descent_step is None and n < start:
            first_descent_step = step

        if first_positive_surplus_step is None and surplus > 0:
            first_positive_surplus_step = step

        if n >= start:
            last_above_start_step = step

        if n == 1:
            break

    reached_one = n == 1
    total_steps = len(seq_v2)

    final_descent_step = last_above_start_step + 1

    counter = Counter(seq_v2)

    count_1 = counter.get(1, 0)
    count_2 = counter.get(2, 0)
    count_3 = counter.get(3, 0)
    count_4_plus = sum(v for k, v in counter.items() if k >= 4)

    avg_v2 = sum(seq_v2) / total_steps if total_steps else 0

    return {
        "start": start,
        "classe_mod_1024": start % 1024,
        "reached_one": reached_one,
        "total_steps": total_steps,

        "first_descent_step": first_descent_step,
        "final_descent_step": final_descent_step,
        "last_above_start_step": last_above_start_step,

        "first_positive_surplus_step": first_positive_surplus_step,

        "peak_step": peak_step,
        "max_value": max_value,
        "max_ratio": max_ratio,

        "max_debt": max_debt,
        "max_debt_step": max_debt_step,

        "max_run_1": longest_run(seq_v2, 1),

        "count_1": count_1,
        "count_2": count_2,
        "count_3": count_3,
        "count_4_plus": count_4_plus,

        "ratio_1": count_1 / total_steps if total_steps else 0,
        "ratio_2": count_2 / total_steps if total_steps else 0,
        "ratio_3": count_3 / total_steps if total_steps else 0,
        "ratio_4_plus": count_4_plus / total_steps if total_steps else 0,

        "total_v2": sum(seq_v2),
        "avg_v2": avg_v2,
        "final_surplus": sum(seq_v2) - total_steps * CRITICAL_V2,

        "prefix_50": ",".join(map(str, seq_v2[:50])),
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def main():
    numbers = read_top_numbers(INPUT_FILE, TOP_N)

    rows = []

    print("Analisi rientro definitivo sotto lo start")
    print(f"Numeri analizzati: {len(numbers)}")
    print("-" * 140)

    for start in numbers:
        row = analyze_number(start)
        rows.append(row)

        print(
            f"n={start:10d} | "
            f"peak={row['peak_step']:4d} | "
            f"first_down={row['first_descent_step']:4d} | "
            f"final_down={row['final_descent_step']:4d} | "
            f"last_above={row['last_above_start_step']:4d} | "
            f"max_debt={row['max_debt']:8.3f} | "
            f"max_ratio={row['max_ratio']:12.3f} | "
            f"avg_v2={row['avg_v2']:.3f}"
        )

    rows.sort(
        key=lambda x: (
            x["final_descent_step"],
            x["max_debt"],
            x["max_ratio"],
        ),
        reverse=True
    )

    export_csv(OUTPUT_FILE, rows)

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print()
    print("Top 30 per rientro definitivo più tardivo:")
    print("-" * 140)

    for row in rows[:30]:
        print(
            f"n={row['start']:10d} | "
            f"final_down={row['final_descent_step']:4d} | "
            f"peak={row['peak_step']:4d} | "
            f"max_debt={row['max_debt']:8.3f} | "
            f"max_ratio={row['max_ratio']:12.3f} | "
            f"max_run_1={row['max_run_1']:3d} | "
            f"ratio_1={row['ratio_1']:.3f} | "
            f"avg_v2={row['avg_v2']:.3f}"
        )

    print()
    print("Per aprirlo:")
    print(f"open '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
