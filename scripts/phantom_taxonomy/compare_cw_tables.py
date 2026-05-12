"""
Compare empirical Collatz-Wielandt tables across sampling budgets.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_table(path: Path, label: str) -> list[dict[str, object]]:
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            matrix = row["name"]
            if "_scc_" in matrix:
                mode = matrix.rsplit("_scc_", 1)[1].replace("_edges", "")
            else:
                mode = matrix
            rows.append(
                {
                    "run": label,
                    "mode": mode,
                    "states": int(row["states"]),
                    "edge_types": int(row["edge_types"]),
                    "cw_upper": float(row["cw_upper"]),
                    "status": row["status"],
                    "cw_max_node": row["cw_max_node"],
                }
            )
    return rows


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    by_mode: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_mode.setdefault(str(row["mode"]), []).append(row)

    lines = [
        "# K0=16 Empirical CW Stability",
        "",
        "| run | mode | states | edge types | CW upper | status | max node |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {run} | {mode} | {states} | {edge_types} | {cw_upper:.12g} | "
            "{status} | `{cw_max_node}` |".format(**row)
        )
    lines.extend(["", "## Drift", ""])
    lines.append("| mode | min CW | max CW | spread |")
    lines.append("|---|---:|---:|---:|")
    for mode, group in sorted(by_mode.items()):
        vals = [float(row["cw_upper"]) for row in group]
        lines.append(f"| {mode} | {min(vals):.12g} | {max(vals):.12g} | {max(vals)-min(vals):.12g} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", action="append", nargs=2, metavar=("LABEL", "CSV"), required=True)
    parser.add_argument("--md", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    for label, path in args.table:
        rows.extend(read_table(Path(path), label))
    write_markdown(rows, args.md)
    for row in rows:
        print(f"{row['run']} {row['mode']}: CW={row['cw_upper']:.12g} states={row['states']}")
    print(f"report={args.md}")


if __name__ == "__main__":
    main()
