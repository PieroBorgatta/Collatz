import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache
from collections import Counter


SUMMARY_FILE = "collatz_44_fast_trisk_low_eta_summary.txt"
CSV_FILE = "collatz_44_fast_trisk_low_eta_results.csv"

LIMIT = 20_000_000
LOOKAHEAD = 80
MAX_BLOCK_STEPS = 400

# Candidata base:
LAMBDA = 0.28
MU = 0.03
THETA = 0.30

# Dal 43 il migliore era alpha=1.00.
ALPHA_VALUES = [1.00]

# Qui testiamo eta molto più basso.
ETA_VALUES = [
    0.0000,
    0.0005,
    0.0010,
    0.0015,
    0.0020,
    0.0025,
    0.0030,
    0.0035,
    0.0040,
]

CRITICAL = math.log2(3)

CPU_COUNT = os.cpu_count() or 4
WORKERS = max(1, CPU_COUNT - 1)

# Sul Mac M1 era andato bene 20.000.
CHUNK_SIZE = 20_000


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


@lru_cache(maxsize=600_000)
def future_metrics(n: int):
    """
    Metriche entro LOOKAHEAD:

    Dmax = massimo debito espansivo.
    Cmax = massima cascata dissipativa.
    Pmax = massima pressione v2=1.
    T_star = massimo run-weighted risk:
             cresce quando abbiamo lunghi tratti con pressione v2=1 alta.
    """
    current = n

    cumulative_v2 = 0
    count_1 = 0
    run_1 = 0
    max_run_1 = 0

    dmax = 0.0
    cmax = 0.0
    pmax = 0.0

    # T_star volutamente grezzo ma utile:
    # combina pressione cumulativa, debito e run consecutivi di v2=1.
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

        # rischio temporale:
        # - pressione alta
        # - debito positivo
        # - run consecutivo di 1
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


def htr_from_metrics(n: int, m, alpha: float, eta: float):
    base_h = base_H_from_metrics(n, m)
    t_risk = max(0.0, m["t_star"] - alpha * m["cmax"])
    return base_h + eta * t_risk


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
    }


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


def analyze_one(start: int):
    """
    Calcola traiettoria una volta sola.
    Poi valuta tutti gli eta/alpha.
    """
    trajectory = [start]
    a_seq = []

    n = start
    log_step = None

    max_value = start
    max_value_step = 0

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, a = syracuse(n)

        trajectory.append(n)
        a_seq.append(a)

        if n > max_value:
            max_value = n
            max_value_step = step

        if log_step is None and n < start:
            log_step = step

        if n == 1:
            break

    if log_step is None:
        log_step = MAX_BLOCK_STEPS + 1

    start_metrics = future_metrics(start)

    start_htr = {}
    for alpha in ALPHA_VALUES:
        for eta in ETA_VALUES:
            start_htr[(alpha, eta)] = htr_from_metrics(start, start_metrics, alpha, eta)

    htr_steps = {(alpha, eta): None for alpha in ALPHA_VALUES for eta in ETA_VALUES}
    log_row_by_key = {}

    initial_log = math.log(start)

    cumulative_v2 = 0
    seq_until = []

    for step, value in enumerate(trajectory[1:], start=1):
        a = a_seq[step - 1]
        cumulative_v2 += a
        seq_until.append(a)

        metrics = future_metrics(value)

        for alpha in ALPHA_VALUES:
            for eta in ETA_VALUES:
                key = (alpha, eta)

                if key not in log_row_by_key and step == log_step:
                    log_row_by_key[key] = {
                        "value": value,
                        "log_delta": math.log(value) - initial_log,
                        "dmax": metrics["dmax"],
                        "dmax_delta": metrics["dmax"] - start_metrics["dmax"],
                        "cmax": metrics["cmax"],
                        "cmax_delta": metrics["cmax"] - start_metrics["cmax"],
                        "pmax": metrics["pmax"],
                        "pmax_delta": metrics["pmax"] - start_metrics["pmax"],
                        "t_star": metrics["t_star"],
                        "t_star_delta": metrics["t_star"] - start_metrics["t_star"],
                        "h_delta": htr_from_metrics(value, metrics, alpha, eta) - start_htr[key],
                        "local_debt": step * CRITICAL - cumulative_v2,
                    }

                if htr_steps[key] is not None:
                    continue

                current_htr = htr_from_metrics(value, metrics, alpha, eta)

                if current_htr < start_htr[key]:
                    htr_steps[key] = step

        if all(v is not None for v in htr_steps.values()):
            break

    for key in htr_steps:
        if htr_steps[key] is None:
            htr_steps[key] = MAX_BLOCK_STEPS + 1

    return {
        "start": start,
        "log_step": log_step,
        "htr_steps": htr_steps,
        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / start,
        "a_seq": a_seq,
        "log_row_by_key": log_row_by_key,
    }


