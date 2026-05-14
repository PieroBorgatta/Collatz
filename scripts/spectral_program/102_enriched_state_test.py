"""
102_enriched_state_test.py

Finite diagnostic for a candidate enriched symbolic state.

The previous diagnostics show that full-label 2-adic oscillation does
not contract cleanly, but that the full-over-phase excess is concentrated
in structural source strata such as source_v2_odd = 2|3.

This script asks a narrow question:

    If an enriched symbolic model isolates a declared structural class,
    how much of the full-over-phase excess remains on the complement?

This is not a theorem, not a transfer-operator construction, and not a
spectral-radius computation.  It is a go/no-go diagnostic for whether an
enriched symbolic branch is worth formalizing.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_102_enriched_state_test_report.md"
OUT_CSV = ROOT / "collatz_102_enriched_state_test.csv"

State = tuple[int, int, int]
CandidateFn = Callable[[State], bool]


def load_local(filename: str, name: str):
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
    stem = f"collatz_102_{safe}_enriched_state_test"
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


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = q * (len(ordered) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def fmt_state(state: State) -> str:
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def dominant_source(rows: list[dict[str, Any]]) -> State:
    counts = Counter(row["src"] for row in rows)
    return counts.most_common(1)[0][0]


def candidate_functions() -> dict[str, CandidateFn]:
    return {
        "source_odd_3": lambda s: s[1] == 3,
        "source_v2_2": lambda s: s[0] == 2,
        "source_v2_2_odd_3": lambda s: s[0] == 2 and s[1] == 3,
        "source_v2_0_odd_3": lambda s: s[0] == 0 and s[1] == 3,
        "source_odd_3_or_v2_2": lambda s: s[1] == 3 or s[0] == 2,
        "source_v2_0_or_2_odd_3": lambda s: s[1] == 3 and s[0] in {0, 2},
    }


def pair_metrics(z2, rows0: list[dict[str, Any]], rows1: list[dict[str, Any]]) -> dict[str, float]:
    tvs: dict[str, float] = {}
    for level in z2.SIGNATURE_LEVELS:
        tvs[level] = z2.total_variation(
            z2.distribution(rows0, level),
            z2.distribution(rows1, level),
        )
    return {
        "phase_tv": tvs["phase"],
        "full_tv": tvs["full"],
        "full_excess_over_phase": max(0.0, tvs["full"] - tvs["phase"]),
        "delta_excess_over_phase": max(0.0, tvs["delta"] - tvs["phase"]),
    }


def summarize_values(values: list[float]) -> dict[str, float]:
    return {
        "mean": mean(values) if values else 0.0,
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
        "sum": sum(values),
    }


def make_summary_row(
    *,
    T: int,
    depth: int,
    candidate: str,
    metric: str,
    selected: list[float],
    complement: list[float],
    global_values: list[float],
) -> dict[str, Any]:
    sel = summarize_values(selected)
    comp = summarize_values(complement)
    glob = summarize_values(global_values)
    total_count = len(global_values)
    selected_count = len(selected)
    complement_count = len(complement)
    return {
        "T": T,
        "depth": depth,
        "candidate": candidate,
        "metric": metric,
        "total_samples": total_count,
        "selected_samples": selected_count,
        "selected_mass": selected_count / total_count if total_count else 0.0,
        "selected_mean": sel["mean"],
        "selected_p95": sel["p95"],
        "selected_p99": sel["p99"],
        "selected_max": sel["max"],
        "selected_contribution": sel["sum"] / glob["sum"] if glob["sum"] else 0.0,
        "complement_samples": complement_count,
        "complement_mass": complement_count / total_count if total_count else 0.0,
        "complement_mean": comp["mean"],
        "complement_p95": comp["p95"],
        "complement_p99": comp["p99"],
        "complement_max": comp["max"],
        "complement_contribution": comp["sum"] / glob["sum"] if glob["sum"] else 0.0,
        "global_mean": glob["mean"],
        "global_p95": glob["p95"],
        "global_p99": glob["p99"],
        "global_max": glob["max"],
        "mean_reduction_on_complement": glob["mean"] - comp["mean"],
    }


def analyze_T(z2, tail_mod, ctx, args: argparse.Namespace, T: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    h_mod = 1 << args.hit_bits
    max_j = 1 << (args.max_depth + 1 + args.tail_bits)
    total_groups = (1 << T) * h_mod
    progress_step = max(1, total_groups // 20)
    candidates = candidate_functions()
    metrics = ("full_excess_over_phase", "full_tv")

    global_values: dict[tuple[int, str], list[float]] = defaultdict(list)
    selected_values: dict[tuple[int, str, str], list[float]] = defaultdict(list)
    complement_values: dict[tuple[int, str, str], list[float]] = defaultdict(list)

    seen = 0
    pair_count = 0
    for r in range(1 << T):
        for h in range(h_mod):
            rows = z2.trace_rows_for_group(
                tail_mod=tail_mod,
                ctx=ctx,
                args=args,
                T=T,
                r=r,
                h=h,
                max_j=max_j,
            )
            src = dominant_source(rows)
            candidate_hits = {name: fn(src) for name, fn in candidates.items()}
            for depth in range(args.max_depth + 1):
                for q in range(1 << depth):
                    rows0 = z2.child_rows(rows, depth, q, 0)
                    rows1 = z2.child_rows(rows, depth, q, 1)
                    if not rows0 or not rows1:
                        continue
                    pair_count += 1
                    pair = pair_metrics(z2, rows0, rows1)
                    for metric in metrics:
                        value = pair[metric]
                        global_values[(depth, metric)].append(value)
                        for name, hit in candidate_hits.items():
                            key = (depth, name, metric)
                            if hit:
                                selected_values[key].append(value)
                            else:
                                complement_values[key].append(value)
            seen += 1
            if args.progress and seen % progress_step == 0:
                print(f"    T={T}: processed {seen}/{total_groups} source groups")

    rows_out: list[dict[str, Any]] = []
    for depth in range(args.max_depth + 1):
        for candidate in candidates:
            for metric in metrics:
                rows_out.append(make_summary_row(
                    T=T,
                    depth=depth,
                    candidate=candidate,
                    metric=metric,
                    selected=selected_values[(depth, candidate, metric)],
                    complement=complement_values[(depth, candidate, metric)],
                    global_values=global_values[(depth, metric)],
                ))
    meta = {
        "T": T,
        "max_j": max_j,
        "source_groups": total_groups,
        "pair_count": pair_count,
    }
    return rows_out, meta


def build_report(args: argparse.Namespace, meta_rows: list[dict[str, Any]], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Enriched State Test",
        "",
        "Status: finite diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- T values: `{args.T}`",
        f"- max depth: `{args.max_depth}`",
        f"- tail bits: `{args.tail_bits}`",
        f"- odd bits: `{args.odd_bits}`",
        f"- hit bits: `{args.hit_bits}`",
        f"- v2 cap: `{args.v2_cap}`",
        "",
        "The selected component is the part that an enriched state would",
        "isolate.  The complement columns measure the remaining obstruction",
        "outside that component.",
        "",
        "## Trace Meta",
        "",
        "| T | max j | source groups | parent-child pairs |",
        "|---:|---:|---:|---:|",
    ]
    for meta in meta_rows:
        lines.append(
            f"| {meta['T']} | {meta['max_j']} | {meta['source_groups']} | {meta['pair_count']} |"
        )

    for depth in range(args.max_depth + 1):
        lines.extend([
            "",
            f"## Depth {depth}: Full-Over-Phase Excess",
            "",
            "| candidate | selected mass | selected mean | selected contribution | complement mean | complement p95 | complement contribution | global mean |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        depth_rows = [
            row for row in rows
            if row["depth"] == depth and row["metric"] == "full_excess_over_phase"
        ]
        depth_rows.sort(key=lambda row: (row["selected_contribution"], -row["selected_mass"]), reverse=True)
        for row in depth_rows:
            lines.append(
                f"| `{row['candidate']}` | {row['selected_mass']:.6g} | "
                f"{row['selected_mean']:.6g} | {row['selected_contribution']:.6g} | "
                f"{row['complement_mean']:.6g} | {row['complement_p95']:.6g} | "
                f"{row['complement_contribution']:.6g} | {row['global_mean']:.6g} |"
            )

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "A promising enriched component should have small selected mass, large",
        "selected contribution, and a substantially smaller complement mean",
        "or p95.  This only motivates an enlarged symbolic model; it does not",
        "define an infinite operator or a Banach norm.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test candidate enriched-state source components.")
    parser.add_argument("--T", default="15")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--tail-bits", type=int, default=3)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    z2 = load_local("100_z2_cylinder_oscillation.py", "z2_cylinder")
    tail_mod = z2.load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()

    all_rows: list[dict[str, Any]] = []
    meta_rows = []

    print("=" * 118)
    print("  Enriched state test")
    print("=" * 118)
    print(f"  T={args.T}, max_depth={args.max_depth}, tail_bits={args.tail_bits}")
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, v2_cap={args.v2_cap}")
    print("  No spectral-radius bounds are computed.")

    for T in parse_csv_ints(args.T):
        rows, meta = analyze_T(z2, tail_mod, ctx, args, T)
        all_rows.extend(rows)
        meta_rows.append(meta)
        print(
            f"  T={T}: max_j={meta['max_j']}, source groups={meta['source_groups']}, "
            f"pairs={meta['pair_count']}, summary rows={len(rows)}"
        )

    report_path, csv_path = output_paths(args.output_tag)
    report_path.write_text(build_report(args, meta_rows, all_rows), encoding="utf-8")
    write_csv(all_rows, csv_path)

    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {csv_path.name}")


if __name__ == "__main__":
    main()
