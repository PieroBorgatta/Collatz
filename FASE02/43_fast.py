#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASE 02 — Script 43 FAST
Test H_TR = H + eta * T_risk

Dove:

    H(n) = log(n) + 0.28*Dmax80 - 0.03*Cmax80 + 0.30*Pmax80

    T_star80(n) =
        max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)

    T_risk(n) = max(0, T_star80(n) - alpha*Cmax80(n))

    H_TR(n) = H(n) + eta*T_risk(n)

Idea:
- T_star misura tensione elastica espansiva;
- Cmax80 misura cascata dissipativa già visibile;
- T_risk misura solo la tensione non compensata.

Obiettivo:
- mantenere gli improved alti;
- ridurre falsi allarmi rispetto a H + eta*T_star;
- trovare una coppia alpha/eta migliore.

Output:
- collatz_43_fast_trisk_summary.txt
- collatz_43_fast_trisk_worsenings.csv
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

ALPHA_VALUES = [1.0, 1.5, 2.0, 2.5, 3.0]
ETA_VALUES = [0.004, 0.005, 0.006, 0.007]

CPU_COUNT = os.cpu_count() or 8
WORKERS = max(1, CPU_COUNT - 1)

CHUNK_SIZE = 20_000

OUTPUT_WORSENINGS = "collatz_43_fast_trisk_worsenings.csv"
OUTPUT_SUMMARY = "collatz_43_fast_trisk_summary.txt"

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

@dataclass(slots=True)
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
    t_star_step: int


def compute_metrics(n: int) -> Metrics:
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
        t_star_step=t_star_step,
    )


def t_risk(m: Metrics, alpha: float) -> float:
    value = m.t_star - alpha * m.cmax
    return value if value > 0 else 0.0


def h_tr(m: Metrics, alpha: float, eta: float) -> float:
    return m.base_h + eta * t_risk(m, alpha)


# =============================================================================
# ANALISI
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
    htr_step: int,
    m_start: Metrics,
    m_log: Metrics,
    alpha: float,
) -> str:
    max_ratio = max(values) / n if values else 1.0

    ratio_1_until_h = 0.0
    if htr_step > 0:
        segment = a_values[: min(htr_step, len(a_values))]
        if segment:
            ratio_1_until_h = sum(1 for a in segment if a == 1) / len(segment)

    dmax_delta = m_log.dmax - m_start.dmax
    cmax_delta = m_log.cmax - m_start.cmax
    trisk_delta = t_risk(m_log, alpha) - t_risk(m_start, alpha)

    high_pressure = m_log.pmax >= 0.8 or ratio_1_until_h >= 0.65
    dmax_grows = dmax_delta > 0
    cmax_drops = cmax_delta < 0
    trisk_grows = trisk_delta > 0
    explosion = max_ratio >= 100

    loss = htr_step - log_step

    if loss >= 50 and dmax_grows and cmax_drops and high_pressure:
        return "VERO_RIBELLE_ESTREMO"

    if loss >= 10 and (dmax_grows or high_pressure or explosion or trisk_grows):
        return "VERO_RIBELLE"

    if loss >= 5:
        return "INTERMEDIO"

    return "FALSO_ALLARME"


