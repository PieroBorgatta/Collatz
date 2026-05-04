"""
55_shadowing_congruence.py

Shadowing dei cicli fantasma: dal fenomeno computazionale a un lemma esatto.

Per una parola periodica w = (a_0, ..., a_{L-1}) con A = sum(a_i), la mappa
Syracuse compressa soddisfa

    S_w(n) = (3^L n + C) / 2^A.

Il punto fisso razionale 2-adico e'

    q = C / (2^A - 3^L).

Lemma guida
-----------
Un intero dispari n segue la parola w ripetuta b volte se

    n == q  (mod 2^(bA + 1)).

Il bit extra e' necessario per fissare le valutazioni esatte, non solo la
divisibilita' minima: all'ultimo passo bisogna escludere divisibilita' per
2^(a+1).

Nel caso phantom, 3^L > 2^A, quindi q e' un razionale 2-adico con valore
reale negativo. I positivi non possono essere q, ma possono coincidere con q
modulo molte potenze di 2: questo spiega i "ribelli" come shadowing finito
di orbite negative espansive.

Questo script verifica il lemma sui phantom trovati, costruisce i minimi
interi positivi che shadowano b periodi e misura:

  - n0 minimo congruente a q modulo 2^(bA+1)
  - valore dopo b periodi
  - crescita osservata
  - extra periodi interi ancora shadowati accidentalmente
  - stopping time sotto n0 dopo l'uscita

Non e' una prova di Collatz. Serve a isolare il prossimo obiettivo teorico:
quantificare l'uscita dallo shadowing e il pagamento del debito accumulato.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from importlib import util
from pathlib import Path


def load_module(filename: str, name: str):
    path = Path(__file__).with_name(filename)
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def v2_split(m: int) -> tuple[int, int]:
    a = 0
    while (m & 1) == 0:
        m >>= 1
        a += 1
    return a, m


def odd_syracuse_step(n: int) -> tuple[int, int]:
    a, nxt = v2_split(3 * n + 1)
    return a, nxt


def valuation_word(n: int, steps: int) -> list[int]:
    out = []
    cur = n
    for _ in range(steps):
        a, cur = odd_syracuse_step(cur)
        out.append(a)
    return out


def iterate_odd(n: int, steps: int) -> int:
    cur = n
    for _ in range(steps):
        _, cur = odd_syracuse_step(cur)
    return cur


def first_mismatch(observed: list[int], expected: list[int]) -> int | None:
    for i, (a, b) in enumerate(zip(observed, expected), start=1):
        if a != b:
            return i
    if len(observed) != len(expected):
        return min(len(observed), len(expected)) + 1
    return None


def v2_fraction_difference(n: int, q: Fraction) -> int:
    # q has odd denominator for all Collatz words, so v2(denominator)=0.
    diff_num = n * q.denominator - q.numerator
    if diff_num == 0:
        return 10**9
    diff_num = abs(diff_num)
    a = 0
    while (diff_num & 1) == 0:
        diff_num >>= 1
        a += 1
    return a


def stopping_below_start(n: int, start: int, max_steps: int) -> tuple[int | None, int, float]:
    cur = n
    max_value = n
    for step in range(1, max_steps + 1):
        _, cur = odd_syracuse_step(cur)
        if cur > max_value:
            max_value = cur
        if cur < start:
            return step, max_value, max_value / start
    return None, max_value, max_value / start


def count_extra_full_periods(n: int, word: list[int], max_extra_periods: int) -> int:
    cur = n
    full = 0
    for _ in range(max_extra_periods):
        for expected_a in word:
            a, cur = odd_syracuse_step(cur)
            if a != expected_a:
                return full
        full += 1
    return full


def phantom_records(k_min: int, k_max: int) -> list[dict]:
    lifts = load_module("53_lift_phantom_cycles.py", "phantom_lifts")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")

    records = []
    seen_words = set()
    for k in range(k_min, k_max + 1):
        level = lifts.find_cycles(k)
        for c in level["cycles"]:
            if not c["is_phantom"]:
                continue
            word = tuple(int(level["a_of"][idx]) for idx in c["indices"])
            # Keep shifted words if they occur at different k: the phase matters
            # for the residue q mod 2^K.
            key = (k, word)
            if key in seen_words:
                continue
            seen_words.add(key)
            q = shadows.rational_periodic_point(list(word))
            records.append({
                "k": k,
                "cycle_id": c["cycle_id"],
                "length": c["length"],
                "sum_a": c["sum_a"],
                "product": c["product"],
                "first_residue": c["first_residue"],
                "word": list(word),
                "q": q,
            })
    return records


def analyze_record(record: dict, b_max: int, max_extra_steps: int) -> list[dict]:
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    word = record["word"]
    q = record["q"]
    period_len = record["length"]
    period_bits = record["sum_a"]
    rows = []

    for b in range(1, b_max + 1):
        # +1: exact valuations require excluding divisibility by the next
        # power of two at the final step of the repeated word.
        modulus_bits = b * period_bits + 1
        modulus = 1 << modulus_bits
        n0 = shadows.rational_mod_power_of_two(q, modulus_bits)
        if n0 == 0:
            n0 = modulus

        expected = word * b
        observed = valuation_word(n0, len(expected))
        mismatch = first_mismatch(observed, expected)
        follows = mismatch is None

        after_shadow = iterate_odd(n0, b * period_len)
        extra_periods = count_extra_full_periods(after_shadow, word, max_extra_periods=8)
        extra_stop, max_after, max_ratio_after = stopping_below_start(
            after_shadow, n0, max_extra_steps
        )

        rows.append({
            "k": record["k"],
            "cycle_id": record["cycle_id"],
            "period_len": period_len,
            "period_bits": period_bits,
            "period_product": record["product"],
            "b": b,
            "modulus_bits": modulus_bits,
            "n0": n0,
            "n0_bit_length": n0.bit_length(),
            "v2_n0_minus_q": v2_fraction_difference(n0, q),
            "follows_word": int(follows),
            "first_mismatch_step": mismatch or "",
            "after_shadow": after_shadow,
            "shadow_growth_ratio": after_shadow / n0,
            "expected_period_growth": record["product"] ** b,
            "extra_full_periods": extra_periods,
            "extra_stop_steps_below_n0": extra_stop if extra_stop is not None else "",
            "extra_max_ratio_from_n0": max_ratio_after,
        })

    return rows


def print_summary(rows: list[dict]) -> None:
    print("\n" + "=" * 100)
    print("  SHADOWING MINIMO: n0 = q mod 2^(bA+1)")
    print("=" * 100)
    print(f"  {'k':>3} {'id':>3} {'b':>2} {'bits':>5} {'n0 bits':>7} "
          f"{'v2(n-q)':>8} {'ok':>3} {'growth':>12} {'extraP':>6} "
          f"{'stop<start':>11} {'max/start':>11}")
    for r in rows:
        stop = r["extra_stop_steps_below_n0"]
        stop_text = str(stop) if stop != "" else "-"
        print(f"  {r['k']:>3} {r['cycle_id']:>3} {r['b']:>2} "
              f"{r['modulus_bits']:>5} {r['n0_bit_length']:>7} "
              f"{r['v2_n0_minus_q']:>8} {r['follows_word']:>3} "
              f"{r['shadow_growth_ratio']:>12.6g} {r['extra_full_periods']:>6} "
              f"{stop_text:>11} {r['extra_max_ratio_from_n0']:>11.6g}")

    bad = [r for r in rows if not r["follows_word"]]
    print("\n" + "=" * 100)
    if bad:
        print(f"  ATTENZIONE: {len(bad)} casi non seguono la parola attesa.")
    else:
        print("  Tutti i minimi positivi congruenti a q mod 2^(bA+1) seguono esattamente")
        print("  la parola phantom ripetuta b volte. Questo conferma il lemma operativo.")


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analizza lo shadowing dei phantom razionali 2-adici."
    )
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-max", type=int, default=6)
    parser.add_argument("--max-extra-steps", type=int, default=20000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("=" * 100)
    print("  Shadowing congruenziale dei cicli fantasma")
    print("=" * 100)
    print(f"  k range: {args.k_min}..{args.k_max}")
    print(f"  b max:   {args.b_max}")

    records = phantom_records(args.k_min, args.k_max)
    print(f"  Phantom records: {len(records)}")

    rows = []
    for record in records:
        q = record["q"]
        print(f"    k={record['k']}, id={record['cycle_id']}, "
              f"L={record['length']}, A={record['sum_a']}, "
              f"product={record['product']:.6f}, q={q}")
        rows.extend(analyze_record(record, args.b_max, args.max_extra_steps))

    out_path = "collatz_55_shadowing_congruence.csv"
    write_csv(rows, out_path)
    print_summary(rows)
    print(f"\n  Salvato CSV: {out_path}")


if __name__ == "__main__":
    main()
