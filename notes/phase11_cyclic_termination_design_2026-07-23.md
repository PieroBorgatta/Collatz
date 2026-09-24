# Phase 11: minimal cyclic-termination design

Date: 2026-07-23

## Decision

The first termination experiment will not build another large finite transfer
matrix and will not treat the sampled script-126 return rows as universal
rules. It will use exact Syracuse words and a small cyclic certificate whose
back-edges carry a natural-valued precision trace.

The new arithmetic primitive is in
`lean/CollatzShadowing/PrecisionTax.lean`. For an expansive word `w`, put

```text
P = 3^length(w)
Q = 2^sum(w)
C = syracuseWordConst(w)
D = P - Q
precision_w(n) = nu2(D*n + C).
```

If `w` matches `n` and sends it to `m`, then

```text
Q * (D*m + C) = P * (D*n + C)
precision_w(m) + sum(w) = precision_w(n).
```

Thus a repetition back-edge for a positive-sum expansive word has an exact
well-founded decrease. This is the constructive form of the finite-precision
cost of shadowing a negative periodic phantom.

## Complementary cycle constraints

`lean/CollatzShadowing/CycleConstraints.lean` treats the opposite scale: a
complete positive periodic orbit. If a nonempty exponent word `w` matches a
positive `n` and returns to `n`, it proves

```text
(2^sum(w) - 3^length(w)) * n = syracuseWordConst(w)
3^length(w) < 2^sum(w).
```

Consequently every divisor of the positive denominator must divide the word
constant. This is a cheap exact modular sieve for a proposed lasso; it avoids
orbit enumeration and rejects the entire word at once.

The same module proves a less standard prefix barrier. Let `j` be the first
prefix at which

```text
3^j < 2^B(j).
```

If the source is a minimum element of the putative cycle, then

```text
3*n <= j*3^j.
```

Thus any independent lower bound on a cycle minimum forces the initial
exponent sequence to remain expansive for a quantitatively long time. For
example, inserting the `2^71` verification threshold already used by the
project gives `j >= 43`: the first 42 prefixes satisfy
`2^B(i) <= 3^i`. In particular `B(42) <= 66`, so at least 18 of the first 42
accelerated exponents must equal `1`.

This does not exclude cycles by itself. It does turn a global lower bound
into a rigid local word constraint, which can be combined with exact
cylinders and the modular sieve without a large computation.

## Exact configuration

A checker-facing configuration is

```text
base_bits # current_bits #
```

where both bit strings are finite, normalized, least-significant-bit first,
and end at an explicit high-bit marker `#`. Its semantic projection is a pair
of positive odd naturals `(base, current)`.

The initial A0 configuration uses the already proved parametric identities

```text
base    = 103 + 256*t
current = 593 + 1458*t
128*current = 729*base + 817.
```

`base` remains fixed while macros update `current`. A terminal edge must prove
`current < base`, which is exactly the strict-descent target required by
`CollatzBridge.lean`.

## Minimal certificate schema

The first certificate should contain only:

```text
Node:
  id
  exact guard (word cylinder / finite-word predicate)
  active precision trace, if any

Edge:
  source node
  target node or DROP
  fixed Syracuse exponent word
  exact word-match guard
  trace relation: strict decrease, weak decrease, or trace switch

SCC certificate:
  nodes and edges in the SCC
  one trace thread that progresses on every infinite traversal
  or an exact proof that the SCC language is empty

Lasso check:
  concatenated exponent word W
  A = sum(W), L = length(W), C = syracuseWordConst(W)
  exact cycle candidate n = C / (2^A - 3^L), checked only when the
  denominator is positive and divides C
```

All values `A`, `L`, `C`, the affine endpoint, and the word cylinder must be
recomputed by the checker from the exponent word. They are not trusted
fields.

For a potential disproof, a stronger lasso artifact may give a nonempty
finite-word language `L` and prove exact closure under a macro together with
`current >= base` and exclusion of `1`. Such a verified closed trap would
produce a genuine nonterminating orbit family; failure to find one says
nothing globally.

## Reuse

- `CollatzBridge.lean`: `evalSyracuseWord`,
  `SyracuseWordMatchesFrom`,
  `evalSyracuseWord_mul_pow_sum_eq_affine_of_matches`,
  `directDropAt_of_word_chain_matches_eval_lt`, and the A0 common-prefix
  identities.
- `PrecisionTax.lean`: exact progress trace for a periodic expansive
  back-edge.
- `NoInfinite.lean`: existing sign/congruence rejection for positive
  eventually-periodic expansive phantoms.
- `EpisodeGraph.lean`: finite SCC and reachability shell.
- `scripts/spectral_program/126_A0_return_branch_affine_probe.py`:
  `exact_word_cylinder` and observed words may prioritize refinements, but its
  sampled branch labels are not proof inputs.

The Perron--Frobenius/CW and weak averaged layers are deliberately outside this
experiment.

## Mandatory regression family

For every even `r >= 2`, let

```text
n_r = 2^(r+1) - 1.
```

Its binary representation is an odd-length finite string of `1` bits. Its
first `r` accelerated exponents are `1`, the next exponent is exactly `2`,
and after the word `[1]^r ++ [2]` the endpoint is

```text
(3^(r+1) - 1) / 2 > n_r.
```

Therefore:

- the finite high-bit marker forces exit from the all-`1` phantom;
- exit from a periodic phantom does **not** imply descent;
- a certificate based only on one periodic precision counter is insufficient;
- switching traces inside a residual SCC are essential.

This family must be tested symbolically, not by enumerating its members.

## First experiment and kill criteria

1. Instantiate the exact precision trace for `[1]`, `[1,2]`, and `[2,1]`.
2. Start from the A0 post-prefix state and split only the low-exponent residual
   cases needed to expose those three templates.
3. Build the residual SCCs and ask for a cyclic trace proof; do not search for
   a large global ranking.
4. Apply the regression family above before adding more states.

Stop this prototype if any of the following occurs:

- a proposed edge cannot be lifted from samples to an exact word cylinder;
- closing the regression family requires the future hitting time or an
  unbounded valuation history as a state field;
- after patterns of length at most `3`, an SCC has neither a progressing
  precision trace nor an exact empty/cycle certificate;
- the number of residual control states more than doubles under each
  one-symbol refinement;
- the result is only another finite prefix coverage statement.

Success for the first prototype is intentionally smaller than Collatz: an
exact cyclic certificate proving strict descent for one new infinite A0
subfamily that includes arbitrarily long phantom-shadowing prefixes.
