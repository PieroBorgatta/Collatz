# Phase 10 Refined Square Key Drift

Date: 2026-05-25

Status: finite diagnostic update for script
`111_refined_square_key_drift_inspector.py`.

## Question

Script `110_refined_square_probe.py` showed that the square A1 kernel

```text
(PhaseState, t mod 2^10) -> (PhaseState, next_t mod 2^10)
```

still has much larger prefix drift than the phase-only kernel at the same
prefix scale.  The next question was whether this drift is concentrated in a
few refined source keys or distributed across a broader structural family.

## Run

```text
python scripts/spectral_program/111_refined_square_key_drift_inspector.py \
  --T 14 \
  --j-counts 32,64 \
  --bits 10 \
  --v2-cap 14 \
  --max-steps 1000 \
  --progress \
  --output-tag T14_j32_64_b10
```

Outputs:

```text
scripts/spectral_program/collatz_111_T14_j32_64_b10_refined_square_key_drift_report.md
scripts/spectral_program/collatz_111_T14_j32_64_b10_refined_square_key_drift_top_keys.csv
scripts/spectral_program/collatz_111_T14_j32_64_b10_refined_square_key_drift_phase_strata.csv
scripts/spectral_program/collatz_111_T14_j32_64_b10_refined_square_key_drift_residue_strata.csv
```

## Global Result

The script reproduces the script-`110` global drift:

```text
weighted_l1_mean = 0.0121733793
```

for `T = 14`, `j = 32 -> 64`, `b = 10`.

The drift is not dominated by a tiny set of individual keys:

```text
top 10 source keys:   0.0822067093 of total contribution
top 25 source keys:   0.131231692
top 100 source keys:  0.254601736
```

This argues against a finite exceptional-list explanation.

## Structural Concentration

Although the drift is not concentrated in a few keys, it is strongly
structured by source family.  Aggregating the phase strata by `(v2, odd mod
4)` gives:

```text
source family   contribution share
0|3             0.276675986
0|1             0.257316208
1|3             0.151018091
1|1             0.074874169
```

Together these four families explain about `0.759884454` of the total
`b=10` drift.

Residue bands also matter.  The two largest `rlo mod 32` strata are:

```text
rlo mod 32 = 6    contribution share 0.0845938932
rlo mod 32 = 26   contribution share 0.0748741690
```

So the obstruction is neither a few isolated keys nor featureless noise.  It
is a broad low-valuation/odd-residue phenomenon with visible low-residue
bands.

## Interpretation

The A1 branch remains alive as a research branch, but the shape of the
obstruction changed:

```text
wrong model:  remove a small exceptional list of bad refined residues
better model: split/control source families such as (v2, odd mod 4)
```

This pushes the next analytic move toward a two-level or mixed norm:

```text
primary quotient:       PhaseState or PhaseState + r mod 2^10
source-family weight:   explicit control for low v2 / odd residue families
error target:           weak averaged row-TV, not uniform row-TV
```

## Consequence for Gate 10.B

This diagnostic does not close Gate 10.B.

It does, however, rule out the most naive A1 hope: the remaining drift is not
caused by a small handful of removable source keys.  Any successful A1 theorem
must control structured source families, especially low `v2` with odd residue
`1` or `3` modulo `4`.

The most honest next step is therefore to test whether a source-family
weighted weak norm lowers the effective prefix drift without creating a new
large exceptional set.
