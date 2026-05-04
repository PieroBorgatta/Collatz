import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache
from collections import Counter


OUTPUT_FILE = "collatz_100M_validate_final_candidate.csv"
SUMMARY_FILE = "collatz_100M_summary_validate_final_candidate.txt"

# Alza qui il limite.
# Primo test consigliato: 20 milioni.
LIMIT = 100_000_000

MAX_BLOCK_STEPS = 400
LOOKAHEAD = 80

LAMBDA = 0.28
MU = 0.03
THETA = 0.30

CRITICAL = math.log2(3)

CPU_COUNT = os.cpu_count() or 4
WORKERS = max(1, CPU_COUNT - 1)
CHUNK_SIZE = 100_000


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


@lru_cache(maxsize=700_000)
def future_metrics(n: int):
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

    for step in range(1, LOOKAHEAD + 1):
        if current == 1:
            break

        current, a = syracuse(current)

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

    return {
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
    }


def H(n: int):
    m = future_metrics(n)
    return (
        math.log(n)
        + LAMBDA * m["dmax"]
        - MU * m["cmax"]
        + THETA * m["pmax"]
    )


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


def quick_analyze(start: int):
    initial_log = math.log(start)
    initial_metrics = future_metrics(start)
    initial_h = (
        initial_log
        + LAMBDA * initial_metrics["dmax"]
        - MU * initial_metrics["cmax"]
        + THETA * initial_metrics["pmax"]
    )

    n = start

    log_step = None
    h_step = None
    log_row = None

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

        current_h = (
            math.log(n)
            + LAMBDA * metrics["dmax"]
            - MU * metrics["cmax"]
            + THETA * metrics["pmax"]
        )

        if log_step is None and n < start:
            log_step = step
            log_row = {
                "value": n,
                "log_delta": math.log(n) - initial_log,
                "dmax": metrics["dmax"],
                "dmax_delta": metrics["dmax"] - initial_metrics["dmax"],
                "cmax": metrics["cmax"],
                "cmax_delta": metrics["cmax"] - initial_metrics["cmax"],
                "pmax": metrics["pmax"],
                "pmax_delta": metrics["pmax"] - initial_metrics["pmax"],
                "pavg": metrics["pavg"],
                "h_delta": current_h - initial_h,
                "local_debt": step * CRITICAL - cumulative_v2,
            }

        if h_step is None and current_h < initial_h:
            h_step = step

        if log_step is not None and h_step is not None:
            break

        if n == 1:
            break

    if log_step is None:
        log_step = MAX_BLOCK_STEPS + 1

    if h_step is None:
        h_step = MAX_BLOCK_STEPS + 1

    if log_row is None:
        log_row = {
            "value": None,
            "log_delta": None,
            "dmax": None,
            "dmax_delta": None,
            "cmax": None,
            "cmax_delta": None,
            "pmax": None,
            "pmax_delta": None,
            "pavg": None,
            "h_delta": None,
            "local_debt": None,
        }

    counter = Counter(seq_v2)
    ratio_1 = counter.get(1, 0) / len(seq_v2) if seq_v2 else 0.0
    avg_v2 = sum(seq_v2) / len(seq_v2) if seq_v2 else 0.0

    loss = h_step - log_step

    row = {
        "start": start,
        "log_step": log_step,
        "h_step": h_step,
        "loss": loss,

        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / start,

        "ratio_1_until_h": ratio_1,
        "avg_v2_until_h": avg_v2,
        "count_1_until_h": counter.get(1, 0),
        "count_2_until_h": counter.get(2, 0),
        "count_3_until_h": counter.get(3, 0),
        "count_4_plus_until_h": sum(v for k, v in counter.items() if k >= 4),

        "initial_dmax": initial_metrics["dmax"],
        "initial_cmax": initial_metrics["cmax"],
        "initial_pmax": initial_metrics["pmax"],
        "initial_pavg": initial_metrics["pavg"],

        "log_value": log_row["value"],
        "log_delta_at_log_step": log_row["log_delta"],

        "dmax_at_log_step": log_row["dmax"],
        "dmax_delta_at_log_step": log_row["dmax_delta"],

        "cmax_at_log_step": log_row["cmax"],
        "cmax_delta_at_log_step": log_row["cmax_delta"],

        "pmax_at_log_step": log_row["pmax"],
        "pmax_delta_at_log_step": log_row["pmax_delta"],
        "pavg_at_log_step": log_row["pavg"],

        "h_delta_at_log_step": log_row["h_delta"],
        "local_debt_at_log_step": log_row["local_debt"],
    }

    row["classification"] = classify(row)

    return row


