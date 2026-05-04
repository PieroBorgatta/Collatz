"""
85_truncation_stability.py

Empirical truncation error of FULL_{T, j_count} as j_count grows.

Why this script.

    The matrices FULL_{T, j} used in scripts 77/82/84 are built by sampling
    a finite range j = 0..j_count-1 of high-bit lifts. The bound

        rho(FULL_{T, j}) <= core_action(v) + tail_action(v) <~ 0.054

    is a valid upper bound for the truncated operator. It only certifies
    the true (untruncated) return operator if FULL_{T, j} stabilizes as j
    grows. Script 76 already showed that ~30% of (r, h) groups have a
    transition signature that changes between lifts at T=12.

    Concretely we ask:

      (1) does the dominant transition signature per (r, h) group
          stabilize as j_count doubles?
      (2) does the action of FULL_{T, j} on a fixed test vector v converge
          in j (Cauchy property)?
      (3) does the perturbative bound bound_F(T, j) admit a Cauchy tail in
          j that is small compared to (1 - bound_F)?

    If (2) and (3) hold with geometric decay in j, we have an a posteriori
    truncation certificate: the limit operator's bound differs from the
    finite-j bound by a quantifiable amount, all of which is still well
    below 1.

The script reuses 84.matrices_for_cell to build FULL/CORE/TAIL and a fixed
v computed from j_count = j_min. It then measures, for j in a doubling
sequence:

    delta_action(j) = || (FULL_{T, j} - FULL_{T, j_min}) v ||_inf
    delta_bound(j)  = bound_F(T, j) - bound_F(T, j_min)
    sig_drift(j)    = fraction of (r, h) groups whose dominant signature
                      changed when going from j_min to j
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_85_truncation_stability.csv"


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


def trace_block(tail_mod, T: int, j_count: int, args: argparse.Namespace):
    """Like 84.matrices_for_cell but also returns per-(r,h) dominant
    signatures so we can measure signature drift across truncations."""
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

    dominant_sigs = {}
    for key, group_rows in groups.items():
        counts = Counter(row["signature"] for row in group_rows)
        core_sig, _ = counts.most_common(1)[0]
        dominant_sigs[key] = core_sig
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
    return states, idx, FULL, CORE, TAIL, dominant_sigs


def evaluate_with_test_vector(FULL: np.ndarray, CORE: np.ndarray, TAIL: np.ndarray, v: np.ndarray, eps: float):
    Fv = FULL @ v
    Cv = CORE @ v
    Tv = TAIL @ v
    mask = v > eps
    if not mask.any():
        return 0.0, 0.0, 0.0
    full_act = float((Fv[mask] / v[mask]).max())
    core_act = float((Cv[mask] / v[mask]).max())
    tail_act = float((Tv[mask] / v[mask]).max())
    return full_act, core_act, tail_act


def realign_to_states(M: np.ndarray, states_src: list, states_dst: list, idx_dst: dict) -> np.ndarray:
    """Pad/permute M (built on states_src) into a matrix on states_dst."""
    n = len(states_dst)
    out = np.zeros((n, n))
    for i_src, s_src in enumerate(states_src):
        if s_src not in idx_dst:
            continue
        i_dst = idx_dst[s_src]
        for j_src, s_dst in enumerate(states_src):
            if s_dst not in idx_dst:
                continue
            j_dst = idx_dst[s_dst]
            out[i_dst, j_dst] = M[i_src, j_src]
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stabilita' del troncamento in j.")
    parser.add_argument("--T", default="10,12")
    parser.add_argument("--j-counts", default="16,32,64,128")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--eps-floor", type=float, default=1e-10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    bound_mod = load_module("84_weighted_perturbation_bound.py", "weighted_bound")

    Ts = parse_csv_ints(args.T)
    js = sorted(parse_csv_ints(args.j_counts))
    j_min = js[0]

    rows = []
    print("=" * 140)
    print("  Truncation stability in j (Cauchy test, fixed test vector from j_min)")
    print("=" * 140)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, j_min={j_min}")
    print("  Each j uses its own Perron eigenvector v_j; bound is bound_F(T, j).")

    for T in Ts:
        # Reference: build at j_min, get test vector v0 and reference bound.
        states_ref, idx_ref, F_ref, C_ref, Tm_ref, sigs_ref = trace_block(tail_mod, T, j_min, args)
        _, v_ref = bound_mod.perron_right_eigvec(F_ref)
        full0, core0, tail0 = evaluate_with_test_vector(F_ref, C_ref, Tm_ref, v_ref, args.eps_floor)
        bound0 = core0 + tail0
        n_groups = (1 << T) * (1 << args.hit_bits)

        prev_sigs = sigs_ref
        prev_bound = bound0
        for j in js:
            states_j, idx_j, F_j, C_j, Tm_j, sigs_j = trace_block(tail_mod, T, j, args)
            # Use j's own Perron vector to evaluate bound_F(T, j). This is
            # the certifiable quantity for this j_count.
            _, v_j = bound_mod.perron_right_eigvec(F_j)
            full_j, core_j, tail_j = evaluate_with_test_vector(
                F_j, C_j, Tm_j, v_j, max(args.eps_floor, 1e-6 * v_j.max())
            )
            bound_j = core_j + tail_j

            # Signature drift: vs j_min and vs the previous j.
            drift_vs_min = sum(
                1 for k, sig in sigs_ref.items() if sig != sigs_j.get(k, sig)
            )
            drift_vs_prev = sum(
                1 for k, sig in prev_sigs.items() if sig != sigs_j.get(k, sig)
            )
            sig_drift_min = drift_vs_min / n_groups
            sig_drift_prev = drift_vs_prev / n_groups

            row = {
                "T": T,
                "j_count": j,
                "n_groups": n_groups,
                "sig_drift_vs_jmin": sig_drift_min,
                "sig_drift_vs_prev": sig_drift_prev,
                "full_action": full_j,
                "core_action": core_j,
                "tail_action": tail_j,
                "bound": bound_j,
                "delta_bound_vs_jmin": bound_j - bound0,
                "delta_bound_vs_prev": bound_j - prev_bound,
            }
            rows.append(row)
            print(
                f"  {T:>3} {j:>4} drift_min={sig_drift_min:>7.4f} drift_prev={sig_drift_prev:>7.4f} "
                f"core={core_j:>9.6g} tail={tail_j:>9.6g} bound={bound_j:>9.6g} "
                f"d_bnd_min={(bound_j-bound0):>+10.6g} d_bnd_prev={(bound_j-prev_bound):>+10.6g}"
            )
            prev_sigs = sigs_j
            prev_bound = bound_j

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")


if __name__ == "__main__":
    main()
