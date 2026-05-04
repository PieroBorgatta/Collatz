#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASE 02 — Collatz/Syracuse
Analisi della Tensione Elastica T(n)

Questo script legge il CSV dei peggioramenti prodotto dalla validazione precedente
e calcola una nuova metrica:

    T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)

dove:

    D(k) = k*log2(3) - sum(a_i)
    ratio_1(k) = numero di a_i=1 nei primi k passi / k

Serve per misurare il "debito sotto vincolo espansivo",
cioè la tensione elastica del corridoio 2-adico.
"""

from __future__ import annotations

import csv
import math
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIG
# =============================================================================

LOOKAHEAD_TENSION = 80
FUTURE_STEPS_AFTER_TENSION = 400
MAX_FULL_STEPS = 2000

INPUT_CANDIDATES = [
    "../collatz_100M_validate_final_candidate.csv",
    "../collatz_37_validate_final_candidate.csv",
    "collatz_100M_validate_final_candidate.csv",
    "collatz_37_validate_final_candidate.csv",
]

OUTPUT_ALL = "collatz_38_tensione_elastica.csv"
OUTPUT_TOP_TSTAR = "collatz_38_top_tensione_star.csv"
OUTPUT_TOP_RECOVERY = "collatz_38_top_cascate_post_tensione.csv"
OUTPUT_SUMMARY = "collatz_38_summary_tensione_elastica.txt"

LOG2_3 = math.log2(3)


# =============================================================================
# COLLATZ / SYRACUSE
# =============================================================================

def v2(x: int) -> int:
    """
    Ritorna nu_2(x), cioè il massimo esponente e tale che 2^e divide x.
    """
    return (x & -x).bit_length() - 1


def syracuse_step_odd(n: int) -> Tuple[int, int]:
    """
    Mappa accelerata di Syracuse sui dispari:

        S(n) = (3n + 1) / 2^a

    Ritorna:
        nuovo dispari, a = v2(3n+1)
    """
    m = 3 * n + 1
    a = v2(m)
    return m >> a, a


def generate_orbit_data(n: int, max_steps: int) -> Tuple[List[int], List[int]]:
    """
    Genera orbita accelerata sui dispari.

    odd_values[0] = n
    a_values[i] = v2(3*odd_values[i]+1)
    odd_values[i+1] = S(odd_values[i])
    """
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
# METRICHE
# =============================================================================

@dataclass
class TensionMetrics:
    n: int

    steps_generated: int
    reached_1: bool
    total_steps_to_1: Optional[int]

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


def compute_tension_metrics(
    n: int,
    lookahead: int = LOOKAHEAD_TENSION,
    future_steps: int = FUTURE_STEPS_AFTER_TENSION,
    max_full_steps: int = MAX_FULL_STEPS,
) -> TensionMetrics:
    """
    Calcola le metriche di tensione elastica per un numero dispari n.
    """

    required_steps = max(lookahead + future_steps, max_full_steps)
    odd_values, a_values = generate_orbit_data(n, required_steps)

    steps_generated = len(a_values)
    reached_1 = odd_values[-1] == 1
    total_steps_to_1 = steps_generated if reached_1 else None

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

        # TENSIONE ELASTICA PRINCIPALE
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

    # Versione semplice / grezza
    t_simple = dmax80 * (1.0 + pmax80) * (1.0 + 0.1 * lmax1_80)

    # -------------------------------------------------------------------------
    # Cascata futura dopo il picco di tensione
    # -------------------------------------------------------------------------

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

        steps_generated=steps_generated,
        reached_1=reached_1,
        total_steps_to_1=total_steps_to_1,

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
    )


# =============================================================================
# CSV INPUT
# =============================================================================

def find_input_file() -> str:
    for path in INPUT_CANDIDATES:
        if os.path.exists(path):
            return path

    print("ERRORE: non trovo nessun CSV di input.")
    print("Ho cercato:")
    for path in INPUT_CANDIDATES:
        print(f"  - {path}")
    sys.exit(1)


def detect_delimiter(path: str) -> str:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        return dialect.delimiter
    except csv.Error:
        return ","


def clean_key(k: object) -> str:
    """
    Pulisce il nome colonna:
    - rimuove BOM UTF-8
    - rimuove spazi
    """
    return str(k).replace("\ufeff", "").strip()


def read_worsening_numbers(path: str) -> List[Dict[str, str]]:
    delimiter = detect_delimiter(path)

    # utf-8-sig elimina automaticamente il BOM se presente
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

    cleaned: List[Dict[str, str]] = []
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
        row["_n_int"] = str(n)
        row["_n_col"] = n_col

        cleaned.append(row)

    return cleaned


# =============================================================================
# OUTPUT
# =============================================================================

def get_n_for_display(row: Dict[str, object]) -> str:
    for key in ["n", "N", "start", "Start", "START", "number", "Number", "_n_int"]:
        if key in row and str(row[key]).strip():
            return str(row[key]).strip()
    return ""


def metrics_to_row(original_row: Dict[str, str], m: TensionMetrics) -> Dict[str, object]:
    row: Dict[str, object] = {}

    for k, v in original_row.items():
        if k in ["_n_int", "_n_col"]:
            continue
        row[k] = v

    # Se il CSV originale aveva start, manteniamo start.
    # Se non aveva n, aggiungiamo anche n per comodità.
    if "n" not in row:
        row["n"] = m.n

    row.update({
        "t_simple": f"{m.t_simple:.12f}",
        "t_star": f"{m.t_star:.12f}",
        "t_star_step": m.t_star_step,

        "lmax1_80": m.lmax1_80,
        "pmax80_recalc": f"{m.pmax80:.12f}",
        "dmax80_recalc": f"{m.dmax80:.12f}",
        "cmax80_recalc": f"{m.cmax80:.12f}",

        "debt_at_tension": f"{m.debt_at_tension:.12f}",
        "c_at_tension": f"{m.c_at_tension:.12f}",
        "ratio1_at_tension": f"{m.ratio1_at_tension:.12f}",
        "ones_at_tension": m.ones_at_tension,
        "sum_a_at_tension": m.sum_a_at_tension,

        "max_ratio_full_recalc": f"{m.max_ratio_full:.12f}",
        "max_value_full_recalc": m.max_value_full,
        "step_max_value_recalc": m.step_max_value,

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

        "steps_generated": m.steps_generated,
        "reached_1": int(m.reached_1),
        "total_steps_to_1": "" if m.total_steps_to_1 is None else m.total_steps_to_1,
    })

    return row


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


def write_summary(
    path: str,
    input_path: str,
    rows: List[Dict[str, object]],
    elapsed: float,
) -> None:
    total = len(rows)

    t_values = [safe_float(r, "t_star") for r in rows]
    recovery_values = [safe_float(r, "future_recovery_margin") for r in rows]
    cascade_values = [safe_float(r, "future_cascade_after_tension") for r in rows]

    positive_recovery = sum(1 for x in recovery_values if x > 0)
    positive_cascade_beats = sum(
        1 for r in rows
        if str(r.get("first_cascade_beats_debt_after_tension", "")).strip() != ""
    )
    below_start_after_tension = sum(
        1 for r in rows
        if str(r.get("first_below_start_after_tension", "")).strip() != ""
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write("FASE 02 — ANALISI TENSIONE ELASTICA\n")
        f.write("=" * 100 + "\n\n")

        f.write(f"Input: {input_path}\n")
        f.write(f"Output principale: {OUTPUT_ALL}\n")
        f.write(f"Output top T*: {OUTPUT_TOP_TSTAR}\n")
        f.write(f"Output top cascate: {OUTPUT_TOP_RECOVERY}\n\n")

        f.write(f"LOOKAHEAD_TENSION = {LOOKAHEAD_TENSION}\n")
        f.write(f"FUTURE_STEPS_AFTER_TENSION = {FUTURE_STEPS_AFTER_TENSION}\n")
        f.write(f"MAX_FULL_STEPS = {MAX_FULL_STEPS}\n")
        f.write(f"Tempo totale secondi = {elapsed:.2f}\n\n")

        f.write("Formula principale:\n")
        f.write("-" * 100 + "\n")
        f.write("T_star(n) = max_{1<=k<=80} max(D(k),0) * ratio_1(k) * log2(k+1)\n\n")
        f.write("D(k) = k*log2(3) - sum(a_i)\n")
        f.write("ratio_1(k) = #{a_i=1}/k\n\n")

        f.write("Statistiche globali:\n")
        f.write("-" * 100 + "\n")
        f.write(f"Numeri analizzati: {total}\n")

        if total:
            f.write(f"T_star media: {sum(t_values)/total:.12f}\n")
            f.write(f"T_star max:   {max(t_values):.12f}\n")
            f.write(f"T_star min:   {min(t_values):.12f}\n\n")

            f.write(f"Cascata futura media: {sum(cascade_values)/total:.12f}\n")
            f.write(f"Cascata futura max:   {max(cascade_values):.12f}\n\n")

            f.write(f"Recovery margin media: {sum(recovery_values)/total:.12f}\n")
            f.write(f"Recovery margin max:   {max(recovery_values):.12f}\n")
            f.write(f"Recovery margin min:   {min(recovery_values):.12f}\n\n")

            f.write(
                "Casi in cui la cascata futura supera il debito al picco T*: "
                f"{positive_recovery}/{total} ({positive_recovery/total:.8%})\n"
            )
            f.write(
                "Casi con primo step futuro in cui C_future > debt_T: "
                f"{positive_cascade_beats}/{total} ({positive_cascade_beats/total:.8%})\n"
            )
            f.write(
                "Casi con rientro sotto start dopo il picco T*: "
                f"{below_start_after_tension}/{total} ({below_start_after_tension/total:.8%})\n\n"
            )

        f.write("Top 30 per T_star:\n")
        f.write("-" * 100 + "\n")

        top_t = sorted(rows, key=lambda r: safe_float(r, "t_star"), reverse=True)[:30]

        for r in top_t:
            f.write(
                f"n={get_n_for_display(r):>10} | "
                f"T*={safe_float(r, 't_star'):>12.6f} | "
                f"step_T={r.get('t_star_step')} | "
                f"debt_T={safe_float(r, 'debt_at_tension'):>10.6f} | "
                f"ratio1_T={safe_float(r, 'ratio1_at_tension'):>8.6f} | "
                f"Lmax1={r.get('lmax1_80')} | "
                f"future_C={safe_float(r, 'future_cascade_after_tension'):>10.6f} | "
                f"recovery={safe_float(r, 'future_recovery_margin'):>10.6f}\n"
            )

        f.write("\nTop 30 per recovery margin:\n")
        f.write("-" * 100 + "\n")

        top_recovery = sorted(rows, key=lambda r: safe_float(r, "future_recovery_margin"), reverse=True)[:30]

        for r in top_recovery:
            f.write(
                f"n={get_n_for_display(r):>10} | "
                f"recovery={safe_float(r, 'future_recovery_margin'):>12.6f} | "
                f"future_C={safe_float(r, 'future_cascade_after_tension'):>10.6f} | "
                f"T*={safe_float(r, 't_star'):>10.6f} | "
                f"step_T={r.get('t_star_step')} | "
                f"first_C>D={r.get('first_cascade_beats_debt_after_tension')} | "
                f"first_below_start={r.get('first_below_start_after_tension')}\n"
            )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    start_time = time.time()

    input_path = find_input_file()

    print("=" * 100)
    print("FASE 02 — TENSIONE ELASTICA COLLATZ/SYRACUSE")
    print("=" * 100)
    print(f"Input: {input_path}")
    print(f"LOOKAHEAD_TENSION = {LOOKAHEAD_TENSION}")
    print(f"FUTURE_STEPS_AFTER_TENSION = {FUTURE_STEPS_AFTER_TENSION}")
    print(f"MAX_FULL_STEPS = {MAX_FULL_STEPS}")
    print()

    original_rows = read_worsening_numbers(input_path)
    total = len(original_rows)

    print(f"Numeri da analizzare: {total}")
    print()

    output_rows: List[Dict[str, object]] = []

    for idx, row in enumerate(original_rows, start=1):
        n = int(row["_n_int"])

        m = compute_tension_metrics(
            n=n,
            lookahead=LOOKAHEAD_TENSION,
            future_steps=FUTURE_STEPS_AFTER_TENSION,
            max_full_steps=MAX_FULL_STEPS,
        )

        out_row = metrics_to_row(row, m)
        output_rows.append(out_row)

        if idx == 1 or idx % 100 == 0 or idx == total:
            elapsed = time.time() - start_time
            print(
                f"{idx:>5}/{total} | "
                f"n={n:>10} | "
                f"T*={m.t_star:>10.6f} | "
                f"step_T={m.t_star_step:>3} | "
                f"debt_T={m.debt_at_tension:>9.5f} | "
                f"ratio1_T={m.ratio1_at_tension:>7.4f} | "
                f"future_C={m.future_cascade_after_tension:>9.5f} | "
                f"recovery={m.future_recovery_margin:>9.5f} | "
                f"elapsed={elapsed:.1f}s"
            )

    write_csv(OUTPUT_ALL, output_rows)

    top_tstar = sorted(output_rows, key=lambda r: safe_float(r, "t_star"), reverse=True)
    write_csv(OUTPUT_TOP_TSTAR, top_tstar)

    top_recovery = sorted(output_rows, key=lambda r: safe_float(r, "future_recovery_margin"), reverse=True)
    write_csv(OUTPUT_TOP_RECOVERY, top_recovery)

    elapsed = time.time() - start_time

    write_summary(
        path=OUTPUT_SUMMARY,
        input_path=input_path,
        rows=output_rows,
        elapsed=elapsed,
    )

    print()
    print("Completato.")
    print(f"Tempo totale: {elapsed:.2f} secondi")
    print(f"CSV principale: {OUTPUT_ALL}")
    print(f"CSV top T*: {OUTPUT_TOP_TSTAR}")
    print(f"CSV top cascate: {OUTPUT_TOP_RECOVERY}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_ALL}'")
    print(f"open '{OUTPUT_SUMMARY}'")


if __name__ == "__main__":
    main()
