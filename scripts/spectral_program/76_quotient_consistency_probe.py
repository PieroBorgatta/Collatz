"""
76_quotient_consistency_probe.py

Consistency probe for the finite critical quotient.

75_critical_symbolic_operator.py enumerates t = 0..2^T-1. That is a finite
truncation unless the first-return transition is stable under

    t -> t + j * 2^T.

This script tests that stability. For each residue r mod 2^T and several
block lifts j, it compares the observed transition signature:

    terminal / return,
    destination phase,
    delta_t_bits bucket.

If mismatches decay as T grows, the finite quotient is becoming a valid
symbolic approximation. If they persist, the state needs more high-bit data.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_SUMMARY = ROOT / "collatz_76_quotient_consistency_summary.csv"
OUT_MISMATCH = ROOT / "collatz_76_quotient_consistency_mismatches.csv"


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


def transition_signature(
    op,
    *,
    t: int,
    h: int,
    target: dict,
    target_residue: int,
    target_modulus: int,
    records: list[dict],
    target_key: tuple[int, int, int],
    shadowing,
    odd_bits: int,
    hit_bits: int,
    v2_cap: int,
    max_steps: int,
) -> tuple:
    n0 = op.make_start_from_residue(target_residue, target_modulus, t)
    result = op.first_return_or_terminal(
        n0,
        records,
        target,
        target_key,
        target_residue,
        target_modulus,
        shadowing,
        max_steps,
    )
    if result.get("terminal"):
        return ("terminal",)
    next_t = result["next_t"]
    dst = op.state_of(next_t, h + 1, odd_bits, hit_bits, v2_cap)
    delta = next_t.bit_length() - t.bit_length()
    # Bucket exact delta; if this is too strict, future scripts can relax it.
    return ("return", dst[0], dst[1], dst[2], delta)


def analyze_T(args: argparse.Namespace, T: int) -> tuple[dict, list[dict]]:
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    target_residue, target_modulus, _ = op.residue_for(target, 1, shadows)

    h_mod = 1 << args.hit_bits
    j_values = list(range(args.j_count))
    mismatches = []
    total_classes = 0
    stable_classes = 0
    signature_counts = Counter()

    for r in range(1 << T):
        for h in range(h_mod):
            total_classes += 1
            signatures = []
            for j in j_values:
                t = r + (j << T)
                signatures.append(transition_signature(
                    op,
                    t=t,
                    h=h,
                    target=target,
                    target_residue=target_residue,
                    target_modulus=target_modulus,
                    records=records,
                    target_key=target_key,
                    shadowing=shadowing,
                    odd_bits=args.odd_bits,
                    hit_bits=args.hit_bits,
                    v2_cap=args.v2_cap,
                    max_steps=args.max_steps,
                ))
            counts = Counter(signatures)
            signature_counts.update(counts)
            if len(counts) == 1:
                stable_classes += 1
            elif len(mismatches) < args.keep_mismatches:
                mismatches.append({
                    "T": T,
                    "r": r,
                    "h": h,
                    "distinct_signatures": len(counts),
                    "most_common_count": counts.most_common(1)[0][1],
                    "signatures": " | ".join(f"{sig}:{count}" for sig, count in counts.most_common()),
                })

    summary = {
        "T": T,
        "odd_bits": args.odd_bits,
        "hit_bits": args.hit_bits,
        "j_count": args.j_count,
        "total_classes": total_classes,
        "stable_classes": stable_classes,
        "mismatch_classes": total_classes - stable_classes,
        "stable_fraction": stable_classes / total_classes if total_classes else 0.0,
        "top_signatures": " | ".join(f"{sig}:{count}" for sig, count in signature_counts.most_common(8)),
    }
    return summary, mismatches


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Testa consistenza del quoziente t mod 2^T.")
    parser.add_argument("--T", default="6,8,10")
    parser.add_argument("--j-count", type=int, default=8)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--keep-mismatches", type=int, default=200)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summaries = []
    mismatches = []
    print("=" * 116)
    print("  Quotient consistency probe")
    print("=" * 116)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, j_count={args.j_count}")
    print(f"  {'T':>4} {'classes':>10} {'stable':>10} {'mismatch':>10} {'stable%':>10}")
    for T in parse_csv_ints(args.T):
        summary, rows = analyze_T(args, T)
        summaries.append(summary)
        mismatches.extend(rows)
        print(
            f"  {T:>4} {summary['total_classes']:>10} {summary['stable_classes']:>10} "
            f"{summary['mismatch_classes']:>10} {summary['stable_fraction']:>10.4f}"
        )

    write_csv(summaries, OUT_SUMMARY)
    write_csv(mismatches, OUT_MISMATCH)
    print("\n  Output:")
    print(f"    {OUT_SUMMARY.name}")
    print(f"    {OUT_MISMATCH.name}")


if __name__ == "__main__":
    main()
