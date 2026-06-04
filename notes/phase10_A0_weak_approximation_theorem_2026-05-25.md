# A0 Weak Approximation Theorem

Date: 2026-05-25

Status: conditional theorem skeleton.  This is the current clean target for
Gate 10.B.  It is not a proof of Collatz, not a spectral gap, and not a
Lasota-Yorke theorem.

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

### A0W7. Limit Operator Convention

There is a declared killed weighted operator `U` such that the finite
approximants are compared by:

```text
I_N K_N E_N -> U
```

in `B_s -> B_w`, or else the statement is explicitly restricted to Cauchy
convergence of the approximants `I_N K_N E_N`.

## Conclusion

Under A0W1-A0W7:

```text
|| I_N (K_{2N} - K_N) E_N ||_{B_s -> B_w}
  <= C_E C_I (D_N + r_N + tau_{N,L} + exceptional_tail_N).
```

If:

```text
D_N -> 0,
r_N -> 0,
tau_{N,L} -> 0,
lim_R limsup_N exceptional_tail_{N,R} -> 0,
```

then the A0 finite-rank approximants are Cauchy in the declared weak operator
topology:

```text
I_N K_N E_N
```

has a weak limit or approximates the declared `U`, depending on A0W7.

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
D_N -> 0,
low-v2 decay after the exact high-v2 source-tail count,
E_N/I_N Banach bounds,
limit operator convention.
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

The next proof-level task is A0W2:

```text
prove or falsify the two-parameter Cauchy/tail statement.
```

Computationally, the next useful support script should not add new features.
It should continue estimating the two parts separately:

```text
D_N(v2 < R) ~ c_R N^{-alpha_R}
mu_N(v2 >= R) <= eps_R, with eps_R -> 0
```

or expose where that decomposition fails.
