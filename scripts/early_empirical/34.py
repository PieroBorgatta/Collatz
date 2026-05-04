import csv
from statistics import mean


INPUT_FILE = "collatz_33_worsenings_lambda030_mu004.csv"
OUTPUT_FILE = "collatz_34_classificazione_peggioramenti.csv"
SUMMARY_FILE = "collatz_34_summary_classificazione_peggioramenti.txt"


def to_int(x):
    if x in ("", "None", None):
        return 0
    return int(float(x))


def to_float(x):
    if x in ("", "None", None):
        return 0.0
    return float(x)


def classify(row):
    loss = row["loss"]
    max_ratio = row["max_ratio"]
    ratio_1 = row["ratio_1_until_h"]
    dmax_delta = row["dmax_delta_at_log_step"]
    cmax_delta = row["cmax_delta_at_log_step"]

    labels = []

    if loss >= 80 or max_ratio >= 1000:
        labels.append("VERO_RIBELLE_ESTREMO")
    elif loss >= 25 or max_ratio >= 100 or ratio_1 >= 0.62:
        labels.append("VERO_RIBELLE")
    elif loss <= 3 and max_ratio <= 3:
        labels.append("FALSO_ALLARME")
    else:
        labels.append("INTERMEDIO")

    if dmax_delta > 0:
        labels.append("DMAX_CRESCE")

    if cmax_delta < 0:
        labels.append("CMAX_SCENDE")

    if ratio_1 >= 0.65:
        labels.append("ALTA_DENSITA_V2_1")

    if max_ratio >= 1000:
        labels.append("ESPLOSIONE_FORTE")

    return "+".join(labels)


def read_rows():
    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            parsed = dict(row)

            int_fields = [
                "start",
                "log_step",
                "log_value",
                "h_step",
                "h_value",
                "loss",
                "initial_dmax_step",
                "initial_cmax_step",
                "initial_max_single_v2",
                "initial_max_single_v2_step",
                "dmax_step_at_log_step",
                "cmax_step_at_log_step",
                "max_single_v2_at_log_step",
                "max_single_v2_step_at_log_step",
                "max_value",
                "max_value_step",
                "max_run_1_until_h",
                "count_1_until_h",
                "count_2_until_h",
                "count_3_until_h",
                "count_4_plus_until_h",
            ]

            float_fields = [
                "initial_dmax",
                "initial_cmax",
                "dmax_at_log_step",
                "dmax_delta_at_log_step",
                "cmax_at_log_step",
                "cmax_delta_at_log_step",
                "log_delta_at_log_step",
                "h_delta_at_log_step",
                "local_debt_at_log_step",
                "max_ratio",
                "avg_v2_until_h",
                "ratio_1_until_h",
            ]

            for field in int_fields:
                if field in parsed:
                    parsed[field] = to_int(parsed[field])

            for field in float_fields:
                if field in parsed:
                    parsed[field] = to_float(parsed[field])

            parsed["classification"] = classify(parsed)
            rows.append(parsed)

    return rows


def export_csv(rows):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(rows):
    counts = {}

    for row in rows:
        main_class = row["classification"].split("+")[0]
        counts[main_class] = counts.get(main_class, 0) + 1

    true_rebels = [
        r for r in rows
        if r["classification"].startswith("VERO_RIBELLE")
    ]

    false_alarms = [
        r for r in rows
        if r["classification"].startswith("FALSO_ALLARME")
    ]

    intermediates = [
        r for r in rows
        if r["classification"].startswith("INTERMEDIO")
    ]

    by_loss = sorted(rows, key=lambda r: r["loss"], reverse=True)
    by_ratio = sorted(rows, key=lambda r: r["max_ratio"], reverse=True)
    by_ratio_1 = sorted(rows, key=lambda r: r["ratio_1_until_h"], reverse=True)

    lines = []

    lines.append("CLASSIFICAZIONE PEGGIORAMENTI H PRUDENTE")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Totale peggioramenti: {len(rows)}")
    lines.append("")

    lines.append("Conteggi principali:")
    lines.append("-" * 120)
    for k, v in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{k}: {v}")

    lines.append("")
    lines.append("Statistiche per gruppo:")
    lines.append("-" * 120)

    for name, group in [
        ("VERI_RIBELLI", true_rebels),
        ("FALSI_ALLARMI", false_alarms),
        ("INTERMEDI", intermediates),
    ]:
        if not group:
            continue

        lines.append(name)
        lines.append(f"  count: {len(group)}")
        lines.append(f"  loss medio: {mean(r['loss'] for r in group):.6f}")
        lines.append(f"  max_ratio medio: {mean(r['max_ratio'] for r in group):.6f}")
        lines.append(f"  ratio_1 medio: {mean(r['ratio_1_until_h'] for r in group):.6f}")
        lines.append(f"  dmax_delta medio: {mean(r['dmax_delta_at_log_step'] for r in group):.6f}")
        lines.append(f"  cmax_delta medio: {mean(r['cmax_delta_at_log_step'] for r in group):.6f}")
        lines.append("")

    sections = [
        ("Top 25 per loss", by_loss),
        ("Top 25 per max_ratio", by_ratio),
        ("Top 25 per ratio v2=1", by_ratio_1),
    ]

    for title, data in sections:
        lines.append(title)
        lines.append("-" * 120)

        for r in data[:25]:
            lines.append(
                f"n={r['start']:10d} | "
                f"class={r['classification']} | "
                f"loss={r['loss']:4d} | "
                f"max_ratio={r['max_ratio']:10.3f} | "
                f"ratio_1={r['ratio_1_until_h']:.6f} | "
                f"dmax_delta={r['dmax_delta_at_log_step']:+.6f} | "
                f"cmax_delta={r['cmax_delta_at_log_step']:+.6f}"
            )

        lines.append("")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = read_rows()
    export_csv(rows)
    export_summary(rows)

    print("Classificazione peggioramenti completata")
    print("-" * 120)
    print(f"Input: {INPUT_FILE}")
    print(f"Totale righe: {len(rows)}")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprire:")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
