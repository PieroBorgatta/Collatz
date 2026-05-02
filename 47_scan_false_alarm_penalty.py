#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
47_scan_false_alarm_penalty.py

Fase 03 - Scan empirico di una penalizzazione mirata sui falsi allarmi deboli.

Input:
    collatz_100M_validate_final_candidate.csv

Output:
    collatz_47_false_alarm_penalty_scan.csv
    collatz_47_false_alarm_penalty_summary.txt

Nota importante:
    Questo script NON rifà la validazione completa su tutti i dispari < 100M.
    Lavora solo sui 2839 casi peggiorati della baseline H.

    Serve a capire se una correzione locale, calcolabile dal lookahead 80,
    può ridurre i falsi allarmi senza intaccare troppo i veri ribelli.

Baseline:
    H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)

Variante esplorativa:
    WeakShortPressure(n) =
        max(0, Pmax80(n) - Pmax80^(m)(n))
        * max(0, threshold_ratio1_80 - ratio_1_80)

    H_47(n) = H(n) - gamma * WeakShortPressure(n)

Qui non si dichiara alcuna prova formale della Congettura di Collatz.
È solo una validazione empirica sui peggioramenti già individuati.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


LOG2_3 = math.log2(3.0)

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


def v2(x: int) -> int:
    """Restituisce v2(x), cioè l'esponente massimo di 2 che divide x."""
    if x <= 0:
        raise ValueError("v2 definito qui solo per interi positivi")

    return (x & -x).bit_length() - 1


def syracuse_next_odd(n: int) -> Tuple[int, int]:
    """
    Mappa accelerata di Syracuse sui dispari.

    S(n) = (3n + 1) / 2^v2(3n + 1)

    Ritorna:
        nuovo dispari, a = v2(3n+1)
    """
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


def lookahead_metrics(n: int, lookahead: int = 80) -> Dict[str, float]:
    """
    Ricalcola Dmax80, Cmax80, Pmax80, Pmax80^(m), ratio_1_80 e avg_v2_80.
    """
    cur = int(n)

    sum_a = 0.0
    count_a1 = 0

    dmax = 0.0
    cmax = 0.0
    pmax = 0.0
    pmax_argk = 0

    pmax_m = {
        4: 0.0,
        6: 0.0,
        8: 0.0,
        10: 0.0,
        12: 0.0,
    }

    a_values: List[int] = []

    for k in range(1, lookahead + 1):
        cur, a = syracuse_next_odd(cur)
        a_values.append(a)

        sum_a += a
        if a == 1:
            count_a1 += 1

        debt = k * LOG2_3 - sum_a
        cascade = sum_a - k * LOG2_3
        pressure = count_a1 / k

        if debt > dmax:
            dmax = debt

        if cascade > cmax:
            cmax = cascade

        if pressure > pmax:
            pmax = pressure
            pmax_argk = k

        for m in pmax_m:
            if k >= m and pressure > pmax_m[m]:
                pmax_m[m] = pressure

    ratio_1_80 = count_a1 / lookahead
    avg_v2_80 = sum(a_values) / lookahead

    out = {
        "dmax80_recalc": dmax,
        "cmax80_recalc": cmax,
        "pmax80_recalc": pmax,
        "pmax80_argk": pmax_argk,
        "ratio_1_80": ratio_1_80,
        "avg_v2_80": avg_v2_80,
    }

    for m, val in pmax_m.items():
        out[f"pmax80_m{m}"] = val
        out[f"drop_pmax_m{m}"] = pmax - val

    return out


def family(classification: str) -> str:
    """
    Estrae la famiglia principale dalla classificazione composita.
    """
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


def weak_short_pressure(
    row: pd.Series,
    m: int,
    threshold_ratio1_80: float,
) -> float:
    """
    Penalità esplorativa.

    L'idea:
    - se Pmax80 è alto solo per prefissi corti, drop_pmax_m è positivo;
    - se la densità globale di a_i=1 nei primi 80 passi è bassa,
      ratio_1_80 resta sotto soglia;
    - il prodotto isola una pressione breve ma poco sostenuta.

    Non usa loss, max_ratio o h_step, quindi è calcolabile già da n.
    """
    drop = max(0.0, float(row[f"drop_pmax_m{m}"]))
    ratio_gap = max(0.0, threshold_ratio1_80 - float(row["ratio_1_80"]))
    return drop * ratio_gap


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


