import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache
from collections import Counter


OUTPUT_FILE = "collatz_45_100M_trisk_eta0025_worsenings.csv"
SUMMARY_FILE = "collatz_45_100M_trisk_eta0025_summary.txt"

LIMIT = 100_000_000
LOOKAHEAD = 80
MAX_BLOCK_STEPS = 500

# Base H
LAMBDA = 0.28
MU = 0.03
THETA = 0.30

# Micro-correzione T_risk trovata dal 44
ALPHA = 1.00
ETA = 0.0025

CRITICAL = math.log2(3)

CPU_COUNT = os.cpu_count() or 4
WORKERS = max(1, CPU_COUNT - 1)

# Sul Mac M1 puoi lasciare 50_000 o 100_000.
# 100_000 riduce overhead ma stampa meno spesso.
CHUNK_SIZE = 50_000


def v2(x: int) -> int:
    c = 0
    while x % 2 == 0:
        x //= 2
        c += 1
    return c


def syracuse(n: int):
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


@lru_cache(maxsize=700_000)
def future_metrics(n: int):
    current = n

    cumulative_v2 = 0
    count_1 = 0
    run_1 = 0
    max_run_1 = 0

    dmax = 0.0
    cmax = 0.0
    pmax = 0.0
    t_star = 0.0

    steps_done = 0

    for step in range(1, LOOKAHEAD + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        steps_done += 1
        cumulative_v2 += a

        if a == 1:
            count_1 += 1
            run_1 += 1
            max_run_1 = max(max_run_1, run_1)
        else:
            run_1 = 0

        debt = step * CRITICAL - cumulative_v2
        cascade = cumulative_v2 - step * CRITICAL
        pressure = count_1 / step

        dmax = max(dmax, debt)
        cmax = max(cmax, cascade)
        pmax = max(pmax, pressure)

        # Stessa definizione usata nel 44:
        local_risk = max(0.0, debt) * pressure * (1.0 + run_1 / 10.0)
        t_star = max(t_star, local_risk)

    pavg = count_1 / steps_done if steps_done else 0.0

    return {
        "dmax": dmax,
        "cmax": cmax,
        "pmax": pmax,
        "pavg": pavg,
        "t_star": t_star,
        "max_run_1": max_run_1,
    }


def base_H_from_metrics(n: int, m):
    return (
        math.log(n)
        + LAMBDA * m["dmax"]
        - MU * m["cmax"]
        + THETA * m["pmax"]
    )


def htr_from_metrics(n: int, m):
    base_h = base_H_from_metrics(n, m)
    t_risk = max(0.0, m["t_star"] - ALPHA * m["cmax"])
    return base_h + ETA * t_risk


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
    initial_htr = htr_from_metrics(start, initial_metrics)

    n = start

    log_step = None
    htr_step = None
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
        current_htr = htr_from_metrics(n, metrics)

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

                "t_star": metrics["t_star"],
                "t_star_delta": metrics["t_star"] - initial_metrics["t_star"],

                "htr_delta": current_htr - initial_htr,
                "local_debt": step * CRITICAL - cumulative_v2,
            }

        if htr_step is None and current_htr < initial_htr:
            htr_step = step

        if log_step is not None and htr_step is not None:
            break

        if n == 1:
            break

    if log_step is None:
        log_step = MAX_BLOCK_STEPS + 1

    if htr_step is None:
        htr_step = MAX_BLOCK_STEPS + 1

    if log_row is None:
        log_row = {
            "value": "",
            "log_delta": 0.0,
            "dmax": 0.0,
            "dmax_delta": 0.0,
            "cmax": 0.0,
            "cmax_delta": 0.0,
            "pmax": 0.0,
            "pmax_delta": 0.0,
            "t_star": 0.0,
            "t_star_delta": 0.0,
            "htr_delta": 0.0,
            "local_debt": 0.0,
        }

    counter = Counter(seq_v2)
    ratio_1 = counter.get(1, 0) / len(seq_v2) if seq_v2 else 0.0
    avg_v2 = sum(seq_v2) / len(seq_v2) if seq_v2 else 0.0

    loss = htr_step - log_step

    row = {
        "start": start,

        "log_step": log_step,
        "htr_step": htr_step,
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
        "initial_t_star": initial_metrics["t_star"],

        "log_value": log_row["value"],
        "log_delta_at_log_step": log_row["log_delta"],

        "dmax_at_log_step": log_row["dmax"],
        "dmax_delta_at_log_step": log_row["dmax_delta"],

        "cmax_at_log_step": log_row["cmax"],
        "cmax_delta_at_log_step": log_row["cmax_delta"],

        "pmax_at_log_step": log_row["pmax"],
        "pmax_delta_at_log_step": log_row["pmax_delta"],

        "t_star_at_log_step": log_row["t_star"],
        "t_star_delta_at_log_step": log_row["t_star_delta"],

        "htr_delta_at_log_step": log_row["htr_delta"],
        "local_debt_at_log_step": log_row["local_debt"],
    }

    row["classification"] = classify(row)

    return row


