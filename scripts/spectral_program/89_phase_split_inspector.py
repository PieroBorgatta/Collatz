"""
89_phase_split_inspector.py

Inspect the worst phase-unstable high-bit cylinders found by
88_cylinder_signature_stability.py.

This script does not compute spectral-radius bounds.  It asks whether a
low destination-phase majority can be explained by simple extra symbolic
coordinates such as j mod 2^q, next_t mod 2^q, delta, or return step.

The output is a diagnostic for Gate 10.B: if a small coordinate explains
the split, the PhaseState quotient may be refinable; if not, the analytic
branch should move toward a countable return-signature model or the
finite-rank fallback.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from importlib import util
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent
DEFAULT_GROUPS = ROOT / "collatz_88_cylinder_group_summary.csv"
OUT_DETAIL = ROOT / "collatz_89_phase_split_details.csv"
OUT_COORDS = ROOT / "collatz_89_phase_split_coordinates.csv"
OUT_SUMMARY = ROOT / "collatz_89_phase_split_summary.md"


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


def fmt_state(state: tuple[int, int, int] | None) -> str:
    if state is None:
        return "terminal"
    return f"v2={state[0]}|odd={state[1]}|h={state[2]}"


def parse_state(text: str) -> tuple[int, int, int] | None:
    if not text or text == "terminal":
        return None
    vals = {}
    for part in text.split("|"):
        k, v = part.split("=")
        vals[k] = int(v)
    return vals["v2"], vals["odd"], vals["h"]


def read_candidate_groups(args: argparse.Namespace) -> list[dict]:
    path = Path(args.groups)
    rows = []
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["mode"] != "prefix":
                continue
            if int(row["j_count"]) != args.j_count:
                continue
            if args.bulk_only and row["boundary_flag"] != "bulk":
                continue
            if args.h is not None and int(row["h"]) != args.h:
                continue
            status = float(row["status_majority_fraction"])
            phase = float(row["phase_majority_fraction"])
            if status < args.min_status_majority:
                continue
            if phase > args.max_phase_majority:
                continue
            rows.append(row)

    rows.sort(
        key=lambda row: (
            float(row["phase_majority_fraction"]),
            float(row["full_majority_fraction"]),
            int(row["T"]),
            int(row["r"]),
            int(row["h"]),
        )
    )
    return rows[: args.limit_groups]


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, _ = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target, target_key, residue, modulus


def trace_detail(ctx, args: argparse.Namespace, T: int, r: int, h: int, j: int) -> dict:
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
    base = {
        "T": T,
        "r": r,
        "h": h,
        "j": j,
        "t": t,
        "src": fmt_state(src),
        "j_mod_2": j % 2,
        "j_mod_4": j % 4,
        "j_mod_8": j % 8,
        "j_mod_16": j % 16,
        "j_mod_32": j % 32,
        "step": result["step"],
        "step_mod_2": result["step"] % 2,
        "step_mod_4": result["step"] % 4,
        "step_mod_8": result["step"] % 8,
    }
    if result.get("terminal"):
        return {
            **base,
            "status": "terminal",
            "terminal": 1,
            "unresolved": int(result.get("unresolved", 0)),
            "next_t": "",
            "dst": "terminal",
            "delta": "",
            "weight": 0.0,
            "next_t_mod_2": "",
            "next_t_mod_4": "",
            "next_t_mod_8": "",
            "next_t_mod_16": "",
            "next_t_mod_32": "",
            "phase_signature": "terminal",
            "full_signature": "terminal",
        }

    next_t = result["next_t"]
    dst = op.state_of(next_t, h + 1, args.odd_bits, args.hit_bits, args.v2_cap)
    delta = next_t.bit_length() - t.bit_length()
    return {
        **base,
        "status": "return",
        "terminal": 0,
        "unresolved": 0,
        "next_t": next_t,
        "dst": fmt_state(dst),
        "delta": delta,
        "weight": 2.0 ** (-delta),
        "next_t_mod_2": next_t % 2,
        "next_t_mod_4": next_t % 4,
        "next_t_mod_8": next_t % 8,
        "next_t_mod_16": next_t % 16,
        "next_t_mod_32": next_t % 32,
        "phase_signature": fmt_state(dst),
        "full_signature": f"{fmt_state(dst)}|delta={delta}",
    }


def coord_value(row: dict, coord: str):
    value = row.get(coord, "")
    return value if value != "" else "NA"


def coordinate_quality(rows: list[dict], coord: str, target: str) -> dict:
    buckets = defaultdict(list)
    for row in rows:
        buckets[coord_value(row, coord)].append(row)

    total = len(rows)
    weighted_purity = 0.0
    min_purity = 1.0
    max_bucket = 0
    pure_buckets = 0
    bucket_count = 0
    signatures_seen = set()

    for bucket_rows in buckets.values():
        if not bucket_rows:
            continue
        bucket_count += 1
        counts = Counter(row[target] for row in bucket_rows)
        signatures_seen.update(counts)
        majority_count = counts.most_common(1)[0][1]
        purity = majority_count / len(bucket_rows)
        weighted_purity += purity * len(bucket_rows) / total if total else 0.0
        min_purity = min(min_purity, purity)
        max_bucket = max(max_bucket, len(bucket_rows))
        pure_buckets += int(purity == 1.0)

    return {
        "coordinate": coord,
        "target": target,
        "sample_count": total,
        "bucket_count": bucket_count,
        "avg_bucket_size": total / bucket_count if bucket_count else 0.0,
        "distinct_target_count": len(signatures_seen),
        "weighted_purity": weighted_purity,
        "min_bucket_purity": min_purity if bucket_count else 0.0,
        "pure_bucket_fraction": pure_buckets / bucket_count if bucket_count else 0.0,
        "max_bucket_size": max_bucket,
    }


def inspect_group(ctx, args: argparse.Namespace, group: dict) -> tuple[list[dict], list[dict]]:
    T = int(group["T"])
    r = int(group["r"])
    h = int(group["h"])
    details = []
    for j in range(args.j_count):
        t = r + (j << T)
        if t == 0 and not args.include_t_zero:
            continue
        details.append(trace_detail(ctx, args, T, r, h, j))

    coord_names = [
        "j_mod_2",
        "j_mod_4",
        "j_mod_8",
        "j_mod_16",
        "j_mod_32",
        "step_mod_2",
        "step_mod_4",
        "step_mod_8",
        "delta",
        "next_t_mod_2",
        "next_t_mod_4",
        "next_t_mod_8",
        "next_t_mod_16",
        "next_t_mod_32",
    ]
    coord_rows = []
    for coord in coord_names:
        for target in ("phase_signature", "full_signature"):
            quality = coordinate_quality(details, coord, target)
            coord_rows.append({
                "T": T,
                "r": r,
                "h": h,
                "source_phase": group["source_phase"],
                "status_majority_fraction": group["status_majority_fraction"],
                "phase_majority_fraction": group["phase_majority_fraction"],
                "full_majority_fraction": group["full_majority_fraction"],
                **quality,
            })
    return details, coord_rows


def summarize(details: list[dict], coord_rows: list[dict], groups: list[dict], args: argparse.Namespace) -> str:
    nontrivial = [
        row for row in coord_rows
        if int(row["bucket_count"]) > 0
        and float(row["avg_bucket_size"]) >= args.min_avg_bucket_size
    ]
    best_phase = sorted(
        [row for row in nontrivial if row["target"] == "phase_signature"],
        key=lambda row: (-float(row["weighted_purity"]), -float(row["min_bucket_purity"]), row["coordinate"], row["r"]),
    )[:20]
    best_full = sorted(
        [row for row in nontrivial if row["target"] == "full_signature"],
        key=lambda row: (-float(row["weighted_purity"]), -float(row["min_bucket_purity"]), row["coordinate"], row["r"]),
    )[:20]

    lines = [
        "# Phase Split Inspector Summary",
        "",
        "Status: diagnostic output, not a theorem.",
        "",
        "## Inputs",
        "",
        f"- groups file: `{args.groups}`",
        f"- selected groups: `{len(groups)}`",
        f"- j_count: `{args.j_count}`",
        f"- max phase majority: `{args.max_phase_majority}`",
        f"- min status majority: `{args.min_status_majority}`",
        f"- h filter: `{args.h if args.h is not None else 'all'}`",
        f"- include t=0: `{args.include_t_zero}`",
        f"- minimum average bucket size in ranked coordinates: `{args.min_avg_bucket_size}`",
        "",
        "## Selected Groups",
        "",
        "| T | r | h | source phase | status maj | phase maj | full maj |",
        "|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in groups:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | `{row['source_phase']}` | "
            f"{float(row['status_majority_fraction']):.6g} | "
            f"{float(row['phase_majority_fraction']):.6g} | "
            f"{float(row['full_majority_fraction']):.6g} |"
        )

    lines.extend([
        "",
        "## Best Coordinates for Destination Phase",
        "",
        "| T | r | h | coordinate | buckets | avg bucket | weighted purity | min bucket purity | pure bucket fraction |",
        "|---:|---:|---:|---|---:|---:|---:|---:|---:|",
    ])
    for row in best_phase:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | `{row['coordinate']}` | "
            f"{row['bucket_count']} | {float(row['avg_bucket_size']):.6g} | "
            f"{float(row['weighted_purity']):.6g} | "
            f"{float(row['min_bucket_purity']):.6g} | {float(row['pure_bucket_fraction']):.6g} |"
        )

    lines.extend([
        "",
        "## Best Coordinates for Full Signature",
        "",
        "| T | r | h | coordinate | buckets | avg bucket | weighted purity | min bucket purity | pure bucket fraction |",
        "|---:|---:|---:|---|---:|---:|---:|---:|---:|",
    ])
    for row in best_full:
        lines.append(
            f"| {row['T']} | {row['r']} | {row['h']} | `{row['coordinate']}` | "
            f"{row['bucket_count']} | {float(row['avg_bucket_size']):.6g} | "
            f"{float(row['weighted_purity']):.6g} | "
            f"{float(row['min_bucket_purity']):.6g} | {float(row['pure_bucket_fraction']):.6g} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "A coordinate with weighted purity near `1` and high minimum bucket",
        "purity is a candidate refinement coordinate.  A coordinate that only",
        "works because it has one bucket per sampled lift is not by itself a",
        "mathematical explanation; it must generalize in `j` and `T`.",
        "",
        "These diagnostics do not imply Conjecture 6, an infinite operator, a",
        "Lasota-Yorke inequality, Keller-Liverani convergence, or a spectral",
        "gap.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect phase splits in worst Gate-10.B cylinders.")
    parser.add_argument("--groups", default=str(DEFAULT_GROUPS))
    parser.add_argument("--j-count", type=int, default=32)
    parser.add_argument("--limit-groups", type=int, default=12)
    parser.add_argument("--max-phase-majority", type=float, default=0.5)
    parser.add_argument("--min-status-majority", type=float, default=1.0)
    parser.add_argument("--h", type=int, default=None)
    parser.add_argument("--bulk-only", action="store_true", default=True)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--min-avg-bucket-size", type=float, default=2.0)
    parser.add_argument("--include-t-zero", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    groups = read_candidate_groups(args)
    if not groups:
        raise SystemExit("no matching groups found; run 88 first or loosen filters")
    ctx = setup()

    all_details = []
    all_coord_rows = []
    print("=" * 118)
    print("  Phase split inspector")
    print("=" * 118)
    print(f"  selected_groups={len(groups)}, j_count={args.j_count}")
    for group in groups:
        print(
            f"  T={group['T']} r={group['r']} h={group['h']} "
            f"phase_majority={float(group['phase_majority_fraction']):.6g}"
        )
        details, coord_rows = inspect_group(ctx, args, group)
        all_details.extend(details)
        all_coord_rows.extend(coord_rows)

    write_csv(all_details, OUT_DETAIL)
    write_csv(all_coord_rows, OUT_COORDS)
    OUT_SUMMARY.write_text(summarize(all_details, all_coord_rows, groups, args), encoding="utf-8")

    print("\n  Output:")
    print(f"    {OUT_DETAIL.name}")
    print(f"    {OUT_COORDS.name}")
    print(f"    {OUT_SUMMARY.name}")


if __name__ == "__main__":
    main()
