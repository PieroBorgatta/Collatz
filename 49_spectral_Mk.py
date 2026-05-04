"""
49_spectral_Mk.py

Analisi spettrale dell'operatore di trasferimento per la mappa Syracuse
sui residui dispari mod 2^k.

==============================================================================
COSTRUZIONE
==============================================================================

Stati: residui dispari r in {1, 3, 5, ..., 2^k - 1}, indicizzati i = (r-1)/2,
quindi half = 2^(k-1) stati.

Per ogni residuo r:
    a = v_2(3r+1)
    m = (3r+1) / 2^a   (dispari)

Transizione: nel modello di Markov mod 2^k, l'immagine dopo un passo
Syracuse appartiene alla classe m mod 2^(k-a), e la sua determinazione
piu' fine richiede informazione su n di ordine 2^k (che non abbiamo).
Distribuiamo quindi uniformemente la probabilita' sui 2^a residui mod 2^k
che si riducono a m mod 2^(k-a):
    P_k[i, j] = 1/2^a   se r' = m + l*2^(k-a) (mod 2^k) per qualche l in [0, 2^a)
              = 0       altrimenti

P_k e' una matrice stocastica (somma riga = 1). Per Perron-Frobenius
rho(P_k) = 1 e l'autovalore 1 e' algebricamente semplice (catena
ergodica). Gli altri autovalori |lambda_2|, |lambda_3|, ... < 1
controllano il tasso di mixing.

OPERATORE PESATO L_{k,q}:
    L_{k,q}[i, j] = P_k[i, j] * s(i)^q,     s(i) = 3 / 2^a_i

s(i) e' il fattore di crescita asintotico |S(n)/n| ~ 3/2^a per n grande,
e q e' un parametro di momento.

Per q=1, rho(L_{k,1}) misura il primo momento aritmetico:
    E[ |n_t| ] ~ |n_0| * rho(L_{k,1})^t

Questo NON e' il Lyapunov logaritmico. In regime i.i.d. ideale:
    E[3 / 2^a] = 1
quindi il primo momento e' neutro, dominato dalle code rare.

La contrazione "tipica" appare invece nella pressione:
    p_k(q) = log rho(L_{k,q})
e nel drift logaritmico:
    p'_k(0) ~= E[log(3 / 2^a)] = log(3/4) < 0.

Sotto distribuzione uniforme sulle classi dispari mod 2^k, il limite i.i.d.
per la pressione e':
    rho(q) = E[(3 / 2^a)^q] = 3^q / (2^(q+1) - 1).
Vale rho(0)=rho(1)=1, mentre rho(q)<1 per 0<q<1.

==============================================================================
RIFERIMENTI
==============================================================================

Quadro teorico affine: il preprint non peer-reviewed Nov 2025 "The Collatz
Conjecture and the Spectral Calculus for Arithmetic Dynamics"
(preprints.org/202511.1440) formula un approccio via operatore di
trasferimento, disuguaglianza Lasota-Yorke e gap spettrale su uno spazio
multiscala adattato al pre-image tree.

Questo script e' la realizzazione computazionale concreta a finita
dimensione di una discretizzazione diversa: residui dispari mod 2^k e
operatori pesati L_{k,q}.

"""

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import eigs
import time


def v2_split(m):
    """Ritorna (v_2(m), m / 2^v_2(m))."""
    a = 0
    while (m & 1) == 0:
        m >>= 1
        a += 1
    return a, m


