# Phase 11: lazy 2-adic trie and cyclic trace prototype

Date: 2026-07-23

## Verdict

The first prototype supports the new direction, but also supplies an early
kill signal.

The useful replacement for finite residue sampling is an exact lazy 2-adic
trie. It already discovers and certifies infinite descent leaves. A naive
breadth-first expansion of that trie, however, retains too many growing
residual states. The next experiment must quotient residual states by a
progress trace; merely increasing the trie depth would recreate the failed
large-automaton strategy.

Nothing in this note proves or disproves the Collatz conjecture.

## Exact symbolic core

`scripts/phantom_taxonomy/symbolic_2adic_trie.py` represents:

```text
Cylinder:  u = r (mod 2^k)
OddAffine: F + G*u, with G odd.
```

For every depth `m`, it computes the unique root cylinder

```text
u = -F*G^(-1) (mod 2^m)
```

on which `v2(F+G*u) >= m`. Refinement follows only that root child; its
sibling has an exact, uniform valuation and closes immediately. The core also
implements cylinder intersection and exact reparameterization
`u = r + 2^k*v`.

The self-test checks the Phase-11 critical-cell congruences and explicitly
reports zero enumerated integer ranges.

## Constructive periodic-shadow bound

`lean/CollatzShadowing/PrecisionTax.lean` now telescopes the one-block
precision tax. For an expansive word `w`, write

```text
A = sum(w)
D = 3^length(w) - 2^A
P_w(n) = nu2(D*n + syracuseWordConst(w)).
```

If the first `k` consecutive copies of `w` actually match, Lean proves

```text
P_w(eval(w)^k(n)) + k*A = P_w(n),
k*A <= P_w(n),
k*A <= log_2(D*n + syracuseWordConst(w)).
```

For `A > 0`, this gives a finite explicit upper bound on the number of
consecutive blocks and a constructive theorem excluding an infinite actual
run of `w`. This is stronger operationally than merely saying that infinite
congruence to the phantom is impossible.

`lean/CollatzShadowing/PrecisionTemplates.lean` instantiates the result as

```text
[1]   : k   <= nu2(n + 1)
[1,2] : 3*k <= nu2(n + 5)
[2,1] : 3*k <= nu2(n + 7).
```

These are the first checker-ready cyclic trace templates.

They are progress traces, not terminal edges. The Lean theorems
`a0Endpoint_word_one_not_drop`, `a0Endpoint_word_one_two_not_drop`, and
`a0Endpoint_word_two_one_not_drop` show that none of these three words can by
itself move the A0 endpoint below its original source. Their precision budgets
prove that repetition must end; a separate high-valuation exit or a proved
trace switch is still necessary.

## Two Lean-verified infinite A0 leaves

The A0 common prefix sends

```text
103 + 256*t  ->  593 + 1458*t.
```

`lean/CollatzShadowing/A0InfiniteSubfamily.lean` proves two disjoint infinite
families without finite search.

### Leaf 1

For

```text
t = 2 + 16*u,
n = 615 + 4096*u,
```

the next exponent after the common prefix is at least `5`. The resulting
endpoint is bounded above by

```text
329 + 2187*u < 615 + 4096*u.
```

Lean proves `DirectDropAt 7 n` and hence `HasStrictDescent n`.

### Leaf 2

For

```text
t = 10 + 32*u,
n = 2663 + 8192*u,
```

the next exponent is exactly `4`, giving `2845 + 8748*u`. The following
exponent is at least `2`, and the endpoint is bounded above by

```text
2134 + 6561*u < 2663 + 8192*u.
```

Lean proves `DirectDropAt 8 n`.

Together these two formally proved cylinders occupy dyadic measure

```text
1/16 + 1/32 = 3/32
```

of the A0 parameter `t`.

## Bounded symbolic experiment

`scripts/phantom_taxonomy/a0_lazy_trie_prototype.py` derives transitions from
affine numerator factorization and the lazy-trie core. It contains no table of
sampled transitions and enumerates no integer values of `t`.

With `max_bits=8` and `max_steps=4`, it produces a prefix-free complete
frontier:

