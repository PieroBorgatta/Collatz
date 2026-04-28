import csv
import math


OUTPUT_FILE = "collatz_29_lambda_fine_scan.csv"
SUMMARY_FILE = "collatz_29_summary_lambda_fine_scan.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
DEBT_LOOKAHEAD = 80

# scansione fine
LAMBDAS = [round(x / 100, 2) for x in range(1, 101)]

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
    max_step = 0

    for step in range(1, lookahead + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        cumulative_v2 += a

        debt = step * CRITICAL - cumulative_v2

        if debt > max_debt:
            max_debt = debt
            max_step = step

    _cache_debt[key] = (max_debt, max_step)
    return _cache_debt[key]


def H(n: int, lam: float):
    debt, _ = max_future_debt(n)
    return math.log(n) + lam * debt


def descent_step(start: int, lam: float):
    initial_h = H(start, lam)
    n = start

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, _ = syracuse(n)

        if H(n, lam) < initial_h:
            return step

        if n == 1:
            break

    return MAX_BLOCK_STEPS + 1


def test_lambda(lam: float):
    total = 0

    improved = 0
    worsened = 0
    same = 0

    sum_log = 0
    sum_h = 0

    max_log = 0
    max_h = 0

    worst_loss = 0
    worst_loss_n = None

    best_gain = 0
    best_gain_n = None

    for n in range(3, LIMIT + 1, 2):
        total += 1

        log_step = descent_step(n, 0.0)
        h_step = descent_step(n, lam)

        sum_log += log_step
        sum_h += h_step

        max_log = max(max_log, log_step)
        max_h = max(max_h, h_step)

        if h_step < log_step:
            improved += 1
            gain = log_step - h_step
            if gain > best_gain:
                best_gain = gain
                best_gain_n = n
        elif h_step > log_step:
            worsened += 1
            loss = h_step - log_step
            if loss > worst_loss:
                worst_loss = loss
                worst_loss_n = n
        else:
            same += 1

        if total % 500_000 == 0:
            print(
                f"lambda={lam:.2f} | "
                f"analizzati={total:,} | "
                f"improved={improved:,} | "
                f"worsened={worsened:,}"
            )

    return {
        "lambda": lam,
        "total": total,
        "avg_log_step": sum_log / total,
        "avg_h_step": sum_h / total,
        "max_log_step": max_log,
        "max_h_step": max_h,
        "improved": improved,
        "worsened": worsened,
        "same": same,
        "improved_ratio": improved / total,
        "worsened_ratio": worsened / total,
        "same_ratio": same / total,
        "worst_loss": worst_loss,
        "worst_loss_n": worst_loss_n,
        "best_gain": best_gain,
        "best_gain_n": best_gain_n,
        "score_avg_gain": (sum_log - sum_h) / total,
    }


def export_csv(filename: str, rows: list):
    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, rows: list):
    by_worsened = sorted(rows, key=lambda r: (r["worsened"], r["avg_h_step"]))
    by_avg = sorted(rows, key=lambda r: r["avg_h_step"])
    by_score = sorted(rows, key=lambda r: r["score_avg_gain"], reverse=True)
    by_max = sorted(rows, key=lambda r: (r["max_h_step"], r["avg_h_step"]))

    lines = []

    lines.append("SCANSIONE FINE LAMBDA - H(n)=log(n)+lambda*Dmax80(n)")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    lines.append("")

    sections = [
        ("Migliori per pochi peggioramenti", by_worsened),
        ("Migliori per media H più bassa", by_avg),
        ("Migliori per guadagno medio", by_score),
        ("Migliori per max step", by_max),
    ]

    for title, data in sections:
        lines.append(title)
        lines.append("-" * 120)

        for r in data[:20]:
            lines.append(
                f"lambda={r['lambda']:.2f} | "
                f"avg_H={r['avg_h_step']:.6f} | "
                f"max_H={r['max_h_step']:3d} | "
                f"improved={r['improved']:8d} | "
                f"worsened={r['worsened']:8d} | "
                f"worst_loss={r['worst_loss']:4d} | "
                f"score={r['score_avg_gain']:+.6f}"
            )

        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = []

    print("Scansione fine lambda")
    print("-" * 120)
    print(f"LIMIT = {LIMIT}")
    print(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    print()

    for lam in LAMBDAS:
        print()
        print(f"Testing lambda={lam:.2f}")
        print("-" * 120)

        row = test_lambda(lam)
        rows.append(row)

        print(
            f"lambda={lam:.2f} | "
            f"avg_H={row['avg_h_step']:.6f} | "
            f"max_H={row['max_h_step']} | "
            f"improved={row['improved']} | "
            f"worsened={row['worsened']} | "
            f"score={row['score_avg_gain']:+.6f}"
        )

    export_csv(OUTPUT_FILE, rows)
    export_summary(SUMMARY_FILE, rows)

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")
    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
