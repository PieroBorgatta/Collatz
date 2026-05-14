# Phase 10 Candidate Operator Definition

Date: 2026-05-13

Status: candidate definition note.  This is not a theorem and not a
claim that the finite `FULL_T` / `FULL_{T,j}` matrices are projections of
the operator below.  The purpose is to isolate the exact mathematical
object that would have to pass Gate 10.B.

Related notes:

- `notes/phase10_operator_gate.md`
- `notes/phase10_orientation.md`
- `notes/phase10_cylinder_stability_plan.md`

## 1. Executive Summary

The cleanest way to avoid premature analytic claims is to define the
candidate first as a killed weighted transition kernel:

```text
K(src,dst) = killed first-return transition weight from src to dst.
```

There are two levels:

1. a positive-integer first-return kernel, which is directly faithful to
   the current scripts;
2. a 2-adic/profinite extension, which exists only if local constancy or
   controlled cylinder convergence can be proved.

The current finite matrices are exact finite objects, but they are not
yet proved to be projections of the 2-adic candidate.  That statement is
precisely the remaining Gate 10.B problem.

## 2. Raw integer first-return data

Fix a monitored phantom target record.  In the current critical-symbolic
scripts this is:

```text
target_key = (12, 2, 1).
```

Let the target congruence class be represented by:

```text
n(t) = residue + t * modulus,
```

where `residue` and `modulus` are obtained from the target rational
phantom representative.  In the script this is
`make_start_from_residue(residue, modulus, t)`.

For now, the faithful domain is:

```text
X_N = N_0 x H,
H = Z / 2^m_hit Z.
```

A raw state is:

```text
x = (t,h).
```

The phase quotient used by the finite matrices is:

```text
pi_V,m(t,h) =
  (min(nu_2(t), V), odd_part(t) mod 2^m_odd, h mod 2^m_hit).
```

For the generated high-bit file, `m_odd = 2`, `m_hit = 2`, and the
observed valuation cap is `V = 13`.

## 3. First-return/killing rule

Given `x = (t,h)`, define:

```text
n0 = n(t).
```

Trace the odd Syracuse map from `n0`.  The current scripts terminate in
three possible ways:

1. killed/drop:

   ```text
   current_n < n0.
   ```

2. first return to the monitored target after a distinct monitored hit:

   ```text
   target_key is reached again.
   ```

3. unresolved/budget:

   ```text
   max_steps is exhausted.
   ```

Only case 2 produces a nonterminal transition.  Cases 1 and 3 are killed
or terminal for operator purposes.

When case 2 occurs, the next local parameter is:

```text
t' = (current_n - residue) / modulus.
```

The raw transition is:

```text
tau_N(t,h) = (t', h+1 mod 2^m_hit).
```

The current weight exponent is:

```text
delta(t,h) = bit_length(t') - bit_length(t).
```

The current high-bit script uses weight

```text
w(t,h) = 2^{-delta(t,h)}.
```

The older critical-symbolic script allows

```text
w_s(t,h) = 2^{-s delta(t,h)}.
```

Important caveat: `bit_length` and `current_n < n0` are archimedean
features.  They do not automatically extend continuously to `Z_2`.

## 4. Positive-integer kernel

The direct countable-state kernel is:

```text
K_N((t,h),(t',h')) =
  w_s(t,h)   if tau_N(t,h) = (t',h'),
  0          otherwise.
```

with killed mass:

```text
kappa(t,h) = 1 - sum_{t',h'} K_N((t,h),(t',h')).
```

This object is faithful to the scripts, but it lives on a countable
archimedean state space.  It is not yet the desired 2-adic transfer
operator.

Possible operators associated to `K_N`:

```text
U_N f(t,h) =
  sum_{t',h'} K_N((t,h),(t',h')) f(t',h').
```

and

```text
L_N f(t',h') =
  sum_{t,h} K_N((t,h),(t',h')) f(t,h).
```

Here `U_N` is row-source/Koopman-like and `L_N` is incoming/Ruelle-like.
They are transposes on finite truncations, but not the same operator on
infinite Banach spaces.

## 5. 2-adic candidate

The desired analytic candidate would live on:

```text
X_2 = Z_2 x H.
```

The formal target is a partially defined killed first-return map:

```text
tau_2 : D subset X_2 -> X_2
```

and a weight:

```text
w_s : D -> R_{\ge 0}.
```

Then the push-forward kernel would be:

```text
K_2(x,B) = 1_D(x) w_s(x) 1_B(tau_2(x)).
```

For a finite partition `P`, the projected row-source matrix would be:

```text
K_P(C,D) =
  mu(C)^(-1) integral_C K_2(x,D) dmu(x).
```

For the phase partition, cells are inverse images of

```text
pi_V,m(t,h) =
  (min(nu_2(t), V), odd_part(t) mod 2^m_odd, h mod 2^m_hit).
```

under the map `Z_2 x H -> PhaseState V`.

Gate 10.B asks whether the generated finite matrices are exactly these
`K_P`, controlled approximations of them, or neither.

## 6. Required extension conditions

The 2-adic candidate is legitimate only if the following conditions can
be proved or replaced by a weaker precise substitute.

### 6.1 Cylinder stability of return signatures

For each sufficiently fine cylinder

```text
C = {t in Z_2 : t == a mod 2^T} x {h},
```

the terminal/return status should either be constant on positive integer
representatives in `C`, or converge in a controlled averaging sense.

