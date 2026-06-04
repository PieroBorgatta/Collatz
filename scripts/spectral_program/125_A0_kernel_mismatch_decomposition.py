"""
125_A0_kernel_mismatch_decomposition.py

Decompose the residual kernel-period mismatch found by script 124.

For each source phase and truncation pair (S,A), compare the killed
single-source kernel signature at t and at t + 2^m, where m is chosen large
enough to kill the bounded valuation-word discrepancy.  The pointwise
kernel vector is:

  drop / unresolved tail -> zero vector,
  return(dst, delta)     -> 2^(-delta) e_dst.

The L1 difference between the two pointwise vectors is then assigned to:

  drop_return_boundary,
  destination_label_change,
  delta_only_weight_change,
  unresolved_tail_boundary.

Finite diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import math
from functools import lru_cache
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent


def output_paths(tag: str | None) -> tuple[Path, Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_125{suffix}_A0_kernel_mismatch_decomposition"
    return (
        ROOT / f"{stem}_report.md",
        ROOT / f"{stem}_rows.csv",
        ROOT / f"{stem}_examples.csv",
    )


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_ints(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_phase(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected phase {text!r}; expected v2|odd|h")
    return int(parts[0]), int(parts[1]), int(parts[2])


def parse_phases(text: str) -> list[tuple[int, int, int]]:
    return [parse_phase(part.strip()) for part in text.split(",") if part.strip()]


def fmt_phase(phase: tuple[int, int, int]) -> str:
    return f"{phase[0]}|{phase[1]}|{phase[2]}"


def phase_progression(v2: int, odd: int, sample_limit: int) -> list[int]:
    modulus = 1 << (v2 + 2)
    start = odd << v2
    if start <= 0:
        start += modulus
    return [start + idx * modulus for idx in range(sample_limit)]


def phase_samples(v2: int, odd: int, sample_limit: int, span: int, mode: str) -> list[int]:
    if mode == "prefix":
        return phase_progression(v2, odd, sample_limit)
    if mode == "dyadic-prefix":
        modulus = 1 << (v2 + 2)
        start = odd << v2
        if start <= 0:
            start += modulus
        if start >= span:
            return []
        count = ((span - 1 - start) // modulus) + 1
        return [start + idx * modulus for idx in range(count)]
    if mode != "spread":
        raise ValueError(f"unknown sample mode: {mode}")
    modulus = 1 << (v2 + 2)
    start = odd << v2
    if start <= 0:
        start += modulus
    if start >= span:
        return []
    count = ((span - 1 - start) // modulus) + 1
    if count <= sample_limit:
        return [start + idx * modulus for idx in range(count)]
    indices = sorted({(idx * count) // sample_limit for idx in range(sample_limit)})
    return [start + idx * modulus for idx in indices]


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, bits = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target_key, residue, modulus, bits


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


def format_float(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def weight(delta: int) -> float:
    return 2.0 ** (-delta)


def trace_kind(sig: tuple[Any, ...]) -> str:
    return str(sig[0])


def point_l1(left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[float, str]:
    left_kind = trace_kind(left)
    right_kind = trace_kind(right)
    tail_kinds = {"valuation_tail", "step_tail"}

    if left == right:
        return 0.0, "equal"
    if left_kind in tail_kinds or right_kind in tail_kinds:
        if left_kind == "return" and right_kind in tail_kinds:
            return weight(int(left[2])), "return_vs_tail"
        if right_kind == "return" and left_kind in tail_kinds:
            return weight(int(right[2])), "tail_vs_return"
        return 0.0, "tail_zero_boundary"
    if left_kind == "drop" and right_kind == "drop":
        return 0.0, "drop_equal"
    if left_kind == "drop" and right_kind == "return":
        return weight(int(right[2])), "drop_vs_return"
    if left_kind == "return" and right_kind == "drop":
        return weight(int(left[2])), "return_vs_drop"
    if left_kind == "return" and right_kind == "return":
        left_dst, left_delta = left[1], int(left[2])
        right_dst, right_delta = right[1], int(right[2])
        left_w = weight(left_delta)
        right_w = weight(right_delta)
        if left_dst == right_dst:
            return abs(left_w - right_w), "delta_only"
        return left_w + right_w, "destination_change"
    return 0.0, f"other_{left_kind}_vs_{right_kind}"


def analyze(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    op, shadowing, records, target_key, residue, modulus, target_modulus_bits = setup()

    @lru_cache(maxsize=None)
    def trace_kernel(t: int, h: int, step_cap: int, a_cap: int) -> tuple[Any, ...]:
        n0 = op.make_start_from_residue(residue, modulus, t)
        cur = n0
        last_key = target_key
        for _step in range(1, step_cap + 1):
            a, cur = shadowing.odd_syracuse_step(cur)
            if a > a_cap:
                return ("valuation_tail",)
            if cur < n0:
                return ("drop",)

            key, _best_v = op.best_shadow(cur, records, shadowing)
            if key is None:
                last_key = None
                continue
            if key != last_key:
                if key == target_key:
                    next_t = op.local_t_from_residue(cur, residue, modulus)
                    dst = op.state_of(
                        next_t,
                        h + 1,
                        args.odd_bits,
                        args.hit_bits,
                        args.v2_cap,
                    )
                    delta = next_t.bit_length() - t.bit_length()
                    return ("return", dst, delta)
                last_key = key
        return ("step_tail",)

    rows: list[dict[str, Any]] = []
    example_rows: list[dict[str, Any]] = []
    phases = parse_phases(args.phases)
    for phase in phases:
        v2, odd, h = phase
        for step_cap in parse_ints(args.step_caps):
            for a_cap in parse_ints(args.a_caps):
                period_m = max(args.min_period_m, step_cap * a_cap + 1 - target_modulus_bits)
                period = 1 << period_m
                span = 1 << (args.prefix_bits if args.sample_mode == "dyadic-prefix" else period_m)
                samples = phase_samples(v2, odd, args.sample_limit, span, args.sample_mode)
                counts: dict[str, int] = {}
                l1_sums: dict[str, float] = {}
                kind_counts: dict[str, int] = {}
                total_l1 = 0.0
                nonzero = 0
                left_return = 0
                left_drop = 0
                left_tail = 0
                right_return = 0
                right_drop = 0
                right_tail = 0
                max_l1 = 0.0

                for t in samples:
                    left = trace_kernel(t, h, step_cap, a_cap)
                    right = trace_kernel(t + period, h, step_cap, a_cap)
                    l1, category = point_l1(left, right)
                    counts[category] = counts.get(category, 0) + 1
                    l1_sums[category] = l1_sums.get(category, 0.0) + l1
                    kind_counts[f"{trace_kind(left)}_to_{trace_kind(right)}"] = (
                        kind_counts.get(f"{trace_kind(left)}_to_{trace_kind(right)}", 0) + 1
                    )
                    total_l1 += l1
                    max_l1 = max(max_l1, l1)
                    nonzero += int(l1 > 0.0)
                    left_return += int(trace_kind(left) == "return")
                    left_drop += int(trace_kind(left) == "drop")
                    left_tail += int(trace_kind(left) in {"valuation_tail", "step_tail"})
                    right_return += int(trace_kind(right) == "return")
                    right_drop += int(trace_kind(right) == "drop")
                    right_tail += int(trace_kind(right) in {"valuation_tail", "step_tail"})
                    if l1 > 0.0 and len(example_rows) < args.max_examples:
                        example_rows.append(
                            {
                                "phase": fmt_phase(phase),
                                "step_cap": step_cap,
                                "a_cap": a_cap,
                                "period_m": period_m,
                                "t": t,
                                "category": category,
                                "l1": l1,
                                "left": repr(left),
                                "right": repr(right),
                            }
                        )

                n = len(samples)
                row: dict[str, Any] = {
                    "phase": fmt_phase(phase),
                    "step_cap": step_cap,
                    "a_cap": a_cap,
                    "period_m": period_m,
                    "sample_count": n,
                    "total_point_l1_mean": total_l1 / n if n else 0.0,
                    "nonzero_l1_rate": nonzero / n if n else 0.0,
                    "max_point_l1": max_l1,
                    "left_return_rate": left_return / n if n else 0.0,
                    "left_drop_rate": left_drop / n if n else 0.0,
                    "left_tail_rate": left_tail / n if n else 0.0,
                    "right_return_rate": right_return / n if n else 0.0,
                    "right_drop_rate": right_drop / n if n else 0.0,
                    "right_tail_rate": right_tail / n if n else 0.0,
                }
                categories = [
                    "destination_change",
                    "delta_only",
                    "drop_vs_return",
                    "return_vs_drop",
                    "return_vs_tail",
                    "tail_vs_return",
                    "tail_zero_boundary",
                ]
                for category in categories:
                    row[f"{category}_count"] = counts.get(category, 0)
                    row[f"{category}_rate"] = counts.get(category, 0) / n if n else 0.0
                    row[f"{category}_l1_mean"] = l1_sums.get(category, 0.0) / n if n else 0.0
                    row[f"{category}_l1_share"] = (
                        l1_sums.get(category, 0.0) / total_l1 if total_l1 else 0.0
                    )
                row["kind_transition_counts"] = " | ".join(
                    f"{key}:{value}" for key, value in sorted(kind_counts.items())
                )
                rows.append(row)
    return rows, example_rows, target_modulus_bits


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((int(row["step_cap"]), int(row["a_cap"])), []).append(row)
    out: list[dict[str, Any]] = []
    categories = [
        "destination_change",
        "delta_only",
        "drop_vs_return",
        "return_vs_drop",
        "return_vs_tail",
        "tail_vs_return",
    ]
    for (step_cap, a_cap), items in sorted(grouped.items()):
        row: dict[str, Any] = {
            "step_cap": step_cap,
            "a_cap": a_cap,
            "period_m_max": max(int(item["period_m"]) for item in items),
            "total_point_l1_mean": mean(float(item["total_point_l1_mean"]) for item in items),
            "nonzero_l1_rate_mean": mean(float(item["nonzero_l1_rate"]) for item in items),
            "left_drop_rate_mean": mean(float(item["left_drop_rate"]) for item in items),
            "left_return_rate_mean": mean(float(item["left_return_rate"]) for item in items),
            "left_tail_rate_mean": mean(float(item["left_tail_rate"]) for item in items),
        }
        for category in categories:
            row[f"{category}_l1_mean"] = mean(
                float(item[f"{category}_l1_mean"]) for item in items
            )
            row[f"{category}_l1_share_mean"] = mean(
                float(item[f"{category}_l1_share"]) for item in items
            )
        out.append(row)
    return out


def write_report(
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    target_modulus_bits: int,
    report_path: Path,
    rows_path: Path,
    examples_path: Path,
) -> None:
    summary = aggregate(rows)
    best_l1 = min(summary, key=lambda row: float(row["total_point_l1_mean"]))
    focus_items = [
        row
        for row in rows
        if int(row["step_cap"]) == args.focus_step_cap and int(row["a_cap"]) == args.focus_a_cap
    ]

    lines: list[str] = []
    lines.append("# A0 Kernel Mismatch Decomposition")
    lines.append("")
    lines.append("Status: finite diagnostic for TODO `10.M`; not a proof.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- phases: `{args.phases}`")
    lines.append(f"- step caps S: `{args.step_caps}`")
    lines.append(f"- valuation caps A: `{args.a_caps}`")
    lines.append(f"- sample limit per phase: `{args.sample_limit}`")
    lines.append(f"- sample mode: `{args.sample_mode}`")
    lines.append(f"- target modulus bits: `{target_modulus_bits}`")
    lines.append(f"- rows CSV: `{rows_path.name}`")
    lines.append(f"- examples CSV: `{examples_path.name}`")
    lines.append("")
    lines.append("Pointwise vector convention:")
    lines.append("")
    lines.append("```text")
    lines.append("drop/tail          -> 0")
    lines.append("return(dst,delta)  -> 2^-delta e_dst")
    lines.append("```")
    lines.append("")
    lines.append("## Aggregate Decomposition")
    lines.append("")
    lines.append("| S | A | m | point L1 | nonzero rate | dst-change L1 | delta-only L1 | drop->return L1 | return->drop L1 | tail-return L1 |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary:
        tail_return_l1 = float(row["return_vs_tail_l1_mean"]) + float(row["tail_vs_return_l1_mean"])
        lines.append(
            f"| {row['step_cap']} | {row['a_cap']} | {row['period_m_max']} | "
            f"{format_float(row['total_point_l1_mean'])} | "
            f"{format_float(row['nonzero_l1_rate_mean'])} | "
            f"{format_float(row['destination_change_l1_mean'])} | "
            f"{format_float(row['delta_only_l1_mean'])} | "
            f"{format_float(row['drop_vs_return_l1_mean'])} | "
            f"{format_float(row['return_vs_drop_l1_mean'])} | "
            f"{format_float(tail_return_l1)} |"
        )
    lines.append("")
    lines.append("## Best Grid Point")
    lines.append("")
    lines.append("| metric | S | A | value |")
    lines.append("|---|---:|---:|---:|")
    lines.append(
        f"| smallest total point L1 mean | {best_l1['step_cap']} | "
        f"{best_l1['a_cap']} | {format_float(best_l1['total_point_l1_mean'])} |"
    )
    lines.append("")
    lines.append(f"## Focus S={args.focus_step_cap}, A={args.focus_a_cap}")
    lines.append("")
    lines.append("| phase | point L1 | nonzero | dst-change share | delta-only share | drop-return share | return-drop share |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for row in focus_items:
        drop_return_share = float(row["drop_vs_return_l1_share"])
        return_drop_share = float(row["return_vs_drop_l1_share"])
        lines.append(
            f"| `{row['phase']}` | "
            f"{format_float(row['total_point_l1_mean'])} | "
            f"{format_float(row['nonzero_l1_rate'])} | "
            f"{format_float(row['destination_change_l1_share'])} | "
            f"{format_float(row['delta_only_l1_share'])} | "
            f"{format_float(drop_return_share)} | "
            f"{format_float(return_drop_share)} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This diagnostic tests whether the residual boundary is mainly a change")
    lines.append("of destination label, a harmless weight/delta perturbation on the same")
    lines.append("destination, or a true drop/return boundary.  A proof route is cleaner")
    lines.append("if `delta_only` dominates, because that becomes a bit-length boundary")
    lines.append("estimate.  Destination changes or drop/return flips require a stronger")
    lines.append("archimedean boundary lemma.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phases", default="0|3|0,1|3|0,3|1|0,7|3|0")
    parser.add_argument("--step-caps", default="25,50,75")
    parser.add_argument("--a-caps", default="6,8,10")
    parser.add_argument("--sample-limit", type=int, default=256)
    parser.add_argument("--sample-mode", default="spread", choices=["prefix", "spread", "dyadic-prefix"])
    parser.add_argument(
        "--prefix-bits",
        type=int,
        default=12,
        help="dyadic prefix size for --sample-mode dyadic-prefix; enumerates t < 2^prefix_bits",
    )
    parser.add_argument("--min-period-m", type=int, default=32)
    parser.add_argument("--focus-step-cap", type=int, default=75)
    parser.add_argument("--focus-a-cap", type=int, default=10)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-examples", type=int, default=80)
    parser.add_argument("--output-tag", default="current_A0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, examples, target_modulus_bits = analyze(args)
    report_path, rows_path, examples_path = output_paths(args.output_tag)
    write_csv(rows, rows_path)
    write_csv(examples, examples_path)
    write_report(
        args=args,
        rows=rows,
        target_modulus_bits=target_modulus_bits,
        report_path=report_path,
        rows_path=rows_path,
        examples_path=examples_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {rows_path}")
    print(f"wrote {examples_path}")


if __name__ == "__main__":
    main()
