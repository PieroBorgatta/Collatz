import csv
import math


OUTPUT_FILE = "collatz_26_test_debt_lyapunov.csv"
SUMMARY_FILE = "collatz_26_summary_debt_lyapunov.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
DEBT_LOOKAHEAD = 80

LAMBDAS = [
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.75,
    1.00,
]

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
    """
    D_max(n) = massimo debito gravitazionale nei prossimi lookahead passi.

    Questa è una misura del rischio futuro:
    se nei prossimi passi il numero entra in una lunga zona espansiva,
    D_max sarà alto.
    """
    key = (n, lookahead)

    if key in _cache_debt:
        return _cache_debt[key]

    current = n
    cumulative_v2 = 0
    max_debt = 0.0

    for step in range(1, lookahead + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        cumulative_v2 += a

        debt = step * CRITICAL - cumulative_v2

        if debt > max_debt:
            max_debt = debt

    _cache_debt[key] = max_debt

    return max_debt


def H(n: int, lam: float):
    return math.log(n) + lam * max_future_debt(n)


def descent_step(start: int, lam: float):
    initial_h = H(start, lam)
    n = start

    best_delta = 0.0
    best_step = 0
    best_value = start

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, _ = syracuse(n)

        current_h = H(n, lam)
        delta = current_h - initial_h

        if delta < best_delta:
            best_delta = delta
            best_step = step
            best_value = n

        if current_h < initial_h:
            return {
                "success": True,
                "step": step,
                "value": n,
                "best_delta": best_delta,
                "best_step": best_step,
                "best_value": best_value,
            }

        if n == 1:
            break

    return {
        "success": False,
        "step": None,
        "value": None,
        "best_delta": best_delta,
        "best_step": best_step,
        "best_value": best_value,
    }


def test_lambda(lam: float):
    total = 0

    improved = 0
    worsened = 0
    same = 0

    failures_log = 0
    failures_h = 0

    sum_log_step = 0
    sum_h_step = 0

    max_log_step = 0
    max_h_step = 0

    hardest_h = []
    improvements = []
    worsenings = []

    for n in range(3, LIMIT + 1, 2):
        total += 1

        res_log = descent_step(n, 0.0)
        res_h = descent_step(n, lam)

        if not res_log["success"]:
            failures_log += 1

        if not res_h["success"]:
            failures_h += 1

        log_step = res_log["step"] if res_log["success"] else MAX_BLOCK_STEPS + 1
        h_step = res_h["step"] if res_h["success"] else MAX_BLOCK_STEPS + 1

        sum_log_step += log_step
        sum_h_step += h_step

        max_log_step = max(max_log_step, log_step)
        max_h_step = max(max_h_step, h_step)

        if h_step < log_step:
            improved += 1
            improvements.append({
                "n": n,
                "log_step": log_step,
                "h_step": h_step,
                "gain": log_step - h_step,
                "debt": max_future_debt(n),
            })
        elif h_step > log_step:
            worsened += 1
            worsenings.append({
                "n": n,
                "log_step": log_step,
                "h_step": h_step,
                "loss": h_step - log_step,
                "debt": max_future_debt(n),
            })
        else:
            same += 1

        hardest_h.append({
            "n": n,
            "log_step": log_step,
            "h_step": h_step,
            "debt": max_future_debt(n),
        })

        if total % 250_000 == 0:
            print(
                f"lambda={lam:.2f} | "
                f"analizzati={total:,} | "
                f"improved={improved:,} | "
                f"worsened={worsened:,}"
            )

    hardest_h.sort(key=lambda x: x["h_step"], reverse=True)
    improvements.sort(key=lambda x: x["gain"], reverse=True)
    worsenings.sort(key=lambda x: x["loss"], reverse=True)

    return {
        "lambda": lam,
        "total": total,

        "failures_log": failures_log,
        "failures_h": failures_h,

        "avg_log_step": sum_log_step / total,
        "avg_h_step": sum_h_step / total,

        "max_log_step": max_log_step,
        "max_h_step": max_h_step,

        "improved": improved,
        "worsened": worsened,
        "same": same,

        "improved_ratio": improved / total,
        "worsened_ratio": worsened / total,
        "same_ratio": same / total,

        "hardest_h": hardest_h[:30],
        "top_improvements": improvements[:30],
        "top_worsenings": worsenings[:30],
    }


def export_csv(filename: str, rows: list):
    fieldnames = [
        "lambda",
        "total",
        "failures_log",
        "failures_h",
        "avg_log_step",
        "avg_h_step",
        "max_log_step",
        "max_h_step",
        "improved",
        "worsened",
        "same",
        "improved_ratio",
        "worsened_ratio",
        "same_ratio",
    ]

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})


def export_summary(filename: str, rows: list):
    lines = []

    lines.append("TEST LYAPUNOV CON DEBITO FUTURO")
    lines.append("=" * 120)
    lines.append("")
    lines.append("Funzione testata:")
    lines.append("")
    lines.append("H_lambda(n) = log(n) + lambda * D_max(n)")
    lines.append("")
    lines.append("D_max(n) = max debt nei prossimi DEBT_LOOKAHEAD passi")
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    lines.append("")

    for row in rows:
        lines.append("-" * 120)
        lines.append(f"lambda = {row['lambda']}")
        lines.append("")
        lines.append(f"failures log: {row['failures_log']}")
        lines.append(f"failures H:   {row['failures_h']}")
        lines.append("")
        lines.append(f"avg log step: {row['avg_log_step']:.6f}")
        lines.append(f"avg H step:   {row['avg_h_step']:.6f}")
        lines.append("")
        lines.append(f"max log step: {row['max_log_step']}")
        lines.append(f"max H step:   {row['max_h_step']}")
        lines.append("")
        lines.append(f"improved: {row['improved']} ({row['improved_ratio']:.6f})")
        lines.append(f"worsened: {row['worsened']} ({row['worsened_ratio']:.6f})")
        lines.append(f"same:     {row['same']} ({row['same_ratio']:.6f})")
        lines.append("")

        lines.append("Hardest H cases:")
        for x in row["hardest_h"][:10]:
            lines.append(
                f"n={x['n']} | log_step={x['log_step']} | "
                f"h_step={x['h_step']} | debt={x['debt']:.6f}"
            )

        lines.append("")
        lines.append("Top improvements:")
        for x in row["top_improvements"][:10]:
            lines.append(
                f"n={x['n']} | log_step={x['log_step']} | "
                f"h_step={x['h_step']} | gain={x['gain']} | "
                f"debt={x['debt']:.6f}"
            )

        lines.append("")
        lines.append("Top worsenings:")
        for x in row["top_worsenings"][:10]:
            lines.append(
                f"n={x['n']} | log_step={x['log_step']} | "
                f"h_step={x['h_step']} | loss={x['loss']} | "
                f"debt={x['debt']:.6f}"
            )

        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = []

    print("Test Lyapunov con debito futuro")
    print("-" * 120)
    print(f"LIMIT = {LIMIT}")
    print(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    print(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    print()

    for lam in LAMBDAS:
        print()
        print(f"Testing lambda={lam}")
        print("-" * 120)

        row = test_lambda(lam)
        rows.append(row)

        print(
            f"lambda={lam:.2f} | "
            f"avg_log={row['avg_log_step']:.6f} | "
            f"avg_H={row['avg_h_step']:.6f} | "
            f"improved={row['improved']} | "
            f"worsened={row['worsened']} | "
            f"max_log={row['max_log_step']} | "
            f"max_H={row['max_h_step']}"
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
