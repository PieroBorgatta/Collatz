# Phase 10 Operator Choice

Date: 2026-05-14

Status: provisional operator-choice note.  This fixes the next working
convention for Gate 10.B/10.C.  It is not a theorem and does not assert
that the finite `full_T` / `FULL_{T,j}` matrices are projections of an
infinite operator.

## 1. Decision

Use the killed labelled kernel as the primary mathematical object:

```text
K(src,dst) >= 0.
```

Use the row-source function-side operator as the primary analytic
operator:

```text
(U_K f)(src) = sum_dst K(src,dst) f(dst).
```

Keep the push-forward on measures as the dual/mass interpretation:

```text
(P_K^* mu)(dst) = sum_src K(src,dst) mu(src).
```

Do not use the Ruelle/preimage operator as the primary Phase-10 object
yet:

```text
(L_K f)(dst) = sum_src K(src,dst) f(src).
```

`L_K` may be studied later, but only after a genuine preimage/branch
structure is constructed.

## 2. Why This Is the Correct Next Step

The generated phase/high-bit matrices are row-source:

```text
M_row[src,dst] = K(src,dst).
```

Their natural action on functions is:

```text
(M_row v)(src) = sum_dst K(src,dst) v(dst).
```

This is exactly the finite version of `U_K`.  Therefore `U_K` minimizes
orientation mismatch with the existing `FULL` / high-bit layer.

The push-forward `P_K^*` is still essential, because killing and lost
mass are most naturally interpreted on measures:

```text
mass after one step = P_K^* mu(X).
```

But using `P_K^*` as the primary object would push the analytic program
toward signed-measure Banach spaces immediately.  That may be possible,
but it is a harder starting point.

The Ruelle/preimage operator `L_K` is the most tempting language from
thermodynamic formalism, but it is currently the riskiest false analogy:

- the finite matrices were not generated as preimage sums;
- inverse branches are not yet identified;
- branch count/summability/BIP/positive recurrence are all open;
- `L_K` may be the transpose of what the generated row-source matrices
  actually approximate.

## 3. Working Phase Space

The candidate phase space remains:

```text
X = Z_2 x H,
```

where `H` is a finite hit/phase component, for example:

```text
H = Z / 4Z
```

or a modest finite refinement if required by the data.

Finite source cells are 2-adic cylinders:

```text
C(r,a,h) = {t in Z_2 : t == r mod 2^a} x {h}.
```

The finite phase quotient is:

```text
pi(t,h) = (min(v2(t), V), odd(t) mod 4, h mod 4),
```

possibly refined by extra high-bit coordinates.

## 4. Killed Labelled Kernel

Let `D subset X` be the nonterminal domain where the monitored
first-return is defined.  Let:

```text
tau : D -> X
delta : D -> Z
w_s(x) = 2^{-s delta(x)}.
```

The formal deterministic killed kernel is:

```text
K_s(x,B) = 1_D(x) w_s(x) 1_B(tau(x)).
```

On a finite partition `P = {C_i}`, the row-source projected kernel would
be:

```text
K_P(i,j)
  = m(C_i)^(-1) integral_{C_i cap D cap tau^{-1}(C_j)}
      2^{-s delta(x)} dm(x).
```

This is the object against which `FULL_{T,j}` should be compared if
Gate 10.B is to succeed.

Important status:

```text
No equality K_P = FULL_{T,j} has been proved.
No convergence FULL_{T,j} -> K_P or K has been proved.
```

## 5. Primary Operator: `U_s`

Define:

```text
(U_s f)(x)
  = 1_D(x) 2^{-s delta(x)} f(tau(x)).
```

Finite partition version:

```text
(U_P v)(i) = sum_j K_P(i,j) v(j).
```

Compatibility:

- this matches the row-source `FULL` orientation;
- it matches the function-side finite CW inequality;
- it avoids prematurely invoking preimage thermodynamic formalism.

Main analytic risk:

```text
U_s is composition/Koopman-like, so it may not regularize.
```

Therefore a classical Lasota-Yorke mechanism is not automatic.  Any
strong norm must be designed around cylinder-depth loss, tail control,
or martingale variation.  This is a real risk, not a technicality.

## 6. Dual Mass Operator: `P_s^*`

The dual push-forward is:

```text
(P_s^* mu)(B)
  = integral_{D cap tau^{-1}(B)}
      2^{-s delta(x)} dmu(x).
```

Finite version:

```text
(P_P^* mu)(j) = sum_i K_P(i,j) mu(i).
```

Use `P_s^*` for:

- killed mass accounting;
- tail-mass diagnostics;
- possible drift/tightness conditions;
- interpreting `DeltaTail_global` and terminal loss.

