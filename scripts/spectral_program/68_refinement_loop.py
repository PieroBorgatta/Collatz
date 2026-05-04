"""
68_refinement_loop.py

Loop automatico di raffinamento dell'automa critico.

Strategia:
  1. parti dai blocchi base BULK/E1..E5;
  2. calcola la matrice pesata normalizzata e rho;
  3. trova la singola riga di ritorno con contributo massimo;
  4. crea un nuovo blocco atomico che isola quella firma;
  5. ripeti.

La firma atomica usata qui e':

    source_k, source_cycle_id, source_b, source_t, hit_index,
    from_t_v2, from_odd_mod_256, delta_t_bits

Questo non e' ancora un certificato teorico generale: e' un test di
terminazione del raffinamento empirico. Se rho scende sotto 1 dopo pochi
atomi, la pressione e' dominata da eccezioni finite. Se non scende, stiamo
vedendo una famiglia infinita da descrivere simbolicamente.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter

import numpy as np


def read_csv_int(path: str) -> list[dict[str, int]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def base_classify(t_v2: int, odd_mod: int, hit_index: int) -> str:
    if t_v2 == 20:
        return "E1_v2_20"
    if odd_mod & 3 == 1:
        return "E2_odd_mod4_1"
    if odd_mod & 7 == 3:
        return "E3_odd_mod8_3"
    if hit_index == 7:
        return "E4_hit_7"
    if t_v2 == 21:
        return "E5_v2_21"
    return "BULK"


def row_signature(row: dict[str, int]) -> tuple[int, ...]:
    return (
        row["source_k"],
        row["source_cycle_id"],
        row["source_b"],
        row["source_t"],
        row["hit_index"],
        row["from_t_v2"],
        row["from_odd_mod_256"],
        row["delta_t_bits"],
    )


def source_block(row: dict[str, int], atoms: dict[tuple[int, ...], str]) -> str:
    sig = row_signature(row)
    if sig in atoms:
        return atoms[sig]
    return base_classify(row["from_t_v2"], row["from_odd_mod_256"], row["hit_index"])


def dest_block(row: dict[str, int], atoms: dict[tuple[int, ...], str]) -> str:
    # Destination is the next critical hit. We do not know the full row signature
    # of that next hit here, so destination uses base block. This is conservative
    # for finding source atoms; next iteration can isolate that hit as source.
    return base_classify(row["to_t_v2"], row["to_odd_mod_256"], row["hit_index"] + 1)


def terminal_block(row: dict[str, int]) -> str:
    return base_classify(row["t_v2"], row["odd_mod_256"], row["hit_index"])


def all_blocks(returns: list[dict[str, int]], terminals: list[dict[str, int]], atoms: dict[tuple[int, ...], str]) -> list[str]:
    blocks = set(atoms.values())
    for row in returns:
        blocks.add(source_block(row, atoms))
        blocks.add(dest_block(row, atoms))
    for row in terminals:
        blocks.add(terminal_block(row))
    return sorted(blocks, key=lambda b: (not b.startswith("BULK"), b))


def build_matrix(returns: list[dict[str, int]], terminals: list[dict[str, int]], atoms: dict[tuple[int, ...], str], s: float):
    blocks = all_blocks(returns, terminals, atoms)
    idx = {b: i for i, b in enumerate(blocks)}
    weighted = np.zeros((len(blocks), len(blocks)), dtype=float)
    source_counts = Counter()
    terminal_counts = Counter()

    for row in returns:
        src = source_block(row, atoms)
        dst = dest_block(row, atoms)
        source_counts[src] += 1
        weighted[idx[src], idx[dst]] += 2.0 ** (-s * row["delta_t_bits"])

    for row in terminals:
        block = terminal_block(row)
        source_counts[block] += 1
        terminal_counts[block] += 1

    M = np.zeros_like(weighted)
    for block in blocks:
        denom = source_counts[block]
        if denom:
            M[idx[block], :] = weighted[idx[block], :] / denom

    return blocks, M, source_counts, terminal_counts, weighted


def spectral_radius(M: np.ndarray) -> float:
    vals = np.linalg.eigvals(M)
    return float(max(abs(v) for v in vals)) if vals.size else 0.0


def heaviest_unisolated_row(returns: list[dict[str, int]], atoms: dict[tuple[int, ...], str], s: float) -> dict[str, int] | None:
    candidates = []
    for row in returns:
        sig = row_signature(row)
        if sig in atoms:
            continue
        weight = 2.0 ** (-s * row["delta_t_bits"])
        candidates.append((weight, row))
    if not candidates:
        return None
    return max(candidates, key=lambda x: x[0])[1]


def block_pressure_rows(blocks, M, source_counts, terminal_counts) -> list[dict]:
    out = []
    for i, block in enumerate(blocks):
        out.append({
            "block": block,
            "sources": source_counts[block],
            "terminals": terminal_counts[block],
            "row_sum": float(M[i, :].sum()),
            "exit_fraction": terminal_counts[block] / source_counts[block] if source_counts[block] else 0.0,
        })
    out.sort(key=lambda r: -r["row_sum"])
    return out


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def run_loop(returns: list[dict[str, int]], terminals: list[dict[str, int]], s: float, max_iters: int) -> tuple[list[dict], list[dict], dict]:
    atoms: dict[tuple[int, ...], str] = {}
    history = []

    for it in range(max_iters + 1):
        blocks, M, source_counts, terminal_counts, weighted = build_matrix(returns, terminals, atoms, s)
        rho = spectral_radius(M)
        top_blocks = block_pressure_rows(blocks, M, source_counts, terminal_counts)
        history.append({
            "iteration": it,
            "atom_count": len(atoms),
            "block_count": len(blocks),
            "rho": rho,
            "top_block": top_blocks[0]["block"] if top_blocks else "",
            "top_row_sum": top_blocks[0]["row_sum"] if top_blocks else 0.0,
            "top_sources": top_blocks[0]["sources"] if top_blocks else 0,
        })
        if rho < 1.0:
            break
        row = heaviest_unisolated_row(returns, atoms, s)
        if row is None:
            break
        atom_name = f"A{len(atoms)+1}_d{row['delta_t_bits']}_b{row['source_b']}_t{row['source_t']}_h{row['hit_index']}"
        atoms[row_signature(row)] = atom_name

    atom_rows = []
    for sig, name in atoms.items():
        atom_rows.append({
            "atom": name,
            "source_k": sig[0],
            "source_cycle_id": sig[1],
            "source_b": sig[2],
            "source_t": sig[3],
            "hit_index": sig[4],
            "from_t_v2": sig[5],
            "from_odd_mod_256": sig[6],
            "delta_t_bits": sig[7],
        })
    return history, atom_rows, atoms


def print_summary(history: list[dict], atom_rows: list[dict]) -> None:
    print("=" * 112)
    print("  Refinement loop atomico")
    print("=" * 112)
    print(f"  {'it':>4} {'atoms':>6} {'blocks':>7} {'rho':>14} {'top block':<24} {'row sum':>12} {'sources':>8}")
    for row in history:
        print(f"  {row['iteration']:>4} {row['atom_count']:>6} {row['block_count']:>7} "
              f"{row['rho']:>14.6g} {row['top_block']:<24} "
              f"{row['top_row_sum']:>12.6g} {row['top_sources']:>8}")
    print("\n  Atomi creati:")
    for row in atom_rows[:30]:
        print(f"    {row['atom']}: b={row['source_b']} t={row['source_t']} "
              f"hit={row['hit_index']} v2={row['from_t_v2']} "
              f"odd256={row['from_odd_mod_256']} delta={row['delta_t_bits']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Loop automatico di raffinamento atomico.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--terminals", default="collatz_62_critical_terminals.csv")
    parser.add_argument("--s", type=float, default=1.0)
    parser.add_argument("--max-iters", type=int, default=40)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    returns = []
    terminals = []
    with open(args.returns, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            returns.append({k: int(v) for k, v in row.items()})
    with open(args.terminals, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            terminals.append({k: int(v) for k, v in row.items()})

    history, atom_rows, atoms = run_loop(returns, terminals, args.s, args.max_iters)
    write_csv(history, "collatz_68_refinement_history.csv")
    write_csv(atom_rows, "collatz_68_refinement_atoms.csv")
    print_summary(history, atom_rows)
    print("\n  Output:")
    print("    collatz_68_refinement_history.csv")
    print("    collatz_68_refinement_atoms.csv")


if __name__ == "__main__":
    main()
