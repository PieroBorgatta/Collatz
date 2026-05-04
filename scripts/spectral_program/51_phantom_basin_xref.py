"""
51_phantom_basin_xref.py

Cross-reference fra:
  (a) i basin dei "phantom cycle" della mappa deterministica f mod 2^k
      (vedi 50_deterministic_cycles.py)
  (b) il tronco di confluenza 8.216.025.965 (e i 62 ribelli sotto 5M)
  (c) le statistiche empiriche per residuo mod 2^10
      (collatz_classi_mod_2^10_limit_5000000.csv)
  (d) le statistiche multistep mod 2^10
      (collatz_classi_multistep_mod_2^10_limit_5000000_steps_40.csv)

OBIETTIVO
---------
Verificare l'ipotesi: i residui che ospitano orbite empiricamente esplosive
sono concentrati nel BASIN dei cicli fantasma di f mod 2^k.

Se sì:
  * il "ribelle" e' un'orbita reale che si aggancia temporaneamente
    a un ciclo fantasma di scala k;
  * la crescita osservata corrisponde al cycle product del fantasma;
  * il tronco di confluenza e' la "via di uscita" dal fantasma verso il
    bacino del ciclo banale {1}.
"""

import csv
import time
from math import log2

TRONCO = 8_216_025_965


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
        r_next = m_odd & mask
        next_idx[i] = (r_next - 1) >> 1

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
            cycle_indices = path[ci:]
            cycle_id = len(cycles)
            cycle_a_values = [a_of[idx] for idx in cycle_indices]
            cycle_residues = [(idx << 1) | 1 for idx in cycle_indices]
            sum_a = sum(cycle_a_values)
            L = len(cycle_indices)
            try:
                product = (3 ** L) / (2 ** sum_a)
            except OverflowError:
                product = float("inf")
            cycles.append({
                "cycle_id": cycle_id,
                "indices": cycle_indices,
                "residues": cycle_residues,
                "a_values": cycle_a_values,
                "length": L,
                "sum_a": sum_a,
                "avg_a": sum_a / L,
                "product": product,
            })
            for idx in cycle_indices:
                cycle_of[idx] = cycle_id
        for idx in path:
            state[idx] = 2

    return cycles, cycle_of, next_idx, a_of


def basin_of_idx(idx, cycle_of, next_idx):
    """Trova il cycle_id a cui converge l'indice idx."""
    cur = idx
    steps = 0
    while cycle_of[cur] == -1 and steps < 10**6:
        cur = next_idx[cur]
        steps += 1
    return cycle_of[cur], steps


def report_cycles(cycles, label=""):
    cycles_sorted = sorted(cycles, key=lambda c: -c["product"])
    print(f"\n  Cicli a {label}: {len(cycles)} totali")
    print(f"  {'id':>3} {'L':>4} {'avg_a':>7} {'product':>14}")
    for c in cycles_sorted:
        marker = " (banale)" if c["length"] == 1 and c["residues"] == [1] else ""
        marker += " <- PHANTOM" if c["product"] > 1 else ""
        print(f"  {c['cycle_id']:>3} {c['length']:>4} {c['avg_a']:>7.4f} "
              f"{c['product']:>14.6e}{marker}")


def cross_reference_tronco(k_values):
    print("\n" + "=" * 76)
    print("  CROSS-REFERENCE 1: tronco 8.216.025.965 mod 2^k")
    print("=" * 76)
    print(f"  Tronco = {TRONCO}")
    print(f"  Tronco e' dispari? {TRONCO & 1 == 1}")

    print(f"\n  {'k':>3} {'mask':>10} {'tronco mod 2^k':>16} {'basin cycle':>14} "
          f"{'cycle product':>15} {'steps to cycle':>16}")
    for k in k_values:
        cycles, cycle_of, next_idx, a_of = find_cycles(k)
        residue = TRONCO & ((1 << k) - 1)
        if residue & 1 == 0:
            print(f"  {k:>3}  RESIDUO PARI: {residue} (impossibile in mappa S)")
            continue
        idx = (residue - 1) >> 1
        cyc_id, steps = basin_of_idx(idx, cycle_of, next_idx)
        if cyc_id < 0:
            cyc_label = "n/a"
            cyc_product = float("nan")
        else:
            cyc = cycles[cyc_id]
            cyc_label = f"id={cyc_id} (L={cyc['length']})"
            cyc_product = cyc["product"]
            if cyc["product"] > 1:
                cyc_label += " PHANTOM!"
        print(f"  {k:>3}  {(1<<k):>10}  {residue:>16}  {cyc_label:>14}  "
              f"{cyc_product:>15.6e}  {steps:>16}")