def build_Pk_and_weighted(k, q_values=(1.0,)):
    """
    Costruisce simultaneamente:
      P_k: matrice Markov stocastica sui residui dispari mod 2^k
      L_{k,q}: operatori pesati L_q = diag(s^q) @ P,
               con s(i) = 3/2^a_i

    Ritorna (P_k, weighted_by_q, info) come csr_matrix.
    """
    N = 1 << k
    half = N >> 1
    P = lil_matrix((half, half), dtype=np.float64)
    weighted_by_q = {
        q: lil_matrix((half, half), dtype=np.float64)
        for q in q_values
    }

    boundary_count = 0  # residui con a >= k (caso degenere)
    a_distribution = {}

    for i in range(half):
        r = (i << 1) | 1  # 2i + 1
        a, m_odd = v2_split(3 * r + 1)
        a_distribution[a] = a_distribution.get(a, 0) + 1

        if a >= k:
            # Caso di confine: m mod 2^(k-a) ha precisione 0,
            # diffusione uniforme su tutti i residui dispari.
            boundary_count += 1
            prob_per = 1.0 / half
            s = 3.0 / (1 << a)
            for j in range(half):
                P[i, j] += prob_per
                for q, Lq in weighted_by_q.items():
                    Lq[i, j] += prob_per * (s ** q)
            continue

        prob_per = 1.0 / (1 << a)
        s = 3.0 / (1 << a)

        step = 1 << (k - a)
        m_low = m_odd & (step - 1)  # m mod 2^(k-a)
        n_targets = 1 << a
        for l in range(n_targets):
            r_prime = (m_low + l * step) & (N - 1)
            if r_prime == 0:
                # Non dovrebbe mai succedere: m e' dispari, quindi m_low dispari
                continue
            idx = (r_prime - 1) >> 1
            P[i, idx] += prob_per
            for q, Lq in weighted_by_q.items():
                Lq[i, idx] += prob_per * (s ** q)

    info = {
        "k": k,
        "half": half,
        "boundary_count": boundary_count,
        "a_distribution": a_distribution,
    }
    return (
        csr_matrix(P),
        {q: csr_matrix(Lq) for q, Lq in weighted_by_q.items()},
        info,
    )


def spectral_analysis(M, n_eigs=10, label="M"):
    """Calcola autovalori di magnitudine massima."""
    n_eigs = min(n_eigs, M.shape[0] - 2)
    t0 = time.time()
    try:
        eigenvalues = eigs(
            M, k=n_eigs, which="LM",
            return_eigenvectors=False,
            maxiter=10000, tol=1e-10,
        )
    except Exception as e:
        print(f"  [errore eigs su {label}]: {e}")
        return None
    t1 = time.time()
    eigenvalues = sorted(eigenvalues, key=lambda x: -abs(x))
    return {
        "eigenvalues": eigenvalues,
        "rho": abs(eigenvalues[0]),
        "elapsed_s": t1 - t0,
    }


def print_eigs(result, label):
    if result is None:
        return
    print(f"\n--- Spettro di {label} (top {len(result['eigenvalues'])}) ---")
    print(f"  rho = |lambda_1| = {result['rho']:.8f}")
    print(f"  tempo eigs: {result['elapsed_s']:.3f}s")
    for i, ev in enumerate(result["eigenvalues"]):
        if abs(ev.imag) < 1e-10:
            print(f"    lambda_{i+1} = {ev.real:+.8f}                  |.| = {abs(ev):.8f}")
        else:
            sign = "+" if ev.imag >= 0 else "-"
            print(f"    lambda_{i+1} = {ev.real:+.8f} {sign} {abs(ev.imag):.8f}i  |.| = {abs(ev):.8f}")


def report_a_distribution(info):
    half = info["half"]
    print(f"\n  Distribuzione a = v_2(3r+1) sui {half} residui dispari mod 2^{info['k']}:")
    print(f"  (atteso: P(a=j) = 1/2^j sotto residuo uniforme)")
    print(f"  {'a':>3} {'count':>8} {'osservata':>10} {'attesa':>10}")
    total = sum(info["a_distribution"].values())
    for a in sorted(info["a_distribution"].keys()):
        c = info["a_distribution"][a]
        obs = c / total
        exp = 1 / (1 << a) if a < info["k"] else 0
        print(f"  {a:>3} {c:>8} {obs:>10.6f} {exp:>10.6f}")
    print(f"  Boundary residues (a >= k): {info['boundary_count']}")


def iid_pressure_limit(q):
    """Limite i.i.d. per E[(3/2^a)^q], con P(a=j)=2^-j."""
    return (3.0 ** q) / ((2.0 ** (q + 1.0)) - 1.0)


