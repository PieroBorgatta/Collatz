"""
77_high_bit_tail_bound.py

Empirical high-bit tail decomposition for the critical return operator.

The quotient consistency probe showed that the transition is not determined
only by t mod 2^T. This script separates the lifted sample

    t = r + j * 2^T

into:

  CORE: the majority transition signature for each pair (r, h mod 4);
  TAIL: all minority signatures, i.e. the high-bit-dependent residue.

For each T and number of lifts j_count, it builds three normalized transfer
matrices on the phase state

    (v2(t), odd(t) mod 4, h mod 4)

with weights 2^(-delta_t_bits):

  FULL = CORE + TAIL

and reports:

  rho(FULL), rho(CORE), rho(TAIL), ||TAIL||_inf, rho(CORE)+||TAIL||_inf.

If the last quantity is < 1, then the observed high-bit tail is small enough
to certify contraction by the elementary perturbation bound:

    rho(CORE + TAIL) <= rho(CORE) + ||TAIL||.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parent
OUT_SUMMARY = ROOT / "collatz_77_high_bit_tail_summary.csv"
OUT_ROWS = ROOT / "collatz_77_high_bit_tail_rows.csv"


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


def spectral_radius(matrix: csr_matrix) -> float:
    n = matrix.shape[0]
    if n == 0 or matrix.nnz == 0:
        return 0.0
    if n <= 64:
        vals = np.linalg.eigvals(matrix.toarray())
        return float(max(abs(v) for v in vals)) if vals.size else 0.0
    vals = eigs(matrix, k=1, which="LM", return_eigenvectors=False, maxiter=20000, tol=1e-10)
    return float(abs(vals[0]))


def matrix_inf_norm(matrix: csr_matrix) -> float:
    if matrix.shape[0] == 0:
        return 0.0
    row_sums = np.asarray(abs(matrix).sum(axis=1)).ravel()
    return float(row_sums.max()) if row_sums.size else 0.0


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, _ = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target, target_key, residue, modulus


def trace_row(
    *,
    op,
    shadowing,
    records,
    target,
    target_key,
    residue: int,
    modulus: int,
    t: int,
    h: int,
    odd_bits: int,
    hit_bits: int,
    v2_cap: int,
    max_steps: int,
) -> dict:
    n0 = op.make_start_from_residue(residue, modulus, t)
    src = op.state_of(t, h, odd_bits, hit_bits, v2_cap)
    result = op.first_return_or_terminal(
        n0,
        records,
        target,
        target_key,
        residue,
        modulus,
        shadowing,
        max_steps,
    )
    if result.get("terminal"):
        return {
            "terminal": 1,
            "src": src,
            "dst": None,
            "delta": None,
            "weight": 0.0,
            "signature": ("terminal",),
        }
    next_t = result["next_t"]
    dst = op.state_of(next_t, h + 1, odd_bits, hit_bits, v2_cap)
    delta = next_t.bit_length() - t.bit_length()
    weight = 2.0 ** (-delta)
    return {
        "terminal": 0,
        "src": src,
        "dst": dst,
        "delta": delta,
        "weight": weight,
        "signature": ("return", dst[0], dst[1], dst[2], delta),
    }


def build_matrices(rows: list[dict], states: list[tuple[int, int, int]], source_counts: Counter):
    idx = {state: i for i, state in enumerate(states)}
    buckets = {
        "full": Counter(),
        "core": Counter(),
        "tail": Counter(),
    }
    for row in rows:
        if row["terminal"]:
            continue
        key = (row["src"], row["dst"])
        buckets["full"][key] += row["weight"]
        buckets[row["part"]][key] += row["weight"]

    matrices = {}
    for name, weights in buckets.items():
        data = []
        rr = []
        cc = []
        for (src, dst), weight in weights.items():
            denom = source_counts[src]
            if denom == 0:
                continue
            rr.append(idx[src])
            cc.append(idx[dst])
            data.append(weight / denom)
        matrices[name] = csr_matrix((data, (rr, cc)), shape=(len(states), len(states)))
    return matrices


def analyze_T(args: argparse.Namespace, T: int) -> tuple[dict, list[dict]]:
    op, shadowing, records, target, target_key, residue, modulus = setup()
    h_mod = 1 << args.hit_bits
    source_counts = Counter()
    all_rows = []
    groups = defaultdict(list)

    for r in range(1 << T):
        for h in range(h_mod):
            group_key = (r, h)
            for j in range(args.j_count):
                t = r + (j << T)
                row = trace_row(
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
                row.update({"T": T, "r": r, "h": h, "j": j, "t": t})
                source_counts[row["src"]] += 1
                all_rows.append(row)
                groups[group_key].append(row)

    stable_groups = 0
    tail_events = 0
    tail_weight = 0.0
    full_weight = 0.0
    diagnostic_rows = []

    for (r, h), group_rows in groups.items():
        counts = Counter(row["signature"] for row in group_rows)
        core_sig, core_count = counts.most_common(1)[0]
        if len(counts) == 1:
            stable_groups += 1
        for row in group_rows:
            row["part"] = "core" if row["signature"] == core_sig else "tail"
            if not row["terminal"]:
                full_weight += row["weight"]
                if row["part"] == "tail":
                    tail_weight += row["weight"]
                    tail_events += 1
        if len(counts) > 1 and len(diagnostic_rows) < args.keep_rows:
            diagnostic_rows.append({
                "T": T,
                "r": r,
                "h": h,
                "distinct_signatures": len(counts),
                "core_count": core_count,
                "tail_count": len(group_rows) - core_count,
                "signatures": " | ".join(f"{sig}:{count}" for sig, count in counts.most_common()),
            })

    states = sorted(set(source_counts) | {row["dst"] for row in all_rows if row["dst"] is not None})
    matrices = build_matrices(all_rows, states, source_counts)
    rho_full = spectral_radius(matrices["full"])
    rho_core = spectral_radius(matrices["core"])
    rho_tail = spectral_radius(matrices["tail"])
    tail_inf = matrix_inf_norm(matrices["tail"])
    core_inf = matrix_inf_norm(matrices["core"])
    full_inf = matrix_inf_norm(matrices["full"])

    total_groups = len(groups)
    summary = {
        "T": T,
        "j_count": args.j_count,
        "odd_bits": args.odd_bits,
        "hit_bits": args.hit_bits,
        "state_count": len(states),
        "total_groups": total_groups,
        "stable_groups": stable_groups,
        "stable_fraction": stable_groups / total_groups if total_groups else 0.0,
        "total_observations": len(all_rows),
        "terminal_observations": sum(1 for row in all_rows if row["terminal"]),
        "terminal_fraction": sum(1 for row in all_rows if row["terminal"]) / len(all_rows),
        "tail_events": tail_events,
        "tail_event_fraction": tail_events / len(all_rows),
        "full_weight": full_weight,
        "tail_weight": tail_weight,
        "tail_weight_fraction": tail_weight / full_weight if full_weight else 0.0,
        "rho_full": rho_full,
        "rho_core": rho_core,
        "rho_tail": rho_tail,
        "norm_inf_full": full_inf,
        "norm_inf_core": core_inf,
        "norm_inf_tail": tail_inf,
        "rho_core_plus_tail_inf": rho_core + tail_inf,
    }
    return summary, diagnostic_rows


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Decompone core/tail dei bit alti.")
    parser.add_argument("--T", default="6,8,10")
    parser.add_argument("--j-count", type=int, default=8)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--keep-rows", type=int, default=200)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summaries = []
    diagnostic_rows = []
    print("=" * 122)
    print("  High-bit tail bound")
    print("=" * 122)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, j_count={args.j_count}")
    print(f"  {'T':>4} {'stable%':>9} {'tail ev%':>9} {'rho full':>12} {'rho core':>12} {'tail inf':>12} {'bound':>12}")
    for T in parse_csv_ints(args.T):
        summary, rows = analyze_T(args, T)
        summaries.append(summary)
        diagnostic_rows.extend(rows)
        print(
            f"  {T:>4} {summary['stable_fraction']:>9.4f} "
            f"{summary['tail_event_fraction']:>9.4f} "
            f"{summary['rho_full']:>12.6g} {summary['rho_core']:>12.6g} "
            f"{summary['norm_inf_tail']:>12.6g} "
            f"{summary['rho_core_plus_tail_inf']:>12.6g}"
        )

    write_csv(summaries, OUT_SUMMARY)
    write_csv(diagnostic_rows, OUT_ROWS)
    print("\n  Output:")
    print(f"    {OUT_SUMMARY.name}")
    print(f"    {OUT_ROWS.name}")


if __name__ == "__main__":
    main()