def cross_reference_classi_mod_1024():
    """
    Confronta la classifica empirica per residuo mod 1024 con il basin
    del phantom cycle a k=10.
    """
    print("\n" + "=" * 76)
    print("  CROSS-REFERENCE 2: residui mod 1024 - basin phantom vs avg_max_ratio")
    print("=" * 76)

    cycles, cycle_of, next_idx, a_of = find_cycles(10)
    report_cycles(cycles, "k=10")

    # Trova il phantom cycle (id != ciclo banale {1})
    phantom_ids = [c["cycle_id"] for c in cycles if c["product"] > 1]
    if not phantom_ids:
        print("  Nessun phantom cycle a k=10 — niente da confrontare")
        return
    phantom_id = phantom_ids[0]
    phantom = cycles[phantom_id]
    print(f"\n  Phantom cycle scelto: id={phantom_id}, L={phantom['length']}, "
          f"product={phantom['product']:.4f}")
    phantom_basin = set()
    for i in range(len(cycle_of)):
        cyc, _ = basin_of_idx(i, cycle_of, next_idx)
        if cyc == phantom_id:
            phantom_basin.add((i << 1) | 1)
    print(f"  Basin phantom: {len(phantom_basin)} residui")

    # Carica statistiche multistep
    multistep_path = "collatz_classi_multistep_mod_2^10_limit_5000000_steps_40.csv"
    rows = []
    with open(multistep_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            try:
                row["classe_mod"] = int(row["classe_mod"])
                row["count"] = int(row["count"])
                row["avg_max_ratio"] = float(row["avg_max_ratio"])
                row["max_ratio"] = float(row["max_ratio"])
                row["avg_final_ratio"] = float(row["avg_final_ratio"])
                row["min_final_ratio"] = float(row["min_final_ratio"])
                row["no_descent_ratio"] = float(row["no_descent_ratio"])
                rows.append(row)
            except (KeyError, ValueError):
                continue

    print(f"  Caricati {len(rows)} residui dispari da {multistep_path}")

    # Sort by avg_max_ratio descending
    rows.sort(key=lambda r: -r["avg_max_ratio"])

    # Top 30 most expansive — quanti sono nel phantom basin?
    top_n_values = [10, 30, 50, 100, 200, 256, 512]
    print(f"\n  Top-N residui per avg_max_ratio: quanti nel phantom basin?")
    print(f"  {'top N':>7} {'in basin':>10} {'in cycle banale':>17} {'frazione phantom':>18}")
    for top_n in top_n_values:
        if top_n > len(rows):
            continue
        in_basin = sum(1 for r in rows[:top_n] if r["classe_mod"] in phantom_basin)
        in_trivial = top_n - in_basin
        frac = in_basin / top_n
        print(f"  {top_n:>7} {in_basin:>10} {in_trivial:>17} {frac:>18.4f}")

    # Also: top 20 worst residues with full info
    print(f"\n  Top 20 residui per avg_max_ratio (mod 1024):")
    print(f"  {'residue':>8} {'avg_max_ratio':>14} {'no_descent_ratio':>17} {'phantom?':>10}")
    for r in rows[:20]:
        in_phantom = "PHANTOM" if r["classe_mod"] in phantom_basin else "banale"
        print(f"  {r['classe_mod']:>8} {r['avg_max_ratio']:>14.4f} "
              f"{r['no_descent_ratio']:>17.6f} {in_phantom:>10}")

    # Statistiche aggregate
    in_phantom = [r for r in rows if r["classe_mod"] in phantom_basin]
    in_trivial = [r for r in rows if r["classe_mod"] not in phantom_basin]
    if in_phantom and in_trivial:
        print(f"\n  Statistiche aggregate (avg_max_ratio):")
        print(f"  {'gruppo':>15} {'n':>6} {'media':>14} {'mediana':>14} {'max':>14}")
        for label, group in [("phantom basin", in_phantom),
                             ("trivial basin", in_trivial)]:
            vals = [r["avg_max_ratio"] for r in group]
            mean = sum(vals) / len(vals)
            med = sorted(vals)[len(vals) // 2]
            mx = max(vals)
            print(f"  {label:>15} {len(group):>6} {mean:>14.4f} {med:>14.4f} {mx:>14.4f}")
        print(f"\n  Statistiche aggregate (no_descent_ratio):")
        print(f"  {'gruppo':>15} {'n':>6} {'media':>14} {'mediana':>14} {'max':>14}")
        for label, group in [("phantom basin", in_phantom),
                             ("trivial basin", in_trivial)]:
            vals = [r["no_descent_ratio"] for r in group]
            mean = sum(vals) / len(vals)
            med = sorted(vals)[len(vals) // 2]
            mx = max(vals)
            print(f"  {label:>15} {len(group):>6} {mean:>14.6f} {med:>14.6f} {mx:>14.6f}")


def main():
    t0 = time.time()
    print("=" * 76)
    print("  Cross-reference fra phantom cycles e dati empirici")
    print("=" * 76)

    # 1) Cross-ref tronco
    cross_reference_tronco([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

    # 2) Cross-ref residui mod 1024 con statistiche empiriche
    cross_reference_classi_mod_1024()

    print(f"\n\nTempo totale: {time.time()-t0:.2f}s")


if __name__ == "__main__":
    main()
