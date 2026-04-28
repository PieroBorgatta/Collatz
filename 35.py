import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache


OUTPUT_FILE = "collatz_35_scan_debt_cascade_pressure.csv"
SUMMARY_FILE = "collatz_35_summary_debt_cascade_pressure.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
LOOKAHEAD = 80

CRITICAL = math.log2(3)

# Base prudente trovata:
# lambda=0.30, mu=0.04
LAMBDAS = [0.28, 0.30, 0.32, 0.34]
MUS = [0.02, 0.03, 0.04, 0.05, 0.06]

# Nuovo termine: pressione espansiva data dalla densità di v2=1.
# Theta > 0 penalizza i corridoi con molti v2=1.
THETAS = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

CPU_COUNT = os.cpu_count() or 4
WORKERS = max(1, CPU_COUNT - 1)
CHUNK_SIZE = 25_000


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


@lru_cache(maxsize=600_000)
def future_metrics(n: int):
    """
    Metriche future entro LOOKAHEAD.

    Dmax:
        massimo debito futuro:
        D(k) = k*log2(3) - sum(v2)

    Cmax:
        massimo surplus/cascata futura:
        C(k) = sum(v2) - k*log2(3)

    Pmax:
        massima pressione espansiva:
        P(k) = (# v2=1 nei primi k passi) / k

    Pavg:
        densità media di v2=1 nei primi LOOKAHEAD passi.
    """
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

    max_single_v2 = 0
    max_single_v2_step = 0

    longest_run_1 = 0
    current_run_1 = 0

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


def empty_stats():
    return {
        "total": 0,
        "sum_log": 0,
        "sum_h": 0,
        "max_log": 0,
        "max_h": 0,
        "improved": 0,
        "worsened": 0,
        "same": 0,
        "worst_loss": 0,
        "worst_loss_n": None,
        "best_gain": 0,
        "best_gain_n": None,
    }


def merge_stats(target, source):
    target["total"] += source["total"]
    target["sum_log"] += source["sum_log"]
    target["sum_h"] += source["sum_h"]

    target["max_log"] = max(target["max_log"], source["max_log"])
    target["max_h"] = max(target["max_h"], source["max_h"])

    target["improved"] += source["improved"]
    target["worsened"] += source["worsened"]
    target["same"] += source["same"]

    if source["worst_loss"] > target["worst_loss"]:
        target["worst_loss"] = source["worst_loss"]
        target["worst_loss_n"] = source["worst_loss_n"]

    if source["best_gain"] > target["best_gain"]:
        target["best_gain"] = source["best_gain"]
        target["best_gain_n"] = source["best_gain_n"]


def analyze_number_for_all_params(start: int):
    """
    Calcola una sola traiettoria e valuta tutte le combinazioni lambda/mu/theta.
    """
    trajectory = [start]
    n = start

    log_step = None

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, _ = syracuse(n)
        trajectory.append(n)

        if log_step is None and n < start:
            log_step = step

        if n == 1:
            break

    if log_step is None:
        log_step = MAX_BLOCK_STEPS + 1

    start_log = math.log(start)
    start_metrics = future_metrics(start)

    start_h_values = {}

    for lam in LAMBDAS:
        for mu in MUS:
            for theta in THETAS:
                start_h_values[(lam, mu, theta)] = (
                    start_log
                    + lam * start_metrics["dmax"]
                    - mu * start_metrics["cmax"]
                    + theta * start_metrics["pmax"]
                )

    h_steps = {
        (lam, mu, theta): None
        for lam in LAMBDAS
        for mu in MUS
        for theta in THETAS
    }

    for step, value in enumerate(trajectory[1:], start=1):
        value_log = math.log(value)
        value_metrics = future_metrics(value)

        for lam in LAMBDAS:
            for mu in MUS:
                for theta in THETAS:
                    key = (lam, mu, theta)

                    if h_steps[key] is not None:
                        continue

                    current_h = (
                        value_log
                        + lam * value_metrics["dmax"]
                        - mu * value_metrics["cmax"]
                        + theta * value_metrics["pmax"]
                    )

                    if current_h < start_h_values[key]:
                        h_steps[key] = step

        if all(v is not None for v in h_steps.values()):
            break

    for key in h_steps:
        if h_steps[key] is None:
            h_steps[key] = MAX_BLOCK_STEPS + 1

    return log_step, h_steps


