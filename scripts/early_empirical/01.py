import math
import csv
from collections import defaultdict


def v2(x: int) -> int:
    """
    Restituisce ν2(x), cioè quante volte x è divisibile per 2.
    Esempio: v2(40) = 3 perché 40 = 5 * 2^3.
    """
    count = 0

    while x % 2 == 0:
        x //= 2
        count += 1

    return count


def syracuse(n: int) -> int:
    """
    Mappa accelerata di Syracuse sui numeri dispari:

        S(n) = (3n + 1) / 2^ν2(3n + 1)

    Input: numero dispari positivo.
    Output: prossimo numero dispari della traiettoria.
    """
    x = 3 * n + 1
    return x >> v2(x)


def analyze_mod_classes(limit: int = 5_000_000, m: int = 10):
    """
    Analizza i numeri dispari fino a 'limit' e raggruppa
    la variazione logaritmica per classi modulo 2^m.

    Esempio:
        m = 10  -> modulo 1024
        classi dispari: 1, 3, 5, ..., 1023
    """
    modulus = 2 ** m

    stats = defaultdict(lambda: {
        "count": 0,
        "sum_delta": 0.0,
        "positive": 0,
        "negative": 0,
        "zero": 0,
        "max_delta": -10**18,
        "min_delta": 10**18,
        "sum_v2": 0,
        "max_v2": 0,
        "min_v2": 10**18,
        "sum_ratio": 0.0,
        "max_ratio": -10**18,
        "min_ratio": 10**18,
    })

    for n in range(3, limit + 1, 2):
        s = syracuse(n)

        delta = math.log(s) - math.log(n)
        ratio = s / n
        a = v2(3 * n + 1)
        cls = n % modulus

        stats[cls]["count"] += 1
        stats[cls]["sum_delta"] += delta
        stats[cls]["sum_v2"] += a
        stats[cls]["sum_ratio"] += ratio

        if delta > 0:
            stats[cls]["positive"] += 1
        elif delta < 0:
            stats[cls]["negative"] += 1
        else:
            stats[cls]["zero"] += 1

        stats[cls]["max_delta"] = max(stats[cls]["max_delta"], delta)
        stats[cls]["min_delta"] = min(stats[cls]["min_delta"], delta)

        stats[cls]["max_v2"] = max(stats[cls]["max_v2"], a)
        stats[cls]["min_v2"] = min(stats[cls]["min_v2"], a)

        stats[cls]["max_ratio"] = max(stats[cls]["max_ratio"], ratio)
        stats[cls]["min_ratio"] = min(stats[cls]["min_ratio"], ratio)

    rows = []

    for cls, data in stats.items():
        count = data["count"]

        avg_delta = data["sum_delta"] / count
        avg_v2 = data["sum_v2"] / count
        avg_ratio = data["sum_ratio"] / count

        positive_ratio = data["positive"] / count
        negative_ratio = data["negative"] / count

        rows.append({
            "classe_mod": cls,
            "count": count,
            "avg_delta": avg_delta,
            "avg_ratio": avg_ratio,
            "positive_ratio": positive_ratio,
            "negative_ratio": negative_ratio,
            "avg_v2": avg_v2,
            "min_v2": data["min_v2"],
            "max_v2": data["max_v2"],
            "max_delta": data["max_delta"],
            "min_delta": data["min_delta"],
            "max_ratio": data["max_ratio"],
            "min_ratio": data["min_ratio"],
        })

    rows.sort(key=lambda x: x["avg_delta"], reverse=True)

    return rows


def export_csv(rows, output_file: str):
    """
    Esporta i risultati in CSV compatibile con Excel italiano.
    Separatore: ;
    Encoding: utf-8-sig
    """
    fieldnames = [
        "classe_mod",
        "count",
        "avg_delta",
        "avg_ratio",
        "positive_ratio",
        "negative_ratio",
        "avg_v2",
        "min_v2",
        "max_v2",
        "max_delta",
        "min_delta",
        "max_ratio",
        "min_ratio",
    ]

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows, top_n: int = 30):
    """
    Stampa a terminale le classi più pericolose.
    """
    print("Classi più pericolose, cioè con crescita media maggiore:")
    print("-" * 120)

    for row in rows[:top_n]:
        print(
            f"classe {row['classe_mod']:4d} | "
            f"avg_delta={row['avg_delta']:+.6f} | "
            f"avg_ratio={row['avg_ratio']:.6f} | "
            f"positive_ratio={row['positive_ratio']:.3f} | "
            f"avg_v2={row['avg_v2']:.3f} | "
            f"min_v2={row['min_v2']:2d} | "
            f"max_v2={row['max_v2']:2d}"
        )

    print()
    print("Classi più favorevoli, cioè con discesa media maggiore:")
    print("-" * 120)

    for row in rows[-top_n:]:
        print(
            f"classe {row['classe_mod']:4d} | "
            f"avg_delta={row['avg_delta']:+.6f} | "
            f"avg_ratio={row['avg_ratio']:.6f} | "
            f"positive_ratio={row['positive_ratio']:.3f} | "
            f"avg_v2={row['avg_v2']:.3f} | "
            f"min_v2={row['min_v2']:2d} | "
            f"max_v2={row['max_v2']:2d}"
        )


if __name__ == "__main__":
    LIMIT = 5_000_000
    M = 10

    print(f"Analisi Collatz/Syracuse")
    print(f"Numeri dispari analizzati fino a: {LIMIT:,}".replace(",", "."))
    print(f"Modulo: 2^{M} = {2 ** M}")
    print()

    rows = analyze_mod_classes(limit=LIMIT, m=M)

    output_file = f"collatz_classi_mod_2^{M}_limit_{LIMIT}.csv"
    export_csv(rows, output_file)

    print_summary(rows, top_n=30)

    print()
    print(f"File CSV generato: {output_file}")
    print(f"Righe scritte: {len(rows)}")
    print()
    print("Per aprirlo su Mac:")
    print(f"open '{output_file}'")