def empty_stat() -> Dict[str, int]:
    return {
        "total": 0,
        "improved": 0,
        "worsened": 0,
        "same": 0,
        "log_step_sum": 0,
        "htr_step_sum": 0,
        "max_log_step": 0,
        "max_htr_step": 0,
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
    dst["htr_step_sum"] += src["htr_step_sum"]

    dst["max_log_step"] = max(dst["max_log_step"], src["max_log_step"])
    dst["max_htr_step"] = max(dst["max_htr_step"], src["max_htr_step"])

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


def analyze_number(n: int) -> Tuple[List[Dict[str, object]], Dict[str, Dict[str, int]]]:
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

    local_stats: Dict[str, Dict[str, int]] = {}
    worsening_rows: List[Dict[str, object]] = []

    for alpha in ALPHA_VALUES:
        for eta in ETA_VALUES:
            key = f"a={alpha:.2f}|e={eta:.3f}"

            h0 = h_tr(m_start, alpha, eta)

            htr_step: Optional[int] = None

            for k in range(1, len(values)):
                candidate = values[k]
                m_candidate = get_metrics(candidate)

                if h_tr(m_candidate, alpha, eta) < h0:
                    htr_step = k
                    break

            if htr_step is None:
                continue

            delta = htr_step - log_step

            stat = {
                "total": 1,
                "improved": 0,
                "worsened": 0,
                "same": 0,
                "log_step_sum": log_step,
                "htr_step_sum": htr_step,
                "max_log_step": log_step,
                "max_htr_step": htr_step,
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

            elif delta == 0:
                stat["same"] = 1

            else:
                stat["worsened"] = 1
                stat["worst_loss"] = delta
                stat["worst_loss_n"] = n

                cls = classify_worsening(
                    n=n,
                    values=values,
                    a_values=a_values,
                    log_step=log_step,
                    htr_step=htr_step,
                    m_start=m_start,
                    m_log=m_log,
                    alpha=alpha,
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

                tr_start = t_risk(m_start, alpha)
                tr_log = t_risk(m_log, alpha)

                worsening_rows.append({
                    "alpha": alpha,
                    "eta": eta,
                    "start": n,
                    "classification": cls,

                    "log_step": log_step,
                    "htr_step": htr_step,
                    "loss": delta,

                    "max_value": max_value,
                    "max_value_step": max_value_step,
                    "max_ratio": max_value / n,

                    "initial_base_h": m_start.base_h,
                    "initial_t_star": m_start.t_star,
                    "initial_cmax": m_start.cmax,
                    "initial_t_risk": tr_start,
                    "initial_dmax": m_start.dmax,
                    "initial_pmax": m_start.pmax,
                    "initial_pavg": m_start.pavg,
                    "initial_lmax1": m_start.lmax1,
                    "initial_t_star_step": m_start.t_star_step,
                    "initial_debt_at_tension": m_start.debt_at_tension,
                    "initial_ratio1_at_tension": m_start.ratio1_at_tension,

                    "log_base_h": m_log.base_h,
                    "log_t_star": m_log.t_star,
                    "log_cmax": m_log.cmax,
                    "log_t_risk": tr_log,
                    "log_dmax": m_log.dmax,
                    "log_pmax": m_log.pmax,
                    "log_pavg": m_log.pavg,
                    "log_lmax1": m_log.lmax1,

                    "t_risk_delta_at_log_step": tr_log - tr_start,
                    "t_star_delta_at_log_step": m_log.t_star - m_start.t_star,
                    "dmax_delta_at_log_step": m_log.dmax - m_start.dmax,
                    "cmax_delta_at_log_step": m_log.cmax - m_start.cmax,
                    "pmax_delta_at_log_step": m_log.pmax - m_start.pmax,
                })

            local_stats[key] = stat

    return worsening_rows, local_stats


# =============================================================================
# WORKER
# =============================================================================

def process_chunk(start_odd: int, end_odd: int) -> Tuple[List[Dict[str, object]], Dict[str, Dict[str, int]], int]:
    keys = [f"a={a:.2f}|e={e:.3f}" for a in ALPHA_VALUES for e in ETA_VALUES]
    stats = {key: empty_stat() for key in keys}
    worsenings: List[Dict[str, object]] = []
    processed = 0

    for n in range(start_odd, end_odd, 2):
        processed += 1

        rows, local_stats = analyze_number(n)

        if rows:
            worsenings.extend(rows)

        for key, st in local_stats.items():
            merge_stat(stats[key], st)

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


def parse_key(key: str) -> Tuple[float, float]:
    # key = "a=1.00|e=0.004"
    left, right = key.split("|")
    alpha = float(left.split("=")[1])
    eta = float(right.split("=")[1])
    return alpha, eta


def write_summary(path: str, stats: Dict[str, Dict[str, int]], elapsed: float, processed: int) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("FASE 02 — SCRIPT 43 FAST — TEST T_RISK\n")
        f.write("=" * 100 + "\n\n")

        f.write("Funzione:\n")
        f.write("-" * 100 + "\n")
        f.write("H_TR(n) = H(n) + eta*T_risk(n)\n")
        f.write("T_risk(n) = max(0, T_star80(n) - alpha*Cmax80(n))\n\n")

        f.write("Config:\n")
        f.write("-" * 100 + "\n")
        f.write(f"LIMIT = {LIMIT}\n")
        f.write(f"LOOKAHEAD = {LOOKAHEAD}\n")
        f.write(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}\n")
        f.write(f"ALPHA_VALUES = {ALPHA_VALUES}\n")
        f.write(f"ETA_VALUES = {ETA_VALUES}\n")
        f.write(f"CPU_COUNT = {CPU_COUNT}\n")
        f.write(f"WORKERS = {WORKERS}\n")
        f.write(f"CHUNK_SIZE = {CHUNK_SIZE}\n")
        f.write(f"Processed odds = {processed}\n")
        f.write(f"Tempo totale secondi = {elapsed:.2f}\n\n")

        f.write("Statistiche globali:\n")
        f.write("-" * 100 + "\n")
        f.write(
            f"{'ALPHA':>8} {'ETA':>8} {'TOTAL':>10} {'IMPROVED':>12} {'WORSENED':>12} {'SAME':>12} "
            f"{'AVG_LOG':>12} {'AVG_HTR':>12} {'MAX_LOG':>10} {'MAX_HTR':>10} "
            f"{'WORST_LOSS':>12} {'N_LOSS':>12} {'BEST_GAIN':>12} {'N_GAIN':>12} "
            f"{'FALSE':>10}\n"
        )

        ordered_keys = sorted(stats.keys(), key=parse_key)

        best_score = None
        best_key = None

        rows_for_score = []

        for key in ordered_keys:
            alpha, eta = parse_key(key)
            st = stats[key]
            total = st["total"]

            avg_log = st["log_step_sum"] / total if total else 0.0
            avg_htr = st["htr_step_sum"] / total if total else 0.0

            f.write(
                f"{alpha:>8.2f} "
                f"{eta:>8.3f} "
                f"{total:>10} "
                f"{st['improved']:>12} "
                f"{st['worsened']:>12} "
                f"{st['same']:>12} "
                f"{avg_log:>12.6f} "
                f"{avg_htr:>12.6f} "
                f"{st['max_log_step']:>10} "
                f"{st['max_htr_step']:>10} "
                f"{st['worst_loss']:>12} "
                f"{st['worst_loss_n']:>12} "
                f"{st['best_gain']:>12} "
                f"{st['best_gain_n']:>12} "
                f"{st['falso_allarme']:>10}\n"
            )

            # score prudente: premia improved, penalizza worsened e falsi allarmi
            score = st["improved"] - 20 * st["worsened"] - 50 * st["falso_allarme"]

            rows_for_score.append((score, key, alpha, eta, st))

            if best_score is None or score > best_score:
                best_score = score
                best_key = key

        f.write("\nClassificazione peggioramenti:\n")
        f.write("-" * 100 + "\n")
        f.write(
            f"{'ALPHA':>8} {'ETA':>8} {'VERO_RIBELLE':>16} {'ESTREMO':>12} "
            f"{'INTERMEDIO':>14} {'FALSO_ALLARME':>16}\n"
        )

        for key in ordered_keys:
            alpha, eta = parse_key(key)
            st = stats[key]

            f.write(
                f"{alpha:>8.2f} "
                f"{eta:>8.3f} "
                f"{st['vero_ribelle']:>16} "
                f"{st['estremo']:>12} "
                f"{st['intermedio']:>14} "
                f"{st['falso_allarme']:>16}\n"
            )

        f.write("\nScore empirico grezzo:\n")
        f.write("-" * 100 + "\n")
        f.write("score = improved - 20*worsened - 50*falso_allarme\n\n")
        f.write(f"{'ALPHA':>8} {'ETA':>8} {'SCORE':>16}\n")

        for score, key, alpha, eta, st in sorted(rows_for_score, reverse=True):
            f.write(f"{alpha:>8.2f} {eta:>8.3f} {score:>16}\n")

        f.write("\n")
        f.write(f"Best key secondo score grezzo: {best_key} con score {best_score}\n")


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
    print("FASE 02 — SCRIPT 43 FAST — TEST T_RISK")
    print("=" * 100)
    print(f"LIMIT = {LIMIT}")
    print(f"ALPHA_VALUES = {ALPHA_VALUES}")
    print(f"ETA_VALUES = {ETA_VALUES}")
    print(f"CPU_COUNT = {CPU_COUNT}")
    print(f"WORKERS = {WORKERS}")
    print(f"CHUNK_SIZE = {CHUNK_SIZE}")
    print()

    if os.path.exists(OUTPUT_WORSENINGS):
        os.remove(OUTPUT_WORSENINGS)

    keys = [f"a={a:.2f}|e={e:.3f}" for a in ALPHA_VALUES for e in ETA_VALUES]
    global_stats = {key: empty_stat() for key in keys}

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

            for key in keys:
                merge_stat(global_stats[key], stats[key])

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
