#!/usr/bin/env python3
"""
Export exact high-bit majority core/tail transfer edges.

This is a Lean-facing companion to
``scripts/spectral_program/77_high_bit_tail_bound.py``.  It uses the same
majority-signature split for each lifted group ``(r, h)`` but writes exact
rational weights instead of floating-point summaries.
"""

from __future__ import annotations

import argparse
import csv
import sys
import types
from collections import Counter, defaultdict
from fractions import Fraction
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "spectral_program"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "high_bit_tail_edges_T10_j32.csv"


def install_spectral_dependency_stubs() -> None:
    """Allow importing legacy spectral scripts without numpy/scipy installed."""
    try:
        __import__("numpy")
    except ModuleNotFoundError:
        sys.modules.setdefault("numpy", types.ModuleType("numpy"))
    scipy = sys.modules.setdefault("scipy", types.ModuleType("scipy"))
    sparse = sys.modules.setdefault("scipy.sparse", types.ModuleType("scipy.sparse"))
    sparse_linalg = sys.modules.setdefault("scipy.sparse.linalg", types.ModuleType("scipy.sparse.linalg"))
    setattr(sparse, "csr_matrix", object)
    setattr(sparse_linalg, "eigs", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("scipy stub")))
    setattr(scipy, "sparse", sparse)


def load_module(filename: str, name: str):
    install_spectral_dependency_stubs()
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, _ = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target, target_key, residue, modulus


def weight_of_delta(delta: int) -> Fraction:
    if delta >= 0:
        return Fraction(1, 2**delta)
    return Fraction(2 ** (-delta), 1)


def trace_row(ctx, args: argparse.Namespace, r: int, h: int, j: int) -> dict:
    op, shadowing, records, target, target_key, residue, modulus = ctx
    t = r + (j << args.T)
    n0 = op.make_start_from_residue(residue, modulus, t)
    src = op.state_of(t, h, args.odd_bits, args.hit_bits, args.v2_cap)
    result = op.first_return_or_terminal(
        n0,
        records,
        target,
        target_key,
        residue,
        modulus,
        shadowing,
        args.max_steps,
    )
    if result.get("terminal"):
        return {
            "terminal": 1,
            "src": src,
            "dst": None,
            "delta": None,
            "weight": Fraction(0, 1),
            "signature": ("terminal",),
        }
    next_t = result["next_t"]
    dst = op.state_of(next_t, h + 1, args.odd_bits, args.hit_bits, args.v2_cap)
    delta = next_t.bit_length() - t.bit_length()
    return {
        "terminal": 0,
        "src": src,
        "dst": dst,
        "delta": delta,
        "weight": weight_of_delta(delta),
        "signature": ("return", dst[0], dst[1], dst[2], delta),
    }


def fmt_state(state: tuple[int, int, int]) -> str:
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def add_weight(
    buckets: dict[str, Counter],
    graph: str,
    src: tuple[int, int, int],
    dst: tuple[int, int, int],
    weight: Fraction,
) -> None:
    buckets[graph][(src, dst)] += weight


def export_edges(args: argparse.Namespace) -> list[dict]:
    ctx = setup()
    h_mod = 1 << args.hit_bits
    source_counts: Counter = Counter()
    buckets = {"full": Counter(), "core": Counter(), "tail": Counter()}
    edge_counts = {"full": Counter(), "core": Counter(), "tail": Counter()}

    for r in range(1 << args.T):
        for h in range(h_mod):
            group_rows = [trace_row(ctx, args, r, h, j) for j in range(args.j_count)]
            counts = Counter(row["signature"] for row in group_rows)
            core_sig, _core_count = counts.most_common(1)[0]
            for row in group_rows:
                src = row["src"]
                source_counts[src] += 1
                if row["terminal"]:
                    continue
                dst = row["dst"]
                assert dst is not None
                part = "core" if row["signature"] == core_sig else "tail"
                add_weight(buckets, "full", src, dst, row["weight"])
                add_weight(buckets, part, src, dst, row["weight"])
                edge_counts["full"][(src, dst)] += 1
                edge_counts[part][(src, dst)] += 1

    rows = []
    for graph in ("full", "core", "tail"):
        for (src, dst), weight in sorted(buckets[graph].items()):
            source_count = source_counts[src]
            normalized = weight / source_count
            rows.append(
                {
                    "T": args.T,
                    "j_count": args.j_count,
                    "odd_bits": args.odd_bits,
                    "hit_bits": args.hit_bits,
                    "v2_cap": args.v2_cap,
                    "graph": graph,
                    "src": fmt_state(src),
                    "dst": fmt_state(dst),
                    "count": edge_counts[graph][(src, dst)],
                    "weight_num": weight.numerator,
                    "weight_den": weight.denominator,
                    "source_count": source_count,
                    "normalized_num": normalized.numerator,
                    "normalized_den": normalized.denominator,
                }
            )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, default=10)
    parser.add_argument("--j-count", type=int, default=32)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=10)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = export_edges(args)
    write_csv(rows, args.output)
    print(f"wrote {len(rows)} edge rows to {args.output}")


if __name__ == "__main__":
    main()
