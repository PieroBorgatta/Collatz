import csv


INPUT_FILE = "collatz_21_metriche_famiglie.csv"
OUTPUT_FILE = "collatz_22_classificazione_famiglie.csv"
SUMMARY_FILE = "collatz_22_summary_classificazione_famiglie.txt"


def read_rows(filename: str):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            parsed = dict(row)

            int_fields = [
                "family_rank",
                "members_count",
                "nodes_count",
                "max_common_value",
                "min_common_value",
                "common_span",
                "steps_to_1",
                "total_v2",
                "max_debt_trunk_step",
                "max_value_inside_trunk",
                "max_value_inside_trunk_step",
                "biggest_drop_v2",
                "biggest_drop_step",
                "biggest_drop_from",
                "biggest_drop_to",
            ]

            float_fields = [
                "max_avg_step",
                "min_avg_step",
                "avg_v2",
                "final_surplus",
                "max_debt_trunk",
                "max_ratio_inside_trunk",
                "biggest_drop_ratio",
                "surplus_per_step",
                "nodes_per_member",
            ]

            bool_fields = [
                "trunk_starts_dissipative",
            ]

            for field in int_fields:
                if field in parsed and parsed[field] not in ("", "None"):
                    parsed[field] = int(float(parsed[field]))

            for field in float_fields:
                if field in parsed and parsed[field] not in ("", "None"):
                    parsed[field] = float(parsed[field])

            for field in bool_fields:
                if field in parsed:
                    parsed[field] = str(parsed[field]).lower() == "true"

            rows.append(parsed)

    return rows


def classify(row):
    members = row["members_count"]
    nodes = row["nodes_count"]
    max_common = row["max_common_value"]
    surplus_step = row["surplus_per_step"]
    dissipative = row["trunk_starts_dissipative"]
    max_debt = row["max_debt_trunk"]

    labels = []

    # Autostrade larghe
    if members >= 20 and nodes >= 20:
        labels.append("A_AUTOSTRADA_LARGA")

    # Confluenza larga ma corta
    if members >= 20 and nodes < 20:
        labels.append("B_CONFLUENZA_LARGA_CORTA")

    # Tronchi altissimi
    if max_common >= 10_000_000_000:
        labels.append("C_TRONCO_ALTO")

    # Tronchi estremi
    if max_common >= 100_000_000_000:
        labels.append("C2_TRONCO_ESTREMO")

    # Ultra dissipativi
    if surplus_step >= 0.75:
        labels.append("D_ULTRA_DISSIPATIVO")

    # Dissipativi da subito
    if dissipative:
        labels.append("E_DISSIPATIVO_DA_SUBITO")

    # Misti: hanno surplus finale positivo ma partono con debito
    if not dissipative and max_debt > 0:
        labels.append("F_MISTO")

    # Piccoli
    if members <= 3 and nodes <= 3:
        labels.append("G_MICRO")

    if not labels:
        labels.append("Z_NON_CLASSIFICATO")

    return "+".join(labels)


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list):
    counts = {}

    for row in rows:
        cls = row["classification"]
        counts[cls] = counts.get(cls, 0) + 1

    by_members = sorted(rows, key=lambda x: x["members_count"], reverse=True)
    by_height = sorted(rows, key=lambda x: x["max_common_value"], reverse=True)
    by_surplus_step = sorted(rows, key=lambda x: x["surplus_per_step"], reverse=True)

    lines = []

    lines.append("CLASSIFICAZIONE FAMIGLIE GRAVITAZIONALI")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Famiglie totali: {len(rows)}")
    lines.append("")
    lines.append("Conteggi per classificazione:")
    lines.append("-" * 120)

    for cls, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{cls}: {count}")

    lines.append("")
    lines.append("Top 20 per membri:")
    lines.append("-" * 120)

    for r in by_members[:20]:
        lines.append(
            f"id={r['family_id']} | "
            f"class={r['classification']} | "
            f"members={r['members_count']} | "
            f"nodes={r['nodes_count']} | "
            f"max_common={r['max_common_value']} | "
            f"avg_v2={r['avg_v2']:.6f} | "
            f"surplus_step={r['surplus_per_step']:.6f} | "
            f"diss={r['trunk_starts_dissipative']}"
        )

    lines.append("")
    lines.append("Top 20 per altezza:")
    lines.append("-" * 120)

    for r in by_height[:20]:
        lines.append(
            f"id={r['family_id']} | "
            f"class={r['classification']} | "
            f"members={r['members_count']} | "
            f"nodes={r['nodes_count']} | "
            f"max_common={r['max_common_value']} | "
            f"avg_v2={r['avg_v2']:.6f} | "
            f"surplus_step={r['surplus_per_step']:.6f} | "
            f"diss={r['trunk_starts_dissipative']}"
        )

    lines.append("")
    lines.append("Top 20 per dissipazione per step:")
    lines.append("-" * 120)

    for r in by_surplus_step[:20]:
        lines.append(
            f"id={r['family_id']} | "
            f"class={r['classification']} | "
            f"members={r['members_count']} | "
            f"nodes={r['nodes_count']} | "
            f"max_common={r['max_common_value']} | "
            f"avg_v2={r['avg_v2']:.6f} | "
            f"surplus_step={r['surplus_per_step']:.6f} | "
            f"diss={r['trunk_starts_dissipative']}"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = read_rows(INPUT_FILE)

    for row in rows:
        row["classification"] = classify(row)

    export_csv(OUTPUT_FILE, rows)
    export_summary(SUMMARY_FILE, rows)

    print("Classificazione completata")
    print("-" * 120)
    print(f"Famiglie classificate: {len(rows)}")
    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
