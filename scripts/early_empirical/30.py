import csv
import math
from collections import Counter


OUTPUT_FILE = "collatz_30_worsenings_lambda_045.csv"
SUMMARY_FILE = "collatz_30_summary_worsenings_lambda_045.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
DEBT_LOOKAHEAD = 80
LAMBDA = 0.45

CRITICAL = math.log2(3)


def v2(x: int) -> int:
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def syracuse(n: int):
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


_cache_debt = {}


def max_future_debt(n: int):
    key = n

    if key in _cache_debt:
        return _cache_debt[key]

    current = n
    cumulative_v2 = 0
    max_debt = 0.0
    max_step = 0
    debt_sequence = []

    for step in range(1, DEBT_LOOKAHEAD + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        cumulative_v2 += a

        debt = step * CRITICAL - cumulative_v2
        debt_sequence.append(debt)

        if debt > max_debt:
            max_debt = debt
            max_step = step

    result = {
        "max_debt": max_debt,
        "max_step": max_step,
        "debt_sequence": debt_sequence,
    }

    _cache_debt[key] = result
    return result


def H(n: int):
    d = max_future_debt(n)
    return math.log(n) + LAMBDA * d["max_debt"]


def build_trajectory_analysis(start: int):
    initial_log = math.log(start)
    initial_debt_data = max_future_debt(start)
    initial_debt = initial_debt_data["max_debt"]
    initial_debt_step = initial_debt_data["max_step"]
    initial_h = initial_log + LAMBDA * initial_debt

    n = start

    rows = []

    first_log_step = None
    first_log_value = None

    first_h_step = None
    first_h_value = None

    max_value = start
    max_value_step = 0

    cumulative_v2 = 0
    seq_v2 = []

    for step in range(1, MAX_BLOCK_STEPS + 1):
        previous = n
        n, a = syracuse(n)

        seq_v2.append(a)
        cumulative_v2 += a

        if n > max_value:
            max_value = n
            max_value_step = step

        debt_data = max_future_debt(n)
        future_debt = debt_data["max_debt"]
        future_debt_step = debt_data["max_step"]

        log_delta = math.log(n) - initial_log
        debt_delta = future_debt - initial_debt
        h_delta = log_delta + LAMBDA * debt_delta

        local_debt = step * CRITICAL - cumulative_v2
        local_surplus = cumulative_v2 - step * CRITICAL

        row = {
            "step": step,
            "value": n,
            "v2": a,
            "ratio_to_start": n / start,
            "log_delta": log_delta,
            "future_debt": future_debt,
            "future_debt_step": future_debt_step,
            "future_debt_delta": debt_delta,
            "h_delta": h_delta,
            "local_debt_from_start": local_debt,
            "local_surplus_from_start": local_surplus,
        }

        rows.append(row)

        if first_log_step is None and n < start:
            first_log_step = step
            first_log_value = n

        if first_h_step is None and h_delta < 0:
            first_h_step = step
            first_h_value = n
            break

        if n == 1:
            break

    if first_h_step is None:
        first_h_step = MAX_BLOCK_STEPS + 1
        first_h_value = None

    counter = Counter(seq_v2)

    return {
        "start": start,
        "initial_debt": initial_debt,
        "initial_debt_step": initial_debt_step,
        "first_log_step": first_log_step,
        "first_log_value": first_log_value,
        "first_h_step": first_h_step,
        "first_h_value": first_h_value,
        "loss": (
            first_h_step - first_log_step
            if first_log_step is not None and first_h_step is not None
            else None
        ),
        "max_value": max_value,
        "max_value_step": max_value_step,
        "max_ratio": max_value / start,
        "seq_v2": seq_v2,
        "count_1": counter.get(1, 0),
        "count_2": counter.get(2, 0),
        "count_3": counter.get(3, 0),
        "count_4_plus": sum(v for k, v in counter.items() if k >= 4),
        "ratio_1": counter.get(1, 0) / len(seq_v2) if seq_v2 else 0,
        "avg_v2": sum(seq_v2) / len(seq_v2) if seq_v2 else 0,
        "rows": rows,
    }


def quick_steps(start: int):
    """
    Restituisce:
    - primo step log puro sotto start
    - primo step H sotto H(start)
    """
    initial_log = math.log(start)
    initial_debt = max_future_debt(start)["max_debt"]
    initial_h = initial_log + LAMBDA * initial_debt

    n = start

    log_step = None
    h_step = None

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, _ = syracuse(n)

        if log_step is None and n < start:
            log_step = step

        current_h = H(n)

        if h_step is None and current_h < initial_h:
            h_step = step

        if log_step is not None and h_step is not None:
            break

        if n == 1:
            break

    if log_step is None:
        log_step = MAX_BLOCK_STEPS + 1

    if h_step is None:
        h_step = MAX_BLOCK_STEPS + 1

    return log_step, h_step


def longest_run(seq, value):
    best = 0
    current = 0

    for x in seq:
        if x == value:
            current += 1
            best = max(best, current)
        else:
            current = 0

    return best


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list, detail_blocks: list):
    by_loss = sorted(rows, key=lambda r: r["loss"], reverse=True)
    by_initial_debt = sorted(rows, key=lambda r: r["initial_debt"], reverse=True)
    by_debt_at_log = sorted(rows, key=lambda r: r["future_debt_at_log_step"], reverse=True)
    by_ratio = sorted(rows, key=lambda r: r["max_ratio"], reverse=True)

    avg_loss = sum(r["loss"] for r in rows) / len(rows) if rows else 0
    avg_initial_debt = sum(r["initial_debt"] for r in rows) / len(rows) if rows else 0
    avg_debt_log = sum(r["future_debt_at_log_step"] for r in rows) / len(rows) if rows else 0
    avg_ratio_1 = sum(r["ratio_1_until_h"] for r in rows) / len(rows) if rows else 0

    lines = []

    lines.append("ANALISI PEGGIORAMENTI LAMBDA=0.45")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    lines.append(f"LAMBDA = {LAMBDA}")
    lines.append("")
    lines.append(f"Peggioramenti trovati: {len(rows)}")
    lines.append(f"Loss medio: {avg_loss:.6f}")
    lines.append(f"Initial debt medio: {avg_initial_debt:.6f}")
    lines.append(f"Future debt at log step medio: {avg_debt_log:.6f}")
    lines.append(f"Ratio v2=1 medio fino a H descent: {avg_ratio_1:.6f}")
    lines.append("")

    sections = [
        ("Top 30 per loss", by_loss),
        ("Top 30 per initial debt", by_initial_debt),
        ("Top 30 per future debt al log-step", by_debt_at_log),
        ("Top 30 per max ratio", by_ratio),
    ]

    for title, data in sections:
        lines.append(title)
        lines.append("-" * 120)

        for r in data[:30]:
            lines.append(
                f"n={r['start']:10d} | "
                f"log_step={r['log_step']:4d} | "
                f"h_step={r['h_step']:4d} | "
                f"loss={r['loss']:4d} | "
                f"init_debt={r['initial_debt']:.6f} | "
                f"debt_log={r['future_debt_at_log_step']:.6f} | "
                f"debt_delta_log={r['future_debt_delta_at_log_step']:+.6f} | "
                f"h_delta_log={r['h_delta_at_log_step']:+.6f} | "
                f"max_ratio={r['max_ratio']:.3f} | "
                f"ratio_1={r['ratio_1_until_h']:.6f}"
            )

        lines.append("")

    lines.append("")
    lines.append("DETTAGLIO PRIMI PEGGIORAMENTI")
    lines.append("=" * 120)
    lines.extend(detail_blocks[:25])

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def make_detail_block(analysis):
    lines = []

    lines.append("-" * 120)
    lines.append(f"n = {analysis['start']}")
    lines.append(f"initial_debt = {analysis['initial_debt']:.6f}")
    lines.append(f"initial_debt_step = {analysis['initial_debt_step']}")
    lines.append(f"log_step = {analysis['first_log_step']}")
    lines.append(f"h_step = {analysis['first_h_step']}")
    lines.append(f"loss = {analysis['loss']}")
    lines.append(f"max_value = {analysis['max_value']}")
    lines.append(f"max_ratio = {analysis['max_ratio']:.6f}")
    lines.append(f"avg_v2_until_h = {analysis['avg_v2']:.6f}")
    lines.append(f"ratio_1_until_h = {analysis['ratio_1']:.6f}")
    lines.append("")
    lines.append("step | value | v2 | ratio | log_delta | future_debt | debt_delta | h_delta | local_debt")
    lines.append("-" * 120)

    for row in analysis["rows"][:80]:
        lines.append(
            f"{row['step']:4d} | "
            f"{row['value']:14d} | "
            f"{row['v2']:2d} | "
            f"{row['ratio_to_start']:.9f} | "
            f"{row['log_delta']:+.9f} | "
            f"{row['future_debt']:.6f} | "
            f"{row['future_debt_delta']:+.6f} | "
            f"{row['h_delta']:+.9f} | "
            f"{row['local_debt_from_start']:+.6f}"
        )

    lines.append("")

    return "\n".join(lines)


