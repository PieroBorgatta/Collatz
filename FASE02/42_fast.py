#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASE 02 — Script 42 FAST
Validazione finale candidata H_T con eta = 0.006 fino a 100M.

Funzione:

    H_T(n) = log(n)
             + 0.28*Dmax80(n)
             - 0.03*Cmax80(n)
             + 0.30*Pmax80(n)
             + 0.006*T_star80(n)

dove:

    T_star80(n) =
        max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)

Obiettivo:
- validare la nuova funzione candidata su tutti i dispari fino a LIMIT;
- confrontare log_step vs HT_step;
- classificare i peggioramenti;
- produrre CSV peggioramenti + summary.

Output:
- collatz_42_eta006_validate_100M_worsenings.csv
- collatz_42_eta006_validate_100M_summary.txt
"""

from __future__ import annotations

import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIG
# =============================================================================

LIMIT = 100_000_000

LOOKAHEAD = 80
MAX_BLOCK_STEPS = 400

ETA = 0.006

CPU_COUNT = os.cpu_count() or 8
WORKERS = max(1, CPU_COUNT - 1)

CHUNK_SIZE = 100_000

OUTPUT_WORSENINGS = "collatz_42_eta006_validate_100M_worsenings.csv"
OUTPUT_SUMMARY = "collatz_42_eta006_validate_100M_summary.txt"

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

class Metrics:
    __slots__ = (
        "base_h",
        "t_star",
        "ht",
        "dmax",
        "cmax",
        "pmax",
        "pavg",
        "lmax1",
        "debt_at_tension",
        "ratio1_at_tension",
        "t_star_step",
    )

    def __init__(
        self,
        base_h: float,
        t_star: float,
        ht: float,
        dmax: float,
        cmax: float,
        pmax: float,
        pavg: float,
        lmax1: int,
        debt_at_tension: float,
        ratio1_at_tension: float,
        t_star_step: int,
    ):
        self.base_h = base_h
        self.t_star = t_star
        self.ht = ht
        self.dmax = dmax
        self.cmax = cmax
        self.pmax = pmax
        self.pavg = pavg
        self.lmax1 = lmax1
        self.debt_at_tension = debt_at_tension
        self.ratio1_at_tension = ratio1_at_tension
        self.t_star_step = t_star_step


def compute_metrics(n: int) -> Metrics:
    """
    Calcola H base, T_star e H_T per un numero.
    """
    _, a_values = generate_orbit(n, LOOKAHEAD)

    if not a_values:
        base_h = math.log(n)
        t_star = 0.0
        return Metrics(
            base_h=base_h,
            t_star=t_star,
            ht=base_h + ETA * t_star,
            dmax=0.0,
            cmax=0.0,
            pmax=0.0,
            pavg=0.0,
            lmax1=0,
            debt_at_tension=0.0,
            ratio1_at_tension=0.0,
            t_star_step=0,
        )

    dmax = float("-inf")
    cmax = float("-inf")
    pmax = 0.0

    ones_count = 0
    sum_a = 0

    t_star = float("-inf")
    t_star_step = 0
    debt_at_tension = 0.0
    ratio1_at_tension = 0.0

    lmax1 = 0
    current_run_1 = 0

    for k, a in enumerate(a_values, start=1):
        sum_a += a

        if a == 1:
            ones_count += 1
            current_run_1 += 1
            if current_run_1 > lmax1:
                lmax1 = current_run_1
        else:
            current_run_1 = 0

        debt = k * LOG2_3 - sum_a
        cascade = sum_a - k * LOG2_3
        ratio1 = ones_count / k

        if debt > dmax:
            dmax = debt

        if cascade > cmax:
            cmax = cascade

        if ratio1 > pmax:
            pmax = ratio1

        positive_debt = debt if debt > 0 else 0.0
        t_candidate = positive_debt * ratio1 * math.log2(k + 1)

        if t_candidate > t_star:
            t_star = t_candidate
            t_star_step = k
            debt_at_tension = debt
            ratio1_at_tension = ratio1

    pavg = ones_count / len(a_values)

    base_h = (
        math.log(n)
        + 0.28 * dmax
        - 0.03 * cmax
        + 0.30 * pmax
    )

    ht = base_h + ETA * t_star

    return Metrics(
        base_h=base_h,
        t_star=t_star,
        ht=ht,
        dmax=dmax,
        cmax=cmax,
        pmax=pmax,
        pavg=pavg,
        lmax1=lmax1,
        debt_at_tension=debt_at_tension,
        ratio1_at_tension=ratio1_at_tension,
        t_star_step=t_star_step,
    )


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
    t_star_delta = m_log.t_star - m_start.t_star

    high_pressure = m_log.pmax >= 0.8 or ratio_1_until_h >= 0.65
    dmax_grows = dmax_delta > 0
    cmax_drops = cmax_delta < 0
    tension_grows = t_star_delta > 0
    explosion = max_ratio >= 100

    loss = ht_step - log_step

    if loss >= 50 and dmax_grows and cmax_drops and high_pressure:
        return "VERO_RIBELLE_ESTREMO"

    if loss >= 10 and (dmax_grows or high_pressure or explosion or tension_grows):
        return "VERO_RIBELLE"

    if loss >= 5:
        return "INTERMEDIO"

    return "FALSO_ALLARME"


def analyze_number(n: int) -> Tuple[Optional[Dict[str, object]], Dict[str, int]]:
    values, a_values = generate_orbit(n, MAX_BLOCK_STEPS)

    log_step = first_log_below_start(values, n)

    if log_step is None:
        return None, {
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

    metrics_cache: Dict[int, Metrics] = {}

    def get_metrics(x: int) -> Metrics:
        m = metrics_cache.get(x)
        if m is None:
            m = compute_metrics(x)
            metrics_cache[x] = m
        return m

    m_start = get_metrics(n)
    m_log = get_metrics(values[log_step])

    h0 = m_start.ht

    ht_step: Optional[int] = None

    for k in range(1, len(values)):
        candidate = values[k]
        m_candidate = get_metrics(candidate)

        if m_candidate.ht < h0:
            ht_step = k
            break

    if ht_step is None:
        return None, {
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
        return None, stat

    if delta == 0:
        stat["same"] = 1
        return None, stat

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

    row = {
        "start": n,
        "classification": cls,

        "log_step": log_step,
        "ht_step": ht_step,
        "loss": delta,

        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / n,

        "initial_base_h": m_start.base_h,
        "initial_t_star": m_start.t_star,
        "initial_ht": m_start.ht,
        "initial_dmax": m_start.dmax,
        "initial_cmax": m_start.cmax,
        "initial_pmax": m_start.pmax,
        "initial_pavg": m_start.pavg,
        "initial_lmax1": m_start.lmax1,
        "initial_t_star_step": m_start.t_star_step,
        "initial_debt_at_tension": m_start.debt_at_tension,
        "initial_ratio1_at_tension": m_start.ratio1_at_tension,

        "log_base_h": m_log.base_h,
        "log_t_star": m_log.t_star,
        "log_ht": m_log.ht,
        "log_dmax": m_log.dmax,
        "log_cmax": m_log.cmax,
        "log_pmax": m_log.pmax,
        "log_pavg": m_log.pavg,
        "log_lmax1": m_log.lmax1,

        "t_star_delta_at_log_step": m_log.t_star - m_start.t_star,
        "dmax_delta_at_log_step": m_log.dmax - m_start.dmax,
        "cmax_delta_at_log_step": m_log.cmax - m_start.cmax,
        "pmax_delta_at_log_step": m_log.pmax - m_start.pmax,
    }

    return row, stat


# =============================================================================
# STATISTICHE / WORKER
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

    if src["max_log_step"] > dst["max_log_step"]:
        dst["max_log_step"] = src["max_log_step"]

    if src["max_ht_step"] > dst["max_ht_step"]:
        dst["max_ht_step"] = src["max_ht_step"]

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


def process_chunk(start_odd: int, end_odd: int) -> Tuple[List[Dict[str, object]], Dict[str, int], int]:
    stats = empty_stat()
    worsenings: List[Dict[str, object]] = []
    processed = 0

    for n in range(start_odd, end_odd, 2):
        processed += 1

        row, stat = analyze_number(n)

        merge_stat(stats, stat)

        if row is not None:
            worsenings.append(row)

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


def write_summary(path: str, stats: Dict[str, int], elapsed: float, processed: int) -> None:
    total = stats["total"]

    avg_log = stats["log_step_sum"] / total if total else 0.0
    avg_ht = stats["ht_step_sum"] / total if total else 0.0

    with open(path, "w", encoding="utf-8") as f:
        f.write("FASE 02 — SCRIPT 42 FAST — VALIDAZIONE H_T ETA=0.006\n")
        f.write("=" * 100 + "\n\n")

        f.write("Candidata finale:\n")
        f.write("-" * 100 + "\n")
        f.write("H_T(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n) + 0.006*T_star80(n)\n\n")
        f.write("T_star80(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)\n\n")

        f.write("Config:\n")
        f.write("-" * 100 + "\n")
        f.write(f"LIMIT = {LIMIT}\n")
        f.write(f"LOOKAHEAD = {LOOKAHEAD}\n")
        f.write(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}\n")
        f.write(f"ETA = {ETA}\n")
        f.write(f"CPU_COUNT = {CPU_COUNT}\n")
        f.write(f"WORKERS = {WORKERS}\n")
        f.write(f"CHUNK_SIZE = {CHUNK_SIZE}\n")
        f.write(f"Processed odds = {processed}\n")
        f.write(f"Tempo totale secondi = {elapsed:.2f}\n\n")

        f.write("Statistiche globali:\n")
        f.write("-" * 100 + "\n")
        f.write(f"Totale dispari analizzati: {total}\n")
        f.write(f"Improved: {stats['improved']} ({stats['improved'] / total:.8f})\n")
        f.write(f"Worsened: {stats['worsened']} ({stats['worsened'] / total:.8f})\n")
        f.write(f"Same: {stats['same']} ({stats['same'] / total:.8f})\n\n")

        f.write(f"Avg log step: {avg_log:.6f}\n")
        f.write(f"Avg HT step:  {avg_ht:.6f}\n")
        f.write(f"Max log step: {stats['max_log_step']}\n")
        f.write(f"Max HT step:  {stats['max_ht_step']}\n")
        f.write(f"Worst loss:   {stats['worst_loss']} su n={stats['worst_loss_n']}\n")
        f.write(f"Best gain:    {stats['best_gain']} su n={stats['best_gain_n']}\n\n")

        f.write("Classificazione peggioramenti:\n")
        f.write("-" * 100 + "\n")
        f.write(f"VERO_RIBELLE: {stats['vero_ribelle']}\n")
        f.write(f"VERO_RIBELLE_ESTREMO: {stats['estremo']}\n")
        f.write(f"INTERMEDIO: {stats['intermedio']}\n")
        f.write(f"FALSO_ALLARME: {stats['falso_allarme']}\n")


# =============================================================================
# MAIN
# =============================================================================

def build_chunks() -> List[Tuple[int, int]]:
    chunks: List[Tuple[int, int]] = []

    start = 3

    while start < LIMIT:
        end = min(start + CHUNK_SIZE * 2, LIMIT)

        if end % 2 == 0:
            end += 1

        chunks.append((start, end))
        start = end

    return chunks


def main() -> None:
    start_time = time.time()

    print("=" * 100)
    print("FASE 02 — SCRIPT 42 FAST — VALIDAZIONE H_T ETA=0.006")
    print("=" * 100)
    print(f"LIMIT = {LIMIT}")
    print(f"ETA = {ETA}")
    print(f"CPU_COUNT = {CPU_COUNT}")
    print(f"WORKERS = {WORKERS}")
    print(f"CHUNK_SIZE = {CHUNK_SIZE}")
    print()

    if os.path.exists(OUTPUT_WORSENINGS):
        os.remove(OUTPUT_WORSENINGS)

    global_stats = empty_stat()
    processed_total = 0
    chunks_done = 0
    header_written = False

    total_odds = (LIMIT - 1) // 2
    chunks = build_chunks()

    print(f"Chunks totali: {len(chunks)}")
    print()

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        futures = [
            executor.submit(process_chunk, start_odd, end_odd)
            for start_odd, end_odd in chunks
        ]

        for future in as_completed(futures):
            worsenings, stats, processed = future.result()

            processed_total += processed
            chunks_done += 1

            merge_stat(global_stats, stats)

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
                f"worsened={global_stats['worsened']} | "
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
