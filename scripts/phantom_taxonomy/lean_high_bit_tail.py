#!/usr/bin/env python3
"""
Generate a Lean import for exact high-bit majority core/tail matrices.

Input rows are produced by ``export_high_bit_tail_edges.py`` and contain
exact normalized rational entries for the three graphs ``full``, ``core``,
and ``tail``.  The generated Lean file defines ``Full`` as ``Core + Tail``
after checking the CSV equality exactly.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


def parse_state(text: str) -> tuple[int, int, int]:
    parts = dict(part.split("=", 1) for part in text.split("|"))
    return int(parts["v2"]), int(parts["odd"]), int(parts["h"])


def matrix_expr(entries: dict[tuple[tuple[int, int, int], tuple[int, int, int]], Fraction]) -> str:
    by_src: dict[tuple[int, int, int], list[tuple[tuple[int, int, int], Fraction]]] = defaultdict(list)
    for (src, dst), weight in entries.items():
        by_src[src].append((dst, weight))

    lines = []
    for src in sorted(by_src):
        lines.append(f"  if i = ({src[0]}, {src[1]}, {src[2]}) then")
        for dst, weight in sorted(by_src[src]):
            val = f"(({weight.numerator} : NNReal) / ({weight.denominator} : NNReal))"
            lines.append(f"    if j = ({dst[0]}, {dst[1]}, {dst[2]}) then {val} else")
        lines.append("    0")
        lines.append("  else")
    lines.append("  0")
    return "\n".join(lines)


def support_name(namespace: str, matrix_name: str, src: tuple[int, int, int]) -> str:
    return f"{namespace}{matrix_name}Support_{src[0]}_{src[1]}_{src[2]}"


def row_sum_name(namespace: str, matrix_name: str, src: tuple[int, int, int]) -> str:
    return f"{namespace}{matrix_name}_rowSum_{src[0]}_{src[1]}_{src[2]}"


def state_expr(state: tuple[int, int, int]) -> str:
    return f"({state[0]}, {state[1]}, {state[2]})"


def support_expr(states: list[tuple[int, int, int]]) -> str:
    return "[" + ", ".join(state_expr(state) for state in states) + "].toFinset"


def rcases_conjunction(names: list[str]) -> str:
    if len(names) == 1:
        return f"    have {names[0]} := hsrc"
    return "    rcases hsrc with ⟨" + ", ".join(names) + "⟩"


def row_support_defs(
    target_v: int,
    namespace: str,
    matrix_name: str,
    entries: dict[tuple[tuple[int, int, int], tuple[int, int, int]], Fraction],
) -> str:
    by_src: dict[tuple[int, int, int], list[tuple[tuple[int, int, int], Fraction]]] = defaultdict(list)
    for (src, dst), weight in entries.items():
        by_src[src].append((dst, weight))

    chunks = []
    for src in sorted(by_src):
        dsts = [dst for dst, _weight in sorted(by_src[src])]
        row_sum = sum((weight for _dst, weight in by_src[src]), Fraction(0))
        hnames = [f"h{k}" for k in range(len(dsts))]
        simp_matrices = (
            f"{namespace}Full, {namespace}Core, {namespace}Tail"
            if matrix_name == "Full"
            else f"{namespace}{matrix_name}"
        )
        chunks.append(
            f"""
/-- Destination support of row `{state_expr(src)}` in `{namespace}{matrix_name}`. -/
def {support_name(namespace, matrix_name, src)} : Finset (PhaseState {target_v}) :=
  {support_expr(dsts)}

set_option linter.flexible false in
set_option maxHeartbeats 1000000 in
-- Generated row-support arithmetic can exceed the default heartbeat budget.
/-- Exact row sum for `{state_expr(src)}` in `{namespace}{matrix_name}`. -/
theorem {row_sum_name(namespace, matrix_name, src)} :
    (∑ j, {namespace}{matrix_name} {state_expr(src)} j) =
      (({row_sum.numerator} : NNReal) / ({row_sum.denominator} : NNReal)) := by
  rw [show (∑ j, {namespace}{matrix_name} {state_expr(src)} j) =
      ∑ j ∈ {support_name(namespace, matrix_name, src)}, {namespace}{matrix_name} {state_expr(src)} j by
    symm
    refine Finset.sum_subset (by intro dst hdst; simp) ?_
    intro dst _ hsrc
    simp [{support_name(namespace, matrix_name, src)}] at hsrc
{rcases_conjunction(hnames)}
    simp [{simp_matrices}, {", ".join(hnames)}]]
  simp [{support_name(namespace, matrix_name, src)}, {simp_matrices}]
  try norm_num
"""
        )
    return "\n".join(chunks)


def row_cases(
    target_v: int,
    namespace: str,
    matrix_name: str,
    active_sources: set[tuple[int, int, int]],
) -> str:
    states = [(v, o, h) for v in range(0, target_v + 1) for o in range(0, 4) for h in range(0, 4)]
    cases = []
    for src in states:
        if src in active_sources:
            cases.append(
                "\n".join(
                    [
                        f"  · change (∑ j, {namespace}{matrix_name} {state_expr(src)} j) ≤ 1",
                        f"    rw [{row_sum_name(namespace, matrix_name, src)}]",
                        "    rw [← NNReal.coe_le_coe]",
                        "    norm_num",
                    ]
                )
            )
        else:
            if matrix_name == "Full":
                cases.append(f"  · simp [{namespace}Full, {namespace}Core, {namespace}Tail]")
            else:
                cases.append(f"  · simp [{namespace}{matrix_name}]")
    return "\n".join(cases)


def row_substochastic_theorem(
    target_v: int,
    namespace: str,
    matrix_name: str,
    entries: dict[tuple[tuple[int, int, int], tuple[int, int, int]], Fraction],
) -> str:
    active_sources = {src for src, _dst in entries}
    return f"""
