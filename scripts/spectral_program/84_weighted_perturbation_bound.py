"""
84_weighted_perturbation_bound.py

Sharper perturbative bound for the critical return operator using a
weighted row norm aligned with the spectrum of CORE.

Why this script.

    Script 83 showed that the gap rho(FULL) - rho(CORE) decays in T while
    ||TAIL||_inf does not. So the elementary bound

        rho(CORE + TAIL) <= rho(CORE) + ||TAIL||_inf

    is too coarse: it overestimates the perturbation by an order of
    magnitude because the boundary layer rows have large inf-norm but lie
    where the dominant eigenvector of CORE has small mass.

    The right object is a weighted bound. Let v >= 0 be a right
    nonnegative eigenvector of CORE for some eigenvalue mu_C close to
    rho(CORE). Then (CORE + TAIL) v = mu_C v + TAIL v, and by
    Collatz-Wielandt for nonneg matrices

        rho(CORE + TAIL) <= mu_C + max_i (TAIL v)_i / v_i

    provided v_i > 0 for all i in the support that matters. We measure
    that ratio. If it stays << 1 - mu_C uniformly in T and j, the
    perturbation strategy of the lemma is in the right form.

    To handle CORE possibly not being irreducible (so a single Perron
    eigenvector may not span all states) we also test using v_full, the
    right eigenvector of FULL itself. The latter always exists with
    positive entries on the recurrent classes; it gives the upper bound

        rho(FULL) = max_i (FULL v_full)_i / (v_full)_i

    so any inflation when restricted to TAIL is exactly the slack
    available for the perturbation argument.
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_84_weighted_perturbation_bound.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def perron_right_eigvec(
    M: np.ndarray,
    n_iter: int = 5000,
    tol: float = 1e-12,
    epsilon: float = 1e-12,
) -> tuple[float, np.ndarray]:
    """Right Perron eigenvector via power iteration on M + epsilon * J.

    The tiny rank-1 perturbation makes the matrix irreducible so the
    Perron-Frobenius theorem applies and the iteration converges to a
    strictly positive eigenvector. epsilon is below numerical noise so
    the eigenvalue is essentially rho(M)."""
    n = M.shape[0]
    if n == 0:
        return 0.0, np.zeros(0)
    M_pert = M + epsilon  # broadcasts: adds epsilon to every entry.
    v = np.ones(n) / n
    mu = 0.0
    for _ in range(n_iter):
        w = M_pert @ v
        nrm = w.max()
        if nrm <= 0:
            return 0.0, np.ones(n) / n
        w = w / nrm
        if np.linalg.norm(w - v, ord=np.inf) < tol:
            v = w
            mu = nrm
            break
        v = w
        mu = nrm
    return float(mu), v


def weighted_action_ratio(M: np.ndarray, v: np.ndarray, eps_floor: float) -> tuple[float, int]:
    """Return (max_i (M v)_i / v_i, argmax) restricted to coordinates
    where v_i > eps_floor. Ignores zero-mass coordinates."""
    if M.shape[0] == 0:
        return 0.0, -1
    Mv = M @ v
    mask = v > eps_floor
    if not mask.any():
        return 0.0, -1
    ratios = np.zeros_like(v)
    ratios[mask] = Mv[mask] / v[mask]
    i = int(np.argmax(ratios))
    return float(ratios[i]), i


def matrices_for_cell(tail_mod, T: int, j_count: int, args: argparse.Namespace):
    """Reproduce 77.analyze_T's matrix construction but return the dense
    FULL/CORE/TAIL matrices and the state list, instead of just rho's."""
    from collections import Counter, defaultdict

    op, shadowing, records, target, target_key, residue, modulus = tail_mod.setup()
    h_mod = 1 << args.hit_bits
    source_counts = Counter()
    all_rows = []
    groups = defaultdict(list)

    for r in range(1 << T):
        for h in range(h_mod):
            for j in range(j_count):
                t = r + (j << T)
                row = tail_mod.trace_row(
                    op=op,
                    shadowing=shadowing,
                    records=records,
                    target=target,
                    target_key=target_key,
                    residue=residue,
                    modulus=modulus,
                    t=t,
                    h=h,
                    odd_bits=args.odd_bits,
                    hit_bits=args.hit_bits,
                    v2_cap=args.v2_cap,
                    max_steps=args.max_steps,
                )
                source_counts[row["src"]] += 1
                all_rows.append(row)
                groups[(r, h)].append(row)

    for group_rows in groups.values():
        counts = Counter(row["signature"] for row in group_rows)
        core_sig, _ = counts.most_common(1)[0]
        for row in group_rows:
            row["part"] = "core" if row["signature"] == core_sig else "tail"

    states = sorted(set(source_counts) | {row["dst"] for row in all_rows if row["dst"] is not None})
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    FULL = np.zeros((n, n))
    CORE = np.zeros((n, n))
    TAIL = np.zeros((n, n))
    for row in all_rows:
        if row["terminal"]:
            continue
        denom = source_counts[row["src"]]
        if denom == 0:
            continue
        i, jj = idx[row["src"]], idx[row["dst"]]
        w = row["weight"] / denom
        FULL[i, jj] += w
        if row["part"] == "core":
            CORE[i, jj] += w
        else:
            TAIL[i, jj] += w
    return states, FULL, CORE, TAIL


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bound perturbativo pesato.")
    parser.add_argument("--T", default="8,10,12")
    parser.add_argument("--j-counts", default="16,32")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--eps-floor", type=float, default=1e-10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")

    rows = []
    print("=" * 138)
    print("  Weighted perturbation bound: rho(FULL) vs mu_C + ||TAIL v||_v")
    print("=" * 138)
    header = (
        f"  {'T':>3} {'j':>4} {'n':>5} "
        f"{'rho_full':>10} {'mu_core':>10} "
        f"{'||T v_C||_C':>12} {'bound_C':>10} "
        f"{'||T v_F||_F':>12} {'bound_F':>10} "
        f"{'gap_full-C':>11}"
    )
    print(header)
    print("-" * len(header))

    for T in parse_csv_ints(args.T):
        for j_count in parse_csv_ints(args.j_counts):
            states, FULL, CORE, TAIL = matrices_for_cell(tail_mod, T, j_count, args)

            mu_full, v_full = perron_right_eigvec(FULL)
            mu_core, v_core = perron_right_eigvec(CORE)

            # Weighted norm of TAIL using CORE's right eigenvector.
            tail_act_C, _ = weighted_action_ratio(TAIL, v_core, args.eps_floor)
            bound_C = mu_core + tail_act_C

            # Weighted norm of TAIL using FULL's right eigenvector.
            tail_act_F, _ = weighted_action_ratio(TAIL, v_full, args.eps_floor)
            # Sanity: full action ratio == mu_full.
            full_act_F, _ = weighted_action_ratio(FULL, v_full, args.eps_floor)
            core_act_F, _ = weighted_action_ratio(CORE, v_full, args.eps_floor)
            bound_F = core_act_F + tail_act_F

            row = {
                "T": T,
                "j_count": j_count,
                "states": len(states),
                "rho_full": mu_full,
                "mu_core": mu_core,
                "tail_action_on_v_core": tail_act_C,
                "bound_via_v_core": bound_C,
                "tail_action_on_v_full": tail_act_F,
                "core_action_on_v_full": core_act_F,
                "full_action_on_v_full": full_act_F,
                "bound_via_v_full": bound_F,
                "gap_full_minus_core": mu_full - mu_core,
            }
            rows.append(row)
            print(
                f"  {T:>3} {j_count:>4} {len(states):>5} "
                f"{mu_full:>10.6g} {mu_core:>10.6g} "
                f"{tail_act_C:>12.6g} {bound_C:>10.6g} "
                f"{tail_act_F:>12.6g} {bound_F:>10.6g} "
                f"{(mu_full - mu_core):>11.6g}"
            )

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")
    print()
    print("  Reading guide:")
    print("    bound_C = mu_core + max_i (TAIL v_core)_i / (v_core)_i")
    print("    bound_F = (CORE v_full + TAIL v_full ratios add up to mu_full)")
    print("    bound_C is a true upper bound for rho(FULL) when v_core supports all states;")
    print("    it should be >= rho_full and is the certifiable quantity.")


if __name__ == "__main__":
    main()
