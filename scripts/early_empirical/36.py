import csv
import math
from collections import Counter
from statistics import mean


OUTPUT_FILE = "collatz_36_worsenings_best_pressure.csv"
SUMMARY_FILE = "collatz_36_summary_worsenings_best_pressure.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
LOOKAHEAD = 80

# Miglior candidato prudente trovato da 35.py
LAMBDA = 0.28
MU = 0.03
THETA = 0.30

CRITICAL = math.log2(3)


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


_cache_metrics = {}


def future_metrics(n: int):
    if n in _cache_metrics:
        return _cache_metrics[n]

    current = n
    cumulative_v2 = 0
    count_v2_1 = 0
    steps_done = 0

    max_debt = 0.0
    max_debt_step = 0

    max_cascade = 0.0
    max_cascade_step = 0

    max_pressure = 0.0
    max_pressure_step = 0

    longest_run_1 = 0
    current_run_1 = 0

    max_single_v2 = 0
    max_single_v2_step = 0

    seq_v2 = []

    for step in range(1, LOOKAHEAD + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        seq_v2.append(a)

        steps_done += 1
        cumulative_v2 += a

        if a == 1:
            count_v2_1 += 1
            current_run_1 += 1
            longest_run_1 = max(longest_run_1, current_run_1)
        else:
            current_run_1 = 0

        debt = step * CRITICAL - cumulative_v2
        cascade = cumulative_v2 - step * CRITICAL
        pressure = count_v2_1 / step

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

        if cascade > max_cascade:
            max_cascade = cascade
            max_cascade_step = step

        if pressure > max_pressure:
            max_pressure = pressure
            max_pressure_step = step

        if a > max_single_v2:
            max_single_v2 = a
            max_single_v2_step = step

    avg_pressure = count_v2_1 / steps_done if steps_done else 0.0

    result = {
        "dmax": max_debt,
        "dmax_step": max_debt_step,
        "cmax": max_cascade,
        "cmax_step": max_cascade_step,
        "pmax": max_pressure,
        "pmax_step": max_pressure_step,
        "pavg": avg_pressure,
        "longest_run_1": longest_run_1,
        "max_single_v2": max_single_v2,
        "max_single_v2_step": max_single_v2_step,
        "prefix_v2": ",".join(map(str, seq_v2[:80])),
    }

    _cache_metrics[n] = result
    return result


def H(n: int):
    m = future_metrics(n)
    return (
        math.log(n)
        + LAMBDA * m["dmax"]
        - MU * m["cmax"]
        + THETA * m["pmax"]
    )


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


def classify(row):
    loss = row["loss"]
    max_ratio = row["max_ratio"]
    ratio_1 = row["ratio_1_until_h"]
    pmax_log = row["pmax_at_log_step"]
    dmax_delta = row["dmax_delta_at_log_step"]
    cmax_delta = row["cmax_delta_at_log_step"]

    labels = []

    if loss >= 80 or max_ratio >= 1000:
        labels.append("VERO_RIBELLE_ESTREMO")
    elif loss >= 25 or max_ratio >= 100 or ratio_1 >= 0.62 or pmax_log >= 0.70:
        labels.append("VERO_RIBELLE")
    elif loss <= 3 and max_ratio <= 3 and ratio_1 < 0.50:
        labels.append("FALSO_ALLARME")
    else:
        labels.append("INTERMEDIO")

    if dmax_delta > 0:
        labels.append("DMAX_CRESCE")

    if cmax_delta < 0:
        labels.append("CMAX_SCENDE")

    if ratio_1 >= 0.65:
        labels.append("ALTA_DENSITA_V2_1")

    if pmax_log >= 0.75:
        labels.append("ALTA_PRESSIONE_PMAX")

    if max_ratio >= 1000:
        labels.append("ESPLOSIONE_FORTE")

    return "+".join(labels)


def build_trajectory_analysis(start: int):
    initial_log = math.log(start)
    initial_metrics = future_metrics(start)
    initial_h = H(start)

    n = start

    rows = []

    first_log_step = None
    first_log_value = None

    first_h_step = None
    first_h_value = None

    max_value = start
    max_value_step = 0

    cumulative_v2 = 0
    seq_v2 = []

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, a = syracuse(n)

        seq_v2.append(a)
        cumulative_v2 += a

        if n > max_value:
            max_value = n
            max_value_step = step

        metrics = future_metrics(n)

        log_delta = math.log(n) - initial_log

        dmax_delta = metrics["dmax"] - initial_metrics["dmax"]
        cmax_delta = metrics["cmax"] - initial_metrics["cmax"]
        pmax_delta = metrics["pmax"] - initial_metrics["pmax"]

        h_delta = H(n) - initial_h

        local_debt = step * CRITICAL - cumulative_v2
        local_surplus = cumulative_v2 - step * CRITICAL

        row = {
            "step": step,
            "value": n,
            "v2": a,
            "ratio_to_start": n / start,
            "log_delta": log_delta,

            "dmax": metrics["dmax"],
            "dmax_step": metrics["dmax_step"],
            "dmax_delta": dmax_delta,

            "cmax": metrics["cmax"],
            "cmax_step": metrics["cmax_step"],
            "cmax_delta": cmax_delta,

            "pmax": metrics["pmax"],
            "pmax_step": metrics["pmax_step"],
            "pmax_delta": pmax_delta,
            "pavg": metrics["pavg"],
            "longest_run_1_future": metrics["longest_run_1"],

            "max_single_v2": metrics["max_single_v2"],
            "max_single_v2_step": metrics["max_single_v2_step"],

            "h_delta": h_delta,
            "local_debt_from_start": local_debt,
            "local_surplus_from_start": local_surplus,
        }

        rows.append(row)

        if first_log_step is None and n < start:
            first_log_step = step
            first_log_value = n

        if first_h_step is None and h_delta < 0:
            first_h_step = step
            first_h_value = n
            break

        if n == 1:
            break

    if first_log_step is None:
        first_log_step = MAX_BLOCK_STEPS + 1

    if first_h_step is None:
        first_h_step = MAX_BLOCK_STEPS + 1

    counter = Counter(seq_v2)

    return {
        "start": start,

        "initial_dmax": initial_metrics["dmax"],
        "initial_dmax_step": initial_metrics["dmax_step"],
        "initial_cmax": initial_metrics["cmax"],
        "initial_cmax_step": initial_metrics["cmax_step"],
        "initial_pmax": initial_metrics["pmax"],
        "initial_pmax_step": initial_metrics["pmax_step"],
        "initial_pavg": initial_metrics["pavg"],
        "initial_longest_run_1": initial_metrics["longest_run_1"],

        "first_log_step": first_log_step,
        "first_log_value": first_log_value,

        "first_h_step": first_h_step,
        "first_h_value": first_h_value,

        "loss": first_h_step - first_log_step,

        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / start,

        "seq_v2": seq_v2,

        "count_1": counter.get(1, 0),
        "count_2": counter.get(2, 0),
        "count_3": counter.get(3, 0),
        "count_4_plus": sum(v for k, v in counter.items() if k >= 4),

        "ratio_1": counter.get(1, 0) / len(seq_v2) if seq_v2 else 0,
        "avg_v2": sum(seq_v2) / len(seq_v2) if seq_v2 else 0,
        "max_run_1": longest_run(seq_v2, 1),

        "rows": rows,
    }


def quick_steps(start: int):
    initial_log = math.log(start)
    initial_h = H(start)

    n = start

    log_step = None
    h_step = None

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, _ = syracuse(n)

        if log_step is None and n < start:
            log_step = step

        if h_step is None and H(n) < initial_h:
            h_step = step

        if log_step is not None and h_step is not None:
            break

        if n == 1:
            break

    if log_step is None:
        log_step = MAX_BLOCK_STEPS + 1

    if h_step is None:
        h_step = MAX_BLOCK_STEPS + 1

    return log_step, h_step


def make_detail_block(analysis):
    lines = []

    lines.append("-" * 120)
    lines.append(f"n = {analysis['start']}")
    lines.append(f"initial_dmax = {analysis['initial_dmax']:.6f}")
    lines.append(f"initial_cmax = {analysis['initial_cmax']:.6f}")
    lines.append(f"initial_pmax = {analysis['initial_pmax']:.6f}")
    lines.append(f"initial_pavg = {analysis['initial_pavg']:.6f}")
    lines.append(f"initial_longest_run_1 = {analysis['initial_longest_run_1']}")
    lines.append(f"log_step = {analysis['first_log_step']}")
    lines.append(f"h_step = {analysis['first_h_step']}")
    lines.append(f"loss = {analysis['loss']}")
    lines.append(f"max_value = {analysis['max_value']}")
    lines.append(f"max_ratio = {analysis['max_ratio']:.6f}")
    lines.append(f"avg_v2_until_h = {analysis['avg_v2']:.6f}")
    lines.append(f"ratio_1_until_h = {analysis['ratio_1']:.6f}")
    lines.append(f"max_run_1_until_h = {analysis['max_run_1']}")
    lines.append("")
    lines.append(
        "step | value | v2 | ratio | log_delta | "
        "dmax | dmax_delta | cmax | cmax_delta | pmax | pmax_delta | h_delta"
    )
    lines.append("-" * 120)

    for row in analysis["rows"][:100]:
        lines.append(
            f"{row['step']:4d} | "
            f"{row['value']:14d} | "
            f"{row['v2']:2d} | "
            f"{row['ratio_to_start']:.9f} | "
            f"{row['log_delta']:+.9f} | "
            f"{row['dmax']:.6f} | "
            f"{row['dmax_delta']:+.6f} | "
            f"{row['cmax']:.6f} | "
            f"{row['cmax_delta']:+.6f} | "
            f"{row['pmax']:.6f} | "
            f"{row['pmax_delta']:+.6f} | "
            f"{row['h_delta']:+.9f}"
        )

    lines.append("")

    return "\n".join(lines)


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list, detail_blocks: list):
    by_loss = sorted(rows, key=lambda r: r["loss"], reverse=True)
    by_ratio = sorted(rows, key=lambda r: r["max_ratio"], reverse=True)
    by_pmax = sorted(rows, key=lambda r: r["pmax_at_log_step"], reverse=True)
    by_ratio_1 = sorted(rows, key=lambda r: r["ratio_1_until_h"], reverse=True)

    counts = {}
    for r in rows:
        main = r["classification"].split("+")[0]
        counts[main] = counts.get(main, 0) + 1

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

    lines = []

    lines.append("ANALISI PEGGIORAMENTI MIGLIOR CANDIDATO CON PRESSIONE")
    lines.append("=" * 120)
    lines.append("")
    lines.append(
        f"H(n) = log(n) + {LAMBDA}*Dmax80(n) - {MU}*Cmax80(n) + {THETA}*Pmax80(n)"
    )
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"LOOKAHEAD = {LOOKAHEAD}")
    lines.append("")
    lines.append(f"Peggioramenti trovati: {len(rows)}")
    lines.append("")

    lines.append("Conteggi classificazione:")
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
        lines.append(f"  pmax_log medio: {mean(r['pmax_at_log_step'] for r in group):.6f}")
        lines.append(f"  dmax_delta medio: {mean(r['dmax_delta_at_log_step'] for r in group):.6f}")
        lines.append(f"  cmax_delta medio: {mean(r['cmax_delta_at_log_step'] for r in group):.6f}")
        lines.append("")

    sections = [
        ("Top 30 per loss", by_loss),
        ("Top 30 per max_ratio", by_ratio),
        ("Top 30 per pmax al log-step", by_pmax),
        ("Top 30 per ratio v2=1", by_ratio_1),
    ]

    for title, data in sections:
        lines.append(title)
        lines.append("-" * 120)

        for r in data[:30]:
            lines.append(
                f"n={r['start']:10d} | "
                f"class={r['classification']} | "
                f"loss={r['loss']:4d} | "
                f"max_ratio={r['max_ratio']:10.3f} | "
                f"ratio_1={r['ratio_1_until_h']:.6f} | "
                f"pmax_log={r['pmax_at_log_step']:.6f} | "
                f"dmax_delta={r['dmax_delta_at_log_step']:+.6f} | "
                f"cmax_delta={r['cmax_delta_at_log_step']:+.6f} | "
                f"h_delta_log={r['h_delta_at_log_step']:+.6f}"
            )

        lines.append("")

    lines.append("")
    lines.append("DETTAGLIO PRIMI PEGGIORAMENTI")
    lines.append("=" * 120)
    lines.extend(detail_blocks[:30])

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    print("Analisi peggioramenti miglior candidato con pressione")
    print("-" * 120)
    print(f"H = log(n) + {LAMBDA}*Dmax80 - {MU}*Cmax80 + {THETA}*Pmax80")
    print()

    summary_rows = []
    detail_blocks = []

    processed = 0
    worsened = 0

    for n in range(3, LIMIT + 1, 2):
        processed += 1

        log_step, h_step = quick_steps(n)

        if h_step > log_step:
            worsened += 1

            analysis = build_trajectory_analysis(n)
            log_row = analysis["rows"][analysis["first_log_step"] - 1]

            row = {
                "start": n,

                "log_step": analysis["first_log_step"],
                "log_value": analysis["first_log_value"],

                "h_step": analysis["first_h_step"],
                "h_value": analysis["first_h_value"],

                "loss": analysis["loss"],

                "initial_dmax": analysis["initial_dmax"],
                "initial_dmax_step": analysis["initial_dmax_step"],
                "initial_cmax": analysis["initial_cmax"],
                "initial_cmax_step": analysis["initial_cmax_step"],
                "initial_pmax": analysis["initial_pmax"],
                "initial_pmax_step": analysis["initial_pmax_step"],
                "initial_pavg": analysis["initial_pavg"],
                "initial_longest_run_1": analysis["initial_longest_run_1"],

                "dmax_at_log_step": log_row["dmax"],
                "dmax_step_at_log_step": log_row["dmax_step"],
                "dmax_delta_at_log_step": log_row["dmax_delta"],

                "cmax_at_log_step": log_row["cmax"],
                "cmax_step_at_log_step": log_row["cmax_step"],
                "cmax_delta_at_log_step": log_row["cmax_delta"],

                "pmax_at_log_step": log_row["pmax"],
                "pmax_step_at_log_step": log_row["pmax_step"],
                "pmax_delta_at_log_step": log_row["pmax_delta"],
                "pavg_at_log_step": log_row["pavg"],
                "longest_run_1_future_at_log_step": log_row["longest_run_1_future"],

                "max_single_v2_at_log_step": log_row["max_single_v2"],
                "max_single_v2_step_at_log_step": log_row["max_single_v2_step"],

                "log_delta_at_log_step": log_row["log_delta"],
                "h_delta_at_log_step": log_row["h_delta"],
                "local_debt_at_log_step": log_row["local_debt_from_start"],

                "max_value": analysis["max_value"],
                "max_value_step": analysis["max_value_step"],
                "max_ratio": analysis["max_ratio"],

                "avg_v2_until_h": analysis["avg_v2"],
                "ratio_1_until_h": analysis["ratio_1"],
                "max_run_1_until_h": analysis["max_run_1"],

                "count_1_until_h": analysis["count_1"],
                "count_2_until_h": analysis["count_2"],
                "count_3_until_h": analysis["count_3"],
                "count_4_plus_until_h": analysis["count_4_plus"],

                "prefix_120_v2": ",".join(map(str, analysis["seq_v2"][:120])),
            }

            row["classification"] = classify(row)

            summary_rows.append(row)

            if len(detail_blocks) < 40:
                detail_blocks.append(make_detail_block(analysis))

        if processed % 250_000 == 0:
            print(
                f"analizzati={processed:,} | "
                f"peggioramenti={worsened}"
            )

    summary_rows.sort(key=lambda r: r["loss"], reverse=True)

    export_csv(OUTPUT_FILE, summary_rows)
    export_summary(SUMMARY_FILE, summary_rows, detail_blocks)

    print()
    print(f"Peggioramenti trovati: {len(summary_rows)}")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
