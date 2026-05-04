import csv
import hashlib


INPUT_FILE = "collatz_11_confluenze_alte.csv"
OUTPUT_FILE = "collatz_20_famiglie_tronchi.csv"
DETAIL_FILE = "collatz_20_dettaglio_famiglie_tronchi.txt"


def read_rows(filename: str):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            members = tuple(sorted(int(x) for x in row["members"].split(",") if x.strip()))

            rows.append({
                "common_value": int(row["common_value"]),
                "members_count": int(row["members_count"]),
                "min_step": int(row["min_step"]),
                "max_step": int(row["max_step"]),
                "avg_step": float(row["avg_step"]),
                "members": members,
            })

    return rows


def members_hash(members):
    text = ",".join(map(str, members))
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def group_by_members(rows):
    groups = {}

    for row in rows:
        key = row["members"]

        if key not in groups:
            groups[key] = {
                "members": key,
                "members_count": len(key),
                "nodes": [],
            }

        groups[key]["nodes"].append(row)

    result = []

    for members, group in groups.items():
        nodes = sorted(group["nodes"], key=lambda x: x["common_value"], reverse=True)

        common_values = [n["common_value"] for n in nodes]
        avg_steps = [n["avg_step"] for n in nodes]

        result.append({
            "family_id": members_hash(members),
            "members_count": len(members),
            "nodes_count": len(nodes),
            "max_common_value": max(common_values),
            "min_common_value": min(common_values),
            "max_avg_step": max(avg_steps),
            "min_avg_step": min(avg_steps),
            "members": members,
            "common_values": common_values,
            "nodes": nodes,
        })

    result.sort(
        key=lambda x: (
            x["members_count"],
            x["nodes_count"],
            x["max_common_value"],
        ),
        reverse=True
    )

    return result


def export_csv(filename: str, families: list):
    rows = []

    for fam in families:
        rows.append({
            "family_id": fam["family_id"],
            "members_count": fam["members_count"],
            "nodes_count": fam["nodes_count"],
            "max_common_value": fam["max_common_value"],
            "min_common_value": fam["min_common_value"],
            "max_avg_step": fam["max_avg_step"],
            "min_avg_step": fam["min_avg_step"],
            "members_preview": ",".join(map(str, list(fam["members"])[:30])),
            "common_values_preview": ",".join(map(str, fam["common_values"][:30])),
        })

    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_detail(filename: str, families: list):
    lines = []

    lines.append("FAMIGLIE DI TRONCHI PER INSIEME DI MEMBRI")
    lines.append("=" * 120)
    lines.append("")

    for idx, fam in enumerate(families, start=1):
        lines.append("-" * 120)
        lines.append(f"Famiglia #{idx}")
        lines.append(f"family_id: {fam['family_id']}")
        lines.append(f"membri: {fam['members_count']}")
        lines.append(f"nodi comuni: {fam['nodes_count']}")
        lines.append(f"massimo valore comune: {fam['max_common_value']}")
        lines.append(f"minimo valore comune: {fam['min_common_value']}")
        lines.append("")
        lines.append("Primi 50 valori comuni della famiglia:")
        lines.append(", ".join(map(str, fam["common_values"][:50])))
        lines.append("")
        lines.append("Membri:")
        lines.append(", ".join(map(str, fam["members"])))
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = read_rows(INPUT_FILE)
    families = group_by_members(rows)

    export_csv(OUTPUT_FILE, families)
    export_detail(DETAIL_FILE, families)

    print("Analisi famiglie di tronchi completata")
    print("-" * 120)
    print(f"Nodi di confluenza letti: {len(rows)}")
    print(f"Famiglie distinte trovate: {len(families)}")
    print()

    print("Top 30 famiglie:")
    print("-" * 120)

    for idx, fam in enumerate(families[:30], start=1):
        print(
            f"{idx:3d}) "
            f"id={fam['family_id']} | "
            f"members={fam['members_count']:4d} | "
            f"nodes={fam['nodes_count']:4d} | "
            f"max_common={fam['max_common_value']:15d} | "
            f"min_common={fam['min_common_value']:15d}"
        )

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"TXT generato: {DETAIL_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{DETAIL_FILE}'")


if __name__ == "__main__":
    main()
