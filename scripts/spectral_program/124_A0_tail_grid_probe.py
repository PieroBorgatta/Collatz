"""
124_A0_tail_grid_probe.py

Grid probe for the corrected A0 dyadic-discrepancy route.

Script 123 showed that bounded pure valuation words become exactly
periodic at sufficiently large 2-adic shifts, while the actual kernel
still has archimedean delta/drop residuals and large return-depth tails.

This script varies:

  S = return-depth cutoff,
  A = intermediate valuation cap,

and measures the three remaining terms separately:

  valuation_tail:       high a_i before symbolic return,
  return_depth_tail:    no symbolic return by S before valuation_tail,
  archimedean_boundary: drop/delta effects visible in the actual kernel.

Finite diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
from functools import lru_cache
from importlib import util
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_124{suffix}_A0_tail_grid_probe"
    return ROOT / f"{stem}_report.md", ROOT / f"{stem}_rows.csv"


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


def analyze(args: argparse.Namespace) -> tuple[list[dict[str, Any]], int]:
    op, shadowing, records, target_key, residue, modulus, target_modulus_bits = setup()

    @lru_cache(maxsize=None)
    def trace(mode: str, t: int, h: int, step_cap: int, a_cap: int) -> tuple[Any, ...]:
        n0 = op.make_start_from_residue(residue, modulus, t)
        cur = n0
        last_key = target_key
        word: list[int] = []
        for step in range(1, step_cap + 1):
            a, cur = shadowing.odd_syracuse_step(cur)
            if a > a_cap:
                return ("valuation_tail",)
            if mode == "valuation_word":
                word.append(a)
                continue

            if mode == "kernel" and cur < n0:
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
                    if mode == "shadow":
                        return ("return", dst)
                    delta = next_t.bit_length() - t.bit_length()
                    return ("return", dst, delta)
                last_key = key

        if mode == "valuation_word":
            return ("word", tuple(word))
        return ("step_tail",)

    rows: list[dict[str, Any]] = []
    step_caps = parse_ints(args.step_caps)
    a_caps = parse_ints(args.a_caps)
    for phase in parse_phases(args.phases):
        v2, odd, h = phase
        for step_cap in step_caps:
            for a_cap in a_caps:
                period_m = max(args.min_period_m, step_cap * a_cap + 1 - target_modulus_bits)
                period = 1 << period_m
                samples = phase_samples(v2, odd, args.sample_limit, period, args.sample_mode)
                valuation_tail = 0
                return_depth_tail = 0
                symbolic_returns = 0
                drops = 0
                kernel_returns = 0
                kernel_valuation_tail = 0
                kernel_step_tail = 0
                word_period_mismatch = 0
                shadow_period_mismatch = 0
                kernel_period_mismatch = 0
                shadow_examples: list[str] = []
                kernel_examples: list[str] = []

                for t in samples:
                    word_left = trace("valuation_word", t, h, step_cap, a_cap)
                    word_right = trace("valuation_word", t + period, h, step_cap, a_cap)
                    shadow_left = trace("shadow", t, h, step_cap, a_cap)
                    shadow_right = trace("shadow", t + period, h, step_cap, a_cap)
                    kernel_left = trace("kernel", t, h, step_cap, a_cap)
                    kernel_right = trace("kernel", t + period, h, step_cap, a_cap)

                    valuation_tail += int(shadow_left[0] == "valuation_tail")
                    return_depth_tail += int(shadow_left[0] == "step_tail")
                    symbolic_returns += int(shadow_left[0] == "return")
                    drops += int(kernel_left[0] == "drop")
                    kernel_returns += int(kernel_left[0] == "return")
                    kernel_valuation_tail += int(kernel_left[0] == "valuation_tail")
                    kernel_step_tail += int(kernel_left[0] == "step_tail")

                    if word_left != word_right:
                        word_period_mismatch += 1
                    if shadow_left != shadow_right:
                        shadow_period_mismatch += 1
                        if len(shadow_examples) < args.keep_examples:
                            shadow_examples.append(f"t={t}: {shadow_left} != {shadow_right}")
                    if kernel_left != kernel_right:
                        kernel_period_mismatch += 1
                        if len(kernel_examples) < args.keep_examples:
                            kernel_examples.append(f"t={t}: {kernel_left} != {kernel_right}")

                n = len(samples)
                shadow_mismatch_rate = shadow_period_mismatch / n if n else 0.0
                kernel_mismatch_rate = kernel_period_mismatch / n if n else 0.0
                rows.append(
                    {
                        "phase": fmt_phase(phase),
                        "step_cap": step_cap,
                        "a_cap": a_cap,
                        "period_m": period_m,
                        "sample_count": n,
                        "valuation_tail_rate": valuation_tail / n if n else 0.0,
                        "return_depth_tail_rate": return_depth_tail / n if n else 0.0,
                        "symbolic_return_rate": symbolic_returns / n if n else 0.0,
                        "drop_rate": drops / n if n else 0.0,
                        "kernel_return_rate": kernel_returns / n if n else 0.0,
                        "kernel_valuation_tail_rate": kernel_valuation_tail / n if n else 0.0,
                        "kernel_step_tail_rate": kernel_step_tail / n if n else 0.0,
                        "kernel_unresolved_tail_rate": (
                            (kernel_valuation_tail + kernel_step_tail) / n if n else 0.0
                        ),
                        "word_period_mismatch_rate": word_period_mismatch / n if n else 0.0,
                        "shadow_period_mismatch_rate": shadow_mismatch_rate,
                        "kernel_period_mismatch_rate": kernel_mismatch_rate,
                        "arch_period_excess_rate": max(0.0, kernel_mismatch_rate - shadow_mismatch_rate),
                        "shadow_examples": " | ".join(shadow_examples),
                        "kernel_examples": " | ".join(kernel_examples),
                    }
                )
    return rows, target_modulus_bits


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for row in rows:
        key = (int(row["step_cap"]), int(row["a_cap"]))
        grouped.setdefault(key, []).append(row)
    out: list[dict[str, Any]] = []
    for (step_cap, a_cap), items in sorted(grouped.items()):
        out.append(
            {
                "step_cap": step_cap,
                "a_cap": a_cap,
                "period_m_max": max(int(row["period_m"]) for row in items),
                "valuation_tail_mean": mean(float(row["valuation_tail_rate"]) for row in items),
                "return_depth_tail_mean": mean(float(row["return_depth_tail_rate"]) for row in items),
                "drop_mean": mean(float(row["drop_rate"]) for row in items),
                "kernel_unresolved_tail_mean": mean(
                    float(row["kernel_unresolved_tail_rate"]) for row in items
                ),
                "word_period_mismatch_max": max(float(row["word_period_mismatch_rate"]) for row in items),
                "shadow_period_mismatch_mean": mean(float(row["shadow_period_mismatch_rate"]) for row in items),
                "kernel_period_mismatch_mean": mean(float(row["kernel_period_mismatch_rate"]) for row in items),
                "arch_period_excess_mean": mean(float(row["arch_period_excess_rate"]) for row in items),
            }
        )
    return out


def write_report(
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    target_modulus_bits: int,
    report_path: Path,
    csv_path: Path,
) -> None:
    summary = summarize(rows)
    best_return = min(summary, key=lambda row: float(row["return_depth_tail_mean"]))
    best_kernel_tail = min(summary, key=lambda row: float(row["kernel_unresolved_tail_mean"]))
    best_boundary = min(summary, key=lambda row: float(row["kernel_period_mismatch_mean"]))

    lines: list[str] = []
    lines.append("# A0 Tail Grid Probe")
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
    lines.append(f"- rows CSV: `{csv_path.name}`")
    lines.append("")
    lines.append("The period exponent used for each `(S,A)` is:")
    lines.append("")
    lines.append("```text")
    lines.append("period_m = max(min_period_m, S*A + 1 - target_modulus_bits).")
    lines.append("```")
    lines.append("")
    lines.append("## Aggregate Grid")
    lines.append("")
    lines.append("| S | A | m | val tail | symbolic tail | drop | kernel tail | word mismatch max | shadow mismatch | kernel mismatch | arch excess |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary:
        lines.append(
            f"| {row['step_cap']} | {row['a_cap']} | {row['period_m_max']} | "
            f"{format_float(row['valuation_tail_mean'])} | "
            f"{format_float(row['return_depth_tail_mean'])} | "
            f"{format_float(row['drop_mean'])} | "
            f"{format_float(row['kernel_unresolved_tail_mean'])} | "
            f"{format_float(row['word_period_mismatch_max'])} | "
            f"{format_float(row['shadow_period_mismatch_mean'])} | "
            f"{format_float(row['kernel_period_mismatch_mean'])} | "
            f"{format_float(row['arch_period_excess_mean'])} |"
        )
    lines.append("")
    lines.append("## Extremes")
    lines.append("")
    lines.append("| metric | S | A | value |")
    lines.append("|---|---:|---:|---:|")
    lines.append(
        f"| smallest return-depth tail mean | {best_return['step_cap']} | "
        f"{best_return['a_cap']} | {format_float(best_return['return_depth_tail_mean'])} |"
    )
    lines.append(
        f"| smallest kernel unresolved tail mean | {best_kernel_tail['step_cap']} | "
        f"{best_kernel_tail['a_cap']} | {format_float(best_kernel_tail['kernel_unresolved_tail_mean'])} |"
    )
    lines.append(
        f"| smallest kernel-period mismatch mean | {best_boundary['step_cap']} | "
        f"{best_boundary['a_cap']} | {format_float(best_boundary['kernel_period_mismatch_mean'])} |"
    )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("A proof of the current A0 branch needs the non-periodic terms to be")
    lines.append("controlled.  The symbolic return tail is deliberately pessimistic:")
    lines.append("it ignores archimedean drops, while the actual killed kernel maps")
    lines.append("drops to the zero row.  The `kernel tail` column is therefore the")
    lines.append("more relevant unresolved mass for the killed kernel.  Valuation tails")
    lines.append("should be handled by dyadic counting, and the archimedean")
    lines.append("boundary from `delta` and `drop` by a separate boundary estimate.")
    lines.append("The `word mismatch max` column checks that the pure bounded valuation")
    lines.append("word is already killed by the chosen large 2-adic period.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phases", default="0|3|0,1|3|0,3|1|0,7|3|0")
    parser.add_argument("--step-caps", default="10,25,50,75")
    parser.add_argument("--a-caps", default="4,6,8,10")
    parser.add_argument("--sample-limit", type=int, default=128)
    parser.add_argument("--sample-mode", default="spread", choices=["prefix", "spread"])
    parser.add_argument("--min-period-m", type=int, default=32)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--keep-examples", type=int, default=2)
    parser.add_argument("--output-tag", default="current_A0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, target_modulus_bits = analyze(args)
    report_path, csv_path = output_paths(args.output_tag)
    write_csv(rows, csv_path)
    write_report(
        args=args,
        rows=rows,
        target_modulus_bits=target_modulus_bits,
        report_path=report_path,
        csv_path=csv_path,
    )
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
