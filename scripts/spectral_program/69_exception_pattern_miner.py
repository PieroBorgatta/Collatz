"""
69_exception_pattern_miner.py

Mine symbolic patterns behind the atomic exceptions found by
68_refinement_loop.py.

The goal is not to prove anything yet. The goal is to test whether the
31 atomic splits that made the empirical automaton subcritical are just
memorized rows, or whether they cluster into compact 2-adic rules:

  - congruences source_t mod 2^m;
  - congruences from_odd_mod_256 mod 2^m;
  - equalities and thresholds on b, hit_index, v2(t);
  - simple relations such as hit_index = source_b - c.

For every candidate rule we report:

  atom coverage    how many of the known atoms it catches;
  row coverage     how many return rows it catches;
  weight coverage  sum(2^-delta_t_bits) of caught atoms/rows at s=1;
  precision        atom_weight / row_weight.

High atom coverage with non-tiny precision is the signal we want: it means
there may be a general exception family rather than isolated accidents.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent
RETURNS_PATH = ROOT / "collatz_62_critical_returns.csv"
ATOMS_PATH = ROOT / "collatz_68_refinement_atoms.csv"
OUT_UNARY = ROOT / "collatz_69_exception_unary_rules.csv"
OUT_COMBO = ROOT / "collatz_69_exception_combo_rules.csv"
OUT_COVER = ROOT / "collatz_69_exception_greedy_cover.csv"


Row = dict[str, int]
Predicate = Callable[[Row], bool]


@dataclass(frozen=True)
class Rule:
    name: str
    pred: Predicate
    atom_ids: frozenset[int]
    row_ids: frozenset[int]
    atom_weight: float
    row_weight: float

    @property
    def atom_count(self) -> int:
        return len(self.atom_ids)

    @property
    def row_count(self) -> int:
        return len(self.row_ids)

    @property
    def precision_weight(self) -> float:
        return self.atom_weight / self.row_weight if self.row_weight else 0.0

    @property
    def selectivity(self) -> float:
        return self.atom_count / self.row_count if self.row_count else 0.0

    def to_row(self) -> dict[str, object]:
        return {
            "rule": self.name,
            "atom_count": self.atom_count,
            "row_count": self.row_count,
            "atom_weight_s1": self.atom_weight,
            "row_weight_s1": self.row_weight,
            "precision_weight": self.precision_weight,
            "selectivity_count": self.selectivity,
            "covered_atoms": ",".join(str(i + 1) for i in sorted(self.atom_ids)),
        }


def read_int_csv(path: Path) -> list[Row]:
    with path.open(encoding="utf-8") as f:
        rows = []
        for row in csv.DictReader(f, delimiter=";"):
            out = {}
            for k, v in row.items():
                try:
                    out[k] = int(v)
                except ValueError:
                    continue
            rows.append(out)
        return rows


def atom_signature(row: Row) -> tuple[int, ...]:
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


def return_signature(row: Row) -> tuple[int, ...]:
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


def weight_s1(row: Row) -> float:
    return 2.0 ** (-row["delta_t_bits"])


def evaluate_rule(
    name: str,
    pred: Predicate,
    returns: list[Row],
    atom_index_by_return: dict[int, int],
) -> Rule | None:
    atom_ids = set()
    row_ids = set()
    atom_weight = 0.0
    row_weight = 0.0
    for i, row in enumerate(returns):
        if not pred(row):
            continue
        w = weight_s1(row)
        row_ids.add(i)
        row_weight += w
        if i in atom_index_by_return:
            atom_ids.add(atom_index_by_return[i])
            atom_weight += w
    if not atom_ids:
        return None
    return Rule(name, pred, frozenset(atom_ids), frozenset(row_ids), atom_weight, row_weight)


def make_unary_specs(returns: list[Row]) -> list[tuple[str, Predicate]]:
    specs: list[tuple[str, Predicate]] = []

    eq_cols = [
        "source_k",
        "source_cycle_id",
        "source_b",
        "hit_index",
        "from_t_v2",
        "from_odd_mod_256",
        "delta_t_bits",
    ]
    for col in eq_cols:
        for value in sorted({r[col] for r in returns}):
            specs.append((f"{col} == {value}", lambda r, c=col, v=value: r[c] == v))

    for col in ("source_b", "hit_index", "from_t_v2"):
        for value in sorted({r[col] for r in returns}):
            specs.append((f"{col} >= {value}", lambda r, c=col, v=value: r[c] >= v))
            specs.append((f"{col} <= {value}", lambda r, c=col, v=value: r[c] <= v))

    for value in range(-30, 1):
        specs.append((f"delta_t_bits <= {value}", lambda r, v=value: r["delta_t_bits"] <= v))

    for c in range(-3, 10):
        specs.append((f"hit_index == source_b - {c}", lambda r, c=c: r["hit_index"] == r["source_b"] - c))

    for c in range(-40, 41):
        specs.append((f"from_t_v2 - source_b == {c}", lambda r, c=c: r["from_t_v2"] - r["source_b"] == c))

    for m in range(1, 9):
        mod = 1 << m
        residues_t = sorted({r["source_t"] % mod for r in returns})
        residues_odd = sorted({r["from_odd_mod_256"] % mod for r in returns})
        for residue in residues_t:
            specs.append((f"source_t mod {mod} == {residue}", lambda r, mod=mod, residue=residue: r["source_t"] % mod == residue))
        for residue in residues_odd:
            specs.append((f"from_odd_mod_256 mod {mod} == {residue}", lambda r, mod=mod, residue=residue: r["from_odd_mod_256"] % mod == residue))

    return specs


def combine_rules(r1: Rule, r2: Rule, returns: list[Row], atom_index_by_return: dict[int, int]) -> Rule | None:
    if r1.name == r2.name:
        return None
    row_ids = r1.row_ids & r2.row_ids
    if not row_ids:
        return None
    atom_ids = r1.atom_ids & r2.atom_ids
    if len(atom_ids) < 2:
        return None
    atom_weight = 0.0
    row_weight = 0.0
    for i in row_ids:
        w = weight_s1(returns[i])
        row_weight += w
        if i in atom_index_by_return:
            atom_weight += w
    name = f"({r1.name}) AND ({r2.name})"
    return Rule(name, lambda r, a=r1.pred, b=r2.pred: a(r) and b(r), frozenset(atom_ids), frozenset(row_ids), atom_weight, row_weight)


def sort_key(rule: Rule) -> tuple[float, float, int, int]:
    # Favor rules that catch heavy atom mass while not being too broad.
    score = rule.atom_weight * math.sqrt(max(rule.precision_weight, 1e-300))
    return (score, rule.atom_weight, rule.atom_count, -rule.row_count)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def greedy_cover(rules: list[Rule], total_atoms: int) -> list[dict[str, object]]:
    remaining = set(range(total_atoms))
    picked = []
    for step in range(20):
        candidates = [r for r in rules if r.atom_ids & remaining]
        if not candidates:
            break
        best = max(
            candidates,
            key=lambda r: (
                sum(2.0 ** (i / 4.0) for i in r.atom_ids & remaining) * math.sqrt(max(r.precision_weight, 1e-300)),
                len(r.atom_ids & remaining),
                r.precision_weight,
            ),
        )
        new_atoms = best.atom_ids & remaining
        picked.append({
            "step": step + 1,
            "rule": best.name,
            "new_atom_count": len(new_atoms),
            "remaining_after": len(remaining - new_atoms),
            "atom_count_total": best.atom_count,
            "row_count": best.row_count,
            "atom_weight_s1": best.atom_weight,
            "row_weight_s1": best.row_weight,
            "precision_weight": best.precision_weight,
            "new_atoms": ",".join(str(i + 1) for i in sorted(new_atoms)),
        })
        remaining -= new_atoms
        if not remaining:
            break
    return picked


def main() -> None:
    returns = read_int_csv(RETURNS_PATH)
    atoms = read_int_csv(ATOMS_PATH)

    sig_to_atom_id = {atom_signature(row): i for i, row in enumerate(atoms)}
    atom_index_by_return = {}
    for i, row in enumerate(returns):
        sig = return_signature(row)
        if sig in sig_to_atom_id:
            atom_index_by_return[i] = sig_to_atom_id[sig]

    specs = make_unary_specs(returns)
    unary = []
    seen_names = set()
    for name, pred in specs:
        if name in seen_names:
            continue
        seen_names.add(name)
        rule = evaluate_rule(name, pred, returns, atom_index_by_return)
        if rule is not None:
            unary.append(rule)

    unary.sort(key=sort_key, reverse=True)
    write_csv(OUT_UNARY, [r.to_row() for r in unary])

    combo_candidates = unary[:180]
    combos_by_name = {}
    for i, r1 in enumerate(combo_candidates):
        for r2 in combo_candidates[i + 1:]:
            combo = combine_rules(r1, r2, returns, atom_index_by_return)
            if combo is not None:
                combos_by_name[combo.name] = combo
    combos = sorted(combos_by_name.values(), key=sort_key, reverse=True)
    write_csv(OUT_COMBO, [r.to_row() for r in combos[:500]])

    cover_pool = sorted(unary + combos[:500], key=sort_key, reverse=True)
    write_csv(OUT_COVER, greedy_cover(cover_pool, len(atoms)))

    print("=" * 112)
    print("  Exception pattern miner")
    print("=" * 112)
    print(f"  returns: {len(returns):,}")
    print(f"  atoms:   {len(atoms):,}")
    print(f"  matched atoms in returns: {len(atom_index_by_return):,}")
    print("\n  Top unary rules:")
    for rule in unary[:12]:
        print(
            f"    {rule.name:<36} atoms={rule.atom_count:>2} rows={rule.row_count:>5} "
            f"precision_w={rule.precision_weight:.3e} atom_w={rule.atom_weight:.3e}"
        )
    print("\n  Top combo rules:")
    for rule in combos[:12]:
        print(
            f"    {rule.name:<72} atoms={rule.atom_count:>2} rows={rule.row_count:>5} "
            f"precision_w={rule.precision_weight:.3e} atom_w={rule.atom_weight:.3e}"
        )
    print("\n  Output:")
    print(f"    {OUT_UNARY.name}")
    print(f"    {OUT_COMBO.name}")
    print(f"    {OUT_COVER.name}")


if __name__ == "__main__":
    main()
