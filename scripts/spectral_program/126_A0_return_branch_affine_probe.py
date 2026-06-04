"""
126_A0_return_branch_affine_probe.py

Extract the affine form behind sampled A0 return labels.

For a fixed observed valuation word w along an odd Syracuse segment,

    n_s = alpha(w) * n_0 + beta(w),

with alpha(w) = 3^len(w) / 2^sum(w).  In the A0 trace model

    n_0 = residue + modulus * t,
    next_t = (n_s - residue) / modulus.

Thus each fixed word has an exact rational affine candidate

    next_t = slope * t + intercept.

The proof-facing bi-affine form used in Lean is obtained by splitting a
source residue class:

    t = q*u + r,    next_t = a*u + b.

For the observed valuation word itself, the odd source integer n lies in
one exact 2-adic cylinder

    n == word_residue        mod 2^(sum(word)+1).

Since the A0 coordinate is n = target_residue + target_modulus*t, this
induces a congruence for t.  The fields named `word_*` and
`branch_implies_word_congruence` record this arithmetic certificate.  It
does not prove that the branch is the first return in the full shadowing
logic; it only proves the valuation word/formula/state arithmetic on the
declared source progression.

For returned rows the script also checks a sufficient exact no-drop
certificate: every prefix value of the fixed word is an affine function
of `u`, and `n_i(u)-n_0(u)` has nonnegative affine numerator on the whole
progression `u >= 0`.

The `label_*` fields are a first exact attempt at the remaining
first-return gate.  They use only the definition of `best_shadow`: for an
affine prefix value `n_i(u)`, the condition that a phantom record is
visible is a linear congruence modulo `2^(sum_a+1)`.  Failure counters
therefore mean "a congruence class still exists and must be split or
controlled", not that a sampled row is wrong.

With --sample-mode dyadic-prefix, the script enumerates all selected
phase points with t < 2^prefix_bits.  That is a complete finite prefix
partition for the selected phases, not an infinite residue-class proof.

The optional --semantic-replay-step-cap flag performs a second finite outcome
replay with proof-facing priority: after each Syracuse step it checks
`cur < n0` before declaring a valuation tail.  This replay only records
summary counters in `stats`; it does not change the return-branch rows.
The optional --semantic-replay-word-audit flag adds compression counters for
semantic drop words; it is an audit aid, not a new branch extractor.
The optional --semantic-replay-suffix-certificate flag additionally stores
one compact exact row per observed suffix after the common semantic drop
prefix (1,1,2,1,1,1).  This is still a finite audit artifact.
Use --semantic-replay-certificate-cutoff to set the finite small-case cutoff
used by those certificate checks; the default 455 matches the original T14
audit, while later prefixes may need a larger finite cutoff.

This script is only a finite extraction/verification tool.  It does not
prove that a sampled return label persists for all u, and it does not
prove the low-v2 limit.

Run it with the project virtual environment from the repository root:

    .venv/bin/python scripts/spectral_program/126_A0_return_branch_affine_probe.py

The script itself uses only exact rational arithmetic, but it imports the
existing spectral/phantom helpers, which transitively require numpy/scipy.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from fractions import Fraction
from functools import lru_cache
from importlib import util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

INTERMEDIATE_RECORD_KEYS: tuple[tuple[int, int], ...] = (
    (10, 1),
    (11, 1),
    (12, 1),
    (12, 2),
    (20, 1),
)
INTERMEDIATE_CLASS_PROBE_SHIFTS = 8
INTERMEDIATE_CONTINUATION_EXTRA_BITS_CAP = 16
COMMON_SEMANTIC_DROP_PREFIX: tuple[int, ...] = (1, 1, 2, 1, 1, 1)


def load_module(filename: str, name: str):
    path = ROOT / filename
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def output_paths(tag: str | None) -> tuple[Path, Path]:
    suffix = "" if tag is None else "_" + "".join(
        ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag
    )
    stem = f"collatz_126{suffix}_A0_return_branch_affine_probe_branches"
    return ROOT / f"{stem}.csv", ROOT / f"{stem}.json"


def parse_phase(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected phase {text!r}; expected v2|odd|h")
    return int(parts[0]), int(parts[1]), int(parts[2])


def parse_phases(text: str) -> list[tuple[int, int, int]]:
    return [parse_phase(part.strip()) for part in text.split(",") if part.strip()]


def fmt_phase(phase: tuple[int, int, int]) -> str:
    return f"{phase[0]}|{phase[1]}|{phase[2]}"


def fmt_state(state: tuple[int, int, int]) -> str:
    return f"{state[0]}|{state[1]}|{state[2]}"


def record_count_field(key: tuple[int, int]) -> str:
    return f"label_intermediate_visible_k{key[0]}_c{key[1]}_failures"


def record_multiprobe_no_return_field(key: tuple[int, int]) -> str:
    return f"label_intermediate_multiprobe_no_return_k{key[0]}_c{key[1]}"


def parse_state(text: str) -> tuple[int, int, int]:
    parts = text.split("|")
    if len(parts) != 3:
        raise ValueError(f"unexpected state {text!r}; expected v2|odd|h")
    return int(parts[0]), int(parts[1]), int(parts[2])


def phase_progression(v2: int, odd: int, sample_limit: int) -> list[int]:
    modulus = 1 << (v2 + 2)
    start = odd << v2
    if start <= 0:
        start += modulus
    return [start + idx * modulus for idx in range(sample_limit)]


def phase_samples(v2: int, odd: int, sample_limit: int, span: int, mode: str) -> list[int]:
    if mode == "prefix":
        return phase_progression(v2, odd, sample_limit)
    if mode == "dyadic-prefix":
        modulus = 1 << (v2 + 2)
        start = odd << v2
        if start <= 0:
            start += modulus
        if start >= span:
            return []
        count = ((span - 1 - start) // modulus) + 1
        return [start + idx * modulus for idx in range(count)]
    if mode != "spread":
        raise ValueError(f"unknown sample mode: {mode}")
    modulus = 1 << (v2 + 2)
    start = odd << v2
    if start <= 0:
        start += modulus
    if start >= span:
        return []
    count = ((span - 1 - start) // modulus) + 1
    if count <= sample_limit:
        return [start + idx * modulus for idx in range(count)]
    indices = sorted({(idx * count) // sample_limit for idx in range(sample_limit)})
    return [start + idx * modulus for idx in indices]


def setup():
    op = load_module("75_critical_symbolic_operator.py", "critical_symbolic")
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")
    records = shadowing.phantom_records(10, 24)
    target = op.target_record(records, 12, 2)
    target_key = (12, 2, 1)
    residue, modulus, bits = op.residue_for(target, 1, shadows)
    return op, shadowing, records, target, target_key, residue, modulus, bits


def compressed_affine(word: tuple[int, ...]) -> tuple[Fraction, Fraction]:
    alpha = Fraction(1, 1)
    beta = Fraction(0, 1)
    for a in word:
        denom = 1 << a
        alpha = Fraction(3, denom) * alpha
        beta = Fraction(3, denom) * beta + Fraction(1, denom)
    return alpha, beta


def compressed_integer_coefficients(word: tuple[int, ...]) -> tuple[int, int, int]:
    """Return P, C, A such that S_word(n) = (P*n + C) / 2^A."""
    power3 = 1
    constant = 0
    total_a = 0
    for a in word:
        constant = 3 * constant + (1 << total_a)
        power3 *= 3
        total_a += a
    return power3, constant, total_a


def common_prefix_suffix_threshold(word: tuple[int, ...]) -> tuple[bool, int]:
    """Slope/intercept threshold after the common semantic-drop prefix.

    For a suffix `s`, the common-prefix formula is

        128*y = 729*n + 817.

    The sufficient scaled contraction condition is

        3^len(s)*(729*n+817) + 128*C_s < 128*2^A_s*n.

    This returns whether the slope gap is positive and, if so, the smallest
    natural `n` satisfying the strict inequality.
    """
    power3, constant, total_a = compressed_integer_coefficients(word)
    gap = 128 * (1 << total_a) - 729 * power3
    if gap <= 0:
        return False, 0
    intercept = 817 * power3 + 128 * constant
    return True, intercept // gap + 1


def prefix_integer_coefficients(word: tuple[int, ...]) -> list[tuple[int, int, int]]:
    """Prefix coefficients P, C, A for every nonempty prefix of word."""
    power3 = 1
    constant = 0
    total_a = 0
    out: list[tuple[int, int, int]] = []
    for a in word:
        constant = 3 * constant + (1 << total_a)
        power3 *= 3
        total_a += a
        out.append((power3, constant, total_a))
    return out


def no_drop_affine_failure_count(
    *,
    word: tuple[int, ...],
    target_residue: int,
    target_modulus: int,
    q: int,
    r: int,
) -> int:
    """Sufficient certificate that no prefix drops below n0 for all u >= 0."""
    n0_slope = target_modulus * q
    n0_intercept = target_residue + target_modulus * r
    failures = 0
    for power3, constant, total_a in prefix_integer_coefficients(word):
        denominator = 1 << total_a
        slope_num = (power3 - denominator) * n0_slope
        intercept_num = (power3 - denominator) * n0_intercept + constant
        if slope_num < 0 or intercept_num < 0:
            failures += 1
    return failures


def v2_nat(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    out = 0
    while n % 2 == 0:
        n //= 2
        out += 1
    return out


def solve_linear_congruence_mod_power_two(
    slope: int, intercept: int, bits: int
) -> tuple[bool, int, int]:
    """Solve slope*u + intercept == 0 mod 2^bits.

    Returns `(has_solution, residue, modulus_bits)`, where a solution set
    is represented by `u == residue mod 2^modulus_bits`.  `modulus_bits=0`
    means all integers modulo `1`.
    """
    if bits <= 0:
        return True, 0, 0
    if slope == 0:
        if intercept % (1 << bits) == 0:
            return True, 0, 0
        return False, 0, 0
    common_bits = min(v2_nat(slope), bits)
    if intercept % (1 << common_bits) != 0:
        return False, 0, 0
    modulus_bits = bits - common_bits
    if modulus_bits == 0:
        return True, 0, 0
    modulus = 1 << modulus_bits
    reduced_slope = (slope >> common_bits) % modulus
    reduced_intercept = intercept >> common_bits
    residue = (-reduced_intercept * pow(reduced_slope, -1, modulus)) % modulus
    return True, residue, modulus_bits


def prefix_affine_coefficients(
    *,
    word: tuple[int, ...],
    target_residue: int,
    target_modulus: int,
    q: int,
    r: int,
) -> tuple[list[tuple[int, int]], int]:
    """Integer affine forms n_i(u)=s_i*u+c_i for all nonempty prefixes."""
    n0_slope = target_modulus * q
    n0_intercept = target_residue + target_modulus * r
    failures = 0
    out: list[tuple[int, int]] = []
    for power3, constant, total_a in prefix_integer_coefficients(word):
        denominator = 1 << total_a
        slope_num = power3 * n0_slope
        intercept_num = power3 * n0_intercept + constant
        if slope_num % denominator != 0 or intercept_num % denominator != 0:
            failures += 1
            out.append((0, 0))
        else:
            out.append((slope_num // denominator, intercept_num // denominator))
    return out, failures


def record_visibility_solution(
    *,
    n_slope: int,
    n_intercept: int,
    record: dict[str, Any],
    bits: int,
) -> tuple[bool, int, int]:
    """Whether v2(n(u)-q_record) >= bits can occur for some integer u."""
    q_record: Fraction = record["q"]
    slope = n_slope * q_record.denominator
    intercept = n_intercept * q_record.denominator - q_record.numerator
    return solve_linear_congruence_mod_power_two(slope, intercept, bits)


def congruence_classes_intersect(
    residue_a: int,
    bits_a: int,
    residue_b: int,
    bits_b: int,
) -> bool:
    """Whether two classes modulo powers of two have a common integer."""
    common_bits = min(bits_a, bits_b)
    if common_bits <= 0:
        return True
    return (residue_a - residue_b) % (1 << common_bits) == 0


def congruence_class_contains(
    outer_residue: int,
    outer_bits: int,
    inner_residue: int,
    inner_bits: int,
) -> bool:
    """Whether the inner power-of-two congruence class is contained in outer."""
    if outer_bits <= 0:
        return True
    if inner_bits < outer_bits:
        return False
    return (inner_residue - outer_residue) % (1 << outer_bits) == 0


def classify_return_result(result: dict[str, Any], final_step: int) -> str:
    if result.get("terminal"):
        if result.get("unresolved"):
            return "no_return_by_final"
        return "terminal_by_final"
    step = int(result["step"])
    if step < final_step:
        return "early_target"
    if step == final_step:
        return "same_step"
    return "no_return_by_final"


def trace_target_word(
    *,
    op,
    shadowing,
    records: list[dict[str, Any]],
    target_key: tuple[int, int, int],
    target_residue: int,
    target_modulus: int,
    n0: int,
    max_steps: int,
) -> dict[str, Any]:
    """Trace until the next target return, keeping the valuation word."""
    cur = n0
    last_key = target_key
    word: list[int] = []
    for step in range(1, max_steps + 1):
        a_val, cur = shadowing.odd_syracuse_step(cur)
        word.append(a_val)
        if cur < n0:
            return {"terminal": 1, "step": step, "word": tuple(word)}

        key, _best_v = op.best_shadow(cur, records, shadowing)
        if key is None:
            last_key = None
            continue
        if key != last_key:
            if key == target_key:
                return {
                    "terminal": 0,
                    "step": step,
                    "word": tuple(word),
                    "next_t": op.local_t_from_residue(
                        cur,
                        target_residue,
                        target_modulus,
                    ),
                }
            last_key = key
    return {"terminal": 1, "unresolved": 1, "step": max_steps, "word": tuple(word)}


def label_certificate_attempt(
    *,
    op,
    shadowing,
    word: tuple[int, ...],
    target_residue: int,
    target_modulus: int,
    q: int,
    r: int,
    records: list[dict[str, Any]],
    target: dict[str, Any],
    target_key: tuple[int, int, int],
    post_final_step_cap: int,
) -> dict[str, Any]:
    """Exact congruence diagnostic for the `best_shadow` part of first return.

    A zero intermediate counter proves that every proper prefix has no
    visible phantom label for any integer `u` on the branch.  At the final
    prefix, `final_target_low_failure=0` proves target visibility at level
    `b=1`; `final_target_high_lift_failures>0` means sparse residues can
    lift the same target to `b>=2`, so exact global constancy is not yet
    proved without splitting those residues.
    """
    affines, prefix_integrality_failures = prefix_affine_coefficients(
        word=word,
        target_residue=target_residue,
        target_modulus=target_modulus,
        q=q,
        r=r,
    )
    intermediate_visible_failures = 0
    intermediate_visible_checks = 0
    intermediate_target_visible_failures = 0
    intermediate_competing_visible_failures = 0
    intermediate_target_visible_prefixes = 0
    intermediate_competing_visible_prefixes = 0
    intermediate_visible_by_record = {key: 0 for key in INTERMEDIATE_RECORD_KEYS}
    intermediate_probe_total = 0
    intermediate_probe_candidate_selected = 0
    intermediate_probe_target_selected = 0
    intermediate_probe_competing_selected = 0
    intermediate_probe_none_selected = 0
    intermediate_probe_same_step_return = 0
    intermediate_probe_early_target_return = 0
    intermediate_probe_no_return_by_final = 0
    intermediate_probe_terminal_by_final = 0
    intermediate_multiprobe_total = 0
    intermediate_multiprobe_same_step_return = 0
    intermediate_multiprobe_early_target_return = 0
    intermediate_multiprobe_no_return_by_final = 0
    intermediate_multiprobe_terminal_by_final = 0
    intermediate_target_multiprobe_total = 0
    intermediate_target_multiprobe_same_step_return = 0
    intermediate_target_multiprobe_early_target_return = 0
    intermediate_target_multiprobe_no_return_by_final = 0
    intermediate_target_multiprobe_terminal_by_final = 0
    intermediate_multiprobe_no_return_by_record = {
        key: 0 for key in INTERMEDIATE_RECORD_KEYS
    }
    intermediate_multiprobe_no_return_extended_later_target = 0
    intermediate_multiprobe_no_return_extended_terminal = 0
    intermediate_multiprobe_no_return_extended_unresolved = 0
    intermediate_multiprobe_no_return_later_target_min_delta = 0
    intermediate_multiprobe_no_return_later_target_max_delta = 0
    intermediate_multiprobe_no_return_continuation_supported = 0
    intermediate_multiprobe_no_return_continuation_integrality_failures = 0
    intermediate_multiprobe_no_return_continuation_no_drop_failures = 0
    intermediate_multiprobe_no_return_actual_prefix_matches = 0
    intermediate_multiprobe_no_return_suffix_target_word_matches = 0
    intermediate_multiprobe_no_return_actual_continuation_supported = 0
    intermediate_multiprobe_no_return_actual_continuation_integrality_failures = 0
    intermediate_multiprobe_no_return_actual_continuation_no_drop_failures = 0
    intermediate_multiprobe_no_return_actual_refined_continuation_supported = 0
    intermediate_multiprobe_no_return_actual_refined_continuation_failures = 0
    intermediate_multiprobe_no_return_actual_refined_extra_bits_min = 0
    intermediate_multiprobe_no_return_actual_refined_extra_bits_max = 0
    target_word = tuple(int(a) for a in target["word"])
    intermediate_competing_classes = []
    intermediate_target_classes = []
    intermediate_competing_no_later_target_intersections = 0
    intermediate_competing_later_target_intersections = 0
    intermediate_target_persistent_visibility = 0
    intermediate_target_missing_prior_visibility = 0
    intermediate_target_no_prior_competing_intersections = 0
    intermediate_target_prior_competing_intersections = 0
    intermediate_target_high_lift_covered = 0
    intermediate_target_low_only_visible = 0
    intermediate_boundary_density = Fraction(0, 1)
    intermediate_boundary_min_mod_bits = 0
    intermediate_target_min_mod_bits = 0
    intermediate_competing_min_mod_bits = 0
    final_competing_failures = 0
    final_competing_checks = 0
    final_target_low_failure = 1
    final_target_high_lift_failures = 1
    final_target_high_lift_mod_bits = 0
    final_target_high_lift_residue = 0
    if not affines:
        return {
            "label_prefix_integrality_failures": 1,
            "label_intermediate_visible_failures": 1,
            "label_intermediate_visible_checks": 0,
            "label_intermediate_target_visible_failures": 0,
            "label_intermediate_competing_visible_failures": 0,
            "label_intermediate_target_visible_prefixes": 0,
            "label_intermediate_competing_visible_prefixes": 0,
            **{record_count_field(key): 0 for key in INTERMEDIATE_RECORD_KEYS},
            "label_intermediate_probe_total": 0,
            "label_intermediate_probe_candidate_selected": 0,
            "label_intermediate_probe_target_selected": 0,
            "label_intermediate_probe_competing_selected": 0,
            "label_intermediate_probe_none_selected": 0,
            "label_intermediate_probe_same_step_return": 0,
            "label_intermediate_probe_early_target_return": 0,
            "label_intermediate_probe_no_return_by_final": 0,
            "label_intermediate_probe_terminal_by_final": 0,
            "label_intermediate_multiprobe_total": 0,
            "label_intermediate_multiprobe_same_step_return": 0,
            "label_intermediate_multiprobe_early_target_return": 0,
            "label_intermediate_multiprobe_no_return_by_final": 0,
            "label_intermediate_multiprobe_terminal_by_final": 0,
            "label_intermediate_target_multiprobe_total": 0,
            "label_intermediate_target_multiprobe_same_step_return": 0,
            "label_intermediate_target_multiprobe_early_target_return": 0,
            "label_intermediate_target_multiprobe_no_return_by_final": 0,
            "label_intermediate_target_multiprobe_terminal_by_final": 0,
            **{record_multiprobe_no_return_field(key): 0 for key in INTERMEDIATE_RECORD_KEYS},
            "label_intermediate_multiprobe_no_return_extended_later_target": 0,
            "label_intermediate_multiprobe_no_return_extended_terminal": 0,
            "label_intermediate_multiprobe_no_return_extended_unresolved": 0,
            "label_intermediate_multiprobe_no_return_later_target_min_delta": 0,
            "label_intermediate_multiprobe_no_return_later_target_max_delta": 0,
            "label_intermediate_multiprobe_no_return_continuation_supported": 0,
            "label_intermediate_multiprobe_no_return_continuation_integrality_failures": 0,
            "label_intermediate_multiprobe_no_return_continuation_no_drop_failures": 0,
            "label_intermediate_multiprobe_no_return_actual_prefix_matches": 0,
            "label_intermediate_multiprobe_no_return_suffix_target_word_matches": 0,
            "label_intermediate_multiprobe_no_return_actual_continuation_supported": 0,
            "label_intermediate_multiprobe_no_return_actual_continuation_integrality_failures": 0,
            "label_intermediate_multiprobe_no_return_actual_continuation_no_drop_failures": 0,
            "label_intermediate_multiprobe_no_return_actual_refined_continuation_supported": 0,
            "label_intermediate_multiprobe_no_return_actual_refined_continuation_failures": 0,
            "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_min": 0,
            "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_max": 0,
            "label_intermediate_competing_no_later_target_intersections": 0,
            "label_intermediate_competing_later_target_intersections": 0,
            "label_intermediate_target_persistent_visibility": 0,
            "label_intermediate_target_missing_prior_visibility": 0,
            "label_intermediate_target_no_prior_competing_intersections": 0,
            "label_intermediate_target_prior_competing_intersections": 0,
            "label_intermediate_target_high_lift_covered": 0,
            "label_intermediate_target_low_only_visible": 0,
            "label_final_target_low_failure": 1,
            "label_final_target_high_lift_failures": 1,
            "label_final_target_high_lift_mod_bits": 0,
            "label_final_target_high_lift_residue": 0,
            "label_final_competing_failures": 1,
            "label_final_competing_checks": 0,
            "label_intermediate_boundary_density_num": 0,
            "label_intermediate_boundary_density_den": 1,
            "label_intermediate_boundary_min_mod_bits": 0,
            "label_intermediate_target_min_mod_bits": 0,
            "label_intermediate_competing_min_mod_bits": 0,
            "label_certificate_status": "no_prefixes",
        }

    for prefix_idx, (n_slope, n_intercept) in enumerate(affines[:-1]):
        prefix_target_visible = False
        prefix_competing_visible = False
        for record in records:
            threshold_bits = int(record["sum_a"]) + 1
            key_base = (int(record["k"]), int(record["cycle_id"]))
            intermediate_visible_checks += 1
            has_solution, residue_u, modulus_bits_u = record_visibility_solution(
                n_slope=n_slope,
                n_intercept=n_intercept,
                record=record,
                bits=threshold_bits,
            )
            if has_solution:
                intermediate_visible_failures += 1
                intermediate_boundary_density += Fraction(1, 1 << modulus_bits_u)
                if (
                    intermediate_boundary_min_mod_bits == 0
                    or modulus_bits_u < intermediate_boundary_min_mod_bits
                ):
                    intermediate_boundary_min_mod_bits = modulus_bits_u
                if key_base == (target_key[0], target_key[1]):
                    intermediate_target_visible_failures += 1
                    prefix_target_visible = True
                    intermediate_target_classes.append(
                        {
                            "prefix_idx": prefix_idx,
                            "residue": residue_u,
                            "mod_bits": modulus_bits_u,
                        }
                    )
                    if (
                        intermediate_target_min_mod_bits == 0
                        or modulus_bits_u < intermediate_target_min_mod_bits
                    ):
                        intermediate_target_min_mod_bits = modulus_bits_u
                    high_bits = 2 * int(record["sum_a"]) + 1
                    high_has_solution, high_residue, high_mod_bits = (
                        record_visibility_solution(
                            n_slope=n_slope,
                            n_intercept=n_intercept,
                            record=record,
                            bits=high_bits,
                        )
                    )
                    if (
                        high_has_solution
                        and congruence_class_contains(
                            int(high_residue),
                            int(high_mod_bits),
                            int(residue_u),
                            int(modulus_bits_u),
                        )
                    ):
                        intermediate_target_high_lift_covered += 1
                    else:
                        intermediate_target_low_only_visible += 1
                else:
                    intermediate_competing_visible_failures += 1
                    prefix_competing_visible = True
                    intermediate_competing_classes.append(
                        {
                            "prefix_idx": prefix_idx,
                            "residue": residue_u,
                            "mod_bits": modulus_bits_u,
                        }
                    )
                    if (
                        intermediate_competing_min_mod_bits == 0
                        or modulus_bits_u < intermediate_competing_min_mod_bits
                    ):
                        intermediate_competing_min_mod_bits = modulus_bits_u
                if key_base in intermediate_visible_by_record:
                    intermediate_visible_by_record[key_base] += 1
                representative_u = residue_u
                representative_t = q * representative_u + r
                representative_n0 = target_residue + target_modulus * representative_t
                representative_prefix_n = n_slope * representative_u + n_intercept
                selected_key, _selected_v = op.best_shadow(
                    representative_prefix_n,
                    records,
                    shadowing,
                )
                intermediate_probe_total += 1
                if selected_key is None:
                    intermediate_probe_none_selected += 1
                else:
                    selected_base = (selected_key[0], selected_key[1])
                    if selected_base == key_base:
                        intermediate_probe_candidate_selected += 1
                    if selected_base == (target_key[0], target_key[1]):
                        intermediate_probe_target_selected += 1
                    else:
                        intermediate_probe_competing_selected += 1
                representative_result = op.first_return_or_terminal(
                    representative_n0,
                    records,
                    target,
                    target_key,
                    target_residue,
                    target_modulus,
                    shadowing,
                    len(word),
                )
                representative_kind = classify_return_result(representative_result, len(word))
                if representative_kind == "same_step":
                    intermediate_probe_same_step_return += 1
                elif representative_kind == "early_target":
                    intermediate_probe_early_target_return += 1
                elif representative_kind == "no_return_by_final":
                    intermediate_probe_no_return_by_final += 1
                else:
                    intermediate_probe_terminal_by_final += 1

                class_modulus = 1 << modulus_bits_u
                for shift in range(INTERMEDIATE_CLASS_PROBE_SHIFTS):
                    probe_u = residue_u + shift * class_modulus
                    probe_t = q * probe_u + r
                    probe_n0 = target_residue + target_modulus * probe_t
                    probe_result = op.first_return_or_terminal(
                        probe_n0,
                        records,
                        target,
                        target_key,
                        target_residue,
                        target_modulus,
                        shadowing,
                        len(word),
                    )
                    probe_kind = classify_return_result(probe_result, len(word))
                    intermediate_multiprobe_total += 1
                    if key_base == (target_key[0], target_key[1]):
                        intermediate_target_multiprobe_total += 1
                    if probe_kind == "same_step":
                        intermediate_multiprobe_same_step_return += 1
                        if key_base == (target_key[0], target_key[1]):
                            intermediate_target_multiprobe_same_step_return += 1
                    elif probe_kind == "early_target":
                        intermediate_multiprobe_early_target_return += 1
                        if key_base == (target_key[0], target_key[1]):
                            intermediate_target_multiprobe_early_target_return += 1
                    elif probe_kind == "no_return_by_final":
                        intermediate_multiprobe_no_return_by_final += 1
                        if key_base == (target_key[0], target_key[1]):
                            intermediate_target_multiprobe_no_return_by_final += 1
                        if key_base in intermediate_multiprobe_no_return_by_record:
                            intermediate_multiprobe_no_return_by_record[key_base] += 1
                        extended_result = op.first_return_or_terminal(
                            probe_n0,
                            records,
                            target,
                            target_key,
                            target_residue,
                            target_modulus,
                            shadowing,
                            max(post_final_step_cap, len(word)),
                        )
                        if extended_result.get("terminal"):
                            if extended_result.get("unresolved"):
                                intermediate_multiprobe_no_return_extended_unresolved += 1
                            else:
                                intermediate_multiprobe_no_return_extended_terminal += 1
                        else:
                            intermediate_multiprobe_no_return_extended_later_target += 1
                            later_delta = int(extended_result["step"]) - len(word)
                            if (
                                intermediate_multiprobe_no_return_later_target_min_delta == 0
                                or later_delta
                                < intermediate_multiprobe_no_return_later_target_min_delta
                            ):
                                intermediate_multiprobe_no_return_later_target_min_delta = later_delta
                            if (
                                later_delta
                                > intermediate_multiprobe_no_return_later_target_max_delta
                            ):
                                intermediate_multiprobe_no_return_later_target_max_delta = later_delta
                            actual_trace = trace_target_word(
                                op=op,
                                shadowing=shadowing,
                                records=records,
                                target_key=target_key,
                                target_residue=target_residue,
                                target_modulus=target_modulus,
                                n0=probe_n0,
                                max_steps=max(post_final_step_cap, len(word)),
                            )
                            actual_word = tuple(int(a) for a in actual_trace["word"])
                            if actual_word[: len(word)] == word:
                                intermediate_multiprobe_no_return_actual_prefix_matches += 1
                            if actual_word[len(word):] == target_word:
                                intermediate_multiprobe_no_return_suffix_target_word_matches += 1
                            extended_word = word + target_word
                            sub_modulus = class_modulus * INTERMEDIATE_CLASS_PROBE_SHIFTS
                            sub_q = q * sub_modulus
                            sub_r = q * probe_u + r
                            slope, intercept = return_t_formula(
                                extended_word,
                                target_residue,
                                target_modulus,
                            )
                            a_frac = slope * sub_q
                            b_frac = slope * probe_u * q + slope * r + intercept
                            integrality_failure = int(
                                a_frac.denominator != 1 or b_frac.denominator != 1
                            )
                            no_drop_failures = no_drop_affine_failure_count(
                                word=extended_word,
                                target_residue=target_residue,
                                target_modulus=target_modulus,
                                q=sub_q,
                                r=sub_r,
                            )
                            intermediate_multiprobe_no_return_continuation_integrality_failures += (
                                integrality_failure
                            )
                            intermediate_multiprobe_no_return_continuation_no_drop_failures += (
                                no_drop_failures
                            )
                            if integrality_failure == 0 and no_drop_failures == 0:
                                intermediate_multiprobe_no_return_continuation_supported += 1
                            actual_slope, actual_intercept = return_t_formula(
                                actual_word,
                                target_residue,
                                target_modulus,
                            )
                            actual_a_frac = actual_slope * sub_q
                            actual_b_frac = actual_slope * sub_r + actual_intercept
                            actual_integrality_failure = int(
                                actual_a_frac.denominator != 1
                                or actual_b_frac.denominator != 1
                            )
                            actual_no_drop_failures = no_drop_affine_failure_count(
                                word=actual_word,
                                target_residue=target_residue,
                                target_modulus=target_modulus,
                                q=sub_q,
                                r=sub_r,
                            )
                            intermediate_multiprobe_no_return_actual_continuation_integrality_failures += (
                                actual_integrality_failure
                            )
                            intermediate_multiprobe_no_return_actual_continuation_no_drop_failures += (
                                actual_no_drop_failures
                            )
                            if (
                                actual_integrality_failure == 0
                                and actual_no_drop_failures == 0
                            ):
                                intermediate_multiprobe_no_return_actual_continuation_supported += 1
                            refined_supported = False
                            for extra_bits in range(INTERMEDIATE_CONTINUATION_EXTRA_BITS_CAP + 1):
                                refined_sub_q = sub_q * (1 << extra_bits)
                                refined_a_frac = actual_slope * refined_sub_q
                                refined_b_frac = actual_b_frac
                                refined_integrality_failure = int(
                                    refined_a_frac.denominator != 1
                                    or refined_b_frac.denominator != 1
                                )
                                refined_no_drop_failures = no_drop_affine_failure_count(
                                    word=actual_word,
                                    target_residue=target_residue,
                                    target_modulus=target_modulus,
                                    q=refined_sub_q,
                                    r=sub_r,
                                )
                                if (
                                    refined_integrality_failure == 0
                                    and refined_no_drop_failures == 0
                                ):
                                    refined_supported = True
                                    intermediate_multiprobe_no_return_actual_refined_continuation_supported += 1
                                    if (
                                        intermediate_multiprobe_no_return_actual_refined_extra_bits_min == 0
                                        or extra_bits
                                        < intermediate_multiprobe_no_return_actual_refined_extra_bits_min
                                    ):
                                        intermediate_multiprobe_no_return_actual_refined_extra_bits_min = extra_bits
                                    if (
                                        extra_bits
                                        > intermediate_multiprobe_no_return_actual_refined_extra_bits_max
                                    ):
                                        intermediate_multiprobe_no_return_actual_refined_extra_bits_max = extra_bits
                                    break
                            if not refined_supported:
                                intermediate_multiprobe_no_return_actual_refined_continuation_failures += 1
                    else:
                        intermediate_multiprobe_terminal_by_final += 1
                        if key_base == (target_key[0], target_key[1]):
                            intermediate_target_multiprobe_terminal_by_final += 1
        intermediate_target_visible_prefixes += int(prefix_target_visible)
        intermediate_competing_visible_prefixes += int(prefix_competing_visible)

    for cls in intermediate_competing_classes:
        has_later_target_intersection = any(
            target_cls["prefix_idx"] > cls["prefix_idx"]
            and congruence_classes_intersect(
                int(cls["residue"]),
                int(cls["mod_bits"]),
                int(target_cls["residue"]),
                int(target_cls["mod_bits"]),
            )
            for target_cls in intermediate_target_classes
        )
        if has_later_target_intersection:
            intermediate_competing_later_target_intersections += 1
        else:
            intermediate_competing_no_later_target_intersections += 1

    target_classes_by_prefix: dict[int, list[dict[str, int]]] = {}
    for target_cls in intermediate_target_classes:
        target_classes_by_prefix.setdefault(int(target_cls["prefix_idx"]), []).append(target_cls)

    for cls in intermediate_target_classes:
        prefix_idx = int(cls["prefix_idx"])
        has_prior_competing_intersection = any(
            int(competing_cls["prefix_idx"]) < prefix_idx
            and congruence_classes_intersect(
                int(cls["residue"]),
                int(cls["mod_bits"]),
                int(competing_cls["residue"]),
                int(competing_cls["mod_bits"]),
            )
            for competing_cls in intermediate_competing_classes
        )
        if has_prior_competing_intersection:
            intermediate_target_prior_competing_intersections += 1
        else:
            intermediate_target_no_prior_competing_intersections += 1

        persistent_target = True
        for prior_prefix in range(prefix_idx):
            if not any(
                congruence_class_contains(
                    int(prior_target_cls["residue"]),
                    int(prior_target_cls["mod_bits"]),
                    int(cls["residue"]),
                    int(cls["mod_bits"]),
                )
                for prior_target_cls in target_classes_by_prefix.get(prior_prefix, [])
            ):
                persistent_target = False
                break
        if persistent_target:
            intermediate_target_persistent_visibility += 1
        else:
            intermediate_target_missing_prior_visibility += 1

    final_slope, final_intercept = affines[-1]
    for record in records:
        threshold_bits = int(record["sum_a"]) + 1
        key_base = (int(record["k"]), int(record["cycle_id"]))
        has_basic, _basic_residue, _basic_mod_bits = record_visibility_solution(
            n_slope=final_slope,
            n_intercept=final_intercept,
            record=record,
            bits=threshold_bits,
        )
        if key_base == (target_key[0], target_key[1]):
            final_target_low_failure = 0 if has_basic else 1
            high_bits = 2 * int(record["sum_a"]) + 1
            high_has_solution, high_residue, high_mod_bits = record_visibility_solution(
                n_slope=final_slope,
                n_intercept=final_intercept,
                record=record,
                bits=high_bits,
            )
            final_target_high_lift_failures = int(high_has_solution)
            final_target_high_lift_residue = high_residue if high_has_solution else 0
            final_target_high_lift_mod_bits = high_mod_bits if high_has_solution else 0
        else:
            final_competing_checks += 1
            if has_basic:
                final_competing_failures += 1

    if prefix_integrality_failures:
        status = "blocked_prefix_integrality"
    elif intermediate_visible_failures or final_target_low_failure or final_competing_failures:
        status = "blocked_label_congruence"
    elif final_target_high_lift_failures:
        status = "target_high_lift_boundary"
    else:
        status = "proved_constant_target_b1"

    return {
        "label_prefix_integrality_failures": prefix_integrality_failures,
        "label_intermediate_visible_failures": intermediate_visible_failures,
        "label_intermediate_visible_checks": intermediate_visible_checks,
        "label_intermediate_target_visible_failures": intermediate_target_visible_failures,
        "label_intermediate_competing_visible_failures": intermediate_competing_visible_failures,
        "label_intermediate_target_visible_prefixes": intermediate_target_visible_prefixes,
        "label_intermediate_competing_visible_prefixes": intermediate_competing_visible_prefixes,
        **{
            record_count_field(key): intermediate_visible_by_record[key]
            for key in INTERMEDIATE_RECORD_KEYS
        },
        "label_intermediate_probe_total": intermediate_probe_total,
        "label_intermediate_probe_candidate_selected": intermediate_probe_candidate_selected,
        "label_intermediate_probe_target_selected": intermediate_probe_target_selected,
        "label_intermediate_probe_competing_selected": intermediate_probe_competing_selected,
        "label_intermediate_probe_none_selected": intermediate_probe_none_selected,
        "label_intermediate_probe_same_step_return": intermediate_probe_same_step_return,
        "label_intermediate_probe_early_target_return": intermediate_probe_early_target_return,
        "label_intermediate_probe_no_return_by_final": intermediate_probe_no_return_by_final,
        "label_intermediate_probe_terminal_by_final": intermediate_probe_terminal_by_final,
        "label_intermediate_multiprobe_total": intermediate_multiprobe_total,
        "label_intermediate_multiprobe_same_step_return": intermediate_multiprobe_same_step_return,
        "label_intermediate_multiprobe_early_target_return": intermediate_multiprobe_early_target_return,
        "label_intermediate_multiprobe_no_return_by_final": intermediate_multiprobe_no_return_by_final,
        "label_intermediate_multiprobe_terminal_by_final": intermediate_multiprobe_terminal_by_final,
        "label_intermediate_target_multiprobe_total": intermediate_target_multiprobe_total,
        "label_intermediate_target_multiprobe_same_step_return":
            intermediate_target_multiprobe_same_step_return,
        "label_intermediate_target_multiprobe_early_target_return":
            intermediate_target_multiprobe_early_target_return,
        "label_intermediate_target_multiprobe_no_return_by_final":
            intermediate_target_multiprobe_no_return_by_final,
        "label_intermediate_target_multiprobe_terminal_by_final":
            intermediate_target_multiprobe_terminal_by_final,
        **{
            record_multiprobe_no_return_field(key):
                intermediate_multiprobe_no_return_by_record[key]
            for key in INTERMEDIATE_RECORD_KEYS
        },
        "label_intermediate_multiprobe_no_return_extended_later_target":
            intermediate_multiprobe_no_return_extended_later_target,
        "label_intermediate_multiprobe_no_return_extended_terminal":
            intermediate_multiprobe_no_return_extended_terminal,
        "label_intermediate_multiprobe_no_return_extended_unresolved":
            intermediate_multiprobe_no_return_extended_unresolved,
        "label_intermediate_multiprobe_no_return_later_target_min_delta":
            intermediate_multiprobe_no_return_later_target_min_delta,
        "label_intermediate_multiprobe_no_return_later_target_max_delta":
            intermediate_multiprobe_no_return_later_target_max_delta,
        "label_intermediate_multiprobe_no_return_continuation_supported":
            intermediate_multiprobe_no_return_continuation_supported,
        "label_intermediate_multiprobe_no_return_continuation_integrality_failures":
            intermediate_multiprobe_no_return_continuation_integrality_failures,
        "label_intermediate_multiprobe_no_return_continuation_no_drop_failures":
            intermediate_multiprobe_no_return_continuation_no_drop_failures,
        "label_intermediate_multiprobe_no_return_actual_prefix_matches":
            intermediate_multiprobe_no_return_actual_prefix_matches,
        "label_intermediate_multiprobe_no_return_suffix_target_word_matches":
            intermediate_multiprobe_no_return_suffix_target_word_matches,
        "label_intermediate_multiprobe_no_return_actual_continuation_supported":
            intermediate_multiprobe_no_return_actual_continuation_supported,
        "label_intermediate_multiprobe_no_return_actual_continuation_integrality_failures":
            intermediate_multiprobe_no_return_actual_continuation_integrality_failures,
        "label_intermediate_multiprobe_no_return_actual_continuation_no_drop_failures":
            intermediate_multiprobe_no_return_actual_continuation_no_drop_failures,
        "label_intermediate_multiprobe_no_return_actual_refined_continuation_supported":
            intermediate_multiprobe_no_return_actual_refined_continuation_supported,
        "label_intermediate_multiprobe_no_return_actual_refined_continuation_failures":
            intermediate_multiprobe_no_return_actual_refined_continuation_failures,
        "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_min":
            intermediate_multiprobe_no_return_actual_refined_extra_bits_min,
        "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_max":
            intermediate_multiprobe_no_return_actual_refined_extra_bits_max,
        "label_intermediate_competing_no_later_target_intersections":
            intermediate_competing_no_later_target_intersections,
        "label_intermediate_competing_later_target_intersections":
            intermediate_competing_later_target_intersections,
        "label_intermediate_target_persistent_visibility":
            intermediate_target_persistent_visibility,
        "label_intermediate_target_missing_prior_visibility":
            intermediate_target_missing_prior_visibility,
        "label_intermediate_target_no_prior_competing_intersections":
            intermediate_target_no_prior_competing_intersections,
        "label_intermediate_target_prior_competing_intersections":
            intermediate_target_prior_competing_intersections,
        "label_intermediate_target_high_lift_covered":
            intermediate_target_high_lift_covered,
        "label_intermediate_target_low_only_visible":
            intermediate_target_low_only_visible,
        "label_final_target_low_failure": final_target_low_failure,
        "label_final_target_high_lift_failures": final_target_high_lift_failures,
        "label_final_target_high_lift_mod_bits": final_target_high_lift_mod_bits,
        "label_final_target_high_lift_residue": final_target_high_lift_residue,
        "label_final_competing_failures": final_competing_failures,
        "label_final_competing_checks": final_competing_checks,
        "label_intermediate_boundary_density_num": intermediate_boundary_density.numerator,
        "label_intermediate_boundary_density_den": intermediate_boundary_density.denominator,
        "label_intermediate_boundary_min_mod_bits": intermediate_boundary_min_mod_bits,
        "label_intermediate_target_min_mod_bits": intermediate_target_min_mod_bits,
        "label_intermediate_competing_min_mod_bits": intermediate_competing_min_mod_bits,
        "label_certificate_status": status,
    }


def high_lift_continuation_attempt(
    *,
    word: tuple[int, ...],
    target_word: tuple[int, ...],
    target_residue: int,
    target_modulus: int,
    q: int,
    r: int,
    high_lift_residue: int,
    high_lift_mod_bits: int,
    has_high_lift: bool,
) -> dict[str, Any]:
    """Exact arithmetic for the target high-lift continuation branch.

    If the first target hit lands in lift `b >= 2`, the expected next
    proof-facing branch appends one target phantom period.  This function
    does not prove automaton minimality; it checks that the composed word
    gives an integral affine return formula on the high-lift residue class
    and that the composed word has the same no-drop affine certificate.
    """
    if not has_high_lift or high_lift_mod_bits <= 0:
        return {
            "high_lift_continuation_supported": 0,
            "high_lift_continuation_step": 0,
            "high_lift_continuation_word_sum": 0,
            "high_lift_continuation_q": 0,
            "high_lift_continuation_r": 0,
            "high_lift_continuation_a": 0,
            "high_lift_continuation_b": 0,
            "high_lift_continuation_integrality_failures": 1,
            "high_lift_continuation_no_drop_failures": 1,
        }

    extended_word = word + target_word
    split_modulus = 1 << high_lift_mod_bits
    refined_q = q * split_modulus
    refined_r = q * high_lift_residue + r
    slope, intercept = return_t_formula(extended_word, target_residue, target_modulus)
    a_frac = slope * refined_q
    b_frac = slope * refined_r + intercept
    integrality_failures = 0
    if a_frac.denominator != 1 or b_frac.denominator != 1:
        integrality_failures = 1
        a_int = 0
        b_int = 0
    else:
        a_int = a_frac.numerator
        b_int = b_frac.numerator
    no_drop_failures = no_drop_affine_failure_count(
        word=extended_word,
        target_residue=target_residue,
        target_modulus=target_modulus,
        q=refined_q,
        r=refined_r,
    )
    return {
        "high_lift_continuation_supported": int(integrality_failures == 0),
        "high_lift_continuation_step": len(extended_word),
        "high_lift_continuation_word_sum": sum(extended_word),
        "high_lift_continuation_q": refined_q,
        "high_lift_continuation_r": refined_r,
        "high_lift_continuation_a": a_int,
        "high_lift_continuation_b": b_int,
        "high_lift_continuation_integrality_failures": integrality_failures,
        "high_lift_continuation_no_drop_failures": no_drop_failures,
    }


def exact_word_cylinder(word: tuple[int, ...]) -> tuple[int, int, int]:
    """Exact odd-source cylinder for a valuation word.

    Among odd 2-adics, a fixed valuation word with total A is one residue
    class modulo 2^(A+1).  If S_word(n) = (3^s*n + C)/2^A, exactness is

        3^s*n + C == 2^A   mod 2^(A+1).
    """
    power3, constant, total_a = compressed_integer_coefficients(word)
    modulus_bits = total_a + 1
    modulus = 1 << modulus_bits
    residue = ((1 << total_a) - constant) * pow(power3, -1, modulus)
    return residue % modulus, modulus_bits, modulus


def induced_t_word_congruence(
    *,
    word_residue: int,
    word_mod_bits: int,
    target_residue: int,
    target_mod_bits: int,
) -> tuple[bool, int, int]:
    """Solve target_residue + 2^B*t == word_residue mod 2^M."""
    if word_mod_bits <= target_mod_bits:
        word_modulus = 1 << word_mod_bits
        if target_residue % word_modulus != word_residue:
            return False, 0, 0
        return True, 0, 1

    word_modulus = 1 << word_mod_bits
    target_modulus = 1 << target_mod_bits
    diff = (word_residue - target_residue) % word_modulus
    if diff % target_modulus != 0:
        return False, 0, 0
    t_modulus = 1 << (word_mod_bits - target_mod_bits)
    t_residue = (diff // target_modulus) % t_modulus
    return True, t_residue, t_modulus


def return_t_formula(
    word: tuple[int, ...], residue: int, modulus: int
) -> tuple[Fraction, Fraction]:
    alpha, beta = compressed_affine(word)
    slope = alpha
    intercept = (alpha * residue + beta - residue) / modulus
    return slope, intercept


def lcm_denominators(*values: Fraction) -> int:
    out = 1
    for value in values:
        out = math.lcm(out, value.denominator)
    return out


def power_of_two_log(n: int) -> int | None:
    if n <= 0 or n & (n - 1):
        return None
    return n.bit_length() - 1


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def write_json_certificate(
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    stats: dict[str, Any],
    path: Path,
) -> None:
    certificate_rows: list[dict[str, Any]] = []
    for row in rows:
        cert_row = dict(row)
        cert_row["word"] = [
            int(part) for part in str(row["word"]).split(",") if part
        ]
        for key in (
            "step",
            "word_len",
            "word_sum",
            "sample_count",
            "q",
            "r",
            "a",
            "b",
            "dst_v2",
            "dst_odd",
            "dst_h",
            "state_refinement_supported",
            "period_m",
            "slope_num",
            "slope_den",
            "intercept_num",
            "intercept_den",
            "word_mod_bits",
            "word_residue",
            "t_word_mod_bits",
            "t_word_residue",
            "word_congruence_supported",
            "branch_implies_word_congruence",
            "word_congruence_failures",
            "drop_affine_failures",
            "no_drop_certificate",
            "label_prefix_integrality_failures",
            "label_intermediate_visible_failures",
            "label_intermediate_visible_checks",
            "label_intermediate_target_visible_failures",
            "label_intermediate_competing_visible_failures",
            "label_intermediate_target_visible_prefixes",
            "label_intermediate_competing_visible_prefixes",
            *(record_count_field(key) for key in INTERMEDIATE_RECORD_KEYS),
            "label_intermediate_probe_total",
            "label_intermediate_probe_candidate_selected",
            "label_intermediate_probe_target_selected",
            "label_intermediate_probe_competing_selected",
            "label_intermediate_probe_none_selected",
            "label_intermediate_probe_same_step_return",
            "label_intermediate_probe_early_target_return",
            "label_intermediate_probe_no_return_by_final",
            "label_intermediate_probe_terminal_by_final",
            "label_intermediate_multiprobe_total",
            "label_intermediate_multiprobe_same_step_return",
            "label_intermediate_multiprobe_early_target_return",
            "label_intermediate_multiprobe_no_return_by_final",
            "label_intermediate_multiprobe_terminal_by_final",
            "label_intermediate_target_multiprobe_total",
            "label_intermediate_target_multiprobe_same_step_return",
            "label_intermediate_target_multiprobe_early_target_return",
            "label_intermediate_target_multiprobe_no_return_by_final",
            "label_intermediate_target_multiprobe_terminal_by_final",
            *(record_multiprobe_no_return_field(key) for key in INTERMEDIATE_RECORD_KEYS),
            "label_intermediate_multiprobe_no_return_extended_later_target",
            "label_intermediate_multiprobe_no_return_extended_terminal",
            "label_intermediate_multiprobe_no_return_extended_unresolved",
            "label_intermediate_multiprobe_no_return_later_target_min_delta",
            "label_intermediate_multiprobe_no_return_later_target_max_delta",
            "label_intermediate_multiprobe_no_return_continuation_supported",
            "label_intermediate_multiprobe_no_return_continuation_integrality_failures",
            "label_intermediate_multiprobe_no_return_continuation_no_drop_failures",
            "label_intermediate_multiprobe_no_return_actual_prefix_matches",
            "label_intermediate_multiprobe_no_return_suffix_target_word_matches",
            "label_intermediate_multiprobe_no_return_actual_continuation_supported",
            "label_intermediate_multiprobe_no_return_actual_continuation_integrality_failures",
            "label_intermediate_multiprobe_no_return_actual_continuation_no_drop_failures",
            "label_intermediate_multiprobe_no_return_actual_refined_continuation_supported",
            "label_intermediate_multiprobe_no_return_actual_refined_continuation_failures",
            "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_min",
            "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_max",
            "label_intermediate_competing_no_later_target_intersections",
            "label_intermediate_competing_later_target_intersections",
            "label_intermediate_target_persistent_visibility",
            "label_intermediate_target_missing_prior_visibility",
            "label_intermediate_target_no_prior_competing_intersections",
            "label_intermediate_target_prior_competing_intersections",
            "label_intermediate_target_high_lift_covered",
            "label_intermediate_target_low_only_visible",
            "label_intermediate_boundary_density_num",
            "label_intermediate_boundary_density_den",
            "label_intermediate_boundary_min_mod_bits",
            "label_intermediate_target_min_mod_bits",
            "label_intermediate_competing_min_mod_bits",
            "label_final_target_low_failure",
            "label_final_target_high_lift_failures",
            "label_final_target_high_lift_mod_bits",
            "label_final_target_high_lift_residue",
            "label_final_competing_failures",
            "label_final_competing_checks",
            "label_split_resolution_certificate",
            "high_lift_continuation_supported",
            "high_lift_continuation_step",
            "high_lift_continuation_word_sum",
            "high_lift_continuation_q",
            "high_lift_continuation_r",
            "high_lift_continuation_a",
            "high_lift_continuation_b",
            "high_lift_continuation_integrality_failures",
            "high_lift_continuation_no_drop_failures",
            "affine_integrality_certificate",
            "arithmetic_certificate",
            "min_u",
            "max_u",
            "formula_failures",
            "delta_failures",
            "refined_formula_failures",
            "refined_state_failures",
            "exact_on_samples",
        ):
            if cert_row[key] != "":
                cert_row[key] = int(cert_row[key])
        if cert_row["q_log2"] != "":
            cert_row["q_log2"] = int(cert_row["q_log2"])
        if cert_row["period_u"] != "":
            cert_row["period_u"] = int(cert_row["period_u"])
        for key in (
            "state_mod_bits",
            "u_residue_mod",
            "u_residue",
            "refined_q",
            "refined_r",
            "refined_a",
            "refined_b",
        ):
            if cert_row[key] != "":
                cert_row[key] = int(cert_row[key])
        cert_row["label_certificate_status"] = str(cert_row["label_certificate_status"])
        certificate_rows.append(cert_row)

    payload = {
        "schema": "collatz.phase10.A0_return_branch_affine_probe.v1",
        "status": "finite sampled branch extraction; not a theorem",
        "generated_by": Path(__file__).name,
        "parameters": {
            "phases": args.phases,
            "step_cap": args.step_cap,
            "a_cap": args.a_cap,
            "sample_limit": args.sample_limit,
            "sample_mode": args.sample_mode,
            "prefix_bits": args.prefix_bits,
            "min_period_m": args.min_period_m,
            "odd_bits": args.odd_bits,
            "hit_bits": args.hit_bits,
            "v2_cap": args.v2_cap,
            "semantic_replay_step_cap": int(
                getattr(args, "semantic_replay_step_cap", 0) or 0
            ),
        },
        "stats": stats,
        "verification_meaning": (
            "For every sampled row point, next_t = a*u+b with source "
            "t=q*u+r and the recorded delta equals bit_length(a*u+b) "
            "- bit_length(q*u+r).  When state_refinement_supported=1, "
            "the refined fields give a destination-refined source "
            "progression t=refined_q*v+refined_r and "
            "next_t=refined_a*v+refined_b for the sampled points.  The "
            "word_congruence fields are exact 2-adic cylinder arithmetic "
            "for the valuation word.  arithmetic_certificate=1 means the "
            "row's source progression implies the valuation-word cylinder, "
            "has integral affine return coordinates, passes the sampled "
            "formula/delta/destination-state checks, and has an affine "
            "no-drop prefix certificate.  It is not a proof that this row "
            "is the first return in the global shadowing automaton.  The "
            "label_* fields are an exact congruence diagnostic for that "
            "remaining automaton gate.  label_split_resolution_certificate=1 "
            "means the row passes the current finite split diagnostic: no "
            "intermediate low-only target b=1 class, no later target-visible "
            "intersection after an intermediate competing class before the "
            "final step, no final competing label, and an arithmetic "
            "continuation for the final high-lift target class.  This is "
            "still a finite branch-split certificate, not an infinite "
            "Collatz theorem."
        ),
        "branches": certificate_rows,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def analyze(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    op, shadowing, records, target, target_key, residue, modulus, target_modulus_bits = setup()
    target_word = tuple(int(a) for a in target["word"])
    period_m = max(args.min_period_m, args.step_cap * args.a_cap + 1 - target_modulus_bits)
    span = 1 << (args.prefix_bits if args.sample_mode == "dyadic-prefix" else period_m)
    semantic_replay_step_cap = int(getattr(args, "semantic_replay_step_cap", 0) or 0)
    semantic_replay_suffix_certificate = bool(
        getattr(args, "semantic_replay_suffix_certificate", False)
    )
    semantic_replay_certificate_cutoff = int(
        getattr(args, "semantic_replay_certificate_cutoff", 455) or 455
    )
    semantic_replay_word_audit = bool(
        getattr(args, "semantic_replay_word_audit", False)
        or semantic_replay_suffix_certificate
    )

    @lru_cache(maxsize=None)
    def trace_return(t: int, h: int) -> tuple[Any, ...]:
        n0 = op.make_start_from_residue(residue, modulus, t)
        cur = n0
        last_key = target_key
        word: list[int] = []
        for step in range(1, args.step_cap + 1):
            a_val, cur = shadowing.odd_syracuse_step(cur)
            word.append(a_val)
            if a_val > args.a_cap:
                return ("valuation_tail", tuple(word))
            if cur < n0:
                return ("drop", tuple(word))

            key, _best_v = op.best_shadow(cur, records, shadowing)
            if key is None:
                last_key = None
                continue
            if key != last_key:
                if key == target_key:
                    next_t = op.local_t_from_residue(cur, residue, modulus)
                    dst = op.state_of(
                        next_t,
                        h + 1,
                        args.odd_bits,
                        args.hit_bits,
                        args.v2_cap,
                    )
                    delta = next_t.bit_length() - t.bit_length()
                    return ("return", step, tuple(word), dst, delta, next_t)
                last_key = key
        return ("step_tail", tuple(word))

    @lru_cache(maxsize=None)
    def trace_semantic_replay(t: int, h: int) -> tuple[str, int, tuple[int, ...]]:
        """Replay with proof-facing terminal priority.

        The production branch extractor keeps the historical conservative
        order `valuation_tail` before `drop`.  For the descent bridge, a
        point that is already below its source after the current Syracuse
        step should be classified as a direct drop.  This optional replay
        records only finite outcome counters; it does not alter the return
        branch extraction.
        """
        n0 = op.make_start_from_residue(residue, modulus, t)
        cur = n0
        last_key = target_key
        word: list[int] = []
        for step in range(1, semantic_replay_step_cap + 1):
            a_val, cur = shadowing.odd_syracuse_step(cur)
            word.append(a_val)
            if cur < n0:
                return "drop", step, tuple(word)
            if a_val > args.a_cap:
                return "valuation_tail", step, tuple(word)

            key, _best_v = op.best_shadow(cur, records, shadowing)
            if key is None:
                last_key = None
                continue
            if key != last_key:
                if key == target_key:
                    return "return", step, tuple(word)
                last_key = key
        return "step_tail", semantic_replay_step_cap, tuple(word)

    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    total_samples = 0
    return_samples = 0
    kind_counts: dict[str, int] = {}
    semantic_kind_counts: dict[str, int] = {}
    semantic_step_max: dict[str, int] = {}
    semantic_drop_words: set[tuple[int, ...]] = set()
    semantic_drop_phase_words: dict[tuple[str, tuple[int, ...]], int] = {}
    semantic_drop_suffix_thresholds: dict[tuple[int, ...], int] = {}
    semantic_drop_suffix_slope_failures: set[tuple[int, ...]] = set()
    semantic_drop_suffix_samples: dict[tuple[int, ...], int] = {}
    semantic_drop_common_prefix_samples = 0
    for phase in parse_phases(args.phases):
        v2, odd, h = phase
        samples = phase_samples(v2, odd, args.sample_limit, span, args.sample_mode)
        total_samples += len(samples)
        for t in samples:
            if semantic_replay_step_cap > 0:
                semantic_kind, semantic_step, semantic_word = trace_semantic_replay(t, h)
                semantic_kind_counts[semantic_kind] = (
                    semantic_kind_counts.get(semantic_kind, 0) + 1
                )
                semantic_step_max[semantic_kind] = max(
                    semantic_step_max.get(semantic_kind, 0),
                    semantic_step,
                )
                if semantic_replay_word_audit and semantic_kind == "drop":
                    semantic_drop_words.add(semantic_word)
                    phase_word = (fmt_phase(phase), semantic_word)
                    semantic_drop_phase_words[phase_word] = (
                        semantic_drop_phase_words.get(phase_word, 0) + 1
                    )
                    if semantic_word[: len(COMMON_SEMANTIC_DROP_PREFIX)] == (
                        COMMON_SEMANTIC_DROP_PREFIX
                    ):
                        semantic_drop_common_prefix_samples += 1
                        suffix = semantic_word[len(COMMON_SEMANTIC_DROP_PREFIX):]
                        semantic_drop_suffix_samples[suffix] = (
                            semantic_drop_suffix_samples.get(suffix, 0) + 1
                        )
                        slope_ok, min_n = common_prefix_suffix_threshold(suffix)
                        if slope_ok:
                            prior = semantic_drop_suffix_thresholds.get(suffix)
                            if prior is None or min_n > prior:
                                semantic_drop_suffix_thresholds[suffix] = min_n
                        else:
                            semantic_drop_suffix_slope_failures.add(suffix)
            traced = trace_return(t, h)
            kind_counts[str(traced[0])] = kind_counts.get(str(traced[0]), 0) + 1
            if traced[0] != "return":
                continue
            _kind, step, word, dst, delta, next_t = traced
            return_samples += 1
            key = (fmt_phase(phase), step, word, dst)
            groups.setdefault(key, []).append(
                {
                    "t": t,
                    "next_t": int(next_t),
                    "delta": int(delta),
                }
            )

    rows: list[dict[str, Any]] = []
    exact_failures = 0
    noninteger_branches = 0
    for key, items in groups.items():
        phase_text, step, word, dst = key
        slope, intercept = return_t_formula(word, residue, modulus)
        word_residue, word_mod_bits, _word_modulus = exact_word_cylinder(word)
        word_supported, t_word_residue, t_word_modulus = induced_t_word_congruence(
            word_residue=word_residue,
            word_mod_bits=word_mod_bits,
            target_residue=residue,
            target_mod_bits=target_modulus_bits,
        )
        t_word_mod_bits = power_of_two_log(t_word_modulus) if word_supported else None
        q = lcm_denominators(slope, intercept)
        a_frac = slope * q
        if a_frac.denominator != 1:
            noninteger_branches += 1
            continue
        a_int = a_frac.numerator

        by_residue: dict[int, list[dict[str, Any]]] = {}
        for item in items:
            by_residue.setdefault(int(item["t"]) % q, []).append(item)

        for r, branch_items in sorted(by_residue.items()):
            b_frac = slope * r + intercept
            if b_frac.denominator != 1:
                noninteger_branches += 1
                b_int = 0
                exact = False
            else:
                b_int = b_frac.numerator
                exact = True

            formula_failures = 0
            delta_failures = 0
            word_congruence_failures = 0
            refined_formula_failures = 0
            refined_state_failures = 0
            u_values: list[int] = []
            branch_implies_word = (
                word_supported
                and q % t_word_modulus == 0
                and r % t_word_modulus == t_word_residue
            )
            drop_affine_failures = no_drop_affine_failure_count(
                word=word,
                target_residue=residue,
                target_modulus=modulus,
                q=q,
                r=r,
            )
            no_drop_certificate = int(drop_affine_failures == 0)
            label_attempt = label_certificate_attempt(
                op=op,
                shadowing=shadowing,
                word=word,
                target_residue=residue,
                target_modulus=modulus,
                q=q,
                r=r,
                records=records,
                target=target,
                target_key=target_key,
                post_final_step_cap=args.step_cap,
            )
            high_lift_attempt = high_lift_continuation_attempt(
                word=word,
                target_word=target_word,
                target_residue=residue,
                target_modulus=modulus,
                q=q,
                r=r,
                high_lift_residue=int(label_attempt["label_final_target_high_lift_residue"]),
                high_lift_mod_bits=int(label_attempt["label_final_target_high_lift_mod_bits"]),
                has_high_lift=bool(label_attempt["label_final_target_high_lift_failures"]),
            )
            label_split_resolution_certificate = int(
                int(label_attempt["label_prefix_integrality_failures"]) == 0
                and int(label_attempt["label_final_target_low_failure"]) == 0
                and int(label_attempt["label_final_competing_failures"]) == 0
                and int(label_attempt["label_intermediate_target_low_only_visible"]) == 0
                and int(label_attempt["label_intermediate_target_high_lift_covered"])
                    == int(label_attempt["label_intermediate_target_visible_failures"])
                and int(label_attempt["label_intermediate_competing_later_target_intersections"]) == 0
                and int(high_lift_attempt["high_lift_continuation_supported"]) == 1
                and int(high_lift_attempt["high_lift_continuation_integrality_failures"]) == 0
                and int(high_lift_attempt["high_lift_continuation_no_drop_failures"]) == 0
            )
            dst_v2, dst_odd, dst_h = dst
            refinement_supported = dst_v2 < args.v2_cap
            state_mod_bits = dst_v2 + args.odd_bits if refinement_supported else 0
            state_modulus = 1 << state_mod_bits if refinement_supported else 0
            target_residue = dst_odd << dst_v2 if refinement_supported else 0
            if refinement_supported:
                a_inv = pow(a_int, -1, state_modulus)
                u_residue = ((target_residue - b_int) * a_inv) % state_modulus
                refined_q = q * state_modulus
                refined_r = q * u_residue + r
                refined_a = a_int * state_modulus
                refined_b = a_int * u_residue + b_int
            else:
                u_residue = 0
                refined_q = 0
                refined_r = 0
                refined_a = 0
                refined_b = 0
            for item in branch_items:
                t = int(item["t"])
                u = (t - r) // q
                u_values.append(u)
                predicted = a_int * u + b_int
                if predicted != int(item["next_t"]):
                    formula_failures += 1
                source_t = q * u + r
                predicted_delta = predicted.bit_length() - source_t.bit_length()
                if predicted_delta != int(item["delta"]):
                    delta_failures += 1
                if (
                    not word_supported
                    or int(item["t"]) % t_word_modulus != t_word_residue
                ):
                    word_congruence_failures += 1
                if refinement_supported:
                    if u % state_modulus != u_residue:
                        refined_state_failures += 1
                    v = (t - refined_r) // refined_q
                    refined_predicted = refined_a * v + refined_b
                    if t < refined_r or (t - refined_r) % refined_q != 0:
                        refined_formula_failures += 1
                    elif refined_predicted != int(item["next_t"]):
                        refined_formula_failures += 1
            exact = exact and formula_failures == 0 and delta_failures == 0
            affine_integrality_certificate = int(exact and word_supported)
            arithmetic_certificate = int(
                exact
                and word_supported
                and branch_implies_word
                and word_congruence_failures == 0
                and drop_affine_failures == 0
                and refined_formula_failures == 0
                and refined_state_failures == 0
            )
            exact_failures += int(not exact)

            q_log = power_of_two_log(q)
            period_u = ""
            if q_log is not None and q_log <= period_m:
                period_u = str(1 << (period_m - q_log))

            rows.append(
                {
                    "phase": phase_text,
                    "step": step,
                    "dst": fmt_state(dst),
                    "word": ",".join(str(x) for x in word),
                    "word_len": len(word),
                    "word_sum": sum(word),
                    "sample_count": len(branch_items),
                    "q": q,
                    "q_log2": q_log if q_log is not None else "",
                    "r": r,
                    "a": a_int,
                    "b": b_int,
                    "dst_v2": dst_v2,
                    "dst_odd": dst_odd,
                    "dst_h": dst_h,
                    "state_refinement_supported": int(refinement_supported),
                    "state_mod_bits": state_mod_bits if refinement_supported else "",
                    "u_residue_mod": state_modulus if refinement_supported else "",
                    "u_residue": u_residue if refinement_supported else "",
                    "refined_q": refined_q if refinement_supported else "",
                    "refined_r": refined_r if refinement_supported else "",
                    "refined_a": refined_a if refinement_supported else "",
                    "refined_b": refined_b if refinement_supported else "",
                    "period_m": period_m,
                    "period_u": period_u,
                    "slope_num": slope.numerator,
                    "slope_den": slope.denominator,
                    "intercept_num": intercept.numerator,
                    "intercept_den": intercept.denominator,
                    "word_mod_bits": word_mod_bits,
                    "word_residue": word_residue,
                    "t_word_mod_bits": t_word_mod_bits if t_word_mod_bits is not None else "",
                    "t_word_residue": t_word_residue if word_supported else "",
                    "word_congruence_supported": int(word_supported),
                    "branch_implies_word_congruence": int(branch_implies_word),
                    "word_congruence_failures": word_congruence_failures,
                    "drop_affine_failures": drop_affine_failures,
                    "no_drop_certificate": no_drop_certificate,
                    **label_attempt,
                    "label_split_resolution_certificate":
                        label_split_resolution_certificate,
                    **high_lift_attempt,
                    "affine_integrality_certificate": affine_integrality_certificate,
                    "arithmetic_certificate": arithmetic_certificate,
                    "min_u": min(u_values) if u_values else "",
                    "max_u": max(u_values) if u_values else "",
                    "formula_failures": formula_failures,
                    "delta_failures": delta_failures,
                    "refined_formula_failures": refined_formula_failures,
                    "refined_state_failures": refined_state_failures,
                    "exact_on_samples": int(exact),
                }
            )

    rows.sort(
        key=lambda row: (
            -int(row["sample_count"]),
            str(row["phase"]),
            int(row["step"]),
            int(row["q"]),
            int(row["r"]),
        )
    )
    branch_sample_count_total = sum(int(row["sample_count"]) for row in rows)
    stats = {
        "period_m": period_m,
        "sample_span_bits": args.prefix_bits if args.sample_mode == "dyadic-prefix" else period_m,
        "total_samples": total_samples,
        "return_samples": return_samples,
        "drop_samples": kind_counts.get("drop", 0),
        "valuation_tail_samples": kind_counts.get("valuation_tail", 0),
        "step_tail_samples": kind_counts.get("step_tail", 0),
        "return_label_groups": len(groups),
        "branch_rows": len(rows),
        "branch_sample_count_total": branch_sample_count_total,
        "branch_sample_count_coverage_failures": int(
            branch_sample_count_total != return_samples
        ),
        "exact_failures": exact_failures,
        "noninteger_branches": noninteger_branches,
        "word_congruence_failures": sum(int(row["word_congruence_failures"]) for row in rows),
        "drop_affine_failures": sum(int(row["drop_affine_failures"]) for row in rows),
        "no_drop_certificate_rows": sum(int(row["no_drop_certificate"]) for row in rows),
        "label_prefix_integrality_failures": sum(
            int(row["label_prefix_integrality_failures"]) for row in rows
        ),
        "label_intermediate_visible_failures": sum(
            int(row["label_intermediate_visible_failures"]) for row in rows
        ),
        "label_intermediate_target_visible_failures": sum(
            int(row["label_intermediate_target_visible_failures"]) for row in rows
        ),
        "label_intermediate_competing_visible_failures": sum(
            int(row["label_intermediate_competing_visible_failures"]) for row in rows
        ),
        "label_intermediate_target_visible_prefixes": sum(
            int(row["label_intermediate_target_visible_prefixes"]) for row in rows
        ),
        "label_intermediate_competing_visible_prefixes": sum(
            int(row["label_intermediate_competing_visible_prefixes"]) for row in rows
        ),
        **{
            record_count_field(key): sum(
                int(row[record_count_field(key)]) for row in rows
            )
            for key in INTERMEDIATE_RECORD_KEYS
        },
        "label_intermediate_probe_total": sum(
            int(row["label_intermediate_probe_total"]) for row in rows
        ),
        "label_intermediate_probe_candidate_selected": sum(
            int(row["label_intermediate_probe_candidate_selected"]) for row in rows
        ),
        "label_intermediate_probe_target_selected": sum(
            int(row["label_intermediate_probe_target_selected"]) for row in rows
        ),
        "label_intermediate_probe_competing_selected": sum(
            int(row["label_intermediate_probe_competing_selected"]) for row in rows
        ),
        "label_intermediate_probe_none_selected": sum(
            int(row["label_intermediate_probe_none_selected"]) for row in rows
        ),
        "label_intermediate_probe_same_step_return": sum(
            int(row["label_intermediate_probe_same_step_return"]) for row in rows
        ),
        "label_intermediate_probe_early_target_return": sum(
            int(row["label_intermediate_probe_early_target_return"]) for row in rows
        ),
        "label_intermediate_probe_no_return_by_final": sum(
            int(row["label_intermediate_probe_no_return_by_final"]) for row in rows
        ),
        "label_intermediate_probe_terminal_by_final": sum(
            int(row["label_intermediate_probe_terminal_by_final"]) for row in rows
        ),
        "label_intermediate_multiprobe_total": sum(
            int(row["label_intermediate_multiprobe_total"]) for row in rows
        ),
        "label_intermediate_multiprobe_same_step_return": sum(
            int(row["label_intermediate_multiprobe_same_step_return"]) for row in rows
        ),
        "label_intermediate_multiprobe_early_target_return": sum(
            int(row["label_intermediate_multiprobe_early_target_return"]) for row in rows
        ),
        "label_intermediate_multiprobe_no_return_by_final": sum(
            int(row["label_intermediate_multiprobe_no_return_by_final"]) for row in rows
        ),
        "label_intermediate_multiprobe_terminal_by_final": sum(
            int(row["label_intermediate_multiprobe_terminal_by_final"]) for row in rows
        ),
        "label_intermediate_target_multiprobe_total": sum(
            int(row["label_intermediate_target_multiprobe_total"]) for row in rows
        ),
        "label_intermediate_target_multiprobe_same_step_return": sum(
            int(row["label_intermediate_target_multiprobe_same_step_return"])
            for row in rows
        ),
        "label_intermediate_target_multiprobe_early_target_return": sum(
            int(row["label_intermediate_target_multiprobe_early_target_return"])
            for row in rows
        ),
        "label_intermediate_target_multiprobe_no_return_by_final": sum(
            int(row["label_intermediate_target_multiprobe_no_return_by_final"])
            for row in rows
        ),
        "label_intermediate_target_multiprobe_terminal_by_final": sum(
            int(row["label_intermediate_target_multiprobe_terminal_by_final"])
            for row in rows
        ),
        **{
            record_multiprobe_no_return_field(key): sum(
                int(row[record_multiprobe_no_return_field(key)]) for row in rows
            )
            for key in INTERMEDIATE_RECORD_KEYS
        },
        "label_intermediate_multiprobe_no_return_extended_later_target": sum(
            int(row["label_intermediate_multiprobe_no_return_extended_later_target"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_extended_terminal": sum(
            int(row["label_intermediate_multiprobe_no_return_extended_terminal"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_extended_unresolved": sum(
            int(row["label_intermediate_multiprobe_no_return_extended_unresolved"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_later_target_min_delta": min(
            (
                int(row["label_intermediate_multiprobe_no_return_later_target_min_delta"])
                for row in rows
                if int(row["label_intermediate_multiprobe_no_return_extended_later_target"]) > 0
            ),
            default=0,
        ),
        "label_intermediate_multiprobe_no_return_later_target_max_delta": max(
            (
                int(row["label_intermediate_multiprobe_no_return_later_target_max_delta"])
                for row in rows
                if int(row["label_intermediate_multiprobe_no_return_extended_later_target"]) > 0
            ),
            default=0,
        ),
        "label_intermediate_multiprobe_no_return_continuation_supported": sum(
            int(row["label_intermediate_multiprobe_no_return_continuation_supported"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_continuation_integrality_failures": sum(
            int(row["label_intermediate_multiprobe_no_return_continuation_integrality_failures"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_continuation_no_drop_failures": sum(
            int(row["label_intermediate_multiprobe_no_return_continuation_no_drop_failures"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_prefix_matches": sum(
            int(row["label_intermediate_multiprobe_no_return_actual_prefix_matches"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_suffix_target_word_matches": sum(
            int(row["label_intermediate_multiprobe_no_return_suffix_target_word_matches"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_continuation_supported": sum(
            int(row["label_intermediate_multiprobe_no_return_actual_continuation_supported"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_continuation_integrality_failures": sum(
            int(row["label_intermediate_multiprobe_no_return_actual_continuation_integrality_failures"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_continuation_no_drop_failures": sum(
            int(row["label_intermediate_multiprobe_no_return_actual_continuation_no_drop_failures"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_refined_continuation_supported": sum(
            int(row["label_intermediate_multiprobe_no_return_actual_refined_continuation_supported"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_refined_continuation_failures": sum(
            int(row["label_intermediate_multiprobe_no_return_actual_refined_continuation_failures"])
            for row in rows
        ),
        "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_min": min(
            (
                int(row["label_intermediate_multiprobe_no_return_actual_refined_extra_bits_min"])
                for row in rows
                if int(row["label_intermediate_multiprobe_no_return_actual_refined_continuation_supported"]) > 0
            ),
            default=0,
        ),
        "label_intermediate_multiprobe_no_return_actual_refined_extra_bits_max": max(
            (
                int(row["label_intermediate_multiprobe_no_return_actual_refined_extra_bits_max"])
                for row in rows
                if int(row["label_intermediate_multiprobe_no_return_actual_refined_continuation_supported"]) > 0
            ),
            default=0,
        ),
        "label_intermediate_competing_no_later_target_intersections": sum(
            int(row["label_intermediate_competing_no_later_target_intersections"])
            for row in rows
        ),
        "label_intermediate_competing_later_target_intersections": sum(
            int(row["label_intermediate_competing_later_target_intersections"])
            for row in rows
        ),
        "label_intermediate_target_persistent_visibility": sum(
            int(row["label_intermediate_target_persistent_visibility"]) for row in rows
        ),
        "label_intermediate_target_missing_prior_visibility": sum(
            int(row["label_intermediate_target_missing_prior_visibility"]) for row in rows
        ),
        "label_intermediate_target_no_prior_competing_intersections": sum(
            int(row["label_intermediate_target_no_prior_competing_intersections"])
            for row in rows
        ),
        "label_intermediate_target_prior_competing_intersections": sum(
            int(row["label_intermediate_target_prior_competing_intersections"])
            for row in rows
        ),
        "label_intermediate_target_high_lift_covered": sum(
            int(row["label_intermediate_target_high_lift_covered"]) for row in rows
        ),
        "label_intermediate_target_low_only_visible": sum(
            int(row["label_intermediate_target_low_only_visible"]) for row in rows
        ),
        "label_intermediate_boundary_density_num_sum": sum(
            Fraction(
                int(row["label_intermediate_boundary_density_num"]),
                int(row["label_intermediate_boundary_density_den"]),
            )
            for row in rows
        ).numerator,
        "label_intermediate_boundary_density_den_sum": sum(
            Fraction(
                int(row["label_intermediate_boundary_density_num"]),
                int(row["label_intermediate_boundary_density_den"]),
            )
            for row in rows
        ).denominator,
        "label_intermediate_boundary_min_mod_bits": min(
            (
                int(row["label_intermediate_boundary_min_mod_bits"])
                for row in rows
                if int(row["label_intermediate_visible_failures"]) > 0
            ),
            default=0,
        ),
        "label_intermediate_target_min_mod_bits": min(
            (
                int(row["label_intermediate_target_min_mod_bits"])
                for row in rows
                if int(row["label_intermediate_target_visible_failures"]) > 0
            ),
            default=0,
        ),
        "label_intermediate_competing_min_mod_bits": min(
            (
                int(row["label_intermediate_competing_min_mod_bits"])
                for row in rows
                if int(row["label_intermediate_competing_visible_failures"]) > 0
            ),
            default=0,
        ),
        "label_final_target_low_failures": sum(
            int(row["label_final_target_low_failure"]) for row in rows
        ),
        "label_final_target_high_lift_failures": sum(
            int(row["label_final_target_high_lift_failures"]) for row in rows
        ),
        "label_final_target_high_lift_min_mod_bits": min(
            (
                int(row["label_final_target_high_lift_mod_bits"])
                for row in rows
                if int(row["label_final_target_high_lift_failures"]) > 0
            ),
            default=0,
        ),
        "label_final_target_high_lift_max_mod_bits": max(
            (
                int(row["label_final_target_high_lift_mod_bits"])
                for row in rows
                if int(row["label_final_target_high_lift_failures"]) > 0
            ),
            default=0,
        ),
        "label_final_competing_failures": sum(
            int(row["label_final_competing_failures"]) for row in rows
        ),
        "label_split_resolution_certificate_rows": sum(
            int(row["label_split_resolution_certificate"]) for row in rows
        ),
        "high_lift_continuation_supported_rows": sum(
            int(row["high_lift_continuation_supported"]) for row in rows
        ),
        "high_lift_continuation_integrality_failures": sum(
            int(row["high_lift_continuation_integrality_failures"]) for row in rows
        ),
        "high_lift_continuation_no_drop_failures": sum(
            int(row["high_lift_continuation_no_drop_failures"]) for row in rows
        ),
        "high_lift_continuation_step_delta_min": min(
            (
                int(row["high_lift_continuation_step"]) - int(row["step"])
                for row in rows
                if int(row["high_lift_continuation_supported"]) > 0
            ),
            default=0,
        ),
        "high_lift_continuation_step_delta_max": max(
            (
                int(row["high_lift_continuation_step"]) - int(row["step"])
                for row in rows
                if int(row["high_lift_continuation_supported"]) > 0
            ),
            default=0,
        ),
        "label_status_proved_constant_target_b1": sum(
            1 for row in rows if row["label_certificate_status"] == "proved_constant_target_b1"
        ),
        "label_status_target_high_lift_boundary": sum(
            1 for row in rows if row["label_certificate_status"] == "target_high_lift_boundary"
        ),
        "label_status_blocked_label_congruence": sum(
            1 for row in rows if row["label_certificate_status"] == "blocked_label_congruence"
        ),
        "label_status_blocked_prefix_integrality": sum(
            1 for row in rows if row["label_certificate_status"] == "blocked_prefix_integrality"
        ),
        "branch_word_certificate_failures": sum(
            1 - int(row["branch_implies_word_congruence"]) for row in rows
        ),
        "arithmetic_certificate_rows": sum(int(row["arithmetic_certificate"]) for row in rows),
        "refined_formula_failures": sum(int(row["refined_formula_failures"]) for row in rows),
        "refined_state_failures": sum(int(row["refined_state_failures"]) for row in rows),
    }
    if semantic_replay_step_cap > 0:
        semantic_drop_samples = semantic_kind_counts.get("drop", 0)
        semantic_return_samples = semantic_kind_counts.get("return", 0)
        semantic_valuation_tail_samples = semantic_kind_counts.get("valuation_tail", 0)
        semantic_step_tail_samples = semantic_kind_counts.get("step_tail", 0)
        semantic_loss_samples = (
            semantic_valuation_tail_samples + semantic_step_tail_samples
        )
        stats.update(
            {
                "semantic_replay_enabled": 1,
                "semantic_replay_step_cap": semantic_replay_step_cap,
                "semantic_replay_total_samples": total_samples,
                "semantic_replay_drop_samples": semantic_drop_samples,
                "semantic_replay_return_samples": semantic_return_samples,
                "semantic_replay_valuation_tail_samples": semantic_valuation_tail_samples,
                "semantic_replay_step_tail_samples": semantic_step_tail_samples,
                "semantic_replay_loss_samples": semantic_loss_samples,
                "semantic_replay_loss_free": int(semantic_loss_samples == 0),
                "semantic_replay_drop_step_max": semantic_step_max.get("drop", 0),
                "semantic_replay_return_step_max": semantic_step_max.get("return", 0),
                "semantic_replay_valuation_tail_step_max": semantic_step_max.get(
                    "valuation_tail", 0
                ),
                "semantic_replay_step_tail_step_max": semantic_step_max.get(
                    "step_tail", 0
                ),
            }
        )
        if semantic_replay_word_audit:
            semantic_drop_phase_word_singletons = sum(
                1 for count in semantic_drop_phase_words.values() if count == 1
            )
            semantic_drop_suffix_phase_groups: dict[tuple[int, ...], int] = {}
            semantic_drop_suffix_phase_singletons: dict[tuple[int, ...], int] = {}
            for (_phase_text, word), count in semantic_drop_phase_words.items():
                if word[: len(COMMON_SEMANTIC_DROP_PREFIX)] != (
                    COMMON_SEMANTIC_DROP_PREFIX
                ):
                    continue
                suffix = word[len(COMMON_SEMANTIC_DROP_PREFIX):]
                semantic_drop_suffix_phase_groups[suffix] = (
                    semantic_drop_suffix_phase_groups.get(suffix, 0) + 1
                )
                if count == 1:
                    semantic_drop_suffix_phase_singletons[suffix] = (
                        semantic_drop_suffix_phase_singletons.get(suffix, 0) + 1
                    )
            suffix_certificate_rows: list[dict[str, Any]] = []
            all_suffixes = (
                set(semantic_drop_suffix_thresholds)
                | semantic_drop_suffix_slope_failures
                | set(semantic_drop_suffix_samples)
            )
            for suffix in sorted(all_suffixes, key=lambda s: (len(s), sum(s), s)):
                power3, const, total_a = compressed_integer_coefficients(suffix)
                slope_gap = 128 * (1 << total_a) - 729 * power3
                slope_ok, min_n = common_prefix_suffix_threshold(suffix)
                suffix_certificate_rows.append(
                    {
                        "suffix": list(suffix),
                        "suffix_len": len(suffix),
                        "suffix_sum": total_a,
                        "suffix_const": const,
                        "slope_gap": slope_gap,
                        "threshold_min_n": min_n,
                        "slope_ok": int(slope_ok),
                        "threshold_le_455": int(slope_ok and min_n <= 455),
                        "threshold_le_cutoff": int(
                            slope_ok and min_n <= semantic_replay_certificate_cutoff
                        ),
                        "sample_count": semantic_drop_suffix_samples.get(suffix, 0),
                        "phase_word_group_count":
                            semantic_drop_suffix_phase_groups.get(suffix, 0),
                        "phase_word_singleton_group_count":
                            semantic_drop_suffix_phase_singletons.get(suffix, 0),
                    }
                )
            suffix_pair_rows_by_key: dict[tuple[int, int], dict[str, Any]] = {}
            for row in suffix_certificate_rows:
                key = (int(row["suffix_len"]), int(row["suffix_sum"]))
                pair = suffix_pair_rows_by_key.get(key)
                if pair is None:
                    pair = {
                        "suffix_len": key[0],
                        "suffix_sum": key[1],
                        "row_count": 0,
                        "sample_count": 0,
                        "phase_word_group_count": 0,
                        "phase_word_singleton_group_count": 0,
                        "slope_gap": int(row["slope_gap"]),
                        "suffix_const_max": int(row["suffix_const"]),
                        "threshold_min_n_max": int(row["threshold_min_n"]),
                        "slope_ok": int(row["slope_ok"]),
                        "threshold_le_455": int(row["threshold_le_455"]),
                        "threshold_le_cutoff": int(row["threshold_le_cutoff"]),
                    }
                    suffix_pair_rows_by_key[key] = pair
                pair["row_count"] = int(pair["row_count"]) + 1
                pair["sample_count"] = (
                    int(pair["sample_count"]) + int(row["sample_count"])
                )
                pair["phase_word_group_count"] = (
                    int(pair["phase_word_group_count"])
                    + int(row["phase_word_group_count"])
                )
                pair["phase_word_singleton_group_count"] = (
                    int(pair["phase_word_singleton_group_count"])
                    + int(row["phase_word_singleton_group_count"])
                )
                pair["suffix_const_max"] = max(
                    int(pair["suffix_const_max"]), int(row["suffix_const"])
                )
                pair["threshold_min_n_max"] = max(
                    int(pair["threshold_min_n_max"]), int(row["threshold_min_n"])
                )
                pair["slope_ok"] = min(int(pair["slope_ok"]), int(row["slope_ok"]))
                pair["threshold_le_455"] = min(
                    int(pair["threshold_le_455"]),
                    int(row["threshold_le_455"]),
                )
                pair["threshold_le_cutoff"] = min(
                    int(pair["threshold_le_cutoff"]),
                    int(row["threshold_le_cutoff"]),
                )
            suffix_pair_rows = sorted(
                suffix_pair_rows_by_key.values(),
                key=lambda row: (int(row["suffix_len"]), int(row["suffix_sum"])),
            )
            for row in suffix_pair_rows:
                suffix_len = int(row["suffix_len"])
                suffix_sum = int(row["suffix_sum"])
                slope_gap = int(row["slope_gap"])
                threshold_max = int(row["threshold_min_n_max"])
                suffix_const_max = int(row["suffix_const_max"])
                expected_gap = 128 * (1 << suffix_sum) - 729 * (3 ** suffix_len)
                valid_at_455 = (
                    suffix_len > 0
                    and 729 * (3 ** suffix_len) <= 128 * (1 << suffix_sum)
                    and slope_gap == expected_gap
                    and 817 * (3 ** suffix_len) + 128 * suffix_const_max
                    < slope_gap * threshold_max
                    and threshold_max <= 455
                )
                valid_at_cutoff = (
                    suffix_len > 0
                    and 729 * (3 ** suffix_len) <= 128 * (1 << suffix_sum)
                    and slope_gap == expected_gap
                    and 817 * (3 ** suffix_len) + 128 * suffix_const_max
                    < slope_gap * threshold_max
                    and threshold_max <= semantic_replay_certificate_cutoff
                )
                row["valid_at_455"] = int(valid_at_455)
                row["valid_at_cutoff"] = int(valid_at_cutoff)
            suffix_certificate_failures = sum(
                1
                for row in suffix_certificate_rows
                if not int(row["slope_ok"]) or not int(row["threshold_le_cutoff"])
            )
            suffix_pair_certificate_failures = sum(
                1
                for row in suffix_pair_rows
                if not int(row["valid_at_cutoff"])
            )
            suffix_pair_coverage_missing_failures = 0
            suffix_pair_coverage_const_bound_failures = 0
            suffix_pair_coverage_threshold_bound_failures = 0
            suffix_pair_coverage_covered_suffix_rows = 0
            suffix_pair_coverage_covered_samples = 0
            suffix_pair_coverage_covered_phase_word_groups = 0
            for row in suffix_certificate_rows:
                key = (int(row["suffix_len"]), int(row["suffix_sum"]))
                pair = suffix_pair_rows_by_key.get(key)
                if pair is None:
                    suffix_pair_coverage_missing_failures += 1
                    continue
                const_ok = int(row["suffix_const"]) <= int(pair["suffix_const_max"])
                threshold_ok = int(row["threshold_min_n"]) <= int(
                    pair["threshold_min_n_max"]
                )
                valid_pair = bool(int(pair.get("valid_at_cutoff", 0)))
                if not const_ok:
                    suffix_pair_coverage_const_bound_failures += 1
                if not threshold_ok or not valid_pair:
                    suffix_pair_coverage_threshold_bound_failures += 1
                if const_ok and threshold_ok and valid_pair:
                    suffix_pair_coverage_covered_suffix_rows += 1
                    suffix_pair_coverage_covered_samples += int(row["sample_count"])
                    suffix_pair_coverage_covered_phase_word_groups += int(
                        row["phase_word_group_count"]
                    )
            suffix_pair_coverage_uncovered_suffix_rows = (
                len(suffix_certificate_rows)
                - suffix_pair_coverage_covered_suffix_rows
            )
            source_pair_coverage_covered_samples = (
                suffix_pair_coverage_covered_samples
            )
            source_pair_coverage_uncovered_samples = (
                semantic_drop_samples - source_pair_coverage_covered_samples
            )
            source_pair_coverage_failure_total = (
                source_pair_coverage_uncovered_samples
                + suffix_pair_coverage_missing_failures
                + suffix_pair_coverage_const_bound_failures
                + suffix_pair_coverage_threshold_bound_failures
                + (semantic_drop_samples - semantic_drop_common_prefix_samples)
            )
            stats.update(
                {
                    "semantic_replay_word_audit_enabled": 1,
                    "semantic_replay_drop_distinct_words": len(semantic_drop_words),
                    "semantic_replay_drop_phase_word_groups": len(
                        semantic_drop_phase_words
                    ),
                    "semantic_replay_drop_phase_word_singleton_groups":
                        semantic_drop_phase_word_singletons,
                    "semantic_replay_drop_distinct_suffixes": len(
                        semantic_drop_suffix_thresholds
                    ) + len(semantic_drop_suffix_slope_failures),
                    "semantic_replay_drop_suffix_slope_failure_words": len(
                        semantic_drop_suffix_slope_failures
                    ),
                    "semantic_replay_drop_suffix_threshold_max": (
                        max(semantic_drop_suffix_thresholds.values())
                        if semantic_drop_suffix_thresholds else 0
                    ),
                    "semantic_replay_drop_common_prefix_len": len(
                        COMMON_SEMANTIC_DROP_PREFIX
                    ),
                    "semantic_replay_drop_common_prefix_samples":
                        semantic_drop_common_prefix_samples,
                    "semantic_replay_drop_common_prefix_failures":
                        semantic_drop_samples
                        - semantic_drop_common_prefix_samples,
                }
            )
            if semantic_replay_suffix_certificate:
                stats.update(
                    {
                        "semantic_replay_suffix_certificate_enabled": 1,
                        "semantic_replay_suffix_certificate_cutoff":
                            semantic_replay_certificate_cutoff,
                        "semantic_replay_suffix_certificate_row_count": len(
                            suffix_certificate_rows
                        ),
                        "semantic_replay_suffix_certificate_failures":
                            suffix_certificate_failures,
                        "semantic_replay_suffix_certificate_threshold_max": max(
                            (
                                int(row["threshold_min_n"])
                                for row in suffix_certificate_rows
                                if int(row["slope_ok"])
                            ),
                            default=0,
                        ),
                        "semantic_replay_suffix_certificate_rows":
                            suffix_certificate_rows,
                        "semantic_replay_suffix_pair_certificate_row_count": len(
                            suffix_pair_rows
                        ),
                        "semantic_replay_suffix_pair_certificate_cutoff":
                            semantic_replay_certificate_cutoff,
                        "semantic_replay_suffix_pair_certificate_failures":
                            suffix_pair_certificate_failures,
                        "semantic_replay_suffix_pair_certificate_threshold_max": max(
                            (
                                int(row["threshold_min_n_max"])
                                for row in suffix_pair_rows
                                if int(row["slope_ok"])
                            ),
                            default=0,
                        ),
                        "semantic_replay_suffix_pair_certificate_rows":
                            suffix_pair_rows,
                        "semantic_replay_suffix_pair_coverage_suffix_rows": len(
                            suffix_certificate_rows
                        ),
                        "semantic_replay_suffix_pair_coverage_covered_suffix_rows":
                            suffix_pair_coverage_covered_suffix_rows,
                        "semantic_replay_suffix_pair_coverage_uncovered_suffix_rows":
                            suffix_pair_coverage_uncovered_suffix_rows,
                        "semantic_replay_suffix_pair_coverage_covered_drop_samples":
                            suffix_pair_coverage_covered_samples,
                        "semantic_replay_suffix_pair_coverage_covered_phase_word_groups":
                            suffix_pair_coverage_covered_phase_word_groups,
                        "semantic_replay_suffix_pair_coverage_missing_pair_failures":
                            suffix_pair_coverage_missing_failures,
                        "semantic_replay_suffix_pair_coverage_const_bound_failures":
                            suffix_pair_coverage_const_bound_failures,
                        "semantic_replay_suffix_pair_coverage_threshold_bound_failures":
                            suffix_pair_coverage_threshold_bound_failures,
                        "semantic_replay_suffix_pair_coverage_loss_free": int(
                            suffix_pair_coverage_uncovered_suffix_rows == 0
                            and suffix_pair_coverage_missing_failures == 0
                            and suffix_pair_coverage_const_bound_failures == 0
                            and suffix_pair_coverage_threshold_bound_failures == 0
                        ),
                        "semantic_replay_source_pair_coverage_drop_samples":
                            semantic_drop_samples,
                        "semantic_replay_source_pair_coverage_covered_samples":
                            source_pair_coverage_covered_samples,
                        "semantic_replay_source_pair_coverage_uncovered_samples":
                            source_pair_coverage_uncovered_samples,
                        "semantic_replay_source_pair_coverage_common_prefix_failures":
                            semantic_drop_samples
                            - semantic_drop_common_prefix_samples,
                        "semantic_replay_source_pair_coverage_failure_total":
                            source_pair_coverage_failure_total,
                        "semantic_replay_source_pair_coverage_loss_free": int(
                            source_pair_coverage_failure_total == 0
                        ),
                    }
                )
    return rows, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phases", default="0|3|0,1|3|0,3|1|0,7|3|0")
    parser.add_argument("--step-cap", type=int, default=75)
    parser.add_argument("--a-cap", type=int, default=10)
    parser.add_argument("--sample-limit", type=int, default=256)
    parser.add_argument("--sample-mode", default="spread", choices=["prefix", "spread", "dyadic-prefix"])
    parser.add_argument(
        "--prefix-bits",
        type=int,
        default=12,
        help="dyadic prefix size for --sample-mode dyadic-prefix; enumerates t < 2^prefix_bits",
    )
    parser.add_argument("--min-period-m", type=int, default=32)
    parser.add_argument("--odd-bits", type=int, default=2)
    parser.add_argument("--hit-bits", type=int, default=2)
    parser.add_argument("--v2-cap", type=int, default=13)
    parser.add_argument(
        "--semantic-replay-step-cap",
        type=int,
        default=0,
        help=(
            "optional finite replay cap using proof-facing terminal priority: "
            "drop is checked before valuation_tail; 0 disables the replay"
        ),
    )
    parser.add_argument(
        "--semantic-replay-word-audit",
        action="store_true",
        help=(
            "when semantic replay is enabled, count distinct drop words and "
            "phase-word groups; this is an audit only and does not alter rows"
        ),
    )
    parser.add_argument(
        "--semantic-replay-suffix-certificate",
        action="store_true",
        help=(
            "when semantic replay is enabled, include exact suffix certificate "
            "rows after the common drop prefix in the JSON stats payload"
        ),
    )
    parser.add_argument(
        "--semantic-replay-certificate-cutoff",
        type=int,
        default=455,
        help=(
            "finite small-case cutoff used when checking semantic suffix/pair "
            "certificates; default 455 matches the original T14 audit"
        ),
    )
    parser.add_argument("--output-tag", default="current_A0")
    parser.add_argument("--no-write", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, stats = analyze(args)
    csv_path, json_path = output_paths(args.output_tag)
    if not args.no_write:
        write_csv(rows, csv_path)
        write_json_certificate(args=args, rows=rows, stats=stats, path=json_path)
    print("A0 return branch affine probe")
    print(f"period_m={stats['period_m']}")
    print(f"sample_span_bits={stats['sample_span_bits']}")
    print(f"total_samples={stats['total_samples']}")
    print(f"return_samples={stats['return_samples']}")
    print(f"drop_samples={stats['drop_samples']}")
    print(f"valuation_tail_samples={stats['valuation_tail_samples']}")
    print(f"step_tail_samples={stats['step_tail_samples']}")
    print(f"return_label_groups={stats['return_label_groups']}")
    print(f"branch_rows={stats['branch_rows']}")
    print(f"branch_sample_count_total={stats['branch_sample_count_total']}")
    print(
        "branch_sample_count_coverage_failures="
        f"{stats['branch_sample_count_coverage_failures']}"
    )
    print(f"exact_failures={stats['exact_failures']}")
    print(f"noninteger_branches={stats['noninteger_branches']}")
    print(f"word_congruence_failures={stats['word_congruence_failures']}")
    print(f"drop_affine_failures={stats['drop_affine_failures']}")
    print(f"no_drop_certificate_rows={stats['no_drop_certificate_rows']}")
    print(f"label_prefix_integrality_failures={stats['label_prefix_integrality_failures']}")
    print(f"label_intermediate_visible_failures={stats['label_intermediate_visible_failures']}")
    print(
        "label_intermediate_visible_split="
        f"target:{stats['label_intermediate_target_visible_failures']},"
        f"competing:{stats['label_intermediate_competing_visible_failures']}"
    )
    print(
        "label_intermediate_visible_prefix_split="
        f"target:{stats['label_intermediate_target_visible_prefixes']},"
        f"competing:{stats['label_intermediate_competing_visible_prefixes']}"
    )
    print(
        "label_intermediate_visible_by_record="
        + ",".join(
            f"k{key[0]}c{key[1]}:{stats[record_count_field(key)]}"
            for key in INTERMEDIATE_RECORD_KEYS
        )
    )
    print(
        "label_intermediate_probe_selected="
        f"candidate:{stats['label_intermediate_probe_candidate_selected']},"
        f"target:{stats['label_intermediate_probe_target_selected']},"
        f"competing:{stats['label_intermediate_probe_competing_selected']},"
        f"none:{stats['label_intermediate_probe_none_selected']}"
    )
    print(
        "label_intermediate_probe_outcome="
        f"same_step:{stats['label_intermediate_probe_same_step_return']},"
        f"early_target:{stats['label_intermediate_probe_early_target_return']},"
        f"no_return_by_final:{stats['label_intermediate_probe_no_return_by_final']},"
        f"terminal_by_final:{stats['label_intermediate_probe_terminal_by_final']}"
    )
    print(
        "label_intermediate_multiprobe_outcome="
        f"total:{stats['label_intermediate_multiprobe_total']},"
        f"same_step:{stats['label_intermediate_multiprobe_same_step_return']},"
        f"early_target:{stats['label_intermediate_multiprobe_early_target_return']},"
        f"no_return_by_final:{stats['label_intermediate_multiprobe_no_return_by_final']},"
        f"terminal_by_final:{stats['label_intermediate_multiprobe_terminal_by_final']}"
    )
    print(
        "label_intermediate_target_multiprobe_outcome="
        f"total:{stats['label_intermediate_target_multiprobe_total']},"
        f"same_step:{stats['label_intermediate_target_multiprobe_same_step_return']},"
        f"early_target:{stats['label_intermediate_target_multiprobe_early_target_return']},"
        f"no_return_by_final:{stats['label_intermediate_target_multiprobe_no_return_by_final']},"
        f"terminal_by_final:{stats['label_intermediate_target_multiprobe_terminal_by_final']}"
    )
    print(
        "label_intermediate_multiprobe_no_return_by_record="
        + ",".join(
            f"k{key[0]}c{key[1]}:{stats[record_multiprobe_no_return_field(key)]}"
            for key in INTERMEDIATE_RECORD_KEYS
        )
    )
    print(
        "label_intermediate_multiprobe_no_return_extended="
        f"later_target:{stats['label_intermediate_multiprobe_no_return_extended_later_target']},"
        f"terminal:{stats['label_intermediate_multiprobe_no_return_extended_terminal']},"
        f"unresolved:{stats['label_intermediate_multiprobe_no_return_extended_unresolved']},"
        "later_delta_range:"
        f"{stats['label_intermediate_multiprobe_no_return_later_target_min_delta']}.."
        f"{stats['label_intermediate_multiprobe_no_return_later_target_max_delta']}"
    )
    print(
        "label_intermediate_multiprobe_no_return_continuation="
        f"supported:{stats['label_intermediate_multiprobe_no_return_continuation_supported']},"
        "failures:"
        f"integrality:{stats['label_intermediate_multiprobe_no_return_continuation_integrality_failures']},"
        f"no_drop:{stats['label_intermediate_multiprobe_no_return_continuation_no_drop_failures']}"
    )
    print(
        "label_intermediate_multiprobe_no_return_actual_continuation="
        f"prefix_match:{stats['label_intermediate_multiprobe_no_return_actual_prefix_matches']},"
        f"suffix_target_word:{stats['label_intermediate_multiprobe_no_return_suffix_target_word_matches']},"
        f"supported:{stats['label_intermediate_multiprobe_no_return_actual_continuation_supported']},"
        "failures:"
        f"integrality:{stats['label_intermediate_multiprobe_no_return_actual_continuation_integrality_failures']},"
        f"no_drop:{stats['label_intermediate_multiprobe_no_return_actual_continuation_no_drop_failures']}"
    )
    print(
        "label_intermediate_multiprobe_no_return_actual_refined_continuation="
        f"supported:{stats['label_intermediate_multiprobe_no_return_actual_refined_continuation_supported']},"
        f"failures:{stats['label_intermediate_multiprobe_no_return_actual_refined_continuation_failures']},"
        "extra_bits_range:"
        f"{stats['label_intermediate_multiprobe_no_return_actual_refined_extra_bits_min']}.."
        f"{stats['label_intermediate_multiprobe_no_return_actual_refined_extra_bits_max']}"
    )
    print(
        "label_intermediate_competing_later_target_intersections="
        f"none:{stats['label_intermediate_competing_no_later_target_intersections']},"
        f"some:{stats['label_intermediate_competing_later_target_intersections']}"
    )
    print(
        "label_intermediate_target_persistence="
        f"persistent:{stats['label_intermediate_target_persistent_visibility']},"
        f"missing_prior:{stats['label_intermediate_target_missing_prior_visibility']},"
        f"no_prior_competing:{stats['label_intermediate_target_no_prior_competing_intersections']},"
        f"prior_competing:{stats['label_intermediate_target_prior_competing_intersections']}"
    )
    print(
        "label_intermediate_target_lift_cover="
        f"high_lift_covered:{stats['label_intermediate_target_high_lift_covered']},"
        f"low_only:{stats['label_intermediate_target_low_only_visible']}"
    )
    print(
        "label_intermediate_boundary_density_sum="
        f"{stats['label_intermediate_boundary_density_num_sum']}/"
        f"{stats['label_intermediate_boundary_density_den_sum']}"
    )
    print(f"label_intermediate_boundary_min_mod_bits={stats['label_intermediate_boundary_min_mod_bits']}")
    print(
        "label_intermediate_split_min_mod_bits="
        f"target:{stats['label_intermediate_target_min_mod_bits']},"
        f"competing:{stats['label_intermediate_competing_min_mod_bits']}"
    )
    print(f"label_final_target_low_failures={stats['label_final_target_low_failures']}")
    print(f"label_final_target_high_lift_failures={stats['label_final_target_high_lift_failures']}")
    print(
        "label_final_target_high_lift_mod_bits_range="
        f"{stats['label_final_target_high_lift_min_mod_bits']}.."
        f"{stats['label_final_target_high_lift_max_mod_bits']}"
    )
    print(f"label_final_competing_failures={stats['label_final_competing_failures']}")
    print(
        "label_split_resolution_certificate_rows="
        f"{stats['label_split_resolution_certificate_rows']}"
    )
    print(f"high_lift_continuation_supported_rows={stats['high_lift_continuation_supported_rows']}")
    print(
        "high_lift_continuation_step_delta_range="
        f"{stats['high_lift_continuation_step_delta_min']}.."
        f"{stats['high_lift_continuation_step_delta_max']}"
    )
    print(
        "high_lift_continuation_failures="
        f"integrality:{stats['high_lift_continuation_integrality_failures']},"
        f"no_drop:{stats['high_lift_continuation_no_drop_failures']}"
    )
    print(f"label_status_proved_constant_target_b1={stats['label_status_proved_constant_target_b1']}")
    print(f"label_status_target_high_lift_boundary={stats['label_status_target_high_lift_boundary']}")
    print(f"label_status_blocked_label_congruence={stats['label_status_blocked_label_congruence']}")
    print(f"label_status_blocked_prefix_integrality={stats['label_status_blocked_prefix_integrality']}")
    print(f"branch_word_certificate_failures={stats['branch_word_certificate_failures']}")
    print(f"arithmetic_certificate_rows={stats['arithmetic_certificate_rows']}")
    print(f"refined_formula_failures={stats['refined_formula_failures']}")
    print(f"refined_state_failures={stats['refined_state_failures']}")
    if stats.get("semantic_replay_enabled", 0):
        print(
            "semantic_replay="
            f"step_cap:{stats['semantic_replay_step_cap']},"
            f"drop:{stats['semantic_replay_drop_samples']},"
            f"return:{stats['semantic_replay_return_samples']},"
            f"valuation_tail:{stats['semantic_replay_valuation_tail_samples']},"
            f"step_tail:{stats['semantic_replay_step_tail_samples']},"
            f"loss:{stats['semantic_replay_loss_samples']},"
            f"loss_free:{stats['semantic_replay_loss_free']}"
        )
        print(
            "semantic_replay_step_max="
            f"drop:{stats['semantic_replay_drop_step_max']},"
            f"return:{stats['semantic_replay_return_step_max']},"
            f"valuation_tail:{stats['semantic_replay_valuation_tail_step_max']},"
            f"step_tail:{stats['semantic_replay_step_tail_step_max']}"
        )
        if stats.get("semantic_replay_word_audit_enabled", 0):
            print(
                "semantic_replay_drop_word_audit="
                f"distinct_words:{stats['semantic_replay_drop_distinct_words']},"
                f"phase_word_groups:{stats['semantic_replay_drop_phase_word_groups']},"
                "phase_word_singletons:"
                f"{stats['semantic_replay_drop_phase_word_singleton_groups']},"
                "distinct_suffixes:"
                f"{stats['semantic_replay_drop_distinct_suffixes']},"
                "suffix_slope_failures:"
                f"{stats['semantic_replay_drop_suffix_slope_failure_words']},"
                "suffix_threshold_max:"
                f"{stats['semantic_replay_drop_suffix_threshold_max']},"
                "common_prefix_failures:"
                f"{stats['semantic_replay_drop_common_prefix_failures']},"
                "common_prefix_samples:"
                f"{stats['semantic_replay_drop_common_prefix_samples']}"
            )
        if stats.get("semantic_replay_suffix_certificate_enabled", 0):
            print(
                "semantic_replay_suffix_certificate="
                f"rows:{stats['semantic_replay_suffix_certificate_row_count']},"
                f"cutoff:{stats['semantic_replay_suffix_certificate_cutoff']},"
                f"failures:{stats['semantic_replay_suffix_certificate_failures']},"
                "threshold_max:"
                f"{stats['semantic_replay_suffix_certificate_threshold_max']}"
            )
            print(
                "semantic_replay_suffix_pair_certificate="
                f"rows:{stats['semantic_replay_suffix_pair_certificate_row_count']},"
                f"cutoff:{stats['semantic_replay_suffix_pair_certificate_cutoff']},"
                f"failures:"
                f"{stats['semantic_replay_suffix_pair_certificate_failures']},"
                "threshold_max:"
                f"{stats['semantic_replay_suffix_pair_certificate_threshold_max']}"
            )
            print(
                "semantic_replay_suffix_pair_coverage="
                f"suffix_rows:{stats['semantic_replay_suffix_pair_coverage_suffix_rows']},"
                "covered_suffix_rows:"
                f"{stats['semantic_replay_suffix_pair_coverage_covered_suffix_rows']},"
                "uncovered_suffix_rows:"
                f"{stats['semantic_replay_suffix_pair_coverage_uncovered_suffix_rows']},"
                "covered_drop_samples:"
                f"{stats['semantic_replay_suffix_pair_coverage_covered_drop_samples']},"
                "covered_phase_word_groups:"
                f"{stats['semantic_replay_suffix_pair_coverage_covered_phase_word_groups']},"
                "failures:"
                f"missing_pair:{stats['semantic_replay_suffix_pair_coverage_missing_pair_failures']},"
                f"const_bound:{stats['semantic_replay_suffix_pair_coverage_const_bound_failures']},"
                "threshold_bound:"
                f"{stats['semantic_replay_suffix_pair_coverage_threshold_bound_failures']},"
                f"loss_free:{stats['semantic_replay_suffix_pair_coverage_loss_free']}"
            )
            print(
                "semantic_replay_source_pair_coverage="
                f"drop_samples:{stats['semantic_replay_source_pair_coverage_drop_samples']},"
                "covered_samples:"
                f"{stats['semantic_replay_source_pair_coverage_covered_samples']},"
                "uncovered_samples:"
                f"{stats['semantic_replay_source_pair_coverage_uncovered_samples']},"
                "common_prefix_failures:"
                f"{stats['semantic_replay_source_pair_coverage_common_prefix_failures']},"
                "failure_total:"
                f"{stats['semantic_replay_source_pair_coverage_failure_total']},"
                f"loss_free:{stats['semantic_replay_source_pair_coverage_loss_free']}"
            )
    if not args.no_write:
        print(f"wrote {csv_path}")
        print(f"wrote {json_path}")
    print("top branches:")
    for row in rows[: min(10, len(rows))]:
        print(
            "  "
            f"phase={row['phase']} step={row['step']} dst={row['dst']} "
            f"count={row['sample_count']} t={row['q']}*u+{row['r']} "
            f"next={row['a']}*u+{row['b']} "
            f"refined_t={row['refined_q']}*v+{row['refined_r']} "
            f"arith_cert={row['arithmetic_certificate']} "
            f"label={row['label_certificate_status']}"
        )


if __name__ == "__main__":
    main()
