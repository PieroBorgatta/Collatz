import csv
import math


INPUT_FILE = "collatz_11_confluenze_alte.csv"
OUTPUT_FILE = "collatz_19_analisi_tronchi_dissipativi.csv"
SUMMARY_FILE = "collatz_19_summary_tronchi_dissipativi.txt"

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


def read_common_nodes(filename: str, top_n: int):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            rows.append({
                "common_value": int(row["common_value"]),
                "members_count": int(row["members_count"]),
                "min_step": int(row["min_step"]),
                "max_step": int(row["max_step"]),
                "avg_step": float(row["avg_step"]),
            })

            if len(rows) >= top_n:
                break

    return rows


def analyze_trunk(start: int, max_steps: int = 100_000):
    n = start

    cumulative_v2 = 0
    max_debt = 0.0
    max_debt_step = 0

    min_surplus = 0.0
    min_surplus_step = 0

    max_value = start
    max_value_step = 0

    biggest_drop_ratio = 1.0
    biggest_drop_step = None
    biggest_drop_v2 = None
    biggest_drop_from = None
    biggest_drop_to = None

    seq_v2 = []

    for step in range(1, max_steps + 1):
        previous = n
        n, a = syracuse(n)

        seq_v2.append(a)
        cumulative_v2 += a

        critical = step * CRITICAL_V2
        surplus = cumulative_v2 - critical
        debt = critical - cumulative_v2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if surplus < min_surplus:
            min_surplus = surplus
            min_surplus_step = step

        if n > max_value:
            max_value = n
            max_value_step = step

        drop_ratio = n / previous

        if drop_ratio < biggest_drop_ratio:
            biggest_drop_ratio = drop_ratio
            biggest_drop_step = step
            biggest_drop_v2 = a
            biggest_drop_from = previous
            biggest_drop_to = n

        if n == 1:
            break

    total_steps = step
    total_v2 = cumulative_v2
    avg_v2 = total_v2 / total_steps
    final_surplus = total_v2 - total_steps * CRITICAL_V2

    return {
        "trunk_start": start,
        "reached_one": n == 1,
        "steps_to_1": total_steps,
        "total_v2": total_v2,
        "avg_v2": avg_v2,
        "critical_v2": CRITICAL_V2,
        "final_surplus": final_surplus,
        "max_debt": max_debt,
        "max_debt_step": max_debt_step,
        "min_surplus": min_surplus,
        "min_surplus_step": min_surplus_step,
        "starts_dissipative": max_debt == 0.0,
        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / start,
        "biggest_drop_ratio": biggest_drop_ratio,
        "biggest_drop_step": biggest_drop_step,
        "biggest_drop_v2": biggest_drop_v2,
        "biggest_drop_from": biggest_drop_from,
        "biggest_drop_to": biggest_drop_to,
        "prefix_80_v2": ",".join(map(str, seq_v2[:80])),
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
    dissipative = [r for r in rows if r["starts_dissipative"]]
    non_dissipative = [r for r in rows if not r["starts_dissipative"]]

    rows_by_members = sorted(rows, key=lambda x: x["members_count"], reverse=True)
    rows_by_surplus = sorted(rows, key=lambda x: x["final_surplus"], reverse=True)
    rows_by_debt = sorted(rows, key=lambda x: x["max_debt"], reverse=True)

    lines = []

    lines.append("ANALISI TRONCHI DISSIPATIVI")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Tronchi analizzati: {len(rows)}")
    lines.append(f"Tronchi dissipativi da subito: {len(dissipative)}")
    lines.append(f"Tronchi con debito iniziale: {len(non_dissipative)}")
    lines.append("")
    lines.append("TOP 30 PER MEMBRI")
    lines.append("-" * 120)

    for r in rows_by_members[:30]:
        lines.append(
            f"trunk={r['trunk_start']:15d} | "
            f"members={r['members_count']:4d} | "
            f"steps={r['steps_to_1']:4d} | "
            f"avg_v2={r['avg_v2']:.6f} | "
            f"surplus={r['final_surplus']:+.6f} | "
            f"max_debt={r['max_debt']:.6f} | "
            f"dissipative={r['starts_dissipative']}"
        )

    lines.append("")
    lines.append("TOP 30 PER SURPLUS FINALE")
    lines.append("-" * 120)

    for r in rows_by_surplus[:30]:
        lines.append(
            f"trunk={r['trunk_start']:15d} | "
            f"members={r['members_count']:4d} | "
            f"steps={r['steps_to_1']:4d} | "
            f"avg_v2={r['avg_v2']:.6f} | "
            f"surplus={r['final_surplus']:+.6f} | "
            f"max_debt={r['max_debt']:.6f}"
        )

    lines.append("")
    lines.append("TOP 30 PER MAX_DEBT")
    lines.append("-" * 120)

    for r in rows_by_debt[:30]:
        lines.append(
            f"trunk={r['trunk_start']:15d} | "
            f"members={r['members_count']:4d} | "
            f"steps={r['steps_to_1']:4d} | "
            f"avg_v2={r['avg_v2']:.6f} | "
            f"surplus={r['final_surplus']:+.6f} | "
            f"max_debt={r['max_debt']:.6f}"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    nodes = read_common_nodes(INPUT_FILE, TOP_N)

    rows = []

    print("Analisi tronchi dissipativi")
    print("-" * 120)
    print(f"Tronchi analizzati: {len(nodes)}")
    print()

    for idx, node in enumerate(nodes, start=1):
        analysis = analyze_trunk(node["common_value"])

        row = {
            **node,
            **analysis,
        }

        rows.append(row)

        print(
            f"{idx:3d}) trunk={row['trunk_start']:15d} | "
            f"members={row['members_count']:4d} | "
            f"steps={row['steps_to_1']:4d} | "
            f"avg_v2={row['avg_v2']:.6f} | "
            f"surplus={row['final_surplus']:+.6f} | "
            f"max_debt={row['max_debt']:.6f} | "
            f"diss={row['starts_dissipative']}"
        )

    rows.sort(key=lambda x: (x["members_count"], x["final_surplus"]), reverse=True)

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
