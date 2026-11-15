# A0 Weak Approximation Theorem

Date: 2026-05-25

Status: conditional theorem skeleton, corrected 2026-11-13. The finite
action-error inequality remains valid. The original conclusion that
successive drifts tending to zero imply Cauchy convergence is withdrawn;
the additional compatibility and convergence hypotheses below are needed.
This is not a proof of Collatz, a spectral gap, or a Lasota-Yorke theorem.
See the [November correction and branch-clock lemma](research_sprint_2026-11-13/agents/S11_KERNEL_IT.md).

## Object

For each prefix scale `N`, let:

```text
Q_N       finite PhaseState alphabet
mu_N      finite nonnegative source-row weight
K_N       A0 phase-only averaged row-source kernel
D_N       weighted row-L1 prefix drift
E_N       projection/observation map from strong space to finite observables
I_N       inclusion/reconstruction map from finite weak rows to weak space
```

The finite drift is:

```text
D_N = sum_i mu_N(i) sum_j |K_{2N}(i,j) - K_N(i,j)|.
```

The newest measured A0 values are:

```text
T=14, b=0:
  D_{32,64}  = 0.000420440901
  D_{64,128} = 0.000285774472
```

## Theorem A0WeakApproximation

Assume:

### A0W1. Finite Kernel Identification

The script-generated A0 phase-only rows are exactly the finite kernels
`K_N`, up to an explicit bookkeeping residual `r_N`:

```text
||K_N^{script} - K_N||_{ell_infty -> L1(mu_N)} <= r_N.
```

Current status:

```text
CSV-internal identity verified for earlier Phase-10 data by script 107.
Lean import/match for the newest T=14/T=15 prefix kernels is still open.
```

### A0W2. Finite Weak Drift

The phase-only prefix drifts tend to zero:

```text
D_N -> 0.
```

Current status:

```text
finite evidence positive, theorem open.
```

This is a necessary drift target, not a sufficient Cauchy criterion.
For example, the one-state substochastic kernels
`K_{2^m}=(1+sin(log(m+1)))/2` have successive differences tending to zero
and do not converge.

### A0W3. Exceptional-Source Tail

There exists a source subset `E_N(R)` containing sparse high-`v2` rows such
that:

```text
lim_{R -> infinity} limsup_N mu_N(E_N(R)) = 0,
```

and the complement has controlled row drift.  The finite diagnostics now
support the sharper two-parameter form:

```text
lim_{R -> infinity} limsup_{N -> infinity}
  [D_N(v2 < R) + 2 mu_N(v2 >= R)] = 0.
```

Current evidence:

```text
max-row source at T=14, 64->128, b=0:
  phase 14|3|h,
  sample weight 47 per h,
  total exceptional mass for four h ~= 2.98818e-5.
```

Current theorem-level update for the script-`111` source model:

```text
mu_N(v2 >= R)
  = (floor((L - 1)/2^R) + floor((R' - 1)/2^R)) / (L + R' - 2)
  <= 2^-R
```

for the two compared prefixes `L,R'`, with `t=0` excluded.  Thus the
high-`v2` mass part of A0W3 is proved for the current finite source model.
The remaining A0W3 content is the low-`v2` decay term `D_N(v2 < R) -> 0`
for each fixed `R`.

### A0W4. Tail/Killing Control

Terminal/killed observations, excluded cells, and any `delta > L`
truncation are controlled by a separate error term:

```text
tau_{N,L} -> 0
```

in the same weak norm.

### A0W5. Projection Bound

There is a strong Banach space `B_s` and finite observation maps:

```text
E_N : B_s -> ell_infty(Q_N)
```

with uniform constant `C_E`:

```text
||E_N f||_infty <= C_E ||f||_{B_s}.
```

### A0W6. Inclusion Bound

There is a weak Banach space `B_w` and reconstruction/inclusion maps:

```text
I_N : L1(mu_N) -> B_w
```

with uniform constant `C_I`:

```text
||I_N g||_{B_w} <= C_I ||g||_{L1(mu_N)}.
```

### A0W7. Common Space and Additional Convergence Hypothesis

Declare `A_N=I_N K_N E_N` in one common space of bounded operators
`B_s -> B_w`. A bound on `I_N(K_{2N}-K_N)E_N` does not by itself bound
`A_{2N}-A_N` when the maps or finite alphabets vary: comparison maps and
their compatibility errors must be supplied.

A sufficient norm-convergence hypothesis is a nonnegative summable
sequence `a_m` with

```text
||A_{2^(m+1)}-A_{2^m}||_{B_s -> B_w} <= a_m,
sum_m a_m < infinity.
```

The error `a_m` must include the drift, bookkeeping, truncation, exceptional
tail and comparison-map errors at the declared cutoffs. In a complete
operator-norm space this proves convergence along dyadic scales by the
triangle inequality. Convergence on all scales requires an additional
interpolation/comparison estimate. Alternatively, a direct Cauchy estimate
between arbitrary sufficiently large scales, or an independently proved
sampling/conditional-expectation convergence theorem, can be used.
Identifying the resulting limit with a specified killed operator `U` is
a separate obligation; assuming convergence to `U` is not a proof of it.

## Conclusion

Under A0W1-A0W7:

```text
|| I_N (K_{2N} - K_N) E_N ||_{B_s -> B_w}
  <= C_E C_I (D_N + r_N + tau_{N,L} + exceptional_tail_N).
```

The conditions:

```text
D_N -> 0,
r_N -> 0,
tau_{N,L} -> 0,
lim_R limsup_N exceptional_tail_{N,R} -> 0,
```

give vanishing successive finite action errors only. They do not imply
that the approximants are Cauchy. The original claim to that effect is
superseded by the strengthened A0W7 above. A summable bound for the full
dyadic increments gives norm convergence on dyadic scales; a weaker
topology needs its own Cauchy/completeness argument. A rate such as
`a_m <= C*2^(-alpha*m)`, `alpha>0`, would suffice, but is not proved for
the full A0 kernel here.

## Lean-Formalized Part

The finite inequality feeding the theorem is already formalized:

```text
lean/CollatzShadowing/WeakBridge.lean
theorem CollatzShadowing.WeakBridge.weighted_action_diff_le
```

This proves:

```text
finite weighted row-L1 drift controls finite ell_infty -> L1 action error.
```

So Lean now covers the algebraic finite bridge.  The open work is analytic:

```text
compatible, summably controlled full increments (or another Cauchy theorem),
low-v2 decay after the exact high-v2 source-tail count,
E_N/I_N Banach bounds,
identification of the limit operator.
```

## What This Still Does Not Prove

Even a complete proof of `A0WeakApproximationTheorem` would not by itself
prove Collatz.  It would prove that the current finite matrices have a
legitimate weak operator-limit interpretation.

To attack Collatz after that, one would still need a second theorem:

```text
weak approximation + dissipative/spectral property => no divergent orbit.
```

That second theorem is not currently established.

## Immediate Next Task

The next proof-level task is the strengthened A0W2/A0W7 combination:

```text
prove a summable dyadic error bound, or a direct arbitrary-scale Cauchy
estimate, with the tail and comparison-map errors included.
```

Computationally, the next useful support script should not add new features.
It should continue estimating the two parts separately:

```text
D_N(v2 < R) ~ c_R N^{-alpha_R}
mu_N(v2 >= R) <= eps_R, with eps_R -> 0
```

or expose where that decomposition fails.