def empty_stats():
    return {
        "total": 0,
        "worsened": 0,
        "improved": 0,
        "same": 0,

        "sum_log_step": 0,
        "sum_h_step": 0,
        "max_log_step": 0,
        "max_h_step": 0,

        "worst_loss": 0,
        "worst_loss_n": None,

        "best_gain": 0,
        "best_gain_n": None,

        "worsening_rows": [],
    }


def process_chunk(start_odd: int, end_odd: int):
    stats = empty_stats()

    for n in range(start_odd, end_odd + 1, 2):
        row = quick_analyze(n)

        log_step = row["log_step"]
        h_step = row["h_step"]

        stats["total"] += 1
        stats["sum_log_step"] += log_step
        stats["sum_h_step"] += h_step

        stats["max_log_step"] = max(stats["max_log_step"], log_step)
        stats["max_h_step"] = max(stats["max_h_step"], h_step)

        if h_step > log_step:
            stats["worsened"] += 1
            stats["worsening_rows"].append(row)

            if row["loss"] > stats["worst_loss"]:
                stats["worst_loss"] = row["loss"]
                stats["worst_loss_n"] = n

        elif h_step < log_step:
            stats["improved"] += 1
            gain = log_step - h_step

            if gain > stats["best_gain"]:
                stats["best_gain"] = gain
                stats["best_gain_n"] = n

        else:
            stats["same"] += 1

    return {
        "start": start_odd,
        "end": end_odd,
        "processed": stats["total"],
        "stats": stats,
    }


def merge_stats(global_stats, local_stats):
    global_stats["total"] += local_stats["total"]

    global_stats["worsened"] += local_stats["worsened"]
    global_stats["improved"] += local_stats["improved"]
    global_stats["same"] += local_stats["same"]

    global_stats["sum_log_step"] += local_stats["sum_log_step"]
    global_stats["sum_h_step"] += local_stats["sum_h_step"]

    global_stats["max_log_step"] = max(global_stats["max_log_step"], local_stats["max_log_step"])
    global_stats["max_h_step"] = max(global_stats["max_h_step"], local_stats["max_h_step"])

    if local_stats["worst_loss"] > global_stats["worst_loss"]:
        global_stats["worst_loss"] = local_stats["worst_loss"]
        global_stats["worst_loss_n"] = local_stats["worst_loss_n"]

    if local_stats["best_gain"] > global_stats["best_gain"]:
        global_stats["best_gain"] = local_stats["best_gain"]
        global_stats["best_gain_n"] = local_stats["best_gain_n"]

    global_stats["worsening_rows"].extend(local_stats["worsening_rows"])


def make_chunks():
    chunks = []
    current = 3

    while current <= LIMIT:
        end = min(current + (CHUNK_SIZE * 2) - 2, LIMIT)

        if end % 2 == 0:
            end -= 1

        chunks.append((current, end))
        current = end + 2

    return chunks


