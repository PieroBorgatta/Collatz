#!/usr/bin/env python3
"""Exhaustive finite error check for the signed residual, not a density test.

Frozen domain: lengths 2..5, positive exponent total <=12, targets
5,7,31,593 and their canonical siblings; all admissible nonzero two edits.
The as-yet-unbounded analytic theorem is not numerically certified here.
"""

from collections import Counter
from functools import lru_cache
import json

TARGETS = (5, 7, 31, 593)
MAX_LENGTH = 5
MAX_TOTAL = 12


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for head in range(1, total - length + 2):
        for rest in compositions(total - head, length - 1):
            yield (head,) + rest


def constant(word):
    # Direct closed sum, independent of the old surgery probe's recurrence.
    prefix = 0
    result = 0
    for index, exponent in enumerate(word):
        result += 3 ** (len(word) - index - 1) * 2 ** prefix
        prefix += exponent
    return result


def v3(number):
    require(number != 0, "valuation at zero")
    number = abs(number)
    result = 0
    while number % 3 == 0:
        result += 1
        number //= 3
    return result


@lru_cache(maxsize=None)
def inverse(word, target):
    numerator = 2 ** sum(word) * target - constant(word)
    divisor = 3 ** len(word)
    if numerator <= 0 or numerator % divisor:
        return None
    source = numerator // divisor
    require(source % 2 == 1, "admissible word did not give odd source")
    state = source
    for exponent in word:
        value = 3 * state + 1
        actual = 0
        while value % 2 == 0:
            actual += 1
            value //= 2
        require(actual == exponent, "wrong exact exponent")
        state = value
    require(state == target, "wrong endpoint")
    return source


def run():
    counts = Counter()
    examples = []
    for length in range(2, MAX_LENGTH + 1):
        for total in range(length, MAX_TOTAL + 1):
            for word in compositions(total, length):
                counts["words"] += 1
                old_constant = constant(word)
                for n in TARGETS:
                    y = 4 * n + 1 if n % 3 == 1 else 16 * n + 5
                    source = inverse(word, n)
                    if source is not None:
                        counts["exact_original_words"] += 1
                        require(2 ** total * n <= 4 ** length * source,
                                "elementary exponent budget failed")
                    for index in range(length - 1):
                        P = sum(word[:index + 1])
                        tail = word[index + 1:]
                        B = sum(tail)
                        T = constant(tail)
                        require(T % 2 == 1, "tail constant is not odd")
                        for delta in range(1 - word[index], word[-1]):
                            if delta == 0:
                                continue
                            counts["positive_exponent_edits"] += 1
                            shifted = list(word)
                            shifted[index] += delta
                            shifted[-1] -= delta
                            shifted = tuple(shifted)
                            require(min(shifted) >= 1 and sum(shifted) == total,
                                    "invalid balanced edit")
                            Cnew = constant(shifted)
                            d = abs(delta)
                            if delta > 0:
                                factor = 2 ** P
                                residual = 2 ** B * (y - n) - (2 ** d - 1) * T
                                terminal = y - 2 ** d * n
                                require(Cnew - old_constant == (2 ** d - 1) * factor * T,
                                        "positive constant identity failed")
                            else:
                                factor = 2 ** (P - d)
                                residual = 2 ** (B + d) * (y - n) + (2 ** d - 1) * T
                                terminal = 2 ** d * y - n
                                require(old_constant - Cnew == (2 ** d - 1) * factor * T,
                                        "negative constant identity failed")
                            require(residual % 2 == 1 and residual != 0,
                                    "signed residual should be nonzero odd")
                            require(2 ** total * (y - n) - (Cnew - old_constant)
                                    == factor * residual, "full residual identity failed")
                            if source is None:
                                continue
                            image = inverse(shifted, y)
                            if image is None:
                                continue
                            counts["exact_transports"] += 1
                            counts["positive_transports" if delta > 0 else "negative_transports"] += 1
                            require(3 ** length * (image - source) == factor * residual,
                                    "physical residual identity failed")
                            require(residual % 3 ** length == 0, "full depth divisibility failed")
                            require(length <= v3(residual), "depth valuation failed")
                            require(len(tail) <= v3(terminal), "terminal locality failed")
                            require(source != image, "distinct targets at same source and length")
                            examples.append({"n": n, "y": y, "word": word,
                                             "modified": shifted, "delta": delta,
                                             "index": index, "u": source, "v": image,
                                             "q": len(tail), "residual": residual,
                                             "v3_residual": v3(residual)})
    return {"protocol": {"targets": TARGETS, "lengths": [2, MAX_LENGTH],
                          "maximum_total": MAX_TOTAL, "shifts": "all positive-exponent admissible"},
            "counts": dict(sorted(counts.items())), "transports": examples,
            "status": "PASS", "meaning": "finite algebra and exact replay error check only"}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
