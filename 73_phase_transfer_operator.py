"""
73_phase_transfer_operator.py

Refined transfer operator for the critical phantom return map.

Previous scripts showed:

  - the coarse automaton BULK/E1..E5 is supercritical at s=1;
  - atomic refinement can make the observed sample subcritical;
  - the deep exceptions are not finite, but live in 2-adic phase classes.

This script builds the matrix directly on phase states:

    state = (
        v2(t_crit) bucket,
        odd(t_crit) mod 2^m_odd,
        hit_index mod 2^m_hit
    )

Each critical return row contributes an edge source -> destination with weight

    2^(-s * delta_t_bits).

Terminal hits contribute to the source denominator but produce no outgoing
edge. Therefore a spectral radius < 1 means that the observed refined return
operator is subcritical at exponent s.

This is still empirical: the matrix is built from sampled returns. Its role is
to identify the smallest phase coordinates that make contraction visible.
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
OUT_SCAN = ROOT / "collatz_73_phase_transfer_scan.csv"
OUT_STATES = ROOT / "collatz_73_phase_transfer_states.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_int_csv(path: Path) -> list[dict[str, int]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def finite_v2(v: int, cap: int) -> int:
    if v >= 10**8:
        return cap + 1
    return min(v, cap)


def phase_state(t_v2: int, odd_mod_256: int, hit_index: int, odd_bits: int, hit_bits: int, v2_cap: int) -> tuple[int, int, int]:
    odd_mod = 1 << odd_bits
    hit_mod = 1 << hit_bits
    return (
        finite_v2(t_v2, v2_cap),
        odd_mod_256 % odd_mod,
        hit_index % hit_mod,
    )


def source_state(row: dict[str, int], odd_bits: int, hit_bits: int, v2_cap: int) -> tuple[int, int, int]:
    return phase_state(
        row["from_t_v2"],
        row["from_odd_mod_256"],
        row["hit_index"],
        odd_bits,
        hit_bits,
        v2_cap,
    )


def dest_state(row: dict[str, int], odd_bits: int, hit_bits: int, v2_cap: int) -> tuple[int, int, int]:
    return phase_state(
        row["to_t_v2"],
        row["to_odd_mod_256"],
        row["hit_index"] + 1,
        odd_bits,
        hit_bits,
        v2_cap,
    )


def terminal_state(row: dict[str, int], odd_bits: int, hit_bits: int, v2_cap: int) -> tuple[int, int, int]:
    return phase_state(
        row["t_v2"],
        row["odd_mod_256"],
        row["hit_index"],
        odd_bits,
        hit_bits,
        v2_cap,
    )


def spectral_radius_sparse(matrix: csr_matrix) -> float:
    n = matrix.shape[0]
    if n == 0:
        return 0.0
    if n <= 64:
        vals = np.linalg.eigvals(matrix.toarray())
        return float(max(abs(v) for v in vals)) if vals.size else 0.0
    try:
        vals = eigs(matrix, k=1, which="LM", return_eigenvectors=False, maxiter=20000, tol=1e-10)
        return float(abs(vals[0]))
    except Exception:
        vals = np.linalg.eigvals(matrix.toarray())
        return float(max(abs(v) for v in vals)) if vals.size else 0.0


def build_operator(
    returns: list[dict[str, int]],
    terminals: list[dict[str, int]],
    *,
    odd_bits: int,
    hit_bits: int,
    v2_cap: int,
    s: float,
) -> tuple[csr_matrix, list[tuple[int, int, int]], Counter, Counter, Counter]:
    source_counts: Counter = Counter()
    terminal_counts: Counter = Counter()
    edge_weights: Counter = Counter()

    states = set()
    for row in returns:
        src = source_state(row, odd_bits, hit_bits, v2_cap)
        dst = dest_state(row, odd_bits, hit_bits, v2_cap)
        source_counts[src] += 1
        edge_weights[(src, dst)] += 2.0 ** (-s * row["delta_t_bits"])
        states.add(src)
        states.add(dst)

    for row in terminals:
        src = terminal_state(row, odd_bits, hit_bits, v2_cap)
        source_counts[src] += 1
        terminal_counts[src] += 1
        states.add(src)

    ordered = sorted(states)
    idx = {state: i for i, state in enumerate(ordered)}
    data = []
    row_idx = []
    col_idx = []
    for (src, dst), weight in edge_weights.items():
        denom = source_counts[src]
        if denom == 0:
            continue
        row_idx.append(idx[src])
        col_idx.append(idx[dst])
        data.append(weight / denom)

    matrix = csr_matrix((data, (row_idx, col_idx)), shape=(len(ordered), len(ordered)))
    return matrix, ordered, source_counts, terminal_counts, edge_weights


def run_config(
    returns: list[dict[str, int]],
    terminals: list[dict[str, int]],
    *,
    odd_bits: int,
    hit_bits: int,
    v2_cap: int,
    s: float,
) -> tuple[dict, list[dict]]:
    matrix, states, source_counts, terminal_counts, edge_weights = build_operator(
        returns,
        terminals,
        odd_bits=odd_bits,
        hit_bits=hit_bits,
        v2_cap=v2_cap,
        s=s,
    )
    rho = spectral_radius_sparse(matrix)
    row_sums = np.asarray(matrix.sum(axis=1)).ravel()
    nonzero_rows = int(np.count_nonzero(row_sums))
    max_row_sum = float(row_sums.max()) if row_sums.size else 0.0
    summary = {
        "odd_bits": odd_bits,
        "hit_bits": hit_bits,
        "v2_cap": v2_cap,
        "s": s,
        "state_count": len(states),
        "edge_count": matrix.nnz,
        "nonzero_rows": nonzero_rows,
        "rho": rho,
        "max_row_sum": max_row_sum,
        "total_sources": sum(source_counts.values()),
        "terminal_sources": sum(terminal_counts.values()),
        "terminal_fraction": sum(terminal_counts.values()) / sum(source_counts.values()) if source_counts else 0.0,
    }

    state_rows = []
    for i, state in enumerate(states):
        src = source_counts[state]
        if not src:
            continue
        term = terminal_counts[state]
        state_rows.append({
            "odd_bits": odd_bits,
            "hit_bits": hit_bits,
            "v2_cap": v2_cap,
            "state": f"v2={state[0]}|odd={state[1]}|hit={state[2]}",
            "sources": src,
            "terminals": term,
            "exit_fraction": term / src,
            "row_sum": float(row_sums[i]) if i < len(row_sums) else 0.0,
        })
    state_rows.sort(key=lambda r: (-r["row_sum"], -r["sources"]))
    return summary, state_rows


def generate_returns(args: argparse.Namespace) -> tuple[list[dict[str, int]], list[dict[str, int]]]:
    critical = load_module("62_critical_return_map.py", "critical_return_map")
    critical_args = argparse.Namespace(
        k_min=10,
        k_max=24,
        b_min=1,
        b_max=args.b_max,
        t_max=args.t_max,
        t_mode=args.t_mode,
        max_steps=args.max_steps,
        target_k=12,
        target_cycle=2,
        target_b=1,
    )
    return critical.analyze(critical_args)


def load_returns(args: argparse.Namespace) -> tuple[list[dict[str, int]], list[dict[str, int]]]:
    if args.generate:
        return generate_returns(args)
    return read_int_csv(ROOT / args.returns), read_int_csv(ROOT / args.terminals)


def parse_csv_ints(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Operatore di trasferimento su fase 2-adica.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--terminals", default="collatz_62_critical_terminals.csv")
    parser.add_argument("--generate", action="store_true", help="Rigenera ritorni invece di leggere i CSV canonici.")
    parser.add_argument("--b-max", type=int, default=8)
    parser.add_argument("--t-max", type=int, default=1023)
    parser.add_argument("--t-mode", choices=["dense", "powers"], default="dense")
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--s", type=float, default=1.0)
    parser.add_argument("--odd-bits", default="1,2,3,4,5,6,7,8")
    parser.add_argument("--hit-bits", default="0,1,2,3,4")
    parser.add_argument("--v2-cap", type=int, default=32)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    returns, terminals = load_returns(args)
    odd_values = parse_csv_ints(args.odd_bits)
    hit_values = parse_csv_ints(args.hit_bits)

    scan_rows = []
    best_state_rows = []
    print("=" * 118)
    print("  Phase transfer operator")
    print("=" * 118)
    print(f"  returns:   {len(returns):,}")
    print(f"  terminals: {len(terminals):,}")
    print(f"  s={args.s:g}, v2_cap={args.v2_cap}")
    print(f"\n  {'odd':>4} {'hit':>4} {'states':>8} {'edges':>8} {'rho':>14} {'max row':>12}")

    best = None
    for odd_bits in odd_values:
        for hit_bits in hit_values:
            summary, state_rows = run_config(
                returns,
                terminals,
                odd_bits=odd_bits,
                hit_bits=hit_bits,
                v2_cap=args.v2_cap,
                s=args.s,
            )
            scan_rows.append(summary)
            if best is None or summary["rho"] < best[0]["rho"]:
                best = (summary, state_rows)
            verdict = "*" if summary["rho"] < 1.0 else " "
            print(
                f"{verdict} {odd_bits:>3} {hit_bits:>4} "
                f"{summary['state_count']:>8} {summary['edge_count']:>8} "
                f"{summary['rho']:>14.6g} {summary['max_row_sum']:>12.6g}"
            )

    if best is not None:
        best_summary, best_state_rows = best
        for row in best_state_rows[:200]:
            out = dict(best_summary)
            out.update(row)
            best_state_rows[best_state_rows.index(row)] = out
        print("\n  Miglior configurazione:")
        print(
            f"    odd_bits={best_summary['odd_bits']} hit_bits={best_summary['hit_bits']} "
            f"states={best_summary['state_count']} rho={best_summary['rho']:.6g}"
        )
        print("  Stati peggiori:")
        for row in best[1][:12]:
            print(
                f"    {row['state']:<24} sources={row['sources']:<5} "
                f"term={row['terminals']:<4} row_sum={row['row_sum']:.6g}"
            )

    write_csv(scan_rows, OUT_SCAN)
    if best is not None:
        summary, state_rows = best
        enriched = []
        for row in state_rows[:500]:
            out = {
                "best_odd_bits": summary["odd_bits"],
                "best_hit_bits": summary["hit_bits"],
                "best_v2_cap": summary["v2_cap"],
                "best_rho": summary["rho"],
            }
            out.update(row)
            enriched.append(out)
        write_csv(enriched, OUT_STATES)

    print("\n  Output:")
    print(f"    {OUT_SCAN.name}")
    print(f"    {OUT_STATES.name}")


if __name__ == "__main__":
    main()