def empty_stats():
    return {
        "total": 0,
        "improved": 0,
        "worsened": 0,
        "same": 0,

        "sum_log": 0,
        "sum_htr": 0,

        "max_log": 0,
        "max_htr": 0,

        "worst_loss": 0,
        "worst_loss_n": None,

        "best_gain": 0,
        "best_gain_n": None,

        "class_counts": {},

        "top_loss": [],
        "top_ratio": [],
        "top_hdelta": [],
    }


def add_top_item(items, row, key, limit=50):
    items.append(row)
    items.sort(key=lambda r: r[key], reverse=True)
    if len(items) > limit:
        del items[limit:]


def merge_stats(dst, src):
    dst["total"] += src["total"]
    dst["improved"] += src["improved"]
    dst["worsened"] += src["worsened"]
    dst["same"] += src["same"]

    dst["sum_log"] += src["sum_log"]
    dst["sum_htr"] += src["sum_htr"]

    dst["max_log"] = max(dst["max_log"], src["max_log"])
    dst["max_htr"] = max(dst["max_htr"], src["max_htr"])

    if src["worst_loss"] > dst["worst_loss"]:
        dst["worst_loss"] = src["worst_loss"]
        dst["worst_loss_n"] = src["worst_loss_n"]

    if src["best_gain"] > dst["best_gain"]:
        dst["best_gain"] = src["best_gain"]
        dst["best_gain_n"] = src["best_gain_n"]

    for k, v in src["class_counts"].items():
        dst["class_counts"][k] = dst["class_counts"].get(k, 0) + v

    for row in src["top_loss"]:
        add_top_item(dst["top_loss"], row, "loss")

    for row in src["top_ratio"]:
        add_top_item(dst["top_ratio"], row, "max_ratio")

    for row in src["top_hdelta"]:
        add_top_item(dst["top_hdelta"], row, "htr_delta_at_log_step")


def process_chunk(start_odd: int, end_odd: int):
    stats = empty_stats()
    worsening_rows = []

    for n in range(start_odd, end_odd + 1, 2):
        row = quick_analyze(n)

        log_step = row["log_step"]
        htr_step = row["htr_step"]

        stats["total"] += 1
        stats["sum_log"] += log_step
        stats["sum_htr"] += htr_step

        stats["max_log"] = max(stats["max_log"], log_step)
        stats["max_htr"] = max(stats["max_htr"], htr_step)

        if htr_step > log_step:
            stats["worsened"] += 1
            worsening_rows.append(row)

            main_class = row["classification"].split("+")[0]
            stats["class_counts"][main_class] = stats["class_counts"].get(main_class, 0) + 1

            if row["loss"] > stats["worst_loss"]:
                stats["worst_loss"] = row["loss"]
                stats["worst_loss_n"] = n

            add_top_item(stats["top_loss"], row, "loss")
            add_top_item(stats["top_ratio"], row, "max_ratio")
            add_top_item(stats["top_hdelta"], row, "htr_delta_at_log_step")

        elif htr_step < log_step:
            stats["improved"] += 1
            gain = log_step - htr_step

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
        "worsening_rows": worsening_rows,
    }


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


def format_row(r):
    return (
        f"n={r['start']:10d} | "
        f"class={r['classification']} | "
        f"log_step={r['log_step']:4d} | "
        f"htr_step={r['htr_step']:4d} | "
        f"loss={r['loss']:4d} | "
        f"max_ratio={r['max_ratio']:14.3f} | "
        f"ratio_1={r['ratio_1_until_h']:.6f} | "
        f"pmax_log={r['pmax_at_log_step']:.6f} | "
        f"t_star_log={r['t_star_at_log_step']:.6f} | "
        f"dmax_delta={r['dmax_delta_at_log_step']:+.6f} | "
        f"cmax_delta={r['cmax_delta_at_log_step']:+.6f} | "
        f"htr_delta_log={r['htr_delta_at_log_step']:+.6f}"
    )


