# Phase 10 Orientation and Normalization Note

Date: 2026-05-13

Status: operational convention note.  This note does not change any Lean
or Python code.  Its purpose is to prevent a common Phase-10 failure
mode: proving or interpreting a statement for the transpose of the
intended transfer operator.

## 1. Executive Summary

There are currently two matrix orientations in the project:

1. The phase/high-bit finite transfer layer uses **row-source**
   convention:

   ```text
   K(src,dst) = normalized weight from source state src to destination dst.
   ```

   Python sparse matrices and generated phase Lean matrices store this
   as row `src`, column `dst`.

2. The deterministic K16 Collatz-Wielandt certificate uses **incoming**
   convention:

   ```text
   (P v)[dst] = sum_src K(src,dst) v[src].
   ```

   The generated Lean matrix stores row `dst`, column `src`.

These two conventions are transposes of each other.  For finite matrices
their spectral radii agree, but the meaning of row sums, CW vectors,
Markov mass transport, Ruelle operators, and Lasota-Yorke inequalities
does not agree automatically.

Phase 10 should adopt one canonical data convention:

```text
K(src,dst) = transition weight from src to dst.
```

Then all analytic operators must explicitly say whether they use `K` or
`K^T`.

## 2. Canonical finite kernel

The safest neutral object is not a matrix but a kernel:

```text
K : State x State -> R_{\ge 0},
K(src,dst) = transition weight / source normalization.
```

Terminal/killed mass is represented by missing outgoing mass:

```text
sum_dst K(src,dst) <= 1.
```

This convention matches the empirical and deterministic CSV semantics:

```text
src; dst; count/weight; source_events/source_count.
```

The finite matrix may then be materialized in two ways:

```text
M_row[src,dst] = K(src,dst)
M_in [dst,src] = K(src,dst) = M_row^T[dst,src].
```

The two matrices have the same finite spectral radius, but not the same
row-substochastic or CW-vector interpretation.

## 3. Phase/high-bit layer: row-source convention

### 3.1 Python construction

`scripts/spectral_program/75_critical_symbolic_operator.py` builds a
SciPy sparse matrix by appending:

```text
rows.append(idx[src])
cols.append(idx[dst])
data.append(weight / source_counts[src])
```

and then computes row sums:

```text
row_sums = matrix.sum(axis=1).
```

Thus the Python matrix is:

```text
M_row[src,dst] = K(src,dst).
```

Likewise, `scripts/spectral_program/77_high_bit_tail_bound.py` builds
`CORE`, `TAIL`, and `FULL` with:

```text
rr.append(idx[src])
cc.append(idx[dst])
data.append(weight / source_counts[src])
```

Again:

```text
FULL_row[src,dst] = K(src,dst).
```

### 3.2 CSV export

`scripts/phantom_taxonomy/export_high_bit_tail_edges.py` writes rows of
the form:

```text
src, dst, normalized_num, normalized_den, source_count
```

where

```text
normalized = accumulated_weight(src,dst) / source_count(src).
```

This is also row-source kernel data.

### 3.3 Lean import of high-bit matrices

`scripts/phantom_taxonomy/lean_high_bit_tail.py` groups entries by
source:

```text
by_src[src].append((dst, weight))
```

and generates Lean definitions of the form:

```lean
noncomputable def t10j32HighBitTailCore : TransferMatrix 13 :=
fun i j =>
  if i = src then
    if j = dst then weight else ...
```

It also generates row-substochasticity certificates:

```lean
(sum j, M src j) <= 1.
```

Therefore the generated high-bit Lean matrices are row-source matrices:

```text
M(src,dst) = K(src,dst).
```

### 3.4 Lean CW data for T10J32

`scripts/phantom_taxonomy/lean_t10j32_cw.py` reads the same outgoing
data:

```text
outgoing[src].append((dst, weight))
```

and computes CW rows as:

```text
lhs(src) = sum_dst K(src,dst) v(dst).
```

The generated Lean theorem proves:

```text
(M_row v)(src) <= alpha v(src).
```

Interpretation:

- this is a finite Collatz-Wielandt bound for the row-source matrix
  acting on functions by right-neighbor summation;
- it is not the incoming push-forward mass inequality
  `sum_src K(src,dst) v(src) <= alpha v(dst)`;
- the finite spectral radius conclusion is still valid for `M_row`.

## 4. Deterministic K16 layer: incoming convention

`scripts/phantom_taxonomy/deterministic_residue_transfer.py` exports
edge probabilities as:

```text
probability = count / source_events(src).
```

The diagnostic propagation in the script uses outgoing mass:

```text
w[dst_index] += mass(src) * probability(src,dst).
```

However, the exact CW certificate script
`scripts/phantom_taxonomy/scc_cw_certificate.py` computes the CW
quantity in incoming form:

```text
incoming_sum[dst] += probability(src,dst) * vector[src].
```

It records the orientation explicitly:

```text
incoming form: (P v)[dst] =
  sum_src probability(src,dst) * v[src].
```

