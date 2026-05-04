import csv
import time
from decimal import Decimal, getcontext


INPUT_FILE = "collatz_06_pattern_v2_top_debito.csv"
OUTPUT_FILE = "collatz_09_corridoi_2adici_top_debito.csv"

TOP_N = 100

getcontext().prec = 80


def v2(x: int) -> int:
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def syracuse_with_v2(n: int):
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


def check_pattern(n: int, pattern: list[int]) -> bool:
    current = n

    for expected_a in pattern:
        current, actual_a = syracuse_with_v2(current)

        if actual_a != expected_a:
            return False

    return True


def find_residue_fast(pattern: list[int]):
    """
    Costruzione incrementale del corridoio 2-adico.

    Per un pattern a_1,...,a_k il modulo naturale usato è:

        2^(1 + sum(a_i))

    Per i pattern Collatz/Syracuse esatti, di norma emerge una sola classe
    residua dispari modulo 2^(1 + sum(a_i)).
    """
    residues = [1]
    current_power = 1
    current_pattern = []

    for a in pattern:
        current_pattern.append(a)

        old_power = current_power
        old_modulus = 2 ** old_power

        current_power += a
        new_modulus = 2 ** current_power

        multiplier = 2 ** (current_power - old_power)

        new_residues = []

        for r in residues:
            for q in range(multiplier):
                candidate = r + q * old_modulus

                if candidate % 2 == 0:
                    continue

                if check_pattern(candidate, current_pattern):
                    new_residues.append(candidate)

        residues = sorted(set(new_residues))

        if not residues:
            break

    modulus = 2 ** current_power

    return current_power, modulus, residues


def parse_pattern(text: str):
    if text is None:
        return []

    text = str(text).strip()

    if not text:
        return []

    return [int(x.strip()) for x in text.split(",") if x.strip()]


def read_input(filename: str, top_n: int):
    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            rows.append(row)

            if len(rows) >= top_n:
                break

    return rows


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def scientific_density(power: int):
    """
    Densità tra i dispari del corridoio:
        1 / 2^sum_v2

    Poiché modulus_power = 1 + sum_v2,
    tra i dispari modulo 2^(1+sum_v2) ci sono 2^sum_v2 classi.
    """
    if power <= 1:
        return "1"

    sum_v2 = power - 1
    density = Decimal(1) / (Decimal(2) ** Decimal(sum_v2))

    return f"{density:.30E}"


def main():
    print("Analisi corridoi 2-adici dei numeri ribelli")
    print("-" * 150)

    input_rows = read_input(INPUT_FILE, TOP_N)
    output_rows = []

    t_start = time.time()

    for idx, row in enumerate(input_rows, start=1):
        start = int(row["start"])
        pattern = parse_pattern(row["until_debt_peak"])

        if not pattern:
            continue

        t0 = time.time()

        modulus_power, modulus, residues = find_residue_fast(pattern)

        elapsed = time.time() - t0

        residue = residues[0] if residues else None
        solutions_count = len(residues)

        if residue is not None:
            same_as_start = start == residue
            start_congruent = (start - residue) % modulus == 0
            quotient = (start - residue) // modulus if start >= residue else 0
        else:
            same_as_start = False
            start_congruent = False
            quotient = None

        sum_v2 = sum(pattern)

        out = {
            "rank": idx,
            "start": start,
            "classe_mod_1024": row.get("classe_mod_1024", ""),
            "pattern_length": len(pattern),
            "sum_v2": sum_v2,
            "modulus_power": modulus_power,
            "modulus": modulus,
            "solutions_count": solutions_count,
            "residue": residue,
            "start_equals_residue": same_as_start,
            "start_congruent_to_residue": start_congruent,
            "quotient_start_minus_residue_over_modulus": quotient,
            "density_among_odd_classes": scientific_density(modulus_power),
            "max_debt": row.get("max_debt", ""),
            "max_debt_step": row.get("max_debt_step", ""),
            "peak_step": row.get("peak_step", ""),
            "first_descent_step": row.get("first_descent_step", ""),
            "max_run_1": row.get("max_run_1", ""),
            "avg_v2": row.get("avg_v2", ""),
            "ratio_1": row.get("ratio_1", ""),
            "pattern_prefix_80": ",".join(map(str, pattern[:80])),
            "time_seconds": f"{elapsed:.6f}",
        }

        output_rows.append(out)

        print(
            f"{idx:3d}) n={start:10d} | "
            f"len={len(pattern):4d} | "
            f"sum_v2={sum_v2:4d} | "
            f"mod=2^{modulus_power:<4d} | "
            f"solutions={solutions_count:2d} | "
            f"residue={str(residue)[:24]:>24s} | "
            f"same={str(same_as_start):5s} | "
            f"time={elapsed:.4f}s"
        )

    export_csv(OUTPUT_FILE, output_rows)

    total_elapsed = time.time() - t_start

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Tempo totale: {total_elapsed:.3f} secondi")
    print()
    print("Per aprirlo:")
    print(f"open '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
