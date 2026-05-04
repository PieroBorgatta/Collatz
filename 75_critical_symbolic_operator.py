"""
75_critical_symbolic_operator.py

Finite modular transfer operator for the critical phantom node.

This is the first bridge from sampled source families to an exact finite
enumeration. We focus only on the critical node:

    target = (k=12, cycle=2, b=1)

For this node, every hit has the form

    n = r + t * 2^(A+1)

where A is the period sum of the phantom word. We enumerate

    t = 0, ..., 2^T - 1

and all phases h mod H. For each pair (t, h), we trace the odd Syracuse map
until either:

  - the orbit drops below the starting n, counted as terminal;
  - it reaches the next distinct hit of the same critical node, producing
    an edge from source phase to destination phase.

The state is:

    (v2(t) capped, odd(t) mod 2^odd_bits, h mod 2^hit_bits)

and the edge weight is:

    2^(-s * delta_t_bits)

This is still not a theorem for all t, but it is an exact matrix for the
finite quotient t mod 2^T. If rho stabilizes below 1 as T grows, the next
task becomes proving periodicity / tail bounds for the quotient limit.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from importlib import util
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parent
OUT_SCAN = ROOT / "collatz_75_critical_symbolic_scan.csv"
OUT_EDGES = ROOT / "collatz_75_critical_symbolic_edges.csv"


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


def v2_int(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    out = 0
    while (n & 1) == 0:
        n >>= 1
        out += 1
    return out


def odd_part_mod(t: int, odd_mod: int) -> int:
    if t == 0:
        return 0
    return (t >> v2_int(t)) % odd_mod


def finite_v2(t: int, cap: int) -> int:
    v = v2_int(t)
    if v >= 10**8:
        return cap + 1
    return min(v, cap)


def state_of(t: int, h: int, odd_bits: int, hit_bits: int, v2_cap: int) -> tuple[int, int, int]:
    return (
        finite_v2(t, v2_cap),
        odd_part_mod(t, 1 << odd_bits),
        h % (1 << hit_bits),
    )


def target_record(records: list[dict], k: int, cycle_id: int) -> dict:
    for rec in records:
        if rec["k"] == k and rec["cycle_id"] == cycle_id:
            return rec
    raise KeyError((k, cycle_id))


def residue_for(record: dict, b: int, shadows=None) -> tuple[int, int, int]:
    if shadows is None:
        shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    bits = b * record["sum_a"] + 1
    modulus = 1 << bits
    residue = shadows.rational_mod_power_of_two(record["q"], bits)
    if residue == 0:
        residue = modulus
    return residue, modulus, bits


def local_t_from_residue(n: int, residue: int, modulus: int) -> int:
    if (n - residue) % modulus != 0:
        raise ValueError("n is not in the target congruence class")
    return (n - residue) // modulus


def best_shadow(n: int, records: list[dict], shadowing) -> tuple[tuple[int, int, int] | None, int]:
    best = None
    best_v = 0
    for rec in records:
        v = shadowing.v2_fraction_difference(n, rec["q"])
        b = (v - 1) // rec["sum_a"]
        if b < 1:
            continue
        key = (rec["k"], rec["cycle_id"], b)
        if best is None or (b, v) > (best[2], best_v):
            best = key
            best_v = v
    return best, best_v


def make_start_from_residue(residue: int, modulus: int, t: int) -> int:
    return residue + t * modulus


def first_return_or_terminal(
    n0: int,
    records: list[dict],
    target: dict,
    target_key: tuple[int, int, int],
    target_residue: int,
    target_modulus: int,
    shadowing,
    max_steps: int,
) -> dict:
    cur = n0
    last_key = target_key

    for step in range(1, max_steps + 1):
        _, cur = shadowing.odd_syracuse_step(cur)
        if cur < n0:
            return {"terminal": 1, "step": step}

        key, _ = best_shadow(cur, records, shadowing)
        if key is None:
            last_key = None
            continue
        if key != last_key:
            if key == target_key:
                return {
                    "terminal": 0,
                    "step": step,
                    "next_t": local_t_from_residue(cur, target_residue, target_modulus),
                }
            last_key = key

    return {"terminal": 1, "step": max_steps, "unresolved": 1}


def spectral_radius(matrix: csr_matrix) -> float:
    n = matrix.shape[0]
    if n == 0:
        return 0.0
    if n <= 64:
        vals = np.linalg.eigvals(matrix.toarray())
        return float(max(abs(v) for v in vals)) if vals.size else 0.0
    vals = eigs(matrix, k=1, which="LM", return_eigenvectors=False, maxiter=20000, tol=1e-10)
    return float(abs(vals[0]))


def build_for_T(
    *,
    T: int,
    odd_bits: int,
    hit_bits: int,
    v2_cap: int,
    s: float,
    max_steps: int,
) -> tuple[dict, list[dict]]:
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = target_record(records, 12, 2)
    target_key = (12, 2, 1)
    target_residue, target_modulus, _ = residue_for(target, 1, shadows)
    h_mod = 1 << hit_bits

    source_counts: Counter = Counter()
    terminal_counts: Counter = Counter()
    edge_weights: Counter = Counter()
    edge_counts: Counter = Counter()
    terminal_steps = []
    return_steps = []
    unresolved = 0

    for t in range(1 << T):
        n0 = make_start_from_residue(target_residue, target_modulus, t)
        t_bits = t.bit_length()
        for h in range(h_mod):
            src = state_of(t, h, odd_bits, hit_bits, v2_cap)
            source_counts[src] += 1
            result = first_return_or_terminal(
                n0,
                records,
                target,
                target_key,
                target_residue,
                target_modulus,
                shadowing,
                max_steps,
            )
            if result.get("terminal"):
                terminal_counts[src] += 1
                terminal_steps.append(result["step"])
                unresolved += int(result.get("unresolved", 0))
                continue
            next_t = result["next_t"]
            dst = state_of(next_t, h + 1, odd_bits, hit_bits, v2_cap)
            delta_t_bits = next_t.bit_length() - t_bits
            weight = 2.0 ** (-s * delta_t_bits)
            edge_weights[(src, dst)] += weight
            edge_counts[(src, dst)] += 1
            return_steps.append(result["step"])

    states = sorted(set(source_counts) | {dst for _, dst in edge_weights})
    idx = {state: i for i, state in enumerate(states)}
    data = []
    rows = []
    cols = []
    for (src, dst), weight in edge_weights.items():
        rows.append(idx[src])
        cols.append(idx[dst])
        data.append(weight / source_counts[src])
    matrix = csr_matrix((data, (rows, cols)), shape=(len(states), len(states)))
    row_sums = np.asarray(matrix.sum(axis=1)).ravel()
    rho = spectral_radius(matrix)

    summary = {
        "T": T,
        "sample_t_count": 1 << T,
        "odd_bits": odd_bits,
        "hit_bits": hit_bits,
        "v2_cap": v2_cap,
        "s": s,
        "state_count": len(states),
        "edge_count": matrix.nnz,
        "total_sources": sum(source_counts.values()),
        "terminal_sources": sum(terminal_counts.values()),
        "terminal_fraction": sum(terminal_counts.values()) / sum(source_counts.values()),
        "unresolved": unresolved,
        "rho": rho,
        "max_row_sum": float(row_sums.max()) if row_sums.size else 0.0,
        "median_terminal_step": int(np.median(terminal_steps)) if terminal_steps else 0,
        "median_return_step": int(np.median(return_steps)) if return_steps else 0,
    }

    edge_rows = []
    for (src, dst), count in edge_counts.most_common(100):
        edge_rows.append({
            "T": T,
            "src": f"v2={src[0]}|odd={src[1]}|h={src[2]}",
            "dst": f"v2={dst[0]}|odd={dst[1]}|h={dst[2]}",
            "count": count,
            "weight_sum": edge_weights[(src, dst)],
            "source_count": source_counts[src],
            "normalized_weight": edge_weights[(src, dst)] / source_counts[src],
        })
    return summary, edge_rows


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Operatore simbolico finito del nodo critico.")
    parser.add_argument("--T", default="8,10,12")
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--s", type=float, default=1.0)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summaries = []
    all_edges = []
    print("=" * 116)
    print("  Critical symbolic operator")
    print("=" * 116)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, s={args.s:g}")
    print(f"  {'T':>4} {'states':>8} {'edges':>8} {'terminal%':>10} {'rho':>14} {'unres':>8}")
    for T in parse_csv_ints(args.T):
        summary, edges = build_for_T(
            T=T,
            odd_bits=args.odd_bits,
            hit_bits=args.hit_bits,
            v2_cap=args.v2_cap,
            s=args.s,
            max_steps=args.max_steps,
        )
        summaries.append(summary)
        all_edges.extend(edges)
        print(
            f"  {T:>4} {summary['state_count']:>8} {summary['edge_count']:>8} "
            f"{summary['terminal_fraction']:>10.4f} {summary['rho']:>14.6g} "
            f"{summary['unresolved']:>8}"
        )

    write_csv(summaries, OUT_SCAN)
    write_csv(all_edges, OUT_EDGES)
    print("\n  Output:")
    print(f"    {OUT_SCAN.name}")
    print(f"    {OUT_EDGES.name}")


if __name__ == "__main__":
    main()
