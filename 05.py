import csv
import math


CRITICAL_V2 = math.log2(3)


def v2(x: int) -> int:
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def syracuse(n: int) -> tuple[int, int]:
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


def analyze_number(start: int, max_steps: int = 10_000):
    n = start

    cumulative_v2 = 0
    max_debt = 0.0
    max_debt_step = 0

    max_value = start
    max_ratio = 1.0
    peak_step = 0

    first_positive_surplus_step = None
    first_descent_step = None

    consecutive_v2_1 = 0
    max_consecutive_v2_1 = 0

    reached_one = False

    for step in range(1, max_steps + 1):
        n, a = syracuse(n)

        cumulative_v2 += a

        critical_required = step * CRITICAL_V2
        surplus = cumulative_v2 - critical_required
        debt = critical_required - cumulative_v2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if a == 1:
            consecutive_v2_1 += 1
        else:
            consecutive_v2_1 = 0

        if consecutive_v2_1 > max_consecutive_v2_1:
            max_consecutive_v2_1 = consecutive_v2_1

        ratio = n / start

        if n > max_value:
            max_value = n
            max_ratio = ratio
            peak_step = step

        if first_positive_surplus_step is None and surplus > 0:
            first_positive_surplus_step = step

        if first_descent_step is None and n < start:
            first_descent_step = step

        if n == 1:
            reached_one = True
            break

    total_steps = step
    avg_v2 = cumulative_v2 / total_steps if total_steps else 0

    return {
        "start": start,
        "classe_mod_1024": start % 1024,
        "reached_one": reached_one,
        "total_syracuse_steps": total_steps,
        "max_value": max_value,
        "max_ratio": max_ratio,
        "peak_step": peak_step,
        "first_positive_surplus_step": first_positive_surplus_step,
        "first_descent_step": first_descent_step,
        "max_debt": max_debt,
        "max_debt_step": max_debt_step,
        "max_consecutive_v2_1": max_consecutive_v2_1,
        "total_v2": cumulative_v2,
        "avg_v2": avg_v2,
        "final_surplus": cumulative_v2 - total_steps * CRITICAL_V2,
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def main():
    LIMIT = 5_000_000
    MAX_STEPS = 10_000

    rows = []

    print("Analisi debito gravitazionale Collatz/Syracuse")
    print(f"Limite: {LIMIT:,}".replace(",", "."))
    print(f"Soglia critica log2(3): {CRITICAL_V2:.9f}")
    print("-" * 120)

    processed = 0

    for start in range(3, LIMIT + 1, 2):
        row = analyze_number(start, max_steps=MAX_STEPS)
        rows.append(row)

        processed += 1

        if processed % 100_000 == 0:
            print(f"Analizzati {processed:,} numeri dispari...".replace(",", "."))

    by_debt = sorted(rows, key=lambda x: x["max_debt"], reverse=True)
    by_ratio = sorted(rows, key=lambda x: x["max_ratio"], reverse=True)
    by_descent = sorted(rows, key=lambda x: x["first_descent_step"] or 0, reverse=True)

    export_csv("collatz_05_tutti_debito.csv", rows)
    export_csv("collatz_05_top_debito.csv", by_debt[:500])
    export_csv("collatz_05_top_ratio.csv", by_ratio[:500])
    export_csv("collatz_05_top_rientro_tardivo.csv", by_descent[:500])

    print()
    print("Top 30 per massimo debito gravitazionale:")
    print("-" * 120)

    for row in by_debt[:30]:
        print(
            f"n={row['start']:10d} | "
            f"max_debt={row['max_debt']:8.3f} | "
            f"debt_step={row['max_debt_step']:4d} | "
            f"peak_step={row['peak_step']:4d} | "
            f"first_surplus={row['first_positive_surplus_step']} | "
            f"first_descent={row['first_descent_step']} | "
            f"max_ratio={row['max_ratio']:12.3f} | "
            f"max_v2_1_run={row['max_consecutive_v2_1']:3d}"
        )

    print()
    print("File generati:")
    print("collatz_05_tutti_debito.csv")
    print("collatz_05_top_debito.csv")
    print("collatz_05_top_ratio.csv")
    print("collatz_05_top_rientro_tardivo.csv")

    print()
    print("Per aprirli:")
    print("open 'collatz_05_top_debito.csv'")
    print("open 'collatz_05_top_ratio.csv'")
    print("open 'collatz_05_top_rientro_tardivo.csv'")


if __name__ == "__main__":
    main()