def main():
    print("=" * 76)
    print("  Analisi spettrale L_{k,q} per Collatz/Syracuse mod 2^k")
    print("=" * 76)
    log2_3 = np.log2(3)
    print(f"  Drift atteso (random walk a~Geo(1/2)): log(3/4) = {np.log(0.75):+.6f} nat")
    print(f"  rho(L_1) atteso (primo momento):       1.0      = {1.0:.6f}")
    print(f"  rho(P) atteso (Markov stocastico):     1.0")
    print(f"  log_2(3) (soglia critica per a):       {log2_3:.6f}")
    print()

    results = {}
    q_values = (0.25, 0.50, 0.75, 1.00, 1.25, 1.50)

    for k in [6, 8, 10]:
        print(f"\n{'=' * 76}")
        print(f"  k = {k}   (residui dispari = 2^{k-1} = {1 << (k-1)})")
        print('=' * 76)

        t_build = time.time()
        P, weighted_by_q, info = build_Pk_and_weighted(k, q_values=q_values)
        t_build = time.time() - t_build
        print(f"  Costruzione matrici: {t_build:.3f}s   (nnz P = {P.nnz})")

        report_a_distribution(info)

        n_eigs = 8 if k <= 8 else 12

        res_P = spectral_analysis(P, n_eigs=n_eigs, label=f"P_{k}")
        print_eigs(res_P, f"P_{k} (Markov stocastica)")

        L1 = weighted_by_q[1.0]
        res_L = spectral_analysis(L1, n_eigs=n_eigs, label=f"L_{k},q=1")
        print_eigs(res_L, f"L_{k}, q=1 (primo momento aritmetico)")

        if res_L is not None:
            rho_L = res_L["rho"]
            verdict = "NEUTRO/TAIL-DOMINATO" if abs(rho_L - 1.0) < 1e-3 else (
                "CONTRAZIONE" if rho_L < 1 else "ESPANSIONE"
            )
            print(f"\n  >> rho(L_{k}, q=1) = {rho_L:.8f}   [{verdict}]")
            print(f"  >> log_2(rho) = {np.log2(rho_L):+.8f}")
            print(f"  >> rapporto con limite primo-momento 1.0: {rho_L:.6f}")
        if res_P is not None:
            rho_P = res_P["rho"]
            lambda_2 = abs(res_P["eigenvalues"][1])
            print(f"  >> rho(P_{k}) = {rho_P:.8f}   (atteso 1.0)")
            print(f"  >> gap spettrale: 1 - |lambda_2(P)| = {1 - lambda_2:.8f}")

        pressure_rows = []
        print(f"\n  Pressione p_k(q) = log rho(L_{{k,q}}):")
        print(f"  {'q':>6} {'rho_num':>12} {'log_rho':>12} {'rho_iid':>12} {'delta':>12}")
        for q in q_values:
            res_q = spectral_analysis(weighted_by_q[q], n_eigs=4, label=f"L_{k},q={q:g}")
            if res_q is None:
                continue
            rho_q = res_q["rho"]
            rho_iid = iid_pressure_limit(q)
            pressure_rows.append((q, rho_q, np.log(rho_q), rho_iid))
            print(f"  {q:>6.2f} {rho_q:>12.8f} {np.log(rho_q):>+12.8f} "
                  f"{rho_iid:>12.8f} {rho_q-rho_iid:>+12.2e}")

        results[k] = {
            "P": res_P,
            "L": res_L,
            "info": info,
            "pressure": pressure_rows,
        }

    # Riepilogo finale
    print(f"\n\n{'=' * 76}")
    print("  RIEPILOGO")
    print('=' * 76)
    print(f"  {'k':>3} {'half':>8} {'rho(L_1)':>12} {'log2(rho)':>12} {'rho(P_k)':>12} {'gap(P_k)':>12}")
    for k in sorted(results.keys()):
        r = results[k]
        rho_L = r["L"]["rho"] if r["L"] else float("nan")
        rho_P = r["P"]["rho"] if r["P"] else float("nan")
        gap = 1 - abs(r["P"]["eigenvalues"][1]) if r["P"] else float("nan")
        log2_r = np.log2(rho_L) if rho_L > 0 else float("-inf")
        print(f"  {k:>3} {r['info']['half']:>8} {rho_L:>12.8f} {log2_r:>+12.8f} {rho_P:>12.8f} {gap:>12.8f}")


if __name__ == "__main__":
    main()
