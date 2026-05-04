"""
52_phantom_basin_false_alarms.py

Test critico: i 2839 peggioramenti a 100M classificati in 46 — sono
distribuiti diversamente fra phantom basin e trivial basin a seconda della
loro classe (FALSO_ALLARME, VERO_RIBELLE, VERO_RIBELLE_ESTREMO, INTERMEDIO)?

Se sì:
  abbiamo un DISCRIMINATORE ALGEBRICO basato sulla posizione 2-adica del
  numero rispetto al phantom cycle a scala k. Questa e' una feature
  computabile a priori (data n, calcolo n mod 2^k, traccio f, vedo a quale
  ciclo arrivo) — la posso aggiungere a H(n).

Se no:
  i falsi allarmi non hanno una posizione 2-adica privilegiata rispetto al
  phantom, e l'ipotesi e' falsificata.
"""

import csv
import math
from collections import Counter, defaultdict

from scipy.stats import binomtest


def v2_split(m):
    a = 0
    while (m & 1) == 0:
        m >>= 1
        a += 1
    return a, m


def find_cycles(k):
    N = 1 << k
    half = N >> 1
    mask = N - 1
    next_idx = [0] * half
    a_of = [0] * half
    for i in range(half):
        r = (i << 1) | 1
        a, m_odd = v2_split(3 * r + 1)
        a_of[i] = a
        next_idx[i] = ((m_odd & mask) - 1) >> 1
    state = [0] * half
    cycle_of = [-1] * half
    cycles = []
    for start in range(half):
        if state[start] != 0:
            continue
        path = []
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = next_idx[cur]
        if state[cur] == 1:
            ci = path.index(cur)
            cyc_indices = path[ci:]
            cyc_id = len(cycles)
            cyc_a = [a_of[i] for i in cyc_indices]
            sum_a = sum(cyc_a)
            L = len(cyc_indices)
            try:
                product = (3 ** L) / (2 ** sum_a)
            except OverflowError:
                product = float("inf")
            cycles.append({
                "cycle_id": cyc_id,
                "indices": cyc_indices,
                "length": L,
                "sum_a": sum_a,
                "avg_a": sum_a / L,
                "product": product,
            })
            for i in cyc_indices:
                cycle_of[i] = cyc_id
        for i in path:
            state[i] = 2
    return cycles, cycle_of, next_idx


def basin_of_idx(idx, cycle_of, next_idx):
    cur = idx
    steps = 0
    while cycle_of[cur] == -1 and steps < 10**6:
        cur = next_idx[cur]
        steps += 1
    return cycle_of[cur], steps


def basin_for_n(n, k, cycle_of, next_idx):
    """Ritorna (cycle_id, steps) per n a scala k."""
    if n & 1 == 0:
        return -2, 0  # n pari (non dovrebbe accadere)
    residue = n & ((1 << k) - 1)
    if residue & 1 == 0:
        return -2, 0  # residuo pari (n era pari mod 2^k... impossibile per n dispari)
    idx = (residue - 1) >> 1
    return basin_of_idx(idx, cycle_of, next_idx)


