#!/usr/bin/env python3
"""Compare exact census data, tolerating only display-log rounding.

AI-assisted development: Codex with Piero Borgatta, 2026-09-26.
The integer counts, targets, cutoff choices and all other fields must match.
"""
import json
import math
import sys
from pathlib import Path


def compare(expected, actual, path="root"):
    if path.endswith(".scaled_ratio_float"):
        if not isinstance(expected, float) or not isinstance(actual, float):
            raise ValueError(f"{path}: display ratio must be a float")
        if not math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-15):
            raise ValueError(f"{path}: display ratio exceeds rounding tolerance")
    elif isinstance(expected, dict):
        if not isinstance(actual, dict) or expected.keys() != actual.keys():
            raise ValueError(f"{path}: object type or keys differ")
        for key in expected:
            compare(expected[key], actual[key], f"{path}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise ValueError(f"{path}: list type or length differs")
        for i, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, f"{path}[{i}]")
    else:
        if type(expected) is not type(actual) or expected != actual:
            raise ValueError(f"{path}: exact value or type differs")


if __name__ == "__main__":
    compare(json.loads(Path(sys.argv[1]).read_text()), json.loads(Path(sys.argv[2]).read_text()))
    print("Exact integer census matches; display logarithms agree within 1e-12 relative tolerance.")
