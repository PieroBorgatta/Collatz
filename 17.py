import csv
import math
from collections import Counter


TREE_FILE = "collatz_16_albero_inverso_tronco_CORRETTO.csv"
MEMBERS_FILE = "collatz_13_ingressi_autostrada.csv"

OUTPUT_FILE = "collatz_17_confronto_membri_extra.csv"
SUMMARY_FILE = "collatz_17_summary_confronto_membri_extra.txt"

TARGET_LIMIT = 5_000_000
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


def read_tree_nodes(filename: str):
    nodes = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            value = int(row["value"])

            if value <= TARGET_LIMIT:
                nodes.append(value)

    return sorted(set(nodes))


def read_expected_members(filename: str):
    members = set()

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            members.add(int(row["start"]))

    return members


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


def analyze_until_trunk(start: int):
    n = start

    seq_v2 = []
    cumulative_v2 = 0

    max_debt = 0.0
    max_debt_step = 0

    max_value = start
    max_value_step = 0

    first_positive_surplus_step = None
    first_descent_step = None

    for step in range(1, 200_000):
        n, a = syracuse(n)

        seq_v2.append(a)
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

        if n == TRUNK_VALUE:
            break

    counter = Counter(seq_v2)
    steps = len(seq_v2)
    total_v2 = sum(seq_v2)

    return {
        "start": start,
        "entry_step": steps,
        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / start,

        "max_debt": max_debt,
        "max_debt_step": max_debt_step,

        "total_v2_pre_trunk": total_v2,
        "avg_v2_pre_trunk": total_v2 / steps if steps else 0,
        "final_surplus_at_trunk": total_v2 - steps * CRITICAL_V2,
        "final_debt_at_trunk": steps * CRITICAL_V2 - total_v2,

        "count_1": counter.get(1, 0),
        "count_2": counter.get(2, 0),
        "count_3": counter.get(3, 0),
        "count_4_plus": sum(v for k, v in counter.items() if k >= 4),

        "ratio_1": counter.get(1, 0) / steps if steps else 0,
        "ratio_2": counter.get(2, 0) / steps if steps else 0,
        "ratio_3": counter.get(3, 0) / steps if steps else 0,
        "ratio_4_plus": sum(v for k, v in counter.items() if k >= 4) / steps if steps else 0,

        "max_run_1": longest_run(seq_v2, 1),

        "first_positive_surplus_step": first_positive_surplus_step,
        "first_descent_step": first_descent_step,

        "mod_1024": start % 1024,
        "mod_4096": start % 4096,
        "mod_65536": start % 65536,

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


def avg(rows, key):
    if not rows:
        return 0

    return sum(float(r[key]) for r in rows) / len(rows)


def export_summary(filename: str, rows: list):
    members = [r for r in rows if r["is_top_member"]]
    extras = [r for r in rows if not r["is_top_member"]]

    rows_by_debt = sorted(rows, key=lambda x: x["max_debt"], reverse=True)
    rows_by_ratio = sorted(rows, key=lambda x: x["max_ratio"], reverse=True)

    lines = []

    lines.append("CONFRONTO MEMBRI TOP-DEBITO VS EXTRA DELL'ALBERO INVERSO")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Nodi totali sotto limite: {len(rows)}")
    lines.append(f"Membri top-debito: {len(members)}")
    lines.append(f"Extra: {len(extras)}")
    lines.append("")
    lines.append("MEDIE")
    lines.append("-" * 120)
    lines.append(f"max_debt medio membri: {avg(members, 'max_debt'):.6f}")
    lines.append(f"max_debt medio extra:   {avg(extras, 'max_debt'):.6f}")
    lines.append("")
    lines.append(f"max_ratio medio membri: {avg(members, 'max_ratio'):.6f}")
    lines.append(f"max_ratio medio extra:   {avg(extras, 'max_ratio'):.6f}")
    lines.append("")
    lines.append(f"entry_step medio membri: {avg(members, 'entry_step'):.6f}")
    lines.append(f"entry_step medio extra:   {avg(extras, 'entry_step'):.6f}")
    lines.append("")
    lines.append(f"avg_v2 medio membri: {avg(members, 'avg_v2_pre_trunk'):.6f}")
    lines.append(f"avg_v2 medio extra:   {avg(extras, 'avg_v2_pre_trunk'):.6f}")
    lines.append("")
    lines.append(f"ratio_1 medio membri: {avg(members, 'ratio_1'):.6f}")
    lines.append(f"ratio_1 medio extra:   {avg(extras, 'ratio_1'):.6f}")
    lines.append("")
    lines.append("TOP 30 PER MAX_DEBT")
    lines.append("-" * 120)

    for r in rows_by_debt[:30]:
        tag = "MEMBER" if r["is_top_member"] else "EXTRA "
        lines.append(
            f"{tag} | n={r['start']:10d} | "
            f"entry={r['entry_step']:4d} | "
            f"max_debt={r['max_debt']:9.6f} | "
            f"max_ratio={r['max_ratio']:12.3f} | "
            f"avg_v2={r['avg_v2_pre_trunk']:.6f} | "
            f"ratio_1={r['ratio_1']:.6f} | "
            f"max_run_1={r['max_run_1']}"
        )

    lines.append("")
    lines.append("TOP 30 PER MAX_RATIO")
    lines.append("-" * 120)

    for r in rows_by_ratio[:30]:
        tag = "MEMBER" if r["is_top_member"] else "EXTRA "
        lines.append(
            f"{tag} | n={r['start']:10d} | "
            f"entry={r['entry_step']:4d} | "
            f"max_ratio={r['max_ratio']:12.3f} | "
            f"max_debt={r['max_debt']:9.6f} | "
            f"avg_v2={r['avg_v2_pre_trunk']:.6f} | "
            f"ratio_1={r['ratio_1']:.6f} | "
            f"max_run_1={r['max_run_1']}"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    nodes = read_tree_nodes(TREE_FILE)
    expected_members = read_expected_members(MEMBERS_FILE)

    print("Confronto nodi dell'albero inverso sotto 5M")
    print("-" * 120)
    print(f"Nodi sotto limite: {len(nodes)}")
    print(f"Membri top attesi: {len(expected_members)}")
    print()

    rows = []

    for idx, n in enumerate(nodes, start=1):
        row = analyze_until_trunk(n)
        row["is_top_member"] = n in expected_members
        rows.append(row)

        tag = "MEMBER" if row["is_top_member"] else "EXTRA "

        print(
            f"{idx:3d}) {tag} | "
            f"n={n:10d} | "
            f"entry={row['entry_step']:4d} | "
            f"max_debt={row['max_debt']:9.6f} | "
            f"max_ratio={row['max_ratio']:12.3f} | "
            f"avg_v2={row['avg_v2_pre_trunk']:.6f} | "
            f"ratio_1={row['ratio_1']:.3f}"
        )

    rows.sort(key=lambda x: x["max_debt"], reverse=True)

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