def load_input(path: Path) -> pd.DataFrame:
    """
    Legge CSV separato da ; oppure ,.
    """
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
        "initial_dmax",
        "initial_cmax",
        "initial_pmax",
        "classification",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "CSV input non compatibile. Colonne mancanti: "
            + ", ".join(missing)
        )

    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan penalizzazione falsi allarmi deboli - Collatz Fase 03"
    )

    parser.add_argument(
        "--input",
        default="../collatz_100M_validate_final_candidate.csv",
        help="CSV peggioramenti baseline H a 100M",
    )

    parser.add_argument(
        "--out-csv",
        default="collatz_47_false_alarm_penalty_scan.csv",
        help="CSV output scan",
    )

    parser.add_argument(
        "--out-summary",
        default="collatz_47_false_alarm_penalty_summary.txt",
        help="TXT summary output",
    )

    parser.add_argument(
        "--lookahead",
        type=int,
        default=80,
        help="Lookahead Syracuse sui dispari",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    out_csv_path = Path(args.out_csv)
    out_summary_path = Path(args.out_summary)

    df = load_input(input_path)

    df["family"] = df["classification"].apply(family)

    # Ricalcolo metriche lookahead.
    records: List[Dict[str, float]] = []
    total = len(df)

    print(f"Leggo: {input_path}")
    print(f"Righe peggioramenti baseline: {total}")
    print("Ricalcolo lookahead 80 per ogni peggioramento...")

    for idx, n in enumerate(df["start"].astype(int), start=1):
        if idx % 250 == 0 or idx == total:
            print(f"  {idx}/{total}")

        metrics = lookahead_metrics(n, lookahead=args.lookahead)
        records.append(metrics)

    metrics_df = pd.DataFrame(records)
    full = pd.concat([df.reset_index(drop=True), metrics_df], axis=1)

    # Controlli di coerenza col CSV base.
    full["check_pmax_diff"] = full["initial_pmax"] - full["pmax80_recalc"]
    full["check_dmax_diff"] = full["initial_dmax"] - full["dmax80_recalc"]
    full["check_cmax_diff"] = full["initial_cmax"] - full["cmax80_recalc"]

    # Parametri dello scan.
    m_values = [4, 6, 8, 10, 12]

    threshold_values = [
        0.600,
        0.625,
        0.640,
        0.650,
        0.675,
    ]

    gamma_values = [
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.40,
        0.50,
        0.75,
        1.00,
        1.50,
        2.00,
        3.00,
        4.00,
        5.00,
    ]

    scan_rows: List[Dict[str, object]] = []

    # Questa è una simulazione sui soli peggioramenti:
    # se h_delta_at_log_step > 0 nella baseline, la H continua a essere peggiore del log.
    # La penalizzazione riduce h_delta_at_log_step.
    # Se h_delta_47_at_log_step <= 0, quel caso non sarebbe più peggioramento al log-step.
    #
    # ATTENZIONE:
    # questo non garantisce che non peggiori a un altro step successivo.
    # Per conferma servirà una validazione completa 48.
    for m in m_values:
        for thr in threshold_values:
            weak_col = f"weak_short_pressure_m{m}_thr{str(thr).replace('.', '_')}"

            full[weak_col] = full.apply(
                lambda r: weak_short_pressure(r, m=m, threshold_ratio1_80=thr),
                axis=1,
            )

            for gamma in gamma_values:
                h47_delta_col = (
                    f"h47_delta_m{m}_thr{str(thr).replace('.', '_')}"
                    f"_g{str(gamma).replace('.', '_')}"
                )

                full[h47_delta_col] = (
                    pd.to_numeric(full["h_delta_at_log_step"], errors="coerce")
                    - gamma * full[weak_col]
                )

                full[f"fixed_{h47_delta_col}"] = full[h47_delta_col] <= 0.0

                fixed_mask = full[f"fixed_{h47_delta_col}"]
                false_mask = full["family"] == "FALSO_ALLARME"
                inter_mask = full["family"] == "INTERMEDIO"
                true_mask = full["family"].apply(is_true_rebel_family)

                false_fixed = int((fixed_mask & false_mask).sum())
                inter_fixed = int((fixed_mask & inter_mask).sum())
                true_fixed = int((fixed_mask & true_mask).sum())

                false_total = int(false_mask.sum())
                inter_total = int(inter_mask.sum())
                true_total = int(true_mask.sum())

                remaining_worsened_among_known = total - int(fixed_mask.sum())
                remaining_false_among_known = false_total - false_fixed
                remaining_inter_among_known = inter_total - inter_fixed
                remaining_true_among_known = true_total - true_fixed

                # Score grezzo:
                # premia falsi corretti, penalizza veri ribelli corretti.
                # È solo un ordinamento euristico.
                score = false_fixed - 3.0 * true_fixed - 0.5 * inter_fixed

                scan_rows.append(
                    {
                        "m": m,
                        "threshold_ratio1_80": thr,
                        "gamma": gamma,
                        "known_worsened_baseline": total,
                        "fixed_total_known": int(fixed_mask.sum()),
                        "remaining_worsened_among_known": remaining_worsened_among_known,
                        "false_total": false_total,
                        "false_fixed": false_fixed,
                        "false_fixed_pct": false_fixed / false_total if false_total else 0.0,
                        "false_remaining": remaining_false_among_known,
                        "intermedio_total": inter_total,
                        "intermedio_fixed": inter_fixed,
                        "intermedio_fixed_pct": inter_fixed / inter_total if inter_total else 0.0,
                        "intermedio_remaining": remaining_inter_among_known,
                        "true_rebel_total": true_total,
                        "true_rebel_fixed": true_fixed,
                        "true_rebel_fixed_pct": true_fixed / true_total if true_total else 0.0,
                        "true_rebel_remaining": remaining_true_among_known,
                        "score": score,
                        "weak_mean_false": float(full.loc[false_mask, weak_col].mean()),
                        "weak_mean_intermedio": float(full.loc[inter_mask, weak_col].mean()),
                        "weak_mean_true_rebel": float(full.loc[true_mask, weak_col].mean()),
                    }
                )

    scan_df = pd.DataFrame(scan_rows)

    # Ordinamento utile:
    # 1. più falsi corretti
    # 2. meno veri ribelli corretti
    # 3. meno intermedi corretti
    # 4. score alto
    scan_df = scan_df.sort_values(
        by=[
            "false_fixed",
            "true_rebel_fixed",
            "intermedio_fixed",
            "score",
        ],
        ascending=[False, True, True, False],
    )

    scan_df.to_csv(out_csv_path, index=False, sep=";", quoting=csv.QUOTE_MINIMAL)

    # Summary testuale.
    lines: List[str] = []

    lines.append("SCAN 47 - PENALIZZAZIONE FALSI ALLARMI DEBOLI")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Funzione baseline:")
    lines.append("  H(n) = log(n) + 0.28*Dmax80(n) - 0.03*Cmax80(n) + 0.30*Pmax80(n)")
    lines.append("")
    lines.append("Variante esplorativa:")
    lines.append("  WeakShortPressure(n) =")
    lines.append("      max(0, Pmax80(n) - Pmax80^(m)(n))")
    lines.append("      * max(0, threshold_ratio1_80 - ratio_1_80)")
    lines.append("")
    lines.append("  H_47(n) = H(n) - gamma*WeakShortPressure(n)")
    lines.append("")
    lines.append("Nota fondamentale:")
    lines.append("  Questo script lavora solo sui peggioramenti già noti della baseline.")
    lines.append("  Non sostituisce una validazione completa a 100M.")
    lines.append("  Serve solo a scegliere eventuali candidati da validare nello script 48.")
    lines.append("")

    lines.append("Baseline H 100M:")
    lines.append(f"  LIMIT              = {BASELINE['limit']}")
    lines.append(f"  dispari analizzati = {BASELINE['odd_analyzed']}")
    lines.append(f"  avg_H_step         = {BASELINE['avg_H_step']}")
    lines.append(f"  max_H_step         = {BASELINE['max_H_step']}")
    lines.append(f"  worsened           = {BASELINE['worsened']}")
    lines.append(f"  FALSO_ALLARME      = {BASELINE['false_alarms']}")
    lines.append(f"  INTERMEDIO         = {BASELINE['intermedio']}")
    lines.append(f"  VERO_RIBELLE       = {BASELINE['true_rebels']}")
    lines.append(f"  VERO_RIBELLE_ESTREMO = {BASELINE['true_rebels_extreme']}")
    lines.append("")

    lines.append("Righe lette:")
    lines.append(f"  totale peggioramenti CSV = {len(full)}")
    lines.append("")

    lines.append("Distribuzione famiglie:")
    lines.append("-" * 100)
    fam_counts = full["family"].value_counts()
    for fam, count in fam_counts.items():
        lines.append(f"  {fam:24s} {int(count)}")
    lines.append("")

    lines.append("Controlli ricalcolo:")
    lines.append("-" * 100)
    lines.append(f"initial_pmax - pmax80_recalc: {summarize_numeric(full['check_pmax_diff'])}")
    lines.append(f"initial_dmax - dmax80_recalc: {summarize_numeric(full['check_dmax_diff'])}")
    lines.append(f"initial_cmax - cmax80_recalc: {summarize_numeric(full['check_cmax_diff'])}")
    lines.append("")

    lines.append("Descrittori chiave per famiglia:")
    lines.append("-" * 100)
    for fam in ["FALSO_ALLARME", "INTERMEDIO", "VERO_RIBELLE", "VERO_RIBELLE_ESTREMO"]:
        sub = full[full["family"] == fam]
        if len(sub) == 0:
            continue

        lines.append("")
        lines.append(f"{fam}:")
        lines.append(f"  loss:                 {summarize_numeric(sub['loss'])}")
        lines.append(f"  max_ratio:            {summarize_numeric(sub['max_ratio'])}")
        lines.append(f"  ratio_1_until_h:      {summarize_numeric(sub['ratio_1_until_h'])}")
        lines.append(f"  ratio_1_80:           {summarize_numeric(sub['ratio_1_80'])}")
        lines.append(f"  avg_v2_80:            {summarize_numeric(sub['avg_v2_80'])}")
        lines.append(f"  initial_pmax:         {summarize_numeric(sub['initial_pmax'])}")
        lines.append(f"  pmax80_argk:          {summarize_numeric(sub['pmax80_argk'])}")
        lines.append(f"  h_delta_at_log_step:  {summarize_numeric(sub['h_delta_at_log_step'])}")
    lines.append("")

    lines.append("Top 30 combinazioni ordinate per falsi corretti e veri ribelli preservati:")
    lines.append("-" * 100)

    top = scan_df.head(30)
    for _, r in top.iterrows():
        lines.append(
            "m={m:2d} | thr={thr:.3f} | gamma={gamma:5.2f} | "
            "false_fixed={ff:3d}/167 ({ffp:6.2%}) | "
            "true_fixed={tf:4d}/2465 ({tfp:6.2%}) | "
            "inter_fixed={ifx:3d}/207 ({ifp:6.2%}) | "
            "remaining_known={rw:4d} | score={score:8.2f}".format(
                m=int(r["m"]),
                thr=float(r["threshold_ratio1_80"]),
                gamma=float(r["gamma"]),
                ff=int(r["false_fixed"]),
                ffp=float(r["false_fixed_pct"]),
                tf=int(r["true_rebel_fixed"]),
                tfp=float(r["true_rebel_fixed_pct"]),
                ifx=int(r["intermedio_fixed"]),
                ifp=float(r["intermedio_fixed_pct"]),
                rw=int(r["remaining_worsened_among_known"]),
                score=float(r["score"]),
            )
        )

    lines.append("")
    lines.append("Top 30 combinazioni per score euristico:")
    lines.append("-" * 100)

    by_score = scan_df.sort_values(
        by=["score", "false_fixed", "true_rebel_fixed"],
        ascending=[False, False, True],
    ).head(30)

    for _, r in by_score.iterrows():
        lines.append(
            "m={m:2d} | thr={thr:.3f} | gamma={gamma:5.2f} | "
            "false_fixed={ff:3d}/167 ({ffp:6.2%}) | "
            "true_fixed={tf:4d}/2465 ({tfp:6.2%}) | "
            "inter_fixed={ifx:3d}/207 ({ifp:6.2%}) | "
            "remaining_known={rw:4d} | score={score:8.2f}".format(
                m=int(r["m"]),
                thr=float(r["threshold_ratio1_80"]),
                gamma=float(r["gamma"]),
                ff=int(r["false_fixed"]),
                ffp=float(r["false_fixed_pct"]),
                tf=int(r["true_rebel_fixed"]),
                tfp=float(r["true_rebel_fixed_pct"]),
                ifx=int(r["intermedio_fixed"]),
                ifp=float(r["intermedio_fixed_pct"]),
                rw=int(r["remaining_worsened_among_known"]),
                score=float(r["score"]),
            )
        )

    lines.append("")
    lines.append("Interpretazione operativa:")
    lines.append("-" * 100)
    lines.append(
        "Una combinazione interessante dovrebbe correggere un numero non banale di FALSO_ALLARME "
        "senza correggere troppi VERO_RIBELLE o VERO_RIBELLE_ESTREMO."
    )
    lines.append(
        "Se per correggere pochi falsi allarmi vengono corretti molti veri ribelli, "
        "la penalizzazione non è selettiva e non va promossa."
    )
    lines.append(
        "Il candidato migliore emerso qui va validato con uno script 48 su tutti i dispari < 100M, "
        "ricalcolando avg_H_step, max_H_step, worsened e classificazioni complete."
    )
    lines.append("")
    lines.append("Conclusione:")
    lines.append("-" * 100)
    lines.append(
        "Questo è uno screening empirico, non una prova formale. "
        "Non implica in alcun modo una dimostrazione della Congettura di Collatz."
    )

    out_summary_path.write_text("\n".join(lines), encoding="utf-8")

    print("")
    print("Scan 47 completato.")
    print(f"Input:       {input_path}")
    print(f"Output CSV:  {out_csv_path}")
    print(f"Output TXT:  {out_summary_path}")
    print("")
    print("Top 10:")
    print(
        scan_df[
            [
                "m",
                "threshold_ratio1_80",
                "gamma",
                "false_fixed",
                "true_rebel_fixed",
                "intermedio_fixed",
                "remaining_worsened_among_known",
                "score",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
