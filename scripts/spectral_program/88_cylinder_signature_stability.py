"""
88_cylinder_signature_stability.py

Gate-10.B diagnostic for high-bit cylinder stability.

This script does not compute spectral-radius bounds.  It asks whether the
first-return signature for lifts

    t = r + j * 2^T

is stable, Cauchy-like, or genuinely high-bit dependent as j grows.

It separates four signature levels:

  status: terminal vs return;
  phase:  destination phase only;
  delta:  bit-length weight exponent only;
  full:   existing CORE/TAIL signature (terminal or return,dst,delta).

The output is meant to decide which Phase-10 model remains plausible:
compact 2-adic phase space, enlarged symbolic state, countable episode
graph, finite-rank fallback, or inconclusive.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
OUT_GROUPS = ROOT / "collatz_88_cylinder_group_summary.csv"
OUT_DISTS = ROOT / "collatz_88_signature_distribution.csv"
OUT_DRIFT = ROOT / "collatz_88_block_drift.csv"
OUT_DECISION = ROOT / "collatz_88_decision_summary.md"


def output_paths(tag: str | None) -> tuple[Path, Path, Path, Path]:
    if tag is None:
        return OUT_GROUPS, OUT_DISTS, OUT_DRIFT, OUT_DECISION
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_88_{safe}"
    return (
        ROOT / f"{stem}_cylinder_group_summary.csv",
        ROOT / f"{stem}_signature_distribution.csv",
        ROOT / f"{stem}_block_drift.csv",
        ROOT / f"{stem}_decision_summary.md",
    )


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


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def fmt_state(state: tuple[int, int, int] | None) -> str:
    if state is None:
        return "terminal"
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def fmt_sig(sig) -> str:
    if sig is None:
        return "none"
    if isinstance(sig, tuple):
        return "|".join(str(x) for x in sig)
    return str(sig)


def signature(row: dict, level: str):
    if level == "status":
        return ("terminal",) if row["terminal"] else ("return",)
    if level == "phase":
        return ("terminal",) if row["terminal"] else ("return", *row["dst"])
    if level == "delta":
        return ("terminal",) if row["terminal"] else ("return", row["delta"])
    if level == "full":
        return row["signature"]
    raise ValueError(f"unknown signature level: {level}")


SIGNATURE_LEVELS = ("status", "phase", "delta", "full")


def distribution(rows: Iterable[dict], level: str) -> Counter:
    counts = Counter()
    for row in rows:
        counts[signature(row, level)] += 1
    return counts


def weighted_distribution(rows: Iterable[dict], level: str) -> Counter:
    weights = Counter()
    for row in rows:
        weights[signature(row, level)] += row["weight"]
    return weights


def total_variation(a: Counter, b: Counter) -> float:
    total_a = sum(a.values())
    total_b = sum(b.values())
    if total_a == 0 and total_b == 0:
        return 0.0
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a[k] / total_a - b[k] / total_b) for k in keys)


def majority(counts: Counter):
    if not counts:
        return None, 0, 0.0
    sig, count = counts.most_common(1)[0]
    total = sum(counts.values())
    return sig, count, count / total if total else 0.0


def source_phase_for_group(rows: list[dict]) -> tuple[int, int, int] | None:
    if not rows:
        return None
    return rows[0]["src"]


def boundary_flag(src: tuple[int, int, int] | None, T: int) -> str:
    if src is None:
        return "unknown"
    return "boundary" if src[0] >= T else "bulk"


def trace_rows_for_T(tail_mod, ctx, args: argparse.Namespace, T: int, max_j: int):
    op, shadowing, records, target, target_key, residue, modulus = ctx
    h_mod = 1 << args.hit_bits
    groups: dict[tuple[int, int], list[dict]] = defaultdict(list)
    total = (1 << T) * h_mod * max_j
    seen = 0
    progress_step = max(1, total // 20)

    for r in range(1 << T):
        for h in range(h_mod):
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
                groups[(r, h)].append(row)
                seen += 1
                if args.progress and seen % progress_step == 0:
                    print(f"    T={T}: traced {seen}/{total} rows")
    return groups


def summarize_window(
    *,
    T: int,
    r: int,
    h: int,
    mode: str,
    j_start: int,
    j_count: int,
    rows: list[dict],
) -> tuple[dict, list[dict]]:
    src = source_phase_for_group(rows)
    sample_count = len(rows)
    source_counts = Counter(row["src"] for row in rows)
    base = {
        "T": T,
        "r": r,
        "h": h,
        "mode": mode,
        "j_start": j_start,
        "j_count": j_count,
        "sample_count": sample_count,
        "source_phase": fmt_state(src),
        "source_state_count": len(source_counts),
        "source_state_mixed": int(len(source_counts) > 1),
        "source_states": " | ".join(
            f"{fmt_state(state)}:{count}" for state, count in source_counts.most_common()
        ),
        "boundary_flag": boundary_flag(src, T),
        "terminal_fraction": sum(1 for row in rows if row["terminal"]) / sample_count if sample_count else 0.0,
        "return_fraction": sum(1 for row in rows if not row["terminal"]) / sample_count if sample_count else 0.0,
        "full_weight": sum(row["weight"] for row in rows),
    }

    dist_rows = []
    summary = dict(base)
    for level in SIGNATURE_LEVELS:
        counts = distribution(rows, level)
        weights = weighted_distribution(rows, level)
        maj_sig, maj_count, maj_fraction = majority(counts)
        summary[f"distinct_{level}_count"] = len(counts)
        summary[f"{level}_majority_fraction"] = maj_fraction
        summary[f"dominant_{level}_signature"] = fmt_sig(maj_sig)
        for sig, count in counts.most_common():
            dist_rows.append({
                "T": T,
                "r": r,
                "h": h,
                "mode": mode,
                "j_start": j_start,
                "j_count": j_count,
                "sample_count": sample_count,
                "signature_level": level,
                "signature": fmt_sig(sig),
                "count": count,
                "fraction": count / sample_count if sample_count else 0.0,
                "weight_sum": weights[sig],
            })

    full_counts = distribution(rows, "full")
    full_major, _count, _frac = majority(full_counts)
    tail_rows = [row for row in rows if signature(row, "full") != full_major]
    tail_weight = sum(row["weight"] for row in tail_rows)
    full_weight = summary["full_weight"]
    summary["tail_count"] = len(tail_rows)
    summary["tail_weight"] = tail_weight
    summary["tail_weight_fraction"] = tail_weight / full_weight if full_weight else 0.0
    return summary, dist_rows


def prefix_rows(rows: list[dict], j_count: int) -> list[dict]:
    return [row for row in rows if row["j"] < j_count]


def block_rows(rows: list[dict], j_start: int, block_size: int) -> list[dict]:
    j_stop = j_start + block_size
    return [row for row in rows if j_start <= row["j"] < j_stop]


def adjacent_block_drifts(
    *,
    T: int,
    r: int,
    h: int,
    rows: list[dict],
    block_size: int,
    max_j: int,
) -> list[dict]:
    out = []
    starts = list(range(0, max_j - block_size + 1, block_size))
    for a_start, b_start in zip(starts, starts[1:]):
        a_rows = block_rows(rows, a_start, block_size)
        b_rows = block_rows(rows, b_start, block_size)
        if not a_rows or not b_rows:
            continue
        for level in SIGNATURE_LEVELS:
            dist_a = distribution(a_rows, level)
            dist_b = distribution(b_rows, level)
            dom_a, _ca, _fa = majority(dist_a)
            dom_b, _cb, _fb = majority(dist_b)
            out.append({
                "T": T,
                "r": r,
                "h": h,
                "signature_level": level,
                "block_a_start": a_start,
                "block_b_start": b_start,
                "block_size": block_size,
                "tv_distance": total_variation(dist_a, dist_b),
                "dominant_a": fmt_sig(dom_a),
                "dominant_b": fmt_sig(dom_b),
                "dominant_changed": int(dom_a != dom_b),
            })
    return out


def analyze_T(tail_mod, ctx, args: argparse.Namespace, T: int):
    j_counts = parse_csv_ints(args.j_counts)
    if not j_counts:
        raise ValueError("at least one j-count is required")
    max_j = max(j_counts)
    if args.block_size > max_j:
        raise ValueError("--block-size must be <= max(j-counts)")

    print(f"  T={T}: tracing high-bit cylinders up to j={max_j}")
    groups = trace_rows_for_T(tail_mod, ctx, args, T, max_j)

    group_rows = []
    dist_rows = []
    drift_rows = []
    for (r, h), rows in sorted(groups.items()):
        for j_count in j_counts:
            summary, distributions = summarize_window(
                T=T,
                r=r,
                h=h,
                mode="prefix",
                j_start=0,
                j_count=j_count,
                rows=prefix_rows(rows, j_count),
            )
            group_rows.append(summary)
            dist_rows.extend(distributions)

        for j_start in range(0, max_j, args.block_size):
            window = block_rows(rows, j_start, args.block_size)
            if len(window) != args.block_size:
                continue
            summary, distributions = summarize_window(
                T=T,
                r=r,
                h=h,
                mode="block",
                j_start=j_start,
                j_count=args.block_size,
                rows=window,
            )
            group_rows.append(summary)
            dist_rows.extend(distributions)

        drift_rows.extend(
            adjacent_block_drifts(
                T=T,
                r=r,
                h=h,
                rows=rows,
                block_size=args.block_size,
                max_j=max_j,
            )
        )
    return group_rows, dist_rows, drift_rows


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round(q * (len(ordered) - 1)))))
    return ordered[idx]


def summarize_decision(group_rows: list[dict], drift_rows: list[dict], args: argparse.Namespace) -> str:
    prefix_rows_all = [row for row in group_rows if row["mode"] == "prefix"]
    block_rows_all = [row for row in group_rows if row["mode"] == "block"]
    final_j = max(parse_csv_ints(args.j_counts))
    final_prefix = [row for row in prefix_rows_all if row["j_count"] == final_j]
    bulk_final = [row for row in final_prefix if row["boundary_flag"] == "bulk"]
    boundary_final = [row for row in final_prefix if row["boundary_flag"] == "boundary"]

    full_drifts = [row for row in drift_rows if row["signature_level"] == "full"]
    phase_drifts = [row for row in drift_rows if row["signature_level"] == "phase"]
    status_drifts = [row for row in drift_rows if row["signature_level"] == "status"]
    delta_drifts = [row for row in drift_rows if row["signature_level"] == "delta"]

    def avg(rows: list[dict], key: str) -> float:
        return sum(float(row[key]) for row in rows) / len(rows) if rows else 0.0

    def exact_fraction(rows: list[dict], key: str) -> float:
        return sum(1 for row in rows if float(row[key]) == 1.0) / len(rows) if rows else 0.0

    full_tv_values = [float(row["tv_distance"]) for row in full_drifts]
    phase_tv_values = [float(row["tv_distance"]) for row in phase_drifts]
    status_tv_values = [float(row["tv_distance"]) for row in status_drifts]
    delta_tv_values = [float(row["tv_distance"]) for row in delta_drifts]

    full_flip_fraction = avg(full_drifts, "dominant_changed")
    phase_flip_fraction = avg(phase_drifts, "dominant_changed")
    status_flip_fraction = avg(status_drifts, "dominant_changed")
    delta_flip_fraction = avg(delta_drifts, "dominant_changed")

    bulk_phase_exact = exact_fraction(bulk_final, "phase_majority_fraction")
    bulk_status_exact = exact_fraction(bulk_final, "status_majority_fraction")
    bulk_full_exact = exact_fraction(bulk_final, "full_majority_fraction")
    bulk_status_avg = avg(bulk_final, "status_majority_fraction")
    bulk_phase_avg = avg(bulk_final, "phase_majority_fraction")
    bulk_delta_avg = avg(bulk_final, "delta_majority_fraction")
    bulk_full_avg = avg(bulk_final, "full_majority_fraction")
    severe_phase_with_stable_status = [
        row for row in bulk_final
        if float(row["status_majority_fraction"]) == 1.0
        and float(row["phase_majority_fraction"]) <= 0.5
    ]
    boundary_share = len(boundary_final) / len(final_prefix) if final_prefix else 0.0

    top_full = sorted(full_drifts, key=lambda row: (-float(row["tv_distance"]), row["T"], row["r"], row["h"]))[:10]
    top_bulk_unstable = sorted(
        bulk_final,
        key=lambda row: (float(row["full_majority_fraction"]), float(row["phase_majority_fraction"]), row["r"], row["h"]),
    )[:10]

    status_tv_p95 = quantile(status_tv_values, 0.95)
    phase_tv_p95 = quantile(phase_tv_values, 0.95)
    delta_tv_p95 = quantile(delta_tv_values, 0.95)
    full_tv_p95 = quantile(full_tv_values, 0.95)

    recommendation = "inconclusive"
    if (
        bulk_status_avg > 0.995
        and bulk_phase_avg > 0.99
        and phase_tv_p95 < 0.05
        and phase_flip_fraction < 0.02
    ):
        recommendation = "continue Z_2 branch"
    elif bulk_status_avg > 0.99 and bulk_phase_avg > 0.98 and delta_tv_p95 >= 0.05:
        recommendation = "weighted operator trouble"
    elif severe_phase_with_stable_status or (bulk_status_avg > 0.94 and bulk_phase_exact < 0.90):
        recommendation = "enlarge symbolic state"
    elif bulk_status_avg < 0.90 or status_tv_p95 > 0.25:
        recommendation = "killed-domain trouble"
    if full_tv_p95 > 0.25 and full_flip_fraction > 0.10:
        recommendation = "switch to countable episode graph or finite-rank fallback"

    lines = [
        "# Cylinder Signature Stability Decision Summary",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- T values: `{args.T}`",
        f"- j-counts: `{args.j_counts}`",
        f"- block size: `{args.block_size}`",
        f"- odd bits: `{args.odd_bits}`",
        f"- hit bits: `{args.hit_bits}`",
        f"- v2 cap: `{args.v2_cap}`",
        f"- max steps: `{args.max_steps}`",
        f"- include t=0: `{args.include_t_zero}`",
        "",
        "## Aggregate Signals",
        "",
        f"- final prefix j_count: `{final_j}`",
        f"- final prefix groups: `{len(final_prefix)}`",
        f"- boundary group share: `{boundary_share:.6g}`",
        f"- bulk exact status-majority fraction: `{bulk_status_exact:.6g}`",
        f"- bulk exact phase-majority fraction: `{bulk_phase_exact:.6g}`",
        f"- bulk exact full-majority fraction: `{bulk_full_exact:.6g}`",
        f"- bulk average status-majority fraction: `{bulk_status_avg:.6g}`",
        f"- bulk average phase-majority fraction: `{bulk_phase_avg:.6g}`",
        f"- bulk average delta-majority fraction: `{bulk_delta_avg:.6g}`",
        f"- bulk average full-majority fraction: `{bulk_full_avg:.6g}`",
        f"- stable-status bulk groups with phase majority <= 0.5: `{len(severe_phase_with_stable_status)}`",
        f"- status dominant flip fraction across adjacent blocks: `{status_flip_fraction:.6g}`",
        f"- phase dominant flip fraction across adjacent blocks: `{phase_flip_fraction:.6g}`",
        f"- delta dominant flip fraction across adjacent blocks: `{delta_flip_fraction:.6g}`",
        f"- full dominant flip fraction across adjacent blocks: `{full_flip_fraction:.6g}`",
        f"- status TV p95: `{status_tv_p95:.6g}`",
        f"- phase TV p95: `{phase_tv_p95:.6g}`",
        f"- delta TV p95: `{delta_tv_p95:.6g}`",
        f"- full TV p95: `{full_tv_p95:.6g}`",
        "",
        "## Preliminary Recommendation",
        "",
        f"`{recommendation}`",
        "",
        "This recommendation is a modeling diagnostic only.  It does not imply",
        "Conjecture 6, an infinite-operator bound, a Lasota-Yorke inequality,",
        "Keller-Liverani convergence, or a spectral gap.",
        "",
        "## Worst Adjacent-Block Full-Signature Drifts",
        "",
        "| T | r | h | block A | block B | TV | dominant A | dominant B | changed |",
        "|---:|---:|---:|---:|---:|---:|---|---|---:|",
    ]
    for row in top_full:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | {row['block_a_start']} | "
            f"{row['block_b_start']} | {float(row['tv_distance']):.6g} | "
            f"`{row['dominant_a']}` | `{row['dominant_b']}` | {row['dominant_changed']} |"
        )

    lines.extend([
        "",
        "## Worst Bulk Final-Prefix Groups",
        "",
        "| T | r | h | source phase | status maj | phase maj | delta maj | full maj | full tail weight fraction |",
        "|---:|---:|---:|---|---:|---:|---:|---:|---:|",
    ])
    for row in top_bulk_unstable:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | `{row['source_phase']}` | "
            f"{float(row['status_majority_fraction']):.6g} | "
            f"{float(row['phase_majority_fraction']):.6g} | "
            f"{float(row['delta_majority_fraction']):.6g} | "
            f"{float(row['full_majority_fraction']):.6g} | "
            f"{float(row['tail_weight_fraction']):.6g} |"
        )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gate-10.B cylinder signature stability diagnostic.")
    parser.add_argument("--T", default="8")
    parser.add_argument("--j-counts", default="16,32")
    parser.add_argument("--block-size", type=int, default=16)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument(
        "--include-t-zero",
        action="store_true",
        help="include the single lift t=0; by default it is skipped as a 2-adic zero-mass artifact",
    )
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output-tag", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    ctx = tail_mod.setup()

    all_group_rows = []
    all_dist_rows = []
    all_drift_rows = []

    print("=" * 118)
    print("  Cylinder signature stability diagnostic")
    print("=" * 118)
    print(f"  T={args.T}, j_counts={args.j_counts}, block_size={args.block_size}")
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, v2_cap={args.v2_cap}")
    print(f"  include_t_zero={args.include_t_zero}")
    print("  No spectral-radius bounds are computed.")

    for T in parse_csv_ints(args.T):
        group_rows, dist_rows, drift_rows = analyze_T(tail_mod, ctx, args, T)
        all_group_rows.extend(group_rows)
        all_dist_rows.extend(dist_rows)
        all_drift_rows.extend(drift_rows)
        final_j = max(parse_csv_ints(args.j_counts))
        final_prefix = [row for row in group_rows if row["mode"] == "prefix" and row["j_count"] == final_j]
        bulk = [row for row in final_prefix if row["boundary_flag"] == "bulk"]
        bulk_exact_phase = (
            sum(1 for row in bulk if row["phase_majority_fraction"] == 1.0) / len(bulk)
            if bulk else 0.0
        )
        print(
            f"  T={T}: groups={len(final_prefix)}, bulk={len(bulk)}, "
            f"bulk exact phase={bulk_exact_phase:.6g}, drift rows={len(drift_rows)}"
        )

    out_groups, out_dists, out_drift, out_decision = output_paths(args.output_tag)
    write_csv(all_group_rows, out_groups)
    write_csv(all_dist_rows, out_dists)
    write_csv(all_drift_rows, out_drift)
    out_decision.write_text(summarize_decision(all_group_rows, all_drift_rows, args), encoding="utf-8")

    print("\n  Output:")
    print(f"    {out_groups.name}")
    print(f"    {out_dists.name}")
    print(f"    {out_drift.name}")
    print(f"    {out_decision.name}")


if __name__ == "__main__":
    main()