def process_chunk(start_odd: int, end_odd: int):
    local_stats = {
        (alpha, eta): empty_stats()
        for alpha in ALPHA_VALUES
        for eta in ETA_VALUES
    }

    processed = 0

    for n in range(start_odd, end_odd + 1, 2):
        processed += 1
        analysis = analyze_one(n)

        log_step = analysis["log_step"]
        max_ratio = analysis["max_ratio"]

        for alpha in ALPHA_VALUES:
            for eta in ETA_VALUES:
                key = (alpha, eta)
                htr_step = analysis["htr_steps"][key]
                st = local_stats[key]

                st["total"] += 1
                st["sum_log"] += log_step
                st["sum_htr"] += htr_step
                st["max_log"] = max(st["max_log"], log_step)
                st["max_htr"] = max(st["max_htr"], htr_step)

                if htr_step < log_step:
                    st["improved"] += 1
                    gain = log_step - htr_step
                    if gain > st["best_gain"]:
                        st["best_gain"] = gain
                        st["best_gain_n"] = n

                elif htr_step > log_step:
                    st["worsened"] += 1
                    loss = htr_step - log_step

                    if loss > st["worst_loss"]:
                        st["worst_loss"] = loss
                        st["worst_loss_n"] = n

                    seq = analysis["a_seq"][:htr_step]
                    counter = Counter(seq)
                    ratio_1 = counter.get(1, 0) / len(seq) if seq else 0.0
                    avg_v2 = sum(seq) / len(seq) if seq else 0.0

                    log_row = analysis["log_row_by_key"].get(key, {
                        "dmax_delta": 0.0,
                        "cmax_delta": 0.0,
                        "pmax": 0.0,
                        "h_delta": 0.0,
                    })

                    row = {
                        "loss": loss,
                        "max_ratio": max_ratio,
                        "ratio_1_until_h": ratio_1,
                        "avg_v2_until_h": avg_v2,
                        "pmax_at_log_step": log_row["pmax"],
                        "dmax_delta_at_log_step": log_row["dmax_delta"],
                        "cmax_delta_at_log_step": log_row["cmax_delta"],
                    }

                    cls = classify(row).split("+")[0]
                    st["class_counts"][cls] = st["class_counts"].get(cls, 0) + 1

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


def rows_from_stats(global_stats):
    rows = []

    for alpha in ALPHA_VALUES:
        for eta in ETA_VALUES:
            key = (alpha, eta)
            st = global_stats[key]
            total = st["total"]

            false_alarm = st["class_counts"].get("FALSO_ALLARME", 0)
            vero = st["class_counts"].get("VERO_RIBELLE", 0)
            estremo = st["class_counts"].get("VERO_RIBELLE_ESTREMO", 0)
            intermedio = st["class_counts"].get("INTERMEDIO", 0)

            score_grezzo = st["improved"] - 20 * st["worsened"] - 50 * false_alarm

            # Score più severo verso falsi allarmi e intermedi.
            score_clean = (
                st["improved"]
                - 20 * st["worsened"]
                - 100 * false_alarm
                - 30 * intermedio
            )

            rows.append({
                "alpha": alpha,
                "eta": eta,
                "total": total,
                "improved": st["improved"],
                "worsened": st["worsened"],
                "same": st["same"],
                "avg_log": st["sum_log"] / total,
                "avg_htr": st["sum_htr"] / total,
                "max_log": st["max_log"],
                "max_htr": st["max_htr"],
                "worst_loss": st["worst_loss"],
                "worst_loss_n": st["worst_loss_n"],
                "best_gain": st["best_gain"],
                "best_gain_n": st["best_gain_n"],
                "vero_ribelle": vero,
                "estremo": estremo,
                "intermedio": intermedio,
                "falso_allarme": false_alarm,
                "score_grezzo": score_grezzo,
                "score_clean": score_clean,
            })

    return rows