def load_false_alarms(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            try:
                class_family = row.get("class_family") or row["classification"].split("+", 1)[0]
                rows.append({
                    "start": int(row["start"]),
                    "classification": row["classification"],
                    "class_family": class_family,
                    "loss": int(row["loss"]),
                    "max_ratio": float(row["max_ratio"]),
                    "ratio_1_until_h": float(row["ratio_1_until_h"]),
                })
            except (KeyError, ValueError) as e:
                print(f"[skip] {e}: {row}")
    return rows


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else float("nan")


def median(values):
    values = sorted(values)
    if not values:
        return float("nan")
    mid = len(values) // 2
    if len(values) % 2:
        return values[mid]
    return 0.5 * (values[mid - 1] + values[mid])


def analyze_at_k(rows, k):
    print(f"\n{'='*72}")
    print(f"  ANALISI a k={k}")
    print('='*72)

    cycles, cycle_of, next_idx = find_cycles(k)
    phantom_ids = {c["cycle_id"] for c in cycles if c["product"] > 1.0}
    trivial_ids = {c["cycle_id"] for c in cycles if c["product"] <= 1.0}

    print(f"  Cicli: {len(cycles)}, di cui phantom: {len(phantom_ids)}")
    half = 1 << (k - 1)
    # Correct basin computation: trace forward until reaching cycle
    n_phantom_basin = 0
    for i in range(half):
        cyc, _ = basin_of_idx(i, cycle_of, next_idx)
        if cyc in phantom_ids:
            n_phantom_basin += 1
    print(f"  Phantom basin size (basin completo, non solo ciclo): "
          f"{n_phantom_basin}/{half} ({n_phantom_basin/half*100:.2f}%)")

    if not phantom_ids:
        print("  Nessun phantom cycle — analisi inutile a questo k")
        return []

    # Per ogni riga, determina basin
    by_class = defaultdict(lambda: {
        "phantom": 0,
        "trivial": 0,
        "other": 0,
        "total": 0,
        "max_ratio": [],
        "loss": [],
        "ratio_1_until_h": [],
    })
    for row in rows:
        cyc_id, _ = basin_for_n(row["start"], k, cycle_of, next_idx)
        cls = row["class_family"]
        by_class[cls]["total"] += 1
        by_class[cls]["max_ratio"].append(row["max_ratio"])
        by_class[cls]["loss"].append(row["loss"])
        by_class[cls]["ratio_1_until_h"].append(row["ratio_1_until_h"])
        if cyc_id in phantom_ids:
            by_class[cls]["phantom"] += 1
        elif cyc_id in trivial_ids:
            by_class[cls]["trivial"] += 1
        else:
            by_class[cls]["other"] += 1

    expected_phantom = n_phantom_basin / half  # baseline frazione

    print(f"\n  Distribuzione per classe (atteso phantom % sotto uniforme: {expected_phantom*100:.2f}%):")
    print(f"  {'classe':>22} {'totale':>8} {'phantom':>10} {'trivial':>10} {'phantom%':>10} "
          f"{'enrich':>9} {'p_binom':>11} {'med_ratio':>11}")
    classes_order = ["FALSO_ALLARME", "VERO_RIBELLE", "VERO_RIBELLE_ESTREMO", "INTERMEDIO"]
    summary_rows = []
    for cls in classes_order + sorted(set(by_class.keys()) - set(classes_order)):
        if cls not in by_class:
            continue
        d = by_class[cls]
        if d["total"] == 0:
            continue
        frac = d["phantom"] / d["total"]
        enrich = frac / expected_phantom if expected_phantom > 0 else 0
        p_value = binomtest(d["phantom"], d["total"], expected_phantom, alternative="two-sided").pvalue
        med_ratio = median(d["max_ratio"])
        print(f"  {cls:>22} {d['total']:>8} {d['phantom']:>10} {d['trivial']:>10} "
              f"{frac*100:>9.2f}% {enrich:>8.3f}x {p_value:>11.3e} {med_ratio:>11.6f}")
        summary_rows.append({
            "k": k,
            "class_family": cls,
            "total": d["total"],
            "phantom": d["phantom"],
            "trivial": d["trivial"],
            "other": d["other"],
            "phantom_fraction": frac,
            "uniform_baseline": expected_phantom,
            "enrichment": enrich,
            "binom_p_value": p_value,
            "mean_max_ratio": mean(d["max_ratio"]),
            "median_max_ratio": med_ratio,
            "mean_loss": mean(d["loss"]),
            "median_loss": median(d["loss"]),
            "mean_ratio_1_until_h": mean(d["ratio_1_until_h"]),
        })

    # Classe pulita: quanto i falsi allarmi sono separabili dai veri ribelli?
    if "FALSO_ALLARME" in by_class:
        false_frac = by_class["FALSO_ALLARME"]["phantom"] / by_class["FALSO_ALLARME"]["total"]
        rebel_rows = [
            r for r in rows
            if r["class_family"] in {"VERO_RIBELLE", "VERO_RIBELLE_ESTREMO"}
        ]
        rebel_phantom = 0
        for row in rebel_rows:
            cyc_id, _ = basin_for_n(row["start"], k, cycle_of, next_idx)
            if cyc_id in phantom_ids:
                rebel_phantom += 1
        rebel_frac = rebel_phantom / len(rebel_rows) if rebel_rows else math.nan
        print(f"\n  Separazione grezza:")
        print(f"    FALSO_ALLARME in phantom: {false_frac*100:.2f}%")
        print(f"    RIBELLI in phantom:      {rebel_frac*100:.2f}%")
        if rebel_rows:
            lift = rebel_frac / false_frac if false_frac > 0 else math.inf
            print(f"    lift ribelli/falsi:      {lift:.3f}x")

    return summary_rows


def main():
    print("=" * 72)
    print("  Distribuzione phantom basin per classe di peggioramento (100M)")
    print("=" * 72)

    rows = load_false_alarms("collatz_46_false_alarms_analysis.csv")
    print(f"  Caricati {len(rows)} peggioramenti")

    classes = Counter(r["class_family"] for r in rows)
    print(f"\n  Distribuzione classi:")
    for cls, n in classes.most_common():
        print(f"    {cls}: {n}")

    # Test a vari k
    all_summary = []
    for k in [10, 11, 12, 20]:
        all_summary.extend(analyze_at_k(rows, k))

    out_path = "collatz_52_phantom_basin_false_alarms_summary.csv"
    if all_summary:
        fieldnames = list(all_summary[0].keys())
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(all_summary)
        print(f"\n  Salvato riepilogo: {out_path}")


if __name__ == "__main__":
    main()