set_option maxHeartbeats 3000000 in
-- Generated row cases split the finite phase-state space.
/-- Generated row-substochasticity certificate for `{namespace}{matrix_name}`. -/
theorem {namespace}{matrix_name}_rowSubstochastic :
    RowSubstochastic {namespace}{matrix_name} := by
  intro i
  rcases i with ⟨v, o, h⟩
  fin_cases v <;> fin_cases o <;> fin_cases h
{row_cases(target_v, namespace, matrix_name, active_sources)}
"""


def read_entries(input_csv: Path, target_t: int, j_count: int) -> tuple[int, dict[str, dict]]:
    graphs: dict[str, dict[tuple[tuple[int, int, int], tuple[int, int, int]], Fraction]] = {
        "full": {},
        "core": {},
        "tail": {},
    }
    target_v = 0
    with input_csv.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if int(row["T"]) != target_t or int(row["j_count"]) != j_count:
                continue
            graph = row["graph"]
            if graph not in graphs:
                continue
            src = parse_state(row["src"])
            dst = parse_state(row["dst"])
            target_v = max(target_v, *(src + dst))
            weight = Fraction(int(row["normalized_num"]), int(row["normalized_den"]))
            graphs[graph][(src, dst)] = weight

    if not graphs["full"]:
        raise ValueError(f"no full edges for T={target_t}, j_count={j_count}")

    all_keys = set(graphs["full"]) | set(graphs["core"]) | set(graphs["tail"])
    for key in all_keys:
        if graphs["full"].get(key, Fraction(0)) != graphs["core"].get(key, Fraction(0)) + graphs["tail"].get(key, Fraction(0)):
            raise ValueError(f"full != core + tail for edge {key}")
    return target_v, graphs


def generate(input_csv: Path, output: Path, target_t: int, j_count: int, namespace: str) -> None:
    target_v, graphs = read_entries(input_csv, target_t, j_count)
    content = f"""/-
Generated exact high-bit majority core/tail transfer matrices.

Source CSV: `{input_csv}`
Target T: {target_t}
j_count: {j_count}
Observed valuation cap: {target_v}

This file is generated by `scripts/phantom_taxonomy/lean_high_bit_tail.py`.
-/

import CollatzShadowing.Bound

set_option linter.style.longLine false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

namespace CollatzShadowing
namespace Generated

open scoped NNReal

/-- Majority-signature core matrix for the empirical `T = {target_t}`, `j = {j_count}` sample. -/
noncomputable def {namespace}Core : TransferMatrix {target_v} :=
fun i j =>
{matrix_expr(graphs["core"])}

/-- High-bit tail matrix for the empirical `T = {target_t}`, `j = {j_count}` sample. -/
noncomputable def {namespace}Tail : TransferMatrix {target_v} :=
fun i j =>
{matrix_expr(graphs["tail"])}

/-- Full empirical transfer matrix, definitionally split as `core + tail`. -/
noncomputable def {namespace}Full : TransferMatrix {target_v} :=
  {namespace}Core + {namespace}Tail

{row_support_defs(target_v, namespace, "Core", graphs["core"])}

{row_support_defs(target_v, namespace, "Tail", graphs["tail"])}

{row_support_defs(target_v, namespace, "Full", graphs["full"])}

{row_substochastic_theorem(target_v, namespace, "Core", graphs["core"])}

{row_substochastic_theorem(target_v, namespace, "Tail", graphs["tail"])}

{row_substochastic_theorem(target_v, namespace, "Full", graphs["full"])}

/-- The generated full matrix is definitionally the sum of core and tail. -/
theorem {namespace}Full_eq_core_add_tail :
    {namespace}Full = {namespace}Core + {namespace}Tail :=
  rfl

/-- Exact imported majority core/tail decomposition for `T = {target_t}`, `j = {j_count}`. -/
noncomputable def {namespace}Decomposition :
    OperatorDecomposition {target_v} where
  full := {namespace}Full
  core := {namespace}Core
  tail := {namespace}Tail
  full_eq_core_add_tail := {namespace}Full_eq_core_add_tail
  full_rowSubstochastic := {namespace}Full_rowSubstochastic
  core_rowSubstochastic := {namespace}Core_rowSubstochastic
  tail_rowSubstochastic := {namespace}Tail_rowSubstochastic

end Generated
end CollatzShadowing
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-t", type=int, default=10)
    parser.add_argument("--j-count", type=int, default=32)
    parser.add_argument("--namespace", default="t10j32HighBitTail")
    args = parser.parse_args()
    generate(args.input, args.output, args.target_t, args.j_count, args.namespace)


if __name__ == "__main__":
    main()
