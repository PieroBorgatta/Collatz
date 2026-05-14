"""
100_z2_cylinder_oscillation.py

Finite diagnostic for genuine 2-adic high-bit cylinder oscillation.

Script 88 compares contiguous ordinary intervals in the high-bit lift
coordinate j.  This script instead fixes a parent class j mod 2^d and
compares its two 2-adic children:

    j = q + 2^d * (2 ell)
    j = q + 2^d * (2 ell + 1).

The output is a finite diagnostic only.  It is not a theorem, not a
mixed-norm convergence statement, and not a spectral-radius estimate.
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
OUT_REPORT = ROOT / "collatz_100_z2_cylinder_oscillation.md"
OUT_CSV = ROOT / "collatz_100_z2_cylinder_oscillation.csv"

SIGNATURE_LEVELS = ("status", "phase", "delta", "full")


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_CSV
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_100_{safe}_z2_cylinder_oscillation"
    return ROOT / f"{stem}.md", ROOT / f"{stem}.csv"


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


def fmt_sig(sig) -> str:
    if sig is None:
        return "none"
    if isinstance(sig, tuple):
        return "|".join(str(x) for x in sig)
    return str(sig)


def signature(row: dict[str, Any], level: str):
    if level == "status":
        return ("terminal",) if row["terminal"] else ("return",)
    if level == "phase":
        return ("terminal",) if row["terminal"] else ("return", *row["dst"])
    if level == "delta":
        return ("terminal",) if row["terminal"] else ("return", row["delta"])
    if level == "full":
        return row["signature"]
    raise ValueError(f"unknown signature level: {level}")


def distribution(rows: Iterable[dict[str, Any]], level: str) -> Counter:
    counts = Counter()
    for row in rows:
        counts[signature(row, level)] += 1
    return counts


def total_variation(a: Counter, b: Counter) -> float:
    total_a = sum(a.values())
    total_b = sum(b.values())
    if total_a == 0 and total_b == 0:
        return 0.0
    if total_a == 0 or total_b == 0:
        return 1.0
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a[key] / total_a - b[key] / total_b) for key in keys)


def majority(counts: Counter):
    if not counts:
        return None
    return counts.most_common(1)[0][0]


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


def trace_rows_for_group(
    *,
    tail_mod,
    ctx,
    args: argparse.Namespace,
    T: int,
    r: int,
    h: int,
    max_j: int,
) -> list[dict[str, Any]]:
    op, shadowing, records, target, target_key, residue, modulus = ctx
    rows = []
    for j in range(max_j):
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
        row.update({"T": T, "r": r, "h": h, "j": j, "t": t})
        rows.append(row)
    return rows


def child_rows(rows: list[dict[str, Any]], depth: int, q: int, child: int) -> list[dict[str, Any]]:
    return [
        row for row in rows
        if row["j"] % (1 << depth) == q and ((row["j"] >> depth) & 1) == child
    ]


def summarize_pair(
    *,
    T: int,
    r: int,
    h: int,
    depth: int,
    q: int,
    rows0: list[dict[str, Any]],
    rows1: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    out = []
    for level in SIGNATURE_LEVELS:
        dist0 = distribution(rows0, level)
        dist1 = distribution(rows1, level)
        dom0 = majority(dist0)
        dom1 = majority(dist1)
        out.append({
            "T": T,
            "r": r,
            "h": h,
            "depth": depth,
            "parent_q": q,
            "signature_level": level,
            "child0_count": len(rows0),
            "child1_count": len(rows1),
            "tv_distance": total_variation(dist0, dist1),
            "dominant_0": fmt_sig(dom0),
            "dominant_1": fmt_sig(dom1),
            "dominant_changed": int(dom0 != dom1),
        })
    return out


def analyze_T(tail_mod, ctx, args: argparse.Namespace, T: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    h_mod = 1 << args.hit_bits
    max_j = 1 << (args.max_depth + 1 + args.tail_bits)
    pair_rows: list[dict[str, Any]] = []
    total_groups = (1 << T) * h_mod
    seen = 0
    progress_step = max(1, total_groups // 20)

    for r in range(1 << T):
        for h in range(h_mod):
            rows = trace_rows_for_group(
                tail_mod=tail_mod,
                ctx=ctx,
                args=args,
                T=T,
                r=r,
                h=h,
                max_j=max_j,
            )
            for depth in range(args.max_depth + 1):
                for q in range(1 << depth):
                    rows0 = child_rows(rows, depth, q, 0)
                    rows1 = child_rows(rows, depth, q, 1)
                    if not rows0 or not rows1:
                        continue
                    pair_rows.extend(
                        summarize_pair(
                            T=T,
                            r=r,
                            h=h,
                            depth=depth,
                            q=q,
                            rows0=rows0,
                            rows1=rows1,
                        )
                    )
            seen += 1
            if args.progress and seen % progress_step == 0:
                print(f"    T={T}: processed {seen}/{total_groups} source groups")

    meta = {
        "T": T,
        "max_j": max_j,
        "source_groups": total_groups,
        "pair_rows": len(pair_rows),
    }
    return pair_rows, meta


def aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    values: dict[tuple[int, str], list[float]] = defaultdict(list)
    flips: Counter = Counter()
    counts: Counter = Counter()
    child0_counts: dict[tuple[int, str], list[int]] = defaultdict(list)
    child1_counts: dict[tuple[int, str], list[int]] = defaultdict(list)

    for row in rows:
        key = (int(row["depth"]), str(row["signature_level"]))
        values[key].append(float(row["tv_distance"]))
        flips[key] += int(row["dominant_changed"])
        counts[key] += 1
        child0_counts[key].append(int(row["child0_count"]))
        child1_counts[key].append(int(row["child1_count"]))

    out = []
    level_order = {level: i for i, level in enumerate(SIGNATURE_LEVELS)}
    for key in sorted(values, key=lambda item: (item[0], level_order[item[1]])):
        depth, level = key
        vals = values[key]
        out.append({
            "depth": depth,
            "signature_level": level,
            "mean_tv": mean(vals) if vals else 0.0,
            "p95_tv": quantile(vals, 0.95),
            "p99_tv": quantile(vals, 0.99),
            "max_tv": max(vals) if vals else 0.0,
            "dominant_flip_fraction": flips[key] / counts[key] if counts[key] else 0.0,
            "samples": counts[key],
            "child0_min_count": min(child0_counts[key]) if child0_counts[key] else 0,
            "child1_min_count": min(child1_counts[key]) if child1_counts[key] else 0,
        })
    return out


def build_report(args: argparse.Namespace, meta_rows: list[dict[str, Any]], aggregate: list[dict[str, Any]]) -> str:
    lines = [
        "# Z2 Cylinder Oscillation Diagnostic",
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
        f"- max steps: `{args.max_steps}`",
        f"- include t=0: `{args.include_t_zero}`",
        "",
        "For each depth `d`, this compares the two children inside a fixed",
        "high-bit parent class `j mod 2^d`.  This is closer to a 2-adic",
        "martingale oscillation test than adjacent ordinary `j` intervals.",
        "",
        "## Trace Meta",
        "",
        "| T | max j | source groups | pair rows |",
        "|---:|---:|---:|---:|",
    ]
    for meta in meta_rows:
        lines.append(
            f"| {meta['T']} | {meta['max_j']} | {meta['source_groups']} | {meta['pair_rows']} |"
        )

    lines.extend([
        "",
        "## Aggregates",
        "",
        "| depth | level | mean TV | p95 TV | p99 TV | max TV | dominant flip | samples | min child counts |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ])
    for row in aggregate:
        lines.append(
            f"| {row['depth']} | `{row['signature_level']}` | "
            f"{row['mean_tv']:.6g} | {row['p95_tv']:.6g} | "
            f"{row['p99_tv']:.6g} | {row['max_tv']:.6g} | "
            f"{row['dominant_flip_fraction']:.6g} | {row['samples']} | "
            f"{row['child0_min_count']}/{row['child1_min_count']} |"
        )

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "Small values here would support a 2-adic weak/martingale norm.",
        "Large or nondecreasing values would pressure the analytic branch.",
        "Either way, these are finite sampled oscillations, not proof of",
        "continuity, compactness, Lasota-Yorke, or Keller-Liverani",
        "convergence.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="2-adic high-bit cylinder oscillation diagnostic.")
    parser.add_argument("--T", default="15")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--tail-bits", type=int, default=2)
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
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()
    all_pair_rows: list[dict[str, Any]] = []
    meta_rows = []

    print("=" * 118)
    print("  Z2 cylinder oscillation diagnostic")
    print("=" * 118)
    print(f"  T={args.T}, max_depth={args.max_depth}, tail_bits={args.tail_bits}")
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, v2_cap={args.v2_cap}")
    print("  No spectral-radius bounds are computed.")

    for T in parse_csv_ints(args.T):
        pair_rows, meta = analyze_T(tail_mod, ctx, args, T)
        all_pair_rows.extend(pair_rows)
        meta_rows.append(meta)
        print(
            f"  T={T}: max_j={meta['max_j']}, source groups={meta['source_groups']}, "
            f"pair rows={meta['pair_rows']}"
        )

    aggregate = aggregate_rows(all_pair_rows)
    report_path, csv_path = output_paths(args.output_tag)
    report_path.write_text(build_report(args, meta_rows, aggregate), encoding="utf-8")
    write_csv(aggregate, csv_path)

    print("\n  Output:")
    print(f"    {report_path.name}")
    print(f"    {csv_path.name}")


if __name__ == "__main__":
    main()
