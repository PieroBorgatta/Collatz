#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
48_false_alarm_rules_fast.py

Versione veloce e verbosa dello script 48.

Analizza soglie descrittive ex-post sui peggioramenti della baseline H a 100M.

Input:
    ../collatz_100M_validate_final_candidate.csv

Output:
    collatz_48_false_alarm_rules.csv
    collatz_48_false_alarm_rules_summary.txt

Nota:
    Le regole usano loss, max_ratio, ratio_1_until_h e h_delta_at_log_step.
    Sono quindi descrittive/ex-post, NON una nuova formula H(n).
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


BASELINE = {
    "limit": 100_000_000,
    "odd_analyzed": 49_999_999,
    "avg_H_step": 3.131343,
    "max_H_step": 190,
    "worsened": 2839,
    "false_alarms": 167,
    "intermedio": 207,
    "true_rebels": 2066,
    "true_rebels_extreme": 399,
}


def family(classification: str) -> str:
    s = str(classification)

    if s.startswith("FALSO_ALLARME"):
        return "FALSO_ALLARME"

    if s.startswith("INTERMEDIO"):
        return "INTERMEDIO"

    if s.startswith("VERO_RIBELLE_ESTREMO"):
        return "VERO_RIBELLE_ESTREMO"

    if s.startswith("VERO_RIBELLE"):
        return "VERO_RIBELLE"

    return "ALTRO"


def is_true_rebel_family(fam: str) -> bool:
    return fam in {"VERO_RIBELLE", "VERO_RIBELLE_ESTREMO"}


def load_input(path: Path) -> pd.DataFrame:
    print(f"[1/6] Leggo input: {path}")

    try:
        df = pd.read_csv(path, sep=";")
        if len(df.columns) <= 1:
            df = pd.read_csv(path)
    except Exception:
        df = pd.read_csv(path)

    required = [
        "start",
        "log_step",
        "h_step",
        "loss",
        "max_ratio",
        "ratio_1_until_h",
        "dmax_delta_at_log_step",
        "cmax_delta_at_log_step",
        "pmax_at_log_step",
        "pmax_delta_at_log_step",
        "h_delta_at_log_step",
        "classification",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "CSV input non compatibile. Colonne mancanti: "
            + ", ".join(missing)
        )

    print(f"      Righe lette: {len(df)}")
    print(f"      Colonne: {len(df.columns)}")
    return df


def summarize_numeric(series: pd.Series) -> str:
    s = pd.to_numeric(series, errors="coerce").dropna()

    if len(s) == 0:
        return "count=0"

    return (
        f"count={len(s)}, "
        f"min={s.min():.6f}, "
        f"q25={s.quantile(0.25):.6f}, "
        f"median={s.median():.6f}, "
        f"mean={s.mean():.6f}, "
        f"q75={s.quantile(0.75):.6f}, "
        f"max={s.max():.6f}"
    )


def safe_pct(a: int, b: int) -> float:
    if b == 0:
        return 0.0
    return a / b


