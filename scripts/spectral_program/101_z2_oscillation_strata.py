"""
101_z2_oscillation_strata.py

Stratify the genuine 2-adic child-cylinder oscillation diagnostic.

Script 100 asks whether the two children of a high-bit parent class
have similar signature distributions.  This script asks where the
failure lives: is full-label oscillation concentrated in structural
source strata, or spread across the whole finite source layer?

This is finite diagnostic output only.  It is not an infinite-operator
construction, not a Banach-space theorem, and not a spectral estimate.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_101_z2_oscillation_strata_report.md"
OUT_CSV = ROOT / "collatz_101_z2_oscillation_strata.csv"

METRICS = (
    "status_tv",
    "phase_tv",
    "delta_tv",
    "full_tv",
    "delta_excess_over_phase",
    "full_excess_over_phase",
    "full_dominant_changed",
)


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
    stem = f"collatz_101_{safe}_z2_oscillation_strata"
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


def v2_int(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    out = 0
    while (n & 1) == 0:
        n >>= 1
        out += 1
    return out


def capped_v2_text(n: int, cap: int) -> str:
    v = v2_int(n)
    if v >= 10**8:
        return "zero"
    if v >= cap:
        return f">={cap}"
    return str(v)


def fmt_state(state: tuple[int, int, int]) -> str:
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def dominant_source(rows: list[dict[str, Any]]) -> tuple[tuple[int, int, int], int, int]:
    counts = Counter(row["src"] for row in rows)
    state, count = counts.most_common(1)[0]
    return state, count, len(counts)


def group_strata(rows: list[dict[str, Any]], r: int, h: int, v2_cap: int) -> list[tuple[str, str]]:
    src, _count, distinct = dominant_source(rows)
    return [
        ("global", "all"),
        ("source_v2", str(src[0])),
        ("source_odd", str(src[1])),
        ("source_h", str(src[2])),
        ("source_v2_odd", f"{src[0]}|{src[1]}"),
        ("source_state", fmt_state(src)),
        ("source_mixed", str(int(distinct > 1))),
        ("r_v2", capped_v2_text(r, v2_cap)),
        ("r_h", str(h)),
    ]


def pair_metrics(z2, rows0: list[dict[str, Any]], rows1: list[dict[str, Any]]) -> dict[str, float]:
    tvs: dict[str, float] = {}
    doms: dict[str, tuple[Any, Any]] = {}
    for level in z2.SIGNATURE_LEVELS:
        dist0 = z2.distribution(rows0, level)
        dist1 = z2.distribution(rows1, level)
        tvs[level] = z2.total_variation(dist0, dist1)
        doms[level] = (z2.majority(dist0), z2.majority(dist1))
    return {
        "status_tv": tvs["status"],
        "phase_tv": tvs["phase"],
        "delta_tv": tvs["delta"],
        "full_tv": tvs["full"],
        "delta_excess_over_phase": max(0.0, tvs["delta"] - tvs["phase"]),
        "full_excess_over_phase": max(0.0, tvs["full"] - tvs["phase"]),
        "full_dominant_changed": 1.0 if doms["full"][0] != doms["full"][1] else 0.0,
    }


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


def make_row(
    *,
    depth: int,
    stratum: str,
    value: str,
    metric: str,
    values: list[float],
    global_count: int,
    global_sum: float,
) -> dict[str, Any]:
    count = len(values)
    total = sum(values)
    mass_fraction = count / global_count if global_count else 0.0
    contribution_fraction = total / global_sum if global_sum else 0.0
    return {
        "depth": depth,
        "stratum": stratum,
        "value": value,
        "metric": metric,
        "samples": count,
        "mass_fraction": mass_fraction,
        "mean": mean(values) if values else 0.0,
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
        "contribution_fraction": contribution_fraction,
    }


def analyze_T(z2, tail_mod, ctx, args: argparse.Namespace, T: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    h_mod = 1 << args.hit_bits
    max_j = 1 << (args.max_depth + 1 + args.tail_bits)
    total_groups = (1 << T) * h_mod
    progress_step = max(1, total_groups // 20)

    values: dict[tuple[int, str, str, str], list[float]] = defaultdict(list)
    global_values: dict[tuple[int, str], list[float]] = defaultdict(list)

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
            strata = group_strata(rows, r, h, args.v2_cap)
            for depth in range(args.max_depth + 1):
                for q in range(1 << depth):
                    rows0 = z2.child_rows(rows, depth, q, 0)
                    rows1 = z2.child_rows(rows, depth, q, 1)
                    if not rows0 or not rows1:
                        continue
                    pair_count += 1
                    metrics = pair_metrics(z2, rows0, rows1)
                    for metric, metric_value in metrics.items():
                        global_values[(depth, metric)].append(metric_value)
                        for stratum, value in strata:
                            values[(depth, stratum, value, metric)].append(metric_value)
            seen += 1
            if args.progress and seen % progress_step == 0:
                print(f"    T={T}: processed {seen}/{total_groups} source groups")

    global_counts = {key: len(vals) for key, vals in global_values.items()}
    global_sums = {key: sum(vals) for key, vals in global_values.items()}

    rows_out: list[dict[str, Any]] = []
    for (depth, metric), vals in sorted(global_values.items()):
        rows_out.append(make_row(
            depth=depth,
            stratum="global",
            value="all",
            metric=metric,
            values=vals,
            global_count=global_counts[(depth, metric)],
            global_sum=global_sums[(depth, metric)],
        ))

    for (depth, stratum, value, metric), vals in sorted(values.items()):
        if stratum == "global":
            continue
        if len(vals) < args.min_samples:
            continue
        rows_out.append(make_row(
            depth=depth,
            stratum=stratum,
            value=value,
            metric=metric,
            values=vals,
            global_count=global_counts[(depth, metric)],
            global_sum=global_sums[(depth, metric)],
        ))

    meta = {
        "T": T,
        "max_j": max_j,
        "source_groups": total_groups,
        "pair_count": pair_count,
    }
    return rows_out, meta


def top_table(rows: list[dict[str, Any]], depth: int, metric: str, title: str, args: argparse.Namespace) -> list[str]:
    candidates = [
        row for row in rows
        if row["depth"] == depth
        and row["metric"] == metric
        and row["stratum"] not in {"global", "source_state"}
        and row["samples"] >= args.min_samples
    ]
    ranked = sorted(
        candidates,
        key=lambda row: (row["contribution_fraction"], row["mean"], row["p95"]),
        reverse=True,
    )[:args.limit]
    lines = [
        "",
        f"### {title}",
        "",
        "| stratum | value | samples | mass | mean | p95 | max | contribution |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in ranked:
        lines.append(
            f"| `{row['stratum']}` | `{row['value']}` | {row['samples']} | "
            f"{row['mass_fraction']:.6g} | {row['mean']:.6g} | "
            f"{row['p95']:.6g} | {row['max']:.6g} | "
            f"{row['contribution_fraction']:.6g} |"
        )
    return lines


def build_report(args: argparse.Namespace, meta_rows: list[dict[str, Any]], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Z2 Oscillation Strata",
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
        f"- minimum stratum samples: `{args.min_samples}`",
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

    lines.extend([
        "",
        "## Global Full-Label Signals",
        "",
        "| depth | metric | samples | mean | p95 | max |",
        "|---:|---|---:|---:|---:|---:|",
    ])
    for row in rows:
        if row["stratum"] == "global" and row["metric"] in {"full_tv", "full_excess_over_phase"}:
            lines.append(
                f"| {row['depth']} | `{row['metric']}` | {row['samples']} | "
                f"{row['mean']:.6g} | {row['p95']:.6g} | {row['max']:.6g} |"
            )

    for depth in range(args.max_depth + 1):
        lines.extend([
            "",
            f"## Depth {depth}",
        ])
        lines.extend(top_table(rows, depth, "full_tv", "Top Full-TV Contributions", args))
        lines.extend(top_table(rows, depth, "full_excess_over_phase", "Top Full-Over-Phase Excess Contributions", args))

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "Concentration in structural strata supports an enlarged symbolic or",
        "drift-weighted model.  Diffuse contribution across broad strata",
        "pressures the analytic branch.  These finite rows still do not prove",
        "or disprove an infinite operator or a Banach-space estimate.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stratify 2-adic child-cylinder oscillation.")
    parser.add_argument("--T", default="15")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--tail-bits", type=int, default=3)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--min-samples", type=int, default=1024)
    parser.add_argument("--limit", type=int, default=12)
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
    print("  Z2 oscillation strata diagnostic")
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
