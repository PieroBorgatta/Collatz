import csv
import math


INPUT_FILE = "collatz_03_traiettoria_3041127.csv"
OUTPUT_FILE = "collatz_04_analisi_v2_3041127.csv"
SUMMARY_FILE = "collatz_04_summary_3041127.txt"

CRITICAL_V2 = math.log2(3)


def read_trajectory(filename: str):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            rows.append({
                "step": int(row["step"]),
                "value": int(row["value"]),
                "v2": int(row["v2"]),
                "ratio_to_start": float(row["ratio_to_start"]),
                "log_value": float(row["log_value"]),
            })

    return rows


def analyze_v2(rows):
    analyzed = []

    cumulative_v2 = 0
    cumulative_critical = 0.0
    cumulative_surplus = 0.0

    consecutive_v2_1 = 0
    max_consecutive_v2_1 = 0

    peak_row = max(rows, key=lambda r: r["value"])
    peak_step = peak_row["step"]

    first_positive_surplus_step = None
    first_descent_step = None

    start_value = rows[0]["value"]

    for row in rows:
        step = row["step"]
        value = row["value"]
        v2 = row["v2"]

        if step == 0:
            analyzed.append({
                **row,
                "cumulative_v2": 0,
                "critical_required_v2": 0.0,
                "surplus_v2": 0.0,
                "avg_v2_so_far": 0.0,
                "consecutive_v2_1": 0,
                "phase": "start",
            })
            continue

        cumulative_v2 += v2
        cumulative_critical = step * CRITICAL_V2
        cumulative_surplus = cumulative_v2 - cumulative_critical
        avg_v2_so_far = cumulative_v2 / step

        if v2 == 1:
            consecutive_v2_1 += 1
        else:
            consecutive_v2_1 = 0

        max_consecutive_v2_1 = max(max_consecutive_v2_1, consecutive_v2_1)

        if first_positive_surplus_step is None and cumulative_surplus > 0:
            first_positive_surplus_step = step

        if first_descent_step is None and value < start_value:
            first_descent_step = step

        if step < peak_step:
            phase = "ascesa"
        elif step == peak_step:
            phase = "picco"
        elif first_descent_step is not None and step >= first_descent_step:
            phase = "sotto_start"
        else:
            phase = "discesa_post_picco"

        analyzed.append({
            **row,
            "cumulative_v2": cumulative_v2,
            "critical_required_v2": cumulative_critical,
            "surplus_v2": cumulative_surplus,
            "avg_v2_so_far": avg_v2_so_far,
            "consecutive_v2_1": consecutive_v2_1,
            "phase": phase,
        })

    summary = {
        "start": rows[0]["value"],
        "total_steps": rows[-1]["step"],
        "final_value": rows[-1]["value"],
        "total_v2": cumulative_v2,
        "avg_v2": cumulative_v2 / rows[-1]["step"],
        "critical_v2": CRITICAL_V2,
        "final_surplus_v2": cumulative_surplus,
        "peak_step": peak_step,
        "peak_value": peak_row["value"],
        "peak_ratio": peak_row["ratio_to_start"],
        "first_positive_surplus_step": first_positive_surplus_step,
        "first_descent_step": first_descent_step,
        "max_consecutive_v2_1": max_consecutive_v2_1,
    }

    return analyzed, summary


def export_csv(filename: str, rows: list):
    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, summary: dict):
    lines = []

    lines.append("ANALISI V2 - TRAIETTORIA COLLATZ/SYRACUSE")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Numero iniziale: {summary['start']}")
    lines.append(f"Valore finale: {summary['final_value']}")
    lines.append(f"Salti Syracuse totali: {summary['total_steps']}")
    lines.append("")
    lines.append(f"Soglia critica log2(3): {summary['critical_v2']:.9f}")
    lines.append(f"v2 totale accumulato: {summary['total_v2']}")
    lines.append(f"avg_v2 finale: {summary['avg_v2']:.9f}")
    lines.append(f"surplus_v2 finale: {summary['final_surplus_v2']:.9f}")
    lines.append("")
    lines.append(f"Step del picco massimo: {summary['peak_step']}")
    lines.append(f"Valore massimo: {summary['peak_value']}")
    lines.append(f"Rapporto massimo rispetto allo start: {summary['peak_ratio']:.6f}")
    lines.append("")
    lines.append(f"Primo step con surplus_v2 positivo: {summary['first_positive_surplus_step']}")
    lines.append(f"Primo step sotto il valore iniziale: {summary['first_descent_step']}")
    lines.append(f"Massima sequenza consecutiva di v2=1: {summary['max_consecutive_v2_1']}")
    lines.append("")
    lines.append("INTERPRETAZIONE")
    lines.append("-" * 80)
    lines.append(
        "Il valore avg_v2 finale è superiore a log2(3). "
        "Questo significa che, sull'intera traiettoria, la contrazione dovuta alle divisioni per 2 "
        "supera l'espansione dovuta ai fattori 3."
    )
    lines.append("")
    lines.append(
        "I tratti con v2=1 sono le fasi antigravitazionali: in quei passaggi il numero viene circa moltiplicato per 3/2."
    )
    lines.append("")
    lines.append(
        "I passaggi con v2 grandi sono le cadute gravitazionali: recuperano il debito accumulato durante l'ascesa."
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_summary(summary: dict):
    print("Analisi V2 completata")
    print("-" * 100)
    print(f"Numero iniziale: {summary['start']}")
    print(f"Salti Syracuse totali: {summary['total_steps']}")
    print(f"Picco massimo: {summary['peak_value']}")
    print(f"Step del picco: {summary['peak_step']}")
    print(f"Rapporto massimo: {summary['peak_ratio']:.3f}")
    print()
    print(f"Soglia critica log2(3): {summary['critical_v2']:.9f}")
    print(f"avg_v2 finale: {summary['avg_v2']:.9f}")
    print(f"surplus_v2 finale: {summary['final_surplus_v2']:.9f}")
    print()
    print(f"Primo step con surplus_v2 positivo: {summary['first_positive_surplus_step']}")
    print(f"Primo step sotto il valore iniziale: {summary['first_descent_step']}")
    print(f"Massima sequenza consecutiva di v2=1: {summary['max_consecutive_v2_1']}")
    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


def main():
    rows = read_trajectory(INPUT_FILE)
    analyzed, summary = analyze_v2(rows)

    export_csv(OUTPUT_FILE, analyzed)
    export_summary(SUMMARY_FILE, summary)

    print_summary(summary)


if __name__ == "__main__":
    main()
