# Phase 10 High-Bit Limit Conventions

Date: 2026-05-13

Status: definition-design note.  This note fixes the choices that must
be made before any finite matrix can be called an approximation of an
infinite operator.

## 1. Problem

The high-bit experiments use lifts

```text
t = r + j * 2^T.
```

For fixed `T`, `r`, and `h`, the variable `j` ranges over nonnegative
integers.  Gate 10.B asks whether the finite matrices produced from
finite prefixes of `j` are projections or controlled approximants of an
infinite object.

This question is meaningless until the limit in `j` is specified.

## 2. Candidate meanings of `j -> infinity`

### 2.1 2-adic cylinder refinement

Interpret `j mod 2^a` as deeper 2-adic bits:

```text
t == r + q * 2^T mod 2^(T+a).
```

Then increasing `a` refines the source cylinder.

This is the most natural interpretation of the observed `j mod 32`
signal.

Projection target:

```text
E_{T+a} K I_{T+a}
```

for a kernel `K` on `Z_2 x H`, if such a kernel exists.

Failure mode:

- deeper cylinders do not become locally constant or Cauchy in a useful
  norm.

### 2.2 Cesaro high-lift average

For a finite prefix:

```text
A_N F(r,h) = (1/N) sum_{0 <= j < N} F(r + j*2^T, h).
```

One may ask whether

```text
lim_{N -> infinity} A_N F(r,h)
```

exists for the relevant transition signatures and weights.

Projection target:

```text
K_T(C,D) = lim_{N -> infinity}
  (1/N) sum_{0 <= j < N} K_N(r+j*2^T,h; D).
```

This is weaker than local constancy and compatible with the observed
high average majorities.

Failure mode:

- block distributions do not become Cauchy;
- the limit depends on the averaging scheme.

### 2.3 Haar average on `Z_2`

For a source cylinder

```text
C = r + 2^T Z_2,
```

define

```text
K_T(C,D) = mu(C)^(-1) integral_C K_2(x,D) dmu(x).
```

This is the cleanest projection statement, but it presupposes that a
measurable 2-adic kernel `K_2` exists.

Failure mode:

- `delta` and the killed set use archimedean data such as bit length and
  order comparison, so they may not define a regular 2-adic kernel.

### 2.4 No canonical high-bit limit

If none of the above is stable, then `FULL_{T,j}` should be treated as a
finite sampling construction rather than an operator approximation.

Consequence:

```text
analytic Phase 10 should stop and the finite-rank fallback should become
the main product.
```

## 3. Current diagnostics

The present diagnostics do not support exact local constancy on the
current `PhaseState` quotient.

They do support the weaker possibility that block distributions may be
reasonably stable:

- at `T = 10`, `j_count = 128`, adjacent-block dominant flip fractions
  are small;
- at `T = 11`, `j_count = 128`, the same pattern persists;
- at `T = 15`, five extra source bits improve exact majority fractions,
  but do not make the signatures locally constant;
- at `T = 15`, increasing the prefix from `j_count = 16` to
  `j_count = 32` decreases exact phase/full fractions while keeping
  average majorities high and adjacent-block dominant flips rare;
- at `T = 16`, the comparable five-bit deep-cylinder short-prefix test
  repeats the favorable-but-not-exact pattern.

Later diagnostics sharpen this:

- direct 2-adic child-cylinder tests do not show decreasing full-label
  oscillation, so naive martingale continuity on `Z_2` is not currently
  supported;
- the two-component split
  `bad = {odd = 3 and v2 in {0,2}}` captures much of the label excess
  but is coupled and must be treated as a block kernel;
- the block-size sequence `B = 8,16,32` at fixed `T = 15` gives
  decreasing mean good/bad block drift
  `0.012046521 -> 0.0095367816 -> 0.0074155295`;
- however, the `B=16`, `j=64` multipair run gives worsening ordinary
  adjacent-pair means
  `0.009535642 -> 0.013903232 -> 0.018206286` over
  `0->16`, `16->32`, `32->48`.

Thus the plausible branch is:

```text
block-valued labelled kernel + explicitly averaged/mixed-norm
high-lift projection,
not exact local constancy and not naive ordinary adjacent-block Cauchy.
```

This branch remains conditional.

## 4. Required Definition for a Refined Kernel

A refined finite kernel should specify:

```text
source cell C = (r mod 2^T, q mod 2^a, h),
destination observable D = destination phase,
edge label ell = delta or a bounded delta class,
killing/terminal symbol.
```

For a finite high-lift prefix `N`, define empirical probabilities:

```text
K_{T,a,N}(C; D, ell)
  = (1/N) * # { 0 <= k < N :
      trace(r + (q + 2^a k) * 2^T, h)
      returns to destination phase D with label ell }.
```

and terminal mass:

```text
K_{T,a,N}(C; terminal)
  = (1/N) * # { 0 <= k < N : trace is terminal }.
```

The current `T = 15` run is the special case:

```text
base T = 10, a = 5, N = 16.
```

## 5. Gate Conditions

Continue analytic branch only if one can show or credibly target:

1. for fixed `T,a`, the chosen averaging scheme for `K_{T,a,N}` is
   Cauchy in the declared weak/mixed norm;
2. as `a` grows, the unresolved phase variation goes to zero or is
   absorbed into a controlled tail;
3. the `delta` label has summable tails or bounded distortion in the
   chosen norm;
4. killing mass has controlled boundary variation;
5. the resulting kernels define bounded operators on a named Banach
   space.

Failing these, the correct output is the finite-rank fallback, not
Hennion/Keller-Liverani.

## 6. Current Provisional Convention

Do not use the phrase "block-Cauchy" without specifying the averaging
scheme.

Allowed finite diagnostic language:

```text
weighted averaged good/bad block drift decreases in the B=8,16,32
single-pair comparison, but later adjacent pairs at B=16 are worse.
```

Disallowed claim:

```text
ordinary adjacent high-bit blocks are Cauchy.
```

The next mathematical target must therefore be one of:

1. a Cesaro/prefix-average limit with error measured in a weak source
   average;
2. a dyadic/Haar cylinder limit with a different diagnostic than
   ordinary adjacent intervals;
3. fallback to finite-rank if neither can be formulated cleanly.

The current finite evidence favors option 1 over ordinary adjacent
blocks:

```text
prefix 16->32 mean drift = 0.004767821,
prefix 32->64 mean drift = 0.0037076395.
```

This is not enough to claim convergence, but it is enough to set the
next formal target as a prefix-average block kernel `K_N`.
