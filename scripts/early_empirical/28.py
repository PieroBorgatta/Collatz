import csv
import math


OUTPUT_FILE = "collatz_28_discounted_debt_lyapunov.csv"
SUMMARY_FILE = "collatz_28_summary_discounted_debt_lyapunov.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 300
DEBT_LOOKAHEAD = 80

LAMBDAS = [0.2, 0.3, 0.4, 0.5, 0.6]
RHOS = [0.92, 0.94, 0.96, 0.97, 0.98, 0.99]

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


def discounted_future_debt(n: int, rho: float, lookahead: int = DEBT_LOOKAHEAD):
    """
    D_rho(n) = max_k rho^k * D(k)

    dove:
        D(k)=k*log2(3)-somma_v2

    Se il debito massimo arriva lontano, pesa meno.
    """
    key = (n, rho, lookahead)

    if key in _cache_debt:
        return _cache_debt[key]

    current = n
    cumulative_v2 = 0
    max_discounted_debt = 0.0
    max_raw_debt = 0.0
    max_step = 0

    for step in range(1, lookahead + 1):
        if current == 1:
            break

        current, a = syracuse(current)
        cumulative_v2 += a

        raw_debt = step * CRITICAL - cumulative_v2
        discounted = (rho ** step) * raw_debt

        if discounted > max_discounted_debt:
            max_discounted_debt = discounted
            max_raw_debt = raw_debt
            max_step = step

    result = (max_discounted_debt, max_raw_debt, max_step)
    _cache_debt[key] = result

    return result


def H(n: int, lam: float, rho: float):
    debt, _, _ = discounted_future_debt(n, rho)
    return math.log(n) + lam * debt


def descent_step(start: int, lam: float, rho: float):
    initial_h = H(start, lam, rho)
    n = start

    for step in range(1, MAX_BLOCK_STEPS + 1):
        n, _ = syracuse(n)

        if H(n, lam, rho) < initial_h:
            return {
                "success": True,
                "step": step,
                "value": n,
            }

        if n == 1:
            break

    return {
        "success": False,
        "step": None,
        "value": None,
    }


def test_params(lam: float, rho: float):
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

    top_worsenings = []
    top_improvements = []
    hardest_h = []

    for n in range(3, LIMIT + 1, 2):
        total += 1

        res_log = descent_step(n, 0.0, rho)
        res_h = descent_step(n, lam, rho)

        log_step = res_log["step"] if res_log["success"] else MAX_BLOCK_STEPS + 1
        h_step = res_h["step"] if res_h["success"] else MAX_BLOCK_STEPS + 1

        if not res_log["success"]:
            failures_log += 1

        if not res_h["success"]:
            failures_h += 1

        sum_log_step += log_step
        sum_h_step += h_step

        max_log_step = max(max_log_step, log_step)
        max_h_step = max(max_h_step, h_step)

        if h_step < log_step:
            improved += 1
            top_improvements.append({
                "n": n,
                "log_step": log_step,
                "h_step": h_step,
                "gain": log_step - h_step,
            })
        elif h_step > log_step:
            worsened += 1
            debt, raw_debt, debt_step = discounted_future_debt(n, rho)
            top_worsenings.append({
                "n": n,
                "log_step": log_step,
                "h_step": h_step,
                "loss": h_step - log_step,
                "discounted_debt": debt,
                "raw_debt": raw_debt,
                "debt_step": debt_step,
            })
        else:
            same += 1

        hardest_h.append({
            "n": n,
            "h_step": h_step,
            "log_step": log_step,
        })

        if total % 500_000 == 0:
            print(
                f"lambda={lam:.2f} rho={rho:.2f} | "
                f"analizzati={total:,} | "
                f"improved={improved:,} | "
                f"worsened={worsened:,}"
            )

    top_worsenings.sort(key=lambda x: x["loss"], reverse=True)
    top_improvements.sort(key=lambda x: x["gain"], reverse=True)
    hardest_h.sort(key=lambda x: x["h_step"], reverse=True)

    return {
        "lambda": lam,
        "rho": rho,
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

        "top_worsenings": top_worsenings[:20],
        "top_improvements": top_improvements[:20],
        "hardest_h": hardest_h[:20],
    }


def export_csv(filename: str, rows: list):
    fieldnames = [
        "lambda",
        "rho",
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
    rows_by_score = sorted(
        rows,
        key=lambda r: (
            r["failures_h"],
            r["worsened"],
            r["max_h_step"],
            r["avg_h_step"],
        )
    )

    lines = []

    lines.append("TEST LYAPUNOV CON DEBITO FUTURO SCONTATO")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    lines.append("")
    lines.append("Criterio ordinamento:")
    lines.append("failures_h, worsened, max_h_step, avg_h_step")
    lines.append("")

    lines.append("Top combinazioni:")
    lines.append("-" * 120)

    for r in rows_by_score[:30]:
        lines.append(
            f"lambda={r['lambda']:.2f} | "
            f"rho={r['rho']:.2f} | "
            f"avg_H={r['avg_h_step']:.6f} | "
            f"max_H={r['max_h_step']} | "
            f"improved={r['improved']} | "
            f"worsened={r['worsened']} | "
            f"failures={r['failures_h']}"
        )

    best = rows_by_score[0]

    lines.append("")
    lines.append("Migliore combinazione:")
    lines.append("-" * 120)
    lines.append(
        f"lambda={best['lambda']:.2f}, rho={best['rho']:.2f}, "
        f"avg_H={best['avg_h_step']:.6f}, "
        f"max_H={best['max_h_step']}, "
        f"improved={best['improved']}, "
        f"worsened={best['worsened']}"
    )

    lines.append("")
    lines.append("Top peggioramenti della migliore combinazione:")
    lines.append("-" * 120)

    for x in best["top_worsenings"]:
        lines.append(
            f"n={x['n']} | "
            f"log_step={x['log_step']} | "
            f"h_step={x['h_step']} | "
            f"loss={x['loss']} | "
            f"discounted_debt={x['discounted_debt']:.6f} | "
            f"raw_debt={x['raw_debt']:.6f} | "
            f"debt_step={x['debt_step']}"
        )

    lines.append("")
    lines.append("Top miglioramenti della migliore combinazione:")
    lines.append("-" * 120)

    for x in best["top_improvements"]:
        lines.append(
            f"n={x['n']} | "
            f"log_step={x['log_step']} | "
            f"h_step={x['h_step']} | "
            f"gain={x['gain']}"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = []

    print("Test Lyapunov con debito futuro scontato")
    print("-" * 120)
    print(f"LIMIT = {LIMIT}")
    print(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    print(f"DEBT_LOOKAHEAD = {DEBT_LOOKAHEAD}")
    print()

    for lam in LAMBDAS:
        for rho in RHOS:
            print()
            print(f"Testing lambda={lam:.2f}, rho={rho:.2f}")
            print("-" * 120)

            row = test_params(lam, rho)
            rows.append(row)

            print(
                f"lambda={lam:.2f} rho={rho:.2f} | "
                f"avg_H={row['avg_h_step']:.6f} | "
                f"max_H={row['max_h_step']} | "
                f"improved={row['improved']} | "
                f"worsened={row['worsened']} | "
                f"failures={row['failures_h']}"
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
