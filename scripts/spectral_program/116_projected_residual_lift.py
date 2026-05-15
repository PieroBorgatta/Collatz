#!/usr/bin/env python3
"""
Projected residual lift test for the dst_v2 LY repair.

Script 115 measured the optimistic proxy

    residual_proxy = TV(phase) - TV(dst_v2).

This script measures signed residuals after choosing an actual lift
inside each dst_v2 fiber.  It tests whether the candidate decomposition

    U = U Pi_v2 + U Q_v2

has a small residual at the finite child-cylinder level.

Lift choices:
- pair_pooled: eta_z is the pooled child distribution in each pair;
  this is optimistic and pair-dependent;
- uniform: eta_z is uniform on the finite phase fiber;
- global_pooled: optional two-pass lift, eta_z is pooled over all pairs
  at the same depth;
- source_pooled: optional two-pass lift, eta_{source,z} is pooled over
  all pairs at the same depth and finite source PhaseState.

This is finite diagnostic output only.  It does not prove an infinite
operator, Lasota-Yorke, Hennion, Keller-Liverani, a spectral gap, or
Collatz.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_116_projected_residual_lift_report.md"
OUT_CSV = ROOT / "collatz_116_projected_residual_lift.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ints(text: str) -> list[int]:
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_CSV
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_116_{safe}_projected_residual_lift"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}.csv"


def phase_key(row: dict[str, Any]) -> tuple[Any, ...]:
    if row["terminal"]:
        return ("terminal",)
    v2, odd, h = row["dst"]
    return ("return", v2, odd, h)


def v2_key_from_phase(key: tuple[Any, ...]) -> tuple[Any, ...]:
    if key[0] == "terminal":
        return ("terminal",)
    return ("return", key[1])


def distribution(rows: Iterable[dict[str, Any]]) -> dict[tuple[Any, ...], float]:
    counts = Counter(phase_key(row) for row in rows)
    total = sum(counts.values())
    if total == 0:
        return {}
    return {key: count / total for key, count in counts.items()}


def push_v2(dist: dict[tuple[Any, ...], float]) -> dict[tuple[Any, ...], float]:
    out: dict[tuple[Any, ...], float] = defaultdict(float)
    for key, value in dist.items():
        out[v2_key_from_phase(key)] += value
    return dict(out)


def l1_tv(a: dict[tuple[Any, ...], float], b: dict[tuple[Any, ...], float]) -> float:
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(key, 0.0) - b.get(key, 0.0)) for key in keys)


def pooled_eta(
    p0: dict[tuple[Any, ...], float],
    p1: dict[tuple[Any, ...], float],
) -> dict[tuple[Any, ...], dict[tuple[Any, ...], float]]:
    totals: dict[tuple[Any, ...], dict[tuple[Any, ...], float]] = defaultdict(lambda: defaultdict(float))
    for dist in (p0, p1):
        for y, value in dist.items():
            totals[v2_key_from_phase(y)][y] += value
    out: dict[tuple[Any, ...], dict[tuple[Any, ...], float]] = {}
    for z, fiber in totals.items():
        total = sum(fiber.values())
        if total:
            out[z] = {y: value / total for y, value in fiber.items()}
    return out


def uniform_eta(v2_cap: int, hit_bits: int) -> dict[tuple[Any, ...], dict[tuple[Any, ...], float]]:
    h_mod = 1 << hit_bits
    out: dict[tuple[Any, ...], dict[tuple[Any, ...], float]] = {
        ("terminal",): {("terminal",): 1.0}
    }
    for v2 in range(v2_cap + 1):
        fiber = [("return", v2, odd, h) for odd in (1, 3) for h in range(h_mod)]
        mass = 1.0 / len(fiber)
        out[("return", v2)] = {y: mass for y in fiber}
    return out


def residual_tv(
    p0: dict[tuple[Any, ...], float],
    p1: dict[tuple[Any, ...], float],
    eta: dict[tuple[Any, ...], dict[tuple[Any, ...], float]],
) -> float:
    delta_y: dict[tuple[Any, ...], float] = defaultdict(float)
    for y, value in p0.items():
        delta_y[y] += value
    for y, value in p1.items():
        delta_y[y] -= value

    delta_z: dict[tuple[Any, ...], float] = defaultdict(float)
    for y, value in delta_y.items():
        delta_z[v2_key_from_phase(y)] += value

    residual = dict(delta_y)
    for z, dz in delta_z.items():
        for y, weight in eta.get(z, {}).items():
            residual[y] = residual.get(y, 0.0) - dz * weight

    return 0.5 * sum(abs(value) for value in residual.values())


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


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "mean": mean(values) if values else 0.0,
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
    }


def source_key(rows: list[dict[str, Any]]) -> tuple[Any, ...]:
    counts = Counter(row["src"] for row in rows)
    return counts.most_common(1)[0][0]


def iter_pairs(z2, tail_mod, ctx, args: argparse.Namespace, T: int):
    h_mod = 1 << args.hit_bits
    max_j = 1 << (args.max_depth + 1 + args.tail_bits)
    total_groups = (1 << T) * h_mod
    progress_step = max(1, total_groups // 20)
    seen = 0
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
            src = source_key(rows)
            for depth in range(args.max_depth + 1):
                for q in range(1 << depth):
                    rows0 = z2.child_rows(rows, depth, q, 0)
                    rows1 = z2.child_rows(rows, depth, q, 1)
                    if not rows0 or not rows1:
                        continue
                    yield depth, src, distribution(rows0), distribution(rows1)
            seen += 1
            if args.progress and seen % progress_step == 0:
                print(f"    T={T}: processed {seen}/{total_groups} source groups")


def build_global_eta(z2, tail_mod, ctx, args: argparse.Namespace, T: int):
    totals: dict[int, dict[tuple[Any, ...], dict[tuple[Any, ...], float]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(float))
    )
    for depth, _src, p0, p1 in iter_pairs(z2, tail_mod, ctx, args, T):
        for dist in (p0, p1):
            for y, value in dist.items():
                totals[depth][v2_key_from_phase(y)][y] += value
    out: dict[int, dict[tuple[Any, ...], dict[tuple[Any, ...], float]]] = {}
    for depth, z_map in totals.items():
        out[depth] = {}
        for z, fiber in z_map.items():
            total = sum(fiber.values())
            if total:
                out[depth][z] = {y: value / total for y, value in fiber.items()}
    return out


def build_source_eta(z2, tail_mod, ctx, args: argparse.Namespace, T: int):
    totals: dict[int, dict[tuple[Any, ...], dict[tuple[Any, ...], dict[tuple[Any, ...], float]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    )
    for depth, src, p0, p1 in iter_pairs(z2, tail_mod, ctx, args, T):
        for dist in (p0, p1):
            for y, value in dist.items():
                totals[depth][src][v2_key_from_phase(y)][y] += value
    out: dict[int, dict[tuple[Any, ...], dict[tuple[Any, ...], dict[tuple[Any, ...], float]]]] = {}
    for depth, src_map in totals.items():
        out[depth] = {}
        for src, z_map in src_map.items():
            out[depth][src] = {}
            for z, fiber in z_map.items():
                total = sum(fiber.values())
                if total:
                    out[depth][src][z] = {y: value / total for y, value in fiber.items()}
    return out


def analyze_T(z2, tail_mod, ctx, args: argparse.Namespace, T: int):
    eta_uniform = uniform_eta(args.v2_cap, args.hit_bits)
    eta_global = build_global_eta(z2, tail_mod, ctx, args, T) if args.global_lift else {}
    eta_source = build_source_eta(z2, tail_mod, ctx, args, T) if args.source_lift else {}
    metrics: dict[tuple[int, str], list[float]] = defaultdict(list)
    samples: Counter[int] = Counter()

    for depth, src, p0, p1 in iter_pairs(z2, tail_mod, ctx, args, T):
        phase_tv = l1_tv(p0, p1)
        v2_tv = l1_tv(push_v2(p0), push_v2(p1))
        eta_pair = pooled_eta(p0, p1)
        values = {
            "phase_tv": phase_tv,
            "dst_v2_tv": v2_tv,
            "proxy_residual": max(0.0, phase_tv - v2_tv),
            "pair_pooled_residual": residual_tv(p0, p1, eta_pair),
            "uniform_residual": residual_tv(p0, p1, eta_uniform),
        }
        if args.global_lift:
            values["global_pooled_residual"] = residual_tv(p0, p1, eta_global.get(depth, {}))
        if args.source_lift:
            values["source_pooled_residual"] = residual_tv(
                p0,
                p1,
                eta_source.get(depth, {}).get(src, {}),
            )
        for name, value in values.items():
            metrics[(depth, name)].append(value)
        samples[depth] += 1

    rows_out: list[dict[str, Any]] = []
    for depth in range(args.max_depth + 1):
        phase_mean = summarize(metrics[(depth, "phase_tv")])["mean"]
        for metric in sorted(name for d, name in metrics if d == depth):
            summary = summarize(metrics[(depth, metric)])
            rows_out.append({
                "T": T,
                "depth": depth,
                "metric": metric,
                "mean": summary["mean"],
                "p95": summary["p95"],
                "p99": summary["p99"],
                "max": summary["max"],
                "phase_mean": phase_mean,
                "relative_to_phase_mean": summary["mean"] / phase_mean if phase_mean else 0.0,
                "samples": samples[depth],
            })
    meta = {
        "T": T,
        "max_j": 1 << (args.max_depth + 1 + args.tail_bits),
        "source_groups": (1 << T) * (1 << args.hit_bits),
        "samples": sum(samples.values()),
        "global_lift": args.global_lift,
        "source_lift": args.source_lift,
    }
    return rows_out, meta


def build_report(args: argparse.Namespace, meta_rows: list[dict[str, Any]], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Projected Residual Lift Test",
        "",
        "Status: finite diagnostic output only.  This report measures signed",
        "residuals after removing the destination-v2 low mode with explicit",
        "fiber lifts.  It does not prove Lasota-Yorke, Hennion,",
        "Keller-Liverani, a spectral gap, or Collatz.",
        "",
        "## Inputs",
        "",
        f"- T values: `{args.T}`",
        f"- max depth: `{args.max_depth}`",
        f"- tail bits: `{args.tail_bits}`",
        f"- global lift: `{args.global_lift}`",
        f"- source lift: `{args.source_lift}`",
        "",
        "## Trace Meta",
        "",
        "| T | max j | source groups | child-pair samples | global lift | source lift |",
        "|---:|---:|---:|---:|---|---|",
    ]
    for meta in meta_rows:
        lines.append(
            f"| {meta['T']} | {meta['max_j']} | {meta['source_groups']} | "
            f"{meta['samples']} | `{meta['global_lift']}` | `{meta['source_lift']}` |"
        )

    metric_order = {
        "phase_tv": 0,
        "dst_v2_tv": 1,
        "proxy_residual": 2,
        "pair_pooled_residual": 3,
        "global_pooled_residual": 4,
        "source_pooled_residual": 5,
        "uniform_residual": 6,
    }
    lines.extend([
        "",
        "## Residual Summary",
        "",
        "| depth | metric | mean | p95 | max | relative mean |",
        "|---:|---|---:|---:|---:|---:|",
    ])
    for row in sorted(rows, key=lambda r: (int(r["depth"]), metric_order.get(r["metric"], 99))):
        lines.append(
            f"| {row['depth']} | `{row['metric']}` | "
            f"{row['mean']:.6g} | {row['p95']:.6g} | {row['max']:.6g} | "
            f"{row['relative_to_phase_mean']:.6g} |"
        )

    lines.extend([
        "",
        "## Reading",
        "",
        "`proxy_residual` is the script-115 quantity `TV_phase - TV_dst_v2`.",
        "`pair_pooled_residual` is an optimistic signed residual using a",
        "pair-dependent lift inside each dst_v2 fiber.  `global_pooled`",
        "uses one lift per depth.  `source_pooled` uses one lift per depth",
        "and finite source PhaseState.  `uniform_residual` uses a fixed",
        "uniform lift and is a pessimistic sanity check.  If only the",
        "pair-pooled residual is small, the repair is not yet canonical.",
        "If the source-pooled residual is small, a finite source-conditioned",
        "low-mode operator becomes a plausible next target.",
        "",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", default="15")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--tail-bits", type=int, default=3)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--include-t-zero", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--global-lift", action="store_true")
    parser.add_argument("--source-lift", action="store_true")
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    z2 = load_module("100_z2_cylinder_oscillation.py", "z2_cylinder")
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()
    all_rows: list[dict[str, Any]] = []
    meta_rows: list[dict[str, Any]] = []

    print("=" * 118)
    print("  Projected residual lift test")
    print("=" * 118)
    print(
        f"  T={args.T}, max_depth={args.max_depth}, tail_bits={args.tail_bits}, "
        f"global_lift={args.global_lift}, source_lift={args.source_lift}"
    )

    for T in parse_csv_ints(args.T):
        rows, meta = analyze_T(z2, tail_mod, ctx, args, T)
        all_rows.extend(rows)
        meta_rows.append(meta)
        print(
            f"  T={T}: max_j={meta['max_j']}, source groups={meta['source_groups']}, "
            f"samples={meta['samples']}"
        )

    report_path, csv_path = output_paths(args.output_tag)
    write_csv(all_rows, csv_path)
    report_path.write_text(build_report(args, meta_rows, all_rows), encoding="utf-8")
    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {csv_path.name}")


if __name__ == "__main__":
    main()
