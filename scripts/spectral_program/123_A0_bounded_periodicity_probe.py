"""
123_A0_bounded_periodicity_probe.py

Probe the candidate dyadic-discrepancy lemma behind A0/TODO 10.M.

The point is to separate three levels:

  valuation_word:
      finite accelerated valuation word, truncated when some a_i > A.
      This is the cleanest 2-adic object and should become periodic under
      t -> t + 2^m.

  shadow_return:
      first symbolic return to the target phantom node within S steps,
      ignoring archimedean drop below the start and ignoring bit-growth
      weights.  This tests whether the shadowing/return label is also
      controlled by finite 2-adic data.

  kernel:
      the actual finite kernel signature with terminal/drop and delta.
      This includes archimedean information and is not expected to be
      exactly periodic in the same way.

Finite diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
from functools import lru_cache
from importlib import util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_123{suffix}_A0_bounded_periodicity_probe"
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


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, bits = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target, target_key, residue, modulus, bits


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
    op, shadowing, records, _target, target_key, residue, modulus, target_modulus_bits = setup()

    @lru_cache(maxsize=None)
    def signature(mode: str, t: int, h: int) -> tuple[Any, ...]:
        n0 = op.make_start_from_residue(residue, modulus, t)
        cur = n0
        last_key = target_key
        word: list[int] = []
        for step in range(1, args.step_cap + 1):
            a, cur = shadowing.odd_syracuse_step(cur)
            if a > args.a_cap:
                return ("valuation_tail",)
            if mode == "valuation_word":
                word.append(a)
                continue

            if mode == "kernel" and cur < n0:
                return ("terminal",)

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
                    if mode == "shadow_return":
                        return ("return", dst)
                    delta = next_t.bit_length() - t.bit_length()
                    return ("return", dst, delta)
                last_key = key

        if mode == "valuation_word":
            return ("word", tuple(word))
        return ("step_tail",)

    rows: list[dict[str, Any]] = []
    modes = ["valuation_word", "shadow_return", "kernel"]
    for phase in parse_phases(args.phases):
        v2, odd, h = phase
        samples = phase_progression(v2, odd, args.sample_limit)
        for m in parse_ints(args.m_values):
            period = 1 << m
            for mode in modes:
                mismatches = 0
                tail_left = 0
                tail_right = 0
                distinct_left: set[tuple[Any, ...]] = set()
                distinct_right: set[tuple[Any, ...]] = set()
                examples: list[str] = []
                for t in samples:
                    left = signature(mode, t, h)
                    right = signature(mode, t + period, h)
                    distinct_left.add(left)
                    distinct_right.add(right)
                    tail_left += int(left[0] in {"valuation_tail", "step_tail"})
                    tail_right += int(right[0] in {"valuation_tail", "step_tail"})
                    if left != right:
                        mismatches += 1
                        if len(examples) < args.keep_examples:
                            examples.append(f"t={t}: {left} != {right}")
                rows.append(
                    {
                        "phase": fmt_phase(phase),
                        "mode": mode,
                        "m": m,
                        "period": period,
                        "step_cap": args.step_cap,
                        "a_cap": args.a_cap,
                        "sample_count": len(samples),
                        "mismatches": mismatches,
                        "mismatch_rate": mismatches / len(samples) if samples else 0.0,
                        "tail_left_rate": tail_left / len(samples) if samples else 0.0,
                        "tail_right_rate": tail_right / len(samples) if samples else 0.0,
                        "distinct_left": len(distinct_left),
                        "distinct_right": len(distinct_right),
                        "examples": " | ".join(examples),
                    }
                )
    return rows, target_modulus_bits


def write_report(
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    report_path: Path,
    csv_path: Path,
    target_modulus_bits: int,
) -> None:
    valuation_period_upper_m = max(0, args.step_cap * args.a_cap + 1 - target_modulus_bits)
    lines: list[str] = []
    lines.append("# A0 Bounded Periodicity Probe")
    lines.append("")
    lines.append("Status: finite diagnostic for the dyadic discrepancy lemma candidate.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- phases: `{args.phases}`")
    lines.append(f"- step cap S: `{args.step_cap}`")
    lines.append(f"- intermediate valuation cap A: `{args.a_cap}`")
    lines.append(f"- target modulus bits: `{target_modulus_bits}`")
    lines.append(f"- crude valuation-word period upper m: `{valuation_period_upper_m}`")
    lines.append(f"- sample limit per phase: `{args.sample_limit}`")
    lines.append(f"- m values: `{args.m_values}`")
    lines.append(f"- rows CSV: `{csv_path.name}`")
    lines.append("")
    lines.append("## Mode Meaning")
    lines.append("")
    lines.append("- `valuation_word`: capped finite valuation word only; pure 2-adic object.")
    lines.append("- `shadow_return`: symbolic target return, ignoring drop and bit-growth delta.")
    lines.append("- `kernel`: actual bounded kernel signature, including terminal/drop and delta.")
    lines.append("")
    lines.append("## Mismatch Rates")
    lines.append("")
    lines.append("| phase | mode | m | mismatches/sample | tail left | tail right | distinct left/right |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for row in rows:
        lines.append(
            f"| `{row['phase']}` | `{row['mode']}` | {row['m']} | "
            f"{row['mismatches']}/{row['sample_count']} "
            f"({format_float(row['mismatch_rate'])}) | "
            f"{format_float(row['tail_left_rate'])} | "
            f"{format_float(row['tail_right_rate'])} | "
            f"{row['distinct_left']}/{row['distinct_right']} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("A zero mismatch rate for `valuation_word` or `shadow_return` supports")
    lines.append("the exact finite-period part of the dyadic discrepancy route.  Persistent")
    lines.append("mismatches in `kernel` are expected, because terminal/drop and bit-growth")
    lines.append("weights are archimedean features rather than pure 2-adic labels.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phases", default="0|3|0,1|3|0,3|1|0,7|3|0")
    parser.add_argument("--m-values", default="4,8,12,16,20,24")
    parser.add_argument("--sample-limit", type=int, default=512)
    parser.add_argument("--step-cap", type=int, default=25)
    parser.add_argument("--a-cap", type=int, default=8)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--keep-examples", type=int, default=3)
    parser.add_argument("--output-tag", default="current_A0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, target_modulus_bits = analyze(args)
    report_path, csv_path = output_paths(args.output_tag)
    write_csv(rows, csv_path)
    write_report(args, rows, report_path, csv_path, target_modulus_bits)
    print(f"wrote {report_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
