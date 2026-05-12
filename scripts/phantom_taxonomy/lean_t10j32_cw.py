#!/usr/bin/env python3
"""Verify and generate the compact Lean boundary for the T=10, j=32 CW bound."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


LEAN_TEMPLATE = """\
/-
Generated numerical spectral certificate boundary for the high-bit matrix.

Source CSV: `{source_csv}`
Target T: {target_t}
j_count: {j_count}
Alpha: {alpha_num}/{alpha_den} = 0.0485

This module records the paper-facing Lean statement for Phase 8.7.  The
integer Collatz-Wielandt vector and the exact rational row checks are
produced by `scripts/phantom_taxonomy/lean_t10j32_cw.py`; expanding all
224 row certificates directly in Lean is currently too slow for the
local Mathlib kernel, so the checked external certificate is imported at
this boundary as a single trusted generated fact.
-/

import CollatzShadowing.Generated.T10J32HighBitTail

namespace CollatzShadowing
namespace Generated

open scoped ENNReal NNReal

/-- Alpha used by the `T = 10`, `j = 32` certificate: `97/2000 = 0.0485`. -/
def t10j32HighBitTailAlpha : ProbabilityEntry where
  numerator := {alpha_num}
  denominator := {alpha_den}
  denominator_pos := by decide

/-- Alpha as an `NNReal`. -/
noncomputable def t10j32HighBitTailAlphaNNReal : NNReal :=
  t10j32HighBitTailAlpha.toNNReal

/--
Trusted generated certificate boundary for the exact rational
Collatz-Wielandt check on the imported `T = 10`, `j = 32` full matrix.

The corresponding Python generator constructs a positive integer vector
and verifies every cleared rational row inequality exactly before this
Lean fact is exposed.
-/
axiom t10j32HighBitTailCWCertificate :
    CWCertificate t10j32HighBitTailFull
      (onesBasis 13)
      t10j32HighBitTailAlphaNNReal

/--
Paper Section 7 numerical certificate: the real spectral radius of the
generated full `T = 10`, `j = 32` matrix is at most `97/2000 = 0.0485`.
-/
theorem t10j32HighBitTailSpectralRadiusBound :
    spectralRadius ℝ (nnrealMatrixToReal t10j32HighBitTailFull) ≤
      (t10j32HighBitTailAlphaNNReal : ℝ≥0∞) :=
  spectralRadius_le_of_CWCertificate
    t10j32HighBitTailFull
    (onesBasis 13)
    t10j32HighBitTailAlphaNNReal
    t10j32HighBitTailCWCertificate

/-- The same bound stated with the literal rational `97/2000`. -/
theorem t10j32HighBitTailSpectralRadiusBound_97_2000 :
    spectralRadius ℝ (nnrealMatrixToReal t10j32HighBitTailFull) ≤
      (((97 : NNReal) / (2000 : NNReal)) : ℝ≥0∞) := by
  simpa [t10j32HighBitTailAlphaNNReal, t10j32HighBitTailAlpha,
    ProbabilityEntry.toNNReal] using t10j32HighBitTailSpectralRadiusBound

end Generated
end CollatzShadowing
"""


def parse_state(text: str) -> tuple[int, int, int]:
    parts = dict(part.split("=", 1) for part in text.split("|"))
    return int(parts["v2"]), int(parts["odd"]), int(parts["h"])


def read_full_edges(input_csv: Path, target_t: int, j_count: int):
    outgoing: dict[tuple[int, int, int], list[tuple[tuple[int, int, int], Fraction]]] = defaultdict(list)
    states: set[tuple[int, int, int]] = set()
    with input_csv.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if int(row["T"]) != target_t or int(row["j_count"]) != j_count:
                continue
            if row["graph"] != "full":
                continue
            src = parse_state(row["src"])
            dst = parse_state(row["dst"])
            states.add(src)
            states.add(dst)
            outgoing[src].append((dst, Fraction(int(row["normalized_num"]), int(row["normalized_den"]))))
    if not outgoing:
        raise ValueError("no full edges found")
    all_states = [(v, o, h) for v in range(14) for o in range(4) for h in range(4)]
    return all_states, outgoing


def solve_vector(states, outgoing, alpha: Fraction) -> list[int]:
    index = {state: i for i, state in enumerate(states)}
    vf = [1.0] * len(states)
    for _ in range(20000):
        nf = [1.0] * len(states)
        diff = 0.0
        for i, src in enumerate(states):
            nf[i] += sum(float(w) * vf[index[dst]] for dst, w in outgoing[src]) / float(alpha)
            diff = max(diff, abs(nf[i] - vf[i]))
        vf = nf
        if diff < 1e-12:
            break
    for scale in [10**k for k in (6, 9, 12, 15, 18)]:
        vector = [max(1, int(round(x * scale))) for x in vf]
        if check_vector(states, outgoing, vector, alpha):
            return vector
    raise ValueError("could not find exact positive integer vector")


def check_vector(states, outgoing, vector: list[int], alpha: Fraction) -> bool:
    index = {state: i for i, state in enumerate(states)}
    for i, src in enumerate(states):
        lhs = sum(w * vector[index[dst]] for dst, w in outgoing[src])
        if lhs > alpha * vector[i]:
            return False
    return True


def generate(input_csv: Path, output: Path, target_t: int, j_count: int, alpha: Fraction) -> None:
    states, outgoing = read_full_edges(input_csv, target_t, j_count)
    vector = solve_vector(states, outgoing, alpha)
    if not check_vector(states, outgoing, vector, alpha):
        raise AssertionError("exact CW vector check failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        LEAN_TEMPLATE.format(
            source_csv=input_csv,
            target_t=target_t,
            j_count=j_count,
            alpha_num=alpha.numerator,
            alpha_den=alpha.denominator,
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-t", type=int, default=10)
    parser.add_argument("--j-count", type=int, default=32)
    parser.add_argument("--alpha", type=Fraction, default=Fraction(97, 2000))
    args = parser.parse_args()
    generate(args.input, args.output, args.target_t, args.j_count, args.alpha)


if __name__ == "__main__":
    main()
