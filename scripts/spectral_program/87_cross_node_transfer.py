"""
87_cross_node_transfer.py

Cross-node transfer operator on the critical SCC.

Why this script.

    Script 86 measured bound_F at every node of the SCC in isolation:
    each node's own return-to-self matrix is subcritical, with the
    critical node (12, 2, 1) being the worst case (bound_F ~= 0.05).

    But the SCC is held together by transitions BETWEEN nodes, not by
    self-loops. So a single-node certificate is necessary but not
    sufficient: cross-node coupling could amplify the spectrum even when
    each block is contractive.

    This script builds the transfer operator on the union state space

        state = (node_id, v2(t_local), odd(t_local) mod 4, hit_index mod 4)

    where node_id ranges over the user-supplied SCC nodes, t_local is the
    local parameter of that node, and the hit_index counts hits on any
    monitored node.

    For each source state, we enumerate t_local in [0, 2^T), trace
    forward with odd Syracuse, and record the first event:

      - drop below n0 (terminal, no edge);
      - first hit on ANY monitored node, source_node included
        (edge with weight 2^(-delta_bit_length)).

    bound_F is then computed exactly as in 84: with the right Perron
    eigenvector v of FULL, take

        bound_F = max_i (FULL v)_i / v_i.

    No CORE/TAIL split here — the question is just whether the assembled
    cross-node operator stays subcritical.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from importlib import util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "collatz_87_cross_node_transfer.csv"


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
    out = []
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(":")
        if len(parts) != 3:
            raise ValueError(f"bad target {chunk!r}")
        out.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return out


def first_cross_event(
    n0: int,
    records: list[dict],
    target_set: dict,
    shadowing,
    op_mod,
    source_node_key: tuple[int, int, int],
    max_steps: int,
):
    """Trace n0 forward; return first hit on any node in target_set, or
    terminal if drop below n0. target_set maps (k, c, b) -> (residue,
    modulus)."""
    cur = n0
    last_key = source_node_key
    for step in range(1, max_steps + 1):
        _, cur = shadowing.odd_syracuse_step(cur)
        if cur < n0:
            return {"terminal": 1, "step": step}
        key, _ = op_mod.best_shadow(cur, records, shadowing)
        if key is None:
            last_key = None
            continue
        if key != last_key and key in target_set:
            residue, modulus = target_set[key]
            if (cur - residue) % modulus != 0:
                # cur belongs to that node combinatorially but not
                # congruentially at the chosen b: skip and continue.
                last_key = key
                continue
            t_loc = (cur - residue) // modulus
            return {
                "terminal": 0,
                "step": step,
                "dst_node": key,
                "dst_t_local": t_loc,
                "dst_value": cur,
            }
        if key != last_key:
            last_key = key
    return {"terminal": 1, "step": max_steps, "unresolved": 1}


def build_target_set(op_mod, shadows_mod, records, targets: list[tuple[int, int, int]]):
    out = {}
    for k, c, b in targets:
        try:
            target = op_mod.target_record(records, k, c)
            residue, modulus, _ = op_mod.residue_for(target, b, shadows_mod)
        except KeyError:
            continue
        out[(k, c, b)] = (residue, modulus)
    return out


def perron_right_eigvec(M: np.ndarray, n_iter: int = 5000, tol: float = 1e-12, eps: float = 1e-12):
    n = M.shape[0]
    if n == 0:
        return 0.0, np.zeros(0)
    M_pert = M + eps
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Operatore cross-node SCC.")
    parser.add_argument(
        "--targets",
        default="10:1:1,11:1:1,12:1:1,12:2:1,12:2:2",
        help="lista k:c:b separati da virgola",
    )
    parser.add_argument("--T", type=int, default=8)
    parser.add_argument("--j-count", type=int, default=8)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    op_mod = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing_mod = load_module("55_shadowing_congruence.py", "shadowing")
    shadows_mod = load_module("54_phantom_rational_shadows.py", "phantom_shadows")

    records = shadowing_mod.phantom_records(10, 24)
    targets = parse_targets(args.targets)
    target_set = build_target_set(op_mod, shadows_mod, records, targets)

    if not target_set:
        print("  Nessun target valido")
        return

    print("=" * 132)
    print(f"  Cross-node transfer operator  (T={args.T}, j={args.j_count})")
    print("=" * 132)
    print(f"  Nodi monitorati: {sorted(target_set)}")

    # Enumerate all source (node, t, h) and build edges.
    h_mod = 1 << args.hit_bits
    states_set = set()
    edges = Counter()
    source_counts = Counter()
    terminal_counts = Counter()
    cross_edge_counts = Counter()  # node -> node
    unresolved = 0

    for src_node, (residue, modulus) in target_set.items():
        for r in range(1 << args.T):
            for h in range(h_mod):
                for j in range(args.j_count):
                    t = r + (j << args.T)
                    n0 = residue + t * modulus
                    src_phase = op_mod.state_of(t, h, args.odd_bits, args.hit_bits, args.v2_cap)
                    src = (src_node, src_phase)
                    source_counts[src] += 1
                    states_set.add(src)

                    res = first_cross_event(
                        n0, records, target_set, shadowing_mod, op_mod,
                        src_node, args.max_steps,
                    )
                    if res.get("terminal"):
                        terminal_counts[src] += 1
                        unresolved += int(res.get("unresolved", 0))
                        continue
                    dst_node = res["dst_node"]
                    dst_t = res["dst_t_local"]
                    dst_phase = op_mod.state_of(
                        dst_t, h + 1, args.odd_bits, args.hit_bits, args.v2_cap
                    )
                    dst = (dst_node, dst_phase)
                    states_set.add(dst)

                    # Weight uses bit_length to be node-invariant.
                    delta_bits = res["dst_value"].bit_length() - n0.bit_length()
                    weight = 2.0 ** (-delta_bits)
                    edges[(src, dst)] += weight
                    cross_edge_counts[(src_node, dst_node)] += 1

    states = sorted(states_set, key=lambda s: (s[0], s[1]))
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    print(f"  Stati totali: {n}")
    print(f"  Sorgenti totali: {sum(source_counts.values())}")
    print(f"  Terminali: {sum(terminal_counts.values())}  ({sum(terminal_counts.values())/max(1,sum(source_counts.values())):.4f})")
    print(f"  Unresolved: {unresolved}")
    print()
    print("  Edge cross-node aggregate:")
    for (a, b), c in sorted(cross_edge_counts.items()):
        marker = "  (self)" if a == b else ""
        print(f"    {a} -> {b}: {c:>6}{marker}")

    M = np.zeros((n, n))
    for (src, dst), w in edges.items():
        denom = source_counts[src]
        if denom == 0:
            continue
        M[idx[src], idx[dst]] += w / denom

    rho, v = perron_right_eigvec(M)
    eps = max(1e-10, 1e-6 * v.max())
    Mv = M @ v
    mask = v > eps
    bound_F = float((Mv[mask] / v[mask]).max()) if mask.any() else 0.0

    print()
    print(f"  rho(M_cross)   = {rho:.6g}")
    print(f"  bound_F(cross) = {bound_F:.6g}")
    print(f"  status         = {'OK' if bound_F < 1.0 else 'FAIL'}")

    # Write per-node summary.
    out_rows = []
    for node, (residue, modulus) in target_set.items():
        node_states = [s for s in states if s[0] == node]
        node_idx = [idx[s] for s in node_states]
        if not node_idx:
            continue
        node_v = v[node_idx]
        node_v_max = float(node_v.max()) if node_v.size else 0.0
        node_v_sum = float(node_v.sum())
        out_rows.append({
            "node": f"{node[0]}:{node[1]}:{node[2]}",
            "states": len(node_states),
            "v_max_share": node_v_max,
            "v_sum_share": node_v_sum,
        })

    print()
    print("  Massa dell'autovettore di Perron per nodo:")
    for r in out_rows:
        print(f"    {r['node']}: states={r['states']:>3}, v_max={r['v_max_share']:.4f}, v_sum={r['v_sum_share']:.4f}")

    summary_row = {
        "node": "__SUMMARY__",
        "states": n,
        "v_max_share": rho,
        "v_sum_share": bound_F,
    }
    write_csv([summary_row] + out_rows, OUT)
    print()
    print(f"  Output: {OUT.name}")


if __name__ == "__main__":
    main()
