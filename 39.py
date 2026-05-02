#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASE 02 — Script 39
Confronto statistico della Tensione Elastica T*(n)

Obiettivo:
- confrontare T_star tra:
    1. WORSENED: numeri peggiorati dal test 100M
    2. IMPROVED: campione casuale dai numeri improved
    3. SAME: campione casuale dai numeri same
    4. RANDOM_ODD: dispari casuali fino al limite
- verificare se T_star discrimina davvero i ribelli dai numeri normali.

Formula:

    T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)

dove:

    D(k) = k*log2(3) - sum(a_i)
    ratio_1(k) = #{a_i=1}/k

Output:
- collatz_39_confronto_tensione.csv
- collatz_39_summary_confronto_tensione.txt
- collatz_39_top_tstar_global.csv
"""

from __future__ import annotations

import csv
import math
import os
import random
import statistics
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIG
# =============================================================================

LIMIT = 100_000_000

LOOKAHEAD_TENSION = 80
FUTURE_STEPS_AFTER_TENSION = 400
MAX_FULL_STEPS = 2000

# Per non esagerare: prendiamo tanti IMPROVED e SAME quanti sono i peggioramenti.
# Se vuoi aumentare, metti 10000 o 20000.
SAMPLE_PER_GROUP = 2839

RANDOM_ODD_SAMPLE = 2839

RANDOM_SEED = 424242

INPUT_WORSENED_CANDIDATES = [
    "../collatz_100M_validate_final_candidate.csv",
    "collatz_100M_validate_final_candidate.csv",
    "../VALIDAZIONI/collatz_100M_validate_final_candidate.csv",
    "../collatz_37_validate_final_candidate.csv",
]

OUTPUT_ALL = "collatz_39_confronto_tensione.csv"
OUTPUT_TOP_GLOBAL = "collatz_39_top_tstar_global.csv"
OUTPUT_SUMMARY = "collatz_39_summary_confronto_tensione.txt"

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


def generate_orbit_data(n: int, max_steps: int) -> Tuple[List[int], List[int]]:
    odd_values = [n]
    a_values: List[int] = []

    current = n

    for _ in range(max_steps):
        if current == 1:
            break

        nxt, a = syracuse_step_odd(current)
        a_values.append(a)
        odd_values.append(nxt)
        current = nxt

    return odd_values, a_values


# =============================================================================
# H CANDIDATA ORIGINALE
# =============================================================================

def compute_window_metrics(n: int, lookahead: int = LOOKAHEAD_TENSION) -> Tuple[float, float, float, float]:
    """
    Calcola:
    - Dmax80
    - Cmax80
    - Pmax80
    - Pavg80

    Usata per ricostruire H(n).
    """

    _, a_values = generate_orbit_data(n, lookahead)

    if not a_values:
        return 0.0, 0.0, 0.0, 0.0

    dmax = float("-inf")
    cmax = float("-inf")
    pmax = 0.0

    ones_count = 0
    sum_a = 0

    for k, a in enumerate(a_values, start=1):
        sum_a += a

        if a == 1:
            ones_count += 1

        debt = k * LOG2_3 - sum_a
        cascade = sum_a - k * LOG2_3
        ratio1 = ones_count / k

        dmax = max(dmax, debt)
        cmax = max(cmax, cascade)
        pmax = max(pmax, ratio1)

    pavg = ones_count / len(a_values)

    return dmax, cmax, pmax, pavg


def H_value(n: int) -> float:
    """
    H(n) = log(n) + 0.28*Dmax80 - 0.03*Cmax80 + 0.30*Pmax80
    """
    dmax, cmax, pmax, _ = compute_window_metrics(n)
    return math.log(n) + 0.28 * dmax - 0.03 * cmax + 0.30 * pmax


def first_log_below_start(n: int, max_steps: int = 400) -> Optional[int]:
    """
    Primo step Syracuse in cui S^k(n) < n.
    """
    current = n

    for k in range(1, max_steps + 1):
        current, _ = syracuse_step_odd(current)

        if current < n:
            return k

        if current == 1:
            return k

    return None


def classify_by_H(n: int, max_steps: int = 400) -> str:
    """
    Ricostruisce grossolanamente la classe rispetto alla vecchia H:
    - IMPROVED se H scende prima del log
    - WORSENED se H scende dopo il log
    - SAME se uguale o se non si trova entro max_steps

    Nota: per i WORSENED veri usiamo comunque il CSV.
    Questa funzione serve per campionare improved/same senza avere il CSV completo da 50M.
    """
    h0 = H_value(n)

    log_step = first_log_below_start(n, max_steps=max_steps)
    if log_step is None:
        return "UNKNOWN"

    current = n
    h_step = None

    for k in range(1, max_steps + 1):
        current, _ = syracuse_step_odd(current)

        if H_value(current) < h0:
            h_step = k
            break

        if current == 1:
            h_step = k
            break

    if h_step is None:
        return "UNKNOWN"

    if h_step < log_step:
        return "IMPROVED"
    elif h_step > log_step:
        return "WORSENED_REFOUND"
    else:
        return "SAME"


# =============================================================================
# TENSIONE ELASTICA
# =============================================================================

@dataclass
class TensionMetrics:
    n: int
    group: str

    t_simple: float
    t_star: float
    t_star_step: int

    lmax1_80: int
    pmax80: float
    dmax80: float
    cmax80: float

    debt_at_tension: float
    c_at_tension: float
    ratio1_at_tension: float
    ones_at_tension: int
    sum_a_at_tension: int

    max_ratio_full: float
    max_value_full: int
    step_max_value: int

    future_cascade_after_tension: float
    future_cascade_step_after_tension: int
    future_recovery_margin: float
    future_recovery_step_after_tension: int

    first_cascade_beats_debt_after_tension: Optional[int]
    first_below_start_after_tension: Optional[int]

    reached_1: bool
    total_steps_to_1: Optional[int]


def compute_tension_metrics(
    n: int,
    group: str,
    lookahead: int = LOOKAHEAD_TENSION,
    future_steps: int = FUTURE_STEPS_AFTER_TENSION,
    max_full_steps: int = MAX_FULL_STEPS,
) -> TensionMetrics:

    required_steps = max(lookahead + future_steps, max_full_steps)
    odd_values, a_values = generate_orbit_data(n, required_steps)

    reached_1 = odd_values[-1] == 1
    total_steps_to_1 = len(a_values) if reached_1 else None

    max_value_full = max(odd_values)
    step_max_value = odd_values.index(max_value_full)
    max_ratio_full = max_value_full / n

    kmax = min(lookahead, len(a_values))

    dmax80 = float("-inf")
    cmax80 = float("-inf")
    pmax80 = 0.0

    lmax1_80 = 0
    current_run_1 = 0

    best_t_star = float("-inf")
    best_t_star_step = 0
    best_debt_at_tension = 0.0
    best_c_at_tension = 0.0
    best_ratio1_at_tension = 0.0
    best_ones_at_tension = 0
    best_sum_a_at_tension = 0

    ones_count = 0
    sum_a = 0

    for k in range(1, kmax + 1):
        a = a_values[k - 1]
        sum_a += a

        if a == 1:
            ones_count += 1
            current_run_1 += 1
            lmax1_80 = max(lmax1_80, current_run_1)
        else:
            current_run_1 = 0

        debt = k * LOG2_3 - sum_a
        cascade = sum_a - k * LOG2_3
        ratio1 = ones_count / k

        dmax80 = max(dmax80, debt)
        cmax80 = max(cmax80, cascade)
        pmax80 = max(pmax80, ratio1)

        positive_debt = max(debt, 0.0)
        t_star_k = positive_debt * ratio1 * math.log2(k + 1)

        if t_star_k > best_t_star:
            best_t_star = t_star_k
            best_t_star_step = k
            best_debt_at_tension = debt
            best_c_at_tension = cascade
            best_ratio1_at_tension = ratio1
            best_ones_at_tension = ones_count
            best_sum_a_at_tension = sum_a

    if kmax == 0:
        dmax80 = 0.0
        cmax80 = 0.0
        pmax80 = 0.0
        best_t_star = 0.0
        best_t_star_step = 0

    t_simple = dmax80 * (1.0 + pmax80) * (1.0 + 0.1 * lmax1_80)

    future_cascade_after_tension = 0.0
    future_cascade_step_after_tension = 0

    future_recovery_margin = float("-inf")
    future_recovery_step_after_tension = 0

    first_cascade_beats_debt_after_tension: Optional[int] = None
    first_below_start_after_tension: Optional[int] = None

    if best_t_star_step > 0 and best_t_star_step < len(a_values):
        start = best_t_star_step
        end = min(len(a_values), best_t_star_step + future_steps)

        future_sum_a = 0

        for j in range(start + 1, end + 1):
            a = a_values[j - 1]
            future_sum_a += a

            local_len = j - start
            local_cascade = future_sum_a - local_len * LOG2_3

            if local_cascade > future_cascade_after_tension:
                future_cascade_after_tension = local_cascade
                future_cascade_step_after_tension = local_len

            recovery_margin = local_cascade - max(best_debt_at_tension, 0.0)

            if recovery_margin > future_recovery_margin:
                future_recovery_margin = recovery_margin
                future_recovery_step_after_tension = local_len

            if (
                first_cascade_beats_debt_after_tension is None
                and local_cascade > max(best_debt_at_tension, 0.0)
            ):
                first_cascade_beats_debt_after_tension = local_len

            if (
                first_below_start_after_tension is None
                and j < len(odd_values)
                and odd_values[j] < n
            ):
                first_below_start_after_tension = local_len

    if future_recovery_margin == float("-inf"):
        future_recovery_margin = 0.0

    return TensionMetrics(
        n=n,
        group=group,

        t_simple=t_simple,
        t_star=best_t_star,
        t_star_step=best_t_star_step,

        lmax1_80=lmax1_80,
        pmax80=pmax80,
        dmax80=dmax80,
        cmax80=cmax80,

        debt_at_tension=best_debt_at_tension,
        c_at_tension=best_c_at_tension,
        ratio1_at_tension=best_ratio1_at_tension,
        ones_at_tension=best_ones_at_tension,
        sum_a_at_tension=best_sum_a_at_tension,

        max_ratio_full=max_ratio_full,
        max_value_full=max_value_full,
        step_max_value=step_max_value,

        future_cascade_after_tension=future_cascade_after_tension,
        future_cascade_step_after_tension=future_cascade_step_after_tension,
        future_recovery_margin=future_recovery_margin,
        future_recovery_step_after_tension=future_recovery_step_after_tension,

        first_cascade_beats_debt_after_tension=first_cascade_beats_debt_after_tension,
        first_below_start_after_tension=first_below_start_after_tension,

        reached_1=reached_1,
        total_steps_to_1=total_steps_to_1,
    )


# =============================================================================
# CSV INPUT
# =============================================================================

def detect_delimiter(path: str) -> str:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        return dialect.delimiter
    except csv.Error:
        return ","


def clean_key(k: object) -> str:
    return str(k).replace("\ufeff", "").strip()


def find_worsened_file() -> str:
    for path in INPUT_WORSENED_CANDIDATES:
        if os.path.exists(path):
            return path

    print("ERRORE: non trovo il CSV dei peggioramenti.")
    print("Ho cercato:")
    for p in INPUT_WORSENED_CANDIDATES:
        print(f"  - {p}")
    sys.exit(1)


def read_worsened_numbers(path: str) -> List[int]:
    delimiter = detect_delimiter(path)

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        raw_rows = list(reader)

    if not raw_rows:
        print(f"ERRORE: CSV vuoto: {path}")
        sys.exit(1)

    rows: List[Dict[str, str]] = []

    for raw_row in raw_rows:
        row: Dict[str, str] = {}
        for k, v in raw_row.items():
            row[clean_key(k)] = "" if v is None else str(v).strip()
        rows.append(row)

    fieldnames = list(rows[0].keys())

    possible_n_cols = [
        "n",
        "N",
        "start",
        "Start",
        "START",
        "number",
        "Number",
        "numero",
        "Numero",
    ]

    n_col = None

    for col in possible_n_cols:
        if col in fieldnames:
            n_col = col
            break

    if n_col is None:
        print("ERRORE: non trovo la colonna n/start nel CSV.")
        print("Colonne trovate:")
        for c in fieldnames:
            print(f"  - {repr(c)}")
        sys.exit(1)

    numbers: List[int] = []
    seen = set()

    for row in rows:
        raw = str(row[n_col]).replace("\ufeff", "").strip()

        if not raw:
            continue

        try:
            n = int(raw)
        except ValueError:
            continue

        if n % 2 == 0:
            continue

        if n in seen:
            continue

        seen.add(n)
        numbers.append(n)

    return numbers


# =============================================================================
# CAMPIONAMENTO
# =============================================================================

def random_odd_under_limit(limit: int) -> int:
    x = random.randrange(1, limit, 2)
    return x


def build_comparison_samples(worsened_numbers: List[int]) -> Dict[str, List[int]]:
    random.seed(RANDOM_SEED)

    worsened_set = set(worsened_numbers)

    samples: Dict[str, List[int]] = {
        "WORSENED": list(worsened_numbers),
        "IMPROVED": [],
        "SAME": [],
        "RANDOM_ODD": [],
    }

    # RANDOM_ODD semplice
    random_seen = set()

    while len(samples["RANDOM_ODD"]) < RANDOM_ODD_SAMPLE:
        n = random_odd_under_limit(LIMIT)

        if n in random_seen:
            continue

        random_seen.add(n)
        samples["RANDOM_ODD"].append(n)

    print()
    print("Campionamento IMPROVED/SAME tramite riclassificazione H.")
    print("Questo può richiedere un po', ma il campione è piccolo.")
    print()

    attempts = 0
    seen = set(worsened_numbers)

    while (
        len(samples["IMPROVED"]) < SAMPLE_PER_GROUP
        or len(samples["SAME"]) < SAMPLE_PER_GROUP
    ):
        attempts += 1

        n = random_odd_under_limit(LIMIT)

        if n in seen:
            continue

        seen.add(n)

        cls = classify_by_H(n)

        if cls == "IMPROVED" and len(samples["IMPROVED"]) < SAMPLE_PER_GROUP:
            samples["IMPROVED"].append(n)

        elif cls == "SAME" and len(samples["SAME"]) < SAMPLE_PER_GROUP:
            samples["SAME"].append(n)

        if attempts % 1000 == 0:
            print(
                f"attempts={attempts} | "
                f"IMPROVED={len(samples['IMPROVED'])}/{SAMPLE_PER_GROUP} | "
                f"SAME={len(samples['SAME'])}/{SAMPLE_PER_GROUP}"
            )

        # Paracadute, nel caso la riclassificazione sia troppo lenta.
        if attempts > 2_000_000:
            print("ATTENZIONE: troppi tentativi. Mi fermo con i campioni disponibili.")
            break

    return samples


# =============================================================================
# OUTPUT
# =============================================================================

def metric_to_row(m: TensionMetrics) -> Dict[str, object]:
    return {
        "group": m.group,
        "n": m.n,

        "t_simple": f"{m.t_simple:.12f}",
        "t_star": f"{m.t_star:.12f}",
        "t_star_step": m.t_star_step,

        "lmax1_80": m.lmax1_80,
        "pmax80": f"{m.pmax80:.12f}",
        "dmax80": f"{m.dmax80:.12f}",
        "cmax80": f"{m.cmax80:.12f}",

        "debt_at_tension": f"{m.debt_at_tension:.12f}",
        "c_at_tension": f"{m.c_at_tension:.12f}",
        "ratio1_at_tension": f"{m.ratio1_at_tension:.12f}",
        "ones_at_tension": m.ones_at_tension,
        "sum_a_at_tension": m.sum_a_at_tension,

        "max_ratio_full": f"{m.max_ratio_full:.12f}",
        "max_value_full": m.max_value_full,
        "step_max_value": m.step_max_value,

        "future_cascade_after_tension": f"{m.future_cascade_after_tension:.12f}",
        "future_cascade_step_after_tension": m.future_cascade_step_after_tension,
        "future_recovery_margin": f"{m.future_recovery_margin:.12f}",
        "future_recovery_step_after_tension": m.future_recovery_step_after_tension,

        "first_cascade_beats_debt_after_tension": (
            "" if m.first_cascade_beats_debt_after_tension is None
            else m.first_cascade_beats_debt_after_tension
        ),
        "first_below_start_after_tension": (
            "" if m.first_below_start_after_tension is None
            else m.first_below_start_after_tension
        ),

        "reached_1": int(m.reached_1),
        "total_steps_to_1": "" if m.total_steps_to_1 is None else m.total_steps_to_1,
    }


def write_csv(path: str, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_float(row: Dict[str, object], key: str) -> float:
    try:
        return float(row.get(key, 0) or 0)
    except Exception:
        return 0.0


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0

    values_sorted = sorted(values)

    if len(values_sorted) == 1:
        return values_sorted[0]

    pos = (len(values_sorted) - 1) * p
    lower = math.floor(pos)
    upper = math.ceil(pos)

    if lower == upper:
        return values_sorted[int(pos)]

    weight = pos - lower
    return values_sorted[lower] * (1 - weight) + values_sorted[upper] * weight


def group_stats(rows: List[Dict[str, object]], group: str) -> Dict[str, float]:
    vals = [safe_float(r, "t_star") for r in rows if r["group"] == group]

    if not vals:
        return {
            "count": 0,
            "mean": 0,
            "median": 0,
            "min": 0,
            "max": 0,
            "p75": 0,
            "p90": 0,
            "p95": 0,
            "p99": 0,
        }

    return {
        "count": len(vals),
        "mean": sum(vals) / len(vals),
        "median": statistics.median(vals),
        "min": min(vals),
        "max": max(vals),
        "p75": percentile(vals, 0.75),
        "p90": percentile(vals, 0.90),
        "p95": percentile(vals, 0.95),
        "p99": percentile(vals, 0.99),
    }


def write_summary(path: str, rows: List[Dict[str, object]], elapsed: float, input_path: str) -> None:
    groups = ["WORSENED", "IMPROVED", "SAME", "RANDOM_ODD"]

    with open(path, "w", encoding="utf-8") as f:
        f.write("FASE 02 — SCRIPT 39 — CONFRONTO TENSIONE ELASTICA\n")
        f.write("=" * 100 + "\n\n")

        f.write(f"Input WORSENED: {input_path}\n")
        f.write(f"LIMIT = {LIMIT}\n")
        f.write(f"LOOKAHEAD_TENSION = {LOOKAHEAD_TENSION}\n")
        f.write(f"FUTURE_STEPS_AFTER_TENSION = {FUTURE_STEPS_AFTER_TENSION}\n")
        f.write(f"MAX_FULL_STEPS = {MAX_FULL_STEPS}\n")
        f.write(f"SAMPLE_PER_GROUP = {SAMPLE_PER_GROUP}\n")
        f.write(f"RANDOM_ODD_SAMPLE = {RANDOM_ODD_SAMPLE}\n")
        f.write(f"RANDOM_SEED = {RANDOM_SEED}\n")
        f.write(f"Tempo totale secondi = {elapsed:.2f}\n\n")

        f.write("Formula:\n")
        f.write("-" * 100 + "\n")
        f.write("T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)\n\n")

        f.write("Statistiche T_star per gruppo:\n")
        f.write("-" * 100 + "\n")
        f.write(
            f"{'GROUP':<12} {'COUNT':>8} {'MEAN':>14} {'MEDIAN':>14} "
            f"{'MIN':>14} {'MAX':>14} {'P75':>14} {'P90':>14} {'P95':>14} {'P99':>14}\n"
        )

        stats_by_group = {}

        for g in groups:
            st = group_stats(rows, g)
            stats_by_group[g] = st

            f.write(
                f"{g:<12} "
                f"{int(st['count']):>8} "
                f"{st['mean']:>14.6f} "
                f"{st['median']:>14.6f} "
                f"{st['min']:>14.6f} "
                f"{st['max']:>14.6f} "
                f"{st['p75']:>14.6f} "
                f"{st['p90']:>14.6f} "
                f"{st['p95']:>14.6f} "
                f"{st['p99']:>14.6f}\n"
            )

        f.write("\nRapporti principali:\n")
        f.write("-" * 100 + "\n")

        w = stats_by_group["WORSENED"]

        for g in ["IMPROVED", "SAME", "RANDOM_ODD"]:
            st = stats_by_group[g]

            if st["mean"] > 0:
                f.write(f"Mean WORSENED / {g}: {w['mean'] / st['mean']:.6f}\n")
            else:
                f.write(f"Mean WORSENED / {g}: n/a\n")

            if st["median"] > 0:
                f.write(f"Median WORSENED / {g}: {w['median'] / st['median']:.6f}\n")
            else:
                f.write(f"Median WORSENED / {g}: n/a\n")

        f.write("\nSoglie discriminanti semplici:\n")
        f.write("-" * 100 + "\n")

        thresholds = [5, 10, 15, 20, 25, 30, 40, 50, 60]

        for th in thresholds:
            f.write(f"\nT_star >= {th}\n")

            for g in groups:
                group_rows = [r for r in rows if r["group"] == g]
                count = len(group_rows)
                hit = sum(1 for r in group_rows if safe_float(r, "t_star") >= th)
                perc = hit / count if count else 0

                f.write(f"  {g:<12}: {hit:>6}/{count:<6} {perc:>10.4%}\n")

        f.write("\nTop 50 globale per T_star:\n")
        f.write("-" * 100 + "\n")

        top = sorted(rows, key=lambda r: safe_float(r, "t_star"), reverse=True)[:50]

        for r in top:
            f.write(
                f"group={str(r['group']):<10} | "
                f"n={int(r['n']):>10} | "
                f"T*={safe_float(r, 't_star'):>12.6f} | "
                f"debt_T={safe_float(r, 'debt_at_tension'):>10.6f} | "
                f"ratio1_T={safe_float(r, 'ratio1_at_tension'):>8.6f} | "
                f"Lmax1={r['lmax1_80']} | "
                f"future_C={safe_float(r, 'future_cascade_after_tension'):>10.6f} | "
                f"recovery={safe_float(r, 'future_recovery_margin'):>10.6f}\n"
            )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    start_time = time.time()

    print("=" * 100)
    print("FASE 02 — SCRIPT 39 — CONFRONTO TENSIONE ELASTICA")
    print("=" * 100)

    input_path = find_worsened_file()
    worsened_numbers = read_worsened_numbers(input_path)

    print(f"Input WORSENED: {input_path}")
    print(f"WORSENED letti: {len(worsened_numbers)}")
    print()

    samples = build_comparison_samples(worsened_numbers)

    print()
    print("Campioni finali:")
    for group_name, nums in samples.items():
        print(f"  {group_name:<12}: {len(nums)}")
    print()

    output_rows: List[Dict[str, object]] = []

    total_to_process = sum(len(v) for v in samples.values())
    done = 0

    for group_name, nums in samples.items():
        print(f"Analizzo gruppo {group_name}...")

        for n in nums:
            done += 1

            m = compute_tension_metrics(n=n, group=group_name)
            output_rows.append(metric_to_row(m))

            if done == 1 or done % 500 == 0 or done == total_to_process:
                elapsed = time.time() - start_time
                print(
                    f"{done:>6}/{total_to_process} | "
                    f"group={group_name:<10} | "
                    f"n={n:>10} | "
                    f"T*={m.t_star:>10.6f} | "
                    f"debt_T={m.debt_at_tension:>9.5f} | "
                    f"ratio1_T={m.ratio1_at_tension:>7.4f} | "
                    f"elapsed={elapsed:.1f}s"
                )

    write_csv(OUTPUT_ALL, output_rows)

    top_global = sorted(output_rows, key=lambda r: safe_float(r, "t_star"), reverse=True)
    write_csv(OUTPUT_TOP_GLOBAL, top_global)

    elapsed = time.time() - start_time
    write_summary(OUTPUT_SUMMARY, output_rows, elapsed, input_path)

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"CSV principale: {OUTPUT_ALL}")
    print(f"CSV top globale T*: {OUTPUT_TOP_GLOBAL}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print()
    print("Per aprire:")
    print(f"open '{OUTPUT_SUMMARY}'")
    print(f"open '{OUTPUT_ALL}'")
    print(f"open '{OUTPUT_TOP_GLOBAL}'")


if __name__ == "__main__":
    main()
