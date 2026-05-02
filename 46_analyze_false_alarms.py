#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
46_analyze_false_alarms.py

Analisi dei FALSO_ALLARME della funzione base H nella validazione Collatz/Syracuse a 100M.

Input atteso:
    collatz_100M_validate_final_candidate.csv

Output:
    collatz_46_false_alarms_analysis.csv
    collatz_46_false_alarms_summary.txt

Nota metodologica:
    Questo script NON dimostra la Congettura di Collatz.
    Analizza empiricamente i peggioramenti della funzione base H già validati a 100M,
    con focus sui casi classificati come FALSO_ALLARME.

Funzione base:
    H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)

Qui testiamo se Pmax80 è troppo sensibile ai prefissi corti, ricalcolando:
    Pmax80^(m)(n) = max_{m <= k <= 80} #{i<=k : a_i=1}/k
per m = 4, 6, 8, 10, 12.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
from dataclasses import dataclass
from statistics import mean, median
from typing import Dict, Iterable, List, Tuple

import pandas as pd

LOG2_3 = math.log2(3.0)
LOOKAHEAD = 80
M_VALUES = (4, 6, 8, 10, 12)

DEFAULT_INPUT = "collatz_100M_validate_final_candidate.csv"
DEFAULT_OUTPUT_CSV = "collatz_46_false_alarms_analysis.csv"
DEFAULT_OUTPUT_SUMMARY = "collatz_46_false_alarms_summary.txt"

BASELINE_TEXT = """Baseline H 100M:
  LIMIT                 = 100000000
  dispari analizzati    = 49999999
  worsened              = 2839
  FALSO_ALLARME         = 167
  avg_H_step            = 3.131343
  max_H_step            = 190
"""


@dataclass
class PrefixStats:
    pmax: float
    pmax_k: int
    pmax_m: Dict[int, float]
    pmax_m_k: Dict[int, int]
    first_ones_run: int
    max_ones_run: int
    ones_first_4: int
    ones_first_6: int
    ones_first_8: int
    ones_first_10: int
    ones_first_12: int
    ratio_1_80: float
    avg_v2_80: float
    dmax80_recalc: float
    cmax80_recalc: float


def v2(x: int) -> int:
    """Restituisce la valutazione 2-adica v2(x), x > 0."""
    return (x & -x).bit_length() - 1


def syracuse_a_sequence_odd(n: int, lookahead: int = LOOKAHEAD) -> List[int]:
    """Calcola la sequenza a_i = v2(3n_i+1) per la mappa accelerata sui dispari."""
    if n <= 0 or n % 2 == 0:
        raise ValueError(f"n deve essere dispari positivo, ricevuto {n}")

    seq: List[int] = []
    x = n
    for _ in range(lookahead):
        y = 3 * x + 1
        a = v2(y)
        seq.append(a)
        x = y >> a
    return seq


