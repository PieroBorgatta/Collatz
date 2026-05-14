"""
103_component_transition_budget.py

Finite transition-budget diagnostic for a two-component symbolic kernel.

The current Phase 10 candidate is not a single naive Z_2/BV operator.
Diagnostics 101 and 102 suggest isolating a structural source component,
provisionally

    bad(src) := src_odd == 3 and src_v2 in {0, 2}.

This script asks a narrower kernel question:

    Under the sampled return kernel, how much weighted mass flows
    good -> good, good -> bad, bad -> good, bad -> bad, or terminal?

The output is a finite diagnostic only.  It is not a theorem, not an
infinite-operator construction, and not a projection/convergence claim.
It is intended to decide whether a two-component operator ansatz is worth
formalizing.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_103_component_transition_budget_report.md"
OUT_CSV = ROOT / "collatz_103_component_transition_budget.csv"

State = tuple[int, int, int]
Component = str


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_CSV
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_103_{safe}_component_transition_budget"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}.csv"


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_delta_cutoffs(text: str) -> list[int]:
    return sorted({int(x.strip()) for x in text.split(",") if x.strip()})


def bad_state(state: State, rule: str) -> bool:
    v2, odd, _h = state
    if rule == "odd3_v2_0_or_2":
        return odd == 3 and v2 in {0, 2}
    if rule == "v2_2_odd3":
        return v2 == 2 and odd == 3
    if rule == "v2_0_odd3":
        return v2 == 0 and odd == 3
    if rule == "odd3":
        return odd == 3
    if rule == "v2_2":
        return v2 == 2
    if rule == "odd3_or_v2_2":
        return odd == 3 or v2 == 2
    raise ValueError(f"unknown bad rule: {rule}")


def component(state: State, rule: str) -> Component:
    return "bad" if bad_state(state, rule) else "good"


def bad_rule_description(rule: str) -> str:
    descriptions = {
        "odd3_v2_0_or_2": "src_odd == 3 and src_v2 in {0, 2}",
        "v2_2_odd3": "src_v2 == 2 and src_odd == 3",
        "v2_0_odd3": "src_v2 == 0 and src_odd == 3",
        "odd3": "src_odd == 3",
        "v2_2": "src_v2 == 2",
        "odd3_or_v2_2": "src_odd == 3 or src_v2 == 2",
    }
    if rule not in descriptions:
        raise ValueError(f"unknown bad rule: {rule}")
    return descriptions[rule]


def spectral_radius_2x2(a: float, b: float, c: float, d: float) -> float:
    trace = a + d
    determinant = a * d - b * c
    discriminant = max(0.0, trace * trace - 4.0 * determinant)
    root = discriminant ** 0.5
    return max(abs((trace + root) / 2.0), abs((trace - root) / 2.0))


def analyze_T(tail_mod, ctx, args: argparse.Namespace, T: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    op, shadowing, records, target, target_key, residue, modulus = ctx
    h_mod = 1 << args.hit_bits
    total_source_groups = (1 << T) * h_mod
    progress_step = max(1, total_source_groups // 20)
    delta_cutoffs = parse_delta_cutoffs(args.delta_cutoffs)

    source_samples: Counter[Component] = Counter()
    source_states: Counter[tuple[Component, State]] = Counter()
    transition_counts: Counter[tuple[Component, str]] = Counter()
    transition_weights: Counter[tuple[Component, Component]] = Counter()
    returned_counts: Counter[Component] = Counter()
    returned_weights: Counter[Component] = Counter()
    terminal_counts: Counter[Component] = Counter()
    delta_tail_weights: Counter[tuple[Component, int]] = Counter()
    delta_counts: Counter[tuple[Component, int]] = Counter()
    unresolved_counts: Counter[Component] = Counter()

    seen_groups = 0
    total_samples = 0
    for r in range(1 << T):
        for h in range(h_mod):
            for j in range(args.j_count):
                t = r + (j << T)
                if t == 0 and not args.include_t_zero:
                    continue
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
                    odd_bits=args.odd_bits,
                    hit_bits=args.hit_bits,
                    v2_cap=args.v2_cap,
                    max_steps=args.max_steps,
                )
                src_comp = component(row["src"], args.bad_rule)
                source_samples[src_comp] += 1
                source_states[(src_comp, row["src"])] += 1
                total_samples += 1
                if row["terminal"]:
                    terminal_counts[src_comp] += 1
                    transition_counts[(src_comp, "terminal")] += 1
                    unresolved_counts[src_comp] += int(row.get("unresolved", 0))
                    continue
                dst_comp = component(row["dst"], args.bad_rule)
                transition_counts[(src_comp, dst_comp)] += 1
                transition_weights[(src_comp, dst_comp)] += row["weight"]
                returned_counts[src_comp] += 1
                returned_weights[src_comp] += row["weight"]
                delta_counts[(src_comp, row["delta"])] += 1
                for cutoff in delta_cutoffs:
                    if row["delta"] > cutoff:
                        delta_tail_weights[(src_comp, cutoff)] += row["weight"]
            seen_groups += 1
            if args.progress and seen_groups % progress_step == 0:
                print(f"    T={T}: processed {seen_groups}/{total_source_groups} source groups")

    rows: list[dict[str, Any]] = []
    for comp in ("good", "bad"):
        denom = source_samples[comp]
        rows.append({
            "section": "source_component",
            "T": T,
            "component": comp,
            "samples": denom,
            "sample_mass": denom / total_samples if total_samples else 0.0,
            "returned_count": returned_counts[comp],
            "returned_fraction": returned_counts[comp] / denom if denom else 0.0,
            "terminal_count": terminal_counts[comp],
            "terminal_fraction": terminal_counts[comp] / denom if denom else 0.0,
            "unresolved_count": unresolved_counts[comp],
            "weighted_return_mass_per_sample": returned_weights[comp] / denom if denom else 0.0,
        })

    for src_comp in ("good", "bad"):
        denom = source_samples[src_comp]
        returned_weight = returned_weights[src_comp]
        for dst_comp in ("good", "bad"):
            key = (src_comp, dst_comp)
            weight = transition_weights[key]
            count = transition_counts[key]
            rows.append({
                "section": "transition",
                "T": T,
                "src_component": src_comp,
                "dst_component": dst_comp,
                "count": count,
                "count_fraction_per_source_sample": count / denom if denom else 0.0,
                "weighted_mass_per_source_sample": weight / denom if denom else 0.0,
                "conditional_weight_fraction_among_returns": weight / returned_weight if returned_weight else 0.0,
            })
        rows.append({
            "section": "transition",
            "T": T,
            "src_component": src_comp,
            "dst_component": "terminal",
            "count": terminal_counts[src_comp],
            "count_fraction_per_source_sample": terminal_counts[src_comp] / denom if denom else 0.0,
            "weighted_mass_per_source_sample": 0.0,
            "conditional_weight_fraction_among_returns": 0.0,
        })

    for comp in ("good", "bad"):
        for cutoff in delta_cutoffs:
            tail_weight = delta_tail_weights[(comp, cutoff)]
            total_weight = returned_weights[comp]
            rows.append({
                "section": "delta_tail",
                "T": T,
                "component": comp,
                "delta_cutoff": cutoff,
                "tail_weight": tail_weight,
                "tail_weight_fraction_among_returns": tail_weight / total_weight if total_weight else 0.0,
                "tail_weight_per_source_sample": tail_weight / source_samples[comp] if source_samples[comp] else 0.0,
            })

    for comp in ("good", "bad"):
        common = source_states.most_common()
        for (_state_comp, state), count in [
            item for item in common if item[0][0] == comp
        ][: args.keep_states]:
            rows.append({
                "section": "top_source_state",
                "T": T,
                "component": comp,
                "state": f"v2={state[0]}|odd={state[1]}|h={state[2]}",
                "count": count,
                "fraction_within_component": count / source_samples[comp] if source_samples[comp] else 0.0,
            })

    gg = transition_weights[("good", "good")] / source_samples["good"] if source_samples["good"] else 0.0
    gb = transition_weights[("good", "bad")] / source_samples["good"] if source_samples["good"] else 0.0
    bg = transition_weights[("bad", "good")] / source_samples["bad"] if source_samples["bad"] else 0.0
    bb = transition_weights[("bad", "bad")] / source_samples["bad"] if source_samples["bad"] else 0.0
    rows.append({
        "section": "two_component_matrix",
        "T": T,
        "good_to_good": gg,
        "good_to_bad": gb,
        "bad_to_good": bg,
        "bad_to_bad": bb,
        "row_sum_good": gg + gb,
        "row_sum_bad": bg + bb,
        "finite_two_component_spectral_radius": spectral_radius_2x2(gg, gb, bg, bb),
    })

    meta = {
        "T": T,
        "source_groups": total_source_groups,
        "j_count": args.j_count,
        "t_window": args.j_count << T,
        "bad_rule": args.bad_rule,
        "samples": total_samples,
        "good_samples": source_samples["good"],
        "bad_samples": source_samples["bad"],
        "good_weighted_return_mass": returned_weights["good"],
        "bad_weighted_return_mass": returned_weights["bad"],
    }
    return rows, meta


def build_report(args: argparse.Namespace, meta_rows: list[dict[str, Any]], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Two-Component Transition Budget",
        "",
        "Status: finite diagnostic output, not a theorem.",
        "",
        "Bad component convention:",
        "",
        f"- bad rule: `{args.bad_rule}`.",
        f"- `bad(src) := {bad_rule_description(args.bad_rule)}`.",
        "- `good` is the complement in the sampled symbolic state.",
        "",
        "The weighted entries below are empirical averages of `2^{-delta}`",
        "over source samples in the declared component.  Terminal/killed",
        "events carry zero transfer weight in this diagnostic.",
        "",
        "## Inputs",
        "",
        f"- T values: `{args.T}`",
        f"- j count: `{args.j_count}`",
        f"- odd bits: `{args.odd_bits}`",
        f"- hit bits: `{args.hit_bits}`",
        f"- v2 cap: `{args.v2_cap}`",
        f"- bad rule: `{args.bad_rule}`",
        f"- delta cutoffs: `{args.delta_cutoffs}`",
        "",
        "## Trace Meta",
        "",
        "| T | source groups | j count | t window | samples | good samples | bad samples |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for meta in meta_rows:
        lines.append(
            f"| {meta['T']} | {meta['source_groups']} | {meta['j_count']} | {meta['t_window']} | "
            f"{meta['samples']} | {meta['good_samples']} | {meta['bad_samples']} |"
        )

    matrix_rows = [row for row in rows if row["section"] == "two_component_matrix"]
    lines.extend([
        "",
        "## Weighted Two-Component Matrix",
        "",
        "| T | G->G | G->B | row G | B->G | B->B | row B | rho finite 2x2 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in matrix_rows:
        lines.append(
            f"| {row['T']} | {row['good_to_good']:.8g} | {row['good_to_bad']:.8g} | "
            f"{row['row_sum_good']:.8g} | {row['bad_to_good']:.8g} | "
            f"{row['bad_to_bad']:.8g} | {row['row_sum_bad']:.8g} | "
            f"{row['finite_two_component_spectral_radius']:.8g} |"
        )

    source_rows = [row for row in rows if row["section"] == "source_component"]
    lines.extend([
        "",
        "## Source Components",
        "",
        "| T | component | sample mass | returned fraction | terminal fraction | weighted return mass/sample | unresolved |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ])
    for row in source_rows:
        lines.append(
            f"| {row['T']} | `{row['component']}` | {row['sample_mass']:.8g} | "
            f"{row['returned_fraction']:.8g} | {row['terminal_fraction']:.8g} | "
            f"{row['weighted_return_mass_per_sample']:.8g} | {row['unresolved_count']} |"
        )

    transition_rows = [
        row for row in rows
        if row["section"] == "transition" and row["dst_component"] != "terminal"
    ]
    lines.extend([
        "",
        "## Return Flow",
        "",
        "| T | source | destination | count frac/source | weighted mass/source | conditional weighted frac |",
        "|---:|---|---|---:|---:|---:|",
    ])
    for row in transition_rows:
        lines.append(
            f"| {row['T']} | `{row['src_component']}` | `{row['dst_component']}` | "
            f"{row['count_fraction_per_source_sample']:.8g} | "
            f"{row['weighted_mass_per_source_sample']:.8g} | "
            f"{row['conditional_weight_fraction_among_returns']:.8g} |"
        )

    tail_rows = [row for row in rows if row["section"] == "delta_tail"]
    lines.extend([
        "",
        "## Delta Tail Weight",
        "",
        "| T | component | cutoff | tail weight/return weight | tail weight/source |",
        "|---:|---|---:|---:|---:|",
    ])
    for row in tail_rows:
        lines.append(
            f"| {row['T']} | `{row['component']}` | {row['delta_cutoff']} | "
            f"{row['tail_weight_fraction_among_returns']:.8g} | "
            f"{row['tail_weight_per_source_sample']:.8g} |"
        )

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "This diagnostic can support a two-component ansatz only if the good",
        "component has a controlled row budget and the bad component can be",
        "handled either by finite-rank methods, an exceptional-mass estimate,",
        "or a separate labelled-state argument.  A small finite 2x2 spectral",
        "radius here is not a spectral theorem for an infinite operator.",
        "",
        "This script aggregates over actual lifted sources `t`, not over",
        "source-cylinder pair distributions.  Therefore two runs with the",
        "same product `j_count * 2^T` enumerate the same `t` window and are",
        "not independent stability checks in `T`.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure good/bad transition budgets for the sampled return kernel.")
    parser.add_argument("--T", default="15")
    parser.add_argument("--j-count", type=int, default=16)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--delta-cutoffs", default="4,5,8")
    parser.add_argument(
        "--bad-rule",
        default="odd3_v2_0_or_2",
        choices=[
            "odd3_v2_0_or_2",
            "v2_2_odd3",
            "v2_0_odd3",
            "odd3",
            "v2_2",
            "odd3_or_v2_2",
        ],
    )
    parser.add_argument("--keep-states", type=int, default=8)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()

    all_rows: list[dict[str, Any]] = []
    meta_rows: list[dict[str, Any]] = []

    print("=" * 118)
    print("  Two-component transition budget")
    print("=" * 118)
    print(f"  T={args.T}, j_count={args.j_count}")
    print(f"  Bad component: {bad_rule_description(args.bad_rule)}")
    print("  No infinite-operator or spectral-gap claim is made.")

    for T in parse_csv_ints(args.T):
        rows, meta = analyze_T(tail_mod, ctx, args, T)
        all_rows.extend(rows)
        meta_rows.append(meta)
        print(
            f"  T={T}: samples={meta['samples']}, "
            f"good={meta['good_samples']}, bad={meta['bad_samples']}"
        )

    report_path, csv_path = output_paths(args.output_tag)
    report_path.write_text(build_report(args, meta_rows, all_rows), encoding="utf-8")
    write_csv(all_rows, csv_path)

    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {csv_path.name}")


if __name__ == "__main__":
    main()
