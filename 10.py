import csv
from collections import defaultdict


INPUT_FILE = "collatz_05_top_debito.csv"
OUTPUT_FILE = "collatz_10_confluenze_top_debito.csv"
GROUPS_FILE = "collatz_10_gruppi_confluenza.txt"

TOP_N = 500
MAX_STEPS = 10_000


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
    Restituisce dizionario:
        valore dispari -> primo step in cui appare
    """
    n = start
    seen = {n: 0}

    for step in range(1, max_steps + 1):
        n, _ = syracuse(n)

        if n not in seen:
            seen[n] = step

        if n == 1:
            break

    return seen


def find_first_common(start_a: int, traj_a: dict, start_b: int, traj_b: dict):
    common = set(traj_a.keys()) & set(traj_b.keys())

    if not common:
        return None

    best = min(
        common,
        key=lambda x: traj_a[x] + traj_b[x]
    )

    return {
        "a": start_a,
        "b": start_b,
        "common_value": best,
        "step_a": traj_a[best],
        "step_b": traj_b[best],
        "total_steps_to_common": traj_a[best] + traj_b[best],
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_groups(filename: str, root_groups: dict):
    lines = []

    lines.append("GRUPPI DI CONFLUENZA")
    lines.append("=" * 120)
    lines.append("Ogni gruppo raccoglie i numeri che condividono un valore comune nella traiettoria.")
    lines.append("")

    sorted_groups = sorted(
        root_groups.items(),
        key=lambda item: len(item[1]),
        reverse=True
    )

    for common_value, members in sorted_groups:
        lines.append("-" * 120)
        lines.append(f"Valore comune: {common_value}")
        lines.append(f"Numero membri: {len(members)}")
        lines.append("Membri:")
        lines.append(", ".join(map(str, sorted(members))))
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    numbers = read_top_numbers(INPUT_FILE, TOP_N)

    print("Analisi confluenze tra traiettorie Syracuse")
    print(f"Numeri analizzati: {len(numbers)}")
    print("-" * 140)

    trajectories = {}

    for i, n in enumerate(numbers, start=1):
        trajectories[n] = build_trajectory(n)

        if i % 50 == 0:
            print(f"Traiettorie costruite: {i}")

    pair_rows = []
    root_groups = defaultdict(set)

    total_pairs = len(numbers) * (len(numbers) - 1) // 2
    checked = 0

    for i in range(len(numbers)):
        a = numbers[i]
        traj_a = trajectories[a]

        for j in range(i + 1, len(numbers)):
            b = numbers[j]
            traj_b = trajectories[b]

            result = find_first_common(a, traj_a, b, traj_b)

            if result:
                pair_rows.append(result)

                common_value = result["common_value"]
                root_groups[common_value].add(a)
                root_groups[common_value].add(b)

            checked += 1

        if (i + 1) % 25 == 0:
            print(f"Coppie controllate circa: {checked}/{total_pairs}")

    pair_rows.sort(
        key=lambda x: (
            x["common_value"],
            x["total_steps_to_common"]
        )
    )

    export_csv(OUTPUT_FILE, pair_rows)
    export_groups(GROUPS_FILE, root_groups)

    print()
    print(f"Coppie con confluenza trovate: {len(pair_rows)}")
    print(f"Valori comuni distinti: {len(root_groups)}")
    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Gruppi generati: {GROUPS_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{GROUPS_FILE}'")

    print()
    print("Prime 30 confluenze:")
    print("-" * 140)

    for row in pair_rows[:30]:
        print(
            f"{row['a']:10d} + {row['b']:10d} -> "
            f"common={row['common_value']:12d} | "
            f"step_a={row['step_a']:4d} | "
            f"step_b={row['step_b']:4d} | "
            f"tot={row['total_steps_to_common']:4d}"
        )


if __name__ == "__main__":
    main()