def prefix_stats(a_seq: List[int]) -> PrefixStats:
    """Ricalcola Pmax80, Pmax80^(m), Dmax80, Cmax80 e diagnostiche sui prefissi."""
    ones = 0
    sum_a = 0

    pmax = -1.0
    pmax_k = 0
    pmax_m = {m: -1.0 for m in M_VALUES}
    pmax_m_k = {m: 0 for m in M_VALUES}

    dmax = 0.0
    cmax = 0.0

    for k, a in enumerate(a_seq, start=1):
        sum_a += a
        if a == 1:
            ones += 1

        p = ones / k
        if p > pmax:
            pmax = p
            pmax_k = k

        for m in M_VALUES:
            if k >= m and p > pmax_m[m]:
                pmax_m[m] = p
                pmax_m_k[m] = k

        debt = k * LOG2_3 - sum_a
        cascade = sum_a - k * LOG2_3
        if debt > dmax:
            dmax = debt
        if cascade > cmax:
            cmax = cascade

    # run iniziale di a_i = 1
    first_run = 0
    for a in a_seq:
        if a == 1:
            first_run += 1
        else:
            break

    # run massimo di a_i = 1 nei primi 80
    current = 0
    max_run = 0
    for a in a_seq:
        if a == 1:
            current += 1
            max_run = max(max_run, current)
        else:
            current = 0

    return PrefixStats(
        pmax=pmax,
        pmax_k=pmax_k,
        pmax_m=pmax_m,
        pmax_m_k=pmax_m_k,
        first_ones_run=first_run,
        max_ones_run=max_run,
        ones_first_4=sum(1 for a in a_seq[:4] if a == 1),
        ones_first_6=sum(1 for a in a_seq[:6] if a == 1),
        ones_first_8=sum(1 for a in a_seq[:8] if a == 1),
        ones_first_10=sum(1 for a in a_seq[:10] if a == 1),
        ones_first_12=sum(1 for a in a_seq[:12] if a == 1),
        ratio_1_80=sum(1 for a in a_seq[:LOOKAHEAD] if a == 1) / LOOKAHEAD,
        avg_v2_80=sum(a_seq[:LOOKAHEAD]) / LOOKAHEAD,
        dmax80_recalc=dmax,
        cmax80_recalc=cmax,
    )


def class_family(classification: str) -> str:
    if classification.startswith("FALSO_ALLARME"):
        return "FALSO_ALLARME"
    if classification.startswith("VERO_RIBELLE_ESTREMO"):
        return "VERO_RIBELLE_ESTREMO"
    if classification.startswith("VERO_RIBELLE"):
        return "VERO_RIBELLE"
    if classification.startswith("INTERMEDIO"):
        return "INTERMEDIO"
    return "ALTRO"


def numeric_summary(series: pd.Series) -> Dict[str, float]:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) == 0:
        return {"count": 0, "min": math.nan, "q25": math.nan, "median": math.nan, "mean": math.nan, "q75": math.nan, "max": math.nan}
    return {
        "count": int(len(s)),
        "min": float(s.min()),
        "q25": float(s.quantile(0.25)),
        "median": float(s.median()),
        "mean": float(s.mean()),
        "q75": float(s.quantile(0.75)),
        "max": float(s.max()),
    }


def fmt_summary(label: str, stats: Dict[str, float], digits: int = 6) -> str:
    if stats["count"] == 0:
        return f"{label}: nessun dato"
    return (
        f"{label}: count={stats['count']}, "
        f"min={stats['min']:.{digits}f}, "
        f"q25={stats['q25']:.{digits}f}, "
        f"median={stats['median']:.{digits}f}, "
        f"mean={stats['mean']:.{digits}f}, "
        f"q75={stats['q75']:.{digits}f}, "
        f"max={stats['max']:.{digits}f}"
    )