def process_chunk(start_odd: int, end_odd: int):
    local_stats = {
        (lam, mu, theta): empty_stats()
        for lam in LAMBDAS
        for mu in MUS
        for theta in THETAS
    }

    processed = 0

    for n in range(start_odd, end_odd + 1, 2):
        processed += 1

        log_step, h_steps = analyze_number_for_all_params(n)

        for lam in LAMBDAS:
            for mu in MUS:
                for theta in THETAS:
                    key = (lam, mu, theta)
                    h_step = h_steps[key]
                    st = local_stats[key]

                    st["total"] += 1
                    st["sum_log"] += log_step
                    st["sum_h"] += h_step

                    st["max_log"] = max(st["max_log"], log_step)
                    st["max_h"] = max(st["max_h"], h_step)

                    if h_step < log_step:
                        st["improved"] += 1
                        gain = log_step - h_step

                        if gain > st["best_gain"]:
                            st["best_gain"] = gain
                            st["best_gain_n"] = n

                    elif h_step > log_step:
                        st["worsened"] += 1
                        loss = h_step - log_step

                        if loss > st["worst_loss"]:
                            st["worst_loss"] = loss
                            st["worst_loss_n"] = n

                    else:
                        st["same"] += 1

    return {
        "start": start_odd,
        "end": end_odd,
        "processed": processed,
        "stats": local_stats,
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


def export_csv(filename: str, rows: list):
    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list, elapsed: float):
    by_worsened = sorted(
        rows,
        key=lambda r: (
            r["worsened"],
            r["max_h_step"],
            r["avg_h_step"],
        )
    )

    by_avg = sorted(
        rows,
        key=lambda r: (
            r["avg_h_step"],
            r["worsened"],
        )
    )

    by_score = sorted(
        rows,
        key=lambda r: (
            r["score_avg_gain"],
            -r["worsened"],
        ),
        reverse=True
    )

    by_max = sorted(
        rows,
        key=lambda r: (
            r["max_h_step"],
            r["worsened"],
            r["avg_h_step"],
        )
    )

    lines = []

    lines.append("SCAN H = log(n) + lambda*Dmax80(n) - mu*Cmax80(n) + theta*Pmax80(n)")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"LOOKAHEAD = {LOOKAHEAD}")
    lines.append(f"LAMBDAS = {LAMBDAS}")
    lines.append(f"MUS = {MUS}")
    lines.append(f"THETAS = {THETAS}")
    lines.append(f"CPU_COUNT = {CPU_COUNT}")
    lines.append(f"WORKERS = {WORKERS}")
    lines.append(f"CHUNK_SIZE = {CHUNK_SIZE}")
    lines.append(f"Tempo totale secondi = {elapsed:.2f}")
    lines.append("")

    lines.append("Candidato precedente:")
    lines.append("lambda=0.30 | mu=0.04 | theta=0.00 | avg_H=3.147416 | max_H=140 | improved=341157 | worsened=86")
    lines.append("")

    sections = [
        ("Migliori per pochi peggioramenti", by_worsened),
        ("Migliori per media H più bassa", by_avg),
        ("Migliori per guadagno medio", by_score),
        ("Migliori per max step", by_max),
    ]

    for title, data in sections:
        lines.append(title)
        lines.append("-" * 120)

        for r in data[:30]:
            lines.append(
                f"lambda={r['lambda']:.2f} | "
                f"mu={r['mu']:.2f} | "
                f"theta={r['theta']:.2f} | "
                f"avg_H={r['avg_h_step']:.6f} | "
                f"max_H={r['max_h_step']:3d} | "
                f"improved={r['improved']:8d} | "
                f"worsened={r['worsened']:8d} | "
                f"worst_loss={r['worst_loss']:4d} | "
                f"score={r['score_avg_gain']:+.6f} | "
                f"worst_n={r['worst_loss_n']} | "
                f"best_n={r['best_gain_n']}"
            )

        lines.append("")

    conservative = by_worsened[0]
    best_avg = by_avg[0]
    best_max = by_max[0]

    lines.append("RISULTATI SINTETICI")
    lines.append("=" * 120)
    lines.append("")

    lines.append("Migliore candidata conservativa:")
    lines.append(
        f"lambda={conservative['lambda']:.2f}, "
        f"mu={conservative['mu']:.2f}, "
        f"theta={conservative['theta']:.2f}, "
        f"avg_H={conservative['avg_h_step']:.6f}, "
        f"max_H={conservative['max_h_step']}, "
        f"improved={conservative['improved']}, "
        f"worsened={conservative['worsened']}, "
        f"worst_loss={conservative['worst_loss']}"
    )

    lines.append("")
    lines.append("Migliore per media:")
    lines.append(
        f"lambda={best_avg['lambda']:.2f}, "
        f"mu={best_avg['mu']:.2f}, "
        f"theta={best_avg['theta']:.2f}, "
        f"avg_H={best_avg['avg_h_step']:.6f}, "
        f"max_H={best_avg['max_h_step']}, "
        f"improved={best_avg['improved']}, "
        f"worsened={best_avg['worsened']}, "
        f"worst_loss={best_avg['worst_loss']}"
    )

    lines.append("")
    lines.append("Migliore per massimo step:")
    lines.append(
        f"lambda={best_max['lambda']:.2f}, "
        f"mu={best_max['mu']:.2f}, "
        f"theta={best_max['theta']:.2f}, "
        f"avg_H={best_max['avg_h_step']:.6f}, "
        f"max_H={best_max['max_h_step']}, "
        f"improved={best_max['improved']}, "
        f"worsened={best_max['worsened']}, "
        f"worst_loss={best_max['worst_loss']}"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    started = time.time()

    chunks = make_chunks()

    global_stats = {
        (lam, mu, theta): empty_stats()
        for lam in LAMBDAS
        for mu in MUS
        for theta in THETAS
    }

    print("Scan debito + cascata + pressione v2=1")
    print("-" * 120)
    print(f"LIMIT = {LIMIT}")
    print(f"LAMBDAS = {LAMBDAS}")
    print(f"MUS = {MUS}")
    print(f"THETAS = {THETAS}")
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

            for key in global_stats:
                merge_stats(global_stats[key], result["stats"][key])

            elapsed = time.time() - started

            print(
                f"chunk {completed:4d}/{len(chunks)} | "
                f"range={result['start']}-{result['end']} | "
                f"processed_total={processed_total:,} | "
                f"elapsed={elapsed:.1f}s"
            )

    rows = []

    for lam in LAMBDAS:
        for mu in MUS:
            for theta in THETAS:
                key = (lam, mu, theta)
                st = global_stats[key]
                total = st["total"]

                row = {
                    "lambda": lam,
                    "mu": mu,
                    "theta": theta,
                    "total": total,
                    "avg_log_step": st["sum_log"] / total,
                    "avg_h_step": st["sum_h"] / total,
                    "max_log_step": st["max_log"],
                    "max_h_step": st["max_h"],
                    "improved": st["improved"],
                    "worsened": st["worsened"],
                    "same": st["same"],
                    "improved_ratio": st["improved"] / total,
                    "worsened_ratio": st["worsened"] / total,
                    "same_ratio": st["same"] / total,
                    "worst_loss": st["worst_loss"],
                    "worst_loss_n": st["worst_loss_n"],
                    "best_gain": st["best_gain"],
                    "best_gain_n": st["best_gain_n"],
                    "score_avg_gain": (st["sum_log"] - st["sum_h"]) / total,
                }

                rows.append(row)

    rows.sort(key=lambda r: (r["lambda"], r["mu"], r["theta"]))

    elapsed = time.time() - started

    export_csv(OUTPUT_FILE, rows)
    export_summary(SUMMARY_FILE, rows, elapsed)

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
