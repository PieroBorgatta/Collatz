"""
78_tail_row_certificate_probe.py

Inspect the row-wise source of the high-bit tail bound.

77_high_bit_tail_bound.py showed an observed perturbative estimate

    rho(CORE) + ||TAIL||_inf < 1.

This script identifies the states that realize ||TAIL||_inf and decomposes
their tail contribution into concrete residue groups (r, h). The output is
intended to suggest a finite row-wise certificate:

    for every source state x, tail_weight(x) / source_count(x) <= 1/2.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_STATES = ROOT / "collatz_78_tail_state_rows.csv"
OUT_GROUPS = ROOT / "collatz_78_tail_group_rows.csv"


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


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, _ = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target, target_key, residue, modulus


def trace_row(ctx, args: argparse.Namespace, T: int, r: int, h: int, j: int) -> dict:
    op, shadowing, records, target, target_key, residue, modulus = ctx
    t = r + (j << T)
    n0 = op.make_start_from_residue(residue, modulus, t)
    src = op.state_of(t, h, args.odd_bits, args.hit_bits, args.v2_cap)
    result = op.first_return_or_terminal(
        n0,
        records,
        target,
        target_key,
        residue,
        modulus,
        shadowing,
        args.max_steps,
    )
    if result.get("terminal"):
        return {
            "T": T,
            "r": r,
            "h": h,
            "j": j,
            "t": t,
            "src": src,
            "terminal": 1,
            "dst": None,
            "delta": None,
            "weight": 0.0,
            "signature": ("terminal",),
        }
    next_t = result["next_t"]
    dst = op.state_of(next_t, h + 1, args.odd_bits, args.hit_bits, args.v2_cap)
    delta = next_t.bit_length() - t.bit_length()
    return {
        "T": T,
        "r": r,
        "h": h,
        "j": j,
        "t": t,
        "src": src,
        "terminal": 0,
        "dst": dst,
        "delta": delta,
        "weight": 2.0 ** (-delta),
        "signature": ("return", dst[0], dst[1], dst[2], delta),
    }


def fmt_state(state: tuple[int, int, int] | None) -> str:
    if state is None:
        return "terminal"
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def analyze_T(ctx, args: argparse.Namespace, T: int) -> tuple[list[dict], list[dict]]:
    groups = defaultdict(list)
    source_counts = Counter()
    full_weight_by_src = Counter()
    core_weight_by_src = Counter()
    tail_weight_by_src = Counter()
    tail_count_by_src = Counter()
    return_count_by_src = Counter()
    terminal_count_by_src = Counter()
    tail_group_rows = []

    for r in range(1 << T):
        for h in range(1 << args.hit_bits):
            rows = [trace_row(ctx, args, T, r, h, j) for j in range(args.j_count)]
            counts = Counter(row["signature"] for row in rows)
            core_sig, core_count = counts.most_common(1)[0]
            for row in rows:
                row["part"] = "core" if row["signature"] == core_sig else "tail"
                groups[(r, h)].append(row)
                source_counts[row["src"]] += 1
                if row["terminal"]:
                    terminal_count_by_src[row["src"]] += 1
                    continue
                return_count_by_src[row["src"]] += 1
                full_weight_by_src[row["src"]] += row["weight"]
                if row["part"] == "tail":
                    tail_weight_by_src[row["src"]] += row["weight"]
                    tail_count_by_src[row["src"]] += 1
                else:
                    core_weight_by_src[row["src"]] += row["weight"]
            if len(counts) > 1:
                tail_weight = sum(row["weight"] for row in rows if row["part"] == "tail" and not row["terminal"])
                tail_count = sum(1 for row in rows if row["part"] == "tail")
                tail_group_rows.append({
                    "T": T,
                    "r": r,
                    "h": h,
                    "core_signature": str(core_sig),
                    "core_count": core_count,
                    "tail_count": tail_count,
                    "tail_weight": tail_weight,
                    "distinct_signatures": len(counts),
                    "signatures": " | ".join(f"{sig}:{count}" for sig, count in counts.most_common()),
                })

    state_rows = []
    for src, count in source_counts.items():
        state_rows.append({
            "T": T,
            "state": fmt_state(src),
            "source_count": count,
            "terminal_count": terminal_count_by_src[src],
            "return_count": return_count_by_src[src],
            "full_weight": full_weight_by_src[src],
            "core_weight": core_weight_by_src[src],
            "tail_count": tail_count_by_src[src],
            "tail_weight": tail_weight_by_src[src],
            "full_row_sum": full_weight_by_src[src] / count,
            "core_row_sum": core_weight_by_src[src] / count,
            "tail_row_sum": tail_weight_by_src[src] / count,
        })
    state_rows.sort(key=lambda row: (-row["tail_row_sum"], -row["tail_weight"], row["state"]))
    tail_group_rows.sort(key=lambda row: (-row["tail_weight"], -row["tail_count"], row["r"], row["h"]))
    return state_rows, tail_group_rows


def parse_csv_ints(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnostica riga per riga della tail.")
    parser.add_argument("--T", default="8,10")
    parser.add_argument("--j-count", type=int, default=16)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=32)
    parser.add_argument("--max-steps", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ctx = setup()
    all_state_rows = []
    all_group_rows = []
    print("=" * 118)
    print("  Tail row certificate probe")
    print("=" * 118)
    print(f"  odd_bits={args.odd_bits}, hit_bits={args.hit_bits}, j_count={args.j_count}")
    print(f"  {'T':>4} {'max tail row':>14} {'state':<22} {'src':>8} {'tail weight':>12}")
    for T in parse_csv_ints(args.T):
        state_rows, group_rows = analyze_T(ctx, args, T)
        all_state_rows.extend(state_rows)
        all_group_rows.extend(group_rows[:200])
        top = state_rows[0]
        print(
            f"  {T:>4} {top['tail_row_sum']:>14.6g} {top['state']:<22} "
            f"{top['source_count']:>8} {top['tail_weight']:>12.6g}"
        )

    write_csv(all_state_rows, OUT_STATES)
    write_csv(all_group_rows, OUT_GROUPS)
    print("\n  Top states:")
    for row in all_state_rows[:15]:
        print(
            f"    T={row['T']} {row['state']:<22} "
            f"src={row['source_count']:<6} tail_sum={row['tail_row_sum']:.6g} "
            f"tail_weight={row['tail_weight']:.6g}"
        )
    print("\n  Output:")
    print(f"    {OUT_STATES.name}")
    print(f"    {OUT_GROUPS.name}")


if __name__ == "__main__":
    main()
