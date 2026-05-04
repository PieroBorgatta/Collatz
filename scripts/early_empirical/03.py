import csv
import math


RESISTANT_NUMBERS = [
    3041127,
    4561691,
    1212415,
    159487,
    4064103,
    704511,
    1818623,
    239231,
    3219199,
    376831,
    2022639,
    2424831,
    318975,
    1056767,
    1469439,
    2727935,
    358847,
    4828799,
    2559903,
    565247,
    1409023,
    3423871,
    3033959,
    3637247,
    478463,
    1585151,
    3959295,
    2204159,
    4091903,
    753663,
]


def v2(x: int) -> int:
    count = 0

    while x % 2 == 0:
        x //= 2
        count += 1

    return count


def syracuse(n: int) -> tuple[int, int]:
    """
    Mappa accelerata di Syracuse sui dispari.
    Restituisce:
        prossimo dispari
        numero di divisioni per 2 applicate
    """
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


def collatz_full_step(n: int) -> int:
    """
    Passo Collatz classico.
    """
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def analyze_syracuse_until_one(start: int, max_steps: int = 100_000):
    """
    Analizza la traiettoria accelerata sui soli dispari.
    """
    n = start

    max_value = start
    max_ratio = 1.0
    first_descent_step = None
    first_descent_value = None

    total_v2 = 0
    syracuse_steps = 0

    trajectory = []

    trajectory.append({
        "step": 0,
        "value": n,
        "v2": 0,
        "ratio_to_start": 1.0,
        "log_value": math.log(n),
    })

    while n != 1 and syracuse_steps < max_steps:
        n, a = syracuse(n)
        syracuse_steps += 1
        total_v2 += a

        ratio = n / start

        if n > max_value:
            max_value = n
            max_ratio = ratio

        if first_descent_step is None and n < start:
            first_descent_step = syracuse_steps
            first_descent_value = n

        trajectory.append({
            "step": syracuse_steps,
            "value": n,
            "v2": a,
            "ratio_to_start": ratio,
            "log_value": math.log(n),
        })

    reached_one = n == 1

    return {
        "start": start,
        "reached_one": reached_one,
        "syracuse_steps_to_one": syracuse_steps if reached_one else None,
        "first_descent_step": first_descent_step,
        "first_descent_value": first_descent_value,
        "max_value": max_value,
        "max_ratio": max_ratio,
        "total_v2": total_v2,
        "avg_v2": total_v2 / syracuse_steps if syracuse_steps else 0,
        "trajectory": trajectory,
    }


def analyze_classic_until_one(start: int, max_steps: int = 10_000_000):
    """
    Analizza la traiettoria Collatz classica, passo per passo.
    """
    n = start
    steps = 0
    max_value = start

    while n != 1 and steps < max_steps:
        n = collatz_full_step(n)
        steps += 1

        if n > max_value:
            max_value = n

    return {
        "classic_steps_to_one": steps if n == 1 else None,
        "classic_reached_one": n == 1,
        "classic_max_value": max_value,
    }


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_trajectory(filename: str, trajectory: list):
    export_csv(filename, trajectory)


def main():
    summary_rows = []

    best = None

    print("Analisi numeri resistenti fino a 1")
    print("-" * 120)

    for start in RESISTANT_NUMBERS:
        syr = analyze_syracuse_until_one(start)
        classic = analyze_classic_until_one(start)

        row = {
            "start": start,
            "classe_mod_1024": start % 1024,
            "reached_one": syr["reached_one"],
            "syracuse_steps_to_one": syr["syracuse_steps_to_one"],
            "classic_steps_to_one": classic["classic_steps_to_one"],
            "first_descent_step": syr["first_descent_step"],
            "first_descent_value": syr["first_descent_value"],
            "max_value": syr["max_value"],
            "max_ratio": syr["max_ratio"],
            "total_v2": syr["total_v2"],
            "avg_v2": syr["avg_v2"],
        }

        summary_rows.append(row)

        if best is None or row["max_ratio"] > best["summary"]["max_ratio"]:
            best = {
                "summary": row,
                "trajectory": syr["trajectory"],
            }

        print(
            f"n={start:10d} | "
            f"classic_steps={row['classic_steps_to_one']:5d} | "
            f"syr_steps={row['syracuse_steps_to_one']:4d} | "
            f"first_descent={row['first_descent_step']:4d} | "
            f"max_ratio={row['max_ratio']:12.3f} | "
            f"max_value={row['max_value']:15d} | "
            f"avg_v2={row['avg_v2']:.3f}"
        )

    summary_rows.sort(key=lambda x: x["max_ratio"], reverse=True)

    summary_file = "collatz_03_resistenti_fino_a_1.csv"
    export_csv(summary_file, summary_rows)

    best_start = best["summary"]["start"]
    trajectory_file = f"collatz_03_traiettoria_{best_start}.csv"
    export_trajectory(trajectory_file, best["trajectory"])

    print()
    print("Numero più estremo per max_ratio:")
    print("-" * 120)
    print(f"start: {best_start}")
    print(f"classe mod 1024: {best['summary']['classe_mod_1024']}")
    print(f"max_value: {best['summary']['max_value']}")
    print(f"max_ratio: {best['summary']['max_ratio']:.3f}")
    print(f"first_descent_step: {best['summary']['first_descent_step']}")
    print(f"syracuse_steps_to_one: {best['summary']['syracuse_steps_to_one']}")
    print(f"classic_steps_to_one: {best['summary']['classic_steps_to_one']}")
    print(f"avg_v2: {best['summary']['avg_v2']:.6f}")

    print()
    print(f"File riepilogo generato: {summary_file}")
    print(f"File traiettoria generato: {trajectory_file}")

    print()
    print("Per aprirli su Mac:")
    print(f"open '{summary_file}'")
    print(f"open '{trajectory_file}'")


if __name__ == "__main__":
    main()