def export_csv(rows):
    fieldnames = list(rows[0].keys())

    with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(rows, elapsed):
    by_clean = sorted(rows, key=lambda r: r["score_clean"], reverse=True)
    by_false = sorted(rows, key=lambda r: (r["falso_allarme"], r["worsened"], r["avg_htr"]))
    by_avg = sorted(rows, key=lambda r: (r["avg_htr"], r["falso_allarme"]))
    by_max = sorted(rows, key=lambda r: (r["max_htr"], r["falso_allarme"], r["avg_htr"]))

    lines = []

    lines.append("FASE 03 — SCRIPT 44 FAST — T_RISK ETA BASSO")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Funzione:")
    lines.append("-" * 100)
    lines.append("H_TR(n) = H(n) + eta*T_risk(n)")
    lines.append("T_risk(n) = max(0, T_star80(n) - alpha*Cmax80(n))")
    lines.append("")
    lines.append("Config:")
    lines.append("-" * 100)
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"LOOKAHEAD = {LOOKAHEAD}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"ALPHA_VALUES = {ALPHA_VALUES}")
    lines.append(f"ETA_VALUES = {ETA_VALUES}")
    lines.append(f"CPU_COUNT = {CPU_COUNT}")
    lines.append(f"WORKERS = {WORKERS}")
    lines.append(f"CHUNK_SIZE = {CHUNK_SIZE}")
    lines.append(f"Tempo totale secondi = {elapsed:.2f}")
    lines.append("")

    lines.append("Riferimenti:")
    lines.append("-" * 100)
    lines.append("Base H 20M: avg_H=3.141184 | max_H=176 | worsened=408 | false=20")
    lines.append("43 migliore grezzo: alpha=1.00 eta=0.007 | avg_HTR=2.872979 | max_HTR=171 | worsened=468 | false=163")
    lines.append("")

    def section(title, data):
        lines.append(title)
        lines.append("-" * 100)
        lines.append(
            f"{'ALPHA':>8} {'ETA':>8} {'IMPROVED':>12} {'WORSENED':>10} {'AVG_HTR':>12} "
            f"{'MAX_HTR':>8} {'FALSE':>8} {'INTER':>8} {'VERO':>8} {'EXT':>8} {'SCORE_CLEAN':>14}"
        )

        for r in data:
            lines.append(
                f"{r['alpha']:8.2f} "
                f"{r['eta']:8.4f} "
                f"{r['improved']:12d} "
                f"{r['worsened']:10d} "
                f"{r['avg_htr']:12.6f} "
                f"{r['max_htr']:8d} "
                f"{r['falso_allarme']:8d} "
                f"{r['intermedio']:8d} "
                f"{r['vero_ribelle']:8d} "
                f"{r['estremo']:8d} "
                f"{r['score_clean']:14d}"
            )

        lines.append("")

    section("Migliori per score clean", by_clean)
    section("Migliori per pochi falsi allarmi", by_false)
    section("Migliori per media", by_avg)
    section("Migliori per max step", by_max)

    best = by_clean[0]

    lines.append("Verdetto provvisorio:")
    lines.append("-" * 100)
    lines.append(
        f"Best score_clean: alpha={best['alpha']:.2f}, eta={best['eta']:.4f}, "
        f"avg_HTR={best['avg_htr']:.6f}, max_HTR={best['max_htr']}, "
        f"worsened={best['worsened']}, false={best['falso_allarme']}, "
        f"intermedio={best['intermedio']}, score_clean={best['score_clean']}"
    )

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    started = time.time()

    chunks = make_chunks()

    global_stats = {
        (alpha, eta): empty_stats()
        for alpha in ALPHA_VALUES
        for eta in ETA_VALUES
    }

    print("Script 44 — T_risk eta basso")
    print("-" * 100)
    print(f"LIMIT = {LIMIT}")
    print(f"ALPHA_VALUES = {ALPHA_VALUES}")
    print(f"ETA_VALUES = {ETA_VALUES}")
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
                f"processed={processed_total:,} | "
                f"elapsed={elapsed:.1f}s"
            )

    elapsed = time.time() - started

    rows = rows_from_stats(global_stats)
    rows.sort(key=lambda r: (r["alpha"], r["eta"]))

    export_csv(rows)
    export_summary(rows, elapsed)

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"CSV: {CSV_FILE}")
    print(f"Summary: {SUMMARY_FILE}")
    print()
    print("Per aprire:")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
