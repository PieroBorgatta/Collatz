import csv
import math


OUTPUT_FILE = "collatz_27_worsenings_lambda_05.csv"
SUMMARY_FILE = "collatz_27_summary_worsenings_lambda_05.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
DEBT_LOOKAHEAD = 80
LAMBDA = 0.5

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


def max_future_debt(n: int, lookahead: int = DEBT_LOOKAHEAD):
    key = (n, lookahead)

    if key in _cache_debt:
        return _cache_debt[key]

    current = n
    cumulative_v2 = 0
    max_debt = 0.0
    max_debt_step = 0

    for step in range(1, lookahead + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        cumulative_v2 += a

        debt = step * CRITICAL - cumulative_v2

        if debt > max_debt:
            max_debt = debt
            max_debt_step = step

    result = (max_debt, max_debt_step)
    _cache_debt[key] = result

    return result


def H(n: int, lam: float = LAMBDA):
    debt, _ = max_future_debt(n)
    return math.log(n) + lam * debt


def descent_step(start: int, lam: float):
    initial_h = H(start, lam)
    initial_log = math.log(start)
    initial_debt, initial_debt_step = max_future_debt(start)

    n = start

    first_log_descent_step = None
    first_log_descent_value = None

    first_h_descent_step = None
    first_h_descent_value = None

    trajectory = []

    for step in range(1, MAX_BLOCK_STEPS + 1):
        prev = n
        n, a = syracuse(n)

        debt, debt_step = max_future_debt(n)
        current_h = math.log(n) + lam * debt

        row = {
            "step": step,
            "value": n,
            "a": a,
            "ratio_to_start": n / start,
            "log_delta": math.log(n) - initial_log,
            "debt": debt,
            "debt_step": debt_step,
            "h_delta": current_h - initial_h,
        }

        trajectory.append(row)

        if first_log_descent_step is None and n < start:
            first_log_descent_step = step
            first_log_descent_value = n

        if first_h_descent_step is None and current_h < initial_h:
            first_h_descent_step = step
            first_h_descent_value = n
            break

        if n == 1:
            break

    return {
        "start": start,
        "initial_debt": initial_debt,
        "initial_debt_step": initial_debt_step,
        "log_step": first_log_descent_step,
        "log_value": first_log_descent_value,
        "h_step": first_h_descent_step,
        "h_value": first_h_descent_value,
        "loss": (
            first_h_descent_step - first_log_descent_step
            if first_h_descent_step is not None and first_log_descent_step is not None
            else None
        ),
        "trajectory": trajectory,
    }


def main():
    rows = []
    detail_blocks = []

    print("Analisi peggioramenti lambda=0.5")
    print("-" * 120)

    total = 0
    worsened = 0

    for n in range(3, LIMIT + 1, 2):
        total += 1

        result = descent_step(n, LAMBDA)

        if result["log_step"] is not None and result["h_step"] is not None:
            if result["h_step"] > result["log_step"]:
                worsened += 1

                # Dati al momento della discesa log
                log_row = result["trajectory"][result["log_step"] - 1]

                rows.append({
                    "start": n,
                    "log_step": result["log_step"],
                    "log_value": result["log_value"],
                    "h_step": result["h_step"],
                    "h_value": result["h_value"],
                    "loss": result["loss"],
                    "initial_debt": result["initial_debt"],
                    "initial_debt_step": result["initial_debt_step"],
                    "debt_at_log_descent": log_row["debt"],
                    "debt_step_at_log_descent": log_row["debt_step"],
                    "log_delta_at_log_descent": log_row["log_delta"],
                    "h_delta_at_log_descent": log_row["h_delta"],
                    "ratio_at_log_descent": log_row["ratio_to_start"],
                    "v2_at_log_descent": log_row["a"],
                })

                detail_blocks.append(make_detail_block(result))

        if total % 250_000 == 0:
            print(f"analizzati={total:,} | worsenings={worsened}")

    rows.sort(key=lambda x: x["loss"], reverse=True)

    export_csv(OUTPUT_FILE, rows)
    export_summary(SUMMARY_FILE, rows, detail_blocks)

    print()
    print(f"Peggioramenti trovati: {len(rows)}")
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


def make_detail_block(result):
    lines = []

    lines.append("-" * 120)
    lines.append(f"n = {result['start']}")
    lines.append(f"initial_debt = {result['initial_debt']:.6f}")
    lines.append(f"initial_debt_step = {result['initial_debt_step']}")
    lines.append(f"log_step = {result['log_step']}")
    lines.append(f"h_step = {result['h_step']}")
    lines.append(f"loss = {result['loss']}")
    lines.append("")
    lines.append("Primi step traiettoria:")
    lines.append("step | value | v2 | ratio | log_delta | debt | debt_step | h_delta")

    for row in result["trajectory"][:40]:
        lines.append(
            f"{row['step']:4d} | "
            f"{row['value']:12d} | "
            f"{row['a']:2d} | "
            f"{row['ratio_to_start']:.9f} | "
            f"{row['log_delta']:+.9f} | "
            f"{row['debt']:.6f} | "
            f"{row['debt_step']:3d} | "
            f"{row['h_delta']:+.9f}"
        )

    lines.append("")

    return "\n".join(lines)


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list, detail_blocks: list):
    lines = []

    lines.append("PEGGIORAMENTI DELLA FUNZIONE H CON LAMBDA=0.5")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    lines.append(f"LAMBDA = {LAMBDA}")
    lines.append("")
    lines.append(f"Peggioramenti trovati: {len(rows)}")
    lines.append("")

    if rows:
        worst = rows[0]
        lines.append("Peggioramento massimo:")
        lines.append(
            f"n={worst['start']} | "
            f"log_step={worst['log_step']} | "
            f"h_step={worst['h_step']} | "
            f"loss={worst['loss']} | "
            f"initial_debt={worst['initial_debt']:.6f} | "
            f"debt_at_log_descent={worst['debt_at_log_descent']:.6f}"
        )
        lines.append("")

    lines.append("Top 30 peggioramenti:")
    lines.append("-" * 120)

    for r in rows[:30]:
        lines.append(
            f"n={r['start']:10d} | "
            f"log_step={r['log_step']:4d} | "
            f"h_step={r['h_step']:4d} | "
            f"loss={r['loss']:4d} | "
            f"initial_debt={r['initial_debt']:.6f} | "
            f"debt_log={r['debt_at_log_descent']:.6f} | "
            f"log_delta={r['log_delta_at_log_descent']:+.6f} | "
            f"h_delta={r['h_delta_at_log_descent']:+.6f}"
        )

    lines.append("")
    lines.append("DETTAGLIO PEGGIORAMENTI")
    lines.append("=" * 120)

    lines.extend(detail_blocks[:30])

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
