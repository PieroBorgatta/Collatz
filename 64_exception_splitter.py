"""
64_exception_splitter.py

Splitter adattivo delle eccezioni del return-map critico.

Nel nodo critico (12,2,1), la pressione grezza esplode per poche code rare:

    delta_t_bits < 0

Questo script cerca regole finite che isolino tali code usando feature
disponibili al momento del ritorno:

  - source_k, source_cycle_id, source_b
  - hit_index
  - from_t_v2
  - from_odd_mod_256
  - from_t_bits bucket

Per ogni candidato split calcola:
  - quanti bad cattura;
  - precisione;
  - pressione P_s dentro e fuori;
  - riduzione della pressione fuori.

Non e' ancora un certificato: e' il generatore di sottostati eccezionali per
il prossimo automa.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable


Row = dict[str, int]


def read_returns(path: str) -> list[Row]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def read_terminals(path: str) -> list[dict[str, int]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append({k: int(v) for k, v in row.items()})
    return rows


def pressure(rows: list[Row], terminal_count: int, s: float) -> float:
    total = len(rows) + terminal_count
    if total == 0:
        return 0.0
    weighted = sum(2.0 ** (-s * r["delta_t_bits"]) for r in rows)
    return weighted / total


def bad_count(rows: list[Row]) -> int:
    return sum(1 for r in rows if r["delta_t_bits"] < 0)


def feature_values(rows: list[Row], feature: str) -> set[int]:
    if feature == "from_t_bits_bucket4":
        return {r["from_t_bits"] // 4 for r in rows}
    if feature == "from_t_bits_bucket8":
        return {r["from_t_bits"] // 8 for r in rows}
    return {r[feature] for r in rows}


def feature_get(row: Row, feature: str) -> int:
    if feature == "from_t_bits_bucket4":
        return row["from_t_bits"] // 4
    if feature == "from_t_bits_bucket8":
        return row["from_t_bits"] // 8
    return row[feature]


@dataclass
class Rule:
    name: str
    predicate: Callable[[Row], bool]


def candidate_rules(rows: list[Row], max_mod_bits: int) -> list[Rule]:
    features = [
        "source_k",
        "source_cycle_id",
        "source_b",
        "hit_index",
        "from_t_v2",
        "from_odd_mod_256",
        "from_t_bits_bucket4",
        "from_t_bits_bucket8",
    ]
    rules = []

    for feature in features:
        for value in sorted(feature_values(rows, feature)):
            rules.append(Rule(
                name=f"{feature} == {value}",
                predicate=lambda r, feature=feature, value=value: feature_get(r, feature) == value,
            ))

    for bits in range(1, max_mod_bits + 1):
        mod = 1 << bits
        residues = sorted({r["from_odd_mod_256"] & (mod - 1) for r in rows})
        for residue in residues:
            rules.append(Rule(
                name=f"from_odd_mod_2^{bits} == {residue}",
                predicate=lambda r, mod=mod, residue=residue: (r["from_odd_mod_256"] & (mod - 1)) == residue,
            ))

    # Conjunctions with the strongest structural feature: source_b.
    source_bs = sorted({r["source_b"] for r in rows})
    for b in source_bs:
        for bits in range(1, max_mod_bits + 1):
            mod = 1 << bits
            residues = sorted({r["from_odd_mod_256"] & (mod - 1) for r in rows if r["source_b"] == b})
            for residue in residues:
                rules.append(Rule(
                    name=f"source_b == {b} AND from_odd_mod_2^{bits} == {residue}",
                    predicate=lambda r, b=b, mod=mod, residue=residue: (
                        r["source_b"] == b and (r["from_odd_mod_256"] & (mod - 1)) == residue
                    ),
                ))

    return rules


def evaluate_rule(rule: Rule, rows: list[Row], terminal_count: int, s: float) -> dict:
    inside = [r for r in rows if rule.predicate(r)]
    outside = [r for r in rows if not rule.predicate(r)]
    total_bad = bad_count(rows)
    inside_bad = bad_count(inside)
    inside_count = len(inside)
    precision = inside_bad / inside_count if inside_count else 0.0
    recall = inside_bad / total_bad if total_bad else 0.0

    return {
        "rule": rule.name,
        "inside_count": inside_count,
        "inside_bad": inside_bad,
        "precision": precision,
        "recall": recall,
        "outside_count": len(outside),
        "outside_bad": bad_count(outside),
        "pressure_inside": pressure(inside, 0, s),
        "pressure_outside": pressure(outside, terminal_count, s),
    }


def greedy_split(rows: list[Row], terminal_count: int, s: float, max_mod_bits: int, max_rules: int) -> list[dict]:
    remaining = rows[:]
    selected = []
    total_terminal = terminal_count

    for _ in range(max_rules):
        candidates = candidate_rules(remaining, max_mod_bits)
        evaluated = [evaluate_rule(rule, remaining, total_terminal, s) for rule in candidates]
        # Prefer high bad recall, high precision, and low outside pressure.
        evaluated = [
            e for e in evaluated
            if e["inside_bad"] > 0 and e["inside_count"] > 0 and e["precision"] >= 0.05
        ]
        if not evaluated:
            break
        evaluated.sort(
            key=lambda e: (
                e["pressure_outside"],
                -e["inside_bad"],
                -e["precision"],
                e["inside_count"],
            )
        )
        best = evaluated[0]
        selected.append(best)

        # Remove selected exception subset from remaining.
        # Reconstruct predicate by name lookup for simplicity.
        chosen_rule = next(r for r in candidates if r.name == best["rule"])
        remaining = [r for r in remaining if not chosen_rule.predicate(r)]
        if pressure(remaining, total_terminal, s) < 1.0:
            break

    selected.append({
        "rule": "__REMAINDER__",
        "inside_count": len(remaining),
        "inside_bad": bad_count(remaining),
        "precision": bad_count(remaining) / len(remaining) if remaining else 0.0,
        "recall": 1.0,
        "outside_count": 0,
        "outside_bad": 0,
        "pressure_inside": pressure(remaining, total_terminal, s),
        "pressure_outside": 0.0,
    })
    return selected


def delta_distribution(rows: list[Row]) -> list[dict]:
    out = []
    total = len(rows)
    for delta, count in Counter(r["delta_t_bits"] for r in rows).most_common():
        out.append({
            "delta_t_bits": delta,
            "count": count,
            "fraction": count / total if total else 0.0,
        })
    return out


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[Row], terminals: list[dict], selected: list[dict], s: float) -> None:
    print("=" * 112)
    print("  Exception splitter sul return-map critico")
    print("=" * 112)
    print(f"  returns:     {len(rows)}")
    print(f"  terminals:   {len(terminals)}")
    print(f"  bad returns: {bad_count(rows)}")
    print(f"  pressure P_{s:g}: {pressure(rows, len(terminals), s):.6g}")
    print()
    print(f"  {'rule':<58} {'n':>7} {'bad':>6} {'prec':>8} {'recall':>8} {'P_in':>12} {'P_out':>12}")
    for row in selected:
        print(f"  {row['rule']:<58} {row['inside_count']:>7} {row['inside_bad']:>6} "
              f"{row['precision']:>8.4f} {row['recall']:>8.4f} "
              f"{row['pressure_inside']:>12.6g} {row['pressure_outside']:>12.6g}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Splitta eccezioni del nodo critico.")
    parser.add_argument("--returns", default="collatz_62_critical_returns.csv")
    parser.add_argument("--terminals", default="collatz_62_critical_terminals.csv")
    parser.add_argument("--s", type=float, default=1.0)
    parser.add_argument("--max-mod-bits", type=int, default=8)
    parser.add_argument("--max-rules", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_returns(args.returns)
    terminals = read_terminals(args.terminals)
    selected = greedy_split(
        rows,
        terminal_count=len(terminals),
        s=args.s,
        max_mod_bits=args.max_mod_bits,
        max_rules=args.max_rules,
    )
    write_csv(selected, "collatz_64_exception_rules.csv")
    write_csv(delta_distribution(rows), "collatz_64_delta_distribution.csv")
    print_summary(rows, terminals, selected, args.s)
    print("\n  Output:")
    print("    collatz_64_exception_rules.csv")
    print("    collatz_64_delta_distribution.csv")


if __name__ == "__main__":
    main()
