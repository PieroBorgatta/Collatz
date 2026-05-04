"""
50_deterministic_cycles.py

Analisi della mappa Syracuse deterministica sui residui mod 2^k.

==============================================================================
COSTRUZIONE
==============================================================================

f: {1, 3, 5, ..., 2^k - 1} -> {1, 3, ..., 2^k - 1}

Per residuo dispari r:
    a(r) = v_2(3r + 1)
    m(r) = (3r + 1) / 2^a(r)   (sempre dispari)
    f(r) = m(r) mod 2^k        (sempre dispari, perche' 2^k e' pari)

Il sistema discreto (Z/2^k)_dispari sotto f e' deterministico finito,
quindi ogni traiettoria entra in un ciclo dopo un transitorio.

Per ogni ciclo (r_1 -> r_2 -> ... -> r_L -> r_1):
    L            = lunghezza del ciclo
    sum_a        = a_1 + a_2 + ... + a_L
    avg_a        = sum_a / L
    cycle_product = 3^L / 2^sum_a  (rapporto di crescita asintotico per ciclo)
    log2_product  = L * log_2(3) - sum_a

Interpretazione:
- cycle_product > 1  (i.e., avg_a < log_2(3) ≈ 1.585): ciclo espansivo.
  E' una struttura metastabile a scala 2^k che ospita orbite ribelli.
- cycle_product = 1  (avg_a = log_2(3)): neutro (non puo' essere esatto su Q).
- cycle_product < 1  (avg_a > log_2(3)): ciclo dissipativo.

Il ciclo banale {1}: f(1) = (3+1)/4 = 1, quindi {1} con a=2, product = 3/4.
E' contrattivo come atteso (1 e' attrattore globale per Collatz reale).

==============================================================================
NOTA TEORICA
==============================================================================

I cicli di f sono cicli del sistema modulare, NON cicli della Collatz reale
sui naturali. Una possibile divergenza:
- ciclo modulare con product > 1 puo' NON sollevarsi a un ciclo reale,
  perche' a ogni passo le cifre alte di n sono determinate dalla storia
  reale, non riimpostate dalla riduzione mod 2^k.

Pero' i cicli espansivi modulari sono comunque interessanti: identificano
"corridoi 2-adici" in cui un'orbita reale puo' stazionare.

Nel linguaggio della teoria del debito: un ciclo modulare con product > 1
e' una "famiglia di confluenza espansiva" a scala k.

"""

import time
from math import log2

def v2_split(m):
    a = 0
    while (m & 1) == 0:
        m >>= 1
        a += 1
    return a, m


def find_cycles(k):
    """
    Restituisce:
      cycles: lista di dict con info su ciascun ciclo
      cycle_of: idx -> cycle_id (-1 se non in alcun ciclo, cioe' su un albero)
      next_idx: idx -> idx successivo in f
      a_of: idx -> a usato in quel passo
    """
    N = 1 << k
    half = N >> 1
    mask = N - 1

    # Precompute transitions
    next_idx = [0] * half
    a_of = [0] * half
    for i in range(half):
        r = (i << 1) | 1
        a, m_odd = v2_split(3 * r + 1)
        a_of[i] = a
        r_next = m_odd & mask
        next_idx[i] = (r_next - 1) >> 1

    state = [0] * half  # 0 unvisited, 1 in current path, 2 finalized
    cycle_of = [-1] * half
    cycles = []

    for start in range(half):
        if state[start] != 0:
            continue
        path = []
        cur = start
        # Walk until we hit a finalized node or revisit current path
        while state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = next_idx[cur]

        if state[cur] == 1:
            # Cur is in current path -> new cycle
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
                product = float('inf') if 3 ** L > 2 ** sum_a else 0.0
            cycles.append({
                "cycle_id": cycle_id,
                "residues": cycle_residues,
                "a_values": cycle_a_values,
                "length": L,
                "sum_a": sum_a,
                "avg_a": sum_a / L,
                "product": product,
                "log2_product": L * log2(3) - sum_a,
            })
            for idx in cycle_indices:
                cycle_of[idx] = cycle_id

        # Finalize all path nodes
        for idx in path:
            state[idx] = 2

    return cycles, cycle_of, next_idx, a_of


def basin_sizes(cycle_of, next_idx, n_cycles):
    """Per ogni ciclo, conta quanti residui ci confluiscono (incluso il ciclo)."""
    half = len(cycle_of)
    basin = [0] * n_cycles
    for i in range(half):
        cur = i
        while cycle_of[cur] == -1:
            cur = next_idx[cur]
        basin[cycle_of[cur]] += 1
    return basin


