"""
86_scc_node_certificates.py

Compute the weighted perturbative bound (bound_F from script 84) at every
node of the critical SCC, not just (k=12, cycle=2, b=1).

Why this script.

    The bound_F certificate so far has been computed only for the critical
    node (k=12, c=2, b=1). The SCC found in 60_episode_graph_diagnostics
    contains many other nodes:

        (10, 1, b) for b = 1..15
        (11, 1, b) for b = 1..15
        (12, 1, b) for b = 1..2
        (12, 2, b) for b = 1..2

    For the lemma to certify the entire SCC and not just the single
    representative node, we need bound_F to stay uniformly small at every
    node we test.

How.

    Scripts 75/77/84 hardcode the target as (12, 2, 1). This script takes
    a list of (k, c, b) triples and reuses 77's per-cell engine after
    monkey-patching its setup() to point at the requested node. It reports
    bound_F for each node at fixed (T, j_count) and prints a uniformity
    table.
"""

from __future__ import annotations

import argparse
import csv
from importlib import util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_86_scc_node_certificates.csv"


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


def parse_targets(text: str) -> list[tuple[int, int, int]]:
    """Parse a list of k:c:b triples separated by commas."""
    out = []
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(":")
        if len(parts) != 3:
            raise ValueError(f"bad target {chunk!r}; expected k:c:b")
        out.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return out


def make_setup_for_node(op_mod, shadowing_mod, shadows_mod, records, k: int, c: int, b: int):
    target = op_mod.target_record(records, k, c)
    target_key = (k, c, b)
    residue, modulus, _ = op_mod.residue_for(target, b, shadows_mod)

    def setup():
        return (op_mod, shadowing_mod, records, target, target_key, residue, modulus)

    return setup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="bound_F per ogni nodo SCC critica.")
    parser.add_argument(
        "--targets",
        default="10:1:1,10:1:2,11:1:1,11:1:2,12:1:1,12:2:1,12:2:2",
        help="lista k:c:b separati da virgola",
    )
    parser.add_argument("--T", type=int, default=10)
    parser.add_argument("--j-count", type=int, default=32)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Modules for shared state.
    op_mod = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing_mod = load_module("55_shadowing_congruence.py", "shadowing")
    shadows_mod = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    bound_mod = load_module("84_weighted_perturbation_bound.py", "weighted_bound")

    records = shadowing_mod.phantom_records(10, 24)
    targets = parse_targets(args.targets)

    rows = []
    print("=" * 142)
    print(f"  bound_F per ogni nodo della SCC critica  (T={args.T}, j={args.j_count})")
    print("=" * 142)
    header = (
        f"  {'k':>3} {'c':>2} {'b':>2} {'states':>7} "
        f"{'rho_full':>11} {'core_act':>11} {'tail_act':>11} {'bound_F':>11} "
        f"{'status':>10}"
    )
    print(header)
    print("-" * len(header))

    cell_args = argparse.Namespace(
        odd_bits=args.odd_bits,
        hit_bits=args.hit_bits,
        v2_cap=args.v2_cap,
        max_steps=args.max_steps,
    )

    for k, c, b in targets:
        try:
            new_setup = make_setup_for_node(op_mod, shadowing_mod, shadows_mod, records, k, c, b)
        except KeyError:
            print(f"  {k:>3} {c:>2} {b:>2}   skipped: no record for (k={k}, c={c})")
            continue

        # Monkey-patch 77.setup so trace_block uses this node.
        orig_setup = tail_mod.setup
        tail_mod.setup = new_setup
        try:
            states, _, FULL, CORE, TAIL, _ = make_block(tail_mod, args.T, args.j_count, cell_args)
        finally:
            tail_mod.setup = orig_setup

        if FULL.shape[0] == 0:
            row = {
                "k": k, "c": c, "b": b,
                "states": 0, "rho_full": 0.0, "core_action": 0.0,
                "tail_action": 0.0, "bound_F": 0.0, "status": "empty",
            }
            rows.append(row)
            print(f"  {k:>3} {c:>2} {b:>2} {0:>7}    (empty operator)")
            continue

        rho_full, v_full = bound_mod.perron_right_eigvec(FULL)
        eps = max(1e-10, 1e-6 * v_full.max())
        Fv = FULL @ v_full
        Cv = CORE @ v_full
        Tv = TAIL @ v_full
        mask = v_full > eps
        if mask.any():
            full_act = float((Fv[mask] / v_full[mask]).max())
            core_act = float((Cv[mask] / v_full[mask]).max())
            tail_act = float((Tv[mask] / v_full[mask]).max())
        else:
            full_act = core_act = tail_act = 0.0
        bound_F = core_act + tail_act
        status = "OK" if bound_F < 1.0 else "FAIL"

        row = {
            "k": k, "c": c, "b": b,
            "states": len(states),
            "rho_full": rho_full,
            "core_action": core_act,
            "tail_action": tail_act,
            "bound_F": bound_F,
            "status": status,
        }
        rows.append(row)
        print(
            f"  {k:>3} {c:>2} {b:>2} {len(states):>7} "
            f"{rho_full:>11.6g} {core_act:>11.6g} {tail_act:>11.6g} {bound_F:>11.6g} "
            f"{status:>10}"
        )

    write_csv(rows, OUT)
    print("\n  Output:")
    print(f"    {OUT.name}")

    if rows:
        bounds = [r["bound_F"] for r in rows if r["status"] == "OK"]
        if bounds:
            print(f"\n  Riepilogo nodi OK:")
            print(f"    max bound_F  = {max(bounds):.6g}")
            print(f"    min bound_F  = {min(bounds):.6g}")
            print(f"    mean bound_F = {sum(bounds)/len(bounds):.6g}")
        fails = [r for r in rows if r["status"] != "OK" and r["status"] != "empty"]
        if fails:
            print(f"  Nodi FAIL ({len(fails)}):")
            for r in fails:
                print(f"    (k={r['k']}, c={r['c']}, b={r['b']}): bound_F = {r['bound_F']:.6g}")


def make_block(tail_mod, T: int, j_count: int, cell_args):
    """Inline copy of 84.matrices_for_cell to also return state list."""
    from collections import Counter, defaultdict
    op, shadowing, records, target, target_key, residue, modulus = tail_mod.setup()
    h_mod = 1 << cell_args.hit_bits
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
                    odd_bits=cell_args.odd_bits,
                    hit_bits=cell_args.hit_bits,
                    v2_cap=cell_args.v2_cap,
                    max_steps=cell_args.max_steps,
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
    return states, idx, FULL, CORE, TAIL, None


if __name__ == "__main__":
    main()
