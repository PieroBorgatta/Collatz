import csv
from collections import defaultdict


INPUT_FILE = "collatz_05_top_debito.csv"
OUTPUT_FILE = "collatz_11_confluenze_alte.csv"
GROUPS_FILE = "collatz_11_gruppi_confluenza_alta.txt"

TOP_N = 500
MAX_STEPS = 10_000

# Ignoriamo i nodi troppo bassi perché sono la coda banale verso 1.
MIN_COMMON_VALUE = 10_000


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


def build_trajectory(start: int, max_steps: int = MAX_STEPS):
    """
    Restituisce lista di tuple:
        (step, value)
    solo per i dispari della mappa Syracuse.
    """
    n = start
    trajectory = [(0, n)]

    for step in range(1, max_steps + 1):
        n, _ = syracuse(n)
        trajectory.append((step, n))

        if n == 1:
            break

    return trajectory


def main():
    numbers = read_top_numbers(INPUT_FILE, TOP_N)

    print("Analisi confluenze alte tra traiettorie Syracuse")
    print(f"Numeri analizzati: {len(numbers)}")
    print(f"Valori comuni considerati solo se >= {MIN_COMMON_VALUE}")
    print("-" * 140)

    value_to_members = defaultdict(list)

    for idx, start in enumerate(numbers, start=1):
        trajectory = build_trajectory(start)

        for step, value in trajectory:
            if value >= MIN_COMMON_VALUE:
                value_to_members[value].append((start, step))

        if idx % 50 == 0:
            print(f"Traiettorie costruite: {idx}")

    rows = []

    for value, members in value_to_members.items():
        unique_starts = sorted(set(start for start, step in members))

        if len(unique_starts) < 2:
            continue

        steps = [step for start, step in members]

        rows.append({
            "common_value": value,
            "members_count": len(unique_starts),
            "min_step": min(steps),
            "max_step": max(steps),
            "avg_step": sum(steps) / len(steps),
            "members": ",".join(map(str, unique_starts)),
        })

    rows.sort(
        key=lambda x: (
            x["members_count"],
            x["common_value"]
        ),
        reverse=True
    )

    export_csv(OUTPUT_FILE, rows)
    export_groups(GROUPS_FILE, rows)

    print()
    print(f"Nodi di confluenza alta trovati: {len(rows)}")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"TXT generato: {GROUPS_FILE}")

    print()
    print("Top 30 nodi di confluenza alta:")
    print("-" * 140)

    for row in rows[:30]:
        print(
            f"common={row['common_value']:15d} | "
            f"members={row['members_count']:4d} | "
            f"min_step={row['min_step']:4d} | "
            f"max_step={row['max_step']:4d} | "
            f"avg_step={row['avg_step']:.2f}"
        )

    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{GROUPS_FILE}'")


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_groups(filename: str, rows: list):
    lines = []

    lines.append("GRUPPI DI CONFLUENZA ALTA")
    lines.append("=" * 120)
    lines.append(f"Considerati solo valori comuni >= {MIN_COMMON_VALUE}")
    lines.append("")

    for row in rows[:200]:
        lines.append("-" * 120)
        lines.append(f"Valore comune: {row['common_value']}")
        lines.append(f"Numero membri: {row['members_count']}")
        lines.append(f"Step minimo: {row['min_step']}")
        lines.append(f"Step massimo: {row['max_step']}")
        lines.append(f"Step medio: {row['avg_step']:.3f}")
        lines.append("")
        lines.append("Membri:")
        lines.append(row["members"])
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
