"""
54_phantom_rational_shadows.py

I cicli fantasma come ombre di punti periodici razionali 2-adici.

Per una parola di esponenti a_0, ..., a_{L-1}, la composizione Syracuse e':

    S^L(n) = (3^L n + C) / 2^A

dove A = sum a_i e C si calcola ricorsivamente:

    C_0 = 0, A_0 = 0
    C_{j+1} = 3 C_j + 2^{A_j}
    A_{j+1} = A_j + a_j

Il punto periodico 2-adico associato alla parola e':

    n_* = C / (2^A - 3^L).

Se 3^L > 2^A, allora n_* e' negativo nel senso reale, ma perfettamente
valido in Q_2. I cicli fantasma mod 2^k sono proprio ombre finite di questi
punti razionali 2-adici: il residuo del ciclo coincide con n_* modulo 2^k.

Interpretazione:
- Un intero positivo puo' "shadoware" n_* per molti passi se e' molto vicino
  a n_* nella metrica 2-adica.
- Non puo' essere esattamente n_* come numero reale positivo, quindi prima o
  poi deve uscire.
- La difficolta' Collatz diventa quantitativa: dare un limite uniforme a
  quanto a lungo un positivo puo' restare 2-adicamente vicino a ombre negative
  espansive.
"""

from __future__ import annotations

from fractions import Fraction

from importlib import util
from pathlib import Path


def load_lift_module():
    path = Path(__file__).with_name("53_lift_phantom_cycles.py")
    spec = util.spec_from_file_location("phantom_lifts", path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def affine_constant(a_values: list[int]) -> tuple[int, int]:
    total_a = 0
    c = 0
    for a in a_values:
        c = 3 * c + (1 << total_a)
        total_a += a
    return c, total_a


def rational_periodic_point(a_values: list[int]) -> Fraction:
    c, total_a = affine_constant(a_values)
    length = len(a_values)
    denominator = (1 << total_a) - (3 ** length)
    return Fraction(c, denominator)


def rational_mod_power_of_two(x: Fraction, k: int) -> int:
    modulus = 1 << k
    numerator = x.numerator % modulus
    denominator = x.denominator % modulus
    inv_denominator = pow(denominator, -1, modulus)
    return (numerator * inv_denominator) % modulus


def v2_integer(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    a = 0
    while (n & 1) == 0:
        n >>= 1
        a += 1
    return a


def orbit_from_word_mod(x: Fraction, a_values: list[int], k: int) -> list[int]:
    residues = []
    cur = x
    for a in a_values:
        residues.append(rational_mod_power_of_two(cur, k))
        cur = Fraction(3 * cur + 1, 1 << a)
    return residues


def main() -> None:
    lift = load_lift_module()
    k_min = 10
    k_max = 24

    print("=" * 86)
    print("  Cicli fantasma come ombre razionali 2-adiche")
    print("=" * 86)
    print(f"  Range: k={k_min}..{k_max}")

    found = 0
    for k in range(k_min, k_max + 1):
        level = lift.find_cycles(k)
        phantoms = [c for c in level["cycles"] if c["is_phantom"]]
        if not phantoms:
            continue

        print("\n" + "-" * 86)
        print(f"  k={k}: {len(phantoms)} phantom cycle(s)")
        print("-" * 86)
        print(f"  {'id':>3} {'L':>4} {'A':>5} {'avg_a':>8} {'product':>12} "
              f"{'first':>10} {'ghost mod 2^k':>15} {'v2 match':>10} {'real n_*':>18}")

        for c in phantoms:
            found += 1
            a_values = [int(level["a_of"][idx]) for idx in c["indices"]]
            ghost = rational_periodic_point(a_values)
            ghost_mod = rational_mod_power_of_two(ghost, k)
            first = c["first_residue"]
            match_v2 = v2_integer(first - ghost_mod)
            match_text = f">={k}" if match_v2 >= k else str(match_v2)
            real_preview = float(ghost) if abs(ghost.numerator) < 10**18 else None
            real_text = f"{real_preview:.6g}" if real_preview is not None else str(ghost)

            print(f"  {c['cycle_id']:>3} {c['length']:>4} {c['sum_a']:>5} "
                  f"{c['avg_a']:>8.4f} {c['product']:>12.6f} "
                  f"{first:>10} {ghost_mod:>15} {match_text:>10} {real_text:>18}")

            residues_from_ghost = orbit_from_word_mod(ghost, a_values, k)
            cycle_residues = [(int(idx) << 1) | 1 for idx in c["indices"]]
            agrees = residues_from_ghost == cycle_residues
            print(f"      ghost orbit matches listed residues mod 2^{k}: {agrees}")
            if c["length"] <= 30:
                print(f"      a-word: {a_values}")
                print(f"      residues: {cycle_residues}")

    print("\n" + "=" * 86)
    if found:
        print("  Lettura: ogni phantom trovato e' congruente a un punto periodico razionale")
        print("  2-adico con valore reale negativo. I ribelli positivi possono solo")
        print("  inseguire queste ombre per un tempo finito, non diventare l'ombra.")
    else:
        print("  Nessun phantom nel range richiesto.")


if __name__ == "__main__":
    main()
