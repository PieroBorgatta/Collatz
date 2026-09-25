#!/usr/bin/env python3
"""Exact finite parity traces and block balances for the Q_v family.

T(n) = n/2 for even n, (3*n+1)/2 for odd n.  A trace of H steps
depends only on n modulo 2**H.  Step r has balance 306*r - 589*J(r).
This is a finite computation, not a uniform assertion about the family.

The divide-and-conquer engine uses the identity
    T**m(n) = 3**J(m) * (n >> m) + T**m(n % 2**m).
It avoids updating an H-bit integer at every small lookup-table block.
Packed trace bit r is the parity of T**r(n), least-significant bit first.
"""

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import time


EVEN_GAIN = 306
ODD_COST = 283
ODD_PENALTY = EVEN_GAIN + ODD_COST


def horizon(v):
    if v < 5:
        raise ValueError("require v >= 5")
    return (589 * (1 << v) + 611) // 612


def initial_residue(v, bits):
    """Q_v mod 2**bits; no complete integer Q_v is constructed."""
    if v < 1 or bits < 1:
        raise ValueError("require v >= 1 and bits >= 1")
    # Repeated squaring with a bit mask avoids general big-integer division
    # by a power-of-two modulus.  Every intermediate is reduced modulo it.
    mask = (1 << (bits + v + 3)) - 1
    residue = 9 & mask
    for _ in range(v):
        residue = (residue * residue) & mask
    return (residue - 1) >> (v + 3)


@lru_cache(maxsize=None)
def leaf_table(width):
    """(odd count, multiplier, exact terminal value, packed parity word)."""
    if not 1 <= width <= 16:
        raise ValueError("require 1 <= leaf width <= 16")
    table = []
    powers = [3**j for j in range(width + 1)]
    for residue in range(1 << width):
        value, odd, word = residue, 0, 0
        for i in range(width):
            bit = value & 1
            odd += bit
            word |= bit << i
            value = (3 * value + 1) >> 1 if bit else value >> 1
        table.append((odd, powers[odd], value, word))
    return table