def progress(done: int, total: int, start_time: float, prefix: str = "") -> None:
    pct = done / total if total else 1.0
    bar_len = 32
    filled = int(bar_len * pct)
    bar = "█" * filled + "░" * (bar_len - filled)

    elapsed = time.time() - start_time
    rate = done / elapsed if elapsed > 0 else 0.0
    remaining = (total - done) / rate if rate > 0 else 0.0

    msg = (
        f"\r{prefix}[{bar}] "
        f"{done:>7}/{total:<7} "
        f"{pct:6.2%} | "
        f"elapsed {elapsed:6.1f}s | "
        f"eta {remaining:6.1f}s"
    )

    print(msg, end="", flush=True)

    if done >= total:
        print("")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analisi veloce soglie falsi allarmi vs ribelli - Collatz Fase 03"
    )

    parser.add_argument(
        "--input",
        default="../collatz_100M_validate_final_candidate.csv",
        help="CSV peggioramenti baseline H a 100M",
    )

    parser.add_argument(
        "--out-csv",
        default="collatz_48_false_alarm_rules.csv",
        help="CSV output regole",
    )

    parser.add_argument(
        "--out-summary",
        default="collatz_48_false_alarm_rules_summary.txt",
        help="TXT summary output",
    )

    parser.add_argument(
        "--progress-every",
        type=int,
        default=1000,
        help="Aggiorna avanzamento ogni N regole valutate",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    out_csv_path = Path(args.out_csv)
    out_summary_path = Path(args.out_summary)

    t0 = time.time()

    df = load_input(input_path)

    print("[2/6] Normalizzo colonne e classificazioni...")

    df["family"] = df["classification"].apply(family)

    numeric_cols = [
        "loss",
        "max_ratio",
        "ratio_1_until_h",
        "dmax_delta_at_log_step",
        "cmax_delta_at_log_step",
        "pmax_at_log_step",
        "pmax_delta_at_log_step",
        "h_delta_at_log_step",
        "log_step",
        "h_step",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    fam = df["family"].to_numpy()

    false_mask = fam == "FALSO_ALLARME"
    inter_mask = fam == "INTERMEDIO"
    true_mask = np.array([is_true_rebel_family(x) for x in fam], dtype=bool)
    extreme_mask = fam == "VERO_RIBELLE_ESTREMO"

    false_total = int(false_mask.sum())
    inter_total = int(inter_mask.sum())
    true_total = int(true_mask.sum())
    extreme_total = int(extreme_mask.sum())
    total_rows = len(df)

    print(f"      Totale peggioramenti: {total_rows}")
    print(f"      FALSO_ALLARME:        {false_total}")
    print(f"      INTERMEDIO:           {inter_total}")
    print(f"      VERO_RIBELLE*:        {true_total}")
    print(f"      ESTREMI:              {extreme_total}")

    print("[3/6] Converto in array NumPy...")

    loss = df["loss"].to_numpy(dtype=float)
    max_ratio = df["max_ratio"].to_numpy(dtype=float)
    ratio_1_until_h = df["ratio_1_until_h"].to_numpy(dtype=float)
    h_delta = df["h_delta_at_log_step"].to_numpy(dtype=float)
    dmax_delta = df["dmax_delta_at_log_step"].to_numpy(dtype=float)
    cmax_delta = df["cmax_delta_at_log_step"].to_numpy(dtype=float)

    print("[4/6] Preparo griglia soglie...")

    loss_thresholds = [1, 2, 3, 4, 5, 7, 10]
    max_ratio_thresholds = [1.0, 1.25, 1.5, 2.0, 2.53125, 3.0, 5.0, 10.0]
    ratio1_thresholds = [0.0, 0.10, 0.20, 0.25, 0.333333, 0.40, 0.45, 0.50, 0.55]
    hdelta_thresholds = [
        0.005,
        0.010,
        0.015,
        0.020,
        0.025,
        0.030,
        0.050,
        0.075,
        0.100,
        0.150,
        0.200,
    ]

    dmax_thresholds = [0.75, 1.0, 1.25, 1.5, 2.0, 3.0]
    cmax_thresholds = [-1.0, -0.75, -0.5, -0.415037, -0.25, -0.10, 0.0]

    main_total = (
        len(loss_thresholds)
        * len(max_ratio_thresholds)
        * len(ratio1_thresholds)
        * len(hdelta_thresholds)
    )

    extended_total = (
        len(loss_thresholds)
        * len(max_ratio_thresholds)
        * len(ratio1_thresholds)
        * len(hdelta_thresholds)
        * len(dmax_thresholds)
        * len(cmax_thresholds)
    )

    grand_total = main_total + extended_total

    print(f"      Regole principali: {main_total}")
    print(f"      Regole estese:     {extended_total}")
    print(f"      Totale regole:     {grand_total}")
    print("")
    print("[5/6] Valuto regole...")

    rule_rows: List[Dict[str, object]] = []

    done = 0
    scan_start = time.time()

    # Precalcoli per ridurre overhead.
    base_masks = []

    for loss_t in loss_thresholds:
        m_loss = loss <= loss_t

        for ratio_t in max_ratio_thresholds:
            m_ratio = max_ratio <= ratio_t
            m_lr = m_loss & m_ratio

            for r1_t in ratio1_thresholds:
                m_r1 = ratio_1_until_h <= r1_t
                m_lrr = m_lr & m_r1

                for hd_t in hdelta_thresholds:
                    m_hd = h_delta <= hd_t
                    base_mask = m_lrr & m_hd

                    base_masks.append(
                        (
                            loss_t,
                            ratio_t,
                            r1_t,
                            hd_t,
                            base_mask,
                        )
                    )

                    selected = int(base_mask.sum())

                    if selected > 0:
                        false_hit = int((base_mask & false_mask).sum())
                        inter_hit = int((base_mask & inter_mask).sum())
                        true_hit = int((base_mask & true_mask).sum())
                        extreme_hit = int((base_mask & extreme_mask).sum())

                        precision_false = safe_pct(false_hit, selected)
                        recall_false = safe_pct(false_hit, false_total)
                        true_leak_pct = safe_pct(true_hit, true_total)
                        inter_leak_pct = safe_pct(inter_hit, inter_total)
                        extreme_leak_pct = safe_pct(extreme_hit, extreme_total)

                        score = (
                            100.0 * recall_false
                            + 60.0 * precision_false
                            - 150.0 * true_leak_pct
                            - 60.0 * inter_leak_pct
                            - 300.0 * extreme_leak_pct
                        )

                        rule_rows.append(
                            {
                                "rule_type": "main_4_conditions",
                                "loss_le": loss_t,
                                "max_ratio_le": ratio_t,
                                "ratio_1_until_h_le": r1_t,
                                "h_delta_at_log_step_le": hd_t,
                                "dmax_delta_le": "",
                                "cmax_delta_le": "",
                                "selected_total": selected,
                                "false_hit": false_hit,
                                "false_precision": precision_false,
                                "false_recall": recall_false,
                                "intermedio_hit": inter_hit,
                                "intermedio_leak_pct": inter_leak_pct,
                                "true_rebel_hit": true_hit,
                                "true_rebel_leak_pct": true_leak_pct,
                                "extreme_hit": extreme_hit,
                                "extreme_leak_pct": extreme_leak_pct,
                                "score": score,
                            }
                        )

                    done += 1
                    if done % args.progress_every == 0:
                        progress(done, grand_total, scan_start, prefix="      ")

    # Regole estese.
    for loss_t, ratio_t, r1_t, hd_t, base_mask in base_masks:
        if not base_mask.any():
            done += len(dmax_thresholds) * len(cmax_thresholds)
            if done % args.progress_every == 0:
                progress(done, grand_total, scan_start, prefix="      ")
            continue

        for dd_t in dmax_thresholds:
            m_dd = dmax_delta <= dd_t

            for cd_t in cmax_thresholds:
                m_cd = cmax_delta <= cd_t
                mask = base_mask & m_dd & m_cd

                selected = int(mask.sum())

                if selected > 0:
                    false_hit = int((mask & false_mask).sum())
                    inter_hit = int((mask & inter_mask).sum())
                    true_hit = int((mask & true_mask).sum())
                    extreme_hit = int((mask & extreme_mask).sum())

                    precision_false = safe_pct(false_hit, selected)
                    recall_false = safe_pct(false_hit, false_total)
                    true_leak_pct = safe_pct(true_hit, true_total)
                    inter_leak_pct = safe_pct(inter_hit, inter_total)
                    extreme_leak_pct = safe_pct(extreme_hit, extreme_total)

                    score = (
                        100.0 * recall_false
                        + 60.0 * precision_false
                        - 150.0 * true_leak_pct
                        - 60.0 * inter_leak_pct
                        - 300.0 * extreme_leak_pct
                    )

                    rule_rows.append(
                        {
                            "rule_type": "extended_6_conditions",
                            "loss_le": loss_t,
                            "max_ratio_le": ratio_t,
                            "ratio_1_until_h_le": r1_t,
                            "h_delta_at_log_step_le": hd_t,
                            "dmax_delta_le": dd_t,
                            "cmax_delta_le": cd_t,
                            "selected_total": selected,
                            "false_hit": false_hit,
                            "false_precision": precision_false,
                            "false_recall": recall_false,
                            "intermedio_hit": inter_hit,
                            "intermedio_leak_pct": inter_leak_pct,
                            "true_rebel_hit": true_hit,
                            "true_rebel_leak_pct": true_leak_pct,
                            "extreme_hit": extreme_hit,
                            "extreme_leak_pct": extreme_leak_pct,
                            "score": score,
                        }
                    )

                done += 1
                if done % args.progress_every == 0:
                    progress(done, grand_total, scan_start, prefix="      ")

    progress(grand_total, grand_total, scan_start, prefix="      ")

    print("")
    print(f"      Regole prodotte non vuote: {len(rule_rows)}")

    if not rule_rows:
        raise RuntimeError("Nessuna regola prodotta.")

    print("[6/6] Ordino e scrivo output...")

    rules = pd.DataFrame(rule_rows)

    rules = rules.sort_values(
        by=[
            "score",
            "false_recall",
            "false_precision",
            "true_rebel_hit",
            "intermedio_hit",
            "selected_total",
        ],
        ascending=[False, False, False, True, True, True],
    )

    rules.to_csv(out_csv_path, index=False, sep=";", quoting=csv.QUOTE_MINIMAL)

    clean_rules = rules[
        (rules["extreme_hit"] == 0)
        & (rules["true_rebel_hit"] <= 10)
        & (rules["false_hit"] >= 5)
    ].copy()

    clean_rules = clean_rules.sort_values(
        by=[
            "false_hit",
            "false_precision",
            "true_rebel_hit",
            "intermedio_hit",
            "score",
        ],
        ascending=[False, False, True, True, False],
    )

    very_clean_rules = rules[
        (rules["extreme_hit"] == 0)
        & (rules["true_rebel_hit"] == 0)
        & (rules["false_hit"] >= 1)
    ].copy()

    very_clean_rules = very_clean_rules.sort_values(
        by=[
            "false_hit",
            "false_precision",
            "intermedio_hit",
            "score",
        ],
        ascending=[False, False, True, False],
    )

    lines: List[str] = []

    lines.append("ANALISI 48 FAST - SOGLIE DESCRITTIVE FALSI ALLARMI VS RIBELLI")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Funzione baseline:")
    lines.append("  H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)")
    lines.append("")
    lines.append("Nota fondamentale:")
    lines.append("  Le regole qui cercate sono ex-post.")
    lines.append("  Usano loss, max_ratio, ratio_1_until_h e h_delta_at_log_step osservati lungo l'orbita.")
    lines.append("  Quindi NON sono direttamente una nuova funzione H(n).")
    lines.append("  Servono a classificare empiricamente i peggioramenti.")
    lines.append("")

    lines.append("Baseline H 100M:")
    lines.append(f"  LIMIT                  = {BASELINE['limit']}")
    lines.append(f"  dispari analizzati     = {BASELINE['odd_analyzed']}")
    lines.append(f"  avg_H_step             = {BASELINE['avg_H_step']}")
    lines.append(f"  max_H_step             = {BASELINE['max_H_step']}")
    lines.append(f"  worsened               = {BASELINE['worsened']}")
    lines.append(f"  FALSO_ALLARME          = {BASELINE['false_alarms']}")
    lines.append(f"  INTERMEDIO             = {BASELINE['intermedio']}")
    lines.append(f"  VERO_RIBELLE           = {BASELINE['true_rebels']}")
    lines.append(f"  VERO_RIBELLE_ESTREMO   = {BASELINE['true_rebels_extreme']}")
    lines.append("")

    lines.append("Righe lette dal CSV:")
    lines.append(f"  totale peggioramenti = {total_rows}")
    lines.append(f"  FALSO_ALLARME        = {false_total}")
    lines.append(f"  INTERMEDIO           = {inter_total}")
    lines.append(f"  VERO_RIBELLE*        = {true_total}")
    lines.append(f"  ESTREMI              = {extreme_total}")
    lines.append("")

    lines.append("Distribuzione famiglie:")
    lines.append("-" * 100)
    for fam_name, count in df["family"].value_counts().items():
        lines.append(f"  {fam_name:24s} {int(count)}")
    lines.append("")

    lines.append("Statistiche descrittive per famiglia:")
    lines.append("-" * 100)

    for fam_name in ["FALSO_ALLARME", "INTERMEDIO", "VERO_RIBELLE", "VERO_RIBELLE_ESTREMO"]:
        sub = df[df["family"] == fam_name]
        if len(sub) == 0:
            continue

        lines.append("")
        lines.append(f"{fam_name}:")
        lines.append(f"  loss:                    {summarize_numeric(sub['loss'])}")
        lines.append(f"  max_ratio:               {summarize_numeric(sub['max_ratio'])}")
        lines.append(f"  ratio_1_until_h:         {summarize_numeric(sub['ratio_1_until_h'])}")
        lines.append(f"  h_delta_at_log_step:     {summarize_numeric(sub['h_delta_at_log_step'])}")
        lines.append(f"  dmax_delta_at_log_step:  {summarize_numeric(sub['dmax_delta_at_log_step'])}")
        lines.append(f"  cmax_delta_at_log_step:  {summarize_numeric(sub['cmax_delta_at_log_step'])}")
        lines.append(f"  pmax_at_log_step:        {summarize_numeric(sub['pmax_at_log_step'])}")
    lines.append("")

    lines.append("Top 40 regole per score:")
    lines.append("-" * 100)
    for _, r in rules.head(40).iterrows():
        lines.append(
            "{rule_type:22s} | "
            "loss<={loss} | ratio<={ratio} | r1h<={r1} | hΔ<={hd} | dD<={dd} | dC<={dc} | "
            "sel={sel:4d} | false={fh:3d}/167 ({fr:6.2%}) | "
            "prec={prec:6.2%} | inter={ih:3d} | true={th:3d} | extreme={eh:3d} | score={score:8.2f}".format(
                rule_type=str(r["rule_type"]),
                loss=r["loss_le"],
                ratio=r["max_ratio_le"],
                r1=r["ratio_1_until_h_le"],
                hd=r["h_delta_at_log_step_le"],
                dd=r["dmax_delta_le"],
                dc=r["cmax_delta_le"],
                sel=int(r["selected_total"]),
                fh=int(r["false_hit"]),
                fr=float(r["false_recall"]),
                prec=float(r["false_precision"]),
                ih=int(r["intermedio_hit"]),
                th=int(r["true_rebel_hit"]),
                eh=int(r["extreme_hit"]),
                score=float(r["score"]),
            )
        )
    lines.append("")

    lines.append("Top 40 regole pulite: extreme_hit=0, true_rebel_hit<=10, false_hit>=5")
    lines.append("-" * 100)
    if clean_rules.empty:
        lines.append("  Nessuna regola pulita trovata con questi criteri.")
    else:
        for _, r in clean_rules.head(40).iterrows():
            lines.append(
                "{rule_type:22s} | "
                "loss<={loss} | ratio<={ratio} | r1h<={r1} | hΔ<={hd} | dD<={dd} | dC<={dc} | "
                "sel={sel:4d} | false={fh:3d}/167 ({fr:6.2%}) | "
                "prec={prec:6.2%} | inter={ih:3d} | true={th:3d} | extreme={eh:3d} | score={score:8.2f}".format(
                    rule_type=str(r["rule_type"]),
                    loss=r["loss_le"],
                    ratio=r["max_ratio_le"],
                    r1=r["ratio_1_until_h_le"],
                    hd=r["h_delta_at_log_step_le"],
                    dd=r["dmax_delta_le"],
                    dc=r["cmax_delta_le"],
                    sel=int(r["selected_total"]),
                    fh=int(r["false_hit"]),
                    fr=float(r["false_recall"]),
                    prec=float(r["false_precision"]),
                    ih=int(r["intermedio_hit"]),
                    th=int(r["true_rebel_hit"]),
                    eh=int(r["extreme_hit"]),
                    score=float(r["score"]),
                )
            )
    lines.append("")

    lines.append("Top 40 regole molto pulite: extreme_hit=0, true_rebel_hit=0")
    lines.append("-" * 100)
    if very_clean_rules.empty:
        lines.append("  Nessuna regola molto pulita trovata con questi criteri.")
    else:
        for _, r in very_clean_rules.head(40).iterrows():
            lines.append(
                "{rule_type:22s} | "
                "loss<={loss} | ratio<={ratio} | r1h<={r1} | hΔ<={hd} | dD<={dd} | dC<={dc} | "
                "sel={sel:4d} | false={fh:3d}/167 ({fr:6.2%}) | "
                "prec={prec:6.2%} | inter={ih:3d} | true={th:3d} | extreme={eh:3d} | score={score:8.2f}".format(
                    rule_type=str(r["rule_type"]),
                    loss=r["loss_le"],
                    ratio=r["max_ratio_le"],
                    r1=r["ratio_1_until_h_le"],
                    hd=r["h_delta_at_log_step_le"],
                    dd=r["dmax_delta_le"],
                    dc=r["cmax_delta_le"],
                    sel=int(r["selected_total"]),
                    fh=int(r["false_hit"]),
                    fr=float(r["false_recall"]),
                    prec=float(r["false_precision"]),
                    ih=int(r["intermedio_hit"]),
                    th=int(r["true_rebel_hit"]),
                    eh=int(r["extreme_hit"]),
                    score=float(r["score"]),
                )
            )
    lines.append("")

    lines.append("Lettura operativa:")
    lines.append("-" * 100)
    lines.append(
        "Se emergono regole con alta precisione sui FALSO_ALLARME e zero o quasi zero VERO_RIBELLE, "
        "allora i falsi allarmi sono una famiglia empiricamente isolabile."
    )
    lines.append(
        "Se invece ogni soglia che prende molti FALSO_ALLARME prende anche molti VERO_RIBELLE, "
        "allora i falsi deboli non sono separabili con queste variabili ex-post semplici."
    )
    lines.append(
        "Questa analisi serve a decidere se ha senso introdurre una classificazione post-validazione, "
        "non a modificare direttamente H(n)."
    )
    lines.append("")

    lines.append("Conclusione:")
    lines.append("-" * 100)
    lines.append(
        "Nessuna regola qui costituisce una prova formale. "
        "La baseline H resta una quasi-Lyapunov empirica validata numericamente a 100M."
    )

    out_summary_path.write_text("\n".join(lines), encoding="utf-8")

    elapsed_total = time.time() - t0

    print("")
    print("Analisi 48 FAST completata.")
    print(f"Tempo totale: {elapsed_total:.2f} secondi")
    print(f"Input:       {input_path}")
    print(f"Output CSV:  {out_csv_path}")
    print(f"Output TXT:  {out_summary_path}")
    print("")
    print("Top 10 regole per score:")
    print(
        rules[
            [
                "rule_type",
                "loss_le",
                "max_ratio_le",
                "ratio_1_until_h_le",
                "h_delta_at_log_step_le",
                "dmax_delta_le",
                "cmax_delta_le",
                "selected_total",
                "false_hit",
                "false_precision",
                "false_recall",
                "intermedio_hit",
                "true_rebel_hit",
                "extreme_hit",
                "score",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
