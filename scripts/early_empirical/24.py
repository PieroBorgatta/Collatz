import csv
import math


OUTPUT_FILE = "collatz_24_test_lyapunov.csv"
SUMMARY_FILE = "collatz_24_summary_lyapunov.txt"

LIMIT = 5_000_000
MAX_BLOCK_STEPS = 200

LAMBDAS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.40,
    0.50,
    0.75,
    1.00,
]


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


def initial_run_v2_1(n: int, max_steps: int = 500):
    """
    Conta quanti passi Syracuse consecutivi iniziali hanno v2=1.
    """
    run = 0
    current = n

    for _ in range(max_steps):
        current, a = syracuse(current)

        if a == 1:
            run += 1
        else:
            break

    return run


def density_v2_1_prefix(n: int, prefix_steps: int = 20):
    """
    Densità di v2=1 nei primi prefix_steps.
    """
    current = n
    count_1 = 0
    steps = 0

    for _ in range(prefix_steps):
        if current == 1:
            break

        current, a = syracuse(current)
        steps += 1

        if a == 1:
            count_1 += 1

    if steps == 0:
        return 0.0

    return count_1 / steps


def penalty(n: int):
    """
    Penalità 2-adica semplice.

    Componente 1:
        run iniziale di v2=1

    Componente 2:
        densità di v2=1 nei primi 20 passi

    La seconda serve perché molti numeri ribelli non hanno solo una run iniziale lunghissima,
    ma una densità alta di 1 distribuita.
    """
    run = initial_run_v2_1(n)
    density = density_v2_1_prefix(n, prefix_steps=20)

    return run + 5.0 * density


def H(n: int, lam: float):
    return math.log(n) + lam * penalty(n)


def analyze_number(start: int, lam: float):
    """
    Cerca entro MAX_BLOCK_STEPS un passo k tale che H(S^k(n)) < H(n).
    """
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
                "start": start,
                "lambda": lam,
                "success": True,
                "descent_step": step,
                "descent_value": n,
                "best_delta": best_delta,
                "best_step": best_step,
                "best_value": best_value,
                "initial_penalty": penalty(start),
            }

        if n == 1:
            break

    return {
        "start": start,
        "lambda": lam,
        "success": False,
        "descent_step": None,
        "descent_value": None,
        "best_delta": best_delta,
        "best_step": best_step,
        "best_value": best_value,
        "initial_penalty": penalty(start),
    }


def test_lambda(lam: float):
    failures = []
    max_descent_step = 0
    sum_descent_step = 0
    success_count = 0

    worst_best_delta = 0.0
    worst_number = None

    processed = 0

    for n in range(3, LIMIT + 1, 2):
        result = analyze_number(n, lam)
        processed += 1

        if result["success"]:
            success_count += 1
            sum_descent_step += result["descent_step"]
            max_descent_step = max(max_descent_step, result["descent_step"])
        else:
            failures.append(result)

            if result["best_delta"] > worst_best_delta:
                worst_best_delta = result["best_delta"]
                worst_number = n

        if processed % 250_000 == 0:
            print(
                f"lambda={lam:.2f} | "
                f"analizzati={processed:,} | "
                f"failures={len(failures)}"
            )

    total = (LIMIT - 1) // 2

    return {
        "lambda": lam,
        "total_numbers": total,
        "success_count": success_count,
        "failure_count": len(failures),
        "success_ratio": success_count / total,
        "max_descent_step": max_descent_step,
        "avg_descent_step": sum_descent_step / success_count if success_count else None,
        "worst_number": worst_number,
        "worst_best_delta": worst_best_delta,
        "failure_examples": failures[:50],
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = [
        "lambda",
        "total_numbers",
        "success_count",
        "failure_count",
        "success_ratio",
        "max_descent_step",
        "avg_descent_step",
        "worst_number",
        "worst_best_delta",
    ]

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for row in rows:
            clean = {k: row.get(k) for k in fieldnames}
            writer.writerow(clean)


def export_summary(filename: str, rows: list):
    lines = []

    lines.append("TEST FUNZIONE DI LYAPUNOV CANDIDATA")
    lines.append("=" * 120)
    lines.append("")
    lines.append("Funzione testata:")
    lines.append("")
    lines.append("H_lambda(n) = log(n) + lambda * penalty(n)")
    lines.append("")
    lines.append("penalty(n) = initial_run_v2_1(n) + 5 * density_v2_1_first_20_steps(n)")
    lines.append("")
    lines.append(f"LIMIT = {LIMIT}")
    lines.append(f"MAX_BLOCK_STEPS = {MAX_BLOCK_STEPS}")
    lines.append("")

    for row in rows:
        lines.append("-" * 120)
        lines.append(f"lambda = {row['lambda']}")
        lines.append(f"success ratio = {row['success_ratio']:.8f}")
        lines.append(f"failures = {row['failure_count']}")
        lines.append(f"max descent step = {row['max_descent_step']}")
        lines.append(f"avg descent step = {row['avg_descent_step']}")
        lines.append(f"worst number = {row['worst_number']}")
        lines.append(f"worst best delta = {row['worst_best_delta']}")
        lines.append("")

        if row["failure_examples"]:
            lines.append("Failure examples:")
            for f in row["failure_examples"][:20]:
                lines.append(
                    f"n={f['start']} | "
                    f"best_delta={f['best_delta']} | "
                    f"best_step={f['best_step']} | "
                    f"best_value={f['best_value']} | "
                    f"initial_penalty={f['initial_penalty']}"
                )
            lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = []

    print("Test funzione di Lyapunov candidata")
    print("-" * 120)
    print(f"LIMIT: {LIMIT}")
    print(f"MAX_BLOCK_STEPS: {MAX_BLOCK_STEPS}")
    print()

    for lam in LAMBDAS:
        print()
        print(f"Testing lambda = {lam}")
        print("-" * 120)

        row = test_lambda(lam)
        rows.append(row)

        print(
            f"lambda={lam:.2f} | "
            f"success_ratio={row['success_ratio']:.8f} | "
            f"failures={row['failure_count']} | "
            f"max_step={row['max_descent_step']} | "
            f"worst={row['worst_number']}"
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