def export_csv(rows):
    if not rows:
        return

    rows = sorted(rows, key=lambda r: r["loss"], reverse=True)
    fieldnames = list(rows[0].keys())

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(stats, elapsed):
    rows = stats["worsening_rows"]

    counts = {}
    for r in rows:
        main = r["classification"].split("+")[0]
        counts[main] = counts.get(main, 0) + 1

    by_loss = sorted(rows, key=lambda r: r["loss"], reverse=True)
    by_ratio = sorted(rows, key=lambda r: r["max_ratio"], reverse=True)
    by_pmax = sorted(rows, key=lambda r: r["pmax_at_log_step"] or 0, reverse=True)
    by_hdelta = sorted(rows, key=lambda r: r["h_delta_at_log_step"] or 0, reverse=True)

    total = stats["total"]

    lines = []

    lines.append("VALIDAZIONE CANDIDATO FINALE")
    lines.append("=" * 120)
    lines.append("")
    lines.append(
        f"H(n) = log(n) + {LAMBDA}*Dmax80(n) - {MU}*Cmax80(n) + {THETA}*Pmax80(n)"
    )
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"LOOKAHEAD = {LOOKAHEAD}")
    lines.append(f"CPU_COUNT = {CPU_COUNT}")
    lines.append(f"WORKERS = {WORKERS}")
    lines.append(f"CHUNK_SIZE = {CHUNK_SIZE}")
    lines.append(f"Tempo totale secondi = {elapsed:.2f}")
    lines.append("")

    lines.append("Statistiche globali:")
    lines.append("-" * 120)
    lines.append(f"Totale dispari analizzati: {total}")
    lines.append(f"Improved: {stats['improved']} ({stats['improved'] / total:.8f})")
    lines.append(f"Worsened: {stats['worsened']} ({stats['worsened'] / total:.8f})")
    lines.append(f"Same: {stats['same']} ({stats['same'] / total:.8f})")
    lines.append("")
    lines.append(f"Avg log step: {stats['sum_log_step'] / total:.6f}")
    lines.append(f"Avg H step:   {stats['sum_h_step'] / total:.6f}")
    lines.append(f"Max log step: {stats['max_log_step']}")
    lines.append(f"Max H step:   {stats['max_h_step']}")
    lines.append(f"Worst loss:   {stats['worst_loss']} su n={stats['worst_loss_n']}")
    lines.append(f"Best gain:    {stats['best_gain']} su n={stats['best_gain_n']}")
    lines.append("")

    lines.append("Classificazione peggioramenti:")
    lines.append("-" * 120)
    for k, v in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{k}: {v}")

    lines.append("")
    lines.append("Top 30 per loss:")
    lines.append("-" * 120)
    for r in by_loss[:30]:
        lines.append(format_row(r))

    lines.append("")
    lines.append("Top 30 per max_ratio:")
    lines.append("-" * 120)
    for r in by_ratio[:30]:
        lines.append(format_row(r))

    lines.append("")
    lines.append("Top 30 per pmax al log-step:")
    lines.append("-" * 120)
    for r in by_pmax[:30]:
        lines.append(format_row(r))

    lines.append("")
    lines.append("Top 30 per h_delta al log-step:")
    lines.append("-" * 120)
    for r in by_hdelta[:30]:
        lines.append(format_row(r))

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def format_row(r):
    return (
        f"n={r['start']:10d} | "
        f"class={r['classification']} | "
        f"log_step={r['log_step']:4d} | "
        f"h_step={r['h_step']:4d} | "
        f"loss={r['loss']:4d} | "
        f"max_ratio={r['max_ratio']:12.3f} | "
        f"ratio_1={r['ratio_1_until_h']:.6f} | "
        f"pmax_log={r['pmax_at_log_step']:.6f} | "
        f"dmax_delta={r['dmax_delta_at_log_step']:+.6f} | "
        f"cmax_delta={r['cmax_delta_at_log_step']:+.6f} | "
        f"h_delta_log={r['h_delta_at_log_step']:+.6f}"
    )


def main():
    started = time.time()

    chunks = make_chunks()
    global_stats = empty_stats()

    print("Validazione candidato finale")
    print("-" * 120)
    print(f"H = log(n) + {LAMBDA}*Dmax80 - {MU}*Cmax80 + {THETA}*Pmax80")
    print(f"LIMIT = {LIMIT}")
    print(f"CPU_COUNT = {CPU_COUNT}")
    print(f"WORKERS = {WORKERS}")
    print(f"CHUNK_SIZE = {CHUNK_SIZE}")
    print(f"Chunks = {len(chunks)}")
    print()

    completed = 0
    processed_total = 0

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        futures = [
            executor.submit(process_chunk, start, end)
            for start, end in chunks
        ]

        for future in as_completed(futures):
            result = future.result()

            completed += 1
            processed_total += result["processed"]

            merge_stats(global_stats, result["stats"])

            elapsed = time.time() - started

            print(
                f"chunk {completed:4d}/{len(chunks)} | "
                f"range={result['start']}-{result['end']} | "
                f"processed_total={processed_total:,} | "
                f"worsened={global_stats['worsened']} | "
                f"elapsed={elapsed:.1f}s"
            )

    elapsed = time.time() - started

    export_csv(global_stats["worsening_rows"])
    export_summary(global_stats, elapsed)

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"Peggioramenti trovati: {global_stats['worsened']}")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
