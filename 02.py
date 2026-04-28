import csv
import math
from collections import defaultdict


def v2(x: int) -> int:
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def syracuse(n: int) -> int:
    x = 3 * n + 1
    return x >> v2(x)


def analyze_descent_time(limit: int, m: int, max_steps: int):
    modulus = 2 ** m

    class_stats = defaultdict(lambda: {
        "count": 0,
        "sum_first_descent": 0,
        "max_first_descent": 0,
        "no_descent_count": 0,
        "sum_max_ratio": 0.0,
        "max_ratio": 0.0,
        "sum_final_ratio": 0.0,
        "max_final_ratio": 0.0,
        "min_final_ratio": 10**18,
    })

    dangerous_numbers = []

    for start in range(3, limit + 1, 2):
        n = start
        cls = start % modulus

        first_descent = None
        max_value = start
        max_ratio = 1.0

        for step in range(1, max_steps + 1):
            n = syracuse(n)

            if n > max_value:
                max_value = n

            current_ratio = n / start
            if current_ratio > max_ratio:
                max_ratio = current_ratio

            if n < start and first_descent is None:
                first_descent = step
                break

        if first_descent is None:
            first_descent_value = max_steps + 1
            no_descent = 1
        else:
            first_descent_value = first_descent
            no_descent = 0

        final_ratio = n / start

        data = class_stats[cls]
        data["count"] += 1
        data["sum_first_descent"] += first_descent_value
        data["max_first_descent"] = max(data["max_first_descent"], first_descent_value)
        data["no_descent_count"] += no_descent
        data["sum_max_ratio"] += max_ratio
        data["max_ratio"] = max(data["max_ratio"], max_ratio)
        data["sum_final_ratio"] += final_ratio
        data["max_final_ratio"] = max(data["max_final_ratio"], final_ratio)
        data["min_final_ratio"] = min(data["min_final_ratio"], final_ratio)

        if first_descent is None or first_descent_value >= 8 or max_ratio >= 10:
            dangerous_numbers.append({
                "start": start,
                "classe_mod": cls,
                "first_descent_step": first_descent_value,
                "no_descent_within_max_steps": no_descent,
                "max_value": max_value,
                "max_ratio": max_ratio,
                "final_value": n,
                "final_ratio": final_ratio,
            })

    class_rows = []

    for cls, data in class_stats.items():
        count = data["count"]

        class_rows.append({
            "classe_mod": cls,
            "count": count,
            "avg_first_descent": data["sum_first_descent"] / count,
            "max_first_descent": data["max_first_descent"],
            "no_descent_count": data["no_descent_count"],
            "no_descent_ratio": data["no_descent_count"] / count,
            "avg_max_ratio": data["sum_max_ratio"] / count,
            "max_ratio": data["max_ratio"],
            "avg_final_ratio": data["sum_final_ratio"] / count,
            "max_final_ratio": data["max_final_ratio"],
            "min_final_ratio": data["min_final_ratio"],
        })

    class_rows.sort(
        key=lambda x: (
            x["no_descent_ratio"],
            x["avg_first_descent"],
            x["max_ratio"]
        ),
        reverse=True
    )

    dangerous_numbers.sort(
        key=lambda x: (
            x["no_descent_within_max_steps"],
            x["first_descent_step"],
            x["max_ratio"]
        ),
        reverse=True
    )

    return class_rows, dangerous_numbers


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_class_summary(class_rows, top_n: int):
    print("Classi modulo più pericolose su più salti:")
    print("-" * 130)

    for row in class_rows[:top_n]:
        print(
            f"classe {row['classe_mod']:4d} | "
            f"avg_first_descent={row['avg_first_descent']:.3f} | "
            f"max_first_descent={row['max_first_descent']:2d} | "
            f"no_descent_ratio={row['no_descent_ratio']:.4f} | "
            f"avg_max_ratio={row['avg_max_ratio']:.3f} | "
            f"max_ratio={row['max_ratio']:.3f}"
        )


def print_dangerous_summary(dangerous_numbers, top_n: int):
    print()
    print("Numeri più resistenti trovati:")
    print("-" * 130)

    for row in dangerous_numbers[:top_n]:
        print(
            f"n={row['start']:10d} | "
            f"classe={row['classe_mod']:4d} | "
            f"first_descent={row['first_descent_step']:2d} | "
            f"max_ratio={row['max_ratio']:.3f} | "
            f"max_value={row['max_value']:15d} | "
            f"final_ratio={row['final_ratio']:.3f}"
        )


if __name__ == "__main__":
    LIMIT = 5_000_000
    M = 10
    MAX_STEPS = 40

    print("Analisi Collatz/Syracuse su blocchi di più salti")
    print(f"Numeri dispari analizzati fino a: {LIMIT:,}".replace(",", "."))
    print(f"Modulo: 2^{M} = {2 ** M}")
    print(f"Numero massimo di salti Syracuse controllati: {MAX_STEPS}")
    print()

    class_rows, dangerous_numbers = analyze_descent_time(
        limit=LIMIT,
        m=M,
        max_steps=MAX_STEPS
    )

    class_file = f"collatz_classi_multistep_mod_2^{M}_limit_{LIMIT}_steps_{MAX_STEPS}.csv"
    dangerous_file = f"collatz_numeri_resistenti_limit_{LIMIT}_steps_{MAX_STEPS}.csv"

    export_csv(class_file, class_rows)
    export_csv(dangerous_file, dangerous_numbers)

    print_class_summary(class_rows, top_n=30)
    print_dangerous_summary(dangerous_numbers, top_n=30)

    print()
    print(f"File classi generato: {class_file}")
    print(f"File numeri resistenti generato: {dangerous_file}")

    print()
    print("Per aprirli su Mac:")
    print(f"open '{class_file}'")
    print(f"open '{dangerous_file}'")
