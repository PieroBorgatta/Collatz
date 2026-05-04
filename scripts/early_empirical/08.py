import csv
import time


OUTPUT_FILE = "collatz_08_pattern_ammissibili_FAST.csv"


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
    Trova le classi residue che generano esattamente il pattern v2.

    Metodo veloce:
    - si parte da tutti i dispari: n ≡ 1 mod 2
    - a ogni nuovo valore a del pattern si aumenta il modulo di 2^a
    - invece di scandire tutto il modulo, si testano solo i sollevamenti dei residui già validi

    Per un pattern a_1,...,a_k il modulo minimo naturale è:

        2^(1 + sum(a_i))

    Tra le classi dispari modulo 2^(1 + sum(a_i)), di norma emerge una classe principale.
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
    odd_classes = modulus // 2

    return {
        "pattern": ",".join(map(str, pattern)),
        "length": len(pattern),
        "sum_v2": sum(pattern),
        "modulus_power": current_power,
        "modulus": modulus,
        "num_odd_classes": odd_classes,
        "solutions_count": len(residues),
        "density_among_odds": len(residues) / odd_classes if odd_classes else 0,
        "first_solution": residues[0] if residues else None,
        "solutions_preview": ",".join(map(str, residues[:20])),
    }


def generate_patterns():
    patterns = []

    # Lunghe sequenze consecutive di 1
    # Ora possiamo spingerci molto più in là senza esplodere coi tempi.
    for length in range(1, 81):
        patterns.append([1] * length)

    # Pattern simili a quelli osservati nei numeri più ribelli
    patterns.extend([
        [1, 1, 2, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [1, 2, 1, 1, 1, 1, 1, 2],
        [1, 2, 1, 1, 1, 2, 1, 1],
        [1, 1, 1, 2, 1, 1, 1, 2],
        [1, 1, 1, 1, 2, 1, 1, 1, 1],

        # Pattern reali visti nei numeri ribelli
        [1, 1, 2, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 2, 3],
        [1, 1, 1, 1, 1, 1, 1, 1, 2, 3],
        [1, 2, 1, 1, 1, 1, 1, 2, 1, 1],

        # Pattern iniziale del numero 3041127 fino al massimo debito
        [
            1, 1, 2, 1, 1, 1, 1, 1, 1, 2,
            1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 2, 2, 1, 1
        ],

        # Pattern iniziale del numero 4637979 fino al massimo debito
        [
            1, 2, 1, 1, 1, 1, 1, 2, 1, 1,
            1, 2, 1, 2, 1, 1, 1, 2, 2, 2,
            1, 1, 1, 1, 2, 1, 1, 1, 1, 4,
            1, 2, 3, 2, 2, 1, 1, 1, 1, 1,
            1, 2, 1, 1, 2, 1, 2, 2, 1, 1,
            1, 1, 2, 1, 1, 1, 2, 2, 1, 1,
            1, 2, 2, 1, 1, 1, 1, 1, 1, 1,
            1
        ],
    ])

    return patterns


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def main():
    print("Analisi pattern v2 ammissibili - VERSIONE FAST")
    print("-" * 150)

    patterns = generate_patterns()
    rows = []

    start_time = time.time()

    for pattern in patterns:
        t0 = time.time()

        row = find_residue_fast(pattern)
        rows.append(row)

        elapsed = time.time() - t0

        print(
            f"pattern_len={row['length']:3d} | "
            f"sum_v2={row['sum_v2']:3d} | "
            f"mod=2^{row['modulus_power']:<4d} | "
            f"solutions={row['solutions_count']:4d} | "
            f"density={row['density_among_odds']:.18f} | "
            f"first={row['first_solution']} | "
            f"time={elapsed:.4f}s"
        )

    export_csv(OUTPUT_FILE, rows)

    total_time = time.time() - start_time

    print()
    print(f"CSV generato: {OUTPUT_FILE}")
    print(f"Tempo totale: {total_time:.3f} secondi")
    print()
    print("Per aprirlo:")
    print(f"open '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
