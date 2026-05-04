import csv
import math
from collections import Counter


INPUT_FILE = "collatz_11_confluenze_alte.csv"
OUTPUT_FILE = "collatz_12_struttura_gruppi_alti.csv"
DETAIL_FILE = "collatz_12_dettaglio_gruppi_alti.txt"

TOP_GROUPS = 50


def read_groups(filename: str, top_n: int):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            members = [int(x) for x in row["members"].split(",") if x.strip()]

            rows.append({
                "common_value": int(row["common_value"]),
                "members_count": int(row["members_count"]),
                "min_step": int(row["min_step"]),
                "max_step": int(row["max_step"]),
                "avg_step": float(row["avg_step"]),
                "members": sorted(members),
            })

            if len(rows) >= top_n:
                break

    return rows


def gcd_list(values):
    if not values:
        return 0

    g = abs(values[0])

    for v in values[1:]:
        g = math.gcd(g, abs(v))

    return g


def v2(x: int) -> int:
    if x == 0:
        return 999999

    count = 0

    while x % 2 == 0:
        x //= 2
        count += 1

    return count


def analyze_group(group):
    members = group["members"]

    diffs_from_first = [m - members[0] for m in members[1:]]
    consecutive_diffs = [
        members[i + 1] - members[i]
        for i in range(len(members) - 1)
    ]

    gcd_from_first = gcd_list(diffs_from_first)
    gcd_consecutive = gcd_list(consecutive_diffs)

    v2_gcd_from_first = v2(gcd_from_first) if gcd_from_first else None
    v2_gcd_consecutive = v2(gcd_consecutive) if gcd_consecutive else None

    moduli = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 65536]

    mod_stats = {}

    for mod in moduli:
        residues = [m % mod for m in members]
        counter = Counter(residues)

        mod_stats[mod] = {
            "distinct": len(counter),
            "most_common_residue": counter.most_common(1)[0][0],
            "most_common_count": counter.most_common(1)[0][1],
            "residues_preview": ",".join(map(str, sorted(counter.keys())[:20])),
        }

    return {
        "common_value": group["common_value"],
        "members_count": group["members_count"],
        "min_step": group["min_step"],
        "max_step": group["max_step"],
        "avg_step": group["avg_step"],

        "min_member": min(members),
        "max_member": max(members),
        "span": max(members) - min(members),

        "gcd_diffs_from_first": gcd_from_first,
        "v2_gcd_diffs_from_first": v2_gcd_from_first,
        "gcd_consecutive_diffs": gcd_consecutive,
        "v2_gcd_consecutive_diffs": v2_gcd_consecutive,

        "distinct_mod_64": mod_stats[64]["distinct"],
        "distinct_mod_128": mod_stats[128]["distinct"],
        "distinct_mod_256": mod_stats[256]["distinct"],
        "distinct_mod_512": mod_stats[512]["distinct"],
        "distinct_mod_1024": mod_stats[1024]["distinct"],
        "distinct_mod_2048": mod_stats[2048]["distinct"],
        "distinct_mod_4096": mod_stats[4096]["distinct"],
        "distinct_mod_8192": mod_stats[8192]["distinct"],
        "distinct_mod_65536": mod_stats[65536]["distinct"],

        "common_residue_mod_1024": mod_stats[1024]["most_common_residue"],
        "common_residue_mod_1024_count": mod_stats[1024]["most_common_count"],

        "members": ",".join(map(str, members)),
        "mod_stats": mod_stats,
        "consecutive_diffs": consecutive_diffs,
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    clean_rows = []

    for row in rows:
        r = dict(row)
        r.pop("mod_stats", None)
        r.pop("consecutive_diffs", None)
        clean_rows.append(r)

    fieldnames = list(clean_rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(clean_rows)


def export_detail(filename: str, rows: list):
    lines = []

    lines.append("STRUTTURA DEI GRUPPI DI CONFLUENZA ALTA")
    lines.append("=" * 120)
    lines.append("")

    for idx, row in enumerate(rows, start=1):
        lines.append("-" * 120)
        lines.append(f"Gruppo #{idx}")
        lines.append(f"Valore comune: {row['common_value']}")
        lines.append(f"Membri: {row['members_count']}")
        lines.append(f"Step medio: {row['avg_step']:.3f}")
        lines.append("")
        lines.append(f"Min membro: {row['min_member']}")
        lines.append(f"Max membro: {row['max_member']}")
        lines.append(f"Span: {row['span']}")
        lines.append("")
        lines.append(f"GCD differenze dal primo: {row['gcd_diffs_from_first']}")
        lines.append(f"v2(GCD differenze dal primo): {row['v2_gcd_diffs_from_first']}")
        lines.append(f"GCD differenze consecutive: {row['gcd_consecutive_diffs']}")
        lines.append(f"v2(GCD differenze consecutive): {row['v2_gcd_consecutive_diffs']}")
        lines.append("")
        lines.append("Statistiche residue:")
        for mod, stat in row["mod_stats"].items():
            lines.append(
                f"mod {mod:6d} | "
                f"residui distinti={stat['distinct']:4d} | "
                f"residuo più comune={stat['most_common_residue']:6d} | "
                f"count={stat['most_common_count']:4d} | "
                f"preview={stat['residues_preview']}"
            )
        lines.append("")
        lines.append("Membri:")
        lines.append(row["members"])
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    groups = read_groups(INPUT_FILE, TOP_GROUPS)

    analyzed = []

    print("Analisi struttura gruppi di confluenza alta")
    print(f"Gruppi analizzati: {len(groups)}")
    print("-" * 140)

    for group in groups:
        row = analyze_group(group)
        analyzed.append(row)

        print(
            f"common={row['common_value']:15d} | "
            f"members={row['members_count']:4d} | "
            f"gcd={row['gcd_diffs_from_first']:8d} | "
            f"v2_gcd={str(row['v2_gcd_diffs_from_first']):>3s} | "
            f"distinct_mod_1024={row['distinct_mod_1024']:4d} | "
            f"common_mod1024={row['common_residue_mod_1024']:4d} "
            f"({row['common_residue_mod_1024_count']})"
        )

    export_csv(OUTPUT_FILE, analyzed)
    export_detail(DETAIL_FILE, analyzed)

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"TXT generato: {DETAIL_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{DETAIL_FILE}'")


if __name__ == "__main__":
    main()
