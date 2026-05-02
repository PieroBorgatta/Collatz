#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASE 02 — Script 41 FAST
Calibrazione fine di eta per H_T = H + eta*T*

Questo script testa eta piccoli attorno al valore promettente 0.005.

Funzione:

    H_T(n) = log(n) + 0.28*Dmax80 - 0.03*Cmax80 + 0.30*Pmax80 + eta*T_star(n)

con:

    T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)

Obiettivo:
- confrontare eta=0 con eta piccoli;
- trovare il miglior compromesso tra:
    - aumento improved;
    - basso numero di worsened;
    - basso numero di falsi allarmi;
    - riduzione AVG_HT;
    - riduzione MAX_HT;
    - contenimento worst_loss.

Output:
- collatz_41_fast_eta_fine_summary.txt
- collatz_41_fast_eta_fine_worsenings.csv
"""

from __future__ import annotations

import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIG
# =============================================================================

LIMIT = 20_000_000
LOOKAHEAD = 80
MAX_BLOCK_STEPS = 400

ETA_VALUES = [
    0.000,
    0.002,
    0.003,
    0.004,
    0.005,
    0.006,
    0.007,
    0.008,
    0.010,
]

CPU_COUNT = os.cpu_count() or 8
WORKERS = max(1, CPU_COUNT - 1)

CHUNK_SIZE = 20_000

OUTPUT_WORSENINGS = "collatz_41_fast_eta_fine_worsenings.csv"
OUTPUT_SUMMARY = "collatz_41_fast_eta_fine_summary.txt"

LOG2_3 = math.log2(3)


# =============================================================================
# COLLATZ / SYRACUSE
# =============================================================================

def v2(x: int) -> int:
    return (x & -x).bit_length() - 1


def syracuse_step_odd(n: int) -> Tuple[int, int]:
    m = 3 * n + 1
    a = v2(m)
    return m >> a, a


def generate_orbit(n: int, max_steps: int) -> Tuple[List[int], List[int]]:
    values = [n]
    a_values: List[int] = []

    current = n

    for _ in range(max_steps):
        if current == 1:
            break

        current, a = syracuse_step_odd(current)
        values.append(current)
        a_values.append(a)

    return values, a_values


# =============================================================================
# METRICHE
# =============================================================================

@dataclass
class Metrics:
    base_h: float
    t_star: float
    dmax: float
    cmax: float
    pmax: float
    pavg: float
    lmax1: int
    debt_at_tension: float
    ratio1_at_tension: float


def compute_metrics(n: int) -> Metrics:
    """
    Calcola H base e T_star per un numero.
    """
    _, a_values = generate_orbit(n, LOOKAHEAD)

    if not a_values:
        return Metrics(
            base_h=math.log(n),
            t_star=0.0,
            dmax=0.0,
            cmax=0.0,
            pmax=0.0,
            pavg=0.0,
            lmax1=0,
            debt_at_tension=0.0,
            ratio1_at_tension=0.0,
        )

    dmax = float("-inf")
    cmax = float("-inf")
    pmax = 0.0

    ones_count = 0
    sum_a = 0

    t_star = float("-inf")
    debt_at_tension = 0.0
    ratio1_at_tension = 0.0

    lmax1 = 0
    current_run_1 = 0

    for k, a in enumerate(a_values, start=1):
        sum_a += a

        if a == 1:
            ones_count += 1
            current_run_1 += 1
            lmax1 = max(lmax1, current_run_1)
        else:
            current_run_1 = 0

        debt = k * LOG2_3 - sum_a
        cascade = sum_a - k * LOG2_3
        ratio1 = ones_count / k

        dmax = max(dmax, debt)
        cmax = max(cmax, cascade)
        pmax = max(pmax, ratio1)

        positive_debt = max(debt, 0.0)
        t_candidate = positive_debt * ratio1 * math.log2(k + 1)

        if t_candidate > t_star:
            t_star = t_candidate
            debt_at_tension = debt
            ratio1_at_tension = ratio1

    pavg = ones_count / len(a_values)

    base_h = (
        math.log(n)
        + 0.28 * dmax
        - 0.03 * cmax
        + 0.30 * pmax
    )

    return Metrics(
        base_h=base_h,
        t_star=t_star,
        dmax=dmax,
        cmax=cmax,
        pmax=pmax,
        pavg=pavg,
        lmax1=lmax1,
        debt_at_tension=debt_at_tension,
        ratio1_at_tension=ratio1_at_tension,
    )


def ht_value(metrics: Metrics, eta: float) -> float:
    return metrics.base_h + eta * metrics.t_star


# =============================================================================
# ANALISI NUMERO
# =============================================================================

def first_log_below_start(values: List[int], start: int) -> Optional[int]:
    for k in range(1, len(values)):
        if values[k] < start:
            return k
    return None


def classify_worsening(
    n: int,
    values: List[int],
    a_values: List[int],
    log_step: int,
    ht_step: int,
    m_start: Metrics,
    m_log: Metrics,
) -> str:
    max_ratio = max(values) / n if values else 1.0

    ratio_1_until_h = 0.0
    if ht_step > 0:
        segment = a_values[: min(ht_step, len(a_values))]
        if segment:
            ratio_1_until_h = sum(1 for a in segment if a == 1) / len(segment)

    dmax_delta = m_log.dmax - m_start.dmax
    cmax_delta = m_log.cmax - m_start.cmax

    high_pressure = m_log.pmax >= 0.8 or ratio_1_until_h >= 0.65
    dmax_grows = dmax_delta > 0
    cmax_drops = cmax_delta < 0
    explosion = max_ratio >= 100

    loss = ht_step - log_step

    if loss >= 50 and dmax_grows and cmax_drops and high_pressure:
        return "VERO_RIBELLE_ESTREMO"

    if loss >= 10 and (dmax_grows or high_pressure or explosion):
        return "VERO_RIBELLE"

    if loss >= 5:
        return "INTERMEDIO"

    return "FALSO_ALLARME"


def analyze_number(n: int) -> Tuple[List[Dict[str, object]], Dict[float, Dict[str, int]]]:
    values, a_values = generate_orbit(n, MAX_BLOCK_STEPS)

    log_step = first_log_below_start(values, n)

    if log_step is None:
        return [], {}

    metrics_cache: Dict[int, Metrics] = {}

    def get_metrics(x: int) -> Metrics:
        m = metrics_cache.get(x)
        if m is None:
            m = compute_metrics(x)
            metrics_cache[x] = m
        return m

    m_start = get_metrics(n)
    m_log = get_metrics(values[log_step])

    local_stats: Dict[float, Dict[str, int]] = {}
    worsening_rows: List[Dict[str, object]] = []

    for eta in ETA_VALUES:
        h0 = ht_value(m_start, eta)

        ht_step: Optional[int] = None

        for k in range(1, len(values)):
            candidate = values[k]
            m_candidate = get_metrics(candidate)

            if ht_value(m_candidate, eta) < h0:
                ht_step = k
                break

        if ht_step is None:
            continue

        delta = ht_step - log_step

        stat = {
            "total": 1,
            "improved": 0,
            "worsened": 0,
            "same": 0,
            "log_step_sum": log_step,
            "ht_step_sum": ht_step,
            "max_log_step": log_step,
            "max_ht_step": ht_step,
            "worst_loss": 0,
            "worst_loss_n": 0,
            "best_gain": 0,
            "best_gain_n": 0,
            "vero_ribelle": 0,
            "estremo": 0,
            "intermedio": 0,
            "falso_allarme": 0,
        }

        if delta < 0:
            stat["improved"] = 1
            stat["best_gain"] = -delta
            stat["best_gain_n"] = n

        elif delta > 0:
            stat["worsened"] = 1
            stat["worst_loss"] = delta
            stat["worst_loss_n"] = n

            cls = classify_worsening(
                n=n,
                values=values,
                a_values=a_values,
                log_step=log_step,
                ht_step=ht_step,
                m_start=m_start,
                m_log=m_log,
            )

            if cls == "VERO_RIBELLE_ESTREMO":
                stat["estremo"] = 1
            elif cls == "VERO_RIBELLE":
                stat["vero_ribelle"] = 1
            elif cls == "INTERMEDIO":
                stat["intermedio"] = 1
            else:
                stat["falso_allarme"] = 1

            max_value = max(values)
            max_value_step = values.index(max_value)

            worsening_rows.append({
                "eta": eta,
                "start": n,
                "classification": cls,
                "log_step": log_step,
                "ht_step": ht_step,
                "loss": delta,
                "max_value": max_value,
                "max_value_step": max_value_step,
                "max_ratio": max_value / n,

                "initial_t_star": m_start.t_star,
                "initial_dmax": m_start.dmax,
                "initial_cmax": m_start.cmax,
                "initial_pmax": m_start.pmax,
                "initial_pavg": m_start.pavg,
                "initial_lmax1": m_start.lmax1,
                "initial_debt_at_tension": m_start.debt_at_tension,
                "initial_ratio1_at_tension": m_start.ratio1_at_tension,

                "log_t_star": m_log.t_star,
                "log_dmax": m_log.dmax,
                "log_cmax": m_log.cmax,
                "log_pmax": m_log.pmax,
                "log_pavg": m_log.pavg,

                "t_star_delta_at_log_step": m_log.t_star - m_start.t_star,
                "dmax_delta_at_log_step": m_log.dmax - m_start.dmax,
                "cmax_delta_at_log_step": m_log.cmax - m_start.cmax,
                "pmax_delta_at_log_step": m_log.pmax - m_start.pmax,
            })

        else:
            stat["same"] = 1

        local_stats[eta] = stat

    return worsening_rows, local_stats


# =============================================================================
# BATCH / MULTIPROCESS
# =============================================================================

def empty_stat() -> Dict[str, int]:
    return {
        "total": 0,
        "improved": 0,
        "worsened": 0,
        "same": 0,
        "log_step_sum": 0,
        "ht_step_sum": 0,
        "max_log_step": 0,
        "max_ht_step": 0,
        "worst_loss": 0,
        "worst_loss_n": 0,
        "best_gain": 0,
        "best_gain_n": 0,
        "vero_ribelle": 0,
        "estremo": 0,
        "intermedio": 0,
        "falso_allarme": 0,
    }


def merge_stat(dst: Dict[str, int], src: Dict[str, int]) -> None:
    dst["total"] += src["total"]
    dst["improved"] += src["improved"]
    dst["worsened"] += src["worsened"]
    dst["same"] += src["same"]

    dst["log_step_sum"] += src["log_step_sum"]
    dst["ht_step_sum"] += src["ht_step_sum"]

    dst["max_log_step"] = max(dst["max_log_step"], src["max_log_step"])
    dst["max_ht_step"] = max(dst["max_ht_step"], src["max_ht_step"])

    if src["worst_loss"] > dst["worst_loss"]:
        dst["worst_loss"] = src["worst_loss"]
        dst["worst_loss_n"] = src["worst_loss_n"]

    if src["best_gain"] > dst["best_gain"]:
        dst["best_gain"] = src["best_gain"]
        dst["best_gain_n"] = src["best_gain_n"]

    dst["vero_ribelle"] += src["vero_ribelle"]
    dst["estremo"] += src["estremo"]
    dst["intermedio"] += src["intermedio"]
    dst["falso_allarme"] += src["falso_allarme"]


def process_chunk(start_odd: int, end_odd: int) -> Tuple[List[Dict[str, object]], Dict[float, Dict[str, int]], int]:
    stats = {eta: empty_stat() for eta in ETA_VALUES}
    worsenings: List[Dict[str, object]] = []
    processed = 0

    for n in range(start_odd, end_odd, 2):
        processed += 1

        rows, local_stats = analyze_number(n)

        if rows:
            worsenings.extend(rows)

        for eta, st in local_stats.items():
            merge_stat(stats[eta], st)

    return worsenings, stats, processed


# =============================================================================
# OUTPUT
# =============================================================================

def append_csv(path: str, rows: List[Dict[str, object]], write_header: bool) -> None:
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        for row in rows:
            clean = {}
            for k, v in row.items():
                if isinstance(v, float):
                    clean[k] = f"{v:.12f}"
                else:
                    clean[k] = v
            writer.writerow(clean)


def write_summary(path: str, stats: Dict[float, Dict[str, int]], elapsed: float, processed: int) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("FASE 02 — SCRIPT 41 FAST — CALIBRAZIONE FINE ETA\n")
        f.write("=" * 100 + "\n\n")

        f.write(f"LIMIT = {LIMIT}\n")
        f.write(f"LOOKAHEAD = {LOOKAHEAD}\n")
        f.write(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}\n")
        f.write(f"ETA_VALUES = {ETA_VALUES}\n")
        f.write(f"CPU_COUNT = {CPU_COUNT}\n")
        f.write(f"WORKERS = {WORKERS}\n")
        f.write(f"CHUNK_SIZE = {CHUNK_SIZE}\n")
        f.write(f"Processed odds = {processed}\n")
        f.write(f"Tempo totale secondi = {elapsed:.2f}\n\n")

        f.write("Funzione:\n")
        f.write("-" * 100 + "\n")
        f.write("H_T(n) = log(n) + 0.28*Dmax80 - 0.03*Cmax80 + 0.30*Pmax80 + eta*T_star\n\n")
        f.write("T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)\n\n")

        f.write("Statistiche globali per eta:\n")
        f.write("-" * 100 + "\n")
        f.write(
            f"{'ETA':>8} {'TOTAL':>10} {'IMPROVED':>12} {'WORSENED':>12} {'SAME':>12} "
            f"{'AVG_LOG':>12} {'AVG_HT':>12} {'MAX_LOG':>10} {'MAX_HT':>10} "
            f"{'WORST_LOSS':>12} {'N_LOSS':>12} {'BEST_GAIN':>12} {'N_GAIN':>12}\n"
        )

        for eta in ETA_VALUES:
            st = stats[eta]
            total = st["total"]

            avg_log = st["log_step_sum"] / total if total else 0.0
            avg_ht = st["ht_step_sum"] / total if total else 0.0

            f.write(
                f"{eta:>8.3f} "
                f"{total:>10} "
                f"{st['improved']:>12} "
                f"{st['worsened']:>12} "
                f"{st['same']:>12} "
                f"{avg_log:>12.6f} "
                f"{avg_ht:>12.6f} "
                f"{st['max_log_step']:>10} "
                f"{st['max_ht_step']:>10} "
                f"{st['worst_loss']:>12} "
                f"{st['worst_loss_n']:>12} "
                f"{st['best_gain']:>12} "
                f"{st['best_gain_n']:>12}\n"
            )

        f.write("\nClassificazione peggioramenti per eta:\n")
        f.write("-" * 100 + "\n")
        f.write(
            f"{'ETA':>8} {'VERO_RIBELLE':>16} {'ESTREMO':>12} "
            f"{'INTERMEDIO':>14} {'FALSO_ALLARME':>16}\n"
        )

        for eta in ETA_VALUES:
            st = stats[eta]

            f.write(
                f"{eta:>8.3f} "
                f"{st['vero_ribelle']:>16} "
                f"{st['estremo']:>12} "
                f"{st['intermedio']:>14} "
                f"{st['falso_allarme']:>16}\n"
            )

        f.write("\nScore empirico grezzo:\n")
        f.write("-" * 100 + "\n")
        f.write("score = improved - 20*worsened - 50*falso_allarme\n")
        f.write("Serve solo come euristica per scegliere eta, non ha valore matematico.\n\n")
        f.write(f"{'ETA':>8} {'SCORE':>16}\n")

        best_eta = None
        best_score = None

        for eta in ETA_VALUES:
            st = stats[eta]
            score = st["improved"] - 20 * st["worsened"] - 50 * st["falso_allarme"]

            if best_score is None or score > best_score:
                best_score = score
                best_eta = eta

            f.write(f"{eta:>8.3f} {score:>16}\n")

        f.write("\n")
        f.write(f"Best eta secondo score grezzo: {best_eta} con score {best_score}\n")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    start_time = time.time()

    print("=" * 100)
    print("FASE 02 — SCRIPT 41 FAST — CALIBRAZIONE FINE ETA")
    print("=" * 100)
    print(f"LIMIT = {LIMIT}")
    print(f"ETA_VALUES = {ETA_VALUES}")
    print(f"CPU_COUNT = {CPU_COUNT}")
    print(f"WORKERS = {WORKERS}")
    print(f"CHUNK_SIZE = {CHUNK_SIZE}")
    print()

    if os.path.exists(OUTPUT_WORSENINGS):
        os.remove(OUTPUT_WORSENINGS)

    global_stats = {eta: empty_stat() for eta in ETA_VALUES}

    total_odds = (LIMIT - 1) // 2
    processed_total = 0
    chunks_done = 0

    chunks = []

    start = 3
    while start < LIMIT:
        end = min(start + CHUNK_SIZE * 2, LIMIT)
        chunks.append((start, end))
        start = end if end % 2 == 1 else end + 1

    print(f"Chunks totali: {len(chunks)}")
    print()

    header_written = False

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        futures = [
            executor.submit(process_chunk, start_odd, end_odd)
            for start_odd, end_odd in chunks
        ]

        for future in as_completed(futures):
            worsenings, stats, processed = future.result()

            processed_total += processed
            chunks_done += 1

            for eta in ETA_VALUES:
                merge_stat(global_stats[eta], stats[eta])

            if worsenings:
                append_csv(
                    OUTPUT_WORSENINGS,
                    worsenings,
                    write_header=not header_written,
                )
                header_written = True

            elapsed = time.time() - start_time
            speed = processed_total / elapsed if elapsed > 0 else 0.0
            pct = processed_total / total_odds * 100

            print(
                f"chunks={chunks_done:>5}/{len(chunks)} | "
                f"processed={processed_total:>10}/{total_odds} ({pct:6.2f}%) | "
                f"speed={speed:,.0f} n/s | "
                f"elapsed={elapsed:.1f}s"
            )

            write_summary(
                OUTPUT_SUMMARY,
                global_stats,
                elapsed,
                processed_total,
            )

    elapsed = time.time() - start_time

    write_summary(
        OUTPUT_SUMMARY,
        global_stats,
        elapsed,
        processed_total,
    )

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"CSV peggioramenti: {OUTPUT_WORSENINGS}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print()
    print(f"open '{OUTPUT_SUMMARY}'")
    print(f"open '{OUTPUT_WORSENINGS}'")


if __name__ == "__main__":
    main()