Failure mode:

- if return signatures fluctuate forever with high bits and no limiting
  law, then `FULL_{T,j}` is not a projection of a canonical `K_2`.

### 6.2 Cylinder stability of destination phase

For the finite phase quotient, the value

```text
pi_V,m(tau_N(t,h))
```

should be constant or have a controlled limiting distribution on source
cylinders.

Failure mode:

- high-bit dependence may survive every finite depth in a way that is not
  captured by a compact/tail perturbation.

Current diagnostic evidence:

- at `T = 10`, `j_count = 64`, there are `60` bulk groups with stable
  return status and destination-phase majority at most `0.5`;
- at `T = 10`, `j_count = 128`, there are still `56` bulk groups with
  stable return status and destination-phase majority at most `0.5`;
- at `T = 11`, `j_count = 128`, the corresponding count is `84`;
- with a strict minimum average bucket size of `4`, the best simple
  global coordinate for destination phase is again `j mod 32`, with
  mean groupwise purity about `0.972656` at `T = 10` and `0.97061` at
  `T = 11`;
- this is not a projection theorem, because the corresponding full
  weighted signature has mean groupwise purity only about `0.794643` at
  `T = 10` and `0.797619` at `T = 11`;
- the next required step is to define a refined symbolic state and test
  whether it improves full-signature stability, not merely phase
  stability.

### 6.3 Weight regularity

The exponent

```text
delta(t,h) = bit_length(t') - bit_length(t)
```

must be replaced by, or shown compatible with, a cylinder-measurable
weight on `Z_2`.

Failure mode:

- `bit_length` is not a 2-adic continuous observable.  If no regularized
  or symbolic substitute exists, a 2-adic Lasota-Yorke framework is
  unlikely.

### 6.4 Killing regularity

The killed set

```text
{(t,h) : orbit drops below n(t) before first return}
```

must be measurable and preferably clopen up to controlled tails.

Failure mode:

- the order comparison `current_n < n0` is archimedean.  If its boundary
  is too irregular in `Z_2`, BV/Lipschitz estimates may fail.

### 6.5 Projection identity or error bound

For finite partitions `P_T`, one needs either:

```text
M_T = E_T K_2 I_T
```

exactly, or

```text
||M_T - E_T K_2 I_T||_{strong -> weak} <= epsilon_T,
epsilon_T -> 0.
```

Failure mode:

- if the finite matrices are only finite sampling artifacts, then
  Keller-Liverani is not applicable.

## 7. Relation to current finite matrices

### 7.1 `full_T`

The finite `full_T` matrix from `75_critical_symbolic_operator.py`
corresponds to:

```text
uniform enumeration of 0 <= t < 2^T,
h in H,
then quotient by pi_V,m.
```

It is exact for that finite enumeration.  It is not yet known to equal a
Haar conditional expectation of a 2-adic operator.

### 7.2 `FULL_{T,j}`

The high-bit matrix from `77_high_bit_tail_bound.py` corresponds to:

```text
t = r + j * 2^T
```

for finitely many `j`, followed by majority CORE and minority TAIL
classification.

This is not a linear projection.  It can become an analytic object only
after one defines what the `j -> infinity` limit means:

- Haar average over the high-bit tail;
- Cesaro average over lift prefixes;
- another invariant/tail measure;
- or no canonical limit.

### 7.3 K16 deterministic residue-cell matrix

The K16 deterministic matrix corresponds more naturally to a finite
countable-state truncation/lumping:

```text
raw SCC source nodes -> macro-state (K,b).
```

It is already a clean finite kernel.  Its infinite extension would be a
countable episode graph operator, not automatically the same as the
phase `FULL_T` operator.

## 8. Candidate Banach targets

The positive-integer kernel `K_N` suggests weighted sequence spaces:

```text
ell_infty(W), ell_1(W), or drift/minorization frameworks.
```

The 2-adic kernel `K_2`, if it exists, suggests:

```text
Lip(Z_2 x H), BV on residue cylinders, or symbolic Holder spaces.
```

The countable symbolic model suggests:

```text
weighted Holder spaces over a countable Markov shift.
```

No Banach target should be selected before conditions 6.1-6.5 are tested
against the actual first-return data.

## 9. Minimal mathematical statement for Gate 10.B

A positive 10.B result should state something like:

> There exists a measurable killed weighted kernel `K_2` on `Z_2 x H`
> and a sequence of finite partitions `P_T` such that the generated
> finite matrices are `E_T K_2 I_T`, or converge to them in an explicitly
> stated mixed norm.

A negative 10.B result should state:

> The generated `FULL_{T,j}` matrices cannot currently be identified with
> projections or controlled approximants of a canonical infinite kernel.
> Therefore Phase 10 should switch to the finite-rank fallback.

Current status:

```text
unknown.
```

## 10. Next checks

1. For fixed small residues `(r,h)`, test whether the return signature
   stabilizes over lifts `t = r + j * 2^T` as `j` grows.
2. Separate instability of destination phase from instability of
   `delta`.
3. Test whether terminal/drop status is cylinder-stable or has a stable
   tail frequency.
4. Record counterexamples as first-class data; they are not failures of
   the project, they are information about the correct branch.
5. If stability fails, try the countable episode graph model before
   abandoning the analytic branch entirely.

The concrete diagnostic design for these checks is recorded in
`notes/phase10_cylinder_stability_plan.md`.