```text
closed leaves             45
residual leaves           65
valuation splits         109
closed dyadic measure   49/128
residual dyadic measure 79/128
maximum residual slope
  relative to the start   81/16
```

The two Lean leaves above are rediscovered automatically. The other closed
Python leaves are exact affine certificates, but have not been imported into
Lean.

## Trace-switch gate

The proposed local quotient was tested rather than assumed.
`scripts/phantom_taxonomy/a0_residual_quotient.py` preserves, for every
residual state, its exact source/current affine relation, applicable short
trace, and complete rooted valuation profile. On the 65 residual leaves it
finds:

```text
distinct exact words       65
exact merge classes        65
largest merge class         1
frontier reduction       0/65
```

Grouping only by the labels `n+1`, `n+5`, and `n+7` would reduce the count,
but only by discarding the source relation and the 2-adic root that determines
later transitions. That quotient is therefore rejected.

There is also an exact obstruction to using those three scalar traces as a
closed size-change library. The feasible macro lasso `[1] ; [1,2]` cycles

```text
(nu2(n+1),nu2(n+5),nu2(n+7))
    (3,2,1) -> (2,5,1) -> (3,2,1).
```

`lean/CollatzShadowing/ThreeTraceObstruction.lean` constructs arbitrarily
precise natural approximants to the hidden fixed point `-19/11`; hence this is
not a spurious abstract matrix path.

The positive replacement is in
`lean/CollatzShadowing/SwitchingPrecision.lean`. Give each control point an
affine label `(D,C)` and use the precision

```text
P(D,C,n) = nu2(D*n+C).
```

Across `2^e*m=3*n+1`, a switch to `(D',C')` is valid when some odd `q`
satisfies

```text
3*D' = q*D,
D' + 2^e*C' = q*C.
```

Lean then proves

```text
P(D',C',m) + e = P(D,C,n).
```

For the obstructing lasso the compatible labels are

```text
(11,19) -> (11,23) -> (11,29) -> (11,19),
```

and the hidden precision loses exactly four bits. Free relabeling is
explicitly ruled out: without the compatibility equations, a shift can
manufacture any desired precision value.

## Research decision

The prototype passes the exactness test and fails the naive scalability test:

- exact cylinders replace sampled representatives successfully;
- infinite subfamilies can be closed with short affine inequalities;
- periodic phantom repetitions have a finite, logarithmic precision budget;
- after only four residual steps, `79/128` of the parameter measure is still
  unresolved and some surviving affine slopes have grown by `81/16`;
- the first exact local quotient gives no merges at all;
- the fixed three-trace library admits an exact repeated control cycle.

Therefore both a deeper breadth-first trie and the proposed local residual
quotient are stopped. The surviving experiment is narrower:

1. attach unknown affine labels `(D_i,C_i)` to the nodes of a proposed small
   residual SCC;
2. solve the edge compatibility equations exactly;
3. accept the SCC only if every infinite traversal follows a compatible
   precision thread with positive total exponent;
4. retain the finite high-bit marker for acyclic exits and terminal descent;
5. reject the architecture if no small control graph can be proposed without
   first enumerating a deeper residue tree.

The remaining issue is now algebraic and explicit: construct a small control
graph whose edge labels admit compatible affine transport. More residue
sampling cannot answer it.

Update 2026-07-27: the exact graph solver has now answered this gate.
Compatible scalar labels exist only when every cycle through a control node
shares the same rational formal point. A genuinely branching SCC containing
the `[1]` and `[1,2]` cycles is inconsistent, and the same two-node graph
contains infinitely many distinct cycle fixed points from
`[1]^(r+1) ++ [2]`. Therefore the scalar-label SCC program is retained only
as a periodic-lasso checker, not as the global aperiodic route. See
`phase11_affine_trace_graph_verdict_2026-07-27.md`.

## Reproduction

```bash
python3 scripts/phantom_taxonomy/symbolic_2adic_trie.py
python3 scripts/phantom_taxonomy/a0_lazy_trie_prototype.py
python3 scripts/phantom_taxonomy/a0_residual_quotient.py
lake build
```