But do not silently switch the spectral problem from `U_s` to `P_s^*`.
For finite matrices the spectra of transposes agree; in infinite
Banach spaces they may not.

## 7. Secondary Operator: `L_s`

The preimage/Ruelle candidate would be:

```text
(L_s f)(x)
  = sum_{y in D : tau(y) = x}
      2^{-s delta(y)} f(y).
```

This should remain secondary until the project has:

1. a countable preimage/branch description;
2. a summable potential;
3. a distortion or variation estimate;
4. recurrence/BIP or a substitute if using Sarig-style machinery;
5. a proof that finite matrices approximate this operator or its
   transpose.

Current verdict:

```text
Do not build Phase 10 around L_s yet.
```

## 8. Candidate Norm Direction

For `U_s`, the least artificial current Banach direction is:

```text
B_s = bounded functions with martingale/cylinder variation on Z_2 x H,
B_w = L^1(m) or cylinder-distribution weak norm.
```

The strong seminorm should measure how much `f` changes under deeper
2-adic cylinder refinement.  The weak norm should allow finite
distributional errors such as:

```text
A_phase_block,
A_label_bounded,
DeltaTail_global,
DeltaTail_local with exceptional-mass control,
BoundaryError.
```

This is not yet a Banach theorem.  It is the next object to formulate
precisely.

## 9. Gate 10.B Restatement Under This Choice

With `U_s` primary, Gate 10.B becomes:

```text
Can the generated row-source matrices FULL_{T,j} be interpreted as
finite approximants of U_s on cylinder/phase partitions?
```

More explicitly, can one define maps:

```text
E_N : B_s -> finite observables,
I_N : finite observables -> B_s,
```

such that:

```text
|| U_s - I_N FULL_N E_N ||_{B_s -> B_w} -> 0
```

or at least:

```text
|| E_N U_s I_N - FULL_N || -> 0
```

in a declared finite norm?

Current answer:

```text
Unknown.
```

## 10. Immediate Next Work

Completed immediately after this operator choice:

1. `notes/phase10_mixed_norm_candidate.md` now uses `U_s` as the
   primary operator;
2. the finite maps `E_n` and `I_n` are defined as conditional
   expectation onto cylinder cells and inclusion of cell-constant
   observables;
3. `notes/phase10_error_decomposition.md` now separates the ideal
   projected kernel `K_n = E_n U_s I_n` from the generated empirical
   `FULL_N`.
4. the first finite row-TV bridge is stated: uniform row-TV controls
   `ell_infty -> ell_infty`, while average row-TV controls
   `ell_infty -> L1(omega)`.

Remaining next work:

1. decide whether the source averaging weight `omega` in the finite
   row-TV bridge is exactly the projected Haar/counting measure or needs
   boundary/source-partition corrections;
2. prove or reject the bridge from script-`99` row-TV proxies to the
   chosen `B_s -> L1(m)` norm;
3. formulate a first conditional proposition for:

```text
|| U_s - I_N FULL_N E_N ||_{B_s -> B_w}.
```

4. Ask any collaborator the narrowed question:

```text
Is a Koopman-side killed weighted first-return operator on Z_2 x H,
with martingale/cylinder variation norm, a viable object for
Hennion/Keller-Liverani style analysis?
```

After scripts `103`--`105`, the operator-choice note should be refined
as follows.  The next `U_s` model should be block-valued:

```text
X = X_G disjoint_union X_B,
U_s =
[[U_GG, U_GB],
 [U_BG, U_BB]].
```

The provisional bad component is:

```text
X_B = {odd = 3 and v2 in {0,2}},
```

with the warning that this is a finite-data-driven split, not a
canonical dynamical decomposition.

The high-bit limit convention should be prefix/Cesaro first.  The
operator approximants are therefore not ordinary adjacent blocks but:

```text
K_N(src,tau)
  = (1/N) sum_{0 <= k < N}
      1_{return} 1_{dest in tau} 2^{-delta},
tau in {G,B},
```

with killed terminal mass recorded separately.  The immediate
approximation target is:

```text
||K_{2N} - K_N||_{ell_infty(component) -> L1(omega_N)} -> 0,
```

then, only after a Banach pair is fixed:

```text
||K_{2N} - K_N||_{B_s -> B_w} -> 0.
```

This is still a weak mixed-norm target.  It is not a spectral-radius
statement, and it does not identify `FULL_{T,j}` as a projection of an
infinite operator.

## 11. Decision Summary

Current recommended convention:

```text
kernel first:       K(src,dst)
primary operator:   U_s
dual mass operator: P_s^*
secondary only:     L_s
```

This is the most conservative choice because it follows the generated
finite data instead of importing thermodynamic-formalism language too
early.