def export_summary(stats, elapsed):
    total = stats["total"]

    lines = []

    lines.append("VALIDAZIONE 100M — H_TR MICRO-CORREZIONE T_RISK")
    lines.append("=" * 120)
    lines.append("")
    lines.append("Funzione:")
    lines.append("-" * 120)
    lines.append("H_TR(n) = H(n) + eta*T_risk(n)")
    lines.append("H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)")
    lines.append("T_risk(n) = max(0, T_star80(n) - alpha*Cmax80(n))")
    lines.append("")
    lines.append(f"ALPHA = {ALPHA}")
    lines.append(f"ETA = {ETA}")
    lines.append("")
    lines.append("Config:")
    lines.append("-" * 120)
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"LOOKAHEAD = {LOOKAHEAD}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"CPU_COUNT = {CPU_COUNT}")
    lines.append(f"WORKERS = {WORKERS}")
    lines.append(f"CHUNK_SIZE = {CHUNK_SIZE}")
    lines.append(f"Tempo totale secondi = {elapsed:.2f}")
    lines.append("")

    lines.append("Riferimento base H 100M:")
    lines.append("-" * 120)
    lines.append("Base H 100M: avg_H=3.131343 | max_H=190 | worsened=2839 | false=167")
    lines.append("")

    lines.append("Statistiche globali:")
    lines.append("-" * 120)
    lines.append(f"Totale dispari analizzati: {total}")
    lines.append(f"Improved: {stats['improved']} ({stats['improved'] / total:.8f})")
    lines.append(f"Worsened: {stats['worsened']} ({stats['worsened'] / total:.8f})")
    lines.append(f"Same: {stats['same']} ({stats['same'] / total:.8f})")
    lines.append("")
    lines.append(f"Avg log step: {stats['sum_log'] / total:.6f}")
    lines.append(f"Avg HTR step: {stats['sum_htr'] / total:.6f}")
    lines.append(f"Max log step: {stats['max_log']}")
    lines.append(f"Max HTR step: {stats['max_htr']}")
    lines.append(f"Worst loss: {stats['worst_loss']} su n={stats['worst_loss_n']}")
    lines.append(f"Best gain: {stats['best_gain']} su n={stats['best_gain_n']}")
    lines.append("")

    lines.append("Classificazione peggioramenti:")
    lines.append("-" * 120)
    for k, v in sorted(stats["class_counts"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{k}: {v}")

    lines.append("")
    lines.append("Top 50 per loss:")
    lines.append("-" * 120)
    for r in stats["top_loss"]:
        lines.append(format_row(r))

    lines.append("")
    lines.append("Top 50 per max_ratio:")
    lines.append("-" * 120)
    for r in stats["top_ratio"]:
        lines.append(format_row(r))

    lines.append("")
    lines.append("Top 50 per htr_delta al log-step:")
    lines.append("-" * 120)
    for r in stats["top_hdelta"]:
        lines.append(format_row(r))

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    started = time.time()

    chunks = make_chunks()
    global_stats = empty_stats()
    all_worsening_rows = []

    print("Validazione 100M — H_TR eta=0.0025")
    print("-" * 120)
    print(f"LIMIT = {LIMIT}")
    print(f"ALPHA = {ALPHA}")
    print(f"ETA = {ETA}")
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
            all_worsening_rows.extend(result["worsening_rows"])

            elapsed = time.time() - started

            print(
                f"chunk {completed:4d}/{len(chunks)} | "
                f"range={result['start']}-{result['end']} | "
                f"processed={processed_total:,} | "
                f"worsened={global_stats['worsened']} | "
                f"elapsed={elapsed:.1f}s"
            )

    elapsed = time.time() - started

    export_csv(all_worsening_rows)
    export_summary(global_stats, elapsed)

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"Peggioramenti: {global_stats['worsened']}")
    print(f"CSV: {OUTPUT_FILE}")
    print(f"Summary: {SUMMARY_FILE}")
    print()
    print("Per aprire:")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
