import csv
import math
from statistics import mean


FAMILIES_FILE = "collatz_20_famiglie_tronchi.csv"
DETAIL_FILE = "collatz_20_dettaglio_famiglie_tronchi.txt"
OUTPUT_FILE = "collatz_21_metriche_famiglie.csv"
SUMMARY_FILE = "collatz_21_summary_metriche_famiglie.txt"

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


def parse_csv_families(filename: str):
    families = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            common_values = [
                int(x)
                for x in row["common_values_preview"].split(",")
                if x.strip()
            ]

            members_preview = [
                int(x)
                for x in row["members_preview"].split(",")
                if x.strip()
            ]

            families.append({
                "family_id": row["family_id"],
                "members_count": int(row["members_count"]),
                "nodes_count": int(row["nodes_count"]),
                "max_common_value": int(row["max_common_value"]),
                "min_common_value": int(row["min_common_value"]),
                "max_avg_step": float(row["max_avg_step"]),
                "min_avg_step": float(row["min_avg_step"]),
                "members_preview": members_preview,
                "common_values_preview": common_values,
            })

    return families


def analyze_trunk(start: int, max_steps: int = 200_000):
    n = start
    cumulative_v2 = 0

    max_debt = 0.0
    max_debt_step = 0

    max_value = start
    max_value_step = 0

    biggest_drop_ratio = 1.0
    biggest_drop_v2 = None
    biggest_drop_step = None
    biggest_drop_from = None
    biggest_drop_to = None

    seq_v2 = []

    for step in range(1, max_steps + 1):
        previous = n
        n, a = syracuse(n)

        seq_v2.append(a)
        cumulative_v2 += a

        debt = step * CRITICAL_V2 - cumulative_v2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if n > max_value:
            max_value = n
            max_value_step = step

        ratio = n / previous

        if ratio < biggest_drop_ratio:
            biggest_drop_ratio = ratio
            biggest_drop_v2 = a
            biggest_drop_step = step
            biggest_drop_from = previous
            biggest_drop_to = n

        if n == 1:
            break

    total_steps = step
    total_v2 = cumulative_v2
    avg_v2 = total_v2 / total_steps if total_steps else 0
    final_surplus = total_v2 - total_steps * CRITICAL_V2

    return {
        "steps_to_1": total_steps,
        "total_v2": total_v2,
        "avg_v2": avg_v2,
        "final_surplus": final_surplus,
        "max_debt_trunk": max_debt,
        "max_debt_trunk_step": max_debt_step,
        "trunk_starts_dissipative": max_debt == 0.0,
        "max_value_inside_trunk": max_value,
        "max_value_inside_trunk_step": max_value_step,
        "max_ratio_inside_trunk": max_value / start,
        "biggest_drop_ratio": biggest_drop_ratio,
        "biggest_drop_v2": biggest_drop_v2,
        "biggest_drop_step": biggest_drop_step,
        "biggest_drop_from": biggest_drop_from,
        "biggest_drop_to": biggest_drop_to,
        "prefix_60_v2_trunk": ",".join(map(str, seq_v2[:60])),
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
    by_members = sorted(rows, key=lambda x: x["members_count"], reverse=True)
    by_nodes = sorted(rows, key=lambda x: x["nodes_count"], reverse=True)
    by_height = sorted(rows, key=lambda x: x["max_common_value"], reverse=True)
    by_surplus = sorted(rows, key=lambda x: x["final_surplus"], reverse=True)
    by_dissipation_ratio = sorted(rows, key=lambda x: x["surplus_per_step"], reverse=True)

    dissipative = [r for r in rows if r["trunk_starts_dissipative"]]

    lines = []

    lines.append("METRICHE DELLE FAMIGLIE GRAVITAZIONALI")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Famiglie analizzate: {len(rows)}")
    lines.append(f"Famiglie con tronco dissipativo da subito: {len(dissipative)}")
    lines.append(f"Percentuale dissipative da subito: {len(dissipative) / len(rows):.4f}")
    lines.append("")
    lines.append(f"Media membri: {mean(r['members_count'] for r in rows):.6f}")
    lines.append(f"Media nodi comuni: {mean(r['nodes_count'] for r in rows):.6f}")
    lines.append(f"Media avg_v2 tronco: {mean(r['avg_v2'] for r in rows):.6f}")
    lines.append(f"Media surplus finale: {mean(r['final_surplus'] for r in rows):.6f}")
    lines.append("")

    sections = [
        ("TOP 20 PER MEMBRI", by_members),
        ("TOP 20 PER NODI COMUNI", by_nodes),
        ("TOP 20 PER ALTEZZA MASSIMA", by_height),
        ("TOP 20 PER SURPLUS FINALE", by_surplus),
        ("TOP 20 PER SURPLUS PER STEP", by_dissipation_ratio),
    ]

    for title, data in sections:
        lines.append(title)
        lines.append("-" * 120)

        for r in data[:20]:
            lines.append(
                f"id={r['family_id']} | "
                f"members={r['members_count']:4d} | "
                f"nodes={r['nodes_count']:4d} | "
                f"max_common={r['max_common_value']:15d} | "
                f"steps={r['steps_to_1']:4d} | "
                f"avg_v2={r['avg_v2']:.6f} | "
                f"surplus={r['final_surplus']:+.6f} | "
                f"surplus_step={r['surplus_per_step']:+.6f} | "
                f"max_debt_trunk={r['max_debt_trunk']:.6f} | "
                f"diss={r['trunk_starts_dissipative']}"
            )

        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    families = parse_csv_families(FAMILIES_FILE)

    rows = []

    print("Analisi metriche famiglie gravitazionali")
    print("-" * 120)
    print(f"Famiglie lette: {len(families)}")
    print()

    for idx, fam in enumerate(families, start=1):
        trunk = analyze_trunk(fam["max_common_value"])

        row = {
            "family_rank": idx,
            "family_id": fam["family_id"],
            "members_count": fam["members_count"],
            "nodes_count": fam["nodes_count"],
            "max_common_value": fam["max_common_value"],
            "min_common_value": fam["min_common_value"],
            "common_span": fam["max_common_value"] - fam["min_common_value"],
            "max_avg_step": fam["max_avg_step"],
            "min_avg_step": fam["min_avg_step"],
            **trunk,
        }

        row["surplus_per_step"] = (
            row["final_surplus"] / row["steps_to_1"]
            if row["steps_to_1"]
            else 0
        )

        row["nodes_per_member"] = (
            row["nodes_count"] / row["members_count"]
            if row["members_count"]
            else 0
        )

        rows.append(row)

        print(
            f"{idx:3d}) id={row['family_id']} | "
            f"members={row['members_count']:4d} | "
            f"nodes={row['nodes_count']:4d} | "
            f"max_common={row['max_common_value']:15d} | "
            f"avg_v2={row['avg_v2']:.6f} | "
            f"surplus={row['final_surplus']:+.6f} | "
            f"diss={row['trunk_starts_dissipative']}"
        )

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
