# Phase 10 A0 v2 Tail Formula

Date: 2026-05-25

Status: exact finite source-count lemma for the current script-`111` A0
phase-strata source model.

## Question

Script `115` reduced the A0 weak approximation route to a double-limit
decomposition:

```text
D_N <= D_N(v2 < R) + 2 * mu_N(v2 >= R).
```

The numerical tail masses looked geometric:

```text
mu_N(v2 >= R) ~= 2^-R.
```

The question was whether this was another empirical fit or an exact
counting fact.

## Result

For a script-`111` A0 comparison with

```text
L = j_left  * 2^T
R = j_right * 2^T
```

and with `t=0` excluded, the source phase satisfies:

```text
mu({phase_v2 >= q})
  = (floor((L - 1)/2^q) + floor((R - 1)/2^q)) / (L + R - 2)
  <= 2^-q.
```

This is exact for every `q` up to the source `v2` cap.  The hit-coordinate
factor cancels from numerator and denominator.

## Verification

Command:

```text
python3 scripts/spectral_program/117_A0_v2_tail_formula.py \
  --output-tag current_A0
```

Outputs:

```text
scripts/spectral_program/collatz_117_current_A0_A0_v2_tail_formula_report.md
scripts/spectral_program/collatz_117_current_A0_A0_v2_tail_formula_by_scale.csv
```

Headline check:

```text
max absolute observed-formula error = 0
max formula / 2^-q                 = 0.9999904633
```

Latest scale:

```text
q    observed tail      formula tail       2^-q
4    0.06249940395      0.06249940395      0.0625
6    0.01562437415      0.01562437415      0.015625
8    0.00390561670      0.00390561670      0.00390625
10   0.000975927338     0.000975927338     0.0009765625
12   0.000243504997     0.000243504997     0.000244140625
14   0.0000603994118    0.0000603994118    0.00006103515625
```

## Lean Artifact

The integer core is formalized in:

```text
lean/CollatzShadowing/WeakBridge.lean
```

The theorem is:

```text
CollatzShadowing.WeakBridge.TailCount.dyadic_tail_count_mul_le
```

It states:

```text
((floor((L - 1)/2^q) + floor((R - 1)/2^q)) * 2^q)
  <= L + R - 2.
```

Verification:

```text
cd lean
lake build CollatzShadowing.WeakBridge
lake build CollatzShadowing
```

Both builds pass.

## Meaning

The high-`v2` tail part of the A0 weak decomposition is no longer a fitted
diagnostic.  It is an exact finite source-count bound.

The remaining hard statement is now sharply isolated:

```text
for every fixed R, prove D_N(v2 < R) -> 0.
```

Script `115` gives strong finite evidence for this low-`v2` decay, with
power-law exponents near `0.6`, but that part is still not proved.
