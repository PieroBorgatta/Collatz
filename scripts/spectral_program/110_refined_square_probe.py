"""
110_refined_square_probe.py

Finite smoke test for the A1 refined-source branch.

Scripts 108 and 109 show that adding low source-residue bits improves
source collapse but does not by itself produce a square transfer matrix:
the existing CSVs record only destination PhaseState.  This script
retraces a finite window and records destination low residue bits too,
so that it can build square kernels on

  (PhaseState, t mod 2^b) -> (PhaseState, next_t mod 2^b).

This is a finite diagnostic only.  It is not a spectral theorem, not a
Gate-10.B closure, and not a replacement for the existing Lean FULL
objects.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_REPORT = ROOT / "collatz_110_refined_square_probe_report.md"
OUT_BY_PAIR = ROOT / "collatz_110_refined_square_probe_by_pair.csv"


def output_paths(tag: str | None) -> tuple[Path, Path]:
    if tag is None:
        return OUT_REPORT, OUT_BY_PAIR
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag)
    stem = f"collatz_110_{safe}_refined_square_probe"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_by_pair.csv"


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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


def weighted_quantile(pairs: list[tuple[float, float]], q: float) -> float:
    positive = sorted((value, weight) for value, weight in pairs if weight > 0.0)
    if not positive:
        return 0.0
    total = sum(weight for _value, weight in positive)
    threshold = q * total
    running = 0.0
    for value, weight in positive:
        running += weight
        if running >= threshold:
            return value
    return positive[-1][0]


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "mean": mean(values) if values else 0.0,
        "median": median(values) if values else 0.0,
        "p95": quantile(values, 0.95),
        "p99": quantile(values, 0.99),
        "max": max(values) if values else 0.0,
    }


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


def fmt_phase(state: tuple[int, int, int] | None) -> str:
    if state is None:
        return "terminal"
    return f"{state[0]}|{state[1]}|{state[2]}"


def refined_key(state: tuple[int, int, int], t: int, bits: int) -> str:
    if bits <= 0:
        return fmt_phase(state)
    return f"{fmt_phase(state)}|rlo{bits}={t % (1 << bits)}"


def l1_diff(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    return sum(abs(float(a.get(key, 0.0)) - float(b.get(key, 0.0))) for key in keys)


def trace_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    tail_mod = load_module("77_high_bit_tail_bound.py", "high_bit_tail")
    op, shadowing, records, target, target_key, residue, modulus = tail_mod.setup()
    h_mod = 1 << args.hit_bits
    j_counts = parse_csv_ints(args.j_counts)
    max_j = max(j_counts)
    rows: list[dict[str, Any]] = []
    total = (1 << args.T) * h_mod * max_j
    progress_step = max(1, total // 20)
    seen = 0
    for r in range(1 << args.T):
        for h in range(h_mod):
            for j in range(max_j):
                t = r + (j << args.T)
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
                row.update({"T": args.T, "r": r, "h": h, "j": j, "t": t})
                rows.append(row)
                seen += 1
                if args.progress and seen % progress_step == 0:
                    print(f"traced {seen}/{total}")
    return rows


def kernel_for(rows: list[dict[str, Any]], *, j_count: int, bits: int) -> dict[str, dict[str, Any]]:
    source_counts: Counter[str] = Counter()
    terminal_counts: Counter[str] = Counter()
    return_weight: Counter[str] = Counter()
    edges: dict[str, Counter[str]] = defaultdict(Counter)

    for row in rows:
        if int(row["j"]) >= j_count:
            continue
        src_key = refined_key(row["src"], int(row["t"]), bits)
        source_counts[src_key] += 1
        if row["terminal"]:
            terminal_counts[src_key] += 1
            continue
        next_t = row.get("next_t")
        if next_t is None:
            raise ValueError("nonterminal row is missing next_t")
        dst_key = refined_key(row["dst"], int(next_t), bits)
        weight = float(row["weight"])
        edges[src_key][dst_key] += weight
        return_weight[src_key] += weight

    out: dict[str, dict[str, Any]] = {}
    for src_key, count in source_counts.items():
        denom = float(count)
        out[src_key] = {
            "row": {dst: weight / denom for dst, weight in edges[src_key].items()},
            "sample_count": count,
            "terminal_fraction": terminal_counts[src_key] / denom if denom else 0.0,
            "weighted_return_mass": return_weight[src_key] / denom if denom else 0.0,
        }
    return out


def score_pair(rows: list[dict[str, Any]], *, bits: int, left: int, right: int) -> dict[str, Any]:
    k_left = kernel_for(rows, j_count=left, bits=bits)
    k_right = kernel_for(rows, j_count=right, bits=bits)
    common = sorted(set(k_left) & set(k_right))
    diffs = [l1_diff(k_left[key]["row"], k_right[key]["row"]) for key in common]
    weights = [
        0.5 * (float(k_left[key]["sample_count"]) + float(k_right[key]["sample_count"]))
        for key in common
    ]
    total_weight = sum(weights)
    weighted_pairs = list(zip(diffs, weights, strict=True))
    weighted_mean = (
        sum(diff * weight for diff, weight in weighted_pairs) / total_weight
        if total_weight
        else 0.0
    )
    sizes_left = [float(item["sample_count"]) for item in k_left.values()]
    sizes_right = [float(item["sample_count"]) for item in k_right.values()]
    row: dict[str, Any] = {
        "bits": bits,
        "j_left": left,
        "j_right": right,
        "source_keys_left": len(k_left),
        "source_keys_right": len(k_right),
        "common_source_keys": len(common),
        "missing_left_keys": len(set(k_right) - set(k_left)),
        "missing_right_keys": len(set(k_left) - set(k_right)),
        "mean_samples_per_key_left": mean(sizes_left) if sizes_left else 0.0,
        "mean_samples_per_key_right": mean(sizes_right) if sizes_right else 0.0,
        "median_samples_per_key_left": median(sizes_left) if sizes_left else 0.0,
        "median_samples_per_key_right": median(sizes_right) if sizes_right else 0.0,
        "weighted_l1_mean": weighted_mean,
        "weighted_l1_p95": weighted_quantile(weighted_pairs, 0.95),
        "weighted_l1_p99": weighted_quantile(weighted_pairs, 0.99),
        "weighted_l1_max": max(diffs) if diffs else 0.0,
    }
    for key, value in summarize(diffs).items():
        row[f"key_l1_{key}"] = value
    return row


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.9g}"
    return str(value)


def write_report(
    *,
    rows: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    args: argparse.Namespace,
    path: Path,
) -> None:
    terminal = sum(1 for row in rows if row["terminal"])
    returned = len(rows) - terminal
    lines: list[str] = []
    lines.append("# Refined Square Kernel Probe")
    lines.append("")
    lines.append("Status: finite smoke diagnostic only.  This report does not")
    lines.append("close Gate 10.B and does not define an infinite operator.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- T: `{args.T}`")
    lines.append(f"- j-counts: `{args.j_counts}`")
    lines.append(f"- refine bits: `{args.refine_bits}`")
    lines.append(f"- odd bits: `{args.odd_bits}`")
    lines.append(f"- hit bits: `{args.hit_bits}`")
    lines.append(f"- v2 cap: `{args.v2_cap}`")
    lines.append(f"- max steps: `{args.max_steps}`")
    lines.append(f"- traced rows: `{len(rows)}`")
    lines.append(f"- terminal rows: `{terminal}`")
    lines.append(f"- return rows: `{returned}`")
    lines.append("")
    lines.append("## Prefix Drift")
    lines.append("")
    lines.append(
        "| bits | j_left | j_right | source keys | mean samples/key | "
        "weighted L1 mean | weighted L1 p95 | key L1 p95 | max |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in scores:
        mean_samples = min(
            float(row["mean_samples_per_key_left"]),
            float(row["mean_samples_per_key_right"]),
        )
        lines.append(
            f"| {row['bits']} | {row['j_left']} | {row['j_right']} | "
            f"{row['common_source_keys']} | {format_float(mean_samples)} | "
            f"{format_float(row['weighted_l1_mean'])} | "
            f"{format_float(row['weighted_l1_p95'])} | "
            f"{format_float(row['key_l1_p95'])} | "
            f"{format_float(row['weighted_l1_max'])} |"
        )
    lines.append("")
    lines.append("## Interpretation Guardrails")
    lines.append("")
    lines.append("- `bits = 0` is the phase-only square kernel.")
    lines.append("- `bits > 0` records low residue bits at both source and destination.")
    lines.append("- This is a retraced smoke window, not a generated Lean matrix.")
    lines.append("- A useful `A1` branch still needs larger-scale stability and a Banach norm.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, default=12)
    parser.add_argument("--j-counts", default="16,32")
    parser.add_argument("--refine-bits", default="0,5,8,10")
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
    j_counts = parse_csv_ints(args.j_counts)
    if len(j_counts) < 2:
        raise SystemExit("need at least two j-counts")
    bits_list = parse_csv_ints(args.refine_bits)
    rows = trace_rows(args)
    scores: list[dict[str, Any]] = []
    for left, right in zip(j_counts, j_counts[1:], strict=False):
        for bits in bits_list:
            scores.append(score_pair(rows, bits=bits, left=left, right=right))

    report_path, csv_path = output_paths(args.output_tag)
    write_csv(scores, csv_path)
    write_report(rows=rows, scores=scores, args=args, path=report_path)
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
