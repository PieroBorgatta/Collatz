#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASE 02 — Script 40
Test nuova quasi-Lyapunov con Tensione Elastica T*

Funzione originale:

    H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)

Nuova funzione:

    H_T(n) = H(n) + eta*T_star(n)

dove:

    T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)

Obiettivo:
- testare diversi eta;
- confrontare log_step vs H_step vs H_T_step;
- vedere se H_T anticipa meglio i ribelli;
- verificare se riduce i peggioramenti o li rende più significativi.

Output:
- collatz_40_ht_eta_summary.txt
- collatz_40_ht_eta_results.csv
- collatz_40_ht_eta_worsenings.csv
"""

from __future__ import annotations

import csv
import math
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIG
# =============================================================================

LIMIT = 20_000_000

LOOKAHEAD = 80
MAX_BLOCK_STEPS = 400

ETA_VALUES = [0.005, 0.01, 0.02, 0.03, 0.05]

OUTPUT_RESULTS = "collatz_40_ht_eta_results.csv"
OUTPUT_WORSENINGS = "collatz_40_ht_eta_worsenings.csv"
OUTPUT_SUMMARY = "collatz_40_ht_eta_summary.txt"

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
# METRICHE H E T*
# =============================================================================

@dataclass
class WindowMetrics:
    dmax: float
    cmax: float
    pmax: float
    pavg: float
    t_star: float
    t_star_step: int
    lmax1: int
    debt_at_tension: float
    ratio1_at_tension: float


def compute_window_metrics(n: int, lookahead: int = LOOKAHEAD) -> WindowMetrics:
    _, a_values = generate_orbit(n, lookahead)

    if not a_values:
        return WindowMetrics(
            dmax=0.0,
            cmax=0.0,
            pmax=0.0,
            pavg=0.0,
            t_star=0.0,
            t_star_step=0,
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
            t_star_step = k
            debt_at_tension = debt
            ratio1_at_tension = ratio1

    pavg = ones_count / len(a_values)

    return WindowMetrics(
        dmax=dmax,
        cmax=cmax,
        pmax=pmax,
        pavg=pavg,
        t_star=t_star,
        t_star_step=t_star_step,
        lmax1=lmax1,
        debt_at_tension=debt_at_tension,
        ratio1_at_tension=ratio1_at_tension,
    )


def H_base(n: int) -> float:
    m = compute_window_metrics(n)

    return (
        math.log(n)
        + 0.28 * m.dmax
        - 0.03 * m.cmax
        + 0.30 * m.pmax
    )


def H_tension(n: int, eta: float) -> float:
    m = compute_window_metrics(n)

    h = (
        math.log(n)
        + 0.28 * m.dmax
        - 0.03 * m.cmax
        + 0.30 * m.pmax
        + eta * m.t_star
    )

    return h


# =============================================================================
# ANALISI TRAIETTORIA
# =============================================================================

@dataclass
class EtaStats:
    eta: float
    total: int = 0

    improved: int = 0
    worsened: int = 0
    same: int = 0

    avg_log_step_sum: int = 0
    avg_ht_step_sum: int = 0

    max_log_step: int = 0
    max_ht_step: int = 0

    worst_loss: int = 0
    worst_loss_n: int = 0

    best_gain: int = 0
    best_gain_n: int = 0

    true_rebel: int = 0
    extreme_rebel: int = 0
    intermediate: int = 0
    false_alarm: int = 0


def first_log_below_start(values: List[int], start: int) -> Optional[int]:
    for k in range(1, len(values)):
        if values[k] < start:
            return k
    return None


def max_ratio_until(values: List[int], start: int, until_step: int) -> float:
    if until_step <= 0:
        return 1.0

    segment = values[: min(len(values), until_step + 1)]
    return max(segment) / start


def classify_worsening(
    n: int,
    values: List[int],
    a_values: List[int],
    log_step: int,
    ht_step: int,
    wm_start: WindowMetrics,
    wm_log: WindowMetrics,
) -> str:
    max_ratio = max(values) / n if values else 1.0

    ratio_1_until_h = 0.0
    if ht_step > 0:
        segment = a_values[: min(ht_step, len(a_values))]
        if segment:
            ratio_1_until_h = sum(1 for a in segment if a == 1) / len(segment)

    dmax_delta = wm_log.dmax - wm_start.dmax
    cmax_delta = wm_log.cmax - wm_start.cmax

    high_pressure = wm_log.pmax >= 0.8 or ratio_1_until_h >= 0.65
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


def analyze_number_for_eta(n: int, eta: float) -> Optional[Dict[str, object]]:
    values, a_values = generate_orbit(n, MAX_BLOCK_STEPS)

    log_step = first_log_below_start(values, n)
    if log_step is None:
        return None

    h0 = H_tension(n, eta)

    ht_step: Optional[int] = None
    ht_value_at_step: Optional[float] = None

    for k in range(1, len(values)):
        candidate = values[k]
        h_candidate = H_tension(candidate, eta)

        if h_candidate < h0:
            ht_step = k
            ht_value_at_step = h_candidate
            break

    if ht_step is None:
        return None

    wm_start = compute_window_metrics(n)
    wm_log = compute_window_metrics(values[log_step])

    delta = ht_step - log_step

    if ht_step < log_step:
        result = "IMPROVED"
    elif ht_step > log_step:
        result = "WORSENED"
    else:
        result = "SAME"

    classification = ""

    if result == "WORSENED":
        classification = classify_worsening(
            n=n,
            values=values,
            a_values=a_values,
            log_step=log_step,
            ht_step=ht_step,
            wm_start=wm_start,
            wm_log=wm_log,
        )

    return {
        "eta": eta,
        "start": n,
        "result": result,
        "classification": classification,

        "log_step": log_step,
        "ht_step": ht_step,
        "delta": delta,

        "max_value": max(values),
        "max_value_step": values.index(max(values)),
        "max_ratio": max(values) / n,

        "initial_dmax": wm_start.dmax,
        "initial_cmax": wm_start.cmax,
        "initial_pmax": wm_start.pmax,
        "initial_pavg": wm_start.pavg,
        "initial_t_star": wm_start.t_star,
        "initial_t_star_step": wm_start.t_star_step,
        "initial_lmax1": wm_start.lmax1,
        "initial_debt_at_tension": wm_start.debt_at_tension,
        "initial_ratio1_at_tension": wm_start.ratio1_at_tension,

        "log_dmax": wm_log.dmax,
        "log_cmax": wm_log.cmax,
        "log_pmax": wm_log.pmax,
        "log_pavg": wm_log.pavg,
        "log_t_star": wm_log.t_star,

        "dmax_delta_at_log_step": wm_log.dmax - wm_start.dmax,
        "cmax_delta_at_log_step": wm_log.cmax - wm_start.cmax,
        "pmax_delta_at_log_step": wm_log.pmax - wm_start.pmax,
        "t_star_delta_at_log_step": wm_log.t_star - wm_start.t_star,
    }


# =============================================================================
# OUTPUT
# =============================================================================

def write_csv(path: str, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            clean = {}
            for k, v in row.items():
                if isinstance(v, float):
                    clean[k] = f"{v:.12f}"
                else:
                    clean[k] = v
            writer.writerow(clean)


def write_summary(path: str, stats_by_eta: Dict[float, EtaStats], elapsed: float) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("FASE 02 — SCRIPT 40 — TEST H_T = H + eta*T*\n")
        f.write("=" * 100 + "\n\n")

        f.write(f"LIMIT = {LIMIT}\n")
        f.write(f"LOOKAHEAD = {LOOKAHEAD}\n")
        f.write(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}\n")
        f.write(f"ETA_VALUES = {ETA_VALUES}\n")
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

        for eta, st in stats_by_eta.items():
            avg_log = st.avg_log_step_sum / st.total if st.total else 0
            avg_ht = st.avg_ht_step_sum / st.total if st.total else 0

            f.write(
                f"{eta:>8.3f} "
                f"{st.total:>10} "
                f"{st.improved:>12} "
                f"{st.worsened:>12} "
                f"{st.same:>12} "
                f"{avg_log:>12.6f} "
                f"{avg_ht:>12.6f} "
                f"{st.max_log_step:>10} "
                f"{st.max_ht_step:>10} "
                f"{st.worst_loss:>12} "
                f"{st.worst_loss_n:>12} "
                f"{st.best_gain:>12} "
                f"{st.best_gain_n:>12}\n"
            )

        f.write("\nClassificazione peggioramenti per eta:\n")
        f.write("-" * 100 + "\n")
        f.write(
            f"{'ETA':>8} {'VERO_RIBELLE':>16} {'ESTREMO':>12} "
            f"{'INTERMEDIO':>14} {'FALSO_ALLARME':>16}\n"
        )

        for eta, st in stats_by_eta.items():
            f.write(
                f"{eta:>8.3f} "
                f"{st.true_rebel:>16} "
                f"{st.extreme_rebel:>12} "
                f"{st.intermediate:>14} "
                f"{st.false_alarm:>16}\n"
            )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    start_time = time.time()

    print("=" * 100)
    print("FASE 02 — SCRIPT 40 — TEST H_T = H + eta*T*")
    print("=" * 100)
    print(f"LIMIT = {LIMIT}")
    print(f"ETA_VALUES = {ETA_VALUES}")
    print()

    all_rows: List[Dict[str, object]] = []
    worsening_rows: List[Dict[str, object]] = []

    stats_by_eta: Dict[float, EtaStats] = {
        eta: EtaStats(eta=eta) for eta in ETA_VALUES
    }

    odds = range(3, LIMIT, 2)
    total_odds = (LIMIT - 1) // 2

    for idx, n in enumerate(odds, start=1):
        for eta in ETA_VALUES:
            row = analyze_number_for_eta(n, eta)

            if row is None:
                continue

            st = stats_by_eta[eta]
            st.total += 1

            log_step = int(row["log_step"])
            ht_step = int(row["ht_step"])
            delta = int(row["delta"])

            st.avg_log_step_sum += log_step
            st.avg_ht_step_sum += ht_step
            st.max_log_step = max(st.max_log_step, log_step)
            st.max_ht_step = max(st.max_ht_step, ht_step)

            if row["result"] == "IMPROVED":
                st.improved += 1

                gain = log_step - ht_step
                if gain > st.best_gain:
                    st.best_gain = gain
                    st.best_gain_n = n

            elif row["result"] == "WORSENED":
                st.worsened += 1

                worsening_rows.append(row)

                loss = ht_step - log_step
                if loss > st.worst_loss:
                    st.worst_loss = loss
                    st.worst_loss_n = n

                cls = row["classification"]

                if cls == "VERO_RIBELLE_ESTREMO":
                    st.extreme_rebel += 1
                elif cls == "VERO_RIBELLE":
                    st.true_rebel += 1
                elif cls == "INTERMEDIO":
                    st.intermediate += 1
                elif cls == "FALSO_ALLARME":
                    st.false_alarm += 1

            else:
                st.same += 1

            all_rows.append(row)

        if idx == 1 or idx % 100_000 == 0 or idx == total_odds:
            elapsed = time.time() - start_time
            print(f"{idx:>10}/{total_odds} | n={n:>10} | elapsed={elapsed:.1f}s")

    elapsed = time.time() - start_time

    write_csv(OUTPUT_RESULTS, all_rows)
    write_csv(OUTPUT_WORSENINGS, worsening_rows)
    write_summary(OUTPUT_SUMMARY, stats_by_eta, elapsed)

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"CSV risultati: {OUTPUT_RESULTS}")
    print(f"CSV peggioramenti: {OUTPUT_WORSENINGS}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print()
    print("Apri:")
    print(f"open '{OUTPUT_SUMMARY}'")


if __name__ == "__main__":
    main()