def _put_word(trace, offset, width, word):
    byte, shift = divmod(offset, 8)
    word <<= shift
    for i in range((width + shift + 7) // 8):
        trace[byte + i] |= (word >> (8 * i)) & 255


def parity_trace(residue, bits, leaf_width=16, method="divide"):
    """Return canonical packed parity bytes for exactly ``bits`` T steps.

    ``divide`` is the fast recursive engine; ``linear`` independently applies
    the short affine maps to the remaining modular residue.  Both are exact.
    The linear method is useful for smaller replay checks, but scales poorly.
    """
    if bits < 1 or residue < 0 or residue.bit_length() > bits:
        raise ValueError("require a positive precision and a residue in range")
    if not 1 <= leaf_width <= 16:
        raise ValueError("require 1 <= leaf_width <= 16")
    if method not in ("divide", "linear"):
        raise ValueError("method must be divide or linear")
    trace = bytearray((bits + 7) // 8)

    def visit(value, length, offset, need_terminal=True):
        if length <= leaf_width:
            odd, multiplier, terminal, word = leaf_table(length)[value]
            _put_word(trace, offset, length, word)
            return odd, multiplier, terminal
        # Full-width leaves stay aligned; only the final leaf can be shorter.
        left = max(1, (length // leaf_width) // 2) * leaf_width
        right = length - left
        odd_l, mul_l, end_l = visit(value & ((1 << left) - 1), left, offset)
        middle = mul_l * (value >> left) + end_l
        odd_r, mul_r, end_r = visit(
            middle & ((1 << right) - 1), right, offset + left,
            need_terminal,
        )
        if not need_terminal:
            return odd_l + odd_r, 0, 0
        return odd_l + odd_r, mul_l * mul_r, mul_r * (middle >> right) + end_r

    if method == "divide":
        visit(residue, bits, 0, False)
    else:
        remaining, offset = bits, 0
        while remaining:
            take = min(leaf_width, remaining)
            low = residue & ((1 << take) - 1)
            _, multiplier, terminal, word = leaf_table(take)[low]
            _put_word(trace, offset, take, word)
            remaining -= take
            residue = (multiplier * (residue >> take) + terminal) & (
                (1 << remaining) - 1
            )
            offset += take
    return bytes(trace)


def direct_trace(residue, bits):
    """Independent elementary T replay, intended for small test cases."""
    if bits < 1 or residue < 0 or residue.bit_length() > bits:
        raise ValueError("require a positive precision and a residue in range")
    trace = bytearray((bits + 7) // 8)
    for r in range(bits):
        odd = residue & 1
        trace[r >> 3] |= odd << (r & 7)
        residue = (3 * residue + 1) >> 1 if odd else residue >> 1
    return bytes(trace)


# Summary: length, odd, delta, minimum, min_position, maximum, max_position,
#          maximum_drawdown, drawdown_start, drawdown_end.
EMPTY = (0,) * 10


def _merge(left, right):
    length, odd, delta, lo, lo_at, hi, hi_at, draw, start, end = left
    nr, jr, dr, lr, lra, hr, hra, rr, rsa, rea = right
    low, low_at = (delta + lr, length + lra) if delta + lr < lo else (lo, lo_at)
    high, high_at = (delta + hr, length + hra) if delta + hr > hi else (hi, hi_at)
    candidates = ((draw, start, end), (rr, length + rsa, length + rea),
                  (hi - delta - lr, hi_at, length + lra))
    best = min(candidates, key=lambda row: (-row[0], row[1], row[2]))
    return (length + nr, odd + jr, delta + dr, low, low_at, high, high_at, *best)


@lru_cache(maxsize=None)
def _summary_table(width, drift):
    table = []
    for word in range(1 << width):
        result = EMPTY
        for i in range(width):
            odd = (word >> i) & 1
            delta = EVEN_GAIN - drift - ODD_PENALTY * odd
            step = (1, odd, delta, min(0, delta), int(delta < 0),
                    max(0, delta), int(delta > 0), max(0, -delta), 0,
                    int(delta < 0))
            result = _merge(result, step)
        table.append(result)
    return table


def _summary_dict(summary, offset=0, balance=0):
    n, j, delta, low, low_at, high, high_at, draw, start, end = summary
    return {
        "start_step": offset, "end_step": offset + n, "length": n,
        "odd_steps": j, "balance_start": balance, "balance_end": balance + delta,
        "balance_delta": delta, "minimum_balance": balance + low,
        "minimum_at_step": offset + low_at, "maximum_balance": balance + high,
        "maximum_at_step": offset + high_at, "maximum_drawdown": draw,
        "drawdown_from_step": offset + start, "drawdown_to_step": offset + end,
    }


def summarize_trace(trace, bits, block_size=256, drift=0):
    """Exact block counts, prefix extrema, and largest peak-to-later-trough loss.

    Extrema include the initial prefix.  Ties select the earliest position;
    drawdown ties select the lexicographically earliest (start, end) pair.
    All positions and balances in returned records are absolute.  With drift
    d the balance is (306-d)*r - 589*J(r); d=1 gives the proposed credit walk.
    """
    if bits < 1 or len(trace) != (bits + 7) // 8 or block_size < 1:
        raise ValueError("invalid trace length or block size")
    if bits % 8 and trace[-1] >> (bits % 8):
        raise ValueError("unused high bits in packed trace must be zero")
    overall, blocks, offset = EMPTY, [], 0
    while offset < bits:
        end = min(bits, offset + block_size)
        summary, pos = EMPTY, offset
        while pos < end:
            take = min(8 - (pos & 7), end - pos)
            word = (trace[pos >> 3] >> (pos & 7)) & ((1 << take) - 1)
            summary = _merge(summary, _summary_table(take, drift)[word])
            pos += take
        blocks.append(_summary_dict(summary, offset, overall[2]))
        overall = _merge(overall, summary)
        offset = end
    result = _summary_dict(overall)
    result["drift_per_step"] = drift
    result["block_size"] = block_size
    result["blocks"] = blocks
    return result


def analyze_level(v, block_size=256, leaf_width=16, method="divide",
                  trace_path=None):
    """Compute one finite level; optional trace can be independently replayed."""
    bits = horizon(v)
    t0 = time.perf_counter()
    residue = initial_residue(v, bits)
    residue_digest = hashlib.sha256(residue.to_bytes((bits + 7) // 8, "little")).hexdigest()
    t1 = time.perf_counter()
    trace = parity_trace(residue, bits, leaf_width, method)
    t2 = time.perf_counter()
    result = summarize_trace(trace, bits, block_size)
    result["drifted_balance"] = summarize_trace(trace, bits, block_size, drift=1)
    t3 = time.perf_counter()
    if trace_path is not None:
        Path(trace_path).write_bytes(trace)
    result.update({
        "v": v, "horizon": bits, "budget": 1 << (v - 1),
        "budget_passed": result["odd_steps"] <= (1 << (v - 1)),
        "terminal_balance_nonnegative": result["balance_end"] >= 0,
        "method": method, "leaf_width": leaf_width,
        "initial_residue_sha256": residue_digest,
        "parity_trace_sha256": hashlib.sha256(trace).hexdigest(),
        "timings_seconds": {"initial_residue": t1 - t0, "parity_trace": t2 - t1,
                            "summaries": t3 - t2},
        "scope": "Exact finite modular computation, not a uniform theorem.",
    })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v", type=int, required=True)
    parser.add_argument("--block-size", type=int, default=256)
    parser.add_argument("--leaf-width", type=int, default=16)
    parser.add_argument("--method", choices=("divide", "linear"), default="divide")
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze_level(args.v, args.block_size, args.leaf_width, args.method, args.trace)
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output is None:
        print(encoded, end="")
    else:
        args.output.write_text(encoded)
        compact = {key: value for key, value in result.items() if key != "blocks"}
        compact["drifted_balance"] = {
            key: value for key, value in result["drifted_balance"].items()
            if key != "blocks"
        }
        print(json.dumps(compact))


if __name__ == "__main__":
    main()