def analyze_k(k, verbose=True):
    t0 = time.time()
    cycles, cycle_of, next_idx, a_of = find_cycles(k)
    t1 = time.time()
    half = 1 << (k - 1)

    basins = basin_sizes(cycle_of, next_idx, len(cycles))
    for c, b in zip(cycles, basins):
        c["basin_size"] = b

    cycles_sorted = sorted(cycles, key=lambda c: -c["product"])

    n_expansive = sum(1 for c in cycles if c["product"] > 1.0)
    n_neutral = sum(1 for c in cycles if abs(c["product"] - 1.0) < 1e-12)
    n_contractive = sum(1 for c in cycles if c["product"] < 1.0)

    print(f"\n{'='*72}")
    print(f"  k = {k}   half = {half}   tempo: {t1-t0:.3f}s")
    print('='*72)
    print(f"  Cicli totali: {len(cycles)}")
    print(f"  Espansivi (product > 1):   {n_expansive}")
    print(f"  Neutri (product = 1):      {n_neutral}")
    print(f"  Dissipativi (product < 1): {n_contractive}")

    if cycles_sorted:
        max_p = cycles_sorted[0]["product"]
        min_p = cycles_sorted[-1]["product"]
        max_L = max(c["length"] for c in cycles)
        max_basin = max(c["basin_size"] for c in cycles)
        print(f"  Prodotto max: {max_p:.6f}    min: {min_p:.6e}")
        print(f"  Lunghezza max: {max_L}        Bacino max: {max_basin}/{half}")

    if verbose:
        print(f"\n  TOP 8 cicli per prodotto (decrescente):")
        print(f"  {'id':>3} {'L':>5} {'sum_a':>7} {'avg_a':>8} {'product':>14} {'log2(p)':>10} {'basin':>8}")
        for c in cycles_sorted[:8]:
            print(f"  {c['cycle_id']:>3} {c['length']:>5} {c['sum_a']:>7} "
                  f"{c['avg_a']:>8.4f} {c['product']:>14.6e} "
                  f"{c['log2_product']:>+10.4f} {c['basin_size']:>8}")
            if c["length"] <= 12:
                print(f"      residui: {c['residues']}")
                print(f"      a:       {c['a_values']}")

        print(f"\n  TOP 5 cicli per bacino (residui che confluiscono):")
        cycles_by_basin = sorted(cycles, key=lambda c: -c["basin_size"])
        print(f"  {'id':>3} {'L':>5} {'avg_a':>8} {'product':>14} {'basin':>8}")
        for c in cycles_by_basin[:5]:
            print(f"  {c['cycle_id']:>3} {c['length']:>5} {c['avg_a']:>8.4f} "
                  f"{c['product']:>14.6e} {c['basin_size']:>8}")

    return cycles


def main():
    print("=" * 72)
    print("  Cicli deterministici di f: Z/2^k -> Z/2^k per Syracuse")
    print("=" * 72)
    print(f"  Soglia critica: avg_a = log_2(3) ≈ {log2(3):.6f}")
    print(f"    avg_a > log_2(3) -> dissipativo (product < 1)")
    print(f"    avg_a < log_2(3) -> espansivo  (product > 1)")
    print(f"  Ciclo banale atteso: {{1}} con a=2, product = 3/4 = 0.75")

    summary = []
    # Scan completo k=6..20 per trovare il pattern dei cicli fantasma
    for k in range(6, 21):
        cycles = analyze_k(k, verbose=(k in [10, 11, 12, 13, 14, 16, 20]))
        summary.append({
            "k": k,
            "n_cycles": len(cycles),
            "n_expansive": sum(1 for c in cycles if c["product"] > 1),
            "max_product": max((c["product"] for c in cycles), default=0),
            "max_length": max((c["length"] for c in cycles), default=0),
            "max_basin_phantom": max(
                (c["basin_size"] for c in cycles if c["product"] > 1),
                default=0,
            ),
            "total_basin_phantom": sum(
                c["basin_size"] for c in cycles if c["product"] > 1
            ),
        })

    print(f"\n\n{'='*72}")
    print(f"  RIEPILOGO")
    print('='*72)
    print(f"  {'k':>3} {'cicli':>7} {'espansivi':>11} {'L max':>7} "
          f"{'product max':>14} {'max basin ph.':>14} {'tot basin ph.':>14}")
    for s in summary:
        marker = " <-- PHANTOM" if s["n_expansive"] > 0 else ""
        print(f"  {s['k']:>3} {s['n_cycles']:>7} {s['n_expansive']:>11} "
              f"{s['max_length']:>7} {s['max_product']:>14.6f} "
              f"{s['max_basin_phantom']:>14} {s['total_basin_phantom']:>14}{marker}")


if __name__ == "__main__":
    main()