def add_recomputed_features(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total = len(df)
    for idx, row in df.iterrows():
        n = int(row["start"])
        a_seq = syracuse_a_sequence_odd(n, LOOKAHEAD)
        st = prefix_stats(a_seq)

        out = row.to_dict()
        out["class_family"] = class_family(str(row["classification"]))
        out["a_seq_80"] = " ".join(map(str, a_seq))

        out["pmax80_recalc"] = st.pmax
        out["pmax80_argmax_k"] = st.pmax_k
        out["pmax80_from_short_prefix_lt4"] = st.pmax_k < 4
        out["pmax80_from_short_prefix_lt6"] = st.pmax_k < 6
        out["pmax80_from_short_prefix_lt8"] = st.pmax_k < 8
        out["pmax80_from_short_prefix_lt10"] = st.pmax_k < 10
        out["pmax80_from_short_prefix_lt12"] = st.pmax_k < 12

        for m in M_VALUES:
            out[f"pmax80_m{m}"] = st.pmax_m[m]
            out[f"pmax80_m{m}_argmax_k"] = st.pmax_m_k[m]
            out[f"pmax80_drop_m{m}"] = st.pmax - st.pmax_m[m]

        out["first_ones_run"] = st.first_ones_run
        out["max_ones_run_80"] = st.max_ones_run
        out["ones_first_4"] = st.ones_first_4
        out["ones_first_6"] = st.ones_first_6
        out["ones_first_8"] = st.ones_first_8
        out["ones_first_10"] = st.ones_first_10
        out["ones_first_12"] = st.ones_first_12
        out["ratio_1_80_recalc"] = st.ratio_1_80
        out["avg_v2_80_recalc"] = st.avg_v2_80
        out["dmax80_recalc"] = st.dmax80_recalc
        out["cmax80_recalc"] = st.cmax80_recalc
        out["initial_pmax_diff_check"] = float(row.get("initial_pmax", math.nan)) - st.pmax
        out["initial_dmax_diff_check"] = float(row.get("initial_dmax", math.nan)) - st.dmax80_recalc
        out["initial_cmax_diff_check"] = float(row.get("initial_cmax", math.nan)) - st.cmax80_recalc

        rows.append(out)

    return pd.DataFrame(rows)


def threshold_table(enriched: pd.DataFrame, false_df: pd.DataFrame, true_df: pd.DataFrame) -> List[str]:
    """
    Tabella esplorativa: quanto taglierebbe una penalità robusta basata su pmax80_m?
    Non modifica H, non rivalida la formula; serve solo a vedere separazione empirica.
    """
    lines = []
    lines.append("Analisi esplorativa Pmax80 robusto")
    lines.append("-" * 100)
    lines.append("Nota: qui non si propone ancora una nuova H. Si misura solo la separazione tra falsi allarmi e veri ribelli.")
    lines.append("")

    for m in M_VALUES:
        col = f"pmax80_drop_m{m}"
        lines.append(f"Drop = Pmax80 - Pmax80^(m), m={m}")
        lines.append(fmt_summary("  FALSO_ALLARME", numeric_summary(false_df[col])))
        lines.append(fmt_summary("  VERO_RIBELLE + ESTREMO", numeric_summary(true_df[col])))

        # soglie candidate: quanto spesso i falsi hanno drop alto, e quanti veri ribelli verrebbero colpiti.
        for thr in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
            f_hit = int((false_df[col] >= thr).sum())
            t_hit = int((true_df[col] >= thr).sum())
            f_pct = f_hit / len(false_df) * 100 if len(false_df) else 0.0
            t_pct = t_hit / len(true_df) * 100 if len(true_df) else 0.0
            lines.append(
                f"    soglia drop>={thr:.2f}: falsi colpiti={f_hit:3d}/{len(false_df)} ({f_pct:6.2f}%), "
                f"veri ribelli colpiti={t_hit:4d}/{len(true_df)} ({t_pct:6.2f}%)"
            )
        lines.append("")
    return lines


def write_summary(enriched: pd.DataFrame, out_path: str) -> None:
    false_df = enriched[enriched["class_family"] == "FALSO_ALLARME"].copy()
    true_df = enriched[enriched["class_family"].isin(["VERO_RIBELLE", "VERO_RIBELLE_ESTREMO"])].copy()
    inter_df = enriched[enriched["class_family"] == "INTERMEDIO"].copy()

    lines: List[str] = []
    lines.append("ANALISI 46 - FALSI ALLARMI FUNZIONE BASE H A 100M")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Funzione analizzata:")
    lines.append("  H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)")
    lines.append("")
    lines.append(BASELINE_TEXT.rstrip())
    lines.append("")
    lines.append("Righe lette dal CSV dei peggioramenti:")
    lines.append(f"  totale peggioramenti = {len(enriched)}")
    lines.append(f"  FALSO_ALLARME       = {len(false_df)}")
    lines.append(f"  INTERMEDIO          = {len(inter_df)}")
    lines.append(f"  VERO_RIBELLE*       = {len(true_df)}")
    lines.append("")

    lines.append("Distribuzione famiglie di classificazione")
    lines.append("-" * 100)
    for name, count in enriched["class_family"].value_counts().items():
        lines.append(f"  {name:<24} {count}")
    lines.append("")

    lines.append("Domande principali sui FALSO_ALLARME")
    lines.append("-" * 100)
    qcols = [
        ("loss", "1. Loss"),
        ("max_ratio", "2. Max ratio"),
        ("initial_pmax", "3. Initial Pmax80"),
        ("pmax80_argmax_k", "3b. k del massimo Pmax80"),
        ("dmax_delta_at_log_step", "4. dmax_delta_at_log_step"),
        ("cmax_delta_at_log_step", "5. cmax_delta_at_log_step"),
        ("ratio_1_until_h", "6. ratio_1_until_h"),
        ("ratio_1_80_recalc", "6b. ratio_1 sui primi 80"),
        ("avg_v2_80_recalc", "avg v2 sui primi 80"),
    ]
    for col, label in qcols:
        lines.append(fmt_summary(f"{label} - FALSO_ALLARME", numeric_summary(false_df[col])))
        if col in true_df.columns:
            lines.append(fmt_summary(f"{label} - VERO_RIBELLE*", numeric_summary(true_df[col])))
        lines.append("")

    lines.append("Sensibilità di Pmax80 ai prefissi corti")
    lines.append("-" * 100)
    for k in (4, 6, 8, 10, 12):
        col = f"pmax80_from_short_prefix_lt{k}"
        f_count = int(false_df[col].sum())
        t_count = int(true_df[col].sum())
        lines.append(
            f"  argmax(Pmax80) < {k:2d}: "
            f"FALSO_ALLARME={f_count:3d}/{len(false_df)} ({f_count/len(false_df)*100:6.2f}%) | "
            f"VERO_RIBELLE*={t_count:4d}/{len(true_df)} ({t_count/len(true_df)*100:6.2f}%)"
        )
    lines.append("")

    for m in M_VALUES:
        lines.append(fmt_summary(f"Pmax80^(m={m}) - FALSO_ALLARME", numeric_summary(false_df[f"pmax80_m{m}"])))
        lines.append(fmt_summary(f"Pmax80^(m={m}) - VERO_RIBELLE*", numeric_summary(true_df[f"pmax80_m{m}"])))
        lines.append(fmt_summary(f"Drop Pmax80-Pmax80^(m={m}) - FALSO_ALLARME", numeric_summary(false_df[f"pmax80_drop_m{m}"])))
        lines.append(fmt_summary(f"Drop Pmax80-Pmax80^(m={m}) - VERO_RIBELLE*", numeric_summary(true_df[f"pmax80_drop_m{m}"])))
        lines.append("")

    lines.extend(threshold_table(enriched, false_df, true_df))

    lines.append("Top 40 FALSO_ALLARME per loss")
    lines.append("-" * 100)
    display_cols = [
        "start", "loss", "log_step", "h_step", "max_ratio", "ratio_1_until_h",
        "initial_pmax", "pmax80_argmax_k", "pmax80_m4", "pmax80_m6", "pmax80_m8", "pmax80_m10", "pmax80_m12",
        "dmax_delta_at_log_step", "cmax_delta_at_log_step", "h_delta_at_log_step",
    ]
    top_false = false_df.sort_values(["loss", "max_ratio"], ascending=[False, False]).head(40)
    for _, r in top_false.iterrows():
        lines.append(
            f"n={int(r['start']):10d} | loss={int(r['loss']):3d} | "
            f"log_step={int(r['log_step']):3d} | h_step={int(r['h_step']):3d} | "
            f"max_ratio={float(r['max_ratio']):10.3f} | ratio_1_h={float(r['ratio_1_until_h']):.6f} | "
            f"P={float(r['initial_pmax']):.6f}@k={int(r['pmax80_argmax_k'])} | "
            f"P4={float(r['pmax80_m4']):.6f} P6={float(r['pmax80_m6']):.6f} "
            f"P8={float(r['pmax80_m8']):.6f} P10={float(r['pmax80_m10']):.6f} P12={float(r['pmax80_m12']):.6f} | "
            f"dD={float(r['dmax_delta_at_log_step']):+.6f} | "
            f"dC={float(r['cmax_delta_at_log_step']):+.6f} | "
            f"dHlog={float(r['h_delta_at_log_step']):+.6f}"
        )
    lines.append("")

    lines.append("Controlli ricalcolo")
    lines.append("-" * 100)
    lines.append(fmt_summary("initial_pmax - pmax80_recalc", numeric_summary(enriched["initial_pmax_diff_check"]), digits=12))
    lines.append(fmt_summary("initial_dmax - dmax80_recalc", numeric_summary(enriched["initial_dmax_diff_check"]), digits=12))
    lines.append(fmt_summary("initial_cmax - cmax80_recalc", numeric_summary(enriched["initial_cmax_diff_check"]), digits=12))
    lines.append("")

    lines.append("Conclusione operativa")
    lines.append("-" * 100)
    lines.append("Questa analisi serve a decidere se testare una variante robusta della pressione Pmax80.")
    lines.append("Una nuova formula va eventualmente validata con uno script successivo, confrontando sempre:")
    lines.append("  avg_H_step, max_H_step, worsened, FALSO_ALLARME, VERO_RIBELLE, VERO_RIBELLE_ESTREMO")
    lines.append("contro la baseline H a 100M.")
    lines.append("Non c'è alcuna implicazione di prova formale della Congettura di Collatz.")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisi falsi allarmi H base 100M - Collatz/Syracuse")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="CSV dei peggioramenti base H a 100M")
    parser.add_argument("--out-csv", default=DEFAULT_OUTPUT_CSV, help="CSV di analisi in output")
    parser.add_argument("--out-summary", default=DEFAULT_OUTPUT_SUMMARY, help="Summary txt in output")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(
            f"Input non trovato: {args.input}\n"
            f"Metti lo script nella stessa cartella del file {DEFAULT_INPUT}, oppure usa --input /percorso/file.csv"
        )

    df = pd.read_csv(args.input, sep=";")
    required = {
        "start", "log_step", "h_step", "loss", "max_ratio", "ratio_1_until_h",
        "initial_dmax", "initial_cmax", "initial_pmax",
        "dmax_delta_at_log_step", "cmax_delta_at_log_step",
        "h_delta_at_log_step", "classification",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Colonne mancanti nel CSV: {missing}")

    enriched = add_recomputed_features(df)

    # Ordine comodo: falsi allarmi sopra, poi per loss decrescente.
    family_order = {
        "FALSO_ALLARME": 0,
        "INTERMEDIO": 1,
        "VERO_RIBELLE": 2,
        "VERO_RIBELLE_ESTREMO": 3,
        "ALTRO": 4,
    }
    enriched["_family_order"] = enriched["class_family"].map(family_order).fillna(9)
    enriched = enriched.sort_values(["_family_order", "loss", "max_ratio"], ascending=[True, False, False])
    enriched = enriched.drop(columns=["_family_order"])

    enriched.to_csv(args.out_csv, sep=";", index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    write_summary(enriched, args.out_summary)

    false_count = int((enriched["class_family"] == "FALSO_ALLARME").sum())
    print("Analisi 46 completata.")
    print(f"Input:        {args.input}")
    print(f"Righe input:  {len(df)}")
    print(f"Falsi allarmi:{false_count}")
    print(f"Output CSV:   {args.out_csv}")
    print(f"Output TXT:   {args.out_summary}")


if __name__ == "__main__":
    main()