def main():
    print("Analisi peggioramenti lambda=0.45")
    print("-" * 120)

    summary_rows = []
    detail_blocks = []

    processed = 0
    worsened = 0

    for n in range(3, LIMIT + 1, 2):
        processed += 1

        log_step, h_step = quick_steps(n)

        if h_step > log_step:
            worsened += 1

            analysis = build_trajectory_analysis(n)

            log_row = analysis["rows"][analysis["first_log_step"] - 1]

            row = {
                "start": n,
                "log_step": analysis["first_log_step"],
                "log_value": analysis["first_log_value"],
                "h_step": analysis["first_h_step"],
                "h_value": analysis["first_h_value"],
                "loss": analysis["loss"],
                "initial_debt": analysis["initial_debt"],
                "initial_debt_step": analysis["initial_debt_step"],
                "future_debt_at_log_step": log_row["future_debt"],
                "future_debt_step_at_log_step": log_row["future_debt_step"],
                "future_debt_delta_at_log_step": log_row["future_debt_delta"],
                "log_delta_at_log_step": log_row["log_delta"],
                "h_delta_at_log_step": log_row["h_delta"],
                "local_debt_at_log_step": log_row["local_debt_from_start"],
                "max_value": analysis["max_value"],
                "max_value_step": analysis["max_value_step"],
                "max_ratio": analysis["max_ratio"],
                "avg_v2_until_h": analysis["avg_v2"],
                "ratio_1_until_h": analysis["ratio_1"],
                "max_run_1_until_h": longest_run(analysis["seq_v2"], 1),
                "count_1_until_h": analysis["count_1"],
                "count_2_until_h": analysis["count_2"],
                "count_3_until_h": analysis["count_3"],
                "count_4_plus_until_h": analysis["count_4_plus"],
                "prefix_100_v2": ",".join(map(str, analysis["seq_v2"][:100])),
            }

            summary_rows.append(row)

            if len(detail_blocks) < 40:
                detail_blocks.append(make_detail_block(analysis))

        if processed % 250_000 == 0:
            print(
                f"analizzati={processed:,} | "
                f"peggioramenti={worsened}"
            )

    summary_rows.sort(key=lambda r: r["loss"], reverse=True)

    export_csv(OUTPUT_FILE, summary_rows)
    export_summary(SUMMARY_FILE, summary_rows, detail_blocks)

    print()
    print(f"Peggioramenti trovati: {len(summary_rows)}")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