The generated Lean file
`lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean` follows
this incoming convention.  Its comment states:

```text
Matrix rows are destination states and columns are source states,
matching `(P v)[dst] = sum_src probability(src,dst) * v[src]`.
```

Therefore the K16 deterministic Lean matrix is:

```text
M_in[dst,src] = K(src,dst) = M_row^T[dst,src].
```

The theorem proves a CW inequality for the incoming/push-forward matrix:

```text
(M_in v)(dst) <= alpha v(dst).
```

## 5. Consequences for Phase 10

### 5.1 Finite spectral radius

For finite matrices:

```text
r(M_row) = r(M_in).
```

Thus a certified spectral-radius upper bound survives transposition.
This is why the existing finite certificates remain meaningful.

### 5.2 Row-substochasticity

Row-substochasticity is orientation-sensitive.

If

```text
M_row[src,dst] = K(src,dst),
```

then

```text
sum_dst M_row[src,dst] <= 1
```

means killed outgoing mass is at most one for each source.

If

```text
M_in[dst,src] = K(src,dst),
```

then row sums are incoming sums:

```text
sum_src M_in[dst,src],
```

which need not be bounded by one.  Incoming row sums are not the same as
source-wise substochasticity.

Therefore `RowSubstochastic` should be used only for row-source matrices
unless a theorem explicitly states the incoming interpretation.

### 5.3 CW vectors

A CW vector for `M_row` proves:

```text
sum_dst K(src,dst) v(dst) <= alpha v(src).
```

This is a function-side, Koopman-like inequality.

A CW vector for `M_in` proves:

```text
sum_src K(src,dst) v(src) <= alpha v(dst).
```

This is a measure-side, push-forward/incoming inequality.

Both imply the same finite spectral-radius upper bound when formalized
for the corresponding finite matrix, but they are not the same
Lyapunov/drift statement.

### 5.4 Transfer vs push-forward vs Ruelle

For an infinite Phase-10 operator, the project must choose explicitly:

1. Markov push-forward on measures:

   ```text
   (P_* mu)(B) = integral K(x,B) dmu(x).
   ```

   Matrix representation on column mass vectors is incoming:

   ```text
   M_in[dst,src] = K(src,dst).
   ```

2. Koopman / forward operator on functions:

   ```text
   (U f)(src) = sum_dst K(src,dst) f(dst).
   ```

   Matrix representation is row-source:

   ```text
   M_row[src,dst] = K(src,dst).
   ```

3. Ruelle / transfer preimage operator:

   ```text
   (L f)(x) = sum_{y : tau(y)=x} w(y) f(y).
   ```

   For deterministic branches this is naturally incoming/preimage
   oriented, closer to `M_in`.

The spectral radius of finite transposes is the same, but essential
spectral radius, compactness mechanisms, Lasota-Yorke constants, weak
norms, and projection errors must be formulated for one chosen operator.

## 6. Recommended Phase-10 convention

Use this convention in all future notes:

```text
K(src,dst) = killed weighted transition kernel.
```

Then define:

```text
U_K f(src)   = sum_dst K(src,dst) f(dst)
L_K f(dst)   = sum_src K(src,dst) f(src)
P_K^* mu(dst)= sum_src K(src,dst) mu(src)
```

where `L_K` and `P_K^*` have the same finite incoming matrix
representation but act on different spaces/duals depending on the
chosen Banach framework.

Recommended naming:

- `K` for the abstract transition kernel;
- `M_row` for row-source matrix materialization;
- `M_in` for incoming matrix materialization;
- `U_K` for the function-side forward/Koopman operator;
- `L_K` for the Ruelle/preimage or incoming transfer operator;
- `P_K^*` for push-forward on measures.

## 7. Required cleanups before 10.D

Before writing a formal Phase-10 operator definition, resolve:

1. For `FULL_T` and `FULL_{T,j}`, decide whether the analytic object is
   `U_K`, `L_K`, or `P_K^*`.
2. Add generator metadata saying explicitly:

   ```text
   orientation = row-source
   ```

   or

   ```text
   orientation = incoming
   ```

3. Decide whether future generated CW certificates should all use one
   orientation.  The least confusing choice for analytic transfer
   operators is likely incoming/Ruelle, but the least invasive choice for
   existing high-bit phase code is row-source.
4. If both orientations are retained, generate a small bridge note or
   theorem:

   ```text
   M_in = M_row^T
   r(M_in) = r(M_row)
   ```

   for finite matrices used in certificates.
5. Do not interpret `RowSubstochastic` for incoming matrices as a Markov
   outgoing-mass statement.

## 8. Immediate recommendation

For Phase 10.B and 10.D, define the infinite object first as a kernel:

```text
K(x,dy)
```

or, in discrete notation:

```text
K(src,dst).
```

Only after that should the project choose the operator:

```text
U_K, L_K, or P_K^*.
```

This avoids baking a transpose into the mathematical model before the
Banach space is chosen.
